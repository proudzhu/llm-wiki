---
type: concept
created: 2026-08-14
updated: 2026-08-14
tags:
  - neural-network
  - adaptive-processing
  - speech-coding
  - hybrid-dsp-dnn
---

# AdaShape

**AdaShape (Adaptive Temporal Shaping)** is a module that multiplies an audio signal sample-wise with a **locally periodic sequence of non-negative weights** computed from a latent feature sequence. It was proposed by Büthe, Mustafa, Valin, Helwani & Goodwin in **NoLACE** (ICASSP 2024) for improving low-complexity speech codec enhancement. In [[sources/buthe-2025-blind-wideband-to-fullband-extension|BBWENet (Büthe & Valin 2025)]], AdaShape implements **spectral folding "in a broader sense"** — one of the two bandwidth-extension mechanisms of the hybrid DSP/DNN pipeline.

## Formulation

Given an input signal $x(\cdot)$ and a latent feature sequence $\phi(\cdot)$ from a feature encoder, AdaShape computes a time-varying, non-negative weight sequence and applies it sample-wise:

$$
\mathrm{AdaShape}(x(\cdot), \phi(\cdot))(n) = \alpha(n, \phi(\cdot), x(\cdot)) \cdot x(n)
$$

Multiplying a signal by a periodic weight sequence creates mirror images (folding) of the spectrum. By making the weights **locally periodic and signal-dependent**, AdaShape extends this classical folding idea: it can fold the spectrum at the desired positions and adapt the folding to the signal content. It is also capable in principle of sharpening pulses in voiced parts, but post-hoc analysis in BBWENet shows the model mostly uses folding for extending **unvoiced** parts.

## Role in BBWENet

In BBWENet's bandwidth-extension pipeline, AdaShape provides the **spectral-folding extension path**, complementary to the non-linear extension path:

- **Unvoiced parts** → extended primarily by AdaShape (folding), especially effective when combined with spectral flattening as pre-filtering;
- **Voiced parts** → extended primarily by the non-linear function $f(x) = x\sin(\ln|x|)$.

The second (superwideband→fullband) stage relies mainly on AdaShape output plus imaging from the short FIR interpolation filters. A linear decomposition of the output (Figure 3 of the paper) into bypass + AdaShape + NonLin contributions reveals this division of labor directly.

## Related Concepts

- [[concepts/adaconv|AdaConv]] — sibling adaptive module from the same lab (adaptive filter *weights* rather than sample-wise weights)
- [[concepts/blind-bandwidth-extension|Blind Bandwidth Extension]] — the task where AdaShape implements spectral folding
- [[concepts/adaptive-convolution|Adaptive Convolution (Wang et al. 2025)]] — frame-wise dynamic convolution; different mechanism, same adaptive-processing family

## Related Sources

- [[sources/buthe-2025-blind-wideband-to-fullband-extension|Büthe & Valin 2025: A Lightweight and Robust Method for Blind Wideband-to-Fullband Extension of Speech]] — uses AdaShape for spectral-folding-based extension in blind BWE
