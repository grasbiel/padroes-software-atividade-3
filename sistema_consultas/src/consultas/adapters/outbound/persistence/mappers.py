
from __future__ import annotations
from consultas.domain.entities.consulta import Consulta
from consultas.domain.entities.exame import Exame
from consultas.domain.entities.medicamento import Medicamento
from consultas.domain.entities.medico import Medico
from consultas.domain.entities.paciente import Paciente
from consultas.domain.entities.prescricao import Prescricao
from consultas.domain.entities.prontuario import Prontuario
from consultas.domain.enums.estado_consulta import EstadoConsulta
from consultas.domain.enums.sexo import Sexo
from consultas.domain.enums.tipo_atendimento import TipoAtendimento
from consultas.domain.value_objects.identificadores import (
    ConsultaId, EnderecoId, ExameId, MedicamentoId, MedicoId, PacienteId, PlanoSaudeId,
    PrescricaoId, ProntuarioId,
)
from consultas.adapters.outbound.persistence.orm_models import (
    ConsultaModel, ExameModel, MedicamentoModel, MedicoModel, PacienteModel, PrescricaoModel, ProntuarioModel,
)

def medico_to_domain(m: MedicoModel) -> Medico:
    return Medico(id=MedicoId(m.id), nome_medico=m.nome_medico, crm=m.crm)

def medicamento_to_domain(m: MedicamentoModel) -> Medicamento:
    return Medicamento(id=MedicamentoId(m.id), nome_medicamento=m.nome_medicamento)

def exame_to_domain(m: ExameModel) -> Exame:
    return Exame(id=ExameId(m.id), nome_exame=m.nome_exame)

def paciente_to_domain(m: PacienteModel) -> Paciente:
    return Paciente(
        id=PacienteId(m.id), nome_crianca=m.nome_crianca, nome_responsavel=m.nome_responsavel,
        data_nascimento=m.data_nascimento, sexo=Sexo(m.sexo), endereco_id=EnderecoId(m.endereco_id),
        plano_saude_id=PlanoSaudeId(m.plano_saude_id) if m.plano_saude_id else None,
    )

def consulta_to_domain(m: ConsultaModel) -> Consulta:
    return Consulta(
        id=ConsultaId(m.id), paciente_id=PacienteId(m.paciente_id), medico_id=MedicoId(m.medico_id),
        data_hora=m.data_hora, novo_paciente=m.novo_paciente,
        tipo_atendimento=TipoAtendimento(m.tipo_atendimento), estado=EstadoConsulta(m.estado),
    )

def consulta_to_model(c: Consulta) -> ConsultaModel:
    cid = int(c.id)
    return ConsultaModel(
        id=cid if cid else None,
        paciente_id=int(c.paciente_id),
        medico_id=int(c.medico_id),
        data_hora=c.data_hora,
        novo_paciente=c.novo_paciente,
        tipo_atendimento=c.tipo_atendimento.value,
        estado=c.estado.value,
    )

def prontuario_to_domain(m: ProntuarioModel) -> Prontuario:
    return Prontuario(
        id=ProntuarioId(m.id), consulta_id=ConsultaId(m.consulta_id), peso=m.peso, altura=m.altura,
        descricao_sintomas=m.descricao_sintomas, observacao_clinica=m.observacao_clinica,
        exame_ids=tuple(ExameId(pe.exame_id) for pe in m.exames),
    )

def prescricao_to_domain(m: PrescricaoModel) -> Prescricao:
    return Prescricao(
        id=PrescricaoId(m.id), prontuario_id=ProntuarioId(m.prontuario_id),
        medicamento_id=MedicamentoId(m.medicamento_id), dosagem=m.dosagem,
        administracao=m.administracao, tempo_de_uso=m.tempo_de_uso,
    )
