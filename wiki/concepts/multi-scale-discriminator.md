---
type: concept
created: 2026-11-08
updated: 2026-11-08
sources:
  - wiki/sources/wu-2026-dbmif-multimodal-fusion.md
  - raw/papers/zhao-2025-lightweight-transformer/full-text.md
tags:
  - speech-enhancement
  - gan
  - discriminator
  - subband
---

# Multi-Scale Discriminator

A **multi-scale discriminator** is the adversarial critic design introduced by MelGAN for waveform generation: several discriminators with different receptive fields (or different resolutions of the same signal) score real and generated audio, and their hinge/least-squares losses are summed. It is the standard way to give a waveform-domain generator both global structure and local texture supervision, since a single discriminator at one resolution cannot penalise both.

## Standard Form (MelGAN)

$K$ discriminators, each a strided-conv stack with progressively larger receptive field, applied to the raw waveform. The generator is trained with an adversarial term plus a **feature-matching** term that minimises the L1 distance between the discriminators' intermediate features for real and generated input. The feature-matching term is what keeps GAN training stable and prevents the over-smoothing that a pure adversarial objective produces.

## Subband Variant (DBMIF)

DBMIF (Wu et al. 2026) extends the idea along the *spectral* axis instead of only the temporal one:

| Component | Operates on | Structure |
|:----------|:------------|:----------|
| $D_{\mathrm{wav}}$ | Raw full-band waveform at 16 kHz | 7 strided convs, kernel sizes 15 / 41×4 / 5 / 3, grouped convs (g=4) from layer 2, 1→16→64→256→1024→1024→1024→1 |
| $D_{\mathrm{sub}}$ ×3 | The same 4 [[concepts/pseudo-qmf-bank\|PQMF]] subbands, concatenated channel-wise | 8 convs, kernel sizes 3 / 7×5 / 5 / 3, stride 2 after layer 1, groups 4, channels 4→36→72→144→288→576→1152→1152→1; the three copies differ only in dilation $d \in \{1,2,3\}$ |

The full-band critic enforces global structural coherence and low-frequency consistency; the dilated subband critics enforce fine spectral fidelity at three different periodicities inside each band. Reusing the generator's own analysis bank for the critics means the adversarial signal is aligned with the representation the generator works in.

## Losses

Hinge discriminator objective over all $K$ critics ($k = 0,\dots,3$ in DBMIF):

$$
L_D = \sum_{k}\left[\mathbb{E}_{\mathrm{y}}\left[\max(0, 1 - D_k(\mathrm{y}))\right] + \mathbb{E}_{\hat{\mathrm{y}}}\left[\max(0, 1 + D_k(\hat{\mathrm{y}}))\right]\right]
$$

Generator adversarial and feature-matching terms:

$$
L_G^{\mathrm{adv}} = \sum_{k}\mathbb{E}_{\hat{\mathbf{y}}}\left[\max(0, 1 - D_k(\hat{\mathbf{y}}))\right], \qquad
L_G^{\mathrm{fm}} = \sum_{k}\sum_{i=1}^{N_k-1}\frac{1}{M_i}\left\lVert D_k^{(i)}(\mathrm{y}) - D_k^{(i)}(\hat{\mathrm{y}})\right\rVert_1
$$

$$
L_G = L_G^{\mathrm{adv}} + \lambda L_G^{\mathrm{fm}}
$$

DBMIF uses $\lambda = 1000$ and no explicit spectral reconstruction loss — structural fidelity rests entirely on the critics plus feature matching.

## Multi-Period + Multi-Scale on a Tiny Generator (LCT-GAN)

LCT-GAN (Zhao & Madhu 2025) pairs a MelGAN-style **multi-period** discriminator — which reshapes the waveform into 2-D periodic views so it can score structure at several periods — with a HiFi-GAN-style multi-scale discriminator, both fed raw waveform. The point of interest is not the critics themselves but their **cost profile**: the generator is 0.14 M parameters / 0.35 G MAC/s, and the critics exist only during training, so the pair adds substantial training compute to a model whose inference budget is 6% of DeepFilterNet2's parameters. The ablation isolates the effect — going from generator-only to GAN on VoiceBank+DEMAND moves PESQ 3.01 → 3.06, COVL 3.75 → 3.80, CBAK 3.64 → 3.66, SIG/OVL on DNS3 3.00 → 3.06 / 2.74 → 2.80 with **no BAK degradation** — i.e. the critics buy speech preservation without licensing noise leakage, which is the failure mode a purely adversarial objective can produce.

## Costs and Cautions
- **Perceptual gain, not fidelity guarantee** — GAN-trained enhancers in the BC literature consistently top DNSMOS (DBMIF 3.35, EBEN 3.17 vs. 2.66–2.94 for discriminative T-F models) while hallucination risk at low SNR is not directly measured. An ASR-consistency check is the usual missing falsification test.
- **Compute** — four discriminators triples the training-side cost relative to a single critic; at inference only the generator is kept, so this does not affect deployment.
- **Weight normalisation** throughout both DBMIF critic families (Leaky-ReLU $\alpha = 0.1$, linear output layer).

## Related Concepts

- [[concepts/pseudo-qmf-bank|Pseudo-QMF Bank]] — provides the subband decomposition reused by the critics
- [[concepts/erb-scale|ERB Scale]] — where perceptual band weighting enters the discriminator in related work
- [[concepts/spectral-norm|Spectral Normalization]] — the alternative stabiliser for discriminator training
- [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]] — where GAN-trained systems trade fidelity for naturalness

## Related Sources

- [[sources/wu-2026-dbmif-multimodal-fusion|Wu et al. 2026: DBMIF]] — waveform + 3 dilation-factor subband critics for AC/BC enhancement
- [[sources/zhao-2025-lightweight-transformer|Zhao & Madhu 2025: Study of Lightweight Transformer Architectures for Single-Channel Speech Enhancement]] — MelGAN-style multi-period + multi-scale critics on a 0.14 M-parameter generator; +0.05 PESQ/+0.05 COVL with no BAK loss
