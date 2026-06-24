
from __future__ import annotations
from dataclasses import dataclass
from consultas.domain.value_objects.identificadores import PlanoSaudeId

@dataclass(frozen=True, slots=True)
class PlanoSaude:
    id: PlanoSaudeId
    nome_plano: str
