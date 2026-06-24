
from __future__ import annotations
from dataclasses import dataclass
from consultas.domain.value_objects.identificadores import ExameId

@dataclass(frozen=True, slots=True)
class Exame:
    id: ExameId
    nome_exame: str
