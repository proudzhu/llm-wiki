---
type: concept
created: 2026-11-22
updated: 2026-11-22
sources:
  - raw/papers/dang-2022-dpt-fsnet/full-text.md
tags:
  - speech-enhancement
  - subband
  - architecture
  - deep-learning
---

# Full-Band and Sub-Band Fusion

**Full-band and sub-band fusion** is a speech-enhancement modeling paradigm combining two complementary views of the spectrogram: **sub-band** processing models the temporal evolution within each narrow frequency band (local spectral patterns differ across bands), while **full-band** processing models cross-frequency structure within each frame (harmonic and global spectral context). Introduced for real-time SE by **FullSubNet** (Hao, Su, Horaud & Li, ICASSP 2021) as explicit full-band + sub-band network branches; later designs realize the fusion in different structural forms.

## Structural Forms

| Design | Fusion mechanism |
|:-------|:-----------------|
| FullSubNet (Hao et al. 2021) | Separate full-band and sub-band model branches, fused explicitly |
| [[concepts/dpt-fsnet\|DPT-FSNet]] (Dang et al. 2022) | Inside one [[concepts/dual-path-transformer\|dual-path transformer]]: intra path = sub-band (per-bin temporal sequence), inter path = full-band (per-frame spectral sequence), alternating $B$ times |
| [[concepts/tf-gridnet\|TF-GridNet]] (Wang et al. 2023) | Alternating full-/sub-band layers with self-attention, extended to multi-channel separation with a beamforming stage |
| [[concepts/sub-band-full-band-architecture\|Sub-Band and Full-Band Architecture]] (Kuang et al. 2025) | Two-step granularity split: ERB sub-band gains (coarse envelope) then full-band deep filtering (fine suppression) |

DPT-FSNet's ablation isolates the fusion gain: with both dual-path transformers modeling sub-bands only, WB-PESQ is 3.20 on VoiceBank+DEMAND; assigning the inter path to full-band modeling raises it to 3.33 at matched parameters and complexity.

## Reverberation Advantage

Both FullSubNet and DPT-FSNet report that the fusion margin over full-band-only models is **larger on reverberant data** (DPT-FSNet on DNS: 3.53 vs NSNet's 2.37 with reverb, 3.26 vs 2.15 without). The shared explanation: the sub-band path focuses on the temporal evolution of the narrow-band spectrum, which is where reverberation manifests — making the paradigm relevant to [[concepts/dereverberation|dereverberation]] as well as denoising.

## Related Concepts

- [[concepts/dpt-fsnet|DPT-FSNet]]
- [[concepts/dual-path-transformer|Dual-Path Transformer]]
- [[concepts/tf-gridnet|TF-GridNet]]
- [[concepts/sub-band-full-band-architecture|Sub-Band and Full-Band Architecture]] — the two-step granularity-split cousin
- [[concepts/band-split-rnn|Band-Split RNN]] — non-uniform subband splits for music separation
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]]
- [[concepts/dereverberation|Dereverberation]]

## Related Sources

- [[sources/dang-2022-dpt-fsnet|Dang, Chen & Zhang 2022: DPT-FSNet]] — fusion realized inside a dual-path transformer, with the sub-band-only vs full-sub ablation