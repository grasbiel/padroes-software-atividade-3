
from __future__ import annotations
from consultas.domain.builders.prontuario_builder import ProntuarioBuilder
from consultas.domain.value_objects.identificadores import ConsultaId, ExameId, ProntuarioId

def test_prontuario_builder() -> None:
    pront = (
        ProntuarioBuilder(ProntuarioId(1), ConsultaId(10))
        .com_medidas(12.5, 0.85)
        .com_sintomas("Febre")
        .com_observacao("Repouso")
        .adicionar_exame(ExameId(2))
        .build()
    )
    assert pront.peso == 12.5
    assert pront.exame_ids == (ExameId(2),)
