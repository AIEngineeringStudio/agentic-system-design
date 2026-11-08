# AI System Design #1 — FAQ Support Assistant

`Stage 6 of 6: Architecture Decisions`

---

**Goal:**
Understand when to use deterministic lookup, RAG, or an autonomous agent.
Then extract decisions that apply to other AI systems.

## 1. Compare the three approaches

|                    | Deterministic FAQ     | RAG + LLM                                  | Bounded AI Agent                              |
|--------------------|-----------------------|--------------------------------------------|-----------------------------------------------|
| Main idea          | Find a known answer   | Retrieve evidence, then generate an answer | Choose tools and steps dynamically            |
| AI model required? | No                    | Yes                                        | Usually                                       |
| Data access        | Approved FAQ records  | Approved documents or records              | Approved APIs and tools                       |
| Flexibility        | Low                   | Medium–high                                | High                                          |
| Complexity         | Low                   | Medium                                     | High                                          |
| Main risk          | Missing valid matches | Unsupported generated claims               | Incorrect or unauthorized actions             |
| Best fit           | Simple policy FAQ     | Complex knowledge questions                | Multi-step tasks needing dynamic tool choices |

These are qualitative design comparisons, not measured performance or cost
benchmarks.

## 2. Approach A — Deterministic FAQ lookup

```
+----------------------+
| Customer question    |
+----------------------+
           |
           v
+----------------------+
| Approved FAQ lookup  |
+----------------------+
           |
           v
+----------------------+
| Exact policy answer  |
| or abstention        |
+----------------------+
```

Example: "Can I return an opened item?"

The system matches `FAQ-RETURN-01` and returns the stored policy.

Use this when the FAQ collection is small, answers are standardized, and you
need predictable behavior.

The main limitation is language flexibility. A customer can ask a valid question
using words the matcher does not recognize.

Our Stage 4 and Stage 5 implementations follow this approach.

## 3. Approach B — RAG + LLM

RAG (Retrieval-Augmented Generation) combines evidence retrieval with
language-model generation.

```
+----------------------+
| Customer question    |
+----------------------+
           |
           v
+----------------------+
| Evidence retrieval   |
| Keyword / Hybrid     |
+----------------------+
           |
           v
+----------------------+
| Approved passages    |
+----------------------+
           |
           v
+----------------------+
| LLM drafts answer    |
+----------------------+
           |
           v
+----------------------+
| Evidence validation  |
| Answer or abstain    |
+----------------------+
```

Example: "I removed the packaging. Am I still eligible for a refund?"

The retrieval layer finds the policy about opened products. The LLM can explain
the policy in language that matches the question.

Use RAG when questions vary significantly, content is larger or more complex,
and natural-language synthesis provides clear value.

However, RAG does not guarantee correct answers. You still need approved-source
filtering, valid citations, policy freshness, and abstention.

Important distinction: RAG is not automatically an agent. A fixed retrieve →
generate → validate pipeline is a normal application workflow.

## 4. Approach C — Bounded AI agent

An agent becomes useful when the application must dynamically select operations
based on the customer's request.

Example: "Where is my order, and am I eligible for a refund?"

The system might need to retrieve order status, check customer-specific purchase
information, and consult refund policy.

```
+------------------------+
| Customer request       |
+------------------------+
            |
            v
+------------------------+
| Bounded AI Agent       |
| Select required tools  |
+------------------------+
            |
      +-----+------+
      |            |
      v            v
+------------+ +------------+
| Order API  | | Policy API |
+------------+ +------------+
      |            |
      +-----+------+
            |
            v
+------------------------+
| Validate evidence      |
| Prepare response       |
+------------------------+
```

An agent is justified when dynamic tool selection or adaptive multi-step work is
needed.

But if every request follows the same predictable sequence, ordinary application
code is often simpler.

Security boundary: The agent may request an order lookup, but the order service
must verify customer identity and access rights. The agent cannot grant itself
permissions.

For refunds or other business writes, use explicit authorization and a
deterministic execution workflow.

## 5. Architecture selection guide

```
+----------------------------------+
| What must the system accomplish? |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Can approved fixed answers       |
| handle the task?                 |
+----------------------------------+
         |                 |
        YES                NO
         |                 |
         v                 v
+----------------+  +----------------------+
| Deterministic  |  | Needs evidence-based |
| FAQ lookup     |  | language synthesis?  |
+----------------+  +----------------------+
                           |          |
                          YES         NO
                           |          |
                           v          v
                    +-----------+ +----------------+
                    | RAG + LLM | | Use explicit   |
                    +-----------+ | app workflow   |
                                  +----------------+

If the task also needs dynamic tool selection,
consider a bounded agent with authorized tools.
```

This is a decision guide, not a mandatory upgrade path. A system does not become
better simply by adding an LLM or an agent.

## 6. When should we upgrade our FAQ assistant?

| Observed problem                                 | Justified improvement                                       |
|--------------------------------------------------|-------------------------------------------------------------|
| Simple keyword matching misses valid questions   | Improve retrieval first                                     |
| Many complex documents require explanation       | Introduce RAG + LLM                                         |
| Questions require live order information         | Add authorized business API access                          |
| The required sequence changes by customer intent | Consider a bounded tool agent                               |
| Policies change frequently                       | Improve indexing and freshness controls                     |
| Incorrect answers increase                       | Improve evaluations and validation before adding complexity |

The curriculum specifically recommends adding embedding or hybrid retrieval only
when simple matching is no longer sufficient.&#x20;

sdt-anchor-01-faq-support-assistant.md

## 7. Remaining risks

Even after the Stage 5 improvements, these risks remain.

| Risk                                      | Required control                                   |
|-------------------------------------------|----------------------------------------------------|
| Search misses a relevant policy           | Retrieval evaluation with representative questions |
| Search finds the wrong policy             | Relevance and source validation                    |
| Two policies conflict                     | Explicit policy ownership and version resolution   |
| Model invents claims                      | Grounding evaluation and safe response validation  |
| Customer requests unauthorized data       | Server-side authorization                          |
| Index or source becomes unavailable       | Clear error handling and recovery                  |
| Model or retrieval changes reduce quality | Regression tests and controlled rollout            |

The Stage 5 tests passed on synthetic data. They do not prove production-level
accuracy, latency, or security. Those claims need representative workloads and
defined acceptance targets.

## 8. Reusable architecture principles

The most important lessons from design #1 are:

1. Identify the source of truth first. The LLM is not the authority on business
   facts.
2. Use the simplest suitable design. A plain lookup can be better than an agent.
3. Separate retrieval from generation. Finding evidence and writing an answer
   are different responsibilities.
4. Keep authorization outside the model. Every protected business operation
   requires server-side checks.
5. Treat abstention as valid behavior. An unsupported answer is worse than a
   clear escalation.
6. Measure actual task quality. HTTP success alone does not establish
   correctness.

This matches the central architecture principle of Module 01: prefer
deterministic code when dynamic tool decisions are unnecessary.&#x20;

sdt-module-01-agent-fundamentals.md

## Final design decision for #1

**Recommended baseline:** Deterministic FAQ lookup

**Why:** The defined scope uses a small, approved FAQ repository, does not
require live business-system actions, and prioritizes correctness.

**Upgrade to RAG:** When measured retrieval limitations or document complexity
justify generated answers.

**Upgrade to an agent:** Only when new requirements demand adaptive tool use or
multi-step operations.

**The general pattern is:**

`Approved source → authorized access → evidence retrieval → controlled response →
measurement.`

This pattern applies beyond FAQs, including enterprise knowledge assistants and
policy-support systems.

**AI System Design #1 complete — all six stages covered.**
