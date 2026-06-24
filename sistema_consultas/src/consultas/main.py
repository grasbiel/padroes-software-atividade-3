
from __future__ import annotations
from fastapi import FastAPI
from consultas.adapters.inbound.rest.router import router
from consultas.adapters.outbound.notifications.console_notificador import ConsoleNotificador
from consultas.adapters.outbound.notifications.event_bus import InProcessEventPublisher, NotificacaoEventListener
from consultas.adapters.outbound.persistence.database import create_session_factory
from consultas.adapters.outbound.persistence.seed import seed_database

app = FastAPI(title="Sistema de Consultas Médicas", version="0.1.0")
app.include_router(router)

@app.on_event("startup")
def on_startup() -> None:
    session_factory = create_session_factory()
    app.state.session_factory = session_factory
    app.state.event_publisher = InProcessEventPublisher()
    listener = NotificacaoEventListener(ConsoleNotificador())
    app.state.event_publisher.registrar(listener)
    with session_factory() as session:
        seed_database(session)

def create_app() -> FastAPI:
    return app
