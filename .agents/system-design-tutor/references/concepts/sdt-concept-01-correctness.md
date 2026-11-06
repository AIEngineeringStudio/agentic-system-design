# Shared concept: correctness and state ownership

Read this only if the requested design needs transactions, concurrency, durable state or financial safety.

## Reason from an invariant

Identify the business outcome that must never be violated before picking storage. Examples: a posted ledger transaction must balance; one seat may have one confirmed owner; a logical authorization must not duplicate its business effect.

**Relational transaction:** local atomic updates and integrity constraints can protect a bounded set of rows. A cross-service call is normally outside that atomic boundary.

**Idempotency:** persist a logical-operation identifier, bind it to validated request content and tenant/actor scope, and replay an appropriate prior response. Specify retention, in-flight duplicate behavior and what a changed payload under the same key means. A retry of an external request must obey that provider's rules.

**Consistency:** strong reads are useful for correctness-critical state; eventually consistent views are useful for derived projections when freshness is disclosed. Do not use an ordinary cache as the authoritative balance.

**Concurrency:** uniqueness constraints, conditional updates, optimistic version checks, or row locks each prevent different races. Choose by contention and critical invariants; consider deadlock and retry behavior.

**Ledger design:** immutable balanced postings and reversal/correction entries create an audit trail; separately materialized balances must reconcile to the journal. Avoid presenting all bookkeeping as identical to card authorization/capture/settlement.

**Unknown outcomes:** a timeout does not prove the downstream action failed. Persist unknown/pending state and perform a permitted status lookup or reconciliation before acting again.

## Questions for the architecture (not learner assessments)

What is the authoritative state? Which writes must be atomic? Which duplicates are possible? What is the safe recovery path if the external system completes the action but response is lost?
