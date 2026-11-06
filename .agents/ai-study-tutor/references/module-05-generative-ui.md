# Module 05 — Generative UI, MCP Apps, AG-UI and A2UI

**Learning boundary:** Compare structured UI, embedded UI and frontend event
streaming without conflating protocols.

**One-line mental model:**
`AI result -> trusted rendering strategy -> user interaction -> authorized backend`

## Necessary concepts, only when the case needs them

**GenUI** is a broad approach to presenting dynamic AI-generated or AI-selected
interfaces. **MCP Apps** embeds a sandboxed HTML view in a compatible MCP host.
**AG-UI** defines agent-to-first-party-frontend event communication. **A2UI**
describes declarative component trees that a compatible host renders. These are
different architecture boundaries, and none is universally supported.

## Patterns and decisions to reuse

- **Primary decision rule:** A generated form or button never grants authority;
  the backend rechecks access on every effect.
- Start with the baseline boundary and identify source of truth, authority and
  error semantics before selecting products.
- Show one happy path and one failure path, then justify added components as
  responses to constraints.
- Keep code labs small and local with fake records; label production
  architecture as a design, not deployed implementation.

## Problem briefs (these are design prompts, not pre-solved lessons)

### #34 — AI sales dashboard from structured answers ★ anchor

**User need:** Show a chart instead of a paragraph.

- **Teach on demand:** JSON UI schema, allowlisted components.
- **Small working lab:** Render a typed chart in self-contained HTML.
- **Production evolution:** Schema validation, escaping, a11y and printable
  fallback.
- **Decision to explain:** Fixed UI vs model-selected approved components.

### #35 — Conversational configuration wizard

**User need:** Update a form based on conversational preferences.

- **Teach on demand:** UI state, validation and actions.
- **Small working lab:** Build a native HTML wizard from an approved field
  registry.
- **Production evolution:** Repeat authorization on submit; handle stale state.
- **Decision to explain:** Trusted components vs generated raw code.

### #36 — Expense-analysis MCP App ★ anchor

**User need:** Embed expense charts within compatible chat hosts.

- **Teach on demand:** MCP Apps ui:// resources, host bridge, sandbox.
- **Small working lab:** Attach HTML view to MCP expense summary tool.
- **Production evolution:** Host compatibility, authorization, isolation and
  text fallback.
- **Decision to explain:** MCP Apps vs plain tool result.

### #37 — Ticket-approval MCP App

**User need:** Approve a proposed ticket action inside chat.

- **Teach on demand:** Bidirectional host/app calls, approval semantics.
- **Small working lab:** Build a sandboxed action panel with mock backend.
- **Production evolution:** Server-side approver authority, expiry, audit,
  replay protection.
- **Decision to explain:** App-view action vs model-triggered tool call.

### #38 — Live incident console with AG-UI ★ anchor

**User need:** Stream an investigation into a first-party application.

- **Teach on demand:** Run lifecycle, event streams and state deltas.
- **Small working lab:** Render a live incident timeline from mock AG-UI-like
  events.
- **Production evolution:** Resume cursor, tool-payload redaction and
  cancellation.
- **Decision to explain:** AG-UI vs custom SSE events.

### #39 — Declarative A2UI request form

**User need:** A remote agent proposes a form using approved native components.

- **Teach on demand:** Declarative components, action/data binding.
- **Small working lab:** Render allowlisted UI nodes in plain HTML.
- **Production evolution:** Restrict components/actions and enforce schema
  versions.
- **Decision to explain:** A2UI vs embedded HTML view.

### #40 — Portable UI comparison lab

**User need:** Show same results in chat and standalone web app.

- **Teach on demand:** Presentation adapters, transport/renderer split.
- **Small working lab:** Build both MCP App and first-party HTML views on one
  data contract.
- **Production evolution:** Capability fallback, accessibility and version skew.
- **Decision to explain:** MCP Apps vs AG-UI/A2UI.

### #41 — Enterprise agent cockpit

**User need:** Combine chat, progress and an editable workspace.

- **Teach on demand:** AG-UI state ownership, UI composition.
- **Small working lab:** Build two-pane HTML agent console with event timeline.
- **Production evolution:** Concurrent edits, policy checks, reconnection and
  tracing.
- **Decision to explain:** Chat-only vs shared agent workspace.

## Example baseline diagram for this module

```text
+-----------------------------+
|       User requirement      |
+-----------------------------+
              |
              v
+-----------------------------+
|      Smallest valid flow    |
+-----------------------------+
              |
              v
+-----------------------------+
|    Business source of truth |
+-----------------------------+
```

**Important:** This is only a visual placeholder. Draw the actual components
from the selected case requirements; do not present this as the final
architecture. Keep diagrams connected with solid `+ - |` lines and arrows.

**Case IDs in this module:** #34, #35, #36, #37, #38, #39, #40, #41.
