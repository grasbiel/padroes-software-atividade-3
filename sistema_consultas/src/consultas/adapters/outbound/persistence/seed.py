
from __future__ import annotations
from datetime import date, datetime
from sqlalchemy.orm import Session
from consultas.adapters.outbound.persistence.orm_models import (
    ConsultaModel,
    EnderecoModel,
    ExameModel,
    MedicamentoModel,
    MedicoModel,
    PacienteModel,
    PlanoSaudeModel,
    TelefoneModel,
)

def seed_database(session: Session) -> None:
    if session.query(MedicoModel).first():
        return
    plano = PlanoSaudeModel(id=1, nome_plano="Unimed Infantil")
    endereco = EnderecoModel(
        id=1, logradouro="Rua das Flores", numero="100", complemento="", bairro="Centro",
        cidade="São Luís", estado="MA", cep="65000-000",
    )
    medico = MedicoModel(id=1, nome_medico="Dr. Vilegas", crm="12345-MA")
    paciente = PacienteModel(
        id=1, nome_crianca="Ana Silva", nome_responsavel="Maria Silva", data_nascimento=date(2018, 5, 10),
        sexo="feminino", plano_saude_id=1, endereco_id=1,
    )
    meds = [
        MedicamentoModel(id=1, nome_medicamento="Paracetamol"),
        MedicamentoModel(id=2, nome_medicamento="Amoxicilina"),
    ]
    exames = [ExameModel(id=1, nome_exame="Hemograma"), ExameModel(id=2, nome_exame="Raio-X")]
    telefone = TelefoneModel(id=1, numero="98999990000", tipo="celular", paciente_id=1)
    consulta = ConsultaModel(
        id=1,
        paciente_id=1,
        medico_id=1,
        data_hora=datetime.combine(date.today(), datetime.min.time().replace(hour=9, minute=0)),
        novo_paciente=False,
        tipo_atendimento="plano",
        estado="agendada",
    )
    session.add_all([plano, endereco, medico, paciente, telefone, consulta, *meds, *exames])
    session.commit()
