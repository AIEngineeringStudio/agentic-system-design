# Module 04 — Agent orchestration, workflows and durable state

**File:** `sdt-module-04-orchestration.md`  
**IDs:** #26–#33  
**Module learning goal:** Progress from tool loops to durable stateful workflows
with safe approvals and recovery.

## Architectural mental model

`Request -> typed workflow state -> agent/tool steps -> durable outcome`

Use finite state machines for side effects, checkpoints for long runs and
reconciliation for unknown remote results.

## Teaching requirements within this module

Start with the stated business scenario and source of truth. Introduce the
concepts in the **Basics** field only when they unblock the current stage. First
draw the smallest appropriate architecture and implement a safe local mock. Then
show how the named production concern changes it. Do not reveal the reference
final architecture at the beginning of a lesson. Do not quiz the learner. If a
case is marked as an anchor in `sdt-catalog.md`, check whether its individual
anchor file is available; otherwise derive the same depth from this case brief.

## Case briefs

### #26 IT incident investigator [DEEP-DIVE ANCHOR]

- **Problem:** Investigate outages through logs and metrics.
- **Basics at point of use:** Bounded tool loop, evidence, runbooks.
- **Working mock:** Build an incident timeline from mock observability tools.
- **Production evolution:** Read-only access, query budgets, missing evidence
  and stop conditions.
- **Architectural trade-off:** Runbook vs adaptive investigation.

### #27 Plan-execute research workflow

- **Problem:** Plan retrieval then synthesize an answer.
- **Basics at point of use:** Planner/executor, typed state graph.
- **Working mock:** Build plan->retrieve->synthesize->cite with checkpoints.
- **Production evolution:** Bounded revisions, recoverable state and trace
  linking.
- **Architectural trade-off:** Fixed pipeline vs dynamic plan.

### #28 Refund approval agent [DEEP-DIVE ANCHOR]

- **Problem:** Propose a refund but require an approved business action.
- **Basics at point of use:** Human-in-the-loop, state transitions, idempotency.
- **Working mock:** Implement proposed->approved->mock-refunded in a local
  store.
- **Production evolution:** Approval expiry, amount cap, duplicate effect
  prevention.
- **Architectural trade-off:** Automatic agent action vs deterministic approval.

### #29 Supplier onboarding agent

- **Problem:** Coordinate a process over days and departments.
- **Basics at point of use:** Durable execution, callbacks and compensation.
- **Working mock:** Wait for mock document-review signal and resume.
- **Production evolution:** Crash recovery, cancellation, SLA and stuck work.
- **Architectural trade-off:** Agent loop vs workflow engine.

### #30 Parallel contract comparison

- **Problem:** Compare several documents concurrently.
- **Basics at point of use:** Fan-out/fan-in, worker isolation and aggregation.
- **Working mock:** Analyze mock contracts in parallel and compare clauses.
- **Production evolution:** Worker limits, errors and provenance.
- **Architectural trade-off:** Serial vs concurrent workers.

### #31 Event-triggered operations assistant

- **Problem:** Start supervised AI work from monitoring alerts.
- **Basics at point of use:** Event consumption, dedupe and correlation.
- **Working mock:** Trigger mock investigations from a simulated alert stream.
- **Production evolution:** Alert storms, retries, delivery semantics and
  authority.
- **Architectural trade-off:** Chat request vs background event.

### #32 Large batch classification agent

- **Problem:** Process high-volume ticket batches.
- **Basics at point of use:** Queue, throughput, routing and backpressure.
- **Working mock:** Classify synthetic tickets with cheap/fallback routes.
- **Production evolution:** Dead-letter queues, budget caps and fairness.
- **Architectural trade-off:** Interactive vs batch inference.

### #33 Crash-recoverable agent runtime

- **Problem:** Survive a mid-execution failure without repeating writes.
- **Basics at point of use:** Checkpoints, action ledger, reconcile-unknown.
- **Working mock:** Simulate crash/restart before and after mock external calls.
- **Production evolution:** At-least-once effects, idempotency and recovery.
- **Architectural trade-off:** Replay full run vs resume from state.

## Common misconceptions to correct

- Having an AI model in a request path does not automatically require agent
  orchestration.
- A technically valid diagram is not sufficient without authorization, state
  ownership and failure behavior.
- Examples should use synthetic data, explicitly labeled assumptions and local
  runnable behavior where possible.
