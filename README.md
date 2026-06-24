# Padrões de Software — Atividade 3

Sistema de Consultas e Prontuários Médicos (Dr. Vilegas) — **Arquitetura Hexagonal**.

## Documentação

- [Regras de negócio](regras-de-negocio.md)
- [Projeto Python + FastAPI](sistema_consultas/README.md) — instruções completas de instalação e execução

## Início rápido

```bash
cd sistema_consultas
uv venv && uv sync --all-extras
uv run uvicorn consultas.main:app --reload --app-dir src
```

Branch de desenvolvimento: `python`
