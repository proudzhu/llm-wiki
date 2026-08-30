---
type: concept
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/valin-2024-fargan/full-text.md
tags:
  - pitch
  - neural-vocoder
  - speech-synthesis
  - autoregressive
  - speech-coding
---

# Pitch Prediction

**Pitch prediction** (long-term prediction) is the use of the *pitch period* to predict the current speech signal from the signal one period earlier — exploiting the fact that voiced speech is nearly periodic, so $\hat{x}(n-T)$ is an accurate prediction of $x(n)$. Classical speech coders combine it with short-term [[concepts/linear-prediction|linear prediction]] (CELP's two-stage predictor). In [[concepts/fargan|FARGAN]] ([[sources/valin-2024-fargan|Valin et al. 2024]]), pitch prediction is repurposed as an explicit **second autoregressive feedback** of a neural vocoder: rather than being learned implicitly, the network is handed the signal from one pitch period back as an input.

## Formulation

FARGAN synthesizes in subframes of $N = 40$ samples (2.5 ms at 16 kHz). The predicted signal is

$$
p(n)=\begin{cases}\hat{x}(n-T)&T\geq N\\
\hat{x}(n-2T)&\text{otherwise},\end{cases}
$$

where $\hat{x}$ is the already-synthesized history and $T$ the input pitch period. Looking back two periods when $T<N$ guarantees the lookback never overlaps the current subframe. Since the highest pitch allowed is 500 Hz ($T=32$), $T$ can never be shorter than $N/2$, so $2T \geq 64 > N$ always holds.

In FARGAN the prediction is:

- **renormalized** by the gain of the subframe where it is *used* (not where the audio was generated) — part of the model's gain normalization;
- **gated** by a voicing-dependent gate computed from the conditioning, so the prediction is not used for unvoiced speech;
- **fed to every layer** of the subframe network, not just its input.

## Why It Works

For voiced speech, samples one period back are an accurate prediction of the current subframe — the generator only has to model the *residual* between consecutive periods, exactly as CELP's adaptive codebook offloads periodicity from the fixed codebook. This concentrates network capacity on the aperiodic excitation detail, which is why the mechanism improves quality *and* reduces complexity: FARGAN's ablation shows removing pitch prediction (at equal weight count) costs 0.12 PESQ and worsens mean pitch error from 4.108 to 4.239.

The 2.5-ms subframe size is itself chosen to make optimal use of pitch prediction: with $T \geq 32$ samples, a 40-sample subframe is on the order of one pitch period, keeping the lookback local and the feedback tight.

## Limitations

Because the pitch period directly indexes the synthesis history, a pitch-predictive model presumes a single periodic source: FARGAN "cannot be easily adapted to synthesize general audio and music." The same coupling means the pitch estimate must be reliable — the voicing gate is the safeguard for unvoiced segments.

Earlier attempts to add direct pitch prediction to [[concepts/lpcnet|LPCNet]] (density-estimation training with teacher forcing) reportedly failed; FARGAN's authors attribute those failures to teacher forcing, since the mismatch between ground-truth and synthesized history is exactly where pitch prediction is most sensitive.

## Relation to Other Pitch Features

- In [[concepts/lpcnet|LPCNet]], pitch enters only as *conditioning* (period, correlation) — the network must discover periodicity itself. FARGAN makes the pitch period an *operator* on the synthesis history.
- In [[concepts/percepnet|PercepNet]] / [[concepts/pitch-coherence|pitch coherence]], periodicity is a *feature* driving comb filtering for enhancement; FARGAN uses it for *generation*.
- CARGAN relies on the autoregressive inductive bias to learn pitch *implicitly*; FARGAN externalizes it.

## Related Concepts

- [[concepts/fargan|FARGAN]] — the vocoder built around this mechanism
- [[concepts/linear-prediction|Linear Prediction]] — the short-term counterpart in the classical two-stage predictor
- [[concepts/lpcnet|LPCNet]] — conditioning-only use of pitch; failed direct-prediction attempts
- [[concepts/pitch-coherence|Pitch Coherence]] — periodicity as a feature rather than an operator
- [[concepts/exposure-bias|Teacher Forcing and Exposure Bias]] — why pitch prediction resisted earlier integration

## Related Sources

- [[sources/valin-2024-fargan|Valin, Mustafa & Büthe 2024: FARGAN]] — introduces pitch prediction as a second autoregressive feedback
