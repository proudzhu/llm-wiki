#!/usr/bin/env python3
"""Step 3d: Fallback PDF extraction via pdftotext (when MinerU fails).

Produces plain text without images. Font mismatch warnings are normal.

Usage:
  python .agents/skills/paper-reader/scripts/extract_pdftotext.py --slug author-year-title

Requires: poppler-utils (pdftotext on PATH).
"""
import argparse, os, subprocess, sys

# Force UTF-8 stdout/stderr so non-ASCII characters in paper titles, figure
# names, and subprocess output don't trip Windows cp1252 consoles.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass


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

    print(f"Running: pdftotext -layout {pdf_path} {txt_path}")
    result = subprocess.run(
        ['pdftotext', '-layout', pdf_path, txt_path],
        capture_output=True, text=True,
        encoding='utf-8', errors='replace',
    )
    # pdftotext exits 0 even with warnings; check output file exists
    if not os.path.exists(txt_path) or os.path.getsize(txt_path) == 0:
        print(f"pdftotext failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    if result.stderr:
        print(f"(warnings are normal): {result.stderr.strip()[:200]}")

    size_kb = os.path.getsize(txt_path) / 1024
    print(f"Wrote: {txt_path} ({size_kb:.0f} KB)")

    # Delete the PDF
    os.remove(pdf_path)
    print(f"Deleted PDF: {pdf_path}")
    print("\nNote: pdftotext produces .txt without images.")


if __name__ == '__main__':
    main()
