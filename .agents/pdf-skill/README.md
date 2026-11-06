# Architect's Field Notes PDF Skill

Reusable agent skill for producing PDFs that match the look and structure of the five Senior Solution Architect interview study guides.

**Contents:** Agent `SKILL.md`, exact color/typography specification, editable print CSS, pdf-skill script, structural QA script, multi-PDF merger, and a working sample (Markdown + HTML + PDF).

## Quick start

From the skill directory:

```bash
python -m pip install -r requirements.txt
python scripts/build_pdf.py examples/sample.md --output example-output.pdf --html example-output.html
python scripts/qa_pdf.py example-output.pdf --render-dir qa --contact-sheet qa/sheet.jpg
```

If required system libraries are missing for WeasyPrint, consult its official installation documentation for your OS. An installed **Inter** font family produces the closest match; fallback sans-serif fonts work but may change page breaks. Font files are not included.

## Use with an agent

Provide the **entire folder** to an agent environment that supports local skills and instruct it to follow `SKILL.md` for PDF creation. Skill installation directories vary by agent product and workspace; follow that environment's current instructions. The package is not automatically installed just because it was downloaded.

## Source format

The input is UTF-8 Markdown containing at least one `##` heading, optionally with YAML frontmatter. See `examples/sample.md` for complete metadata and examples of tables, code, quotation callouts, worksheets, and checkboxes. The tool preserves original text and replaces an old `## Contents` list with generated navigation.

## Palette

| Theme | Accent |
|---|---|
| teal | `#19BAA1` |
| amber | `#EEAA63` |
| lavender | `#8399F2` |
| coral | `#FA967C` |
| cyan | `#64C8E6` |

All styles share the same dark navy (`#112C3A`) front cover and white body pages. For editable, self-contained, print-friendly HTML output, pass `--html`.

## License and content

This package contains no font binaries. Sample content is original demonstration text. Do not assume the sample metrics, situations, or business claims are statements of fact.
