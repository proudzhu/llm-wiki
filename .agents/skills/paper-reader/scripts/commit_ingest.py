#!/usr/bin/env python3
"""Step 13: Stage ingest files and commit.

Stages the standard ingest file set plus any new/modified entity, concept,
and synthesis pages. Also auto-stages any other wiki/ modifications detected
via `git status` (e.g., concept pages edited to add bidirectional cross-
references per Step 8). Verifies no paper.pdf is accidentally staged.

Usage:
  uv run python .agents/skills/paper-reader/scripts/commit_ingest.py \
      --slug author-year-title \
      --message "ingest: Short Title (Author Year)" \
      --entities author1 author2 \
      --concepts concept1 concept2 \
      --synthesis synth1

Always files staged:
  raw/papers/{slug}/  wiki/sources/{slug}.md  wiki/index.md  wiki/log.md
  wiki/sources/index.md  wiki/entities/index.md  wiki/concepts/index.md
  wiki/synthesis/index.md

Auto-staged (detected via git status, not required in --entities/--concepts/
--synthesis):
  Any modified or untracked file under wiki/ (e.g., existing concept pages
  edited to add cross-references back to the new source). This prevents the
  recurring bug where Step 8 edits to existing concept pages are silently
  dropped from the commit because the operator forgot to list them.
"""
import argparse, os, subprocess, sys

# Force UTF-8 stdout/stderr so non-ASCII characters in paper titles, author
# names (e.g., "Østergaard"), and git output don't trip Windows cp1252 consoles.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass


def git(args, check=True):
    """Run a git command, return CompletedProcess. Forces UTF-8 I/O."""
    result = subprocess.run(
        ['git'] + args,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
    )
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
    p.add_argument('--strict', action='store_true',
                   help='Disable auto-staging of unlisted wiki/ modifications. '
                        'Use only when you intentionally want to leave edits '
                        'uncommitted (e.g., partial ingest for review).')
    args = p.parse_args()

    # Always-staged files. Note: wiki/synthesis/index.md may not exist on a
    # fresh repo; the filter below drops missing paths.
    files = [
        f'raw/papers/{args.slug}',
        f'wiki/sources/{args.slug}.md',
        'wiki/index.md',
        'wiki/log.md',
        'wiki/sources/index.md',
        'wiki/entities/index.md',
        'wiki/concepts/index.md',
        'wiki/synthesis/index.md',
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

    # Stage explicit list first
    git(['add'] + existing)

    # Auto-stage any other modified/untracked wiki/ files not in the explicit
    # list. This catches Step 8 edits to existing concept/entity pages that
    # the operator forgot to pass via --concepts/--entities. Without this, the
    # commit silently drops those edits and the working tree stays dirty.
    auto_staged = []
    if not args.strict:
        status = git(['status', '--porcelain']).stdout
        for line in status.splitlines():
            # Porcelain format: XY <path>  (X=index, Y=worktree)
            if len(line) < 4:
                continue
            xy, path = line[:2], line[3:]
            path = path.strip().strip('"')
            # Skip already-staged files (XY starts with a letter in index col)
            if xy[0] in ('A', 'M', 'R', 'C', 'D'):
                continue
            # Only auto-stage wiki/ modifications
            if not path.startswith('wiki/'):
                continue
            # Skip paper.pdf defensively (shouldn't be under wiki/ but be safe)
            if 'paper.pdf' in path:
                continue
            auto_staged.append(path)
        if auto_staged:
            git(['add'] + auto_staged)
            print(f"=== Auto-staged unlisted wiki/ modifications ===")
            for path in auto_staged:
                print(f"  {path}")
            print(f"(Auto-staged {len(auto_staged)} file(s) not in explicit "
                  f"--entities/--concepts/--synthesis list. Use --strict to "
                  f"disable this behavior.)\n")

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
        # Re-stage the explicit list + auto-staged files
        git(['add'] + existing + auto_staged)

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
        # Verify commit actually captured all expected files; warn if any are
        # still unstaged (can happen if a parallel-edit race dropped content).
        remaining = git(['status', '--short']).stdout.strip()
        if remaining:
            print("\nWARN: uncommitted changes remain after commit:",
                  file=sys.stderr)
            print(remaining, file=sys.stderr)
            print("Re-run with the affected files, or use `git add -p` to "
                  "inspect.", file=sys.stderr)
    else:
        print(f"\nCommit failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)


if __name__ == '__main__':
    main()
