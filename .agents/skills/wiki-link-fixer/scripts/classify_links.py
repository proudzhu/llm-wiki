#!/usr/bin/env python3
"""Step 1: Scan wiki/ and classify all wikilink convention violations.

Outputs a JSON report (stdout) and a human-readable summary (stderr).
Does NOT modify any files.

Categories:
  - missing_prefix: [[beamforming]] -> [[concepts/beamforming]]
  - wiki_prefix:    [[wiki/concepts/foo]] -> [[concepts/foo]]
  - dotdot_prefix:  [[../concepts/foo]] -> [[concepts/foo]]
  - log_informal:   [[Beamforming]] in log.md -> [[concepts/beamforming|Beamforming]]
  - truly_broken:   target page does not exist (left for manual review)
"""
import sys
import os
import re
import glob
import json
import argparse

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

CATEGORIES = ['entities', 'concepts', 'sources', 'synthesis', 'queries']


def extract_target(raw_link: str) -> str:
    """Extract the page target from a [[...]] wikilink.

    Handles section anchors (#Section) and escaped pipes (\\|).
    Returns the target slug (without display text or anchor).
    """
    if '#' in raw_link:
        raw_link = raw_link.split('#', 1)[0]
    if '\\|' in raw_link:
        target = raw_link.split('\\|', 1)[0]
    elif '|' in raw_link:
        target = raw_link.split('|', 1)[0]
    else:
        target = raw_link
    return target.strip()


def find_category_for_slug(slug: str, case_insensitive: bool = False) -> str | None:
    """Find which category contains a slug. Returns category name or None.

    If case_insensitive=True, performs a case-insensitive filename match
    (used for log_informal refs where the human-readable name may have caps).
    """
    if case_insensitive:
        slug_lower = slug.lower()
        for cat in CATEGORIES:
            d = f'wiki/{cat}'
            if not os.path.isdir(d):
                continue
            for entry in os.listdir(d):
                if entry.lower() == f'{slug_lower}.md':
                    return f'{cat}/{entry[:-3]}'
        return None

    for cat in CATEGORIES:
        if os.path.exists(f'wiki/{cat}/{slug}.md'):
            return f'{cat}/{slug}'
    return None


def classify_file(path: str, report: dict) -> None:
    """Classify all wikilinks in a single file, populating the report dict."""
    rel = os.path.relpath(path).replace('\\', '/')
    is_log = rel.endswith('log.md')

    with open(path, encoding='utf-8') as fh:
        content = fh.read()

    for m in re.finditer(r'\[\[([^\[\]]+?)\]\]', content):
        raw = m.group(1)
        if raw.strip() == '...':
            continue

        target = extract_target(raw)
        if not target:
            continue

        # raw/ embeds are correct as-is
        if target.startswith('raw/'):
            continue

        # ../ prefix -> convention violation
        if target.startswith('../'):
            fix = target.lstrip('./')
            report['dotdot_prefix'].append({
                'target': target,
                'fix': fix,
                'location': rel,
            })
            continue

        # wiki/ prefix -> redundant
        if target.startswith('wiki/'):
            fix = target[5:]
            fixed_path = os.path.normpath(f'wiki/{fix}.md')
            if os.path.exists(fixed_path):
                report['wiki_prefix'].append({
                    'target': target,
                    'fix': fix,
                    'location': rel,
                })
            else:
                report['truly_broken'].append({
                    'target': target,
                    'location': rel,
                })
            continue

        # Already has a category prefix?
        if '/' in target:
            target_path = os.path.normpath(f'wiki/{target}.md')
            if not os.path.exists(target_path):
                report['truly_broken'].append({
                    'target': target,
                    'location': rel,
                })
            # Otherwise: well-formed link, skip
            continue

        # Bare slug, no slash
        target_path = os.path.normpath(f'wiki/{target}.md')
        if os.path.exists(target_path):
            # Truly a top-level page (rare) — well-formed, skip
            continue

        # Try to find the right category
        found = find_category_for_slug(target)
        if found:
            if is_log:
                # In log.md, bare slugs are often human-readable names
                # (e.g., [[Beamforming]]) — treat as log_informal
                report['log_informal'].append({
                    'target': target,
                    'fix': found,
                    'location': rel,
                })
            else:
                report['missing_prefix'].append({
                    'target': target,
                    'fix': found,
                    'location': rel,
                })
            continue

        # Bare slug, no category match — try case-insensitive (log.md only)
        if is_log:
            found_ci = find_category_for_slug(target, case_insensitive=True)
            if found_ci:
                report['log_informal'].append({
                    'target': target,
                    'fix': found_ci,
                    'location': rel,
                })
                continue

        # Truly broken
        report['truly_broken'].append({
            'target': target,
            'location': rel,
        })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', '-o', default=None,
                        help='Write full JSON report to this file (default: stdout)')
    args = parser.parse_args()

    report = {
        'missing_prefix': [],
        'wiki_prefix': [],
        'dotdot_prefix': [],
        'log_informal': [],
        'truly_broken': [],
    }

    for f in glob.glob('wiki/**/*.md', recursive=True):
        classify_file(f, report)

    # Summary to stderr
    print('=== Wikilink Classification Summary ===', file=sys.stderr)
    print(f'  missing_prefix: {len(report["missing_prefix"])}', file=sys.stderr)
    print(f'  wiki_prefix:    {len(report["wiki_prefix"])}', file=sys.stderr)
    print(f'  dotdot_prefix:  {len(report["dotdot_prefix"])}', file=sys.stderr)
    print(f'  log_informal:   {len(report["log_informal"])}', file=sys.stderr)
    print(f'  truly_broken:   {len(report["truly_broken"])} (not auto-fixable)',
          file=sys.stderr)
    total_fixable = (len(report['missing_prefix']) + len(report['wiki_prefix'])
                     + len(report['dotdot_prefix']) + len(report['log_informal']))
    print(f'  --- TOTAL fixable: {total_fixable}', file=sys.stderr)

    json_out = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as fh:
            fh.write(json_out)
        print(f'Report written to {args.output}', file=sys.stderr)
    else:
        print(json_out)


if __name__ == '__main__':
    main()
