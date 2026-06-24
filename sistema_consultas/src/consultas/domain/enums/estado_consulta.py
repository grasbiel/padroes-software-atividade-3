
from __future__ import annotations
from enum import Enum

class EstadoConsulta(str, Enum):
    AGENDADA = "agendada"
    REALIZADA = "realizada"
    CANCELADA = "cancelada"
