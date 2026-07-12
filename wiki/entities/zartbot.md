---
type: entity
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/articles/dspark-speculative-decoding.md
  - https://mp.weixin.qq.com/s/RRHg9UCCInSc_zEcIgjNBQ
tags:
  - author
  - blogger
  - llm-inference
  - speculative-decoding
  - wechat
---

# zartbot

**zartbot** is a Chinese-language technical blogger who writes long-form, code-level walkthroughs of LLM inference and systems topics, published primarily on WeChat. The author's posts are signed "渣注" ("Slacker's note") and are characterized by:

- **Primary-source depth.** Posts typically read the original paper *and* the reference implementation, then explain both side-by-side. Code excerpts are drawn from the actual repositories (e.g., `deepspec`, `transformers`) rather than paraphrased.
- **First-principles framing.** Concepts are motivated from underlying mathematical or systems principles — e.g., deriving speculative decoding's speedup formula from first-order latency accounting, or framing draft training as optimal transport.
- **Interleaved commentary.** The author's own analysis ("渣注") is interspersed with the paper's content, flagging where the author disagrees with or extends the original framing.

## Notable Work in This Wiki

- [[sources/zartbot-2026-dspark-speculative-decoding|详细谈谈DSpark投机解码的原理 (2026-07-04)]] — a comprehensive walkthrough of [[concepts/dspark|DSpark]], set against the full six-stage history of [[concepts/speculative-decoding|speculative decoding]] from 2022 to 2026. This article is the source for the wiki's concept pages on DSpark, DFlash, EAGLE, Medusa, MTP, and tree attention.

## Topics Covered

Based on the article indexed in this wiki, zartbot's areas of focus include:

- LLM inference acceleration (speculative decoding, draft models, tree attention).
- Production serving systems (DeepSeek-V4 deployment, hardware-aware scheduling).
- The interplay between algorithmic improvements and systems-level constraints (memory bandwidth, batch capacity, throughput curves).

## References

- WeChat article: [详细谈谈DSpark投机解码的原理](https://mp.weixin.qq.com/s/RRHg9UCCInSc_zEcIgjNBQ) (2026-07-04).
- Wiki source page: [[sources/zartbot-2026-dspark-speculative-decoding|zartbot 2026]].
