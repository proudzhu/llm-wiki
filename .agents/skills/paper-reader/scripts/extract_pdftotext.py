#!/usr/bin/env python3
"""Step 3d: Fallback PDF extraction (when MinerU fails).

Uses pdftotext (poppler) if on PATH; otherwise falls back to pypdf, which
produces comparable plain text without any system dependency. Produces
plain text without images and deletes the PDF afterward (the same
invariant as every other extraction script).

Usage:
  uv run python .agents/skills/paper-reader/scripts/extract_pdftotext.py --slug author-year-title

Requires: poppler-utils (pdftotext on PATH) OR pypdf (in project deps).
"""
import argparse, os, shutil, subprocess, sys

# Force UTF-8 stdout/stderr so non-ASCII characters in paper titles, figure
# names, and subprocess output don't trip Windows cp1252 consoles.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass


def extract_with_pdftotext(pdf_path, txt_path):
    """Return (ok, warning_text) using the poppler pdftotext binary."""
    result = subprocess.run(
        ['pdftotext', '-layout', pdf_path, txt_path],
        capture_output=True, text=True,
        encoding='utf-8', errors='replace',
    )
    if not os.path.exists(txt_path) or os.path.getsize(txt_path) == 0:
        return False, result.stderr
    return True, result.stderr


def extract_with_pypdf(pdf_path, txt_path):
    """Return (ok, warning_text) using the pypdf library."""
    try:
        from pypdf import PdfReader
    except ImportError:
        return False, "pypdf not installed (run: uv add pypdf)"
    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ''
        pages.append(text)
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(pages))
    return os.path.getsize(txt_path) > 0, None


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--slug', required=True, help='Paper slug')
    args = p.parse_args()

    paper_dir = os.path.join('raw', 'papers', args.slug)
    pdf_path = os.path.join(paper_dir, 'paper.pdf')
    txt_path = os.path.join(paper_dir, 'full-text.txt')

    if not os.path.exists(pdf_path):
        print(f"ERROR: {pdf_path} not found. Run prepare_paper.py first.",
              file=sys.stderr)
        sys.exit(1)

    if shutil.which('pdftotext'):
        print(f"Running: pdftotext -layout {pdf_path} {txt_path}")
        ok, warning = extract_with_pdftotext(pdf_path, txt_path)
        engine = 'pdftotext'
        if not ok:
            print(f"pdftotext failed:\n{warning}", file=sys.stderr)
            print("Falling back to pypdf...", file=sys.stderr)
            ok, warning = extract_with_pypdf(pdf_path, txt_path)
            engine = 'pypdf'
    else:
        print("pdftotext (poppler) not on PATH — using pypdf fallback")
        ok, warning = extract_with_pypdf(pdf_path, txt_path)
        engine = 'pypdf'

    if not ok:
        print(f"ERROR: extraction failed ({engine}):\n{warning}", file=sys.stderr)
        sys.exit(1)

    if engine == 'pdftotext' and warning:
        print(f"(warnings are normal): {warning.strip()[:200]}")

    size_kb = os.path.getsize(txt_path) / 1024
    print(f"Wrote: {txt_path} ({size_kb:.0f} KB, engine: {engine})")

    # Delete the PDF
    os.remove(pdf_path)
    print(f"Deleted PDF: {pdf_path}")
    print("\nNote: plain-text extraction produces .txt without images.")


if __name__ == '__main__':
    main()
