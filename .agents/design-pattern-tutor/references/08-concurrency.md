# Concurrency Patterns and Primitives

The producer-consumer lesson here is in-process. Use the
[messaging reference](06-messaging-event-driven.md) for broker acknowledgement,
redelivery, and cross-process business effects; a local queue does not establish
those guarantees.

## Rule

Concurrency should be taught by first creating a race, resource bottleneck, or scheduling problem.

Do not start from synchronization APIs.

---

## Future / Promise

Teach:
- deferred result;
- success/failure;
- composition;
- cancellation where supported;
- exception propagation.

---

## Producer-Consumer

### Lab

```text
Producer → bounded queue → workers
```

Teach:
- capacity;
- backpressure;
- worker count;
- shutdown;
- failure.

---

## Thread Pool / Worker Pool

Show why unbounded thread/task creation is dangerous.

Measure throughput versus contention conceptually.

---

## Lock / Mutex

First create a race on shared mutable state.

Then add a critical section.

Teach:
- race conditions;
- deadlock;
- lock scope;
- contention.

---

## Semaphore

Use to limit concurrent access to a finite resource.

Example:
at most 10 calls to a fragile external API.

---

## Read-Write Lock

Teach only with a workload where read/write ratios make the trade-off meaningful.

Warn that it is not automatically faster than a normal mutex.

---

## Reactor

Teach when discussing:
- event loops;
- non-blocking I/O;
- network servers.

Focus on readiness events and callbacks/continuations.

---

## Actor Model

Teach:
- isolated mutable state;
- mailbox;
- message passing;
- supervision concepts if relevant.

---

## Leader Election

Use for:
- singleton scheduled jobs;
- clustered coordinators;
- distributed schedulers.

Teach leases/failure detection conceptually before implementation details.
