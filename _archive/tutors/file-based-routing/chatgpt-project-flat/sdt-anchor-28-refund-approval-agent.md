# Anchor design #28 — Refund approval agent

**Tutor-only deep reference.** Intended for incremental teaching, not to be
shown in full during Stage 1 unless the learner requests a complete design.

**Primary module:** `sdt-module-04-orchestration.md`  
**User scenario:** A support assistant proposes refunds for valid claims, but an
actual refund is a high-impact business operation that requires separate
authorization.

## Stage 1 — Actors, constraints and source of truth

- Agent: prepares a recommendation; cannot move money.
- Approval workflow: binds reviewer, amount, recipient and expiry to a draft.
- Refund service: checks authorization, idempotency and provider outcome.

**Priorities to discuss:** correctness and permission boundary first;
interactive latency and complexity second. Ask for missing hard constraints only
when they materially affect design, otherwise state illustrative assumptions
explicitly.

## Stage 2 — Basics introduced only when needed

- Human-in-the-loop: user or reviewer approves a specific proposed effect.
- Idempotency: retries of the same logical operation do not create a second
  refund.
- Unknown outcome: a timeout after a remote call does not prove it failed.

## Stage 3 — Minimal working architecture

```text
+--------------------------+
|  Agent refund proposal   |
+--------------------------+
              |
              v
+--------------------------+
| Stored pending request   |
+--------------------------+
              |
              v
+--------------------------+
| Human approval           |
+--------------------------+
              |
              v
+--------------------------+
| AuthZ + mock refund tool |
+--------------------------+
              |
              v
+--------------------------+
| Audited outcome          |
+--------------------------+
```

**Illustrative logical request** (not necessarily literal protocol wire format):

```json
{"action":"propose_refund","order_id":"O-17","amount":25,"currency":"USD"}
```

**Illustrative logical result**, generated from synthetic data:

```json
{"proposal_id":"P-17","state":"pending_approval","operation_id":"refund-O-17-v1"}
```

Explain actor → first authorized boundary → real source of truth → returned
data. Highlight where the model suggests actions but the service decides whether
to execute them.

## Stage 4 — Hands-on lab

Store synthetic refund proposals in SQLite. Provide explicit approve/reject
actions and a mock provider that sometimes times out. Use one stable operation
ID for each approved refund, with reconciliation before retry.

Keep the proof of concept small and runnable; provide exact setup, fixture data,
observable output and a negative or failure test. Do not pretend a prototype is
production-ready, or claim a protocol implementation is official without a
verified SDK.

## Stage 5 — Production evolution (not all at once)

| New constraint                      | Justified change                                                               | Evidence of correct behavior             |
|-------------------------------------|--------------------------------------------------------------------------------|------------------------------------------|
| Approval is altered after a preview | Bind approval to frozen order/amount/recipient and expire it.                  | Modified proposal denied.                |
| Provider response is lost           | Record `unknown` and query provider status before a replay.                    | Only one logical refund despite retries. |
| Refund exceeds policy               | Business service enforces approver role, amount limits and refund eligibility. | Unauthorized amount denied.              |
| Audit must survive worker restarts  | Persist state transitions and correlation IDs in an append-only history.       | Crash/restart timeline reconstructed.    |

**Critical failure to walk through:** The provider returns no response after
processing. Do NOT mark it failed and repeat automatically; mark `unknown`,
reconcile, and then choose the next step.

## Stage 6 — Architecture judgement

Use deterministic state transitions around the side effect, even when an agent
determines the proposal. An agent loop alone is a poor replacement for a
payment/refund workflow.

**Reusable pattern:** begin with a clear source of truth, a bounded action/data
interface and the simplest credible user experience. Add distributed components
only when stated requirements force those boundaries. Show the final production
diagram only once the learner has seen which requirement justified each
addition.
