---
type: concept
created: 2026-07-24
updated: 2026-07-24
sources:
  - raw/papers/liang-wenfeng-investor-exchange-meeting/full-text.md
tags:
  - agi
  - llm
  - research-roadmap
  - intelligence-stages
  - liang-wenfeng
---

# AGI Roadmap Staircase

A distinctive narrative of how artificial intelligence progresses toward AGI, articulated by [[entities/wenfeng-liang|Liang Wenfeng]] (founder of [[entities/deepseek|DeepSeek]]) in his 2026 investor exchange meeting. The roadmap is **staircase-shaped**: each step is built on top of the previous one, and no step is disposable.

## The Staircase

1. **Language models (GPT)** — the foundation. No current ceiling observed: "language model scaling, I have not seen an upper limit so far."
2. **Chain-of-Thought (CoT)** — already exceeds top humans on competition math and coding, but plateaued without reaching AGI.
3. **Agents** — current frontier (as of 2026); will solve all problems solvable by agents, then plateau at the agent capability ceiling.
4. **Continuous learning** — the next bottleneck, **not yet solved globally**; not one technique but a problem requiring many methods. See [[concepts/continuous-learning|Continuous Learning]].
5. **Self-iterating singularity** — after continuous learning, the model can develop its own next version, then the next, in a recursive loop. Liang emphasizes this is "not really a singularity — it's a long gradual process, but habitually we call it one."
6. **Embodied AI** — last, only after self-iteration is possible. Doing embodied AI first is "the hard route"; doing it last means "the model itself develops the embodied version, not us."

## Key Properties

- **Cumulative** — agents use CoT, CoT uses language models. Each step is non-disposable.
- **Traceable** — the next bottleneck is visible from the current step. "From where we stand now (Agent), the next bottleneck we see is continuous learning — relatively clear."
- **Non-linear past the singularity** — AI can accelerate AI research, so progress past the self-iteration step is non-linear.
- **No critical point** — explicitly framed as having no singularity; "it's a continuous process."

## What is NOT on the Roadmap

Liang explicitly excludes from the intelligence main line at this stage:

- **World models** — "many things can be called world models, the meaning is unclear"; not the most important thing at this stage
- **Video generation** — "good business, but has no relationship to the intelligence roadmap"; Sora-style video gen was a fad that small companies later cut
- **3D generation** — not on the intelligence main line

These may be good businesses, but DeepSeek does not pursue them: "We only do something if it is on the intelligence roadmap."

## Significance

The staircase is presented as DeepSeek's internal roadmap, not the only possible roadmap. Liang explicitly notes "everyone's view is different, no right or wrong." However, it shapes DeepSeek's resource allocation:

- Research investment goes to the next bottleneck (continuous learning) rather than to world models or video
- "Comfortable" cadence: agents and language-model scaling continue in parallel with continuous-learning research
- Embodied AI deferred until after self-iteration is solved — "we don't need to do it; the model will do it itself"

## Related Concepts

- [[concepts/continuous-learning|Continuous Learning]] — step 4, the current frontier
- [[concepts/dspark|DSpark]] — DeepSeek's contribution to inference efficiency, supporting the agent step
- [[concepts/speculative-decoding|Speculative Decoding]] — broader family to which DSpark belongs

## Related Sources

- [[sources/liang-wenfeng-investor-exchange-meeting|Liang Wenfeng 2026: Investor Exchange Meeting]] — primary articulation of this roadmap
