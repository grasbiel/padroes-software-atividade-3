
from __future__ import annotations
from dataclasses import dataclass
from consultas.domain.enums.tipo_telefone import TipoTelefone
from consultas.domain.value_objects.identificadores import PacienteId, TelefoneId

@dataclass(frozen=True, slots=True)
class Telefone:
    id: TelefoneId
    numero: str
    tipo: TipoTelefone
    paciente_id: PacienteId
