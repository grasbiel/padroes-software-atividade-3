
from __future__ import annotations
from datetime import date
from consultas.application.dtos.consulta_dtos import ConsultaDiaItemDTO
from consultas.application.ports.out.repositories import ConsultaRepository, PacienteRepository
from consultas.domain.exceptions import EntityNotFoundError

class ListarConsultasDoDiaUseCase:
    def __init__(self, consultas: ConsultaRepository, pacientes: PacienteRepository) -> None:
        self._consultas = consultas
        self._pacientes = pacientes

    def executar(self, dia: date) -> list[ConsultaDiaItemDTO]:
        itens: list[ConsultaDiaItemDTO] = []
        for consulta in self._consultas.listar_por_dia(dia):
            paciente = self._pacientes.obter_por_id(consulta.paciente_id)
            if paciente is None:
                raise EntityNotFoundError(f"Paciente {consulta.paciente_id} não encontrado.")
            itens.append(ConsultaDiaItemDTO(
                consulta_id=int(consulta.id), data_hora=consulta.data_hora,
                nome_paciente=paciente.nome_crianca, novo_paciente=consulta.novo_paciente,
                estado=consulta.estado.value,
            ))
        return sorted(itens, key=lambda i: i.data_hora)
