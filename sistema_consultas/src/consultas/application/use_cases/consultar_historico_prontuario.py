
from __future__ import annotations
from consultas.application.dtos.consulta_dtos import ContextoProntuarioDTO, HistoricoMedidaDTO
from consultas.application.ports.out.repositories import (
    ConsultaRepository, ExameRepository, MedicamentoRepository, PacienteRepository, ProntuarioRepository,
)
from consultas.domain.exceptions import EntityNotFoundError
from consultas.domain.value_objects.identificadores import ConsultaId

class ConsultarHistoricoProntuarioUseCase:
    def __init__(
        self, consultas: ConsultaRepository, pacientes: PacienteRepository,
        prontuarios: ProntuarioRepository, medicamentos: MedicamentoRepository, exames: ExameRepository,
    ) -> None:
        self._consultas = consultas
        self._pacientes = pacientes
        self._prontuarios = prontuarios
        self._medicamentos = medicamentos
        self._exames = exames

    def executar(self, consulta_id: ConsultaId) -> ContextoProntuarioDTO:
        consulta = self._consultas.obter_por_id(consulta_id)
        if consulta is None:
            raise EntityNotFoundError("Consulta não encontrada.")
        paciente = self._pacientes.obter_por_id(consulta.paciente_id)
        if paciente is None:
            raise EntityNotFoundError("Paciente não encontrado.")
        historico: list[HistoricoMedidaDTO] = []
        for pront in self._prontuarios.listar_historico_paciente(paciente.id):
            if pront.consulta_id == consulta_id:
                continue
            c = self._consultas.obter_por_id(pront.consulta_id)
            if c is None:
                continue
            historico.append(HistoricoMedidaDTO(data_consulta=c.data_hora, peso=pront.peso, altura=pront.altura))
        return ContextoProntuarioDTO(
            consulta_id=int(consulta.id), paciente_id=int(paciente.id), nome_paciente=paciente.nome_crianca,
            historico=tuple(sorted(historico, key=lambda h: h.data_consulta)),
            medicamentos_disponiveis=tuple(m.nome_medicamento for m in self._medicamentos.listar_todos()),
            exames_disponiveis=tuple(e.nome_exame for e in self._exames.listar_todos()),
        )
