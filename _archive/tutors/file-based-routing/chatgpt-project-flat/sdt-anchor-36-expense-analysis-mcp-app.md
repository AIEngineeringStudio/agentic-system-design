# Anchor design #36 — Expense-analysis MCP App

**Tutor-only deep reference.** Intended for incremental teaching, not to be
shown in full during Stage 1 unless the learner requests a complete design.

**Primary module:** `sdt-module-05-generative-ui.md`  
**User scenario:** A spending analyst asks a ChatGPT-like AI host for an
interactive Q3 expense breakdown with adjustable thresholds inside the
conversation.

## Stage 1 — Actors, constraints and source of truth

- MCP Apps-capable host: operates the MCP client and sandboxed app view.
- Expense MCP server: owns typed tools and linked UI resource.
- Expense API and database: authorize requested data based on verified identity.

**Priorities to discuss:** correctness and permission boundary first;
interactive latency and complexity second. Ask for missing hard constraints only
when they materially affect design, otherwise state illustrative assumptions
explicitly.

## Stage 2 — Basics introduced only when needed

- MCP tool: typed data operation, independent of UI markup.
- MCP Apps: optional MCP extension with linked `ui://` view and host bridge;
  compatible host required.
- UI state: changing a local filter does not grant permission to query other
  data.

## Stage 3 — Minimal working architecture

```text
+-------------------------+
| Analyst in AI host      |
+-------------------------+
             |
             v
+-------------------------+
| Host MCP client         |
+-------------------------+
             |
             v
+-------------------------+
| Expense MCP server      |
| Tool + linked UI view   |
+-------------------------+
             |
             v
+-------------------------+
| Fake expense database   |
+-------------------------+
```

**Illustrative logical request** (not necessarily literal protocol wire format):

```json
{"tool":"get_expense_summary","arguments":{"period":"2026-Q3","department":"sales"}}
```

**Illustrative logical result**, generated from synthetic data:

```json
{"period":"2026-Q3","currency":"USD","categories":[{"name":"Travel","amount":1800},{"name":"Software","amount":650}],"as_of":"2026-10-01T00:00:00Z"}
```

Explain actor → first authorized boundary → real source of truth → returned
data. Highlight where the model suggests actions but the service decides whether
to execute them.

## Stage 4 — Hands-on lab

Build a self-contained light-mode HTML chart preview over fake data. Then attach
the HTML as an MCP App UI resource to an expense-summary tool using a verified
SDK in a compatible host; distinguish UI-only preview from compliant MCP App.

Keep the proof of concept small and runnable; provide exact setup, fixture data,
observable output and a negative or failure test. Do not pretend a prototype is
production-ready, or claim a protocol implementation is official without a
verified SDK.

## Stage 5 — Production evolution (not all at once)

| New constraint                           | Justified change                                                              | Evidence of correct behavior      |
|------------------------------------------|-------------------------------------------------------------------------------|-----------------------------------|
| Host cannot render the embedded view     | Return a useful text/structured tool result with an explicit UI fallback.     | Non-Apps host read test.          |
| Users have different expense permissions | Authorize period and department in the server; never trust iframe parameters. | Cross-department deny.            |
| UI submits a high-impact action          | Route via allowed host-mediated tool interface and reauthorize server-side.   | Unauthorized app action rejected. |
| Data may be stale                        | Include `as_of`, display freshness and use verified refresh.                  | Stale-data user-visible state.    |

**Critical failure to walk through:** The analyst loses permission after loading
the chart. A later refresh is rejected regardless of locally displayed iframe
values.

## Stage 6 — Architecture judgement

Use MCP Apps only for a host that supports inline sandboxed HTML. For your own
web frontend, AG-UI or regular UI components may be the better match. A2UI is
declarative host-rendered components, not interchangeable with embedded HTML.

**Reusable pattern:** begin with a clear source of truth, a bounded action/data
interface and the simplest credible user experience. Add distributed components
only when stated requirements force those boundaries. Show the final production
diagram only once the learner has seen which requirement justified each
addition.
