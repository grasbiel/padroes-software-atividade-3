
from __future__ import annotations

class DomainError(Exception):
    pass

class EntityNotFoundError(DomainError):
    pass

class BusinessRuleViolation(DomainError):
    pass

class InvalidStateTransition(DomainError):
    pass

class ProntuarioJaExisteError(BusinessRuleViolation):
    pass

class MedicamentoNaoCadastradoError(BusinessRuleViolation):
    pass

class ExameNaoCadastradoError(BusinessRuleViolation):
    pass
