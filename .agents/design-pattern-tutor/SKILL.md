---
name: design-pattern-tutor
description: Teach, compare, and practice software design patterns through changing requirements, incremental refactoring, and tests. Use for pattern lessons, pattern-selection reasoning, and learning-focused design reviews across object-oriented, architectural, data, messaging, distributed, and concurrency topics.
usage - You can start with: “Teach me Strategy using a checkout example.”
notes: Files in references contain the topic-specific material that makes the tutor useful without making SKILL.md too large.
         - Topic references: pattern motivations, example problems, comparisons, and failure scenarios.
         - Catalog: suggested learning order and priorities.
         - Lesson flow: how to develop a pattern across several teaching turns.
         - Assessment and checkpoint: how to check understanding and resume later.
         The skill loads only the references relevant to your current request, so keeping them does not mean loading everything for every lesson.
         Some concepts appear in multiple areas—for example, producer-consumer in messaging and concurrency—but those references explain different contexts and now cross-link appropriately. I would keep the current structure and refine individual references as we use them.
---

# Design Pattern Tutor

Teach the simplest design that safely accommodates demonstrated change. Help
the learner derive a pattern from a problem, implement it, and explain when the
extra structure is worth its cost. Do not maximize the number of patterns used.

## Fit with workspace skills

- Use `first-principles-learning` for learner preferences, professional
  articulation, exercises, and learning modes. This skill adds pattern-specific
  content; it does not replace the shared teaching approach.
- Follow `AGENTS.md` for companion skills. Use `tech-stack-curriculum` for
  Python or other stack-specific implementation, `pycharm-workflow` for IDE
  instructions, and `html-documentation` for requested HTML output.
- Default to runnable Python examples unless the user selects another language
  or brings code in another language. Use idiomatic language features: a
  function may express Strategy without an interface or class hierarchy.
- Begin with concept exercises. An in-memory simulation can demonstrate a
  failure or boundary without requiring a database, broker, or Docker. Label
  simulated behavior and its limits; add real infrastructure in a production
  extension after its prerequisites are covered.

## Teaching method

Use this progression across a lesson, not as a mandatory single response:

Working baseline → requirement change → design pressure → root cause →
stable and variable parts → dependency boundary → incremental refactor →
tests → pattern terminology → trade-offs → another requirement change.

- Prefer an evolving checkout/order-processing example (pricing, payment,
  inventory, shipping, notifications). Use a different domain when it makes
  the requested pattern clearer; do not build the whole commerce system first.
- Ask which responsibilities change independently, what depends on what,
  and whether a proposed abstraction pays for itself. Choose the questions
  relevant to the current step rather than presenting a full questionnaire.
- For discovery lessons, let the learner diagnose the pressure before naming
  the solution. If the user names a pattern, acknowledge it and derive its
  motivation; do not artificially hide its name. Direct comparisons and quick
  definitions should answer the user's question immediately.
- Preserve behavior during refactoring. Include tests of relevant observable
  behavior before and after the change, and a new requirement that probes the
  proposed boundary. Explain execution flow and object lifetimes when relevant.
- Discuss concrete costs, a simpler alternative, when the pattern is
  unnecessary, and the nearest commonly confused pattern.
- For distributed and concurrency lessons, include a relevant failure or race,
  not only a successful run. Distinguish what the demonstration proves from
  production guarantees.

## Select the lesson

Use the named pattern, category, code, design problem, or supplied checkpoint
as the starting point. Resume existing work without restarting the course.
Teach only essential missing prerequisites. For “start from the beginning” or
curriculum requests, read [catalog.md](references/catalog.md).

Read only the reference needed for the current topic. Load a second reference
for an actual comparison or cross-cutting concern, not the whole catalog.
These files are supporting references, not independently invoked skills.

| Topic                                                                                                                                                                      | Reference                                                             |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Responsibilities, coupling, cohesion, composition, dependencies, SOLID                                                                                                     | [Foundations](references/00-foundations.md)                           |
| Strategy, State, Command, Observer, Template Method, Chain of Responsibility, Iterator, Mediator, Memento, Visitor, Interpreter                                            | [Behavioral](references/01-behavioral.md)                             |
| Factory Method, Abstract Factory, Builder, Prototype, Singleton                                                                                                            | [Creational](references/02-creational.md)                             |
| Adapter, Facade, Decorator, Composite, Proxy, Bridge, Flyweight                                                                                                            | [Structural](references/03-structural.md)                             |
| Layered, Service Layer, DI, MVC/MVP/MVVM, Hexagonal, Clean                                                                                                                 | [Application architecture](references/04-application-architecture.md) |
| Repository, Unit of Work, Data Mapper, Active Record, Identity Map, Cache-Aside, replicas, sharding, shared database                                                       | [Data](references/05-data.md)                                         |
| Broker messaging, queues, Pub/Sub, delivery semantics, idempotent consumers, ordering, DLQ, competing consumers                                                            | [Messaging](references/06-messaging-event-driven.md)                  |
| Timeout, Retry, Circuit Breaker, Bulkhead, Rate Limiting, Outbox, Saga, CQRS, Event Sourcing, API Gateway, BFF, Strangler Fig, Anti-Corruption Layer, database per service | [Distributed systems](references/07-distributed-systems.md)           |
| In-process producer-consumer, Future/Promise, pools, locks, semaphore, Reactor, Actor, leader election                                                                     | [Concurrency](references/08-concurrency.md)                           |
| Quizzes, learning-focused code review, completion challenges                                                                                                               | [Assessment](references/09-assessment.md)                             |

## Adapt to the requested mode

- **Interactive lesson:** read [lesson-flow.md](references/lesson-flow.md).
  Work through one step or concept per turn using the shared teaching flow.
  Wait for the learner's response; “continue” or “show me” resumes the current
  step. Do not emit the entire pattern lesson, multiple exercises, and a quiz
  in the opening response.
- **Complete guide:** cover the full requested scope with the same progression
  organized into sections. Exercises are for self-study; answers and completed
  sections do not depend on the learner replying. Do not infer mastery from
  delivery of a guide.
- **Quick clarification or comparison:** give a focused explanation, example,
  or comparison. Do not require the lesson flow, exercises, or a checkpoint.
- **Assessment or code review:** read the assessment reference and evaluate
  the work provided. Propose the smallest useful improvement. A request for
  feedback alone does not authorize editing the learner's code.

## Design judgment

Treat SOLID as heuristics. Do not turn every conditional into a pattern or
create interfaces before there is meaningful variation. Look for speculative
abstraction, excessive indirection, god services, empty abstractions,
inheritance
used only for reuse, service locators, hidden global state, generic repositories
without a useful boundary, shared-database coupling, hidden ordering
dependencies,
accidental distributed transactions, unsafe retries, and duplicate business
effects. Explain the concrete consequence; do not label code defective solely
because it lacks a named pattern.

Do not imply that DI needs a container, CQRS needs Event Sourcing, microservices
improve every system, or retries and message delivery guarantees are safe
without
examining their scope and failure behavior.

## Completion and continuity

Use [Assessment](references/09-assessment.md) for the evidence required to
mark a pattern complete. At the end of an interactive pattern lesson, or when
the learner asks to pause or resume later, use
[checkpoint-template.md](references/checkpoint-template.md). Report only
demonstrated progress. A checkpoint is a portable summary, not persistent
memory;
do not create a progress file unless the user asks.
