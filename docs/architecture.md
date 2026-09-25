# Architecture

## System Overview

```mermaid
flowchart TD
	web[apps/web - Next.js] -->|REST + SSE| api[apps/api - FastAPI]
	api --> guardsIn[Input guards]
	guardsIn --> graph[LangGraph trip coordinator]
	graph --> gateway[LiteLLM gateway]
	graph --> mcpClient[MCP client adapters]
	mcpClient --> geo[mcp-servers/geocoding]
	mcpClient --> weather[mcp-servers/weather]
	mcpClient --> search[mcp-servers/travel-search]
	mcpClient --> actionGuard[Action guard]
	actionGuard --> booking[mcp-servers/booking]
	graph --> guardsOut[Output guards]
	guardsOut --> api
	api --> db[(PostgreSQL)]
	graph --> checkpoints[(LangGraph checkpoints)]
```

## Components

| Component | Responsibility |
| --- | --- |
| `apps/web` | Trip intake, conversational refinement, checklist editing, comparison and approval UI |
| `apps/api` | HTTP API, auth, persistence, guard registry, graph execution, streaming responses |
| LangGraph coordinator | Routes work to specialized agents as subgraphs; holds trip state; pauses at approval interrupts |
| LiteLLM gateway | Single entry point for model calls; model selection, fallback chain, timeouts, cost logging |
| MCP servers | Bounded, typed access to one external domain each; own their credentials |
| `packages/domain` | Pydantic models shared by API, agents, and MCP servers; source for OpenAPI → TS types |
| `evals/` | DeepEval datasets and suites; not imported by runtime code |

## Agents (LangGraph subgraphs)

| Agent | Phase | Tools |
| --- | --- | --- |
| Trip coordinator | 1 | Delegates to subgraphs |
| Packing agent | 1 | geocoding, weather |
| Preference/profile agent | 2 | profile store |
| Research agent | 2 | travel-search, places |
| Itinerary agent | 2 | places, destination-knowledge, weather |
| Approval and booking agent | 3 | booking (behind action guard) |

## Key Flows

### Phase 1 packing flow
1. Web submits trip intake → API validates against domain models.
2. Input guards run (injection, off-topic, PII redaction).
3. Coordinator geocodes destination, fetches weather via MCP.
4. Packing agent produces a structured `PackingList`.
5. Output guards validate schema and weather faithfulness.
6. API persists trip draft and list; web renders editable checklist.

### Phase 3 booking approval
1. Booking agent prepares a checkout-ready selection.
2. Graph hits an interrupt; API returns an approval request with a full summary.
3. Traveler approves in the UI → API issues a short-lived, user-bound approval token.
4. Graph resumes; action guard verifies the token before the booking MCP tool runs.
5. Every step is written to the audit log.

## Cross-Cutting Concerns

- **Config:** `pydantic-settings`, environment-driven; `.env.example` documents every variable.
- **Observability:** structured JSON logs, trace IDs across API → graph → MCP, OpenTelemetry-ready.
- **Security:** secrets per MCP server, encrypted sensitive fields, no sensitive data in prompts, OWASP-aligned API defaults (CORS allow-list, input size limits, rate limits).
- **Failure handling:** tool errors propagate as typed errors to the graph and are shown to the user; agents never fabricate substitutes.
