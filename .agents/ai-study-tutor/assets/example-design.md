# Example of a fully developed lesson (not loaded by default)

**Case #36: Expense-analysis MCP App**  
**Status:** Reference example for tutor authors. In a real lesson, reveal one
stage at a time unless the learner requests the complete design.

## Stage 1 — A user requirement, not a technology choice

An analyst types: “Show Q3 expenses by category and help me inspect anything
over $1,000.” They want to inspect a chart inside their AI assistant, not read a
static paragraph. Expenses are controlled company records.

**Requirements:**

- A signed-in analyst can retrieve only authorized expense summaries.
- Show category totals, a threshold filter, and supporting transaction rows.
- Updating the local filter should feel immediate; requesting a new time range
  may require a server call.
- If an AI host cannot embed a view, the answer should still give a useful text
  summary.

**Priority order:** prevent data leakage > correct totals > usable inline
interaction > response latency > UI polish.

**Explicit assumptions:** demo uses synthetic expense records and a host known
to support the MCP Apps extension. No money moves. The analyst is permitted to
read, not edit, these expenses.

## Stage 2 — The few concepts this requirement introduces

- **Tool:** named, typed request such as
  `get_expense_summary(period, department)`. The server queries data and
  enforces permission. The model/host may suggest calling the tool; it cannot
  bypass policy.
- **MCP:** protocol for the host's MCP client to communicate with an
  expense-server endpoint. MCP is useful here if the tool should be reused
  across compatible clients.
- **MCP Apps:** optional MCP extension allowing a compatible host to display a
  sandboxed HTML view associated with a tool and linked UI resource. Host and
  SDK support must be confirmed.
- **UI state:** filtering already retrieved rows can happen locally; durable
  business facts and access policy remain server-side.

Small logical request, **not literal SDK wire format**:

```json
{"tool":"get_expense_summary","arguments":{"period":"2026-Q3","department":"sales"}}
```

Small logical response, using *fake values*:

```json
{
  "period":"2026-Q3",
  "currency":"USD",
  "categories":[
    {"category":"Travel","amount":1800},
    {"category":"Software","amount":650}
  ],
  "as_of":"2026-10-01T00:00:00Z"
}
```

## Stage 3 — Minimum working architecture

```text
+----------------------------+
|   Analyst in an AI host    |
|   (MCP Apps-compatible)    |
+----------------------------+
               |
               v
+----------------------------+
|  Host MCP client           |
+----------------------------+
               |
               v
+----------------------------+
|  Expense MCP server        |
|  - typed summary tool      |
|  - linked UI resource      |
+----------------------------+
               |
               v
+----------------------------+
|  Mock expense data store   |
+----------------------------+

Host loads linked UI view in sandboxed iframe:

+----------------------------+
|   Embedded expense view    |
|   chart | threshold | rows |
+----------------------------+
```

**Happy path:** (1) host requests the tool, (2) server verifies user and
period, (3) query returns approved synthetic records, (4) host receives
structured data and discovers linked UI resource, (5) compatible host renders
the view, (6) analyst filters existing data. The view never owns authority for a
data read or write.

## Stage 4 — A tiny executable local preview

The included `assets/expense-preview.html` is a self-contained, printable,
light-mode HTML prototype. Open it locally in a browser. It filters *hard-coded
synthetic rows* by a threshold, displays category totals and supports print. It
requires no service or credentials.

**Important:** This preview demonstrates **only the UI behavior**, **not** an
MCP server, compliant MCP Apps host bridge, sandbox or remote authorization. For
an actual MCP App implementation, use the
current [official ext-apps SDK and examples](https://github.com/modelcontextprotocol/ext-apps);
verify your target host supports the optional extension. The tutor must not
claim a plain HTML prototype is itself a standards-compliant MCP App.

**Example behavior:** threshold $1,000 selects Travel $1,800 and removes
Software $650 from the visible category list. This UI-only filtering does not
mutate source data.

## Stage 5 — Evolve to production from real constraints

| New requirement              | Why the baseline is not enough             | Architectural change                                             | Trade-off                           |
|------------------------------|--------------------------------------------|------------------------------------------------------------------|-------------------------------------|
| Tenant privacy               | Prompt may refer to another team's records | Enforce principal and tenant access on MCP server/database query | More identity integration           |
| Unknown host UI support      | Some hosts do not display MCP Apps         | Provide readable tool text/structured output fallback            | Two presentation paths              |
| Expense memos may be hostile | Source content can contain instructions    | Treat fetched fields as data, never instructions; escape UI text | More validation                     |
| Tool may time out            | Remote query can stall                     | Explicit error display, bounded timeout, retry for safe reads    | Stale/partial results need labeling |
| UI cache may be old          | User may see outdated amounts              | Include `as_of`, freshness contract, server-authorized refresh   | More state management               |
| Teams need debugging         | Errors cross host/tool/UI boundaries       | Correlation IDs and redacted tool/DB traces                      | Instrumentation overhead            |

```text
+------------------------------+
|   Signed-in analyst          |
+------------------------------+
               |
               v
+------------------------------+
|  Compatible AI host          |
|  Auth context + MCP client   |
+------------------------------+
               |
               v
+------------------------------+
|  Remote expense MCP server   |
|  Scope checks, quotas, audit |
+------------------------------+
               |
               v
+------------------------------+
|  Governed expense query API  |
+------------------------------+
               |
               v
+------------------------------+
|  Authorized system of record |
+------------------------------+

Host-managed app view:

+------------------------------+
| Sandboxed expense UI iframe  |
| Local filters + host bridge  |
+------------------------------+
               |
               v
+------------------------------+
| Host-mediated authorized     |
| tool request / status        |
+------------------------------+
```

**Failure scenario:** an analyst loads summary data, then loses access. A later
refresh must return access denied from the service; the old iframe must not be
treated as permission to retrieve new data. Local already-rendered values may
remain visible until the host clears them; define that behavior as part of data
retention/session policy.

**Production evidence to request from the application team, not the learner:**
denied cross-tenant reads, UI fallback on unsupported hosts, no inline arbitrary
HTML execution, trace correlation, error display on timeout, and schema-version
compatibility.

## Stage 6 — Extract the reusable architecture pattern

| Option                 | Fits when                                                                        | Limit                                               |
|------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------|
| Plain MCP result       | The output is short or structured data                                           | No inline rich interaction                          |
| MCP Apps               | A compatible conversational host needs embedded HTML associated with an MCP tool | Optional host support and sandbox constraints       |
| AG-UI + owned frontend | You own a web app and need agent event/state streaming                           | You maintain application UI and runtime integration |
| A2UI                   | Agent declares a component layout rendered natively from an allowlist            | Renderer/component compatibility required           |

**Reusable lesson:** Separate tool access, data authority, host capability, view
rendering and user interactions. Never use UI state or model-chosen tool
arguments as security authority. The strongest design is not the one with every
AI standard—it is the one with clear boundaries meeting the real requirements.

**Related cases:** #34 (structured UI), #38 (AG-UI live console), #39 (A2UI) and
#37 (MCP App approval).
