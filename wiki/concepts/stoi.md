---
type: concept
created: 2026-11-20
updated: 2026-11-22
sources:
  - raw/papers/dang-2022-dpt-fsnet/full-text.md
  - raw/papers/fu-2019-metricgan/full-text.md
  - raw/papers/fu-2020-metricgan-post-processing/full-text.md
  - raw/papers/fu-2021-metricgan-plus/full-text.md
tags:
  - evaluation-metric
  - speech-intelligibility
---

# STOI (Short-Time Objective Intelligibility)

**STOI** is an objective **intelligibility** metric for speech (Taal, Hendriks, Heusdens & Jensen, *IEEE TASLP* 2011). Unlike [[concepts/pesq|PESQ]], which measures perceived **quality**, STOI targets how much of the speech is *understood*. Its score ranges from 0 to 1, with higher better — so it is conventionally reported as a fraction (e.g. 0.768) rather than on the MOS-like scales PESQ and the composite measures use.

## Design

STOI compares short-time spectral envelopes of the degraded and clean signals after a one-third-octave band decomposition (15 bands, 0–5 kHz), removing silent/low-energy regions and clipping to a per-band normalized representation before correlating. Because it works on normalized short-time envelopes and disregards phase and overall level, it is largely invariant to gain and delay — the property that makes it a reasonable intelligibility proxy across codecs, maskers and noise types.

## What a Metric-Optimization Experiment Reveals About It

The distinguishing evidence in this wiki comes from the score-assignment experiment of [[sources/fu-2019-metricgan|Fu et al. (ICML 2019)]], which trains a generator to hit an *arbitrarily specified* STOI target. Driving the target down makes the generator remove **speech components themselves** — with a uniform-mask constraint forcing the cheapest route, "the speech components are almost removed". The same experiment with PESQ as the target instead makes the output *noisier*. Since the generator seeks the minimal-effort way to satisfy the objective, the two behaviours identify each metric's dominant sensitivity:

| Metric | Cheap way to lower the score | What that implies |
|:-------|:-----------------------------|:------------------|
| STOI | delete speech content | speech content is the only thing STOI tracks |
| PESQ | add noise | noise intrusion dominates PESQ, intelligibility does not |

This is the cleanest experimental separation of the two metrics in the corpus: STOI responds to the presence of speech, PESQ to the absence of noise.

## Caveats

- **Band-limited observation.** STOI observes roughly 0–5 kHz; it says nothing about fullband content above that (the point raised in [[sources/kim-2026-faster-enhancer|Kim 2026]] when evaluating 48 kHz models). The blind spot is not merely evaluative: [[sources/fu-2020-metricgan-post-processing|Fu et al. 2020]] observe that using STOI (or PESQ) as a MetricGAN training surrogate can *generate* high-frequency noise, since the metric cannot penalize it.
- **Scale-blind.** Like PESQ, STOI is insensitive to output-level drift — [[sources/li-2024-dbccrn|Li et al. 2024]] introduced [[concepts/scale-error|ScaleError]] precisely because PESQ/STOI/COVL miss amplitude errors that clip in playback.
- **Intelligibility ≠ pleasantness.** A signal can gain STOI while sounding unnatural; the AB tests in [[sources/pascual-2017-segan|Pascual 2017]]-style evaluations and the quality-vs-intelligibility gap in [[sources/li-2020-residual-noise-control|Li et al. 2020]] both show the two axes diverging.
- **Score inflation in the literature.** VoiceBank+DEMAND systems routinely report STOI 0.93–0.95, a range in which differences are numerically tiny but perceptually meaningful; the benchmark's headroom above 0.95 is small.

## Related Concepts

- [[concepts/pesq|PESQ]] — the quality metric STOI is usually reported alongside, and the one it empirically separates from
- [[concepts/voicebank-demand|VoiceBank+DEMAND]] — the benchmark where STOI is most reported
- [[concepts/scale-error|ScaleError]]
- [[concepts/black-box-metric-optimization|Black-Box Metric Score Optimization]] — the framing that made the STOI/PESQ sensitivity contrast measurable
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN]] — the score-assignment experiment separating STOI's speech-content sensitivity from PESQ's noise sensitivity
- [[sources/kim-2026-faster-enhancer|Kim 2026: faster-enhancer.c]] — STOI's 0–5 kHz observation band as a fullband-evaluation caveat
- [[sources/li-2024-dbccrn|Li, Sun, Zhang & Van hamme 2024: DBCCRN]] — STOI's blindness to output-scale drift
- [[sources/dang-2022-dpt-fsnet|Dang, Chen & Zhang 2022: DPT-FSNet]] — near-ceiling data point: STOI 0.96 on VoiceBank+DEMAND, 95.23% (with reverb) / 97.68% (no reverb) on DNS 2020
- [[sources/fu-2020-metricgan-post-processing|Fu et al. 2020: MetricGAN Post-Processing]] — STOI's band limit as a *training* hazard: surrogate fine-tuning can generate high-frequency noise the metric ignores; STOI still rises 0.932 → 0.946 as a side effect of PESQ optimization
- [[sources/fu-2021-metricgan-plus|Fu et al. 2021: MetricGAN+]] — optimizes PESQ only; the STOI counterpart is separate work (iMetricGAN, Interspeech 2020), cited as evidence the metric-surrogate framework transfers across metrics
