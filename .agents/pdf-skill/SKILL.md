---
name: architect-field-notes-pdf
description: Create polished, print-friendly, A4 PDFs from Markdown using the exact visual system of the Senior Solution Architect behavioral interview guides: deep navy editorial cover, per-topic accent colors, Inter typography, numbered navigation, teal/cyan-style callouts, ruled chapter headings, zebra tables, headers and footers. Use for new interview guides, study guides, architecture handbooks, field notes, or consistent collections.
---

# Architect's Field Notes — PDF Style Skill

Create PDFs with the same **visual language** as the original five Senior Solution Architect study guides. Prefer the bundled **Markdown → standalone HTML → WeasyPrint PDF** pipeline. Do not redesign these documents unless the user requests a different style.

## When to use

Use when the user requests PDF files matching the earlier study guides, the *Architect's Field Notes* visual style, or a series of consistent interview / learning documents. It can also style other long-form Markdown handbooks, provided an editorial A4 layout is appropriate.

## First steps

1. Check the project for a local `SKILL.md` and follow it if present.
2. Read `references/style-guide.md` for exact visual tokens and layout behavior.
3. Confirm the source is available. Preserve the source's sequence, claims, examples, disclaimers, tables, and worksheet blanks; do not fabricate information.
4. Use `scripts/build_pdf.py` with the original Markdown and appropriate cover metadata. Prefer content in Markdown plus YAML frontmatter (see `examples/sample.md`).
5. Always render and inspect the output; use `scripts/qa_pdf.py` as a first check, not a substitute for page review.

## Non-negotiable design rules

- A4 portrait, light pages, deep navy full-bleed cover (`#112C3A`); **no dark interior or dark mode**.
- Inter for body text and Inter Display for display headings when installed. Use system font fallbacks if unavailable. Do not package/distribute font files.
- Branded cover with small letterspaced masthead, accent bar, large title (white line + colored line), quiet subtitle, fine separator, edition number, and circular outline ornament.
- White editorial pages: left/right 19 mm margins, small uppercase running header, two-digit footer page number, compact headings, cyan/teal-style vertical accent on callouts, and navy table headers.
- The accent theme is per topic. Keep the base design identical across a series. Available themes: `teal`, `amber`, `lavender`, `coral`, and `cyan`. Exact colors are in `references/style-guide.md`.
- Page 1 is a full cover. Page 2 is introduction and auto-generated clickable table of contents. Main content starts on page 3. Chapters continue rather than always starting new pages.
- Preserve meaningful blank worksheet cells and checkbox lists; do not replace blank fields with generated answers.

## Build a PDF

```bash
python scripts/build_pdf.py input.md \
  --output output.pdf \
  --html output.html \
  --theme cyan \
  --number 05 --total 05 \
  --title 'Problem Solving & Decision Making' \
  --cover-lines 'Problem Solving|& Decision Making' \
  --tagline 'DIAGNOSE THE PROBLEM. WEIGH THE OPTIONS. OWN THE OUTCOME.'
```

Generated `.html` is **self-contained**, with inlined CSS and no network requirements; it is also print-friendly. Do not manually modify generated HTML unless the rendering script cannot support a specific content requirement.

### Reusable document metadata

Frontmatter in the Markdown source can configure:

```yaml
---
title: "Problem Solving & Decision Making"
cover_lines: ["Problem Solving", "& Decision Making"]
theme: cyan
number: "05"
total: "05"
tagline: "DIAGNOSE THE PROBLEM. WEIGH THE OPTIONS. OWN THE OUTCOME."
brand: "THE ARCHITECT'S FIELD NOTES"
series: "BEHAVIORAL INTERVIEW STUDY GUIDE"
audience: "SENIOR / PRINCIPAL SOLUTION ARCHITECT INTERVIEWS"
footer_right: "PROBLEM SOLVING & DECISION MAKING"
footer_left: "SENIOR / PRINCIPAL SOLUTION ARCHITECT"
cover_note: "A practical guide to evidence-based STAR answers, senior-level judgment, and focused rehearsal."
intro_label: "YOUR STUDY COMPANION"
---
```

The source requires `##` chapters. A pre-existing `## Contents` or `## Table of contents` is replaced with a generated, clickable contents list. All other source text is retained. If headings are not numbered, the builder uses all second-level headings as chapters. Use `--help` for CLI overrides.

## Quality-control workflow

```bash
python scripts/qa_pdf.py output.pdf --render-dir ./qa-pages --contact-sheet ./qa-pages/sheet.jpg
```

- View cover, introduction, table-heavy pages, page breaks through long quotes, and last page at readable resolution.
- Verify headings are not orphaned, tables do not bleed beyond margins, code is not clipped, accents have good contrast, and no unexpected blank pages exist.
- Confirm bookmarks, clickable contents, page count, full text and source fidelity. Check important numeric claims and disclaimers against the supplied source.
- If any defect is found, change CSS or metadata, rebuild, re-render, and re-check. Do **not** fix by silently deleting content or shrinking everything indiscriminately.

## Multi-file collections

Render each source to its own PDF first. Then merge in a defined order:

```bash
python scripts/merge_pdfs.py --output complete_collection.pdf 01.pdf 02.pdf 03.pdf
python scripts/qa_pdf.py complete_collection.pdf --contact-sheet collection.jpg
```

Avoid inventing total page counts in the user-facing response; inspect the finished output first. If a large combined PDF fails to download, provide a separate ZIP containing it and the individual PDFs.

## Dependencies

Install from `requirements.txt` when the environment does not provide the packages. WeasyPrint may require platform rendering libraries (Cairo/Pango) on some machines. Prefer installed `Inter` fonts, but never bundle font files in the skill. If WeasyPrint cannot run, explain the missing dependency instead of claiming a PDF was produced.

## Bundled resources

- `assets/field_notes.css` — editable source of truth for layout and color tokens.
- `scripts/build_pdf.py` — Markdown + frontmatter renderer (PDF and standalone HTML).
- `scripts/qa_pdf.py` — structural checks and rendered page previews.
- `scripts/merge_pdfs.py` — merge PDFs, preserving and nesting bookmarks.
- `references/style-guide.md` — measured palette, typography, content components and guardrails.
- `examples/sample.md`, `sample.pdf`, `sample.html` — runnable sample with expected output.
