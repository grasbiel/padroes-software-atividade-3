
from __future__ import annotations

from datetime import date, datetime

from consultas.adapters.outbound.persistence.in_memory import (
    InMemoryConsultaRepository,
    InMemoryPacienteRepository,
)
from consultas.application.use_cases.listar_consultas_do_dia import ListarConsultasDoDiaUseCase
from consultas.domain.entities.consulta import Consulta
from consultas.domain.entities.paciente import Paciente
from consultas.domain.enums.sexo import Sexo
from consultas.domain.enums.tipo_atendimento import TipoAtendimento
from consultas.domain.value_objects.identificadores import ConsultaId, EnderecoId, MedicoId, PacienteId


def test_listar_consultas_do_dia() -> None:
    consultas = InMemoryConsultaRepository()
    pacientes = InMemoryPacienteRepository()
    paciente = Paciente(
        id=PacienteId(1),
        nome_crianca="Ana Silva",
        nome_responsavel="Maria",
        data_nascimento=date(2018, 5, 10),
        sexo=Sexo.FEMININO,
        endereco_id=EnderecoId(1),
    )
    pacientes.salvar(paciente)
    consultas.salvar(
        Consulta(
            id=ConsultaId(1),
            paciente_id=paciente.id,
            medico_id=MedicoId(1),
            data_hora=datetime(2026, 6, 24, 9, 0),
            novo_paciente=False,
            tipo_atendimento=TipoAtendimento.PLANO,
        )
    )
    uc = ListarConsultasDoDiaUseCase(consultas, pacientes)
    itens = uc.executar(date(2026, 6, 24))
    assert len(itens) == 1
    assert itens[0].nome_paciente == "Ana Silva"
    assert itens[0].novo_paciente is False
    assert itens[0].estado == "agendada"
