# Shared concept: security, enterprise and operations

Read only when trust boundaries, enterprise integration, multi-region recovery, governance or regulated data matter.

**Trust boundaries:** map which actor controls each network, data store, token and key. Authentication answers identity; authorization answers allowed actions. Use least privilege, protected channels, scoped credentials and audit evidence.

**IAM:** distinguish identity federation (OIDC/SAML), session/token lifecycle, authorization policy (RBAC/ABAC), revocation paths and step-up authentication.

**Sensitive financial data:** minimize exposure, use tokenization and protected key management where applicable. Refer to current PCI Security Standards Council material for current requirements; do not invent compliance claims.

**Reliability:** define SLO/error budget, RPO (maximum tolerable data-loss time) and RTO (maximum recovery time), alert ownership, tested restore and incident response. Multi-region writes introduce conflict, ordering and split-brain problems.

**Enterprise integration:** map source-of-truth ownership, existing legacy contracts, SLAs, change windows and failure modes. Plan backward-compatible APIs, rollout, cutover/rollback, parallel validation and manual reconciliation where needed.

**Operations and cost:** distinguish steady-state from failure-state capacity, rate-limit downstream calls, measure business invariants, document runbooks, and identify which team owns each component.

## Architecture review lens

Business capability; existing integration contract; security/privacy boundary; data ownership; deployment and migration; RPO/RTO; cost and vendor exit; governance. Keep current compliance/service claims grounded in official documentation.
