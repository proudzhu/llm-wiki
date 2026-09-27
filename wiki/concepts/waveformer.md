---
type: concept
created: 2026-09-27
updated: 2026-09-27
sources:
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
tags:
  - target-sound-extraction
  - neural-network
  - transformer
  - realtime-processing
---

# Waveformer

**Waveformer** (Veluri et al., ICASSP 2023) is a streaming neural network architecture for real-time [[concepts/target-sound-extraction|target sound extraction]] conditioned on a one-hot class query. It is an encoder–decoder mask-estimation network: a convolution-based encoder builds context over past chunks, and a transformer decoder generates the target-sound mask. The original Waveformer is single-channel, was demonstrated in real time only on a desktop computer, and was evaluated solely on synthetic data.

## Architecture

- **Encoder**: Wavenet-style stack of dilated causal convolutions processed with the Fast Wavenet dynamic-programming algorithm, so a 1–1.5 s past-only receptive field is maintained without reprocessing history each chunk.
- **Decoder**: transformer decoder conditioned on a label embedding of the query vector.
- **Latent masking**: an input 1D convolution maps time-domain audio to a latent space; the estimated mask is applied there; a transposed convolution reconstructs audio. (Time-domain latent masking avoids an STFT and its window-induced latency.)

## Binaural Extension (Veluri et al. 2023)

The semantic-hearing network modifies Waveformer for [[concepts/binaural-target-sound-extraction|binaural target sound extraction]]:

- **Same dimensionality for encoder and decoder** — Waveformer's smaller decoder dimensionality required projection layers that break residual paths (mitigated by a long residual connection); the binaural version drops both, at no performance loss.
- **Joint dual-channel processing** — both ears share one latent representation and one mask estimator, halving compute vs running Waveformer per ear (240 vs 357 MFLOPS) and cutting runtime from 25.85 ms to 6.56 ms (D=128), enabling smartphone-class real-time operation.

## Related Concepts

- [[concepts/target-sound-extraction|Target Sound Extraction]]
- [[concepts/binaural-target-sound-extraction|Binaural Target Sound Extraction]]
- [[concepts/semantic-hearing|Semantic Hearing]]

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
