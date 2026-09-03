#!/usr/bin/env python3
"""Step 4a: Map MinerU figure files to figure numbers in full-text.md.

MinerU extracts papers as hash-named JPEG crops in raw/papers/{slug}/figures/
and inlines SOME of them into full-text.md as ![](figures/HASH.jpg). Multi-panel
figures are usually split into several files, and axis/colorbar strips are
sometimes extracted but never referenced. Manually pairing the ~14 hashes with
"Fig. N." captions (by rendering the PDF or template matching) is slow and
error-prone. This script does the pairing in one call.

Usage:
  uv run python .agents/skills/paper-reader/scripts/map_figures.py --slug author-year-title
  uv run python .agents/skills/paper-reader/scripts/map_figures.py --slug ... --json

Output:
  - For each caption, the image files assigned to it (by line proximity in
    full-text.md, since MinerU's reading order is usually reliable but not
    always), plus any "(a)"/"(b)" sub-label lines in the same span.
    If no caption-style lines exist, in-text "Fig. N" references (first
    mention per figure) are used as anchors instead (mode: in-text in the
    JSON output; verify heuristic pairings against sub-labels).
  - Files in figures/ that full-text.md never references (usually axis strips
    or split-off sub-panels — check dimensions; skip strips).
  - Referenced files that are MISSING on disk (hash typos that would abort
    `mkdocs build --strict`).

Handles both MinerU markdown (![](figures/HASH.jpg)) and arXiv-HTML embed
wikilink (![[raw/papers/{slug}/figures/fig1.png|alt]]) reference styles.

Requires: nothing beyond the Python stdlib.
"""
import argparse
import json
import os
import re
import sys

# Force UTF-8 stdout/stderr so non-ASCII caption text doesn't trip Windows
# cp1252 consoles.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass

# Matches any `figures/<name>` token with an image extension, regardless of
# wrapper syntax: ![](figures/x.jpg), ![[raw/papers/s/figures/x.png|alt]],
# or bare references.
IMG_RE = re.compile(r'figures/([A-Za-z0-9_\-\.]+\.(?:png|jpe?g|gif|webp))')
# IEEE captions start the line: "Fig. 1.", "Fig. 2:", "Figure 3:" ...
# The punctuation after the number is REQUIRED: in-text prose like
# "Figure 1 compares logmelspec..." has no period after the digit and
# must not be mistaken for a caption.
CAP_RE = re.compile(r'^\s*(?:Fig(?:\.?|ure)|FIGURE)\s*(\d+)\s*[:.)]')
# In-text figure references: "Fig. 1", "Figs. 2 and 3", "Figure 4" anywhere
# in a line. Used ONLY as a fallback anchor when no caption-style lines
# exist (pitfalls.md #32) — CAP_RE deliberately excludes these to avoid
# mistaking prose for captions; here the prose IS the only anchor.
INTEXT_RE = re.compile(r'\b(?:Figs?\.|Figures?)\s*(\d+)\b', re.IGNORECASE)
# Sub-panel labels inside a figure: "(a)", "(b)", "(i)", "(left)" ...
SUB_RE = re.compile(r'^\s*\(([a-z]+|ivx{0,3}|left|middle|right|top|bottom)\)')

# JPEG SOF markers carrying dimensions (stdlib-only size probe).
_SOF = (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD,
        0xCE, 0xCF)


def jpeg_size(path):
    """Return (width, height) for a JPEG without PIL, or None."""
    try:
        with open(path, 'rb') as f:
            data = f.read(1 << 16)
        if data[:2] != b'\xff\xd8':
            return None
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            length = int.from_bytes(data[i + 2:i + 4], 'big')
            if marker in _SOF:
                h = int.from_bytes(data[i + 5:i + 7], 'big')
                w = int.from_bytes(data[i + 7:i + 9], 'big')
                return w, h
            i += 2 + length
    except Exception:
        pass
    return None


def parse_full_text(md_path):
    """Return (images, captions, sublabels, mode) as lists of (line_no, value).

    captions are caption-style lines ("Fig. 1." / "Figure 2:") when any
    exist. When none exist, the FIRST in-text mention of each figure number
    ("Fig. 1 shows ...", "as shown in Figure 3") is used as a pseudo-caption
    anchor (mode='in-text') — MinerU places each crop near where the figure
    appeared in the reading order, so first-mention proximity is a usable
    heuristic (pitfalls.md #32).
    """
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()
    images, captions, subs = [], [], []
    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip('\n')
        for m in IMG_RE.finditer(line):
            images.append((idx, m.group(1)))
        m = CAP_RE.match(line)
        if m:
            captions.append((idx, int(m.group(1))))
        elif SUB_RE.match(line):
            subs.append((idx, line.strip()[:60]))

    mode = 'captions'
    if not captions:
        seen = {}
        for idx, raw in enumerate(lines, start=1):
            for m in INTEXT_RE.finditer(raw):
                n = int(m.group(1))
                if n not in seen:
                    seen[n] = idx
        if seen:
            # Keep first mention per figure number, ordered by line.
            captions = [(line_no, n) for n, line_no in
                        sorted(seen.items(), key=lambda kv: kv[1])]
            mode = 'in-text'
    return images, captions, subs, mode


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--slug', required=True, help='Paper slug')
    p.add_argument('--json', action='store_true',
                   help='Emit machine-readable JSON instead of the report')
    args = p.parse_args()

    paper_dir = os.path.join('raw', 'papers', args.slug)
    md_path = os.path.join(paper_dir, 'full-text.md')
    figures_dir = os.path.join(paper_dir, 'figures')

    if not os.path.exists(md_path):
        print(f"ERROR: {md_path} not found.", file=sys.stderr)
        sys.exit(1)

    images, captions, subs, mode = parse_full_text(md_path)
    on_disk = sorted(os.listdir(figures_dir)) if os.path.isdir(figures_dir) else []
    on_disk_set = set(on_disk)

    # Sanity: figure numbers should be sequential from 1; flag gaps.
    cap_nums = [n for _, n in captions]
    gaps = [n for n in range(1, max(cap_nums) + 1) if n not in cap_nums] if cap_nums else []

    # Assign each image to the nearest caption (by line distance). When tied,
    # prefer the later caption (IEEE captions follow the figure, and MinerU's
    # reading order can interleave panels after a caption).
    result = []  # list of {num, line, text_hint, images:[{file,line}], subs:[...]}
    for cidx, cnum in captions:
        entry = {'num': cnum, 'line': cidx, 'images': [], 'subs': []}
        # caption text hint: the remainder of the caption line
        result.append(entry)
    if not result:
        print("NOTE: neither caption lines nor in-text 'Fig. N' references "
              "found in full-text.md — figure numbers cannot be mapped "
              "automatically. Review the text and images manually.",
              file=sys.stderr)
    elif mode == 'in-text':
        print("NOTE: no caption lines found; anchored on the first in-text "
              "'Fig. N' reference of each figure. Pairing is heuristic: a "
              "first-mention anchor can precede the image block of an "
              "EARLIER figure (MinerU reading order interleaves), merging "
              "adjacent figures into one group. Verify groupings against "
              "panel counts and the sub-labels below before embedding "
              "(pitfalls.md #32).",
              file=sys.stderr)

    def nearest_caption(iline):
        best, bdist = None, None
        for entry in result:
            d = abs(entry['line'] - iline)
            if bdist is None or d < bdist or (d == bdist and entry['line'] > best['line']):
                best, bdist = entry, d
        return best

    referenced = set()
    for iline, fname in images:
        entry = nearest_caption(iline)
        if entry is not None:
            entry['images'].append({'file': fname, 'line': iline})
        referenced.add(fname)

    for sline, label in subs:
        entry = nearest_caption(sline)
        if entry is not None:
            entry['subs'].append({'line': sline, 'label': label})

    # Read caption hint text from md file for display
    with open(md_path, encoding='utf-8') as f:
        md_lines = f.readlines()

    missing = sorted(referenced - on_disk_set)
    unreferenced = [f for f in on_disk if f not in referenced]
    dims = {f: jpeg_size(os.path.join(figures_dir, f)) for f in on_disk}
    strips = [f for f in unreferenced
              if dims[f] and dims[f][1] < dims[f][0] * 0.2]

    if args.json:
        out = {
            'slug': args.slug,
            'mode': mode,
            'figures': [
                {
                    'num': e['num'],
                    'line': e['line'],
                    'hint': md_lines[e['line'] - 1].strip()[:120],
                    'images': [{'file': i['file'], 'line': i['line']}
                               for i in e['images']],
                    'sublabels': [s['label'] for s in e['subs']],
                } for e in result
            ],
            'unreferenced': [
                {'file': f, 'size': dims[f], 'strip': f in strips} for f in unreferenced
            ],
            'missing': missing,
            'gaps': gaps,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        sys.exit(0 if not missing else 2)

    print(f"=== Figure map: {md_path} ===")
    for e in result:
        hint = md_lines[e['line'] - 1].strip()
        print(f"\nFig. {e['num']}. (line {e['line']})  {hint[:110]}")
        if e['subs']:
            print(f"  sub-labels: {', '.join(s['label'] for s in e['subs'])}")
        if not e['images']:
            print("  (no images referenced nearby — check if this figure is "
                  "vector/text-only or was cropped out)")
        for i in e['images']:
            marker = ''
            if dims.get(i['file']):
                w, h = dims[i['file']]
                marker = f" ({w}x{h})"
            print(f"  line {i['line']:>4}: figures/{i['file']}{marker}")

    if gaps:
        print(f"\nWARNING: figure numbers not present: {gaps} — caption "
              "regex may have missed one (e.g. 'Figure 1:' styled differently).")

    if unreferenced:
        print(f"\n=== Unreferenced files in figures/ ({len(unreferenced)}) ===")
        for f in unreferenced:
            tag = ''
            if dims[f]:
                w, h = dims[f]
                tag = f" ({w}x{h})"
            if f in strips:
                tag += "  <-- likely axis/colorbar strip, skip"
            print(f"  figures/{f}{tag}")
        print("\nThese are crops MinerU split off but did not inline. Unless a "
              "caption's 'images' list above is empty (missing panel), skip them.")

    if missing:
        print(f"\nERROR: {len(missing)} referenced file(s) MISSING on disk:")
        for f in missing:
            print(f"  figures/{f}")
        print("A typo in a hash filename will abort `mkdocs build --strict`. "
              "Copy filenames verbatim from this output.")
        sys.exit(2)
    else:
        print("\nAll referenced figure files exist on disk.")


if __name__ == '__main__':
    main()
