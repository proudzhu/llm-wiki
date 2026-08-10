---
type: source
created: 2026-08-10
updated: 2026-08-10
sources:
  - raw/papers/timcheck-2023-intel-neuromorphic-dns-challenge/full-text.md
  - https://doi.org/10.48550/arXiv.2303.09503
  - zotero://select/items/0_TJJYB8BC
tags:
  - speech-enhancement
  - neuromorphic-computing
  - spiking-neural-networks
  - challenge
  - benchmark
  - low-power
  - real-time
  - intel
  - loihi
  - audio-denoising
---

# Timcheck, Shrestha, Rubin, Kupryjanow, Orchard, Pindor, Shea & Davies 2023: The Intel Neuromorphic DNS Challenge

- **Authors**: [[entities/jonathan-timcheck|Jonathan Timcheck]], [[entities/sumit-bam-shrestha|Sumit Bam Shrestha]], [[entities/daniel-ben-dayan-rubin|Daniel Ben Dayan Rubin]], [[entities/adam-kupryjanow|Adam Kupryjanow]], [[entities/garrick-orchard|Garrick Orchard]], [[entities/lukasz-pindor|Lukasz Pindor]], [[entities/timothy-shea|Timothy Shea]], [[entities/mike-davies|Mike Davies]]
- **Institutions**: Neuromorphic Computing Lab, Intel Labs; Design Engineering Group Poland, Intel
- **Venue**: arXiv preprint 2303.09503v3 (1 Aug 2023); subsequently published in *Neuromorphic Computing and Engineering*
- **Type**: Preprint / challenge paper
- **DOI**: [10.48550/arXiv.2303.09503](https://doi.org/10.48550/arXiv.2303.09503)
- **arXiv**: [2303.09503](http://arxiv.org/abs/2303.09503)
- **Zotero**: [TJJYB8BC](zotero://select/items/0_TJJYB8BC)
- **Code**: [IntelLabs/IntelNeuromorphicDNSChallenge](https://github.com/IntelLabs/IntelNeuromorphicDNSChallenge) (MIT license)

## Summary

The Intel Neuromorphic DNS Challenge (Intel N-DNS Challenge) is a benchmark and competition framework that targets **real-time monaural audio denoising on neuromorphic hardware**, inspired by the Microsoft [[concepts/dns-challenge|DNS Challenge]] but reframed around power/latency/resource efficiency rather than audio quality alone. The paper introduces two tracks — a simulation-based algorithmic track (Track 1, proxy power/latency) and a [[concepts/loihi-2|Loihi 2]] hardware track (Track 2, measured power/latency) — defines a holistic evaluation methodology (audio quality + power + latency + chip resources), releases a 500-hour dataset derived from the Microsoft DNS Challenge corpus, and provides an SDNN (sigma-delta neural network) baseline that achieves comparable audio quality to Microsoft [[concepts/nsnet2|NsNet2]] with an **order-of-magnitude lower power proxy** and **5× fewer parameters**. The challenge is the primary benchmark referenced by SNN-based speech enhancement work such as [[concepts/sse-net|SSE-Net]] ([[sources/liu-2026-sse-net|Liu et al. 2026]]).

## Problem Formulation

The paper identifies a gap in the neuromorphic computing field: most benchmarks are bespoke, custom tasks designed to highlight a single neuromorphic system, making cross-system comparison impossible. To address this, the authors select **audio denoising** as a challenge task because it:

1. Is ubiquitous and commercially relevant (voice calls, hearing aids, ASR front-ends).
2. Plays to neuromorphic strengths: low-bandwidth, temporal, sparse T-F structure, low-power edge deployment.
3. Has an established conventional counterpart (Microsoft DNS Challenge) for direct comparison.
4. Is unsaturated and not computationally prohibitive.

The single-microphone denoising task follows the standard additive noise model in the time domain:

$$
y(t) = x(t) + n(t),
$$

with optional reverberant extension $y(t) = h(t) * x(t) + n(t)$. The objective is to recover $x(t)$ from $y(t)$ in real time (≤40 ms end-to-end latency) on a neuromorphic system.

### Critique of prior neuromorphic benchmarks

The paper reviews existing neuromorphic challenges and identifies their limitations:

| Benchmark | Limitation |
|-----------|------------|
| N-MNIST / N-Caltech101 | Source is static image; lacks spatiotemporal content once saccadic motion compensated |
| DVS Gesture | Specialized event-based sensor; small dataset (1,342 instances); fine-grained timing not vital (25 ms timestep suffices) |
| Spiking Heidelberg Datasets (keyword spotting) | Cochlear encoding power cost unquantified; information preservation unquantified; bottleneck for harder audio tasks |
| Braille reading, EMG+DVS gesture fusion | Niche sensors/applications; limited real-world impact |

Audio denoising is positioned as addressing all these shortcomings.

## Methodology

### Challenge structure

![[raw/papers/timcheck-2023-intel-neuromorphic-dns-challenge/figures/6d2216ea8f2e7ae2fcfc85d0cbfe8075acd0f0336904ef3ac5cc3a18d49cd67f.jpg|Intel N-DNS Challenge solution structure]]

*Figure 2: Intel N-DNS Challenge solution structure. Noisy audio is encoded, processed by a neuromorphic denoiser (N-DNS), and decoded back to clean audio. Track 1 simulates the N-DNS on CPU; Track 2 runs it on Loihi 2 hardware.*

The challenge defines two tracks:

- **Track 1 (Algorithmic)**: Develop a high-quality denoising solution that operates efficiently on a neuromorphic system. The neuromorphic component is **simulated** on conventional hardware; latency and a power proxy are estimated. Intended for rapid development and to inspire future hardware features.
- **Track 2 (Loihi 2)**: Develop a denoising system that runs on actual [[concepts/loihi-2|Loihi 2]] hardware. Power and latency are **measured**, not estimated.

Both tracks share the same pipeline: noisy audio → encoder → neuromorphic denoiser → decoder → clean audio. The encoder, decoder, and neuromorphic denoiser are all constituents of a solution and all contribute to power/latency evaluation.

### Real-time latency definition

![[raw/papers/timcheck-2023-intel-neuromorphic-dns-challenge/figures/ff8fc6416acfc9b9f7c7cb9c7c22365325fa041dce466088c413ed9d0cd562e8.jpg|Real-time N-DNS pipeline]]

*Figure 3: Real-time N-DNS pipeline. Latency sums data buffer latency, encoder–decoder (CPU) latency, and N-DNS network latency. Track 1 excludes the (CPU) neuromorphic denoiser processing time, assuming neuromorphic hardware parallelism completes a timestep in microseconds.*

End-to-end latency must be ≤40 ms for a solution to qualify as real-time. Latency is decomposed into:

1. **Data buffer latency** — time to collect audio for one discrete timestep (e.g., STFT window length).
2. **Encoder–decoder latency** — wall-clock time to encode one timestep and decode it back.
3. **Network (N-DNS) latency** — algorithmic delay introduced by the neuromorphic denoiser, measured as the maximum cross-correlation lag between clean target and denoised output.

In Track 1, the CPU processing time for the simulated neuromorphic denoiser is *excluded* from latency (the assumption being that real neuromorphic hardware completes spike processing within microseconds per timestep). In Track 2, latency is measured directly on a reference CPU + Loihi 2 system.

### Power and power-delay product

For Track 1, the paper defines a **power proxy** based on neuromorphic computational primitives:

$$
P_{\text{proxy}} = \text{Effective SynOPS} = \text{SynOPS} + 10 \times \text{NeuronOPS},
$$

where SynOPS and NeuronOPS are the mean synaptic operations and neuron updates per second of audio processed in the N-DNS stage. The 10× weighting reflects measurements on the Loihi architecture showing one neuron operation costs ≈10× one synaptic operation. For conventional networks (e.g., NsNet2), "Ops" refer to multiply–accumulate operations (MACs). The **PDP proxy** is $P_{\text{proxy}} \times L$ (units of Ops). Encoder/decoder power is excluded from Track 1 for simplicity (and is implicitly bounded by the real-time constraint).

For Track 2, power is directly measured on the CPU + Loihi 2 reference system, and $PDP = P_{\text{Track2}} \times L$.

### Chip resource metrics

For Track 2, the definitive resource metric is **core count** on Loihi 2. For Track 1 (where mapping to chip is not yet done), indirect measures are used: **parameter count** (unique synaptic state + neuron parameters, exploiting convolutional/compression features) and **model size** (sum of bit widths of all unique parameters in bytes). Because Loihi 2 supports 1–8 bit synaptic weights, two networks with the same parameter count can have very different model sizes.

### Audio quality metrics

- **SI-SNR** (Scale-Invariant Source-to-Noise Ratio): $10 \log_{10} \frac{\|s_{\text{target}}\|^2}{\|e_{\text{noise}}\|^2}$, where $s_{\text{target}} := \frac{\langle \hat{s}, s \rangle s}{\|s\|^2}$ and $e_{\text{noise}} := \hat{s} - s_{\text{target}}$. Chosen for simplicity, generality, scale invariance, and direct usability as a training loss.
- **DNSMOS** — deep-network predictor of Mean Opinion Score, with three subscores: SIG (speech signal quality), BAK (background noise quality), OVRL (overall). Chosen for high correlation with human perceptual assessment; DNSMOS (OVRL) was used in the Microsoft DNS Challenge, enabling cross-comparison.
- **Minimum SI-SNR improvement requirements**:
  - $\text{SI-SNRi}_{\text{data}} > 3\,\text{dB}$ (improvement over noisy input)
  - $\text{SI-SNRi}_{\text{enc+dec}} > 3\,\text{dB}$ (improvement attributable to the neuromorphic denoiser itself, beyond encoder/decoder processing)

The second requirement enforces the spirit of the challenge: the neuromorphic component must be responsible for a significant portion of the denoising, not merely a passthrough while the encoder/decoder do the work.

### Baseline solution: sigma-delta neural network (SDNN)

![[raw/papers/timcheck-2023-intel-neuromorphic-dns-challenge/figures/f7ae816676794ab710402694e4449781a7386d2c6198056e3e9f937f986cdb5f.jpg|Sigma-delta neural network baseline solution structure]]

*Figure 4: SDNN baseline solution structure. STFT encoder → delta-encoded magnitude → 3-layer feedforward sigma-delta ReLU network with axonal delays → multiplicative mask → ISTFT decoder.*

The released baseline (Track 1) is a [[concepts/sigma-delta-neural-network|sigma-delta neural network (SDNN)]] — a feedforward ReLU architecture adapted to neuromorphic computation via two mechanisms:

1. **Sparse message passing (sigma-delta encoding)**: Delta encoding transmits only changes exceeding a threshold, sparsifying inter-layer communication; sigma encoding reconstructs the signal at the receiving end. A sigma-delta neuron wraps a ReLU nonlinearity with these units, drastically reducing synaptic operations on data with temporal similarity.
2. **Axonal delays**: Learnable delays endow the network with short-term memory, allowing interaction of features from different points in time — important for spatio-temporal audio processing.

**Pipeline**:

- **Encoder**: STFT of noisy audio (window 512, hop 128 → 8 ms timestep at 16 kHz), followed by delta encoding of the STFT magnitude.
- **N-DNS**: 3-layer feedforward sigma-delta ReLU network with axonal delays, predicting a multiplicative mask at some delay.
- **Decoder**: Combine the predicted mask with the delayed STFT magnitude and phase, then ISTFT with the same window/hop.

Training uses Lava-dl (an extended SLAYER backpropagation tool with surrogate gradients for non-differentiable spikes), quantization-aware (matching Loihi 2 fixed-precision), with a combined negative-SI-SNR + STFT-magnitude-MSE loss and a RADAM optimizer.

### Neuromorphic features utilized

The baseline deliberately uses only a subset of Loihi 2's performant features, leaving substantial room for improvement:

| Neuromorphic feature | In baseline |
|---|---|
| Sparse activity | ✓ |
| Sparse connectivity | ✗ |
| Recurrence | ✗ |
| Stateful neurons | ✓ |
| Neuron temporal dynamics | ✗ |
| Synaptic plasticity | ✗ |
| Graded spikes | ✓ |
| Delay as computational element | ✓ |

## Experimental Setup

| Aspect | Configuration |
|--------|---------------|
| **Task** | Real-time monaural audio denoising |
| **Dataset** | Intel N-DNS dataset (derived from Microsoft DNS Challenge corpus); 500 hours / 60,000 samples of 30-second segments; clean + noise + noisy at 16 kHz, 16-bit; synthesized SNR 20 dB to −5 dB; languages include English, German, French, Spanish, Russian |
| **Audio quality metrics** | SI-SNR, SI-SNRi (vs. data and vs. enc+dec), DNSMOS (SIG/BAK/OVRL) |
| **Compute metrics** | Latency (≤40 ms real-time), Power proxy (SynOPS + 10×NeuronOPS), PDP proxy, Parameter count, Model size |
| **Real-time threshold** | 40 ms end-to-end latency |
| **Min. quality improvement** | SI-SNRi_data > 3 dB AND SI-SNRi_enc+dec > 3 dB |
| **Baselines compared** | Microsoft NsNet2 (DNS 2022 baseline), Intel DNS network (proprietary production model, LSTM + 2D conv, power unavailable) |
| **Evaluation system** | Intel Xeon Platinum 8280 @ 2.70 GHz, 32 GB RAM (Feb 2023) |
| **SDNN encoder** | STFT, window 512, hop 128 (8 ms timestep) |
| **SDNN architecture** | 3-layer feedforward sigma-delta ReLU with axonal delays |
| **SDNN training** | Lava-dl / SLAYER surrogate gradient; quantization-aware; loss = −SI-SNR + STFT-magnitude MSE; RADAM optimizer |

## Results

### Track 1 baseline comparison (validation set)

| Network | SI-SNR (dB) | SI-SNRi data (dB) | SI-SNRi enc+dec (dB) | DNSMOS OVRL | DNSMOS SIG | DNSMOS BAK | Latency enc+dec (ms) | Latency total (ms) | Power proxy (M-Ops/s) | PDP proxy (M-Ops) | Params (×10³) | Model size (KB) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Microsoft NsNet2 | 11.89 | 4.26 | 4.26 | 2.95 | 3.27 | 3.94 | 0.024 | 20.024 | 136.13 | 2.72 | 2,681 | 10,500 |
| Intel DNS network | 12.71 | 5.09 | 5.09 | 3.09 | 3.35 | 4.08 | 0.036 | 32.036 | — | — | 1,901 | 3,802 |
| **SDNN baseline** | **12.50** | **4.88** | **4.88** | 2.71 | 3.21 | 3.46 | 0.036 | 32.036 | **14.54** | **0.44** | **525** | **465** |
| Validation (noisy) | 7.62 | — | — | 2.45 | 3.19 | 2.72 | — | — | — | — | — | — |

*Table II: Evaluation metrics comparison. Audio quality: higher is better. Compute/resource: lower is better. DNSMOS scores are not directly comparable to Microsoft DNS Challenge scores due to differing validation/test set composition.*

### Key findings

- **Audio quality**: SDNN baseline achieves **higher SI-SNR than NsNet2** (12.50 vs. 11.89 dB) — expected since training targeted SI-SNR loss. DNSMOS OVRL is lower than NsNet2 (2.71 vs. 2.95), but substantially improved over noisy input (2.45).
- **Power efficiency**: SDNN baseline power proxy is **14.54 M-Ops/s — 9.4× lower than NsNet2** (136.13 M-Ops/s), despite processing data at 1.25× higher throughput.
- **PDP**: 0.44 M-Ops for SDNN vs. 2.72 M-Ops for NsNet2 — **6.2× lower**.
- **Parameters**: 525K vs. 2,681K — **5× fewer**.
- **Model size**: 465 KB vs. 10,500 KB — **22× smaller**, attributed to quantization-aware training matching Loihi 2's 1–8 bit synaptic weights.
- **Latency**: SDNN total 32.036 ms (well under the 40 ms real-time threshold); NsNet2 20.024 ms. SDNN's higher latency is due to its 8 ms STFT timestep vs. NsNet2's finer-grained buffering.
- **Intel DNS network** (proprietary, production): highest SI-SNR (12.71) and DNSMOS across the board, but no power metrics available; serves as an "upper-bound aspirational target" for challenge submissions.

### Interpretation

The authors emphasize that the SDNN baseline is a *deliberately simple* feedforward architecture that exploits only 4 of 8 performant Loihi 2 features (Table I). They anticipate that solutions incorporating recurrence, sparse connectivity, neuron temporal dynamics, and synaptic plasticity will yield *further* significant improvements in power and model size — motivating the challenge's open call for algorithmic innovation.

The sigma-delta approach is highlighted as **general**: sigma-delta sparsification can be applied to any ReLU-like nonlinearity and to typical neuromorphic neuron dynamics (leaky integrators, resonators), making it one of many neuromorphic features available to challenge participants.

## Key Contributions

1. **Identify audio denoising as an excellent neuromorphic challenge task** — ubiquitous, commercially relevant, low-bandwidth, temporal, sparse T-F structure, well-matched to neuromorphic hardware. Addresses shortcomings of prior neuromorphic benchmarks (N-MNIST, DVS Gesture, Spiking Heidelberg Datasets).
2. **Define a two-track challenge structure** — Track 1 (algorithmic, simulated, proxy metrics) for rapid iteration and Track 2 (Loihi 2 hardware, measured metrics) for rigorous demonstration, bridging algorithmic innovation and hardware reality.
3. **Holistic evaluation methodology** — beyond audio quality, define metrics for power (proxy + measured), latency (with explicit decomposition), and chip resources (core count for Track 2; parameter count + model size for Track 1), plus the derived PDP. The minimum-SI-SNRi requirements enforce that the neuromorphic component itself contributes meaningfully to denoising.
4. **Power proxy formulation** — $P_{\text{proxy}} = \text{SynOPS} + 10 \times \text{NeuronOPS}$, calibrated to Loihi energy measurements, enabling Track 1 comparison without neuromorphic hardware. This proxy has been adopted by subsequent SNN-SE work (e.g., [[concepts/sse-net|SSE-Net]]).
5. **Public dataset and tooling** — 500-hour dataset derived from Microsoft DNS Challenge corpus, dataloader modules, evaluation pipeline, and baseline solution released under MIT license at [IntelLabs/IntelNeuromorphicDNSChallenge](https://github.com/IntelLabs/IntelNeuromorphicDNSChallenge).
6. **SDNN baseline demonstrating neuromorphic advantage** — a simple sigma-delta ReLU network with axonal delays achieves NsNet2-comparable SI-SNR with **9.4× lower power proxy, 5× fewer parameters, and 22× smaller model size**, providing a concrete starting point and motivating the challenge's premise that ≥10× power reductions are achievable on neuromorphic hardware.

## Related Concepts

- [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]] — the canonical concept page for this benchmark
- [[concepts/loihi-2|Loihi 2]] — Intel neuromorphic chip targeted by Track 2
- [[concepts/sigma-delta-neural-network|Sigma-Delta Neural Network (SDNN)]] — baseline architecture
- [[concepts/neuromorphic-computing|Neuromorphic Computing]]
- [[concepts/spiking-neural-networks|Spiking Neural Networks]]
- [[concepts/dns-challenge|DNS Challenge (Microsoft)]] — the ANN-era predecessor that inspired this challenge
- [[concepts/nsnet2|NSNet2]] — Microsoft DNS 2022 baseline used for comparison
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]] — the Intel N-DNS Challenge's power/latency/resource methodology contributes a neuromorphic axis to the cross-source efficiency comparison
