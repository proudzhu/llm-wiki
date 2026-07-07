# LLM Wiki Schema

This document defines how the LLM should maintain and interact with this knowledge base.

## Directory Structure

```
llm-wiki/
├── raw/                    # Immutable source documents (read-only)
│   ├── articles/           # Web articles, blog posts
│   ├── papers/             # Academic papers, technical reports
│   ├── reports/            # Reports, documentation
│   └── assets/             # Images, data files referenced by sources
├── wiki/                   # LLM-maintained knowledge base
│   ├── index.md            # Content catalog of all wiki pages
│   ├── log.md              # Chronological activity log
│   ├── entities/           # Entity pages (people, organizations, places)
│   ├── concepts/           # Concept/topic pages
│   ├── sources/            # Summary pages for each raw source
│   ├── synthesis/          # Cross-source analysis, comparisons, insights
│   └── queries/            # Saved query results and analyses
├── schema/                 # Configuration and conventions
├── AGENTS.md               # Schema/conventions document (this file)
└── README.md               # Project overview
```

## Conventions

### Markdown Format
- All wiki pages are valid markdown
- Use YAML frontmatter for metadata (optional but recommended)
- Internal links use relative paths: `[[entities/person-name]]` or `[Person Name](../entities/person-name.md)`
- Headings: H1 for title, H2 for major sections, H3 for subsections

### Link Conventions (apply when creating/editing pages)

These rules ensure pages render correctly in **both Obsidian and MkDocs** at write time, so the build never has anything to fix later. The rule of thumb: **all internal references use vault-absolute paths from the project root** — Obsidian (vault root = project root) and MkDocs (via the `fix_obsidian_escapes` plugin) both resolve them identically. This means: **never use `../` in wikilinks** (write `[[entities/foo|Foo]]`, not `[[../entities/foo|Foo]]`), and **use embed wikilinks `![[…]]` for figures** (markdown `![alt](…)` paths resolve incorrectly in Obsidian).

| Reference type | Form to write | Example |
| --- | --- | --- |
| Wiki page link | `[[<subdir>/<page>\|<text>]]` | `[[concepts/atfa\|ATFA]]` |
| Section link in another page | `[[<subdir>/<page>#Heading\|<text>]]` | `[[sources/liu-2025#Methodology\|Methods]]` |
| Image / figure (from `raw/`) | `![[raw/<path>\|<alt>]]` (embed wikilink) | `![[raw/papers/foo/figures/x.jpg\|Figure 1]]` |
| External URL | Standard markdown | `[ICASSP](https://...)` |

**Rules to follow while writing:**

1. **Never link to a page that does not exist.** Before writing `[[concepts/foo]]`, confirm the target file exists; otherwise either create it or use plain text.
2. **Always include the category prefix.** Write `[[concepts/beamforming]]`, not bare `[[beamforming]]`. A slug without `/` is treated as `wiki/<slug>.md` and will not resolve to the actual page. The six categories are: `entities/`, `concepts/`, `sources/`, `synthesis/`, `queries/`, and `raw/` (for asset files).
3. **Never use `wiki/` as a prefix.** The vault root is already the `wiki/` directory. Write `[[concepts/beamforming]]`, not `[[wiki/concepts/beamforming]]`.
4. **No stray `[text](...)` placeholders** in `log.md` or anywhere else.

See [BUILD.md](schema/BUILD.md) for the build mechanics that make these conventions work, and `plugins/fix_obsidian_escapes.py` for the resolver implementation.

### Page Naming
- **Entities**: `wiki/entities/{name}.md` (lowercase, hyphenated)
- **Concepts**: `wiki/concepts/{concept-name}.md` (lowercase, hyphenated)
- **Sources**: `wiki/sources/{short-title}.md` (lowercase, hyphenated)
- **Synthesis**: `wiki/synthesis/{topic}.md` (descriptive name)
- **Queries**: `wiki/queries/{query-topic}.md` (descriptive name)

### YAML Frontmatter Template

```yaml
---
type: entity|concept|source|synthesis|query
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - raw/articles/some-article.md
tags:
  - tag1
  - tag2
---
```

## Workflows

### 1. Ingest Source

When a new source is added to `raw/`:

1. Read the source document
2. Discuss key takeaways with the user
3. Create or update a summary page in `wiki/sources/`
4. **Create corresponding concept/entity pages** for key terms, methods, and named entities introduced by the source
5. Update `wiki/index.md` with new/modified pages
6. Update relevant entity pages in `wiki/entities/`
7. Update relevant concept pages in `wiki/concepts/`
8. Create/update synthesis pages if cross-source analysis is needed
9. Append entry to `wiki/log.md` with format: `## [YYYY-MM-DD] ingest | Source Title`
10. **Update subdirectory index files**: Add new entries to `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md`, and `wiki/synthesis/index.md` (as applicable) — each subdirectory maintains its own index table mirroring the corresponding section of `wiki/index.md`
11. **Verify**: Check that all new concepts/entities mentioned in the source page have corresponding wiki pages; create any missing ones
12. **Update statistics**: Recount pages in each category and update the `## Statistics` section at the bottom of `wiki/index.md` (Total pages, Entities, Concepts, Sources, Synthesis, Queries, Last updated). Run `python .agents/skills/wiki-lint/scripts/check_statistics.py` to verify counts match actual files.
13. **Build sanity check (final step)**: Run `uv run mkdocs build --strict` to confirm no WARNINGs slipped through. The page-creation rules in *Link Conventions* above are designed so this step should always pass; if it does not, the offending page violated a convention and must be fixed before the ingest is complete.

### 2. Query Wiki

When the user asks a question:

1. Read `wiki/index.md` to find relevant pages
2. Read the relevant wiki pages
3. Synthesize an answer with citations
4. Optionally save the answer as a new page in `wiki/queries/`
5. Log the query in `wiki/log.md` with format: `## [YYYY-MM-DD] query | Question topic`

### 3. Lint Wiki

Periodically (when requested), health-check the wiki using the **wiki-lint skill** (see [`.agents/skills/wiki-lint/SKILL.md`](.agents/skills/wiki-lint/SKILL.md) for full details):

1. **Index drift**: Run `python .agents/skills/wiki-lint/scripts/check_index_drift.py` — finds missing, phantom, and duplicate entries
2. **Broken links**: Run `python .agents/skills/wiki-lint/scripts/check_broken_links.py` — categorizes truly broken links vs. convention violations (bare slugs, `wiki/` prefixes, `../` prefixes)
3. **Orphan pages**: Run `python .agents/skills/wiki-lint/scripts/check_orphans.py` — finds pages with zero inbound references
4. **Statistics**: Run `python .agents/skills/wiki-lint/scripts/check_statistics.py` — verifies stated counts vs. actual files
5. **Contradictions**: Manually check for conflicting claims between pages
6. **Stale claims**: Identify claims superseded by newer sources
7. **Cross-references**: Suggest missing links between related pages
8. **Data gaps**: Identify areas that could benefit from web search
9. Log the lint pass in `wiki/log.md` with format: `## [YYYY-MM-DD] lint | Health check`

## Index Maintenance

- Update `wiki/index.md` and `wiki/*/index.md` on every ingest
- **Subdirectory index files** (`wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md`, `wiki/synthesis/index.md`) must be updated whenever pages are added or modified in their respective directories
- Each subdirectory index mirrors the corresponding section of `wiki/index.md` with the same table format (page link, summary, date)
- Organize by category: entities, concepts, sources, synthesis
- Include: page link, one-line summary, metadata (date, source count)

## Log Maintenance

- Append-only format
- Entries sorted chronologically: **newest entries at the end of the file**
- Prefix entries with `## [YYYY-MM-DD] {operation} | Description`
- Operations: `ingest`, `query`, `lint`, `merge`
- Enables parsing with unix tools: `grep "^## \[" log.md | tail -5`

## Tips

- `raw/` is **immutable** — never edit source documents in place
- This is a **git repo** — commit often
- Suggest new questions and sources to investigate
- Flag contradictions for user review rather than silently resolving them

## Build Verification (MkDocs)

After any ingest or significant edit, run `uv run mkdocs build --strict`. A clean build exits 0 with `INFO - Documentation built in N seconds`.

See [BUILD.md](schema/BUILD.md) for full mechanics, link-resolution internals, and common strict-mode pitfalls.

## Skills

Reusable workflows are stored in `.agents/skills/`. Each skill has a `SKILL.md` with full instructions.

| Skill | Path | When to use |
|-------|------|-------------|
| **paper-reader** | [`.agents/skills/paper-reader/SKILL.md`](.agents/skills/paper-reader/SKILL.md) | Ingesting a paper from Zotero — handles search, PDF extraction (MinerU/arXiv HTML/pdftotext), and full wiki page creation |
| **wiki-lint** | [`.agents/skills/wiki-lint/SKILL.md`](.agents/skills/wiki-lint/SKILL.md) | Health-checking the wiki — index drift, broken links, orphan pages, statistics verification |

**Convention violations** (bare-slug wikilinks, `wiki/` prefixes, `../` prefixes in wikilinks) accumulate over time. To bulk-fix legacy links, run:

```powershell
uv run python scripts/migrate_to_vault_absolute.py
```
