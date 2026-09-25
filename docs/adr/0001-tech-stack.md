# ADR 0001: Technology Stack and Repository Layout

- **Status:** Accepted
- **Date:** 2026-09-24

## Context

Fernweh replaces the PackMate prototypes (Create React App site, Streamlit UI, FastAPI endpoint with direct Gemini/Groq calls). The rebuild needs agent orchestration with human-in-the-loop approval, MCP-based tool access, LLM evaluation, and runtime guardrails. The evaluation and guardrails ecosystems (DeepEval, Guardrails AI) are Python-first.

## Decision

| Concern | Choice |
| --- | --- |
| Backend | Python 3.12, FastAPI, Pydantic v2, `uv` workspaces |
| Orchestration | LangGraph |
| LLM access | LiteLLM with config-driven primary model and fallback chain |
| Tools | MCP servers via the official `mcp` Python SDK; consumed through MCP client adapters in LangGraph |
| Frontend | Next.js App Router, TypeScript strict, Tailwind CSS, `pnpm` |
| Persistence | PostgreSQL in deployed environments, SQLite for local/tests; SQLAlchemy 2.x + Alembic |
| Testing | pytest, pytest-asyncio, Hypothesis, respx; Vitest, Playwright |
| Evals | DeepEval |
| Guardrails | Guardrails AI validators + code-level policy guards |
| Layout | Monorepo with `apps/`, `packages/`, `mcp-servers/`, `evals/`, `infra/`, `docs/` |

## Rationale

- **LangGraph** provides explicit state, checkpointing, and interrupts, which map directly to the booking approval requirement.
- **LiteLLM** avoids provider lock-in and keeps the legacy primary/fallback behavior as configuration.
- **Monorepo** keeps domain contracts, API, MCP servers, and evals versioned together, so contract changes and their evals land in one PR.
- **Python backend** aligns with DeepEval, Guardrails AI, the MCP SDK, and the legacy packing logic.

## Consequences

- Two toolchains (`uv` and `pnpm`) must be wired into one `Makefile` and CI pipeline.
- TypeScript API types are generated from OpenAPI; the Python domain package is the single source of truth.
- SQLite/Postgres differences must be covered by running integration tests against both.
