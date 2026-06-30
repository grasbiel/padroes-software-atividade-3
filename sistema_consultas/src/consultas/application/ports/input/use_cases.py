from __future__ import annotations

from datetime import date
from typing import Protocol

from consultas.application.dtos.consulta_dtos import (
    AgendarConsultaInputDTO,
    ConsultaDiaItemDTO,
    ContextoProntuarioDTO,
    ReceituarioDTO,
    RegistrarProntuarioInputDTO,
)
from consultas.domain.value_objects.identificadores import ConsultaId


class ListarConsultasDoDiaUseCasePort(Protocol):
    def executar(self, dia: date) -> list[ConsultaDiaItemDTO]: ...


class RegistrarProntuarioUseCasePort(Protocol):
    def executar(self, entrada: RegistrarProntuarioInputDTO) -> int: ...


class ConsultarHistoricoProntuarioUseCasePort(Protocol):
    def executar(self, consulta_id: ConsultaId) -> ContextoProntuarioDTO: ...


class GerarReceituarioUseCasePort(Protocol):
    def executar(self, consulta_id: ConsultaId) -> ReceituarioDTO: ...


class AgendarConsultaUseCasePort(Protocol):
    def executar(self, entrada: AgendarConsultaInputDTO) -> int: ...
