# LLM Wiki

A personal knowledge base incrementally built and maintained by an LLM.

## Overview

This project implements the **LLM Wiki Pattern** — instead of traditional RAG (retrieval-augmented generation) where the LLM rediscovers knowledge from scratch on every query, an LLM incrementally builds and maintains a persistent wiki: a structured, interlinked collection of markdown files.

> **Human's job**: Curate sources, direct analysis, ask good questions, think about meaning.
> **LLM's job**: Everything else (summarizing, cross-referencing, filing, bookkeeping).

## Directory Structure

```
llm-wiki/
├── raw/                    # Immutable source documents (read-only)
│   ├── articles/           # Web articles, blog posts
│   ├── papers/             # Academic papers, technical reports
│   ├── reports/            # Reports, documentation
│   └── assets/             # Images, data files referenced by sources
│
├── wiki/                   # LLM-maintained knowledge base
│   ├── index.md            # Content catalog of all wiki pages
│   ├── log.md              # Chronological activity log
│   ├── entities/           # Entity pages (people, organizations, places)
│   ├── concepts/           # Concept/topic pages
│   ├── sources/            # Summary pages for each raw source
│   ├── synthesis/          # Cross-source analysis, comparisons, insights
│   └── queries/            # Saved query results and analyses
│
├── schema/                 # Configuration and conventions
│   └── AGENTS.md           # Instructions for the LLM on how to maintain the wiki
│
└── README.md               # This file
```

## How It Works

### Three Layers

1. **Raw Sources** (`raw/`) — Your curated collection of source documents. These are **immutable** — the LLM reads from them but never modifies them.

2. **The Wiki** (`wiki/`) — LLM-generated markdown files: summaries, entity pages, concept pages, comparisons, synthesis. The LLM owns this layer entirely.

3. **The Schema** (`schema/AGENTS.md`) — Tells the LLM how the wiki is structured, what conventions to follow, and what workflows to execute. This is what makes the LLM a disciplined wiki maintainer rather than a generic chatbot.

### Three Operations

| Operation | Description |
|-----------|-------------|
| **Ingest** | Drop a new source into `raw/`, tell the LLM to process it. The LLM reads it, updates relevant wiki pages, and logs the activity. |
| **Query** | Ask questions against the wiki. The LLM finds relevant pages, synthesizes an answer with citations, and optionally saves it. |
| **Lint** | Periodic health check: contradictions between pages, stale claims, orphan pages, missing cross-references. |

### Special Files

- **`wiki/index.md`** — Content-oriented catalog of all wiki pages, organized by category. The LLM reads this first when answering queries.
- **`wiki/log.md`** — Chronological, append-only record of operations. Parseable with unix tools: `grep "^## \[" wiki/log.md | tail -5`

## Getting Started

1. **Add a source**: Place a document (article, paper, report) into `raw/articles/`, `raw/papers/`, or `raw/reports/`.
2. **Tell the LLM to ingest**: Share the `schema/AGENTS.md` with your LLM agent and ask it to process the new source.
3. **Browse the wiki**: Open `wiki/index.md` to see what's in the knowledge base. Use Obsidian for the best experience (graph view, real-time preview).
4. **Ask questions**: Query the wiki through your LLM. Good answers can be saved as new pages in `wiki/queries/`.

## Recommended Tools

- **Obsidian** — Markdown editor with graph view, web clipper, and plugin ecosystem
- **qmd** — Local search engine for markdown files (hybrid BM25/vector search)
- **Marp** — Markdown-based slide deck format
- **Dataview** — Obsidian plugin for querying page frontmatter

## Version Control

The wiki is just a git repo. Initialize it to get version history, branching, and collaboration:

```bash
git init
git add .
git commit -m "Initial wiki setup"
```

## Learn More

- [[LLM Wiki Pattern]] — The core concept explained
- [Original Gist by Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — The source document
