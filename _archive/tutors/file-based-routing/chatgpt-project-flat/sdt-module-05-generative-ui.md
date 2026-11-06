# Module 05 — Generative UI, MCP Apps, AG-UI and A2UI

**File:** `sdt-module-05-generative-ui.md`  
**IDs:** #34–#41  
**Module learning goal:** Separate UI rendering, embedded MCP views and
agent-to-frontend event streaming.

## Architectural mental model

`Model/data -> host/renderer -> interactive UI -> authorized action`

MCP Apps is embedded host UI; AG-UI events stream agent state; A2UI is
declarative host-rendered component data. Do not conflate them.

## Teaching requirements within this module

Start with the stated business scenario and source of truth. Introduce the
concepts in the **Basics** field only when they unblock the current stage. First
draw the smallest appropriate architecture and implement a safe local mock. Then
show how the named production concern changes it. Do not reveal the reference
final architecture at the beginning of a lesson. Do not quiz the learner. If a
case is marked as an anchor in `sdt-catalog.md`, check whether its individual
anchor file is available; otherwise derive the same depth from this case brief.

## Case briefs

### #34 AI sales dashboard from structured answers [DEEP-DIVE ANCHOR]

- **Problem:** Present dynamic charts and tables rather than prose.
- **Basics at point of use:** Typed visual schema, approved components.
- **Working mock:** Render chart data in self-contained HTML with user
  filtering.
- **Production evolution:** XSS prevention, schema/a11y validation and print
  fallback.
- **Architectural trade-off:** Fixed dashboard vs trusted GenUI rendering.

### #35 Conversational configuration wizard

- **Problem:** Collect settings through a dynamic form.
- **Basics at point of use:** Form state, validation, UI/action boundary.
- **Working mock:** Build native HTML form from an approved component registry.
- **Production evolution:** Server revalidation, stale state and authorized
  submit.
- **Architectural trade-off:** Generated arbitrary HTML vs constrained
  components.

### #36 Expense-analysis MCP App [DEEP-DIVE ANCHOR]

- **Problem:** Embed an interactive expense chart in a compatible AI host.
- **Basics at point of use:** ui:// resource, MCP Apps host bridge, iframe
  sandbox.
- **Working mock:** Mock a summary tool linked to an HTML view using official
  SDK when available.
- **Production evolution:** Host capability fallback, authorization, sandbox
  messaging and trace.
- **Architectural trade-off:** MCP Apps vs plain result vs own web app.

### #37 Ticket-approval MCP App

- **Problem:** Allow a reviewer to approve a tool-proposed change inside chat.
- **Basics at point of use:** Host-mediated view action, business-side approval.
- **Working mock:** Build a mock ticket-view approval interface.
- **Production evolution:** Approver identity, expiration, replay defense and
  audit.
- **Architectural trade-off:** Model-invoked action vs verified view action.

### #38 Live incident console with AG-UI [DEEP-DIVE ANCHOR]

- **Problem:** Stream long-running agent activity to a web app.
- **Basics at point of use:** Run lifecycle, event stream, state
  snapshots/deltas.
- **Working mock:** Build an HTML timeline from AG-UI event fixtures.
- **Production evolution:** Reconnection, cancellation, redaction and state
  ordering.
- **Architectural trade-off:** AG-UI vs custom SSE payloads.

### #39 Declarative A2UI request form

- **Problem:** Let an agent propose a UI while host controls components.
- **Basics at point of use:** Declarative UI, allowed component catalog.
- **Working mock:** Render a typed form tree in plain HTML.
- **Production evolution:** Reject unsafe components, actions and unknown schema
  versions.
- **Architectural trade-off:** A2UI vs MCP Apps HTML.

### #40 Portable UI comparison lab

- **Problem:** Present the same result in different host environments.
- **Basics at point of use:** Transport vs presentation, adapter boundaries.
- **Working mock:** Implement a shared JSON result rendered as web UI and
  embedded host view.
- **Production evolution:** Capability detection, schema migration and
  accessibility.
- **Architectural trade-off:** MCP Apps vs AG-UI/A2UI.

### #41 Enterprise agent cockpit

- **Problem:** Combine chat, live progress and workspace edits.
- **Basics at point of use:** AG-UI state and UI ownership.
- **Working mock:** Build a two-panel HTML console with event-driven state.
- **Production evolution:** Concurrent edits, policy enforcement, reconnection
  and logs.
- **Architectural trade-off:** Single chat vs agent workspace.

## Common misconceptions to correct

- Having an AI model in a request path does not automatically require agent
  orchestration.
- A technically valid diagram is not sufficient without authorization, state
  ownership and failure behavior.
- Examples should use synthetic data, explicitly labeled assumptions and local
  runnable behavior where possible.
