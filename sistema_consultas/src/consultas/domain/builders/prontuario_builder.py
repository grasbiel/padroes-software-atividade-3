
from __future__ import annotations
from consultas.domain.entities.prontuario import Prontuario
from consultas.domain.value_objects.identificadores import ConsultaId, ExameId, ProntuarioId

class ProntuarioBuilder:
    def __init__(self, prontuario_id: ProntuarioId, consulta_id: ConsultaId) -> None:
        self._id = prontuario_id
        self._consulta_id = consulta_id
        self._peso: float | None = None
        self._altura: float | None = None
        self._sintomas = ""
        self._observacao = ""
        self._exames: list[ExameId] = []

    def com_medidas(self, peso: float, altura: float) -> ProntuarioBuilder:
        self._peso = peso
        self._altura = altura
        return self

    def com_sintomas(self, descricao: str) -> ProntuarioBuilder:
        self._sintomas = descricao
        return self

    def com_observacao(self, observacao: str) -> ProntuarioBuilder:
        self._observacao = observacao
        return self

    def adicionar_exame(self, exame_id: ExameId) -> ProntuarioBuilder:
        self._exames.append(exame_id)
        return self

    def build(self) -> Prontuario:
        if self._peso is None or self._altura is None:
            raise ValueError("Peso e altura são obrigatórios.")
        return Prontuario(
            id=self._id,
            consulta_id=self._consulta_id,
            peso=self._peso,
            altura=self._altura,
            descricao_sintomas=self._sintomas,
            observacao_clinica=self._observacao,
            exame_ids=tuple(self._exames),
        )
