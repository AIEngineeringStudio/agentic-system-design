# Anchor 03 — Settlement and reconciliation

**Catalog case:** 3 — Capture, clearing and settlement. **Primary module:** `sdt-module-02-payments.md`. **Optional shared concept:** `sdt-concept-02-messaging-workflows.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Move completed authorization/capture activity through clearing/settlement-related exchanges and detect differences between internal and external records.

## 2. Functional requirements

Receive capture/clearing evidence; produce or receive settlement batches; match external records; record exceptions; retry safe reprocessing.

## 3. Ranked non-functional constraints

Money movement correctness, reconciliation completeness and auditability over real-time UX.

## 4. Workload and assumptions

The precise network and partner settlement semantics are integration-specific; use them only if supplied or verified.

## 5. Contracts and error semantics

Batch/event intake with batch_id, record_id and source; settlement status query; operator exception workflow; file receipt/ack status.

## 6. State model and invariant

Canonical transaction/capture records; batch manifests; external line items; reconciliation matches; exceptions with ownership and resolution history.

## 7. Minimum viable architecture (ASCII)

```text
Capture records ---> Clearing/settlement workflow -> External partner/files
        |                        |                 |
        +--> Internal ledger ----+--> Matching engine <--+
                                      |
                                 Exception queue
```

## 8. Requirements -> decisions -> trade-offs

1. Keep authorization, capture, clearing and settlement as distinct states.
2. Use durable batches/events instead of stretching one synchronous transaction across organizations.
3. Reconcile independent records by stable business references and amount/currency, not only arrival order.

## 9. Critical execution paths

**Successful flow:** Capture approved -> prepare outbound batch -> exchange with partner -> receive acknowledgements and bank/network evidence -> match -> mark reconciled.

**Failure / retry / recovery:** Missing, duplicate or late lines enter a typed exception queue. Reprocessing must not generate duplicate postings. Unmatched money must remain visible to operators.

## 10. Scale, security and enterprise review

**Scale and reliability:** Partition matching by business key/batch where safe; enforce retention and watermarks for late data; measure unmatched value, age and completion rates.

**Enterprise and operational readiness:** Protect regulated data, maintain immutable evidence, make back-office ownership and manual escalation explicit, document partner cutover and recovery.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

If partner sends real-time events, ingest them as evidence but do not remove the independent reconciliation control.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
