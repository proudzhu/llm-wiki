---
type: concept
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/mezza-2024-hybrid-plc/full-text.md
tags:
  - packet-loss-concealment
  - hybrid-dsp-dnn
  - residual-learning
  - real-time
  - low-complexity
  - networked-music-performance
---

# PARCnet

**PARCnet** (parallel autoregressive residual network) is a hybrid packet loss concealment architecture introduced by [[entities/alessandro-ilic-mezza|Mezza]], Amerena, Bernardini & Sarti ([[sources/mezza-2024-hybrid-plc|IEEE OJSP 2024]]) for real-time [[concepts/networked-music-performance|networked music performance]]. Its defining move is to **reformulate PLC as residual prediction**: instead of generating a waveform from scratch, a feed-forward neural network predicts the nonlinear residual term of an online [[concepts/linear-prediction|linear autoregressive]] predictor, and the two contributions are summed. At 416 k parameters it is the smallest deep PLC model in its comparison and the only deep method in that study that runs in real time at 32 kHz on a laptop CPU.

## Key Formulations

For a lost $M$-sample packet starting at index $k$ with past context $\mathbf{x}=[y[k-N],\dots,y[k-1]]^{T}$:

$$
\hat{\mathbf{y}} = \mathbf{y}_{\mathrm{AR}} + \mathbf{v}\odot f_\theta(\mathbf{x}),
$$

where $\mathbf{y}_{\mathrm{AR}}$ is the $\mathrm{AR}(p)$ forecast (fitted online by autocorrelation + Levinson–Durbin on a 100 ms window with 10 ms stride, [[concepts/diagonal-loading|diagonally loaded]] by $\mu=10^{-3}$), $f_\theta$ is a causal fully-convolutional network mapping $N$ context samples to $M'$ residual samples, and $\mathbf{v}$ is a fade-in envelope with $v_\ell=\ell/(K-1)$ for $0\le\ell<K=16$, $v_\ell=1$ thereafter.

Three design consequences follow:

1. **Smooth-handed seam** — the AR branch is accurate for the first few samples and continues the signal without a discontinuity, while the feed-forward branch (accurate later in the packet) is faded in over 16 samples. Without $\mathbf{v}$, a jump discontinuity of the first kind appears at the seam and produces an audible click.
2. **Training over the context too** — the target window includes the valid context, $\min_\theta\mathcal{L}(\tilde{\mathbf{y}},\ \mathcal{F}_\theta(\tilde{\mathbf{x}})+\tilde{\mathbf{y}}_{\mathrm{AR}})$, so the network is explicitly pushed to model the linear predictor's residual rather than the missing packet alone.
3. **Small network, cheap inference** — frame-by-frame feed-forward inference (rather than sample-by-sample autoregression, as in Thyssen et al. 1994) lets the architecture shrink; inference is purely time-domain even though training uses a multi-resolution STFT + MSE + log-magnitude loss.

Outbound transitions (prediction → next received packet) are handled by predicting $M'>M$ samples (25% overshoot) and linearly cross-fading the overlap.

## Architecture

Encoder–bottleneck–decoder, all 1D convolutions:

- **Encoder** — 4 dilated residual blocks (skip path + dilation-1 conv + dilation-2 and dilation-4 stacks, batch norm, LeakyReLU 0.2), filters 8/16/32/64, kernel 11, max-pooling ×2 between blocks.
- **Bottleneck** — 6 GLU blocks (pointwise input stack 32 ch → GLU kernel 11 → pointwise output stack 64 ch, residual shortcut + PReLU), GLU dilation $2^{j-1}$.
- **Decoder** — 4 dilated residual blocks, filters 64/32/16/8, kernel 7, nearest-neighbour upsampling ×2.
- **Head** — pointwise conv + $\tanh$.

## Why It Matters for PLC

PARCnet occupies a distinct corner of the neural-PLC design space: it is *feed-forward* (fast, no autoregressive sampling loop, no drift) yet *not* a pure waveform mapper — the quasi-harmonic short-time structure of music is carried by the classical all-pole model, and only the non-white residual is learned. Empirically the linear branch is a strong baseline in its own right ($\mathrm{AR}(128)$ beats every deep baseline on NMSE/PEAQ/PLCMOS at 32 kHz on piano), which reframes neural PLC as *residual refinement* rather than waveform generation.

## Related Concepts

- [[concepts/packet-loss-concealment|Packet Loss Concealment]] — the umbrella task
- [[concepts/linear-prediction|Linear Prediction]] — the AR branch and the residual the network learns
- [[concepts/diagonal-loading|Diagonal Loading]] — conditioning of the autocorrelation matrix
- [[concepts/networked-music-performance|Networked Music Performance]] — the target application
- [[concepts/lpcnet|LPCNet]] — autoregressive neural PLC, the contrasting branch of the feed-forward/autoregressive dichotomy

## Related Sources

- [[sources/mezza-2024-hybrid-plc|Mezza, Amerena, Bernardini & Sarti 2024: Hybrid Packet Loss Concealment for Real-Time Networked Music Applications]] — introduces PARCnet
