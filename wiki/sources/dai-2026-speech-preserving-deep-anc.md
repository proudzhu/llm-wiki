---
type: source
created: 2026-04-22
updated: 2026-04-25
sources:
  - http://arxiv.org/abs/2604.10979
  - zotero://select/items/0_C9Q3C69G
tags:
  - active-noise-control
  - deep-learning
  - speech-preservation
  - convolutional-recurrent-network
  - complex-spectrum-mapping
  - reverberant-environment
---

# Dai 2026: Speech-Preserving Deep ANC in Reverberant Environments

**Author**: [[entities/shuning-dai|Shuning Dai]]
**Supervisor**: Gan Woon Seng
**Institution**: Nanyang Technological University (School of EEE)
**Year**: 2026
**Type**: Master's Dissertation (MSc in Signal Processing and Machine Learning)
**arXiv**: [2604.10979](https://arxiv.org/abs/2604.10979)
**Zotero**: [C9Q3C69G](zotero://select/items/0_C9Q3C69G)

## Summary

This dissertation proposes an end-to-end **Deep ANC** system that solves two critical limitations of traditional FxLMS: (1) the inability to handle non-stationary/nonlinear acoustic paths, and (2) the accidental cancellation of desired speech. The system uses a **Convolutional Recurrent Network (CRN)** with **Complex Spectrum Mapping (CSM)** to selectively reduce noise while preserving speech fidelity in reverberant settings ($RT_{60} = 0.3s$). A custom **speech-preserving loss function** drives the network to generate anti-noise that cancels only the noise component, leaving the target speech transparent.

## Problem Formulation

### Signal Model
Single-channel feedforward ANC with three paths:
- **Primary path** $P(z)$: Noise source → error microphone
- **Secondary path** $S(z)$: Secondary speaker → error microphone (D/A, amplifier, speaker, acoustic channel, A/D)
- **Controller** $W(z)$: Reference mic → control signal

Error signal: $e(n) = d(n) - y(n) * s(n)$, where $d(n) = d_{noise}(n) + d_{speech}(n)$

### Spectral Selectivity
Traditional ANC minimizes $E[e^2(n)] \to 0$ (total cancellation). This work decomposes $d(n) = v(n) + s_{target}(n)$ and seeks $e(n) \approx s_{target}(n)$, meaning anti-noise $a(n) \approx -v(n)$ only.

### Complex Spectrum Mapping (CSM)
Instead of amplitude-only masking (which ignores phase), CSM simultaneously estimates real and imaginary STFT components:
- Input: $X_r(m,k)$ and $X_i(m,k)$ as two independent channels
- Output: $Y_r(m,k)$ and $Y_i(m,k)$ for the control signal
- Reconstruction via iSTFT: $y(n) = \text{iSTFT}(Y_r + jY_i)$
- STFT: 320-point FFT (20 ms frame), 160-point hop (10 ms), Hanning window, 50% overlap

## CRN Architecture

Encoder → LSTM Bottleneck → Decoder with skip connections (U-Net style):

| Module | Layer | Kernel (T,F) | Stride (T,F) | Channels | Activation |
|--------|-------|-------------|-------------|----------|------------|
| Encoder | 5× Conv2d | 2×3 | 5×(1,2) | 16→32→…→1024 | ELU |
| Bottleneck | Linear Projection | - | - | 1024→256 | Linear |
| Bottleneck | 2× LSTM | - | - | Hidden: 256 | Tanh/Sigmoid |
| Decoder | 5× Transposed Conv2d | 2×3 | 5×(1,2) | 1024→…→32→16→2 | ELU/Linear* |

*Final output layer (2 channels) uses linear activation for complex spectrum (real + imaginary). Skip connections between matching encoder-decoder layers.

**Key design choices**:
- **Causal convolution**: Asymmetric zero-padding (past only, no future) ensures real-time deployability
- **ELU activation**: More robust than ReLU for negative inputs common in audio spectra
- **Linear projection**: 1024→256 before LSTM reduces parameters for real-time feasibility
- **Skip connections**: Preserve fine-grained phase details from encoder to decoder

## Acoustic Environment Simulation

### Image Source Method (ISM) via pyroomacoustics
- **Room**: 4m × 3m × 2.5m (small office / vehicle interior)
- **Reverberation**: $RT_{60} = 0.3s$ (moderate acoustic treatment)
- **Sampling rate**: 16 kHz
- **RIR length**: 512 points (truncated)

| Component | Coordinate (x,y,z) [m] | Description |
|-----------|------------------------|-------------|
| Primary noise source | (1.00, 1.50, 1.20) | Co-located with ref mic |
| Reference microphone | (1.00, 1.50, 1.20) | Captures reference signal |
| Error microphone | (3.00, 1.50, 1.20) | Target noise reduction position |
| Secondary source | (3.05, 1.50, 1.20) | 5 cm from error mic (near-field) |

The 5 cm secondary-source-to-error-mic distance simulates near-field applications (e.g., ANC headrests) and minimizes acoustic delay for broadband causality.

## Speech Preservation Strategy

### Supervised Learning Framework
Secondary path $s(n)$ is modeled as a **fixed convolutional layer** after the CRN output:
- Forward: $a(n) = y(n) * s(n)$
- Backward: Gradients propagate through frozen $s(n)$ to CRN
- Network learns to compensate for secondary path amplitude/phase distortion implicitly

### Speech-Preserving Loss Function
$$\mathcal{L}_{speech} = \frac{1}{L} \sum_{n=1}^{L} (e(n) - d_{speech}(n))^2$$

Substituting $e(n) = d_{noise}(n) + d_{speech}(n) + a(n)$:

$$\mathcal{L}_{speech} = \frac{1}{L} \sum_{n=1}^{L} (d_{noise}(n) + a(n))^2$$

The speech components cancel algebraically, leaving a loss that minimizes residual noise only. The network learns $a(n) \approx -d_{noise}(n)$ without any incentive to cancel speech.

## Training Configuration

| Category | Parameter | Value |
|----------|-----------|-------|
| Acoustic | Sampling Rate | 16 kHz |
| Acoustic | Frame Size / Hop | 320 / 160 samples (20/10 ms) |
| Acoustic | Input | STFT (Real, Imag) |
| Optimization | Optimizer | Adam |
| Optimization | Learning Rate | 0.0005 (pre-train) / 0.00025 (fine-tune) |
| Optimization | Loss | Speech-Preserving MSE |
| Optimization | Gradient Clipping | Threshold = 5.0 |
| Optimization | AMP | Mixed FP16/FP32 |
| Training | Batch Size | 16 |
| Training | Epochs | 70 (40 pre-train + 30 fine-tune) |

**Two-stage training**:
1. Pre-training (40 epochs, lr=0.0005): Learn physical acoustic characteristics and secondary path inverse mapping
2. Fine-tuning (30 epochs, lr=0.00025): Refine near loss minimum

**Data**: 10,000 samples each for pure noise and speech-preservation tasks. Noise from NOISEX-92, speech from LibriSpeech test-clean. Dynamic mixing with SNR ∈ [0, 10] dB.

## Results

### Pure Noise Reduction (RT60 = 0.3s)

| Noise Type | Category | FxLMS (dB) | Deep ANC (dB) | Improvement |
|:-----------|:---------|:-----------|:--------------|:------------|
| Engine | Periodic | 12.22 | 22.92 | +10.70 |
| Babble | Non-stationary | 5.28 | 18.17 | +12.89 |
| Factory1 | Non-stationary | 6.17 | 18.49 | +12.32 |
| Volvo | Stationary | 4.91 | 19.08 | +14.17 |
| F16 | Broadband | 8.71 | 17.35 | +8.64 |

### Speech Preservation (SNR = 5 dB)

| Noise Type | Category | NR (dB) | PESQ Improvement | STOI Improvement |
|:-----------|:---------|:--------|:-----------------|:-----------------|
| Engine | Periodic | 8.88 | +0.686 | +0.101 |
| Babble | Non-stationary | 5.30 | +0.359 | +0.066 |
| Factory1 | Non-stationary | 7.22 | +0.444 | +0.080 |
| Volvo | Stationary | 13.70 | +0.464 | +0.001 |
| F16 | Broadband | 8.19 | +0.632 | +0.100 |

### Key Physical Insights
- **Harmonic comb filter**: Deep ANC precisely levels harmonic peaks (e.g., 1500 Hz, 2200 Hz in Engine) with >20 dB local attenuation, while FxLMS leaves residual spikes
- **Nonlinear compensation**: 10-15 dB improvement over FxLMS at harmonic frequency points due to implicit nonlinear modeling
- **Transient response**: Deep ANC enters steady-state instantly; FxLMS remains under-converged under Babble due to gradient lag
- **Waveform fidelity**: In Volvo scenario, output waveform nearly perfectly overlaps clean speech (phase-aligned, envelope-preserved)

## Key Contributions

1. **Selective ANC via speech-preserving loss**: First comprehensive integration of a speech-preservation mechanism into a deep-learning ANC control loop, using algebraic cancellation in the loss function
2. **Robustness in reverberant environments**: Validated in ISM-simulated room with RT60=0.3s, not ideal anechoic conditions
3. **Nonlinear compensation**: CRN implicitly models and suppresses secondary path nonlinearities (speaker harmonic distortion), outperforming FxLMS by 10-15 dB at harmonic peaks
4. **Speech fidelity**: PESQ and STOI evaluations confirm enhanced hearing naturalness without damaging intelligibility

## ANC vs Speech Enhancement Distinction

The paper clearly distinguishes speech-preserving ANC from traditional Speech Enhancement (SE):
- **Real-time constraints**: ANC must generate anti-noise within sound propagation delay (<10 ms); SE can tolerate longer latency
- **Physical superposition**: ANC achieves cancellation via wave interference in air; SE filters in the digital domain
- **Secondary path compensation**: Deep ANC must account for the electroacoustic transfer function; SE does not model physical propagation

## Future Work Directions

1. **Time-domain architecture**: Replace STFT with Wave-U-Net for sub-millisecond latency; model quantization/pruning for embedded deployment
2. **Multi-channel + spatial selectivity**: Combine spectral selectivity with beamforming for directional sound control
3. **Hybrid architecture**: Traditional FxLMS for steady-state + deep network for non-stationary/nonlinear components
4. **Adaptive mechanisms**: Meta-learning and online fine-tuning for dynamic acoustic environments (changing secondary paths)

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/speech-preserving-anc|Speech-Preserving ANC]]
- [[concepts/image-source-method|Image Source Method]]
- [[concepts/transparency-mode|Transparency Mode]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Synthesis

- [[synthesis/ai-driven-anc|AI-Driven ANC]]
- [[synthesis/nonlinear-anc-approaches|Nonlinear ANC Approaches]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]

## Related Entities

- [[entities/shuning-dai|Shuning Dai]] — Author
