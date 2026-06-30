
from __future__ import annotations

from datetime import datetime

from fastapi.testclient import TestClient

from consultas.main import app


def test_fluxo_registrar_prontuario_e_receituario() -> None:
    with TestClient(app) as client:
        agendar = client.post(
            "/consultas",
            json={
                "paciente_id": 1,
                "medico_id": 1,
                "data_hora": datetime(2099, 12, 31, 15, 0).isoformat(),
                "tipo_atendimento": "plano",
                "novo_paciente": False,
            },
        )
        assert agendar.status_code == 200
        consulta_id = agendar.json()["consulta_id"]

        resp = client.post(
            f"/consultas/{consulta_id}/prontuario",
            json={
                "peso": 22.5,
                "altura": 1.10,
                "descricao_sintomas": "Febre",
                "observacao_clinica": "Sem alterações",
                "exame_ids": [1],
                "prescricoes": [
                    {
                        "medicamento_id": 1,
                        "dosagem": "200mg",
                        "administracao": "oral",
                        "tempo_de_uso": "5 dias",
                    }
                ],
            },
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["prontuario_id"] >= 1

        receita = client.get(f"/consultas/{consulta_id}/receituario").json()
        assert receita["nome_medico"] == "Dr. Vilegas"
        assert receita["crm"] == "12345-MA"
        assert len(receita["itens"]) == 1
        assert receita["itens"][0]["medicamento"] == "Paracetamol"
