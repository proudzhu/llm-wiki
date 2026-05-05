---
type: concept
created: 2026-04-10
updated: 2026-04-10
sources:
- raw/articles/llm-wiki-karpathy.md
tags:
- architecture
- knowledge-management
- llm
---

# LLM Wiki Pattern

## Overview

A pattern for building personal knowledge bases where an LLM incrementally builds and maintains a persistent wiki, rather than retrieving from raw documents at query time (traditional RAG).

## Core Insight

Traditional RAG systems (NotebookLM, ChatGPT file uploads, most RAG) work by:
1. Indexing documents for retrieval
2. Finding relevant chunks at query time
3. Generating an answer from those chunks

**Problem**: The LLM rediscovers knowledge from scratch on every question. Nothing accumulates. Ask a subtle question requiring synthesis of five documents, and the LLM must find and piece together fragments every time.

**Solution**: The LLM reads sources once, extracts key information, and integrates it into a persistent wiki. Knowledge is compiled once and kept current, not re-derived.

## Architecture

```
┌─────────────────┐
│  Raw Sources    │  ← Immutable (articles, papers, images)
│  (read-only)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Schema      │  ← Configuration (AGENTS.md / CLAUDE.md)
│  (instructions) │     Tells LLM how to structure & maintain wiki
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Wiki        │  ← LLM-maintained (markdown files)
│  (LLM-owned)    │     Summaries, entities, concepts, synthesis
└─────────────────┘
```

## Operations

| Operation | Description | Frequency |
|-----------|-------------|-----------|
| **Ingest** | Process a new source, update relevant wiki pages (10-15 pages) | Per source |
| **Query** | Answer questions by searching wiki, synthesize with citations | As needed |
| **Lint** | Health check: contradictions, stale claims, orphans, missing links | Periodic |

## Key Files

- **`index.md`** — Content-oriented catalog of all wiki pages, organized by category
- **`log.md`** — Chronological, append-only record of operations (parseable with unix tools)

## Why It Works

The tedious part of knowledge base maintenance is bookkeeping: updating cross-references, keeping summaries current, noting contradictions, maintaining consistency. Humans abandon wikis because maintenance burden grows faster than value. LLMs don't get bored and can touch 15 files in one pass.

**Human's job**: Curate sources, direct analysis, ask good questions, think about meaning.
**LLM's job**: Everything else (summarizing, cross-referencing, filing, bookkeeping).

## Historical Context

Related to Vannevar Bush's **Memex** (1945) — a personal, curated knowledge store with associative trails between documents. Bush's vision was closer to this pattern than to what the web became: private, actively curated, with connections between documents as valuable as the documents themselves. The part Bush couldn't solve was who does the maintenance. The LLM handles that.

## Applications

| Domain | Use Case |
|--------|----------|
| Personal | Goals, health, self-improvement — journal entries, articles, podcast notes |
| Research | Deep topic exploration — papers, articles, reports with evolving thesis |
| Reading | Book companion wiki — characters, themes, plot threads, connections |
| Business/Team | Internal wiki — Slack threads, meeting transcripts, project docs, customer calls |
| Other | Competitive analysis, due diligence, trip planning, course notes, hobbies |

## Related Sources

- [LLM Wiki (Karpathy Gist)](../sources/llm-wiki-karpathy.md) — The original idea file

## Related Concepts
- [[how-ai-impacts-coding]]
- [[karpathy-llm-os]]
- [[llm-wiki-karpathy]]
- [[jensen-huang-nvidia-moat]]

- RAG (Retrieval-Augmented Generation) — baseline approach this pattern improves upon
- Memex (Vannevar Bush) — personal knowledge stores with associative trails
- Knowledge Management — traditional wiki and documentation practices


## Related Concepts
- [[active-noise-control|Active Noise Control]]