
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from consultas.domain.value_objects.identificadores import ConsultaId, PacienteId, ProntuarioId

@dataclass(frozen=True, slots=True)
class DomainEvent:
    ocorrido_em: datetime

@dataclass(frozen=True, slots=True)
class ConsultaAgendadaEvent(DomainEvent):
    consulta_id: ConsultaId
    paciente_id: PacienteId

@dataclass(frozen=True, slots=True)
class ProntuarioRegistradoEvent(DomainEvent):
    prontuario_id: ProntuarioId
    consulta_id: ConsultaId
    paciente_id: PacienteId

class DomainEventListener(Protocol):
    def on_event(self, event: DomainEvent) -> None: ...
