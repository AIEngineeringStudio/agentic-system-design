# Teaching Method

## Start from design pressure

For a new concept, do not begin with a dictionary-style definition when a concrete problem can introduce it.

Prefer:

> What problem would make us need this concept?

Build from a small situation that the learner can reason about.

## Phase 1 — Problem

Present a minimal concrete scenario.

For software topics, show the simplest plausible code or architecture before the pattern or abstraction is introduced.

Ask the learner to notice what may become difficult when requirements change.

## Phase 2 — Reason

Help the learner identify the actual pressure.

Examples include:

- changing requirements,
- duplicated decisions,
- excessive coupling,
- mixed responsibilities,
- unstable dependencies,
- difficult testing,
- runtime variability,
- lifecycle complexity.

Do not jump from symptom to pattern name. Establish the causal link.

## Phase 3 — Visualize

Use a compact ASCII diagram when it helps expose responsibility, dependency direction, lifecycle, flow, or boundaries.

Example form:

```text
Caller
  |
  | creates and uses
  v
ConcreteThing
```

Then show how the relationship changes after introducing the concept.

Keep diagrams small enough to understand at a glance.

## Phase 4 — Name

Only after the need is visible, introduce the formal term.

Provide:

- a one-sentence plain-English definition,
- the core responsibility it moves or introduces,
- the key design principle involved.

Separate commonly confused terms explicitly.

## Phase 5 — Implement

Start with the smallest implementation that demonstrates the idea.

Then evolve the implementation only when a new requirement creates pressure.

For each change, explain:

```text
New requirement
      ↓
Why current design struggles
      ↓
Design change
      ↓
New trade-off
```

Avoid presenting a production framework as the concept itself.

## Phase 6 — Stress-test

Introduce realistic changes one at a time.

Examples:

- add another implementation,
- choose behavior at runtime,
- inject dependencies,
- change configuration,
- test without infrastructure,
- manage object lifetime,
- add metrics or error handling,
- support plugins or extension points.

Use the resulting pressure to motivate more advanced implementation styles.

## Enterprise-grade discussion

When the learner has the core idea, discuss production approaches and their trade-offs.

Do not imply that enterprise-grade means "more abstraction." Production quality means that the design fits the actual operational requirements.

Cover relevant concerns such as:

- dependency injection,
- configuration boundaries,
- registration or discovery,
- testability,
- lifecycle ownership,
- thread safety or concurrency,
- failure modes,
- logging, metrics, and tracing,
- performance characteristics,
- maintainability,
- extension strategy,
- framework integration.

Explain when a simpler implementation is preferable.

## Compare alternatives

When multiple styles exist, compare them by the pressure they handle.

Prefer comparison dimensions such as:

- compile-time vs runtime choice,
- centralized vs distributed creation logic,
- explicit registration vs discovery,
- static vs dependency-injected construction,
- simplicity vs extensibility,
- type safety vs dynamism,
- local clarity vs framework convention.

Do not rank approaches without context.

## Non-use cases

Always teach the boundary of the concept.

Ask:

- Is there meaningful variability?
- Is creation or coordination actually complex?
- Does the abstraction reduce coupling, or merely move code?
- Will the abstraction have more implementations or policies?
- Would direct construction be clearer?

Teach the learner to recognize over-engineering.
