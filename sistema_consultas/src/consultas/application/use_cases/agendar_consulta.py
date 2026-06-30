
from __future__ import annotations
from datetime import datetime, timezone
from consultas.application.dtos.consulta_dtos import AgendarConsultaInputDTO
from consultas.application.ports.out.event_publisher import DomainEventPublisher
from consultas.application.ports.out.gateways import MedicoRegistroProfissionalGateway
from consultas.application.ports.out.repositories import (
    ConsultaRepository,
    MedicoRepository,
    PacienteRepository,
    TelefoneRepository,
)
from consultas.domain.entities.consulta import Consulta
from consultas.domain.entities.paciente import Paciente
from consultas.domain.entities.telefone import Telefone
from consultas.domain.enums.sexo import Sexo
from consultas.domain.enums.tipo_telefone import TipoTelefone
from consultas.domain.events import ConsultaAgendadaEvent
from consultas.domain.exceptions import BusinessRuleViolation, CrmInvalidoError, EntityNotFoundError
from consultas.domain.factories.paciente_factory import PacienteFactory
from consultas.domain.strategies.atendimento import politica_para
from consultas.domain.value_objects.identificadores import (
    ConsultaId, EnderecoId, MedicoId, PacienteId, PlanoSaudeId,
)

class AgendarConsultaUseCase:
    def __init__(
        self,
        consultas: ConsultaRepository,
        pacientes: PacienteRepository,
        medicos: MedicoRepository,
        telefones: TelefoneRepository,
        crm_gateway: MedicoRegistroProfissionalGateway,
        eventos: DomainEventPublisher,
    ) -> None:
        self._consultas = consultas
        self._pacientes = pacientes
        self._medicos = medicos
        self._telefones = telefones
        self._crm_gateway = crm_gateway
        self._eventos = eventos

    def executar(self, entrada: AgendarConsultaInputDTO) -> int:
        medico_id = MedicoId(entrada.medico_id)
        medico = self._medicos.obter_por_id(medico_id)
        if medico is None:
            raise EntityNotFoundError("Médico não encontrado.")
        if not self._crm_gateway.validar_crm(medico):
            raise CrmInvalidoError(f"CRM inválido: {medico.crm}")

        paciente: Paciente
        if entrada.novo_paciente:
            if entrada.data_nascimento is None or entrada.sexo is None or entrada.endereco_id is None:
                raise BusinessRuleViolation("Dados do paciente novo são obrigatórios.")
            paciente = PacienteFactory.criar_novo(
                id=self._pacientes.proximo_id(),
                nome_crianca=entrada.nome_crianca or "",
                nome_responsavel=entrada.nome_responsavel or "",
                data_nascimento=entrada.data_nascimento,
                sexo=Sexo(entrada.sexo),
                endereco_id=EnderecoId(entrada.endereco_id),
                telefone_informado=bool(entrada.telefone_numero),
                plano_saude_id=PlanoSaudeId(entrada.plano_saude_id) if entrada.plano_saude_id else None,
            )
            self._pacientes.salvar(paciente)
            if entrada.telefone_numero:
                self._telefones.salvar(Telefone(
                    id=self._telefones.proximo_id(), numero=entrada.telefone_numero,
                    tipo=TipoTelefone.CELULAR, paciente_id=paciente.id,
                ))
            paciente_id = paciente.id
        else:
            if entrada.paciente_id is None:
                raise BusinessRuleViolation("paciente_id é obrigatório para paciente existente.")
            paciente_id = PacienteId(entrada.paciente_id)
            encontrado = self._pacientes.obter_por_id(paciente_id)
            if encontrado is None:
                raise EntityNotFoundError("Paciente não encontrado.")
            paciente = encontrado
        politica_para(entrada.tipo_atendimento).validar_agendamento(paciente)
        consulta = Consulta(
            id=self._consultas.proximo_id(),
            paciente_id=paciente_id,
            medico_id=medico_id,
            data_hora=entrada.data_hora,
            novo_paciente=entrada.novo_paciente,
            tipo_atendimento=entrada.tipo_atendimento,
        )
        consulta_salva = self._consultas.salvar(consulta)
        self._eventos.publicar(
            ConsultaAgendadaEvent(
                ocorrido_em=datetime.now(timezone.utc),
                consulta_id=consulta_salva.id,
                paciente_id=paciente_id,
            )
        )
        return int(consulta_salva.id)
