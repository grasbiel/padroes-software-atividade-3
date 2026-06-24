
from __future__ import annotations
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class PlanoSaudeModel(Base):
    __tablename__ = "plano_saude"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_plano: Mapped[str] = mapped_column(String(100))

class EnderecoModel(Base):
    __tablename__ = "endereco"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    logradouro: Mapped[str] = mapped_column(String(45))
    numero: Mapped[str] = mapped_column(String(45))
    complemento: Mapped[str] = mapped_column(String(45))
    bairro: Mapped[str] = mapped_column(String(45))
    cidade: Mapped[str] = mapped_column(String(45))
    estado: Mapped[str] = mapped_column(String(45))
    cep: Mapped[str] = mapped_column(String(11))

class PacienteModel(Base):
    __tablename__ = "paciente"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_crianca: Mapped[str] = mapped_column(String(45))
    nome_responsavel: Mapped[str] = mapped_column(String(45))
    data_nascimento: Mapped[date] = mapped_column(Date)
    sexo: Mapped[str] = mapped_column(String(10))
    plano_saude_id: Mapped[int | None] = mapped_column(ForeignKey("plano_saude.id"), nullable=True)
    endereco_id: Mapped[int] = mapped_column(ForeignKey("endereco.id"))

class TelefoneModel(Base):
    __tablename__ = "telefone"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    numero: Mapped[str] = mapped_column(String(20))
    tipo: Mapped[str] = mapped_column(String(15))
    paciente_id: Mapped[int] = mapped_column(ForeignKey("paciente.id"))

class MedicoModel(Base):
    __tablename__ = "medico"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_medico: Mapped[str] = mapped_column(String(45))
    crm: Mapped[str] = mapped_column(String(20))

class MedicamentoModel(Base):
    __tablename__ = "medicamento"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_medicamento: Mapped[str] = mapped_column(String(100))

class ExameModel(Base):
    __tablename__ = "exame"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_exame: Mapped[str] = mapped_column(String(100))

class ConsultaModel(Base):
    __tablename__ = "consulta"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("paciente.id"))
    medico_id: Mapped[int] = mapped_column(ForeignKey("medico.id"))
    data_hora: Mapped[datetime] = mapped_column(DateTime)
    novo_paciente: Mapped[bool] = mapped_column(Boolean)
    tipo_atendimento: Mapped[str] = mapped_column(String(20))
    estado: Mapped[str] = mapped_column(String(20))

class ProntuarioModel(Base):
    __tablename__ = "prontuario"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consulta_id: Mapped[int] = mapped_column(ForeignKey("consulta.id"), unique=True)
    peso: Mapped[float] = mapped_column(Float)
    altura: Mapped[float] = mapped_column(Float)
    descricao_sintomas: Mapped[str] = mapped_column(Text)
    observacao_clinica: Mapped[str] = mapped_column(Text)
    exames: Mapped[list["ProntuarioExameModel"]] = relationship(back_populates="prontuario")

class ProntuarioExameModel(Base):
    __tablename__ = "prontuario_exame"
    prontuario_id: Mapped[int] = mapped_column(ForeignKey("prontuario.id"), primary_key=True)
    exame_id: Mapped[int] = mapped_column(ForeignKey("exame.id"), primary_key=True)
    prontuario: Mapped[ProntuarioModel] = relationship(back_populates="exames")

class PrescricaoModel(Base):
    __tablename__ = "prescricao"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prontuario_id: Mapped[int] = mapped_column(ForeignKey("prontuario.id"))
    medicamento_id: Mapped[int] = mapped_column(ForeignKey("medicamento.id"))
    dosagem: Mapped[str] = mapped_column(String(45))
    administracao: Mapped[str] = mapped_column(String(45))
    tempo_de_uso: Mapped[str] = mapped_column(String(45))
