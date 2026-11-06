# Convert the Study Plan into a Modular Tutor

Would it be useful to turn this study plan into a reusable AI study-tutor skill
with learning modules that can be loaded independently?

If so, recommend a structure and explain how it would work. The design should:

- Separate the tutor's teaching approach from design-specific content.
- Load only the module relevant to the learner's current topic, while allowing
  modules to reference one another when useful.
- Explain a design progressively, starting from requirements and building toward
  the final architecture rather than revealing the complete solution at once.
- Let learners move at their own pace, revisit topics, or skip ahead.
- Support understanding without adding unwanted quizzes, tests, or assessments.
- Make it straightforward to add or update modules as the study plan grows.

Focus on a practical structure and learning experience. Avoid proposing extra
features, such as progress analytics, gamification, collaboration tools, or
platform integrations, unless they are necessary to meet these goals.

## Changes for ChatGPT Projects

Skill.md expects routing based on directory structure.

For cases where I can't create/maintain folders like with web based ChatGPT
project sources, create a flat version of the skill with a single folder
`chatgpt-project-flat` containing all the files. Use instruction-based routing.

1. Add `PROJECT_INSTRUCTIONS.txt` with instructions to add in ChatGPT Project
   Instructions.
2. Add `SKILL.md`, `sdt-catalog.md`, and the relevant module files.
3. Add individual anchor and concept files as needed.
