#!/usr/bin/env python3
"""Step 12 one-call verification: wikilinks + backlinks + mkdocs --strict.

Runs the three Step 12 checks sequentially and reports a single consolidated
result — one blocking invocation instead of three separate calls. Fail-fast:
if an early check fails, later checks are skipped (fix broken links before
paying for a 60-110 s build).

Usage:
  uv run python .agents/skills/paper-reader/scripts/verify_all.py --slug SLUG

Exit 0 = all three checks passed; 1 = first failure (printed).
"""
import argparse
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPTS = os.path.dirname(os.path.abspath(__file__))


def run_step(name, args):
    print(f"\n=== {name} ===", flush=True)
    r = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS, args[0])] + args[1:],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=1200,
    )
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    if out:
        print(out)
    if err:
        # INFO banner noise from mkdocs/Material goes to stderr; keep it but
        # don't let it imply failure on its own.
        print(err)
    return r.returncode


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slug", required=True, help="Source page slug (no .md)")
    args = p.parse_args()

    checks = [
        ("Step 12a: verify_wikilinks", ["verify_wikilinks.py", "--slug", args.slug]),
        ("Step 12b: check_backlinks", ["check_backlinks.py", "--slug", args.slug]),
        ("Step 12c: mkdocs build --strict", ["build_check.py"]),
    ]

    for name, argv in checks:
        try:
            rc = run_step(name, argv)
        except subprocess.TimeoutExpired:
            print(f"\nFAILED: {name} timed out", file=sys.stderr)
            sys.exit(1)
        if rc != 0:
            print(f"\nFAILED at {name} (exit {rc}) — fix and re-run; "
                  f"later checks were skipped.", file=sys.stderr)
            sys.exit(1)

    print("\nALL CHECKS PASSED: wikilinks + backlinks + mkdocs --strict.")


if __name__ == "__main__":
    main()
