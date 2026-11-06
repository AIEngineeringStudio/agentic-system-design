# Architect's Field Notes — Visual Design Specification

The visual system below was extracted from the five previously generated **Senior Solution Architect Behavioral Interview Study Guide** PDFs. This is a recreation of that style, not a pixel-perfect import of an unavailable original source stylesheet. It is designed to be robust and portable.

## Design principles

**Editorial, restrained, confident, print-first.** A dark statement cover contrasts with quiet, white content pages. Accent color distinguishes topics, not status or importance. Dense source material remains readable through hierarchy, whitespace and compact tables. Avoid shadows, photographs, gradients, decorative emoji, bright containers, and unsupported illustrations.

## Exact base colors

| Token | Hex | Application |
|---|---|---|
| `--navy` | `#112C3A` | Full-bleed front cover |
| `--header` | `#193A4B` | Table header backgrounds and dark code panels |
| `--heading` | `#17313E` | Headings and principal labels |
| `--ink` | `#273944` | Body text |
| `--muted` | `#75838D` | Small headers and running metadata |
| `--line` | `#D9E2E7` | Hairline separators |
| `--zebra` | `#F6F8F9` | Alternating table rows |
| White | `#FFFFFF` | Interior page background and table-head text |

### Matching original per-topic accent palette

| Original topic | Theme key | Accent | Pale highlight |
|---|---|---|---|
| Collaboration & Teamwork | `teal` | `#19BAA1` | `#EAF8F5` |
| Adaptability | `amber` | `#EEAA63` | `#FFF3E7` |
| Communication Skills | `lavender` | `#8399F2` | `#F0F2FF` |
| Time Management & Prioritization | `coral` | `#FA967C` | `#FFF1ED` |
| Problem Solving & Decision Making | `cyan` | `#64C8E6` | `#EAF8FC` |

For new guides, select a palette color purposefully. Reuse the five approved accents if matching existing documents is more important than differentiating every new document.

## Page geometry

- Paper: A4 portrait, **210 × 297 mm** (595.28 × 841.89 PDF points).
- Interior side margins: **19 mm**; usable width about **172 mm**.
- Interior top/bottom: **19 mm**, with small headers/footers in the page margin boxes.
- Cover: **full bleed** dark navy; cover text inset ~**26 mm** from the sides.
- Cover decorative rules: fine light strokes, two large, subtle circular outlines off-page.
- Page number: two digits, bottom right. Running header: small muted uppercase text aligned left and right.

## Typography

| Role | Face | Typical size | Notes |
|---|---|---:|---|
| Cover title | Inter Display ExtraBold / Bold | 42 pt | First line white, second in accent; negative tracking |
| Cover masthead | Inter ExtraBold | 9.5 pt | Widely tracked uppercase |
| Cover tagline | Inter Regular | 11.5–12 pt | Uppercase, understated light blue-grey |
| TOC title | Inter Display Bold | 21 pt | `Inside this guide` |
| Intro title | Inter Display Bold | 14 pt | Underlined with subtle hairline |
| Main chapter | Inter Display Bold | 17.2 pt | Separate accent `CHAPTER` overline |
| Subheading | Inter Display Bold | 11.6 pt | Tight, readable |
| Main body | Inter Regular | 9.4 pt | ~1.55 line-height |
| Tables | Inter Regular / Bold | 8 pt | Dark header, 2.2–2.4 mm padding |
| Running header/footer | Inter | 6.3–7 pt | Letterspaced uppercase |

Use an installed Inter family; use DejaVu Sans or a similar sans-serif fallback. Do **not** redistribute font binaries.

## Signature components

1. **Cover:** brand label top-left; `01 OF 05` type series label; short colored horizontal bar around 80 mm from top; large 1–2 line title starting around 97 mm; tagline around 174 mm; small descriptive subtitle; hairline above footer; number at bottom right.
2. **Preface:** accent uppercase `YOUR STUDY COMPANION`; concise source-derived introduction; callout for truthfulness/disclaimers; generated numbered TOC with horizontal rules. Prefer its own page.
3. **Chapters:** cyan/colored overline `CHAPTER` followed by clean deep-navy title. Subsequent sections flow across pages rather than forcing a break before every chapter.
4. **Callouts:** soft accent-tinted rectangle with 2.5-point vertical accent border at left, no shadow, compact insets.
5. **Tables:** #193A4B header with white text; even rows #F6F8F9; thin dividers; top-aligned cells. Repeat table headers across pages.
6. **Lists and worksheets:** compact bullets, generous enough row spacing, printed empty boxes for checklists, blank cells kept blank.
7. **Long quotations:** styled like callouts, allowed to flow if very long to avoid oversized blank pages.
8. **Code:** restrained navy background; monospaced text, wrapped to printable width.

## Source handling

- Keep all substantive text intact. Do not remove examples, tables, worksheets, or disclaimers to improve pagination.
- Replace a *source-generated* contents list with clickable PDF navigation. The old contents list is not substantive content.
- Keep the source order and heading names. Explicit metadata controls the cover title and number, not body assertions.
- Warn if an unusually wide table exceeds A4 width. Use 7.15 pt table font for 5+ columns only; otherwise preserve standard 8 pt.
- For content outside the study-guide format (e.g., legal documents, resumes, certificates), this editorial template may need a different structural layout. Do not force all content into this style without review.

## QA acceptance criteria

- Correct A4 size; readable full-bleed cover; page 2 navigation; consistent running headers/footers.
- No missing pages, blank pages caused by accidental forced breaks, cut-off cells, ugly orphaned titles, clipped code, or black glyph replacement.
- At least one successful visual render; inspect first, second, table-heavy, and final pages.
- In-document links and PDF bookmarks work; combined collections have clear top-level bookmarks.
- Verified count of pages and PDFs before sending download links.
