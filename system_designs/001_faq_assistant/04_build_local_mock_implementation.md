# AI System Design #1 — FAQ Support Assistant

`Stage 4 of 6: Working Local Mock`

The mock uses only Python's standard library. No API keys, external services, or
additional packages are required.

--- 

## 1. What we built

| Component                      | Implementation                              |
|--------------------------------|---------------------------------------------|
| API                            | `POST /faq/ask`                             |
| FAQ repository                 | 12 synthetic FAQ records                    |
| Approved policies              | 10                                          |
| Outdated, conflicting policies | 2, excluded from answers                    |
| Retrieval                      | Conservative keyword matching               |
| Response gate                  | Returns one approved policy or abstains     |
| Tests                          | 9 automated checks, including HTTP requests |

**Important:** We intentionally do not call an LLM yet.
The curriculum requires us to prove that retrieval and evidence handling work
before introducing a model.

## 2. Working architecture

```
+---------------------------+
| Customer / HTTP Client    |
+---------------------------+
              |
              | POST /faq/ask
              ▼
+---------------------------+
| FAQ HTTP API              |
| Validate request          |
+---------------------------+
              |
              ▼
+---------------------------+
| Keyword Matcher           |
| Match approved FAQs only  |
+---------------------------+
              |
              ▼
+---------------------------+
| Synthetic FAQ Repository  |
| 10 approved, 2 outdated   |
+---------------------------+
              |
              ▼
+---------------------------+
| Response Gate             |
| One match -> answer       |
| Otherwise -> abstain      |
+---------------------------+
              |
              ▼
+---------------------------+
| JSON Response             |
| status, answer, source_ids|
+---------------------------+
```

All components run inside one Python process. The FAQ repository is the mock
business source of truth. The customer cannot change approval flags through the
API.

## 3. Core implementation

The main function is `answer_question()`. Its essential logic is:

```python

terms = keywords(question)

matches = [
    record
    for record in FAQS
    if record["approved"]
       and terms.issubset(
        keywords(record["question"])
    )
]

if len(matches) != 1:
    return dict(ABSTAIN)

match = matches[0]

return {
    "status": "grounded",
    "answer": match["answer"],
    "source_ids": [match["source_id"]]
}

```

The complete implementation also validates input and rejects questions with
fewer than two meaningful keywords.

Three important decisions:

- **Approved filtering:** Outdated policies cannot become answers.
- **Conservative matching:** Unknown qualifiers and ambiguous matches cause
  abstention.
- **Exact policy response:** The API returns stored approved text, not generated
  claims.

This is a deliberately narrow matcher, not a general semantic search system.

## 4. Run it locally

Download the Python file and open a terminal in the directory containing it.

### Step A — Run automated tests

```shell
python faq_support_mock.py --test
```

### Step B — Start the API

```shell
python faq_support_mock.py --serve --port 8000
```

The server listens at `http://127.0.0.1:8000`.

### Step C — Send a request

Open a second terminal:

```shell
curl -X POST http://127.0.0.1:8000/faq/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Can I return an opened item?",
    "customer_locale": "en-US"
  }'
```

## 5. Actual execution results

I started the HTTP server and sent real requests to it. These are the observed
outputs, not illustrative predictions.

### Test A — Approved return policy [Passed]

Input: Can I return an opened item?

```json
{
  "status": "grounded",
  "answer": "Opened items can be returned within 14 days of purchase if undamaged.",
  "source_ids": [
    "FAQ-RETURN-01"
  ]
}
```

### Test B — Missing evidence [Passed]

Input: Can Black Friday purchases be returned after 60 days?

```json
{
  "status": "insufficient_evidence",
  "answer": "I cannot confirm this from our approved FAQs. Please contact customer support.",
  "source_ids": []
}
```

The API does not invent promotional policies.

### Test C — Conflicting outdated policy [Passed]

Input: How long does standard shipping take?

```json
{
  "status": "grounded",
  "answer": "Standard shipping takes 3-5 business days.",
  "source_ids": [
    "FAQ-SHIP-01"
  ]
}
```

The outdated 7–10-day policy is excluded.

### Test D — Invalid request [Passed]

Input: Empty question

```json
{
  "error": "question must be a non-empty string of at most 250 characters"
}
```

HTTP status: 400 Bad Request

## 6. What the tests establish

Automated test results : [9 passed · 0 failed]

The test suite covers approved answers, outdated policies, missing evidence,
ambiguity, unexpected instruction text, invalid input, unsupported locale,
fixture integrity and real HTTP handling.

## 7. Limitations of this mock

**This is a working prototype, not a production AI assistant.**

The matcher supports only narrow keyword patterns. It may reject valid
paraphrases. It does not measure semantic relevance, detect all contradictions,
or understand policy meaning. The status `grounded` means an approved record was
uniquely matched, not that general answer correctness has been proven.

Also, Python's `http.server` is appropriate for this local demonstration, but
the official documentation warns against using it as a production web
server.

## Stage 4 takeaway

We now have a verifiable baseline:

Question → approved FAQ lookup → exact answer or abstention.

---

> Next: Stage 5 — Production Evolution.
> We will introduce each improvement only when a requirement justifies it,
> starting with better retrieval, policy freshness, and answer-quality
> evaluation.
>
> Continue to Stage 5