#!/usr/bin/env python3
"""Basic structural PDF QA and optional multi-page contact sheet.

This detects gross defects, but a person/agent must still inspect rendered pages.
Requires PyMuPDF; Pillow for --contact-sheet.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import fitz


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--contact-sheet", type=Path, help="Create JPEG contact sheet of all pages")
    ap.add_argument("--render-dir", type=Path, help="Save first, second, middle and last pages as PNG")
    args = ap.parse_args()
    errors = []
    warnings = []
    if not args.pdf.is_file():
        raise SystemExit(f"PDF not found: {args.pdf}")
    doc = fitz.open(args.pdf)
    if doc.needs_pass:
        errors.append("Document is password-protected")
    if not len(doc):
        errors.append("Document has no pages")
    if len(doc) > 0:
        pages = len(doc)
        page_box = doc[0].rect
        if abs(page_box.width - 595.28) > 3 or abs(page_box.height - 841.89) > 3:
            warnings.append("Page size differs from A4")
        if len(doc.get_toc()) == 0:
            warnings.append("No outline/bookmark entries found")
        if not any(any(link.get('uri') or link.get('page', -1) >= 0 or link.get('nameddest') for link in page.get_links()) for page in doc):
            warnings.append("No clickable links found")
        for n, page in enumerate(doc, 1):
            text = page.get_text().strip()
            if len(text) < (130 if n == 1 else 60):
                warnings.append(f"Page {n} contains little text ({len(text)} characters)")
            rect = page.rect
            for b in page.get_text('blocks'):
                if not isinstance(b[4], str):
                    continue
                box = fitz.Rect(b[:4])
                if box.x0 < -2 or box.y0 < -2 or box.x1 > rect.width+2 or box.y1 > rect.height+2:
                    errors.append(f"Text block outside page bounds on page {n}: {box}")
        if args.render_dir:
            args.render_dir.mkdir(parents=True, exist_ok=True)
            sampled = sorted({0, 1, pages // 2, pages - 1} & set(range(pages)))
            for idx in sampled:
                dst = args.render_dir / f"page-{idx+1:02d}.png"
                doc[idx].get_pixmap(matrix=fitz.Matrix(1.6,1.6), alpha=False).save(dst)
            print(f"Wrote {len(sampled)} page previews to {args.render_dir}")
        if args.contact_sheet:
            from PIL import Image, ImageDraw
            import io
            thumbs = []
            for idx, page in enumerate(doc):
                pix = page.get_pixmap(matrix=fitz.Matrix(.42, .42), alpha=False)
                im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
                thumbs.append(im)
            cols = 4
            gap = 13
            w = max(im.width for im in thumbs)
            h = max(im.height for im in thumbs)
            rows = (len(thumbs)+cols-1)//cols
            sheet = Image.new('RGB',(cols*w+(cols+1)*gap, rows*h+(rows+1)*gap),(235,238,240))
            for i,im in enumerate(thumbs):
                x = gap+(i%cols)*(w+gap); y=gap+(i//cols)*(h+gap)
                sheet.paste(im,(x,y))
            args.contact_sheet.parent.mkdir(parents=True, exist_ok=True)
            sheet.save(args.contact_sheet,quality=85)
            print(f"Wrote {args.contact_sheet}")
    print(f"PDF: {args.pdf}\nPages: {len(doc)}\nBookmarks: {len(doc.get_toc()) if len(doc) else 0}\nStatus: {'FAIL' if errors else 'PASS'}")
    for msg in warnings: print(f"WARNING: {msg}")
    for msg in errors: print(f"ERROR: {msg}")
    if warnings: print("Review images manually; automated checks cannot detect every clipping or overflow issue.")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
