# Sistema de Consultas Médicas

Módulo de **Consultas e Prontuários Médicos** do Dr. Vilegas (pediatra), desenvolvido para a disciplina **Padrões de Software e Refatoração** (IFMA/DComp).

O projeto segue **Arquitetura Hexagonal** (Ports and Adapters), com domínio independente de frameworks, tipagem estática em Python e API REST via FastAPI.

---

## Requisitos

| Ferramenta | Versão | Observação |
|------------|--------|------------|
| Python | >= 3.11 (testado com **3.14.4**) | Já instalado na máquina |
| [uv](https://docs.astral.sh/uv/) | latest | Gerenciador de pacotes e ambientes virtuais |

### Instalar o uv (se ainda não tiver)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env   # adiciona uv ao PATH
uv --version
```

Não é necessário instalar pip, venv ou poetry manualmente — o `uv` cuida de tudo.

---

## Configuração do projeto

```bash
cd sistema_consultas

# 1. Criar ambiente virtual (.venv/)
uv venv

# 2. Instalar dependências (produção + dev: pytest, mypy, ruff)
uv sync --all-extras
```

O ambiente virtual fica em `sistema_consultas/.venv/`. Todos os comandos abaixo usam `uv run`, que ativa o venv automaticamente.

---

## Executar a API

```bash
uv run uvicorn consultas.main:app --reload --app-dir src
```

- API: http://127.0.0.1:8000
- Documentação interativa (Swagger): http://127.0.0.1:8000/docs
- Banco SQLite: `consultas.db` (criado automaticamente no startup)

No primeiro startup, o sistema popula o banco com dados de exemplo:
- Médico: Dr. Vilegas (CRM 12345-MA)
- Paciente: Ana Silva
- Medicamentos: Paracetamol, Amoxicilina
- Exames: Hemograma, Raio-X
- 1 consulta agendada para **hoje às 09:00**

---

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/consultas/dia?dia=YYYY-MM-DD` | Lista consultas do dia (horário, paciente, se é novo) |
| `GET` | `/consultas/{id}/contexto-prontuario` | Histórico de medidas + catálogos de remédios/exames |
| `POST` | `/consultas/{id}/prontuario` | Médico registra prontuário |
| `GET` | `/consultas/{id}/receituario` | Emite receituário com CRM do médico |
| `POST` | `/consultas` | Secretária agenda consulta |

### Exemplos com curl

**Listar consultas de hoje:**

```bash
curl http://127.0.0.1:8000/consultas/dia
```

**Ver contexto para preencher prontuário (consulta id=1):**

```bash
curl http://127.0.0.1:8000/consultas/1/contexto-prontuario
```

**Registrar prontuário:**

```bash
curl -X POST http://127.0.0.1:8000/consultas/1/prontuario \
  -H "Content-Type: application/json" \
  -d '{
    "peso": 22.5,
    "altura": 1.10,
    "descricao_sintomas": "Febre e tosse",
    "observacao_clinica": "Sem alterações na ausculta",
    "exame_ids": [1],
    "prescricoes": [
      {
        "medicamento_id": 1,
        "dosagem": "200mg",
        "administracao": "oral",
        "tempo_de_uso": "5 dias"
      }
    ]
  }'
```

**Gerar receituário:**

```bash
curl http://127.0.0.1:8000/consultas/1/receituario
```

**Agendar nova consulta (paciente existente):**

```bash
curl -X POST http://127.0.0.1:8000/consultas \
  -H "Content-Type: application/json" \
  -d '{
    "paciente_id": 1,
    "medico_id": 1,
    "data_hora": "2026-06-25T14:00:00",
    "tipo_atendimento": "plano",
    "novo_paciente": false
  }'
```

---

## Testes e qualidade

```bash
# Testes unitários (domínio + casos de uso)
uv run pytest -v

# Verificação de tipos (strict mode)
uv run mypy src

# Linter (opcional)
uv run ruff check src tests
```

---

## Arquitetura Hexagonal

```
src/consultas/
├── domain/                  # CORE — regras de negócio (sem frameworks)
│   ├── entities/            # Paciente, Consulta, Prontuario, etc.
│   ├── enums/               # EstadoConsulta, Sexo, TipoAtendimento
│   ├── value_objects/       # IDs tipados, MedidaCorporal
│   ├── factories/           # PacienteFactory (Factory Pattern)
│   ├── builders/            # ProntuarioBuilder (Builder Pattern)
│   ├── strategies/          # Tipo de atendimento (Strategy Pattern)
│   └── events.py            # Eventos de domínio
├── application/             # Casos de uso e portas
│   ├── ports/input/         # Protocols dos casos de uso (portas de entrada)
│   ├── ports/out/           # Repositories + Gateways (Protocol)
│   ├── use_cases/           # 5 casos de uso
│   └── dtos/                # Objetos de transferência
├── adapters/
│   ├── inbound/rest/        # FastAPI (adaptador de entrada)
│   └── outbound/
│       ├── persistence/     # SQLAlchemy + SQLite (adaptador de saída)
│       ├── crm/             # Integração CRM via httpx (Etapa 02)
│       └── notifications/   # Observer + ConsoleNotificador (Etapa 02)
└── main.py                  # Composition root (injeção de dependências)
```

### Fluxo de dependências

```
FastAPI Router → Use Case → Entidades de Domínio
                    ↓
              Repository (Protocol)
                    ↓
         SQLAlchemy Adapter (implementação concreta)
```

O domínio **nunca** importa FastAPI, SQLAlchemy ou Pydantic.

---

## Padrões de projeto aplicados

| Padrão | Onde | Finalidade |
|--------|------|------------|
| **Repository** | `application/ports/out/repositories.py` | Isolar persistência do domínio |
| **State** | `EstadoConsulta` em `Consulta` | Controlar transições agendada → realizada → cancelada |
| **Builder** | `ProntuarioBuilder` | Montar prontuário com prescrições e exames |
| **Factory** | `PacienteFactory` | Criar paciente novo no cadastro inicial |
| **Strategy** | `TipoAtendimento` | Regras diferentes para plano vs particular |
| **Observer** | `InProcessEventPublisher` | Notificações ao agendar/registrar prontuário |
| **Adapter/Gateway** | CRM e notificações | Integração com sistemas externos |

---

## Casos de uso implementados

1. **ListarConsultasDoDia** — exibe consultas do dia para o médico
2. **RegistrarProntuario** — fluxo principal do caso de uso do PDF
3. **ConsultarHistoricoProntuario** — histórico de peso/altura
4. **GerarReceituario** — receita com medicamentos e CRM do médico
5. **AgendarConsulta** — secretária agenda (paciente novo ou existente)

---

## Regras de negócio

- Uma consulta gera **exatamente um** prontuário
- O prontuário pertence exclusivamente à consulta
- Paciente pode ou não ter plano de saúde
- Medicamentos e exames devem estar pré-cadastrados
- Apenas consultas **agendadas** podem receber prontuário

---

## Etapa 02 — Evolução do sistema

Implementado no código:
- **II** — Notificações (Observer + `NotificacaoGateway`)
- **III** — Integração CRM (`MedicoRegistroProfissionalGateway`)

Justificativas das features **I, IV e V** (não implementadas): ver [docs/evolucao-sistema.md](docs/evolucao-sistema.md).

---

## Git — branch python

```bash
# Na raiz do repositório
git add sistema_consultas/
git commit -m "feat: implementação Python com arquitetura hexagonal e FastAPI"
git push -u origin python
```

Abra um PR de `python` → `main` para revisão do grupo.

---

## Referências

- [regras-de-negocio.md](../regras-de-negocio.md) — requisitos consolidados
- PDF da atividade — diagrama UML e critérios de avaliação
