# Anchor design #18 — Document Q&A with RAG

**Tutor-only deep reference.** Intended for incremental teaching, not to be
shown in full during Stage 1 unless the learner requests a complete design.

**Primary module:** `sdt-module-03-rag-memory.md`  
**User scenario:** Employees need answers from approved company documents, with
enough citations to verify important statements.

## Stage 1 — Actors, constraints and source of truth

- Document owners: define source access policy and effective versions.
- Ingestion/indexing: creates searchable derived data; index is not source of
  truth.
- Retrieval/answer API: enforces ACLs before passages reach the model.

**Priorities to discuss:** correctness and permission boundary first;
interactive latency and complexity second. Ask for missing hard constraints only
when they materially affect design, otherwise state illustrative assumptions
explicitly.

## Stage 2 — Basics introduced only when needed

- Chunking: split a document into retrievable passages while retaining source
  identity.
- Embedding: encode semantic similarity; not a replacement for exact identifier
  search.
- Grounded generation: answer only using retrieved evidence and cite passages.

## Stage 3 — Minimal working architecture

```text
+-------------------------+
|  Employee question      |
+-------------------------+
             |
             v
+-------------------------+
| Auth + retrieval filter |
+-------------------------+
             |
             v
+-------------------------+
| Document search index   |
| with source references  |
+-------------------------+
             |
             v
+-------------------------+
| Grounded answer model   |
+-------------------------+
```

**Illustrative logical request** (not necessarily literal protocol wire format):

```json
{"question":"What is the travel approval rule?","user_id":"employee-42"}
```

**Illustrative logical result**, generated from synthetic data:

```json
{"answer":"Approval is required for the covered travel category.","citations":[{"document":"policy-3","section":"2.1"}],"status":"grounded"}
```

Explain actor → first authorized boundary → real source of truth → returned
data. Highlight where the model suggests actions but the service decides whether
to execute them.

## Stage 4 — Hands-on lab

Create 25 synthetic policy snippets with document IDs and group ACLs. Implement
keyword retrieval and cite exact passage IDs. Compare to a simple vector or
hybrid retrieval implementation only when search quality makes it useful.

Keep the proof of concept small and runnable; provide exact setup, fixture data,
observable output and a negative or failure test. Do not pretend a prototype is
production-ready, or claim a protocol implementation is official without a
verified SDK.

## Stage 5 — Production evolution (not all at once)

| New constraint                   | Justified change                                                                     | Evidence of correct behavior                      |
|----------------------------------|--------------------------------------------------------------------------------------|---------------------------------------------------|
| Users have different permissions | Enforce ACL prefiltering/authorization at retrieval, not after generating an answer. | Negative cross-group citation test.               |
| Documents change                 | Index updates and deletions must propagate with freshness metadata.                  | Stale-index and tombstone test.                   |
| Exact codes are important        | Combine keyword and semantic retrieval; optionally rerank.                           | Evaluate recall for codes and semantic questions. |
| Model invents citations          | Validate cited IDs against actually retrieved passages; abstain when missing.        | Citation-precision regression suite.              |

**Critical failure to walk through:** HR-only policy appears in search results
for an engineering user; retrieval must reject it before text reaches the model.

## Stage 6 — Architecture judgement

Long-context prompting can be appropriate for a small known set; RAG is
preferable when the corpus is large, changeable, permissioned or must support
search across sources.

**Reusable pattern:** begin with a clear source of truth, a bounded action/data
interface and the simplest credible user experience. Add distributed components
only when stated requirements force those boundaries. Show the final production
diagram only once the learner has seen which requirement justified each
addition.
