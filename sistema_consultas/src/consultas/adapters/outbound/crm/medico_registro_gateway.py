
from __future__ import annotations
import httpx
from consultas.application.ports.out.gateways import MedicoRegistroProfissionalGateway
from consultas.domain.entities.medico import Medico

class HttpMedicoRegistroProfissionalGateway(MedicoRegistroProfissionalGateway):
    """Stub de integração externa para validação de CRM via HTTP."""

    def __init__(self, base_url: str = "https://api.crm.exemplo.gov.br") -> None:
        self._base_url = base_url.rstrip("/")

    def validar_crm(self, medico: Medico) -> bool:
        url = f"{self._base_url}/medicos/{medico.crm}"
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(url)
            return response.status_code == 200
        except httpx.HTTPError:
            return False
