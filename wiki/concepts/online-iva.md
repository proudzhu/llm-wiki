---
type: concept
created: 2026-10-04
updated: 2026-10-05
sources:
  - raw/papers/li-2020-online-gciva/full-text.md
  - raw/papers/goto-2022-iss-gciva/full-text.md
  - raw/papers/ueda-2024-online-joint-optimization/full-text.md
tags:
  - blind-source-separation
  - independent-vector-analysis
  - online-processing
  - speech-enhancement
---

# Online IVA

**Online IVA** refers to frame-wise, real-time updates of the [[concepts/independent-vector-analysis|IVA]] demixing matrices, as opposed to **blockwise** updates over multi-frame blocks. Online updates are preferred in low-delay scenarios (hearing aids, teleconference systems, real-time speech recognition interfaces) because estimation delay grows with block size, but they suffer from insufficient statistics — the per-frame data is far too little to estimate the IVA auxiliary statistics well. The standard resolution is the **online blockwise** scheme: compute statistics from the arrived current frame plus several past frames.

## Autoregressive Auxiliary Variables

The key mechanism, introduced for AuxIVA by Taniguchi et al. (2014, HSCMA) and adopted by [[sources/li-2020-online-gciva|Li, Koishida & Makino 2020]] for geometrically constrained IVA, is a recursion on the auxiliary weighted covariance. The blockwise statistic over the latest $L$ frames,

$$
\boldsymbol{V}_j(\omega,t) = \frac{1}{L}\sum_{\tau=t-L+1}^{t} \frac{G_R'(r_j(t))}{r_j(t)}\,\boldsymbol{x}(\omega,t)\boldsymbol{x}^{\mathsf{H}}(\omega,t),
$$

is replaced by the autoregressive recursion

$$
\boldsymbol{V}_j(\omega,t) = \alpha\,\boldsymbol{V}_j(\omega,t-L) + (1-\alpha)\,\frac{1}{L}\sum_{\tau=t-L+1}^{t} \frac{G_R'(r_j(t))}{r_j(t)}\,\boldsymbol{x}(\omega,t)\boldsymbol{x}^{\mathsf{H}}(\omega,t),
$$

with forgetting factor $0 \le \alpha < 1$ ($\alpha = 0$ recovers the blockwise version). This keeps sufficient statistics at small $L$ without retaining long observation histories: the recursion carries the past forward implicitly, so each new block costs only the summation over its own $L$ frames.

**Forgetting-factor trade-off**: a large $\alpha$ weighs long-range statistics (better for spatially fixed sources); a small $\alpha$ lets the blockwise term react quickly to source movement. In Li, Koishida & Makino 2020, $\alpha = 0.96$ with $L = 1$ worked for both stationary and moving interference.

## Properties

- Inherits the auxiliary-function (majorize-minimize) framework's stable, step-size-free updates — unlike gradient-based online ICA, no learning-rate tuning is required.
- Because only the statistics $\boldsymbol{V}_j$ depend on all observations, the online modification is confined to this single quantity; the per-row demixing updates are unchanged.
- Demonstrated real-time capability: < 16 ms per 16 ms frame for the online GCAV-IVA dual-microphone system on a desktop CPU (Intel i7-7800X).

## Inverse-Free Online Updates via ISS

The per-row update rules above (IP or VCD style) require matrix inversions per frequency, source, and iteration. Replacing them with [[concepts/iterative-source-steering|ISS]] rank-1 updates removes the inversions entirely: [[sources/goto-2022-iss-gciva|Goto, Ueda, Li, Yamada & Makino 2022]] derive online GC-AuxIVA-ISS this way (extending their offline GC-AuxIVA-ISS, [[sources/goto-2022-offline-iss-gciva|Goto et al. EUSIPCO 2022]]), keeping the autoregressive covariance recursion untouched (the ISS update operates on $\boldsymbol{W}_{fn}$, not on the statistics) and cutting the runtime of the geometrically constrained online system by 25–75% at equal enhancement quality. ISS-based online updates also handle moving sources efficiently, since only the demixing filters whose steering changed need updating (Nakashima & Ono 2022).

## From Online IVA to Online IVE and Online Joint Optimization

[[sources/ueda-2024-online-joint-optimization|Ueda et al. 2024]] extend the online paradigm along two axes. First, the separation model: **online-IVE** applies the IVE efficiency trick (a closed-form update of all noise rows $\boldsymbol{W}_{\mathrm{Z}}$ at once) to the online recursion, giving the first online algorithm for *multi-source* extraction at $O(FNM^2)$ per frame — and requiring a new block-matrix-inversion update of $\boldsymbol{W}^{-\mathsf{H}}$ because the multi-column noise-row update breaks the rank-1 inversion lemma. Second, the objective: **online-WPE×IVA/IVE** couples the separation with [[concepts/weighted-prediction-error|WPE]] dereverberation under a single forgetting-factor likelihood ([[concepts/online-joint-optimization|online joint optimization]]), where each block keeps its **own forgetting factor** — $\alpha = 0.99$ for IVE's small $M \times M$ statistics, $\beta = 0.9999$ for WPE's large $ML \times ML$ statistics. Experiments in car (RT60 ≈ 60 ms) and office (RT60 ≈ 780 ms) environments show that forcing one factor on both blocks destabilizes the optimization, sharpening the single-$\alpha$ trade-off above. The resulting system separates sources with 8 ms STFT frames at a 10.01 ms total delay, within the 12 ms in-car communication budget.

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA]]
- [[concepts/iterative-source-steering|Iterative Source Steering]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/online-joint-optimization|Online Joint Optimization (online-WPE×IVE)]]

## Related Sources

- [[sources/li-2020-online-gciva|Li, Koishida & Makino 2020: Online Directional Speech Enhancement Using Geometrically Constrained IVA]] — online GCAV-IVA (oGCAV-IVA) and online AuxIVA baseline, both using the autoregressive auxiliary-variable recursion
- [[sources/goto-2022-iss-gciva|Goto, Ueda, Li, Yamada & Makino 2022: Accelerating Online GC-IVA with Iterative Source Steering]] — inverse-free online GC-AuxIVA-ISS via ISS rank-1 updates; 25–75% runtime reduction over the VCD-based online variant
- [[sources/ueda-2024-online-joint-optimization|Ueda, Nakatani, Ikeshita, Kinoshita, Araki & Makino 2024: Blind and Spatially-Regularized Online Joint Optimization]] — derives online-IVE by endowing the IVE update rules with forgetting-factor statistics, and extends it to online joint WPE×IVE dereverberation at 8 ms frame size
