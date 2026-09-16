#!/usr/bin/env python3
"""Step 3b: Extract paper content from arXiv HTML via Defuddle.

Workflow:
  1. Verify arXiv HTML version exists (200 status) — no filesystem side
     effects, so a 404 leaves nothing behind.
  2. Create raw/papers/{slug}/ if missing (arXiv-only papers can skip
     prepare_paper.py entirely).
  3. Run `defuddle parse` to produce markdown.
  4. Download figures referenced in the markdown to figures/.
  5. Replace remote image links with local embed wikilinks.
  6. Delete the PDF if it exists (extraction source is HTML).

Usage:
  uv run python .agents/skills/paper-reader/scripts/extract_arxiv_html.py --arxiv-id 2607.01834 --slug author-year-title

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


def resolve_defuddle():
    """Resolve the defuddle executable path.

    On Windows, npm-installed CLIs ship as `.cmd` shims. `subprocess.run` with
    a list argument calls `CreateProcess` directly, which does NOT consult
    `PATHEXT`, so `['defuddle', ...]` raises `FileNotFoundError` even when
    `defuddle.cmd` is on PATH. `shutil.which` does consult `PATHEXT`, so we
    use it to resolve the full executable path before invoking subprocess.
    Returns the path string, or None if not found.
    """
    return shutil.which('defuddle')


def check_arxiv_html(arxiv_id):
    """Return the first arXiv HTML URL that exists, or None.

    Tries the unversioned URL first (canonical), then versioned URLs
    (v1, v2, v3) — older papers sometimes only serve the versioned HTML
    page (Luo 2022 ingest: /html/2209.15174 returned 406 while
    /html/2209.15174v1 returned 200).

    A browser User-Agent is mandatory: arXiv's CDN rejects urllib's
    default UA with HTTP 406 even for URLs that exist — the same behavior
    documented at _fetch_via_curl for figure downloads (Kim 2021 ingest).
    Without it, BOTH probe URLs 406 and the script wrongly reports the
    paper as having no HTML, falling back to MinerU unnecessarily.
    """
    candidates = [f"https://arxiv.org/html/{arxiv_id}"]
    candidates += [f"https://arxiv.org/html/{arxiv_id}v{i}" for i in (1, 2, 3)]
    last_err = None
    for url in candidates:
        try:
            req = urllib.request.Request(url, method='HEAD',
                                         headers=HTML_PROBE_HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    return url
        except Exception as e:
            last_err = e
            continue
    if last_err is not None:
        print(f"  WARN: last probe error: {last_err}", file=sys.stderr)
    return None


def check_defuddle():
    """Return True if defuddle CLI is on PATH."""
    exe = resolve_defuddle()
    if exe is None:
        return False
    try:
        subprocess.run(
            [exe, '--version'],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
        )
        return True
    except FileNotFoundError:
        return False


def run_defuddle(url, out_path):
    """Run defuddle parse to extract markdown."""
    exe = resolve_defuddle()
    if exe is None:
        print("defuddle CLI not found on PATH. Install with: npm install -g defuddle",
              file=sys.stderr)
        sys.exit(1)
    print(f"Running defuddle on {url} ...")
    result = subprocess.run(
        [exe, 'parse', url, '--md', '-o', out_path],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
    )
    if result.returncode != 0:
        print(f"defuddle failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"Wrote: {out_path}")


# Matches markdown image links: ![alt](url), including defuddle's
# '[[Uncaptioned image]]' nested-bracket alt form for images without alt
# text in the source HTML (a plain [^\]]* alt group silently skips those).
IMG_PATTERN = re.compile(r'!\[(?:\[[^\]]*\]|[^\]]*)\]\((https?://[^)]+)\)')

# Headers for probing /html/ pages. Browser UA is required — arXiv's CDN
# 406-rejects urllib's default UA (see check_arxiv_html docstring). A
# text/html Accept is used rather than BROWSER_HEADERS' image Accept.
HTML_PROBE_HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 '
                   'Safari/537.36'),
    'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
}

BROWSER_HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 '
                   'Safari/537.36'),
    'Accept': 'image/avif,image/webp,image/png,image/*,*/*;q=0.8',
}


def _looks_like_image(data):
    """True if the body plausibly is an image.

    Some CDN blocks return an HTML challenge page with HTTP 200; reject
    bodies that are too small or start with HTML markup.
    """
    if len(data) < 64:
        return False
    head = data[:512].lstrip().lower()
    return not (head.startswith(b'<!doctype') or head.startswith(b'<html')
                or head.startswith(b'<head'))


def _fetch_via_curl(url, timeout=60):
    """Fetch url bytes via curl and return them; raise on any failure.

    curl's TLS fingerprint differs from Python-urllib's, which matters:
    arXiv's CDN intermittently rejects urllib with HTTP 406 even when the
    same URL succeeds via curl in the same minute (observed in the Kim
    2021 ingest: 2 of 3 figures downloaded, the 3rd 406'd; retries with
    browser headers still 406'd, curl succeeded).
    """
    exe = shutil.which('curl')
    if exe is None:
        raise RuntimeError('curl not found on PATH')
    marker = b'\n__CURL_STATUS__'
    result = subprocess.run(
        [exe, '-sS', '-L', '--max-time', str(timeout),
         '-w', marker.decode() + '%{http_code}', url],
        capture_output=True,
    )
    out = result.stdout
    if marker not in out:
        err = result.stderr.decode('utf-8', 'replace').strip()
        raise RuntimeError(f'curl failed: {err or "no output"}')
    body, _, status = out.rpartition(marker)
    code = status.decode('ascii', 'replace').strip()
    if not code.startswith('2'):
        raise RuntimeError(f'HTTP {code}')
    return body


def fetch_image_bytes(url, referer):
    """Download an image robustly against arXiv CDN 406 challenges.

    Strategy: urllib with browser headers first (fast path, no external
    dependency), then a curl fallback (different TLS fingerprint). Raises
    RuntimeError describing both attempts on total failure.
    """
    headers = dict(BROWSER_HEADERS)
    if referer:
        headers['Referer'] = referer
    last_err = None
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        if _looks_like_image(data):
            return data
        last_err = f'non-image body ({len(data)} bytes, likely CDN block page)'
    except Exception as e:
        last_err = str(e)
    try:
        return _fetch_via_curl(url)
    except Exception as e:
        raise RuntimeError(f'urllib: {last_err}; curl fallback: {e}')


def download_figures(md_path, arxiv_id, figures_dir):
    """Download remote images referenced in markdown to figures/."""
    os.makedirs(figures_dir, exist_ok=True)
    with open(md_path, encoding='utf-8') as f:
        content = f.read()

    downloaded = {}
    referer = f"https://arxiv.org/html/{arxiv_id}"

    for m in IMG_PATTERN.finditer(content):
        url = m.group(1)
        if 'arxiv.org' not in url:
            if not url.startswith('/'):
                # Only handle arxiv-hosted images; skip others
                continue
            url = f"https://arxiv.org{url}"

        if url in downloaded:
            # The same URL may be referenced several times (e.g. once as
            # '![alt](url)' and once as defuddle's '[[Uncaptioned image]]'
            # form); download it once and reuse the local name.
            continue

        # Derive a local filename
        ext = os.path.splitext(url)[1] or '.png'
        idx = len(downloaded) + 1
        local_name = f"fig{idx}{ext}"
        local_path = os.path.join(figures_dir, local_name)

        try:
            data = fetch_image_bytes(url, referer)
            with open(local_path, 'wb') as f:
                f.write(data)
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
        # Alt group tolerates defuddle's '![[Uncaptioned image]](url)'
        # nested-bracket form. Both alternatives are bounded (they cannot
        # cross a ']'), so the match cannot span from one image into a
        # later one and swallow the text between them.
        escaped = re.escape(url)
        pattern = rf'!\[(\[[^\]]*\]|[^\]]*)\]\({escaped}\)'

        def _repl(m, ln=local_name):
            alt = m.group(1).strip()
            # Brackets/pipes in an alias would break the embed wikilink
            # (pipe-escaping in the build chain), so drop such aliases.
            if not alt or '[' in alt or ']' in alt or '|' in alt:
                return f'![[raw/papers/{slug}/figures/{ln}]]'
            return f'![[raw/papers/{slug}/figures/{ln}|{alt}]]'

        content = re.sub(pattern, _repl, content)

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

    # Step 1: Verify arXiv HTML exists (before any filesystem side effects,
    # so a 404 does not leave behind an empty raw/papers/{slug}/ directory)
    print(f"Checking arXiv HTML for {args.arxiv_id} ...")
    html_url = check_arxiv_html(args.arxiv_id)
    if html_url is None:
        print(f"arXiv HTML not available for {args.arxiv_id} "
              f"(all probe URLs failed; see WARN above for the last error).")
        print("FALLBACK: Use extract_mineru.py instead.")
        sys.exit(2)

    # Step 2: Create the paper directory if missing (arXiv-only papers can
    # skip prepare_paper.py entirely)
    os.makedirs(paper_dir, exist_ok=True)

    # Step 3: Extract markdown with Defuddle
    run_defuddle(html_url, md_path)

    # Step 4: Download figures
    print("\nDownloading figures ...")
    downloaded = download_figures(md_path, args.arxiv_id, figures_dir)

    # Step 5: Replace remote links with local embed wikilinks
    if downloaded:
        replace_image_links(md_path, downloaded, args.slug)
        print(f"Replaced {len(downloaded)} image link(s) with local embed wikilinks.")

    # Step 6: Delete the PDF
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print(f"\nDeleted PDF: {pdf_path}")

    print(f"\nDone. Extracted text: {md_path}")
    print(f"Figures: {len(downloaded)} in {figures_dir}")


if __name__ == '__main__':
    main()
