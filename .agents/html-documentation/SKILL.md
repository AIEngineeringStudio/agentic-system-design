---
name: html-documentation
description: Create documentation or guides as a single self-contained, light-themed, PDF-friendly HTML file when the user requests HTML output.
---

# HTML Documentation

Use this skill whenever the user asks for documentation, a guide, or learning
material in HTML format. Apply it together with any content-specific skill
selected by `AGENTS.md`.

When `first-principles-learning` also applies, use its complete-guide mode:
retain the learner's preferred language, visuals, examples, and useful
exercises, but cover the full requested scope without stopping after each
concept. Exercises in the guide are for self-study and do not block delivery.
Organize technology topics by prerequisites and distinguish concept exercises
from production extensions using `tech-stack-curriculum` when relevant. The
source-completeness gate below still applies.

## Source completeness gate

Before generating the deliverable:

1. Identify every source the requested document must cover.
2. Retrieve and read each source completely. If output is truncated or
   paginated, continue until the end of the source is reached.
3. Confirm that no required section is missing. Do not replace unavailable
   content with guesses, summaries presented as complete, placeholders, or
   ellipses.
4. If a required source cannot be retrieved completely, do not produce the final
   HTML file. Explain what is missing and request the source or access needed to
   continue.

Generate and return the final file only after this completeness check passes.

## Deliverable requirements

- Produce exactly one `.html` file as the document deliverable.
- Make the file fully self-contained. Put all CSS in a `<style>` element in the
  HTML.
- Do not depend on external stylesheets, fonts, scripts, images, or other
  assets.
- Use a clean, light theme with strong contrast and comfortable line length,
  spacing, and typography.
- Use semantic HTML and a logical heading hierarchy. Prefer elements such as
  `main`, `article`, `section`, `nav`, `header`, `footer`, `figure`, `table`,
  `pre`, and `code` when they match the content.
- Use a simple, responsive, single-column layout. Avoid positioning,
  fixed-height containers, multi-column layouts, and decorative structures that
  split poorly across printed pages.
- Style inline code and code blocks for clear screen reading and reliable PDF
  printing. Preserve whitespace, allow safe wrapping where needed, and prevent
  content from being clipped in print.
- Include print CSS with sensible page margins and page-break handling. Keep
  headings with the content that follows them when practical, and avoid
  splitting code blocks, tables, figures, callouts, and list items across pages
  when doing so would harm readability.
- Ensure printed output remains readable without relying on background colors.
  Hide controls or navigation that have no value in the PDF.

## Verification

Before returning the file, verify that:

- all required source content is represented and no placeholder text remains;
- the document has a doctype, language, character encoding, viewport metadata,
  and a descriptive title;
- every style is embedded and the document has no external runtime or asset
  dependency;
- heading levels are ordered coherently and the document is usable without
  scripts;
- code blocks, tables, links, and long text do not overflow or become
  unreadable;
- print styles are present and page-break behavior is reasonable;
- the HTML opens successfully and, when rendering tools are available, both
  screen and print/PDF output have been inspected.

After verification, hand off only the final `.html` file (or its file link). Do
not add alternate formats unless the user asks for them.
