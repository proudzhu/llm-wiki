"""Shared utilities for wikilink processing.

Used by classify_links.py, fix_links.py, and verify_fix.py.
"""
import os

CATEGORIES = ['entities', 'concepts', 'sources', 'synthesis', 'queries']


def extract_target(raw_link: str) -> tuple[str, str | None, str | None]:
    """Split a wikilink interior into (target, separator, rest).

    Args:
        raw_link: The interior of a [[...]] wikilink (without brackets)

    Returns:
        tuple of (target, separator, rest) where:
        - target: the link target (before any | or \\|), includes section anchor
        - separator: None, '|', or '\\|' (the delimiter that introduced display text)
        - rest: the display text after the separator, or None

    Section anchors are kept on the target side: e.g., for 'foo#Section|Display',
    target='foo#Section', separator='|', rest='Display'.
    """
    # Find the first separator (escaped pipe takes precedence over plain pipe)
    if '\\|' in raw_link:
        idx = raw_link.index('\\|')
        target = raw_link[:idx].strip()
        rest = raw_link[idx + 2:]
        return target, '\\|', rest
    if '|' in raw_link:
        idx = raw_link.index('|')
        target = raw_link[:idx].strip()
        rest = raw_link[idx + 1:]
        return target, '|', rest
    return raw_link.strip(), None, None


def split_anchor(target: str) -> tuple[str, str]:
    """Split 'foo#Section' -> ('foo', '#Section'). Returns (slug, anchor_or_empty)."""
    if '#' in target:
        idx = target.index('#')
        return target[:idx], target[idx:]
    return target, ''


def find_category_for_slug(slug: str, case_insensitive: bool = False) -> str | None:
    """Find which category contains a slug. Returns 'category/slug' or None.

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
