---
type: concept
created: 2026-11-08
updated: 2026-11-08
sources:
  - wiki/sources/wu-2026-dbmif-multimodal-fusion.md
  - wiki/sources/kuang-2025-low-complexity-bc-speech-enhancement.md
tags:
  - signal-processing
  - filter-bank
  - subband
  - speech-enhancement
---

# Pseudo-QMF Bank

A **pseudo-quadrature mirror filter (PQMF)** bank is an $M$-channel analysis/synthesis filter bank that approximates perfect reconstruction with a single prototype low-pass filter modulated by cosine terms. It is the classical subband front-end of perceptual audio codecs (MPEG-1 Layer III, MP3's polyphase bank) and has re-entered speech enhancement as a cheap way to give a network a frequency axis without an STFT.

## Key Formulations

The $M$ analysis filters $h_m$ and synthesis filters $g_m$ are cosine-modulated copies of a prototype $p[n]$ of length $L$:

$$
h_m[n] = 2\,p[L-1-n]\cos\!\left[\frac{(2m+1)\pi}{2M}\left(n-\frac{L-1}{2}\right) + (-1)^m\frac{\pi}{4}\right]
$$

$$
g_m[n] = 2M\,p[n]\cos\!\left[\frac{(2m+1)\pi}{2M}\left(n-\frac{L-1}{2}\right) - (-1)^m\frac{\pi}{4}\right], \qquad 0 \le n \le L-1
$$

Analysis (per modality waveform $\mathrm{x}_c$):

$$
\mathrm{s}_{c,m}[n] = (\mathrm{x}_c * h_m)[n], \qquad m \in \{0,\dots,M-1\}
$$

Synthesis of the enhanced signal:

$$
\hat{\mathrm{y}}[n] = \sum_{m=0}^{M-1}(\hat{\mathrm{s}}_m * g_m)[n]
$$

The prototype is typically a Kaiser-windowed sinc; DBMIF uses $M = 4$ with prototype length $L = 32$ in the released code (its method section states $L = 64$ — the code was verified against the paper during ingest; see [[sources/wu-2026-dbmif-multimodal-fusion#Code Verification|the DBMIF code verification]]). "Pseudo" refers to the near-perfect-reconstruction approximation (Nguyen 1994) — aliasing between adjacent bands is cancelled by the analysis/synthesis pair rather than by ideal brick-wall filters.

## Why Use It in a Neural Enhancer

| Property | Consequence |
|:---------|:------------|
| Fixed, non-learned, linear-phase-ish decomposition | No adaptation cost; the network cannot "cheat" by re-learning a transform |
| 4 bands ⇒ 4× temporal downsampling per band at matched total sample count | Each band is a shorter, lower-rate sequence — cheaper temporal modelling at the *front end* (but with a 4-band CNN encoder-decoder the total MACs can still be several GMACs; see the DBMIF measurement below) |
| Explicit band identity | The fusion mechanism can apply a *different* modality weighting per band (see [[concepts/deep-iterative-attention-fusion|DIAF]]: BC-anchored lows, AC-anchored highs) |
| Reusable at the discriminator | The same bank decomposes real and generated speech for a [[concepts/multi-scale-discriminator|subband discriminator]], so spectral supervision is aligned with the generator's own representation |

It is the subband alternative to the STFT-based T-F domain: time-domain at the sample level, but band-structured. Compare [[concepts/oversampled-filterbank|oversampled filterbank]] for the ANC-side use of modulated filter banks, where the goal is delay-free subband adaptive filtering rather than generative modelling.

## Related Concepts

- [[concepts/sub-band-full-band-architecture|Sub-Band + Full-Band Architecture]] — the ERB-band analogue in lightweight speech enhancement
- [[concepts/oversampled-filterbank|Oversampled Filterbank]] — modulated filter banks for subband adaptive filtering
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]] — the domain it splits
- [[concepts/multi-scale-discriminator|Multi-Scale Discriminator]] — where the same bank is reused
- [[concepts/erb-scale|ERB Scale]] — perceptual (as opposed to near-uniform) band spacing

## Related Sources

- [[sources/wu-2026-dbmif-multimodal-fusion|Wu et al. 2026: DBMIF]] — 4-band PQMF front-end with per-band fusion weights and subband discriminators; released code measured at 10.41 M generator params / 2.60 GMACs/s, so the bank is cheap but does not make the *network* cheap
