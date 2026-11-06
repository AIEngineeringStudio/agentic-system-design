# Module 04 — Agent orchestration, workflows and durable state

**Learning boundary:** Start with bounded actions; introduce explicit state,
checkpoints, compensations and concurrency only when needed.

**One-line mental model:**
`Event/request -> deterministic workflow state -> model/tools -> checkpoint -> outcome`

## Necessary concepts, only when the case needs them

An **agent loop** dynamically chooses steps; a **workflow engine/graph** makes
state transitions explicit. Use durable checkpoints for long processes. *
*Human-in-the-loop** means approval/control by a person at a defined decision
point. Idempotency and reconciliation are necessary when tools have side effects
or outcomes are unknown.

## Patterns and decisions to reuse

- **Primary decision rule:** The model can propose a refund; only authorized
  deterministic code may execute it.
- Start with the baseline boundary and identify source of truth, authority and
  error semantics before selecting products.
- Show one happy path and one failure path, then justify added components as
  responses to constraints.
- Keep code labs small and local with fake records; label production
  architecture as a design, not deployed implementation.

## Problem briefs (these are design prompts, not pre-solved lessons)

### #26 — IT incident investigator ★ anchor

**User need:** Investigate a mock service outage from logs and metrics.

- **Teach on demand:** Tool loops, evidence, stopping rules.
- **Small working lab:** Query mock monitoring tools and create a timeline.
- **Production evolution:** Least-privilege read access, query caps, failures
  and audit.
- **Decision to explain:** Scripted runbook vs autonomous diagnostic loop.

### #27 — Plan-execute research workflow

**User need:** Complete a multi-step research assignment.

- **Teach on demand:** Planner/executor, state graph, checkpoints.
- **Small working lab:** Build plan -> retrieve -> synthesize -> cite.
- **Production evolution:** Resume partial runs and bound plan revisions.
- **Decision to explain:** Static pipeline vs adaptive plan.

### #28 — Refund approval agent ★ anchor

**User need:** Propose a refund with approval before execution.

- **Teach on demand:** HITL, states, idempotency.
- **Small working lab:** Simulate proposal -> user approval -> mock refund.
- **Production evolution:** Approval expiry, amount caps, audit and unknown
  outcomes.
- **Decision to explain:** Approval workflow vs autonomous action.

### #29 — Supplier onboarding agent

**User need:** Onboarding spans documents and departments.

- **Teach on demand:** Durable workflows, timers, callbacks.
- **Small working lab:** Simulate document checks and waiting for review.
- **Production evolution:** Crash resume, cancellations, compensation and SLA.
- **Decision to explain:** Agent loop vs durable workflow engine.

### #30 — Parallel contract comparison

**User need:** Compare several contracts efficiently.

- **Teach on demand:** Fan-out/fan-in and concurrency.
- **Small working lab:** Analyze sample documents and aggregate differences.
- **Production evolution:** Bound parallelism, isolate errors and trace
  evidence.
- **Decision to explain:** Serial vs parallel analysis.

### #31 — Event-triggered operations assistant

**User need:** A monitoring alert triggers an AI investigation.

- **Teach on demand:** Event ingestion, queue, deduplication.
- **Small working lab:** Publish fake alerts and launch controlled
  investigation.
- **Production evolution:** Debounce storms, retry safely and limit authority.
- **Decision to explain:** Human-triggered vs event-triggered workflow.

### #32 — Large batch classification agent

**User need:** Classify a high volume of cases.

- **Teach on demand:** Batching, queueing, routing and backpressure.
- **Small working lab:** Batch route synthetic tickets through model profiles.
- **Production evolution:** Dead letters, spend ceilings, throughput and
  fairness.
- **Decision to explain:** Online interactive vs offline batch execution.

### #33 — Crash-recoverable agent runtime

**User need:** Agent crashes after an external step.

- **Teach on demand:** Checkpointing, retries, action ledger.
- **Small working lab:** Kill and restart a local workflow without repeating
  side effects.
- **Production evolution:** Reconcile unknown action status and checkpoints.
- **Decision to explain:** Replay whole plan vs resume committed steps.

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

**Case IDs in this module:** #26, #27, #28, #29, #30, #31, #32, #33.
