#!/usr/bin/env python3
"""Step 9 triage: find synthesis pages whose frontmatter tags overlap with the
source page's frontmatter tags.

Reads the `tags:` list from `wiki/sources/{slug}.md` and from each
`wiki/synthesis/*.md` (excluding `index.md`), then prints the synthesis
pages that share at least one tag with the source page — sorted by
tag-overlap size — so the agent can decide which pages to actually read.

This is cheaper and more systematic than reading full synthesis pages
(some are 200-400 lines) to decide whether to update them.

Usage:
  uv run python .agents/skills/paper-reader/scripts/triage_synthesis.py --slug SLUG

Exit codes:
  0  always (triage helper, not a pass/fail check)
"""
import argparse, os, re, sys

try:
    import yaml  # PyYAML (transitive dep of mkdocs; also used by update_indexes.py)
except ImportError:
    print("ERROR: PyYAML is required. Install with `pip install pyyaml` or `uv add pyyaml`.",
          file=sys.stderr)
    sys.exit(2)

sys.stdout.reconfigure(encoding='utf-8')

FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)


def read_frontmatter_tags(path):
    """Read the `tags:` list from a markdown file's YAML frontmatter.

    Returns a set of tag strings. Returns an empty set if the file has no
    frontmatter or no `tags:` list. Raises yaml.YAMLError if the frontmatter
    is malformed — the caller should fix the file, not silently skip it.
    """
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    m = FRONTMATTER_RE.match(text)
    if not m:
        return set()

    data = yaml.safe_load(m.group(1))
    if isinstance(data, dict) and isinstance(data.get('tags'), list):
        return {str(t).strip() for t in data['tags'] if t}
    return set()


def main():
    ap = argparse.ArgumentParser(
        description=__doc__.split('\n')[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--slug', required=True,
                    help='Source page slug (reads wiki/sources/{slug}.md)')
    args = ap.parse_args()

    source_path = os.path.join('wiki', 'sources', f'{args.slug}.md')
    synth_dir = os.path.join('wiki', 'synthesis')

    if not os.path.isfile(source_path):
        print(f'ERROR: source page not found: {source_path}', file=sys.stderr)
        sys.exit(1)

    source_tags = read_frontmatter_tags(source_path)
    if not source_tags:
        print(f'WARNING: no tags found in {source_path}')
        print('Cannot perform tag-based triage. Read all synthesis pages or skip Step 9.')
        return

    print(f'Source: {source_path}')
    print(f'Source tags ({len(source_tags)}): {", ".join(sorted(source_tags))}')
    print()

    candidates = []
    skipped = 0
    for fname in sorted(os.listdir(synth_dir)):
        if not fname.endswith('.md') or fname == 'index.md':
            continue
        spath = os.path.join(synth_dir, fname)
        try:
            stags = read_frontmatter_tags(spath)
        except yaml.YAMLError as e:
            print(f'ERROR: malformed YAML frontmatter in {spath}: {e}',
                  file=sys.stderr)
            print('Fix the frontmatter in that file before running triage.',
                  file=sys.stderr)
            sys.exit(1)
        overlap = source_tags & stags
        if overlap:
            candidates.append((fname[:-3], overlap, stags))
        else:
            skipped += 1

    if not candidates:
        print('No synthesis pages share tags with this source page.')
        print(f'-> Skip Step 9 (no synthesis update needed based on tag triage).')
        if skipped:
            print(f'   ({skipped} synthesis page(s) checked, 0 matched.)')
        return

    candidates.sort(key=lambda x: -len(x[1]))
    print(f'CANDIDATE synthesis pages ({len(candidates)}, sorted by tag-overlap size):')
    for slug, overlap, stags in candidates:
        print(f'\n  {slug}.md')
        print(f'    Shared tags ({len(overlap)}): {", ".join(sorted(overlap))}')
        print(f'    All synthesis tags: {", ".join(sorted(stags))}')
    print(f'\n-> Read the {len(candidates)} candidate page(s) above, then evaluate the trigger checklist in SKILL.md Step 9.')
    if skipped:
        print(f'   ({skipped} synthesis page(s) skipped with zero tag overlap.)')


if __name__ == '__main__':
    main()
