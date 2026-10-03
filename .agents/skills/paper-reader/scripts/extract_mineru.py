#!/usr/bin/env python3
"""Step 3c: Extract paper content from PDF via MinerU.

Workflow:
  1. Run `mineru-open-api extract -v` on the PDF, STREAMING output live.
     - The batch ID is captured from the first verbose poll URL.
     - A fatal `Error:` line kills the process immediately.
  2. A watchdog thread polls the documented batch-results API
     (https://mineru.net/api/v4/extract-results/batch/<id>, token read from
     ~/.mineru/config.yaml — never printed) every 10 s and aborts EARLY when:
       - the batch state is `failed` (server-side error, err_msg shown), or
       - the batch stays queued (`waiting-file`/`pending`/`waiting-extract`)
         longer than --pending-timeout (the server queue silently drops
         batches: observed stuck in `pending` forever on the Low 2004 PDF,
         costing a full 540 s blind wait), or
       - the overall --timeout deadline passes.
     If the token/config is unavailable the watchdog disables itself and the
     script degrades to the old behavior (CLI's own --timeout as backstop).
  3. Rename images/ subdirectory to figures/.
  4. Update image references in full-text.md (images/ -> figures/).
  5. Delete the PDF.

Usage:
  uv run python .agents/skills/paper-reader/scripts/extract_mineru.py --slug author-year-title
  uv run python .agents/skills/paper-reader/scripts/extract_mineru.py --slug ... --language ch --model pipeline --timeout 900
  uv run python .agents/skills/paper-reader/scripts/extract_mineru.py --slug ... --pending-timeout 0   # disable stuck-queue abort

MinerU language codes (NOT ISO 639 — MinerU's own convention):
    ch          Chinese (Simplified)  [default]
    ch_server   Chinese (server)
    ch_lite     Chinese (lite)
    en          English
    japan       Japanese
    korean      Korean
    chinese_cht Traditional Chinese
    latin       Latin-script languages
    arabic      Arabic
    east_slavic East Slavic
    cyrillic    Cyrillic
    devanagari  Devanagari
    ta, te, ka  Tamil / Telugu / Kannada

NOTE: `zh` is NOT a valid MinerU language code — use `ch` for Chinese.

Requires: mineru-open-api CLI (npm install -g mineru-open-api).
Verify token first: `mineru-open-api auth --show`
"""
import argparse, json, os, re, shutil, subprocess, sys, threading, time
import urllib.request

# Force UTF-8 stdout/stderr so non-ASCII characters in paper titles, figure
# names, and subprocess output don't trip Windows cp1252 consoles.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass

BATCH_API = 'https://mineru.net/api/v4/extract-results/batch/{}'
QUEUED_STATES = {'waiting-file', 'pending', 'waiting-extract'}
# Batch ID appears in the verbose poll URL (first GET after upload) and in
# the OSS upload path (api-upload/extract/<date>/<batch_id>/<file_id>.pdf).
BATCH_ID_RE = re.compile(r'extract-results/batch/([0-9a-fA-F-]{36})')
OSS_BATCH_RE = re.compile(r'api-upload/extract/\d{4}-\d{2}-\d{2}/([0-9a-fA-F-]{36})/')


def read_mineru_token():
    """Read the API token from ~/.mineru/config.yaml (never print it)."""
    path = os.path.join(os.path.expanduser('~'), '.mineru', 'config.yaml')
    try:
        with open(path, encoding='utf-8') as f:
            m = re.search(r'token:\s*(\S+)', f.read())
        return m.group(1) if m else None
    except OSError:
        return None


def query_batch_state(batch_id, token):
    """Return (state, err_msg) from the batch-results API, or (None, None)
    on any transient error (network blip, 5xx, bad JSON)."""
    req = urllib.request.Request(
        BATCH_API.format(batch_id),
        headers={'Authorization': f'Bearer {token}'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r)
        items = (data.get('data') or {}).get('extract_result') or []
        if not items:
            return None, None
        return items[0].get('state'), items[0].get('err_msg', '') or ''
    except Exception:
        return None, None


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--slug', required=True, help='Paper slug')
    p.add_argument('--language', default='en', help='Paper language (default: en). '
                    'Valid MinerU codes: ch, ch_server, ch_lite, en, japan, korean, '
                    'chinese_cht, latin, arabic, east_slavic, cyrillic, devanagari, '
                    'ta, te, ka. NOTE: "zh" is INVALID — use "ch" for Chinese.')
    p.add_argument('--model', default='vlm', choices=['vlm', 'pipeline'],
                   help='VLM layout analysis (vlm, default) or pipeline (zero-hallucination)')
    p.add_argument('--timeout', type=int, default=600,
                   help='Overall timeout in seconds (default 600)')
    p.add_argument('--pending-timeout', type=int, default=120,
                   help='Abort when the batch stays queued (pending/waiting-file) '
                        'longer than this many seconds — the server queue silently '
                        'drops batches. Default 120; 0 disables.')
    args = p.parse_args()

    # Validate language code against MinerU's accepted set (prevents the
    # [-10002] "field language is invalid" API error at runtime).
    # Reference: https://mineru.net/ & `mineru-open-api extract --help`
    VALID_LANGS = {
        'ch', 'ch_server', 'ch_lite', 'en', 'japan', 'korean', 'chinese_cht',
        'latin', 'arabic', 'east_slavic', 'cyrillic', 'devanagari',
        'ta', 'te', 'ka',
    }
    if args.language not in VALID_LANGS:
        print(f"ERROR: invalid --language {args.language!r}. "
              f"MinerU uses its own codes, not ISO 639. "
              f"Common gotcha: use 'ch' for Chinese, NOT 'zh'.\n"
              f"Valid codes: {sorted(VALID_LANGS)}", file=sys.stderr)
        sys.exit(2)

    paper_dir = os.path.join('raw', 'papers', args.slug)
    pdf_path = os.path.join(paper_dir, 'paper.pdf')
    md_path = os.path.join(paper_dir, 'full-text.md')
    images_dir = os.path.join(paper_dir, 'images')
    figures_dir = os.path.join(paper_dir, 'figures')

    if not os.path.exists(pdf_path):
        print(f"ERROR: {pdf_path} not found. Run prepare_paper.py first.",
              file=sys.stderr)
        sys.exit(1)

    # Step 1: Run MinerU extraction with live streaming output.
    cmd = [
        'mineru-open-api', 'extract', pdf_path,
        '-o', md_path,
        '--language', args.language,
        '--model', args.model,
        '--formula',
        '--table',
        '--timeout', str(args.timeout),
        '-v',  # verbose: exposes the batch ID and gives live progress lines
    ]
    print(f"Running: {' '.join(cmd)}")
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding='utf-8', errors='replace',
    )

    # Shared mutable state: [0]-style cells so the watchdog thread can see
    # updates without locks (CPython attribute writes are atomic enough here).
    batch_id = [None]
    abort_reason = [None]      # set by watchdog OR the reader on fatal errors
    stop = threading.Event()
    start_time = time.monotonic()

    def fail(msg):
        """Record the abort reason and kill the CLI process immediately."""
        if abort_reason[0] is None:
            abort_reason[0] = msg
        if proc.poll() is None:
            proc.kill()

    def watchdog():
        """Poll the batch-results API; abort early on failure or a stuck queue."""
        token = read_mineru_token()
        if not token:
            print('[watchdog] no token in ~/.mineru/config.yaml — disabled '
                  '(falling back to the CLI\'s own timeout)', flush=True)
            return
        last_state, last_report = None, 0.0
        last_progress = time.monotonic()
        while not stop.wait(10):
            bid = batch_id[0]
            if not bid:
                continue
            state, err_msg = query_batch_state(bid, token)
            elapsed = int(time.monotonic() - start_time)
            if state is None:
                continue  # transient poll error — the CLI's own poll governs
            if state != last_state:
                print(f'[watchdog] batch {bid[:8]}… state={state} ({elapsed}s)',
                      flush=True)
                last_state = state
                last_report = time.monotonic()
            if state == 'failed':
                fail(f"server-side extraction FAILED: {err_msg or 'no error message'}")
                return
            if state == 'done':
                # Batch finished — the CLI downloads on its next poll; nothing
                # left for the watchdog to guard.
                return
            if state in QUEUED_STATES:
                stuck = time.monotonic() - last_progress
                if time.monotonic() - last_report >= 30:
                    print(f'[watchdog] still queued ({state}) after {int(stuck)}s'
                          + (f', aborting at {args.pending_timeout}s' if args.pending_timeout
                             else ''), flush=True)
                    last_report = time.monotonic()
                if args.pending_timeout and stuck > args.pending_timeout:
                    fail(f"batch stuck in '{state}' for {int(stuck)}s — the server "
                         f"queue likely dropped it (this is a server-side condition; "
                         f"the batch will never complete)")
                    return
            else:
                # running / any active state counts as progress
                last_progress = time.monotonic()
            if time.monotonic() - start_time >= args.timeout:
                fail(f"overall timeout of {args.timeout}s reached "
                     f"(batch state: {state})")
                return

    t = threading.Thread(target=watchdog, daemon=True)
    t.start()

    # Stream the CLI output line by line: echo live, capture the batch ID,
    # and kill on the first fatal `Error:` line instead of waiting for the
    # process to wind down (or for the full --timeout on hangs).
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        if abort_reason[0]:
            break
        if line.startswith('Error:') or line.startswith('ERROR'):
            fail(f"mineru-open-api reported: {line.strip()}")
            break
        if not batch_id[0]:
            m = BATCH_ID_RE.search(line) or OSS_BATCH_RE.search(line)
            if m:
                batch_id[0] = m.group(1)
                print(f'[watchdog] tracking batch {batch_id[0]}', flush=True)

    stop.set()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()

    if abort_reason[0] is not None or proc.returncode != 0:
        print(f"\nMinerU extraction failed: {abort_reason[0] or f'exit code {proc.returncode}'}",
              file=sys.stderr)
        print("\nTroubleshooting:", file=sys.stderr)
        print("  - Verify token: mineru-open-api auth --show", file=sys.stderr)
        print("  - If 'parsing failed' or state=failed, check PDF validity "
              "(prepare_paper.py verifies header)", file=sys.stderr)
        print("  - If stuck in 'pending': the queue dropped the batch — re-running "
              "this script submits a FRESH batch and often succeeds", file=sys.stderr)
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
