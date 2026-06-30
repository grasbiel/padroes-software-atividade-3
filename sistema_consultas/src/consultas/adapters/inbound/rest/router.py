from __future__ import annotations

from dataclasses import asdict
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from consultas.adapters.inbound.rest.dependencies import (
    build_repositories,
    get_crm_gateway,
    get_db,
    get_event_publisher,
)
from consultas.adapters.inbound.rest.schemas import (
    AgendarConsultaRequest,
    ConsultaDiaResponse,
    ContextoProntuarioResponse,
    HistoricoMedidaResponse,
    ItemReceituarioResponse,
    ReceituarioResponse,
    RegistrarProntuarioRequest,
)
from consultas.application.dtos.consulta_dtos import (
    AgendarConsultaInputDTO,
    PrescricaoInputDTO,
    RegistrarProntuarioInputDTO,
)
from consultas.adapters.outbound.notifications.event_bus import InProcessEventPublisher
from consultas.application.ports.out.gateways import MedicoRegistroProfissionalGateway
from consultas.application.use_cases.agendar_consulta import AgendarConsultaUseCase
from consultas.application.use_cases.consultar_historico_prontuario import ConsultarHistoricoProntuarioUseCase
from consultas.application.use_cases.gerar_receituario import GerarReceituarioUseCase
from consultas.application.use_cases.listar_consultas_do_dia import ListarConsultasDoDiaUseCase
from consultas.application.use_cases.registrar_prontuario import RegistrarProntuarioUseCase
from consultas.domain.enums.tipo_atendimento import TipoAtendimento
from consultas.domain.exceptions import BusinessRuleViolation, DomainError, EntityNotFoundError
from consultas.domain.value_objects.identificadores import ConsultaId

router = APIRouter(prefix="/consultas", tags=["consultas"])


def _http_error(exc: DomainError) -> HTTPException:
    if isinstance(exc, EntityNotFoundError):
        return HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, BusinessRuleViolation):
        return HTTPException(status_code=422, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))


@router.get("/dia", response_model=list[ConsultaDiaResponse])
def listar_consultas_do_dia(
    dia: date | None = None, session: Session = Depends(get_db)
) -> list[ConsultaDiaResponse]:
    repos = build_repositories(session)
    use_case = ListarConsultasDoDiaUseCase(repos.consultas, repos.pacientes)
    alvo = dia or date.today()
    return [ConsultaDiaResponse(**asdict(item)) for item in use_case.executar(alvo)]


@router.get("/{consulta_id}/contexto-prontuario", response_model=ContextoProntuarioResponse)
def contexto_prontuario(consulta_id: int, session: Session = Depends(get_db)) -> ContextoProntuarioResponse:
    repos = build_repositories(session)
    use_case = ConsultarHistoricoProntuarioUseCase(
        repos.consultas,
        repos.pacientes,
        repos.prontuarios,
        repos.medicamentos,
        repos.exames,
    )
    try:
        dto = use_case.executar(ConsultaId(consulta_id))
    except DomainError as exc:
        raise _http_error(exc) from exc
    return ContextoProntuarioResponse(
        consulta_id=dto.consulta_id,
        paciente_id=dto.paciente_id,
        nome_paciente=dto.nome_paciente,
        historico=[
            HistoricoMedidaResponse(data_consulta=h.data_consulta, peso=h.peso, altura=h.altura)
            for h in dto.historico
        ],
        medicamentos_disponiveis=list(dto.medicamentos_disponiveis),
        exames_disponiveis=list(dto.exames_disponiveis),
    )


@router.post("/{consulta_id}/prontuario")
def registrar_prontuario(
    consulta_id: int,
    body: RegistrarProntuarioRequest,
    session: Session = Depends(get_db),
    eventos: InProcessEventPublisher = Depends(get_event_publisher),
) -> dict[str, int]:
    repos = build_repositories(session)
    use_case = RegistrarProntuarioUseCase(
        repos.consultas,
        repos.pacientes,
        repos.prontuarios,
        repos.medicamentos,
        repos.exames,
        repos.prescricoes,
        eventos,
    )
    entrada = RegistrarProntuarioInputDTO(
        consulta_id=consulta_id,
        peso=body.peso,
        altura=body.altura,
        descricao_sintomas=body.descricao_sintomas,
        observacao_clinica=body.observacao_clinica,
        exame_ids=body.exame_ids,
        prescricoes=[PrescricaoInputDTO(**p.model_dump()) for p in body.prescricoes],
    )
    try:
        prontuario_id = use_case.executar(entrada)
    except DomainError as exc:
        raise _http_error(exc) from exc
    return {"prontuario_id": prontuario_id}


@router.get("/{consulta_id}/receituario", response_model=ReceituarioResponse)
def gerar_receituario(consulta_id: int, session: Session = Depends(get_db)) -> ReceituarioResponse:
    repos = build_repositories(session)
    use_case = GerarReceituarioUseCase(
        repos.consultas,
        repos.prontuarios,
        repos.prescricoes,
        repos.medicamentos,
        repos.medicos,
    )
    try:
        dto = use_case.executar(ConsultaId(consulta_id))
    except DomainError as exc:
        raise _http_error(exc) from exc
    return ReceituarioResponse(
        consulta_id=dto.consulta_id,
        nome_medico=dto.nome_medico,
        crm=dto.crm,
        itens=[
            ItemReceituarioResponse(
                medicamento=i.medicamento,
                dosagem=i.dosagem,
                administracao=i.administracao,
                tempo_de_uso=i.tempo_de_uso,
            )
            for i in dto.itens
        ],
    )


@router.post("")
def agendar_consulta(
    body: AgendarConsultaRequest,
    session: Session = Depends(get_db),
    eventos: InProcessEventPublisher = Depends(get_event_publisher),
    crm_gateway: MedicoRegistroProfissionalGateway = Depends(get_crm_gateway),
) -> dict[str, int]:
    repos = build_repositories(session)
    use_case = AgendarConsultaUseCase(
        repos.consultas,
        repos.pacientes,
        repos.medicos,
        repos.telefones,
        crm_gateway,
        eventos,
    )
    entrada = AgendarConsultaInputDTO(
        paciente_id=body.paciente_id,
        medico_id=body.medico_id,
        data_hora=body.data_hora,
        tipo_atendimento=TipoAtendimento(body.tipo_atendimento),
        novo_paciente=body.novo_paciente,
        nome_crianca=body.nome_crianca,
        nome_responsavel=body.nome_responsavel,
        data_nascimento=body.data_nascimento,
        sexo=body.sexo,
        endereco_id=body.endereco_id,
        telefone_numero=body.telefone_numero,
        plano_saude_id=body.plano_saude_id,
    )
    try:
        consulta_id = use_case.executar(entrada)
    except DomainError as exc:
        raise _http_error(exc) from exc
    return {"consulta_id": consulta_id}
