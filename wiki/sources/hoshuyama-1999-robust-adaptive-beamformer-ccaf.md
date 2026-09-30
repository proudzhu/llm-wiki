---
type: source
created: 2026-09-30
updated: 2026-09-30
sources:
  - raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/full-text.md
  - https://doi.org/10.1109/78.790650
  - zotero://select/items/0_DEHT62WU
tags:
  - beamforming
  - adaptive-filtering
  - microphone-arrays
  - robust-beamforming
  - gsc
  - speech-enhancement
---

# Hoshuyama, Sugiyama & Hirano 1999: A Robust Adaptive Beamformer with a Blocking Matrix Using Constrained Adaptive Filters

**Authors**: [[entities/osamu-hoshuyama|Osamu Hoshuyama]], [[entities/akihiko-sugiyama|Akihiko Sugiyama]], [[entities/akihiro-hirano|Akihiro Hirano]]
**Affiliation**: Multimedia Signal Processing, C&C Media Research Laboratories, NEC Corporation, Kawasaki, Japan
**Venue**: IEEE Transactions on Signal Processing, vol. 47, no. 10, pp. 2677–2684, Oct. 1999
**Type**: Journal Article
**DOI**: [10.1109/78.790650](https://doi.org/10.1109/78.790650)
**Zotero**: [DEHT62WU](zotero://select/items/0_DEHT62WU)

## Summary

This paper proposes a robust adaptive microphone-array beamformer built as a [[concepts/gsc-beamformer|generalized sidelobe canceller (GSC)]] in which **both** adaptive stages are coefficient-constrained. The novelty is an [[concepts/adaptive-blocking-matrix|adaptive blocking matrix (BM)]] made of [[concepts/coefficient-constrained-adaptive-filter|coefficient-constrained adaptive filters (CCAFs)]] that each have their *individual* tap coefficients clamped to a box region $[\psi_{m,n}, \phi_{m,n}]$; the constrained region is designed so that only target signals arriving inside a user-specified angular sector are minimized at the BM outputs. Because the CCAFs are prevented from adapting to interference outside that sector, the BM tracks the target DOA over a bounded range without mistracking and — crucially — **without consuming the array's degrees of freedom for interference reduction**, so the design scales down to small arrays (4 microphones here). The second stage is a multiple-input canceller (MC) of [[concepts/norm-constrained-adaptive-filter|norm-constrained adaptive filters (NCAFs)]] (after Cox et al. 1987), which suppresses the residual [[concepts/target-signal-cancellation|target-signal cancellation]] that survives imperfect blocking. In a 0.3-s reverberation room the beamformer reaches 19 dB interference reduction (vs. 3 dB for the fixed beamformer and 9 dB for the prior norm-constrained robust beamformer) and 3.8 MOS on a five-point scale, 1.0 point above the previous robust beamformer, while tolerating up to 20° of [[concepts/steering-vector-error|target-direction error]] — a limit the user specifies through the constraint region.

## Problem Formulation

A GSC (Fig. 1) splits beamforming into three blocks:

- a **fixed beamformer (FBF)** that coherently enhances the target,
- a **blocking matrix (BM)** that is meant to cancel the target and pass only interference, producing $M$ reference signals $y_m(k)$,
- a **multiple-input canceller (MC)** that adaptively subtracts the components of $y_m(k)$ correlated with the delayed FBF output $d(k-Q)$, giving the output $z(k)$.

The GSC extracts the signal from the DOA encoded in the steering vector. With classical adaptive beamformers such as the simple Griffiths–Jim beamformer (GJBF), **[[concepts/target-signal-cancellation|target-signal cancellation]]** occurs whenever the steering vector is in error. [[concepts/steering-vector-error|Steering-vector error]] arises from microphone position error, microphone sensitivity error, reverberation, and target-direction error — and the paper argues that **target-direction error dominates in practice**, because the talker moves and the exact DOA is unknowable. The failure mechanism is specific: if any target energy leaks into the BM outputs $y_m(k)$, the MC (whose job is to minimize output power) treats it as interference and cancels the target itself.

The paper groups prior remedies into three families and identifies the cost of each:

| Family | Examples | Cost |
|:-------|:---------|:-----|
| Constraints inside the MC | leakage, noise injection, norm constraint (Cox et al. 1987) | Allowing a *large* direction error also restrains interference reduction |
| Improved spatial filters in the BM | Claesson & Nordholm 1992; Er & Cantoni 1986; Fudge & Linebarger 1995 | Consume degrees of freedom for interference reduction, or require more microphones |
| Target tracking / calibration | Er & Ng 1994; Fudge & Linebarger 1994; Affes et al. 1994 | Mistracks burst signals such as speech; requires matrix products (high computation) |

The design goal is therefore to allow a large target-direction error **without** losing degrees of freedom, without adding microphones, and without matrix operations.

## Methodology

The proposed beamformer (Fig. 2) keeps the GSC topology but makes the BM adaptive under coefficient constraints and the MC adaptive under a norm constraint.

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/0766b058ff06a2591e3577f24a9373309da8db0e3e413b60c219fa12ee9473f9.jpg|Structure of the generalized sidelobe canceller]]
*Figure 1: Structure of the generalized sidelobe canceller (FBF, blocking matrix, multiple-input canceller).*

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/156547f9dfd9b3ee4d124d34ea400c02e4b9574fad6723fe76e125a5cfadfc75.jpg|Structure of the proposed beamformer]]
*Figure 2: Structure of the proposed robust beamformer — a CCAF-based adaptive blocking matrix fed by the FBF output as a common reference signal, and a norm-constrained multiple-input canceller.*

### Adaptive Blocking Matrix with Coefficient-Constrained Adaptive Filters

Each CCAF is operated as an adaptive noise canceller whose **input is the FBF output** $d(k)$ and whose output is subtracted from a delayed microphone signal (Eqs. 1–3):

$$y_m(k) = x_m(k-P) - H_m^T(k)D(k), \qquad m = 0,\dots,M-1 \tag{1}$$

$$H_m(k) \triangleq [h_{m,0}(k), h_{m,1}(k), \dots, h_{m,N-1}(k)]^T \tag{2}$$

$$D(k) \triangleq [d(k), d(k-1), \dots, d(k-N+1)]^T \tag{3}$$

where $N$ is the CCAF length, $x_m(k)$ the $m$-th microphone signal, and $P$ a causality delay. Adaptation is NLMS **followed by a per-coefficient clamp** (Eqs. 4–5):

$$h'_{m,n} = h_{m,n}(k) + \alpha \frac{y_m(k)}{\lVert D(k) \rVert^2} d(k-n) \tag{4}$$

$$h_{m,n}(k+1) = \begin{cases} \phi_{m,n}, & h'_{m,n} > \phi_{m,n} \\ \psi_{m,n}, & h'_{m,n} < \psi_{m,n} \\ h'_{m,n}, & \text{otherwise} \end{cases} \tag{5}$$

with $\alpha$ the step size and $\phi_{m,n}$, $\psi_{m,n}$ the upper and lower limits of each coefficient. The essential idea is that **the optimal filter coefficients for target-signal minimization vary strongly with target DOA**, whereas the coefficients that would minimize *interference* do not lie in the same region. Constraining each coefficient to a box that contains the target-minimizing solutions over a chosen DOA sector therefore achieves two things at once:

1. **Bounded target tracking** — the CCAF minimization drives $y_m(k)$ to remove the target, and because the constraint region follows the target's coefficient trajectory over the sector, the BM's spatial pattern tracks the target DOA across that sector. Outside the sector the constraint makes the target-minimizing solution unreachable, so the beamformer does not mistrack onto interference. The maximum allowable target-direction error is thus **a direct user design parameter** (a ±20° sector in the paper), and if no interference falls inside the sector — the common case for microphone arrays — no mistracking occurs.
2. **No loss of degrees of freedom for interference reduction** — the CCAF cannot converge to the interference-minimizing solution, so a *large* residual interference survives at the BM outputs. That residual is exactly what the MC needs as a target-free reference: the larger the mismatch between the constrained region and the interference-minimizing coefficients, the higher the interference-reduction capability of the MC. Feeding the **FBF output** as the common reference to all CCAFs amplifies this effect, since the FBF enhances the target and therefore widens the gap between target-minimizing and interference-minimizing coefficient shapes. The paper notes that with a single microphone (no target enhancement) the two coefficient sets are nearly indistinguishable and the benefit disappears.

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/1a2f56b272de88ea79fc32ceb8a5bb28e81ac379e6c4eff3c2a8d5b0cce36f2e.jpg|CCAF coefficients for a 0-degree target]]
![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/def71ed14d8d76c17001c4a11d7cc08697722233ec4625f51bf5208a04dec2dc.jpg|CCAF coefficients for +/-10 degree targets]]
![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/69f2824fc1780d291462ecd892ad36e26769b1d5b523106abfefc2e167593076.jpg|CCAF coefficients for +/-20 degree targets]]
![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/45381ffaaad342c2eb5b4d057a88a9f7b8d0aeeeebb37c2152eeea572b6e6e49.jpg|CCAF coefficients for +/-30 degree targets]]
*Figure 3: Optimal CCAF coefficient sets for target DOAs of 0°, ±10°, ±20° and ±30°, with the dashed envelope $[\psi_n, \phi_n]$ showing the constraint region designed to allow ±20° of target-direction error. Inside the region (0°, ±10°, ±20°) the minimizer fits within the box and the target is cancelled at the BM; at ±30° the optimal coefficients fall largely outside the box, so the constraint prevents target cancellation and the target passes through to the MC.*

### Multiple-Input Canceller with Norm-Constrained Adaptive Filters

The MC (Eqs. 6–11) subtracts $L$-tap filtered BM outputs from the delayed FBF signal:

$$z(k) = d(k-Q) - \sum_{m=0}^{M-1} W_m^T(k)Y_m(k) \tag{6}$$

$$W_m(k) \triangleq [w_{m,0}(k), \dots, w_{m,L-1}(k)]^T, \qquad Y_m(k) \triangleq [y_m(k), \dots, y_m(k-L+1)]^T \tag{7,8}$$

The NCAF coefficients are updated by NLMS and then **rescaled if their total squared norm exceeds a threshold $K$** (Cox et al.'s norm constraint):

$$W'_m = W_m(k) + \beta \frac{z(k)}{\sum_{j=0}^{M-1} \lVert Y_j(k) \rVert^2} Y_m(k) \tag{9}$$

$$\Omega = \sum_{m=0}^{M-1} \lVert W'_m \rVert^2 \tag{10}$$

$$W_m(k+1) = \begin{cases} \sqrt{K/\Omega}\, W'_m, & \Omega > K \\ W'_m, & \text{otherwise} \end{cases} \tag{11}$$

The norm constraint restrains excess tap growth, which inhibits the MC from cancelling the target when target energy leaks through the BM. The authors argue this second safety net is **essential rather than optional**: complete target rejection in a reverberant room would need more than 1000 taps per CCAF, which is impractical (slow convergence, large misadjustment, high computation), and adaptation at low SIR adds misadjustment-driven leakage. A restrained MC is the cheaper guarantee.

### Adaptation-Mode Control (SIR-Dependent Gating)

The two stages adapt under **opposite** SIR conditions, in analogy to double-talk control in echo cancellation:

- **BM / CCAFs adapt during high-SIR periods.** For the BM, the target is the desired signal and interference is undesired, so high SIR gives the fastest convergence to the correct (target-minimizing) coefficients.
- **MC / NCAFs adapt during low-SIR periods.** For the MC the interference is the desired signal and the target is undesired. Adapting the MC while the target dominates would cause misadjustment of the MC coefficients, degrading interference reduction and modulating (distorting) the target.

The authors note that this is the single most consequential operational choice: controlling the MC adaptation yields better interference reduction *and* less distortion.

### Computational Complexity

All BM adaptations avoid matrix products entirely (unlike tracking/calibration methods). Multiplications in the BM and MC total roughly $MN + ML$ for filtering, plus the same order for NLMS adaptation, plus scaling in the MC. Including the FBF, the total is about **twice the norm-constrained method of Cox et al.**, i.e. a small constant factor rather than an order-of-magnitude increase.

## Experimental Setup

| Aspect | Anechoic simulation | Reverberant experiment |
|:-------|:--------------------|:-----------------------|
| Array | 4-channel equispaced broadside array, 4.1 cm spacing | 4 uncalibrated omni directional mics on a universal PCB, broadside linear array, 4.1 cm spacing |
| Sampling rate | 8 kHz | 8 kHz |
| Band | 0.3–3.7 kHz | 0.3–3.4 kHz |
| FBF | Simple delay-and-sum, $d(k) = \frac{1}{M}\sum_m x_m(k)$ (Eq. 12) | Same |
| Signals | Bandlimited Gaussian (sim. 1–2, 4); colored signal from $F(z^{-1}) = 1/(1-0.9z^{-1})$ (sim. 3) | Male speech in English (target) + white noise source ~45° off the target DOA, both at 2.0 m |
| Room | Anechoic | $T_{60} \approx 0.3$ s (small office) |
| Taps | 16 for both CCAFs and NCAFs | 16 for both |
| Parameters | $P=5$, $Q=10$, $K=10.0$, $\alpha=0.1$, $\beta=0.2$ | step sizes re-tuned: $\alpha = 0.02$ for CCAFs, $\beta = 0.004$ for NCAFs; all other parameters as above |
| Adaptation schedule | CCAFs 50 000 iterations, then NCAFs 150 000 iterations | — |
| Max allowable direction error | 20° (unless stated) | — |
| Baselines | FBF, simple GJBF, norm-constrained method (Cox et al.) | FBF, simple GJBF, norm-constrained method |
| Metrics | Normalized output power vs. DOA; sensitivity vs. frequency | Output power trajectories, interference-reduction ratio (IRR), MOS (10 non-professional subjects, single-mic = 1 / clean speech = 5 anchors) |

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/2b4998a983e96bdd8d4f86c3b6145042086c80ede085f098296c9b097ea96ac4.jpg|Equipment arrangement in experiments]]
*Figure 9: Equipment arrangement for the reverberant-room data acquisition.*

## Results

### Anechoic simulations

**Steering robustness and interference reduction (Fig. 4).** Normalized output power after convergence vs. single-signal DOA, with the target assumed at 0° and 20° allowable error. The proposed beamformer (the only method designed for a ±20° sector) simultaneously delivers robustness over the sector and **30 dB of interference reduction at $\theta = \pm 30°$** — the classical trade-off is broken because the BM's constraint, not the MC's, provides the robustness.

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/2b9e4466c6dc10219e6a06f4e58aceb6cd0ddf7eabec94f0d1610ea6c5771021.jpg|Normalized output power after convergence as a function of DOA]]
*Figure 4: Normalized output power after convergence as a function of DOA — FBF, simple GJBF, norm-constrained method, and the proposed beamformer with 20° allowable target-direction error.*

**Frequency dependence (Fig. 5).** The directivity pattern varies only weakly with frequency, making the design suitable for broadband array processing. The high-sensitivity region matches the designed sector ($-20° < \theta < 20°$) with a small sensitivity difference inside it. The one caveat: a **~3 dB ripple** in the target-signal frequency response — acceptable for speech communication and voice command, but flagged by the authors as potentially problematic for applications sensitive to frequency response, e.g. some speech recognition front-ends.

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/6c5a4a5d22ce51a2ca9b6158e6b1f549a78fdf6463525db1d3e9ef444c416cfa.jpg|Sensitivities after convergence as a function of DOA at different frequencies]]
*Figure 5: Sensitivities after convergence as a function of DOA at different frequencies.*

**SIR dependence (Fig. 6).** With the target placed 10° off the assumed DOA and the interference DOA scanned, the curves show a sharp peak at $\theta = 10°$ for sufficiently high SIR — i.e. the target is minimized at the BM precisely as designed. For **SIR above about 10 dB** (below a typical teleconferencing SIR), interference is suppressed even when it arrives *inside* the allowable target sector. When the interference arrives outside the sector, even SIR near 0 dB causes almost no problem.

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/ff7af80e4c23158fb376d7995787e31098fa11778a87986525a820095af7397b.jpg|Normalized output power after convergence as a function of DOA with different SIR's]]
*Figure 6: Normalized output power after convergence as a function of DOA with different SIRs.*

**Colored signals — the principal limitation (Fig. 7).** With a lowpass-colored target, the high-sensitivity DOA region *widens*: the allowable target-direction range depends on the target and interference spectra, because the BM's blocking capability is frequency dependent. Dominant low-frequency components are highly correlated and are easily cancelled at the BM — i.e. the BM partly absorbs a colored interference that the MC then cannot cancel. On this test the norm-constrained method's >6 dB region is 80° wide ($-40° \le \theta \le 40°$, 40° wider than its white-signal case), while the proposed method's is 48° ($-24° \le \theta \le 24°$, only 8° wider). So the proposed beamformer is degraded less by coloration, but the effect is real and is a property of the architecture rather than of tuning.

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/b1811ab8eaf9146ec77943601e38d796b013fb0ce8b492d76c8bc467c00103ec.jpg|Normalized output power after convergence as a function of DOA for a colored signal]]
*Figure 7: Normalized output power after convergence as a function of DOA for a colored signal.*

**User-specifiable robustness (Fig. 8).** Sweeping the coefficient constraints produces allowable target-direction errors of approximately **4°, 6°, 9°, 12°, 16° and 20°** — direct evidence that the robustness/aggressiveness trade-off is a design knob exposed to the user, not an emergent property.

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/905fdfd88979e83e0fa727d3f7d5172426509be5b8f0385126ed3da4f117c795.jpg|Normalized output power after convergence for different allowable target directions]]
*Figure 8: Normalized output power after convergence for different allowable target directions.*

### Reverberant-room evaluation

**Objective (Fig. 10).** During voice activity (samples 1 720 000–1 740 000) the FBF causes almost no target cancellation, the GJBF cancels the target severely, and both the norm-constrained method and the proposed beamformer cancel about **2 dB** — subjectively small. During voice absence (after sample 1 760 000), the interference-reduction ratio separates the methods decisively:

| Method | Target cancellation (voice active) | Interference reduction (voice absent) | MOS |
|:-------|:----------------------------------|:--------------------------------------|:----|
| FBF (delay-and-sum) | ~0 dB (none) | 3 dB | 1.7 |
| Simple GJBF | severe | — (target destroyed) | 2.8 |
| Norm-constrained method (Cox et al. 1987) | ~2 dB | 9 dB | 2.6 |
| **Proposed (CCAF BM + NCAF MC)** | **~2 dB** | **19 dB** | **3.8** |

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/3cb712c5cf673c9964a6bd119521508316fec37cd0df7106a1be44c7ddbe5e47.jpg|Output powers for a male speech and a white noise]]
*Figure 10: Output powers for male speech and a white noise source, $T_{60} \approx 0.3$ s.*

**Step-size sensitivity (Fig. 11).** Increasing the NCAF step size $\beta$ suppresses interference faster (before sample 20 000) but audibly increases breathing noise. Decreasing the CCAF step size $\alpha$ reduces breathing noise but increases target cancellation early in adaptation (samples 10 000–20 000) and lowers the final IRR (samples 1 760 000–1 780 000). The authors conclude step-size selection is critical here and suggest step-size control or a new adaptation algorithm as future work.

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/02b05558cc6dd302e3e6f0e36f396e994b4a7f414edf833baa8e5efa85b97f01.jpg|Output powers for different step sizes]]
*Figure 11: Output powers for different step sizes.*

**Subjective (Fig. 12).** MOS with ten non-professional subjects, using the single-microphone capture (1) and clean male speech (5) as anchors and instructing that target cancellation should score low. The proposed beamformer's **3.8** is the highest of the four methods and **1.0 point above the previous robust (norm-constrained) beamformer's 2.6**. Qualitative observations: target reverberation is *reduced* (the FBF enhances the direct path), target cancellation is heard as high-frequency attenuation, and moving sources produce breathing noise that disappears within a few seconds of adaptation.

![[raw/papers/hoshuyama-1999-robust-adaptive-beamformer-ccaf/figures/62b553148e836706d4e4b19f3d96a86756ad4aed955f0a17cc53c6959c5a09b5.jpg|Mean opinion score]]
*Figure 12: Mean opinion score for the four beamformers.*

## Key Contributions

1. **Coefficient-constrained adaptive filters (CCAFs) as an adaptive blocking matrix.** Introduces a blocking matrix in which each tap of each adaptive filter is clamped to its own interval $[\psi_{m,n}, \phi_{m,n}]$ (Eq. 5), converting the classical target-leakage failure into a bounded, *designable* tracking region.
2. **Robustness as a user-specified design parameter.** Because the constraint region is chosen from the target-minimizing coefficient trajectories over a DOA sector, the maximum allowable target-direction error (up to 20° here, and swept 4°–20° in Fig. 8) is set explicitly by the designer rather than emerging from a scalar regularization constant.
3. **Robustness without spending degrees of freedom.** Unlike BM-side spatial-filter remedies, the constrained CCAF *deliberately* leaves interference uncancelled at the BM outputs, converting the prior trade-off (robustness vs. interference reduction vs. microphone count) into a win-win on 4 microphones: 30 dB anechoic interference reduction at $\theta = \pm 30°$ and 19 dB IRR in a 0.3-s reverberation room.
4. **The FBF's target enhancement is load-bearing.** Identifies that feeding the FBF output as the common reference to all CCAFs is what separates target-minimizing from interference-minimizing coefficient shapes — the mechanism does not work with a single microphone, which reframes the FBF as a functional part of the robustness mechanism rather than merely a target-enhancing pre-filter.
5. **Opposite-SIR adaptation-mode control.** Formalizes BM adaptation during high-SIR periods and MC adaptation during low-SIR periods (the double-talk analogue), showing that MC adaptation control simultaneously improves interference reduction and reduces target distortion.
6. **Practical, matrix-free implementation.** Avoids the matrix products of target-tracking/calibration methods at a cost of about twice the multiplications of the norm-constrained method, and the paper reports the design was already validated in hardware in a companion ICASSP 1998 paper.

## Limitations and Caveats

- **Spectrum-dependent validity of the constraint region.** The allowable target-direction sector calibrated for white signals narrows/widens with the signal spectra (Fig. 7). A colored interference just outside the nominal sector is partly absorbed by the BM and is then unavailable to the MC — an architectural property, mitigated but not removed (8° widening vs. 40° for the norm-constrained method).
- **~3 dB target-response ripple** across frequency, which the authors explicitly flag as possibly unacceptable for frequency-response-sensitive systems such as some ASR front-ends.
- **Step-size sensitivity.** Performance depends on both step sizes in opposite directions (Fig. 11); no adaptation control is provided, and the authors name step-size control as open work.
- **Constraint region must be designed per array.** The limits are derived from the microphone arrangement and the desired sector, so the design is not array-agnostic.
- Speech-only, single-interference evaluation: 4 microphones, 8 kHz, one male English talker, one white-noise interferer, $T_{60} \approx 0.3$ s.

## Related Concepts

- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller (GSC)]]
- [[concepts/adaptive-blocking-matrix|Adaptive Blocking Matrix (ABM)]]
- [[concepts/coefficient-constrained-adaptive-filter|Coefficient-Constrained Adaptive Filter (CCAF)]]
- [[concepts/norm-constrained-adaptive-filter|Norm-Constrained Adaptive Filter (NCAF)]]
- [[concepts/target-signal-cancellation|Target-Signal Cancellation]]
- [[concepts/steering-vector-error|Steering-Vector Error]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
