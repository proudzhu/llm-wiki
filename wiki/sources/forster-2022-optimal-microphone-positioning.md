---
type: source
created: 2026-10-31
updated: 2026-10-31
sources:
  - raw/papers/forster-2022-optimal-microphone-positioning/full-text.txt
  - zotero://select/items/0_2CN4IR2F
tags:
  - active-noise-control
  - feedforward-anc
  - headphones
  - multi-channel
  - microphone-positioning
  - direction-of-arrival
---

# Forster, Fabry & Jax 2022: Optimal Microphone Positioning for Multi-Channel Feedforward ANC Headphones

**Authors**: [[entities/jonas-forster|Jonas Forster]], [[entities/johannes-fabry|Johannes Fabry]], [[entities/peter-jax|Peter Jax]]

**Institutions**: RWTH Aachen University, Institute of Communication Systems; Elevear GmbH

**Venue**: DAGA 2022 — 48th German Annual Conference on Acoustics, Stuttgart, Germany

**Year**: 2022 | **Type**: Conference Paper (4 pages)

**Zotero**: [2CN4IR2F](zotero://select/items/0_2CN4IR2F)

## Summary

This paper addresses where to place reference microphones on a headphone shell for multi-channel feedforward ANC. The authors propose a causality-aware **MSE time-domain cost function (MSE-TD CF)** — a path-based multi-channel Wiener formulation for an approximated diffuse sound field — as an evaluation criterion, contrasting it with the frequency-domain multiple coherence function (MCF), which bounds performance but ignores causality. Equipping a Bose QC25 with 10 additional MEMS microphones and using a greedy selection algorithm over measured device-related impulse responses (5° azimuth resolution), they find that ipsilateral reference microphones add roughly 9 dB of active gain over the conventional single-channel system, while contralateral microphones contribute almost nothing under the causal criterion because their useful filters would be acausal.

## Problem Formulation

The system is a **multiple-input single-output (MISO) feedforward ANC** headphone: $J$ reference microphones on the shell, one internal error microphone, one loudspeaker. An external noise source at azimuth $\theta$ emits $X_{\mathrm{src}}(z)$, which reaches the reference microphones via acoustic paths $Q_{\mathrm{ext},a,j}(z,\theta)$ and the error microphone via $Q_{\mathrm{int},a}(z,\theta)$; the secondary path from loudspeaker to error microphone is $S_a(z)$. Including the transducer and converter characteristics, the DSP-visible paths are $Q_{\mathrm{ext},j}(z,\theta)$, $Q_{\mathrm{int}}(z,\theta)$, and $S(z)$.

The feedforward system aims to minimize the error signal

$$
E(\theta) = X_{\mathrm{src}}\left(Q_{\mathrm{int}}(\theta) - \sum_{j \in \mathcal{J}} Q_{\mathrm{ext},j}(\theta)\, S\, W_j(\theta)\right),
$$

where $W_j(\theta)$ is the optimal (possibly acausal) directional feedforward filter for channel $j$, creating an anti-phase estimate of the disturbance $D(\theta)$ at the error microphone while accounting for the secondary path. The model deliberately depends mainly on direction of arrival — fit-induced variations of $S$ and $Q_{\mathrm{int}}$ (as in [[concepts/secondary-path-variability|Secondary Path Variability]]) are set aside to keep the focus on spatial exploitation.

**Maximum achievable performance** is given by the ratio of error-mic PSD with filtering $\Phi_{ee}$ to the PSD without filtering $\Phi_{dd}$:

$$
\frac{\Phi_{ee}}{\Phi_{dd}} = 1 - \frac{\Phi_{ud}^{H} \Phi_{uu}^{-1} \Phi_{ud}}{\Phi_{dd}} = 1 - \eta_{ud}^2,
$$

where $\Phi_{uu} \in \mathbb{R}^{J \times J}$ is the matrix of cross-PSDs between all reference microphones, $\Phi_{ud} \in \mathbb{R}^{J \times 1}$ the vector of cross-PSDs between each reference microphone and the error microphone, and $\eta_{ud}^2$ the [[concepts/multiple-coherence-function|Multiple Coherence Function (MCF)]] — the theoretical upper bound. To maximize the MCF, any additional reference microphone should be correlated as little as possible with all previous reference microphones but as much as possible with the error microphone. Crucially, the MCF is derived in the frequency domain and **does not account for causality** — the gap this paper fills.

## Methodology

### From Signal-Based to Path-Based Cost Function

An approximated diffuse field is modeled as $M$ mutually uncorrelated white Gaussian noise sources in a horizontal ring around the headphone. With the filtered reference $r_j(n) = u_j(n) * s(n)$, the error signal in vector notation is

$$
\mathbf{e} = \mathbf{d} - \sum_{j \in \mathcal{J}} \mathbf{r}_j \tilde{\mathbf{w}}_j \in \mathbb{R}^{L_{wr}},
$$

with the time-invariant MISO feedforward filter $\tilde{\mathbf{w}}_j \in \mathbb{R}^{L_w}$ and $L_{wr} = L_w + L_r - 1$. Minimizing the cost

$$
C = \left\| \mathbf{d} - \sum_{j \in \mathcal{J}} \mathbf{r}_j \tilde{\mathbf{w}}_j \right\|^2
$$

yields the recursive (Gauss–Jordan-solvable) multi-channel Wiener solution per channel:

$$
\tilde{\mathbf{w}}_j = \left( \mathbf{r}_j^T \mathbf{r}_j \right)^{-1} \left( \mathbf{r}_j^T \mathbf{d} - \mathbf{r}_j^T \sum_{\nu \in \mathcal{J} \setminus j} \mathbf{r}_\nu \tilde{\mathbf{w}}_\nu \right).
$$

The key step: under uncorrelated-WGN sources, the correlation matrix entries $\phi_{r_j r_\nu}(\lambda)$ reduce to sums of **impulse correlations between the modified secondary paths** $\tilde{s}_j(n,\theta_m) = q_{\mathrm{ext},j}(n,\theta_m) * s(n)$ — no diffuse-field microphone-signal measurements are needed. The cost function becomes purely **path-based**:

$$
C = \sum_{m=1}^{M} \left\| q_{\mathrm{int}}(\theta_m) - \sum_{j \in \mathcal{J}} \tilde{\mathbf{s}}_j(\theta_m) \tilde{\mathbf{w}}_j \right\|^2.
$$

This is the **MSE-TD CF** (see [[concepts/mse-td-cost-function|MSE-TD Cost Function]]). Instead of measuring microphone signals in a diffuse field, it suffices to measure the individual paths for a sufficiently large number of DoAs in an audio lab or (semi-)anechoic chamber. The formulation is similar to Elliott & Cheer's frequency-domain result for local active control with remote sensors (JASA 2015), but derived here in the time domain — which is exactly what makes the resulting FIR filter coefficients **causal**, in contrast to the MCF.

### Greedy Microphone Selection

A brute-force search over $p$-channel subsets of $J$ reference microphones costs $O_{\mathrm{bf}}(p) = \binom{J}{p}$ cost-function evaluations per subset size (reaching ~1000 evaluations for $J = 12$). The authors' **greedy algorithm** initializes with the set of all available microphones $\mathcal{J}$ and target count $P$: in step $p$, it evaluates each remaining candidate alone (appended to the already-chosen set $\mathcal{P}$), picks the best by the cost function, moves it from $\mathcal{J}$ to $\mathcal{P}$, and repeats — only $O_{\mathrm{greedy}}(p) = J - p$ evaluations per step. Greedy is not optimal (the best-performing chain can differ), but in their investigations the difference stayed below 1 dB in terms of the active-gain metric.

### Evaluation Criteria

Both criteria are compared on the **one-third-octave-band-smoothed active gain** over bands $\kappa$ from 50 to 4500 Hz:

$$
g = 10 \log_{10} \left( \frac{1}{K} \sum_{\kappa=1}^{K} \left( \frac{E(\kappa)}{D(\kappa)} \right)^2 \right) \, \mathrm{dB},
$$

with spatially uncorrelated WGN source signals as the simulated diffuse field. MCF computation uses Welch's method (8192-sample Hann window, 4096-sample overlap); the MSE-TD CF uses filter length $L_w = 1024$ samples.

## Experimental Setup

| Parameter | Value |
|---|---|
| Headphone | Bose QC25 (commercially available ANC headphone) |
| Added sensors | 10 digital MEMS microphones on the outer shell (L1–L5 ipsilateral, R1–R5 contralateral) |
| Built-in microphones | L0, R0 (used as candidates too → $J = 12$) |
| Electronics | Custom board: two ADAU1787 DSPs + USB sound card, connected via time-division multiplexing |
| Paths measured | Secondary path $S$ (once); DRIRs $Q_{\mathrm{int}}(\theta)$, $Q_{\mathrm{ext},j}(\theta)$ for all microphones |
| Azimuth resolution | 5° (turntable) |
| Environment | Audio lab per ITU-R BS.1116-2 |
| Head | HEAD acoustics HMS II.3 artificial head on turntable |
| Source | Neumann KH120A at 2 m, exponential sweeps |
| Identification | Spectral division |
| Simulated field | $M$ mutually uncorrelated WGN sources in horizontal ring (approximated diffuse field) |
| Filter length | $L_w = 1024$ samples |
| MCF spectra | Welch, 8192-sample Hann window, 4096-sample overlap |
| Evaluation band | One-third-octave bands, 50–4500 Hz |

## Results

### Microphone Selection Order (Greedy)

| Order | MSE-TD CF | MCF |
|---|---|---|
| 1–6 | L2, L3, L1, L0, L5, L4 | L2, L3, L1, L0, L5, L4 |
| 7 | R4 | R3 |
| 8 | R1 | R5 |
| 9 | R5 | R4 |
| 10 | R0 | R1 |
| 11 | R2 | R2 |
| 12 | R3 | R0 |

*Table: Selection order for both evaluation criteria. The first six picks (all ipsilateral + built-in L0) are identical; the criteria diverge exactly on the contralateral candidates.*

### Key Findings

1. **Ipsilateral microphones dominate**: the largest performance increase (~9 dB additional active gain) comes from the ipsilateral reference microphones compared to a conventional single-channel system.
2. **Single-channel performance is correlation-limited, not causality-limited**: both ECs agree closely at $P = 1$ (L2 chosen first — strongest correlation with the error microphone), indicating the one-channel case is mainly limited by correlation.
3. **MCF diverges from MSE-TD CF on contralateral microphones**: in the diffuse-field scenario, contralateral mic signals are less correlated with the previous microphones *and* less correlated with the ipsilateral error microphone, so the MCF still projects performance gains — but the corresponding filters would have to be **acausal** to contribute significantly. Under the causality-constrained MSE-TD CF, contralateral microphones add essentially nothing.
4. **Greedy picks the most distant microphone**: starting from L2, the MSE-TD CF consistently prefers the most distant remaining microphone — low cross-correlation with previous microphones while maintaining strong correlation with the error mic, in agreement with diffuse-field theory. The trend is interrupted only by the built-in L0, explained by its different microphone characteristics (vs. the added MEMS microphones).

## Key Contributions

1. **Causality-aware positioning criterion**: the MSE-TD cost function — a path-based, time-domain multi-channel Wiener formulation for an approximated diffuse field — replaces the causality-blind MCF for reference-microphone positioning, producing causal FIR coefficients that reflect practically realizable performance.
2. **Path-based measurability**: the diffuse-field cost function collapses to impulse correlations between modified secondary paths, so microphone signals in a real diffuse field never need to be measured — only per-DoA path measurements in a lab.
3. **Greedy selection algorithm**: reduces the microphone-subset search from $\binom{J}{p}$ to $J - p$ evaluations per step (relevant for computationally costly criteria), empirically within 1 dB of the brute-force optimum.
4. **First systematic multi-position study on a real headphone**: a commercially available ANC headphone (Bose QC25) equipped with 10 additional MEMS microphones, with all device-related impulse responses measured at 5° azimuth resolution.
5. **Actionable placement guidance**: ~9 dB of additional active gain is available from distributing reference microphones ipsilaterally around the shell; contralateral placement is wasted under causality — a design rule for multi-microphone ANC headphones.

## Related Concepts

- [[concepts/reference-microphone-positioning|Reference Microphone Positioning]] — the umbrella problem this paper addresses
- [[concepts/mse-td-cost-function|MSE-TD Cost Function]] — the paper's novel evaluation criterion
- [[concepts/multiple-coherence-function|Multiple Coherence Function (MCF)]] — the causality-blind upper bound used as comparison
- [[concepts/feedforward-anc|Feedforward ANC]] — the architecture being extended to multiple references
- [[concepts/multi-reference-anc|Multi-Reference ANC]] — wearable-scale instance of multi-reference feedforward ANC
- [[concepts/multi-channel-anc|Multi-Channel ANC]] — the MISO configuration
- [[concepts/causality|Causality in ANC]] — why contralateral references cannot contribute under causal filters
- [[concepts/broad-band-feedforward-anc|Broad-Band Feedforward ANC]] — single-reference coherence limit generalized by the MCF
- [[concepts/wiener-filter|Wiener Filter]] — the multi-channel causal Wiener solution at the core of the criterion
- [[concepts/device-specific-hrtf|Device-Specific HRTF (DHRTF)]] — the DRIR measurement methodology across DoAs

## Related Synthesis

- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
- [[synthesis/multichannel-anc-efficiency-and-robustness|Multichannel ANC Efficiency and Robustness]]
