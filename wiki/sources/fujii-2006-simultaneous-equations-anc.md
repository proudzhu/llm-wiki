---
type: source
created: 2026-05-23
updated: 2026-05-23
sources:
  - raw/papers/fujii-2006-simultaneous-equations-anc/full-text.md
  - https://doi.org/10.1250/ast.27.270
  - zotero://select/items/0_TW8DUFVN
tags:
  - active-noise-control
  - simultaneous-equations-method
  - feedforward-anc
  - secondary-path-change
  - auxiliary-filter
---

# Fujii, Yamaguchi, Hashimoto, Fujita & Muneyasu 2006: Verification of Simultaneous Equations Method by an Experimental Active Noise Control System

| Field | Detail |
|-------|--------|
| **Authors** | [[entities/kensaku-fujii|Kensaku Fujii]], [[entities/kotaro-yamaguchi|Kotaro Yamaguchi]], [[entities/shigeyuki-hashimoto|Shigeyuki Hashimoto]], [[entities/yusuke-fujita|Yusuke Fujita]], [[entities/mitsuji-muneyasu|Mitsuji Muneyasu]] |
| **Institution** | University of Hyogo (Fujii, Yamaguchi, Hashimoto); Catsystem Corporation (Fujita); Kansai University (Muneyasu) |
| **Venue** | Acoustical Science and Technology, Vol. 27, No. 5, pp. 270–277 |
| **Year** | 2006 |
| **Type** | Journal article |
| **DOI** | [10.1250/ast.27.270](https://doi.org/10.1250/ast.27.270) |
| **Zotero** | [Link](zotero://select/items/0_TW8DUFVN) |

## Summary

This paper experimentally verifies the **simultaneous equations method** for feedforward active noise control (ANC) — a technique that estimates the optimal noise control filter without requiring an explicit secondary path model. Unlike the conventional filtered-x algorithm, which relies on a separately identified secondary path filter (and degrades when the path changes), the simultaneous equations method uses an auxiliary filter to identify the overall path. By giving two different coefficient vectors to the noise control filter, two independent equations are obtained, allowing the optimal filter to be solved directly. The authors apply a frequency-domain adaptive algorithm for overall path identification to improve convergence speed, demonstrate automatic recovery from secondary path changes via computer simulation, and validate the method on a physical duct-based ANC system using recorded diesel engine noise.

## Problem Formulation

The feedforward ANC system (Fig. 1) consists of a noise detection microphone $M_d$, a loudspeaker $S_p$, and an error microphone $M_e$. The primary noise $N(z)$ propagates through:

- **Primary path** $P(z)$: from $M_d$ to $M_e$ (to be canceled)
- **Secondary path** $C(z)$: from $S_p$ to $M_e$ (the acoustic path the control signal must traverse)
- **Feedback path** $B(z)$: from $S_p$ back to $M_d$ (can cause howling)

The noise control filter $H(z)$ drives $S_p$ to produce anti-noise. The goal is to find $H_{\text{opt}}(z)$ satisfying:

$$
P(z) + H_{\text{opt}}(z) \tilde{C}(z) = 0
$$

where $\tilde{C}(z) = C(z) - \Delta B(z) P(z)$ accounts for imperfect feedback cancellation ($\Delta B(z) = B(z) - \hat{B}(z)$).

The filtered-x algorithm requires a model of $C(z)$ (secondary path filter), which must be re-identified whenever the secondary path changes — a major practical limitation.

## Methodology

### Simultaneous Equations Principle

The simultaneous equations method introduces an **auxiliary filter** $S(z)$ that identifies the **overall path** from the noise control filter input to the error microphone output:

$$
S(z) = P(z) + H(z) \tilde{C}(z)
$$

With only one equation, $P(z)$ and $\tilde{C}(z)$ cannot be separated. However, by giving **two different coefficient vectors** $H_1(z)$ and $H_2(z)$ to the noise control filter, two equations are obtained:

$$
\begin{aligned}
S_1(z) &= P(z) + H_1(z) \tilde{C}(z) \\
S_2(z) &= P(z) + H_2(z) \tilde{C}(z)
\end{aligned}
$$

Solving these simultaneously yields:

$$
P(z) = \frac{S_1(z) H_2(z) - S_2(z) H_1(z)}{H_2(z) - H_1(z)}, \quad
\tilde{C}(z) = \frac{S_1(z) - S_2(z)}{H_1(z) - H_2(z)}
$$

Substituting into the optimality condition gives the optimal filter directly:

$$
H_{\text{opt}}(z) = \frac{S_1(z) H_2(z) - S_2(z) H_1(z)}{S_2(z) - S_1(z)}
$$

**Key insight**: No explicit secondary path model is needed — the auxiliary filter automatically captures the current overall path, enabling the method to track secondary path changes.

### Frequency-Domain Adaptive Algorithm

The authors apply a frequency-domain adaptive algorithm to estimate the auxiliary filter's frequency response $S(k)$:

$$
S_{j+1}(k) = S_j(k) + \mu \frac{\sum_{i=jI+1}^{(j+1)I} D_i(k) X_i^*(k)}{\sum_{i=jI+1}^{(j+1)I} X_i(k) X_i^*(k)}
$$

where $j$ is the block number, $\mu$ is step size, $I$ is the number of blocks, $D_i(k)$ is the $k$-th spectrum element of the identification error, and $X_i(k)$ is the $k$-th spectrum element of the noise control filter input.

The optimal filter is computed in the frequency domain and transformed back via inverse FFT:

$$
H_{\text{opt}}(k) = \frac{S_1(k) H_2(k) - S_2(k) H_1(k)}{S_2(k) - S_1(k)}
$$

### Updating Procedure

The coefficient vector is continuously refreshed by:

1. Initialize $H_1 = \boldsymbol{0}$, estimate $S_1(k)$ via FFT-based adaptive algorithm
2. Set $H_2 = [a, 0, \dots, 0]^T$ (nonzero constant), estimate $S_2(k)$
3. Compute $H_{\text{opt}}(k)$ from Eq. (15), transform back to time-domain
4. Replace $H_1 \leftarrow H_2$, $H_2 \leftarrow H_{\text{opt}}$, and repeat

This iterative procedure automatically recovers the noise reduction effect when the secondary path changes.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Duct** | Vinyl chloride pipe, 83 mm diameter |
| **Controller** | Pentium IV 3 GHz (Dell Dimension 8300) |
| **Audio interface** | M Audio Delta 44 |
| **Power amplifier** | Yamaha HC-2700 |
| **Loudspeaker** | Pioneer TS-E1076 |
| **Microphone** | Audio Technica AT-805F |
| **Sampling frequency** | 8 kHz |
| **Noise control filter taps** | 512 |
| **Auxiliary filter taps** | 1,024 |
| **FFT duration** | 2,048 samples |
| **Step size $\mu$** | 0.25 |
| **Blocks $I$** | 5 |
| **Iterations $J$** | 20 |
| **Primary noise sources** | (a) Jet fan noise (simulated via second-order resonance), (b) Recorded diesel engine generator exhaust noise |

## Results

### Simulation Results

1. **Automatic recovery**: The estimation error drops to approximately −50 dB after convergence. When the secondary path is artificially inverted (from $C(z)$ to $-C(z)$) mid-iteration, the error spikes then automatically returns to −50 dB within ∼10 iterations.

2. **Convergence speed comparison**: The frequency-domain simultaneous equations method converges significantly faster than the filtered-x NLMS algorithm (step size 0.1). The filtered-x reaches −50 dB in ∼30 iterations, while the proposed method reaches −50 dB in ∼10 iterations — and this comparison assumes perfect secondary path identification for filtered-x, which is unrealistic.

### Experimental Results

1. **Noise reduction**: Output power at the error microphone decreases to less than −20 dB after 2–4 updating operations (∼512 seconds = 2,000 FFT durations) for both jet fan and diesel engine noise.

2. **Averaging operation**: To reduce residual fluctuation below −20 dB, a coefficient averaging scheme is applied: $\hat{H}_{\text{opt}}(k) = H_{\text{opt}}(k) \times 0.1 + \hat{H}_{\text{opt}}(k) \times 0.9$, activated only when output power < −20 dB.

3. **Frequency response**: Wideband noise reduction (no low/high-frequency inversion observed, which is a known advantage).

4. **Path change recovery**: Experimental confirmation that the method automatically recovers the noise reduction effect after secondary path changes (simulated by multiplying the control output by −1).

## Key Contributions

1. **First experimental verification** of the simultaneous equations method in a physical ANC system (previously only simulation-based).
2. **Application of frequency-domain adaptive algorithm** to overall path identification, improving convergence speed over time-domain NLMS and the cross-spectrum method.
3. **Demonstration of automatic recovery** from secondary path changes without injecting extra noise into the loudspeaker.
4. **Introduction of coefficient averaging** to stabilize the noise reduction effect below −20 dB.
5. **Validation on realistic noise sources** (jet fan noise, diesel engine exhaust noise).

## Related Concepts

- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/simultaneous-equations-method|Simultaneous Equations Method]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]
- [[concepts/frequency-domain-anc|Frequency Domain ANC]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/auxiliary-filter|Auxiliary Filter]]

## Related Synthesis

- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]]
- [[synthesis/adaptive-algorithm-tradeoffs|Adaptive Algorithm Tradeoffs]]
- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]]
