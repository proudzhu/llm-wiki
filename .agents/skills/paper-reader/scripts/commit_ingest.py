#!/usr/bin/env python3
"""Step 13: Stage ingest files and commit.

Stages the standard ingest file set plus any new/modified entity, concept,
and synthesis pages. Verifies no paper.pdf is accidentally staged.

Usage:
  python .agents/skills/paper-reader/scripts/commit_ingest.py \
      --slug author-year-title \
      --message "ingest: Short Title (Author Year)" \
      --entities author1 author2 \
      --concepts concept1 concept2 \
      --synthesis synth1

Always files staged:
  raw/papers/{slug}/  wiki/sources/{slug}.md  wiki/index.md  wiki/log.md
  wiki/sources/index.md  wiki/entities/index.md  wiki/concepts/index.md
"""
import argparse, os, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')


def git(args, check=True):
    """Run a git command, return CompletedProcess."""
    result = subprocess.run(['git'] + args, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"git {' '.join(args)} failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--slug', required=True, help='Paper slug')
    p.add_argument('--message', required=True, help='Commit message')
    p.add_argument('--entities', nargs='*', default=[], help='Entity slugs (no .md)')
    p.add_argument('--concepts', nargs='*', default=[], help='Concept slugs (no .md)')
    p.add_argument('--synthesis', nargs='*', default=[], help='Synthesis slugs (no .md)')
    p.add_argument('--no-verify', action='store_true',
                   help='Bypass pre-commit hooks (use if hook has env issues)')
    args = p.parse_args()

    # Build the file list
    files = [
        f'raw/papers/{args.slug}',
        f'wiki/sources/{args.slug}.md',
        'wiki/index.md',
        'wiki/log.md',
        'wiki/sources/index.md',
        'wiki/entities/index.md',
        'wiki/concepts/index.md',
    ]
    for slug in args.entities:
        files.append(f'wiki/entities/{slug}.md')
    for slug in args.concepts:
        files.append(f'wiki/concepts/{slug}.md')
    for slug in args.synthesis:
        files.append(f'wiki/synthesis/{slug}.md')

    # Filter to existing files (avoid git errors on optional indexes)
    existing = [f for f in files if os.path.exists(f)]
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        print(f"WARN: skipping non-existent files: {missing}", file=sys.stderr)

    # Stage
    git(['add'] + existing)

    # Verify no paper.pdf is staged
    status = git(['status', '--short'])
    staged_pdfs = [
        line for line in status.stdout.splitlines()
        if 'paper.pdf' in line
    ]
    if staged_pdfs:
        print(f"ERROR: paper.pdf is staged! Removing...", file=sys.stderr)
        for line in staged_pdfs:
            # Extract the path from the status line
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                path = parts[1].strip().strip('"')
                git(['rm', '--cached', path])
                if os.path.exists(path):
                    os.remove(path)
        git(['add'] + existing)

    # Show staged status
    print("=== Staged files ===")
    staged = git(['status', '--short']).stdout
    print(staged if staged.strip() else '(nothing staged)')

    # Commit
    commit_cmd = ['commit']
    if args.no_verify:
        commit_cmd.append('--no-verify')
    commit_cmd += ['-m', args.message]
    result = git(commit_cmd, check=False)
    if result.returncode == 0:
        print(f"\nCommitted: {args.message}")
    else:
        print(f"\nCommit failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)


if __name__ == '__main__':
    main()
