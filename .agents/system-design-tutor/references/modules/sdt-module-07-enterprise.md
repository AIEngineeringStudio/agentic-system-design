# Tutor Module 7 — Security and Enterprise Architecture

**Routing identity:** `sdt-module-07-enterprise.md` (match filename even when directory paths are unavailable).

**Load policy:** Use this module only for its own cases or when a specific shared pattern is necessary. Use `sdt-catalog.md` to identify a design; load one anchor file only for an anchor case. For a non-anchor case, derive the worked example using the case's documented architectural choice and `sdt-method-template.md`. Do not imply that the source plan provides complete designs for all 73 cases.

## Anchor files associated with this module

- **Case 57 — Enterprise IAM:** `sdt-anchor-15-enterprise-iam.md`
- **Case 62 — Legacy modernization:** `sdt-anchor-16-legacy-modernization.md`

## Source-derived domain reference

The following section preserves the input roadmap's domain case selection, architectural choices and teaching notes. This is educational reference material, not a claim about any employer's actual systems or interview content.

## 9. Module 7 — Security and Enterprise Architecture

|  # | Design problem              | Main architectural choice                                       |
|---:|-----------------------------|-----------------------------------------------------------------|
| 57 | Enterprise single sign-on   | OIDC/SAML, trust federation, session and token lifetimes        |
| 58 | Multi-factor authentication | Step-up verification, recovery, device trust, risk signals      |
| 59 | Authorization platform      | RBAC vs. ABAC, policy evaluation, revocation                    |
| 60 | Secrets and key management  | KMS/HSM, key lifecycle, rotation, least privilege               |
| 61 | B2B partner API             | Contract versioning, mTLS/OAuth, quotas, failure isolation      |
| 62 | Mainframe modernization     | Strangler migration, anti-corruption layer, dual-run validation |
| 63 | Hybrid-cloud integration    | Connectivity, trust boundary, egress, latency and ownership     |
| 64 | Cardholder-data boundary    | Tokenization, segmentation, audit and PCI scope                 |
| 65 | Consent and privacy service | Consent versioning, policy checks, deletion/retention           |

### Architecture review lens

For each major design, answer within the explanation:

- **Business alignment:** Which capability, customer journey or regulatory need
  is served?
- **Integration:** Which systems already exist? What are their contracts and
  failure modes?
- **Security:** Who is trusted, where does sensitive data move, and who can
  access it?
- **Ownership:** Which team supports each service, schema, shared component and
  incident?
- **Delivery:** How can it migrate safely with rollback and backward-compatible
  interfaces?
- **Cost:** What grows with traffic, storage, redundancy, vendor calls and
  operational effort?
- **Governance:** How are decisions documented, reviewed and revised as
  constraints change?

## Applying this module to a requested case

1. Begin from the exact case's choice/trade-off in the table above; determine what business invariant and user journey make it relevant.
2. Start with one minimal system and an ASCII flow; do not assume microservices, cross-region writes or complex event infrastructure without a constraint.
3. Show at least one credible alternative and its downside; label all invented traffic and latency numbers illustrative.
4. Trace a success path plus the failure path implied by the case's central risk. Recover explicitly from duplicate/reordered/timeout events where they apply.
5. Add security, costs, ownership, DR and migration when they change the architectural decision.
6. Prefer the separate anchor reference for deep cases, or use `sdt-method-template.md` for non-anchor cases. No quizzes or assessments.
