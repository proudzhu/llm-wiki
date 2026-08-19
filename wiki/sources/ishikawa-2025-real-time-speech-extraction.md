---
type: source
created: 2026-08-19
updated: 2026-08-19
sources:
  - raw/papers/ishikawa-2025-real-time-speech-extraction/full-text.md
  - https://doi.org/10.1109/ACCESS.2025.3569590
  - zotero://select/items/0_4U5QAMLY
tags:
  - blind-source-separation
  - independent-low-rank-matrix-analysis
  - rank-constrained-spatial-covariance-matrix-estimation
  - real-time-speech-extraction
  - spatial-regularization
  - diffuse-noise
  - fast-demixing-matrix-estimation
aliases:
  - Ishikawa et al. 2025: Real-Time RCSCME-based Speech Extraction
---

# Ishikawa, Nakamura, Takamune, Kitamura, Saruwatari, Takahashi & Kondo 2025: Real-Time Speech Extraction via RCSCME + SR-ILRMA with Fast Demixing

**Authors**: Yuto Ishikawa, Tomohiko Nakamura, Norihiro Takamune, Daichi Kitamura, Hiroshi Saruwatari, Yu Takahashi, Kazunobu Kondo
**Institutions**: The University of Tokyo (Ishikawa, Nakamura, Takamune, Saruwatari); National Institute of Technology, Kagawa College (Kitamura); Yamaha Corporation (Takahashi, Kondo)
**Published**: IEEE Access, vol. 13, pp. 80229–80251, May 2025
**DOI**: [10.1109/ACCESS.2025.3569590](https://doi.org/10.1109/ACCESS.2025.3569590)
**Zotero**: [zotero://select/items/0_4U5QAMLY](zotero://select/items/0_4U5QAMLY)

## Summary

This paper proposes a **real-time extension** of the offline speech extraction method based on [[concepts/independent-low-rank-matrix-analysis|ILRMA]] and [[concepts/rank-constrained-spatial-covariance-matrix-estimation|RCSCME]] by introducing the **blockwise batch algorithm**: the ILRMA part estimates a time-invariant demixing matrix $\mathbf{W}_i$ over multiple frames in parallel, while the RCSCME part runs every STFT shift (32 ms) using the latest $\mathbf{W}_i$. To overcome **channel-selection errors** that arise in short observation windows, two new **spatial regularizers** for ILRMA are designed — *SR-ILRMA* (using the prior target steering vector) and *NSR-ILRMA* (a null-based variant that admits the cheaper IP update). Two accelerated and numerically stable update algorithms — **FastVCD** and **FastIP** — are derived by a sequence of four algebraic transformations of the VCD/IP update rules, and are analytically equivalent to the originals. Experiments show that the proposed real-time framework with NSR-ILRMA + FastIP runs in real time on a CPU and on NVIDIA Jetson AGX modules, while exceeding conventional Online IVA-IP/ISS in SDR/SIR improvement under diffuse-noise conditions.

## Problem Formulation

### ILRMA Setting

For $M$ microphones and $N=M$ point sources in the STFT domain with frequency bin $i$, frame $j$, and source $n$:

$$\mathbf{x}_{ij} = \mathbf{A}_i \mathbf{s}_{ij}, \qquad \mathbf{y}_{ij} = \mathbf{W}_i \mathbf{x}_{ij},$$

where $\mathbf{W}_i = \mathbf{A}_i^{-1} = (\mathbf{w}_{i1}, \ldots, \mathbf{w}_{iN})^{\mathsf{H}}$ is the demixing matrix. Each separated coefficient $y_{ijn}$ follows a complex Gaussian with time-variant variance $r_{ijn}$ modeled by NMF:

$$r_{ijn} = \sum_k t_{ikn} v_{kjn}.$$

The ILRMA cost (scaled negative log-likelihood) is

$$\mathcal{T}_{\mathrm{ILRMA}} = \frac{1}{J}\sum_{i,j,n}\!\left(\frac{|\mathbf{w}_{in}^{\mathsf{H}}\mathbf{x}_{ij}|^2}{\sum_k t_{ikn}v_{kjn}} + \log\!\sum_k t_{ikn}v_{kjn}\right) - \sum_i \log|\det\mathbf{W}_i|^2 + \text{const.} \tag{4}$$

$\mathbf{W}_i$ is updated by **iterative projection (IP)** and the NMF variables by the MM algorithm.

### RCSCME Setting

The observed-signal covariance is modeled as a time-varying weighted sum of the rank-1 target-speech SCM and the full-rank diffuse-noise SCM:

$$\mathcal{R}_{ij}^{(\mathrm{x})} = r_{ij}^{(\mathrm{t})}\mathbf{a}_i^{(\mathrm{t})}(\mathbf{a}_i^{(\mathrm{t})})^{\mathsf{H}} + r_{ij}^{(\mathrm{n})}\mathcal{R}_i^{(\mathrm{n})}, \tag{18}$$

where $\mathbf{a}_i^{(\mathrm{t})}$ is the target-speech steering vector (the $n^{(\mathrm{t})}$-th column of $\mathbf{W}_i^{-1}$), and the diffuse-noise SCM is built from the $M-1$ non-target ILRMA channels:

$$\mathcal{R}_i^{(\mathrm{n})} = \mathcal{R}_i^{\prime(\mathrm{n})} + \lambda_i \mathbf{z}_i\mathbf{z}_i^{\mathsf{H}}, \quad \mathcal{R}_i^{\prime(\mathrm{n})} = \frac{1}{J}\sum_j \hat{\mathbf{u}}_{ij}\hat{\mathbf{u}}_{ij}^{\mathsf{H}}. \tag{20, 21}$$

A sparsity-inducing inverse-gamma prior on $r_{ij}^{(\mathrm{t})}$ yields the MAP cost

$$\mathcal{T}_{\mathrm{RCSCME}} = \sum_{i,j}\!\left[\mathbf{x}_{ij}^{\mathsf{H}}(\mathcal{R}_{ij}^{(\mathrm{x})})^{-1}\mathbf{x}_{ij} + \log\det\mathcal{R}_{ij}^{(\mathrm{x})} + (\alpha+1)\log r_{ij}^{(\mathrm{t})} + \frac{\beta}{r_{ij}^{(\mathrm{t})}}\right] + \text{const.} \tag{23}$$

Updates for $r_{ij}^{(\mathrm{t})}, r_{ij}^{(\mathrm{n})}, \lambda_i$ are derived via the **majorization-equalization algorithm**. After convergence, the target image is extracted via the [[concepts/multi-channel-wiener-filter|multichannel Wiener filter]]:

$$\hat{\mathbf{s}}_{ij} = \frac{r_{ij}^{(\mathrm{t})}}{r_{ij}^{(\mathrm{t})} + \lambda_i r_{ij}^{(\mathrm{n})}}\,\mathbf{a}_i^{(\mathrm{t})}\mathbf{w}_{in^{(\mathrm{t})}}^{\mathsf{H}}\mathbf{x}_{ij}. \tag{33}$$

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/3528f0fddb084bfb0547b78c189276f5ec1a32baf7dbb42b2368e2308879003a.jpg|Flow of speech extraction method based on ILRMA and RCSCME.]]

*Figure 2: Flow of speech extraction method based on ILRMA and RCSCME.*

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/b8025dd110e8a8facfe628493b569768aabddd31f23f9528c24f0bff29ecf956.jpg|Schematics of supposed situation in ILRMA (left) and RCSCME (right).]]

*Figure 3: Schematics of supposed situation in ILRMA (left) and RCSCME (right).*

## Methodology

### A. Real-Time Framework: Blockwise Batch Algorithm

The offline RCSCME-based method is split into the ILRMA part (computes $\mathbf{W}_i$ and the channel index $n^{(\mathrm{t})}$) and the RCSCME part (uses $\mathbf{W}_i, n^{(\mathrm{t})}$ to extract target). The two parts run **in parallel**:

- ILRMA part: every $\tau_3$ ms, reads the most recent $\tau_1$-s-long observation and updates $\mathbf{W}_i, n^{(\mathrm{t})}$ (computation can span multiple frames).
- RCSCME part: every $\tau_4$ ms (the STFT shift, 32 ms), reads the most recent $\tau_2$-s-long observation and the latest $\mathbf{W}_i, n^{(\mathrm{t})}$ from ILRMA, runs a few RCSCME iterations, and outputs $\hat{\mathbf{s}}_{ij}$.

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/5b1b2adb3e95012f8acf1b5c470938815d9921cf0a8d43b148c8e028a9b9d151.jpg|Schematic of parallel processing in real-time RCSCME-based speech extraction method.]]

*Figure 4: Schematic of parallel processing in real-time RCSCME-based speech extraction method.*

### B. New Problem: Channel Selection Error in Real-Time Mode

When the $\tau_1$-s window contains insufficient target speech, the maximum-kurtosis criterion used offline can pick the wrong channel and discard the target speech entirely. The remedy is to incorporate **spatial prior information** (approximate target direction) via spatially regularized ILRMA.

### C. SR-ILRMA: Spatial Regularization Using Prior Target Steering Vector

Conventional SR-ILRMA requires steering vectors for **all** sources. Since the application scenario provides only the **target** steering vector $\hat{\mathbf{a}}_{in^{(\mathrm{t})}}$, the paper designs a new regularizer:

- Replaces the Euclidean distance $\sum_{i,n}\|\mathbf{w}_{in} - \hat{\mathbf{w}}_{in}\|^2$ with a Mahalanobis distance using metric $(\hat{\mathbf{A}}_i\hat{\mathbf{A}}_i^{\mathsf{H}})^{-1}$, then specializes it to use **only** $\hat{\mathbf{a}}_{in^{(\mathrm{t})}}$.
- The resulting regularizer (Eq. 37) involves only $\mathbf{w}_{in^{(\mathrm{t})}}$ and $\hat{\mathbf{a}}_{in^{(\mathrm{t})}}$, so the **other rows of $\mathbf{W}_i$** are updated by the standard IP rule and only the target row carries the regularization term.
- Parameter estimation is derived via **vectorwise coordinate descent (VCD)**.

### D. NSR-ILRMA: Null-Based Spatially Regularized ILRMA

VCD is more expensive than IP. To allow IP, the paper modifies the regularizer so that the target-row update of $\mathbf{W}_i$ is constrained via a **null beamformer** built from $\hat{\mathbf{a}}_{in^{(\mathrm{t})}}$. The new regularizer (Eq. 48) penalizes the component of $\mathbf{w}_{in^{(\mathrm{t})}}$ orthogonal to $\hat{\mathbf{a}}_{in^{(\mathrm{t})}}$, which admits a closed-form IP-style update. The resulting method is **NSR-ILRMA**.

### E. FastVCD and FastIP: Fast, Numerically Stable Demixing Updates

Starting from the VCD/IP update rules, the paper applies a four-step sequence of algebraic transformations to remove general-matrix inversions, demixing-matrix appearances, and conditional branches:

| Transformation | What it removes/replaces | Effect |
|---|---|---|
| (i) | General matrix inversion $\to$ Hermitian matrix inversion (via Sherman–Morrison) | Removes the dominant $\mathcal{O}(N^3)$ inversion |
| (ii) | Two matrix–vector products replaced by two memory accesses + one matrix–vector product | Small but consistent speedup |
| (iii) | Matrix–matrix products replaced by row/column updates using the structure of $\mathbf{F}_{in}^{(l)}$ | Major speedup; $\mathbf{W}_i$ only appears in its own update |
| (iv) | Conditional branch in $\varphi_{in}^{(l)}$ collapsed into a single closed form using phase of $\chi_{in}^{(l)}$ | Removes NaN-causing branch |

The resulting **FastVCD** (used in SR-ILRMA) and **FastIP** (used in Naive- and NSR-ILRMA) are **analytically equivalent** to the originals: the cost function is monotonic non-increasing along the update sequence.

## Experimental Setup

| Condition | Setting |
|---|---|
| Sampling rate | 16 kHz |
| STFT | 64-ms Hann window, 32-ms shift |
| Sources | 1 directional target speech + diffuse noise (real-world recorded), input SNR $\in \{0, 5, 10\}$ dB |
| NMF bases $K$ | 10 |
| ILRMA iterations | 30 (every $\tau_3 = 512$ ms, $\tau_1 = 5$ s window) |
| RCSCME iterations | 3 (every $\tau_4 = 32$ ms, $\tau_2 = 3$ s window) |
| Prior steering vector | Free-field, same height/distance as recording |
| Regularizer weight $\bar\mu_{in}^{(\mathrm{SR})}, \bar\mu_{in}^{(\mathrm{N S R})}$ | 0.1 |
| Weight scheduler $\varrho^{(l)}$ | 1 (constant) |
| RCSCME hyperparams $\alpha, \beta, \varpi$ | 1.6, $10^{-16}$, 0.1 |
| Reference CPU | Intel Core i9-13900KF, 128 GB RAM |
| Edge devices | NVIDIA Jetson AGX Xavier (Jetpack 5.1), AGX Orin (Jetpack 5.1.2) |
| Data types | NMF variables `bfloat16`, others single-precision |
| Conventional methods compared | Online IVA-IP, Online IVA-ISS |
| Proposed methods compared | NaiveILRMA (kurtosis-based channel selection) + FastIP; SR-ILRMA + FastVCD; NSR-ILRMA + FastIP |
| Metrics | SDR improvement, SIR improvement, processing time |

## Results

### A. FastVCD vs Conventional VCD (CPU)

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/2277c4766945b2f5a4a19b65c1388013240f163846c198e7d99fae6d928b10c4.jpg|Boxplot of computation time for each method.]]

*Figure 6: Boxplot of computation time for each method.*

- **FastVCD runs in ~2/3 the time of Normal VCD.** Transformations (i) and (iii) contribute the largest speedups; (ii) and (iv) give smaller but consistent gains.

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/43f549b02f53bd265f1797b314d7ad103c72d21eddcc33c1a95507bcf46bda6f.jpg|Proportions of unstable cases vs control parameter s.]]

*Figure 7: Proportions of unstable cases with respect to control parameter $s$ for stability of input data in each method.*

- **FastVCD is more numerically stable** than Normal VCD across all values of the ill-conditioning parameter $\varsigma$ in the toy-model experiment (100 trials per $\varsigma$).

### B. Real-Time RCSCME-Based Method on CPU

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/10f0e189e63472a0923a2892a9aa7c6907d6a2729ca4e62a320b442989ad2176.jpg|Boxplots of processing times for RCSCME part of all methods.]]

*Figure 8: Boxplots of processing times for RCSCME part of all methods.*

- **RCSCME part**: max processing time 28.1 ms < 32 ms STFT shift → all proposed methods function in **real time**.

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/6a0568ac5b18372d216f1fe51fcfe9b8d01bc6af15d1f4aec596a1916e8f5058.jpg|Boxplots of processing times for ILRMA part of all methods.]]

*Figure 9: Boxplots of processing times for ILRMA part of all methods.*

- **ILRMA part**: Naive and NSR-ILRMA are competitive (~444 ms avg); SR-ILRMA is slower because of FastVCD's higher per-iteration cost. All fit comfortably within the 512-ms ILRMA-cadence window.

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/21286b5ddc62241954bc96b5a8f78328b931dfaa378fad45713eace7ee0522e3.jpg|SDR improvement for each method at input SNR = 0 dB.]]

*Figure 10(a): SDR improvement [dB] for each method when input SNR was 0 dB.* (See Figs. 11/12 in the source for SNR = 5 dB and 10 dB; the relative ordering is the same.)

- All three proposed methods **outperform** Online IVA-IP and Online IVA-ISS in average SDR and SIR improvement under all input SNRs.
- NaiveILRMA occasionally suffers very low SDR (channel-selection errors); **SR- and NSR-ILRMA eliminate these failures**.

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/92d61b60c1983e182faf9ae0c08f71c0e9d6fafa4d6b6bfac7f17d7ff273abd5.jpg|Spectrograms of separated signal corresponding to target speech estimated by ILRMA part of NaiveILRMA (left) and NSR-ILRMA (right) in real-time scenario.]]

*Figure 13 (right): Spectrograms of separated signal — NaiveILRMA shows discontinuities around 1–3 s (channel-selection error); NSR-ILRMA restores the missing target speech.*

### C. Real-Time Operation on Edge Devices (NVIDIA Jetson)

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/6935d5e89ad2c765304eb17f98bff349ccfeb455caa8097f7869dece216772cf.jpg|SDR improvement for each device.]]

*Figure 14(a): SDR improvement [dB] for each device (NSR-ILRMA, SNR = 0 dB).* (b) SIR improvement is similar across devices.

- **AGX Xavier and AGX Orin achieve essentially identical SDR/SIR to the CPU**, confirming portability to low-power platforms.
- Jetson ILRMA-part times are shorter than CPU because GPU parallelizes NSR-ILRMA's matrix ops; AGX Orin is the fastest.

### D. Robustness to Errors in Prior Direction

![[raw/papers/ishikawa-2025-real-time-speech-extraction/figures/abf53525ab36b69d3d7c364a591a7dd40adf72d1c65f2febd1d2bca3f3209e21.jpg|Average SDR relative to that with correct prior direction for each method.]]

*Figure 17 (left): Average SDR relative to that with correct prior direction.* (Right) SIR relative. Prior direction is the horizontal angle between virtual source and microphone array relative to the correct angle.

- The **acceptable range** (relative SDR degradation < 0.5 dB, relative SIR degradation < 1 dB) is approximately $[-30°, +9°]$, asymmetric due to a loud background-music loudspeaker biasing toward positive angles.
- SR-ILRMA and NSR-ILRMA have **comparable acceptable ranges**, confirming robustness to prior-direction errors of both regularizers.

## Key Contributions

1. **Real-time RCSCME-based speech extraction framework** via the blockwise batch algorithm — ILRMA part runs across multiple frames while RCSCME runs every STFT shift, achieving real-time operation on a CPU and on Jetson edge devices.
2. **Two new spatial regularizers for ILRMA** that use **only the prior target-speech steering vector** (rather than all-source priors): **SR-ILRMA** (VCD-based) and **NSR-ILRMA** (null-based, admits IP). Both reduce channel-selection errors in short-window real-time mode.
3. **FastVCD and FastIP algorithms**: four algebraic transformations of the conventional VCD/IP updates that remove general-matrix inversions, eliminate the conditional branch, and are analytically equivalent to the originals — providing ~33% speedup and improved numerical stability.
4. **Empirical validation on edge devices**: NVIDIA Jetson AGX Xavier / AGX Orin achieve the same SDR/SIR as a desktop CPU with shorter ILRMA-part processing time, confirming practicality for human-avatar/robot communication.
5. **Robustness analysis** to errors in the prior target direction showing an acceptable range of approximately $[-30°, +9°]$ without significant SDR/SIR degradation.

## Related Concepts

- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis (ILRMA)]]
- [[concepts/rank-constrained-spatial-covariance-matrix-estimation|Rank-Constrained Spatial Covariance Matrix Estimation (RCSCME)]]
- [[concepts/fast-demixing-matrix-estimation|Fast Demixing Matrix Estimation (FastVCD / FastIP)]]
- [[concepts/spatial-regularization|Spatial Regularization]]
- [[concepts/iterative-source-steering|Iterative Source Steering (ISS)]] (related fast-update paradigm)
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- Blind Source Separation (BSS), Diffuse Noise, Steering Vector

## Related Entities

- [[entities/yuto-ishikawa|Yuto Ishikawa]]
- [[entities/tomohiko-nakamura|Tomohiko Nakamura]]
- [[entities/norihiro-takamune|Norihiro Takamune]]
- [[entities/daichi-kitamura|Daichi Kitamura]]
- [[entities/hiroshi-saruwatari|Hiroshi Saruwatari]]
- [[entities/yu-takahashi|Yu Takahashi]]
- [[entities/kazunobu-kondo|Kazunobu Kondo]]

## Related Synthesis

(None yet — candidate topics: comparison of fast-update rules across IVA/ILRMA families, real-time BSS frameworks for human–avatar communication.)
