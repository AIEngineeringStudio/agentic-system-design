# Assessment and Completion

Assess independent design reasoning, not recall of pattern names. Use one
exercise at a time in interactive lessons. A complete guide may collect
self-study exercises but cannot establish the reader's mastery.

## Exercise choices

- **Diagnosis:** give simple code and a change. Ask what varies independently,
  what is coupled, and what the cheapest useful boundary would be.
- **Implementation:** supply a runnable starting example and a new requirement.
  Ask for a refactor; evaluate correctness, dependency direction, testability,
  and unnecessary abstraction. Distinguish the supplied baseline from the
  learner's own modifications when recording evidence.
- **Comparison:** use the relevant neighboring pair: Strategy/State,
  Adapter/Facade, Decorator/Proxy, Factory Method/Abstract Factory,
  Observer/Pub-Sub, Active Record/Data Mapper, Layered/Hexagonal,
  Retry/Circuit Breaker, Saga/distributed ACID transaction, or CQRS/Event Sourcing.
- **Simplification:** show an interface per stable implementation, hidden global
  Singleton, repository with no boundary benefit, unsafe payment retry, or
  unnecessary microservices. Ask for a simpler design and its trade-off.
- **Failure injection:** use a relevant timeout, duplicate/out-of-order message,
  crash after commit, partial saga failure, cache outage, queue backlog, or
  lock contention. Ask the learner to predict and then observe the effect.

## Completion evidence

Mark a pattern complete only after the learner has demonstrated:

1. Diagnosis of the motivating problem, including what stays stable and varies.
2. A working implementation/refactor and tests of relevant behavior.
3. An explanation of the dependency boundary, costs, and when not to use it.
4. A distinction from a nearby pattern or simpler alternative.
5. Adaptation to a fresh requirement without merely copying the worked answer.

A completion challenge can supply fresh code without a pattern label, introduce
a change, then stress the proposed design with another change. Assess the
smallest adequate solution, even when it uses no named pattern. Record missing
evidence as pending; do not claim mastery from a score alone.

## Optional rubric

Use when the learner requests grading or a structured assessment. Score each
observed dimension 0–2: diagnosis, dependency reasoning, simplicity,
correctness, test strategy, trade-offs, comparison, and response to change.
Use 0 for incorrect reasoning, 1 for partial or assisted performance, and 2
for independent correct reasoning. Mark unobserved dimensions as not assessed;
do not fabricate a total out of 16 for an incomplete assessment.

For a fully observed assessment: 0–6 suggests revisiting fundamentals, 7–10
indicates developing understanding, 11–13 indicates competence, and 14–16
indicates strong performance on this exercise. These are tutor feedback bands,
not a validated measurement of general mastery. Use the completion evidence
above to determine checkpoint status.
