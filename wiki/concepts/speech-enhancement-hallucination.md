---
type: concept
created: 2026-09-03
updated: 2026-09-03
sources:
  - raw/papers/shetu-2026-generative-discriminative-comparison/full-text.md
tags:
  - speech-enhancement
  - generative-models
  - evaluation-metrics
  - hallucination
---

# Speech Enhancement Hallucination

**Hallucination in generative speech enhancement** occurs when a conditional generative model (GAN, diffusion, flow) produces speech content — phonemes, words, or spectral components — that is not present in the underlying clean signal, typically in conditions where the noisy observation $\mathbf{y}$ provides little usable information about the target speech.

## Evaluation Metrics

- **WER / CER**: word/character error rates of an ASR system (Whisper base, scored with JiWER) applied to enhanced speech against the clean transcript.
- **LPS (Levenshtein phoneme similarity)**: phoneme-level similarity between enhanced and clean speech, introduced for hallucination detection in generative SE (Pirklbauer et al. 2023); also the hallucination metric of the [[concepts/urgent-challenge|URGENT Challenge]] evaluation framework.

## Empirical Findings (Shetu, Habets & Brendel 2026)

- At moderate SNR ([-7,0] dB, matched conditions), all generative methods *improve* WER/CER/LPS over the noisy input — hallucination is limited: e.g., DisCoGAN and NCSN++ (GAN) reach LPS 85% ([-7,-4] dB) and 92% ([-3,0] dB), versus 55%/69% for noisy speech; GAN-based methods hallucinate less than diffusion-based methods.
- Below -7 dB SNR, hallucination metrics degrade significantly, and spectrogram inspection reveals **spurious spectral content** in generative outputs that is absent from the clean signal.
- Interpretation: conditional generative SE models rely heavily on the conditioning signal $\mathbf{y}$; when $\mathbf{y}$ is almost entirely masked by noise, the model falls back on its learned speech prior and hallucinates.

This aligns with the [[concepts/urgent-challenge|URGENT Challenge]] motivation for LPS-based hallucination scoring and with DiffVQE's reporting of LPS alongside quality metrics — hallucination is becoming a standard evaluation axis for generative SE.

## Related Concepts

- [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]]
- [[concepts/urgent-challenge|URGENT Challenge]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]
- [[concepts/one-step-generative-models|One-Step Generative Models]]

## Related Sources

- [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026: Generative vs. Discriminative SE]]
- [[sources/lugo-2026-diffvqe|Lugo et al. 2026: DiffVQE]] — reports LPS for single-step generative AEC + denoise
