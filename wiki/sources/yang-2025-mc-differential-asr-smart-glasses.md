---
type: source
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/yang-2025-mc-differential-asr-smart-glasses/full-text.md
  - https://arxiv.org/abs/2509.14430
  - zotero://select/items/0_UVUJA5LX
tags:
  - speech-recognition
  - beamforming
  - smart-glasses
  - wearer-speech-recognition
  - side-talk
  - multi-channel
  - mvdr
---

# Yang, Huang, Xu, Wan, Shon, Liu, Fan, Yang, Siohan, Liu, Sun & Metze 2025: Multi-Channel Differential ASR for Robust Wearer Speech Recognition on Smart Glasses

**Authors**: [[entities/yufeng-yang|Yufeng Yang]], [[entities/yiteng-huang|Yiteng Huang]], [[entities/yong-xu|Yong Xu]], [[entities/li-wan|Li Wan]], [[entities/suwon-shon|Suwon Shon]], [[entities/yang-liu|Yang Liu]], [[entities/yifeng-fan|Yifeng Fan]], [[entities/zhaojun-yang|Zhaojun Yang]], [[entities/olivier-siohan|Olivier Siohan]], [[entities/yue-liu|Yue Liu]], [[entities/ming-sun|Ming Sun]], [[entities/florian-metze|Florian Metze]]
**Affiliation**: Meta (Reality Labs); Yufeng Yang intern at Meta
**Venue**: arXiv:2509.14430 (2025)
**Type**: Preprint
**DOI**: arXiv:2509.14430
**Zotero**: [UVUJA5LX](zotero://select/items/0_UVUJA5LX)

---

## Summary

This paper introduces **multi-channel differential ASR**, a system that combines complementary frontends — an internal adjusted [[concepts/mvdr-beamformer|MVDR]] beamformer steered to the wearer's mouth, fixed microphone selection (the closest nose mic), and a lightweight streaming [[concepts/side-talk-detection|side-talk detection (STD)]] model — as additional input channels to a streaming RNN-T ASR backbone. Unlike the traditional approach that uses a single beamformer as frontend, differential ASR feeds the ASR model with multiple complementary/contrastive representations, yielding up to an 18.0% relative WER reduction for [[concepts/wearer-speech-recognition|wearer speech recognition (WSR)]] on Ray-Ban Meta smart glasses in side-talk conditions.

## Problem Formulation

[[concepts/wearer-speech-recognition|Wearer speech recognition (WSR)]] on smart glasses is vulnerable to side-talk from bystanders, because the microphones operate in open-field conditions rather than close-talk. Prior work ([[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition|Lin et al. 2024 — AGADIR]], [[sources/feng-2025-directional-source-separation-smart-glasses|Feng et al. 2025]]) used a beamformer as the sole frontend to the ASR model. However, when only the wearer is being transcribed in the presence of side-talk, the beamformer alone cannot fully suppress the WSR degradation. Traditional alternatives — speech enhancement, speaker diarization, [[concepts/target-speaker-extraction|target speaker extraction]] — add latency and may require modeling speaker identity, raising privacy concerns for an always-on wearable.

The design goal: improve WSR robustness to side-talk with (i) no additional latency, (ii) no speaker-identity modeling, and (iii) minimal additional trainable parameters (<1M).

## Methodology

![[raw/papers/yang-2025-mc-differential-asr-smart-glasses/figures/fig1.png|AGADIR differential ASR architecture]]

*Figure 1: Diagram of the proposed multi-channel differential ASR system for robust WSR on smart glasses.*

### Differential ASR Principle

The differential ASR framework uses several frontends whose outputs **complement or contrast** each other. Rather than running a single beamformer and feeding only its output to the ASR model, the framework feeds the ASR backbone with multiple parallel representations (beamformed audio, raw close-mic audio, and a stream of side-talk logits/embeddings). All frontends are frozen — only the ASR model and small feature-extraction layers are trained, keeping additional trainable parameters under 1M.

### Frontend Modules

1. **Beamformer (ch-x)** — internal adjusted [[concepts/mvdr-beamformer|MVDR]] that steers the 5-mic array towards the wearer's mouth. Unlike the [[concepts/nlcmv-beamforming|NLCMV]] beamformer of AGADIR (which steers multiple directions for conversational ASR), this MVDR focuses solely on the wearer and is therefore more suitable for WSR.
2. **Microphone selection (ch-0)** — fixed selection of the nose microphone as the closest mic to the wearer's mouth (highest SNR), no latency, no learned parameters.
3. **Side-talk detection (STD) model** — lightweight (~2M parameter) streaming [[concepts/side-talk-detection|TCN-based]] classifier producing sample-level logits over {wearer, bystander, non-speech}. The STD model is trained on real non-user data; it does not model speaker identity, protecting privacy. STD logits are converted to an `embed` of dimension 5 via two Conv2D layers (kernel [20,1], strides [10,1] and [16,1]) that downsample to match the ASR feature frame rate.

### Feature Extraction & ASR Backbone

- **Log-Mel features**: 80-dimensional per channel
- **Feature extraction (ch-x only)**: 80-dim log-Mel
- **Feature extraction (ch-x + ch-0)**: concatenate 80-dim log-Mel of each, halve each to 40-dim via two streaming Conv2D layers (kernel [2,5], stride [1,2], GLU activation), then concatenate
- **Embedding**: STD logits → 2× Conv2D → 5-dim embedding (frame-rate matched to features)
- **Concatenated input** → RNN-T (Emformer, 20 layers, input dim 320, 4 attention heads, FF dim 2048, context 10 past frames, segment size 2, GELU activation, conv kernel [7,0] with Swish; encoder output 768-dim; predictor: 256-dim embeddings + 2-layer 256-hidden LSTM → 768-dim projection; joint network → 4096 SentencePiece BPE units)
- **Total trainable parameters**: ~70M; **ASR latency**: 120 ms
- **Training loss**: RNN-T loss; tri-stage LR schedule (peak 5e-4, 20k warmup); Adam (betas 0.9/0.98, weight decay 1e-6); 32× NVIDIA H100 GPUs, batch size 3600

### Multi-Channel Differential Combination

Three frontend combinations are explored:
- `ch-x + embed` — beamformer + STD
- `ch-x + ch-0` — beamformer + microphone selection
- `ch-x + ch-0 + embed` — all three frontends (best configuration)

## Experimental Setup

### Datasets

![[raw/papers/yang-2025-mc-differential-asr-smart-glasses/figures/fig2.png|Smart-glasses microphone layout]]

*Figure 2: Microphone location on a pair of smart glasses (5 mics: 1 nose + 2×2 temple pairs).*

| Dataset | Size | Details |
|---------|------|---------|
| Train (clean) | 500,554 utts | LibriSpeech multi-channel, simulated via measured RIRs on Ray-Ban Meta smart glasses |
| Train (noisy) | 500,554 utts | Same + side-talk from LibriSpeech bystander, SNR 10–25 dB, overlap 0–100% |
| Validation | 6,747 utts | LibriSpeech dev, clean only |
| Sim test | 3,558 + 3,502 utts | test-clean & test-other, clean + noisy (overlap 0% & 50%) |
| Real test | 188,640 utts | HATS-mounted Ray-Ban Meta, 72 bystander locations: 8 angles × 3 heights × 3 distances; speaker order: wearer-first or bystander-first |

![[raw/papers/yang-2025-mc-differential-asr-smart-glasses/figures/fig3.png|HATS recording setup]]

*Figure 3: Recording setup for real data collection with HATS (head and torso simulator) and loudspeakers at 72 bystander locations (8 angles × 3 heights × 3 distances).*

### Systems Compared

Five systems: two baselines (clean-trained ch-x, noisy-trained ch-x) and three differential variants (all noisy-trained).

## Results

### Simulated Data (Table 1)

| System | test-clean (clean) | test-other (clean) | Avg clean | test-clean (0%) | test-clean (50%) | test-other (0%) | test-other (50%) | Avg noisy |
|--------|---|---|---|---|---|---|---|---|
| Clean-trained ch-x | 5.70 | 14.75 | 10.23 | 88.62 | 46.07 | 89.75 | 51.23 | 68.92 |
| Noisy-trained ch-x | 6.46 | 16.48 | 11.68 | 6.37 | 6.63 | 16.72 | 17.42 | 11.79 |
| Noisy-trained ch-x + embed | 6.06 | 15.99 | 11.14 | 5.98 | 6.20 | 16.01 | 16.57 | 11.19 |
| Noisy-trained ch-x + ch-0 | 6.21 | 16.30 | 11.39 | 6.07 | 6.46 | 16.34 | 16.96 | 11.46 |
| Noisy-trained ch-x + ch-0 + embed | 6.07 | 16.08 | 11.21 | 6.03 | 6.21 | 16.11 | 16.78 | 11.28 |

- Noisy training alone gives 82.8% relative WER reduction (WERR) vs clean-trained on side-talk data — data augmentation is essential.
- Best differential system (`ch-x + embed`) on noisy data: **5.1% relative WERR** over noisy-trained ch-x baseline.

### Real Recorded Data (Table 2)

| System | Wearer-only | wearer-bystander 0% | wearer-bystander 50% | bystander-wearer 0% | bystander-wearer 50% | Avg noisy |
|--------|---|---|---|---|---|---|
| Clean-trained ch-x | 6.30 | 29.20 | 15.28 | 40.96 | 23.81 | 27.31 |
| Noisy-trained ch-x | 7.20 | 7.19 | 7.41 | 7.22 | 7.63 | 7.36 |
| Noisy-trained ch-x + embed | 6.82 | 6.79 | 7.02 | 6.85 | 7.06 | 6.93 |
| Noisy-trained ch-x + ch-0 | 6.51 | 6.50 | 6.57 | 6.38 | 6.50 | 6.49 |
| Noisy-trained ch-x + ch-0 + embed | **6.29** | **6.28** | **6.37** | **6.30** | **6.26** | **6.30** |

- Best full system `ch-x + ch-0 + embed`: **18.0% relative WERR** vs noisy-trained ch-x baseline (7.36 → 6.30), and 76.9% relative WERR vs clean-trained (27.31 → 6.30).
- Real data shows the full three-frontend combination wins; on simulated data the STD-only variant was best. Real conditions likely benefit more from the close-mic robustness.

### Angle Analysis

![[raw/papers/yang-2025-mc-differential-asr-smart-glasses/figures/fig4.png|WER by bystander angle]]

*Figure 4: WER comparison on real data for different bystander angles: (A) wearer-bystander 0% overlap; (B) wearer-bystander 50% overlap; (C) bystander-wearer 0% overlap; (D) bystander-wearer 50% overlap. All systems trained on noisy data. WER range [6.0%, 8.0%] shown by color.*

At 0% overlap, WERs are stable across angles. At 50% overlap, angles 270°, 315°, and 0° (wearer-bystander) and 225° (bystander-wearer) are harder — suggesting future beamformer design should reduce the angle gap.

## Key Contributions

1. **Differential ASR framework**: a novel design pattern that feeds an ASR backbone with multiple complementary/contrastive frontend outputs (beamformer, microphone selection, STD embedding) rather than a single beamformer output, achieving up to 18.0% relative WERR on real side-talk data.
2. **Streaming side-talk detection (STD)**: a lightweight (~2M parameter) TCN-based streaming classifier producing sample-level logits over {wearer, bystander, non-speech} that, unlike speaker diarization, does not model speaker identity — preserving privacy for always-on wearables.
3. **HATS real-recorded evaluation dataset**: 188,640 utterances over 72 bystander locations (8 angles × 3 heights × 3 distances) with both speaker-order conditions, enabling fine-grained angle/distance/height analysis.
4. **Angle-resolved failure analysis**: identifies specific hard angles (270°/315°/0° wearer-bystander, 225° bystander-wearer at 50% overlap), motivating beamformer design that reduces the angle gap rather than the average WER.

## Related Concepts

- [[concepts/differential-asr|Differential ASR]]
- [[concepts/wearer-speech-recognition|Wearer Speech Recognition (WSR)]]
- [[concepts/side-talk-detection|Side-Talk Detection (STD)]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/nlcmv-beamforming|NLCMV Beamforming]]
- [[concepts/voice-activity-detection|Voice Activity Detection (VAD)]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/target-speaker-asr|Target Speaker ASR]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]

## Related Sources

- [[sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition|Lin et al. 2024: AGADIR — Array-Geometry Agnostic Directional Speech Recognition]] — predecessor directional ASR system; this paper replaces NLCMV multi-direction beamforming with a single-direction wearer-focused MVDR + differential frontends.
- [[sources/feng-2025-directional-source-separation-smart-glasses|Feng et al. 2025: Directional Source Separation for Smart Glasses]] — same smart-glasses ASR context, complementary approach via source separation.

## Related Synthesis

(none yet — Step 9 triage found no synthesis page covering directional ASR / smart-glasses WSR)
