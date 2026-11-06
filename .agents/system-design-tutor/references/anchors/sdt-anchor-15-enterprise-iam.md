# Anchor 15 — Enterprise IAM

**Catalog case:** 57 — Enterprise single sign-on. **Primary module:** `sdt-module-07-enterprise.md`. **Optional shared concept:** `sdt-concept-04-security-operations.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Authenticate workforce/partner identities and authorize enterprise actions across many applications while supporting federation and revocation.

## 2. Functional requirements

Federated login; issue/validate sessions or tokens; evaluate permissions; rotate keys; revoke access; record evidence.

## 3. Ranked non-functional constraints

Security, least privilege, revocation responsiveness, operational uptime and integration compatibility.

## 4. Workload and assumptions

Identity providers, protocols, acceptable offline authorization staleness and organization policy must be specified.

## 5. Contracts and error semantics

OIDC/SAML federation with approved IdP; policy-check interface `is_allowed(subject, action, resource, context)`; administrative provisioning and audit.

## 6. State model and invariant

Identity mapping; groups/roles/attributes; authorization policy versions; token/session metadata and revocation signals.

## 7. Minimum viable architecture (ASCII)

```text
User -> Enterprise IdP -> Federation broker -> App session/token
                                          |
App/API -> Policy enforcement -> Decision service -> Policy store
                                   |
                            Revocation/audit events
```

## 8. Requirements -> decisions -> trade-offs

1. Federation delegates credential validation; applications still enforce resource-level authorization.
2. RBAC is simpler for stable roles; ABAC is flexible but can complicate debugging/governance.
3. Cached authorization decisions reduce latency but require explicit revocation/staleness contracts.

## 9. Critical execution paths

**Successful flow:** Authenticate with IdP -> validate assertion/token and audience -> establish scoped session -> evaluate policy at resource access -> log relevant decision.

**Failure / retry / recovery:** Revoked user with cached token may remain active until refresh unless short lifetimes or push revocation exist. IdP outages need declared break-glass/service continuity design.

## 10. Scale, security and enterprise review

**Scale and reliability:** Cache verifiable keys and policy data carefully, measure decision latency, isolate tenants and protect authorization service from request amplification.

**Enterprise and operational readiness:** Joiner/mover/leaver workflow, privileged approvals, least privilege reviews, audit retention, service ownership and threat modeling.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

For external B2B partners, tenant-scoped policy and identity mapping become more important than for a single workforce realm.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
