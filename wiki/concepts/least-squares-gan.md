---
type: concept
created: 2026-11-20
updated: 2026-11-20
sources:
  - raw/papers/pascual-2017-segan/full-text.md
tags:
  - gan
  - generative-models
  - loss-function
  - speech-enhancement
---

# Least-Squares GAN (LSGAN)

**LSGAN** (Mao et al. 2016) is a [[concepts/generative-vs-discriminative-speech-enhancement|GAN]] training variant that replaces the discriminator's sigmoid cross-entropy loss with a **least-squares loss on binary codes** (1 for real, 0 for fake). The motivation is the vanishing-gradient problem of the original GAN objective: once a sample is on the correct side of the decision boundary the sigmoid saturates, its gradient vanishes, and the generator receives almost no signal even for samples that are far from the real data manifold. The squared-error loss penalizes samples *by distance to the boundary* instead of only by classification correctness, so gradients persist; in the original paper this also pulls generated samples toward the decision boundary and produces higher-quality images.

## Formulation

Conditioned on side information $\mathbf{x}_c$ (in speech enhancement, the noisy signal $\tilde{\mathbf{x}}$), the LSGAN objectives are

$$\min_{D} V_{\text{LSGAN}}(D) = \tfrac{1}{2}\mathbb{E}_{\mathbf{x},\mathbf{x}_c\sim p_{\text{data}}}\left[(D(\mathbf{x},\mathbf{x}_c)-1)^2\right] + \tfrac{1}{2}\mathbb{E}_{\mathbf{z},\mathbf{x}_c}\left[D(G(\mathbf{z},\mathbf{x}_c),\mathbf{x}_c)^2\right]$$

$$\min_{G} V_{\text{LSGAN}}(G) = \tfrac{1}{2}\mathbb{E}_{\mathbf{z},\mathbf{x}_c}\left[(D(G(\mathbf{z},\mathbf{x}_c),\mathbf{x}_c)-1)^2\right]$$

## Use in Speech Enhancement

**[[concepts/segan|SEGAN]] (Pascual, Bonafonte & Serrà 2017)** is the paper that brought LSGAN into speech enhancement, adopting it in place of the plain min–max objective and **adding an $L_1$ anchor** to the generator term:

$$\min_{G} V_{\text{SEGAN}}(G) = \tfrac{1}{2}\mathbb{E}\left[(D(G(\mathbf{z},\tilde{\mathbf{x}}),\tilde{\mathbf{x}})-1)^2\right] + \lambda\,\lVert G(\mathbf{z},\tilde{\mathbf{x}}) - \mathbf{x}\rVert_1, \qquad \lambda = 100$$

The split of duties matters: the adversarial term supplies realism (fine-grained, distribution-matching detail that a conditional-mean regression cannot express) while the $L_1$ term supplies fidelity to the clean target. SEGAN's ablation on the weight is instructive — at $\lambda = 1$ the $L_1$ term sat two orders of magnitude below the adversarial term and had no practical effect, so the two terms must be balanced within a couple of orders of magnitude for the anchor to bite.

## Related Concepts

- [[concepts/segan|SEGAN]] — the speech-enhancement architecture built on this objective
- [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]] — where GAN objectives sit in the SE landscape
- [[concepts/vanishing-gradient-problem|Vanishing Gradient Problem]] — the failure LSGAN removes from the discriminator
- [[concepts/multi-scale-discriminator|Multi-Scale Discriminator]] — the critic design used by later waveform-domain GAN systems

## Related Sources

- [[sources/pascual-2017-segan|Pascual, Bonafonte & Serrà 2017: SEGAN]] — adopts LSGAN for waveform-level enhancement and calibrates the $L_1$ weight
