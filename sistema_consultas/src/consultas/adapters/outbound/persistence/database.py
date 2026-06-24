
from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from consultas.adapters.outbound.persistence.orm_models import Base

def create_session_factory(database_url: str = "sqlite:///./consultas.db") -> sessionmaker[Session]:
    engine = create_engine(database_url, future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
