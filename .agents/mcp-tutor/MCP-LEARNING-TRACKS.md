# Recommendation: Separate MCP learning tracks

## Tracks

| Track          | Focus                                                                                                                                                                                      | Prerequisites                             |
|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| **MCP**        | Core protocol concepts, hosts, clients, servers, tools, resources, prompts, and request/result flow.                                                                                       | None; start here.                         |
| **MCP Apps**   | How an MCP interaction can include a visual UI, and how that UI relates to the MCP server and host.                                                                                        | Basic MCP concepts.                       |
| **App Bridge** | How a host uses `@modelcontextprotocol/ext-apps/app-bridge` to connect an embedded MCP App UI with its MCP server. Cover the responsibilities of the host, bridge, iframe, UI, and server. | Basic MCP concepts; MCP Apps for context. |

Each track should be learnable on its own. When a learner chooses a later track without the prerequisites, teach only
the needed concepts from earlier tracks rather than requiring them to complete every track first.

## Shared teaching guidance

- Reuse `SKILL.md` for the learning workflow, examples, environment, and safety guidance.
- Explain the concepts and responsibilities before introducing their libraries or tools.
- Keep each track's roadmap and examples focused on that topic.
- Avoid treating MCP, MCP Apps, and App Bridge as interchangeable technologies.
