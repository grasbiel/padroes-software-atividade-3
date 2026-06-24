
from __future__ import annotations
from datetime import date
from consultas.domain.entities.paciente import Paciente
from consultas.domain.enums.sexo import Sexo
from consultas.domain.exceptions import BusinessRuleViolation
from consultas.domain.value_objects.identificadores import EnderecoId, PacienteId, PlanoSaudeId

class PacienteFactory:
    @staticmethod
    def criar_novo(
        *,
        id: PacienteId,
        nome_crianca: str,
        nome_responsavel: str,
        data_nascimento: date,
        sexo: Sexo,
        endereco_id: EnderecoId,
        telefone_informado: bool,
        plano_saude_id: PlanoSaudeId | None = None,
    ) -> Paciente:
        if not telefone_informado:
            raise BusinessRuleViolation("Paciente novo exige telefone de contato.")
        if not nome_crianca.strip() or not nome_responsavel.strip():
            raise BusinessRuleViolation("Nomes da criança e do responsável são obrigatórios.")
        return Paciente(
            id=id,
            nome_crianca=nome_crianca.strip(),
            nome_responsavel=nome_responsavel.strip(),
            data_nascimento=data_nascimento,
            sexo=sexo,
            endereco_id=endereco_id,
            plano_saude_id=plano_saude_id,
        )
