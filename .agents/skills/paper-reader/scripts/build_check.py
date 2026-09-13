#!/usr/bin/env python3
"""Step 12: Run MkDocs strict build to verify no warnings.

Tries `uv run mkdocs build --strict` first, falls back to `python -m mkdocs
build --strict`. A clean build exits 0 with 'Documentation built in N
seconds'.

IMPORTANT: do NOT add --quiet. mkdocs's --quiet sets the log level to ERROR,
which filters WARNING records before strict-mode's warning counter sees
them — the build then exits 0 despite strict violations. Observed in the
Ke 2021 ingest: 12 broken log-link warnings were invisible under --quiet
(build_check.py reported "BUILD OK") and caught only by the commit-time
build. INFO-level nav lines in the output are normal and harmless.

On success, writes a freshness marker file `.tmp_build_ok` (gitignored via
the `.tmp_*` pattern). commit_ingest.py reads this marker: if the build
passed recently AND no build-input file has been modified since, it commits
with --no-verify to skip the pre-commit hook's duplicate ~60 s build.

Usage:
  uv run python .agents/skills/paper-reader/scripts/build_check.py

Exit code 0 = clean build, non-zero = build failed or warnings found.
"""
import os
import subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

BUILD_OK_MARKER = '.tmp_build_ok'


def write_build_ok_marker():
    """Record that a strict build just passed (mtime = build time)."""
    try:
        with open(BUILD_OK_MARKER, 'w', encoding='utf-8') as f:
            f.write('mkdocs build --strict passed\n')
    except OSError as e:
        # Marker is an optimization, never a hard failure
        print(f"WARN: could not write {BUILD_OK_MARKER}: {e}", file=sys.stderr)


def main():
    cmds = [
        ['uv', 'run', 'mkdocs', 'build', '--strict'],
        ['python', '-m', 'mkdocs', 'build', '--strict'],
    ]
    last_err = None
    for cmd in cmds:
        try:
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=False)
            if result.returncode == 0:
                print("\nBUILD OK: mkdocs build --strict passed (exit 0)")
                write_build_ok_marker()
                return 0
            print(f"\nBUILD FAILED: exit code {result.returncode}", file=sys.stderr)
            return result.returncode
        except FileNotFoundError:
            last_err = cmd[0]
            continue

    print(f"ERROR: Neither 'uv' nor 'python -m mkdocs' is available "
          f"(last tried: {last_err})", file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
