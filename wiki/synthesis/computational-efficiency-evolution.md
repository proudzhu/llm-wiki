---
type: synthesis
created: 2026-04-12
updated: 2026-07-21
sources:
- zotero://select/items/0_WLMRLH9W
- zotero://select/items/0_5SFJK2MD
- zotero://select/items/0_76XGXYSM
- zotero://select/items/0_N8MHRKXP
- zotero://select/items/0_BACCUUCC
- zotero://select/items/0_TXVFFJPG
- zotero://select/items/0_FN59JY3C
- zotero://select/items/0_NUV4VYRE
tags:
  - lightweight-speech-enhancement
- computational-complexity
- efficiency
- fast-rls
- gpu-dsp
- nonlinear-filtering
- memory-efficiency
- real-time-systems
- recurrent-neural-networks
- quantization
- model-compression
aliases:
- Computational and Memory Efficiency in Adaptive Systems
---

# Computational Efficiency in ANC: From O(N²) to GPU-Accelerated DSP

> Cross-source synthesis connecting: Cioffi & Kailath (1984) fast RLS, Li & Chen (2023) FxLMS complexity survey, Spanio & Rodà (2025) TorchFX GPU DSP, Zhao & Chen (2023) nonlinear adaptive filters, and Rong et al. (2024) GTCRN ultralightweight speech enhancement.

---

## The Shifting Bottleneck

Over 40 years, the computational bottleneck in ANC has shifted three times:

| Era | Bottleneck | Solution | Key Papers |
|-----|-----------|----------|-----------|
| **1980s-1990s** | Per-sample FLOPs (RLS = $O(N^2)$) | Fast RLS, lattice filters | Cioffi & Kailath (1984) |
| **2000s-2020s** | Filter length $L$ (long secondary paths) | Subband, delayed update, reduced-order | Li & Chen (2023) survey |
| **2020s+** | Developer productivity + nonlinearity | GPU DSP, neural controllers | Spanio & Rodà (2025), Zhao & Chen (2023) |

Each era redefined what "efficient" means.

---

## 1. The Fast RLS Era (1980s)

### The Problem

Standard RLS (Recursive Least Squares) requires $O(N^2)$ multiplications per sample for a filter of length $N$. In 1984, this was prohibitive: DSP chips had ~1-5 MIPS capability.

### Cioffi & Kailath (1984)

**Key contribution**: Reduced RLS from $O(N^2)$ to $O(N)$ using:
- **Fast transversal filter structure**: Exploits the shift-invariance of the input data matrix
- **Lattice formulation**: Numerically stable recursive update of reflection coefficients

**Algorithm structure**:
```
Forward prediction error ──→ Reflection coefficient update ──→ Backward prediction error
                              ↓
                        Kalman gain update (O(N) instead of O(N²))
                              ↓
                        Filter coefficient update
```

**Why it mattered**: RLS converges 10× faster than LMS but was $N$× more expensive. Fast RLS made it feasible for real-time ANC with $N < 100$.

**Why it faded**: Fast RLS is numerically unstable in finite precision — small rounding errors accumulate and cause divergence. LMS, while slower, is robust.

---

## 2. The FxLMS Complexity Era (2000s-2020s)

### The Survey

Li & Chen (2023) surveyed 40 years of FxLMS complexity reduction techniques:

| Technique | Complexity Reduction | NR Degradation | Best For |
|-----------|---------------------|----------------|----------|
| **Delayed update** | $O(L/P)$ where $P$ = update period | < 1 dB ($P \leq 4$) | Broadband ANC |
| **Subband processing** | $O(L/S)$ where $S$ = number of subbands | 1-3 dB | Wideband noise |
| **Reduced-order filter** | $O(L_{reduced})$ where $L_{reduced} \ll L$ | 2-5 dB | Low-frequency dominant |
| **Lookup table (narrow-band)** | $O(1)$ per harmonic | < 0.5 dB | Tonal noise (engine, fan) |
| **Frequency-domain block processing** | $O(L \log L / B)$ where $B$ = block size | < 1 dB | Long filters ($L > 512$) |

### The Trade-off Surface

All complexity reduction techniques face the same trade-off:

```
NR (dB)
  ▲
  │  Full FxLMS
  │  (O(L), baseline)
  │
  │        Delayed update
  │        (O(L/P), < 1 dB loss)
  │
  │            Subband
  │            (O(L/S), 1-3 dB loss)
  │
  │                Reduced-order
  │                (O(L_reduced), 2-5 dB loss)
  │
  └─────────────────────────────────► Complexity (MIPS)
```

### Key Design Rules (from the Survey)

1. **For narrow-band noise** (tonal): Use lookup table — $O(1)$ per harmonic, negligible NR loss
2. **For broadband noise with long secondary path** ($L > 512$): Use frequency-domain block processing — $O(L \log L / B)$
3. **For broadband noise with short secondary path** ($L < 256$): Use delayed update — simplest, least NR loss
4. **For wideband noise across multiple octaves**: Use subband processing — independent optimization per band

---

## 3. The GPU DSP Era (2020s+)

### Spanio & Rodà (2025): TorchFX

**Core idea**: Implement audio DSP pipelines using PyTorch + GPU acceleration rather than hand-optimized C code.

```
PyTorch DSP Pipeline:
    Input audio ──→ torch.fft() ──→ Frequency-domain processing ──→ torch.ifft() ──→ Output
                       ↓
                  GPU-accelerated (CUDA)
                       ↓
                  Batch processing (frames of audio)
```

**Why this matters for ANC**:
- **Developer productivity**: DSP algorithms expressed in high-level PyTorch, not fixed-point C
- **GPU parallelism**: Batch-process multiple channels simultaneously
- **Differentiable DSP**: Gradients flow through the entire pipeline — enables end-to-end optimization of ANC controllers

**Limitations for ANC**:
- **Latency**: GPU kernel launch overhead (~100-500 μs) exceeds ANC latency budgets (< 1 ms for 48 kHz)
- **Batch processing**: GPU works on blocks of audio, introducing algorithmic delay
- **Power consumption**: GPU is impractical for battery-powered ANC (earbuds, glasses)

**Where it fits**: Offline training of ANC controllers, multi-channel ANC on powered systems (vehicle, room), research prototyping.

---

## 4. The Nonlinear Filtering Era

### Zhao & Chen (2023): Nonlinear Adaptive Filters

The book covers four families of nonlinear adaptive filters applicable to ANC:

| Filter Type | Complexity | Nonlinearity Model | Best For |
|-------------|-----------|-------------------|----------|
| **Volterra filter** | $O(N^P)$ where $P$ = order | Polynomial expansion | Mild nonlinear distortion |
| **Kernel filter** | $O(N \cdot M)$ where $M$ = kernel size | Reproducing kernel Hilbert space | Arbitrary nonlinearities |
| **Spline filter** | $O(N \cdot K)$ where $K$ = spline knots | Piecewise polynomial | Smooth nonlinearities |
| **Subband nonlinear** | $O(L/S \cdot P^2)$ | Nonlinearity per subband | Wideband nonlinear noise |

### The Complexity Explosion

Nonlinear filters are exponentially more expensive than linear ones:

| Filter | Multiplications/sample | Example: $N=64$ |
|--------|----------------------|-----------------|
| Linear FIR | $N$ | 64 |
| 2nd-order Volterra | $N + N^2/2$ | 2,080 |
| 3rd-order Volterra | $N + N^2/2 + N^3/6$ | 45,760 |
| Kernel (Gaussian, $M=32$) | $N \cdot M$ | 2,048 |
| Spline ($K=8$ knots) | $N \cdot K$ | 512 |

**Practical implication**: Nonlinear ANC is only feasible with complexity reduction (subband, reduced-order, or GPU acceleration).

---

## 5. The Complete Efficiency Landscape

### 5.1 Algorithm × Complexity × NR

| Algorithm | Complexity | NR (Gaussian) | NR (Impulsive) | NR (Nonlinear) |
|-----------|-----------|---------------|----------------|----------------|
| FxLMS (full) | $O(L)$ | 20-25 dB | 5-8 dB (unstable) | 10-15 dB |
| FxLMS (delayed) | $O(L/P)$ | 19-24 dB | 5-8 dB | 10-15 dB |
| FxLMS (subband) | $O(L/S)$ | 18-23 dB | 5-8 dB | 10-15 dB |
| FxLMS (frequency-domain) | $O(L \log L / B)$ | 20-25 dB | 5-8 dB | 10-15 dB |
| FxRLS | $O(L^2)$ | 25-30 dB | 8-12 dB | 15-20 dB |
| Fast FxRLS | $O(L)$ | 25-30 dB | 8-12 dB | 15-20 dB |
| FxGMCC | $O(L) + \text{kernel}$ | 20-23 dB | 18-22 dB | 15-20 dB |
| Nonlinear FxLMS (Volterra) | $O(L^2)$ | 22-27 dB | 8-12 dB | 20-25 dB |
| MPC (closed-form) | $O(N_{state}^2)$ | 22-26 dB | 10-15 dB | 15-20 dB |

### 5.2 The 2026 Efficiency Frontier

Three approaches currently define the Pareto frontier:

1. **Subband FxLMS**: Best balance of complexity and NR for broadband noise
2. **FxGMCC**: Best robustness to impulsive noise at moderate complexity
3. **GPU-accelerated TorchFX**: Best for research/prototyping, not yet for embedded deployment
4. **GTCRN (Rong et al. 2024)**: Neural speech enhancement at extreme efficiency — only 23.7 K parameters and 39.6 MMACs/s, outperforming RNNoise and matching models with 100× more parameters. Represents the lightweight deep learning frontier for edge-device audio processing.
5. **[[sources/schroter-2022-deepfilternet|DeepFilterNet (Schröter et al., ICASSP 2022)]]**: Two-stage deep filtering framework with 1.8M params and 0.35 GMACs/s, achieving WB-PESQ 2.81 at 48 kHz full-band. Serves as the key baseline for GTCRN and subsequent ultralightweight models.
6. **[[concepts/mn-tango|MN-TANGO (Benslimane et al., 2026)]]**: A hybrid neural-spatial distributed binaural SE system that exploits a unique structural prior — the downstream [[concepts/gevd-spatial-filtering|GEVD-based]] spatial filter absorbs most quantization-induced mask errors — to push neural compression to extremes. Combining architectural simplification (single-stage MN-TANGO, 0.5 M params / 30.79 MMAC/s vs. 1.0 M / 65.65 for full TANGO), [[concepts/quantization-aware-training|W8A8 QAT]], [[concepts/erb-scale|ERB]] compression, and [[concepts/grouped-recurrent-neural-network|grouped LSTM]] ($G=8$), it reaches **4.65 MMAC/s and 0.177 MB** — a 14× compute reduction and 23× memory reduction relative to the FP32 TANGO baseline, with final SI-SIR still at 21.2/21.3 dB. The key insight is that **hybrid neural-spatial architectures are quantization-robust by construction**, opening a compression axis unavailable to purely neural SE models.
7. **[[concepts/cofi-lite|CoFi-Lite (Yang et al., IEEE SPL 2026)]]**: Pushes the *purely neural* ultra-lightweight SE frontier below GTCRN — **12.87M MACs/s and 83.12k params** while *outperforming* GTCRN (PESQ 2.16 vs. 2.07 on DNS3) at 40.26% of its compute and 34% lower RTF. The mechanism is **asymmetric capacity reallocation** rather than uniform slimming: a deeply compressed coarse path (×16, ERB-merged full-band envelope) paired with a nearly uncompressed fine path (×2, low frequencies below 2 kHz), bridged by a lightweight [[concepts/cross-path-fusion|Cross-Path Fusion]] module (+0.14 PESQ in ablation). Its scaled-up variant matches AdaptCRN with 19.34% fewer MACs. Complementary to MN-TANGO's quantization axis: CoFi-Lite shows architectural decoupling alone can still halve the compute of the previous best design.

### 5.3 The Open Question

**Can neural/learned ANC controllers match traditional algorithms at lower computational cost?**

Yuan et al. (2026) showed that a neural network + DSP hybrid pipeline achieves competitive NR (9.6-11.2 dB) with 113 μs DSP latency. But the neural component (200ms update cycle) is too slow for real-time adaptation. The next frontier may be **learned controllers that are compiled to efficient DSP code** — combining the expressiveness of neural networks with the latency of hand-optimized filters.

---

## 6. Memory Bottlenecks in Temporal Processing

Memory efficiency is often the first constraint hit in real-time streaming data.

### 6.1 The "Time" Dimension

- **BPTT (Backpropagation Through Time)**: Memory scales $O(T)$ linearly with sequence length because the entire hidden state trajectory must be stored.
- **Forward Error Propagation (FEP)**: Zucchet et al. (2026) show that by propagating gradients forward, we can achieve memory complexity independent of sequence length $T$. This is a game-changer for streaming data where $T$ is theoretically infinite.

### 6.2 The "State" Dimension ($N$)

- **RNN/State-Space Models**: Complexity for exact gradient computation (RTRL) is $O(N^4)$ memory (or $O(N^3)$ optimized).
- **Approximation**: Strategies like diagonal connectivity approximations (xLSTM, Linear Recurrent Units) reduce memory to $O(N)$, enabling scaling to larger models.

## 7. The 2026 Efficiency Frontier

As we move toward multi-modal platforms (e.g., ANC + awareness + gaze-guided input), efficiency is increasingly handled through **structural priors**:

- **Linearization**: Moving toward "linear-recurrent" or "state-space" structures (LRU, state-space models) inherently reduces the computational cost of gradient calculation compared to non-linear RNNs.
- **Event-Driven/Adaptive Rate**: Running resource-intensive modules (like virtual error estimators) at lower sample rates than the primary audio loop.
- **Hardware-Algorithm Co-Design**: Algorithms like FEP are being designed for streaming, analog-compatible flows, where the memory bottleneck of storing hidden states is fundamentally removed.

---

## Related Concepts

- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/frequency-domain-anc|Frequency-Domain ANC]]
- [[concepts/subband-anc|Subband ANC]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]
- [[concepts/generalized-maximum-correntropy-criterion|Generalized Maximum Correntropy Criterion]]
- [[concepts/model-predictive-control|Model Predictive Control]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/state-space-model|State-Space Model]]
- [[concepts/backpropagation-through-time|Backpropagation Through Time]]
- [[concepts/real-time-recurrent-learning|Real-Time Recurrent Learning]]
- [[concepts/linear-recurrent-unit|Linear Recurrent Unit]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/quantization-aware-training|Quantization-Aware Training (QAT)]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/gevd-spatial-filtering|GEVD-Based Spatial Filtering]]

## Related Sources

- [[sources/fujii-2006-simultaneous-equations-anc|Fujii et al. 2006: Verification of Simultaneous Equations Method]] — Frequency-domain processing for the simultaneous equations method, reducing computational cost vs. time-domain NLMS-based transformation
- [[sources/rong-2024-gtcrn-speech-enhancement-ultralow|Rong et al. 2024: GTCRN — A Speech Enhancement Model Requiring Ultralow Computational Resources]]
- [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement|Yang et al. 2026: CoFi-Lite — Pushing the Limits of Ultra-Lightweight Speech Enhancement]] — asymmetric coarse/fine-path decoupling beats GTCRN at 40% of its compute (12.87M MACs/s)
- [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement|Tan & Wang 2018: CRN for Real-Time Speech Enhancement (original CRN proposal)]]
- [[sources/schroter-2022-deepfilternet|Schröter et al. 2022: DeepFilterNet — Low Complexity Speech Enhancement via Deep Filtering]]
- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]] — Hybrid neural-spatial robustness to INT8 quantization; 14× compute / 23× memory reduction vs. FP32 TANGO
