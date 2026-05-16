---
type: concept
created: 2026-05-16
updated: 2026-05-16
sources:
  - wiki/sources/liu-2025-robust-fusion-bc-ac-attention.md
tags:
  - multi-modal-fusion
  - robustness
  - speech-enhancement
  - bone-conduction
  - training-strategy
---

# Sensor-Failure Robust Multi-Modal Fusion

**Sensor-failure robust multi-modal fusion** refers to architectural and training choices that allow a multi-modal model to **gracefully degrade** when one or more input modalities become invalid (disconnected, occluded, or producing low-SNR garbage). For wearable bone-conducted (BC) and air-conducted (AC) sensor fusion this is a critical practical issue: the BC sensor can lose contact with the skin during head/jaw movement, and the external AC microphone can be obscured by clothing or wind.

## The Failure Mode

Most learning-based BC/AC fusion methods are trained assuming **both channels are always valid**. When one channel becomes invalid at inference time:

| Method | Output PESQ when AC fails (vs. noisy BC = 1.24) | Output PESQ when BC fails (vs. noisy AC = 2.16) |
|---|---:|---:|
| FCN Fusion | 1.45 | 2.13 |
| MMINet | 1.18 (worse than input) | 1.88 (worse than input) |
| Aff Fusion | 1.22 (worse than input) | 1.98 (worse than input) |

These methods *amplify* the dead channel's noise into the output instead of falling back to the surviving channel.

## Mitigation Strategies

### 1. Special Training (ST) — Random Channel Dropout (Liu 2025)

Liu, Chen & Yin propose to **randomly replace one input channel with low-amplitude white noise** during training:

- Probability of failure: $p_{AC} = p_{BC} = 0.2$ each (independent).
- White noise (low amplitude) simulates a disconnected sensor delivering only thermal noise.

This is a multi-modal analogue of dropout applied at the modality level. The model learns three regimes simultaneously: both-valid, AC-only, BC-only — without needing separate sub-networks.

**Effect on Liu 2025**:

| Failure case | Without ST | With ST |
|---|---:|---:|
| AC fails (BC = 1.24) | 1.53 PESQ | **2.54 PESQ** |
| BC fails (AC = 2.16) | 2.62 PESQ | **3.39 PESQ** |

ST training transforms a 0.31 PESQ degradation (under AC failure) into a +1.30 PESQ improvement.

### 2. Architectural Robustness — Dual-Path Mask + Multi-Axis Attention

Surprisingly, the Liu 2025 model — even *without* ST training — already outperforms baselines under sensor failure (PESQ 2.62 vs. 1.98 best baseline when BC fails; 1.53 vs. 1.45 best baseline when AC fails). The authors attribute this to:

- **Dual-channel mask architecture**: Each surviving channel has its own learnable mask, so the model can attenuate the dead channel's mask toward zero rather than blindly summing both.
- **[[concepts/adaptive-time-frequency-attention|ATFA]]**: Self-attention along time and frequency axes provides global context that can detect that one channel is uninformative.

### 3. Voice Activity Gating

Where applicable (e.g., [[concepts/bcs-guided-speech-enhancement|BCS-guided SE]] in Heitkaemper 2026), a [[concepts/voice-activity-detection|VAD]] derived from BC can gate the enhancement pathway, falling back to raw AC when no BC speech is detected.

## Comparison with Conventional Robustness

This problem is distinct from standard noise robustness:

| Property | Standard noise robustness | Sensor-failure robustness |
|---|---|---|
| What changes | SNR within a modality | Entire modality goes dead |
| Failure rate | Continuous | Discrete on/off |
| Training data | SNR sweep with valid signals | Random modality dropout |
| Model assumption | Both modalities informative | Either subset can be informative |

## Design Principles

1. **Train for the failure cases you expect** — random modality dropout is cheap and effective.
2. **Prefer per-modality output heads** (dual-mask) over single shared heads — gives the network a knob to "turn off" a dead channel.
3. **Multi-axis attention** provides architectural priors that help even without ST training.
4. **Validate at inference** — measure not only average performance but worst-case channel-failure performance.

## Related Concepts

- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/adaptive-time-frequency-attention|Adaptive Temporal-Frequency Attention (ATFA)]]
- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/robust-adaptive-filtering|Robust Adaptive Filtering]]

## Related Sources

- [[sources/liu-2025-robust-fusion-bc-ac-attention|Liu, Chen & Yin 2025: Robust BC/AC Fusion with ATFA]]
- [[sources/kuang-2024-lightweight-speech-enhancement-bone-air|Kuang, Yang & Yang 2024: Lightweight BC/AC Speech Enhancement]]
- [[sources/he-2025-vibomni|He et al. 2025: VibOmni]]
