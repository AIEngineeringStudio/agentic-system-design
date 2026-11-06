# Anchor design #73 — Unified enterprise agentic platform

**Tutor-only deep reference.** Intended for incremental teaching, not to be
shown in full during Stage 1 unless the learner requests a complete design.

**Primary module:** `sdt-module-09-advanced-ai.md`  
**User scenario:** An enterprise wants several independent AI products to reuse
approved tools, host different UI styles, and delegate to specialized agent
services without sacrificing governance.

## Stage 1 — Actors, constraints and source of truth

- Control plane: identities, registries, policy, model/tool releases and tenant
  budgets.
- Runtime/data plane: agent workflows, MCP tool services, optional A2A
  delegation and business APIs.
- Experience plane: owned web frontends, compatible conversational hosts and
  approved UI components.

**Priorities to discuss:** correctness and permission boundary first;
interactive latency and complexity second. Ask for missing hard constraints only
when they materially affect design, otherwise state illustrative assumptions
explicitly.

## Stage 2 — Basics introduced only when needed

- Control plane vs data plane: governance/configuration differs from live
  execution.
- MCP and A2A: different tool/client and remote-agent integration boundaries.
- Observability/evaluation: measure task outcomes, cost and incidents across
  execution boundaries.

## Stage 3 — Minimal working architecture

```text
+---------------------------+
|   Operator / web UI       |
+---------------------------+
              |
              v
+---------------------------+
|   One bounded agent       |
+---------------------------+
              |
              v
+---------------------------+
| Two approved read tools   |
+---------------------------+
```

**Illustrative logical request** (not necessarily literal protocol wire format):

```json
{"request":"Investigate incident INC-42","actor":"operator-5","tenant":"company-A"}
```

**Illustrative logical result**, generated from synthetic data:

```json
{"run_id":"RUN-42","status":"needs_review","evidence":["metric-7","change-3"],"next_action":"operator_approval"}
```

Explain actor → first authorized boundary → real source of truth → returned
data. Highlight where the model suggests actions but the service decides whether
to execute them.

## Stage 4 — Hands-on lab

Start with one incident agent and two synthetic monitoring tools. Add a simple
event timeline and one mock remote specialist; document which integration is
MCP, which is A2A, and which can remain direct APIs. Build no platform-wide
microservices until justified.

Keep the proof of concept small and runnable; provide exact setup, fixture data,
observable output and a negative or failure test. Do not pretend a prototype is
production-ready, or claim a protocol implementation is official without a
verified SDK.

## Stage 5 — Production evolution (not all at once)

| New constraint                                 | Justified change                                                                     | Evidence of correct behavior               |
|------------------------------------------------|--------------------------------------------------------------------------------------|--------------------------------------------|
| Many teams need tool interoperability          | Introduce a governed MCP catalog and ownership/version review.                       | Contract/version compatibility checks.     |
| Some agents are independently deployed         | Introduce A2A only across these autonomous service boundaries.                       | Task lifecycle and artifact validation.    |
| Different UI hosts need different experiences  | Use first-party frontend events or embedded host apps selectively; support fallback. | Host capability and accessibility tests.   |
| High-impact actions need governance            | Central policy design with service-side enforcement, approvals and audit.            | Unauthorized action and crash/retry tests. |
| Operations and model changes cause regressions | Trace requests end to end and gate releases with scenario evals.                     | Task-level success metrics and rollback.   |

**Critical failure to walk through:** A request crosses an MCP tool, an external
A2A specialist and an app UI, then times out mid-action. Retain run/task/action
IDs, reconcile remote effects, show honest status and keep policy enforcement
within each business service.

## Stage 6 — Architecture judgement

A central platform is valuable for shared identity, reusable tool governance,
tracing and deployment standards. Product teams should still own business
semantics and source-of-truth APIs. Avoid turning platform abstractions into
mandatory layers for every app.

**Reusable pattern:** begin with a clear source of truth, a bounded action/data
interface and the simplest credible user experience. Add distributed components
only when stated requirements force those boundaries. Show the final production
diagram only once the learner has seen which requirement justified each
addition.
