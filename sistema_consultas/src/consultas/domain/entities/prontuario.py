
from __future__ import annotations
from dataclasses import dataclass
from consultas.domain.value_objects.identificadores import ConsultaId, ExameId, ProntuarioId

@dataclass(frozen=True, slots=True)
class Prontuario:
    id: ProntuarioId
    consulta_id: ConsultaId
    peso: float
    altura: float
    descricao_sintomas: str
    observacao_clinica: str
    exame_ids: tuple[ExameId, ...] = ()

    def __post_init__(self) -> None:
        if self.peso <= 0 or self.altura <= 0:
            raise ValueError("Peso e altura devem ser positivos.")
