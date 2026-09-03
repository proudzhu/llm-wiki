#!/usr/bin/env python3
"""Step 11: Append a formatted entry to wiki/log.md.

The log is append-only with newest entries at the end. Each entry starts
with a `---` separator, then a `## [YYYY-MM-DD] {op} | {title}` heading,
followed by the body content.

Usage:
  # From a file:
  uv run python .agents/skills/paper-reader/scripts/append_log.py \
      --op ingest --title "Paper Title (Author Year)" --file entry.md

  # From stdin:
  echo "body content" | uv run python .agents/skills/paper-reader/scripts/append_log.py \
      --op ingest --title "..." --stdin

  # From a string:
  uv run python .agents/skills/paper-reader/scripts/append_log.py \
      --op query --title "Question topic" --body "One-line answer..."

Operations: ingest, query, lint, merge.
"""
import argparse, datetime, re, sys

sys.stdout.reconfigure(encoding='utf-8')

LOG_PATH = 'wiki/log.md'
VALID_OPS = ('ingest', 'query', 'lint', 'merge')

# Markdown links whose targets cannot resolve from wiki/log.md: `../`
# escapes the docs root, `wiki/` doubles it. Both abort `mkdocs build
# --strict` at commit time (pitfalls.md #40 — the Ke 2021 ingest appended
# 12 such links and the commit-time build failed).
BAD_LINK_RE = re.compile(r'\]\(\s*(?:\.\./|wiki/)')


def validate_body(body):
    """Reject markdown links that break `mkdocs build --strict` from log.md."""
    m = BAD_LINK_RE.search(body)
    if m:
        print("ERROR: log entry body contains a non-resolving markdown link:\n"
              f"  ...{body[max(0, m.start() - 30):m.start() + 40]}...\n"
              "Links like [Text](../sources/foo.md) or [Text](wiki/sources/foo.md) "
              "do not resolve from wiki/log.md and abort `mkdocs build --strict`.\n"
              "Fix: use vault-absolute wikilinks [[sources/foo|Text]] or "
              "backticked plain paths `wiki/sources/foo.md` instead.",
              file=sys.stderr)
        sys.exit(2)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--op', required=True, choices=VALID_OPS, help='Operation type')
    p.add_argument('--title', required=True, help='Entry title (after |)')
    p.add_argument('--file', help='Read body content from this file')
    p.add_argument('--stdin', action='store_true', help='Read body from stdin')
    p.add_argument('--body', help='Body content as a string')
    args = p.parse_args()

    # Gather body content
    if args.file:
        with open(args.file, encoding='utf-8') as f:
            body = f.read().strip()
    elif args.stdin:
        body = sys.stdin.read().strip()
    elif args.body is not None:
        body = args.body.strip()
    else:
        body = ''

    validate_body(body)

    today = datetime.date.today().isoformat()
    entry = f"\n---\n\n## [{today}] {args.op} | {args.title}\n\n"
    if body:
        entry += f"{body}\n"

    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(entry)

    print(f"Appended log entry: [{today}] {args.op} | {args.title}")
    print(f"Log file: {LOG_PATH}")


if __name__ == '__main__':
    main()
