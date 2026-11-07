# AI System Design #1 — FAQ Support Assistant

`Stage 3 of 6: Minimal Architecture`

---

**Goal:**
Build the smallest system that answers customer questions using approved FAQs,
cites evidence, and refuses unsupported answers.

We will use ASCII diagrams, typed contracts, one successful request, and one
failure path. No unnecessary frameworks.

## 1. Minimal component architecture

```
+----------------------------+
|          Customer          |
+----------------------------+
              |
              | Question
              ▼
+----------------------------+
|       FAQ Answer API       |
| - Validate input           |
| - Coordinate processing    |
+----------------------------+
              |
              | Search
              ▼
+----------------------------+
|       FAQ Lookup           |
| - Find matching FAQ        |
| - Only approved records    |
+----------------------------+
              |
              | Approved evidence
              ▼
+----------------------------+
|           LLM              |
| - Question + FAQ evidence  |
| - Generate answer draft    |
+----------------------------+
              |
              | Draft
              ▼
+----------------------------+
|       Response Gate        |
| - Check source IDs         |
| - Enforce safe fallback    |
| - Answer or abstain        |
+----------------------------+
              |
              ▼
+----------------------------+
|          Customer          |
+----------------------------+

FAQ Lookup reads from:
+----------------------------+
|     Approved FAQ Store     |
|  Business source of truth  |
+----------------------------+
```

This is a logical component diagram.
All application components can initially run in one backend process.

### Component responsibilities

| Component      | Responsibility                                   |
|----------------|--------------------------------------------------|
| Customer       | Submits a natural-language question              |
| FAQ Answer API | Validates and coordinates the request            |
| FAQ Lookup     | Finds relevant approved policies                 |
| FAQ Store      | Holds authoritative policy records               |
| LLM            | Produces a natural-language draft using evidence |
| Response Gate  | Decides whether a safe response can be returned  |

**Critical distinction:**
The LLM drafts text. The application controls which sources can be used and what
is returned.

For a small FAQ set, an approved-text response may be safer than accepting an
unchecked LLM paraphrase.

## 2. Request sequence — happy path

Assume the approved FAQ store contains this synthetic record:

```
{
  "source_id": "FAQ-RETURN-01",
  "text": "Opened items can be returned within 14 days if undamaged.",
  "approved": true
}
```

**Request flow**

```markdown

1. Customer sends question

   `Can I return an opened item?`

2. API validates input

   Confirms the question is present and within accepted length limits.

3. FAQ Lookup retrieves evidence

   Returns `FAQ-RETURN-01`, which is marked approved.

4. LLM drafts a grounded response

   The model receives the question and matching policy text, not unrestricted
   authority to invent return rules.

5. Response Gate processes the draft

   Checks the cited source ID against retrieved evidence.
   For the conservative V1, it can return the exact approved policy text
   instead of relying on an unverified paraphrase.

6. API returns the answer

   Includes the response status and server-verified source ID.
```

**Expected response:**

```json
{
  "status": "grounded",
  "answer": "Opened items can be returned within 14 days if undamaged.",
  "source_ids": [
    "FAQ-RETURN-01"
  ]
}
```

## 3. Typed API contracts

We need clear types between components.
Below are simple Python-style contracts for our logical JSON messages.

```python
from typing import Literal, TypedDict


class AskRequest(TypedDict):
    question: str
    customer_locale: str


class FAQRecord(TypedDict):
    source_id: str
    text: str
    approved: bool


class AskResponse(TypedDict):
    status: Literal["grounded", "insufficient_evidence"]
    answer: str
    source_ids: list[str]
```

The public API is:

`POST /faq/ask`

**Request:**

```
{
  "question": "Can I return an opened item?",
  "customer_locale": "en-US"
}
```

**Response types:**

| Field        | Type         | Meaning                                    |
|--------------|--------------|--------------------------------------------|
| `status`     | Enum         | `grounded` or `insufficient_evidence`      |
| `answer`     | String       | Customer-visible response                  |
| `source_ids` | String array | Approved FAQ records supporting the answer |

These are teaching-level contracts. Network errors and detailed validation
errors will need additional handling when we implement the API.

## 4. Trust boundaries and ownership

A correct architecture must separate the customer's input, business policy, and
model output.

```
**Customer question**

Untrusted input. The customer may provide incorrect claims or malicious
instructions.



**Application boundary**

Validates the request, selects approved evidence, and controls the output.



**FAQ repository**

FAQ administrators own the policy content and approval status.



**LLM output**

A draft, not trusted evidence. It cannot approve policies or grant itself
access.

```

The response gate must never accept a source ID merely because the LLM generated
it.

Checking source IDs alone does not prove that every statement in the answer is
supported. That is why the initial version can return exact approved policy text
or a controlled template.

## 5. One failure path — missing evidence

Customer asks:

> "Can Black Friday purchases be returned after 60 days?"

Suppose the FAQ repository contains no approved Black Friday return policy.

```
+---------------------------+
| Customer question         |
+---------------------------+
             |
             ▼
+---------------------------+
| Search approved FAQs      |
+---------------------------+
             |
             ▼
+---------------------------+
| No sufficient evidence    |
+---------------------------+
             |
             ▼
+---------------------------+
| 'Do not generate' policy  |
| Use safe fallback         |
+---------------------------+
             |
             ▼
+---------------------------+
| Abstain and offer support |
+---------------------------+
```

Expected response:

```
{
  "status": "insufficient_evidence",
  "answer": "I cannot confirm the Black Friday return policy from our approved FAQs. Please contact customer support.",
  "source_ids": []
}
```

Notice that `no LLM call is required when sufficient evidence is absent`. This
saves work and avoids an unnecessary chance of fabrication.

A **lookup-service outage is different from a genuine no-match result**.
In implementation, we must **report the outage as an error rather than silently
treating it as missing policy**.

## 6. Architecture decisions

| Decision                     | Reason                                                      |
|------------------------------|-------------------------------------------------------------|
| Single backend application   | Keeps V1 simple                                             |
| Read-only FAQ repository     | No customer-facing policy modifications                     |
| Simple FAQ matching first    | Small approved FAQ set                                      |
| Optional LLM drafting        | Natural wording without giving the model business authority |
| Application-owned source IDs | Prevents fabricated citations                               |
| Explicit abstention          | Prevents unsupported policy claims                          |

We do not need MCP, multi-agent orchestration, a vector database, or a workflow
engine yet.

These would add complexity without solving a demonstrated requirement.

## Stage 3 takeaway

The key design principle is to **keep evidence and business decisions outside
the LLM**.

The lookup finds approved information. The model can help with wording. 
The application decides whether the answer is safe to return.

---

> Next: **Stage 4 — Build a Working Local Mock**
>
> We will create a small Python implementation with synthetic FAQs, a working
> lookup function, a local answer endpoint, valid source IDs, and visible
> failure
> behavior. We will verify its output before adding a real model.
>
> Continue to Stage 4
