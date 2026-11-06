# Anchor design #01 — FAQ support assistant

**Tutor-only deep reference.** Intended for incremental teaching, not to be
shown in full during Stage 1 unless the learner requests a complete design.

**Primary module:** `sdt-module-01-agent-fundamentals.md`  
**User scenario:** A customer asks whether they can return an item. Policies are
in a small, approved FAQ. A wrong answer can create an incorrect expectation.

## Stage 1 — Actors, constraints and source of truth

- Customer: asks a question and may supply misleading text.
- FAQ repository: only approved policy text is the source of truth.
- Answer service: retrieves matching policy and decides whether evidence is
  sufficient.

**Priorities to discuss:** correctness and permission boundary first;
interactive latency and complexity second. Ask for missing hard constraints only
when they materially affect design, otherwise state illustrative assumptions
explicitly.

## Stage 2 — Basics introduced only when needed

- Model response: a language model can phrase an answer; it does not certify
  policy accuracy.
- Grounding: include matching FAQ text as evidence before generation.
- Abstention: decline to invent an answer if the FAQ does not cover it.

## Stage 3 — Minimal working architecture

```text
+-------------------------+
|    Customer question    |
+-------------------------+
             |
             v
+-------------------------+
|  FAQ matching service   |
+-------------------------+
             |
             v
+-------------------------+
| Approved FAQ passages   |
+-------------------------+
             |
             v
+-------------------------+
|  Answer or abstain      |
+-------------------------+
```

**Illustrative logical request** (not necessarily literal protocol wire format):

```json
{"question":"Can I return an opened item?","customer_locale":"en-US"}
```

**Illustrative logical result**, generated from synthetic data:

```json
{"answer":"Please check the applicable return rule.","source_ids":["faq-return-01"],"status":"grounded"}
```

Explain actor → first authorized boundary → real source of truth → returned
data. Highlight where the model suggests actions but the service decides whether
to execute them.

## Stage 4 — Hands-on lab

Create 12 synthetic FAQ records, including two conflicting outdated answers.
Retrieve by keyword first, respond with the source ID, and return
`insufficient_evidence` when the question has no match. Add a model only after
deterministic retrieval works.

Keep the proof of concept small and runnable; provide exact setup, fixture data,
observable output and a negative or failure test. Do not pretend a prototype is
production-ready, or claim a protocol implementation is official without a
verified SDK.

## Stage 5 — Production evolution (not all at once)

| New constraint                                       | Justified change                                                                    | Evidence of correct behavior                    |
|------------------------------------------------------|-------------------------------------------------------------------------------------|-------------------------------------------------|
| More questions than simple keyword matching supports | Use embedding or hybrid retrieval; keep source IDs and an abstention rule.          | Retrieval recall and false-citation evaluation. |
| Wrong policy version can mislead                     | Version approved sources; show a policy effective date and rebuild index on change. | Version-based regression test.                  |
| Sensitive customer data might enter prompts          | Minimize and redact personal information; enforce storage/access limits.            | Prompt/log redaction review.                    |
| Answers may hallucinate                              | Enforce citation checks and measure grounded answer correctness.                    | Offline groundedness cases with human review.   |

**Critical failure to walk through:** A customer asks about a promotion that is
absent from the FAQ. The safe behavior is `insufficient_evidence` with a helpful
escalation path, not an invented policy.

## Stage 6 — Architecture judgement

If exact FAQ matching handles the workload, do not introduce a multi-agent
workflow or MCP solely to add AI branding. Add a tool or retrieval protocol only
when integration/reuse requirements justify it.

**Reusable pattern:** begin with a clear source of truth, a bounded action/data
interface and the simplest credible user experience. Add distributed components
only when stated requirements force those boundaries. Show the final production
diagram only once the learner has seen which requirement justified each
addition.
