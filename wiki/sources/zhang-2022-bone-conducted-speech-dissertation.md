---
type: source
created: 2026-04-22
updated: 2026-04-28
sources:
  - raw/papers/zhang-2022-bone-conducted-speech-dissertation/full-text.txt
  - https://doi.org/10.24561/00019784
  - zotero://select/items/0_T6BE3UFG
tags:
  - bone-conduction
  - signal-processing
  - pitch-extraction
  - speech-synthesis
  - doctoral-dissertation
  - least-squares
  - iir-filter
---

# Zhang 2022: Statistical Signal Processing of Bone-Conducted Speech

**Author**: Shiming Zhang (張 詩銘)
**Supervisor**: Professor Tetsuya Shimamura
**University**: Saitama University, Japan
**Year**: 2022
**Thesis Type**: Doctoral Dissertation
**DOI**: [10.24561/00019784](https://doi.org/10.24561/00019784)
**Zotero**: [T6BE3UFG](zotero://select/items/0_T6BE3UFG)

## Summary

This dissertation investigates the analysis and synthesis of Bone-Conducted (BC) speech using statistical signal processing. BC speech is captured via vibrations on the skull, making it highly robust to environmental noise (~10 dB SNR gain over AC) but limited in bandwidth (muffled sound). The work focuses on two main areas: (1) robust pitch extraction via dual-modal fusion (WACF-CEP and WACF-WACF), and (2) BC speech synthesis from Air-Conducted (AC) speech using a first-order IIR filter identified via Least Squares.

## Problem Formulation

### BC Speech Signal Model

The recorded AC and BC signals are modeled as:

```
xa(n) = sa(n) + va(n)    (AC: clean speech + noise)
xb(n) = sb(n) + vb(n)    (BC: clean speech + noise)
```

Key property: BC noise power is significantly lower than AC noise power across all noise types (white, babble, train, factory, car interior), yielding ~10 dB SNR gain.

### SNR Measurements (8 speakers, 5 noise types)

| Noise Type | AC SNR [dB] | BC SNR [dB] | BC Gain [dB] |
|------------|-------------|-------------|--------------|
| White | ~-1.0 | ~10.2 | ~11.1 |
| Babble | ~-1.3 | ~8.2 | ~9.5 |
| Train | ~-1.4 | ~8.5 | ~10.0 |
| Factory | ~-1.4 | ~8.3 | ~9.7 |
| Car | ~-1.3 | ~8.4 | ~9.7 |

## Methodology

### 1. Dual-Modal Pitch Extraction

#### 1.1 WACF-CEP Method

Combines AC Weighted Auto-Correlation Function with BC Cepstrum via nonlinear multiplication:

```
Wab(τ) = Qa(τ) · Cb(τ)
```

where:
- `Qa(τ)` = WACF of AC speech (resistant to noise via amplitude weighting)
- `Cb(τ)` = CEP of BC speech (clean due to ~10 dB SNR gain)

**Mechanism**: Multiplication enhances common pitch peaks while suppressing pseudo-peaks unique to each modality. AC noise and BC noise are statistically independent, so their error patterns don't correlate.

**Processing time**: 0.724 s per second of speech (vs 21.6 s for BaNa).

#### 1.2 WACF-WACF Method

Applies WACF to both AC and BC signals, then multiplies:

```
Ŵab(τ) = Wa(τ) · Wb(τ)
```

**Performance**: Superior to WACF-CEP in white (random) noise, but inferior in periodic noise (babble, train, factory, car) where CEP better corrects WACF errors.

#### 1.3 Experimental Setup

- **Speakers**: 4 male + 4 female
- **Sampling**: 16 kHz (downsampled from 44.1 kHz)
- **Frame**: 50 ms, 10 ms shift, Hamming window
- **FFT**: 1024 points
- **Pitch range**: 60-500 Hz
- **GPE threshold**: 10% deviation from reference
- **Noise types**: White, Babble, Train, Factory, Car interior
- **Baseline**: BaNa (state-of-the-art AC-only method)

#### 1.4 Results: Gross Pitch Error (GPE)

**WACF-CEP** outperforms all baselines (ACF, WACF, CEP, BaNa, CEP-BC) across all 5 noise types for both male and female speakers. Key findings:

- BaNa performs best among AC-only methods but degrades severely at low SNR
- CEP-BC (BC-only) outperforms all AC-only methods, confirming BC's noise robustness
- WACF-CEP combines the strengths of both modalities, achieving the lowest GPE
- Processing time is 30x faster than BaNa

**WACF-WACF** outperforms WACF-CEP in white noise but underperforms in periodic noise environments.

### 2. BC Speech Synthesis via LS-IIR

#### 2.1 Model

AC-to-BC conversion modeled as first-order IIR filter:

```
H(z) = β / (1 - αz⁻¹)
```

where 0 < α < 1, β > 0 ensures low-pass nature and stability.

Time-domain relation:

```
b̂(n) = α·b̂(n-1) + β·a(n)
```

#### 2.2 System Identification via Equation Error Approach

Direct minimization of `E = Σ[b(n) - b̂(n)]²` is nonlinear. Instead, use equation error:

```
b(n) - α·b(n-1) = β·a(n)
```

Reparameterize: p = 1/β, q = -α/β → `p·b(n) + q·b(n-1) = a(n)`

LS solution:

```
θ = (RᵀR)⁻¹RᵀV
```

where R is the observed data matrix from BC speech, V is the AC speech vector.

#### 2.3 Filter Design Procedure

1. Extract 15 frames per vowel (/a/, /i/, /u/, /e/, /o/) from recorded sentences
2. Pick 10 center frames (25 ms length, 10 ms overlap)
3. Compute LS coefficients for each frame
4. Select best (minimum E) and worst (maximum E) coefficient pairs
5. Average across speakers for general-purpose filter

#### 2.4 Identified Coefficients

| Case | α (male) | β (male) | E (male) | α (female) | β (female) | E (female) |
|------|----------|----------|----------|------------|------------|------------|
| Best (min error) | 0.75 | 0.20 | 0.14 | 0.76 | 0.21 | 0.16 |
| Worst (max error) | 0.66 | 0.31 | 0.36 | 0.65 | 0.34 | 0.41 |

**Coefficient ranges**: α ∈ [0.68, 0.81], β ∈ [0.17, 0.27] for best pairs.

**Filter characteristics**:
- Clear low-pass response with ~15-20 dB high-frequency attenuation
- Group delay: low-frequency components delayed by ~3 samples, high-frequency slightly advanced (<1 sample)
- Closed vowels (/i/, /u/) have larger LS errors than open vowels (/a/, /e/, /o/) — matches BC amplitude characteristics

#### 2.5 Why IIR over FIR?

- FIR filters create notch characteristics, unsuitable for smooth spectral attenuation
- IIR poles naturally create spectral peaks with smooth skirts matching BC attenuation curves
- First-order is sufficient; higher orders complicate stability analysis ("stability triangle" constraint)

### 3. Evaluation

#### 3.1 LAR Distance (Log-Area Ratio)

| Speakers | AC to BC | Filtered AC to BC | Improvement |
|----------|----------|-------------------|-------------|
| Male | 0.37 | 0.18 | 51% reduction |
| Female | 0.41 | 0.21 | 49% reduction |

Low LAR = processed speech similar to reference BC speech.

#### 3.2 Listening Test

20 listeners judged whether synthesized BC speech was closer to real AC or BC:

| Speech | Judged as BC | Judged as AC |
|--------|-------------|-------------|
| BCBM (male, best) | 20/20 | 0/20 |
| BCWM (male, worst) | 0/20 | 20/20 |
| BCBF (female, best) | 16/20 | 4/20 |
| BCWF (female, worst) | 0/20 | 20/20 |

Perfect score for male best case. Female case slightly lower due to higher pitch making AC/BC distinction less perceptible.

#### 3.3 Noise-Robustness of Synthesized BC

The IIR filter significantly reduces environmental noise power:
- White noise: extreme reduction (low-pass nature eliminates most energy)
- Babble/Train noise: 70-80% power reduction

#### 3.4 Pitch Extraction from Synthesized BC

Pitch extraction from synthesized BC speech outperforms extraction from both recorded AC and recorded BC speech, because:
- Synthesized BC inherits noise robustness from the IIR low-pass filtering
- AC speech suffers from strong first formant interference causing pitch detection errors
- BC speech can have accurate pitch detection but synthesized BC further cleans the signal

## Key Contributions

1. **WACF-CEP**: Dual-modal pitch extraction combining AC WACF with BC cepstrum, achieving lowest GPE across 5 noise types with 30x faster processing than BaNa.
2. **WACF-WACF**: Alternative dual-modal method superior in white noise but inferior in periodic noise.
3. **LS-IIR synthesis**: First-order IIR filter (α ≈ 0.75, β ≈ 0.20) for real-time AC-to-BC conversion, validated by LAR distance (0.37→0.18) and listening tests (20/20 correct for male).
4. **SNR quantification**: Systematic measurement showing ~10 dB BC SNR gain across 5 noise types and 8 speakers.
5. **Noise-robustness analysis**: IIR synthesis filter reduces babble/train noise by 70-80%, white noise even more.

## Limitations

- Does not address the inverse problem (BC-to-AC bandwidth extension)
- First-order IIR may not capture all spectral nuances, especially for female speakers
- Coefficient variability across speakers suggests need for speaker-adaptive filters
- No deep learning or neural approaches explored

## Relevance to Smart Hearables

- **Foundation for multimodal sensor fusion**: WACF-CEP demonstrates the power of AC+BC fusion for robust pitch tracking
- **AC-to-BC synthesis as preprocessing**: Enables BC-based processing pipelines using only standard AC microphones
- **Low computational cost**: Both methods are suitable for embedded DSP (no GPU required)

## Related Concepts

- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/signal-processing|Signal Processing]]
- [[concepts/adaptive-filtering|Adaptive Filtering]]

## Related Synthesis

- [[synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]]

## Related Entities

- [[entities/shiming-zhang|Shiming Zhang]]
