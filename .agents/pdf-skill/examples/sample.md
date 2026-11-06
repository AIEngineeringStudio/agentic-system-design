---
title: "Architecture Decision Field Guide"
cover_lines:
  - "Architecture"
  - "Decision Field Guide"
theme: cyan
number: "06"
total: "06"
tagline: "FRAME THE CHOICE. TEST THE RISKS. RECORD THE REASONING."
cover_note: "A practical reference for clear, evidence-based design decisions."
series: "SOLUTION ARCHITECTURE PRACTICE GUIDE"
audience: "SENIOR SOLUTION ARCHITECTS"
footer_right: "ARCHITECTURE DECISION FIELD GUIDE"
---

## Decision quality at senior level

**Purpose:** Turn a complicated technical choice into a transparent decision that can withstand business and engineering review.

> **Note:** The examples below are illustrative. Replace them with verified details from your own work.

## Contents

1. [Frame the problem](#1-frame-the-problem)
2. [Evaluate trade-offs](#2-evaluate-trade-offs)
3. [Practice worksheet](#3-practice-worksheet)

## 1. Frame the problem

A strong design decision starts with an **observable business need**, not a preferred technology. Name what must be true after the change.

### Questions to answer

- Which user journey is affected?
- What would happen if no action were taken?
- Who is accountable for risk acceptance?

| Dimension | Useful evidence | Warning sign |
|---|---|---|
| Problem | Customer impact and time constraint | Solution described before problem |
| Risk | Failure mode, severity, reversibility | No rollback owner |
| Ownership | Named decision maker and reviewers | Everyone “agreed” but nobody decided |

## 2. Evaluate trade-offs

Compare feasible choices consistently. Include the cost of **doing nothing** when that is a realistic option.

> **Example:** A team compares a full rewrite with an incremental migration. A bounded pilot may reduce uncertainty before committing the organization to a larger operating model.

| Criterion | Keep current | Incremental | Full rewrite |
|---|---|---|---|
| Cost | Low upfront | Moderate | High |
| Delivery risk | Existing limits | Managed change | Broad change |
| Reversibility | High | Often higher | Often lower |

### A simple decision sequence

```text
Define problem -> Compare options -> Test risks -> Decide -> Review results
```

## 3. Practice worksheet

Complete this before a review meeting.

- [ ] Business objective and required outcome are clear.
- [ ] At least two realistic options have been compared.
- [ ] Security, reliability, and cost constraints are explicit.
- [ ] Rollout and rollback responsibilities are assigned.
- [ ] Success measures and review dates are recorded.

**Decision:** _____________________________________

**Why alternatives lost:** __________________________

**Evidence that would change my recommendation:** __________________________
