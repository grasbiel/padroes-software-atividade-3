
from __future__ import annotations
from dataclasses import dataclass
from consultas.domain.value_objects.identificadores import MedicamentoId, PrescricaoId, ProntuarioId

@dataclass(frozen=True, slots=True)
class Prescricao:
    id: PrescricaoId
    prontuario_id: ProntuarioId
    medicamento_id: MedicamentoId
    dosagem: str
    administracao: str
    tempo_de_uso: str
