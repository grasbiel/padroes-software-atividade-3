
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from consultas.domain.enums.sexo import Sexo
from consultas.domain.value_objects.identificadores import EnderecoId, PacienteId, PlanoSaudeId

@dataclass(frozen=True, slots=True)
class Paciente:
    id: PacienteId
    nome_crianca: str
    nome_responsavel: str
    data_nascimento: date
    sexo: Sexo
    endereco_id: EnderecoId
    plano_saude_id: PlanoSaudeId | None = None

    @property
    def possui_plano(self) -> bool:
        return self.plano_saude_id is not None
