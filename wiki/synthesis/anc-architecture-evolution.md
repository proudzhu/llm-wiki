---
type: synthesis
created: 2026-04-12
updated: 2026-05-17
sources:
  - zotero://select/items/0_QVJMFTWC
  - raw/papers/kuo-2006-anc-headphones/full-text.txt
tags:
  - anc-architecture
  - feedback
  - feedforward
  - hybrid
  - imc
  - mvc
---

# ANC Architecture Evolution: Feedforward → Feedback → Hybrid

> Cross-source synthesis connecting [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]], [[sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]], [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]], and [[sources/benois-2020-hybrid-pseudo-cascaded-anc-headphones|Benois 2020: Hybrid and Pseudo-Cascaded ANC for Headphones]].

---

## The Core Trade-off: Reference Signal Availability

All ANC architectures are defined by a single question: **can you measure the noise before it reaches the cancellation zone?**

| Architecture | Reference Signal? | When to Use | Key Limitation |
|-------------|-------------------|-------------|----------------|
| **Feedforward** | Yes (upstream microphone) | Ducts, predictable noise sources | Requires physical access to upstream location |
| **Feedback** | No (error sensor only) | Headsets, enclosed spaces | Performance depends on noise predictability |
| **Hybrid** | Both | Complex environments | Increased complexity and cost |

This fundamental constraint drives all subsequent design decisions.

---

## 1. Feedforward ANC (Kuo 1999)

The standard architecture described in [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]:

```
Primary noise ──→ Reference mic ──→ FxLMS controller ──→ Secondary speaker
                        ↓                                       ↓
                   x(n) filtered                            Anti-noise
                        ↓                                       ↓
                  ┌──────────────────────────────────────────────┘
                  ↓
             Cancellation zone ──→ Error mic ──→ e(n) ──→ FxLMS update
```

**FxLMS update**:
$$w(n+1) = w(n) + \mu \cdot e(n) \cdot x_f(n)$$

Where $x_f(n) = \hat{s}(n) * x(n)$ is the reference signal filtered through the estimated secondary path.

**Why FxLMS, not LMS?** The secondary path $S(z)$ between speaker and error mic introduces phase shifts that make standard LMS unstable. FxLMS accounts for this by filtering the reference signal through $\hat{S}(z)$ before the update.

**Performance**: 10-25 dB noise reduction for predictable (narrow-band) noise. Limited by:
- Causality constraint (anti-noise must arrive before primary noise)
- Secondary path estimation accuracy
- Acoustic feedback (anti-noise radiating upstream to reference mic)

---

## 2. Feedback ANC (Pawelczyk 1997)

When no upstream reference is available (e.g., headphones), we must synthesize the reference from the error signal alone.

### 2.1 Internal Model Control (IMC)

The IMC structure regenerates the reference signal:
$$\hat{x}(n) = e(n) + \hat{s}(n) * y(n)$$

This transforms the feedback system into an equivalent feedforward configuration, allowing FxLMS to be used. However:
- **Computational cost**: The convolution $\hat{s}(n) * y(n)$ requires $O(L_{\hat{S}})$ multiplications per sample, where $L_{\hat{S}}$ is the secondary path filter length (often 256-1024 taps)
- **Compatibility**: Off-the-shelf feedforward FxLMS controllers cannot be used directly — the reference signal synthesis requires custom hardware/software

### 2.2 MVC (Minimum Variance Control)

[[sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]] also describes MVC-based feedback: the controller minimizes the variance of the error signal directly, without IMC's reference synthesis. This requires solving optimization problems and is vulnerable to changing conditions.

### 2.3 Simplified Adaptive Feedback (Wu 2014)

[[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] eliminates IMC's convolution by using the error signal **directly** as the reference:
$$x_{sa}(n) = e(n)$$

This trades noise reduction performance (3-5 dB less than IMC-based systems) for:
- **Eliminating the convolution** entirely
- **Enabling direct use** of commercial FxLMS controllers
- **Lower computational load** suitable for DSP implementation

**The fundamental insight**: For many practical ANC scenarios, the performance loss from dropping IMC is acceptable given the simplicity gain.

### 2.4 The Complete Hardware Benchmark (Kuo, Mitra & Gan 2006)

[[sources/kuo-2006-anc-headphones|Kuo, Mitra & Gan 2006]] is the canonical real-time instantiation of IMC-based AFANC on headphones: a Sennheiser HD 565 modified with one error mic per ear-cup, a 65-tap $\hat{S}(z)$ (step 0.05) for reference synthesis, a 110-tap FxLMS control filter ($\mu=0.3$), assembly-coded on a TMS320C32 at 8 kHz. It achieved 50+ dB sinusoidal cancellation up to 2 kHz and 16–27 dB on 2200/3700 rpm engine harmonics — beating a Bose QuietComfort 2, dramatically so at low frequencies (20.9 vs 0.7 dB at 61 Hz; 25.6 vs 7.0 dB at 116 Hz), which is exactly the band where commercial feedforward-heavy designs leave headroom. Two design lessons generalize beyond the architecture choice:
1. **Flatten the secondary path before adapting** — the error microphone is placed (of eight candidates) where $|S(e^{j\omega})|$ has the fewest dips and peaks (near the external auditory meatus, guided by pinna spectral filtering), because $W^{opt}(z) = P(z)/S(z)$ is unstable wherever $|S| \approx 0$; that location also matched the KEMAR ear-canal response, the perceptual target.
2. **Music as identification excitation** — the 65-tap $\hat{S}(z)$ can be identified with spectrally dense music ("O Fortuna", near-flat 0–4 kHz) as accurately as with white noise or chirp, removing the audible-calibration annoyance that Route 1 of [[secondary-path-modeling-evolution|Secondary Path Modeling Evolution]] accepts as its cost.

---

## 3. Hybrid ANC (Benois 2020)

[[sources/benois-2020-hybrid-pseudo-cascaded-anc-headphones|Benois 2020: Hybrid and Pseudo-Cascaded ANC for Headphones]] demonstrates that **neither feedforward nor feedback alone is optimal** for headphones:

| Scenario | Feedforward alone | Feedback alone | Hybrid |
|----------|------------------|----------------|--------|
| Low-frequency broadband noise | Good (predictable) | Poor (unpredictable) | Best |
| Mid-frequency tonal noise | Good | Good | Best |
| High-frequency noise | Poor (causality limit) | Poor (phase limit) | Moderate |
| Changing acoustic conditions | Requires re-tuning | Self-adapting | Best of both |

### Three-Stage Hybrid Architecture

Benois proposes combining **all three** approaches:
1. **Feedforward** (FF) — primary noise cancellation using upstream reference
2. **Minimum Variance Control** (MVC) — feedback cancellation for low frequencies
3. **Internal Model Control** (IMC) — feedback cancellation with reference synthesis

The **pseudo-cascaded** implementation processes them sequentially rather than in parallel, reducing computational complexity while maintaining performance.

**Modified Normalized FxLMS (N-FxLMS)** is used for adaptation, with a two-stage optimization procedure.

### 3.1 Spatially Constrained Hybrid (Xiao 2023)

Hybrid architecture evolution does not stop at combining FF/IMC/MVC — [[sources/xiao-2023-spatially-selective-anc|Xiao, Xu & Zhao 2023]] add a **spatial dimension**: a Frost-type linear constraint (built from relative impulse responses) imposed on the hybrid ANC cost function so that sound from a desired direction is *physically preserved* ($e_s(n)=s(n)$) while noise from undesired directions is minimized. This decouples the architecture question (which references to use) from the *selectivity* question (what to cancel): on a six-microphone AR-glasses array it achieves NR 29.1 dB with SDI −25.1 dB, using only ~2% of the secondary-source energy of cancel-and-reconstruct schemes. See [[concepts/spatially-selective-anc|Spatially Selective ANC]].

---

## 4. Cross-Architecture Algorithm Comparison

| Architecture | Primary Algorithm | Adaptive? | Computational Cost | Performance |
|-------------|-------------------|-----------|-------------------|-------------|
| Feedforward | [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] | Yes | $O(L_x + L_{\hat{S}})$ | 10-25 dB |
| Feedback (IMC) | IMC + [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] | Yes | $O(L_x + 2L_{\hat{S}})$ | 8-20 dB |
| Feedback (Simplified) | [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] (error as reference) | Yes | $O(L_x)$ | 5-15 dB |
| Feedback (MVC) | RLS / Optimal control | Yes (offline) | $O(N_{state}^2)$ | 8-18 dB |
| Hybrid (FF+IMC+MVC) | Modified N-FxLMS | Yes | $O(L_x + 3L_{\hat{S}} + N_{state}^2)$ | 15-30 dB |

---

## 5. Key Design Principles

### 5.1 When to Use Each Architecture

1. **Feedforward**: When you can place a reference microphone upstream of the cancellation zone (ducts, industrial noise sources)
2. **Feedback**: When the noise source is internal or inaccessible (headphones, enclosed spaces)
3. **Hybrid**: When maximum performance is needed and computational resources allow (premium headphones, aircraft cabins)

### 5.2 The Computational Bottleneck

The convolution with $\hat{S}(z)$ dominates computation in IMC-based systems. [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]] shows this can be eliminated entirely. [[sources/benois-2020-hybrid-pseudo-cascaded-anc-headphones|Benois 2020: Hybrid and Pseudo-Cascaded ANC for Headphones]] shows it can be managed through pseudo-cascaded processing.

### 5.3 The Stability Trade-off

All adaptive ANC systems face the same stability constraint: the phase error in $\hat{S}(z)$ must be < 90° for convergence. This limits the bandwidth over which adaptive feedback ANC can operate. Feedforward ANC is less sensitive to this because the reference signal is physically measured rather than synthesized.

---

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]
- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[concepts/broad-band-feedforward-anc|Broad-Band Feedforward ANC]]
- [[concepts/narrow-band-feedforward-anc|Narrow-Band Feedforward ANC]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/acoustic-feedback|Acoustic Feedback]]
- [[concepts/frequency-domain-anc|Frequency-Domain ANC]]
- [[concepts/subband-anc|Subband ANC]]
- [[concepts/model-predictive-control|Model Predictive Control]]

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
- [[sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]]
- [[sources/wu-2014-simplified-adaptive-feedback-anc|Wu 2014: Simplified Adaptive Feedback ANC]]
- [[sources/benois-2020-hybrid-pseudo-cascaded-anc-headphones|Benois 2020: Hybrid and Pseudo-Cascaded ANC for Headphones]]
- [[sources/liang-2026-delayed-mpc-anc-paper-reading-note|Liang 2026: Delayed MPC for ANC Paper Reading Note]]
- [[sources/wills-2008-mpc-constraint-handling-anc-avc|Wills 2008: MPC Constraint Handling in ANC/AVC]]
- [[sources/fujii-2006-simultaneous-equations-anc|Fujii et al. 2006: Verification of Simultaneous Equations Method]] — Secondary-path-model-free feedforward ANC architecture using an auxiliary filter
- [[sources/xiao-2023-spatially-selective-anc|Xiao, Xu & Zhao 2023: Spatially Selective Active Noise Control Systems]] — Frost-type spatial constraint on hybrid ANC: preserve desired-direction sound instead of cancel-and-reconstruct
- [[sources/kuo-2006-anc-headphones|Kuo, Mitra & Gan 2006: Active Noise Control System for Headphone Applications]] — complete IMC-based AFANC headphone on TMS320C32; error-mic placement to flatten $|S(z)|$ and music-based secondary-path identification
