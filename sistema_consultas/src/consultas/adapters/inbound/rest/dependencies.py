from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass
from typing import cast

from fastapi import Request
from sqlalchemy.orm import Session

from consultas.adapters.outbound.notifications.event_bus import InProcessEventPublisher
from consultas.application.ports.out.gateways import MedicoRegistroProfissionalGateway
from consultas.adapters.outbound.persistence.sqlalchemy_repositories import (
    SqlAlchemyConsultaRepository,
    SqlAlchemyExameRepository,
    SqlAlchemyMedicamentoRepository,
    SqlAlchemyMedicoRepository,
    SqlAlchemyPacienteRepository,
    SqlAlchemyPrescricaoRepository,
    SqlAlchemyProntuarioRepository,
    SqlAlchemyTelefoneRepository,
)
from consultas.application.ports.out.repositories import (
    ConsultaRepository,
    ExameRepository,
    MedicamentoRepository,
    MedicoRepository,
    PacienteRepository,
    PrescricaoRepository,
    ProntuarioRepository,
    TelefoneRepository,
)


@dataclass(frozen=True, slots=True)
class RepositoriesBundle:
    consultas: ConsultaRepository
    pacientes: PacienteRepository
    medicos: MedicoRepository
    medicamentos: MedicamentoRepository
    exames: ExameRepository
    prontuarios: ProntuarioRepository
    prescricoes: PrescricaoRepository
    telefones: TelefoneRepository


def get_db(request: Request) -> Generator[Session, None, None]:
    session_factory = request.app.state.session_factory
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def build_repositories(session: Session) -> RepositoriesBundle:
    return RepositoriesBundle(
        consultas=SqlAlchemyConsultaRepository(session),
        pacientes=SqlAlchemyPacienteRepository(session),
        medicos=SqlAlchemyMedicoRepository(session),
        medicamentos=SqlAlchemyMedicamentoRepository(session),
        exames=SqlAlchemyExameRepository(session),
        prontuarios=SqlAlchemyProntuarioRepository(session),
        prescricoes=SqlAlchemyPrescricaoRepository(session),
        telefones=SqlAlchemyTelefoneRepository(session),
    )


def get_event_publisher(request: Request) -> InProcessEventPublisher:
    return cast(InProcessEventPublisher, request.app.state.event_publisher)


def get_crm_gateway(request: Request) -> MedicoRegistroProfissionalGateway:
    return cast(MedicoRegistroProfissionalGateway, request.app.state.crm_gateway)
