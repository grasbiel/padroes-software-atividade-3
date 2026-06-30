
from __future__ import annotations
from typing import Protocol
from consultas.domain.entities.medico import Medico

class MedicoRegistroProfissionalGateway(Protocol):
    def validar_crm(self, medico: Medico) -> bool: ...

class NotificacaoGateway(Protocol):
    def notificar(self, destinatario: str, mensagem: str) -> None: ...
