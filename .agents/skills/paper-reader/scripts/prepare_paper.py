#!/usr/bin/env python3
"""Step 3a: Create paper directory, copy PDF from Zotero storage, verify header.

Handles non-ASCII filenames (umlauts, CJK) reliably via Python's shutil,
which bash `cp` mishandles on Windows.

Usage:
  uv run python .agents/skills/paper-reader/scripts/prepare_paper.py --slug author-year-title --pdf-key 5H7GWRF3
  uv run python .agents/skills/paper-reader/scripts/prepare_paper.py --slug ... --pdf-key ... --zotero-storage "D:\\Zotero\\storage"

Exit codes: 0 success, 1 no PDF found, 2 bad header, 3 copy error.
"""
import argparse, glob, os, shutil, sys

sys.stdout.reconfigure(encoding='utf-8')


def find_zotero_storage():
    """Try common Zotero storage locations."""
    home = os.environ.get('USERPROFILE', os.path.expanduser('~'))
    candidates = [
        os.path.join(home, 'Zotero', 'storage'),
        r'C:\Users\proud\Zotero\storage',
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return candidates[0]


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--slug', required=True, help='Paper slug (e.g. author-year-title)')
    p.add_argument('--pdf-key', required=True, help='Zotero PDF attachment key')
    p.add_argument('--zotero-storage', default=None,
                   help='Zotero storage dir (default: auto-detect)')
    args = p.parse_args()

    storage = args.zotero_storage or find_zotero_storage()
    src_dir = os.path.join(storage, args.pdf_key)

    # Find the PDF (glob handles non-ASCII filenames)
    pdfs = glob.glob(os.path.join(src_dir, '*.pdf'))
    if not pdfs:
        print(f"ERROR: No PDF found in {src_dir}", file=sys.stderr)
        sys.exit(1)

    src_pdf = pdfs[0]
    dest_dir = os.path.join('raw', 'papers', args.slug)
    dest_pdf = os.path.join(dest_dir, 'paper.pdf')

    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy2(src_pdf, dest_pdf)
    print(f"Copied: {src_pdf}")
    print(f"     -> {dest_pdf}")

    # Verify %PDF- header
    with open(dest_pdf, 'rb') as f:
        header = f.read(5)
    if header != b'%PDF-':
        print(f"ERROR: Bad PDF header: {header!r} (expected b'%PDF-')", file=sys.stderr)
        sys.exit(2)

    size_kb = os.path.getsize(dest_pdf) / 1024
    print(f"Verified: %PDF- header OK ({size_kb:.0f} KB)")
    print(f"\nNext: run an extraction script on slug '{args.slug}'")


if __name__ == '__main__':
    main()
