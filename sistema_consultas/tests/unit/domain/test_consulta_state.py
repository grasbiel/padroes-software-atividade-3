
from __future__ import annotations
from datetime import datetime
import pytest
from consultas.domain.entities.consulta import Consulta
from consultas.domain.enums.estado_consulta import EstadoConsulta
from consultas.domain.enums.tipo_atendimento import TipoAtendimento
from consultas.domain.exceptions import InvalidStateTransition
from consultas.domain.value_objects.identificadores import ConsultaId, MedicoId, PacienteId

def test_consulta_marcar_realizada() -> None:
    c = Consulta(
        id=ConsultaId(1), paciente_id=PacienteId(1), medico_id=MedicoId(1),
        data_hora=datetime(2026, 6, 24, 10, 0), novo_paciente=False,
        tipo_atendimento=TipoAtendimento.PARTICULAR,
    )
    realizada = c.marcar_realizada()
    assert realizada.estado is EstadoConsulta.REALIZADA

def test_consulta_cancelar_invalida_apos_realizada() -> None:
    c = Consulta(
        id=ConsultaId(1), paciente_id=PacienteId(1), medico_id=MedicoId(1),
        data_hora=datetime(2026, 6, 24, 10, 0), novo_paciente=False,
        tipo_atendimento=TipoAtendimento.PARTICULAR, estado=EstadoConsulta.REALIZADA,
    )
    with pytest.raises(InvalidStateTransition):
        c.cancelar()
