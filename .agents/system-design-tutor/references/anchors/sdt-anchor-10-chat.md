# Anchor 10 — Chat

**Catalog case:** 23 — WhatsApp-style chat. **Primary module:** `sdt-module-03-scalable-apps.md`. **Optional shared concept:** `sdt-concept-03-scale-performance.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Support one-to-one or group chat with responsive delivery, durable messages and eventual pickup on disconnected devices.

## 2. Functional requirements

Connect/authenticate; send message; sync history; receive acknowledgements; reconnect and retrieve missed messages.

## 3. Ranked non-functional constraints

Stable per-conversation ordering, durable delivery semantics and responsive online UX.

## 4. Workload and assumptions

Group size, cross-device guarantees, encryption model and message retention must be defined.

## 5. Contracts and error semantics

Connect via WebSocket-like session; send(conversation_id, client_msg_id, body); history(cursor); ack(server_msg_id).

## 6. State model and invariant

Conversations/membership; Messages(conversation_id, server_sequence, client_msg_id, body); device delivery cursor; ephemeral presence.

## 7. Minimum viable architecture (ASCII)

```text
Chat clients <-> Connection gateways -> Chat write service -> Message DB
                           |                      |
                        Session routing        Event fan-out -> device streams
                                                 |
                                           Offline sync/read API
```

## 8. Requirements -> decisions -> trade-offs

1. Persistent sockets reduce poll overhead for frequent updates; polling remains simpler for infrequent updates.
2. Order messages per conversation using assigned sequence or partition owner, not a fictitious global order.
3. Store durable history separately from ephemeral presence/connection state.

## 9. Critical execution paths

**Successful flow:** Authenticate/membership -> assign unique message/sequence -> commit -> fan-out online -> offline devices resume by cursor.

**Failure / retry / recovery:** Client retries with same message ID deduplicate. Disconnected client replays from persisted cursor; slow consumer triggers bounded queue/backpressure.

## 10. Scale, security and enterprise review

**Scale and reliability:** Partition by conversation while guarding celebrity-size groups, use connection gateway routing and limit fan-out amplification.

**Enterprise and operational readiness:** Abuse reports, identity authorization, data retention, privacy controls, monitoring and incident readiness.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

End-to-end encryption changes server indexing, moderation, key distribution and device synchronization significantly.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
