from setuptools import setup, find_packages

setup(
    name="mkdocs-fix-obsidian-escapes",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "fix_obsidian_escapes = plugins.fix_obsidian_escapes:FixObsidianEscapesPlugin",
        ]
    },
    install_requires=["mkdocs>=1.0"],
)
