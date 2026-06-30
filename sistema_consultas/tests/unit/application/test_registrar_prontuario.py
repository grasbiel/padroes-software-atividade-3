
from __future__ import annotations
from datetime import datetime
import pytest
from consultas.adapters.outbound.notifications.event_bus import InProcessEventPublisher
from consultas.adapters.outbound.persistence.in_memory import (
    InMemoryConsultaRepository, InMemoryExameRepository, InMemoryMedicamentoRepository,
    InMemoryPacienteRepository, InMemoryPrescricaoRepository, InMemoryProntuarioRepository,
)
from consultas.application.dtos.consulta_dtos import PrescricaoInputDTO, RegistrarProntuarioInputDTO
from consultas.application.use_cases.registrar_prontuario import RegistrarProntuarioUseCase
from consultas.domain.entities.consulta import Consulta
from consultas.domain.entities.exame import Exame
from consultas.domain.entities.medicamento import Medicamento
from consultas.domain.entities.paciente import Paciente
from consultas.domain.enums.sexo import Sexo
from consultas.domain.enums.tipo_atendimento import TipoAtendimento
from consultas.domain.exceptions import ConsultaNaoAgendadaError
from consultas.domain.value_objects.identificadores import (
    ConsultaId, EnderecoId, ExameId, MedicamentoId, MedicoId, PacienteId,
)
from datetime import date

def _setup() -> tuple[RegistrarProntuarioUseCase, ConsultaId]:
    consultas = InMemoryConsultaRepository()
    pacientes = InMemoryPacienteRepository()
    prontuarios = InMemoryProntuarioRepository()
    medicamentos = InMemoryMedicamentoRepository([Medicamento(MedicamentoId(1), "Paracetamol")])
    exames = InMemoryExameRepository([Exame(ExameId(1), "Hemograma")])
    prescricoes = InMemoryPrescricaoRepository()
    eventos = InProcessEventPublisher()
    paciente = Paciente(
        id=PacienteId(1), nome_crianca="Ana", nome_responsavel="Maria",
        data_nascimento=date(2018, 1, 1), sexo=Sexo.FEMININO, endereco_id=EnderecoId(1),
    )
    pacientes.salvar(paciente)
    consulta = Consulta(
        id=ConsultaId(1), paciente_id=paciente.id, medico_id=MedicoId(1),
        data_hora=datetime(2026, 6, 24, 9, 0), novo_paciente=False,
        tipo_atendimento=TipoAtendimento.PARTICULAR,
    )
    consultas.salvar(consulta)
    prontuarios.registrar_mapa_consulta_paciente(consulta.id, paciente.id)
    uc = RegistrarProntuarioUseCase(
        consultas, pacientes, prontuarios, medicamentos, exames, prescricoes, eventos,
    )
    return uc, consulta.id

def test_registrar_prontuario_sucesso() -> None:
    uc, consulta_id = _setup()
    pid = uc.executar(RegistrarProntuarioInputDTO(
        consulta_id=int(consulta_id), peso=20.0, altura=1.0, descricao_sintomas="Tosse",
        observacao_clinica="OK", exame_ids=[1],
        prescricoes=[PrescricaoInputDTO(1, "5ml", "oral", "7 dias")],
    ))
    assert pid == 1

def test_registrar_prontuario_duplicado() -> None:
    uc, consulta_id = _setup()
    entrada = RegistrarProntuarioInputDTO(
        consulta_id=int(consulta_id), peso=20.0, altura=1.0, descricao_sintomas="Tosse",
        observacao_clinica="OK", exame_ids=[], prescricoes=[],
    )
    uc.executar(entrada)
    with pytest.raises(ConsultaNaoAgendadaError):
        uc.executar(entrada)
