# Design Pattern Learning Catalog

Read for curriculum planning, “start from the beginning,” or selecting a next
topic. Priorities are learning suggestions for this workspace, not universal
rankings or prerequisites. Teach a requested topic directly after only its
essential prerequisites. Do not display this whole catalog in an ordinary
interactive lesson.

## Suggested main path

1. Foundations: responsibilities, composition, coupling, and dependencies.
2. Strategy → State → Command → Observer.
3. Factory Method → Builder.
4. Adapter → Facade → Decorator → Proxy → Chain of Responsibility.
5. Dependency Injection → Layered Architecture → Service Layer → Repository.
6. Hexagonal / Ports & Adapters → Clean Architecture concepts.
7. Producer/Consumer → Message Queue → Publish/Subscribe → Delivery Semantics
   → Idempotent Consumer → Message Ordering.
8. Timeout → Retry → Circuit Breaker → Cache-Aside.
9. Transactional Outbox → Saga → CQRS; Event Sourcing is an optional extension.

Arrows suggest an instructional order, not a technical dependency. Builder does
not require Factory Method, Facade does not require Adapter, and CQRS does not
require Saga or Event Sourcing. Introduce only prerequisites needed for the
selected example. In particular, cover transactions before Outbox, delivery
semantics before broker recovery patterns, and shared-state races before locks.

## Priority guide

| Family      | Practice deeply                                                                                      | Learn next when relevant                                                                                              | Recognize; implement when needed                   |
|-------------|------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| Behavioral  | Strategy, State, Command, Observer, Chain of Responsibility                                          | Template Method, Iterator                                                                                             | Mediator, Memento, Visitor, Interpreter            |
| Creational  | Factory Method, Builder                                                                              | Abstract Factory                                                                                                      | Prototype, Singleton and its alternatives          |
| Structural  | Adapter, Facade, Decorator, Proxy, Composite                                                         | Bridge                                                                                                                | Flyweight                                          |
| Application | DI, Layered, Service Layer, Hexagonal, Clean concepts, MVC                                           | MVVM for UI work                                                                                                      | MVP                                                |
| Data        | Repository, Cache-Aside                                                                              | Unit of Work, Data Mapper, Active Record, Read Replicas                                                               | Identity Map, Sharding, Shared Database trade-offs |
| Messaging   | Producer/Consumer, Message Queue, Pub/Sub, Delivery Semantics, Idempotent Consumer, Message Ordering | Dead Letter Queue, Competing Consumers                                                                                | Broker-specific mechanisms only when needed        |
| Distributed | Timeout, Retry, Circuit Breaker, Transactional Outbox, Saga, CQRS concepts                           | Bulkhead, Rate Limiting, API Gateway, BFF, Anti-Corruption Layer, Strangler Fig, Database per Service, Event Sourcing | Production adoption depends on the actual problem  |
| Concurrency | Future/Promise, bounded Producer-Consumer, Thread/Worker Pool, Lock/Mutex, Semaphore                 | Read-Write Lock, Reactor, Actor Model                                                                                 | Leader Election                                    |

Priorities live here; topic references provide pressures, labs, and comparisons.
The collection includes object-oriented patterns, architectural approaches,
operational techniques, and concurrency primitives. Explain their scope instead
of presenting them all as the same kind of pattern.
