"""One-shot migration: vault-absolute links for Obsidian + MkDocs parity.

Rewrites two patterns across all `wiki/**/*.md` files:

1.  `[[../<subdir>/<page>|<text>]]` -> `[[<subdir>/<page>|<text>]]`
    Strips the leading `../` from wiki-internal wikilinks so they resolve as
    vault-absolute paths in Obsidian (with `newLinkFormat: absolute`) and
    are picked up unchanged by the MkDocs RoamLinkReplacer.

2.  `![<alt>](../raw/<path>)` -> `![[raw/<path>|<alt>]]`
    Converts markdown image references that point at the sibling `raw/`
    tree into Obsidian embed wikilinks. The MkDocs `EmbedRoamLinkReplacer`
    converts these back into proper relative markdown images at build time.
    This makes images render in Obsidian (which treats embed wikilinks as
    vault-absolute) without breaking the MkDocs build.

Run from the repo root:

    uv run python scripts/migrate_to_vault_absolute.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


WIKILINK_PARENT_RE = re.compile(r"\[\[\.\./([^\]\|#]+?)((?:#[^\]\|]+)?(?:\|[^\]]+)?)\]\]")
EMBED_PARENT_RE = re.compile(r"!\[\[\.\./([^\]\|]+?)(\|[^\]]+)?\]\]")
IMAGE_RAW_RE = re.compile(r"!\[([^\]]*)\]\(\.\./raw/([^)]+)\)")


def migrate_text(text: str) -> tuple[str, dict[str, int]]:
    counts = {"wikilink_parent": 0, "embed_parent": 0, "image_raw": 0}

    def _wikilink(match: re.Match) -> str:
        counts["wikilink_parent"] += 1
        return f"[[{match.group(1)}{match.group(2)}]]"

    def _embed(match: re.Match) -> str:
        counts["embed_parent"] += 1
        target = match.group(1)
        suffix = match.group(2) or ""
        return f"![[{target}{suffix}]]"

    def _image(match: re.Match) -> str:
        counts["image_raw"] += 1
        alt = match.group(1)
        path = match.group(2)
        if alt:
            return f"![[raw/{path}|{alt}]]"
        return f"![[raw/{path}]]"

    text = WIKILINK_PARENT_RE.sub(_wikilink, text)
    text = EMBED_PARENT_RE.sub(_embed, text)
    text = IMAGE_RAW_RE.sub(_image, text)
    return text, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Report changes without writing files.")
    parser.add_argument("--root", default="wiki",
                        help="Directory to scan (default: wiki).")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 1

    total = {"wikilink_parent": 0, "embed_parent": 0, "image_raw": 0}
    files_changed = 0

    for path in sorted(root.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        rewritten, counts = migrate_text(original)
        if rewritten == original:
            continue
        files_changed += 1
        for key in total:
            total[key] += counts[key]
        delta = ", ".join(f"{k}={v}" for k, v in counts.items() if v)
        print(f"  {path.as_posix()}: {delta}")
        if not args.dry_run:
            path.write_text(rewritten, encoding="utf-8")

    mode = "DRY RUN" if args.dry_run else "WROTE"
    print()
    print(f"{mode}: {files_changed} files, "
          f"{total['wikilink_parent']} wikilinks, "
          f"{total['embed_parent']} embed wikilinks, "
          f"{total['image_raw']} markdown images")
    return 0


if __name__ == "__main__":
    sys.exit(main())
