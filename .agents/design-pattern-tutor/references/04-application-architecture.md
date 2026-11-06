# Application Architecture

## Layered Architecture

### Lab
Small order API:

```text
HTTP
 ↓
Application Service
 ↓
Domain
 ↓
Persistence
```

Then deliberately create boundary leakage and repair it.

Teach responsibility and dependency flow.

---

## Service Layer

Model use cases such as:
- PlaceOrder
- CancelOrder
- RefundOrder

Avoid a giant "Services" dumping ground.

---

## Dependency Injection

### First
Build object graph manually in `main()` / composition root.

### Then
Optionally show a DI container.

Core lesson:

```text
Dependency Injection != DI framework
```

Teach:
- constructor injection;
- lifetime;
- composition root;
- test substitution.

Warn about service locator.

---

## Repository

Use the [data reference](05-data.md) for the Repository lesson. Here, discuss
only its relationship to the application boundary when needed.

---

## MVC

Teach through a small UI/web flow.

Explain framework variations rather than pretending one MVC interpretation is universal.

---

## MVP

Teach by comparison when relevant to a UI framework/codebase.

---

## MVVM

Teach:
- view model;
- binding;
- observable state;
- testable presentation logic.

---

## Hexagonal Architecture / Ports & Adapters

Treat these as one architectural family.

### Lab
Version A:
domain imports SQL, queue, vendor HTTP SDK.

Version B:

```text
        Application Core
             |
          Ports
       /     |      \
     DB    Queue    Payment
      |      |         |
   Adapters Adapters Adapters
```

Teach dependency direction.

---

## Clean Architecture

Teach after Hexagonal Architecture.

Focus on dependency rule, not folder names.

Question:

> Can business rules execute without HTTP, database, queue, or framework?

If no, inspect dependency direction.

---

## CQRS

Use the [distributed-systems reference](07-distributed-systems.md) after basic
application architecture is understood.
