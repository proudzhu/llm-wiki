---
type: concept
created: 2026-08-11
updated: 2026-08-11
sources:
  - raw/papers/le-2026-efficient-nn-tinyml-review/full-text.md
tags:
  - model-compression
  - pruning
  - sparsity
  - efficient-deep-learning
  - tinyml
  - bayesian-compression
---

# Model Pruning

**Model pruning** is a model-compression technique that removes less-important parameters (weights, neurons, filters, or channels) from a trained neural network to reduce its size and computational cost. It exploits the overparameterization of deep networks — "only a small fraction of the total parameters are critical" (Denil et al. 2013) — and can be viewed simultaneously as a compression method, a form of regularization (analogous to dropout but permanent), and a form of [[concepts/neural-architecture-search|neural architecture search]] aiming to find Pareto-optimal architectures.

## Taxonomy

Pruning methods are organized along two orthogonal axes: **granularity** (unstructured vs structured) and **induction method** (magnitude-based, regularization-based, [[concepts/bayesian-compression|Bayesian]]). The Lê et al. (2026) review of TinyML adds Bayesian pruning as a third granularity-level category that subsumes both.

### Unstructured Pruning

Removes individual fine-grained weights scattered throughout the weight matrices. It is "the simplest and most sparsity-inducing type of pruning because trained NNs are less sensitive to one weight than a specific block."

- **Magnitude-based pruning** — remove weights by absolute value; "model- and task-agnostic, can seamlessly incorporate within training, and is easy to implement." Gale et al. (2017) showed it provides state-of-the-art or comparable performance to more complex methods.
- **Polynomial gradual sparsity** (Zhu & Gupta 2017) — at every $\Delta t$ steps, set a gradual number of lowest-magnitude weights to zero until target sparsity $s_f$ is reached:
  $$s_t = s_f + (s_0 - s_f) \left(1 - \tfrac{t - t_0}{n \Delta t}\right)^3$$
  The cubic schedule "prune[s] quickly and early when there is the most redundancy, and then slow down... as there is little remaining redundancy." Golatkar et al. (2019) found that the early regularization phase is the most critical to performance, supporting early pruning.
- **Lottery Ticket Hypothesis** (Frankle & Carbin 2018) — dense networks contain sparse subnetworks ("winning tickets") that train to comparable accuracy from initialization. The Strong Lottery Ticket Hypothesis (SLTH) extends this to universal tickets across applications, suggesting "training DL models could be replaced by efficient NN pruning" (Burkholz et al. 2022).

**Advantage**: highest sparsity rate (up to 90% with acceptable accuracy loss on large networks); flexible across architectures. **Disadvantage**: "sporadically induced weights... may be difficult to efficiently leverage on embedded hardware," although "previous work demonstrated that it is possible to leverage high sparsity with practical encoding" (Han et al. 2016).

### Structured Pruning

Removes parameters in blocks — neurons, filters, channels, entire rows or columns of weight matrices — preserving dense-matrix layout. "The clear advantage of structured pruning is that it is hardware efficient because it may allow skipping entire filters or rows during a matrix multiplication."

- **Redundancy-based** — Srinivas & Babu identify duplicate neuron pairs and remove one with a recovery step.
- **Regularization-based** — penalty terms encourage channel-level pruning in CNNs (He et al. 2017; Molchanov et al.), neuron-level pruning (Alvarez & Salzmann 2016), or layer-level pruning. Achieves ~60% sparsity without significant loss.

**Disadvantage**: "strict compression rules that make them more difficult to achieve without degrading performance and require a certain amount of block sparsity to obtain a faster runtime than baseline." Wider, sparser networks tend to generalize better than smaller dense counterparts produced by structured pruning (Ballas 2022; Golubeva et al. 2021; Hoefler et al. 2021).

### Bayesian Pruning

Uses Bayesian inference with sparsity-inducing priors to drive parameters toward zero, then prunes parameters whose posterior mass concentrates at zero. The Lê et al. (2026) review presents this as a unifying third category; see [[concepts/bayesian-compression|Bayesian Compression]] for the spike-and-slab, horseshoe, and log-uniform prior formulations.

## Combining Pruning with Other Compression Methods

Multiple works show that combining pruning with other model-compression methods — particularly quantization — produces high compression rates without significant performance loss:

| Combination | Dataset | Result |
|-------------|---------|--------|
| Pruning + quantization + Huffman encoding (Han et al. 2016) | ImageNet | 49× size reduction, <0.5% accuracy loss |
| Bayesian structured pruning (Fedorov et al. 2019) | MNIST | 80× parameter reduction, 98.64% accuracy, 2.77 kB model |
| Structured pruning (Liberis & Lane) | Google Speech Commands v2-12 | 96.03% accuracy, 115 kB model |

## TinyML Considerations

For TinyML deployment on ultra-low-power MCUs:

- **Structured pruning is "effective out of the box"** for TinyML because it produces hardware-efficient dense subnetworks that integrate cleanly with [[concepts/tinymlops|TinyMLOps]] frameworks like TFLM and CMSIS-NN.
- **Unstructured pruning "poses challenges in fully leveraging its benefits for edge inference"** — sparse-matrix kernels are not natively supported on Cortex-M MCUs, so the speedup from sparsity may not materialize without custom sparse encodings.
- **Magnitude-based pruning is natively supported by TensorFlow** via the `tfmot` toolkit, easing integration with TFLM-based deployment pipelines.
- **Bayesian pruning** yields the highest compression ratios (80× on MNIST) but requires variational-inference training infrastructure not yet standard in TinyMLOps toolchains.

The review notes that "structured pruning approaches are more hardware efficient" while "unstructured pruning approaches are more flexible across diverse architectures and yield the highest sparsity rate" — a fundamental tradeoff for TinyML practitioners.

## Related Concepts

- [[concepts/bayesian-compression|Bayesian Compression]] — spike-and-slab, horseshoe, log-uniform priors for pruning and quantization
- [[concepts/tinyml|TinyML]] — the deployment context where pruning is most binding
- [[concepts/neural-architecture-search|Neural Architecture Search]] — pruning as a form of NAS
- [[concepts/quantization-aware-training|Quantization-Aware Training]] — frequently combined with pruning
- [[concepts/post-training-quantization|Post-Training Quantization]] — frequently combined with pruning

## Related Sources

- [[sources/le-2026-efficient-nn-tinyml-review|Lê, Wolinski & Arbel 2026: Efficient NNs for TinyML — A Comprehensive Review]] — presents the unstructured/structured/Bayesian taxonomy for TinyML
- [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024: Lightweight Deep Learning for Resource-Constrained Environments]] — surveys pruning as one of four compression methods
