
from __future__ import annotations
from datetime import date, datetime
from pydantic import BaseModel, Field

class ConsultaDiaResponse(BaseModel):
    consulta_id: int
    data_hora: datetime
    nome_paciente: str
    novo_paciente: bool
    estado: str

class HistoricoMedidaResponse(BaseModel):
    data_consulta: datetime
    peso: float
    altura: float

class ContextoProntuarioResponse(BaseModel):
    consulta_id: int
    paciente_id: int
    nome_paciente: str
    historico: list[HistoricoMedidaResponse]
    medicamentos_disponiveis: list[str]
    exames_disponiveis: list[str]

class PrescricaoRequest(BaseModel):
    medicamento_id: int
    dosagem: str
    administracao: str
    tempo_de_uso: str

class RegistrarProntuarioRequest(BaseModel):
    peso: float = Field(gt=0)
    altura: float = Field(gt=0)
    descricao_sintomas: str
    observacao_clinica: str
    exame_ids: list[int] = Field(default_factory=list)
    prescricoes: list[PrescricaoRequest] = Field(default_factory=list)

class ItemReceituarioResponse(BaseModel):
    medicamento: str
    dosagem: str
    administracao: str
    tempo_de_uso: str

class ReceituarioResponse(BaseModel):
    consulta_id: int
    nome_medico: str
    crm: str
    itens: list[ItemReceituarioResponse]

class AgendarConsultaRequest(BaseModel):
    paciente_id: int | None = None
    medico_id: int
    data_hora: datetime
    tipo_atendimento: str
    novo_paciente: bool = False
    nome_crianca: str | None = None
    nome_responsavel: str | None = None
    data_nascimento: date | None = None
    sexo: str | None = None
    endereco_id: int | None = None
    telefone_numero: str | None = None
    plano_saude_id: int | None = None
