# Contributing

## Prerequisites

- Python 3.12 and [`uv`](https://docs.astral.sh/uv/)
- Node.js LTS and `pnpm`
- Docker (for local Postgres)

## Getting Started

```sh
cp .env.example .env   # fill in local values; never commit .env
make setup
make check
make dev
```

## Branching and Commits

- Trunk-based: short-lived branches off `main`, merged via pull request.
- Branch names: `feat/<scope>-<summary>`, `fix/...`, `chore/...`, `docs/...`.
- Commits follow [Conventional Commits](https://www.conventionalcommits.org/): `feat(api): add packing list endpoint`.

## Pull Requests

Each PR should be one vertical slice or one focused change and must:

- [ ] Pass `make check` (lint, types, tests, evals where applicable, guardrail tests)
- [ ] Include tests for new behavior; bug fixes include a regression test
- [ ] Add or update DeepEval cases when prompts, agents, or model config change
- [ ] Add or update guards when new user input, tool output, or actions are introduced
- [ ] Update [PLAN.md](PLAN.md) progress and `.env.example` for new config
- [ ] Add an ADR in [docs/adr](docs/adr) for architectural decisions

See [docs/quality-gates.md](docs/quality-gates.md) for thresholds and [AGENTS.md](AGENTS.md) for coding standards.

## ADRs

Copy the format of [docs/adr/0001-tech-stack.md](docs/adr/0001-tech-stack.md), number sequentially, and set the status to `Proposed` until the PR merges.
