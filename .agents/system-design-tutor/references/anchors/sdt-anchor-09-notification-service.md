# Anchor 09 — Notification service

**Catalog case:** 20 — Multi-channel notifications. **Primary module:** `sdt-module-03-scalable-apps.md`. **Optional shared concept:** `sdt-concept-02-messaging-workflows.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Send transactional notifications through multiple delivery channels without letting external vendors slow the originating business operation.

## 2. Functional requirements

Accept notification intent; resolve preferences/templates; enqueue deliveries; retry transient errors; surface terminal status.

## 3. Ranked non-functional constraints

Durable accepted intent, user consent/preferences, bounded retry cost and delivery observability.

## 4. Workload and assumptions

Delivery guarantees of email/SMS/push vendors, user notification policy and time limits must be specified.

## 5. Contracts and error semantics

publish(event_id, user_id, channel_intent); GET /deliveries/{id}; worker-to-provider delivery contract with message_id.

## 6. State model and invariant

NotificationIntent(id, business_event_id, recipient, template, status); Deliveries per channel with attempts and vendor references; preference snapshots.

## 7. Minimum viable architecture (ASCII)

```text
Business service -> Outbox/event stream -> Notification fan-out -> Work queues
                                                       |            |
                                                Preferences DB   Channel workers -> Providers
                                                                       |
                                                                 Delivery ledger
```

## 8. Requirements -> decisions -> trade-offs

1. Use a durable event/outbox to decouple notification from a critical transaction.
2. Separate channels/worker pools so one provider failure does not block others.
3. Choose work queue for attempts and event stream when independent consumers/history are needed.

## 9. Critical execution paths

**Successful flow:** Commit business operation/outbox -> consume -> check preference/template -> enqueue channel jobs -> record provider acknowledgement.

**Failure / retry / recovery:** Consumer redelivery should not create an uncontrolled duplicate. Provider accepted but reply lost is an uncertain outcome; retry behavior depends on provider idempotency and message class.

## 10. Scale, security and enterprise review

**Scale and reliability:** Apply per-provider rate limits, bounded exponential backoff, dead-letter/replay policy and send-latency/undelivered-age metrics.

**Enterprise and operational readiness:** Consent, opt-out, PII minimization, template governance and incident ownership.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

For high-value, legally mandated messages, delivery evidence and escalation requirements may be stronger than for promotional notifications.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
