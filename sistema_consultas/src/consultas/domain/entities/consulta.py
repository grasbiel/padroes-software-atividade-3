
from __future__ import annotations
from dataclasses import dataclass, replace
from datetime import datetime
from consultas.domain.enums.estado_consulta import EstadoConsulta
from consultas.domain.enums.tipo_atendimento import TipoAtendimento
from consultas.domain.exceptions import InvalidStateTransition
from consultas.domain.value_objects.identificadores import ConsultaId, MedicoId, PacienteId

@dataclass(frozen=True, slots=True)
class Consulta:
    id: ConsultaId
    paciente_id: PacienteId
    medico_id: MedicoId
    data_hora: datetime
    novo_paciente: bool
    tipo_atendimento: TipoAtendimento
    estado: EstadoConsulta = EstadoConsulta.AGENDADA

    @property
    def agendada(self) -> bool:
        return self.estado is EstadoConsulta.AGENDADA

    def marcar_realizada(self) -> Consulta:
        if self.estado is not EstadoConsulta.AGENDADA:
            raise InvalidStateTransition("Somente consultas agendadas podem ser realizadas.")
        return replace(self, estado=EstadoConsulta.REALIZADA)

    def cancelar(self) -> Consulta:
        if self.estado is not EstadoConsulta.AGENDADA:
            raise InvalidStateTransition("Somente consultas agendadas podem ser canceladas.")
        return replace(self, estado=EstadoConsulta.CANCELADA)
