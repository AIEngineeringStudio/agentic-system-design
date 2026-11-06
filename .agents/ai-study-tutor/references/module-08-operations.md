# Module 08 — Evaluation, observability, reliability and operations

**Learning boundary:** Treat answer quality, traceability, budgets and recovery
as production requirements.

**One-line mental model:**
`User request -> traced model/tool/workflow -> observed task result`

## Necessary concepts, only when the case needs them

Production reliability requires task-level success measurement, not just healthy
HTTP endpoints. Trace and metrics capture model/tool boundaries; evaluations
test task outcomes and grounding. Rate limits, bounded retries, idempotency
ledgers, canary rollouts and disaster recovery address different failure modes.

## Patterns and decisions to reuse

- **Primary decision rule:** Never present sample capacity, success rates or
  SLOs as facts; label them illustrative.
- Start with the baseline boundary and identify source of truth, authority and
  error semantics before selecting products.
- Show one happy path and one failure path, then justify added components as
  responses to constraints.
- Keep code labs small and local with fake records; label production
  architecture as a design, not deployed implementation.

## Problem briefs (these are design prompts, not pre-solved lessons)

### #58 — Agent tracing and evaluation dashboard ★ anchor

**User need:** Diagnose a broken agent run.

- **Teach on demand:** Traces, spans, outcomes and cost.
- **Small working lab:** Trace synthetic model/tool calls and render a summary.
- **Production evolution:** Redact spans, correlate across MCP/A2A and sample.
- **Decision to explain:** Custom logs vs OpenTelemetry conventions.

### #59 — Grounded-answer regression suite

**User need:** A new prompt may improve one case but break others.

- **Teach on demand:** Golden datasets, grounding and eval criteria.
- **Small working lab:** Compare two mock assistant versions on 30 cases.
- **Production evolution:** Repeated runs, human adjudication and release gates.
- **Decision to explain:** Exact-match tests vs graded evaluation.

### #60 — Model gateway and fallback

**User need:** Route tasks by quality, price and latency.

- **Teach on demand:** Model routing, timeout and fallback.
- **Small working lab:** Use two mock model backends for simple/complex tasks.
- **Production evolution:** Rate/cost caps, privacy and fallback quality.
- **Decision to explain:** One model vs tiered routing.

### #61 — High-load agent admission control

**User need:** Bursts exceed provider quotas.

- **Teach on demand:** Queues, budgets, backpressure.
- **Small working lab:** Prioritize interactive over batch work.
- **Production evolution:** Shed load, tenant fairness, expiration and
  observability.
- **Decision to explain:** Unlimited queues vs admission control.

### #62 — Replay-safe external actions

**User need:** A tool call timed out after an unknown side effect.

- **Teach on demand:** Idempotency and reconciliation.
- **Small working lab:** Simulate duplicate sends after a crash.
- **Production evolution:** Use stable request IDs, action ledger and status
  query.
- **Decision to explain:** Retry blindly vs reconcile before retry.

### #63 — Safe prompt and agent rollout

**User need:** Release new prompts, models and tools gradually.

- **Teach on demand:** Canary, shadow and rollback.
- **Small working lab:** Compare candidate versions on sample traffic.
- **Production evolution:** Gate on task quality, schemas and checkpoint
  compatibility.
- **Decision to explain:** Big-bang vs gradual releases.

### #64 — Agent service SLO and on-call

**User need:** Team needs measurable agent service health.

- **Teach on demand:** Task success, latency, incident response.
- **Small working lab:** Define fake metrics and operational dashboard.
- **Production evolution:** Distinguish infra errors from model failures.
- **Decision to explain:** Uptime metrics vs task-level SLOs.

### #65 — Multi-region agent disaster recovery

**User need:** Region failure interrupts agent execution.

- **Teach on demand:** RPO/RTO, checkpoints and failover.
- **Small working lab:** Restore a mock workflow to a secondary environment.
- **Production evolution:** Reconcile effects, secrets and recovery drills.
- **Decision to explain:** Active/passive vs active/active.

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

**Case IDs in this module:** #58, #59, #60, #61, #62, #63, #64, #65.
