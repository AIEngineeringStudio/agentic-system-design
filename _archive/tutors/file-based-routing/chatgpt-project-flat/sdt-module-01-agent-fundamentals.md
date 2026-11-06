# Module 01 — Agent fundamentals and application patterns

**File:** `sdt-module-01-agent-fundamentals.md`  
**IDs:** #1–#8  
**Module learning goal:** Identify when a plain model call, structured workflow,
or bounded agent is justified.

## Architectural mental model

`User -> API -> model/structured output -> guarded business response`

Prefer deterministic code for decisions that do not require dynamic tool choice.
Separate model-suggested actions from actual tool execution.

## Teaching requirements within this module

Start with the stated business scenario and source of truth. Introduce the
concepts in the **Basics** field only when they unblock the current stage. First
draw the smallest appropriate architecture and implement a safe local mock. Then
show how the named production concern changes it. Do not reveal the reference
final architecture at the beginning of a lesson. Do not quiz the learner. If a
case is marked as an anchor in `sdt-catalog.md`, check whether its individual
anchor file is available; otherwise derive the same depth from this case brief.

## Case briefs

### #01 FAQ support assistant [DEEP-DIVE ANCHOR]

- **Problem:** Answer a customer's policy question only from approved material.
- **Basics at point of use:** Model input/output, retrieval grounding,
  abstention.
- **Working mock:** Implement a small FAQ-answer endpoint with source IDs.
- **Production evolution:** Restrict sources, track unanswered questions,
  evaluate citations and latency.
- **Architectural trade-off:** Retrieval-backed reply vs autonomous agent.

### #02 Support-ticket triage and routing

- **Problem:** Classify new support tickets into responsible queues.
- **Basics at point of use:** Typed output, JSON schema, deterministic routing.
- **Working mock:** Route synthetic tickets from category/priority JSON to mock
  queues.
- **Production evolution:** Validate classes and permissions, handle unknown
  tickets and measure misroutes.
- **Architectural trade-off:** Rules/classifier vs LLM extraction.

### #03 Order-status tool agent [DEEP-DIVE ANCHOR]

- **Problem:** Answer order status using a live business system.
- **Basics at point of use:** Function calls, tool contracts, agent loop, AuthZ.
- **Working mock:** Call get_order_status(order_id) with fake customer
  identities.
- **Production evolution:** Restrict order ownership server-side, cap tool calls
  and handle timeouts.
- **Architectural trade-off:** Direct API call vs tool-equipped agent.

### #04 Document intake and extraction

- **Problem:** Parse uploaded invoices into structured records.
- **Basics at point of use:** Multimodal extraction, normalization and schema
  validation.
- **Working mock:** Extract fields from synthetic invoices into a local data
  store.
- **Production evolution:** Deduplication, malware/PII handling, confidence and
  human correction.
- **Architectural trade-off:** One-shot model response vs
  extract/validate/correct.

### #05 Read-only analytics copilot

- **Problem:** Convert business questions to governed analytics.
- **Basics at point of use:** Text-to-SQL, semantic layer, query safety.
- **Working mock:** Ask questions of a sandbox SQL database and render
  chart-ready JSON.
- **Production evolution:** Restrict columns/tables, bound queries, audit and
  enforce tenant filters.
- **Architectural trade-off:** Model-generated SQL vs governed metrics APIs.

### #06 Research report generator

- **Problem:** Synthesize a brief from different evidence sources.
- **Basics at point of use:** Query planning, retrieval, citation and synthesis.
- **Working mock:** Build a cited report from local mock sources.
- **Production evolution:** Evidence provenance, source freshness, contradictory
  facts and budget.
- **Architectural trade-off:** Single prompt vs evidence-first pipeline.

### #07 Email draft-and-send assistant

- **Problem:** Draft a reply and send only after user authorization.
- **Basics at point of use:** Action vs suggestion, approval, idempotency.
- **Working mock:** Draft a mock email and simulate approved sending.
- **Production evolution:** Approver/recipient checks, send dedupe and audit.
- **Architectural trade-off:** Autonomous send vs explicit approval.

### #08 Goal-to-task planning assistant

- **Problem:** Decompose a goal into safe executable steps.
- **Basics at point of use:** Planner-executor, iteration budgets, termination.
- **Working mock:** Plan and execute three bounded steps with mock tools.
- **Production evolution:** Loop detection, cost ceilings, retries and
  permission gates.
- **Architectural trade-off:** Static workflow vs agent planning.

## Common misconceptions to correct

- Having an AI model in a request path does not automatically require agent
  orchestration.
- A technically valid diagram is not sufficient without authorization, state
  ownership and failure behavior.
- Examples should use synthetic data, explicitly labeled assumptions and local
  runnable behavior where possible.
