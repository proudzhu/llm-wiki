---
type: concept
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/zhao-2024-sicrn/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - state-space-model
  - inplace-convolution
  - attention
  - module
---

# SIC Block

The **SIC block** (State space model + Inplace Convolution block) is the novel drop-in convolutional module introduced by [[concepts/sicrn|SICRN]] (Zhao, He & Zhang 2024). It combines a 2D [[concepts/inplace-convolution|inplace convolution]] (local-feature branch) with an [[concepts/s4nd|S4ND]] layer (global-feature branch) and fuses them through an attention map. The SIC block is designed as a direct replacement for the standard strided convolution in a [[concepts/convolutional-recurrent-network|CRN]] encoder/decoder, with the goal of preserving the original spectral structure (no downsampling) while recovering the full-band correlations that pure inplace convolutions miss.

## Motivation

The SIC block is the synthesis of two prior observations:

1. **[[concepts/inplace-convolution|Inplace convolutions]]** (stride 1 on frequency) preserve per-bin structure and avoid the frequency-axis aliasing of standard CRN downsampling, but process each frequency bin independently — they cannot learn full-band correlations.
2. **[[concepts/s4nd|S4ND]]** has an effectively infinite receptive field along every axis and therefore excels at global feature modeling, but lacks the local inductive bias of convolution and may miss fine-grained sub-band structure.

SICRN's central claim is that the two are complementary: the SIC block uses S4ND's global view to *gate* the inplace convolution's local view via an attention map, achieving both global context and local detail in a single module.

## Mathematical Formulation

Given an input tensor $X$ with channel dimension $c$, the SIC block **bifurcates** the channel dimension into two halves. The first half is processed by 2D inplace convolution (local branch); the second half by S4ND (global branch). A 1D convolution reduces the local-branch output to a single-channel attention map, which is summed with the global-branch output and passed through a sigmoid to produce the attention map. The final output is the local branch's feature multiplied by this attention map.

$$X^{L}_{0 \sim c/2} = C_{1d}\!\left( \operatorname{IC}(X_{0 \sim c/2}) \right)$$

$$X^{R}_{c/2 \sim c} = \operatorname{S}(X_{c/2 \sim c})$$

$$ATmap = \sigma\!\left( C_{1d}\!\left( \operatorname{IC}(X_{0 \sim c/2}) \right) + X^{R}_{c/2 \sim c} \right)$$

$$\mathrm{X} = X^{L}_{0 \sim c/2} \cdot ATmap$$

where:

- $\operatorname{IC}(\cdot)$ is the 2D inplace convolution (stride 1 on both frequency and time).
- $\operatorname{S}(\cdot)$ is the S4ND convolution kernel (the global state-space layer).
- $C_{1d}(\cdot)$ is a 1D convolution that projects the local-branch features down to the attention map dimension.
- $\sigma$ is the sigmoid activation.
- $X^{L}_{0 \sim c/2}$ are the local features, $X^{R}_{c/2 \sim c}$ the global features, and $ATmap$ the attention map.

The configuration used in [[concepts/sicrn|SICRN]] is 3 inplace-convolution layers and 4 S4ND blocks per SIC block.

## S4ND Sub-Block

The S4ND branch is wrapped in a residual block:

$$\text{S4ND block}: \quad \text{S4ND} \to \text{ELU} \to \text{Linear} \to \text{+ residual} \to \text{BatchNorm}$$

The residual connection mitigates gradient vanishing/exploding; BatchNorm stabilizes the output distribution. See [[concepts/s4nd|S4ND]] for the underlying state-space formulation.

## Empirical Evidence

The SICRN paper isolates the S4ND contribution via the **IICRN** ablation: replacing the 4-layer S4ND inside each SIC block with a 4-layer inplace convolution (so the block becomes purely local) degrades all metrics on the DNS Challenge test set. The gap is larger on the reverberant condition (~0.09 WB-PESQ) than the anechoic condition (~0.03 WB-PESQ), which the authors interpret as evidence that the global S4ND branch is most valuable when the test distribution differs from training — i.e., when explicit full-band context helps most.

| Variant | With-Reverb WB-PESQ | Without-Reverb WB-PESQ |
|---|---|---|
| IICRN (inplace conv only, no S4ND) | 2.797 | 2.596 |
| **SICRN (full SIC block)** | **2.891** | **2.624** |

## Relationship to Other Inplace-CRN Augmentations

The SIC block addresses the same full-band-modeling gap that [[concepts/cepstral-frequency-block|ICCRN's Cepstral Frequency Block (CFB)]] addresses — both augment a pure inplace design with a parallel branch that captures cross-frequency structure. The two solutions differ in mechanism:

| | CFB ([[concepts/iccrn|ICCRN]]) | S4ND branch (SICRN) |
|---|---|---|
| Domain | Cepstral (FFT of frequency axis) | Native time-frequency |
| Operation | Learned linear transform + 1D conv | State-space ODE convolution |
| Receptive field | Bounded by FFT window / kernel size | Theoretically infinite along every axis |
| Causality | Causal | Causal |
| Cost | Small (FFT is $O(F \log F)$) | Small (state-space convolution is $O(L \log L)$ via FFT) |

## Related Concepts

- [[concepts/sicrn|SICRN]] — the architecture that uses the SIC block
- [[concepts/s4nd|S4ND]] — the global-feature branch
- [[concepts/inplace-convolution|Inplace Convolution]] — the local-feature branch
- [[concepts/cepstral-frequency-block|Cepstral Frequency Block]] — sibling solution to the same full-band-modeling gap
- [[concepts/attention-mechanism|Attention Mechanism]] — the SIC block uses sigmoid attention for global-local fusion
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the family whose convolutions the SIC block replaces

## Related Sources

- [[sources/zhao-2024-sicrn|Zhao, He & Zhang 2024: SICRN — State Space Model + Inplace Convolution for Speech Enhancement]]
