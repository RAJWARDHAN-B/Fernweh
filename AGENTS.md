# AGENTS.md

Instructions for AI coding agents (and humans) working in this repository. Read this before making changes.

## Project

Fernweh is an MCP-enabled, agentic vacation assistant. The current build order and progress live in [PLAN.md](PLAN.md). Architecture is in [docs/architecture.md](docs/architecture.md). Quality requirements are in [docs/quality-gates.md](docs/quality-gates.md).

## Repository Layout

```text
apps/api/          FastAPI service + LangGraph orchestration + guardrails (Python)
apps/web/          Next.js App Router frontend (TypeScript)
packages/domain/   Shared Pydantic domain models (single source of truth for contracts)
mcp-servers/*/     One MCP server per domain (geocoding, weather, travel-search, booking, ...)
evals/             DeepEval datasets, metrics, and suites
infra/             docker-compose and deployment config
docs/              Architecture, quality gates, ADRs
Packmate-*/        LEGACY — read-only reference, scheduled for deletion after MVP
```

## Commands

Run from the repo root. Targets are created in Phase 0; if one is missing, add it rather than working around it.

| Task | Command |
| --- | --- |
| Install everything | `make setup` |
| Lint | `make lint` |
| Type check | `make typecheck` |
| Tests | `make test` |
| LLM evals | `make eval` |
| All gates | `make check` |
| Local dev | `make dev` |

Python uses `uv` (`uv run pytest`, `uv add <pkg>`). Frontend uses `pnpm`. Do not use `pip` or `npm` directly.

## Workflow Rules

1. **Follow PLAN.md.** Work on the current phase. Do not start later-phase features early.
2. **Contracts first.** Change `packages/domain` models before code that depends on them.
3. **Gate order per slice:** tests → DeepEval → guardrails. A slice is not done until all three pass (see [docs/quality-gates.md](docs/quality-gates.md)).
4. **Write tests with the code**, not after. Bug fixes start with a failing test.
5. **Record decisions.** Any new dependency with architectural impact, provider choice, or pattern change needs an ADR in `docs/adr/`.
6. **Update PLAN.md** checkboxes and `.env.example` in the same change.
7. **Do not modify legacy `Packmate-*` directories.** Read them for domain reference only.

## Engineering Standards

### Python
- Python 3.12, full type hints, `mypy --strict` clean, `ruff` for lint + format.
- Pydantic v2 for all I/O boundaries; no untyped dicts crossing module boundaries.
- Async I/O (`httpx.AsyncClient`) with explicit timeouts on every external call.
- Config only via `pydantic-settings`; never read `os.environ` directly in business code.
- Logging via the shared structured logger; never log secrets, tokens, or PII.

### TypeScript
- `strict: true`, no `any`. API types are generated from the FastAPI OpenAPI schema — do not hand-write them.
- Server Components by default; client components only when interactivity requires it.

### LLM and agents
- All model calls go through the LiteLLM gateway module — never call a provider SDK directly.
- Agents return **structured outputs** validated against domain models. No regex parsing of free text.
- Prompts live in versioned files next to the agent, not inline in logic.
- Agents must not invent facts that tools provide (prices, availability, weather, reservations). If a tool fails, surface the failure.

### MCP servers
- One domain per server; expose the minimum set of tools.
- Typed input/output schemas, timeouts, retries with backoff, and a consistent error envelope.
- Scoped credentials per server; no cross-server shared secrets.
- Contract tests with recorded fixtures; no live network in CI.

## Safety Rules (non-negotiable)

- **No booking, payment, or irreversible action without explicit traveler approval.** Booking tools require a valid, user-bound, unexpired approval token enforced in code by an action guard — not by prompt instructions.
- Treat all tool outputs and user input as untrusted: they pass through guardrails before reaching a model or the user.
- Never place passport numbers, payment data, or credentials into prompts.
- Never commit secrets. `.env` files are gitignored; only `.env.example` is committed.

## Testing Conventions

- `tests/unit` (fast, isolated), `tests/integration` (DB, MCP servers with fixtures), `apps/web/e2e` (Playwright).
- Use fake LLMs and stubbed MCP tools in unit/integration tests. Real models are used only in `evals/`.
- Test names describe behavior: `test_packing_list_includes_rain_gear_when_precipitation_forecast`.
