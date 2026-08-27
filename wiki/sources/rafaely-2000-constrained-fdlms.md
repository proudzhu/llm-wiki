---
type: source
created: 2026-08-27
updated: 2026-08-27
sources:
  - raw/papers/rafaely-2000-constrained-fdlms/full-text.md
  - https://doi.org/10.1109/78.845922
  - zotero://select/items/0_KVF3QFKE
tags:
  - adaptive-filtering
  - frequency-domain
  - constrained-optimization
  - sound-equalization
  - active-noise-control
---

# Rafaely & Elliott 2000: Computationally Efficient Frequency-Domain LMS with Constraints

**Authors**: [[entities/boaz-rafaely|Boaz Rafaely]], [[entities/stephen-j-elliott|Stephen J. Elliott]]
**Institution**: Institute of Sound and Vibration Research (ISVR), University of Southampton
**Venue**: IEEE Transactions on Signal Processing, vol. 48, no. 6, pp. 1649–1655, June 2000
**Type**: Journal article
**DOI**: [10.1109/78.845922](https://doi.org/10.1109/78.845922)
**Zotero**: [KVF3QFKE](zotero://select/items/0_KVF3QFKE)

## Summary

This paper extends the frequency-domain LMS (FDLMS) algorithm to incorporate **practical frequency-domain constraints** on the adaptive filter — e.g. limits on its magnitude response, output power, or robust-stability margin — while remaining cheap enough for real-time implementation on conventional DSP hardware. Constraints are formulated as convex functions in the discrete frequency domain and folded into the LMS cost function via a **penalty-function formulation**, with a steepest-descent search converging to the constrained minimum. The approach is demonstrated on adaptive sound equalization, where a 4 dB magnitude constraint prevents the >20 dB filter peaks that conventional FDLMS produces at locations away from the equalization microphone.

## Problem Formulation

The constrained adaptive filtering problem is posed as:

$$
\begin{array}{ll} \text{minimize} & J = E\left[\mathbf{e}^T(n)\mathbf{e}(n)\right] \\ \text{subject to} & c_i(\mathbf{w}) < 0 \qquad i = 1, \dots, I \end{array}
$$

where the constraint functions $c_i(\mathbf{w})$ are assumed **convex** in the filter coefficients. Convexity of both objective and constraints guarantees a unique global minimum (provided a feasible solution exists). General-purpose convex solvers (interior-point etc.) could solve this offline but are too computationally expensive for real-time audio-rate DSP; the paper instead seeks a minimal-complexity modification of the FDLMS update.

## Methodology

### Base algorithm: FDLMS with time-domain filtering

The paper uses the delayless configuration (Morgan & Thi 1995): filtering is performed in the **time domain** (avoiding the one-block delay of full frequency-domain filtering), while the correlation for adaptation is computed in the frequency domain with FFT size $2N$ and block size $N$:

$$
\mathbf{w}_{m+1} = \mathbf{w}_m + \mu \cdot \mathrm{IFFT}\{X^*(k)\,E(k)\}_{+}
$$

where $\{\cdot\}_{+}$ denotes the causal part (causality gradient constraint, Shynk 1992).

![[raw/papers/rafaely-2000-constrained-fdlms/figures/b46511016a2e31d60a21f13eefdc209e06deac789fecaef232c6b4dac3d927f1.jpg|Frequency-domain LMS block diagram]]
*Figure 1: Frequency-domain LMS algorithm with time-domain filtering and frequency-domain adaptation.*

### Penalty-function formulation

The constrained problem is reformulated with a quadratic one-sided penalty added to the cost:

$$
J = E[\mathbf{e}^T(n)\mathbf{e}(n)] + \sigma \sum_{i=1}^{I} \left\{\max[c_i(\mathbf{w}), 0]\right\}^2
$$

The penalty is zero while constraints hold and grows as $\sigma c_i^2$ when violated; $\sigma$ controls constraint tightness. Because $c_i$ is convex, the penalized cost remains convex, so steepest descent converges to the (unique) constrained minimum. The penalty gradient uses the "zero-if-satisfied" operator $[c_i]_z = c_i \cdot (\mathrm{sign}(c_i)+1)/2$, which is trivially cheap on a DSP (one sign, one multiply), giving the general constrained update:

$$
\mathbf{w}_{m+1} = \mathbf{w}_m + \mu \left(\mathrm{IFFT}\{X^*E\}_{+} + 2\sigma \sum_{i=1}^{I} [c_i(\mathbf{w}_m)]_z \frac{\partial}{\partial \mathbf{w}} c_i(\mathbf{w}_m)\right)
$$

### Three practical constraints

| Constraint | Formulation | Update term added inside the IFFT |
|:-----------|:------------|:-----------------------------------|
| **Magnitude limit** | $c_k = \vert W(k)\vert^2 - L(k) < 0$ (convex quadratic; $L(k)$ sets a per-frequency gain bound) | $4\sigma N \cdot [\vert W\vert^2 - L]_z\, W$ |
| **Output power limit** | $\frac{1}{N}\sum_k \vert X(k) W(k)\vert^2 < p$ (2-norm; protects actuators from overload) | $4\sigma [P - p]_z\, \vert X(k)\vert^2 W$ |
| **[[concepts/robust-stability-constraint\|Robust stability]]** (for feedback controllers via [[concepts/internal-model-control\|IMC]]) | $c_k = \vert W(k) G(k) B(k)\vert^2 - 1 < 0$ ($G$ = plant model, $B$ = multiplicative-uncertainty bound) | $4\sigma N \cdot [\vert W G B\vert^2 - 1]_z\, \vert G B\vert^2 W$ |

All three are convex (the magnitude and robust-stability constraints are quadratic forms with positive semi-definite matrices), and each adds only a modest number of multiplications over conventional FDLMS.

## Experimental Setup

| Item | Value |
|:-----|:------|
| Application | Adaptive sound equalization (compensating loudspeaker + acoustic path) |
| Plant responses | Measured $G_1$ (loudspeaker → equalization microphone) and $G_2$ (loudspeaker → point 10 cm away) in an enclosure |
| Simulation | Matlab, sampling rate 10 kHz, block size $N = 2048$, several thousand block iterations |
| Algorithms compared | Conventional FDLMS; FDLMS with 4 dB magnitude constraint; leaky FDLMS (leak $\gamma$ tuned to limit filter magnitude to ≈4 dB) |
| Constraint | $L(k)$ set to limit $\vert W(k)\vert$ to 4 dB at all frequencies |
| Convergence coefficient | Fixed small $\mu$ (smaller for the constrained algorithm to ensure convergence); no line search |

![[raw/papers/rafaely-2000-constrained-fdlms/figures/9201389ba2994b4744e6c5da03695af80f587832160643bfe39a7a2f6326c2ea.jpg|Adaptive sound equalization system block diagram]]
*Figure 2: Block diagram of the adaptive sound equalization system — $W$ models the inverse of the acoustic path $G_1$, with a modeling delay for causality.*

## Results

- **At the equalization microphone** (Fig. 3): unconstrained FDLMS equalizes best (compensating nearly all notches); the constrained FDLMS cannot fill the deepest notches (they would require large filter gain) but achieves good equalization at most frequencies.

![[raw/papers/rafaely-2000-constrained-fdlms/figures/c273207170c8d5a5ec017b9c5f129595fc06748f237d0afd688e742bd7b2e7da.jpg|Magnitude responses of unequalized and equalized path G1]]
*Figure 3: Magnitude response of the unequalized path $G_1$ (dashed), equalized with conventional FDLMS (thin solid) and with the magnitude-constrained FDLMS at 4 dB (thick solid).*

- **10 cm away from the microphone** (Fig. 4): the notches of $G_1$ and $G_2$ occur at different frequencies (they stem from interference between acoustic modes). The unconstrained equalizer therefore produces a **peak of over 20 dB around 500 Hz** in $|WG_2|$ plus additional high-frequency peaks — badly distorted sound away from the microphone. The constrained equalizer shows no extreme peaks.

![[raw/papers/rafaely-2000-constrained-fdlms/figures/a0a93681c93429253eb8d0a9726847c44cd057b05d49f8b070a2f52ea0683dd5.jpg|Magnitude responses of unequalized and equalized path G2]]
*Figure 4: Magnitude response of $G_2$ (dashed) and the equalized response $|WG_2|$ with conventional FDLMS (thin solid — note the >20 dB peak near 500 Hz) and with the 4 dB-constrained FDLMS (thick solid).*

- **Versus leaky LMS** (Figs. 5–6): the leaky FDLMS achieves a similar ~4 dB gain limit, but the leak penalizes the response at **all frequencies** — limiting peaks in one band degrades equalization in others. The penalty-function constraint affects only the frequencies that actually violate the bound, and the bound is set explicitly rather than found by trial and error for the leak factor $\gamma$.

![[raw/papers/rafaely-2000-constrained-fdlms/figures/ba0fc3d485baca1ce96d000eae3d679e1a554c871bff28d7265e71138449e5b6.jpg|Leaky FDLMS equalized response]]
*Figure 5: Equalized response $|WG_1|$ using the leaky FDLMS with the leak chosen to limit filter magnitude to about 4 dB — the leak degrades the response at all frequencies.*

![[raw/papers/rafaely-2000-constrained-fdlms/figures/976e3aafe315428b57f5437f0978411ab95f36bd211af0c1f1e67ccc9f2b4ed9.jpg|Magnitude responses of the three equalization filters]]
*Figure 6: Magnitude responses of the converged equalization filters — conventional FDLMS (thin solid, large peaks), leaky FDLMS (dashed), and constrained FDLMS (thick solid, accurately limited to 4 dB over several frequency ranges).*

- **Convergence** (Fig. 7): the conventional FDLMS converges slowest but reaches the smallest error; the constrained and leaky variants converge in fewer iterations at the price of larger steady-state error (the constrained algorithm additionally used a smaller $\mu$ for stability).

![[raw/papers/rafaely-2000-constrained-fdlms/figures/869f1c03115b5559cf436600c7de15d86b51affb12f7d28504371fab0c0b89eb.jpg|Block-averaged error convergence curves]]
*Figure 7: Block-averaged error vs. block number for conventional FDLMS (thin solid), leaky FDLMS (dashed), and constrained FDLMS (thick solid).*

## Key Contributions

1. **Constrained FDLMS algorithm**: a penalty-function formulation (with the $[c_i]_z$ sign-operator and steepest descent) that folds arbitrary convex frequency-domain constraints into the FDLMS update at negligible additional computational cost — implementable in real time on conventional DSP hardware, unlike general convex-optimization solvers.
2. **Catalogue of convex practical constraints**: per-frequency magnitude limits, output-power limits (actuator protection), and robust-stability constraints for IMC-based adaptive feedback controllers — each with a closed-form gradient expressible as an IFFT.
3. **Frequency-selective vs. global regularization insight**: demonstration (in the sound-equalization study) that the penalty-function constraint limits gain only at violating frequencies, whereas the widely-used leaky LMS penalizes all frequencies and requires trial-and-error tuning of the leak factor.
4. **Spatial-variability argument for gain constraints**: in room equalization, notches shift position with microphone location, so unconstrained inverse filters create large peaks that distort sound elsewhere; an explicit magnitude constraint bounds this distortion.

## Related Concepts

- [[concepts/constrained-fdlms|Constrained FDLMS]] — the algorithm introduced by this paper
- [[concepts/robust-stability-constraint|Robust Stability Constraint]] — the $|WGB|^2 < 1$ constraint, here enforced adaptively
- [[concepts/internal-model-control|Internal Model Control]] — feedback configuration enabling feedforward-style adaptation
- [[concepts/output-constraint-anc-algorithms|Output Constraint ANC Algorithms]] — later time-domain family addressing the same output-power constraint
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] — the simpler global-penalty alternative compared against
- [[concepts/multidelay-block-frequency-domain-adaptive-filter|Multidelay Block Frequency-Domain Adaptive Filter]] — related block frequency-domain adaptation family (AEC)

## Related Synthesis

- [[synthesis/nonlinear-anc-approaches|Nonlinear ANC Approaches]] — constrained FDLMS as the linear/constrained branch contrasted with nonlinear adaptive controllers
