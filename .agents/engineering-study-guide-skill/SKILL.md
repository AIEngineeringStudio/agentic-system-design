---
name: engineering-study-guide
description: Create or refine a self-contained, offline HTML engineering study guide for experienced Senior Software Engineers preparing for Staff and Principal interviews. Use when asked to convert lesson material into a green-themed interactive guide with A4 printing, role-specific interview answers, or to consolidate the guide requirements.
---

# Engineering Study Guide Skill

## Purpose
Produce a single, working HTML5 study guide that supports foundational learning, Senior-level implementation reasoning, and Principal-level architectural judgment. Use plain English while preserving technical accuracy.

## Required input
- Lesson source material and the intended lesson order (normally Lessons 1–20).
- Any requested topic, audience, or scope changes.

If the user supplies only requirements, **do not invent lessons**. Create a requirements/specification HTML instead, clearly labeled as such. If the user asks for a completed lesson guide but the lesson content is missing, ask for the source material. Do not treat a requirements document as the lesson source.

## Audience
**Primary:** Experienced Senior Software Engineer preparing for Staff or Principal Engineer interviews.

Assume familiarity with programming, OOP, REST/HTTP, relational databases, basic system design, Git, testing, and CI/CD. Do **not** assume expertise in DDD, advanced architecture, event-driven systems, distributed consistency, enterprise integration, governance, or Principal-level leadership. Years of experience are not proof of expertise.

## Instruction precedence
1. The user's latest explicit request and supplied source material.
2. This skill's content integrity and accessibility rules.
3. The reference requirements document for details not overridden by the user.

## Workflow
1. Read all supplied lessons and related files. Preserve the original order, scope, and meaning.
2. Identify missing lessons, uncertain claims, contradictions, and duplicated requirements. Ask for essential missing source content rather than inventing it.
3. If factual verification is needed and tools permit it, prioritize official technical documentation. Do not present unverified claims as verified.
4. Build an outline and ensure consistent coverage of each lesson.
5. Generate a **single standalone `.html` file** with embedded CSS and vanilla JavaScript; no external network dependencies, CDN, libraries, images, or fonts.
6. Validate structure, navigation, accessibility, interactivity, offline operation, and A4 print CSS. Test browser behavior where a browser is available; otherwise explicitly distinguish code inspection from actual browser testing.
7. Deliver a link to the HTML and briefly identify any missing content or untested features.

## Lesson template (repeat for each source lesson)
1. Lesson title and objective.
2. **Beginner — Understand:** Plain-English explanation, definitions on first use, why it matters, and appropriate use cases.
3. **Practical example:** Realistic example; code or ASCII diagram only where helpful, with explanation.
4. **Senior — Apply:** At least one realistic interview question and a separate model answer focused on implementation, testing, operational behavior, design trade-offs, and failure cases.
5. **Principal — Evaluate and Lead:** A separate question and model answer focused on competing architectural options, constraints, cross-team/system impact, risks, migration/adoption, leadership, and measurable outcomes.
6. **Key takeaways:** Three to five concise points, including relevant misconceptions.

Keep beginner explanations and advanced interview answers visually distinct. Principal answers must differ in **scope and judgment**, not merely length.

## Dedicated Principal review
After the lessons, include scenario-based Principal review covering architectural choices, scalability, reliability, consistency, security, maintainability, modernization, anti-patterns, organizational trade-offs, cross-team influence, and measurement of outcomes. State assumptions and compare alternatives.

## Learning outcomes
- **Foundational:** Explain concepts, why they exist, use cases, and mistakes.
- **Senior:** Implement, test, troubleshoot, own technical delivery, and defend choices within service/system boundaries.
- **Principal:** Set architectural direction across teams/systems; balance delivery, cost, risk, reliability, and business outcomes; manage ambiguity and migrations; influence adoption.

Learning progression: **Understand → Implement → Lead**.

## Visual system
- Light theme only. White/off-white background, forest-green headings, muted emerald/sage accents, charcoal body text, and subtle borders.
- Clean typography, strong contrast, restrained decoration, consistent spacing.
- Responsive on mobile, tablet, and desktop.
- Semantic HTML5 landmarks, meaningful headings, keyboard-accessible controls, visible focus states, and labeled inputs.
- No dark mode, gradients, distracting animations, or external assets.

## Interactive behavior
Implement in embedded vanilla JS:
- Linked table of contents.
- Keyword search.
- Expand/collapse lesson details and Expand All / Collapse All.
- Show/hide model interview answers for self-testing.
- Completion tracking and overall progress using localStorage, with graceful fallback if storage is unavailable.
- Print / Save as PDF button.

All essential learning content must be available with JavaScript disabled. Use native `<details>` where practical. Do not make content permanently inaccessible due to scripting failures.

## A4 print contract
Use `@page { size: A4; margin: 15mm; }` and `@media print`:
- White background, dark text, legible typography.
- Hide search, sticky navigation, buttons, progress controls, and other UI-only elements.
- Print **all** lessons and answers, even when collapsed on screen. Account for native `<details>` behavior explicitly in print CSS.
- Avoid splitting headings, tables, code blocks, and important content where practical.
- Prevent clipping, horizontal overflow, and unnecessary blank pages.
- Preserve readable ASCII diagrams and code formatting.
- Do not rely on background colors to convey meaning.

## Accuracy and integrity
- Preserve the provided lesson sequence and intended meaning.
- Never manufacture absent lessons, citations, measurements, or source claims.
- Explain specialized terms at first mention.
- Separate verified facts from examples, assumptions, and hypothetical scenarios.
- Use concise, non-academic English suitable for non-native speakers.
- Merge duplicate requirements without dropping unique constraints.
- Do not claim browser or print testing was completed unless it was actually performed.

## Acceptance checklist
- [ ] All supplied lessons are present in the correct order, or omissions are disclosed.
- [ ] Each lesson includes beginner, example, Senior Q&A, Principal Q&A, and takeaways.
- [ ] Principal review section is present.
- [ ] One self-contained HTML file, functional offline.
- [ ] Responsive light-green design with accessible controls.
- [ ] Search, disclosure, completion tracking, and print controls function.
- [ ] A4 print includes all content and answers without clipping.
- [ ] No invented source content or unsupported verification claims.

## Reference
See `references/consolidated-requirements.html` for the consolidated original requirements and reader baseline. It is a **specification**, not the 20 lesson source material.
