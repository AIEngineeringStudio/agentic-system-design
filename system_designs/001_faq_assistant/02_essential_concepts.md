# AI System Design #1 — FAQ Support Assistant

`Stage 2 of 6: Essential AI Concepts`

---

We will learn three concepts using the same customer-support problem.
No frameworks or full architecture yet.

## 1. Model Input and Output

A **Large Language Model (LLM)** takes input text and generates output text.

For our FAQ assistant,
the input can contain a `customer question` and an `approved company policy`.

```
INPUT
    "Can I return an opened item?"
    
            │ 
            ▼
            
LLM
Generates natural-language text

            │ 
            ▼
            
POSSIBLE OUTPUT
    "Yes, you can return the item within 30 days."
```

**Problem:** Where did "30 days" come from?

The model may produce a plausible answer based on learned patterns. That does
not prove it matches this company's policy.

**Lesson:** An LLM can write an answer, but it cannot independently certify that
answer as company policy.

## 2. Grounding

**Grounding means providing trusted evidence that the model must use when
preparing its answer**.

Suppose our approved FAQ repository contains:

`FAQ-RETURN-01` **[Approved · Example]**

"Opened items can be returned within 14 days of purchase if they are undamaged."

Instead of sending only the question to the model, we supply the relevant FAQ
text.

```
Customer question
        |
        ▼
Find matching approved FAQ
        |
        ▼
Question + FAQ evidence
        |
        ▼
LLM generates answer
```

Now the expected answer is:

> Yes. Opened items can be returned within 14 days of purchase if they are
> undamaged.
>
> Source: FAQ-RETURN-01

### Why grounding matters

| Without grounding          | With grounding                              |
|----------------------------|---------------------------------------------|
| Model may invent "30 days" | Answer uses approved "14 days"              |
| Source may be unknown      | Source ID is included                       |
| Hard to verify             | Customer or support team can check evidence |

**Important:** Grounding **reduces the risk** of unsupported answers.
It **does not guarantee correctness**.

The application must still check:

- cited source IDs are valid and
- the answer is supported.

This concept leads toward **retrieval-backed generation**, which we will
implement later.

## 3. Abstention

Abstention means the assistant chooses not to answer when it lacks enough
reliable evidence.

Imagine the customer asks:

> "Can I return an item purchased during a Black Friday promotion?"

The approved FAQ only explains ordinary returns. It says nothing about
promotional purchases.

```
❌ Unsafe answer
    "Yes, Black Friday items have a 30-day return period."
    [This invents a promotional policy.]


✅ Safe answer
    "I couldn't find an approved policy for Black Friday purchases.
    Please contact customer support to confirm."
    [No unsupported policy is invented.]
```

A practical rule is:

```
Relevant approved evidence?
          |
     +----+----+
     |         |
    YES        NO
     |         |
     ▼         ▼
  Answer     Abstain
  + cite     + escalate
```

This is a simplified decision rule.

A matching FAQ is not automatically sufficient; it must actually support the
requested answer.

## 4. Combine the three concepts

Consider three synthetic customer questions.

**Example explorer**

```
- Can I return an opened item?

MATCHED APPROVED FAQ
Opened items can be returned within 14 days of purchase if undamaged.
Source: FAQ-RETURN-01

**Expected assistant response** [Grounded]
Opened items can be returned within 14 days of purchase if undamaged.

---

- How long does standard shipping take?

MATCHED APPROVED FAQ
Standard shipping takes 3-5 business days.
Source: FAQ-SHIPPING-02

**Expected assistant response** [Grounded]
Standard shipping takes 3-5 business days.

---

- Do Black Friday purchases have different return rules?

MATCHED APPROVED FAQ
No relevant approved policy found.

**Expected assistant response** [Abstained]
I couldn't find an approved policy for Black Friday purchases. Please contact 
customer support to confirm.
```

## 5. What we do not need yet

For this first version, we have not established a need for:

- **Autonomous agent:** No multistep independent decision-making is required.
- **MCP:** No reusable external tool integration is required.
- **Vector database:** Small FAQ collection may work with simple text matching.
- **Multi-agent system:** One bounded answer-generation process is enough.

We should introduce these only when requirements justify them.

## Stage 2 takeaway

| Concept            | What it provides                                 |
|--------------------|--------------------------------------------------|
| Model input/output | Understand and generate natural-language answers |
| Grounding          | Base answers on approved evidence                |
| Abstention         | Avoid unsupported answers                        |

**Core principle:**

- The LLM writes the answer.
- Approved company policies establish what the answer can claim.
- Application logic must enforce the evidence rules.

---

> Next:
> **Stage 3 — Minimal Working Architecture**  
> We will draw the smallest ASCII architecture, identify component ownership and
> trust boundaries, and walk through one request with JSON input/output
> contracts.
>
>Continue to Stage 3
