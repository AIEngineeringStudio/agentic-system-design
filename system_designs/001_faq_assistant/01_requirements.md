# AI System Design #1 — FAQ Support Assistant

`Stage 1 of 6: Requirements`

---

**Goal:**
Design an AI assistant that answers customer questions using only approved
company policies.

## 1. Real-world problem

Imagine an e-commerce company receiving hundreds of customer questions every
day.

**Examples:**

- Can I return an opened product?
- How long does delivery take?
- Can I cancel my order?
- When will I receive my refund?

Today, human support agents read company policies and answer these questions
manually.

**Business goal:**
Automate common FAQ answers while preventing incorrect policy information.

The challenge is not simply generating natural-language answers.
It is ensuring every answer agrees with an approved company policy.

## 2. Actors and responsibilities

| Actor                | Responsibility                                       |
|----------------------|------------------------------------------------------|
| Customer             | Asks a question in natural language                  |
| FAQ administrator    | Maintains approved company policies                  |
| AI support assistant | Finds relevant information and prepares an answer    |
| Human support agent  | Handles questions the assistant cannot safely answer |

**Source of truth:** The approved FAQ repository.

> The AI model is not the source of truth.
> AI model's training data and its own generated statements cannot establish
> company policy.

## 3. Functional requirements

| ID    | Requirement                                         | Priority |
|-------|-----------------------------------------------------|----------|
| FR-01 | Accept customer questions in natural language       | Must     |
| FR-02 | Use only approved FAQ content when answering        | Must     |
| FR-03 | Return a clear answer with supporting FAQ source ID | Must     |
| FR-04 | Refuse to invent answers when evidence is missing   | Must     |
| FR-05 | Provide a human-support escalation path             | Should   |
| FR-06 | Record unanswered questions for FAQ improvement     | Should   |

For this design, `refuse to invent` means the assistant explains that it cannot
confirm the answer from approved information.

## 4. Non-functional requirements

Rank the constraints by importance.

| Rank | Constraint       | Expected behavior                                      |
|------|------------------|--------------------------------------------------------|
| 1    | Correctness      | Answers must be supported by approved policy           |
| 2    | Access control   | Only permitted FAQ content can be used                 |
| 3    | Evidence quality | Every policy answer must reference a real source       |
| 4    | Latency          | Response should be fast enough for interactive support |
| 5    | Simplicity       | Avoid unnecessary architectural complexity             |

⚠️ The curriculum does not specify numerical latency, availability or traffic
targets. We should not invent these as business requirements.

## 5. Scope boundaries

```
✅ In scope — V1
Read approved FAQs, answer policy questions, cite source IDs, and handle missing
evidence.


❌ Out of scope — V1
Process refunds, cancel orders, modify customer records or execute financial
transactions.
```

**Assumptions for our initial design:**
One e-commerce business, a small approved FAQ collection, English questions, and
a read-only assistant. These are teaching assumptions, not confirmed
business requirements.

## 6. Representative customer journey

```
CUSTOMER
    "Can I return an opened item?"

APPROVED FAQ — SYNTHETIC EXAMPLE
    `FAQ-RETURN-01`: "Opened items can be returned within 14 days if undamaged."

EXPECTED ANSWER

    "Yes. According to our return policy, opened items can be returned 
    within 14 days if undamaged."
    
    Source: FAQ-RETURN-01
```

### Important failure scenario

Customer asks:

> Can I return an item purchased during a special promotion?

But the approved FAQs contain no promotion-return policy.

**Correct behavior:** Say the information is unavailable and suggest contacting
support.

**Incorrect behavior:** Invent a plausible promotional return rule.

This is a central requirement of design: `FR-04`.

## 7. Definition of success

The first version succeeds when it can:

- Return supported answers with valid FAQ IDs.
- Avoid making unsupported policy claims.
- Handle unknown questions without fabricating information.
- Keep business actions outside the assistant's authority.

We will later measure these behaviors using synthetic test cases.

> Stage 1 complete — Requirements defined.

---
