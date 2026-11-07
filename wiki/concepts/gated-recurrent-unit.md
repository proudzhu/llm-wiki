---
type: concept
created: 2026-07-18
updated: 2026-11-07
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
  - raw/papers/li-2026-realtime-music-separation-dsp/full-text.md
  - raw/papers/valin-2018-lpcnet/full-text.md
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
  - raw/papers/zhang-2021-adl-mvdr/full-text.md
  - raw/papers/westhausen-2022-tplcnet/full-text.md
  - raw/papers/perez-2018-film-visual-reasoning/full-text.md
  - raw/papers/yan-2025-lisennet/full-text.md
  - raw/papers/ahn-2026-fastenhancer/full-text.md
  - raw/papers/kim-2026-faster-enhancer/full-text.md
  - raw/papers/laroche-2026-lisenet-embedded/full-text.md
tags:
  - deep-learning
  - recurrent-neural-network
  - gated-network
  - efficiency
---

# Gated Recurrent Unit (GRU)

The **Gated Recurrent Unit (GRU)** is a recurrent neural network architecture introduced by Cho et al. (2014) as a simplified alternative to [[concepts/long-short-term-memory\|LSTM]]. GRUs combine the forget and input gates into a single **update gate** and merge the cell state and hidden state, reducing the number of parameters while maintaining comparable performance.

## Architecture

The GRU has two gates — the update gate $\mathbf{z}_t$ and the reset gate $\mathbf{r}_t$ — and updates its hidden state as:

$$
\mathbf{z}_t = \sigma(\mathbf{W}_{xz}\mathbf{x}_t + \mathbf{W}_{hz}\mathbf{h}_{t-1} + \mathbf{b}_z), \tag{1}
$$

$$
\mathbf{r}_t = \sigma(\mathbf{W}_{xr}\mathbf{x}_t + \mathbf{W}_{hr}\mathbf{h}_{t-1} + \mathbf{b}_r), \tag{2}
$$

$$
\mathbf{h}_t' = \tanh(\mathbf{W}_{xh}\mathbf{x}_t + \mathbf{r}_t \odot (\mathbf{W}_{hh}\mathbf{h}_{t-1}) + \mathbf{b}_h), \tag{3}
$$

$$
\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \mathbf{h}_t', \tag{4}
$$

where $\mathbf{z}_t$ is the update gate, $\mathbf{r}_t$ is the reset gate, and $\mathbf{h}_t'$ is the candidate hidden state.

## Gate Roles

- **Update gate** $\mathbf{z}_t$: determines how much of the previous hidden state $\mathbf{h}_{t-1}$ to carry forward to the current hidden state $\mathbf{h}_t$.
- **Reset gate** $\mathbf{r}_t$: controls how much of the previous hidden state to forget when computing the candidate hidden state.

## Comparison with LSTM

GRUs have fewer parameters than LSTM due to the absence of a separate cell state and the combined gating mechanism. This typically leads to faster training times. Studies cited in [[sources/mienye-2024-rnn-comprehensive-review\|Mienye et al. 2024]] show that GRUs can achieve performance comparable to LSTM, making them attractive when computational resources are limited or faster training is needed. The choice between GRU and LSTM depends on the specific task and dataset.

## Applications

- **Sentiment analysis** — Zulqarnain et al. 2024 used GRU with attention mechanisms
- **Machine translation** — Zulqarnain et al. 2024 used GRU in multi-stage feature attention
- **Time-series forecasting** — Chen et al. 2024 used bidirectional GRU with temporal convolutional networks (TCNs)
- **Decision-making** — Liu & Diao 2024 used GRU with deep RL for autonomous driving

Within the llm-wiki, GRU is the recurrent backbone in:
- [[concepts/lpcnet\|LPCNet]] (Valin & Skoglund 2018) — two-stage vocoder: block-sparse $\mathrm{GRU_{A}}$ (384 units, 16×1 blocks at 10% density) plus dense $\mathrm{GRU_{B}}$ (16 units) replacing the output fully-connected layer
- [[concepts/percepnet\|PercepNet]] (Valin et al. 2021) — 5-layer GRU neural post filter
- [[concepts/nsnet2\|NSNet2]] — FC+GRU speech enhancement baseline
- [[concepts/dtln\|DTLN]] — dual-path GRU for low-latency speech enhancement
- [[concepts/tplcnet\|tPLCnet]] (Westhausen & Meyer 2022) — two **bidirectional** GRU layers over a short context buffer predict an entire lost 10 ms frame in one shot (seq2one); the final BGRU hidden state condenses the whole buffer into the frame prediction
- [[concepts/convolutional-recurrent-network\|CRN]] — CNN+GRU for speech enhancement
- [[concepts/mingru\|MinGRU]] — minimal gated GRU variant
- [[concepts/hyst-net\|HyST-Net]] (Zhao & Madhu 2026) — GRU chosen for the *temporal* axis of the interleaved bottleneck precisely for its compact recurrent state: causal MHA with key-value caching costs memory/compute linear in context length, non-trivial for lightweight streaming on edge devices, while the GRU state stays constant (RTF 0.22 in strict frame-by-frame CPU streaming)
- [[concepts/adl-mvdr|ADL-MVDR]] (Zhang et al. 2021) — two GRU-Nets *replace the matrix operations* of the MVDR solution: one regresses the steering vector (in place of PCA on the speech covariance), the other the inverse noise covariance (in place of matrix inversion), recursively accumulating statistics across frames. This revives the classical result that RNNs can solve matrix inversion in real time (Wang 1993; Zhang & Ge 2005) inside a modern end-to-end speech-separation system, and is what makes joint training with the front-end stable where closed-form inversion was not.
- [[concepts/tfc-tdf-unet|TFC-TDF U-Net]] (Li et al. 2026) — GRU recurrence chosen over LSTM for *indefinite streaming stability*: the GRU state $h_t = (1-z_t)h_{t-1} + z_t\tilde{h}_t$ is a convex combination of bounded terms and stays in $[-1,1]$ by construction, whereas an LSTM cell state is an unbounded running sum (measured growing 399→962 over 120 s with no plateau), eventually saturating downstream activations and forcing periodic resets that reintroduce buffering latency. Six GRUs cost 4.37 ms of the 10.43 ms frame budget on the target DSP, and the state stays 32-bit float because it is an accumulator carried indefinitely.
- [[concepts/film-layer|FiLM]] (Perez et al. 2018) — the FiLM generator that conditions a CNN on a question is a GRU with 4096 hidden units over 200-d word embeddings; its final hidden state is affine-projected to per-layer $(\gamma, \beta)$ modulation parameters. An early example of a GRU as a *conditioning encoder* rather than a sequence-to-sequence backbone

## Related Concepts

- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]
- [[concepts/vanishing-gradient-problem\|Vanishing Gradient Problem]]
- [[concepts/backpropagation-through-time\|Backpropagation Through Time]]
- [[concepts/mingru\|MinGRU]] — minimal gated GRU variant
- [[concepts/lisennet|LiSenNet]] — frequency-Bi-GRU + temporal-uni-GRU dual-path bottleneck
- [[concepts/rnnformer|RNNFormer]] (Ahn et al. 2026) — GRU as the *time axis* of FastEnhancer's dual-path bottleneck, chosen for streaming: its constant-size state avoids the key-value caching that time-axis MHSA would need (ablation: DPT variant with 31-frame lookbehind is far slower despite fewer params). The frequency axis uses MHSA instead — the inverse of LiSenNet's frequency-GRU choice, with the RTF/SISDR curve favoring RNNFormer.
- [[concepts/faster-enhancer-c|faster-enhancer.c]] (Kim 2026) — the GRU's deployment profile from the systems side: it is the top per-frame compute bucket (82.2 µs of ~452 µs) in the int8 runtime port of FastEnhancer-Medium, so its two matrices + three gates + hidden update + fp16 state write are fused into one kernel per SIMD tier; the hidden state deliberately stays fp16 because int8 state would lose ~40 dB SNR through the decoder concat

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]]
- [[sources/valin-2018-lpcnet\|Valin & Skoglund 2018: LPCNet]] — sparse $\mathrm{GRU_{A}}$ + dense $\mathrm{GRU_{B}}$ vocoder backbone
- [[sources/valin-2021-percepnet-joint-echo-control\|Valin et al. 2021: PercepNet]] — GRU-based AEC system
- [[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel et al. 2024: Bark-AEC]] — NSNet2-style FC+GRU post filter
- [[sources/zhao-2026-spectrally-adaptive-loss\|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — GRU as temporal axis of HyST-Net's hybrid bottleneck
- [[sources/yan-2025-lisennet\|Yan, Zhang, Fan, Zhou & Liu 2025: LiSenNet]] — causal dual-path bottleneck pairs a frequency-axis Bi-GRU (hidden 12) with a unidirectional temporal GRU (hidden 24) plus a [[concepts/convglu|ConvGLU]] channel mixer; N = 2 repetitions is the ablation's efficiency sweet spot
- [[sources/zhang-2021-adl-mvdr\|Zhang et al. 2021: ADL-MVDR]] — GRU-Nets replace matrix inversion and PCA inside the MVDR solution, reviving classical RNN matrix-inversion results (Wang 1993; Zhang & Ge 2005) in an end-to-end speech separator
- [[sources/li-2026-realtime-music-separation-dsp\|Li, Liu, Malsky & Yi 2026: Real-Time Music Source Separation on a Low-Power Audio DSP]] — GRU state bounded in $[-1,1]$ by construction for indefinite streaming on a DSP (vs. LSTM's unbounded cell state); state stays 32-bit float because it is an accumulator carried indefinitely
- [[sources/westhausen-2022-tplcnet\|Westhausen & Meyer 2022: tPLCnet — Real-Time Deep Packet Loss Concealment in the Time Domain]] — bidirectional-GRU seq2one PLC; triggered on demand at loss time only
- [[sources/perez-2018-film-visual-reasoning\|Perez, Strub, de Vries, Dumoulin & Courville 2018: FiLM: Visual Reasoning with a General Conditioning Layer]] — GRU question encoder (4096 units) as the FiLM generator: final hidden state projected to per-layer (γ, β) feature-modulation parameters
- [[sources/ahn-2026-fastenhancer\|Ahn, Han, Woo & Kim 2026: FastEnhancer]] — GRU as the time axis of the RNNFormer dual-path block; beats time-axis MHSA on streaming RTF in ablation
- [[sources/kim-2026-faster-enhancer\|Kim 2026: faster-enhancer.c]] — fused single-kernel int8 GRU with fp16 state; top compute bucket in the runtime's profile
- [[sources/laroche-2026-lisenet-embedded\|Laroche & Olsson 2026: Beyond Model Size]] — the temporal GRU *can* run on an MCU NPU (hidden state as graph I/O, affine transforms as dense ops) but is replaced by a dilated TCN in the primary model: FIFO state flushes quantization errors out of the receptive field, whereas quantized recurrent state can accumulate them (and drift over long streams); the GRU variant is still the faster/lighter-state option (2.18 ms/frame, 17 KiB vs. 4.83 ms, 154 KiB)
