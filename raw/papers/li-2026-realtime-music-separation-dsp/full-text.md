Jianan Li    Li Liu    Ken Malsky    Gabby Yi

###### Abstract

Real-time music source separation is validated on desktop CPUs and GPUs. Does any published system fit the embedded audio hardware it targets? On a commercial audio DSP ($2$  MB SRAM, $2.07$   $\mathrm{GMAC\,s^{-1}}$ measured), none does, and the constraints eliminate different models: memory rules out the $16$ – $51$  M parameter TasNet/X-UMX family, per-frame compute rules out RT-STT, needing $5.5\times$ the available MAC rate. Parameter count predicts neither: weight reuse spans $1\times$ to $345\times$. We then build one that fits. Training on *continuous* rather than block-padded convolution context proves essential: a model scoring $3.93$  dB block-wise otherwise collapses to silence within $2$  s frame-by-frame. A gated complex FIR *deep filter* adds a latency knob, gaining $0.38$  dB even when strictly causal. It reaches $4.70$  dB cSDR on MUSDB18-HQ and runs in $10.43$  ms of an $11.6$  ms hop, $0.5$ – $0.7$  dB behind systems that do not fit.

<sup>†</sup>

## 1 Introduction

Deep learning has transformed music source separation (MSS) [^1] [^2], but the strongest systems are large and offline, consuming a whole track at once [^3] [^4] [^5]. A smaller literature targets the *real-time* regime: HS-TasNet [^6] demixes at $23$  ms latency and RT-STT [^7] matches that latency with ${\sim}0.4$  M parameters, alongside work on accompaniment separation [^8] and singing-voice cancellation [^9]. Both leading systems are explicit that latency is not the only constraint: each separates *algorithmic latency* from *computational efficiency* and reports per-frame processing time, and HS-TasNet notes that Conv-TasNet [^10] is slow in practice despite having “only 9 M parameters”.

Those times are measured on an i7-class CPU and an RTX-class GPU [^6] [^7]. A separator built for hearing aids, in-ear monitors or a live-sound processor runs instead on a low-power audio DSP: a fixed multiply–accumulate (MAC) rate, a hard per-frame deadline, and a few megabytes of on-chip SRAM. “ $3.9$  ms on an RTX 3080Ti” does not transfer. Efficiency-oriented separation has reached mobile GPUs [^11] and speech enhancement runs routinely on embedded parts [^12], but MSS is harder at the same budget (four correlated outputs, and a decoder that reconstructs every stem), and we know of no MSS system evaluated against, or demonstrated on, such a device.

We close that gap. Section 2 states deployability as two hardware-independent constraints, weight memory and MAC per frame, and evaluates the published systems against a commercial budget; Sections 3–5 design, train and deploy a separator that fits. Along the way we report a streaming failure of independent interest: block-padded convolution training makes continuous inference out-of-distribution, and a model scoring $3.93$  dB block-wise collapses to silence within ${\sim}2$  s frame-by-frame.

The backbone follows the TFC-TDF U-Net lineage [^13] [^14] as specialised for real time by RT-STT [^7], itself derived from DTTNet [^15]; band-split models [^4] [^5] [^16] and low-latency speech separation [^17] are the other relevant strands, and efficiency-driven designs such as SCNet [^18] reduce cost at desktop scale rather than to an embedded budget. On top we add *deep filtering* [^19] [^12], which replaces the point-wise complex mask with a short complex FIR filter per time–frequency bin convolved along time; used offline as a post-filter on Hybrid Demucs [^20] and for impulsive/stationary separation [^21], we use it causally, gate it per source so the network can decline it, and treat its past/future tap split as an explicit latency control.

## 2 The Embedded Budget

Target. We use the Analog Devices SHARC-FX (ADSP-21835) as a representative low-power audio DSP: $1$  GHz, $512$  kB L1, $2$  MB on-chip L2. Its published peak is $24$  GFLOPS, or $8$   $\mathrm{GMAC\,s^{-1}}$ in $32$ -bit float and $16$   $\mathrm{GMAC\,s^{-1}}$ in $16$ -bit fixed point. Our hand-scheduled floating-point runtime sustains $2.07$   $\mathrm{GMAC\,s^{-1}}$ on this part (measured, §5.4). At $44.1$  kHz with a $512$ -sample hop, the $23$  ms operating point of both baselines, this gives $86.1$ frames s <sup>-1</sup> and an $11.6$  ms per-frame deadline. The part has a DDR interface, so weights could live off-chip; we exclude that deliberately, because they are re-read every frame, so streaming them puts a recurring transfer on the critical path of that deadline: our $501$  kB of weights at $86.1$ frames s <sup>-1</sup> is ${\sim}44$  MB s <sup>-1</sup> sustained for as long as the device runs. Double-buffered DMA hides the latency but not the bandwidth, and external memory adds board cost and power to a product that chose this class of part to avoid both. $M_{\mathrm{L2}}$ is thus a design constraint, not a hardware limit, and the analysis is parameterised by $(M_{\mathrm{L2}},R)$ so it can be re-run for any target.

Peak rate is not deployable rate. A datasheet peak assumes every issue slot retires a useful MAC: no cache miss, no carried state, no serialisation. Budgeting against it would be a category error. Our $2.07$   $\mathrm{GMAC\,s^{-1}}$ is $26\%$ of the float peak and is hand-scheduled; a TFLite-Micro port on the same part spent ${\sim}90\%$ of its time moving data. We therefore compare *required* against *measured achievable* rate. Granting a baseline $16$ -bit fixed point at our efficiency gives it $4.2$   $\mathrm{GMAC\,s^{-1}}$; RT-STT still needs $2.7\times$ that, so the verdict does not rest on denying baselines fixed-point arithmetic.

Two constraints. A model is deployable only if it satisfies both:

$$
\displaystyle W\cdot b\;\leq\;M_{\mathrm{L2}},
$$
$$
\displaystyle C_{\mathrm{frame}}\cdot f_{\mathrm{s}}/H\;\leq\;R,
$$

where $W$ is the parameter count, $b$ bytes per weight, $C_{\mathrm{frame}}$ the MAC per frame, $H$ the hop and $R$ the sustained MAC rate. We evaluate the memory constraint from published parameter counts under the *most generous* assumption available to those systems, $b=1$ (int8), which none of them claims; activations and streaming state are excluded, so the true gap is larger.

Weight reuse, and why $W$ does not predict $C_{\mathrm{frame}}$. For a fully-connected or recurrent layer evaluated once per frame, each weight takes part in exactly one multiply–accumulate, so $C_{\mathrm{frame}}\!=\!W$ identically. Convolution over frequency breaks this: a kernel is reused at every bin. Define the reuse factor $\rho=C_{\mathrm{frame}}/W$. It is $\rho\!\approx\!1$ for the TasNet/X-UMX family, which is dominated by frame-rate LSTMs and dense layers, and $\rho\!=\!345$ for RT-STT, whose $383$  k weights are evaluated across $384$ frequency bins every frame. Because $\rho$ spans two and a half orders of magnitude across Table 1, no ordering by parameter count can predict per-frame cost. This also gives the baselines’ compute for free: at $\rho\!\approx\!1$ the published $W$ *is* a per-frame MAC estimate, and a lower bound once their convolutional front ends are added. We validate the identity on X-UMX, whose architecture is fully specified [^6]: summing its layers gives $31.5$  M MAC/frame against $31$  M reported parameters.

Result. Table 1 and Fig. 1 give the verdict: no published system satisfies both constraints, and the two constraints eliminate different models. Weight memory rules out X-UMX, TasNet and both HS-TasNet variants by $8.0$ – $25.5\times$, a gap no scheduling or quantisation strategy closes. Compute independently rules out RT-STT, which passes memory easily at $19\%$ of L2 and then needs $11.4$   $\mathrm{GMAC\,s^{-1}}$, $5.5\times$ what the device sustains. Three of the four large models also exceed the compute budget, by $1.3$ – $2.1\times$: at $\rho\!\approx\!1$ being large *is* being expensive per frame.

HS-TasNet-S is the instructive exception: at $16$  M parameters it is the only prior system that would meet the frame deadline ($67\%$ of budget), yet it overruns L2 by $8.0\times$. RT-STT is its mirror image. The constraints are close to anti-correlated across architecture families, which is why no single size proxy can summarise deployability: RT-STT carries $2.9\times$ the parameters of our deployed model and $6\times$ its per-frame cost, at the same latency.

Scope. The verdict is scoped to audio DSPs of this class, where this part sits at the favourable end: $14.43$  AudioMark/MHz against $3.63$ for a Cortex-M55 and $0.76$ for a Cortex-M4 [^22], so it only hardens on M-class targets. It would not hold on an application processor with a vector backend.

Table 1: Published real-time MSS against a commercial audio DSP budget ($2$  MB L2, $2.07$   $\mathrm{GMAC\,s^{-1}}$ measured, $86.1$ frames s <sup>-1</sup>); memory assumes int8, the most generous case for each system, while our weights are float32. Quality and parameters are from [^6] (rows 1–4) and [^7] (RT-STT). <sup>∗</sup> computed from the published architecture; <sup>†</sup> from the $\rho\!\approx\!1$ identity, hence a lower bound; remaining rows profiled directly.

| Model | cSDR | Params | Mem. | GMAC/s | $\rho$ |
| --- | --- | --- | --- | --- | --- |
| X-UMX | 3.93 | 31 M | $15.5\times$ | $2.71^{*}$ | 1 |
| TasNet | 4.40 | 51 M | $25.5\times$ | $4.39^{\dagger}$ | 1 |
| HS-TasNet-S | 4.48 | 16 M | $8.0\times$ | $1.38^{\dagger}$ | 1 |
| HS-TasNet | 4.65 | 42 M | $21.0\times$ | $3.62^{\dagger}$ | 1 |
| RT-STT | 5.17 | 383 K | ok | 11.39 | 345 |
| full-band $+$ DF (ours) | 5.49 | 444 K | ok | 13.31 | 348 |
| slim $+$ DF (ours) | 4.34 | 129 K | ok | 1.55 | 140 |
| deployed (ours) | 4.70 | 131 K | ok | 1.89 | 167 |

Figure 1: Published real-time MSS against a commercial audio DSP: both budgets as axes, so the deployable set is the shaded box. The two constraints eliminate different systems (HS-TasNet-S meets the frame deadline but overruns L2, RT-STT the reverse), and parameter count predicts neither. Quality is given in Table 1.

## 3 Method

Figure 2: (a) Streaming signal path for one STFT frame: the causal TFC-TDF U-Net emits a complex ratio mask $M_{t}$, a deep-filter head predicts per-bin complex FIR taps $W_{k}$ and a gate $G$ from the latent $Z_{t}$, and the two estimates are blended before the iSTFT. (b) Block internals; the look-ahead order $Q$ is the only source of added algorithmic latency.

Fig. 2 shows the system; panel (a) gives the layer order, and all convolutions are depthwise-separable and left-padded in time. We describe only what the budget forced.

### 3.1 Backbone

The separator is a causal TFC-TDF U-Net [^13] [^7] operating on the real-valued STFT of the mixture ($n_{\mathrm{fft}}{=}1024$, hop $H{=}512$, no centre padding, so frame $t$ depends only on past samples). The $1024$ -point transform gives $513$ bins; following [^7] we keep the lowest $F{=}384$ ($0$ – $16.5$  kHz) and reconstruct $16.5$ – $22.05$  kHz by scaling the mixture’s high band by a per-source gain from the top in-band bins. The crop is a compute dial, MAC scaling linearly in $F$; we also report an $F{=}192$ ($0$ – $8.27$  kHz) variant.

Two choices are dictated by streaming rather than accuracy. *(i)* The recurrence is a GRU, whose state $h_{t}=(1-z_{t})h_{t-1}+z_{t}\tilde{h}_{t}$ is a convex combination of bounded terms and so stays in $[-1,1]$ by construction, whereas an LSTM cell state $c_{t}=f_{t}c_{t-1}+i_{t}g_{t}$ is an unbounded running sum. Streaming two trained checkpoints for $120$  s and tracking $\max|\cdot|$ of the state, the LSTM grows from $399$ to $962$, still rising at $+2.4$  s <sup>-1</sup> with no plateau, while the GRU sits at exactly $1.00$. An unbounded state eventually saturates the downstream activations, so an LSTM needs periodic resets, which reintroduce buffering latency. We did not test whether forget-bias initialisation or recurrent normalisation would bound it instead; the GRU removes the failure mode by construction, which on a part with no reset path is the cheaper argument. *(ii)* The network emits a complex ratio mask on the input spectrum, $\hat{S}^{\mathrm{bb}}_{t}=M_{t}\odot X_{t}$, so silence maps to exactly silence and the idle noise floor is zero by construction rather than by training.

### 3.2 Deep filter

From the latent features $Z_{t}$ a small convolutional head predicts, per source and TF bin, a complex FIR filter $W_{k}$ of order $N{=}P{+}Q{+}1$ and a gate $G\in(0,1)$. The head is two $3\times 3$ convolutions (width $32$, BN, ReLU) and a $1\times 1$ projection to $S(2N{+}1)$ channels, so taps are shared across frequency by construction; it adds $58.5$  k parameters, $15.2\%$ over the backbone. Real and imaginary parts are each $\tanh$ -bounded, the only stability constraint we impose. At $Q{=}0$ the head’s own time padding is left-only, so the coefficient *predictor* is causal too; without that the filter is causal but its taps are not. The filter is applied to the *mixture* spectrum,

$$
\hat{S}^{\mathrm{df}}_{t}\;=\;\sum_{k=-Q}^{P}W_{k}\odot X_{t-k},
$$

and blended with the mask estimate,

$$
\hat{S}_{t}\;=\;G\odot\hat{S}^{\mathrm{bb}}_{t}+(1-G)\odot\hat{S}^{\mathrm{df}}_{t}.
$$

Because the filter reads the mixture, it too maps silence to silence. The split between $P$ past and $Q$ future taps sets the added algorithmic latency exactly: $Q\cdot H/f_{\mathrm{s}}=11.6Q$  ms. We use $N{=}5$ with $Q\in\{0,1,2\}$.

### 3.3 Training on continuous context

Causal convolutions are normally trained on independent chunks, each zero-padded on the left; at inference the same layers see a running cache of real past frames. Stacked layers compound the mismatch: a $3\times 3$ kernel depends on two past frames, so an $L$ -layer stack makes the first $2L$ frames of a chunk depend on padding. With $L\approx 8$ layers across encoder, latent and decoder, ${\sim}16$ of the $65$ frames in a $0.755$  s chunk, a quarter of them, sit in a regime that never occurs in deployment.

The consequence is easy to miss. A chunk-trained model scores $3.93$  dB under the standard block-wise protocol, which resets state at every block, while the *same weights* run frame-by-frame collapse to silent output within ${\sim}2$  s (Fig. 3b). An ablation isolates the cause: threading recurrent state across blocks while keeping the per-block zero padding costs only ${\sim}0.2$  dB, so it is the convolution context, not the recurrent state. Training on single continuous segments ($5.8$  s, one forward pass, no internal padding) restores frame-by-frame performance to within $0.1$  dB of block-wise. The recipe is otherwise unremarkable, and that is the point: one forward pass over a $500$ -frame segment cut at a random position, sources re-mixed across tracks as usual, batch $6$ ($8.8$  GB on one T4), AdamW at $10^{-4}$, gradient-norm clip $3.0$, mixed precision; the DF head is warm-started onto a converged backbone. A truncated-BPTT variant must also overlap consecutive chunks by $n_{\mathrm{fft}}{-}H$ samples, or the frame grid skips a position at every boundary.

Figure 3: (a) Per-stem cSDR across the look-ahead sweep: every stem rises already at the strictly causal $Q{=}0$, so the gain is complex FIR filtering rather than future information. (b) Streaming trajectory under continuous frame-by-frame inference; median of $8$ test tracks, shaded interquartile range. Both start identically at $t{=}0$, where the convolution cache genuinely is zero, but the chunk-trained model collapses to silence within ${\sim}2$  s.

Table 2: Deployable operating points. Time/frame at $1$  GHz against the $11.6$  ms deadline, end to end (signal processing included). Times are measured on the part; the two slim $+$ DF rows are projected from the measured $F{=}192$ rate, network term scaled by MAC and the $0.28$  ms of signal processing held fixed.

| Model | cSDR | uSDR | MAC/fr | Time/fr | Budget |
| --- | --- | --- | --- | --- | --- |
| slim, no DF | 4.04 | 4.24 | 15.1 M | 7.56 ms | 65% |
| slim $+$ DF (LA0) | 4.10 | 4.30 | 18.0 M | 8.98 ms | 77% |
| slim $+$ DF (LA2) | 4.34 | 4.52 | 18.0 M | 8.98 ms | 77% |
| full $+$ DF (LA2) | 4.70 | 4.70 | 21.9 M | 10.43 ms | 90% |

## 4 Experimental Setup

Data and metrics. MUSDB18-HQ [^23], evaluated on the full $50$ -song test split at $44.1$  kHz. We report cSDR (median over $1$  s windows, then over songs, silent reference windows gated) and uSDR (whole-song SDR, mean over songs) [^1] [^2]. cSDR is a plain energy ratio, not the BSSEval-v4 projection of museval [^24] [^25]: on our $50$ tracks, evaluated on the stereo pair, they differ by $-1.33$ to $+1.21$  dB per stem and the sign is not consistent across stems, so cross-paper comparisons are indicative. To make ours directly comparable we report both for the deployed model: $4.70$  dB cSDR is $4.48$  dB under BSSEval-v4, per stem $5.09/5.65/3.87/4.18$ against $6.30/5.21/3.56/2.85$ for vocals/drums/bass/other. “ALL” is the stem mean.

Training. AdamW at lr $10^{-4}$ with an $L_{1}$ waveform loss and the augmentation of [^7]; deployable variants use the continuous-context recipe of §3.3.

Compute accounting. MAC/frame is counted with hooks on every convolution, linear and recurrent layer, and calibrated against hardware: the counter reproduces the $15.08$  M MAC/frame we independently time on the part. The profiler, the feasibility script and the on-device reference runtime will be released.

## 5 Results

### 5.1 Deployable operating points

Table 2 reports the operating points. The full-band separator reaches $4.70$  dB cSDR at $21.9$  M MAC/frame and runs on the part in $10.43$  ms of the $11.6$  ms hop inside $1963$ of $2040$  kB of L2 (§5.4), so it satisfies both constraints by measurement rather than projection. The $F{=}192$ variant trades $0.36$  dB for $77\%$ of compute and a wide memory margin.

### 5.2 Streaming stability

Fig. 3(b) shows what block-wise evaluation hides. Two checkpoints differing *only* in training context are run frame-by-frame with state and convolution cache carried, as the DSP runs them. At $t{=}0$ they are indistinguishable, because the cache genuinely is zero at stream start: the regime chunk training creates. As real context fills it, the chunk-trained model degrades to $0.04$  dB within ${\sim}2$  s and stays there (a silent estimate scores exactly $0$  dB by construction, which is the signature), while the continuous-trained model holds $3.17$  dB (medians over $8$ tracks, last $30$  s). Block-wise, the two are indistinguishable at $3.93$  dB. The deployed model’s continuous cSDR matches its block-wise value, and the mask holds the idle floor at exactly zero.

### 5.3 Look-ahead as a latency knob

Fig. 3(a) sweeps $Q$ on the full-band model, where the effect is cleanest. A *strictly causal* filter ($Q{=}0$) gains $0.38$  dB cSDR and $0.23$  dB uSDR over the matched no-DF baseline, on *every* stem: the gain is complex FIR filtering, not future information. One look-ahead frame ($11.6$  ms) adds $0.19$  dB; the aggregate then flattens ($5.50\to 5.49$) while uSDR still rises ($5.35\to 5.39$). Bounded look-ahead is cheap, and on the full-band model most of it is unnecessary. The slim model qualifies that: at $Q{=}0$ it gains only $0.06$  dB on both metrics, reaching $+0.30$  dB cSDR and $+0.28$  dB uSDR only with both look-ahead frames (Table 2). Cropping to $F{=}192$ leaves a strictly causal filter little to exploit.

What the gate learns. Blend usage $1{-}G$ starts at $0.119$ for every source and converges to $0.104$ (vocals), $0.021$ (other), $0.017$ (drums) and $0.007$ (bass). The near-zero bass gate is not a collapsed optimisation: overriding it at inference on $8$ tracks moves bass in one direction only, $-0.22$  dB forced shut and $-0.34$, $-1.90$, $-3.80$  dB when forced to $0.119$, $0.4$ and $0.8$. Deep filtering does not pay on a source whose energy already sits in a few bins.

### 5.4 On-device validation

The runtime is a hand-scheduled floating-point frame loop, not a generic inference engine. The deployed full-band model runs end to end (int $\to$ float, STFT, network, high band, iSTFT, float $\to$ int) in $10.43$  ms mean and $10.44$  ms worst case, $90\%$ of the $11.6$  ms deadline, inside $1963$ of $2040$  kB of L2 and $447$ of $512$  kB of L1. The $0.01$  ms spread matters as much as the mean: with no allocation, cache refill or data-dependent branch in the frame path, the deadline is met rather than usually met. The six GRUs are $4.37$  ms of it and the deep-filter head $2.77$. Reduced precision is confined to where it cannot accumulate: the convolution ring caches are $16$ -bit float, halving their $1050$  kB, but they hold a two-frame sliding window, while the weights and the indefinitely carried GRU state stay $32$ -bit. The build tracks the PyTorch streaming twin to $7.2\times 10^{-4}$ relative and runs for hours without drift. The $F{=}192$ no-DF variant is measured too, at $7.56$  ms ($65\%$) in $1362$  kB, entirely $32$ -bit and matching to $1.4\times 10^{-6}$; its $15.08$  M MAC in $7.28$  ms is the $2.07$   $\mathrm{GMAC\,s^{-1}}$ used throughout.

## 6 Discussion and Limitations

We are behind on quality. At $4.70$  dB (bootstrap $95\%$ interval $[4.21,5.09]$ over the $50$ tracks) we sit $0.47$  dB below RT-STT on our metric, or $0.69$  dB comparing BSSEval-v4 like for like, and are indistinguishable from HS-TasNet. We do not claim to match RT-STT; we claim it does not run on this class of device. Our unconstrained model reaches $5.49$  dB but needs $6.4\times$ the available compute.

MAC is necessary, not sufficient. It ignores bandwidth and serialisation: at equal MAC a frequency-axis recurrence vectorises far worse than a time-axis one. Pair it with measured time, as in Table 2.

Scope and unmeasured quantities. The memory verdict follows from published parameter counts; the compute verdict for systems we did not implement rests on the $\rho\!\approx\!1$ identity and is a lower bound. Our RT-STT MAC comes from a reproduction scoring $4.93$  dB, so we pair the authors’ quality with our compute and mark it. Rows $1$ and $4$ of Table 2 are measured on hardware, the two $F{=}192$ DF rows are not. We report no fixed-point accuracy: integer formats are not free here, because the recurrent state *is* an accumulator carried indefinitely, which is why it stays $32$ -bit on the part. We report compute, not energy, and MUSDB18-HQ leaves domain robustness untested.

Latency. At $Q{=}2$ the system adds $23.2$  ms to the $23$  ms window: fine for assistive listening and remixing, not for live stage monitoring, where $Q{=}0$ costs $0.24$  dB.

## 7 Conclusion

No published real-time music source separator runs on the embedded hardware it targets, and the reason is not model size: the two constraints eliminate different families and parameter count predicts neither. Building one that fits was a training problem, not an architectural one; ours runs on-device at $4.70$  dB cSDR in $10.43$  ms of an $11.6$  ms hop.

[^1]: Yuki Mitsufuji, Giorgio Fabbro, Stefan Uhlich, Fabian-Robert Stöter, Alexandre Défossez, Minseok Kim, Woosung Choi, Chin-Yun Yu, and Kin-Wai Cheuk, “Music demixing challenge 2021,” Frontiers in Signal Processing, vol. 1, pp. 808395, 2022.

[^2]: Giorgio Fabbro et al., “The sound demixing challenge 2023 – music demixing track,” Trans. Int. Soc. Music Information Retrieval (TISMIR), vol. 7, pp. 63–84, 2024.

[^3]: Simon Rouard, Francisco Massa, and Alexandre Défossez, “Hybrid transformers for music source separation,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process. (ICASSP), 2023, pp. 1–5.

[^4]: Yi Luo and Jianwei Yu, “Music source separation with band-split RNN,” IEEE/ACM Trans. Audio, Speech, and Language Processing, vol. 31, pp. 1893–1901, 2023.

[^5]: Wei-Tsung Lu, Ju-Chiang Wang, Qiuqiang Kong, and Yun-Ning Hung, “Music source separation with band-split RoPE transformer,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process. (ICASSP), 2024, pp. 481–485.

[^6]: Satvik Venkatesh, Arthur Benilov, Philip Coleman, and Frederic Roskam, “Real-time low-latency music source separation using hybrid spectrogram-TasNet,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process. (ICASSP), 2024, pp. 611–615.

[^7]: Junyu Wu, Jie Liu, Tianrui Pan, Jie Tang, and Gangshan Wu, “Towards practical real-time low-latency music source separation,” in Proc. IEEE Int. Conf. Multimedia and Expo (ICME), 2025, pp. 1–6.

[^8]: Chun-Hsiang Wang, Chung-Che Wang, Jun-You Wang, Jyh-Shing Roger Jang, and Yen-Hsun Chu, “Improving real-time music accompaniment separation with MMDenseNet,” in Proc. Conf. Oriental COCOSDA (O-COCOSDA), 2024, pp. 1–6.

[^9]: Clara Borrelli, James Rae, Dogac Basaran, Matt McVicar, Mehrez Souden, and Matthias Mauch, “Resource-constrained stereo singing voice cancellation,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process. (ICASSP), 2024, pp. 436–440.

[^10]: Yi Luo and Nima Mesgarani, “Conv-TasNet: Surpassing ideal time-frequency magnitude masking for speech separation,” IEEE/ACM Trans. Audio, Speech, and Language Processing, vol. 27, no. 8, pp. 1256–1266, 2019.

[^11]: Hanbin Bae, Byungjun Kang, Jiwon Kim, Jaeyong Hwang, Hosang Sung, and Hoon-Young Cho, “Single-channel distance-based source separation for mobile GPU in outdoor and indoor environments,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process. (ICASSP), 2025, pp. 1–5.

[^12]: Hendrik Schröter, Alberto N. Escalante-B., Tobias Rosenkranz, and Andreas Maier, “DeepFilterNet: A low complexity speech enhancement framework for full-band audio based on deep filtering,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process. (ICASSP), 2022, pp. 7407–7411.

[^13]: Woosung Choi, Minseok Kim, Jaehwa Chung, Daewon Lee, and Soonyoung Jung, “Investigating U-Nets with various intermediate blocks for spectrogram-based singing voice separation,” in Proc. Int. Soc. Music Information Retrieval Conf. (ISMIR), 2020.

[^14]: Woosung Choi, Deep Learning-based Latent Source Analysis for Source-aware Audio Manipulation, Ph.D. thesis, Korea University, 2021.

[^15]: Junyu Chen, Susmitha Vekkot, and Pancham Shukla, “Music source separation based on a lightweight deep learning framework (DTTNet: Dual-path TFC-TDF UNet),” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process. (ICASSP), 2024, pp. 656–660.

[^16]: Yun-Ning Hung, Igor Pereira, and Filip Korzeniowski, “Moises-Light: Resource-efficient band-split U-Net for music source separation,” in Proc. IEEE Workshop Applicat. Signal Process. Audio Acoust. (WASPAA), 2025, pp. 1–5.

[^17]: Gerald Schuller, “Low latency time domain multichannel speech and music source separation,” in Proc. Asilomar Conf. Signals, Systems, and Computers, 2021, pp. 549–553.

[^18]: Weinan Tong, Jiaxu Zhu, Jun Chen, Shiyin Kang, Tao Jiang, Yang Li, Zhiyong Wu, and Helen Meng, “SCNet: Sparse compression network for music source separation,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process. (ICASSP), 2024, pp. 1276–1280.

[^19]: Wolfgang Mack and Emanuël A. P. Habets, “Deep filtering: Signal extraction and reconstruction using complex time-frequency filters,” IEEE Signal Processing Letters, vol. 27, pp. 61–65, 2020.

[^20]: Keren Shao, Ke Chen, and Shlomo Dubnov, “Music enhancement with deep filters: A technical report for the ICASSP 2024 Cadenza challenge,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process. Workshops (ICASSPW), 2024, pp. 119–120.

[^21]: Clémentine Berger, Paraskevas Stamatiadis, Roland Badeau, and Slim Essid, “IS <sup>3</sup>: Generic impulsive–stationary sound separation in acoustic scenes using deep filtering,” in Proc. IEEE Workshop Applicat. Signal Process. Audio Acoust. (WASPAA), 2025, pp. 1–5.

[^22]: EEMBC, “AudioMark: An EEMBC benchmark for audio processing on embedded systems,” https://www.eembc.org/audiomark/, 2024, Scores accessed 2026-08-13.

[^23]: Zafar Rafii, Antoine Liutkus, Fabian-Robert Stöter, Stylianos Ioannis Mimilakis, and Rachel Bittner, “The MUSDB18-HQ corpus for music separation (uncompressed version of MUSDB18),” https://doi.org/10.5281/zenodo.3338373, 2019.

[^24]: Fabian-Robert Stöter, Antoine Liutkus, and Nobutaka Ito, “The 2018 signal separation evaluation campaign,” in Proc. Int. Conf. Latent Variable Analysis and Signal Separation (LVA/ICA), 2018, pp. 293–305.

[^25]: Emmanuel Vincent, Rémi Gribonval, and Cédric Févotte, “Performance measurement in blind audio source separation,” IEEE Trans. Audio, Speech, and Language Processing, vol. 14, no. 4, pp. 1462–1469, 2006.