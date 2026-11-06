# Module 03 — RAG, context engineering and memory

**File:** `sdt-module-03-rag-memory.md`  
**IDs:** #18–#25  
**Module learning goal:** Manage grounded evidence, permission-aware retrieval,
context windows, and durable memory.

## Architectural mental model

`Source -> index/retrieval -> permission filtering -> grounded answer`

Memory is durable user/session information; retrieval is finding source
material; model context is finite. Treat each differently.

## Teaching requirements within this module

Start with the stated business scenario and source of truth. Introduce the
concepts in the **Basics** field only when they unblock the current stage. First
draw the smallest appropriate architecture and implement a safe local mock. Then
show how the named production concern changes it. Do not reveal the reference
final architecture at the beginning of a lesson. Do not quiz the learner. If a
case is marked as an anchor in `sdt-catalog.md`, check whether its individual
anchor file is available; otherwise derive the same depth from this case brief.

## Case briefs

### #18 Document Q&A with RAG [DEEP-DIVE ANCHOR]

- **Problem:** Answer from approved enterprise documents.
- **Basics at point of use:** Chunking, embeddings, retrieval, grounding.
- **Working mock:** Index synthetic documents and answer with source references.
- **Production evolution:** Retrieval evaluations, ACLs, deletions and
  staleness.
- **Architectural trade-off:** Long context vs retrieval.

### #19 Permission-aware enterprise search

- **Problem:** Different users have different document rights.
- **Basics at point of use:** ACL prefiltering, search trimming, identity.
- **Working mock:** Search a fake HR/engineering collection as multiple users.
- **Production evolution:** Propagate revocations and prevent snippet leakage.
- **Architectural trade-off:** Pre-filter vs post-filter.

### #20 Hybrid search and reranking

- **Problem:** Find exact IDs and conceptual matches.
- **Basics at point of use:** Keyword/BM25, vectors, fusion, reranking.
- **Working mock:** Compare keyword/vector/hybrid results on a benchmark.
- **Production evolution:** Freshness, rank quality, p95 latency and indexing
  cost.
- **Architectural trade-off:** Semantic vs lexical vs hybrid.

### #21 Customer 360 evidence assistant [DEEP-DIVE ANCHOR]

- **Problem:** Join CRM facts, orders and internal policies.
- **Basics at point of use:** Structured+unstructured federation and evidence.
- **Working mock:** Join mock SQL customer records with cited policy passages.
- **Production evolution:** Source ownership, conflicts, ACLs and misleading
  joins.
- **Architectural trade-off:** Federation vs centralized knowledge store.

### #22 Long-term assistant memory

- **Problem:** Retain only useful and approved preferences.
- **Basics at point of use:** Session summaries, memory, retention/consent.
- **Working mock:** Save, inspect, update and delete preferences in local
  storage.
- **Production evolution:** Staleness, privacy, injection and deletion
  propagation.
- **Architectural trade-off:** Session vs long-term memory.

### #23 Multilingual policy assistant

- **Problem:** Answer questions across languages.
- **Basics at point of use:** Cross-lingual retrieval and translation.
- **Working mock:** Build synthetic bilingual FAQ with source-language
  citations.
- **Production evolution:** Test language quality and local legal caveats.
- **Architectural trade-off:** Translation-first vs multilingual retrieval.

### #24 Near-real-time knowledge indexing

- **Problem:** Reflect changed business data in answers.
- **Basics at point of use:** CDC/event indexing, tombstones, eventual
  consistency.
- **Working mock:** Update search from mock change events.
- **Production evolution:** Replay ordering, ACL changes and rebuild.
- **Architectural trade-off:** Batch vs event-driven ingestion.

### #25 Evidence verification agent

- **Problem:** Label unsupported claims in a report.
- **Basics at point of use:** Claim extraction, citation matching, abstention.
- **Working mock:** Verify claims against stored passages and flag missing
  evidence.
- **Production evolution:** False citations, independent retrieval and human
  review.
- **Architectural trade-off:** Model self-check vs evidence verification.

## Common misconceptions to correct

- Having an AI model in a request path does not automatically require agent
  orchestration.
- A technically valid diagram is not sufficient without authorization, state
  ownership and failure behavior.
- Examples should use synthetic data, explicitly labeled assumptions and local
  runnable behavior where possible.
