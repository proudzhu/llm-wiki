"""MkDocs build hooks.

Exposes the sibling `raw/` tree (figures, images, data files) inside the MkDocs
virtual file system so wiki pages can reference them with a single `../raw/...`
relative path under `--strict`.

Implementation: the `on_files` hook registers every non-markdown file under
`raw/` as a `File` object whose served URL is `raw/<relative path>`. No
filesystem mutation occurs — there is no symlink or junction, and no cleanup
is required, so interrupted builds never leave the repository in a dirty state.
"""

from pathlib import Path

from mkdocs.structure.files import File


SKIP_SUFFIXES = {".md", ".markdown", ".txt"}


def on_files(files, config, **kwargs):
    docs_dir = Path(config["docs_dir"]).resolve()
    raw_root = (docs_dir.parent / "raw").resolve()

    if not raw_root.is_dir():
        return files

    project_root = docs_dir.parent

    for path in raw_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue

        src_path = path.relative_to(project_root).as_posix()

        files.append(
            File(
                path=src_path,
                src_dir=str(project_root),
                dest_dir=config["site_dir"],
                use_directory_urls=config["use_directory_urls"],
            )
        )

    return files
