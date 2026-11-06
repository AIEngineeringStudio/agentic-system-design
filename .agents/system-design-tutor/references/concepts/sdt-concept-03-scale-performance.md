# Shared concept: scaling and performance

Read only when the case has meaningful scale, hot keys, large reads, fan-out, real-time connections or overload.

**Begin with workload shape:** read/write ratio, peak factor, object size, top keys, data retention and expected latency. Treat all sample numbers as illustrative unless sourced.

**Replication vs sharding:** replicas commonly help reads and availability but introduce lag; sharding distributes writes/storage but adds cross-shard and rebalancing complexity.

**Caching:** choose cache-aside/write-through based on read freshness, update coupling and invalidation. Specify TTL, stampede prevention, hot-key behavior and what happens when the cache is unavailable.

**Rate limits:** token bucket favors burst tolerance; sliding windows offer different fairness/precision/cost trade-offs. Atomicity, distributed counters, key locality and clock assumptions matter.

**Fan-out:** write-time fan-out reduces per-read cost but amplifies writes for very popular producers; read-time fan-out shifts work to retrieval and can reduce celebrity amplification.

**Realtime push:** WebSocket-style sessions support low-latency bidirectional updates but require connection ownership, presence expiry, reconnect/replay and load management.

**Admission control/backpressure:** rejecting or queuing bounded work protects correctness and tail latency. Blind retries can amplify a partial outage; use bounded retry budgets, jitter and isolation.

## Decision discipline

Add a cache, queue, CDN, partition or multi-region layer only for a demonstrated requirement. State its invalidation, failure, and operating cost.
