---
type: source
created: 2026-04-26
updated: 2026-04-26
sources:
  - http://arxiv.org/abs/2509.15864
  - zotero://select/items/0_IA5SPUL5
tags:
  - active-noise-control
  - feedback-anc
  - uncertainty-modeling
  - robust-control
  - internal-model-control
  - convex-hull
  - elliptic-model
---

# Hilgemann, Chatzimoustafa & Jax 2024: Data-Driven Uncertainty Modeling for Robust Feedback ANC

**Authors**: [[../entities/florian-hilgemann|Florian Hilgemann]], [[../entities/egke-chatzimoustafa|Egke Chatzimoustafa]], [[../entities/peter-jax|Peter Jax]]
**Institution**: RWTH Aachen University
**Published**: J. Audio Eng. Soc., vol. 72, no. 12, pp. 873-883, 2024
**Type**: Journal Article
**arXiv**: [2509.15864](http://arxiv.org/abs/2509.15864)
**DOI**: [10.17743/jaes.2022.0185](http://dx.doi.org/10.17743/jaes.2022.0185)
**Zotero**: [IA5SPUL5](zotero://select/items/0_IA5SPUL5)

---

## Summary

Conventional feedback ANC controllers use norm-bounded (disk) uncertainty models that overestimate the true plant variations, leading to overly conservative designs and suboptimal attenuation. This paper proposes two data-driven uncertainty models — **elliptic** and **convex hull** — that more accurately capture the frequency-dependent shape of measured secondary-path variations in headphones. Integrated into an IMC-based constrained least-squares optimization, these models enable 10–18 dB more active attenuation below 1 kHz compared to the conventional disk model, while maintaining robust stability confirmed by extensive measurements with 21 human wearers.

## Problem Formulation

### The Controlled System

The secondary path $G(z)$ (discrete-time plant) varies due to:
- Head/ear shape differences between wearers
- Fit variations: **normal**, **loose** (leakage), **tight** (pressing)
- Manufacturing tolerances, wear, temperature

Measurements on Bose QC45 (over-ear) and QC20 (in-ear) with 222 and 166 frequency responses respectively show:
- 3–5 dB inter-person gain variation at 300 Hz–1 kHz
- >10 dB variation below 200 Hz
- >30 dB total magnitude variance at low frequencies

### Why Disk Models Fail

The norm-bounded (disk) model $\Pi_\mu^{(NB)}$ covers the entire circle of radius $R_\mu$ centered at $G_\mu^{(0)}$, even when observations cluster in non-circular shapes. At 200 Hz, observations are elongated along the imaginary axis — the disk covers the negative real part where no measurements exist, wasting design freedom.

## Methodology

### IMC-Based Controller Optimization

Uses the [[../concepts/internal-model-control|Internal Model Control]] (IMC) structure with feedforward filter $Q(z)$ and internal model $\hat{G}(z)$:

$$K(z) = \frac{Q(z)}{1 - \hat{G}(z) Q(z)}$$

The sensitivity (closed-loop response) is:

$$S(z) = 1 - Q(z) \hat{G}(z)$$

The optimization minimizes the frequency-weighted nominal sensitivity:

$$J(q) = \frac{1}{N_\Omega} \sum_{\mu=1}^{N_\Omega} |W_{1,\mu} \cdot [1 - G_\mu Q_\mu(q)]|^2$$

subject to robust stability constraints $C_\mu(q) < 0$ at each frequency bin $\mu$.

### Uncertainty Models

| Model | Geometry | Parameters | Area vs. Disk | Constraint Type |
|:------|:---------|:-----------|:--------------|:----------------|
| **Norm-Bounded** | Single disk | Center $G_\mu^{(0)}$, radius $R_\mu$ | 100% (baseline) | Convex |
| **Multi-Disk** | Union of $p_\mu$ disks | Centers $G_{l,\mu}^{(0)}$, radii $R_{l,\mu}$ | ~70–80% | Convex |
| **Elliptic** | Single ellipse | Center $G_\mu^{(0)}$, semi-axes $R_{x,\mu}$, $R_{y,\mu}$, angle $\theta_\mu$ | ~60–70% | Non-convex |
| **Convex Hull** | Polyhedral (half-space intersection) | Weights $A_{0l,\mu}$, $A_{1l,\mu}$, offsets $B_{l,\mu}$, $m_\mu$ half-spaces | ~60% | Non-convex |

#### Elliptic Model

$$\Pi_\mu^{(E)} = \left\{ G \in \mathbb{C} : \left(\frac{X_\mu}{R_{x,\mu}}\right)^2 + \left(\frac{Y_\mu}{R_{y,\mu}}\right)^2 \leq 1 \right\}$$

where $X_\mu$ and $Y_\mu$ are rotated coordinates with angle $\theta_\mu$. Parameters obtained from the smallest enclosing ellipse (Löwner-John ellipsoid) via Welzl's algorithm or convex optimization.

**Constraint function** (non-convex in $q$):

$$C_\mu^{(E)}(q) = |Q_\mu(q)| - \frac{X_\mu'^2(q)}{R_{x,\mu}^2} - \frac{Y_\mu'^2(q)}{R_{y,\mu}^2}$$

#### Convex Hull Model

$$\Pi_\mu^{(CH)} = \bigcap_{l=1}^{m_\mu} \left\{ G \in \mathbb{C} : A_{0l,\mu} \Re(G) + A_{1l,\mu} \Im(G) + B_{l,\mu} \leq 0 \right\}$$

Parameters obtained via the quickhull algorithm. Contiguity is inherent — transitions between fits are captured.

**Constraint function** (non-convex, uses smooth min-approximation):

$$C_\mu^{(CH)}(q) = \min\left(V_{1,\mu}(q), \ldots, V_{m_\mu,\mu}(q)\right)$$

where each $V_{l,\mu}(q)$ tests whether the critical point lies outside the $l$-th half-space of the rotated open-loop uncertainty set.

### Key Insight: Multiplication by $K_\mu$ Transforms the Uncertainty Set

The open-loop response $L_\mu = K_\mu \cdot G_\mu$ scales and rotates the uncertainty set. For the convex hull:

$$\alpha_{l,\mu}' = \alpha_{l,\mu} + \angle K_\mu, \quad B_{l,\mu}' = |K_\mu| B_{l,\mu}$$

This allows writing explicit constraint functions that depend on $q$ through $K_\mu(q)$.

## Experimental Setup

### Hardware
- **Over-ear**: Bose QC45 (manufacturer ANC electronics removed, ADAU1787 codec at $f_s = 192$ kHz)
- **In-ear**: Bose QC20 (same setup)
- **Dummy head**: Head Acoustics HMS II.3

### Measurements
- 222 measurements (over-ear), 166 (in-ear)
- 35 human subjects (ages 18–61), normal fits
- Dummy head: induced loose fits (spectacle frames, straps), tight fits (straps pressing)
- Other cases: open (face-up on table), closed (face-down, blocked)
- Log-sweep excitation, 10 s duration
- Measurement room compliant with ITU-R BS.1116-2

### Controller Design Parameters
- $N_q = 8192$ FIR filter length
- $N_\Omega = 8192$ frequency bins, 0–24 kHz
- Internal model $\hat{G}(z)$: average of 35 normal fits
- Design goal $W_1(z)$: 8th-order Butterworth bandpass, 31 dB peak gain, 0 dB crossovers at ~40 Hz and ~1 kHz
- IIR implementation: 50th-order via balanced truncation

## Results

### Optimization Objective Values

| Model | $J(q)$ | Improvement vs. Disk |
|:------|:-------|:---------------------|
| Norm-Bounded | 1.11 | — |
| Multi-Disk | 0.66 | 40% |
| Elliptic | 0.56 | 50% |
| Convex Hull | 0.54 | 51% |

### Average ANC Performance (21 Human Wearers, Over-Ear)

| Frequency | Disk Model | Convex Hull Model | Improvement |
|:----------|:-----------|:------------------|:------------|
| 300 Hz | ~11 dB | ~29 dB | **+18 dB** |
| 140–280 Hz | 22–29 dB (peak) | 29–31 dB (peak) | +2–9 dB |
| 200–500 Hz | Deviates from target | Closely follows target | Significant |

### Robustness Verification
- **No instability observed** for any model with any fit (loose, normal, tight, transitioning)
- Loose/tight fit performance confirmed on dummy head
- All models guarantee the same practical stability; the difference is performance

### In-Ear vs. Over-Ear
- Convex hull model improves both headphone types
- Elliptic model did **not** improve in-ear performance (between disk and multi-disk) — different uncertainty manifestation
- Below 100 Hz, convex hull achieves design goal more closely for in-ear than over-ear

### Waterbed Trade-off
- Improved low-frequency attenuation comes at the cost of **more severe waterbed amplification** at higher frequencies (>1 kHz) for the elliptic and convex hull models

## Key Contributions

1. **Elliptic uncertainty model** for feedback ANC — captures elongated variations with fewer parameters than multi-disk
2. **Convex hull uncertainty model** for feedback ANC — minimal-area contiguous model that inherently covers fit transitions
3. **Explicit constraint functions** for both models within IMC-based optimization, including the key insight that $K_\mu$ transforms the uncertainty set via scaling and rotation
4. **Smooth min-approximation** for the non-smooth convex hull constraint: $\min(x_1, \ldots, x_m) \approx -\frac{1}{\rho} \log \sum \exp(-\rho x_l)$
5. **Real-time prototype validation** with 21 human wearers confirming 10–18 dB improvement over conventional disk models while maintaining robust stability
6. **Contiguity requirement** — the model must be a single connected region to guarantee stability during fit transitions (unlike the tri-rectangle model)

## Related Concepts

- [[../concepts/feedback-anc|Feedback ANC]]
- [[../concepts/internal-model-control|Internal Model Control]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/uncertainty-modeling-for-anc|Uncertainty Modeling for ANC]]
- [[../concepts/robust-stability-constraint|Robust Stability Constraint]]
- [[../concepts/convex-hull-uncertainty-model|Convex Hull Uncertainty Model]]
- [[../concepts/elliptic-uncertainty-model|Elliptic Uncertainty Model]]

## Related Sources

- [[../sources/cha-2023-dnoisenet-feedback-anc|Cha 2023: DNoiseNet Feedback ANC]] — Deep learning approach to feedback ANC
- [[../sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]] — MVC for feedback ANC
- [[../sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Simplified IMC structure

## Related Entities

- [[../entities/florian-hilgemann|Florian Hilgemann]]
- [[../entities/egke-chatzimoustafa|Egke Chatzimoustafa]]
- [[../entities/peter-jax|Peter Jax]]
- [[../entities/stephen-j-elliott|Stephen J. Elliott]] — Pioneer of feedback ANC and optimal control
- [[../entities/boaz-rafaely|Boaz Rafaely]] — H₂/H∞ feedback ANC for headrest
