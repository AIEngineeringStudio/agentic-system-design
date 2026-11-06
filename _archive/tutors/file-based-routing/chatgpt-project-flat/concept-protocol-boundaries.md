# Cross-module reference — MCP, MCP Apps, AG-UI, A2UI, A2A and Skills

Use this file only when a design requires more than one of these concepts or the
user requests a comparison. Introduce each concept at the stage where the user
problem creates its need. These are **different boundaries**, not rival
implementations of one interface.

## Decision-oriented definitions

| Concern                                            | Technology       | Architectural boundary                                  | When justified                                                 | Key limitation                                                |
|----------------------------------------------------|------------------|---------------------------------------------------------|----------------------------------------------------------------|---------------------------------------------------------------|
| AI host accesses tools/data                        | **MCP**          | Host/client ↔ MCP server                                | Tools, resources and prompts should be reusable across clients | Does not itself make calls authorized or support an inline UI |
| Interactive app inside AI chat                     | **MCP Apps**     | MCP host ↔ sandboxed app view associated with MCP tools | Rich charts/forms in a compatible host                         | Optional extension, not universal host support                |
| Agent runtime streams progress to a custom web UI  | **AG-UI**        | Agent ↔ first-party frontend event stream/state         | Live run/tool events and user interactions                     | Not an MCP server/tool transport                              |
| Agent describes trusted UI components              | **A2UI**         | Declarative component data ↔ host renderer              | App renders its own approved components                        | Requires compatible renderer and component catalog            |
| Agent delegates to an independently deployed agent | **A2A**          | Remote agent ↔ remote agent                             | Discovery, task lifecycle and artifacts across services        | More complexity, remote identity and failure modes            |
| Agent reuses procedural guidance                   | **Agent Skills** | Instructions + supporting resources for an agent        | Repeatable task procedures, small initial context              | Not equivalent to executing tools or authorizing them         |

## One enterprise example with each layer

User asks: "Investigate an incident and show the findings interactively."

```text
+-----------------------------+
|     User and web console    |
+-----------------------------+
              |
              | AG-UI events
              v
+-----------------------------+
|     Incident agent          |
|  Workflow and state owner   |
+-----------------------------+
              |
              +------------------------------+
              |                              |
              | MCP                          | A2A
              v                              v
+-----------------------------+  +-----------------------------+
|    MCP monitoring server    |  |   Remote research agent     |
+-----------------------------+  +-----------------------------+
              |
              v
+-----------------------------+
|  Logs / metrics / runbooks  |
+-----------------------------+
```

An **MCP App** could separately render a sandboxed inline incident dashboard
within a compatible AI host. An **A2UI** message could specify an incident form
for a compatible trusted component renderer. Neither is required for the AG-UI
web console shown above.

## Choose at the actual decision point

1. Need to invoke an API from one agent only? Direct typed function may be
   sufficient. Need reusable client interoperability? Consider MCP.
2. Own the web frontend and need agent streaming? Consider AG-UI. Need only
   dynamic components in your owned app? Structured JSON and approved components
   may be enough.
3. Need a view inside third-party AI host? Check MCP Apps extension support;
   provide text/structured fallback otherwise.
4. Need an agent-to-agent service contract? Consider A2A only when agents
   operate across independent process/ownership boundaries.
5. Need reusable instructions rather than integration? Use Agent Skills; do not
   mistake `SKILL.md` for a business authorization or data API.

## Official sources (check current version and host/SDK compatibility)

- MCP: https://modelcontextprotocol.io/specification
- MCP Apps: https://github.com/modelcontextprotocol/ext-apps
- AG-UI: https://github.com/ag-ui-protocol/ag-ui
- A2UI: https://a2ui.org/
- A2A: https://a2a-protocol.org/
- Agent Skills: https://agentskills.io/specification

Do not assume these exact protocol capabilities exist in every vendor product.
If specific SDK code is requested, verify its released API.
