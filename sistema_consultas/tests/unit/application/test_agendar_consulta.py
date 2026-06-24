
from __future__ import annotations
from datetime import date, datetime
from consultas.adapters.outbound.notifications.event_bus import InProcessEventPublisher
from consultas.adapters.outbound.persistence.in_memory import (
    InMemoryConsultaRepository, InMemoryPacienteRepository, InMemoryTelefoneRepository,
)
from consultas.application.dtos.consulta_dtos import AgendarConsultaInputDTO
from consultas.application.use_cases.agendar_consulta import AgendarConsultaUseCase
from consultas.domain.enums.tipo_atendimento import TipoAtendimento

def test_agendar_paciente_existente() -> None:
    from consultas.domain.entities.paciente import Paciente
    from consultas.domain.enums.sexo import Sexo
    from consultas.domain.value_objects.identificadores import EnderecoId, PacienteId

    consultas = InMemoryConsultaRepository()
    pacientes = InMemoryPacienteRepository()
    telefones = InMemoryTelefoneRepository()
    pacientes.salvar(Paciente(
        id=PacienteId(1), nome_crianca="Ana", nome_responsavel="Maria",
        data_nascimento=date(2018, 1, 1), sexo=Sexo.FEMININO, endereco_id=EnderecoId(1),
    ))
    uc = AgendarConsultaUseCase(consultas, pacientes, telefones, InProcessEventPublisher())
    cid = uc.executar(AgendarConsultaInputDTO(
        paciente_id=1, medico_id=1, data_hora=datetime(2026, 6, 25, 10, 0),
        tipo_atendimento=TipoAtendimento.PARTICULAR, novo_paciente=False,
    ))
    assert cid == 1
