---
type: concept
created: 2026-07-18
updated: 2026-09-06
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
  - raw/papers/valin-2018-lpcnet/full-text.md
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
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
- [[concepts/convolutional-recurrent-network\|CRN]] — CNN+GRU for speech enhancement
- [[concepts/mingru\|MinGRU]] — minimal gated GRU variant
- [[concepts/hyst-net\|HyST-Net]] (Zhao & Madhu 2026) — GRU chosen for the *temporal* axis of the interleaved bottleneck precisely for its compact recurrent state: causal MHA with key-value caching costs memory/compute linear in context length, non-trivial for lightweight streaming on edge devices, while the GRU state stays constant (RTF 0.22 in strict frame-by-frame CPU streaming)

## Related Concepts

- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]
- [[concepts/vanishing-gradient-problem\|Vanishing Gradient Problem]]
- [[concepts/backpropagation-through-time\|Backpropagation Through Time]]
- [[concepts/mingru\|MinGRU]] — minimal gated GRU variant

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]]
- [[sources/valin-2018-lpcnet\|Valin & Skoglund 2018: LPCNet]] — sparse $\mathrm{GRU_{A}}$ + dense $\mathrm{GRU_{B}}$ vocoder backbone
- [[sources/valin-2021-percepnet-joint-echo-control\|Valin et al. 2021: PercepNet]] — GRU-based AEC system
- [[sources/seidel-2024-bark-scale-nn-residual-suppression|Seidel et al. 2024: Bark-AEC]] — NSNet2-style FC+GRU post filter
- [[sources/zhao-2026-spectrally-adaptive-loss|Zhao & Madhu 2026: Spectrally Adaptive Loss for Streaming Speech Enhancement]] — GRU as temporal axis of HyST-Net's hybrid bottleneck
