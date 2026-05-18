---
type: source
created: 2026-05-18
updated: 2026-05-18
sources:
  - raw/papers/lu-2021-anc-survey-nonlinear/full-text.txt
  - https://doi.org/10.1016/j.sigpro.2020.107929
  - zotero://select/items/0_JCYXHN43
tags:
  - active-noise-control
  - nonlinear-systems
  - survey
  - volterra-filter
  - flann-filter
  - kernel-adaptive-filter
  - spline-adaptive-filter
  - heuristic-algorithms
---

# Lu et al. 2021: Survey on ANC Past Decade — Part II (Nonlinear Systems)

**Authors**: [[../entities/lu-lu|Lu Lu]], [[../entities/kai-li-yin|Kai-Li Yin]], [[../entities/rodrigo-de-lamare|Rodrigo C. de Lamare]], [[../entities/zongsheng-zheng|Zongsheng Zheng]], [[../entities/yi-yu|Yi Yu]], [[../entities/xiaomin-yang|Xiaomin Yang]], [[../entities/badong-chen|Badong Chen]]
**Institutions**: Sichuan University; CETUC, PUC-Rio; Southwest University of Science and Technology; Xi'an Jiaotong University
**Published**: *Signal Processing*, Vol. 181, 107929, April 2021
**Type**: Review article (journal)
**DOI**: [10.1016/j.sigpro.2020.107929](https://doi.org/10.1016/j.sigpro.2020.107929)
**Zotero**: [JCYXHN43](zotero://select/items/0_JCYXHN43)

## Summary

Part II of a two-part survey reviewing **nonlinear active noise control (NLANC)** algorithms developed in the decade 2009–2020. Where Part I covered linear ANC, this paper focuses on the techniques required when the primary path, secondary path, or noise source itself exhibits nonlinear behavior — situations where conventional [[../concepts/filtered-x-lms-algorithm|FxLMS]] and its variants suffer suboptimal performance. The authors structure the field around four pillars: **Volterra-based algorithms**, **FLANN-based algorithms**, **bilinear filters**, and a wave of newer methods (spline ANC, kernel adaptive filters, nonlinear distributed ANC). They additionally survey heuristic optimisers (GA, PSO, BFO, FF, FWA), recent applications (fMRI, transformer, vehicle, ANC-IoT, hearing aids), and conclude with open research challenges.

## Problem Formulation

Three sources of nonlinearity in ANC systems:

| Type | Examples |
|:-----|:---------|
| Nonlinearities in the primary path | Primary noise propagating in a duct with very high SPL |
| Nonlinearities in the secondary path | Overdriven electronics/speakers, amplifier saturation |
| Nonlinearities in components of the ANC system | Actuator harmonics, near-saturation amplitudes, chaotic noise from blowers/grinders/airfoils/fans |

In these scenarios linear ANC cannot fully exploit the coherence in the noise, motivating two design questions:
1. What modelling structures faithfully capture the nonlinearity?
2. What adaptive algorithms can train those structures online?

## Taxonomy of NLANC Algorithms

### 1. Volterra ANC

Truncated Volterra series viewed as a "universal approximator" (Stone–Weierstrass). The number of coefficients of an $M$-tap, order-$Q$ Volterra filter is

$$ N_c = \frac{(M+Q)!}{M!\,Q!} - 1, $$

which grows as $M^Q$, so practical work is restricted to **second-order Volterra (SOV)** and **third-order Volterra (TOV)**. Notable variants:
- **VFxLMS / VFxLMP / VFxlogLMP / VFxlogCLMP**: $\ell_p$-norm and logarithmic-cost extensions for impulsive noise.
- **VFxRMC**: Volterra filtered-x recursive maximum correntropy under [[../concepts/maximum-correntropy-criterion|MCC]].
- **VFxAP**: Affine-projection variant for multi-channel NLANC.

### 2. Hammerstein ANC

Static nonlinearity in series with a linear dynamic block. Three cascade structures: Hammerstein (N–L), Wiener (L–N), Hammerstein–Wiener (N–L–N) and Wiener–Hammerstein (L–N–L). The polynomial expansion $g(n) = \sum_j p_j x^j(n)$ feeds a downstream linear filter.

### 3. FLANN-based Algorithms

The **Functional Link Artificial Neural Network (FLANN)** is a single-layer LIP filter. Its expanded input vector mixes the raw signal with a basis of nonlinear functions:

$$ x_e(n) = \{x(n), \sin(\pi x(n)), \cos(\pi x(n)), \dots, \sin(b\pi x(n)), \cos(b\pi x(n)), \dots\}^T $$

Coefficient count $N_c = M(2b+1)$, dramatically lower than Volterra. Major branches:
- **FsLMS** (Das & Panda, 2004) and fast/RFsLMS variants
- **GFLANN**: adds cross-terms between $x(n)$ and $\sin/\cos(b\pi x(n))$
- **EFLANN**: exponential factor in the trigonometric expansion for faster convergence
- **RFLANN**: recursive (uses past output) — analogous to FuLMS for IIR adaptation
- Orthogonal-basis variants: **Chebyshev (CN)**, **Fourier (FN)**, **Even-Mirror Fourier (EMFN)**, **Legendre (LN)**

### 4. Bilinear ANC

Cross-products between input and past output give better behaviour under saturation with shorter filter length:

$$ y(n) = \sum_{i=0}^{N_1} a_i(n)x(n{-}i) + \sum_{t=1}^{N_1} b_t(n)y(n{-}t) + \sum_{i,t} c_{i,t}(n)x(n{-}i)y(n{-}t) $$

A "diagonal-channel" update structure simplifies adaptation; FLANN-bilinear hybrids and leaky FeLMS variants extend stability and reduce complexity.

### 5. Spline ANC (Scarpiniti et al., 2013→)

Cascade of an FIR/IIR filter with an **adaptive look-up table (LUT)** whose control points are interpolated by a low-order polynomial spline. Output:

$$ y(n) = \mathbf{u}^T(n)\,\mathbf{C}\,\mathbf{q}_i, $$

where $\mathbf{u}(n) = [u^3, u^2, u, 1]^T$ holds the local span parameter, $\mathbf{C}$ is a pre-computed spline basis matrix, and $\mathbf{q}_i$ is the control-point vector. Both FIR-spline and IIR-spline (FuLMS-driven) variants exist; multi-channel extensions outperform multi-channel VFxLMS/FsLMS in MSE and computational cost.

### 6. Kernel Adaptive Filter (KAF) ANC

Recasts the input into an RKHS via a kernel $\kappa(\cdot, \cdot)$ — typically Gaussian — so that linear adaptation in feature space yields nonlinear adaptation in input space:

$$ y(n) = \sum_{j=1}^{n} a_j\,\kappa(\mathbf{X}, \mathbf{X}_j). $$

First applied to NLANC by Mahesh et al. 2009. Drawbacks: dictionary size grows linearly with samples. Sparsification techniques (quantised KAF, set-membership KAF) curb network growth. Alternative kernels (logistic, tan-sigmoid, inverse-tan) further improve performance.

### 7. Nonlinear Distributed ANC

Integrates FLANN expansions into distributed/incremental algorithms for **Wireless Acoustic Sensor Networks (WASNs)**, ensuring distributed nodes can combat nonlinear distortions. EFLANN-based incremental schemes show lower computational cost than FsLMS/VFxLMS distributed counterparts.

## Heuristic-Based ANC

When the secondary path is strongly nonlinear or non-convex, gradient methods get trapped in local minima. Heuristic global optimisers tackle this:

| Algorithm | Year | Key property |
|:----------|:-----|:-------------|
| Genetic Algorithm (GA) | 1994 (first NLANC-relevant) | First heuristic for ANC; adaptive GA + interior-point methods |
| Backtracking Search (BSA) | 2010s | Population-based EA + sequential quadratic programming |
| Particle Swarm Optimisation (PSO) | 2006 | Cooperation/competition between particles; works without S(z) estimation |
| Bacterial Foraging (BFO) | 2010s | Chemotaxis-inspired; ~5 dB better steady-state vs GA-ANC |
| Firefly (FF) | — | Cascades FLANN+FIR with FF coefficient search |
| Fireworks (FWA) | — | Three variants explored for NLANC |

## Comparison & Coefficient Counts

| Filter | $N_c$ | Suitable for |
|:-------|:------|:-------------|
| SOV | $\tfrac{1}{2}M(M+3)$ | General nonlinear modelling |
| FLANN (trig) | $M(2b+1)$ | Mild–medium nonlinearity, low cost |
| GFLANN | $M(2b+1)+1$ | Cross-term coupling |
| EFLANN | requires exp ops | Faster convergence |
| CN (Chebyshev) | $2M+1$ | Orthogonal, low order |
| FN / EMFN | $M(2b+1)+1$ / $\sum_j \binom{M+j-1}{j}$ | Orthogonal universal approximator; EMFN handles strong nonlinearity |
| LN (Legendre) | $QM+1$ | Mild–medium nonlinearity |
| Bilinear | $N_1^2 + 3N_1 + 1$ | Strong nonlinearity, saturated signals |

Empirical comparison (filter length 77, scenario from [63]) ranks **SOV ≈ LN ≈ CN** at the top of averaged-noise-reduction (ANR) curves.

## Cross-Cutting Strategies

- **Remote microphone technique (RMT)** combined with EWU/FeLMS/FsLMS for NLANC.
- **Convex combination** of two nonlinear models (FLANN ⊕ Volterra).
- **MCC** and **Rényi's entropy** based costs for robust NLANC under impulsive/non-Gaussian noise.
- **Chaotic-noise control** via hybrid FLANN methods.
- **Leaky** and **partial-update (PU)** schemes to bound growth and computation.

## Recent Applications

- **fMRI acoustic noise control** — non-stationary harmonic tracking; DFT-based frequency-domain ANC achieves ~35 dB.
- **Transformer noise control** — internally synthesised reference signal at line-frequency harmonics; ~15 dB to 84–96% energy reduction.
- **Vehicles (road noise)** — multi-channel FxLMS, IMC feedback, VSS median-LMS for rail interior; 4 dB up to 1 kHz.
- **ANC-IoT** — MUTE leverages, PoC system over digital ethernet replacing analog cabling.
- **Hearing-aid integration** — ZoQ-based MSE schemes for combined noise reduction + ANC.
- **Zone-of-quiet extension** — spherical loudspeaker arrays, memetic-algorithm distributed adaptation.
- **Repetitive impulsive noise** — iterative learning control (ILC) and repetitive control (RC) variants.

## Future Research Challenges

1. **Theoretical analysis of FLOM and LIP algorithms** in α-stable noise (variance is infinite, breaking standard MSE analysis).
2. **Sparsification of KAF-ANC** using quantised / set-membership schemes to curb dictionary growth.
3. **Internet of Things integration** — extend ANC-IoT to impulsive noise, distributed nodes, Internet of Vehicles.
4. **Computational complexity** — most NLANC algorithms still laboratory-stage; need practical low-complexity variants.
5. **Optimal memory/population length** selection for both NLANC adaptive filters and heuristic optimisers.
6. **Cost-effective application scenarios** — finding the killer use-case for large-scale commercial NLANC.

## Key Contributions

- First comprehensive 2009–2020 review of NLANC, complementing George & Panda (2013).
- Unified taxonomy linking modelling structures (Volterra/Hammerstein/FLANN/bilinear/spline/KAF) with adaptation algorithms.
- Tabulated coefficient-count formulas across all major filter families.
- Empirical ANR comparison of representative algorithms in a common scenario.
- Curated catalogue of heuristic optimisers and their noise-reduction merits.
- Forward-looking research agenda explicitly tying NLANC to IoT and IoV.

## Related Concepts

- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/nonlinear-active-noise-control|Nonlinear Active Noise Control]]
- [[../concepts/volterra-filter|Volterra Filter]]
- [[../concepts/flann-filter|FLANN Filter]]
- [[../concepts/spline-adaptive-filter|Spline Adaptive Filter]]
- [[../concepts/kernel-adaptive-filter|Kernel Adaptive Filter]]
- [[../concepts/bilinear-filter|Bilinear Filter]]
- [[../concepts/heuristic-anc-algorithms|Heuristic ANC Algorithms]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS]]
- [[../concepts/maximum-correntropy-criterion|Maximum Correntropy Criterion]]
- [[../concepts/impulsive-noise|Impulsive Noise]]
- [[../concepts/kernel-methods|Kernel Methods]]
- [[../concepts/remote-microphone-technique|Remote Microphone Technique]]

## Related Sources

- [[kuo-1999-active-noise-control-tutorial-review|Kuo 1999: ANC Tutorial Review]] — Linear ANC foundations
- [[chen-2016-generalized-correntropy-robust-adaptive-filtering|Chen 2016: Generalized Correntropy]] — Robust cost shared by VFxRMC
- [[xiao-2016-fxaps-impulsive-noise|Xiao 2016: FxAPS]] — Affine-projection family used in VFxAP
- [[jiang-2025-ai-driven-avnc-review|Jiang 2025: AI-Driven AVNC Review]] — Modern deep-learning extensions of NLANC
