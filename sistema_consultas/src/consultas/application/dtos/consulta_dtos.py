
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import Sequence
from consultas.domain.enums.tipo_atendimento import TipoAtendimento

@dataclass(frozen=True, slots=True)
class ConsultaDiaItemDTO:
    consulta_id: int
    data_hora: datetime
    nome_paciente: str
    novo_paciente: bool
    estado: str

@dataclass(frozen=True, slots=True)
class HistoricoMedidaDTO:
    data_consulta: datetime
    peso: float
    altura: float

@dataclass(frozen=True, slots=True)
class ContextoProntuarioDTO:
    consulta_id: int
    paciente_id: int
    nome_paciente: str
    historico: Sequence[HistoricoMedidaDTO]
    medicamentos_disponiveis: Sequence[str]
    exames_disponiveis: Sequence[str]

@dataclass(frozen=True, slots=True)
class ItemReceituarioDTO:
    medicamento: str
    dosagem: str
    administracao: str
    tempo_de_uso: str

@dataclass(frozen=True, slots=True)
class ReceituarioDTO:
    consulta_id: int
    nome_medico: str
    crm: str
    itens: Sequence[ItemReceituarioDTO]

@dataclass(frozen=True, slots=True)
class PrescricaoInputDTO:
    medicamento_id: int
    dosagem: str
    administracao: str
    tempo_de_uso: str

@dataclass(frozen=True, slots=True)
class AgendarConsultaInputDTO:
    paciente_id: int | None
    medico_id: int
    data_hora: datetime
    tipo_atendimento: TipoAtendimento
    novo_paciente: bool
    nome_crianca: str | None = None
    nome_responsavel: str | None = None
    data_nascimento: date | None = None
    sexo: str | None = None
    endereco_id: int | None = None
    telefone_numero: str | None = None
    plano_saude_id: int | None = None

@dataclass(frozen=True, slots=True)
class RegistrarProntuarioInputDTO:
    consulta_id: int
    peso: float
    altura: float
    descricao_sintomas: str
    observacao_clinica: str
    exame_ids: Sequence[int]
    prescricoes: Sequence[PrescricaoInputDTO]
