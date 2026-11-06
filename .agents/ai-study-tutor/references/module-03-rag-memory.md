# Module 03 — RAG, context engineering and memory

**Learning boundary:** Control what evidence enters model context, and keep
provenance, access and lifecycle explicit.

**One-line mental model:**
`Source -> ingest/index -> permission-aware retrieve -> cited model answer`

## Necessary concepts, only when the case needs them

Retrieval is a query-time search over owned sources, not model memory. **RAG**
uses retrieved passages to ground generated answers. Memory is stored state with
purpose, consent, expiry and deletion; it is not equivalent to dumping all past
chats into a prompt. Retrieval quality and answer quality are separately
measured.

## Patterns and decisions to reuse

- **Primary decision rule:** Do not cite content the system did not retrieve or
  grant permission to access.
- Start with the baseline boundary and identify source of truth, authority and
  error semantics before selecting products.
- Show one happy path and one failure path, then justify added components as
  responses to constraints.
- Keep code labs small and local with fake records; label production
  architecture as a design, not deployed implementation.

## Problem briefs (these are design prompts, not pre-solved lessons)

### #18 — Document Q&A with RAG ★ anchor

**User need:** Answer questions from an internal document set.

- **Teach on demand:** Chunking, embeddings, retrieval and citations.
- **Small working lab:** Index sample files and cite passages.
- **Production evolution:** Evaluate retrieval, support deletions and source
  ACLs.
- **Decision to explain:** Entire-document context vs retrieval.

### #19 — Permission-aware enterprise search

**User need:** Two users must see different document results.

- **Teach on demand:** ACL filtering, tenant security, provenance.
- **Small working lab:** Search a mock HR/engineering corpus under different
  users.
- **Production evolution:** Enforce security trimming before leaking snippets.
- **Decision to explain:** Pre-filter vs post-filter and index separation.

### #20 — Hybrid search and reranking

**User need:** Find both product identifiers and semantic matches.

- **Teach on demand:** Keyword search, vectors, fusion, rerank.
- **Small working lab:** Compare lexical, semantic and hybrid results.
- **Production evolution:** Tune relevance, latency, freshness and cost.
- **Decision to explain:** Keyword vs vector vs hybrid.

### #21 — Customer 360 evidence assistant ★ anchor

**User need:** Combine CRM records, orders and policy text.

- **Teach on demand:** Structured/unstructured federation.
- **Small working lab:** Join mock SQL order tools with indexed policies.
- **Production evolution:** Enforce source-level permissions and reconcile
  conflicts.
- **Decision to explain:** Tool federation vs centralized data model.

### #22 — Long-term assistant memory

**User need:** Persist only useful user-approved information.

- **Teach on demand:** Session state, episodic memory, retention.
- **Small working lab:** Save, retrieve, inspect and delete explicit
  preferences.
- **Production evolution:** Consent, privacy, stale entries, prompt injection.
- **Decision to explain:** Per-session summary vs long-term memory.

### #23 — Multilingual policy assistant

**User need:** Answer policy questions across two languages.

- **Teach on demand:** Multilingual search and localization.
- **Small working lab:** Create bilingual source-backed Q&A.
- **Production evolution:** Evaluate language-specific accuracy and caveats.
- **Decision to explain:** Translate-first vs multilingual retrieval.

### #24 — Near-real-time knowledge indexing

**User need:** User changes must appear promptly in AI answers.

- **Teach on demand:** CDC, events, index refresh and tombstones.
- **Small working lab:** Update a local search index from mock change events.
- **Production evolution:** Ordering, replay, access revocation and rebuild.
- **Decision to explain:** Batch ingestion vs event-driven sync.

### #25 — Evidence verification agent

**User need:** Find unsupported statements in an analysis.

- **Teach on demand:** Claim extraction and evidence matching.
- **Small working lab:** Flag claims not backed by cited source excerpts.
- **Production evolution:** Handle false citations, conflicting evidence and
  uncertainty.
- **Decision to explain:** Model self-check vs independent source verification.

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

**Case IDs in this module:** #18, #19, #20, #21, #22, #23, #24, #25.
