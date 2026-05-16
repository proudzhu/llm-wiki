# Build Verification (MkDocs)

The wiki is published via MkDocs Material. The canonical correctness check is:

```powershell
uv run mkdocs build --strict
```

`--strict` causes the build to fail on **any** WARNING. This is intended as a *sanity check* — page-creation conventions in [AGENTS.md → Link Conventions](AGENTS.md) are designed so the build should always pass on the first try. If a WARNING is produced, the offending page violated a convention and should be fixed in place rather than worked around at build time.

## Build mechanics

- **`docs_dir: wiki`** — only the `wiki/` tree is treated as documentation source.
- **Vault root vs. docs root**: The Obsidian vault root is the **project root** (the directory containing `.obsidian/`), but MkDocs' `docs_dir` is the *child* `wiki/` directory. This asymmetry is the root cause of most link-resolution issues. The link conventions paper over the asymmetry by mandating vault-absolute paths everywhere.
- **`raw/` exposed virtually**: `raw/**/*.md` is excluded from the build (see `mkdocs.yml`). The non-markdown contents of `raw/` (figures, images, data) are exposed to MkDocs by [`hooks.py`](../hooks.py)'s `on_files` hook, which registers each file as a `File` whose served URL is `raw/<relative path>`. MkDocs copies those files straight into `site/raw/...` during the build. There is **no symlink, junction, or filesystem mutation** — interrupted builds never leave the working tree dirty.
- **Wikilink resolution**: The custom MkDocs plugin [`fix_obsidian_escapes`](../plugins/fix_obsidian_escapes.py) implements two `on_page_markdown` resolvers:
  - `RoamLinkReplacer` rewrites `[[entities/foo|Foo]]` into a page-relative markdown link `[Foo](../entities/foo.md)`.
  - `EmbedRoamLinkReplacer` rewrites `![[raw/papers/foo/figures/x.jpg|alt]]` into a page-relative markdown image `![alt](../raw/papers/foo/figures/x.jpg)`.
  - Both resolvers treat the wikilink target as **vault-absolute** (relative to project root), strip the `wiki/` prefix when present, and compute `../` segments to convert to a page-relative URL.

This double layer (virtual files + wikilink resolver) is what lets a single text form — `![[raw/.../x.jpg]]` or `[[concepts/foo]]` — render correctly in both Obsidian (which interprets it natively as vault-absolute) and the published MkDocs site.

## Why these conventions exist

Three failure modes the conventions defend against:

- **`../` in wikilinks**: Obsidian's wikilinks are *names*, not paths. `[[../concepts/foo]]` is interpreted as a literal note name "../concepts/foo" and fails to resolve. Vault-absolute (`[[concepts/foo]]`) is the only form that works in Obsidian.
- **Markdown images with relative paths to `raw/`**: From `wiki/sources/foo.md`, the path `../raw/x.jpg` resolves to `<vault>/wiki/raw/x.jpg` in Obsidian (because Obsidian uses vault-relative resolution for markdown images), which does not exist — `raw/` is at `<vault>/raw/`. Embed wikilinks bypass this because Obsidian treats `![[raw/x.jpg]]` as vault-absolute.
- **Nonexistent targets**: Both `[[concepts/missing]]` and `[Foo](../concepts/missing.md)` produce strict-mode WARNINGs. Always verify the target exists before linking.

## Quick commands

Run a full strict build:

```powershell
uv run mkdocs build --strict
```

Filter to only failing-level output:

```powershell
uv run mkdocs build --strict 2>&1 | Select-String -Pattern "WARNING|ERROR|Aborted"
```

Migrate legacy `[[../...]]` and `![alt](../raw/...)` to the current conventions:

```powershell
uv run python scripts/migrate_to_vault_absolute.py
```

A clean run ends with `INFO - Documentation built in N seconds` and exit code 0.
