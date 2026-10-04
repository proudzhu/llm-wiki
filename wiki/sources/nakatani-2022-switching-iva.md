---
type: source
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/nakatani-2022-switching-iva/full-text.md
  - https://doi.org/10.1109/TASLP.2022.3155271
  - zotero://select/items/0_6FPFPGGN
tags:
  - blind-source-separation
  - independent-vector-analysis
  - dereverberation
  - convolutional-beamforming
  - microphone-array
  - switching-system
  - speech-enhancement
---

# Nakatani, Ikeshita, Kinoshita, Sawada, Kamo & Araki 2022: Switching IVA and Its Extension to Blind and Spatially Guided Convolutional Beamforming

**Authors**: [[entities/tomohiro-nakatani|Tomohiro Nakatani]], [[entities/rintaro-ikeshita|Rintaro Ikeshita]], [[entities/keisuke-kinoshita|Keisuke Kinoshita]], [[entities/hiroshi-sawada|Hiroshi Sawada]], [[entities/naoyuki-kamo|Naoyuki Kamo]], [[entities/shoko-araki|Shoko Araki]] (NTT Corporation)
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 30, 2022
**Type**: Journal article
**DOI**: [10.1109/TASLP.2022.3155271](https://doi.org/10.1109/TASLP.2022.3155271)
**Zotero**: [6FPFPGGN](zotero://select/items/0_6FPFPGGN)

## Summary

This paper proposes **switching IVA (swIVA)** and **switching CIVA (swCIVA)**, which incorporate a switching mechanism into IVA-based blind source separation and its convolutional beamforming extension, to enable accurate denoising, dereverberation, and source separation with a **small number of microphones** ($M - N$ small). Time frames of the observed signal are clustered into groups, each well-handled by a conventional (time-invariant) IVA/CIVA with few microphones, and filters plus switches are jointly optimized by maximum-likelihood estimation. Four enabling techniques are introduced: separation matrix-wise switching, a factorized switching model, a coarse-fine source model, and two initialization schemes (blind single-state and spatially guided) that solve the inter-state permutation problem.

## Problem Formulation

$N$ speech sources captured by $M \geq N$ distant microphones with reverberation and diffuse noise are modeled as

$$
\mathbf{x}_{t,f} = \sum_{n=1}^{N} \mathbf{d}_{n,t,f} + \sum_{n=1}^{N} \mathbf{l}_{n,t,f} + \mathbf{v}_{t,f}, \qquad \mathbf{d}_{n,t,f} = \mathbf{h}_{n,f} s_{n,t,f},
$$

where $\mathbf{d}_{n,t,f}$ is the desired signal (direct + early reflections, time-invariant ATF $\mathbf{h}_{n,f}$), $\mathbf{l}_{n,t,f}$ is late reverberation, and $\mathbf{v}_{t,f}$ is diffuse noise.

**The problem**: conventional CIVA/IVA assume a determined point-source model with $N$ speech sources and $M-N$ noise components. This simplification works well when $M \gg N$ (e.g., $M{=}8$, $N{=}2$), but estimation accuracy seriously degrades as $M-N$ decreases (e.g., 2 or 3 microphones for 2 sources) and/or noise level grows — severely limiting practical applicability.

**Key idea**: exploit the sparseness of speech in the STFT domain. Clustering time frames into groups reduces the effective number of sources per group, increasing the usable signal space $M-N$ for noise separation in each group; time-varying prediction matrices similarly adapt dereverberation to the time-varying noise influence.

## Methodology

### swCBF: convolutional beamformer with switching

A time-varying CBF factorizes into a (switching) MCLP filter and a (switching) separation matrix:

$$
\mathbf{z}_{t,f}^{(i)} = \mathbf{x}_{t,f} - (\mathbf{G}_{f}^{(i)})^{\mathsf{H}} \bar{\mathbf{x}}_{t,f}, \qquad
\mathbf{y}_{t,f}^{(i,j)} = (\mathbf{W}_{f}^{(j)})^{\mathsf{H}} \mathbf{z}_{t,f}^{(i)}, \qquad
\mathbf{y}_{t,f} = \sum_{i,j} \beta_{t,f}^{(i,j)} \mathbf{y}_{t,f}^{(i,j)},
$$

with binary switching weights $\beta_{t,f}^{(i,j)} = \gamma_{t,f}^{(i)}\delta_{t,f}^{(j)} \in \{0,1\}$, $\sum_{i,j}\beta_{t,f}^{(i,j)} = 1$; $I$ and $J$ are the numbers of MCLP-filter and separation-matrix states. Two structures are studied:

![[raw/papers/nakatani-2022-switching-iva/figures/812f58fda004ad40d31c5955b0e95bee393f83b3fe73d8635774b1a186e6efe0.jpg|(a) Direct switching model]]
![[raw/papers/nakatani-2022-switching-iva/figures/979cbe04ff46bbd530d8a3220c6c314b62c13e16a8d36620da83aabeaaa2249d.jpg|(b) Factorized switching model]]

*Figure 1: (a) Direct switching model — a set of CBFs followed by one switch; sub-optimal because it cannot separately capture time-varying characteristics for dereverberation and separation. (b) Factorized switching model — separate switches for MCLP filters and separation matrices (adopted).*

![[raw/papers/nakatani-2022-switching-iva/figures/729e89d75e810b271e6540eaa3e61469eb841ffaca7f314c9455ecba48611fab.jpg|Expanded form of a swCBF]]

*Figure 2: Expanded form of a swCBF — the observed signal is dereverberated by $I$ MCLP filters, separated by $J$ separation matrices (yielding $IJ$ output candidates), and a switch selects one output per TF point.*

### ML objective and updates

Under mutual independence and a time-varying Gaussian source model, the log-likelihood is

$$
\mathcal{L}(\mathcal{G}, \mathcal{W}, \Lambda, \mathcal{B}) = \sum_{t,f,i,j} \beta_{t,f}^{(i,j)} \mathcal{L}_{t,f}^{(i,j)}, \quad
\mathcal{L}_{t,f}^{(i,j)} = -\sum_{n=1}^{M}\left(\frac{|y_{n,t,f}^{(i,j)}|^2}{\lambda_{n,t,f}} + \log\lambda_{n,t,f}\right) + 2\log|\det \mathbf{W}_{f}^{(j)}|.
$$

Optimization is by coordinate ascent (Algorithm 1 in the paper):

1. **G update (swWPE part)**: closed-form weighted least-squares per state $i$, using source-wise covariance decomposition (Eq. 20–24) — an extension of swWPE with the spatial model specified by $\mathbf{W}$.
2. **W update (swIVA part)**: iterative projection (IP) as in AuxIVA, applied per state $j$ with state-weighted covariance $\Sigma_{n,f}^{(j)}$ (Eq. 25–29); iterated $K$ times per MCLP update. The separation-matrix-wise switching structure is what makes these efficient IVA solvers (IP, ISS, IPA, accelerated AuxIVA) directly applicable.
3. **$\Lambda$ update**: $\lambda_{n,t,f} \leftarrow |y_{n,t,f}|^2 + \varepsilon$.
4. **B update**: select $\{i,j\}$ maximizing $\mathcal{L}_{t,f}^{(i,j)}$ at each TF point (hard switch).

![[raw/papers/nakatani-2022-switching-iva/figures/b1e6f35fb63ddbd081d9e5da92e445f46fba8a0ab21e95fdf77ce3f73bfd6951.jpg|Schematic diagram of swCIVA]]

*Figure 3: Schematic diagram of swCIVA; it becomes swIVA by dropping the $\mathbf{G}_f$ blocks and setting $I=1$.*

### Coarse-fine source model

A frequency-**independent** (coarse) source model is essential for IVA to solve the frequency permutation problem, while a frequency-**dependent** (fine) model is essential for optimizing the MCLP filters and switches. The hybrid model uses $\lambda_{n,t} = \frac{1}{F}\sum_f \lambda_{n,t,f}$ (coarse) for separation-matrix updates and the fine model elsewhere. See [[concepts/coarse-fine-source-model|Coarse-Fine Source Model]].

### swIVA

swIVA is the special case without reverberation: drop $\mathbf{G}$, substitute $\mathbf{x}_{t,f}$ for $\mathbf{z}_{t,f}^{(i)}$, and set $I=1$. swIVA with $J=1$ equals conventional IVA.

### Initialization: the inter-state permutation problem

Because sources are estimated by different separation matrices at different switching states, they can be **permuted between states**, causing convergence to poor stationary points (simple initialization makes swIVA underperform IVA). Two remedies:

1. **Blind single-state initialization**: optimize with $J=1$ for a fixed number of iterations (immune to inter-state permutation), then copy $\mathbf{W}_{f}^{(1)}$ to all states and re-initialize $\beta_{t,f}^{(i,j)} \leftarrow \beta_{t,f}^{(i,1)}\delta_{t,f}^{(j)}$; fully blind.
2. **Spatially guided initialization**: estimate ATFs from NN-predicted TF masks via GEVD ($\mathbf{a}_{n,f} \leftarrow \Gamma_{V,n,f}\,\mathrm{MaxEig}(\Gamma_{V,n,f}^{-1}\Gamma_{Z,n,f})$), then initialize each state's separation matrix as an MPDR beamformer w.r.t. the shared ATFs (Eq. 39–41). Solves the permutation problem **and** improves the stationary point.

### Computational complexity

swIVA matches IVA's dominant $O(M^3TF)$ covariance cost; the switching overhead appears only in inversion/filtering ($J\times$). swCIVA is dominated by $O(M^3L^2TF)$ covariance like CIVA, with extra terms growing in $I$, $J$ (e.g., $O(IJM^5L^2F)$ for the source-wise covariance decomposition). Measured Python/Numpy runtimes on 13.1 s mixtures: IVA 5.6 s → swCIVA $(3,3)$ 47.2 s (2-Mix); the number of microphones impacts runtime more than the state count.

## Experimental Setup

| Item | Configuration |
|------|---------------|
| Dataset 1 (FWSSNR) | REVERB-2MIX SimuData — 2176 two-source mixtures, 2 or 3 mics, avg 7.9 s, SNR 20 dB, RT60 0.2–0.7 s |
| Dataset 1 (WER) | REVERB-2MIX RealData — 372 mixtures, 2 or 3 mics, avg 6.5 s |
| Dataset 2 | TIMIT-ConvMix — simulated 2-Mix (40 mixtures, 3 mics) / 3-Mix (40 mixtures, 4 mics), CHiME-3 noise (BUS/STR/PED/CAF) at 10 dB, RWCP JR1 RIR, RT60 0.6 s, all speakers continuous |
| STFT | 32 ms window / 8 ms shift, Hann, 16 kHz |
| MCLP filter | Prediction delay $D=2$, CBF length $L=10$ |
| Iterations | $K=5$ W-updates per G-update; 50 separation-matrix / 10 MCLP-filter updates |
| Stabilization | Diagonal loading ($10^{-4}\times\mathrm{Trace}$ for WPE, $10^{-10}\times\mathrm{Trace}$ for IVA); projection back for scale ambiguity |
| TF masks (spatial guide) | Frequency-domain CNN with large receptive field (Conv-TasNet-like), trained with utterance-level uPIT |
| Metrics | FWSSNR, WER (Kaldi TDNN-LFMMI + i-vector + trigram LM), SDR (MUSEVAL v4, bss_eval_images), SIR, noise power reduction |
| Compared | IVA ($J{=}1$), swIVA ($J{=}2,3$), CIVA $(I,J){=}(1,1)$, swCIVA $(1,2),(2,1),(2,2),\ldots,(3,3)$ |

## Results

- **Initialization is decisive**: with simple initialization swIVA *underperformed* IVA (2-ch); with blind single-state and (best) spatially guided initialization, swIVA/swCIVA substantially and consistently outperform IVA/CIVA.
- **Coarse-fine source model is necessary**: the fine model for switches and MCLP filters (with the coarse model for separation matrices) greatly outperformed all-coarse or all-fine configurations on both FWSSNR and WER.
- **Joint beats separate**: joint swCIVA optimization clearly outperformed a cascade of separately-optimized swWPE + swIVA; joint CIVA $(1,1)$ even beat separate swCIVA $(2,2)$ with 3 mics.
- **Factorized beats direct switching model**: with $(I,J){=}(2,2)$ the factorized model substantially outperformed the direct model, whose gains saturated beyond $J{=}2$. The two switch types learn clearly different TF patterns (Fig. 9) — the separation switch tracks the observed spectrogram structure while the MCLP switch does not.

![[raw/papers/nakatani-2022-switching-iva/figures/705649d812cc393af98271a91bbc8d46ced9db78e90d0e57ca5f95c635f88203.jpg|Switching weights of separation matrix]]
![[raw/papers/nakatani-2022-switching-iva/figures/7c5f2ad61d69e265d16b6ea6b7eeed2a99fea8a4e9984d6cb44fb5860924c9db.jpg|Switching weights of MCLP filter]]
![[raw/papers/nakatani-2022-switching-iva/figures/e2dca15426b22b14a22173ddf515b70a044601880098be7257b141f9acd4b311.jpg|Observed spectrogram]]

*Figure 9: Switching weights estimated with the factorized model $(I,J){=}(2,2)$ — (a) separation-matrix switch and (b) MCLP-filter switch show clearly different patterns; (d) observed mixture spectrogram for reference. The separation switch is closely related to the spectrogram structure, the MCLP switch is not.*

- **Number of states**: FWSSNR improved consistently from $I{=}J{=}1$ to 3; WER improved from 1 to 2 states but further increase sometimes degraded it (overfitting — parameters grow linearly in $I$ and $J$).
- **TIMIT-ConvMix (blind single-state init)**: SDR improvement consistent as $I$ and $J$ grow 1→3 for both 2-Mix and 3-Mix (observed SDRs −4.7 / −6.8 dB). With 3-Mix: separation (SIR) 4.70 dB (IVA) → 8.08 dB (swCIVA $I{=}J{=}3$); denoising 6.54 → 7.19 dB; dereverberation 1.24 → 3.92 dB.
- **Microphone sweep (3-Mix)**: swIVA/swCIVA outperformed IVA/CIVA under *all* conditions from 3 to 8 microphones; ICA (with permutation re-alignment) was the weakest baseline.

![[raw/papers/nakatani-2022-switching-iva/figures/8b8b0a4278d8c6876108b0c95f4c9c3a8e2d7caa2db46f10951272491fd897bc.jpg|SDR improvement on 2-Mix]]
![[raw/papers/nakatani-2022-switching-iva/figures/a905e6d94df80abc121e589ea7f53c02d53551009ddf5c392a173dfdda1fa676.jpg|SDR improvement on 3-Mix]]

*Figure 12: SDR improvements on TIMIT-ConvMix 2-Mix (a) and 3-Mix/4ch (b) — consistent gains as $I$ and $J$ increase, after 50 separation-matrix updates with blind single-state initialization.*

## Key Contributions

1. **swIVA**: first incorporation of a switching mechanism into a *blind source separation* algorithm (IVA), with all filters and switches jointly optimized by ML estimation under the same assumptions as IVA — previously switching had only been combined with model-based beamforming (MVDR swBF, wMPDR swCBF, swWPE).
2. **swCIVA**: extension to a blind convolutional beamforming algorithm integrating swIVA and swWPE in a jointly optimal way, capturing two *different* time-varying characteristics (for dereverberation and for separation) via the **factorized switching model**.
3. **Separation matrix-wise switching**: a new switching structure where each separation matrix estimates *all* sources at once, enabling reuse of computationally efficient IVA solvers (IP/ISS/IPA/accelerated AuxIVA).
4. **Coarse-fine source model**: a hybrid frequency-independent/frequency-dependent source model resolving the contradiction between IVA's permutation-free requirement and the fine model needed by switches and MCLP filters.
5. **Two initialization techniques** solving the inter-state permutation problem: blind single-state initialization (fully blind processing) and spatially guided initialization (NN-mask-based ATF estimation + MPDR initialization), the latter also improving the converged stationary point.
6. **Empirical validation** that 2 switching states for both MCLP filters and separation matrices give substantial, consistent improvements over IVA/CIVA with 2–3 microphones across FWSSNR, WER, and SDR.

## Related Concepts

- [[concepts/switching-independent-vector-analysis|Switching Independent Vector Analysis]]
- [[concepts/switching-civa|Switching CIVA (swCIVA)]]
- [[concepts/coarse-fine-source-model|Coarse-Fine Source Model]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/weighted-prediction-error|Weighted Prediction Error (WPE)]]
- [[concepts/mclp|MCLP]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
