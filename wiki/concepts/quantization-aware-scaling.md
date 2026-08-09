---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/lin-2023-tinyml-progress-futures/full-text.md
tags:
  - tinyml
  - on-device-training
  - quantization
  - efficient-deep-learning
  - microcontroller
---

# Quantization-Aware Scaling (QAS)

**Quantization-Aware Scaling (QAS)** is a hyperparameter-free gradient-scaling rule introduced as part of MCUNetV3 to stabilize training of *real* int8-quantized graphs on microcontrollers. It compensates the gradient of each quantized tensor by the inverse square of its quantization scaling factor so that the per-tensor $\lVert\mathbf{W}\rVert/\lVert\mathbf{G}\rVert$ ratio of the quantized graph matches that of the floating-point counterpart, restoring stable optimization without incurring any memory overhead. QAS is surveyed in [[sources/lin-2023-tinyml-progress-futures\|Lin et al. 2023: TinyML — Progress and Futures]] as the algorithm-side fix that makes tiny on-device training practical.

## Motivation: Gradient Scale Mismatch

A quantized linear layer $\mathbf{y} = \mathbf{W}\mathbf{x} + \mathbf{b}$ is conventionally approximated as

$$
\bar{\mathbf{y}}_{\text{int8}} = \texttt{cast2int8}\!\left[s \cdot (\bar{\mathbf{W}}_{\text{int8}}\bar{\mathbf{x}}_{\text{int8}} + \bar{\mathbf{b}}_{\text{int32}})\right],
$$

where $s = s_{\mathbf{W}} \cdot s_{\mathbf{x}}$ is the product of the per-tensor weight and input scaling factors mapping fixed-point results back into int8 range. Forward computation is (approximately) preserved, but the **weight-to-gradient magnitude ratio is distorted by** $s_{\mathbf{W}}^{-2}$:

$$
\frac{\lVert \bar{\mathbf{W}} \rVert}{\lVert \mathbf{G}_{\bar{\mathbf{W}}} \rVert} \approx s_{\mathbf{W}}^{-2} \cdot \frac{\lVert \mathbf{W} \rVert}{\lVert \mathbf{G} \rVert}.
$$

Two failure modes follow:

1. The scaling factor is far smaller than 1, so the quantized $\lVert\mathbf{W}\rVert/\lVert\mathbf{G}\rVert$ is much larger than the floating-point version — the same global learning rate is now mis-scaled per tensor.
2. Weights (int8) and biases (int32) have scaling factors of very different magnitude, producing a characteristic **zigzag pattern** in the per-tensor ratio curve that no single learning rate can match.

Adaptive optimizers like Adam and LARS do not fully address this: Adam partially closes the gap but triples memory (second-order momentum); LARS frequently fails to converge under aggressive scaling. Batch Normalization layers are typically fused away during quantization, removing a natural gradient stabilizer.

## The QAS Rule

QAS rescales the quantized gradients *before* the optimizer step, with no extra memory cost:

$$
\tilde{\mathbf{G}}_{\bar{\mathbf{W}}} = \mathbf{G}_{\bar{\mathbf{W}}} \cdot s_{\mathbf{W}}^{-2}, \qquad \tilde{\mathbf{G}}_{\bar{\mathbf{b}}} = \mathbf{G}_{\bar{\mathbf{b}}} \cdot s^{-2}.
$$

After QAS, the $\lVert\mathbf{W}\rVert/\lVert\mathbf{G}\rVert$ curve of the quantized graph tracks the floating-point reference, eliminating the zigzag and the global offset. QAS is **hyperparameter-free** — the scaling factors $s_{\mathbf{W}}$ and $s$ are already computed during quantization, so QAS adds no tuning surface.

## Empirical Impact (transfer learning, MCUNet backbone, 8 datasets)

| Precision | Optimizer | Avg Acc. |
|---|---|---|
| fp32 | SGD-M | 73.3% |
| int8 | SGD-M | 64.9% |
| int8 | Adam | 71.8% |
| int8 | LARS | 39.8% |
| **int8** | **SGD-M + QAS** | **73.5%** |

QAS closes the int8-vs-fp32 accuracy gap (73.5% vs 73.3%) with **no memory overhead**, while Adam only reaches 71.8% at 3× memory cost. QAS also stabilizes the training curve (faster, smoother convergence on the Cars dataset).

## Relation to Other Quantization Techniques

- Unlike [[concepts/quantization-aware-training\|Quantization-Aware Training]] (QAT), which simulates quantization noise during *forward* training in fp32, QAS targets the *backward* pass of a real int8 graph on bare-metal MCUs where no fp32 fallback exists.
- QAS is orthogonal to [[concepts/post-training-quantization\|Post-Training Quantization]] (PTQ): PTQ determines the scaling factors $s$; QAS reuses those same factors to correct the gradient.

## Related Concepts

- [[concepts/sparse-update\|Sparse Update]] — the companion MCUNetV3 algorithm technique that selects *which* tensors to update; combined with QAS for *how* to update them
- [[concepts/tiny-training-engine\|Tiny Training Engine (TTE)]] — the system that compiles QAS-scaled gradients into bare-metal code
- [[concepts/tinyml\|TinyML]] — problem domain
- [[concepts/quantization-aware-training\|Quantization-Aware Training]]
- [[concepts/post-training-quantization\|Post-Training Quantization]]

## Related Sources

- [[sources/lin-2023-tinyml-progress-futures\|Lin et al. 2023: TinyML — Progress and Futures]] — surveys QAS as part of the MCUNetV3 on-device-training contribution
