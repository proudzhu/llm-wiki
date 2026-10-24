---
type: concept
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/nguyen-2023-predictive-plc/full-text.md
  - raw/papers/westhausen-2022-tplcnet/full-text.md
tags:
  - packet-loss-concealment
  - blind-plc
  - full-band
  - real-time
  - recurrent-neural-network
  - speech-enhancement
  - neural-network
---

# Full-Band Recurrent Network (FRN)

**Full-band recurrent network (FRN)** is a recurrent time-frequency architecture for **blind** packet loss concealment (PLC) of 48 kHz speech, introduced by [[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023]]. It processes complex STFT frames sequentially and combines two branches — an **encoder** that reconstructs the current input frame and a **predictor** that infers the current frame's magnitude from the previous *enhanced output* — fused by a CNN joiner, in a design inspired by the RNN-transducer (encoder + prediction network + joiner).

## Key Formulations

At time step $i$, the encoder maps the lossy input frame $\langle \Re_i^F, \Im_i^F \rangle$ to an enhanced complex frame, while the predictor leverages the previous output $\langle \hat{\Re}_{i-1}^F, \hat{\Im}_{i-1}^F \rangle$:

$$
A_{i-1}^{F} = \sqrt{(\Re_{i-1}^{F})^{2} + (\Im_{i-1}^{F})^{2}}, \qquad
\hat{A}_{i}^{F} = \mathrm{Pred}(A_{i-1}^{F})
$$

The joiner stacks the encoder's real/imaginary parts and the predictor's magnitude into a 3-channel input and applies two causal grouped convolution layers:

$$
\langle \hat{\Re}_{i}^{F}, \hat{\Im}_{i}^{F} \rangle = \mathrm{Joiner}\left(\langle \tilde{\Re}_{i}^{F}, \tilde{\Im}_{i}^{F}, \hat{A}_{i}^{F} \rangle\right), \qquad
\hat{y} = \mathrm{iSTFT}\left(\langle \hat{\Re}_{i}^{F}, \hat{\Im}_{i}^{F} \rangle\right).
$$

Training uses the **multi-resolution STFT loss** on compressed magnitudes $|\mathrm{STFT}(s)|^{\alpha}$ with $\alpha = 0.3$ (a [[concepts/frequency-domain-loss|frequency-domain loss]]), summing spectral convergence (Frobenius norm) and spectral magnitude (L1) terms over $M$ resolutions (auraloss defaults).

## Architecture

- **Encoder** — flattens the complex STFT frame ($2F = 960$ values, $F = 480$) and projects it to dimension 384 via a linear layer + GELU; a residual module of 4 blocks models inter-frame correlation with an RNN (state 384) and intra-frame structure with linear layers (hidden 768); a final linear layer projects back to $2F$. The arrangement is a hybrid of ResMLP and [[concepts/dprnn|dual-path RNN]] ideas.
- **Predictor** — operates on the **log-Mel magnitude** (64 bins) of the previous output: a single-layer [[concepts/long-short-term-memory|LSTM]] (hidden 512) models temporal dynamics, a linear layer projects back to the Mel dimension, and a learnable **inverse-Mel layer** (exponential, linear, absolute activation) maps to the $F$-bin STFT magnitude.
- **Joiner** — two causal grouped convolution layers fuse the 3-channel stack into the final real/imaginary frame.

## Design Rationale

- **Reuse of previous output** — the predictor consumes the model's *own previous enhanced output*, which is essential when several consecutive packets are lost and the raw input is uninformative. The paper cites the decision-directed SNR estimator ([[concepts/decision-directed-a-priori-snr|Ephraim & Malah 1984]]) as the classical precedent for reusing one's previous estimate, and the RNN-transducer (Graves 2012) as the architectural inspiration.
- **Mel-domain bottleneck** — most speech energy concentrates in low frequency bins, so compressing the magnitude to 64 Mel bins makes the predictor efficient; the learnable inverse-Mel layer maps back to linear frequency.
- **Predictor pre-training** — the predictor is first trained on the *target* (clean) audio of the PLC dataset (ensuring it genuinely predicts from the previous frame and stabilizing training), then jointly trained with the encoder; pre-training yields a modest performance improvement.
- **Blindness** — no loss mask, no packet-size metadata, and frame-causal STFT processing (no look-ahead): the model is suitable for real-time full-band (48 kHz) telecommunication where packet metadata may be unavailable.

## Results

On the VCTK test set with simulated losses (10/20/40%) and real loss traces from the Interspeech 2022 PLC Challenge, FRN (9.1M parameters, 4.1 ms per 10-ms frame on one CPU thread, real-time factor 0.41) outperforms the **informed** [[concepts/tplcnet|tPLCnet]] ([[sources/westhausen-2022-tplcnet|Westhausen & Meyer 2022]], 3rd place, Interspeech 2022 PLC Challenge) on PLCMOS, LSD, STOI, and PESQ at all loss rates, and beats the offline blind TFGAN on LSD/STOI/PESQ by ~250%/12%/30%. Ablation on the real-trace set shows the predictor branch's contribution: encoder-only LSD 1.081 → 0.946, STOI 0.862 → 0.889.

## Position in PLC Evolution

FRN is the **blind, full-band** entry in the neural PLC lineage: it extends the recursive re-feeding idea of [[concepts/dnn-regression-plc|DNN regression PLC]] (Lee & Chang 2016 re-fed estimated features during burst losses) into a dedicated network branch with end-to-end training, and it contrasts with the [[concepts/lpcnet|LPCNet]]-based hybrid of [[sources/valin-2022-real-time-plc|Valin et al. 2022]] — where a predictive RNN conditions a *generative* vocoder — by fusing prediction with reconstruction entirely in the complex-STFT domain, without a vocoder stage.

## Related Concepts

- [[concepts/packet-loss-concealment|Packet Loss Concealment]] — the umbrella task; FRN is a blind, real-time, full-band method
- [[concepts/dnn-regression-plc|DNN Regression PLC]] — the earlier frame-regression paradigm whose burst-loss re-feeding anticipates the predictor branch
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]] — architectural inspiration for the encoder's inter-/intra-frame hybrid
- [[concepts/long-short-term-memory|Long Short-Term Memory]] — the predictor's backbone
- [[concepts/frequency-domain-loss|Frequency Domain Loss]] — the multi-resolution STFT training objective
- [[concepts/decision-directed-a-priori-snr|Decision-Directed A Priori SNR Estimation]] — the classical precedent for reusing the previous estimate

## Related Sources

- [[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023: Full-Band Blind Packet-Loss Concealment With Predictive Network]] — introduces the architecture
- [[sources/lee-2016-dnn-plc|Lee & Chang 2016: DNN-Based Packet Loss Concealment]] — earlier regression PLC with recursive burst-loss re-feeding
- [[sources/valin-2022-real-time-plc|Valin et al. 2022: Real-Time Packet Loss Concealment]] — contemporary hybrid generative + predictive PLC (informed, 16 kHz, vocoder-based)
- [[sources/westhausen-2022-tplcnet|Westhausen & Meyer 2022: tPLCnet — Real-Time Deep Packet Loss Concealment in the Time Domain]] — the informed challenge baseline FRN benchmarks against
