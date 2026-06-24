
from __future__ import annotations
from datetime import date
from typing import Sequence
from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload
from consultas.adapters.outbound.persistence import mappers
from consultas.adapters.outbound.persistence.orm_models import (
    ConsultaModel, ExameModel, MedicamentoModel, MedicoModel, PacienteModel, PrescricaoModel,
    ProntuarioExameModel, ProntuarioModel, TelefoneModel,
)
from consultas.domain.entities.consulta import Consulta
from consultas.domain.entities.exame import Exame
from consultas.domain.entities.medicamento import Medicamento
from consultas.domain.entities.medico import Medico
from consultas.domain.entities.paciente import Paciente
from consultas.domain.entities.prescricao import Prescricao
from consultas.domain.entities.prontuario import Prontuario
from consultas.domain.entities.telefone import Telefone
from consultas.domain.value_objects.identificadores import (
    ConsultaId, ExameId, MedicamentoId, MedicoId, PacienteId, PrescricaoId, ProntuarioId, TelefoneId,
)

class SqlAlchemyConsultaRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def salvar(self, consulta: Consulta) -> Consulta:
        existing = self._session.get(ConsultaModel, int(consulta.id))
        model = mappers.consulta_to_model(consulta)
        if existing:
            existing.estado = model.estado
        else:
            self._session.merge(model)
        self._session.flush()
        return consulta

    def obter_por_id(self, consulta_id: ConsultaId) -> Consulta | None:
        row = self._session.get(ConsultaModel, int(consulta_id))
        return mappers.consulta_to_domain(row) if row else None

    def listar_por_dia(self, dia: date) -> Sequence[Consulta]:
        stmt: Select[tuple[ConsultaModel]] = select(ConsultaModel)
        rows = self._session.scalars(stmt).all()
        return [mappers.consulta_to_domain(r) for r in rows if r.data_hora.date() == dia]

    def proximo_id(self) -> ConsultaId:
        return ConsultaId(0)

class SqlAlchemyPacienteRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def salvar(self, paciente: Paciente) -> Paciente:
        model = PacienteModel(
            id=int(paciente.id) or None, nome_crianca=paciente.nome_crianca,
            nome_responsavel=paciente.nome_responsavel, data_nascimento=paciente.data_nascimento,
            sexo=paciente.sexo.value, endereco_id=int(paciente.endereco_id),
            plano_saude_id=int(paciente.plano_saude_id) if paciente.plano_saude_id else None,
        )
        self._session.add(model)
        self._session.flush()
        return Paciente(id=PacienteId(model.id), **{k: getattr(paciente, k) for k in (
            'nome_crianca','nome_responsavel','data_nascimento','sexo','endereco_id','plano_saude_id'
        )})

    def obter_por_id(self, paciente_id: PacienteId) -> Paciente | None:
        row = self._session.get(PacienteModel, int(paciente_id))
        return mappers.paciente_to_domain(row) if row else None

    def proximo_id(self) -> PacienteId:
        return PacienteId(0)

class SqlAlchemyMedicoRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def obter_por_id(self, medico_id: MedicoId) -> Medico | None:
        row = self._session.get(MedicoModel, int(medico_id))
        return mappers.medico_to_domain(row) if row else None

class SqlAlchemyMedicamentoRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def obter_por_id(self, medicamento_id: MedicamentoId) -> Medicamento | None:
        row = self._session.get(MedicamentoModel, int(medicamento_id))
        return mappers.medicamento_to_domain(row) if row else None

    def listar_todos(self) -> Sequence[Medicamento]:
        return [mappers.medicamento_to_domain(r) for r in self._session.scalars(select(MedicamentoModel)).all()]

class SqlAlchemyExameRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def obter_por_id(self, exame_id: ExameId) -> Exame | None:
        row = self._session.get(ExameModel, int(exame_id))
        return mappers.exame_to_domain(row) if row else None

    def listar_todos(self) -> Sequence[Exame]:
        return [mappers.exame_to_domain(r) for r in self._session.scalars(select(ExameModel)).all()]

class SqlAlchemyProntuarioRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def salvar(self, prontuario: Prontuario) -> Prontuario:
        model = ProntuarioModel(
            id=int(prontuario.id) or None, consulta_id=int(prontuario.consulta_id),
            peso=prontuario.peso, altura=prontuario.altura,
            descricao_sintomas=prontuario.descricao_sintomas, observacao_clinica=prontuario.observacao_clinica,
        )
        self._session.add(model)
        self._session.flush()
        for eid in prontuario.exame_ids:
            self._session.add(ProntuarioExameModel(prontuario_id=model.id, exame_id=int(eid)))
        self._session.flush()
        return Prontuario(id=ProntuarioId(model.id), consulta_id=prontuario.consulta_id, peso=prontuario.peso, altura=prontuario.altura, descricao_sintomas=prontuario.descricao_sintomas, observacao_clinica=prontuario.observacao_clinica, exame_ids=prontuario.exame_ids)

    def obter_por_consulta(self, consulta_id: ConsultaId) -> Prontuario | None:
        stmt = select(ProntuarioModel).where(ProntuarioModel.consulta_id == int(consulta_id)).options(
            selectinload(ProntuarioModel.exames)
        )
        row = self._session.scalars(stmt).first()
        return mappers.prontuario_to_domain(row) if row else None

    def listar_historico_paciente(self, paciente_id: PacienteId) -> Sequence[Prontuario]:
        stmt = (
            select(ProntuarioModel)
            .join(ConsultaModel, ConsultaModel.id == ProntuarioModel.consulta_id)
            .where(ConsultaModel.paciente_id == int(paciente_id))
            .options(selectinload(ProntuarioModel.exames))
        )
        return [mappers.prontuario_to_domain(r) for r in self._session.scalars(stmt).all()]

    def proximo_id(self) -> ProntuarioId:
        return ProntuarioId(0)

class SqlAlchemyPrescricaoRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def salvar_varias(self, prescricoes: Sequence[Prescricao]) -> None:
        for p in prescricoes:
            self._session.add(PrescricaoModel(
                id=int(p.id) or None, prontuario_id=int(p.prontuario_id), medicamento_id=int(p.medicamento_id),
                dosagem=p.dosagem, administracao=p.administracao, tempo_de_uso=p.tempo_de_uso,
            ))
        self._session.flush()

    def listar_por_prontuario(self, prontuario_id: ProntuarioId) -> Sequence[Prescricao]:
        stmt = select(PrescricaoModel).where(PrescricaoModel.prontuario_id == int(prontuario_id))
        return [mappers.prescricao_to_domain(r) for r in self._session.scalars(stmt).all()]

    def proximo_id(self) -> PrescricaoId:
        return PrescricaoId(0)

class SqlAlchemyTelefoneRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def salvar(self, telefone: Telefone) -> Telefone:
        self._session.add(TelefoneModel(
            id=int(telefone.id) or None, numero=telefone.numero, tipo=telefone.tipo.value,
            paciente_id=int(telefone.paciente_id),
        ))
        self._session.flush()
        return telefone

    def proximo_id(self) -> TelefoneId:
        return TelefoneId(0)
