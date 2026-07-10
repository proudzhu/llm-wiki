#!/usr/bin/env python3
"""Step 3c: Extract paper content from PDF via MinerU.

Workflow:
  1. Run `mineru-open-api extract` on the PDF.
  2. Rename images/ subdirectory to figures/.
  3. Update image references in full-text.md (images/ -> figures/).
  4. Delete the PDF.

Usage:
  python .agents/skills/paper-reader/scripts/extract_mineru.py --slug author-year-title
  python .agents/skills/paper-reader/scripts/extract_mineru.py --slug ... --language zh --model pipeline --timeout 900

Requires: mineru-open-api CLI (npm install -g mineru-open-api).
Verify token first: `mineru-open-api auth --show`
"""
import argparse, os, shutil, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--slug', required=True, help='Paper slug')
    p.add_argument('--language', default='en', help='Paper language (default: en)')
    p.add_argument('--model', default='vlm', choices=['vlm', 'pipeline'],
                   help='VLM layout analysis (vlm, default) or pipeline (zero-hallucination)')
    p.add_argument('--timeout', type=int, default=600, help='Timeout in seconds (default 600)')
    args = p.parse_args()

    paper_dir = os.path.join('raw', 'papers', args.slug)
    pdf_path = os.path.join(paper_dir, 'paper.pdf')
    md_path = os.path.join(paper_dir, 'full-text.md')
    images_dir = os.path.join(paper_dir, 'images')
    figures_dir = os.path.join(paper_dir, 'figures')

    if not os.path.exists(pdf_path):
        print(f"ERROR: {pdf_path} not found. Run prepare_paper.py first.",
              file=sys.stderr)
        sys.exit(1)

    # Step 1: Run MinerU extraction
    cmd = [
        'mineru-open-api', 'extract', pdf_path,
        '-o', md_path,
        '--language', args.language,
        '--model', args.model,
        '--formula',
        '--table',
        '--timeout', str(args.timeout),
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"MinerU extraction failed:\n{result.stderr}", file=sys.stderr)
        print("\nTroubleshooting:", file=sys.stderr)
        print("  - Verify token: mineru-open-api auth --show", file=sys.stderr)
        print("  - If 'parsing failed', check PDF validity (prepare_paper.py verifies header)",
              file=sys.stderr)
        print("  - Fall back: extract_pdftotext.py", file=sys.stderr)
        sys.exit(1)

    print(f"Wrote: {md_path}")

    # Step 2: Rename images/ to figures/
    if os.path.isdir(images_dir):
        if os.path.isdir(figures_dir):
            # Merge if figures/ already exists
            for f in os.listdir(images_dir):
                shutil.move(os.path.join(images_dir, f), figures_dir)
            os.rmdir(images_dir)
        else:
            shutil.move(images_dir, figures_dir)
        print(f"Renamed: images/ -> figures/")

        # Step 3: Update references in full-text.md
        if os.path.exists(md_path):
            with open(md_path, encoding='utf-8') as f:
                content = f.read()
            content = content.replace('images/', 'figures/')
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Updated image references: images/ -> figures/")

    # Step 4: Delete the PDF
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print(f"Deleted PDF: {pdf_path}")

    # Verify extraction quality hint
    if os.path.exists(md_path):
        with open(md_path, encoding='utf-8') as f:
            lines = f.readlines()
        print(f"\nExtraction complete: {len(lines)} lines in {md_path}")
        print("Verify quality by reading first 200 + last 100 lines.")


if __name__ == '__main__':
    main()
