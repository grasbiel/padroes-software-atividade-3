
from __future__ import annotations
from datetime import date
from typing import DefaultDict, Sequence
from collections import defaultdict
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

class InMemoryConsultaRepository:
    def __init__(self) -> None:
        self._data: dict[ConsultaId, Consulta] = {}
        self._seq = 0

    def salvar(self, consulta: Consulta) -> Consulta:
        self._data[consulta.id] = consulta
        return consulta

    def obter_por_id(self, consulta_id: ConsultaId) -> Consulta | None:
        return self._data.get(consulta_id)

    def listar_por_dia(self, dia: date) -> Sequence[Consulta]:
        return [c for c in self._data.values() if c.data_hora.date() == dia]

    def proximo_id(self) -> ConsultaId:
        self._seq += 1
        return ConsultaId(self._seq)

class InMemoryPacienteRepository:
    def __init__(self) -> None:
        self._data: dict[PacienteId, Paciente] = {}
        self._seq = 0

    def salvar(self, paciente: Paciente) -> Paciente:
        self._data[paciente.id] = paciente
        return paciente

    def obter_por_id(self, paciente_id: PacienteId) -> Paciente | None:
        return self._data.get(paciente_id)

    def proximo_id(self) -> PacienteId:
        self._seq += 1
        return PacienteId(self._seq)

class InMemoryMedicoRepository:
    def __init__(self, medicos: Sequence[Medico] | None = None) -> None:
        self._data = {m.id: m for m in (medicos or [])}

    def obter_por_id(self, medico_id: MedicoId) -> Medico | None:
        return self._data.get(medico_id)

class InMemoryMedicamentoRepository:
    def __init__(self, itens: Sequence[Medicamento] | None = None) -> None:
        self._data = {m.id: m for m in (itens or [])}

    def obter_por_id(self, medicamento_id: MedicamentoId) -> Medicamento | None:
        return self._data.get(medicamento_id)

    def listar_todos(self) -> Sequence[Medicamento]:
        return list(self._data.values())

class InMemoryExameRepository:
    def __init__(self, itens: Sequence[Exame] | None = None) -> None:
        self._data = {e.id: e for e in (itens or [])}

    def obter_por_id(self, exame_id: ExameId) -> Exame | None:
        return self._data.get(exame_id)

    def listar_todos(self) -> Sequence[Exame]:
        return list(self._data.values())

class InMemoryProntuarioRepository:
    def __init__(self) -> None:
        self._by_id: dict[ProntuarioId, Prontuario] = {}
        self._by_consulta: dict[ConsultaId, ProntuarioId] = {}
        self._by_paciente: DefaultDict[PacienteId, list[ProntuarioId]] = defaultdict(list)
        self._seq = 0
        self._consulta_paciente: dict[ConsultaId, PacienteId] = {}

    def registrar_mapa_consulta_paciente(self, consulta_id: ConsultaId, paciente_id: PacienteId) -> None:
        self._consulta_paciente[consulta_id] = paciente_id

    def salvar(self, prontuario: Prontuario) -> Prontuario:
        self._by_id[prontuario.id] = prontuario
        self._by_consulta[prontuario.consulta_id] = prontuario.id
        paciente_id = self._consulta_paciente.get(prontuario.consulta_id)
        if paciente_id is not None and prontuario.id not in self._by_paciente[paciente_id]:
            self._by_paciente[paciente_id].append(prontuario.id)
        return prontuario

    def obter_por_consulta(self, consulta_id: ConsultaId) -> Prontuario | None:
        pid = self._by_consulta.get(consulta_id)
        return self._by_id.get(pid) if pid else None

    def listar_historico_paciente(self, paciente_id: PacienteId) -> Sequence[Prontuario]:
        return [self._by_id[i] for i in self._by_paciente.get(paciente_id, [])]

    def proximo_id(self) -> ProntuarioId:
        self._seq += 1
        return ProntuarioId(self._seq)

class InMemoryPrescricaoRepository:
    def __init__(self) -> None:
        self._data: dict[ProntuarioId, list[Prescricao]] = defaultdict(list)
        self._seq = 0

    def salvar_varias(self, prescricoes: Sequence[Prescricao]) -> None:
        for p in prescricoes:
            self._data[p.prontuario_id].append(p)

    def listar_por_prontuario(self, prontuario_id: ProntuarioId) -> Sequence[Prescricao]:
        return list(self._data.get(prontuario_id, []))

    def proximo_id(self) -> PrescricaoId:
        self._seq += 1
        return PrescricaoId(self._seq)

class InMemoryTelefoneRepository:
    def __init__(self) -> None:
        self._seq = 0

    def salvar(self, telefone: Telefone) -> Telefone:
        return telefone

    def proximo_id(self) -> TelefoneId:
        self._seq += 1
        return TelefoneId(self._seq)
