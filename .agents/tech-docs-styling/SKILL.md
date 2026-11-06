---
name: technical-docs-styling
description: Structure and style technical documentation and learning guides for clarity, scannability, accessibility,
  and low-clutter reading. Use when creating or reorganizing technical guides, tutorials, reference docs, or
  engineering explanations in Markdown.
---

# Technical Documentation and Learning-Guide Styling

Use this skill to make technical Markdown easier to navigate, understand, and remember without diluting technical detail. Some readers find dense prose hard to absorb; offer multiple ways into the same ideas by combining concise explanations with purposeful visual structure. Design for the reader's task first, then use a small, consistent set of formatting patterns to make the structure visible.

For general Markdown conventions and print-friendly source formatting, follow [Readable Markdown Authoring](...). For PDF requests, also follow [Markdown to PDF](...) and the shared PDF theme. This skill adds technical-content and learning-design guidance; it does not define a separate visual theme.

## Start with the reader's task

Identify who the reader is, what they need to do or understand, and what they already know. Choose the document shape to fit that task: a procedure for completing a task, a reference for looking up facts, a tutorial for learning by doing, or a design explanation for understanding decisions.

State the purpose and boundaries early. Put prerequisites, assumptions, environment or version requirements, and important limitations near the beginning, where readers need them. Keep essential information in the main flow; use links for optional depth, not to hide required steps or caveats.

For a learning guide, connect the learning outcome to the content and practice. A useful progression is:

1. State the outcome and prerequisites.
2. Establish the basic mental model and define essential terms.
3. Introduce one new idea at a time, showing how it builds on what came before.
4. Demonstrate the idea with a worked example and explain why it works.
5. Add complexity gradually, then give the reader a practice task.
6. Provide an answer, explanation, or way to check the result.

Make prerequisites between concepts visible. Do not rely on an unexplained term or advanced idea before it has been introduced; when a necessary prerequisite is missing, briefly teach it or link to a clear prerequisite section. Use transitions to explain how each new concept extends, contrasts with, or depends on earlier material. Revisit the core model as details are added so readers can keep the whole idea in view.

Adapt this sequence to the topic rather than forcing every guide into a template. Make the relationship between exercises and answers easy to follow, and do not reveal a solution before the reader has a clear opportunity to try.

## Support visual understanding and recall

Do not make long prose the only way to understand a complex idea. When it improves comprehension, pair the explanation with a useful visual: a flow diagram for sequence, a component diagram for relationships, a timeline for change, or a small comparison for meaningful contrasts. Introduce the visual with the question it answers, then explain its key takeaway in nearby text. Visuals should clarify the same accurate content, not replace necessary assumptions, caveats, or detail.

Chunk information into a small number of meaningful sections. Use descriptive headings, short paragraphs, and consistent visual patterns so readers can see where they are and how ideas connect. For complex processes, present stages in order; for systems, distinguish components and show labeled relationships; for abstract concepts, anchor the explanation with a concrete example or analogy and state where the analogy stops being accurate. Prefer a simple overview before detailed diagrams or exceptions, then add complexity in stages while connecting each stage to the overview.

Help readers actively recall and connect ideas. End a substantial section with a brief recap, a small set of retrieval questions, or a prompt to sketch or explain the concept from memory. Put answers or explanations after a clear pause or in a separate, easy-to-find section. Use summaries to reinforce the main model, not to repeat every detail.

Whenever content uses a label to identify the kind of information that follows, make the label bold wherever it appears: in regular paragraphs, lists, recap sheets, or blockquotes. Keep the label visually distinct from its explanation; do not bold the whole sentence or reminder. For example:

```markdown
**Example:**

> A labeled explanation can use a blockquote without moving its label inside the quote.

> **Concurrency:**
> Visibility is not atomicity; bound queues and dependencies.
```

Use this consistently for cues such as **Plain English:**, **Say it professionally:**, **Example:**, **Follow-up:**, and **Hash collections:**. Do not add a label where ordinary prose is clearer; reserve this pattern for content that benefits from a quick visual cue.

Keep visual emphasis disciplined. Use whitespace, alignment, and a consistent set of labels before adding color or decoration. Avoid turning every paragraph into a box, using several competing highlight styles, or adding diagrams that merely restate nearby text. Convey meaning with labels and structure as well as color, and provide text descriptions for important visuals so the content remains accessible and useful in plain-text and print formats.

## Build a clear visual hierarchy

Use one descriptive title and a logical heading hierarchy. Headings should summarize the section's content or task, not serve as decoration. Do not skip levels, use headings only to make text larger, or create a new heading for every short paragraph.

Lead with the most useful information. Keep paragraphs focused on one idea, explain unfamiliar terms before relying on them, and expand acronyms at first use unless the audience is certain to know them. Use transitions to show cause, sequence, and tradeoffs instead of making readers infer how sections connect.

Keep the page calm and predictable:

- Use whitespace to separate ideas and meaningful sections.
- Use bold for labels or a key term, not whole paragraphs; use italics sparingly.
- Avoid decorative separators, repeated callout boxes, emoji labels, and competing accent styles.
- Keep lists short and parallel. Number only steps or items with meaningful order; avoid deeply nested lists.
- Avoid repeating a heading's wording in the first sentence beneath it.

Choose one presentation pattern for one content role and use it consistently. For labeled definitions, examples, Q&A, and tradeoffs, follow the standalone bold-label pattern in the general authoring skill rather than inventing a new box or table for each kind.

## Keep page layouts readable

When print is in scope, design for the usable area inside the page margins, not the paper's full dimensions. Check the narrower content area when both A4 and Letter are required. Keep body text and code comfortably readable; do not reduce type size just to force content onto a page. Use manageable line lengths and avoid layout choices that depend on screen-only horizontal scrolling.

Prevent awkward page breaks. Keep headings with the opening text that follows, and keep standalone labels with the start of their explanations. Avoid splitting short procedures, worked examples, or tightly related content where a break would make them hard to follow. Long code, tables, and explanations may span pages when that is clearer than shrinking or keeping a large block together.

For code, preserve exact commands and indentation. Long lines may wrap in the rendered document, but copied commands must remain unambiguous. For fixed-width diagrams, preserve alignment and check the rendered size; use a textual explanation or alternative when necessary. Use images with adequate resolution for their printed size, meaningful alternative text, and captions or nearby descriptions when their content needs explanation.

Do not communicate meaning through color alone. Use labels, symbols, or patterns as well, and check important distinctions in grayscale when printing may be monochrome. Keep headers, footers, and page numbers visually subordinate to the content.

## Verify the exported document

When a PDF is requested, follow the repository's [pdf-skill workflow](...), which defines the shared theme and required validation. Check the actual rendered PDF rather than assuming the Markdown source or a screen preview guarantees print quality. If both A4 and Letter are required, render and validate each page size; passing at one size does not establish that the other fits.

Check that internal links, contents/index page references, page numbers, footnotes, exercise-to-answer references, and other navigation still point to the right destinations after pagination. Review code, diagrams, tables, images, and page breaks at final print size. Do not claim a format is verified if the corresponding render or check was not performed.

## Present technical material accurately

Keep commands, configuration, identifiers, paths, and code exact. Use inline code for short literal values and fenced code blocks for multi-line examples; label fences with the language when known. Introduce code with its purpose and relevant assumptions, and explain non-obvious or consequential lines nearby.

Make examples usable and honest. Show required setup, representative input, expected output, and likely failure conditions when they matter. Distinguish illustrative pseudocode from runnable code. Do not remove error handling, security constraints, version context, or edge cases merely to make an example look shorter.

Use diagrams when they communicate relationships or flow more clearly than prose. Give each diagram a brief explanation, keep labels readable, and provide a textual description of its key relationships or sequence. Preserve meaning over visual alignment; mark fixed-width text diagrams as non-wrapping when preparing a PDF.

Use a table only when readers benefit from comparing a few genuinely parallel properties. Prefer a small number of short columns; avoid wide tables, long prose in cells, and tables used only to align content. Wide tables often become cramped or get clipped on portrait A4 and Letter pages, and can be awkward to read on phones. For detailed tradeoffs, definitions, or prose-heavy comparisons, use labeled subsections or focused paragraphs instead. Do not use tables to lay out page content.

If a wide comparison is essential, first see whether it can be split into smaller, logically grouped comparisons without losing context. If not, choose and document a deliberate output treatment, such as a landscape page, and verify that it remains readable in the actual output. Do not solve width problems by shrinking text to illegibility or relying on horizontal scrolling that will not exist in print.

Place warnings and important constraints next to the step or decision they affect. State the consequence and the action the reader should take; do not rely on color, an icon, or an admonition syntax that may not render in the target Markdown viewer.

## Make navigation and accessibility reliable

Use descriptive link text that makes sense out of context. Link to stable, specific destinations and keep references close to the claims they support. Identify whether a claim is measured, sourced, assumed, or hypothetical when that distinction matters.

Use semantic Markdown in reading order. Give links and images meaningful text alternatives; do not use color, position, or visual styling as the only way to convey meaning. Keep heading text unique enough to navigate, and make link purpose clear without requiring surrounding sentences.

Avoid unexplained abbreviations, long unbroken lines, and dense blocks that are difficult to scan. Check that code and tables remain readable on narrow screens and at print width. When printability is required for both A4 and Letter, check the narrower effective content area after margins rather than assuming one page size will fit the other. If a diagram or comparison cannot fit, revise its structure or provide a useful text alternative rather than shrinking it until illegible.

## Edit and review existing guides

Preserve technical meaning, working examples, references, numbering, and verification labels. Improve presentation without silently deleting, summarizing, or changing claims. Follow the repository's existing conventions and do not introduce a new theme or component system for an individual document.

Before finishing, read the document once as its intended audience and check:

- Can the reader tell what the document is for, who it serves, and what to do next?
- Does the order move from context to explanation or action, then to practice or verification where appropriate?
- Are headings, paragraphs, lists, examples, callouts, tables, and diagrams consistent and easy to scan?
- Are commands and code accurate, contextualized, and distinguishable from prose?
- Are assumptions, risks, source context, and limitations visible where they matter?
- Can a reader navigate and understand the content without relying on color or layout alone?
- Does the source remain readable on screen and compatible with the repository's print workflow?
- If printing is in scope, are tables, code, and diagrams legible on the requested page size(s), including both A4 and Letter when both are required?
- If a PDF is in scope, have both required page sizes been rendered and checked, including pagination, image quality, grayscale meaning, and navigation targets?
