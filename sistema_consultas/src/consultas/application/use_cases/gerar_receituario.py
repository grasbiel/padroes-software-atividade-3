
from __future__ import annotations
from consultas.application.dtos.consulta_dtos import ItemReceituarioDTO, ReceituarioDTO
from consultas.application.ports.out.repositories import (
    ConsultaRepository, MedicamentoRepository, MedicoRepository, PrescricaoRepository, ProntuarioRepository,
)
from consultas.domain.exceptions import BusinessRuleViolation, EntityNotFoundError
from consultas.domain.value_objects.identificadores import ConsultaId

class GerarReceituarioUseCase:
    def __init__(
        self, consultas: ConsultaRepository, prontuarios: ProntuarioRepository,
        prescricoes: PrescricaoRepository, medicamentos: MedicamentoRepository, medicos: MedicoRepository,
    ) -> None:
        self._consultas = consultas
        self._prontuarios = prontuarios
        self._prescricoes = prescricoes
        self._medicamentos = medicamentos
        self._medicos = medicos

    def executar(self, consulta_id: ConsultaId) -> ReceituarioDTO:
        consulta = self._consultas.obter_por_id(consulta_id)
        if consulta is None:
            raise EntityNotFoundError("Consulta não encontrada.")
        prontuario = self._prontuarios.obter_por_consulta(consulta_id)
        if prontuario is None:
            raise BusinessRuleViolation("Prontuário inexistente para esta consulta.")
        medico = self._medicos.obter_por_id(consulta.medico_id)
        if medico is None:
            raise EntityNotFoundError("Médico não encontrado.")
        itens: list[ItemReceituarioDTO] = []
        for presc in self._prescricoes.listar_por_prontuario(prontuario.id):
            med = self._medicamentos.obter_por_id(presc.medicamento_id)
            nome = med.nome_medicamento if med else str(presc.medicamento_id)
            itens.append(ItemReceituarioDTO(
                medicamento=nome, dosagem=presc.dosagem, administracao=presc.administracao,
                tempo_de_uso=presc.tempo_de_uso,
            ))
        return ReceituarioDTO(
            consulta_id=int(consulta.id), nome_medico=medico.nome_medico, crm=medico.crm, itens=tuple(itens),
        )
