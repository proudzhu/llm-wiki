#!/usr/bin/env python3
"""Step 12b: Audit one-way backlink omissions (source -> concept/synthesis).

A source page's curated sections (`## Related Concepts` / `## Related
Synthesis`) link to concept/synthesis pages. Steps 8-9 update those target
pages to link back (frontmatter `sources:`, body wikilinks, `## Related
Sources`). This script catches the "Wang 2022 missing from
bcs-guided-speech-enhancement" failure mode: the source links the target, the
target curates a comparable source list, but this particular source never made
it in — typically a Step 8/9 edit that was skipped or silently dropped.

Filters out *design* non-reciprocation (hub pages like `beamforming` that
reference few or none of their in-linkers by design): a target is flagged only
if it already references >= 50% of its in-linkers (partial reciprocation)
AND the missing source shares >= 1 distinctive frontmatter tag with the
target. `mentioned-unlinked` marks sources whose author+year appear in the
target body text without a wikilink (a forgotten `[[...]]`), vs
`not-mentioned` (omitted entirely).

Usage:
  # After an ingest: audit only omissions involving the ingested source
  uv run python .agents/skills/paper-reader/scripts/check_backlinks.py --slug SLUG

  # Full vault audit (periodic lint; slower, reads every source page)
  uv run python .agents/skills/paper-reader/scripts/check_backlinks.py

  # Save the full report to a file as well
  uv run python .agents/skills/paper-reader/scripts/check_backlinks.py --out .tmp_backlink_report.txt

Exit 0 = no omissions, 1 = omissions found, 2 = usage error.
"""
import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

WIKI = Path("wiki")
LINK_RE = re.compile(r"\[\[((?:concepts|synthesis)/[^|\]#]+)")

# Tags too generic to indicate topical kinship between a source and a target.
GENERIC_TAGS = {
    "speech-enhancement", "deep-learning", "machine-learning", "signal-processing",
    "audio-processing", "speech-processing", "neural-networks",
    "deep-learning-for-signal-processing",
}


def curated_section(text: str) -> str:
    """Content of the source page's `## Related Concepts` / `## Related Synthesis` sections."""
    parts = []
    for m in re.finditer(r"^## (Related Concepts|Related Synthesis)\s*$", text, re.M):
        start = m.end()
        nxt = re.search(r"^## ", text[start:], re.M)
        parts.append(text[start:start + nxt.start()] if nxt else text[start:])
    return "\n".join(parts)


def frontmatter_tags(text: str) -> set:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return set()
    return set(re.findall(r"^\s*-\s+(\S+)\s*$", m.group(1), re.M))


def mentioned_in(surname: str, year: str, target_text: str) -> bool:
    if not surname:
        return False
    return bool(re.search(re.escape(surname) + r"[^.\n]{0,80}" + year, target_text))


def build_in_links(src_dir: Path) -> dict:
    """Map: target page (concepts|synthesis)/slug -> set of source slugs linking it."""
    in_links = defaultdict(set)
    for src_file in sorted(src_dir.glob("*.md")):
        if src_file.name == "index.md":
            continue
        section = curated_section(src_file.read_text(encoding="utf-8"))
        if not section:
            continue
        for target in LINK_RE.findall(section):
            if (WIKI / f"{target}.md").exists():
                in_links[target].add(src_file.stem)
    return in_links


def audit(slug_filter: str | None) -> list[str]:
    src_dir = WIKI / "sources"
    in_links = build_in_links(src_dir)

    if slug_filter and not (src_dir / f"{slug_filter}.md").exists():
        print(f"error: wiki/sources/{slug_filter}.md not found", file=sys.stderr)
        sys.exit(2)

    lines, total, targets_hit = [], 0, 0
    for target in sorted(in_links):
        linked = in_links[target]
        if slug_filter and slug_filter not in linked:
            continue  # scoped mode: only targets this source links to
        target_text = (WIKI / f"{target}.md").read_text(encoding="utf-8")
        recip = {s for s in linked if s in target_text}
        missing = linked - recip
        if slug_filter:
            missing &= {slug_filter}  # scoped mode: report only this source's omission
        if not recip or not missing:
            continue
        ratio = len(recip) / len(linked)
        if ratio < 0.5:
            continue  # target curates loosely by design; not the omission pattern
        t_tags = frontmatter_tags(target_text) - GENERIC_TAGS
        keep = []
        for s in sorted(missing):
            s_text = (src_dir / f"{s}.md").read_text(encoding="utf-8")
            if frontmatter_tags(s_text) & t_tags:
                keep.append(s)
        if not keep:
            continue
        targets_hit += 1
        total += len(keep)
        lines.append(f"{target}  (references {len(recip)}/{len(linked)} in-linkers, {ratio:.0%})")
        for s in keep:
            s_text = (src_dir / f"{s}.md").read_text(encoding="utf-8")
            h1 = re.search(r"^# (.+)$", s_text, re.M)
            surname = h1.group(1).split(",")[0].strip() if h1 else ""
            year_m = re.search(r"(20\d\d|19\d\d)", h1.group(1)) if h1 else None
            year = year_m.group(1) if year_m else ""
            cls = "mentioned-unlinked" if mentioned_in(surname, year, target_text) else "not-mentioned"
            lines.append(f"    MISSING [{cls}]: {s}")

    header = [
        f"Targets scanned: {len(in_links)}",
        f"Targets with tag-overlapping missing links: {targets_hit}",
        f"Total candidate omissions: {total}",
        "",
    ]
    return header + lines


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", help="audit only omissions involving this source slug (post-ingest mode)")
    ap.add_argument("--out", type=Path, help="also write the report to this file")
    args = ap.parse_args()

    report = audit(args.slug)
    body = "\n".join(report) + "\n"
    print(body, end="")
    if args.out:
        args.out.write_text(body, encoding="utf-8")
        print(f"\nreport written to {args.out}")

    total = int(re.search(r"Total candidate omissions: (\d+)", body).group(1))
    scope = f"source '{args.slug}'" if args.slug else "full vault"
    print(f"done: {total} missing backlinks ({scope})")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
