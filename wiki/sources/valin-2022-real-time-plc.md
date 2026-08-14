---
type: source
created: 2026-08-14
updated: 2026-08-14
sources:
  - raw/papers/valin-2022-real-time-plc/full-text.md
  - https://arxiv.org/abs/2205.05785
  - zotero://select/items/0_SN5ITVC9
tags:
  - packet-loss-concealment
  - speech-synthesis
  - neural-vocoder
  - lpcnet
  - real-time
  - low-complexity
  - hybrid-dsp-dnn
  - speech-codec
  - opus
  - burg-spectral-estimation
  - perceptual-loss
  - interspeech-2022-plc-challenge
---

# Valin, Mustafa, Montgomery, Terriberry, Klingbeil, Smaragdis & Krishnaswamy 2022: Real-Time Packet Loss Concealment

| Field | Value |
|-------|-------|
| **Authors** | [[entities/jean-marc-valin\|Jean-Marc Valin]], [[entities/ahmed-mustafa\|Ahmed Mustafa]], [[entities/christopher-montgomery\|Christopher Montgomery]], [[entities/timothy-b-terriberry\|Timothy B. Terriberry]], [[entities/michael-klingbeil\|Michael Klingbeil]], [[entities/paris-smaragdis\|Paris Smaragdis]], [[entities/arvindh-krishnaswamy\|Arvindh Krishnaswamy]] |
| **Institution** | Amazon Web Services, Palo Alto, CA, USA (Paris Smaragdis also at University of Illinois at Urbana-Champaign) |
| **Published** | Proc. INTERSPEECH 2022, pp. 570–574 (2nd place, Interspeech 2022 Audio Deep PLC Challenge) |
| **Type** | Conference Paper |
| **arXiv** | [2205.05785](https://arxiv.org/abs/2205.05785) |
| **DOI** | 10.48550/arXiv.2205.05785 |
| **Zotero** | [SN5ITVC9](zotero://select/items/0_SN5ITVC9) |
| **Code** | [github.com/xiph/LPCNet](https://github.com/xiph/LPCNet) (plc_challenge branch); [gitlab.xiph.org/xiph/opus](https://gitlab.xiph.org/xiph/opus) (neural_plc branch) |

## Summary

This paper proposes a hybrid neural **packet loss concealment (PLC)** architecture that combines a generative autoregressive vocoder (LPCNet) with a predictive conditioning model (a GRU-based RNN). The predictive model estimates the acoustic features that LPCNet uses to synthesize the missing speech samples, allowing precise long-term control of the spectral trajectory while still producing natural-sounding speech. The algorithm operates in real time (13–14% of one CPU core in steady state, 2.58 ms worst-case per 10-ms frame on an Intel i7-10810U), supports both causal and non-causal processing, and integrates into the Opus speech codec (replacing the legacy SILK PLC). It ranked **second overall, first in word accuracy** in the Interspeech 2022 Audio Deep Packet Loss Concealment Challenge.

## Problem Formulation

Real-time voice communication over the Internet uses best-effort unreliable transport (RTP/UDP). When voice packets are lost or arrive too late, the receiver must *conceal* the loss to limit quality degradation. Traditional PLC repeats pitch periods (Sanneck et al. 1996), which improves over zero-filling but introduces noticeable artifacts.

**Three core challenges** motivate the work:

1. **Real-time synthesis** — the missing audio must be generated within the playback deadline, on a CPU.
2. **Frequent transitions** between received audio and synthesized concealment require seamless cross-fades and resynchronization, both at the *start* of a loss (transition unknown $U_{0}$) and at the *first received packet after* a loss (transition known $K_{0}$).
3. **Drift / babbling** of purely autoregressive models during long bursts — without conditioning beyond the loss start, autoregressive vocoders drift away from plausible speech.

**Design choice**: Split synthesis into *two time scales* — be "creative" in extending missing segments of a phoneme with plausible-sounding audio, but *never* invent new phonemes or words. This motivates a generative model for short-time samples conditioned on a predictive model for long-time acoustic features.

## Methodology

### Hybrid Generative + Predictive Architecture

A [[concepts/lpcnet|LPCNet]] autoregressive neural vocoder (improved low-complexity variant, $\mathrm{GRU_{A}}$ = 640 units at 15% density) synthesizes the 16 kHz speech samples. LPCNet operates with 20-ms overlapping analysis windows at 10-ms intervals (100 Hz frame rate). Each feature vector contains **18 Bark-frequency cepstral coefficients (BFCCs)**, a pitch period, and a pitch correlation (a [[concepts/bark-scale-spectral-features|Bark-scale]] feature compactly representing the spectral envelope).

A separate **predictive RNN** (1 fully-connected input layer, 2 GRUs of 512 units, 1 fully-connected output layer) predicts the LPCNet feature vectors during loss. Inputs to the prediction network include the known feature vector (or zeros during loss) plus a binary "lost" flag. The prediction conditions the generative model so that the synthesized audio follows a plausible spectral trajectory rather than drifting.

**Causal LPCNet**: The original LPCNet uses two 3×1 convolutions with 2-frame look-ahead (25 ms added latency). For PLC the look-ahead is unavailable during loss, so a strictly causal feature model is used; the 20-ms analysis overlap still imposes 5 ms algorithmic delay.

### Perceptual Loss Functions

Three asymmetric, perceptually-motivated losses replace a single $L_{2}$ term; unpredictable events are treated as label noise (favoring $L_{1}$), and biased terms penalize specific failure modes:

**Spectral / cepstral loss** — overestimating voiced-frame energy hurts more than underestimating it:

$$
\mathcal{L}_{s}=\mathbb{E}\!\left[\sum_{k}\left(\left|\Delta c_{k}\right|+\left|\Delta b_{k}\right|+\alpha\max\!\left(\Delta b_{k},0\right)\right)\right]
$$

where $\Delta c_{k}=\hat{c}_{k}-c_{k}$ is the predicted-minus-true cepstral coefficient, $\Delta b_{k}$ is the corresponding band-energy difference (computed via IDCT of $\Delta c_{k}$), and $\alpha=1$ for voiced frames and $0$ for unvoiced.

**Pitch period loss** — pitch is included in features even for unvoiced frames, so it is noisy; the loss is heavily clamped:

$$
\mathcal{L}_{p}=\mathbb{E}\left[\left|\Delta p\right|+\beta_{1}\min\!\left(\left|\Delta p\right|,50\right)+\beta_{2}\min\!\left(\left|\Delta p\right|,20\right)\right]
$$

with $\beta_{1}=20$ and $\beta_{2}=160$.

**Pitch correlation loss** — overestimating correlation improves pitch stability:

$$
\mathcal{L}_{c}=\mathbb{E}\left[\left|\Delta r\right|+2\max\!\left(-\Delta r,0\right)\right].
$$

### Improved Temporal Resolution via Burg Spectral Features

LPCNet's 20-ms analysis window centered 10 ms before the loss start fails to capture changes immediately preceding a loss. The authors supplement the input with [[concepts/burg-spectral-estimation|Burg maximum-entropy spectral estimates]] computed independently on each 5-ms half-frame, requiring no windowing. The resulting all-pole filters are converted to cepstral coefficients and concatenated to the prediction DNN input. A second benefit: the loss of $k$ frames costs $(k+1)$ LPCNet feature vectors but only $k$ Burg feature vectors.

### Long-Burst Fading

Concealment past ~100 ms is meaningless. Fading too slowly sounds like heavy breathing; too quickly sounds unnatural. The authors linearly decrease the first predicted cepstral coefficient $c_{0}$ after 100 ms to mimic the reverberation decay of a small room with $\mathrm{RT}_{60}=120$ ms. Long losses thus sound like a talker being naturally interrupted.

### Framing, Transitions, and Resynchronization

Four frame types are handled differently: known frames $K$, transition unknown $U_{0}$ at loss start, unknown $U$, transition known $K_{0}$ after loss. Three processing modes are proposed:

- **Causal (no look-ahead)** — uses known samples up to $t$ to update LPCNet state, predicts two feature vectors at loss start (one for $U_{0}$, one for $U$), cross-fades synthesized audio with the first received $K_{0}$ samples to avoid discontinuity.
- **Non-causal (5 ms look-ahead)** — uses 10 ms of speech in the first received packet to extrapolate speech *backwards* by 5 ms, then cross-fades backward and forward extensions. The output is delayed 5 ms so the 5 ms segment is not yet played when resynchronization occurs. All received audio plays unmodified. Total delay = 10 ms frame + 5 ms look-ahead + 2.58 ms worst-case compute = 17.58 ms, within the 20 ms challenge limit.
- **Stateful codec (Opus)** — concealed audio reconstructs the first post-loss packet's decoder state, so non-causal resynchronization is impossible. The codec's inherent linear prediction avoids discontinuity, so the cross-fade step is unnecessary. The proposed PLC **completely replaces the existing SILK PLC** in Opus and its output also seeds the long- and short-term prediction state of the decoder when a new packet arrives.

## Experimental Setup

| Aspect | Configuration |
|--------|---------------|
| **LPCNet training data** | 205 hours of 16 kHz speech from 9 TTS corpora, 900+ speakers, 34 languages/dialects |
| **Prediction DNN training data** | Same 205 hours + 64 hours of PLC-challenge-organizer-provided training speech |
| **Architecture** | LPCNet $\mathrm{GRU_{A}}$ = 640 units at 15% density (improved efficiency variant [16]); prediction RNN = 2 × 512-unit GRUs, 256-unit input FC, FC output |
| **Sign randomization** | Training explicitly randomizes the sign of each sequence so polarity is invariant |
| **Evaluation set** | 966 test utterances, 5 listeners per utterance (CMOS), 15 listeners per utterance (MOS ACR, dev set) |
| **Opus eval configuration** | 24 kb/s speech mode, 20-ms frames, encoder robustness tuned for 20% loss |
| **Baselines** | Zero-fill, PLCMOS-baseline, feature repetition, NetEQ (classical PCM PLC), Opus default SILK PLC |
| **Hardware** | Intel i7-10810U laptop CPU |
| **Objective metrics** | PESQ-WB (P.862.2 wideband extension), PLCMOS, DNSMOS |
| **Subjective metrics** | CCR / CMOS (P.808 crowdsourcing); MOS ACR on dev set |
| **ASR metric** | Word accuracy (WAcc) |

## Results

### Complexity (Table 1)

Processing time per 10-ms frame, by frame type (Intel i7-10810U):

| Algorithm | $K$ | $U_{0}$ | $U$ | $K_{0}$ |
| --- | --- | --- | --- | --- |
| Causal | 1.35 ms | 2.12 ms | 1.34 ms | 1.53 ms |
| Non-Causal | 1.38 ms\* | 1.33 ms | 1.34 ms | 2.58 ms |
| Codec | 1.38 ms | 2.18 ms | 1.37 ms | 0.84 ms |

\*2.54 ms for the first frame following a $K_{0}$ frame.

Steady-state cost is 13–14% of one CPU core; worst case is 2.58 ms. The prediction DNN contributes < 20% of total complexity.

### Interspeech 2022 PLC Challenge (Table 2)

| Algorithm | PLCMOS | DNSMOS | CMOS | WAcc | Overall Score |
| --- | --- | --- | --- | --- | --- |
| 1st place | 4.282 | 3.797 | -0.552 | 0.875 | 0.845 |
| **proposed** | 3.744 | 3.788 | **-0.638** | **0.882** | 0.835 |
| 3rd-place avg. | 3.903 | 3.686 | -0.825 | 0.864 | 0.794 |
| Zero-fill | 2.904 | 3.444 | -1.231 | 0.861 | 0.725 |

The proposed algorithm ranked **2nd overall, 1st in word accuracy**, and 2nd in CMOS. The 95% CI on CMOS values is ~0.035.

### Ablation Study (Table 3)

PESQ-WB / PLCMOS, added incrementally over feature repetition:

| Configuration | PESQ-WB | PLCMOS |
| --- | --- | --- |
| Zero-fill | 2.185 | 2.874 |
| Baseline | 2.059 | 2.786 |
| Repetition | 2.517 | 3.642 |
| +DNN (causal) | 2.647 | 3.688 |
| +perceptual losses (1)–(3) | 2.652 | 3.660 |
| +Burg features | 2.705 | 3.739 |
| +non-causal | 2.766 | 3.790 |

Both metrics agree on all improvements except the perceptual losses, where informal listening confirmed a quality improvement not captured by objective metrics.

### Opus Codec Integration (Fig. 2)

On the dev set (15 listeners × 966 utterances, ACR MOS), the causal and non-causal PCM variants both significantly outperform the popular NetEQ classical PLC and the challenge baseline. The difference between non-causal and causal variants is not statistically significant. Inside Opus-coded speech (24 kb/s, speech mode), the proposed neural PLC significantly outperforms the existing Opus (SILK) PLC.

## Key Contributions

1. **Hybrid generative + predictive PLC architecture** — a generative autoregressive vocoder (LPCNet) conditioned by a predictive RNN feature model, decoupling short-time sample synthesis from long-time spectral-trajectory control. Avoids both the drift of purely autoregressive PLC and the artifacts of feature repetition.
2. **Three perceptually-motivated asymmetric loss functions** — $L_{s}$ for cepstral/band energy with voiced-frame bias, $L_{p}$ for pitch period with heavy clamping, $L_{c}$ for pitch correlation with stability-favoring bias. Together they treat unpredictable PLC events as label noise and bias prediction toward perceptually safer directions.
3. **Burg spectral features at 5 ms half-frame resolution** — overcomes the 20-ms LPCNet window centering limitation without adding latency; one fewer Burg feature vector is lost per packet loss burst.
4. **Long-burst fading via $c_{0}$ decay** — emulates small-room reverberation ($\mathrm{RT}_{60}=120$ ms) by linearly decreasing the predicted $c_{0}$ after 100 ms, avoiding both "heavy breathing" artifacts and abrupt cut-offs.
5. **Causal, non-causal (5 ms look-ahead), and stateful-codec processing modes** with frame-type-specific handling for the four transition classes ($K, U_{0}, U, K_{0}$). Non-causal uses backward extrapolation from the first received packet to cross-fade with forward synthesis, keeping total delay ≤ 17.58 ms.
6. **First neural PLC operating inside the Opus speech codec** — replaces the legacy SILK PLC and seeds the decoder's long-/short-term prediction state on packet arrival.
7. **2nd place overall (1st in WAcc)** in the Interspeech 2022 Audio Deep PLC Challenge, with 13–14% CPU usage in steady state on a laptop CPU.

## Related Concepts

- [[concepts/packet-loss-concealment|Packet Loss Concealment]] — the paper's central problem
- [[concepts/lpcnet|LPCNet]] — the generative vocoder used for sample synthesis
- [[concepts/burg-spectral-estimation|Burg Spectral Estimation]] — half-frame spectral features that overcome LPCNet's window centering limitation
- [[concepts/opus-codec|Opus Audio Codec]] — the stateful codec integration target (replacing SILK PLC)
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — LPCNet uses 18 BFCCs, a Bark-scale cepstral representation
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]] — backbone of both the prediction RNN and LPCNet's $\mathrm{GRU_{A}}$
- [[concepts/percepnet|PercepNet]] — sibling Valin-lab hybrid DSP/DNN real-time system for speech enhancement / AEC (shares the low-complexity, perceptually-motivated design philosophy)
- [[concepts/recurrent-neural-network|Recurrent Neural Network]] — predictive model backbone

## Related Synthesis

(No synthesis pages updated — triage in Step 9 found no existing synthesis page on packet loss concealment or neural PLC. This is the first PLC paper in the wiki.)
