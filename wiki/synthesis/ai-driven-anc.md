---
type: synthesis
created: 2026-04-17
updated: 2026-08-21
tags:
- active-noise-control
- adaptive-filtering
- deep-learning
- generative-models
sources:
  - raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md
  - raw/papers/bai-2026-feedback-guided-anc/full-text.md
---
# AI-Driven Active Noise Control

> **Objective**: Synthesize the recent shift from classical adaptive filtering (FxLMS/FxNLMS) to deep-learning-based ANC strategies, focusing on hybrid architectures, neural noise selection, and generative control.

---

## 1. The Shift from Linear to Nonlinear ANC
Classical ANC (e.g., FxLMS) is inherently linear and relies on the stationary noise assumption. While robust in steady-state environments, it struggles with:
- **Dynamic/Non-stationary noise**: Slow convergence of adaptive steps leads to "noise leakage" during transitions.
- **Nonlinear distortions**: Present in low-cost speakers or high-SPL scenarios where the linear superposition principle fails.

Deep learning approaches move toward **data-driven ANC**, formulating the problem as supervised learning where a network (e.g., CRN) encodes optimal control parameters for diverse environments.

---

## 2. Key Architectural Shifts

### 2.1 Selective Fixed-Filter ANC (SFANC)
SFANC pre-trains a library of filters and selects the most appropriate one in real-time.
- **Neural Selection**: Modern implementations use Convolutional Neural Networks (CNNs) for selection.
    - **1D CNN**: Lightweight, operates directly in the time domain for ultra-low latency on hearables ([XS7Z5XTN](zotero://select/items/XS7Z5XTN)).
    - **2D CNN**: Spectrogram-based classification, often offloaded to a mobile co-processor for higher accuracy ([XS7Z5XTN](zotero://select/items/XS7Z5XTN)).
- **The Hybrid Edge**: The **SFANC-FxNLMS** hybrid ([MKAWB86B](zotero://select/items/MKAWB86B)) uses a CNN for instant coarse filter selection and an FxNLMS kernel for fine-grained steady-state adaptation, combining speed with precision.
- **Non-Neural Selection**: **FRM-SFANC** (Yin et al. 2023) uses online frequency response matching instead of CNNs to select filters. It estimates the primary path frequency response in real time and compares it against pre-trained filter profiles. This approach requires no training data or neural network inference, making it suitable for resource-constrained embedded platforms. The method is formally derived from a hidden Markov model framework where the optimal control filter is the hidden state and the reference signal is the observation.

### 2.2 Generative Fixed-Filter ANC (GFANC)
Unlike SFANC which is limited by its pre-trained library, **GFANC** ([UCJR5KDZ](zotero://select/items/UCJR5KDZ)) uses a generative model and a perfect-reconstruction filter bank to synthesize custom control filters from minimal prior data (e.g., a single broadband filter). This allows for better generalization to untrained, dynamic noises.

### 2.3 Deep ANC (Spectrogram Domain)
**Deep ANC** ([EPKYEGUP](zotero://select/items/EPKYEGUP)) employs a **Convolutional Recurrent Network (CRN)** to estimate the complex spectrograms (real and imaginary parts) of the anti-noise signal.
- **Nonlinear Handling**: Successfully attenuates noise in the presence of nonlinear distortions where linear FxLMS diverges.
- **Delay Compensation**: Uses specialized training strategies to handle the causality constraints and latency of real-time audio buffers.
- **Speech Preservation**: Dai 2026 extends Deep ANC with a [[concepts/speech-preserving-anc|speech-preserving loss function]] that algebraically cancels speech components, training the network to selectively cancel noise while leaving speech transparent. Validated in reverberant environments (RT60=0.3s) with 10-15 dB improvement over FxLMS at harmonic frequencies.

### 2.4 Joint Deep SPE + Adaptive Control
Fareedha et al. (2026) propose an end-to-end framework that jointly estimates the secondary path and generates adaptive control signals. Unlike SFANC/GFANC which assume a fixed secondary path, **DeepSPE** (Conv1D + BiLSTM + Attention) predicts $\hat{S}(z)$ in real time at frame level (32 ms), achieving −16.27 dB NMSE — 3.92 dB better than the best classical method. The estimated path conditions an **ANC-Net** controller that uses SE blocks and temporal attention to generate binary weights for selecting sub-control filters from a pre-trained bank. The dual-stream design achieves −12.38 dB NMSE with only 1.05 M parameters and 0.43 ms latency, outperforming ResNet50 (23.5 M params, 2.6 ms) and DenseNet121 (7.98 M params, 2.2 ms).

### 2.5 Feedback-Guided Controller Fusion (Bai 2026)
A fourth architectural pattern beyond selection, generation, and joint SPE+control: **feedback-guided fusion of pre-trained per-path experts**. [[concepts/feedback-guided-controller-fusion|Bai et al. 2026]] observe that SFANC, GFANC, and DeepSPE all determine the controller from **reference-side features** (input-noise characteristics or estimated secondary path) — none directly reflects the *actual control outcome* under the current acoustic system. Their framework closes this loop by driving a gating network with reference $\mathbf{x}(n)$ + control $\mathbf{y}(n)$ + **delayed residual-error** $\mathbf{e}(n-1)$ signals to dynamically fuse $N$ pre-trained FIR experts (one per acoustic path) with a WaveNet baseline. The delayed-error signal is causal: $\mathbf{e}(n)$ becomes available only after $\mathbf{y}(n)$ propagates through the secondary path. This introduces a **new axis of comparison** for AI-driven ANC: *what signals drive the controller-selection/generation mechanism* — reference-only (SFANC/GFANC/DeepSPE) vs. reference + control + delayed-error (Bai 2026).

The fusion is $\mathbf{y}(n) = \alpha\, \mathbf{y}_W(n) + (1-\alpha)\, \mathbf{y}_M(n)$, exploiting the same FF+FB complementarity as classical [[concepts/hybrid-anc|hybrid ANC]]: the WaveNet branch stabilizes high-frequency behavior (mitigating the MoE-only branch's amplification on certain paths), while the MoE branch substantially improves low-frequency reduction on path outliers. Training is staged (WaveNet → per-path FIR experts → frozen-backbone gating network with cross-entropy path-label auxiliary), and the [[concepts/frequency-aware-anc-loss|frequency-aware ANC loss]] jointly optimizes one-third-octave-band NR, high-frequency rebound, and broadband NMSE.

**Empirical result**: On the CCF-AATC headphone ANC dataset, the 10-expert streaming model achieves **19.00 dB avg NR (50 Hz–5 kHz) with negligible 1–8 kHz amplification**, with stable reduction across condition switches (no convergence time).

---

## 3. The Efficiency Frontier: Real-Time Implementation

The primary hurdle for AI-driven ANC is the computational cost of deep networks on low-power DSPs.

| Strategy | Computational Load | Primary Benefit | Target Device |
|----------|-------------------|-----------------|---------------|
| **1D CNN Selection** | Low | Fast response to dynamic noise | TWS Earbuds |
| **FRM-SFANC** | Very Low | No training data needed; interpretable | Embedded ANC |
| **Hybrid SFANC-FxNLMS** | Moderate | High steady-state reduction | High-end Headphones |
| **CRN Spectrogram** | High | Handles nonlinear distortion | Smart Speakers/Mobile |
| **Feedback-guided MoE fusion** (Bai 2026) | Moderate (672.83 MMac/s, 28.57k params) | Robust to acoustic-path mismatch; no online adaptation; 19 dB avg NR (50 Hz–5 kHz) | Headphones |

### 3.1 Neural Stability and Robustness
Recent research focuses on using RNNs as "stability observers." By predicting the innovative whiteness of the error signal, the network can dynamically adjust the step-size of a traditional FxLMS filter, preventing divergence during impulsive events without the full overhead of an end-to-end neural controller.

---

## Related Synthesis

- [[computational-efficiency-evolution]]
- [[impulsive-noise-control]]
- [[nonlinear-anc-approaches]]

## Related Concepts

- [[concepts/active-noise-control]]
- [[concepts/filtered-x-lms-algorithm]]
- [[concepts/deep-learning-for-signal-processing]]
- [[concepts/secondary-path-modeling]]
- [[concepts/deep-secondary-path-estimation]]

## Related Sources

- [[sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]]
- [[sources/fareedha-2026-joint-deep-spe-anc|Fareedha 2026: Joint Deep SPE and Adaptive Control for ANC]]
- [[sources/wang-2026-predictive-dsfanc-crnn|Wang 2026: Predictive Directional SFANC via CRNN]]
- [[sources/yin-2023-selective-fixed-filter-anc-headphones|Yin 2023: Selective Fixed-Filter ANC Based on Frequency Response Matching in Headphones]]
- [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement|Tan & Wang 2018: CRN for Real-Time Speech Enhancement (original CRN proposal)]]
- [[sources/jiang-2025-ai-driven-avnc-review|Jiang et al. 2025: AI-Driven AVNC Review]] — comprehensive review classifying AI-AVNC into four technical paths
