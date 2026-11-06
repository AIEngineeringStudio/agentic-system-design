#!/usr/bin/env python3
"""Build a matching Architect's Field Notes PDF from Markdown.

Generates a standalone HTML and paginated A4 PDF. No bundled font files.
Requires: markdown-it-py, PyYAML, WeasyPrint.
"""
from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import re
import sys
import unicodedata

import yaml
from markdown_it import MarkdownIt
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
CSS_FILE = ROOT / "assets" / "field_notes.css"
THEMES = {
    "teal": ("#19baa1", "#eaf8f5"),
    "amber": ("#eeaa63", "#fff3e7"),
    "lavender": ("#8399f2", "#f0f2ff"),
    "coral": ("#fa967c", "#fff1ed"),
    "cyan": ("#64c8e6", "#eaf8fc"),
}


def split_metadata(raw: str):
    if not raw.startswith("---\n"):
        return {}, raw
    mark = re.search(r"\n---\s*\n", raw[4:])
    if not mark:
        return {}, raw
    end = 4 + mark.end()
    obj = yaml.safe_load(raw[4:4 + mark.start()]) or {}
    if not isinstance(obj, dict):
        raise ValueError("YAML frontmatter must be a mapping.")
    return obj, raw[end:]


def plain(text: str):
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return re.sub(r"[*_`~]", "", text).strip()


def slugify(text: str):
    t = unicodedata.normalize("NFKD", plain(text)).encode("ascii", "ignore").decode("ascii").lower()
    t = re.sub(r"[^a-z0-9\s-]", "", t)
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", t)).strip("-") or "section"


def cover_lines(title: str):
    """Balanced lines with preference for & without introducing new words."""
    if " & " in title:
        a, b = title.split(" & ", 1)
        return [a, "& " + b]
    if len(title) <= 19:
        return [title]
    pieces = title.split()
    if len(pieces) < 2:
        return [title]
    midpoint = len(title) / 2
    choices = [(abs(len(" ".join(pieces[:i])) - midpoint), i) for i in range(1, len(pieces))]
    idx = min(choices)[1]
    return [" ".join(pieces[:idx]), " ".join(pieces[idx:])]


def split_source(src: str):
    """Strip the source's duplicate contents list and isolate introduction."""
    lines = src.splitlines(keepends=True)
    cleaned = []
    in_old_toc = False
    for line in lines:
        if re.match(r"^#{1,3}\s+(?:Table of contents|Contents|Navigation)\s*$", line, re.I):
            in_old_toc = True
            continue
        if in_old_toc:
            if re.match(r"^#{1,2}\s+", line) and not re.match(r"^#{1,3}\s+(?:Table of contents|Contents|Navigation)\s*$", line, re.I):
                in_old_toc = False
            else:
                continue
        cleaned.append(line)
    src = "".join(cleaned)
    # Main chapters are numbered H2s where available, else every H2.
    markers = list(re.finditer(r"^##\s+\d+[.\s]\s*.+$", src, flags=re.M))
    if not markers:
        markers = list(re.finditer(r"^##\s+.+$", src, flags=re.M))
    if not markers:
        raise ValueError("At least one Markdown '##' chapter heading is required.")
    preface, content = src[:markers[0].start()], src[markers[0].start():]
    headings = [m.group(0)[3:].strip() for m in re.finditer(r"^##\s+.+$", content, flags=re.M)]
    return preface, content, headings


def render_md(src: str, used: dict[str, int]):
    md = MarkdownIt("commonmark", {"html": True, "typographer": True}).enable(["table", "strikethrough"])
    tokens = md.parse(src)
    for i, token in enumerate(tokens):
        if token.type == "heading_open" and i + 1 < len(tokens):
            heading = tokens[i+1].content
            base = slugify(heading)
            used[base] = used.get(base, 0) + 1
            slug = base if used[base] == 1 else f"{base}-{used[base]}"
            token.attrSet("id", slug)
    html = md.renderer.render(tokens, md.options, {})
    # Print-friendly checkbox treatment (no browser form controls).
    def checkbox(m):
        checked = m.group(1).lower() == "x"
        return '<li class="task-list-item"><span class="task-box' + (' checked' if checked else '') + '"></span>'
    html = re.sub(r"<li>\s*\[([ xX])\]\s*", checkbox, html)
    # Fit 5+ column tables to A4 with smaller text.
    html = re.sub(r"<table>(.*?)</table>", lambda m: '<table class="wide">' + m.group(1) + '</table>' if m.group(1).count("<th>") >= 5 else m.group(0), html, flags=re.S)
    return html


def css_string(value):
    return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ') + '"'


def build(input_file: Path, output_file: Path, html_file: Path | None, args):
    meta, src = split_metadata(input_file.read_text(encoding="utf-8-sig"))
    title_match = re.search(r"^#\s+(.+)$", src, flags=re.M)
    title = args.title or meta.get("title") or (plain(title_match.group(1)) if title_match else input_file.stem.replace("_", " "))
    if title_match:
        src = src[:title_match.start()] + src[title_match.end():]
    preface, body, headings = split_source(src)
    theme = args.theme or meta.get("theme") or "cyan"
    if theme not in THEMES:
        raise ValueError(f"Unknown theme {theme!r}. Choose {', '.join(THEMES)}")
    accent, accent_soft = THEMES[theme]
    accent = args.accent or meta.get("accent") or accent
    accent_soft = meta.get("accent_soft") or accent_soft
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", accent) or not re.fullmatch(r"#[0-9a-fA-F]{6}", accent_soft):
        raise ValueError("Accent and accent_soft must be #RRGGBB colors.")
    used = {}
    preface_html = render_md(preface, used)
    content_html = render_md(body, used)
    # Slugs were added to headings in first chapter onward; compute with same repeat logic.
    # Lookup from source headings rather than from untrusted hardcoded anchors.
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content_html, "html.parser")
    toc = [(h.get_text(" ", strip=True), h.get("id", "")) for h in soup.find_all("h2")]
    cover_text = args.cover_lines or meta.get("cover_lines") or cover_lines(title)
    if isinstance(cover_text, str):
        cover_text = [part.strip() for part in cover_text.split("|") if part.strip()]
    if not cover_text or len(cover_text) > 2:
        raise ValueError("cover_lines must have 1 or 2 lines.")
    brand = args.brand or meta.get("brand") or "THE ARCHITECT'S FIELD NOTES"
    series = args.series or meta.get("series") or "BEHAVIORAL INTERVIEW STUDY GUIDE"
    number = str(args.number or meta.get("number") or "01").zfill(2)
    total = str(args.total or meta.get("total") or "01").zfill(2)
    tagline = args.tagline or meta.get("tagline") or "THINK CLEARLY. DECIDE WITH EVIDENCE. DELIVER WITH CONFIDENCE."
    note = meta.get("cover_note") or "A practical guide to evidence-based answers, senior-level judgment, and focused rehearsal."
    audience = meta.get("audience") or "SENIOR / PRINCIPAL SOLUTION ARCHITECT INTERVIEWS"
    footer_right = meta.get("footer_right") or title.upper()
    footer_left = meta.get("footer_left") or "SENIOR / PRINCIPAL SOLUTION ARCHITECT"
    intro_label = meta.get("intro_label") or "YOUR STUDY COMPANION"
    preface_html = re.sub(r"^\s*<hr\s*/?>\s*", "", preface_html)
    preface_html = re.sub(r"\s*<hr\s*/?>\s*$", "", preface_html)
    toc_items = "\n".join(f'<li><span class="toc-num">{i:02d}</span><a href="#{escape(anchor, quote=True)}">{escape(label)}</a></li>' for i, (label, anchor) in enumerate(toc, 1))
    cover_markup = f"<div class='cover-title{' long' if max(map(len,cover_text))>24 else ''}'>{escape(cover_text[0])}{('<span class=second>'+escape(cover_text[1])+'</span>') if len(cover_text)>1 else ''}</div>"
    css = CSS_FILE.read_text(encoding="utf-8")
    css = css.replace("--accent: #64c8e6;", f"--accent: {accent};").replace("--accent-soft: #eaf8fc;", f"--accent-soft: {accent_soft};")
    css += f"\n@page {{ @top-right {{ content: {css_string(footer_right)}; }} @bottom-left {{ content: {css_string(footer_left)}; }} }}\n"
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>{escape(title)} | Field Notes</title><style>{css}</style></head><body>
<section class="cover">
<div class="cover-brand">{escape(brand)}</div>
<div class="cover-series">{escape(series)} &nbsp;/&nbsp; {number} OF {total}</div>
<div class="cover-accent-bar"></div>{cover_markup}
<div class="cover-sub">{escape(tagline)}<div class="cover-note">{escape(note)}</div></div>
<div class="cover-rule"></div><div class="cover-bottom">PREPARED FOR {escape(audience)}<br>READ &nbsp; · &nbsp; REFLECT &nbsp; · &nbsp; PRACTICE</div>
<div class="cover-number">{escape(number)}</div></section>
<section class="preface"><div class="preface-label">{escape(intro_label)}</div>
{preface_html}<nav class="toc"><div class="toc-overline">NAVIGATION</div>
<h2>Inside this guide</h2><ol>{toc_items}</ol></nav></section>
<main class="content">{content_html}</main></body></html>"""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    if html_file:
        html_file.parent.mkdir(parents=True, exist_ok=True)
        html_file.write_text(doc, encoding="utf-8")
    HTML(string=doc, base_url=str(input_file.parent.resolve())).write_pdf(str(output_file))
    print(f"Created {output_file} ({len(toc)} chapters; {theme} theme)")
    if html_file:
        print(f"Standalone HTML: {html_file}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("input", type=Path, help="Markdown source file (supports optional YAML frontmatter)")
    p.add_argument("--output", "-o", required=True, type=Path, help="PDF file")
    p.add_argument("--html", type=Path, help="Optional standalone HTML copy")
    p.add_argument("--theme", choices=THEMES.keys(), help="Topic accent color")
    p.add_argument("--accent", help="Override theme accent, e.g. #64c8e6")
    p.add_argument("--title", help="Override cover title")
    p.add_argument("--cover-lines", help="Explicit line break: 'Line one|Line two'")
    p.add_argument("--number", help="Guide number, e.g. 06")
    p.add_argument("--total", help="Collection total, e.g. 06")
    p.add_argument("--tagline", help="Short cover strapline")
    p.add_argument("--brand", help="Series masthead text")
    p.add_argument("--series", help="Series description")
    args = p.parse_args()
    try:
        build(args.input, args.output, args.html, args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
