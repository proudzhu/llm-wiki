---
type: concept
created: 2026-09-06
updated: 2026-09-06
sources:
  - raw/papers/hu-2026-abse-net/full-text.md
tags:
  - binaural-speech-enhancement
  - active-noise-control
  - hearing-aids
  - open-fit
---

# Active Binaural Speech Enhancement (ABSE)

**Active Binaural Speech Enhancement (ABSE)** is a hybrid framework that integrates [[concepts/active-noise-control|active noise control]] (ANC) with binaural speech enhancement (BSE) for **open-fit hearing aids**. Open-fit (vented) hearing aids bypass the [[concepts/ear-canal-occlusion-effect|occlusion effect]] for wearing comfort, but the vent lets external noise **leak into the ear canal** ($d_L$), corrupting the enhanced signal played by the loudspeaker. In ABSE, the internal loudspeaker simultaneously plays the enhanced signal and an anti-leakage component that cancels the leakage by destructive interference.

## Problem Structure

In the STFT domain, the in-ear error signal of a binaural hearing aid is

$$e_{L}=g_{L}\cdot\bm{\hat{w}}_{L}^{H}\bm{y}+d_{L},$$

where $g_L$ is the **secondary path** (loudspeaker-to-ear-canal ATF) and $d_L$ the acoustic leakage. The leakage's interferer component degrades SINR; its target component interacts with the loudspeaker signal and produces comb-filter artifacts. The goal of ABSE is to jointly maximize speech quality and cancel $d_L$ at the ear canal, while preserving binaural spatial cues (ILD/IPD).

## Architecture Families

| Family | Mechanism | Representatives |
|---|---|---|
| Cascaded | BSE stage followed by ANC stage | FxMWF (Serizel et al. 2010) |
| Parallel | BSE and ANC operate in parallel | Sabin et al. 2024 |
| Unified optimization | BSE and ANC in one objective; closed-form + adaptive solutions | Xiao et al. 2023–2024 (spatially selective ANC) |
| Neural (error-mic-free) | DNN synthesizes the anti-leakage signal; no in-ear microphone at inference | [[concepts/abse-net\|ABSE-NET]] (Hu et al. 2026) |

Traditional ABSE methods place an **error microphone deep inside the ear canal** to provide feedback for model-driven adaptive filters — impractical because the ear canal is too narrow, making long-term wear uncomfortable. Neural approaches such as ABSE-NET remove this requirement by using the error microphone only during training.

## Related Concepts

- [[concepts/abse-net|ABSE-NET]]
- [[concepts/active-noise-control|Active Noise Control]]
- Binaural speech enhancement (see [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]] for the related distributed-processing line)
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/spatially-selective-anc|Spatially Selective ANC]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]
- [[concepts/ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]

## Related Sources

- [[sources/hu-2026-abse-net|Hu et al. 2026: ABSE-NET]]
