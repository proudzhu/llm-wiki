---
type: concept
created: 2026-08-15
updated: 2026-11-11
sources:
  - raw/papers/lugo-2026-diffvqe/full-text.md
  - raw/papers/shetu-2026-generative-discriminative-comparison/full-text.md
  - raw/papers/fu-2026-one-model-many-latencies/full-text.md
tags:
  - dataset
  - challenge
  - speech-enhancement
---

# URGENT Challenge (Speech Enhancement)

The **URGENT (Universality, Robustness, and GeneralizatioN) Challenge** series, organized by Saijo et al., fosters *universal* speech enhancement: models that handle a broad range of speech distortions and recording conditions with one system. It embraces diverse distortion types, high data diversity, and extensive evaluation metrics, and studies language dependency, universality across more distortion types, data scalability, and training on noisy data.

Two editions so far:

- **URGENT 2024** (Interspeech 2024, Zhang et al.): first edition establishing the universality/robustness/generalizability framing.
- **URGENT 2025** (Interspeech 2025, Saijo et al.): second edition with 32 submissions; the best system was discriminative while most other competitive ones were hybrid. Findings: (i) some generative or hybrid approaches were preferred in subjective evaluations over the top discriminative model; (ii) purely generative SE models can exhibit **language dependency**.
- Its evaluation includes hallucination-oriented metrics such as the **Levenshtein phone similarity (LPS)** for detecting hallucinations in generative speech enhancement, alongside P.808/DNSMOS-type quality scoring.

## Role in DiffVQE

[[sources/lugo-2026-diffvqe|DiffVQE (Lugo et al. 2026)]] builds its training corpus from URGENT 2025 speech and noise sources, **excluding CommonVoice 19.0** (generative methods benefit from very high-quality targets) and applying the "Less is More" curation strategy (Li et al., ASRU 2025): threshold-based filtering using DNSMOS, SigMOS, UTMOS, NISQA, and SQUIM_SDR so that only high-quality speech samples are kept. DiffVQE reports the LPS hallucination metric following the URGENT 2025 evaluation framework.

## Role in Fu et al. 2026 (Latency-Flexible USE)

[[sources/fu-2026-one-model-many-latencies|Fu et al. 2026]] use the URGENT 2025 corpus as the training and evaluation basis for a **latency-universal** one-for-all model: five languages and seven sampling rates (8–48 kHz) with the seven degradation types, and the **non-blind** 1,000-utterance test set with the full metric suite (DNSMOS, NISQA, UTMOS, PESQ, ESTOI, SBERT, LPS, ASR CAcc). One deviation matters for cross-paper comparison: following the RE-USE convention, they score against **anechoic clean speech** rather than the organizers' early-reflected references, so their numbers are not directly comparable to published challenge results. They also show that the challenge's own non-causal TF-GridNet baseline (DNSMOS 2.94 / NISQA 2.89 / UTMOS 2.11) is beaten by causal configurations at 40 ms algorithmic latency, which is the point of the latency-control framing.

## Related Concepts

- [[concepts/dns-challenge|DNS Challenge]] — the other major SE challenge series (Microsoft)
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]
- [[concepts/speech-enhancement-hallucination|Speech Enhancement Hallucination]]
- [[concepts/universal-speech-enhancement|Universal Speech Enhancement]] — the task framing the challenge benchmarks

## Related Sources

- [[sources/lugo-2026-diffvqe|Lugo et al. 2026: DiffVQE]]
- [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026: Generative vs. Discriminative SE]] — applies LPS/WER/CER to characterize generative-method hallucination, corroborating the need for hallucination-oriented metrics
- [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026: One Model, Many Latencies]] — trains one latency-flexible model on the URGENT 2025 corpus; 30 configurations, 40–80 ms algorithmic latency, scored against anechoic references
