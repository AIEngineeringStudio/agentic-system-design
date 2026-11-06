# Interactive Pattern Lesson Flow

Use this progression over several turns. The shared `first-principles-learning`
skill supplies each turn's language, explanation, professional articulation,
and one small hands-on task with runnable code and exact run instructions.
Choose a runnable prediction or modification task at diagnosis steps; do not
require the learner to produce a full refactor before the necessary concept
has been explained.

1. **Baseline:** establish the current requirement and the smallest reasonable
   working implementation. Include a behavior check.
2. **Pressure:** introduce one realistic change and let the learner inspect
   its effect. Add a second change only if the design pressure remains unclear.
   Distinguish a harmless conditional from responsibilities that change
   independently.
3. **Diagnosis:** identify stable behavior, variable behavior, the current
   dependency, and the proposed boundary. Show a small before/after dependency
   diagram when helpful. Ask the learner to predict the effect of a change.
4. **Refactor:** make one meaningful change at a time and rerun behavior checks.
   Extract a function first when sufficient; introduce contracts or types only
   when they serve the identified variation. Explain selection and wiring.
5. **Validation:** check existing and new behavior, substitution or isolation
   where relevant, and failure behavior for distributed/concurrent work. Make
   the outcome observable rather than testing class names or folder structure.
6. **Name and evaluate:** connect the derived design to the pattern's intent.
   Explain the dependency change, concrete costs, when the original design is
   preferable, and a neighboring pattern. For a named-pattern request, this
   consolidates terminology already acknowledged at the start.
7. **Transfer:** introduce a fresh requirement and have the learner predict,
   modify, or defend the design. Use the assessment reference when checking
   completion; give one exercise at a time, not an automatic exercise bundle.
8. **Close or pause:** record observed progress using the checkpoint template.
   Choose a relevant next step rather than restarting the pattern.

For a complete guide, this progression may organize sections without response
gates. Quick clarifications do not require this flow. Production concerns should
extend an understood example, not add infrastructure to every baseline.
