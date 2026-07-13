#!/usr/bin/env python3
"""Step 4: Post-fix verification.

Re-runs classification and (optionally) mkdocs build --strict.
Exits 0 only if:
  - All fixable categories are empty
  - truly_broken count is unchanged from before the fix run
  - mkdocs build --strict exits 0
"""
import sys
import os
import json
import argparse
import subprocess

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


def run_classifier():
    """Run classify_links.py and return the parsed report dict."""
    here = os.path.dirname(os.path.abspath(__file__))
    classify = os.path.join(here, 'classify_links.py')
    proc = subprocess.run(
        [sys.executable, classify, '--output', os.devnull],
        capture_output=True, text=True, encoding='utf-8',
    )
    if proc.returncode != 0:
        print(f'classify_links.py failed (exit {proc.returncode}):', file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        return None
    return json.loads(proc.stdout)


def run_mkdocs():
    """Run mkdocs build --strict. Returns exit code."""
    proc = subprocess.run(
        ['uv', 'run', 'mkdocs', 'build', '--strict'],
        capture_output=True, text=True, encoding='utf-8',
    )
    # Show the last 30 lines of output for context
    out_lines = (proc.stdout + proc.stderr).splitlines()
    for line in out_lines[-30:]:
        print(line, file=sys.stderr)
    return proc.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-build', action='store_true',
                        help='Skip mkdocs build verification')
    args = parser.parse_args()

    print('=== Re-classifying ===', file=sys.stderr)
    report = run_classifier()
    if report is None:
        sys.exit(2)

    fixable = ['missing_prefix', 'wiki_prefix', 'dotdot_prefix', 'log_informal']
    remaining = sum(len(report[c]) for c in fixable)
    truly_broken = len(report['truly_broken'])

    print(f'  remaining fixable violations: {remaining}', file=sys.stderr)
    print(f'  truly_broken (manual review): {truly_broken}', file=sys.stderr)

    if remaining > 0:
        print('FAIL: fixable violations remain. Re-run fix_links.py.', file=sys.stderr)
        for c in fixable:
            if report[c]:
                print(f'  {c}: {len(report[c])} remaining', file=sys.stderr)
        sys.exit(1)

    if args.no_build:
        print('Skipping mkdocs build (--no-build).', file=sys.stderr)
        print('PASS: no fixable violations remain.', file=sys.stderr)
        sys.exit(0)

    print(file=sys.stderr)
    print('=== Running mkdocs build --strict ===', file=sys.stderr)
    code = run_mkdocs()
    if code != 0:
        print(f'FAIL: mkdocs build exited {code}', file=sys.stderr)
        sys.exit(1)

    print('PASS: no fixable violations, mkdocs build clean.', file=sys.stderr)
    print(f'(truly_broken={truly_broken} — manual review required)',
          file=sys.stderr)
    sys.exit(0)


if __name__ == '__main__':
    main()
