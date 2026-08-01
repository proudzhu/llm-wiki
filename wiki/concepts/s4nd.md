---
type: concept
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/zhao-2024-sicrn/full-text.md
tags:
  - neural-network
  - state-space-model
  - deep-learning
  - speech-enhancement
  - global-context
---

# S4ND

**S4ND** (State Space model for N-Dimensional signals) is a multidimensional extension of the S4 structured state-space model (Gu, Goel & Ré 2022) proposed by Nguyen et al. (NeurIPS 2022). It turns the 1-D ordinary differential equation (ODE) of S4 into a multidimensional partial differential equation (PDE) governed by an independent SSM along each axis, giving the layer an **effectively infinite receptive field along every input dimension**. In speech enhancement, S4ND is used as a global-feature modeling branch that captures cross-frequency and long-term temporal dependencies without downsampling.

## From S4 to S4ND

### S4 (1-D SSM)

The structured state-space model (S4) is defined in continuous time as:

$$h'(t) = Ah(t) + Bx(t), \qquad y(t) = Ch(t) + Dx(t)$$

discretized with step size $\Delta$:

$$x_{k} = \overline{A} x_{k-1} + \overline{B} u_{k}, \qquad y_{k} = \overline{C} x_{k}$$

$$\overline{A} = (I - \Delta/2 \cdot A)^{-1} (I + \Delta/2 \cdot A)$$

The discrete sequence response can be written as a single (non-circular) convolution with kernel

$$\overline{K} = \left( \overline{C}\overline{B},\; \overline{C}\overline{A}\overline{B},\; \ldots,\; \overline{C}\overline{A}^{L-1}\overline{B} \right)$$

so that $y = \overline{K} * u$, efficiently computable via FFTs once $\overline{K}$ is known.

**Limitation for speech**: S4 was designed for 1-D inputs. Applied to a 2-D $(H, T)$ input (e.g., frequency × time), it processes $H$ rows independently in parallel — there is no correlation in the $H$ dimension. This is unsuitable for frequency-domain speech processing, where cross-frequency structure (harmonics, formants) is exactly what a global model should capture.

### S4ND (N-D PDE extension)

S4ND generalizes the 1-D SSM to N-dimensional signals $u, y: \mathbb{R}^{N} \to \mathbb{C}$ by defining the state $x = (x^{(1)}(\mathbf{t}), \ldots, x^{(N)}(\mathbf{t})) \in \mathbb{C}^{N^{(1)} \times \cdots \times N^{(N)}}$ and the linear PDE

$$\frac{\partial}{\partial t^{(\tau)}} x(\mathbf{t}) = \big(\ldots, A^{(\tau)} x^{(\tau)}(\mathbf{t}), \ldots\big) + B^{(\tau)} u(\mathbf{t})$$

$$y(\mathbf{t}) = \langle C, x(\mathbf{t}) \rangle$$

Equivalently, S4ND runs a separate standard 1-D SSM along **each axis independently**, then combines the results. For the 2-D case relevant to speech (frequency × time), this means S4ND captures both cross-frequency correlations (via the frequency-axis SSM) and long-term temporal correlations (via the time-axis SSM) — exactly what S4 cannot do.

S4ND can be regarded as **a convolution kernel with infinite receptive fields in N dimensions**. Its parameter count and computational load are remarkably low (state-space convolutions are $O(L \log L)$ via FFT), and it is causal when the underlying SSMs are causal.

## Use in Speech Enhancement

The primary speech-enhancement application in this wiki is the [[concepts/sicrn|SICRN]] architecture (Zhao, He & Zhang 2024), where S4ND is the global-feature branch of the [[concepts/sic-block|SIC block]]. SICRN's authors justify choosing S4ND over alternatives as follows:

1. **vs. LSTM**: S4ND's global modeling capacity exceeds LSTM at a smaller parameter and computational count.
2. **vs. S4**: S4 processes frequency bins independently and cannot capture frequency-axis correlations; S4ND's multidimensional PDE formulation captures correlations along every axis.
3. **vs. 2D convolution**: S4ND outperforms 2D convolutions in their experiments (per Nguyen et al. 2022).

In SICRN, the S4ND branch is wrapped in a residual block: `S4ND → ELU → Linear → +residual → BatchNorm`.

The S4ND-U-Net variant of Ku et al. (2023, arXiv:2306.00331) is referenced as prior evidence of S4ND's significant enhancement performance in the frequency domain at low parameter count, while preserving causality and real-time performance.

## Related Concepts

- [[concepts/state-space-model|State-Space Model]] — the broader SSM family (this page covers the deep-learning SSM subfamily; the main SSM page focuses on control-theory applications)
- [[concepts/sicrn|SICRN]] — uses S4ND as its global-feature branch
- [[concepts/sic-block|SIC Block]] — the module that wraps S4ND + inplace convolution
- [[concepts/mamba-mingru|Mamba-MinGRU]] — another deep-learning SSM application (selective SSM + MinGRU) in own-voice cancellation
- [[concepts/inplace-convolution|Inplace Convolution]] — the local counterpart that S4ND complements in SICRN
- [[concepts/long-short-term-memory|LSTM]] — the recurrent baseline that S4ND is compared against in SICRN
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the family whose convolutions S4ND-based blocks augment

## Related Sources

- [[sources/zhao-2024-sicrn|Zhao, He & Zhang 2024: SICRN — State Space Model + Inplace Convolution for Speech Enhancement]]
