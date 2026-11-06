# Creational Patterns

## Factory Method

### Pressure
Construction/selection logic is spread across callers.

### Lab
Select shipping/payment implementation by configuration.

Start with a simple factory function if selection is the only problem. To
derive the classic Factory Method, add a creator workflow whose subclasses
customize the product-construction method. Do not call every helper that
returns an object the classic Factory Method pattern; compare the two forms
and use the simpler one when it meets the requirement.

### Derive
Separate:
- selecting/constructing;
- using.

### Compare
Factory Method vs Abstract Factory vs simple constructor function.

### Stress change
Add a provider requiring credentials/configuration.

---

## Builder

### Pressure
Construction has many optional parameters, invariants, or ordered steps.

### Lab
Build a complex `Report` or `HttpRequest`.

### Compare
Builder vs giant constructor vs named parameters vs factory.

### Stress change
Add validation that depends on multiple fields.

---

## Abstract Factory

### Pressure
Need related families of objects that must be mutually compatible.

### Lab
Cloud/local infrastructure family:

```text
InfrastructureFactory
  ├─ Storage
  ├─ Queue
  └─ Clock
```

Families:
- AWS
- Local test environment

### Compare
Factory Method creates one product abstraction.
Abstract Factory creates a compatible product family.

---

## Prototype

Teach when copying configured/expensive objects is more natural than reconstructing them.

Discuss shallow vs deep copy.

---

## Singleton

### Lab
Implement a global configuration/logger singleton.

Then expose its problems:
- hidden dependency;
- global mutable state;
- tests coupled by state;
- lifecycle ambiguity.

Then replace usage with Dependency Injection and an application-level singleton lifetime.

Key lesson:
Singleton *lifetime* is not the same as the classic Singleton pattern.
