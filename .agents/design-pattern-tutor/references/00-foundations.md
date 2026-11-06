# Design Foundations

## Goal

Teach the learner to reason about design before learning named patterns.

## Topics

- responsibility
- cohesion
- coupling
- encapsulation
- composition
- abstraction
- dependency direction
- stable vs volatile dependencies
- axes of change
- substitution
- testing seams
- refactoring
- SOLID as heuristics

## Core Exercise

Start with an order checkout function containing:

- pricing
- tax
- shipping
- payment
- notification

Ask the learner to identify which responsibilities change independently.

Do not immediately split everything into interfaces.

First distinguish:
- code that is merely long;
- code that is badly coupled;
- code that has unrelated reasons to change.

## SOLID Teaching

### SRP
Teach as:
> one module should have a coherent reason to change.

Avoid:
> one class must do only one tiny thing.

### OCP
Teach as:
> create extension points only around demonstrated variation.

### LSP
Teach through substitution tests.

### ISP
Teach by showing clients depending on methods they do not need.

### DIP
Teach by drawing dependency arrows before discussing DI containers.

## Exit Criteria

Learner can:
- identify an axis of change;
- distinguish cohesion from coupling;
- explain dependency inversion;
- explain why premature abstraction is harmful.
