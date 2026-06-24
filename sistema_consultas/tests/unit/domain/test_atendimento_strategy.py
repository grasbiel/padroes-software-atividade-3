
from __future__ import annotations
from datetime import date
import pytest
from consultas.domain.entities.paciente import Paciente
from consultas.domain.enums.sexo import Sexo
from consultas.domain.enums.tipo_atendimento import TipoAtendimento
from consultas.domain.exceptions import BusinessRuleViolation
from consultas.domain.strategies.atendimento import politica_para
from consultas.domain.value_objects.identificadores import EnderecoId, PacienteId

def test_plano_exige_paciente_com_plano() -> None:
    paciente = Paciente(
        id=PacienteId(1), nome_crianca="A", nome_responsavel="B",
        data_nascimento=date(2020, 1, 1), sexo=Sexo.FEMININO, endereco_id=EnderecoId(1),
    )
    with pytest.raises(BusinessRuleViolation):
        politica_para(TipoAtendimento.PLANO).validar_agendamento(paciente)
