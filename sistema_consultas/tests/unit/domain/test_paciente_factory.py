
from __future__ import annotations
from datetime import date
import pytest
from consultas.domain.enums.sexo import Sexo
from consultas.domain.exceptions import BusinessRuleViolation
from consultas.domain.factories.paciente_factory import PacienteFactory
from consultas.domain.value_objects.identificadores import EnderecoId, PacienteId

def test_paciente_factory_exige_telefone() -> None:
    with pytest.raises(BusinessRuleViolation):
        PacienteFactory.criar_novo(
            id=PacienteId(1), nome_crianca="João", nome_responsavel="Pai",
            data_nascimento=date(2020, 1, 1), sexo=Sexo.MASCULINO,
            endereco_id=EnderecoId(1), telefone_informado=False,
        )
