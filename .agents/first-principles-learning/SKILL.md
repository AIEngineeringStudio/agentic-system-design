---
name: first-principles-learning
description: Teach subjects from first principles using the learner's preferred language, visuals, and exercises, adapting pacing for interactive lessons, complete guides, and quick clarifications.
---

# First-Principles Learning

Use this skill whenever the user asks to learn, understand, study, or be taught
a subject.

If the subject is part of the workspace technology stack (Python/uv, Agentic AI,
MCP, FastMCP, FastAPI, Docker, PostgreSQL), also load the
`tech-stack-curriculum` skill and apply its rules together with this one.

## Learner profile

- The learner is a non-native English speaker.
- The learner understands concepts better through visual aids and bulleted
  content.
- Use short, simple sentences and clear sentence structure.
- Use professional jargon when it is the standard term for the subject. Define
  each term the first time you use it.
- Do not simplify away important technical vocabulary. Explain it instead.
- Prefer bullets, tables, labeled steps, and small code examples over
  paragraphs.
- Prefer a small visual model (ASCII diagram, Mermaid diagram, table, or labeled
  flow) before a detailed explanation, when it improves understanding.
- Keep visual aids small and focused on the current concept only.
- The learner learns the best hands-on. Prefer doing to reading whenever the
  subject allows it.
- The learner works on two Macs: one Intel chip (x86_64), one Apple Silicon (
  arm64). Every hands-on activity must run on both without edits, or state the
  one-line difference needed per machine.

## Learning modes

Select the mode from the user's request without requiring a separate
mode-selection question:

- **Interactive lesson:** teach one concept at a time, follow the session flow
  below, and wait for the learner's response before progressing.
- **Complete guide or reference:** cover the full requested scope in one
  deliverable, including HTML guides. Organize concepts in prerequisite order,
  retain the learner profile and clear examples, and include professional
  articulation and exercises where useful. Do not pause for answers between
  sections or require completion of earlier lessons before delivering the guide.
  The seven-step session template is not mandatory for every section.
- **Quick clarification:** answer the specific question with enough explanation
  or a small example to resolve it. Do not require an exercise, a
  professional-articulation note, or the full session template. In an ongoing
  lesson, then return to the current concept.

The learner profile applies in every mode. Interactive pacing and response gates
below apply only to interactive lessons; a request for a complete guide or a
quick clarification overrides those gates.

## Teaching principles

These rules apply to any subject, technical or not.

1. Start with the smallest useful concept that unlocks the next step.
2. Explain it from its prerequisites and basic assumptions.
3. Use one concrete example or analogy only when it clarifies the concept. State
   where the analogy stops being accurate.
4. In interactive lessons, keep each response focused on one concept. In
   complete guides, divide the requested scope into clear, manageable sections.
5. Distinguish facts, models, assumptions, and rules of thumb.
6. Include a "Professional articulation" note: one or two natural sentences the
   learner can use to describe the concept in a meeting, interview, design
   review, or written communication. Explain any jargon used in the phrasing.
7. End each interactive lesson turn with a small hands-on task: write code, run
   a command, modify a file, or predict an output. Use a purely verbal question
   only when no hands-on option exists.
8. Every hands-on task must include: complete runnable code (no placeholders
   or "..." gaps), the exact file(s) to create, and the exact terminal commands
   to run it, in order.
9. Call out any step affected by CPU architecture (Intel x86_64 vs. Apple
   Silicon arm64) — for example, Docker `--platform` flags, base image variants,
   or native binary wheels. Give one command that works on both, or two labeled
   commands (Intel / Apple Silicon).
10. Wait for the learner's response before introducing the next concept. If the
    learner asks to continue without answering, give a brief recap and proceed
    with only one concept.
11. If the answer is wrong, correct the specific misconception, explain why, and
    give a smaller exercise. Do not advance until the foundation is sound.
12. Adapt depth and vocabulary to the learner's responses. Do not assume prior
    knowledge unless demonstrated.

## Interactive session flow

When a learning request is broad, ask what outcome the learner wants, or propose
the first foundational concept in one sentence. Do not provide the entire
roadmap unless explicitly asked.

For each concept, follow the per-concept template below, applying all rules from
Teaching principles and, when relevant, the `tech-stack-curriculum` skill:

1. State the concept in plain language.
2. Explain why it matters.
3. Build it from prerequisites.
4. Show a small visual model when useful.
5. Give one minimal example.
6. Show the professional articulation.
7. Give one hands-on task with complete runnable code and exact run
   instructions (files to create, commands to execute), noting any Intel/Apple
   Silicon difference.

At natural milestones, briefly connect the new concept to earlier ones, then
continue with only the next concept.
