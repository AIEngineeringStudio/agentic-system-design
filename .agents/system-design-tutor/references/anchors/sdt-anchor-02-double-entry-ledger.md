# Anchor 02 — Double-entry ledger

**Catalog case:** 5 — Double-entry financial ledger. **Primary module:** `sdt-module-02-payments.md`. **Optional shared concept:** `sdt-concept-01-correctness.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Store monetary postings with a complete accounting trail and enforce balanced debits/credits as an indivisible business operation.

## 2. Functional requirements

Post a journal entry; retrieve journal history; produce a balance projection; reverse or correct via new entries; reconcile projections.

## 3. Ranked non-functional constraints

Accounting invariants, transactional durability and audit traceability dominate read speed and availability.

## 4. Workload and assumptions

Currency policy, precision, chart of accounts and posting throughput are domain inputs, not facts to invent.

## 5. Contracts and error semantics

POST /journal-entries with business reference/idempotency key; GET /accounts/{id}/entries; GET /accounts/{id}/balance (with projection freshness).

## 6. State model and invariant

JournalEntry(id, business_ref, posted_at) + Posting(entry_id, account_id, signed_minor_units, currency); for each currency, sum postings = 0 within one transaction; immutable posted journal.

## 7. Minimum viable architecture (ASCII)

```text
Posting API -> Journal service -> Transactional journal DB
                              |
                              +-> Outbox -> Balance projection -> Read API
                              +-> Audit/reconciliation
```

## 8. Requirements -> decisions -> trade-offs

1. Persist immutable postings together rather than updating two independent balances without atomicity.
2. Use a transactional database/constraints for an initial single-boundary ledger.
3. A materialized balance accelerates reads but must be reconstructable and checked against journal totals.

## 9. Critical execution paths

**Successful flow:** Validate accounts/currency -> check balanced batch -> persist entry+postings atomically -> publish change intent -> derive read model.

**Failure / retry / recovery:** On duplicate business reference, replay known result; on partial application, transaction rolls back. On projection failure, journal remains canonical and replay repairs derived balance.

## 10. Scale, security and enterprise review

**Scale and reliability:** Partition only with explicit cross-account/cross-shard posting policy; use per-account sequence/version and monitor lag, unbalanced attempts and reconciliation differences.

**Enterprise and operational readiness:** Define reversal approval, retention, authorization to post, evidence trail, reconciliation ownership and operations for exception handling.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

If transfers span autonomous ledgers, a single local ACID transaction is insufficient; introduce a coordinated protocol and reconciliation with explicit business semantics.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
