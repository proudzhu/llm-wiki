#!/usr/bin/env python3
"""Regression test for the vector-figure harvest in extract_arxiv_html.py.

Why this exists: arXiv renders most plots as `<object type="image/svg+xml">`,
and the HTML->markdown converter only serializes `<img>`. Every SVG figure
therefore vanished from full-text.md with NO warning — a corpus audit found
16 of 36 arXiv-extracted papers affected, 44 caption-anchored figures lost.
`mkdocs build --strict` cannot catch it either, because a missing image is not
a broken link. The failure mode is silent, so it needs a test rather than an
eyeball pass.

The test is offline by design: it feeds a saved HTML fixture into the real
parsing/insertion functions and checks the effect on a temp markdown file, so
no network or arXiv access is needed to run it.

Usage:
  uv run python .agents/skills/paper-reader/scripts/test_vector_figures.py
Exit 0 = pass, 1 = failure.
"""
import importlib.util
import os
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, 'extract_arxiv_html.py')


def load_module():
    spec = importlib.util.spec_from_file_location('extract_arxiv_html', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Minimal but faithful slice of an arXiv HTML page: one raster figure (kept by
# the converter, so it must NOT be re-harvested) and one multi-panel vector
# figure whose panel tags read "(a)"/"(b)" while the outer caption reads
# "Fig. 4". This is the shape that broke in the Fu 2026 ingest.
FIXTURE_HTML = """<html><body>
<figure id="S1.F1" class="ltx_figure">
  <img src="2606.25621v3/raster.png" alt="Refer to caption">
  <figcaption><span class="ltx_tag ltx_tag_figure">Fig. 1</span>: Raster figure.</figcaption>
</figure>
<figure id="S4.F4" class="ltx_figure">
  <figure id="S4.F4.fig1" class="ltx_figure ltx_align_center">
    <div class="ltx_flex_cell"><object type="image/svg+xml" data="2606.25621v3/panel_a.svg" class="ltx_graphics"></object></div>
    <figcaption><span class="ltx_tag ltx_tag_figure">(a)</span> UTMOS vs. latency</figcaption>
  </figure>
  <figure id="S4.F4.fig2" class="ltx_figure ltx_align_center">
    <div class="ltx_flex_cell"><object type="image/svg+xml" data="2606.25621v3/panel_b.svg" class="ltx_graphics"></object></div>
    <figcaption><span class="ltx_tag ltx_tag_figure">(b)</span> CAcc vs. latency</figcaption>
  </figure>
  <figcaption><span class="ltx_tag ltx_tag_figure">Fig. 4</span>: Combined.</figcaption>
</figure>
</body></html>
"""

FIXTURE_MD = """Intro paragraph.

![[raw/papers/demo/figures/fig1.png|Refer to caption]]

Fig. 1: Raster figure.

Body text.

(a) UTMOS vs. latency

(b) CACC vs. latency

Fig. 4: Combined.
"""

PAGE_URL = 'https://arxiv.org/html/2606.25621'


failures = []


def check(name, cond, detail=''):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail and not cond else ''))
    if not cond:
        failures.append(name)


def main():
    mod = load_module()

    print("1. find_vector_figures locates <object> figures and their numbers")
    found = mod.find_vector_figures(FIXTURE_HTML, PAGE_URL)
    check("one vector figure group", len(found) == 1, f"got {found}")
    num, urls = found[0] if found else (None, [])
    check("number comes from the outer caption, not panel tags", num == 4, f"got {num}")
    check("both panels found", len(urls) == 2, f"got {urls}")
    check("urls are absolute", all(u.startswith('https://') for u in urls), f"{urls}")

    print("2. harvest inserts an embed per panel, each under its label")
    with tempfile.TemporaryDirectory() as td:
        figdir = os.path.join(td, 'figures')
        md = os.path.join(td, 'full-text.md')
        os.makedirs(figdir)
        with open(md, 'w', encoding='utf-8', newline='') as f:
            f.write(FIXTURE_MD)

        # Offline stand-in for the downloader: write the SVG bytes directly.
        orig_fetch = mod.fetch_image_bytes

        def fake_fetch(url, referer, allow_svg=False):
            if not allow_svg:
                raise AssertionError("SVG download must pass allow_svg=True")
            return ('<svg xmlns="http://www.w3.org/2000/svg">'
                    f'<!-- {url} --></svg>').encode()
        mod.fetch_image_bytes = fake_fetch
        try:
            n = mod.harvest_vector_figures(md, FIXTURE_HTML, PAGE_URL,
                                          figdir, 'demo')
        finally:
            mod.fetch_image_bytes = orig_fetch

        text = open(md, encoding='utf-8').read()
        lines = text.splitlines()
        check("two embeds inserted", n == 2, f"got {n}")
        check("panel a svg downloaded", os.path.exists(os.path.join(figdir, 'panel_a.svg')))
        check("panel b svg downloaded", os.path.exists(os.path.join(figdir, 'panel_b.svg')))
        check("no embed for the raster figure",
              'raster.png' not in text and text.count('![[raw/papers/demo/figures/') == 3,
              f"embeds={text.count('![[raw/papers/demo/figures/')}")

        # Each panel image must sit between its own label and the next label.
        try:
            ia = next(i for i, l in enumerate(lines) if l.startswith('(a)'))
            ib = next(i for i, l in enumerate(lines) if l.startswith('(b)'))
            embeds = [i for i, l in enumerate(lines) if 'panel_' in l]
            check("panel (a) image follows its label", embeds and ia < embeds[0] < ib,
                  f"a={ia} embeds={embeds} b={ib}")
            check("panel (b) image follows its label", len(embeds) > 1 and embeds[1] > ib)
            cap = next(i for i, l in enumerate(lines) if l.startswith('Fig. 4:'))
            check("both images precede the shared caption", cap > max(embeds), f"cap={cap} embeds={embeds}")
        except StopIteration:
            check("labels/caption still present", False, "fixture text was altered")

        print("3. harvest is idempotent (re-run inserts nothing)")
        mod.fetch_image_bytes = fake_fetch
        try:
            n2 = mod.harvest_vector_figures(md, FIXTURE_HTML, PAGE_URL, figdir, 'demo')
        finally:
            mod.fetch_image_bytes = orig_fetch
        check("second run inserts nothing", n2 == 0, f"got {n2}")
        check("file unchanged on re-run",
              open(md, encoding='utf-8').read() == text)

        print("4. CRLF files keep their line endings")
        crlf_md = os.path.join(td, 'crlf.md')
        with open(crlf_md, 'w', encoding='utf-8', newline='') as f:
            f.write(FIXTURE_MD.replace('\n', '\r\n'))
        mod.fetch_image_bytes = fake_fetch
        try:
            mod.harvest_vector_figures(crlf_md, FIXTURE_HTML, PAGE_URL, figdir, 'demo')
        finally:
            mod.fetch_image_bytes = orig_fetch
        raw = open(crlf_md, 'rb').read()
        check("no bare LF introduced", raw.count(b'\n') == raw.count(b'\r\n'),
              f"lf={raw.count(b'\\n')} crlf={raw.count(b'\\r\\n')}")

    print()
    if failures:
        print(f"FAILED ({len(failures)}): " + ', '.join(failures))
        return 1
    print("ALL VECTOR-FIGURE CHECKS PASSED")
    return 0


if __name__ == '__main__':
    sys.exit(main())
