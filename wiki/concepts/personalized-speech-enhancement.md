---
type: concept
created: 2026-06-19
updated: 2026-06-19
tags:
  - speech-enhancement
  - speaker-adaptation
---

# Personalized Speech Enhancement (PSE)

Personalized speech enhancement (PSE) uses speaker representations to guide the enhancement process, preserving the target speaker's characteristics while suppressing interference and noise. Methods typically condition the enhancement model on speaker embeddings extracted from enrollment audio (clean or noisy). G-MaP-SE addresses the key limitation of noisy-conditioning PSE by refining noisy embeddings via GMM prior matching.

## Related Concepts

- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/prior-matching|Prior Matching]]

## Related Sources

- [[sources/zhu-2026-g-map-se-guided-speech-enhancement|G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Interspeech 2026)]]