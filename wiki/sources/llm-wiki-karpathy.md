---
type: source
created: 2026-04-10
updated: 2026-04-10
sources:
- raw/articles/llm-wiki-karpathy.md
tags:
- knowledge-management
- llm
- pattern
aliases:
- LLM Wiki (Karpathy Gist)
---

# LLM Wiki (Karpathy Gist)

**Original Source**: [Gist by karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## Summary

An idea file describing a pattern for building personal knowledge bases using LLMs. Instead of traditional RAG (retrieval-augmented generation) where the LLM rediscovers knowledge from scratch on every query, this pattern has the LLM incrementally build and maintain a persistent wiki — a structured, interlinked collection of markdown files.

## Key Takeaways

1. **Persistent, compounding artifact**: The wiki accumulates knowledge over time. Cross-references, contradictions, and synthesis are all pre-built, not re-derived on every query.
2. **LLM writes, human curates**: The human sources documents and asks questions; the LLM does all the summarizing, cross-referencing, filing, and bookkeeping.
3. **Three-layer architecture**:
   - **Raw sources** — immutable source documents (articles, papers, images)
   - **The wiki** — LLM-generated markdown pages (summaries, entities, concepts, synthesis)
   - **The schema** — configuration file (e.g., `AGENTS.md`) telling the LLM how to structure and maintain the wiki
4. **Three core operations**:
   - **Ingest** — process a new source, update 10-15 wiki pages
   - **Query** — ask questions, synthesize answers, file results back into the wiki
   - **Lint** — periodic health checks for contradictions, stale claims, orphan pages
5. **Index and log**: Two special files (`index.md` and `log.md`) help navigate the wiki. The index is content-oriented; the log is chronological.
6. **Obsidian as IDE**: The wiki works well with Obsidian for browsing, graph view, and real-time preview of LLM edits.

## Related Concepts

- [LLM Wiki Pattern](../concepts/llm-wiki-pattern.md)
- RAG (Retrieval-Augmented Generation)
- Memex (Vannevar Bush, 1945)

## Related Entities

- *(none yet — add as you discover people/organizations in future sources)*

## Notes

- The document is intentionally abstract — implementation details depend on domain and preferences.
- Mentioned tools: Obsidian, qmd (local search), Marp (slide decks), Dataview (Obsidian plugin).
- The wiki is just a git repo — version history, branching, and collaboration are free.

## Related Synthesis
