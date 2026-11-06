# Module 09 — Emerging and advanced agentic systems

**Learning boundary:** Expand into multimodal, computer-use, skills and unified
platform design while keeping safety and source-of-truth boundaries.

**One-line mental model:**
`Specialized modality/tool -> bounded harness -> trusted system state`

## Necessary concepts, only when the case needs them

Computer use, code execution and multimodal interaction expand the tool surface
and the failure modes. Agent Skills are packaged instructions with lazy
references and optional scripts, **not** a security or execution sandbox. A
unified agentic platform coordinates many capabilities but should not require
every protocol for every case.

## Patterns and decisions to reuse

- **Primary decision rule:** Select the smallest surface that meets a goal;
  enforce execution/environment isolation outside prompts.
- Start with the baseline boundary and identify source of truth, authority and
  error semantics before selecting products.
- Show one happy path and one failure path, then justify added components as
  responses to constraints.
- Keep code labs small and local with fake records; label production
  architecture as a design, not deployed implementation.

## Problem briefs (these are design prompts, not pre-solved lessons)

### #66 — Browser-based travel-admin agent

**User need:** Work with forms in systems lacking tool APIs.

- **Teach on demand:** Computer use, grounding and confirmations.
- **Small working lab:** Preview changes in a fake travel site without
  submitting.
- **Production evolution:** Layout drift, credential isolation, allowlist and
  stop rules.
- **Decision to explain:** API/MCP vs last-resort computer use.

### #67 — Realtime voice support assistant

**User need:** Support a live spoken conversation.

- **Teach on demand:** Streaming speech, turn-taking, interrupts.
- **Small working lab:** Stream fake transcript turns into a support workflow.
- **Production evolution:** Consent, redaction, latency and human transfer.
- **Decision to explain:** Pipeline speech vs realtime multimodal.

### #68 — Visual claims-inspection assistant

**User need:** Analyze user-uploaded images for damage evidence.

- **Teach on demand:** Vision, multimodal extraction and uncertainty.
- **Small working lab:** Create a structured report using synthetic photos.
- **Production evolution:** Privacy, evidence provenance and human final
  decision.
- **Decision to explain:** Vision-only vs deterministic checks plus review.

### #69 — Code-editing agent in sandbox

**User need:** Fix a failing test and propose a patch.

- **Teach on demand:** Code harness, run/test/edit loop.
- **Small working lab:** Modify a toy repo in an isolated workspace.
- **Production evolution:** No secrets or network, capped runs and review gates.
- **Decision to explain:** Model writes code vs bounded edit/test agent.

### #70 — Agent Skills registry and discovery

**User need:** Package reusable workflow guidance.

- **Teach on demand:** SKILL.md, lazy-loading and references.
- **Small working lab:** Create three local toy skills and a selector.
- **Production evolution:** Trust review, script isolation and version pinning.
- **Decision to explain:** Skills vs executable tools.

### #71 — AI workflow builder with visual steps

**User need:** Generate an editable workflow for non-coders.

- **Teach on demand:** Workflow schema, components and static validation.
- **Small working lab:** Render a JSON-defined graph in plain HTML.
- **Production evolution:** Validate cycles, permissions and publish approval.
- **Decision to explain:** Arbitrary generated code vs constrained DSL.

### #72 — Code-and-data analysis workspace

**User need:** Generate repeatable charts from sample data.

- **Teach on demand:** Sandboxed code execution and artifacts.
- **Small working lab:** Run Python analysis of fake CSV and save charts.
- **Production evolution:** Bound CPU/network, lineage and dependency lock.
- **Decision to explain:** Pure text inference vs computation.

### #73 — Unified enterprise agentic platform ★ anchor

**User need:** Govern assistants, UIs, MCP, remote agents and operations.

- **Teach on demand:** Control/data planes, protocols, security and evaluation.
- **Small working lab:** Integrate one agent, two tools, a UI and remote
  specialist.
- **Production evolution:** Multi-tenancy, tracing, rollout, DR and policy
  enforcement.
- **Decision to explain:** Central platform vs team-owned services.

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

**Case IDs in this module:** #66, #67, #68, #69, #70, #71, #72, #73.
