#!/usr/bin/env python3
"""Step 3b: Extract paper content from arXiv HTML via Defuddle.

Workflow:
  1. Verify arXiv HTML version exists (200 status).
  2. Run `defuddle parse` to produce markdown.
  3. Download figures referenced in the markdown to figures/.
  4. Replace remote image links with local embed wikilinks.
  5. Delete the PDF if it exists (extraction source is HTML).

Usage:
  python .agents/skills/paper-reader/scripts/extract_arxiv_html.py --arxiv-id 2607.01834 --slug author-year-title

Requires: defuddle CLI (npm install -g defuddle).
Falls back to MinerU if arXiv HTML is unavailable (404) — exit code 2.
Auto-creates raw/papers/{slug}/ if missing, so arXiv-only papers can skip
prepare_paper.py entirely.
"""
import argparse, os, re, shutil, subprocess, sys, urllib.request

# Force UTF-8 stdout/stderr so non-ASCII characters in paper titles, figure
# names, and subprocess output don't trip Windows cp1252 consoles.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass


def check_arxiv_html(arxiv_id):
    """Return True if arXiv HTML version exists."""
    url = f"https://arxiv.org/html/{arxiv_id}"
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status == 200
    except Exception:
        return False


def check_defuddle():
    """Return True if defuddle CLI is on PATH."""
    try:
        subprocess.run(
            ['defuddle', '--version'],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
        )
        return True
    except FileNotFoundError:
        return False


def run_defuddle(url, out_path):
    """Run defuddle parse to extract markdown."""
    print(f"Running defuddle on {url} ...")
    result = subprocess.run(
        ['defuddle', 'parse', url, '--md', '-o', out_path],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
    )
    if result.returncode != 0:
        print(f"defuddle failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"Wrote: {out_path}")


def download_figures(md_path, arxiv_id, figures_dir):
    """Download remote images referenced in markdown to figures/."""
    os.makedirs(figures_dir, exist_ok=True)
    with open(md_path, encoding='utf-8') as f:
        content = f.read()

    # Match markdown image links: ![alt](url) and bare URLs to arxiv html images
    img_pattern = re.compile(r'!\[([^\]]*)\]\((https?://[^)]+)\)')
    downloaded = {}

    for m in img_pattern.finditer(content):
        alt, url = m.group(1), m.group(2)
        if 'arxiv.org' not in url and not url.startswith('/'):
            # Only handle arxiv-hosted images; skip others
            if not url.startswith('/'):
                continue
            url = f"https://arxiv.org{url}"

        # Derive a local filename
        ext = os.path.splitext(url)[1] or '.png'
        idx = len(downloaded) + 1
        local_name = f"fig{idx}{ext}"
        local_path = os.path.join(figures_dir, local_name)

        try:
            urllib.request.urlretrieve(url, local_path)
            downloaded[url] = local_name
            print(f"  Downloaded: {url} -> figures/{local_name}")
        except Exception as e:
            print(f"  WARN: Could not download {url}: {e}", file=sys.stderr)

    return downloaded


def replace_image_links(md_path, downloaded, slug):
    """Replace remote image URLs with local embed wikilinks."""
    with open(md_path, encoding='utf-8') as f:
        content = f.read()

    for url, local_name in downloaded.items():
        # Replace ![alt](url) with ![[raw/papers/{slug}/figures/{name}|alt]]
        escaped = re.escape(url)
        content = re.sub(
            rf'!\[([^\]]*)\]\({escaped}\)',
            lambda m, ln=local_name: f'![[raw/papers/{slug}/figures/{ln}|{m.group(1)}]]',
            content,
        )

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--arxiv-id', required=True, help='arXiv ID (e.g. 2607.01834)')
    p.add_argument('--slug', required=True, help='Paper slug')
    args = p.parse_args()

    paper_dir = os.path.join('raw', 'papers', args.slug)
    md_path = os.path.join(paper_dir, 'full-text.md')
    figures_dir = os.path.join(paper_dir, 'figures')
    pdf_path = os.path.join(paper_dir, 'paper.pdf')

    if not os.path.isdir(paper_dir):
        print(f"ERROR: {paper_dir} does not exist. Run prepare_paper.py first.",
              file=sys.stderr)
        sys.exit(1)

    # Step 1: Verify arXiv HTML exists
    print(f"Checking arXiv HTML for {args.arxiv_id} ...")
    if not check_arxiv_html(args.arxiv_id):
        print(f"arXiv HTML not available for {args.arxiv_id} (404).")
        print("FALLBACK: Use extract_mineru.py instead.")
        sys.exit(2)

    # Step 2: Extract markdown with Defuddle
    url = f"https://arxiv.org/html/{args.arxiv_id}"
    run_defuddle(url, md_path)

    # Step 3: Download figures
    print("\nDownloading figures ...")
    downloaded = download_figures(md_path, args.arxiv_id, figures_dir)

    # Step 4: Replace remote links with local embed wikilinks
    if downloaded:
        replace_image_links(md_path, downloaded, args.slug)
        print(f"Replaced {len(downloaded)} image link(s) with local embed wikilinks.")

    # Step 5: Delete the PDF
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print(f"\nDeleted PDF: {pdf_path}")

    print(f"\nDone. Extracted text: {md_path}")
    print(f"Figures: {len(downloaded)} in {figures_dir}")


if __name__ == '__main__':
    main()
