---
type: concept
created: 2026-08-31
updated: 2026-08-31
sources:
  - raw/papers/mustafa-2023-framewise-wavegan/full-text.md
tags:
  - neural-vocoder
  - speech-synthesis
  - gan
  - low-complexity
  - real-time
  - framewise-wavegan
---

# Framewise WaveGAN

**Framewise WaveGAN (FWGAN)** is a GAN vocoder introduced by [[entities/ahmed-mustafa|Mustafa]], [[entities/jean-marc-valin|Valin]], [[entities/jan-buthe|Büthe]], [[entities/paris-smaragdis|Smaragdis]] and [[entities/mike-goodwin|Goodwin]] ([[sources/mustafa-2023-framewise-wavegan|ICASSP 2023]]) that generates 16 kHz speech directly in the time domain **one 10-ms frame at a time**, so every model parameter runs at the 100 Hz acoustic-feature rate instead of the 16 kHz signal rate. Built only from GRUs and fully-connected layers — no WaveNet stacks, no upsampling transposed convolutions — it brought adversarial (GAN) vocoding down to **1.2 GFLOPS**, at which point it significantly outperformed the autoregressive maximum-likelihood [[concepts/lpcnet|LPCNet]] at equal complexity and slightly beat LPCNet at 3 GFLOPS in P.808 listening tests, with clearly better pitch consistency (PMAE/VDE). It is the direct predecessor of [[concepts/fargan|FARGAN]].

## Key Formulations

**Complexity of feature-rate models.** Because all parameters run once per conditioning step ($S = 100$ steps/s), the FLOPS cost is

$$
C = N \cdot 2 \cdot S,
$$

with $N$ the parameter count (one multiply + one accumulate per parameter per step). A 7.8M-parameter dense FWGAN therefore costs 1.5 GFLOPS; after [[concepts/structured-sparsity|sparsification]] (GRU density 0.6, FC density 0.65, last three FC layers dense) 5.9M active parameters cost **1.2 GFLOPS**. By contrast, a WaveNet-based GAN vocoder uses every parameter at $f_s = 16\,000$ — even 1.44M-parameter Parallel WaveGAN costs 46 GFLOPS.

**Framewise tensor organization.** All activations are tensors of $[\text{Batch}, \text{Sequence\_dim}, \text{Frame\_dim}]$: Sequence_dim equals the acoustic-feature resolution *everywhere* in the model, and Frame_dim holds the 160-sample frame being generated; the waveform is the flattened sequence of frames. This is the architectural alternative to latent-based vocoders' stack of upsampling layers.

**Architecture** (generator): a conditioning network on [[concepts/lpcnet|LPCNet]] features (18 [[concepts/bark-scale-spectral-features|BFCCs]] + pitch period embedding + pitch correlation → 256-dim representation); a recurrent stack of 5 [[concepts/gated-recurrent-unit|GRUs]] for long-term dependencies; and a stack of [[concepts/framewise-convolution|framewise convolutions]] (1 non-conditional with kernel 3 frames + 4 conditional with kernel 2 frames) for short-term dependencies. All layers use $GLU(X)=X\otimes\sigma(FC(X))$ activation with biases disabled. Total algorithmic delay: 25 ms.

**Training recipe** — the key to stable framewise adversarial generation:

1. Train in the **perceptual domain** (pre-emphasis + AMR-WB weighting filter $W(z)$, $\gamma_1=0.92$, $\gamma_2=0.85$) for faster convergence and output-shaped artifact noise.
2. **Spectral pre-training** (1M steps) with the Parallel WaveGAN multi-resolution STFT loss over six power-of-two FFT sizes 64–2048, $sqrt$ non-linearity — producing a metallic but useful prior.
3. **Spectral adversarial training** (1M steps) with six UnivNet-style multi-resolution **spectrogram** discriminators under a least-squares GAN objective, keeping the spectral loss as regularizer. Time-domain discriminators (MelGAN / StyleMelGAN / HiFi-GAN styles) all *failed to train stably* on the framewise generator — a finding later reused by [[concepts/fargan|FARGAN]].

## Results and Limits

- 20× real-time on CPU (Xeon Platinum 8175M), 75× on V100 (PyTorch).
- **Quality does not scale with complexity**: the 1.5- and 3-GFLOPS FWGAN variants could not outperform the 1.2-GFLOPS model, attributed to weaker discriminator behavior against larger generators — motivating better discriminators rather than bigger generators.
- FWGAN has no explicit pitch structure; FARGAN added [[concepts/pitch-prediction|pitch prediction]] and 2.5-ms subframes to reach 0.6 GFLOPS with higher quality.

## Related Concepts

- [[concepts/framewise-convolution|Framewise Convolution]] — the frame-element kernel the generator is built from
- [[concepts/fargan|FARGAN]] — successor adding pitch-prediction autoregression at 2.5-ms granularity
- [[concepts/lpcnet|LPCNet]] — feature source and the quality/complexity baseline it beat
- [[concepts/frequency-domain-loss|Frequency Domain Loss]] — the multi-resolution STFT loss and spectrogram discriminators
- [[concepts/structured-sparsity|Structured Sparsity]] — the 1.5 → 1.2 GFLOPS reduction
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — the 18-BFCC conditioning representation
- [[concepts/wavernn|WaveRNN]] — the AR density-estimation lineage FWGAN departs from

## Related Sources

- [[sources/mustafa-2023-framewise-wavegan|Mustafa et al. 2023: Framewise WaveGAN]] — the original paper
- [[sources/valin-2024-fargan|Valin, Mustafa & Büthe 2024: FARGAN]] — the successor that reuses the framewise recipe
