# Shared concept: messaging, workflows and derived state

Read only when the design uses async boundaries, events, a long-running process, CDC or a derived index.

**Work queue:** distribute tasks to workers with explicit acknowledgements, timeouts, retries, a dead-letter policy and idempotent execution. **Event stream/log:** durable ordered records per relevant key can serve independent consumers and replay; broker semantics vary by product.

**Outbox:** write domain state and publish-intent atomically in one database transaction. A relay publishes the event later. Repeated relay publishes can occur, so consumers need duplicate-safe handling.

**Inbox/idempotent consumer:** record processed event IDs and complete the intended business effect atomically when possible. Deduplicate by the right business key rather than assuming delivery is unique.

**Saga:** coordinates a process that spans independent commit boundaries. Orchestration centralizes progress and visibility; choreography scatters reaction logic across services. Compensation is a new business action, not a magical reversal of an external transaction.

**CDC:** capture committed source changes through database log integration. It can drive read models and ingestion, but source/target schema contracts and replay behavior still matter.

**Derived read models/indexes:** report freshness and replay/rebuild strategy. The source of truth remains the operational system; out-of-order and duplicate events require correct revision/ordering logic.

**Streaming windows:** distinguish event time and processing time. Out-of-order events need watermark/correction rules and a safe definition of dashboard freshness.

## Failure probes

What happens if state commits but event dispatch fails? If a consumer crashes after side effect but before acknowledgement? If messages arrive out of order? If compensations fail or a workflow is stuck?
