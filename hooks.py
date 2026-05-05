import os
import subprocess
import sys


def on_pre_build(config, **kwargs):
    docs_dir = config["docs_dir"]
    raw_link = os.path.join(docs_dir, "raw")
    raw_target = os.path.join(os.path.dirname(docs_dir), "raw")

    if os.path.exists(raw_link):
        return

    if not os.path.isdir(raw_target):
        return

    if sys.platform == "win32":
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", os.path.abspath(raw_link), os.path.abspath(raw_target)],
            check=True, capture_output=True,
        )
    else:
        os.symlink(os.path.abspath(raw_target), raw_link)


def on_post_build(config, **kwargs):
    docs_dir = config["docs_dir"]
    raw_link = os.path.join(docs_dir, "raw")

    if not os.path.exists(raw_link):
        return

    if sys.platform == "win32":
        subprocess.run(
            ["cmd", "/c", "rmdir", os.path.abspath(raw_link)],
            check=True, capture_output=True,
        )
    else:
        os.unlink(raw_link)
