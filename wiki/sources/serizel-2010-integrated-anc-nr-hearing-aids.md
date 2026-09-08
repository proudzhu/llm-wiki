---
type: source
created: 2026-09-07
updated: 2026-09-08
sources:
  - raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/full-text.md
  - https://doi.org/10.1109/TASL.2009.2030948
  - zotero://select/items/0_742FT4QW
tags:
  - active-noise-control
  - hearing-aids
  - speech-enhancement
  - noise-reduction
  - wiener-filter
  - secondary-path
  - causality
  - multi-channel
---

# Serizel, Moonen, Wouters & Jensen 2010: Integrated Active Noise Control and Noise Reduction in Hearing Aids

**Authors**: [[entities/romain-serizel|Romain Serizel]], [[entities/marc-moonen|Marc Moonen]], [[entities/jan-wouters|Jan Wouters]], [[entities/soren-holdt-jensen|Søren Holdt Jensen]]
**Institutions**: KU Leuven, ESAT-SCD & ExpORL (Belgium); Aalborg University, Dept. of Electronic Systems (Denmark)
**Venue**: IEEE Transactions on Audio, Speech, and Language Processing, vol. 18, no. 6, pp. 1137–1145, August 2010
**Type**: Journal article
**DOI**: [10.1109/TASL.2009.2030948](https://doi.org/10.1109/TASL.2009.2030948)
**Zotero**: [742FT4QW](zotero://select/items/0_742FT4QW)

## Summary

This paper presents combined active noise control (ANC) and noise reduction (NR) schemes for hearing aids with an open fitting, tackling two effects ignored by conventional NR algorithms: the noise leakage through the open fitting and the secondary path (loudspeaker → tympanic membrane) attenuation. Four combination topologies are derived — single-channel cascade, multichannel cascade, parallel, and integrated — with the integrated scheme realized as a Filtered-x Multichannel Wiener Filter (FxMWF). Experimentally, the integrated scheme delivers an almost constant intelligibility-weighted SNR improvement of ~12 dB across hearing-aid gains, versus ~4 dB for the cascaded scheme (which collapses to ~1 dB at realistic causality margins where the integrated scheme still achieves >10 dB), because the integrated filter decomposes into an NR part and an ANC part whose performance does not depend on the NR algorithmic delay.

## Problem Formulation

The signal model is the standard M-microphone NR setup: $y_m(k) = x_m(k) + v_m(k)$, with the desired signal $d(k) = x_1(k-\Delta)$ (speech component of the first microphone up to a delay $\Delta$). The classic [[concepts/multi-channel-wiener-filter|MWF]] $\mathbf{w} = \mathbf{R}_{yy}^{-1}\mathbf{r}_{yd}$ minimizes the MSE $\mathbb{E}[|d(k) - \mathbf{w}^\mathsf{T}\mathbf{y}(k)|^2]$, with correlation statistics estimated during speech-plus-noise periods and noise-only periods.

In the hearing-aid context (Fig. 1), two effects are ignored by this classic scheme:

1. **Secondary path** $S(z)$: the propagation from the hearing-aid loudspeaker to the tympanic membrane (including the loudspeaker response). Its dc gain is lower than 1, so the power of the processed signal is *decreased* on its way to the eardrum.
2. **[[concepts/open-fitting-noise-leakage|Noise leakage]]** $u(k)$: ambient sound entering the ear canal directly through the open fitting (no earmold). This signal is not processed at all, so its SNR is generally *lower* than that of the hearing-aid output.

The signal actually reaching the tympanic membrane is therefore the secondary-path-filtered, amplified NR output *plus* the unprocessed leakage. For the small amplification gains typical of open fittings, the leakage (with its low SNR) can override the action of the NR processing and partly cancel the achieved SNR improvement — a degradation that grows when the secondary-path attenuation is combined with the leakage.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p02-001.png|Multichannel noise reduction system in the hearing aids context]]

*Figure 1: Multichannel noise reduction system in the hearing aids context — MWF-based NR followed by gain g and secondary path S to the tympanic membrane, with unprocessed leakage u added at the eardrum.*

To cancel the noise component of the leakage, feedforward ANC is applied at the tympanic membrane. All proposed systems assume a microphone in the ear canal providing an error signal (commercial hearing aids lack this, but it is technically possible to place one on the eartip). Crucially, only the *noise* component of the leakage is canceled — its speech component is preserved, since it provides localization cues.

## Methodology

### A. NR + Single-Channel ANC in Cascade (Fig. 2)

The most straightforward combination feeds the NR output into a single-channel filtered-x ANC controller. Two structural problems arise:

- The ANC needs an input with a *strong* noise component to synthesize anti-noise, but the NR output is precisely the signal whose noise has been suppressed — with a near-perfect NR the ANC input vanishes and the ANC performs poorly.
- The NR delay $\Delta$ (typically half the NR filter length) is added to the system latency, eating the causality margin available to the ANC.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p03-002.png|Multichannel noise reduction and single-channel active noise control systems in cascade]]

*Figure 2: Multichannel noise reduction and single-channel active noise control systems in cascade.*

### B. NR + Multichannel ANC in Cascade (Fig. 3)

Using the *per-channel filtered microphone signals* (the MWF partial outputs before summation) as the multichannel ANC input fixes the first problem: these signals have a significantly larger noise component than the NR sum output. The reference signals are filtered through the estimated secondary path $\hat{S}$ (filtered-x), and the upper branch applies $g\,\hat{S}$ rather than $g\,I$, so the criterion also compensates the secondary path on the desired speech.

Because the filter must now be updated during both noise-only and speech-plus-noise periods, standard gradient-based ANC adaptation is inconvenient; the filters are instead computed in closed form from estimated second-order statistics (MWF-style): $\mathbf{w} = \mathbf{R}_{\hat{y}\hat{y}}^{-1}\mathbf{r}_{\hat{y}d}$, where $\hat{\mathbf{y}}$ collects the filtered reference signals.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p04-003.png|Multichannel noise reduction and active noise control systems in cascade]]

*Figure 3: Multichannel noise reduction and active noise control systems in cascade — the ANC inputs are the per-channel MWF partial outputs rather than the NR sum.*

A remaining structural weakness: the ANC input and the secondary-path-cancellation reference are the same signals, while ideally the ANC wants noise-rich inputs and the secondary-path compensation wants the clean speech estimate.

### C. ANC and NR in Parallel (Fig. 4)

Putting the two functional blocks in parallel decouples them: an MWF branch performs NR while a multichannel ANC branch (also compensating the secondary path) minimizes the noise sound pressure at the tympanic membrane. The secondary-path-compensation reference is now the amplified speech estimate, not the noise-rich ANC input.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p06-004.png|Active noise control and noise reduction system in parallel]]

*Figure 4: Active noise control and noise reduction system in parallel.*

### D. Integrated ANC + NR: Filtered-x MWF (Fig. 5)

The final step merges both functions into a *single* set of adaptive filters — the [[concepts/filtered-x-mwf|Filtered-x Multichannel Wiener Filter (FxMWF)]]. Each microphone signal is pre-filtered by the secondary-path estimate $\hat{S}$ to form filtered references $\hat{\mathbf{y}}$, and the MSE criterion is defined on the signal reaching the tympanic membrane (not the loudspeaker input). The criterion decomposes into a secondary-path-compensation term on the speech component and an ANC term on the noise at the tympanic membrane, so the single optimal filter

$$\mathbf{w}_{\text{FxMWF}} = \mathbf{R}_{\hat{y}\hat{y}}^{-1}\,\mathbf{r}_{\hat{y}d}$$

simultaneously performs NR (with the secondary path taken into account) and ANC (canceling the leakage noise). Speech-plus-noise statistics feed the speech correlation; noise-only periods supply the noise statistics. This is the paper's central algorithm; see the concept page for the full derivation.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p06-005.png|Integrated multichannel active noise control and noise reduction system]]

*Figure 5: Integrated multichannel active noise control and noise reduction system — a single filter set (FxMWF) on secondary-path-filtered references performs NR and ANC jointly.*

## Robustness to Causality

Feedforward ANC requires the acoustic delay from the noise source to the ear-canal microphone to exceed the sum of: the source-to-reference-microphone delay, the hearing-aid processing delay, the algorithmic delay, and the secondary-path acoustic delay. The surplus is the **degree of causality** $\nu$ (expressed in samples). The bandwidth of good ANC performance shrinks with $\nu$, and once the criterion is violated the ANC efficiency vanishes quickly.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p07-011.png|Delays in hearing aid system environment]]

*Figure 6: Delays in hearing aid system environment — the causality margin is the difference between the noise-to-eardrum acoustic delay and the sum of reference, processing, algorithmic, and secondary-path delays.*

In hearing aids the microphone–loudspeaker distance is a few centimeters, leaving only a few tens of microseconds — a few samples at standard sampling rates.

- **Cascaded schemes**: the NR delay $\Delta = L/2$ (32 samples in the experiments) must fit inside the causality margin, forcing an impossible trade-off between NR performance (long filter) and ANC causality (short delay). In realistic scenarios no satisfying trade-off may exist.
- **Integrated scheme**: under the speech–noise uncorrelatedness assumption, the FxMWF decomposes as $\mathbf{w} = \mathbf{w}^{\parallel} + \mathbf{w}^{\perp}$, where $\mathbf{w}^{\parallel}$ is an NR filter (also compensating the secondary path) and $\mathbf{w}^{\perp}$ an ANC filter canceling the leakage noise. The ANC part does **not** depend on the NR delay $\Delta$, so there is no performance trade-off: the only requirement is that the overall system remain causal.

## Experimental Setup

| Item | Value |
|------|-------|
| Setup | Manikin head + torso with artificial ears; two-microphone BTE hearing aid worn on left ear |
| Error signal | Artificial-ear eardrum microphone (standing in for the ear-canal microphone) |
| Speech source | 0°, three HINT sentences + silence periods, 22 s total |
| Noise source | 270°, multitalker babble (Auditec) |
| Sampling rate | 16 kHz |
| NR filter | Length $L$ with delay $\Delta = L/2 = 32$ samples |
| Secondary path | Estimated offline via NLMS identification |
| Gain $g$ | 0–20 dB (calibrated so that at 0 dB the leakage and loudspeaker signals have equal power for a 0° source) |
| Reference SNR | Leakage SNR = 1.3 dB (input SNR 5 dB) |
| Metric | Intelligibility-weighted SNR improvement (Greenberg et al. 1993 band-importance weighting, ANSI S3.5) |
| Causality | Degree of causality $\nu$ swept from −16 to 48; realistic value $\nu = 2$ samples (measured for the 270° noise DOA) |

## Results

**Leakage and secondary-path effects (Fig. 7).** With leakage only, the degradation of MWF-NR remains small down to gains of 10 dB. With *both* leakage and secondary path, degradations are significant for gains up to at least 20 dB — confirming that leakage cancellation is needed at the small gains typical of open fittings.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p08-006.png|Performance comparison for a Multichannel Wiener Filter noise reduction scheme depending on leakage and secondary path]]

*Figure 7: Performance of the MWF NR scheme depending on leakage and secondary path, as a function of amplification gain.*

**Relaxed causality, $\nu = 48$ (Fig. 8).** With enough causality margin for any processing: the cascaded scheme maintains ~4 dB SNR improvement for gains up to 15 dB (converging to NR-alone above); the integrated scheme achieves an almost constant ~12 dB improvement for all gains.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p08-007.png|Performance comparison for noise reduction scheme with or without active noise control, ν = 48]]

*Figure 8: Performance comparison for NR alone, cascaded NR+ANC, and integrated NR+ANC at degree of causality ν = 48.*

**Causality sweep (Fig. 9).** As $\nu$ drops below the NR delay (32 samples), the cascaded scheme's ANC becomes non-causal and its improvement decays to the NR-alone level. The integrated scheme keeps an almost constant improvement as long as the overall system is causal.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p09-008.png|Performance depending on the degree of non-causality]]

*Figure 9: SNR improvement versus degree of causality for the three algorithms — the cascade collapses below ν = 32 (the NR delay); the integrated scheme is flat while causal.*

**Realistic causality, $\nu = 2$ (Fig. 10).** The cascade yields only ~1 dB over standard NR at low gains (performances converge as gain rises); the integrated scheme maintains >10 dB — the practical case for hearing aids.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p09-009.png|Performance comparison for noise reduction scheme with or without active noise control, ν = 2]]

*Figure 10: Performance comparison at the realistic degree of causality ν = 2.*

**Non-causal regime, $\nu = -16$ (Fig. 11).** Even when the system is non-causal, the integrated approach outperforms standard NR — but here the improvement is mainly due to the secondary-path compensation: an FxMWF variant *without* ANC achieves similar performance. (The ANC contribution vanishes in the non-causal regime; the secondary-path-aware NR does not.)

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p09-010.png|Performance for a non-causal system, ν = −16]]

*Figure 11: Performance for a non-causal system (ν = −16): integrated scheme vs. NR only vs. FxMWF without ANC — the residual benefit is secondary-path compensation.*

## Key Contributions

1. **Leakage + secondary-path analysis**: quantifies how the open-fitting leakage and the secondary-path attenuation — both ignored by conventional MWF-based NR — degrade the SNR at the tympanic membrane, significantly for gains up to at least 20 dB when combined.
2. **Topology taxonomy for ANC + NR**: derives and compares four ways of combining the two functional blocks (single-channel cascade, multichannel cascade, parallel, integrated), showing why the cascade couples an ANC that wants noise-rich inputs with an NR that removes them.
3. **FxMWF algorithm**: a filtered-x Multichannel Wiener Filter that integrates NR and ANC into a single filter set computed from second-order statistics, with the secondary path included in the NR computation so that the minimized error is the difference between the desired signal and the signal actually reaching the tympanic membrane.
4. **Causality decoupling result**: proves (via the $\mathbf{w} = \mathbf{w}^{\parallel} + \mathbf{w}^{\perp}$ decomposition) that the integrated scheme's ANC part is independent of the NR algorithmic delay — eliminating the NR/ANC performance trade-off that cripples cascaded schemes in the few-sample causality margin of real hearing aids.
5. **Experimental validation**: on manikin acoustic-path measurements, the integrated scheme delivers ~12 dB intelligibility-weighted SNR improvement (vs. ~4 dB cascade at $\nu = 48$; >10 dB vs. ~1 dB cascade at the realistic $\nu = 2$), and still outperforms NR in the non-causal regime via secondary-path compensation.

## Limitations and Caveats

- All schemes assume an **ear-canal error microphone**, which commercial hearing aids do not have; adding one raises unresolved issues such as bone conduction into the microphone when the user speaks.
- Evaluation is simulation-only, on measured manikin transfer functions, with a single noise type (multitalker babble) and a single noise DOA (270°).
- The paper cancels only the noise component of the leakage; the schemes can be modified to cancel the full leakage, but localization cues carried by the leakage speech are then lost.
- ANC benefit vanishes once the overall system is non-causal; only the secondary-path-compensation benefit survives (Fig. 11).

## Related Concepts

- [[concepts/filtered-x-mwf|Filtered-x MWF (FxMWF)]] — the paper's central algorithm
- [[concepts/open-fitting-noise-leakage|Open-Fitting Noise Leakage]] — the problem the ANC branch addresses
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — gradient-based counterpart; FxMWF replaces gradient adaptation with closed-form second-order-statistics solutions
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/causality|Causality in ANC]] — degree of causality, hearing-aid latency margins
- [[concepts/secondary-path-modeling|Secondary Path Modeling]] — offline NLMS estimation; hearing-aid secondary path (loudspeaker → tympanic membrane)
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/ear-canal-occlusion-effect|Ear-Canal Occlusion Effect]] — the comfort motivation for open fittings

## Related Sources

- [[sources/xiao-2023-spatially-selective-anc|Xiao 2023: Spatially Selective Active Noise Control Systems]] — evaluates the FxMWF-style partially coupled configuration against constraint-based spatially selective ANC on identical hardware

## Related Synthesis

- [[synthesis/application-specific-anc|Application-Specific ANC]] — hearing aids as an ANC application with extreme causality constraints
