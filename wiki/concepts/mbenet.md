---
type: concept
created: 2026-10-24
updated: 2026-10-24
sources:
  - wiki/sources/zhang-2025-mbenet.md
tags:
  - target-speaker-extraction
  - bone-conduction
  - multi-modal-fusion
  - band-split-rnn
  - multi-task-learning
---

# MBENet

**MBENet** (Multi-modal Bone-conduction Enhancement Network) is the first bone-conduction (BC) and air-conduction (AC) fusion model for [[concepts/target-speaker-extraction|target speaker extraction]] (TSE), proposed by Zhang et al. (ASRU 2025). It replaces the enrollment utterance used by conventional TSE systems with the BC signal — a noise-robust, target-speaker-only but band-limited observation — as the speaker cue, and introduces multi-task learning with BC bandwidth extension as an auxiliary task.

## Architecture

MBENet consists of three modules operating on STFT spectrograms (32 ms Hanning window, 8 ms hop, 16 kHz):

1. **Bone-conduction enhancement module** — a causal [[concepts/convolutional-recurrent-network|CRN]]-style encoder-decoder (3 causal conv layers {16, 32, 64} channels, GRU-64 bottleneck with FC to 1984-dim, 3 transposed-conv layers, dense skip connections, BN+ELU) that extends the bandwidth of the BC magnitude spectrogram; the enhanced magnitude is recombined with the original BC phase.
2. **Band-split fusion module** — AC spectrogram and enhanced BC spectrogram are each split into 31 subbands by a **shared-weight** [[concepts/band-split-rnn|band-split]] module (per-band linear + layer norm), stacked into tensors $\mathbf{Z}_a, \mathbf{Z}_b \in \mathbb{R}^{N \times K \times T}$ and concatenated.
3. **Mask extraction module** — 6 repeated dual-axis LSTM blocks (time-axis LSTM 64 units, then band-axis LSTM 64 units), followed by band merging (inverse of band split) producing a complex mask $\mathbf{M}$ applied to the AC spectrogram: $\hat{\mathbf{X}}_a = \mathbf{M} \odot \mathbf{Y}$.

The model is fully **causal** (causal convolutions, unidirectional RNNs), with 3.8 M parameters — the same count as the pBSRNN baseline.

## Multi-Task Learning: Bandwidth Extension as Auxiliary Task

The training objective combines the extraction loss with an auxiliary loss:

$$
\mathcal{L}_{hybrid} = \mathcal{L}_{sisdr} + \gamma \mathcal{L}_{mse}, \quad \gamma = 15
$$

where $\mathcal{L}_{sisdr}$ is the scale-invariant SDR loss on the final extracted waveform and $\mathcal{L}_{mse}$ is an MSE loss on the BC enhancement module's output magnitude against the **clean target speech** magnitude. The auxiliary task follows the [[concepts/blind-bandwidth-extension|blind bandwidth extension]] tradition (reconstructing wideband speech from band-limited BC input) but its output feeds cross-modal fusion rather than being the final product. Ablation: removing the BC enhancement module (MNet) costs +0.55 dB SI-SDR / 0.14 PESQ.

## Results on ABCS-2Mix

On the simulated ABCS-2Mix dataset (Mandarin AC-BC pairs from the ABCS corpus mixed with a competing speaker at SIR 0–2 dB plus MUSAN noise at SNR −5…10 dB), MBENet outperforms adapted baselines (CRN, SpEx+, MMINet, pBSRNN) on SI-SDR, PESQ, and DNSMOS at every SNR. Two structural findings:

- **BC cue ≫ enrollment-embedding cue in noise**: the AC-only MBENet with speaker-embedding clue reaches 11.19 dB SI-SDR / 2.68 PESQ; the BC-cue full model reaches 16.67 dB / 3.17.
- **Margin grows with noise**: PESQ improvement over pBSRNN rises from +2.74% at 10 dB to +6.03% at −5 dB — the BC modality's noise immunity matters most exactly where AC-only systems degrade.

## Significance

Prior BC-AC fusion work targeted speech enhancement; MBENet extends the paradigm to TSE, demonstrating that the BC channel is not only noise-robust (as in SE) but also **interference-speaker-robust** — the BC sensor captures only the wearer's/speaker's skull vibrations, filtering out competing talkers as well as ambient noise. This makes BC a natural "own-voice" cue, complementary to the enrollment, spatial, and visual clues surveyed in [[concepts/target-speaker-extraction|TSE]].

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[concepts/band-split-rnn|Band-Split RNN (BSRNN)]]
- [[concepts/blind-bandwidth-extension|Blind Bandwidth Extension]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/speaker-embedding|Speaker Embedding]]

## Related Sources

- [[sources/zhang-2025-mbenet|Zhang, Feng, Liu, Zhang & Li 2025: MBENet — Bone-Conduction and Air-Conduction Fusion Network for Target Speaker Extraction]]
