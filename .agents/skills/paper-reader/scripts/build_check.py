#!/usr/bin/env python3
"""Step 12: Run MkDocs strict build to verify no warnings.

Tries `uv run mkdocs build --strict` first, falls back to `python -m mkdocs build --strict`.
A clean build exits 0 with 'INFO - Documentation built in N seconds'.

Usage:
  uv run python .agents/skills/paper-reader/scripts/build_check.py

Exit code 0 = clean build, non-zero = build failed or warnings found.
"""
import subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')


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
