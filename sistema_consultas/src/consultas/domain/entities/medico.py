
from __future__ import annotations
from dataclasses import dataclass
from consultas.domain.value_objects.identificadores import MedicoId

@dataclass(frozen=True, slots=True)
class Medico:
    id: MedicoId
    nome_medico: str
    crm: str
