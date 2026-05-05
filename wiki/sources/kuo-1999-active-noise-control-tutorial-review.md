---
type: source
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
- active-noise-control
- adaptive-signal-processing
- dsp
- review
- tutorial
aliases:
- 'Kuo 1999: Active Noise Control Tutorial Review'
---

# Active Noise Control: A Tutorial Review

**Authors**: [[../entities/sen-m-kuo|Sen M. Kuo]], [[../entities/dennis-r-morgan|Dennis R. Morgan]]
**Published**: Proceedings of the IEEE, Vol. 87, No. 6, June 1999, pp. 943–973
**DOI**: [10.1109/5.763310](https://doi.org/10.1109/5.763310)
**📎 Zotero**: [zotero://select/items/0_99AD6FSU](zotero://select/items/0_99AD6FSU) |

## Summary

A comprehensive tutorial review of **Active Noise Control (ANC)** covering the fundamental theory, adaptive signal processing algorithms, and practical DSP implementation. This is one of the most widely cited ANC papers, covering broad-band feedforward, narrow-band feedforward, adaptive feedback control, multi-channel extensions, online secondary-path modeling, and special algorithms (lattice, frequency-domain, subband, RLS).

## Key Takeaways

### 1. ANC Fundamentals

- ANC generates an "antinoise" of equal amplitude and opposite phase to cancel primary noise via **superposition**
- The 1936 patent by **Lueg** was the first proposal for acoustic ANC using a microphone and loudspeaker
- ANC is particularly effective at **low frequencies** where passive methods (enclosures, barriers, silencers) are bulky, costly, and ineffective
- Performance depends on the **coherence** between reference and error signals: `NR_max(f) = -10·log₁₀[1 - γ²_xd(f)]`

### 2. Broad-Band Feedforward ANC (Section II)

- Uses a **reference sensor** placed upstream to pick up the noise before it reaches the cancellation zone
- The adaptive filter must simultaneously **model the primary path P(z)** and **inverse-model the secondary path S(z)**: `W(z) = P(z)/S(z)`
- The **secondary path** includes: D/A converter, reconstruction filter, power amplifier, loudspeaker, acoustic path, error microphone, preamplifier, antialiasing filter, A/D converter
- **Causality requirement**: The electrical delay must not exceed the acoustic delay from reference microphone to canceling loudspeaker. If violated, only narrow-band/periodic noise can be controlled

### 3. Filtered-X LMS Algorithm (Section II-C)

- The standard LMS algorithm becomes **unstable** when the secondary path S(z) is present because the error signal is not correctly "aligned" in time with the reference signal
- **FXLMS derivation**: The reference signal is filtered through the estimated secondary path Ŝ(z) before being used in the weight update
  ```
  x_f(n) = ŝ(n) * x(n)  (convolution)
  w(n+1) = w(n) + μ · e(n) · x_f(n)
  ```
- **Maximum step size**: `μ_max ≈ 2 / [Δ · P_xf]` where Δ is the overall delay in the secondary path and P_xf is the filtered reference signal power
- The algorithm can tolerate up to **~90° phase error** between S(z) and Ŝ(z) under slow adaptation
- Can be derived via offline modeling (initial training stage) or online adaptive modeling

### 4. Leaky FxLMS Algorithm (Section II-C.3)

- Addresses **high noise levels at low-frequency resonances** that may cause nonlinear distortion by overloading the secondary source
- Modified cost function: `J(n) = e²(n) + β·||w(n)||²`
- Update rule: `w(n+1) = (1 - μβ)·w(n) + μ·e(n)·x_f(n)`
- Benefits: stabilizes the algorithm, reduces numeric error in finite-precision implementation, guarantees unique solution
- Cost: introduces **bias** into the converged solution

### 5. Feedback Effects and Solutions (Section II-D)

**Acoustic feedback**: The antinoise radiates upstream to the reference microphone, corrupting the reference signal.

Solutions:
1. **Feedback neutralization**: Use a separate cancellation filter to subtract the estimated feedback component from the reference sensor signal (similar to acoustic echo cancellation). Must be done offline during ANC operation.
2. **Adaptive IIR filters**: The optimal solution with feedback is generally an IIR function. Uses the **filtered-U recursive LMS** algorithm. Lower order than FIR equivalent but stability concerns.
3. **Adaptive FIR with delayed-X**: Use a sufficiently high-order FIR filter with smaller step size for stability.

### 6. Narrow-Band Feedforward ANC (Section III)

- Uses **tachometer** or frequency estimator to generate reference signals (sine/cosine at fundamental frequencies)
- Reference signal is **not influenced** by the control field (no feedback problem)
- Algorithm: **Sinusoidal ANC (SANC)** — reference signals are `sin(kωn)` and `cos(kωn)` for each harmonic
- Can cancel multiple harmonics simultaneously by expanding the reference vector
- No secondary-path filtering needed when the secondary path is a pure delay (simplifies to standard LMS)

### 7. Adaptive Feedback ANC (Section IV)

- No reference sensor available; controller must work from the error signal alone
- **Internal Model Control (IMC)** structure: regenerates the reference signal using the secondary signal filtered by estimated secondary path: `x̂(n) = e(n) + ŝ(n) * y(n)`
- The IMC-based system acts as an **adaptive predictor** — performance depends on the predictability of the primary noise
- Stability condition: phase difference between S(z) and Ŝ(z) must be < 90°

### 8. Multi-Channel ANC (Section V)

- **Multiple Reference Inputs (MRI)**: Multiple reference sensors, single error sensor — e.g., multiple microphones upstream
- **Multiple-Channel Feedforward**: Multiple reference sensors, multiple secondary sources, multiple error sensors — uses the **multichannel FxLMS** algorithm
- The computational complexity grows as `O(M·L·N)` where M = secondary sources, L = filter length, N = error sensors
- For multi-channel, the reference signal must be filtered through each secondary path estimate to each error sensor

### 9. Online Secondary-Path Modeling (Section VI)

- Offline modeling (initial training) is insufficient when S(z) is **time-varying**
- Online methods add **modeling noise v(n)** to the system during operation to identify S(z) simultaneously with control
- Key challenge: the modeling noise interferes with noise cancellation; methods exist to minimize this interference

### 10. Special Algorithms (Section VII)

| Algorithm | Key Feature |
|-----------|-------------|
| **Lattice ANC** | Better numerical properties, orthogonal stages |
| **Frequency-domain ANC** | Efficient for long filters using FFT/overlap-save |
| **Subband ANC** | Decomposes signal into subbands for faster convergence |
| **RLS (Recursive Least Squares)** | Faster convergence than LMS but higher computation O(L²) |

### 11. Applications (Section VIII)

The paper highlights real-world applications in:
- **Automotive**: Electronic mufflers, passenger compartment noise, active engine mounts
- **Appliances**: Air-conditioning ducts, refrigerators, vacuum cleaners
- **Industrial**: Fans, ducts, transformers, compressors
- **Transportation**: Airplanes, helicopters, diesel locomotives
- **Duct noise cancellation**: Detailed example with experimental results

## Key Equations

| Description | Equation |
|-------------|----------|
| Error signal | `e(n) = d(n) + s(n) * y(n)` |
| Optimal controller | `W(z) = P(z)/S(z)` |
| FXLMS update | `w(n+1) = w(n) + μ·e(n)·x_f(n)` where `x_f(n) = ŝ(n) * x(n)` |
| Leaky FXLMS | `w(n+1) = (1-μβ)·w(n) + μ·e(n)·x_f(n)` |
| Max step size | `μ_max ≈ 2/(Δ·P_xf)` |
| Max NR (dB) | `-10·log₁₀[1 - γ²_xd(f)]` |

## Related Concepts

- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[../concepts/internal-model-control|Internal Model Control]]
- [[../concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[../concepts/broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[../concepts/narrow-band-feedforward-anc|Narrow-Band Feedforward ANC]]
- [[../concepts/multi-channel-anc|Multi-Channel ANC]]
- [[../concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[../concepts/acoustic-feedback|Acoustic Feedback]]

## Related Sources

- [[wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] — Builds on the IMC-based feedback structure described in this tutorial

## Related Synthesis
