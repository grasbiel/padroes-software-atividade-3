from __future__ import annotations

from consultas.application.ports.out.gateways import MedicoRegistroProfissionalGateway
from consultas.domain.entities.medico import Medico


class StubMedicoRegistroProfissionalGateway(MedicoRegistroProfissionalGateway):
    """Adaptador stub: valida CRMs conhecidos (demo/local)."""

    def __init__(self, crms_validos: frozenset[str] | None = None) -> None:
        self._crms_validos = crms_validos or frozenset({"12345-MA"})

    def validar_crm(self, medico: Medico) -> bool:
        return medico.crm in self._crms_validos
