#!/usr/bin/env python3
"""End-to-end orchestration: detect → resolve log → resolve indexes → finalize.

Runs the full conflict-resolution pipeline:
  1. Detect which wiki/ files contain conflict markers.
  2. Resolve conflicts in wiki/log.md (chronological merge + dedupe).
  3. Resolve conflicts in all index files (dedupe by slug).
  4. Finalize: scan for residual markers, recount statistics, update wiki/index.md.

If a step finds nothing to do, it is skipped silently.

Usage:
  python .agents/skills/wiki-conflict-resolver/scripts/resolve_all.py
  python .agents/skills/wiki-conflict-resolver/scripts/resolve_all.py --dry-run
  python .agents/skills/wiki-conflict-resolver/scripts/resolve_all.py --skip-log
  python .agents/skills/wiki-conflict-resolver/scripts/resolve_all.py --skip-index
  python .agents/skills/wiki-conflict-resolver/scripts/resolve_all.py --skip-finalize
"""
import argparse
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))


def run_script(name, *args, dry_run=False):
    """Run a sibling script via subprocess; stream its output."""
    script = os.path.join(HERE, name)
    cmd = [sys.executable, script]
    if dry_run:
        cmd.append('--dry-run')
    cmd.extend(args)
    print(f"\n=== Running {name} ===")
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode


def detect_affected_files(root='wiki'):
    """Quick in-process scan for files with conflict markers."""
    affected = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules', 'site')]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, encoding='utf-8') as f:
                content = f.read()
            if '<<<<<<<' in content and '>>>>>>>' in content:
                affected.append(path)
    return affected


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--dry-run', action='store_true',
                   help='Pass --dry-run to each step (no files written)')
    p.add_argument('--skip-log', action='store_true', help='Skip log.md resolution')
    p.add_argument('--skip-index', action='store_true', help='Skip index resolution')
    p.add_argument('--skip-finalize', action='store_true', help='Skip finalization')
    args = p.parse_args()

    # Step 1: detect
    print("=== Step 1: Detect conflicts ===")
    affected = detect_affected_files()
    if not affected:
        print("No conflict markers found in wiki/. Nothing to do.")
        return
    print(f"Found conflicts in {len(affected)} file(s):")
    for path in affected:
        print(f"  {path}")

    # Step 2: resolve log
    if not args.skip_log:
        rc = run_script('resolve_log_conflict.py', dry_run=args.dry_run)
        if rc != 0:
            print(f"resolve_log_conflict.py exited with {rc}", file=sys.stderr)

    # Step 3: resolve indexes
    if not args.skip_index:
        rc = run_script('resolve_index_conflict.py', '--all', dry_run=args.dry_run)
        if rc != 0:
            print(f"resolve_index_conflict.py exited with {rc}", file=sys.stderr)

    # Step 4: finalize
    if not args.skip_finalize:
        rc = run_script('finalize.py', dry_run=args.dry_run)
        if rc != 0:
            print(f"finalize.py exited with {rc}", file=sys.stderr)

    print()
    print("=== Pipeline complete ===")
    if args.dry_run:
        print("(dry-run mode: no files were modified)")
    else:
        print("Next steps:")
        print("  git diff                   # review changes")
        print("  git add wiki/              # stage resolved files")
        print("  $env:GIT_EDITOR='true'; git rebase --continue")


if __name__ == '__main__':
    main()
