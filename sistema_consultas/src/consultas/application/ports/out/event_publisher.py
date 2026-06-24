
from __future__ import annotations
from typing import Protocol
from consultas.domain.events import DomainEvent

class DomainEventPublisher(Protocol):
    def publicar(self, event: DomainEvent) -> None: ...
