---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
tags:
  - deep-learning
  - optimization
  - training
---

# Adam Optimizer

**Adam** (Adaptive Moment Estimation), introduced by Kingma and Ba (2015), is an adaptive learning rate optimization algorithm that computes individual adaptive learning rates for each parameter using estimates of the first and second moments of the gradients. It is widely used for training [[concepts/recurrent-neural-network\|recurrent neural networks]] and deep learning models in general.

## Update Equations

Given gradient $\mathbf{g}_t$ at step $t$, Adam maintains exponential moving averages of the gradient (first moment) and squared gradient (second moment):

$$
\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1)\mathbf{g}_t, \tag{1}
$$

$$
\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2)\mathbf{g}_t^2, \tag{2}
$$

Bias-corrected estimates:

$$
\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t}, \quad \hat{\mathbf{v}}_t = \frac{\mathbf{v}_t}{1 - \beta_2^t}, \tag{3}
$$

Parameter update:

$$
\theta_t = \theta_{t-1} - \alpha \frac{\hat{\mathbf{m}}_t}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon}, \tag{4}
$$

where $\alpha$ is the learning rate, $\beta_1, \beta_2$ are decay rates (typically 0.9 and 0.999), and $\epsilon$ is a small constant for numerical stability.

## Properties

- **Adaptive per-parameter learning rates** — parameters with large gradients get smaller effective learning rates, and vice versa.
- **Bias correction** — compensates for the initialization bias of moment estimates in early steps.
- **Robust to hyperparameter choice** — works well across a wide range of learning rates and decay rates.
- **First-order method** — only requires gradients, no Hessian computation (unlike second-order methods like Hessian-free optimizers).

## Use in RNN Training

Per [[sources/mienye-2024-rnn-comprehensive-review\|Mienye et al. 2024]], Adam is highlighted as a key advanced optimization technique for RNNs, often combined with [[concepts/gradient-clipping\|gradient clipping]] to handle exploding gradients.

## Related Concepts

- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/gradient-clipping\|Gradient Clipping]]
- [[concepts/vanishing-gradient-problem\|Vanishing/Exploding Gradient Problem]]
- [[concepts/backpropagation-through-time\|Backpropagation Through Time]]

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]] — Section 5.3 covers Adam and other advanced optimization techniques
