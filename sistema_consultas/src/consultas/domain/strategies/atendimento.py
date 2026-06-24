
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from consultas.domain.entities.paciente import Paciente
from consultas.domain.enums.tipo_atendimento import TipoAtendimento
from consultas.domain.exceptions import BusinessRuleViolation

class PoliticaAtendimento(Protocol):
    def validar_agendamento(self, paciente: Paciente) -> None: ...

@dataclass(frozen=True, slots=True)
class AtendimentoPlano:
    def validar_agendamento(self, paciente: Paciente) -> None:
        if not paciente.possui_plano:
            raise BusinessRuleViolation("Paciente deve possuir plano para atendimento por plano.")

@dataclass(frozen=True, slots=True)
class AtendimentoParticular:
    def validar_agendamento(self, paciente: Paciente) -> None:
        return

def politica_para(tipo: TipoAtendimento) -> PoliticaAtendimento:
    if tipo is TipoAtendimento.PLANO:
        return AtendimentoPlano()
    return AtendimentoParticular()
