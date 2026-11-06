#!/usr/bin/env python3
"""Merge PDFs in given order, adding top-level section bookmarks."""
from pathlib import Path
import argparse
import fitz


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", "-o", type=Path, required=True)
    p.add_argument("pdfs", type=Path, nargs="+", help="PDFs to combine in order")
    a=p.parse_args()
    dst=fitz.open()
    bookmarks=[]
    deferred_links=[]
    for path in a.pdfs:
        src=fitz.open(path)
        start=len(dst)+1
        title=(src.metadata.get("title") or path.stem.replace("_"," ")).replace(" | Field Notes", "").strip()
        bookmarks.append([1,title,start])
        for level,label,page in src.get_toc():
            if page >= 1:
                bookmarks.append([level+1,label,start+page-1])
        # PyMuPDF insert_pdf does not preserve WeasyPrint named-destination
        # links reliably. Re-create those links as ordinary in-document links.
        for page_index, source_page in enumerate(src):
            seen=set()
            for link in source_page.get_links():
                signature=(link.get('kind'), tuple(round(v, 2) for v in link['from']), link.get('page'), link.get('uri'))
                if signature in seen: continue
                seen.add(signature)
                kind=link.get('kind')
                if kind in (fitz.LINK_GOTO, fitz.LINK_NAMED) and link.get('page', -1) >= 0:
                    deferred_links.append((start - 1 + page_index, {
                        'kind':fitz.LINK_GOTO, 'from':link['from'],
                        'page':start - 1 + link['page'],
                        'to':(fitz.Point(link.get('to', fitz.Point(0,0)).x, src[link['page']].rect.height - link.get('to', fitz.Point(0,0)).y)
                              if kind == fitz.LINK_NAMED else link.get('to', fitz.Point(0,0)))
                    }))
                elif kind == fitz.LINK_URI and link.get('uri'):
                    deferred_links.append((start - 1 + page_index, {
                        'kind':fitz.LINK_URI, 'from':link['from'], 'uri':link['uri']
                    }))
        dst.insert_pdf(src, links=False)
        src.close()
    for index, link in deferred_links:
        dst[index].insert_link(link)
    dst.set_toc(bookmarks)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    dst.save(a.output, garbage=4, deflate=True)
    print(f"Created {a.output} ({len(dst)} pages; {len(a.pdfs)} source PDFs)")

if __name__=="__main__":
    main()
