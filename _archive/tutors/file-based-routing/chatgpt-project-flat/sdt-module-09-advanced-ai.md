# Module 09 — Emerging and advanced agentic systems

**File:** `sdt-module-09-advanced-ai.md`  
**IDs:** #66–#73  
**Module learning goal:** Extend the baseline to multimodal, skills,
computer-use and integrated enterprise platforms.

## Architectural mental model

`Specialized interface -> bounded agent harness -> business system`

Multimodal or browser/tool capabilities add risk; require grounded outcomes,
safe environments and constrained actions.

## Teaching requirements within this module

Start with the stated business scenario and source of truth. Introduce the
concepts in the **Basics** field only when they unblock the current stage. First
draw the smallest appropriate architecture and implement a safe local mock. Then
show how the named production concern changes it. Do not reveal the reference
final architecture at the beginning of a lesson. Do not quiz the learner. If a
case is marked as an anchor in `sdt-catalog.md`, check whether its individual
anchor file is available; otherwise derive the same depth from this case brief.

## Case briefs

### #66 Browser-based travel-admin agent

- **Problem:** Fill forms in a legacy web UI safely.
- **Basics at point of use:** Computer use, visual grounding, approvals.
- **Working mock:** Complete a local mock travel form without submitting.
- **Production evolution:** Domain limits, layout drift, credential isolation.
- **Architectural trade-off:** API vs browser automation.

### #67 Realtime voice support assistant

- **Problem:** Respond naturally to an interrupted spoken conversation.
- **Basics at point of use:** Streaming audio, turn-taking, transcripts.
- **Working mock:** Drive a fake transcript stream through support tools.
- **Production evolution:** Consent, retention, transfer, responsiveness and
  quality.
- **Architectural trade-off:** Speech pipeline vs real-time multimodal.

### #68 Visual claims-inspection assistant

- **Problem:** Generate a damage report from user images.
- **Basics at point of use:** Vision grounding, OCR when needed, evidence.
- **Working mock:** Analyze fake claim photos to structured findings.
- **Production evolution:** Human review, provenance, uncertainty and privacy.
- **Architectural trade-off:** Vision judgement vs rules+review.

### #69 Code-editing agent in sandbox

- **Problem:** Propose a patch fixing a test failure.
- **Basics at point of use:** Agent harness, file tools and execution loop.
- **Working mock:** Modify a toy repo and run tests locally.
- **Production evolution:** Sandbox limits, no secrets, review before merge.
- **Architectural trade-off:** Unbounded generation vs edit/test loop.

### #70 Agent Skills registry and discovery

- **Problem:** Reuse portable task instructions across agents.
- **Basics at point of use:** SKILL.md, progressive context, references.
- **Working mock:** Build three mock skills and task-based selector.
- **Production evolution:** Skill trust, version pinning and code sandbox.
- **Architectural trade-off:** Skills vs tool APIs.

### #71 AI workflow builder with visual steps

- **Problem:** Create an editable process from a description.
- **Basics at point of use:** Declarative workflow DSL and rendering.
- **Working mock:** Generate typed JSON and render HTML workflow steps.
- **Production evolution:** Validate cycles, permissions and deployment.
- **Architectural trade-off:** Free-form generated code vs constrained DSL.

### #72 Code-and-data analysis workspace

- **Problem:** Analyze tabular data with reproducible computation.
- **Basics at point of use:** Code sandbox, artifacts and provenance.
- **Working mock:** Run code against fake CSV and generate a chart.
- **Production evolution:** Bound CPU/network, store dependencies and outputs.
- **Architectural trade-off:** Model reasoning vs controlled computation.

### #73 Unified enterprise agentic platform [DEEP-DIVE ANCHOR]

- **Problem:** Integrate agent, tools, UI, remote specialists and policies.
- **Basics at point of use:** Control/data planes, MCP, A2A, AG-UI, governance.
- **Working mock:** Connect one fake agent with two tools and remote specialist.
- **Production evolution:** Tenant isolation, IAM, tracing, rollout, DR and
  costs.
- **Architectural trade-off:** Shared platform vs autonomous product teams.

## Common misconceptions to correct

- Having an AI model in a request path does not automatically require agent
  orchestration.
- A technically valid diagram is not sufficient without authorization, state
  ownership and failure behavior.
- Examples should use synthetic data, explicitly labeled assumptions and local
  runnable behavior where possible.
