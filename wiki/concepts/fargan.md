---
type: concept
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/valin-2024-fargan/full-text.md
tags:
  - neural-vocoder
  - speech-synthesis
  - gan
  - autoregressive
  - fargan
  - low-complexity
  - real-time
---

# FARGAN

**FARGAN** (Framewise Autoregressive GAN) is a low-complexity neural vocoder introduced by [[entities/jean-marc-valin|Valin]], [[entities/ahmed-mustafa|Mustafa]] and [[entities/jan-buthe|Büthe]] ([[sources/valin-2024-fargan|IEEE SPL 2024]]). It generates 16 kHz speech in **2.5-ms (40-sample) subframes** — one pass of the generator per subframe — using [[concepts/pitch-prediction|long-term pitch prediction]] as a second autoregressive feedback alongside the previous subframe. Because each subframe is produced in a single pass, the model can be trained adversarially **without teacher forcing** (by unrolling in time), eliminating the [[concepts/exposure-bias|exposure bias]] of density-estimation vocoders. The result: 820k parameters, **600 MFLOPS** (0.8% of one laptop CPU core), with P.808 quality statistically tied to CARGAN and HiFi-GAN v1 at 64–110× their complexity — and significantly better than [[concepts/lpcnet|LPCNet]], FWGAN and HiFi-GAN v3.

## Architecture

Two networks, mirroring the two time scales of speech:

- **Frame conditioning network** (once per 10-ms frame) — a fully-connected layer, a 3×1 convolution, and a transposed convolution performing 4× up-sampling. Input: 32 dims = 20 acoustic features (18 [[concepts/bark-scale-spectral-features|BFCCs]] + pitch period + voicing indicator, as in LPCNet) plus a 12-dimensional pitch embedding. Output: a conditioning latent at the 2.5-ms subframe rate.
- **Subframe synthesis network** (once per 2.5-ms subframe) — Conv 2×1 → GRU1 → GRU2 (skip connection) → GRU3 → FC → FC → gain multiplication; every layer uses tanh and (except the output layer) a gated linear unit $G(\mathbf{x})=\mathbf{x}\odot\sigma(\mathbf{Wx})$. Both autoregressive inputs — the previous subframe and the renormalized, voicing-gated pitch prediction — are fed to **all** layers, not only the input, which stabilizes and speeds convergence (likely a vanishing-gradient remedy).

The output is de-emphasized with $H(z)=1/(1-0.85z^{-1})$, the mirror of LPCNet's pre-emphasis.

## Efficiency Techniques

- **Gain normalization** — a single fully-connected neuron with exponential activation computes a per-subframe gain from the conditioning; the output layer is scaled to full dynamic range, and the autoregressive feedback is renormalized with the gain of the subframe *where it is used* (not where it was generated).
- **8-bit quantization throughout** — bounded tanh/sigmoid activations (unlike ReLU), the pre-emphasized operating domain, and gain normalization together allow 8-bit weights *and* activations; 8-bit weights also yield 4× more operations per SIMD vector length.
- **Cache-resident model** — 820k weights quantize to under 1 MB, fitting the L2 cache of newer CPUs (L3 of older ones).
- **2.5-ms granularity** — smaller than FWGAN's 10-ms frames, chosen to make optimal use of pitch prediction (a period of 500 Hz spans 32 samples); it also reduces model size at a given complexity.

## Training

No teacher forcing: the subframe network is **unrolled in time**, so the autoregressive inputs during training come from the synthesized signal itself. Pre-training uses a six-resolution spectral loss ($\gamma=0.5$ magnitude compression, window sizes 80–2560, 75% overlap; 470k updates, batch 4096, ~2.5 days on one A100); adversarial fine-tuning uses six log-magnitude-STFT discriminators (UnivNet-style with NoLACE's frequency strides and 2D positional embeddings) under a least-squares GAN objective with feature matching, plus the retained spectral loss (50 epochs, lr $2\times10^{-6}$, batch 160). Time-domain multi-scale/multi-period discriminators were found to *degrade* quality on block-wise generators — they win by detecting temporally irregular, perceptually irrelevant detail.

## Results

Trained speaker-independently on 205 hours (900+ speakers, 34 languages), FARGAN reaches PESQ 3.298 / MPE 4.108 (best of all compared vocoders) and 0.6 GFLOPS, versus LPCNet's 2.539 / 5.303 at 2.8 GFLOPS and HiFi-GAN v1's 3.024 / 5.501 at 38.1 GFLOPS. Ablations confirm both autoregressive paths matter: removing pitch prediction costs 0.12 PESQ at equal weight count; removing all autoregression drops PESQ to 2.859.

## Position in the Vocoder Landscape

FARGAN descends from two lines: CARGAN's argument that autoregressive models have an inductive bias for pitch and phase (but its 512-sample chunks still need teacher forcing for the AR part), and FWGAN's framewise adversarial generation (10-ms frames, 1.2 GFLOPS, no explicit pitch structure). FARGAN keeps LPCNet's acoustic features but *drops the LPC filter*, replacing short-term linear prediction with explicit long-term pitch prediction — a GAN rather than a density model, so no softmax sampling either. It replaced LPCNet as the vocoder of the DRED redundancy scheme in **Opus 1.5**, cutting DRED synthesis complexity 5×. Unlike LPCNet it does not generalize to music, since the pitch-prediction lookback presumes a single periodic source.

## Related Concepts

- [[concepts/pitch-prediction|Pitch Prediction]] — the long-term prediction feedback at the core of the design
- [[concepts/exposure-bias|Teacher Forcing and Exposure Bias]] — the training pathology FARGAN's unrolled framewise training eliminates
- [[concepts/lpcnet|LPCNet]] — predecessor; same features, different prediction structure, density-estimation training
- [[concepts/wavernn|WaveRNN]] — the AR density-estimation lineage both depart from
- [[concepts/frequency-domain-loss|Frequency Domain Loss]] — the spectral pre-training loss and STFT discriminator design
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — the 18-BFCC input representation

## Related Sources

- [[sources/valin-2024-fargan|Valin, Mustafa & Büthe 2024: FARGAN]] — the original paper
