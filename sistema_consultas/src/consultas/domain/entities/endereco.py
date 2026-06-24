
from __future__ import annotations
from dataclasses import dataclass
from consultas.domain.value_objects.identificadores import EnderecoId

@dataclass(frozen=True, slots=True)
class Endereco:
    id: EnderecoId
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    estado: str
    cep: str
