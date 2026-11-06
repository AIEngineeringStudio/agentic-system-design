---
name: markdown-to-pdf
description: Create or regenerate a print-ready PDF from a Markdown guide using this repository's shared PDF theme.
  Use when asked to make, export, render, or convert a guide or Markdown document to PDF.
---

# Markdown to PDF

Use this skill for Markdown-to-PDF work in this repository so the user does not need to repeat the theme and layout requirements.

## Repository theme

The shared theme is the source of truth:

- Follow `../markdown-authoring/SKILL.md` for readable source Markdown: avoid wide tables and cluttered lists, and prefer standalone bold labels followed by blockquoted explanations for definitions, Q&A, and similar labeled entries.
- Read `pdf-theme/README.md`.
- Use `pdf-theme/print.css` and `pdf-theme/guide.html` for learning guides.
- Follow `AGENTS.md` and any more specific instructions for the document type.
- The standard is Forest / Sage v1, portrait A4, the shared typography, spacing, palette, cover/index treatment, and page numbering. Do not invent a per-document theme.
- Study-pack exports use the shared A4 stylesheet; existing Letter-size PDFs remain unchanged unless regeneration is requested.

## Workflow

1. **Inspect the source and destination.** Read the Markdown structure, identify its title, main sections, code, tables, diagrams, answer keys, references, local assets, and source-verification labels. Check the established PDF output directory and whether the requested destination already exists. Do not edit the Markdown source, overwrite an existing PDF, or modify archived material unless regeneration or replacement is explicitly requested.

2. **Prepare a print-only representation.** Preserve every substantive item and its order. Do not summarize, delete, or rewrite technical content. Keep headings and stable anchors, exercises and numbering, answer references, coverage matrices, and verified-versus-hypothetical labels. Presentation-only changes for PDF readability are allowed without changing the source file:
   - Present glossary and definition entries as standalone bold labels with a colon inside the bold text, followed by blockquoted definitions, rather than tables or bullet/numbered lists. In Markdown, leave a blank line before the blockquote and between entries.
   - Use the same label-plus-blockquote format for Q&A, examples, tradeoffs, and weak/clearer-answer comparisons, not tables or nested lists. Preserve ordinary narrative prose without forcing it into labeled blocks.
   - Preserve each label as a separate paragraph containing `strong`, followed by a `blockquote` for its body in the semantic HTML. Use the existing shared blockquote styling, not per-document overrides. This is a presentation convention; preserve attribution for actual quotations.
   - Avoid decorative or unnecessary bullets in reference material. Keep numbering where it represents actual sequence, such as procedures or exercises.
   - Retain tables where they meaningfully compare structured information; ensure wide tables remain readable and are not clipped.
   - Preserve code, indentation, and diagram meaning. Mark non-wrapping text diagrams with `class="diagram"` when generating HTML.

3. **Build the PDF with the shared template.** Generate semantic HTML using `pdf-theme/guide.html`, `pdf-theme/print.css`, and a compatible renderer. The first page must contain the title and a compact linked index of main sections only, with dot leaders and actual destination page numbers. Start the complete guide on page 2 and count the cover as page 1. Exclude lesson-level headings from the cover index. Resolve page numbers from the final pagination using CSS `target-counter()` or a verified two-pass method; never ship guessed, blank, stale, or placeholder page numbers. Resolve local stylesheets and assets relative to the generated HTML.

4. **Use a reproducible rendering profile.** Prefer Pandoc-generated HTML and WeasyPrint when already available. Inspect converter/renderer versions and resolved regular, bold, and monospace fonts before rendering. Use Palatino/Palatino Linotype when available, otherwise the theme's permitted system fallback; do not install fonts just for an export. Disable converter styling and syntax highlighting as described in the theme README. Do not install tools or dependencies unless the task requires it and the chosen validation/rendering path is missing a dependency. Do not switch renderers casually between repeat exports.

5. **Validate the final artifact with automated checks, not screenshots.** Never rasterize pages, create PNG/JPEG previews, or read page images; image reads fail in this environment. Run the layout validator with WeasyPrint's own interpreter on the generated HTML, writing the PDF through it so the validated rendering is the delivered file:

   ```sh
   PY="$(head -1 "$(command -v weasyprint)" | sed 's/^#!//')"
   "$PY" pdf-theme/check_layout.py /tmp/guide.html --write /tmp/guide.pdf
   ```

   The default checks A4; pass `--page-size Letter` only for a document explicitly rendered at Letter size. Fix every `FAIL` line and re-run until `RESULT PASS`; review each `WARN`. Use text checks (for example, `pdftotext` when installed) for anything else. Together these verify:
   - A4 dimensions, expected fonts/fallbacks, print backgrounds, palette, and page numbering.
   - The cover fits exactly one page, content starts on page 2, and every index number points to the correct final destination.
   - No missing content, broken links, clipped code/tables, changed diagram meaning, orphaned headings, awkward page breaks, or lost answer keys/source labels.
   - Standalone bold labels remain with the beginning of their blockquotes, rather than stranded on the preceding page.
   - Long blockquotes can span pages without clipping or excessive whitespace; do not force an entire long block to stay together.
   - The source Markdown and unrelated/archived PDFs remain unchanged.

   A browser preview that cannot render actual index numbers is not a final indexed PDF. Palette, print backgrounds, and footer appearance come from the unmodified theme and are not visually inspected; say so in the handoff. If a required validation cannot be performed with available tools, report the limitation plainly instead of claiming it passed.

6. **Deliver and record the profile.** Save to the established PDF directory or the user-requested path, choosing an unused path unless overwrite was explicitly authorized. In the handoff, link the PDF and record the theme version, renderer/converter versions, resolved font families/files where available, page size, settings, and exact conversion command. Reuse the profile for repeat exports.

## Reference conversion

For a standard guide with an H1 title and H2 main sections, the theme README documents the Pandoc/WeasyPrint command. Adapt `--toc-depth` to the actual heading hierarchy and exclude any redundant document-title entry from the cover index without removing it from the source. Resolve assets relative to the generated HTML. Confirm with `pdf-theme/check_layout.py` that all index numbers match the final pagination before delivering.
