
from __future__ import annotations
from consultas.application.ports.out.event_publisher import DomainEventPublisher
from consultas.domain.events import ConsultaAgendadaEvent, DomainEvent, DomainEventListener, ProntuarioRegistradoEvent
from consultas.application.ports.out.gateways import NotificacaoGateway

class InProcessEventPublisher(DomainEventPublisher):
    def __init__(self) -> None:
        self._listeners: list[DomainEventListener] = []

    def registrar(self, listener: DomainEventListener) -> None:
        self._listeners.append(listener)

    def publicar(self, event: DomainEvent) -> None:
        for listener in self._listeners:
            listener.on_event(event)

class NotificacaoEventListener:
  """Observer: reage a eventos de domínio enviando notificações."""

  def __init__(self, notificador: NotificacaoGateway) -> None:
      self._notificador = notificador

  def on_event(self, event: DomainEvent) -> None:
      if isinstance(event, ConsultaAgendadaEvent):
          self._notificador.notificar(
              destinatario=f"paciente:{int(event.paciente_id)}",
              mensagem=f"Consulta {int(event.consulta_id)} agendada com sucesso.",
          )
      elif isinstance(event, ProntuarioRegistradoEvent):
          self._notificador.notificar(
              destinatario=f"paciente:{int(event.paciente_id)}",
              mensagem=f"Prontuário {int(event.prontuario_id)} registrado.",
          )
