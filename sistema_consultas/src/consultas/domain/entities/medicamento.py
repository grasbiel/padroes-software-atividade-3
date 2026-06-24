
from __future__ import annotations
from dataclasses import dataclass
from consultas.domain.value_objects.identificadores import MedicamentoId

@dataclass(frozen=True, slots=True)
class Medicamento:
    id: MedicamentoId
    nome_medicamento: str
