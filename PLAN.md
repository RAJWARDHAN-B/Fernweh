# Fernweh Implementation Plan

This is the source of truth for build order and progress. Update checkboxes in the same PR that completes the work.

Related docs: [AGENTS.md](AGENTS.md) · [CONTRIBUTING.md](CONTRIBUTING.md) · [docs/architecture.md](docs/architecture.md) · [docs/quality-gates.md](docs/quality-gates.md) · [docs/adr](docs/adr)

## Confirmed Decisions

| Concern | Choice | ADR |
| --- | --- | --- |
| Backend | Python 3.12, FastAPI, Pydantic v2, managed with `uv` workspaces | [0001](docs/adr/0001-tech-stack.md) |
| Agent orchestration | LangGraph (state graph, checkpointing, human-in-the-loop interrupts) | [0001](docs/adr/0001-tech-stack.md) |
| LLM access | LiteLLM, provider-agnostic, config-driven model + fallback chain | [0001](docs/adr/0001-tech-stack.md) |
| Tool access | MCP servers built with the official `mcp` Python SDK | [0001](docs/adr/0001-tech-stack.md) |
| Frontend | Next.js (App Router), TypeScript (strict), Tailwind CSS, `pnpm` | [0001](docs/adr/0001-tech-stack.md) |
| Persistence | PostgreSQL (SQLite for local dev/tests), SQLAlchemy 2.x, Alembic | [0001](docs/adr/0001-tech-stack.md) |
| Repo layout | Monorepo: `apps/`, `packages/`, `mcp-servers/`, `evals/`, `infra/`, `docs/` | [0001](docs/adr/0001-tech-stack.md) |
| Quality gates | Tests → DeepEval → Guardrails, enforced in CI | [quality-gates](docs/quality-gates.md) |

## Definition of Done (every slice)

A slice is done only when all of the following pass. See [docs/quality-gates.md](docs/quality-gates.md) for thresholds.

1. **Lint and types:** `ruff`, `mypy --strict`, `eslint`, `tsc --noEmit`.
2. **Tests:** unit + integration tests pass with coverage thresholds met; no live network or live LLM calls.
3. **DeepEval:** eval suite for any touched prompt, agent, or graph node meets metric thresholds.
4. **Guardrails:** input, output, and action guards are in place and have their own tests.
5. **Docs:** PLAN.md updated, ADR added for any architectural decision, `.env.example` updated for new config.

---

## Phase 0 — Foundation and Tooling

Goal: an empty but fully wired monorepo where every quality gate runs in CI.

- [ ] Create monorepo skeleton (`apps/api`, `apps/web`, `packages/domain`, `mcp-servers/`, `evals/`, `infra/`)
- [ ] Root `pyproject.toml` as a `uv` workspace; shared `ruff` and `mypy` config
- [ ] `pnpm` workspace for `apps/web`; ESLint, Prettier, `tsc` strict
- [ ] `pre-commit` hooks: ruff, ruff-format, mypy, gitleaks (secret scan), end-of-file/trailing whitespace
- [ ] `Makefile` targets: `setup`, `lint`, `typecheck`, `test`, `eval`, `check` (runs all gates), `dev`
- [ ] Settings via `pydantic-settings`; `.env.example` is the only committed env file
- [ ] Structured logging (JSON) with request/trace IDs; OpenTelemetry hooks stubbed
- [ ] `infra/docker-compose.yml` for Postgres
- [ ] FastAPI app with `/healthz` and `/readyz`, plus tests
- [ ] Next.js app shell with a smoke test (Vitest) and one Playwright test
- [ ] DeepEval harness in `evals/` with a trivial passing eval and a fake/cheap judge option
- [ ] Guardrails harness in `apps/api` (guard registry + a no-op guard with tests)
- [ ] GitHub Actions: `lint` → `test` → `eval` → `guardrails-tests` → `build`; required on PRs

**Exit criteria:** `make check` passes locally and in CI on a clean clone.

## Phase 1 — Packing and Trip Foundation (MVP)

Goal: a traveler describes a trip, gets a weather-aware, editable packing checklist, and can save the trip draft.

### 1.1 Domain contracts
- [ ] `packages/domain`: Pydantic models for `Traveler`, `Trip`, `Destination`, `DateRange`, `Activity`, `Preferences`, `Constraints`, `PackingList`, `PackingItem`, `WeatherSummary`
- [ ] Generate OpenAPI schema → TypeScript types for `apps/web`
- [ ] Property-based tests (Hypothesis) for validation rules (date ranges, traveler counts, etc.)

### 1.2 MCP servers
- [ ] `mcp-servers/geocoding` — resolve destination to coordinates (Open-Meteo Geocoding API)
- [ ] `mcp-servers/weather` — forecast/climate summary for a location and date range (Open-Meteo)
- [ ] Each server: typed tool schemas, timeouts, retries, error envelopes, recorded HTTP fixtures (`respx`), contract tests

### 1.3 Agents and orchestration
- [ ] LiteLLM gateway module: model config, fallback chain, timeouts, token/cost logging
- [ ] LangGraph `trip_coordinator` graph: intake → geocode → weather → packing → review
- [ ] Packing agent returns structured `PackingList` (schema-validated, no free text parsing)
- [ ] Graph unit tests with a fake LLM and stubbed MCP tools

### 1.4 Quality gates for the slice
- [ ] DeepEval: golden dataset (≥ 30 trips across climates, durations, activities, traveler types)
- [ ] DeepEval metrics: packing completeness (G-Eval), weather faithfulness, schema validity, tool correctness
- [ ] Guardrails: prompt-injection and off-topic input guards; PII redaction before LLM calls; output schema + "no invented weather" guard

### 1.5 API and persistence
- [ ] SQLAlchemy models + Alembic migrations for trips and packing lists
- [ ] Endpoints: create trip draft, generate packing list, update checklist items, get trip
- [ ] Integration tests against SQLite and Postgres (Testcontainers or compose in CI)

### 1.6 Web experience
- [ ] Trip intake form (and conversational refinement)
- [ ] Packing checklist view: check/uncheck, add/remove items, weather context panel, export
- [ ] Playwright E2E: create trip → generate list → edit → reload persists

**Exit criteria (MVP):** full flow works end-to-end locally; all gates green in CI.

### 1.7 Legacy cleanup (after MVP sign-off)
- [ ] Confirm all useful packing-domain behavior from PackMate is covered by tests or evals
- [ ] Delete `Packmate-Frontend/` and `Packmate-Streamlit/` in a dedicated PR
- [ ] Rotate any credentials that legacy code may have used
- [ ] Update README repository layout

## Phase 2 — Research and Planning Agents

Goal: researched, comparable travel options and a coordinated itinerary.

- [ ] ADR: select flight, lodging, maps/places, and activity data providers
- [ ] MCP servers: `travel-search` (flights, lodging), `places` (POIs, transit), `destination-knowledge`
- [ ] Normalized result models (price, duration, location, cancellation terms, source, fetched-at)
- [ ] Research agent and itinerary agent as LangGraph subgraphs
- [ ] Recommendation traces: every recommendation cites its tool results and constraints
- [ ] Comparison UI with filters and trade-off explanations
- [ ] DeepEval: faithfulness to tool outputs, itinerary feasibility, constraint adherence
- [ ] Guardrails: no invented prices/availability; source attribution required on output

## Phase 3 — Booking-Ready Workflows

Goal: checkout-ready bookings that execute only after explicit traveler approval.

- [ ] Authentication (ADR: provider choice) and traveler profiles
- [ ] Encrypted storage for sensitive fields; secrets never passed into prompts
- [ ] `booking` MCP server behind an approval token (sandbox providers first)
- [ ] LangGraph interrupt before any irreversible action; approval UI with full summary
- [ ] Booking status, itinerary sync, changes, cancellations, notifications
- [ ] Guardrails: action guard rejects any booking call without a valid, unexpired, user-bound approval
- [ ] DeepEval + red-team suite: attempts to bypass approval, prompt injection via tool outputs

## Phase 4 — Production Hardening

- [ ] Observability dashboards (latency, cost per trip, tool error rates, eval drift)
- [ ] Rate limiting, abuse protection, audit log for all tool and booking actions
- [ ] Scheduled eval runs against production-like data; regression alerts
- [ ] Deployment pipeline and environment promotion (ADR)
