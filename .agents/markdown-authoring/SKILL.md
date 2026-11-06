---
name: markdown-authoring
description: Write or revise repository Markdown documents with readable, uncluttered structure
  that converts cleanly to portrait A4 PDFs. Use when creating, editing, reorganizing, or formatting Markdown files.
---

# Readable Markdown Authoring

Use this skill when creating or revising Markdown in this repository. Aim for documents that are easy to scan on
screen, understand on first reading, and render cleanly on portrait A4 paper.

## Core style

Prefer clear headings followed by short paragraphs. For definitions, concepts, and reference material, use a
standalone **bold term or label with a colon**, followed by a blockquoted explanation. Put the colon inside the
bold text, leave a blank line before the blockquote, and leave a blank line between entries:

```markdown
**Unclear facts or high uncertainty:**

> Time-box discovery and return with evidence before making a commitment.
```

For explanations spanning multiple paragraphs, prefix every quoted line with `>` and separate paragraphs with
a line containing only `>`. These blocks are a presentation convention, not necessarily external quotations;
preserve attribution for actual quotations. Keep ordinary narrative prose as paragraphs without forced labels.

When discussing literal wording, commands, or short snippets inside a sentence, wrap the exact text in inline code
so it is visually distinct from the explanation. Keep the surrounding prose unformatted; use quotation marks for
actual quotations when appropriate.

For example: In Markdown, `We will use the platform interface` states a decision but not its rationale.

Use tables only when a small, genuinely two-dimensional comparison is easier to understand in rows and columns.
Do not create wide tables, tables with long prose in cells, or tables used only to align text. Convert those into
headed subsections or bold labels followed by blockquoted explanations. Avoid tables of contents or indexes formatted as
Markdown tables.

Keep lists intentional and short. Do not put every sentence or concept in a bullet. Use a numbered list only when
order matters, such as steps, procedures, or exercises. Use a brief unordered list only for a small set of parallel
items that would be less readable as prose. For explanations, glossaries, comparisons, and interview language,
prefer standalone bold labels followed by blockquoted explanations over repeated bullets or nested lists.

For Q&A, examples, and comparisons, use distinct blocks with standalone labels, such as **Question:**, **Answer:**,
**Example:**, **Tradeoff:**, **Weak answer:**, and **Clearer answer:**, each followed by its blockquoted body.
Keep each block focused; use a heading when the topic changes rather than adding another layer of list indentation.

## Print-friendly structure

Use one document title followed by a logical heading hierarchy. Do not skip heading levels for visual effect. Keep
headings concise and descriptive, and avoid leaving a heading stranded from its opening paragraph.
Likewise, keep a standalone bold label with the beginning of its blockquote in print, while allowing long
blockquotes to span pages.

Write for the page width: keep paragraphs focused, avoid long unbroken lines, and use ordinary Markdown wrapping.
Keep code fences, indentation, and diagram spacing intact. If a diagram needs fixed-width alignment, preserve it as a
code block and identify it as a non-wrapping diagram when preparing the PDF representation.

Use emphasis sparingly and consistently. Bold should identify a term, label, or key point; it should not turn whole
paragraphs into visual noise. Use links with meaningful labels and keep source notes close to the claims they support.

## Editing existing documents

Preserve the author's meaning, technical accuracy, examples, references, numbering, and source-verification labels.
When improving layout, change presentation rather than silently removing or summarizing content. Do not modify
generated PDFs or archived sources unless asked.

Before finishing, scan the document for wide tables, dense or nested lists, inconsistent heading levels, and
paragraphs that are difficult to read at A4 width. Replace presentation-only tables or excessive bullets with
standalone bold labels followed by blockquoted explanations where that improves comprehension.

For PDF conversion, also follow [the pdf-skill](...) and the shared
[`pdf-skill/README.md`](...). This skill controls source Markdown readability; 
the PDF skill controls rendering and final-output validation.
