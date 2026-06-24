
from __future__ import annotations
from datetime import datetime, timezone
from consultas.application.dtos.consulta_dtos import RegistrarProntuarioInputDTO
from consultas.application.ports.out.event_publisher import DomainEventPublisher
from consultas.application.ports.out.repositories import (
    ConsultaRepository, ExameRepository, MedicamentoRepository, PacienteRepository,
    PrescricaoRepository, ProntuarioRepository,
)
from consultas.domain.builders.prontuario_builder import ProntuarioBuilder
from consultas.domain.entities.prescricao import Prescricao
from consultas.domain.events import ProntuarioRegistradoEvent
from consultas.domain.exceptions import (
    EntityNotFoundError, ExameNaoCadastradoError, MedicamentoNaoCadastradoError, ProntuarioJaExisteError,
)
from consultas.domain.value_objects.identificadores import ConsultaId, ExameId, MedicamentoId, PrescricaoId

class RegistrarProntuarioUseCase:
    def __init__(
        self, consultas: ConsultaRepository, pacientes: PacienteRepository, prontuarios: ProntuarioRepository,
        medicamentos: MedicamentoRepository, exames: ExameRepository, prescricoes: PrescricaoRepository,
        eventos: DomainEventPublisher,
    ) -> None:
        self._consultas = consultas
        self._pacientes = pacientes
        self._prontuarios = prontuarios
        self._medicamentos = medicamentos
        self._exames = exames
        self._prescricoes = prescricoes
        self._eventos = eventos

    def executar(self, entrada: RegistrarProntuarioInputDTO) -> int:
        consulta_id = ConsultaId(entrada.consulta_id)
        consulta = self._consultas.obter_por_id(consulta_id)
        if consulta is None:
            raise EntityNotFoundError("Consulta não encontrada.")
        if self._prontuarios.obter_por_consulta(consulta_id) is not None:
            raise ProntuarioJaExisteError("Cada consulta possui exatamente um prontuário.")
        paciente = self._pacientes.obter_por_id(consulta.paciente_id)
        if paciente is None:
            raise EntityNotFoundError("Paciente não encontrado.")
        for eid in entrada.exame_ids:
            if self._exames.obter_por_id(ExameId(eid)) is None:
                raise ExameNaoCadastradoError(f"Exame {eid} não cadastrado.")
        for item in entrada.prescricoes:
            if self._medicamentos.obter_por_id(MedicamentoId(item.medicamento_id)) is None:
                raise MedicamentoNaoCadastradoError(f"Medicamento {item.medicamento_id} não cadastrado.")
        builder = ProntuarioBuilder(self._prontuarios.proximo_id(), consulta_id).com_medidas(
            entrada.peso, entrada.altura
        ).com_sintomas(entrada.descricao_sintomas).com_observacao(entrada.observacao_clinica)
        for eid in entrada.exame_ids:
            builder = builder.adicionar_exame(ExameId(eid))
        prontuario = builder.build()
        self._prontuarios.salvar(prontuario)
        prox = int(self._prescricoes.proximo_id())
        prescricoes = [
            Prescricao(
                id=PrescricaoId(prox + idx), prontuario_id=prontuario.id,
                medicamento_id=MedicamentoId(p.medicamento_id), dosagem=p.dosagem,
                administracao=p.administracao, tempo_de_uso=p.tempo_de_uso,
            )
            for idx, p in enumerate(entrada.prescricoes)
        ]
        if prescricoes:
            self._prescricoes.salvar_varias(prescricoes)
        self._consultas.salvar(consulta.marcar_realizada())
        self._eventos.publicar(ProntuarioRegistradoEvent(
            ocorrido_em=datetime.now(timezone.utc), prontuario_id=prontuario.id,
            consulta_id=consulta_id, paciente_id=paciente.id,
        ))
        return int(prontuario.id)
