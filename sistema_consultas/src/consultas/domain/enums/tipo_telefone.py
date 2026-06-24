
from __future__ import annotations
from enum import Enum

class TipoTelefone(str, Enum):
    CELULAR = "celular"
    FIXO = "fixo"
    TRABALHO = "trabalho"
