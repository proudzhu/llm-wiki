---
type: source
created: 2026-07-24
updated: 2026-07-24
sources:
  - raw/papers/liang-wenfeng-investor-exchange-meeting/full-text.md
  - zotero://select/items/0_KI4HWLYE
tags:
  - transcript
  - investor-meeting
  - deepseek
  - agi
  - open-source
  - llm-strategy
  - china-ai
  - liang-wenfeng
---

# Liang Wenfeng 2026: Investor Exchange Meeting (Audio Transcript)

> **Source**: `raw/papers/liang-wenfeng-investor-exchange-meeting/full-text.md` (Zotero: `KI4HWLYE`)
> **Speaker**: [[entities/wenfeng-liang|Liang Wenfeng]] — Founder, [[entities/deepseek|DeepSeek]]
> **Format**: Audio recording transcript (3h 44min, ~900 lines)
> **Recording**: 2026-05-20 · **Transcription**: 2026-07-16
> **Type**: Primary source — closed-door investor exchange meeting (录音文字稿)

## Summary

This is a verbatim transcript of a closed-door investor exchange meeting with Liang Wenfeng, founder of [[entities/deepseek|DeepSeek]]. Recorded on May 20, 2026 — roughly 15 months after the Spring Festival 2025 viral moment that brought DeepSeek to global attention, and shortly after a new funding round. The transcript covers DeepSeek's vision, open-source strategy, AGI roadmap, hardware resource constraints, pricing logic, and organization culture. It is uniquely valuable as a first-person account of the strategic reasoning behind DeepSeek's unconventional choices (open-weight frontier models, "ten-month payback" API pricing, vision-driven flat organization) and as a candid assessment of the US–China compute gap.

The transcript was machine-transcribed and lightly edited by AI; the file's own preface warns that "individual proper nouns and numbers may have recognition errors — please refer to the original recording." Bracketed timestamps (e.g., `[00:11:49]`) mark audio positions.

## Speaker & Context

[[entities/wenfeng-liang|Liang Wenfeng]] (梁文锋) is the founder of [[entities/deepseek|DeepSeek]]. In this meeting he walked investors through six themes:

1. **Vision** that organizes the company and its non-conventional commercial posture
2. **AGI roadmap** — a staircase narrative from language models to embodied AI
3. **Resource gap** between China and the US, and how DeepSeek copes at a fraction of US compute
4. **Commercial logic** — pricing, open-source sustainability, the "ten-month payback / six-fold profit" benchmark
5. **Organization & culture** — no KPI, half formal work / half self-directed research, restraint as strategy
6. **Q&A** on continuous learning, coding agents, hardware depreciation, the next model (V4 follow-ups)

## Vision and Open-Source Strategy

Liang opens by stating the company was founded without the goal of "making money or going public" — the founding intent was to "do something useful for humanity with significant goodwill." He explicitly contrasts DeepSeek's open-source posture with that of 智谱 (Zhipu): "Zhipu's open-source has a feeling of being forced; for us, this is our original intent."

The strategic argument for open-source rests on three pillars:

1. **Vision requirement** — the founding vision *requires* open-source; it cannot be substituted later.
2. **AI is large enough to share** — AI may eventually capture ~10% of global GDP. "You cannot monopolize this; you must share, otherwise you will certainly not survive."
3. **Restraint as competitive moat** — restraint increases the probability of reaching AGI. Open-source is one expression of restraint. See [[concepts/restraint-as-strategy|Restraint as Strategy]].

Liang explicitly states DeepSeek will continue to open-source, including its strongest models: "I don't see what inevitable benefit closed-source brings. Bytedance's models are closed — what benefit does it have? I don't see any." He notes the deployment barrier is high enough that even with full open-weight release, third parties cannot easily match DeepSeek's deployment cost.

## AGI Roadmap: The Staircase

Liang presents a distinctive "staircase" narrative of how intelligence progresses — each step built on the previous, none disposable. See [[concepts/agi-roadmap-staircase|AGI Roadmap Staircase]] for the full staircase.

1. **Language models (GPT)** — the foundation; no observed upper limit on scaling
2. **Chain-of-Thought (CoT)** — already exceeds top humans on competition math and coding; plateaued without reaching AGI
3. **Agents** — current frontier (2026); will solve all problems solvable by agents, then plateau
4. **Continuous learning** — the next bottleneck, currently unsolved globally; "not one technique but a problem." See [[concepts/continuous-learning|Continuous Learning]].
5. **Self-iterating singularity** — after continuous learning, the model develops its own next version; "not really a singularity, but a long gradual process"
6. **Embodied AI** — last, only after the model can self-iterate; doing embodied first is "the hard route"

He explicitly distances DeepSeek from **world models** and **video generation** as not on the intelligence main line at this stage, while acknowledging they are good businesses. "If we are not on the intelligence main line, we don't do it" — including 3D, video, world models.

## Resource Constraints: The US–China Compute Gap

The most concrete numbers in the transcript concern compute:

- DeepSeek currently has ~20k H-equivalent cards, "most of which arrived in the last one or two months"
- A new round of funding is being aggressively spent on cards: "If I can spend it all in half a year, that would be the ideal"
- Huawei 950 allocation from Huawei: ~16k cards (publicly disclosable), equivalent to ~4k B-series cards — "not enough to train the next-generation model, only the current one"
- The US trains models with ~800B activated parameters; China's largest is "in the tens of B" — a ~10x gap
- Training an 800B-activation model would require ~50k GB300 OR ~200k Huawei 950 cards — "we cannot afford this, even spending all 500B [RMB]"

Liang frames the gap as **a resource gap, not a talent gap**:

- "The talent gap is essentially also caused by the compute gap — fewer experiments, less talent development."
- "People are not the bottleneck; resources are."
- Target narrative: "behind the US by 1–2 years, but using 1/20 of their compute" — with the ambition to compress that lag to 6 or 3 months at single-digit-fraction compute.

Domestic hardware (Huawei) is described as ~2 years behind Nvidia and more power-hungry — Huawei cards depreciate over 3 years vs. 5 for Nvidia — but Liang is "optimistic" that in 5 years China will not still be stuck on the production-capacity problem.

## Pricing Logic and the "Ten-Month Payback" Benchmark

DeepSeek's API pricing follows a distinctive internal benchmark: **the price at which the hardware cost is recovered in 10 months**.

- Roughly corresponds to a **6× profit margin** over hardware cost
- Applied uniformly to V3.2 Flash, V4, etc.
- "If we wanted 100× profit, open-source would hurt us — at 6×, it doesn't"
- Demand is price-inelastic at this point: lowering further would not increase usage meaningfully
- Liang notes this is "not profit-maximizing; if it were, we'd price higher"

The pricing is one expression of [[concepts/restraint-as-strategy|restraint as strategy]]: in a market as large as AI, the player willing to take less profit wins. "OpenAI thinks they can monopolize the world, but they will face challengers — including Chinese players willing to take less." The floor is set by viability, the ceiling by competition.

## Organization and Culture

The management philosophy is unusual and explicitly contrasted with conventional commercial companies:

- **No formal organization structure** — "We have no organization; we are organized by vision"
- **No KPI, no考核 (appraisal)** — only the vision, which is not even written down
- **Two-track work split**: bottom-up (each person chooses what to work on) + top-down (formal cross-team projects like V4 release); "formal should not exceed half of an employee's time"
- **Minimal overtime** — explicitly for two reasons: research needs a relaxed environment, and the company's restraint means "there is less to do"
- **"A group of ordinary people doing extraordinary things"** — Liang frames the team as "random ordinary people," not "geniuses"
- **Bell Labs is not the model** — "We are different; we must commercialize. The government will not give us a cent."

The single core interest / risk is named: **team stability**. "As long as everyone doesn't leave, we can definitely make AGI. Money, resources, other factors are easy to obtain. The only non-negotiable is team stability." The recent funding round (with sizable employee options) is described as the largest mitigation of this risk.

## Key Quotes

> "AI 这个事情太⼤了，利益太⼤了。我们⾮常克制，只要能够做成，最后利益都会⾮常⼤。你随便分⼀点，利益就⾮常⼤，所以现在根本不⽤考虑拿这⾥⾯的哪⼀部分利益、怎么拿"

> "我们并没有⽐别⼈有钱，也没有说我们⼈员⽐其他公司更好，其实没有的...我们就是⼀群⾮常平凡的⼈"

> "我们跟美国的差距主要是资源上⾯，然后⼈上⾯差距不是很⼤的。⼈上⾯⼏乎没有差距"

> "你愿景是拿得多，你就先输了，你就会⾯临着更⼤的困难。这个世界就是这样"

> "AI 可以加速 AI 的研究...它不是线性的"

## Q&A Highlights

- **Continuous learning** — not a technique but a problem; many candidate methods, none yet working; "the whole world is still in the exploration stage." See [[concepts/continuous-learning|Continuous Learning]].
- **Coding agent** — the highest-priority vertical for DeepSeek right now; financial / medical / legal verticals are lower priority. Coding is the universal substrate.
- **Hallucination** — a post-training-solvable problem, currently a "product problem" rather than a research priority.
- **Data labeling** — ~half of DeepSeek's core researchers spend time on data labeling; high-quality data labeling is "extremely expensive" — China has no cost advantage here. The bottleneck is time, not capital.
- **Next model** — comfortable cadence is one release every 2–3 months; V4 (current) is "still rough"; next at ~50B activation will not differ much from open-source peers; ~150B activation model targeted for "end of this year, optimistically" — far from O-series scale.
- **TileLang** — DeepSeek is replacing CUDA with TileLang (a higher-level language): "significantly improves efficiency, only 1–2% loss, and we are using AI to write TileLang."
- **US–China gap** — 12–18 months behind on AI; possibly "this year can match foreign models" on the current paradigm — but this is not AGI.
- **Recursive self-improvement** — addressed as the same problem as continuous learning; not a separate technique.

## Key Contributions

This is a primary-source document; its "contributions" are direct disclosures rather than research results:

1. **Strategic reasoning for open-weight frontier models** — the most explicit first-person account of why DeepSeek open-sources its strongest models, framed as both vision and commercial strategy
2. **AGI staircase roadmap** — a distinctive narrative of how intelligence progresses from language models to embodied AI, with each step building on the previous
3. **The "ten-month payback / 6× profit" pricing benchmark** — a concrete formula tying API pricing to hardware depreciation
4. **US–China compute gap quantification** — concrete numbers (~20k H-equivalent, 16k Huawei 950, 800B vs. tens-of-B activation gap)
5. **Vision-driven organization philosophy** — no KPI, no formal structure, half formal / half self-directed research time; explicitly distinguished from Bell Labs

## Related Concepts

- [[concepts/agi-roadmap-staircase|AGI Roadmap Staircase]] — Liang's staircase narrative
- [[concepts/continuous-learning|Continuous Learning]] — the next AI bottleneck per Liang
- [[concepts/restraint-as-strategy|Restraint as Strategy]] — the commercial argument for open-source + low-margin pricing
- [[concepts/speculative-decoding|Speculative Decoding]] — DeepSeek's prior open-source contribution (DSpark)
- [[concepts/dspark|DSpark]] — DeepSeek's production speculative decoding framework

## Related Synthesis

(None — existing synthesis pages focus on audio/speech signal processing, not LLM strategy.)
