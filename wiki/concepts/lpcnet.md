---
type: concept
created: 2026-08-14
updated: 2026-08-30
sources:
  - raw/papers/valin-2022-real-time-plc/full-text.md
  - raw/papers/valin-2018-lpcnet/full-text.md
  - raw/papers/valin-2024-fargan/full-text.md
tags:
  - neural-vocoder
  - speech-synthesis
  - lpcnet
  - low-complexity
  - real-time
  - autoregressive
---

# LPCNet

**LPCNet** is an autoregressive neural speech vocoder that improves on [[concepts/wavernn|WaveRNN]] by incorporating [[concepts/linear-prediction|linear prediction]]. Introduced by [[entities/jean-marc-valin|Jean-Marc Valin]] and [[entities/jan-skoglund|Jan Skoglund]] ([[sources/valin-2018-lpcnet|ICASSP 2019]]), it splits synthesis into a frame-rate network operating on acoustic features at 100 Hz and a sample-rate network that autoregressively generates 16 kHz speech samples conditioned on the frame-rate network's output. The central idea: the spectral envelope (vocal-tract response) is produced by a classical all-pole LPC filter derived from the conditioning cepstrum, so the network only has to model the spectrally flat *excitation* — matching WaveRNN-class quality with far fewer neurons, at under 3 GFLOPS for speaker-independent synthesis.

## Architecture

- **Frame-rate network** — operates at 100 Hz on acoustic feature vectors. The original LPCNet uses two 3×1 convolutional layers (receptive field of 5 frames: two *ahead* of the synthesized frame, two back), whose output is added to a residual connection and passed through two fully-connected layers, producing a **128-dimensional conditioning vector** $\mathbf{f}$ that is held constant throughout each 10-ms frame. The two-frame look-ahead improves synthesis quality at the cost of 25 ms added algorithmic latency; for real-time / packet-loss-concealment use, a strictly causal variant (no look-ahead) is used.
- **Sample-rate network** — autoregressively generates 16 kHz samples of the *excitation* (prediction residual), not the speech signal itself. Inputs per sample are $\mu$-law embeddings of the previous excitation $e_{t-1}$, the past signal $s_{t-1}$, and the LPC prediction $p_{t-1}$, plus the per-frame contributions $\mathbf{g}^{(\cdot)}=\mathbf{U}^{(\cdot)}\mathbf{f}$ precomputed once per frame. The main GRU ($\mathrm{GRU_{A}}$: 384 units in the original, [[concepts/structured-sparsity|block-sparse]] with 16×1 blocks at 10% density) feeds a small dense $\mathrm{GRU_{B}}$ (16 units) in place of the fully-connected layer, then a [[concepts/dual-fc-layer|DualFC]] layer and a softmax over 256 $\mu$-law levels produce $P(e_t)$. The sample is reconstructed as $s_t = p_t + e_t$ and passed through the de-emphasis filter $D(z)=1/(1-0.85z^{-1})$. The improved low-complexity variant (Valin, Isik, Smaragdis & Krishnaswamy, ICASSP 2022) reduces the $\mathrm{GRU_{A}}$ to 640 units at 15% density while meeting real-time constraints on a laptop CPU.
- **LPC filter** — the predictor $p_t=\sum_k a_k s_{t-k}$ is computed each frame from the 18-band Bark cepstrum (→ PSD → auto-correlation → Levinson-Durbin), so the all-pole synthesis filter carries the entire spectral envelope — see [[concepts/linear-prediction|Linear Prediction]].

### Acoustic Features

Each 10-ms synthesized speech segment corresponds to the center of a 20-ms analysis window (5 ms algorithmic delay). The feature vector per frame contains:

- **18 Bark-frequency cepstral coefficients (BFCCs)** — a [[concepts/bark-scale-spectral-features|Bark-scale]] cepstral representation of the spectral envelope
- **Pitch period** (always present, even for unvoiced frames — hence noisy)
- **Pitch correlation** (a periodicity measure; cf. [[concepts/pitch-coherence|pitch coherence]] in PercepNet)

## Efficiency Techniques

Beyond the LPC/DNN division of labor itself, the original paper introduces several mechanisms that together bring speaker-independent synthesis under 3 GFLOPS:

- **Pre-emphasis before $\mu$-law quantization** — a first-order filter $E(z)=1-0.85z^{-1}$ applied to the training data (inverted at the output) shapes the quantization noise for a 16 dB power reduction at Nyquist, making 8-bit $\mu$-law viable for 16 kHz synthesis and halving the output-distribution size versus 16-bit WaveRNN.
- **$\mu$-law embeddings with precomputed products** — each of the 256 $\mu$-law levels maps to a learned embedding (which, inspected after training, encodes the $\mu$-law-to-linear conversion among other functions); the products of the embedding matrices with the GRU's non-recurrent weight submatrices are precomputed (9 $\mathbf{V}^{(\cdot,\cdot)}$ matrices), reducing every non-recurrent input to one add per gate.
- **[[concepts/dual-fc-layer|DualFC]] output layer** — two tanh fully-connected layers combined by an element-wise weighted sum, each implementing roughly one "comparison" for $\mu$-law interval membership.
- **Sampling rule** — a continuous temperature $c=1+\max(0,1.5g_p-0.5)$ driven by pitch correlation, plus a probability threshold $T=0.002$ that zeroes low-probability tails to prevent impulse noise.
- **CELP-like training noise injection** — noise added in the $\mu$-law domain (varied from none up to uniform $[-3,3]$), with the prediction filter applied to the *noisy, quantized* input and a *clean* excitation target, so the network effectively minimizes signal-domain error — an analysis-by-synthesis effect that avoids pre-AbS vocoder artifacts.

## Use in Packet Loss Concealment

In [[sources/valin-2022-real-time-plc|Valin et al. 2022]], LPCNet is the generative backbone of a hybrid PLC architecture: a predictive RNN estimates the LPCNet feature vectors during loss, and LPCNet synthesizes the missing samples. This decouples short-time sample synthesis from long-time spectral-trajectory control, addressing the drift problem of purely autoregressive PLC.

Key adaptations for PLC:

- **Causal feature model** — the original 2-frame look-ahead is removed because future features are unavailable during loss.
- **Sign randomization in training** — the sign of each training sequence is explicitly randomized so the algorithm works for any polarity of the speech signal.
- **State seeding from known samples** — before synthesis, the LPCNet state is updated using known samples $\left[t-15\,\mathrm{ms},t-5\,\mathrm{ms}\right]$ alongside the most recent features, so the autoregressive model is conditioned on actual preceding audio.

## Complexity

The original model totals **≈2.8 GFLOPS** ($N_A=384$ sparse units at 10% density, $N_B=16$, $Q=256$ $\mu$-law levels at 16 kHz, including ≈0.5 GFLOPS of neglected terms) — versus ~10 GFLOPS estimated for the sparse mobile WaveRNN, ~16 GFLOPS for FFTNet, and ~50 GFLOPS estimated for SampleRNN. This enables real-time synthesis on a single Apple A8 (iPhone 6) core or on 20% of a 2.4 GHz Intel Broadwell core. In MUSHRA listening tests, LPCNet significantly exceeds an equivalent-complexity WaveRNN+ baseline (all improvements except LPC), confirming that the linear-prediction split — not the auxiliary tricks alone — drives the gain.

LPCNet also dominates the complexity of the Valin 2022 PLC system; the feature-prediction RNN contributes less than 20% of the total. On an Intel i7-10810U laptop CPU, steady-state (known frame $K$ or unknown frame $U$) processing of a 10-ms frame takes 1.34–1.38 ms, i.e. 13–14% of one CPU core.

## Successor: FARGAN

[[concepts/fargan|FARGAN]] ([[sources/valin-2024-fargan|Valin, Mustafa & Büthe 2024]]) keeps LPCNet's 20-dimensional Bark-cepstral feature set (18 BFCCs + pitch period, with a voicing indicator in place of the pitch correlation) but replaces essentially everything else: the all-pole **LPC filter is dropped**, short-term linear prediction giving way to [[concepts/pitch-prediction|long-term pitch prediction]] as an explicit second autoregressive feedback, and the density-estimation softmax training gives way to adversarial training with no [[concepts/exposure-bias|teacher forcing]]. The result is 600 MFLOPS versus LPCNet's ≈2.8 GFLOPS with significantly higher PESQ/P.808 quality. The paper also reports that earlier attempts to add direct pitch prediction to LPCNet failed — attributed to teacher forcing, since pitch prediction is acutely sensitive to the ground-truth/synthesized history mismatch. FARGAN replaced LPCNet as the DRED redundancy vocoder in Opus 1.5, cutting synthesis complexity 5×.

## Distinction from PercepNet

LPCNet and [[concepts/percepnet|PercepNet]] are sibling Valin-lab hybrid DSP/DNN real-time systems, both sharing the low-complexity, perceptually-motivated design philosophy:

- **LPCNet** (2019) — neural *vocoder* for sample-level waveform synthesis. Bark-scale cepstral features condition an autoregressive sample-rate network.
- **PercepNet** (2020/2021) — neural *post-filter* for speech enhancement and acoustic echo cancellation. ERB-scale (32-band) features condition a DNN that predicts per-band gains and comb-filter strengths.

LPCNet generates speech samples; PercepNet filters an existing noisy/echoed signal. They share the [[entities/jean-marc-valin|Valin]] / [[entities/arvindh-krishnaswamy|Krishnaswamy]] / [[entities/paris-smaragdis|Smaragdis]] authorship line and the hybrid-DSP/DNN design pattern, but operate at different stages of the speech pipeline.

## Related Concepts

- [[concepts/wavernn|WaveRNN]] — the base architecture LPCNet extends
- [[concepts/linear-prediction|Linear Prediction]] — supplies the spectral envelope so the network models only the excitation
- [[concepts/dual-fc-layer|DualFC Layer]] — the output layer introduced with LPCNet
- [[concepts/structured-sparsity|Structured Sparsity]] — 16×1 block-sparse $\mathrm{GRU_{A}}$ with retained diagonal
- [[concepts/packet-loss-concealment|Packet Loss Concealment]] — primary application of LPCNet in Valin 2022
- [[concepts/percepnet|PercepNet]] — sibling Valin-lab hybrid system for speech enhancement / AEC
- [[concepts/fargan|FARGAN]] — successor vocoder: same features, pitch prediction instead of LPC, adversarial training
- [[concepts/pitch-prediction|Pitch Prediction]] — the long-term feedback that replaced LPCNet's short-term predictor
- [[concepts/exposure-bias|Teacher Forcing and Exposure Bias]] — the structural training limitation of LPCNet-class vocoders
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — LPCNet's 18 BFCC inputs
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]] — backbone of the sample-rate network
- [[concepts/opus-codec|Opus Audio Codec]] — codec integration context for PLC

## Related Sources

- [[sources/valin-2018-lpcnet|Valin & Skoglund 2018: LPCNet]] — the original paper: architecture, efficiency techniques, complexity analysis, and MUSHRA evaluation
- [[sources/valin-2022-real-time-plc|Valin et al. 2022: Real-Time Packet Loss Concealment With Mixed Generative and Predictive Model]] — uses the improved low-complexity LPCNet variant with causal features
