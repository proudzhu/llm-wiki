---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
tags:
  - deep-learning
  - recurrent-neural-network
  - lstm-variant
  - gating
---

# Peephole LSTM

**Peephole LSTM** is a variant of [[concepts/long-short-term-memory\|LSTM]] introduced by Gers and Schmidhuber (2000) that enhances the standard architecture by allowing the gates to have direct access to the cell state through **peephole connections**. This additional connection enables the LSTM to better regulate its gating mechanisms based on the current cell state, improving timing decisions.

## Architecture

In standard LSTM, gates see only the input $\mathbf{x}_t$ and previous hidden state $\mathbf{h}_{t-1}$. In Peephole LSTM, the gates additionally see the cell state $\mathbf{c}_{t-1}$ (or $\mathbf{c}_t$ for the output gate):

$$
\mathbf{i}_t = \sigma(\mathbf{W}_{xi}\mathbf{x}_t + \mathbf{W}_{hi}\mathbf{h}_{t-1} + \mathbf{W}_{ci}\mathbf{c}_{t-1} + \mathbf{b}_i), \tag{1}
$$

$$
\mathbf{f}_t = \sigma(\mathbf{W}_{xf}\mathbf{x}_t + \mathbf{W}_{hf}\mathbf{h}_{t-1} + \mathbf{W}_{cf}\mathbf{c}_{t-1} + \mathbf{b}_f), \tag{2}
$$

$$
\mathbf{o}_t = \sigma(\mathbf{W}_{xo}\mathbf{x}_t + \mathbf{W}_{ho}\mathbf{h}_{t-1} + \mathbf{W}_{co}\mathbf{c}_t + \mathbf{b}_o), \tag{3}
$$

where $\mathbf{W}_{ci}$, $\mathbf{W}_{cf}$, $\mathbf{W}_{co}$ are the **peephole weights** connecting the cell state to the input, forget, and output gates respectively. Note that the output gate uses the *current* cell state $\mathbf{c}_t$ (after the cell update), while the input and forget gates use the *previous* cell state $\mathbf{c}_{t-1}$.

## Rationale

The peephole connections allow gates to make decisions based on the full internal state of the cell, not just the output-exposed hidden state. This is particularly useful for tasks requiring precise timing, such as:
- Speech recognition
- Financial time series prediction
- Recognition of complex temporal patterns (e.g., musical notation)

## Applications

Per [[sources/mienye-2024-rnn-comprehensive-review\|Mienye et al. 2024]], Peephole LSTM is listed alongside standard LSTM, GRU, BiLSTM, ESN, and IndRNN as a notable RNN variant (Table 2 of the review). It offers stable gradient flow similar to standard LSTM, with the added benefit of cell-state-aware gating.

## Related Concepts

- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]
- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/bidirectional-lstm\|Bidirectional LSTM]]
- [[concepts/gated-recurrent-unit\|Gated Recurrent Unit (GRU)]]

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]] — surveys peephole LSTM as one of the notable RNN variants
