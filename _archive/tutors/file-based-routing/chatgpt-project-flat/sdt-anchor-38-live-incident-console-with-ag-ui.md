# Anchor design #38 — Live incident console with AG-UI

**Tutor-only deep reference.** Intended for incremental teaching, not to be
shown in full during Stage 1 unless the learner requests a complete design.

**Primary module:** `sdt-module-05-generative-ui.md`  
**User scenario:** An incident operator needs a first-party web console showing
live agent steps, tool calls and cancellation while a slow investigation runs.

## Stage 1 — Actors, constraints and source of truth

- Frontend: displays events and owns local view selections.
- Agent runtime: owns run state and emits lifecycle/tool/text/state events.
- Backend tools: enforce permissions and return verifiable evidence.

**Priorities to discuss:** correctness and permission boundary first;
interactive latency and complexity second. Ask for missing hard constraints only
when they materially affect design, otherwise state illustrative assumptions
explicitly.

## Stage 2 — Basics introduced only when needed

- AG-UI: a standard event protocol for an agent runtime communicating with a
  frontend.
- Event order: runs, text, tools and state are separate event types that must be
  interpreted consistently.
- Reconnection: the UI must know what to do after losing the stream.

## Stage 3 — Minimal working architecture

```text
+----------------------------+
| First-party HTML frontend  |
+----------------------------+
               |
               | AG-UI events
               v
+----------------------------+
| Agent run + event emitter  |
+----------------------------+
               |
               v
+----------------------------+
| Read-only mock tools       |
+----------------------------+
```

**Illustrative logical request** (not necessarily literal protocol wire format):

```json
{"run_id":"RUN-1","event":"TOOL_CALL_START","tool":"get_metrics"}
```

**Illustrative logical result**, generated from synthetic data:

```json
{"run_id":"RUN-1","event":"TOOL_CALL_END","tool":"get_metrics","status":"ok"}
```

Explain actor → first authorized boundary → real source of truth → returned
data. Highlight where the model suggests actions but the service decides whether
to execute them.

## Stage 4 — Hands-on lab

Create an HTML timeline with fixture events representing run started, tool call
started, tool call finished, text streamed and run finished. Then connect it to
a mock backend stream and visibly handle cancellation.

Keep the proof of concept small and runnable; provide exact setup, fixture data,
observable output and a negative or failure test. Do not pretend a prototype is
production-ready, or claim a protocol implementation is official without a
verified SDK.

## Stage 5 — Production evolution (not all at once)

| New constraint               | Justified change                                                              | Evidence of correct behavior                 |
|------------------------------|-------------------------------------------------------------------------------|----------------------------------------------|
| Browser connection drops     | Support reconnect and snapshot/cursor semantics supported by the runtime.     | Reconnect UI does not duplicate steps.       |
| Tool contains sensitive data | Redact tool payloads before sending frontend events.                          | Sensitive field absent in event trace.       |
| User presses Stop            | Map cancel to runtime state; report confirmed cancellation vs pending status. | Long tool cancelled/marked pending honestly. |
| UI receives stale state      | Version state updates and apply only valid changes in event order.            | Out-of-order delivery fixture.               |

**Critical failure to walk through:** The agent loses its backend connection
while a tool remains pending. The UI must show interruption/unknown state, not
claim the incident was resolved.

## Stage 6 — Architecture judgement

AG-UI helps standardize an agent-front-end event boundary for a first-party app;
MCP Apps targets embedded UI in compatible AI hosts. A streaming chat alone may
not require either standard.

**Reusable pattern:** begin with a clear source of truth, a bounded action/data
interface and the simplest credible user experience. Add distributed components
only when stated requirements force those boundaries. Show the final production
diagram only once the learner has seen which requirement justified each
addition.
