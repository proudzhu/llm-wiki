---
type: query
created: 2026-04-11
updated: 2026-04-11
sources:
  - raw/articles/ai-assistance-coding-skills.md
tags:
  - AI-assistance
  - coding
  - productivity
  - skill-formation
---

# How AI Impacts Coding

Based on the wiki's evidence from a single rigorous study — an **RCT by Shen & Tamkin (Anthropic, 2026)** with 52 software developers. The impact is nuanced and depends on **what the developer is doing** and **how they use AI**.

## Two Different Effects

| Scenario                        | Impact                               | Evidence                                     |
| ------------------------------- | ------------------------------------ | -------------------------------------------- |
| **Already skilled** at the task | **+80% speedup** (productivity gain) | Earlier observational research, same authors |
| **Learning something new**      | **−17% mastery** (skill deficit)     | RCT, n=52, p=0.01                            |

So AI both accelerates productivity on well-developed skills **and** hinders acquisition of new ones.

## The Core Problem: Cognitive Offloading

When developers use AI to learn a new library, they offload the mental work to the AI — skipping the "productive struggle" needed for mastery. In the RCT:

- AI group averaged **50%** on a comprehension quiz vs **67%** for hand-coders
- The **largest gap** was on **debugging questions** — the ability to detect and diagnose errors
- Task completion was ~2 min faster but **not statistically significant**

## Six Interaction Patterns (Outcomes Vary Widely)

**Productive patterns** (≥65% quiz score):
- **Conceptual Queries** — Only ask conceptual questions, code independently (fastest high-scoring pattern)
- **Hybrid Queries** — Ask for code + explanations together
- **Verification** — Generate code, then ask follow-up questions to understand

**Unproductive patterns** (<40% quiz score):
- **AI Delegation** — Wholly rely on AI to write code (fastest overall, poorest learning)
- **Hybrid Delegation** — Start with questions, then delegate all coding
- **AI Debugging** — Use AI to debug/verify without building understanding

## Key Implication

The way people interact with AI while trying to be efficient **determines how much they learn**. Under time pressure, junior developers tend toward delegation patterns — completing tasks fast but stunting the debugging and code-reading skills needed to validate AI-written code long-term.
