
from __future__ import annotations
from consultas.application.ports.out.gateways import NotificacaoGateway

class ConsoleNotificador(NotificacaoGateway):
    def notificar(self, destinatario: str, mensagem: str) -> None:
        print(f"[NOTIFICAÇÃO -> {destinatario}] {mensagem}")
