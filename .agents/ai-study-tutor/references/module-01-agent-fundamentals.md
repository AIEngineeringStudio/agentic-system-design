# Module 01 — Agent fundamentals and application patterns

**Learning boundary:** Start with the cheapest justified solution; distinguish
model calls, structured steps, tools and autonomy.

**One-line mental model:**
`Model call -> schema validation -> tool-selected agent -> deterministic action boundary`

## Necessary concepts, only when the case needs them

A **model call** predicts text or structured data; an **agent loop** adds code
that decides how to invoke tools, validate outcomes and stop. **Tool calling**
does not confer authorization. Structured JSON is untrusted until schema and
business invariants are validated. First teach the non-agent solution and add
autonomy only for a named need.

## Patterns and decisions to reuse

- **Primary decision rule:** Use rules/standard application code when business
  decisions are deterministic. Keep tool execution under application control.
- Start with the baseline boundary and identify source of truth, authority and
  error semantics before selecting products.
- Show one happy path and one failure path, then justify added components as
  responses to constraints.
- Keep code labs small and local with fake records; label production
  architecture as a design, not deployed implementation.

## Problem briefs (these are design prompts, not pre-solved lessons)

### #01 — FAQ support assistant ★ anchor

**User need:** Customers ask questions about approved policies.

- **Teach on demand:** Model response, grounding, no-agent baseline.
- **Small working lab:** Answer from a small FAQ with source IDs.
- **Production evolution:** Reject missing evidence; log references and evaluate
  helpfulness.
- **Decision to explain:** Simple retrieval-backed answer vs autonomous agent.

### #02 — Support-ticket triage and routing

**User need:** Turn inbound tickets into typed routes.

- **Teach on demand:** Structured output, confidence, deterministic routing.
- **Small working lab:** Return category and priority JSON and route to a mock
  queue.
- **Production evolution:** Validate all fields, handle ambiguity and add human
  override.
- **Decision to explain:** Rules or classifier vs generative model.

### #03 — Order-status tool agent ★ anchor

**User need:** A user asks about their order.

- **Teach on demand:** Tool calling, read-only authority, tool loops.
- **Small working lab:** Build get_order_status() with a bounded agent loop.
- **Production evolution:** Authorize order ownership, limit calls and trace
  results.
- **Decision to explain:** Direct API access vs tool-access abstraction.

### #04 — Document intake and extraction

**User need:** Convert invoices into validated records.

- **Teach on demand:** Multimodal extraction, schema validation.
- **Small working lab:** Parse synthetic invoices into typed JSON.
- **Production evolution:** Handle duplicates, malware, privacy and manual
  correction.
- **Decision to explain:** One-shot extraction vs staged validation.

### #05 — Read-only analytics copilot

**User need:** Users ask natural-language questions of business data.

- **Teach on demand:** Text-to-SQL, typed metrics, query boundaries.
- **Small working lab:** Query a sandbox SQLite dataset and show a chart.
- **Production evolution:** Enforce row policy, read-only access, timeouts and
  query tracing.
- **Decision to explain:** Model-written SQL vs governed metrics service.

### #06 — Research report generator

**User need:** Create a short evidence-based report.

- **Teach on demand:** Retrieval, synthesis and provenance.
- **Small working lab:** Search mock source documents and cite passages.
- **Production evolution:** Handle contradicting sources, time freshness and
  missing citations.
- **Decision to explain:** Single prompt vs evidence-first pipeline.

### #07 — Email draft-and-send assistant

**User need:** Draft correspondence and send only when approved.

- **Teach on demand:** Side effects, consent, idempotency.
- **Small working lab:** Draft a sample email, show preview and mock send after
  approval.
- **Production evolution:** Reauthorize sender/recipient, prevent duplicate
  sends and audit.
- **Decision to explain:** Autonomous execution vs confirmation gate.

### #08 — Goal-to-task planning assistant

**User need:** Turn a goal into executable safe steps.

- **Teach on demand:** Agent planner, loop budgets, stopping conditions.
- **Small working lab:** Plan three mock steps and execute bounded tool calls.
- **Production evolution:** Control recursion, cost, partial failures and
  authorization.
- **Decision to explain:** Static workflow vs dynamic planner.

## Example baseline diagram for this module

```text
+-----------------------------+
|       User requirement      |
+-----------------------------+
              |
              v
+-----------------------------+
|      Smallest valid flow    |
+-----------------------------+
              |
              v
+-----------------------------+
|    Business source of truth |
+-----------------------------+
```

**Important:** This is only a visual placeholder. Draw the actual components
from the selected case requirements; do not present this as the final
architecture. Keep diagrams connected with solid `+ - |` lines and arrows.

**Case IDs in this module:** #1, #2, #3, #4, #5, #6, #7, #8.
