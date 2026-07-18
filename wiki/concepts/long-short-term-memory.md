---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
tags:
  - deep-learning
  - recurrent-neural-network
  - gated-network
  - long-term-dependency
---

# Long Short-Term Memory (LSTM)

**Long Short-Term Memory (LSTM)** is a recurrent neural network architecture introduced by Hochreiter and Schmidhuber (1997) to address the [[concepts/vanishing-gradient-problem\|vanishing gradient problem]] that plagues basic [[concepts/recurrent-neural-network\|RNNs]]. The key innovation is the use of **gating mechanisms** to control the flow of information through the network, allowing LSTM to maintain and update its internal cell state over long periods.

## Architecture

Each LSTM cell contains three gates — input $\mathbf{i}_t$, forget $\mathbf{f}_t$, output $\mathbf{o}_t$ — that regulate the cell state $\mathbf{c}_t$ and hidden state $\mathbf{h}_t$:

$$
\mathbf{i}_t = \sigma(\mathbf{W}_{xi}\mathbf{x}_t + \mathbf{W}_{hi}\mathbf{h}_{t-1} + \mathbf{b}_i), \tag{1}
$$

$$
\mathbf{f}_t = \sigma(\mathbf{W}_{xf}\mathbf{x}_t + \mathbf{W}_{hf}\mathbf{h}_{t-1} + \mathbf{b}_f), \tag{2}
$$

$$
\mathbf{o}_t = \sigma(\mathbf{W}_{xo}\mathbf{x}_t + \mathbf{W}_{ho}\mathbf{h}_{t-1} + \mathbf{b}_o), \tag{3}
$$

$$
\mathbf{g}_t = \tanh(\mathbf{W}_{xg}\mathbf{x}_t + \mathbf{W}_{hg}\mathbf{h}_{t-1} + \mathbf{b}_g), \tag{4}
$$

$$
\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \mathbf{g}_t, \tag{5}
$$

$$
\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t), \tag{6}
$$

where $\sigma$ is the sigmoid function, $\tanh$ is the hyperbolic tangent, $\odot$ is element-wise multiplication, and $\mathbf{g}_t$ is the candidate cell input.

## Gate Roles

- **Input gate** $\mathbf{i}_t$: controls how much of the new input is written to the cell state.
- **Forget gate** $\mathbf{f}_t$: decides how much of the previous cell state to retain.
- **Output gate** $\mathbf{o}_t$: determines how much of the cell state is exposed as the hidden state.

The cell state $\mathbf{c}_t$ acts as a "conveyor belt" transferring relevant information across time steps. The element-wise multiplications between gates and inputs ensure smooth, stable gradient flow, mitigating the vanishing gradient problem.

## Variants

- **[[concepts/bidirectional-lstm\|Bidirectional LSTM (BiLSTM)]]** — processes the sequence in both forward and backward directions, capturing both past and future context.
- **Stacked LSTM** — stacks multiple LSTM layers; lower layers capture local patterns, higher layers capture abstract long-term dependencies.
- **[[concepts/peephole-lstm\|Peephole LSTM]]** — gates have direct access to the cell state via peephole connections, improving timing decisions.

## Comparison with GRU

LSTM has more parameters (three gates + cell input) than the [[concepts/gated-recurrent-unit\|GRU]] (two gates, merged cell/hidden state). This gives LSTM more expressive power but slower training. In practice, GRU often achieves comparable performance with fewer parameters; the choice depends on the task and dataset.

## Applications

Per [[sources/mienye-2024-rnn-comprehensive-review\|Mienye et al. 2024]], LSTM is identified as the most effective RNN variant for:
- **Text generation** (robust sequence modeling, fewer compute resources than transformers)
- **Speech recognition** (DeepSpeech, DeepSpeech2 — long-range temporal dependencies in audio)
- **Time-series forecasting** (financial markets, weather, renewable energy)
- **Bioinformatics** (DNA/RNA/protein sequence analysis — BiLSTM preferred for full-context tasks)

Within the llm-wiki, LSTM is the recurrent backbone in:
- [[concepts/percepnet\|PercepNet]] (Valin et al. 2021) — original used GRU, but the broader PercepNet family includes LSTM variants
- [[concepts/grouped-recurrent-neural-network\|Grouped RNN]] — grouped LSTM layers in MN-TANGO
- [[concepts/dprnn\|DPRNN]] — dual-path LSTM for source separation

## Related Concepts

- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/gated-recurrent-unit\|Gated Recurrent Unit (GRU)]]
- [[concepts/bidirectional-lstm\|Bidirectional LSTM]]
- [[concepts/peephole-lstm\|Peephole LSTM]]
- [[concepts/vanishing-gradient-problem\|Vanishing Gradient Problem]]
- [[concepts/backpropagation-through-time\|Backpropagation Through Time]]
- [[concepts/activation-functions\|Activation Functions]]
- [[concepts/grouped-recurrent-neural-network\|Grouped Recurrent Neural Network]]

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]] — comprehensive review including LSTM architecture and applications
- [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement\|Tan & Wang 2018: CRN for Speech Enhancement]] — uses LSTM as recurrent layer in CRN
- [[sources/benslimane-2026-tango-quantized-distributed\|Benslimane et al. 2026: Quantized TANGO]] — grouped LSTM for efficient speech enhancement
