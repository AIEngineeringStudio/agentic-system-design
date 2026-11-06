# Module 08 — Evaluation, observability, reliability and operations

**File:** `sdt-module-08-operations.md`  
**IDs:** #58–#65  
**Module learning goal:** Make agent outcomes measurable, traceable, reliable
and affordable in production.

## Architectural mental model

`Request -> traced steps -> measured outcome -> revision/rollout`

Observe task outcomes and model quality, not only HTTP uptime or token counts.

## Teaching requirements within this module

Start with the stated business scenario and source of truth. Introduce the
concepts in the **Basics** field only when they unblock the current stage. First
draw the smallest appropriate architecture and implement a safe local mock. Then
show how the named production concern changes it. Do not reveal the reference
final architecture at the beginning of a lesson. Do not quiz the learner. If a
case is marked as an anchor in `sdt-catalog.md`, check whether its individual
anchor file is available; otherwise derive the same depth from this case brief.

## Case briefs

### #58 Agent tracing and evaluation dashboard [DEEP-DIVE ANCHOR]

- **Problem:** Understand run errors and their cost.
- **Basics at point of use:** Traces, spans, token use and GenAI conventions.
- **Working mock:** Emit mock traces across model and tool calls.
- **Production evolution:** Redact data, correlate distributed spans and retain
  responsibly.
- **Architectural trade-off:** Vendor telemetry vs OpenTelemetry.

### #59 Grounded-answer regression suite

- **Problem:** Prevent prompt changes from breaking factual answers.
- **Basics at point of use:** Golden tests, grounding and grader rubrics.
- **Working mock:** Compare two mock versions on evidence-backed cases.
- **Production evolution:** Representative evals, repeated runs and launch
  gates.
- **Architectural trade-off:** Exact-match vs rubric grading.

### #60 Model gateway and fallback

- **Problem:** Route workload by quality, latency and budget.
- **Basics at point of use:** Model routing, failover and task classes.
- **Working mock:** Simulate two model profiles with routing rules.
- **Production evolution:** Fallback quality, privacy and cost caps.
- **Architectural trade-off:** One model vs tiered selection.

### #61 High-load agent admission control

- **Problem:** Bound concurrent agent work during spikes.
- **Basics at point of use:** Queues, throttles and backpressure.
- **Working mock:** Simulate interactive priority over queued batch requests.
- **Production evolution:** Cancel, expire and fairly allocate tenant capacity.
- **Architectural trade-off:** Unlimited queue vs admission control.

### #62 Replay-safe external actions

- **Problem:** Avoid duplicate business effects on retries.
- **Basics at point of use:** Idempotency, ambiguity and reconciliation.
- **Working mock:** Simulate send/retry after response loss.
- **Production evolution:** Durable action IDs, provider status and audit.
- **Architectural trade-off:** Blind retry vs reconcile.

### #63 Safe prompt and agent rollout

- **Problem:** Change prompts/tools without breaking production.
- **Basics at point of use:** Canary, shadow, backward compatibility.
- **Working mock:** Compare candidate and baseline versions on sample traffic.
- **Production evolution:** Rollback triggers, state migration and schema tests.
- **Architectural trade-off:** Big-bang vs gradual deployment.

### #64 Agent service SLO and on-call

- **Problem:** Define what makes an AI service healthy.
- **Basics at point of use:** Task success, p95, errors, runbooks.
- **Working mock:** Build synthetic task metrics and incident dashboard.
- **Production evolution:** Separate model failures from infra outages, own
  on-call.
- **Architectural trade-off:** HTTP uptime vs task-level success.

### #65 Multi-region agent disaster recovery

- **Problem:** Recover interrupted agent runs after region failure.
- **Basics at point of use:** RPO/RTO, state restore and failover.
- **Working mock:** Recover a fake checkpoint in second region.
- **Production evolution:** Reconcile remote effects, rehearse recovery, secret
  rotation.
- **Architectural trade-off:** Active-passive vs active-active.

## Common misconceptions to correct

- Having an AI model in a request path does not automatically require agent
  orchestration.
- A technically valid diagram is not sufficient without authorization, state
  ownership and failure behavior.
- Examples should use synthetic data, explicitly labeled assumptions and local
  runnable behavior where possible.
