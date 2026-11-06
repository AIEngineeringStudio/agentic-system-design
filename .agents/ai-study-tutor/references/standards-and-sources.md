# Official standards and framework references

Last reviewed: **2026-11-06**. A published specification is not proof that a
particular client, host or SDK supports every capability. Check version and
capability negotiation when implementing.

| Topic               | Official primary source                                             | Check                                                  |
|---------------------|---------------------------------------------------------------------|--------------------------------------------------------|
| Agent Skills        | https://agentskills.io/specification                                | SKILL.md frontmatter, lazy references, paths           |
| MCP                 | https://modelcontextprotocol.io/specification                       | Core tools/resources/prompts, transport, authorization |
| MCP Apps            | https://github.com/modelcontextprotocol/ext-apps                    | Optional embedded UI extension, host support           |
| A2A                 | https://a2a-protocol.org/v1.0.0/specification/                      | Agent discovery, tasks, artifacts and trust            |
| AG-UI               | https://github.com/ag-ui-protocol/ag-ui                             | Frontend event protocol and compatibility              |
| A2UI                | https://a2ui.org/                                                   | Declarative component descriptions and renderer        |
| Agent SDK           | https://openai.github.io/openai-agents-python/                      | Tools, handoffs, guardrails, tracing                   |
| LangGraph           | https://docs.langchain.com/oss/python/langgraph/persistence         | Workflow checkpoints and durable state                 |
| Security            | https://genai.owasp.org/                                            | Model and agent-specific threats                       |
| OpenTelemetry       | https://opentelemetry.io/docs/specs/semconv/gen-ai/                 | GenAI semantic conventions                             |
| Architecture review | https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/ | Enterprise reliability, risk and operations            |

**Classify carefully:** MCP and A2A are different protocols; MCP Apps is an
optional extension; AG-UI is agent-to-frontend event communication; A2UI is a
declarative UI representation; Agent Skills packages reusable instructions.
OpenAI Agents SDK and LangGraph are frameworks. These are not interchangeable.
