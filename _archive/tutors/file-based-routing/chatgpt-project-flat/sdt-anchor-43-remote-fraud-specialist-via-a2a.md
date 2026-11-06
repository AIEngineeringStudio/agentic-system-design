# Anchor design #43 — Remote fraud specialist via A2A

**Tutor-only deep reference.** Intended for incremental teaching, not to be
shown in full during Stage 1 unless the learner requests a complete design.

**Primary module:** `sdt-module-06-multi-agent-a2a.md`  
**User scenario:** An internal fraud-review assistant needs a specialist report
produced by an independently deployed agent run by a different team.

## Stage 1 — Actors, constraints and source of truth

- Calling agent: owns user request and intent.
- A2A remote agent: advertises capabilities and owns its tasks and artifacts.
- Policy gateway: checks allowed data disclosure and endpoint trust before
  delegation.

**Priorities to discuss:** correctness and permission boundary first;
interactive latency and complexity second. Ask for missing hard constraints only
when they materially affect design, otherwise state illustrative assumptions
explicitly.

## Stage 2 — Basics introduced only when needed

- Agent Card: metadata advertising remote agent identity/capabilities; untrusted
  until verified.
- A2A task: an independently tracked remote operation, possibly long-running.
- Artifact: task result that must be validated before influencing business
  decisions.

## Stage 3 — Minimal working architecture

```text
+----------------------------+
| Fraud case coordinator     |
+----------------------------+
               |
               v
+----------------------------+
| A2A client + policy check  |
+----------------------------+
               |
               v
+----------------------------+
| Remote specialist agent    |
| Task + result artifact     |
+----------------------------+
```

**Illustrative logical request** (not necessarily literal protocol wire format):

```json
{"remote_capability":"fraud_review","case_id":"CASE-17","scope":"synthetic_summary_only"}
```

**Illustrative logical result**, generated from synthetic data:

```json
{"task_id":"TASK-17","state":"completed","artifact":{"risk_band":"review","evidence_ids":["evidence-1"]}}
```

Explain actor → first authorized boundary → real source of truth → returned
data. Highlight where the model suggests actions but the service decides whether
to execute them.

## Stage 4 — Hands-on lab

Build two independently launched mock services with a capability document and an
asynchronous task/result protocol. Use the current official A2A SDK when
verified; otherwise label the sample a conceptual simulator, not wire-compatible
A2A.

Keep the proof of concept small and runnable; provide exact setup, fixture data,
observable output and a negative or failure test. Do not pretend a prototype is
production-ready, or claim a protocol implementation is official without a
verified SDK.

## Stage 5 — Production evolution (not all at once)

| New constraint                  | Justified change                                                    | Evidence of correct behavior         |
|---------------------------------|---------------------------------------------------------------------|--------------------------------------|
| Agent Card may be spoofed       | Validate endpoint identity and trust policy before delegation.      | Reject unexpected endpoint.          |
| Remote result takes minutes     | Track task IDs, status updates, cancellation and expiry.            | Resume polling after caller restart. |
| Remote artifact is malformed    | Schema-validate artifacts; do not execute text from the specialist. | Malformed result rejected.           |
| Sensitive case facts could leak | Minimize disclosed fields and apply contractual/tenant policy.      | Access and data-minimization tests.  |

**Critical failure to walk through:** A remote specialist advertises support for
privileged payment writes. The coordinator must not grant access based on
metadata alone; allow only approved read-only review task.

## Stage 6 — Architecture judgement

For in-process specialists, function calls or internal handoffs are simpler. A2A
is justified when delegation crosses independently deployed agent/ownership
boundaries.

**Reusable pattern:** begin with a clear source of truth, a bounded action/data
interface and the simplest credible user experience. Add distributed components
only when stated requirements force those boundaries. Show the final production
diagram only once the learner has seen which requirement justified each
addition.
