# Anchor design #09 — Local ticket-lookup MCP server

**Tutor-only deep reference.** Intended for incremental teaching, not to be
shown in full during Stage 1 unless the learner requests a complete design.

**Primary module:** `sdt-module-02-mcp.md`  
**User scenario:** A support agent wants to ask an AI host for ticket details.
The ticket service exists separately and must be reusable across compatible AI
clients.

## Stage 1 — Actors, constraints and source of truth

- AI host: owns the conversation and MCP client lifecycle.
- MCP server: advertises and validates `get_ticket` and `list_tickets` tools.
- Ticket system: enforces the real owner/tenant permissions for reads.

**Priorities to discuss:** correctness and permission boundary first;
interactive latency and complexity second. Ask for missing hard constraints only
when they materially affect design, otherwise state illustrative assumptions
explicitly.

## Stage 2 — Basics introduced only when needed

- MCP host/client/server: host orchestrates, client communicates, server
  provides tools/resources/prompts.
- Tool schema: contract describing allowable arguments and result types.
- JSON-RPC: protocol messages carry requests and responses; tool definitions do
  not grant rights.

## Stage 3 — Minimal working architecture

```text
+-------------------------+
|  AI host + MCP client   |
+-------------------------+
             |
             v
+-------------------------+
|    Local MCP server     |
| list_tickets/get_ticket |
+-------------------------+
             |
             v
+-------------------------+
|    Fake ticket store    |
+-------------------------+
```

**Illustrative logical request** (not necessarily literal protocol wire format):

```json
{"tool":"get_ticket","arguments":{"ticket_id":"T-100"}}
```

**Illustrative logical result**, generated from synthetic data:

```json
{"ticket_id":"T-100","status":"open","summary":"Synthetic customer ticket"}
```

Explain actor → first authorized boundary → real source of truth → returned
data. Highlight where the model suggests actions but the service decides whether
to execute them.

## Stage 4 — Hands-on lab

Use the current official MCP SDK to expose two typed read-only tools against a
local fixture JSON file. Exercise success, missing ticket, invalid schema and
unauthorized ticket. If SDK APIs cannot be verified, mark interface calls as
conceptual.

Keep the proof of concept small and runnable; provide exact setup, fixture data,
observable output and a negative or failure test. Do not pretend a prototype is
production-ready, or claim a protocol implementation is official without a
verified SDK.

## Stage 5 — Production evolution (not all at once)

| New constraint                          | Justified change                                                                                     | Evidence of correct behavior     |
|-----------------------------------------|------------------------------------------------------------------------------------------------------|----------------------------------|
| Multiple users access different tickets | Derive principal from trusted host/service context; enforce per-ticket authorization.                | Cross-user read denied.          |
| Remote deployment is required           | Choose officially supported remote MCP transport and authentication per negotiated protocol version. | Host/client compatibility run.   |
| A tool can return hostile instructions  | Treat ticket content as untrusted data; never execute instructions embedded in ticket text.          | Prompt-injection rejection test. |
| Server is intermittently down           | Time-box reads, expose machine-readable errors, and provide non-fabricated fallback.                 | Timeout and recovery trace.      |

**Critical failure to walk through:** A host requests ticket `T-200` belonging
to another user. The server refuses even though the tool schema accepts the ID.

## Stage 6 — Architecture judgement

For one app-owned tool, a direct function call may be simpler. MCP makes sense
when multiple hosts need reusable, standards-oriented access to the same
capability.

**Reusable pattern:** begin with a clear source of truth, a bounded action/data
interface and the simplest credible user experience. Add distributed components
only when stated requirements force those boundaries. Show the final production
diagram only once the learner has seen which requirement justified each
addition.
