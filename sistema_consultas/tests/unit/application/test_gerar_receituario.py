
from __future__ import annotations

from datetime import date, datetime

import pytest

from consultas.adapters.outbound.notifications.event_bus import InProcessEventPublisher
from consultas.adapters.outbound.persistence.in_memory import (
    InMemoryConsultaRepository,
    InMemoryExameRepository,
    InMemoryMedicamentoRepository,
    InMemoryMedicoRepository,
    InMemoryPacienteRepository,
    InMemoryPrescricaoRepository,
    InMemoryProntuarioRepository,
)
from consultas.application.dtos.consulta_dtos import PrescricaoInputDTO, RegistrarProntuarioInputDTO
from consultas.application.use_cases.gerar_receituario import GerarReceituarioUseCase
from consultas.application.use_cases.registrar_prontuario import RegistrarProntuarioUseCase
from consultas.domain.entities.consulta import Consulta
from consultas.domain.entities.exame import Exame
from consultas.domain.entities.medico import Medico
from consultas.domain.entities.medicamento import Medicamento
from consultas.domain.entities.paciente import Paciente
from consultas.domain.enums.estado_consulta import EstadoConsulta
from consultas.domain.enums.sexo import Sexo
from consultas.domain.enums.tipo_atendimento import TipoAtendimento
from consultas.domain.exceptions import ConsultaNaoAgendadaError
from consultas.domain.value_objects.identificadores import (
    ConsultaId,
    EnderecoId,
    ExameId,
    MedicamentoId,
    MedicoId,
    PacienteId,
)


def _setup_registrar() -> tuple[RegistrarProntuarioUseCase, GerarReceituarioUseCase, ConsultaId]:
    consultas = InMemoryConsultaRepository()
    pacientes = InMemoryPacienteRepository()
    prontuarios = InMemoryProntuarioRepository()
    medicamentos = InMemoryMedicamentoRepository([Medicamento(MedicamentoId(1), "Paracetamol")])
    exames = InMemoryExameRepository([Exame(ExameId(1), "Hemograma")])
    prescricoes = InMemoryPrescricaoRepository()
    medicos = InMemoryMedicoRepository([Medico(MedicoId(1), "Dr. Vilegas", "12345-MA")])
    eventos = InProcessEventPublisher()

    paciente = Paciente(
        id=PacienteId(1),
        nome_crianca="Ana",
        nome_responsavel="Maria",
        data_nascimento=date(2018, 1, 1),
        sexo=Sexo.FEMININO,
        endereco_id=EnderecoId(1),
    )
    pacientes.salvar(paciente)
    consulta = Consulta(
        id=ConsultaId(1),
        paciente_id=paciente.id,
        medico_id=MedicoId(1),
        data_hora=datetime(2026, 6, 24, 9, 0),
        novo_paciente=False,
        tipo_atendimento=TipoAtendimento.PARTICULAR,
    )
    consultas.salvar(consulta)
    prontuarios.registrar_mapa_consulta_paciente(consulta.id, paciente.id)

    registrar = RegistrarProntuarioUseCase(
        consultas, pacientes, prontuarios, medicamentos, exames, prescricoes, eventos
    )
    receituario = GerarReceituarioUseCase(
        consultas, prontuarios, prescricoes, medicamentos, medicos
    )
    return registrar, receituario, consulta.id


def test_registrar_e_gerar_receituario_com_itens() -> None:
    registrar, receituario, consulta_id = _setup_registrar()
    pid = registrar.executar(
        RegistrarProntuarioInputDTO(
            consulta_id=int(consulta_id),
            peso=20.0,
            altura=1.0,
            descricao_sintomas="Tosse",
            observacao_clinica="OK",
            exame_ids=[1],
            prescricoes=[PrescricaoInputDTO(1, "5ml", "oral", "7 dias")],
        )
    )
    assert pid == 1

    dto = receituario.executar(consulta_id)
    assert dto.nome_medico == "Dr. Vilegas"
    assert dto.crm == "12345-MA"
    assert len(dto.itens) == 1
    assert dto.itens[0].medicamento == "Paracetamol"
    assert dto.itens[0].dosagem == "5ml"


def test_registrar_rejeita_consulta_realizada() -> None:
    registrar, _, consulta_id = _setup_registrar()
    entrada = RegistrarProntuarioInputDTO(
        consulta_id=int(consulta_id),
        peso=20.0,
        altura=1.0,
        descricao_sintomas="Tosse",
        observacao_clinica="OK",
        exame_ids=[],
        prescricoes=[],
    )
    registrar.executar(entrada)
    with pytest.raises(ConsultaNaoAgendadaError):
        registrar.executar(entrada)
