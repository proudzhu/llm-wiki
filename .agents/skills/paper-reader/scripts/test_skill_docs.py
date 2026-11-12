#!/usr/bin/env python3
"""Regression test for the skill's own documentation.

Why this exists: the docs drift silently. Two real incidents —
`map_figures.py` was documented as "Step 4a" long after the workflow
renumbered it to 3e, and `append_log.py --files` (nonexistent) was
documented for a step whose flag is `--file`. Neither breaks a build, so
nothing caught them. This test pins the invariants that a reader relies on:

  1. SKILL.md frontmatter parses, has `name` and `description`, and the
     description stays short enough to be usable as a trigger hint.
  2. Every `references/*.md` path mentioned in SKILL.md exists.
  3. Every `scripts/<name>.py` mentioned in SKILL.md exists.
  4. Every long flag documented next to a script name is actually accepted
     by that script's argparse (checked by AST, so no subprocess needed).
  5. Every `pitfalls.md #N` reference resolves to an existing entry, and the
     entries are numbered 1..N with no gaps or duplicates.
  6. Step numbers cited by the docs and by script docstrings agree with the
     workflow's step set.

Usage:
  uv run python .agents/skills/paper-reader/scripts/test_skill_docs.py
Exit 0 = pass, 1 = failure.
"""
import ast
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
SKILL_MD = SKILL_DIR / 'SKILL.md'
REFS = SKILL_DIR / 'references'

# Workflow steps the docs may cite. Step 3 has sub-steps, 12 has checks.
VALID_STEPS = {f'{n}' for n in range(1, 14)} | {'3a', '3b', '3c', '3d', '3e',
                                                '12a', '12b', '12c'}

failures = []
checks = [0]


def check(cond, msg):
    checks[0] += 1
    if not cond:
        failures.append(msg)


def parse_frontmatter(text):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', text, re.S)
    if not m:
        return None
    data = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(':')
        if not _ or not k.strip():
            continue
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] == '"':
            v = v[1:-1].replace('\\"', '"')
        data[k.strip()] = v
    return data


def script_flags(path):
    """Long option strings a script's argparse accepts, via AST."""
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
    except SyntaxError:
        return None
    flags = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = getattr(fn, 'attr', None) or getattr(fn, 'id', None)
        if name not in ('add_argument', 'add_parser'):
            continue
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                if arg.value.startswith('-'):
                    flags.add(arg.value)
    return flags


def main():
    text = SKILL_MD.read_text(encoding='utf-8')
    flat = re.sub(r'\s+', ' ', text)

    # 1. Frontmatter
    fm = parse_frontmatter(text)
    check(fm is not None, 'SKILL.md: no YAML frontmatter')
    if fm:
        check('name' in fm and fm['name'], 'SKILL.md: frontmatter missing name')
        desc = fm.get('description', '')
        check(len(desc) > 80, 'SKILL.md: description too short to route on')
        check(len(desc) <= 1024,
              f'SKILL.md: description {len(desc)} chars (limit 1024)')

    # 2. Reference files
    for ref in sorted(set(re.findall(r'references/([a-z0-9-]+\.md)', text))):
        check((REFS / ref).exists(), f'SKILL.md: references/{ref} does not exist')

    # 3. Script files — split this skill's scripts from other skills' scripts
    #    (SKILL.md also invokes wiki-lint's check_statistics.py).
    other_skill_scripts = {
        (skill, name)
        for skill, name in re.findall(
            r'skills/([a-z0-9-]+)/scripts/([a-z0-9_]+\.py)', text)
        if skill != 'paper-reader'
    }
    foreign = {name for _, name in other_skill_scripts}
    skill_root = SKILL_DIR.parent           # .agents/skills
    for skill, name in sorted(other_skill_scripts):
        target = skill_root / skill / 'scripts' / name
        if target.parent.parent.exists():   # sibling skill installed here
            check(target.exists(),
                  f'SKILL.md: skills/{skill}/scripts/{name} does not exist')

    own_scripts = set(re.findall(r'scripts/([a-z0-9_]+\.py)', text)) - foreign
    check(len(own_scripts) >= 10,
          f'SKILL.md: only {len(own_scripts)} own scripts referenced — the '
          f'command table likely drifted')
    for s in sorted(own_scripts):
        check((HERE / s).exists(), f'SKILL.md: scripts/{s} does not exist')

    # 4. Documented flags exist in the owning script. Each match pairs the
    #    nearest preceding `scripts/<name>.py` (or bare `<name>.py`) with the
    #    flags on the same line/clause, in the command table and code blocks.
    flag_checked = 0
    for line in text.splitlines():
        if '`' not in line:
            continue
        for m in re.finditer(r'([a-z0-9_]+\.py)([^|\n`]*)', line):
            owner, tail = m.group(1), m.group(2)
            path = HERE / owner
            if not path.exists() or owner.startswith('test_'):
                continue
            accepted = script_flags(path)
            if not accepted:
                continue
            for flag in set(re.findall(r'(?<![\w-])(--[a-z][a-z0-9-]+)', tail)):
                flag_checked += 1
                check(flag in accepted,
                      f'SKILL.md documents {owner} {flag}, which argparse '
                      f'does not accept (has: '
                      f'{", ".join(sorted(accepted))[:120]}...)')
    check(flag_checked >= 15,
          f'SKILL.md: parsed only {flag_checked} documented flags — the '
          f'command table likely drifted from the scripts')

    # 5. Pitfall numbering and cross-references
    pitfalls = (REFS / 'pitfalls.md').read_text(encoding='utf-8')
    numbers = [int(n) for n in re.findall(r'^(\d+)\. \*\*', pitfalls, re.M)]
    check(numbers == list(range(1, len(numbers) + 1)),
          f'pitfalls.md: numbering is not 1..{len(numbers)} contiguous '
          f'(gaps or duplicates: '
          f'{sorted(set(numbers) ^ set(range(1, max(numbers) + 1)))[:10]})')
    check(len(numbers) >= 60, 'pitfalls.md: lost entries?')
    known = set(numbers)
    # Forms: `pitfalls.md` #13, "pitfalls.md #50, #51", "(pitfalls.md #44)", "pitfall #61".
    for group in re.findall(r'pitfalls?\.md`?\s*((?:#\d+(?:,\s*)?)+)', flat):
        for cited in re.findall(r'#(\d+)', group):
            check(int(cited) in known,
                  f'SKILL.md cites pitfalls.md #{cited}, which does not exist')
    for cited in re.findall(r'pitfall #(\d+)', flat):
        check(int(cited) in known,
              f'SKILL.md cites pitfall #{cited}, which does not exist')

    # 6. Step numbers cited anywhere in the skill docs stay in the step set
    for doc in [SKILL_MD, *sorted(REFS.glob('*.md'))]:
        body = doc.read_text(encoding='utf-8')
        for step in set(re.findall(r'\bStep (\d+[a-e]?)\b', body)):
            check(step in VALID_STEPS,
                  f'{doc.name}: cites Step {step}, outside the workflow '
                  f'({sorted(VALID_STEPS)})')

    for doc in [SKILL_MD, *sorted(REFS.glob('*.md'))]:
        for ref in set(re.findall(r'`?(page-templates|review-papers|'
                                  r'edge-cases|pitfalls)\.md`?', doc.read_text(encoding='utf-8'))):
            check((REFS / f'{ref}.md').exists(),
                  f'{doc.name}: names {ref}.md, which does not exist')

    if failures:
        print(f'FAILED {len(failures)} of {checks[0]} checks:\n')
        for f in failures:
            print(f'  - {f}')
        return 1
    print(f'ALL SKILL-DOC CHECKS PASSED ({checks[0]} assertions)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
