# Structural Patterns

## Adapter

### Pressure
A useful component exposes an incompatible interface.

### Lab
Application expects:

```text
PaymentGateway.charge()
```

Vendor SDK exposes:

```text
VendorClient.createTransaction()
```

Wrap with an adapter.

### Stress change
Replace vendor without changing domain/application code.

---

## Facade

### Pressure
A subsystem has too many entry points and orchestration details leak to callers.

### Lab
Checkout façade over:
- inventory;
- tax;
- payment;
- shipping;
- notification.

### Compare
Adapter changes interface compatibility.
Facade simplifies a subsystem.

---

## Decorator

### Pressure
Optional behavior combinations create subclass explosion.

### Lab
Shipping with:
- insurance;
- logging;
- metrics;
- weekend surcharge.

### Compare
Decorator vs Proxy vs middleware.

---

## Proxy

### Pressure
Need to control access to another object.

### Labs
- caching proxy;
- authorization proxy;
- lazy-loading proxy;
- remote proxy.

### Compare
Decorator adds responsibility.
Proxy primarily controls access.

---

## Composite

### Pressure
Individual objects and groups should be treated uniformly.

### Lab
Filesystem or UI tree.

### Stress change
Compute total size / render recursively.

---

## Bridge

### Pressure
Two independent dimensions produce subclass combinations.

### Lab
Shapes × Renderers.

Avoid:
- SvgCircle
- CanvasCircle
- SvgRectangle
- CanvasRectangle

Create:
- Shape hierarchy
- Renderer hierarchy

---

## Flyweight

### Pressure
Huge object counts duplicate identical intrinsic state.

### Lab
Text glyph formatting or game world sprites.

Focus on:
- intrinsic state;
- extrinsic state;
- memory trade-off.
