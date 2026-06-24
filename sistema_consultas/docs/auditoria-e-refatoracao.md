# Auditoria do Projeto — Bugs, Lacunas e Plano de Refatoração

Documento gerado para guiar a melhoria do **Sistema de Consultas Médicas** antes da entrega (25/06/2026).

**Data da auditoria:** 24/06/2026  
**Branch:** `python`  
**Stack:** Python 3.14.4, FastAPI, SQLAlchemy, Arquitetura Hexagonal

---

## Resumo executivo

| Verificação | Resultado |
|-------------|-----------|
| `pytest` (8 testes) | Todos passando |
| `mypy --strict` (63 arquivos) | Sem erros |
| Domínio sem frameworks | OK |
| API sobe e responde | OK |
| Fluxo E2E completo na API | **Com falhas** |
| Git | Código ainda não commitado |

A **Etapa 01** está aproximadamente **90% completa**. A **Etapa 02** está **parcialmente implementada** — existe código e documentação, mas a integração no fluxo real da API tem lacunas.

---

## Bugs encontrados

### Bug 1 — `prontuario_id` retorna `0` e receituário vazio

**Severidade:** Crítica  
**Status:** Aberto

#### Sintoma

Após registrar um prontuário via API:

```json
POST /consultas/1/prontuario  →  {"prontuario_id": 0}
GET  /consultas/1/receituario   →  {"itens": []}
```

O receituário deveria listar os medicamentos prescritos (ex.: Paracetamol), mas retorna lista vazia.

#### Causa raiz

Em `RegistrarProntuarioUseCase`, o prontuário é persistido com ID gerado pelo SQLite (autoincrement), mas o use case continua usando o objeto **antes** do flush:

- `proximo_id()` retorna `ProntuarioId(0)` em todos os repositórios SQLAlchemy
- O repositório `salvar()` devolve o prontuário com ID correto, mas o retorno é ignorado
- As prescrições são criadas com `prontuario_id=prontuario.id`, que ainda é `0`
- O use case retorna `int(prontuario.id)` → sempre `0`

**Arquivo:** `src/consultas/application/use_cases/registrar_prontuario.py`

```python
# Problema: usa prontuario.id antes de obter o ID real do banco
prontuario = builder.build()
self._prontuarios.salvar(prontuario)          # retorno ignorado
# ...
prontuario_id=prontuario.id,                   # ainda é 0
# ...
return int(prontuario.id)                      # retorna 0
```

#### Correção sugerida

```python
prontuario_salvo = self._prontuarios.salvar(prontuario)
# usar prontuario_salvo.id nas prescrições e no retorno
return int(prontuario_salvo.id)
```

#### Como validar

1. `rm consultas.db` e subir a API
2. Registrar prontuário com prescrição
3. Verificar `prontuario_id >= 1`
4. `GET /consultas/1/receituario` deve listar os medicamentos

---

### Bug 2 — Notificações não disparam na API

**Severidade:** Alta  
**Status:** Aberto

#### Sintoma

A Etapa 02 documenta notificações como implementadas (`ConsoleNotificador` + Observer), mas ao agendar ou registrar prontuário via HTTP **nenhuma mensagem aparece no console**.

#### Causa raiz

O `main.py` registra o listener em `app.state.event_publisher`:

```python
app.state.event_publisher = InProcessEventPublisher()
app.state.event_publisher.registrar(NotificacaoEventListener(ConsoleNotificador()))
```

Porém o router usa `request_events_publisher()`, que cria um **publisher novo e vazio** a cada request:

**Arquivo:** `src/consultas/adapters/inbound/rest/dependencies.py`

```python
def request_events_publisher() -> InProcessEventPublisher:
    return InProcessEventPublisher()  # sem listeners registrados
```

#### Correção sugerida

Injetar o publisher do `app.state` via `Request`:

```python
def get_event_publisher(request: Request) -> InProcessEventPublisher:
    return request.app.state.event_publisher
```

Atualizar o router para usar `Depends(get_event_publisher)` em vez de `request_events_publisher()`.

#### Como validar

1. Subir a API com `uv run uvicorn consultas.main:app --reload --app-dir src`
2. Agendar uma consulta
3. Verificar mensagem no console: `Consulta X agendada com sucesso.`

---

### Bug 3 — Integração CRM existe mas não é utilizada

**Severidade:** Alta  
**Status:** Aberto

#### Sintoma

`HttpMedicoRegistroProfissionalGateway` está implementado em `adapters/outbound/crm/`, e `docs/evolucao-sistema.md` marca a feature **III** como implementada, mas **nenhum caso de uso chama o gateway**.

#### Causa raiz

A porta `MedicoRegistroProfissionalGateway` foi definida e o adaptador HTTP criado, porém não há injeção nem chamada em `AgendarConsultaUseCase` ou outro fluxo.

#### Correção sugerida

Opção A — integrar no agendamento:

```python
# AgendarConsultaUseCase.__init__ adiciona gateway
# Antes de salvar consulta:
if not await self._crm_gateway.validar_crm(medico):
    raise CrmInvalidoError(...)
```

Opção B — criar `ValidarMedicoPorCrmUseCase` dedicado + endpoint `GET /medicos/{id}/validar-crm`.

> **Nota:** o gateway atual é `async`; os use cases são síncronos. Pode ser necessário um adaptador síncrono stub para manter o domínio simples, ou usar `asyncio.run()` apenas no adaptador inbound.

#### Como validar

1. Chamar agendamento com médico de CRM inválido → deve rejeitar
2. Com CRM válido (ou stub retornando `True`) → deve prosseguir

---

## Lacunas menores (para a apresentação)

Itens que não quebram o sistema, mas enfraquecem a defesa oral ou a nota.

| # | Item | Situação atual | Impacto na apresentação |
|---|------|----------------|-------------------------|
| L1 | **Portas de entrada** (`application/ports/in/`) | Pasta vazia; use cases são classes sem `Protocol` | O PDF cita interfaces como `RegistrarProntuarioUseCase` — vale criar `Protocol` espelhando cada caso de uso |
| L2 | **Cobertura de testes** | 8 testes unitários; faltam `GerarReceituario`, `ListarConsultasDoDia`, fluxo integrado | Demonstra domínio testável, mas não cobre os bugs da API |
| L3 | **Validação de estado da consulta** | `RegistrarProntuarioUseCase` não verifica `estado == AGENDADA` | Consulta cancelada poderia receber prontuário em cenário extremo |
| L4 | **CRUD de Endereço/Plano** | Apenas seed; paciente novo exige `endereco_id` manual | Fluxo da secretária incompleto para cadastro 100% via API |
| L5 | **Versionamento Git** | Código em untracked; sem commit/push | Impede revisão do grupo e entrega formal |
| L6 | **`proximo_id()` sempre retorna 0** | Funciona com autoincrement SQLite, mas é frágil | Se migrar para outro banco ou lógica de ID, pode falhar silenciosamente |

---

## Checklist vs. requisitos do PDF

| Requisito | Status | Observação |
|-----------|--------|------------|
| Arquitetura hexagonal visível (domain / application / adapters) | OK | Estrutura de pastas clara |
| Domínio sem dependência de frameworks | OK | Verificado com grep |
| Modelo de domínio conforme UML | OK | Todas as entidades presentes |
| Casos de uso do PDF | OK | 5 implementados |
| Portas de saída (repositórios) | OK | `Protocol` em `ports/out/` |
| Portas de entrada (interfaces dos use cases) | Parcial | L1 — sem `Protocol` em `ports/in/` |
| Adaptadores REST | OK | 5 endpoints |
| Adaptadores de persistência | OK | SQLAlchemy + in-memory |
| Regra: 1 consulta = 1 prontuário | OK | Testado; duplicata retorna 422 |
| Receituário com medicamentos, dosagem, CRM | Parcial | Bug 1 — itens vazios na API |
| Etapa 02 — 2 features no código | Parcial | Bugs 2 e 3 — estrutura sem integração |
| Etapa 02 — 3 justificativas escritas | OK | `docs/evolucao-sistema.md` |
| Padrões de projeto conscientes | OK | Repository, State, Builder, Factory, Strategy, Observer |
| SOLID demonstrável | OK | DIP nos repositórios; pode reforçar com ports/in |
| README com instruções de execução | OK | `sistema_consultas/README.md` |

---

## Prioridade de correções

Ordem recomendada para refatoração:

### P0 — Crítico (fazer primeiro)

| # | Tarefa | Arquivo(s) principal(is) | Esforço estimado |
|---|--------|--------------------------|------------------|
| 1 | Corrigir ID do prontuário e prescrições após `salvar()` | `registrar_prontuario.py` | ~15 min |
| 2 | Teste de integração: registrar + receituário com itens | `tests/unit/application/` ou `tests/integration/` | ~30 min |

### P1 — Importante (antes da apresentação)

| # | Tarefa | Arquivo(s) principal(is) | Esforço estimado |
|---|--------|--------------------------|------------------|
| 3 | Conectar `app.state.event_publisher` no router | `dependencies.py`, `router.py` | ~15 min |
| 4 | Integrar CRM no fluxo de agendamento | `agendar_consulta.py`, `router.py` | ~45 min |
| 5 | Validar `estado == AGENDADA` antes de registrar prontuário | `registrar_prontuario.py` | ~10 min |

### P2 — Recomendado (melhora a nota)

| # | Tarefa | Arquivo(s) principal(is) | Esforço estimado |
|---|--------|--------------------------|------------------|
| 6 | Criar `Protocol`s em `application/ports/in/` | `ports/in/*.py` | ~30 min |
| 7 | Testes para `GerarReceituario` e `ListarConsultasDoDia` | `tests/unit/application/` | ~45 min |
| 8 | Endpoint ou fluxo para cadastrar endereço de paciente novo | novo use case + router | ~1 h |
| 9 | Commit e push na branch `python` | git | ~10 min |

### P3 — Opcional (polish)

| # | Tarefa | Esforço estimado |
|---|--------|------------------|
| 10 | Substituir `@app.on_event("startup")` por `lifespan` (FastAPI moderno) | ~20 min |
| 11 | Implementar `proximo_id()` com query `MAX(id)+1` ou sequences | ~30 min |
| 12 | Teste E2E automatizado com `httpx.AsyncClient` + `TestClient` | ~1 h |

---

## Roteiro de refatoração sugerido

```
Fase 1 — Corrigir fluxo principal (P0)
  ├── Fix prontuario_id / prescrições
  ├── Teste registrar → receituário
  └── Validar manualmente com curl

Fase 2 — Completar Etapa 02 (P1)
  ├── Fix event publisher na API
  ├── Integrar CRM no agendamento
  └── Validar estado AGENDADA no prontuário

Fase 3 — Fortalecer para apresentação (P2)
  ├── Ports/in com Protocol
  ├── Mais testes
  └── git add + commit + push

Fase 4 — Polish (P3, se houver tempo)
  └── E2E automatizado, lifespan, proximo_id robusto
```

---

## Comandos úteis durante a refatoração

```bash
cd sistema_consultas

# Rodar testes após cada correção
uv run pytest -v

# Tipagem
uv run mypy src

# Teste manual do fluxo
rm -f consultas.db
uv run uvicorn consultas.main:app --reload --app-dir src

# Em outro terminal:
curl http://127.0.0.1:8000/consultas/dia
curl -X POST http://127.0.0.1:8000/consultas/1/prontuario \
  -H "Content-Type: application/json" \
  -d '{"peso":22.5,"altura":1.10,"descricao_sintomas":"Febre","observacao_clinica":"Ok","exame_ids":[1],"prescricoes":[{"medicamento_id":1,"dosagem":"200mg","administracao":"oral","tempo_de_uso":"5 dias"}]}'
curl http://127.0.0.1:8000/consultas/1/receituario
```

---

## Referências

- [regras-de-negocio.md](../../regras-de-negocio.md)
- [evolucao-sistema.md](./evolucao-sistema.md)
- [README do projeto](../README.md)
