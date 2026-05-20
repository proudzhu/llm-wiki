Zhong-Qiu Wang, and Samuele Cornell Manuscript received on April 30, 2026. (Corresponding author: Zhong-Qiu Wang). Z.-Q. Wang is with the Department of Computer Science and Engineering, Southern University of Science and Technology, Shenzhen 518055, China (e-mail: wang.zhongqiu41@gmail.com / wangzq3@sustech.edu.cn).S. Cornell is with the Language Technologies Institute, Carnegie Mellon University, Pittsburgh, PA 15213, USA (e-mail: cornellsamuele@gmail.com).

###### Abstract

In conversational speech separation and recognition tasks, close-talk microphones are typically attached to each speaker during training data collection to capture near-field, close-talk mixture signals, in addition to using far-field microphones to record far-field mixture signals. Each such close-talk mixture exhibits a reasonably high energy level for the wearer and could intuitively serve as weak supervision for training far-field speech separation models directly on real-recorded far-field signals. However, they are not sufficiently clean for this purpose, as they often contain strong cross-talk speech from other speakers in addition to background noise. To address this, we propose *cross-talk reduction* (CTR), a task aiming to isolate the wearerâ€™s speech from each close-talk mixture, and a novel method called CTRnet, which can be trained directly on real-recorded pairs of close-talk and far-field mixtures to accomplish CTR. Building on CTRnet, we further propose pseudo-label based far-field speech separation (PuLSS), which uses CTRnetâ€™s estimated clean speech as pseudo-labels to train models for separating far-field mixtures. A key advantage of the proposed framework is that both CTRnet and PuLSS can be trained on real-recorded data from the target domain, addressing the generalization gap commonly observed when models are trained exclusively on simulated data. On the CHiME-6 dataset, our framework achieves state-of-the-art ASR performance under both oracle and estimated speaker diarization, surpassing all CHiME-{7,8} challenge submissions. To our knowledge, it is the first neural speech separation method that substantially outperforms guided source separation on real conversational â€œspeech-in-the-wildâ€?data.

## I Introduction

In many pattern analysis and machine intelligence applications, sensors, while recording target signals, inevitably capture concurrent non-target signals (i.e. interference) within the same environment, resulting in a mixture of target and non-target signals [^1]. The non-target signals often pose difficulties for the perception and understanding of the target signals. A prominent example, in audio and acoustic signal processing, is conversational speech separation, a.k.a., the cocktail party problem [^2] [^3] [^4]. In realistic acoustic environments and conversational scenarios (see Fig. 1), speech signals are corrupted by ambient noise, room reverberation, and interference from other speakers. The goal of speech separation is to isolate the speakers of interest from the mixture signals, allowing downstream tasks such as automatic speech recognition (ASR) to perform well [^5] [^6]. Depending on the application, the recording device may range from a single microphone to a microphone array or a set of distributed arrays, with signals typically captured in far-field conditions, where the speaker-to-microphone distance is large relative to the array aperture.

![Refer to caption](figures/fig1.png)

Figure 1: Typical setup for collecting training data in conversational scenarios, where a microphone array is placed at far field to record far-field mixtures. For annotation purposes, a standard practice is to have each speaker wear a close-talk microphone to record close-talk mixtures so that data annotation (e.g., word transcriptions and annotating speaker-activity timestamps) can be facilitated. At deployment, only the far-field array is available for inference.

In the past decade, major advances have been made in speech separation, driven primarily by the adoption of deep learning [^3] [^4]. The current dominant approach relies on supervised learning using large-scale synthetic datasets. To generate these, clean anechoic speech signals from different speakers are first convolved with room impulse responses (RIRs) to simulate reverberant conditions. The resulting signals are then mixed with background noises at varying energy levels to create noisy-reverberant multi-speaker mixtures. Finally, deep neural networks (DNN) are trained on these mixtureâ€“target pairs to learn to predict the clean target speech from noisy-reverberant mixtures [^3]. The clean speech paired with the mixture provides a perfect supervision at the sample level, which allows to fully leverage the power of supervised deep learning. However, although showing impressive performance on simulated mixtures [^7], such fully-supervised, synthetically-trained models often exhibit limited generalizability to real-recorded mixtures [^8] [^9] [^10] [^11] [^12], as current simulation techniques cannot simulate mixtures that are sufficiently realistic, resulting in a persistent domain-mismatch problem between simulated model training and real-world deployment.

A natural solution is to train speech separation models directly on real-recorded mixtures in the target domain, thereby mitigating the domain mismatch problem. However, for real-recorded mixtures, the individual source signals are not available (unlike in the simulated case, where clean sources are available by simulation). As a result, there lacks high-quality sample-level supervision signals for training supervised separation models on real-recorded mixtures.

When collecting far-field conversational data for ASR or speaker diarization, it is a standard practice <sup>1</sup> to simultaneously record each speaker through a microphone placed near their mouth, such as a lapel microphone (see Fig. 1). We refer to each such recording as a *close-talk mixture*, inside which each wearerâ€™s own speech, namely *close-talk speech*, has a much higher energy level than in any far-field mixture, making close-talk mixtures a natural candidate for supervision when training models to separate real-recorded far-field mixtures. However, close-talk mixtures are not clean. They often contain significant cross-talk from other speakers and ambient noise, albeit at lower energy levels than in far-field mixtures. Consequently, close-talk mixtures, which are also mixtures of multiple sound sources, generally cannot be used directly as pseudo-labels for training separation models on real-recorded far-field mixtures. These observations motivate our study of cross-talk reduction: separating each speakerâ€™s close-talk speech from its close-talk mixture. Once separated, these signals can serve as high-quality pseudo-labels and enable supervised training of separation models directly on real-recorded far-field mixtures, thereby mitigating domain mismatches.

A preliminary version [^17] of this work has been published in the IJCAI conference, but only addresses cross-talk reduction by separation on close-talk mixtures. This paper improves cross-talk reduction by separation on close-talk mixtures and extends it for separation on far-field mixtures. Specifically, in [^17], we have made the following contributions:

- We introduce a task named cross-talk reduction and propose to formulate it as a blind deconvolution problem, which requires estimating both the close-talk speech of each speaker and the relative transfer functions (RTF) relating the close-talk speech to reverberant speech at other microphones.
- We propose a solution, CTRnet, which is unsupervised in nature and can be directly trained on pairs of real-recorded close-talk and far-field mixtures.
- We extend this latter to weakly-supervised CTRnet, where speaker-activity timestamps are leveraged as a weak supervision to improve the training of unsupervised CTRnet.

Building upon the conference paper [^17], this paper further makes the following contributions:

- We propose semi-supervised CTRnet, which is trained by combining supervised training if the input mixture is simulated and weakly-supervised training if it is real-recorded.
- We develop a novel mechanism to include noise modeling in CTRnet to deal with ambient noises.
- We introduce a novel mechanism to reduce the reverberation of close-talk speech in CTRnet.
- We propose a pseudo-label approach named PuLSS for far-field speech separation, where close-talk speech estimated by CTRnet is leveraged to derive pseudo-labels for training supervised separation models on real-recorded far-field mixtures (to predict the pseudo-labels). In this way, we can train separation models directly on real-recorded signals in the target domain, potentially realizing better separation.

The proposed PuLSS system obtains state-of-the-art conversational ASR performance on the real-recorded, notoriously-difficult CHiME-6 dataset [^15], representing a practical step toward solving the cocktail party problem in real-world conditions. A sound demo is provided in the link below <sup>2</sup>.

## II Related Work

This paper is related to existing work mainly in two aspects.

### II-A Neural Speech Separation for ASR

Although much progress has been made in supervised neural speech separation, the success of using it as a frontend processing for robust ASR in realistic conversational conditions is limited [^5] [^11] [^6], largely due to the aforementioned domain mismatch problem between simulated training and real-recorded test conditions. Many studies have observed that the predicted target speech by the trained models often exhibits severe speech distortion, which is very detrimental to ASR.

To improve ASR performance, hybrid methods, which combine supervised DNN-based separation with signal processing based linear filtering, have been proposed. One representative approach is to leverage DNN-separated signals to compute signal statistics (e.g., spatial covariance matrices) for linear beamforming, and the beamforming results are then used for ASR. This approach is often effective [^18] [^19] [^12], as beamforming is linearly constrained and thus inherently limits speech distortion [^20]. However, the DNNs still remain sensitive to domain mismatches [^12], and linear filtering itself typically cannot produce sufficient separation in realistic acoustic scenarios, especially when the number of available microphones is limited. Fine-tuning strategies, which jointly fine-tune neural speech separation frontends with a backend ASR model in an end-to-end fashion [^12] [^21], can produce better ASR performance, but joint ASR fine-tuning often degrades the quality of the separated signals themselves [^12].

To improve speech separation itself in realistic conditions, several un- and weakly-supervised approaches, which can be trained directly on target-domain un- or weakly-labeled mixtures, have been proposed. Mixture invariant training [^22] and its variants based on the mixture-of-mixtures concept [^23] [^24] [^25] have shown potential [^26], but they inherently struggle from issues such as source permutation ambiguity, reliance on synthetically-mixed mixtures, lacking dereverberation capabilities, and over- and under-separation [^27], making their applicability to real-world conversational scenarios challenging. Another stream of research realizes unsupervised separation by exploiting multi-channel recordings. For example, UNSSOR [^28] and enhanced RAS [^29] impose mixture constraints among different microphone observations, and DNN-IVA [^30] fuses classical blind source separation with DNNs. However, they only demonstrated effectiveness under simulated conditions with overly simplified setup. Their performance in realistic conversational scenarios is unclear.

Practically, however, none of these previously proposed neural separation methods can produce a satisfactory performance in real-world conversational scenarios, due to challenges in dealing with, e.g., non-stationary ambient noises, time-varying number of speakers, sparse overlap among speakers, long-form recordings (which require producing consistent speaker output channel with no ambiguity), and low signal quality (due to, e.g., microphone failures and synchronization issues) which is very common in real-world deployment. This has been sufficiently demonstrated in recent benchmarks. For example, in the recent CHiME challenges [^11], all systems relied on guided source separation (GSS) [^31], a signal processing algorithm which leverages speaker-activity timestamps and complex-valued Gaussian mixture models to derive signal statistics for linear beamforming. Neural approaches such as VarArray [^32] and continuous source separation [^33] [^34] [^35] have shown promise, but remain less robust even within a single acoustic domain. This is evidenced by their inferior performance compared to GSS-based approaches in the recent NOTSOFAR-1 challenge [^10]. Among the few exceptions are recently-proposed unsupervised full-rank spatial covariance models [^36] [^37] [^38], which have demonstrated competitive and slightly-superior performance to GSS on CHiME-8 conversational data [^38], albeit only with oracle diarization.

In contrast, our proposed PuLSS approach trains separation models directly on real-recorded far-field mixtures using pseudo-labels derived from close-talk mixture signals, thereby avoiding the domain mismatch problems that limit existing neural approaches. To the best of our knowledge, PuLSS is the first neural separation method to significantly outperform GSS in real-recorded conversational scenarios, with both oracle and estimated diarization (see later Section VIII-B and VIII-C).

### II-B Exploiting Close-Talk Mixtures for Speech Enhancement

There are studies exploiting close-talk mixtures for far-field speech enhancement, a task similar to speech separation but dealing with a single target speaker. ctPuLSE [^39] first enhances real-recorded close-talk mixtures by using supervised models trained on simulated mixtures, and then uses the enhanced close-talk speech as pseudo-labels for training far-field speech enhancement models. However, the supervised model used to derive pseudo-labels also suffers from domain mismatch problems when enhancing real-recorded close-talk mixtures. SuperM2M [^40], building upon M2M [^41], trains DNNs on far-field mixtures such that the DNN estimates can be linearly filtered to approximate the speech and noise components in close-talk mixtures. However, this technique assumes a single speaker and is not natively designed to leverage the fact that the close-talk mixture exhibits a higher signal-to-noise ratio (SNR) of the wearer. SuPseudo [^42] and TLS [^43] linearly filter unprocessed close-talk mixtures and use them as pseudo-labels for far-field speech enhancement. This approach assumes that close-talk mixtures are sufficiently clean, which is not the case in most conversational scenarios.

Unlike these methods, our approach handles multi-speaker separation rather than single-speaker enhancement, does not assume clean close-talk mixtures, and avoids domain mismatch by training CTRnet directly on real-recorded mixtures rather than relying on supervised models trained on simulated mixtures to derive pseudo-labels.

## III Physical Model and Objectives

Suppose that we have a set of training mixtures recorded in a number of noisy-reverberant environments, each with a far-field microphone array with $P$ microphones and a maximum of $C$ speakers (each wearing a close-talk microphone near the mouth or on the lapel). See Fig. 1 for an illustration. The physical models for each close-talk mixture and each far-field mixture can be formulated, in the short-time Fourier transform (STFT) domain, as follows:

$$
\displaystyle Y_{d}(t,f)
$$
 
$$
\displaystyle=\sum\nolimits_{c=1}^{C}X_{d}(c,t,f)+V_{d}(t,f),
$$
$$
\displaystyle Y_{p}(t,f)
$$
 
$$
\displaystyle=\sum\nolimits_{c=1}^{C}X_{p}(c,t,f)+V_{p}(t,f),
$$

where $c$ indexes $C$ speakers, $d$ indexes $C$ close-talk microphones (as each speaker wears a single close-talk microphone), $p$ indexes $P$ far-field microphones, $t$ indexes $T$ frames, and $f$ indexes $F$ frequency bins. In Eq. (1), $Y_{d}(t,f)$, $X_{d}(c,t,f)$, and $V_{d}(t,f)$ respectively denote the STFT coefficients of the mixture, reverberant speech (or speaker image) of speaker $c$, and reverberant noise signals captured by close-talk microphone $d$ at time $t$ and frequency $f$. In this paper, when dropping the indices $c$, $t$ and $f$, we refer to the corresponding spectrograms. In Eq. (2), $Y_{p}$, $X_{p}(c)$ and $V_{p}$ respectively denote the STFT spectrograms of the mixture, reverberant speech of speaker $c$, and reverberant noise signals captured by far-field microphone $p$. We denote the close-talk speech of each speaker $c$ as â€?$X_{d}(c)$ with $d=c$ â€?or â€?$X_{d(=c)}(c)$ â€? and denote the cross-talk speech of speaker $c$ at close-talk microphone $d$ as â€?$X_{d}(c)$ with $d\neq c$ â€?

With this formulation, we propose to study cross-talk reduction by speech separation, aiming at reducing the cross-talk speech and noises in each close-talk mixture to estimate the close-talk speech, followed by cross-talk reduction for speech separation, where the resulting estimated close-talk speech are leveraged to derive pseudo-labels for training supervised far-field speech separation models. See Fig. 2 for an overview.

A straightforward way to realize cross-talk reduction is to first simulate many pairs of close-talk mixtures and close-talk speech, and then train a supervised model to predict the close-talk speech based on the close-talk mixtures. However, this supervised approach based on simulated data often exhibits limited generalizability to real-recorded mixtures, as discussed in the Introduction section.

We propose to train models for cross-talk reduction directly on target-domain, real-recorded pairs of close-talk and far-field mixtures, in an un-, weakly- or semi-supervised way, thereby improving the generalizability. In the following sections, we propose CTRnet in Section IV to estimate close-talk speech, followed by a model named PuLSS in V, which leverages estimated close-talk speech to compute pseudo-labels for training supervised far-field speech separation models.

![Refer to caption](figures/fig2.png)

Figure 2: System overview. (a) Training Stage: CTRnet is trained in a semi-supervised manner on real-recorded pairs of close-talk and far-field mixtures to estimate close-talk speech (see Section IV-D ). The estimate is then used as pseudo-labels for training PuLSS in a supervised fashion on real-recorded far-field mixtures (see Section V-D ). In PuLSS, oracle speaker-activity timestamps are used in input features to resolve the speaker-permutation problem during training. (b) Inference Stage: the PuLSS model separates far-field mixtures and an ASR model transcribes the separated speech. At inference time, either oracle speaker-activity timestamps or estimated ones by an external speaker diarization system can be used (see the dashed arrow).

## IV Cross-Talk Reduction by Separation

We propose CTRnet, which can be trained via unsupervised and weakly-supervised learning on real-recorded pairs of close-talk and far-field mixtures to realize cross-talk reduction. To avoid confusion, Table I lists the hyper-parameters of our models, and their default values or set of values to tune.

TABLE I: List of Key Hyper-Parameters of CTRnet and PuLSS.

<table><tbody><tr><td>Model</td><td>Symbols</td><td>Description</td><td>Introduced in</td><td>Values</td></tr><tr><td rowspan="6">CTRnet</td><td><math><semantics><mi>I</mi> <annotation>I</annotation></semantics></math></td><td>Number of past taps in FCP filtering</td><td>Eq. (3)</td><td><math><semantics><mn>13</mn> <annotation>13</annotation></semantics></math></td></tr><tr><td><math><semantics><mi>J</mi> <annotation>J</annotation></semantics></math></td><td>Number of future taps in FCP filtering</td><td>Eq. (3)</td><td><math><semantics><mn>1</mn> <annotation>1</annotation></semantics></math></td></tr><tr><td><math><semantics><mi>Î¾</mi> <annotation>\xi</annotation></semantics></math></td><td>Factor for flooring denominator in FCP</td><td>Eq. (12)</td><td><math><semantics><mn>0.01</mn> <annotation>0.01</annotation></semantics></math></td></tr><tr><td><math><semantics><mi>Î²</mi> <annotation>\beta</annotation></semantics></math></td><td>Weight of speaker-activity loss</td><td>Eq. (16)</td><td><math><semantics><mrow><mo>{</mo> <mn>1.0</mn><mo>,</mo><mn>0.1</mn> <mo>}</mo></mrow> <annotation>\{1.0,0.1\}</annotation></semantics></math></td></tr><tr><td><math><semantics><mi>Î”</mi> <annotation>\Delta</annotation></semantics></math></td><td>Prediction delay for modeling reverberation</td><td>Eq. (24)</td><td><math><semantics><mrow><mo>{</mo> <mn>1</mn><mo>,</mo><mn>2</mn><mo>,</mo><mn>3</mn><mo>,</mo><mn>4</mn> <mo>}</mo></mrow> <annotation>\{1,2,3,4\}</annotation></semantics></math></td></tr><tr><td><math><semantics><msub><mi>Îº</mi> <mn>1</mn></msub> <annotation>\kappa_{1}</annotation></semantics></math></td><td>Weight for supervised loss on simulated data in semi-supervised CTRnet</td><td>Eq. (18)</td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td></tr><tr><td rowspan="5">PuLSS</td><td><math><semantics><mi>L</mi> <annotation>L</annotation></semantics></math></td><td>Number of filter taps to compute pseudo-labels</td><td>Eq. (25)</td><td><math><semantics><mn>2</mn> <annotation>2</annotation></semantics></math></td></tr><tr><td><math><semantics><mi>E</mi> <annotation>E</annotation></semantics></math></td><td>Maximum hypothesized time delay for synchronization</td><td>Eq. (26)</td><td><math><semantics><mn>9</mn> <annotation>9</annotation></semantics></math></td></tr><tr><td><math><semantics><mi>A</mi> <annotation>A</annotation></semantics></math></td><td>Number of filters taps on each side for <math><semantics><msub><mi>â„?/mi> <mtext>CTE</mtext></msub> <annotation>\mathcal{L}_{\text{CTE}}</annotation></semantics></math> loss</td><td>Eq. (29)</td><td><math><semantics><mn>1</mn> <annotation>1</annotation></semantics></math></td></tr><tr><td><math><semantics><mi>Î´</mi> <annotation>\delta</annotation></semantics></math></td><td>Weight of loss on close-talk estimates</td><td>Eq. (31)</td><td><math><semantics><mn>20</mn> <annotation>20</annotation></semantics></math></td></tr><tr><td><math><semantics><msub><mi>Îº</mi> <mn>2</mn></msub> <annotation>\kappa_{2}</annotation></semantics></math></td><td>Weight for supervised loss on simulated data when training PuLSS with both simu and real data</td><td>Eq. (33)</td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td></tr><tr><td rowspan="2">Both CTRnet & PuLSS</td><td><math><semantics><mi>Î±</mi> <annotation>\alpha</annotation></semantics></math></td><td>Magnitude compression factor</td><td>Eq. (8)</td><td><math><semantics><mrow><mo>{</mo> <mn>1.0</mn><mo>,</mo><mn>0.3</mn> <mo>}</mo></mrow> <annotation>\{1.0,0.3\}</annotation></semantics></math></td></tr><tr><td><math><semantics><mi>Î¸</mi> <annotation>\theta</annotation></semantics></math></td><td>Factor in weighted sampling</td><td>Eq. (34)</td><td><math><semantics><mrow><mo>{</mo> <mn>5</mn><mo>,</mo><mn>10</mn><mo>,</mo><mn>20</mn><mo>,</mo><mn>40</mn><mo>,</mo><mn>80</mn> <mo>}</mo></mrow> <annotation>\{5,10,20,40,80\}</annotation></semantics></math></td></tr></tbody></table>

### IV-A Formulating CTR as Blind Deconvolution

Due to the short distance from each speaker to its close-talk microphone, the close-talk speech can be viewed as the dry sound source signal with a small time-delay <sup>3</sup>. In this case, linearly filtering close-talk speech can largely reproduce its cross-talk speech at the close-talk microphones of the other speakers, as well as the reverberant speech of the speaker at far-field microphones. With this understanding, we can reformulate the physical models in Eq. (1) and (2) in the following as (3) and (4), and formulate CTR as a blind deconvolution problem in (IV-A).

In detail, let $Z(d)=X_{d(=c)}(c)$ denote the close-talk speech at close-talk microphone $d$, we can formulate Eq. (1) as

$$
\displaystyle Y_{d}(t,f)=Z(d,t,f)+\sum\limits_{c=1,c\neq d}^{C}X_{d}(c,t,f)+V_{d}(t,f)
$$
 
$$
\displaystyle=Z(d,t,f)+\sum\limits_{c=1,c\neq d}^{C}\mathbf{g}_{d}(c,f)^{{\mathsf{H}}}\ \widetilde{\mathbf{Z}}(c,t,f)+V_{d}^{\prime}(t,f),
$$

where $\widetilde{\mathbf{Z}}(c,t,f)=[Z(c,t-I,f),\dots,Z(c,t,f),\dots,Z(c,t+J,f)]^{\mathsf{T}}\in{\mathbb{C}}^{I+1+J}$ stacks the complex STFT coefficients of a time window of $I+1+J$ time-frequency (T-F) units within frequency bin $f$. Here, $I$ and $J$ respectively denote the number of past and future filter taps, and $\mathbf{g}_{d}(c,f)\in{\mathbb{C}}^{I+1+J}$ is a linear filter. In Eq. (3), we have $X_{d}(c,t,f)\approx\mathbf{g}_{d}(c,f)^{{\mathsf{H}}}\ \widetilde{\mathbf{Z}}(c,t,f)$, which, following narrowband linear approximation [^44] [^45], approximates the cross-talk speech of speaker $c$ captured by close-talk microphone $d$ (i.e., $X_{d}(c)$ with $d\neq c$) as a linear convolution between the close-talk speech of speaker $c$ (i.e., $Z(c)$) and an RTF relating the close-talk speech of speaker $c$ to close-talk microphone $d$ (i.e., $\mathbf{g}_{d}(c,f)$ where $d\neq c$). In Eq. (3), $V_{d}^{\prime}$ absorbs the modeling error of linear approximation. Similarly, for far-field mixtures, we can reformulate Eq.(2) as

$$
\displaystyle Y_{p}(t,f)
$$
 
$$
\displaystyle=\sum\limits_{c=1}^{C}\mathbf{g}_{p}(c,f)^{{\mathsf{H}}}\ \widetilde{\mathbf{Z}}(c,t,f)+V_{p}^{\prime}(t,f),
$$

with $\mathbf{g}_{p}(c,f)$ denoting the RTF from speaker $c$ to far-field microphone $p$ and $V_{p}^{\prime}$ absorbing the modeling error.

With the physical models in Eq. (3) and (4) and assuming $V^{\prime}$ (including ambient noises, and modeling errors incurred by linear approximation) being small, we can realize cross-talk reduction by solving, e.g., the minimization problem below:

$$
\displaystyle\underset{\mathbf{g}_{\cdot}(\cdot,\cdot),Z(\cdot,\cdot,\cdot)}{\operatornamewithlimits{argmin}}\Big(
$$
$$
\displaystyle\sum\limits_{d=1}^{C}\sum\limits_{t,f}\Big|Y_{d}(t,f)-Z(d,t,f)-\sum\limits_{\begin{subarray}{c}c=1,c\neq d\end{subarray}}^{C}{\mathbf{g}}_{d}(c,f)^{{\mathsf{H}}}\ \widetilde{{\mathbf{Z}}}(c,t,f)\Big|^{2}
$$
 
$$
\displaystyle\quad\,\,\,\,\,+\sum\limits_{p=1}^{P}\sum\limits_{t,f}\Big|Y_{p}(t,f)-\sum\limits_{c=1}^{C}{\mathbf{g}}_{p}(c,f)^{{\mathsf{H}}}\ \widetilde{{\mathbf{Z}}}(c,t,f)\Big|^{2}\Big),
$$

which aims at finding the linear filters and close-talk speech signals that are, in a least-square sense, most consistent with the physical models in (3) and (4). This problem is an embodiment of the blind deconvolution problem [^46] in pattern analysis and machine intelligence. It is difficult to solve as both the linear filters and close-talk speech signals are unknown and need to be estimated, but only the summation of their linear-convolutional results (i.e., the close-talk and far-field mixtures) are observed. To deal with this, our preliminary conference paper [^17] proposes to solve this problem via unsupervised deep learning, yielding unsupervised CTRnet, which is described next.

![Refer to caption](figures/fig3.png)

Figure 3: Illustration of unsupervised CTRnet. Best viewed in color.

### IV-B Unsupervised CTRnet

Fig. 3 illustrates unsupervised CTRnet, which trains a DNN, using all the $C$ close-talk mixtures as input, to produce an estimate $\hat{Z}(d)\in{\mathbb{C}}^{T\times F}$ at each close-talk microphone $d$. Differently from the supervised setup, for real-recorded close-talk mixtures, we do not have oracle target speech to directly penalize the estimates $\{\hat{Z}(d)\}_{d=1}^{C}$. In unsupervised CTRnet, we propose to penalize the estimates by checking to what extent the estimates satisfy the physical models hypothesized in Eq. (3) and (4), thereby promoting the estimates to approximate the corresponding close-talk speech. We realize this penalization by considering each of the close-talk and far-field mixtures as a constraint to the estimates, and define a mixture-constraint (MC) loss, which follows the objective in Eq. (IV-A):

$$
\displaystyle\mathcal{L}_{\text{MC}}=\sum\nolimits_{d=1}^{C}\mathcal{L}_{\text{MC},d}+\sum\nolimits_{p=1}^{P}\mathcal{L}_{\text{MC},p},
$$

where $\mathcal{L}_{\text{MC},d}$ is the MC loss at close-talk microphone $d$ and $\mathcal{L}_{\text{MC},p}$ at far-field microphone $p$. Following the physical model in (3) and the first term in (IV-A), at close-talk microphone $d$ we define $\mathcal{L}_{\text{MC},d}$ as

$$
\displaystyle\mathcal{L}_{\text{MC},d}=\sum_{t,f}\mathcal{F}\Big(Y_{d}(t,f),\hat{Y}_{d}(t,f)\Big)
$$
 
$$
\displaystyle=\sum\limits_{t,f}\mathcal{F}\Big(Y_{d}(t,f),\hat{Z}(d,t,f)+\sum_{c=1,c\neq d}^{C}\hat{X}_{d}^{\text{FCP}}(c,t,f)\Big)
$$
 
$$
\displaystyle=\sum\limits_{t,f}\mathcal{F}\Big(Y_{d}(t,f),\hat{Z}(d,t,f)+\sum_{c=1,c\neq d}^{C}\hat{\mathbf{g}}_{d}(c,f)^{{\mathsf{H}}}\ \widetilde{\hat{\mathbf{Z}}}(c,t,f)\Big).
$$

where, following the definitions of $\widetilde{\mathbf{Z}}(c,t,f)$ and $\mathbf{g}_{d}(c,f)$ in Eq. (3), $\widetilde{\hat{\mathbf{Z}}}(c,t,f)=[\hat{Z}(c,t-I,f),\dots,\hat{Z}(c,t,f),\dots,\hat{Z}(c,t+J,f)]^{\mathsf{T}}\in{\mathbb{C}}^{I+1+J}$ stacks a time window of $I+1+J$ T-F units within frequency bin $f$ and $\hat{\mathbf{g}}_{d}(c,f)\in{\mathbb{C}}^{I+1+J}$ is an estimated linear filter used for filtering the estimated close-talk speech of the other speakers to approximate their cross-talk speech at close-talk microphone $d$ (i.e., $\hat{X}_{d}^{\text{FCP}}(c,t,f)=\hat{\mathbf{g}}_{d}(c,f)^{{\mathsf{H}}}\ \widetilde{\hat{\mathbf{Z}}}(c,t,f)$). We estimate the linear filter (i.e., $\hat{\mathbf{g}}_{d}(c,f)$) via the forward convolutive prediction (FCP) algorithm [^47], which will be described later in Eq. (11). Finally, we compute a loss between the reconstructed mixture $\hat{Y}_{d}$ and the observed mixture $Y_{d}$, by using a loss function $\mathcal{F}(\cdot,\cdot)$, which, following [^7], computes an absolute loss on the estimated real, imaginary and magnitude components:

$$
\displaystyle\mathcal{F}\Big(Y_{d}(t,f),\hat{Y}_{d}(t,f)\Big)=\frac{\mathcal{G}\Big(Y_{d}(t,f),\hat{Y}_{d}(t,f)\Big)}{\sum\nolimits_{t^{\prime},f^{\prime}}\big|Y_{d}(t^{\prime},f^{\prime})\big|^{\alpha}},
$$
$$
\displaystyle\mathcal{G}\Big(Y_{d}(t,f),\hat{Y}_{d}(t,f)\Big)=\Big||Y_{d}(t,f)|^{\alpha}-|\hat{Y}_{d}(t,f)|^{\alpha}\Big|
$$
 
$$
\displaystyle+\Big||Y_{d}(t,f)|^{\alpha}\cos(\angle Y_{d}(t,f))-|\hat{Y}_{d}(t,f)|^{\alpha}\cos(\angle\hat{Y}_{d}(t,f))\Big|
$$
 
$$
\displaystyle+\Big||Y_{d}(t,f)|^{\alpha}\sin(\angle Y_{d}(t,f))-|\hat{Y}_{d}(t,f)|^{\alpha}\sin(\angle\hat{Y}_{d}(t,f))\Big|.
$$

In Eq. (8), the denominator is a normalization term balancing the losses at different microphones. Different from the conference paper [^17], this paper introduces a tunable magnitude compression factor $\alpha$ to the loss function, following [^48].

Similarly, following the physical model in (4) and the second term in (IV-A), at each far-field microphone $p$ we define $\mathcal{L}_{\text{MC},p}$ as

$$
\displaystyle\mathcal{L}_{\text{MC},p}
$$
 
$$
\displaystyle=\sum_{t,f}\mathcal{F}\Big(Y_{p}(t,f),\hat{Y}_{p}(t,f)\Big)
$$
 
$$
\displaystyle=\sum_{t,f}\mathcal{F}\Big(Y_{p}(t,f),\sum_{c=1}^{C}\hat{X}_{p}^{\text{FCP}}(c,t,f)\Big)
$$
 
$$
\displaystyle=\sum_{t,f}\mathcal{F}\Big(Y_{p}(t,f),\sum_{c=1}^{C}\hat{\mathbf{g}}_{p}(c,f)^{{\mathsf{H}}}\ \widetilde{\hat{\mathbf{Z}}}(c,t,f)\Big),
$$

where we linearly filter the DNN estimate $\hat{Z}(c)$ for each speaker $c$ using $\hat{\mathbf{g}}_{p}(c,f)$ so that their summation can approximate the observed far-field mixture.

The linear filters, $\hat{\mathbf{g}}_{d}(c,f)$ in Eq. (7) and $\hat{\mathbf{g}}_{p}(c,f)$ in (10), are estimated via FCP by solving the following problem [^47]:

$$
\displaystyle\hat{\mathbf{g}}_{m}(c,f)=\underset{\mathbf{g}_{m}(c,f)}{\text{argmin}}\sum\limits_{t}\frac{\Big|Y_{m}(t,f)-\mathbf{g}_{m}(c,f)^{{\mathsf{H}}}\ \widetilde{\hat{\mathbf{Z}}}(c,t,f)\Big|^{2}}{\lambda_{m}(t,f)},
$$

where $m$ indexes the $C$ close-talk and $P$ far-field microphones, and $\lambda$ is a weighting term defined, following [^47], as

$$
\displaystyle\lambda_{m}(t,f)=\xi\times\max(|Y_{m}|^{2})+|Y_{m}(t,f)|^{2},
$$

with $\xi$ flooring the weighting term and $\max(\cdot)$ extracting the maximum value of a power spectrogram. In this study, we propose another way to compute the weighting term:

$$
\displaystyle\lambda_{m}(t,f)
$$
 
$$
\displaystyle=\xi\times\operatorname{quantile}\big(\Omega,90\big)+|Y_{m}(t,f)|^{2},
$$

where $\Omega=\{\max(|Y_{m}(t,\cdot)|^{2})\}_{t=1}^{T}$ consists of the maximum energy of the T-F units within each frame, and $\operatorname{quantile}\big(\Omega,90\big)$ extracts the $90$ -th percentile. We find that this strategy can more effectively deal with the case when the input mixture has clicking sounds with sudden power bursts (e.g., from microphones moving around or inadvertently touched), which is quite common in real-recorded conversational signals. Notice that the optimization problem in Eq. (11) is a linear regression problem. It has a closed-form solution which can be readily computed. We then plug the solution into Eq. (7) and (10) to compute the MC losses, and train the network.

### IV-C Weakly-Supervised CTRnet

Unsupervised CTRnet is trained on fixed-length mixture segments, assuming at maximum $C$ active speakers to separate within each segment. This assumption however does not always hold as the number of speakers is different for different training segments. See Fig. 4 for an example. When the active number of speakers is smaller than $C$, unsupervised CTRnet tends to over-separate the speakers (e.g., split a speaker to multiple outputs, as doing this would always result in a smaller MC loss); and when the active number of speakers is larger than $C$, unsupervised CTRnet would under-separate the speakers (i.e., cannot sufficiently separate the speakers). These behaviors are similar to what we observe in unsupervised clustering algorithms such as Kmeans when the hypothesized number of clusters differs from the actual number.

To address this issue, we assume that, for each speaker $c$, a speaker-activity timestamp label $d(c)\in\{0,1\}^{N}$ denoting whether each speaker $c$ is active at each sample (assuming the signal is $N$ -sample long) is provided. As mentioned in the Introduction section, in practical setups for collecting real-recorded conversational data, such labels are routinely annotated, and can even be obtained in a semi-automatic way by using additional on-speaker throat microphones [^34].

The timestamps are leveraged as a weak-supervision to improve the training of unsupervised CTRnet, as they can provide the information of the exact number of active speakers at each sample. They are leveraged to mask DNN estimates $\hat{Z}$ before computing the FCP filters and $\mathcal{L}_{\text{MC}}$ loss:

$$
\displaystyle\hat{Z}(c,t,f):=\hat{Z}(c,t,f)\times D(c,t),
$$

where $D(c,t)\in\{0,1\}$, defined based on $d(c)$, is one if the STFT window corresponding to frame $t$ contains any active speech samples of speaker $c$ and is zero otherwise. We name this technique frame muting.

After using frame muting in Eq. (14), the $\mathcal{L}_{\text{MC}}$ loss only penalizes DNN predictions in non-silent ranges marked by the speaker-activity timestamps. However, the predictions in silent ranges are no longer penalized. To deal with this, we introduce a speaker-activity (SA) loss $\mathcal{L}_{\text{SA}}$ to push the DNN estimate towards zero:

$$
\displaystyle\mathcal{L}_{\text{SA}}=\sum\limits_{c=1}^{C}\frac{\sum_{t,f}\big|\hat{Z}(c,t,f)\big|^{\alpha}\times\big(1-D(c,t)\big)}{\sum_{t,f}\big|Y_{d(=c)}(t,f)\big|^{\alpha}},
$$

where the denominator $\sum_{t,f}|Y_{d(=c)}(t,f)|^{\alpha}$ is the compressed energy of the close-talk mixture signal of speaker $c$, serving as a normalization term consistent with Eq. (8). We combine it with $\mathcal{L}_{\text{MC}}$ in (6) for model training:

$$
\displaystyle\mathcal{L}_{\text{MC+SA}}=\mathcal{L}_{\text{MC}}+\beta\times\mathcal{L}_{\text{SA}},
$$

where $\beta\in{\mathbb{R}}_{>0}$ is a tunable weighting term.

![Refer to caption](figures/fig4.png)

Figure 4: Illustration of sparse and time-varying speaker overlap. Each colored block indicates that the corresponding speaker is active. The bracket denotes a fixed-length processing segment used for both training and inference (see Section VI-B ), within which the number of active speakers may vary.

### IV-D Semi-Supervised CTRnet

CTRnet can be trained directly on real-recorded pairs of close-talk and far-field mixtures. However, real-recorded training mixtures are often scarce, as collecting them is labor-intensive. In this context, we propose a semi-supervised learning algorithm that trains the same CTRnet model on both real-recorded and simulated mixtures. When the input mixture is real-recorded, we use the weakly-supervised loss in Eq. (16) for training, and when the input mixture is simulated, we use a supervised loss defined as

$$
\displaystyle\mathcal{L}_{\text{sup,speech}}^{\text{CTRnet}}=\sum_{c=1}^{C}\frac{\sum_{t,f}\mathcal{G}\Big(\hat{Z}(c,t,f),X_{d(=c)}(c,t,f)\Big)}{\sum_{t,f}|Y_{d(=c)}(t,f)|^{\alpha}},
$$

where $\mathcal{G}(\cdot,\cdot)$ is defined in Eq. (9), and $X_{d(=c)}(c)$ and $Y_{d(=c)}$ respectively denote the close-talk speech and close-talk mixture of speaker $c$. The overall loss is defined as

$$
\mathcal{L}_{\text{sup,MC+SA}}^{\text{CTRnet}}=\left\{\begin{aligned} &\kappa_{1}\times\mathcal{L}_{\text{sup}}^{\text{CTRnet}},\text{if input mixture is simulated},\\
&\mathcal{L}_{\text{MC+SA}},\text{if input mixture is real-recorded},\end{aligned}\right.
$$

where $\kappa_{1}\in{\mathbb{R}}_{\geq 0}$ is a tunable weighting term, and $\mathcal{L}_{\text{sup}}^{\text{CTRnet}}$ summates all the supervised losses consisting of $\mathcal{L}_{\text{sup,speech}}^{\text{CTRnet}}$ in Eq. (17) and, optionally, $\mathcal{L}_{\text{sup,noise}}^{\text{CTRnet}}$ defined later in (19).

### IV-E Noise Modeling

The CTRnet models presented so far assume that ambient noises (i.e., $V$) are weak, and do not model noises. This would result in estimated close-talk speech signals inevitably containing noises, as the estimated signals are trained, via the MC losses, to reconstruct observed mixture signals, which are usually noisy. To alleviate this issue, we propose to model noises by training the DNN model to additionally predict the noise signal at each close-talk microphone. In other words, the DNN model is trained to output $2\times C$ signals, with the first $C$ outputs estimating close-talk speech and the rest estimating the noise signals at the close-talk microphones. When the input mixture is simulated, we penalize the noise estimates using the following supervised loss:

$$
\displaystyle\mathcal{L}_{\text{sup,noise}}^{\text{CTRnet}}=\sum_{d=1}^{C}\frac{\sum_{t,f}\mathcal{G}\Big(\hat{V}_{d}(t,f),V_{d}(t,f)\Big)}{\sum_{t,f}|Y_{d}(t,f)|^{\alpha}},
$$

where $\hat{V}_{d}$ denotes the DNN-estimated noise STFT spectrogram at close-talk microphone $d$, and $V_{d}$ the corresponding oracle (available only for simulated mixtures). When the input mixture is real-recorded, we penalize them via MC losses. In detail, we first average the noise estimates and consider the average as a source in addition to the $C$ speakers:

$$
\displaystyle\hat{Z}(C+1)=\frac{1}{C}\sum_{d=1}^{C}\hat{V}_{d},
$$

and modify $\mathcal{L}_{\text{MC},d}$ defined in Eq. (7) and $\mathcal{L}_{\text{MC},p}$ in (10) to include the noise estimate $\hat{Z}(C+1)$:

$$
\displaystyle\mathcal{L}_{\text{MC},d}=\sum\limits_{t,f}\mathcal{F}\Big(Y_{d}(t,f),
$$
$$
\displaystyle\quad\quad\quad\quad\quad\,\,\hat{Z}(d,t,f)+\sum_{c=1,c\neq d}^{C+1}\hat{\mathbf{g}}_{d}(c,f)^{{\mathsf{H}}}\ \widetilde{\hat{\mathbf{Z}}}(c,t,f)\Big),
$$
$$
\displaystyle\mathcal{L}_{\text{MC},p}=\sum_{t,f}\mathcal{F}\Big(Y_{p}(t,f),\sum_{c=1}^{C+1}\hat{\mathbf{g}}_{p}(c,f)^{{\mathsf{H}}}\ \widetilde{\hat{\mathbf{Z}}}(c,t,f)\Big).
$$

An alternative is to randomly choose a noise estimate as $\hat{Z}(C+1)$ for each training example:

$$
\displaystyle\hat{Z}(C+1)=\operatorname{RandomChoice}\big(\{\hat{V}_{d}\}_{d=1}^{C}\big).
$$

For the additional source, we do not apply frame muting, since noise-activity timestamp is not available. We just assume that the noise is always active.

### IV-F Reverb Modeling and Dereverb of Close-Talk Speech

Reverberation exists in close-talk speech. In previous sections, it is assumed much weaker than the direct-path signal and negligible. In this subsection, we explicitly model it in close-talk speech in order to reduce it. In detail, we modify the loss function in Eq. (21) to

$$
\displaystyle\mathcal{L}_{\text{MC},d}=\sum\limits_{t,f}\mathcal{F}\Big(Y_{d}(t,f),
$$
$$
\displaystyle\hat{Z}(d,t,f)+\hat{\mathbf{h}}_{d}(f)^{{\mathsf{H}}}\ \overline{\hat{\mathbf{Z}}}(d,t,f)+\sum_{c=1,c\neq d}^{C+1}\hat{\mathbf{g}}_{d}(c,f)^{{\mathsf{H}}}\ \widetilde{\hat{\mathbf{Z}}}(c,t,f)\Big),
$$

where, different from $\widetilde{\hat{\mathbf{Z}}}(c,t,f)$ defined in Eq. (7), $\overline{\hat{\mathbf{Z}}}(d,t,f)=[\hat{Z}(d,t-I,f),\dots,\hat{Z}(d,t-\Delta,f)]^{\mathsf{T}}\in{\mathbb{C}}^{I-\Delta+1}$ stacks $I-\Delta+1$ T-F units that are at least $\Delta$ ($>0$) frames in the past, and $\hat{\mathbf{h}}_{d}(f)\in{\mathbb{C}}^{I-\Delta+1}$ is computed in the same way as Eq. (11). $\hat{\mathbf{h}}_{d}(f)^{{\mathsf{H}}}\ \overline{\hat{\mathbf{Z}}}(d,t,f)$ is designed to absorb (or explain) the late reverberation component inside the close-talk speech, thereby driving $\hat{Z}(d)$ towards an estimate with less reverberation.

In Eq. (24), $\hat{Z}$ is constrained to estimate a dereverberated close-talk speech. When combining this technique with supervised training on simulated mixtures for semi-supervised training, we should modify the $\mathcal{L}_{\text{sup,speech}}^{\text{CTRnet}}$ loss defined in Eq. (17), where $\hat{Z}$ is however trained to fit close-talk speech. We just replace the speakerâ€™s close-talk speech in Eq. (17) with direct-path signal, which can be readily simulated along with close-talk speech. Note that when noise modeling is not used, the summation in Eq. (24) runs from $c=1$ to $C$ (rather than $C+1$), reducing to a modification of (7) instead of (21).

### IV-G Inference of CTRnet

At inference time, we use $\hat{Z}(c)$ as the estimate of the close-talk speech for each speaker $c$. We just need to run feed-forwarding once to obtain all the estimates. All the FCP filtering operations are not needed at inference time.

We emphasize that speaker-activity timestamps are only needed for model training and not needed for inference.

## V Cross-Talk Reduction for Separation

This section describes how the estimated close-talk speech produced by CTRnet is leveraged to train far-field speech separation models. In our framework shown in Fig. 2, CTRnet is trained first as described in Section IV. Once trained, it is applied to all real-recorded close-talk mixtures in the training set to produce close-talk speech estimates, which are then used as fixed pseudo-labels for training PuLSS. The CTRnet parameters are not updated during PuLSS training.

This section describes PuLSS. See Fig. 5 for an illustration.

![Refer to caption](figures/fig5.png)

Figure 5: Illustration of PuLSS. Best viewed in color.

### V-A Deriving Pseudo-Labels Based on Close-Talk Estimates

With each close-talk estimate, we compute the speakerâ€™s image (ideally, direct-path signal) at a reference far-field microphone by estimating the RTF relating the speaker source signal to its image, and use the computed speaker image as the pseudo-target speech for the far-field mixture. In detail, we first estimate the RTF $\hat{\mathbf{h}}_{q}(c,f)\in{\mathbb{C}}^{L}$ using FCP [^47]:

$$
\displaystyle\hat{\mathbf{h}}_{q}(c,f)=\underset{\mathbf{h}_{q}(c,f)}{\text{argmin}}\sum\limits_{t}\frac{\Big|Y_{q}(t,f)-\mathbf{h}_{q}(c,f)^{{\mathsf{H}}}\ \breve{\hat{\mathbf{Z}}}(c,t+\hat{K},f)\Big|^{2}}{\lambda_{q}(c,t,f)},
$$

where $q\in\{1,\dots,P\}$ denotes a reference far-field microphone, $\breve{\hat{\mathbf{Z}}}(c,t,f)=[\hat{Z}(c,t-L+1,f),\dots,\hat{Z}(c,t,f)]^{\mathsf{T}}\in{\mathbb{C}}^{L}$ stacks a short window of $L$ T-F units in estimated close-talk speech, and $L$ is tuned to a small value (in this study $2$) to encourage $\mathbf{h}_{q}(c,f)$ to approximate the RTF of the direct-path signal. In $\breve{\hat{\mathbf{Z}}}(c,t+\hat{K},f)$, $\hat{K}$ is an estimated time delay (in frames) accounting for time-synchronization issues between close-talk and far-field microphones. In our study, $\hat{K}$ is estimated via enumeration by solving the problem below:

$$
\displaystyle\hat{K}=\underset{K\in\Psi}{\text{argmin}}\Big(\underset{\mathbf{h}_{q}(c,\cdot)}{\text{min}}\sum\limits_{t,f}\frac{\Big|Y_{q}(t,f)-\mathbf{h}_{q}(c,f)^{{\mathsf{H}}}\ \breve{\hat{\mathbf{Z}}}(c,t+K,f)\Big|^{2}}{\lambda_{q}(c,t,f)}\Big),
$$

where $\Psi=\{-E,\dots,0,\dots,E\}$ is a discrete set of hypothesized time delays (in frames), with $E$ (tuned to $9$ in this study) denoting the maximum hypothesized delay. Since the filter tap is assumed small, the computation of Eq. (26) is fast.

With the estimated RTF, we compute the pseudo-label of speaker $c$ at the reference far-field microphone $q$ as follows:

$$
\displaystyle S_{q}^{\text{PL}}(c,t,f)=\hat{\mathbf{h}}_{q}(c,f)^{{\mathsf{H}}}\ \breve{\hat{\mathbf{Z}}}(c,t+\hat{K},f),
$$

where the superscript â€œPLâ€?means pseudo-label.

### V-B Using Pseudo-Labels for Training Far-Field Models

With the pseudo-labels, we can train supervised models directly on far-field mixtures to realize far-field speech separation. For speaker separation, we need to resolve the permutation problem [^49]. A common method is permutation invariant training (PIT) [^49], but it only resolves permutations within each processing block. For long-form audio, continuous speech separation [^33] processes overlapping blocks and stitches them along time, but it introduces a cross-block permutation problem that requires additional speaker reconciliation via, e.g., speaker embeddings and clustering [^50]. To avoid this complexity, we resolve the permutation problem by conditioning the separation model on speaker-activity timestamps. This is conceptually similar to how GSS [^31] leverages speaker-activity timestamps to guide its spatial clustering, albeit here within an end-to-end DNN framework.

We assume that, at training time, the timestamps of all speakers (i.e., $\{D(c)\}_{c=1}^{C}$) are available, and use them to compute masked mixture magnitude spectrograms $\{D(c)\otimes|Y_{q}|\}_{c=1}^{C}$, with $\otimes$ denoting point-wise multiplication, as additional input features (see Fig. 5). These $C$ masked spectrograms are concatenated with the mixture real and imaginary (RI) components and fed to the DNN, which produces $C$ separated outputs $\{\hat{S}_{q}(c)\}_{c=1}^{C}$ in a single forward pass. This assigns each output channel to a specific speaker, removing permutation ambiguity across blocks. Based on $\mathcal{G}(\cdot,\cdot)$ defined in Eq. (9), the loss function is defined as follows:

$$
\displaystyle\mathcal{L}_{\text{PL}}=\sum_{c=1}^{C}\frac{\sum_{t,f}\mathcal{G}\Big(\hat{S}_{q}(c,t,f),S_{q}^{\text{PL}}(c,t,f)\Big)}{\sum_{t,f}|Y_{q}(t,f)|^{\alpha}}.
$$

Although at training time we use oracle speaker-activity timestamps to compute input features, at inference time we can use timestamps estimated by a speaker diarization model to compute the features. See later Section V-E for the details.

### V-C Directly using Close-Talk Estimates for Training

The pseudo-labels $S_{q}^{\text{PL}}$ produced via Eq. (27), due to the linear filtering, often have a lower quality than $\hat{Z}$, possibly limiting the performance of far-field separation. To deal with this, besides using the $\mathcal{L}_{\text{PL}}$ loss in Eq. (28) for training, we linearly filter the DNN estimates to approximate close-talk speech estimated by CTRnet and compute an additional loss:

$$
\displaystyle\mathcal{L}_{\text{CTE}}=\sum_{c=1}^{C}\frac{\sum_{t,f}\mathcal{G}\Big(\hat{Z}(c,t+\hat{K},f),\hat{\mathbf{o}}(c,f)^{\mathsf{H}}\grave{\hat{\mathbf{S}}}_{q}(c,t,f)\Big)}{\sum_{t,f}|Y_{d(=c)}(t,f)|^{\alpha}},
$$

where $\hat{Z}(c)$ denotes the estimated close-talk speech of speaker $c$, $\hat{K}$ is computed via Eq. (26) to account for time-synchronization issues, and $\grave{\hat{\mathbf{S}}}_{q}(c,t,f)=[\hat{S}_{q}(c,t-A,f),\dots,\hat{S}_{q}(c,t,f),\dots,\hat{S}_{q}(c,t+A,f)]^{\mathsf{T}}\in{\mathbb{C}}^{A+1+A}$ stacks a short window of $A+1+A$ T-F units. The linear filter $\hat{\mathbf{o}}(c,f)\in{\mathbb{C}}^{A+1+A}$ is computed by FCP as follows:

$$
\displaystyle\hat{\mathbf{o}}(c,f)=\underset{\mathbf{o}(c,f)}{\text{argmin}}\sum\limits_{t}\frac{\Big|\hat{Z}(c,t+\hat{K},f)-\mathbf{o}(c,f)^{{\mathsf{H}}}\ \grave{\hat{\mathbf{S}}}_{q}(c,t,f)\Big|^{2}}{\hat{\eta}(c,t+\hat{K},f)},
$$

where $\hat{\eta}(c)$ is defined by replacing $Y_{m}$ in (12) with $\hat{Z}(c)$.

We combine the above loss functions for model training:

$$
\displaystyle\mathcal{L}_{\text{PL+CTE}}=\mathcal{L}_{\text{PL}}+\delta\times\mathcal{L}_{\text{CTE}},
$$

where $\delta\in{\mathbb{R}}_{>0}$ is a tunable weighting term. Note that if $\mathcal{L}_{\text{CTE}}$ is used alone for training, the DNN estimates would have a random gain level, as the linear filter in Eq. (29) can compensate for any gain levels in the DNN estimate. We hence need $\mathcal{L}_{\text{PL}}$, which can penalize inaccurate gain estimation.

### V-D Training PuLSS on Simulated and Real Mixtures

Similarly to CTRnet, we can also train PuLSS by additionally including simulated mixtures. If the input mixture is real-recorded, we use pseudo-label as the training target, while, if it is simulated, we use clean speech as the training target. The loss for simulated mixtures can be defined as

$$
\displaystyle\mathcal{L}_{\text{sup}}^{\text{PuLSS}}=\sum_{c=1}^{C}\frac{\sum_{t,f}\mathcal{G}\Big(\hat{S}_{q}(c,t,f),S_{q}(c,t,f)\Big)}{\sum_{t,f}|Y_{q}(t,f)|^{\alpha}},
$$

where $S_{q}(c)$ is the direct-path signal of speaker $c$ at the reference microphone $q$. The overall loss is defined, similarly to Eq. (18) and by using a tunable weighting term $\kappa_{2}$, as

$$
\mathcal{L}_{\text{sup,PL+CTE}}^{\text{PuLSS}}=\left\{\begin{aligned} &\kappa_{2}\times\mathcal{L}_{\text{sup}}^{\text{PuLSS}},\text{if input mixture is simulated};\\
&\mathcal{L}_{\text{PL+CTE}},\text{if input mixture is real-recorded}.\end{aligned}\right.
$$

### V-E Inference of PuLSS

At inference time, depending on the application scenarios, we have two setups. The first one assumes that oracle speaker-activity timestamps are available (i.e., oracle speaker diarization) and fed to the trained model to predict target speech. The second one estimates the speaker-activity timestamps via a speaker diarization model, and feeds the estimated timestamps directly to the trained model to predict target speech.

At inference time, we use $\hat{S}_{q}(c)$ as the separated speech for each speaker $c$. We run feed-forwarding once to obtain all the $C$ estimates. All the FCP filtering operations are not needed.

## VI Experimental Setup

Our experiments aim at verifying whether CTRnet can accurately estimate close-talk speech and whether the estimated close-talk speech can serve as a good pseudo-label for real mixtures and help us develop better far-field speech separation models. This section first introduces the CHiME-6 dataset [^51] designed for conversational speech separation and recognition. Next, we describe our data simulation procedure for supervised training. We then provide details on the evaluation metrics, miscellaneous configurations, and baseline systems.

### VI-A CHiME-6 Dataset

The CHiME-6 dataset [^51] consists of real-recorded conversational sessions, each captured in a different house. Each session has $4$ speakers talking spontaneously for $120$ â€?$150$ minutes. Each speaker wears a binaural close-talk microphone to record their close-talk speech. In some segments, close-talk recordings are missing due to the speaker removing the microphone or hardware malfunction. The close-talk mixtures contain severe cross-talk, since the speakers are typically close to one another while talking. Far-field mixture signals are captured by $6$ Kinect devices (each with $4$ microphones) distributed across the living room, kitchen, and dining room ($2$ devices per room), with speakers free to move between rooms. Realistic noises that are typical in dinner-party scenarios are recorded at the same time along with speech. The task is to recognize each speakerâ€™s speech from the far-field mixtures and to output $4$ transcriptions (one per speaker), which requires accurate speaker diarization. The sampling rate is $16$ kHz.

Our choice of CHiME-6 is dictated by the fact that it is a notoriously-difficult benchmark, primarily because its real-recorded signals are highly representative of the issues a deployed system must handle, such as microphone synchronization errors, signal clipping, frame dropping, microphone failures, moving speakers, time-varying speaker overlap ratios, and realistic environmental noises. Among the scenarios featured in the recent CHiME-{7,8} DASR challenges [^52] [^53] [^11], CHiME-6 is the most challenging. More broadly, unlike datasets in office-meeting scenarios such as NOTSOFAR-1 [^34], AMI [^13] and AliMeeting [^14] which feature more structured conversations in acoustically controlled environments, CHiME-6 captures fully unconstrained dinner-party speech in real domestic settings, making it a perfect example of conversational speech in the wild. As noted in Section II-A, the most successful speech separation algorithm on this dataset to date remains GSS [^31], a signal-processing method, with all the top teams in the CHiME-{7,8} challenges adopting GSS as their only speech separation module [^54] [^55] [^52] [^11].

The official CHiME-6 dataset [^51] consists of $16/2/2$ sessions ($\sim$ $34/2/5$ hours) respectively in its training, validation and test sets. We adopt this session partition but, to make our results directly comparable with the challenge submissions to the CHiME-{7,8} DASR challenges [^52] [^53], we omit from training the two sessions that CHiME-7 DASR reassigned to its test set, resulting in only $14$ training sessions. In our setup, the validation and test sets remain unchanged from CHiME-6 and same as the CHiME-8 DASR challenge, allowing direct comparison with all challenge submissions across the CHiME-{6,7,8} DASR challenges.

### VI-B Dealing with Long-Form Mixtures

In CHiME-6, as mentioned each session is long, lasting $120$ to $150$ minutes. This is typical in conversational datasets. We simply cannot feed-forward the entire signal of each session for training and inference.

For the training of CTRnet and PuLSS, we cut each session to $12$ -second blocks with $11$ -second overlap between consecutive blocks (i.e., extracting a $12$ -second block every $1$ second), resulting in $123,339$ blocks ($\sim$ $411$ hours) for model training.

For the inference of CTRnet and PuLSS, we apply the trained models block-wise to process each session, and stitch the processing results along time. See Fig. 6 for an illustration. Each block has a total length of $W=W_{\text{ctx}}+W_{\text{out}}+W_{\text{ctx}}$, consisting of $W_{\text{ctx}}$ of context on each side, and $W_{\text{out}}$ of center output. In this study, we set $W_{\text{ctx}}$ and $W_{\text{out}}$ to $4$ seconds, resulting in $W=12$ -second blocks. Only the DNN predictions in the center $W_{\text{out}}$ seconds are retained. Consecutive blocks are shifted by $W_{\text{out}}$.

![Refer to caption](figures/fig6.png)

Figure 6: Illustration of block-wise inference.

### VI-C Dealing with Binaural Close-Talk Microphones in CTRnet

The close-talk mixtures in CHiME-6 are recorded by binaural microphones, meaning that each speaker has two close-talk microphones rather than one. To address this, we investigate two strategies. Binaural Strategy #1 considers the right-ear microphones as close-talk microphone while the left-ear one as far-field, resulting in $P+C$ far-field microphones and still $C$ close-talk microphones. Binaural Strategy #2 averages the left- and right-ear mixtures and considers their average as the close-talk mixture, leading to $C$ close-talk and $P$ far-field mixtures. The rationale is that the wearerâ€™s mouth is approximately in the front direction of the two binaural microphones, and simply averaging the two channels is akin to delay-and-sum beamforming, which can boost the SNR of close-talk speech, potentially improving cross-talk reduction.

### VI-D Dealing with Distributed Far-Field Microphone Arrays

In CHiME-6, the devices used for recording far-field mixture signals are multiple Kinect devices, placed in a distributed manner in a random device geometry (but each Kinect device has the same, fixed microphone geometry). In this case, we need to modify our algorithms for training CTRnet and PuLSS.

For CTRnet, we can use all the far-field microphones to compute the MC loss for model training. This could lead to better cross-talk reduction, as more mixture constraints, afforded by the distributed microphone arrays, can be used for training. The FCP filters can be configured long to cover the relative time delays of each speaker at different microphones.

For PuLSS, we can stack all the $24$ far-field microphone signals as input to train a DNN to predict the pseudo-target speech at a reference microphone of all the $24$ microphones. We tried this idea but did not succeed, possibly because in CHiME-6 different speakers exhibit significantly different time delays and energy levels at different arrays. We hence use an alternative, where we only use the signals recorded by each microphone array as input (i.e., $4$ -channel) to train a DNN to predict the pseudo-target speech at a designated reference microphone of the array. At run time, we apply the DNN to process the entire session recorded by each array. After that, we estimate the SNR of each speech segment (identified by oracle or estimated speaker-activity timestamps) of each speaker at each array based on the predicted signal and the mixture in the identified segment, and select the predicted signal with the highest estimated SNR as the estimate of that speaker in the identified segment.

### VI-E Training Segment Sampling Based on Overlap Ratio

For real-recorded conversations, speaker overlap ratio varies with time, as people tend to stay silent while the others are speaking and it is not common to have many speakers talking at the same time. See Fig. 4 for an illustration. This implicitly creates a data imbalance issue for training models on real data, as there are many more training blocks with low speaker overlap ratio than high overlap. The resulting trained models could have limited capability at separating mixtures with high speaker overlap ratio.

To deal with this, we design a weighted sampling strategy, where the more speaker overlap ratio a training block has, the more likely it is selected for model training. The weight for training block $i$ is defined as follows:

$$
\displaystyle w^{(i)}=1+\theta\times\frac{1}{T}\sum_{t=1}^{T}\Big(\max\big(1,\sum_{c=1}^{C}D^{(i)}(c,t)\big)-1\Big),
$$

where $\sum_{c=1}^{C}D^{(i)}(c,t)$ is the number of active speakers at frame $t$, $T$ the number of frames in the block, and $\theta\in{\mathbb{R}}_{\geq 0}$ a tunable hyper-parameter. When there is no speaker overlap, $w^{(i)}=1$, and when every frame has $C$ speakers, $w^{(i)}=1+\theta\times(C-1)$, where $\theta$ controls the sampling weight.

### VI-F Miscellaneous Configurations for CTRnet and PuLSS

TF-GridNet [^7] is used as the DNN architecture for CTRnet and PuLSS, as it has shown strong performance in many speech separation benchmarks. We adopt two configurations, denoted as V1 and V2, specified using the notation of [^7]. The V1 model sets $D=100$, $B=4$, $I=2$, $J=2$, $H=200$, $L=4$ and $E=8$, while V2 changes $D=128$, $B=6$, $I=1$ and $J=1$. The V1 model uses $\sim$ $1/3$ the computation of V2, supporting fast experimentation for ablation studies. Note that the symbols above refer to TF-GridNet hyper-parameters and are distinct from the identically-named variables in Table I.

Both CTRnet and PuLSS are trained via complex spectral mapping [^56], which predicts the real and imaginary (RI) components of target signals based on the RI components of input mixture signals. For PuLSS, we include the mixture magnitude masked by speaker-activity timestamps as additional input features (see Fig. 5) to avoid PIT as explained in Section V-B.

For STFT, the window and hop sizes are respectively set to $16$ and $8$ ms for CTRnet, and to $32$ and $16$ ms for PuLSS. The square root of Hann window is used as the analysis window.

We use Adam as the optimizer to train PuLSS and CTRnet. Each epoch randomly samples $5\%$ of the training blocks. When both simulated and real blocks are used for training, they have the same probabilities of being sampled. The mini-batch size is $2$. The learning rate starts from $10^{-3}$ and is halved if the validation loss is not improved in $2$ epochs. We stop training when the learning rate is reduced to $6.25\times 10^{-5}$. The $L_{2}$ norm for gradient clipping is set to $1.0$.

All the hyper-parameters listed in Table I are tuned based on the CHiME-6 validation set.

### VI-G Data Simulation for Supervised Training

CTRnet and PuLSS can be trained by using simulated mixtures in addition to real-recorded mixtures. This subsection describes the method for data simulation.

For each real-recorded segment extracted from the CHiME-6 sessions for model training, we simulate a signal which is also $12$ -second long. It is synthesized by following the speaker-overlap patterns of the real-recorded segment. In detail, given a $12$ -second speaker-activity timestamp of each speaker (i.e., a zero-one vector), we first identify time ranges where the values are all ones (indicating active speech). Next, we sample a speaker from clean speech databases including LibriSpeech [^57] and EARS [^58], and place, in each of the identified time ranges, a sampled active speech segment of the speaker (that is shorter than the identified time range). The active speech segments of each speaker are pre-identified by using the Pyannote voice activity detection model <sup>4</sup>, and pre-normalized to a sample variance of $1.0$. We then scale each of the four $12$ -second clean speech signals such that their energy level is sampled from the range $[-9,9]$ dB. Based on the Pyroomacoustics toolkit, the clean speech signals and up to $4$ noises sources sampled from the FSD50K dataset [^59] and the pure noise signals in the CHiME-6 training data are placed in different locations in a simulated room (with reverberation time sampled from the range $[0.2,0.7]$ s) to simulate noisy-reverberant far-field mixtures captured by a $4$ -channel far-field microphone array, which is simulated based on the microphone-array geometry of the Kinect device. The speech and noise signals are scaled such that the energy level between the summation of direct-path speech signals and that of reverberant noise signals equals a value sampled from the range $[-20,20]$ dB. Besides simulating far-field mixtures, for each speaker, we place a close-talk microphone to the speaker at a distance sampled from the range $[0.2,0.5]$ m to simulate close-talk mixture. For both far-field and close-talk mixtures, a weak air-conditioning noise sampled from the REVERB dataset [^60] is added. In total, there are $123,339$ $12$ -second blocks ($\sim$ $411$ hours) simulated to train CTRnet and PuLSS.

### VI-H Evaluation Metrics

The separated signal of each speaker, obtained via block-wise inference shown in Fig. 6, has the same length as the input session. Based on oracle or estimated speaker-activity timestamps, it is split into short utterances and then decoded by an ASR model. We evaluate performance using two metrics from the CHiME-{7,8} DASR challenges [^52] [^53] [^11], which are suitable for multi-talker ASR evaluation. When oracle diarization is used, we report the concatenated minimum permutation word error rate (cpWER) [^51] following the challenge protocol. This enables direct comparison with all submissions to the CHiME-7 challenge, which has a track that assumes oracle diarization [^11]. When estimated diarization is used, we report time-constrained cpWER (tcpWER) [^61], which extends cpWER by time-aligning hypothesis words to reference speaker segments before scoring, so that segmentation errors also incur in insertion or deletion penalties. We follow the scoring protocol (including the text normalization) of the CHiME-{7,8} DASR challenges summary paper [^11]. This allows a direct comparison of our results with previous challenge submissions.

### VI-I ASR Models

We evaluate our systems using two ASR models with different capability. The first one, denoted as Default, is the ASR baseline provided by the CHiME-{7,8} challenge organizers [^52] <sup>5</sup>. It is an end-to-end encoder-decoder transformer model with hybrid CTC/attention based on a WavLM encoder. Its training data includes the close-talk and far-field mixtures of CHiME-6, and far-field mixtures enhanced by GSS. See Section 5.3 of [^52] for more details. Note that the default ASR model favors GSS, as it utilizes GSS-enhanced signals for training. This matters for our comparisons, since off-the-shelf ASR models trained without exposure to a separation frontendâ€™s output distribution often fail to benefit from it [^20] [^12]. The second one, denoted as Fine-tuned Parakeet, is based on the Parakeet-TDT-0.6B-v3 model [^62], a $600$ M-parameter FastConformer model with a token-and-duration transducer decoder, pre-trained on ${\sim}1.7$ million hours of speech data. We choose Parakeet-v3, as it is a representative state-of-the-art open English ASR model. Its large-scale pre-training provides a strong starting point that is largely complementary to the dinner-party acoustic conditions of CHiME-6. We fine-tune it on a combination of three data sources from the CHiME-6 training set: PuLSS-enhanced far-field mixtures, CTRnet-enhanced close-talk mixtures, and the original close-talk mixtures. For all the three sources, oracle diarization is used to obtain segment boundaries. Fine-tuning is performed using the NeMo toolkit [^63], with full fine-tuning of the encoder, decoder, joint network, and duration head. We use the AdamW optimizer with a learning rate of $5\times 10^{-5}$, a cosine annealing schedule with $5{,}000$ warm-up steps, and a weight decay of $10^{-3}$. We train for $20$ epochs and select the best checkpoint based on the validation WER. Hyper-parameters are tuned based on the CHiME-6 validation set using PuLSS-enhanced far-field signals with oracle diarization as input.

### VI-J Baseline Systems

We mainly consider two baseline approaches. One is supervised speech separation [^3], where DNN models are trained on simulated data. Based on the data simulated in Section VI-G, our supervised models are trained by penalizing the DNN estimates only using the $\mathcal{L}_{\text{sup,speech}}^{\text{CTRnet}}$ loss for CTRnet and $\mathcal{L}_{\text{sup}}^{\text{PuLSS}}$ for PuLSS. The other one is GSS [^31], a signal processing method. We use the GSS implementation provided in the CHiME-7 DASR challenge <sup>6</sup>. It first performs multi-channel speech dereverberation using the weighted prediction error algorithm, and then computes a T-F mask-based minimum variance distortionless response beamformer for speech separation by using posterior T-F masks estimated by a spatial clustering module guided by speaker-activity timestamps provided by oracle or estimated speaker diarization [^31]. We emphasize that, so far, almost all the systems in public ASR challenges leverage GSS as the only module for speech separation [^11]. Meanwhile, as CHiME-6 is a public dataset used in the CHiME-{6,7,8} challenges, which attracted broad participation, we can readily compare the results of our systems with many existing ones.

TABLE II: ASR Results of CTRnet on CHiME-6 Close-Talk Mixtures (Diarization: Oracle; ASR Model: Default; DNN: V1).

<table><tbody><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">cpWER (%) <math><semantics><mo>â†?/mo> <annotation>\downarrow</annotation></semantics></math></td></tr><tr><td>ID</td><td>Systems</td><td>Binaural Strategy</td><td>#Far-field mics (<math><semantics><mi>P</mi> <annotation>P</annotation></semantics></math>)</td><td>Mag. compress. factor (<math><semantics><mi>Î±</mi> <annotation>\alpha</annotation></semantics></math>)</td><td>Weight for <math><semantics><msub><mi>â„?/mi> <mtext>SA</mtext></msub> <annotation>\mathcal{L}_{\text{SA}}</annotation></semantics></math> (<math><semantics><mi>Î²</mi> <annotation>\beta</annotation></semantics></math>)</td><td>FCP denomin.</td><td>#DNN estimates</td><td>Reverb modeling (<math><semantics><mi>Î”</mi> <annotation>\Delta</annotation></semantics></math>)</td><td>Sampling (<math><semantics><mi>Î¸</mi> <annotation>\theta</annotation></semantics></math>)</td><td>Noise modeling</td><td>Val.</td><td>Test</td></tr><tr><td>0</td><td>Unprocessed mixture</td><td>#1</td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>28.42</mn> <annotation>28.42</annotation></semantics></math></td><td><math><semantics><mn>29.3902</mn> <annotation>29.3902</annotation></semantics></math></td></tr><tr><td>1a</td><td>GSS (<math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math> -channel) <sup><a href="#fn:31">31</a></sup></td><td>#1</td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>30.3918</mn> <annotation>30.3918</annotation></semantics></math></td><td><math><semantics><mn>32.6024</mn> <annotation>32.6024</annotation></semantics></math></td></tr><tr><td>1b</td><td>GSS (<math><semantics><mn>8</mn> <annotation>8</annotation></semantics></math> -channel) <sup><a href="#fn:31">31</a></sup></td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>26.2241</mn> <annotation>26.2241</annotation></semantics></math></td><td><math><semantics><mn>28.2457</mn> <annotation>28.2457</annotation></semantics></math></td></tr><tr><td>2</td><td>Supervised CTRnet</td><td>#1</td><td>â€?/td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>4</td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>30.3595</mn> <annotation>30.3595</annotation></semantics></math></td><td><math><semantics><mn>37.8931</mn> <annotation>37.8931</annotation></semantics></math></td></tr><tr><td>3a</td><td>Unsupervised CTRnet</td><td>#1</td><td><math><semantics><mrow><mrow><mn>0</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <mo>+</mo> <mn>4</mn></mrow> <annotation>0\times 4+4</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td>â€?/td><td>(12)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>79.9664</mn> <annotation>79.9664</annotation></semantics></math></td><td><math><semantics><mn>76.9253</mn> <annotation>76.9253</annotation></semantics></math></td></tr><tr><td>3b</td><td>Unsupervised CTRnet</td><td>#1</td><td><math><semantics><mrow><mrow><mn>1</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <mo>+</mo> <mn>4</mn></mrow> <annotation>1\times 4+4</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td>â€?/td><td>(12)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>81.9534</mn> <annotation>81.9534</annotation></semantics></math></td><td><math><semantics><mn>79.6804</mn> <annotation>79.6804</annotation></semantics></math></td></tr><tr><td>3c</td><td>Unsupervised CTRnet</td><td>#1</td><td><math><semantics><mrow><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <mo>+</mo> <mn>4</mn></mrow> <annotation>6\times 4+4</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td>â€?/td><td>(12)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>21.8305</mn> <annotation>21.8305</annotation></semantics></math></td><td><math><semantics><mn>25.5868</mn> <annotation>25.5868</annotation></semantics></math></td></tr><tr><td>4a</td><td>Weakly-supervised CTRnet</td><td>#1</td><td><math><semantics><mrow><mrow><mn>0</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <mo>+</mo> <mn>4</mn></mrow> <annotation>0\times 4+4</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td>(12)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>21.3363</mn> <annotation>21.3363</annotation></semantics></math></td><td><math><semantics><mn>24.8268</mn> <annotation>24.8268</annotation></semantics></math></td></tr><tr><td>4b</td><td>Weakly-supervised CTRnet</td><td>#1</td><td><math><semantics><mrow><mrow><mn>1</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <mo>+</mo> <mn>4</mn></mrow> <annotation>1\times 4+4</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td>(12)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>21.3634</mn> <annotation>21.3634</annotation></semantics></math></td><td><math><semantics><mn>24.6001</mn> <annotation>24.6001</annotation></semantics></math></td></tr><tr><td>4c</td><td>Weakly-supervised CTRnet</td><td>#1</td><td><math><semantics><mrow><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <mo>+</mo> <mn>4</mn></mrow> <annotation>6\times 4+4</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td>(12)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>21.7914</mn> <annotation>21.7914</annotation></semantics></math></td><td><math><semantics><mn>24.99</mn> <annotation>24.99</annotation></semantics></math></td></tr><tr><td>5</td><td>Weakly-supervised CTRnet</td><td>#2</td><td><math><semantics><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <annotation>6\times 4</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td>(12)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>20.4803</mn> <annotation>20.4803</annotation></semantics></math></td><td><math><semantics><mn>23.3069</mn> <annotation>23.3069</annotation></semantics></math></td></tr><tr><td>6a</td><td>Semi-supervised CTRnet</td><td>#2</td><td><math><semantics><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <annotation>6\times 4</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td>(12)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>20.0472</mn> <annotation>20.0472</annotation></semantics></math></td><td><math><semantics><mn>22.4798</mn> <annotation>22.4798</annotation></semantics></math></td></tr><tr><td>6b</td><td>Semi-supervised CTRnet</td><td>#2</td><td><math><semantics><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <annotation>6\times 4</annotation></semantics></math></td><td><math><semantics><mn>1.0</mn> <annotation>1.0</annotation></semantics></math></td><td><math><semantics><mn>0.1</mn> <annotation>0.1</annotation></semantics></math></td><td>(12)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>19.8774</mn> <annotation>19.8774</annotation></semantics></math></td><td><math><semantics><mn>22.2277</mn> <annotation>22.2277</annotation></semantics></math></td></tr><tr><td>6c</td><td>Semi-supervised CTRnet</td><td>#2</td><td><math><semantics><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <annotation>6\times 4</annotation></semantics></math></td><td><math><semantics><mn>0.3</mn> <annotation>0.3</annotation></semantics></math></td><td><math><semantics><mn>0.1</mn> <annotation>0.1</annotation></semantics></math></td><td>(12)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>19.8417</mn> <annotation>19.8417</annotation></semantics></math></td><td><math><semantics><mn>22.3764</mn> <annotation>22.3764</annotation></semantics></math></td></tr><tr><td>6d</td><td>Semi-supervised CTRnet</td><td>#2</td><td><math><semantics><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <annotation>6\times 4</annotation></semantics></math></td><td><math><semantics><mn>0.3</mn> <annotation>0.3</annotation></semantics></math></td><td><math><semantics><mn>0.1</mn> <annotation>0.1</annotation></semantics></math></td><td>(13)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td>â€?/td><td><math><semantics><mn>19.643</mn> <annotation>19.643</annotation></semantics></math></td><td><math><semantics><mn>22.0009</mn> <annotation>22.0009</annotation></semantics></math></td></tr><tr><td>7</td><td>Semi-supervised CTRnet</td><td>#2</td><td><math><semantics><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <annotation>6\times 4</annotation></semantics></math></td><td><math><semantics><mn>0.3</mn> <annotation>0.3</annotation></semantics></math></td><td><math><semantics><mn>0.1</mn> <annotation>0.1</annotation></semantics></math></td><td>(13)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td><math><semantics><mn>3</mn> <annotation>3</annotation></semantics></math></td><td>â€?/td><td>â€?/td><td><math><semantics><mn>19.4919</mn> <annotation>19.4919</annotation></semantics></math></td><td><math><semantics><mn>22.0354</mn> <annotation>22.0354</annotation></semantics></math></td></tr><tr><td>8</td><td>Semi-supervised CTRnet</td><td>#2</td><td><math><semantics><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <annotation>6\times 4</annotation></semantics></math></td><td><math><semantics><mn>0.3</mn> <annotation>0.3</annotation></semantics></math></td><td><math><semantics><mn>0.1</mn> <annotation>0.1</annotation></semantics></math></td><td>(13)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td>â€?/td><td><math><semantics><mn>20</mn> <annotation>20</annotation></semantics></math></td><td>â€?/td><td><math><semantics><mn>19.4528</mn> <annotation>19.4528</annotation></semantics></math></td><td><math><semantics><mn>21.9084</mn> <annotation>21.9084</annotation></semantics></math></td></tr><tr><td>9</td><td>Semi-supervised CTRnet</td><td>#2</td><td><math><semantics><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <annotation>6\times 4</annotation></semantics></math></td><td><math><semantics><mn>0.3</mn> <annotation>0.3</annotation></semantics></math></td><td><math><semantics><mn>0.1</mn> <annotation>0.1</annotation></semantics></math></td><td>(13)</td><td><math><semantics><mn>4</mn> <annotation>4</annotation></semantics></math></td><td><math><semantics><mn>3</mn> <annotation>3</annotation></semantics></math></td><td><math><semantics><mn>20</mn> <annotation>20</annotation></semantics></math></td><td>â€?/td><td><math><semantics><mn>19.5241</mn> <annotation>19.5241</annotation></semantics></math></td><td><math><semantics><mn>21.8323</mn> <annotation>21.8323</annotation></semantics></math></td></tr><tr><td>10a</td><td>Semi-supervised CTRnet</td><td>#2</td><td><math><semantics><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <annotation>6\times 4</annotation></semantics></math></td><td><math><semantics><mn>0.3</mn> <annotation>0.3</annotation></semantics></math></td><td><math><semantics><mn>0.1</mn> <annotation>0.1</annotation></semantics></math></td><td>(13)</td><td><math><semantics><mrow><mn>4</mn> <mo>+</mo> <mn>4</mn></mrow> <annotation>4+4</annotation></semantics></math></td><td><math><semantics><mn>3</mn> <annotation>3</annotation></semantics></math></td><td><math><semantics><mn>20</mn> <annotation>20</annotation></semantics></math></td><td>(20)</td><td><math><semantics><mn>19.5751</mn> <annotation>19.5751</annotation></semantics></math></td><td><math><semantics><mn>22.0608</mn> <annotation>22.0608</annotation></semantics></math></td></tr><tr><td>10b</td><td>Semi-supervised CTRnet</td><td>#2</td><td><math><semantics><mrow><mn>6</mn> <mo>Ã—</mo> <mn>4</mn></mrow> <annotation>6\times 4</annotation></semantics></math></td><td><math><semantics><mn>0.3</mn> <annotation>0.3</annotation></semantics></math></td><td><math><semantics><mn>0.1</mn> <annotation>0.1</annotation></semantics></math></td><td>(13)</td><td><math><semantics><mrow><mn>4</mn> <mo>+</mo> <mn>4</mn></mrow> <annotation>4+4</annotation></semantics></math></td><td><math><semantics><mn>3</mn> <annotation>3</annotation></semantics></math></td><td><math><semantics><mn>20</mn> <annotation>20</annotation></semantics></math></td><td>(23)</td><td><math><semantics><mn>19.5785</mn> <annotation>19.5785</annotation></semantics></math></td><td><math><semantics><mn>21.8722</mn> <annotation>21.8722</annotation></semantics></math></td></tr></tbody></table>

## VII Evaluation Results on Close-Talk Mixtures

Table II reports the evaluation results of CTRnet. The hyper-parameters for FCP filtering are tuned to $\xi=0.01$, and $I=13$ and $J=1$ (resulting in $15$ -tap filters). The weighting term used in $\mathcal{L}_{\text{MC+SA}}$ in Eq. (16) is tuned to $\beta=1.0$. Since there are $4$ speakers in each session, we set $C=4$, meaning that the number of input microphones to CTRnet is also $4$. The number of far-field microphones, $P$, is equal to $24$ ($=6\times 4$) in default, as there are $6$ Kinect devices, each with $4$ microphones, and all of them are used to compute the MC loss in default.

### VII-A Results of GSS and Supervised CTRnet

The results of unprocessed mixtures are shown in row $0$, where we use the right-ear close-talk mixture (i.e., Binaural Strategy #1) as the separation result for each speaker. The cpWER on the test set is $29.4\%$.

In row $1$ a, we use the right-ear close-talk mixtures to perform GSS, and in $1$ b, we use both the left- and right-ear close-talk mixture for GSS. Since there are $4$ speakers, we have $4$ input channels for $1$ a and $8$ ($=2\times 4$) for $1$ b. We observe that $8$ -channel GSS outperforms $4$ -channel GSS, but the improvement over unprocessed mixtures is small (i.e., from $29.4\%$ to $28.2\%$ cpWER). The small improvement could be because each speaker has very different SNRs at different close-talk microphones and in this case the target T-F masks at different close-talk microphones are significantly different.

Row $2$ reports the results of supervised CTRnet. Although the simulated training data covers a wide range of acoustic conditions, the trained model performs much worse than the unprocessed mixture ($37.9$ % vs. $29.4$ % cpWER). This is consistent with prior observations that supervised neural separation models trained on simulated data introduce artifacts and distortions that hurt downstream ASR when the backend has not been adapted to their output distribution [^8] [^20] [^12].

### VII-B Results of Un- and Weakly-Supervised CTRnet

Row $3$ a- $3$ c report the results of unsupervised CTRnet, which uses the right-ear close-talk mixtures as input and is trained solely on real-recorded mixtures. In $3$ a, the left-ear close-talk microphones are considered as the far-field microphones for loss computation, and therefore $P=4$. In $3$ b, we additionally include the first far-field microphone array for loss computation, resulting in $P=1\times 4+4$ far-field microphone signals for loss computation. In $3$ c, we include all the $6$ far-field microphone arrays for loss computation, leading to $P=6\times 4+4$ channels. We observe that the performance of unsupervised CTRnet heavily depends on the number of far-field microphones used for loss computation. In $3$ a and $3$ b, unsupervised CTRnet does not work, while in $3$ c, it works.

Row $4$ a- $4$ c report the results of weakly-supervised CTRnet, which is trained solely on real-recorded mixtures. Comparing them with $3$ a- $3$ c, we observe that, even if $P$ is small (e.g., $P=4$ in $4$ a), weakly-supervised CTRnet still works, and outperforms unsupervised CTRnet.

In row $5$, we switch to Binaural Strategy $\#2$, where we average each binaural close-talk mixture, and use the $4$ averaged signal as the input to CTRnet. In this case, $P$ equals $6\times 4$. This simple change leads to clear improvement over $4$ c (from $25.0\%$ to $23.3\%$ cpWER).

TABLE III: ASR Results of PuLSS on CHiME-6 Far-Field Mixtures (Diarization: Oracle).

<table><tbody><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">cpWER (%) <math><semantics><mo>â†?/mo> <annotation>\downarrow</annotation></semantics></math></td></tr><tr><td>ID</td><td>System</td><td>Loss function</td><td><math><semantics><mi>Î¸</mi> <annotation>\theta</annotation></semantics></math></td><td>Pseudo-label</td><td>DNN</td><td>ASR backend</td><td>Val.</td><td>Test</td></tr><tr><td>0</td><td>Mixture</td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>Default</td><td><math><semantics><mn>61.3543</mn> <annotation>61.3543</annotation></semantics></math></td><td><math><semantics><mn>62.6238</mn> <annotation>62.6238</annotation></semantics></math></td></tr><tr><td>1</td><td>GSS (24-channel) <sup><a href="#fn:31">31</a></sup></td><td>â€?/td><td>â€?/td><td>â€?/td><td>â€?/td><td>Default</td><td><math><semantics><mn>32.4128</mn> <annotation>32.4128</annotation></semantics></math></td><td><math><semantics><mn>38.5425</mn> <annotation>38.5425</annotation></semantics></math></td></tr><tr><td>2</td><td>Supervised</td><td><math><semantics><msubsup><mi>â„?/mi> <mtext>sup</mtext> <mtext>PuLSS</mtext></msubsup> <annotation>\mathcal{L}_{\text{sup}}^{\text{PuLSS}}</annotation></semantics></math> in (32)</td><td>â€?/td><td>ID <math><semantics><mn>9</mn> <annotation>9</annotation></semantics></math> of Table II</td><td>V1</td><td>Default</td><td><math><semantics><mn>42.5621</mn> <annotation>42.5621</annotation></semantics></math></td><td><math><semantics><mn>49.0369</mn> <annotation>49.0369</annotation></semantics></math></td></tr><tr><td>3a</td><td>PuLSS</td><td><math><semantics><msub><mi>â„?/mi> <mtext>PL</mtext></msub> <annotation>\mathcal{L}_{\text{PL}}</annotation></semantics></math> in (28)</td><td>â€?/td><td>ID <math><semantics><mn>9</mn> <annotation>9</annotation></semantics></math> of Table II</td><td>V1</td><td>Default</td><td><math><semantics><mn>31.4295</mn> <annotation>31.4295</annotation></semantics></math></td><td><math><semantics><mn>35.3647</mn> <annotation>35.3647</annotation></semantics></math></td></tr><tr><td>3b</td><td>PuLSS</td><td><math><semantics><msub><mi>â„?/mi> <mtext>PL+CTE</mtext></msub> <annotation>\mathcal{L}_{\text{PL+CTE}}</annotation></semantics></math> in (31)</td><td>â€?/td><td>ID <math><semantics><mn>9</mn> <annotation>9</annotation></semantics></math> of Table II</td><td>V1</td><td>Default</td><td><math><semantics><mn>28.9227</mn> <annotation>28.9227</annotation></semantics></math></td><td><math><semantics><mn>32.2179</mn> <annotation>32.2179</annotation></semantics></math></td></tr><tr><td>4a</td><td>PuLSS</td><td><math><semantics><msubsup><mi>â„?/mi> <mtext>sup,PL</mtext> <mtext>PuLSS</mtext></msubsup> <annotation>\mathcal{L}_{\text{sup,PL}}^{\text{PuLSS}}</annotation></semantics></math> in (33)</td><td>â€?/td><td>ID <math><semantics><mn>9</mn> <annotation>9</annotation></semantics></math> of Table II</td><td>V1</td><td>Default</td><td><math><semantics><mn>29.3015</mn> <annotation>29.3015</annotation></semantics></math></td><td><math><semantics><mn>33.6725</mn> <annotation>33.6725</annotation></semantics></math></td></tr><tr><td>4b</td><td>PuLSS</td><td><math><semantics><msubsup><mi>â„?/mi> <mtext>sup,PL+CTE</mtext> <mtext>PuLSS</mtext></msubsup> <annotation>\mathcal{L}_{\text{sup,PL+CTE}}^{\text{PuLSS}}</annotation></semantics></math> in (33)</td><td>â€?/td><td>ID <math><semantics><mn>9</mn> <annotation>9</annotation></semantics></math> of Table II</td><td>V1</td><td>Default</td><td><math><semantics><mn>27.5861</mn> <annotation>27.5861</annotation></semantics></math></td><td><math><semantics><mn>31.3019</mn> <annotation>31.3019</annotation></semantics></math></td></tr><tr><td>5</td><td>PuLSS</td><td><math><semantics><msubsup><mi>â„?/mi> <mtext>sup,PL+CTE</mtext> <mtext>PuLSS</mtext></msubsup> <annotation>\mathcal{L}_{\text{sup,PL+CTE}}^{\text{PuLSS}}</annotation></semantics></math> in (33)</td><td><math><semantics><mn>20</mn> <annotation>20</annotation></semantics></math></td><td>ID <math><semantics><mn>9</mn> <annotation>9</annotation></semantics></math> of Table II</td><td>V1</td><td>Default</td><td><math><semantics><mn>27.2838</mn> <annotation>27.2838</annotation></semantics></math></td><td><math><semantics><mn>31.0426</mn> <annotation>31.0426</annotation></semantics></math></td></tr><tr><td>6</td><td>PuLSS</td><td><math><semantics><msubsup><mi>â„?/mi> <mtext>sup,PL+CTE</mtext> <mtext>PuLSS</mtext></msubsup> <annotation>\mathcal{L}_{\text{sup,PL+CTE}}^{\text{PuLSS}}</annotation></semantics></math> in (33)</td><td><math><semantics><mn>20</mn> <annotation>20</annotation></semantics></math></td><td>ID <math><semantics><mn>10</mn> <annotation>10</annotation></semantics></math> b of Table II</td><td>V1</td><td>Default</td><td><math><semantics><mn>27.1735</mn> <annotation>27.1735</annotation></semantics></math></td><td><math><semantics><mn>30.912</mn> <annotation>30.912</annotation></semantics></math></td></tr><tr><td>7a</td><td>PuLSS</td><td><math><semantics><msubsup><mi>â„?/mi> <mtext>sup,PL+CTE</mtext> <mtext>PuLSS</mtext></msubsup> <annotation>\mathcal{L}_{\text{sup,PL+CTE}}^{\text{PuLSS}}</annotation></semantics></math> in (33)</td><td><math><semantics><mn>20</mn> <annotation>20</annotation></semantics></math></td><td>ID <math><semantics><mn>10</mn> <annotation>10</annotation></semantics></math> b of Table II</td><td>V2</td><td>Default</td><td><math><semantics><mn>26.6487</mn> <annotation>26.6487</annotation></semantics></math></td><td><math><semantics><mn>29.9652</mn> <annotation>29.9652</annotation></semantics></math></td></tr><tr><td>7b</td><td>PuLSS</td><td><math><semantics><msubsup><mi>â„?/mi> <mtext>sup,PL+CTE</mtext> <mtext>PuLSS</mtext></msubsup> <annotation>\mathcal{L}_{\text{sup,PL+CTE}}^{\text{PuLSS}}</annotation></semantics></math> in (33)</td><td><math><semantics><mn>20</mn> <annotation>20</annotation></semantics></math></td><td>ID <math><semantics><mn>10</mn> <annotation>10</annotation></semantics></math> b of Table II</td><td>V2</td><td>Fine-tuned Parakeet</td><td><math><semantics><mn>16.7</mn> <annotation>16.7</annotation></semantics></math></td><td><math><semantics><mn>19.5</mn> <annotation>19.5</annotation></semantics></math></td></tr></tbody></table>

### VII-C Results of Semi-Supervised CTRnet

Row $6$ a improves weakly-supervised CTRnet (in row $5$), which is trained solely on real-recorded mixtures, by including supervised training on simulated mixtures, leading to semi-supervised CTRnet. We set $\kappa_{1}$ in Eq. (18) to $1.0$. This change improves the performance from $23.3\%$ in row $5$ to $22.5\%$ cpWER in $6$ a. This improvement indicates the effectiveness of including supervised learning on simulated mixtures.

In row $6$ b, we tune $\beta$ from $1.0$ to $0.1$; in $6$ c, we tune $\alpha$ from $1.0$ to $0.3$; and in $6$ d, we change the FCP denominator from Eq. (12) to (13). Each change produces slight improvement on the validation set (i.e., from $20.0\%$ in $6$ a to $19.9\%$ in $6$ b, to $19.8\%$ in $6$ c, and to $19.6\%$ in $6$ d). The three changes combined produce clearly better cpWER on the test set (i.e., $22.0\%$ cpWER in $6$ d vs. $22.5\%$ cpWER in $6$ a).

Row $7$ reports the results of modeling reverberation in close-talk speech. We tune the prediction delay $\Delta$ based on the set of $\{1,2,3,4\}$. When it is tuned to $3$, on the validation set we obtain slightly better results over $6$ d (i.e., $19.5\%$ vs. $19.6\%$ cpWER), which does not dereverberate close-talk speech.

Row $8$ reports the results of using training segment sampling, where the sampling weight $\theta$ in Eq. (34) is tuned based on the set of $\{5,10,20,40,80\}$. Slightly better cpWER is observed when it is set to $20$ (i.e., $21.9\%$ in row $8$ vs. $22.0\%$ in $6$ d on the test set).

Row $9$ combines reverb modeling and training segment sampling, yielding better results at $21.8\%$ on the test set.

Row $10$ a and $10$ b report the results of including noise modeling in semi-supervised CTRnet, where the DNN is trained to additionally output $4$ noise estimates. Using Eq. (23) to combine the noises estimates works better than (20). Although informal listening tests suggest that the additional noise output can absorb some of the ambient noise, incorporating noise modeling does not improve cpWER. Nonetheless, as we will report later in Table III, CTRnet trained with noise modeling leads to a slightly better PuLSS model.

### VII-D Discussion

In Table II, we use the default ASR model, which is trained on unprocessed close-talk and far-field mixtures, and GSS-enhanced signals (see Section VI-I), so both unprocessed mixtures and GSS outputs are in-domain at inference, while CTRnet outputs are not. In addition, with oracle diarization providing per-speaker segment boundaries, the ASR can learn to implicitly attend to the centered speaker within each segment, which partly accounts for the strong performance of unprocessed mixtures and raises the bar for any separation frontend to be useful. Our weakly- and semi-supervised CTRnet variants outperform GSS (in row $1$ a and $1$ b) and unprocessed mixtures (in row $0$), indicating their effectiveness. In addition, they outperform supervised CTRnet (in row $2$), suggesting the benefits of training on real-recorded data.

## VIII Evaluation Results on Far-Field Mixtures

This section reports the evaluation results of PuLSS on far-field mixtures. $\delta$ in Eq. (31) is tuned to $20$, and $\kappa_{2}$ in (33) is set to $1.0$. The number of input channels to DNN is $4$, which equals the number of microphones in each Kinect device.

### VIII-A Results of GSS, Supervised, and PuLSS Approaches

Table III reports the results on far-field mixtures. In row $0$, the cpWER of unprocessed mixtures is $62.6\%$, which is quite large, indicating the difficulty of this task. It is obtained by directly using the first microphone of the first far-field array for ASR. For GSS, we use all the far-field microphone signals as input, which is $24$ -channel ($=6\times 4$). For the Supervised model, we use the supervised training setup in Fig. 5(b) for training, with all the other setup same as PuLSS. From rows $1$ and $2$, we observe that supervised PuLSS improves over the unprocessed mixture ($49.0\%$ vs. $62.6\%$ cpWER) but performs substantially worse than GSS ($38.5\%$ cpWER).

In comparison, for PuLSS models trained on the real-recorded mixtures using the pseudo-labels derived from the CTRnet in row $9$ of Table II, the results are clearly better. When using the $\mathcal{L}_{\text{PL}}$ loss in Eq. (28), we obtain $35.4\%$ cpWER in $3$ a. When using $\mathcal{L}_{\text{PL+CTE}}$ in (31) with $\delta$ tuned to $20$, we improve the cpWER to $32.2\%$ in $3$ b. Further including supervised learning on simulated mixtures based on the $\mathcal{L}_{\text{sup,PL+CTE}}^{\text{PuLSS}}$ loss in (33) improves cpWER to $31.3\%$ in $4$ b. In row $5$, further performing training segment sampling improves the performance from $31.3\%$ to $31.0\%$ cpWER. In row $6$, we switch to the CTRnet in row $10$ b of Table II, which performs noise modeling, to compute the pseudo-labels for training PuLSS. Slightly better cpWER is observed.

In row $7$ a, we switch the configuration of TF-GridNet from V1 to V2, which uses more computation. This improves PuLSS from $30.9\%$ to $30.0\%$ cpWER. The experiments so far are based on the default ASR model provided with the CHiME-7 DASR challenge. In $7$ b, we fine-tune the pre-trained Parakeet ASR model on the separated close-talk mixtures from CTRnet, separated far-field mixtures from PuLSS, and the original close-talk mixtures. Dramatic improvement is observed (from $30.0\%$ to $19.5\%$ cpWER). This gain comes from the ASR change alone, reflecting the inherently stronger pre-trained Parakeet backbone and its adaptation to the output distribution of our separation models. We use this ASR model in default in subsequent sections. For fair comparison, the GSS results reported in subsequent sections are obtained with the same Parakeet model fine-tuned identically as PuLSS but on GSS-enhanced signals instead, so that both PuLSS and GSS benefit from a matched degree of ASR adaptation.

### VIII-B Comparison with Existing Systems - Oracle Diarization

Table V compares the performance of PuLSS with existing approaches, all using oracle diarization at run time. Again, the results for GSS are obtained by fine-tuning the Parakeet-v3 model in the same way as for PuLSS, but using GSS-enhanced signals instead of PuLSS-enhanced ones. PuLSS achieves strong ASR performance at $19.5\%$ cpWER, slightly improving over the previous best ($19.8\%$ cpWER) obtained by the USTC system [^54], which uses an ensemble of multiple ASR models and iterative multi-stage decoding, with the first-pass ASR output used to refine speaker-activity timestamps for GSS. On the other hand, it significantly outperforms GSS ($19.5\%$ vs. $29.7\%$ cpWER on the test set).

From the gray rows in Table V, we observe that, when using oracle diarization, applying CTRnet can reduce the cpWER of close-talk mixtures from $19.5\%$ to $15.0\%$. This result indicates the effectiveness of CTRnet, and represents a performance upper bound for the downstream PuLSS models.

Note that the comparison between PuLSS and GSS isolates frontend quality and is a fair comparison, while the comparison of PuLSS with previous CHiME-{7,8} challenge submissions in Table V (and later Table V) are not similarly matched, as each challenge submission uses its own ASR backend, which is usually an ensemble of multiple models (see also [^11]) and is much more complicated than ours. The challenge-submission comparison is included to reflect overall system performance.

TABLE IV: ASR Results on CHiME-6 Far-Field Mixtures  
(Diarization: Oracle; ASR Model: Fine-Tuned Parakeet).

<table><tbody><tr><td></td><td></td><td colspan="2">cpWER (%) <math><semantics><mo>â†?/mo> <annotation>\downarrow</annotation></semantics></math></td></tr><tr><td>System</td><td>Challenge</td><td>Val.</td><td>Test</td></tr><tr><td>ESPnet baseline <sup><a href="#fn:52">52</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>32.4</mn> <annotation>32.4</annotation></semantics></math></td><td><math><semantics><mn>35.5</mn> <annotation>35.5</annotation></semantics></math></td></tr><tr><td>NVIDIA NeMo <sup><a href="#fn:52">52</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>21.6</mn> <annotation>21.6</annotation></semantics></math></td><td><math><semantics><mn>25.7</mn> <annotation>25.7</annotation></semantics></math></td></tr><tr><td>BUT-FIT <sup><a href="#fn:64">64</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>23.8</mn> <annotation>23.8</annotation></semantics></math></td><td><math><semantics><mn>27.6</mn> <annotation>27.6</annotation></semantics></math></td></tr><tr><td>NPU <sup><a href="#fn:65">65</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>24.9</mn> <annotation>24.9</annotation></semantics></math></td><td><math><semantics><mn>29.6</mn> <annotation>29.6</annotation></semantics></math></td></tr><tr><td>U. of Cambridge <sup><a href="#fn:66">66</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>22.0</mn> <annotation>22.0</annotation></semantics></math></td><td><math><semantics><mn>26.2</mn> <annotation>26.2</annotation></semantics></math></td></tr><tr><td>USTC <sup><a href="#fn:54">54</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>19.8</mn> <annotation>19.8</annotation></semantics></math></td><td><math><semantics><mn>19.8</mn> <annotation>19.8</annotation></semantics></math></td></tr><tr><td>IACAS-Thinkit <sup><a href="#fn:55">55</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>15.4</mn> <annotation>15.4</annotation></semantics></math></td><td><math><semantics><mn>23.9</mn> <annotation>23.9</annotation></semantics></math></td></tr><tr><td>NTT <sup><a href="#fn:67">67</a></sup></td><td>CHiME-8</td><td><math><semantics><mn>19.8</mn> <annotation>19.8</annotation></semantics></math></td><td><math><semantics><mn>24.0</mn> <annotation>24.0</annotation></semantics></math></td></tr><tr><td>STCON <sup><a href="#fn:68">68</a></sup></td><td>CHiME-8</td><td><math><semantics><mn>18.5</mn> <annotation>18.5</annotation></semantics></math></td><td><math><semantics><mn>23.0</mn> <annotation>23.0</annotation></semantics></math></td></tr><tr><td>GSS (<math><semantics><mn>24</mn> <annotation>24</annotation></semantics></math> -channel) <sup><a href="#fn:31">31</a></sup></td><td>â€?/td><td><math><semantics><mn>24.8</mn> <annotation>24.8</annotation></semantics></math></td><td><math><semantics><mn>29.7</mn> <annotation>29.7</annotation></semantics></math></td></tr><tr><td>PuLSS</td><td>â€?/td><td><math><semantics><mn>16.7</mn> <annotation>16.7</annotation></semantics></math></td><td><math><semantics><mn>19.5</mn> <annotation>19.5</annotation></semantics></math></td></tr><tr><td>Close-Talk Mixtures</td><td>â€?/td><td><math><semantics><mn>18.7</mn> <annotation>18.7</annotation></semantics></math></td><td><math><semantics><mn>19.5</mn> <annotation>19.5</annotation></semantics></math></td></tr><tr><td>â€‚â€…â€‚â€? CTRnet</td><td>â€?/td><td><math><semantics><mn>11.6</mn> <annotation>11.6</annotation></semantics></math></td><td><math><semantics><mn>15.0</mn> <annotation>15.0</annotation></semantics></math></td></tr><tr><td colspan="4">Note: Systems using close-talk mixtures as input are marked in gray.</td></tr></tbody></table>

TABLE V: ASR Results on CHiME-6 Far-Field Mixtures  
(Diarization: Estimated; ASR Model: Fine-Tuned Parakeet).

<table><tbody><tr><td></td><td></td><td colspan="2">tcpWER (%) <math><semantics><mo>â†?/mo> <annotation>\downarrow</annotation></semantics></math></td></tr><tr><td>System</td><td>Challenge</td><td>Val.</td><td>Test</td></tr><tr><td>ESPnet baseline <sup><a href="#fn:52">52</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>65.7</mn> <annotation>65.7</annotation></semantics></math></td><td><math><semantics><mn>85.2</mn> <annotation>85.2</annotation></semantics></math></td></tr><tr><td>NVIDIA NeMo <sup><a href="#fn:52">52</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>45.9</mn> <annotation>45.9</annotation></semantics></math></td><td><math><semantics><mn>63.8</mn> <annotation>63.8</annotation></semantics></math></td></tr><tr><td>BUT-FIT <sup><a href="#fn:64">64</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>61.4</mn> <annotation>61.4</annotation></semantics></math></td><td><math><semantics><mn>77.6</mn> <annotation>77.6</annotation></semantics></math></td></tr><tr><td>NPU <sup><a href="#fn:65">65</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>57.4</mn> <annotation>57.4</annotation></semantics></math></td><td><math><semantics><mn>76.9</mn> <annotation>76.9</annotation></semantics></math></td></tr><tr><td>U. of Cambridge <sup><a href="#fn:66">66</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>44.5</mn> <annotation>44.5</annotation></semantics></math></td><td><math><semantics><mn>55.4</mn> <annotation>55.4</annotation></semantics></math></td></tr><tr><td>USTC <sup><a href="#fn:54">54</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>35.7</mn> <annotation>35.7</annotation></semantics></math></td><td><math><semantics><mn>44.8</mn> <annotation>44.8</annotation></semantics></math></td></tr><tr><td>IACAS-Thinkit <sup><a href="#fn:55">55</a></sup></td><td>CHiME-7</td><td><math><semantics><mn>30.5</mn> <annotation>30.5</annotation></semantics></math></td><td><math><semantics><mn>33.5</mn> <annotation>33.5</annotation></semantics></math></td></tr><tr><td>NTT <sup><a href="#fn:67">67</a></sup></td><td>CHiME-8</td><td><math><semantics><mn>25.5</mn> <annotation>25.5</annotation></semantics></math></td><td><math><semantics><mn>35.3</mn> <annotation>35.3</annotation></semantics></math></td></tr><tr><td>STCON <sup><a href="#fn:68">68</a></sup></td><td>CHiME-8</td><td><math><semantics><mn>22.8</mn> <annotation>22.8</annotation></semantics></math></td><td><math><semantics><mn>33.6</mn> <annotation>33.6</annotation></semantics></math></td></tr><tr><td>GSS (<math><semantics><mn>24</mn> <annotation>24</annotation></semantics></math> -channel) <sup><a href="#fn:31">31</a></sup></td><td></td><td></td><td></td></tr><tr><td>â€‚â€…â€‚â€? STCON diar. <sup><a href="#fn:68">68</a></sup></td><td>â€?/td><td><math><semantics><mn>30.1</mn> <annotation>30.1</annotation></semantics></math></td><td><math><semantics><mn>37.9</mn> <annotation>37.9</annotation></semantics></math></td></tr><tr><td>â€‚â€…â€‚â€? USTC diar. <sup><a href="#fn:54">54</a></sup></td><td>â€?/td><td><math><semantics><mn>29.4</mn> <annotation>29.4</annotation></semantics></math></td><td><math><semantics><mn>33.5</mn> <annotation>33.5</annotation></semantics></math></td></tr><tr><td>PuLSS</td><td></td><td></td><td></td></tr><tr><td>â€‚â€…â€‚â€? STCON diar. <sup><a href="#fn:68">68</a></sup></td><td>â€?/td><td><math><semantics><mn>24.4</mn> <annotation>24.4</annotation></semantics></math></td><td><math><semantics><mn>31.7</mn> <annotation>31.7</annotation></semantics></math></td></tr><tr><td>â€‚â€…â€‚â€? USTC diar. <sup><a href="#fn:54">54</a></sup></td><td>â€?/td><td><math><semantics><mn>26.4</mn> <annotation>26.4</annotation></semantics></math></td><td><math><semantics><mn>28.5</mn> <annotation>28.5</annotation></semantics></math></td></tr><tr><td>Close-Talk Mixtures</td><td></td><td></td><td></td></tr><tr><td>â€‚â€…â€‚â€? STCON diar. <sup><a href="#fn:68">68</a></sup></td><td>â€?/td><td><math><semantics><mn>28.1</mn> <annotation>28.1</annotation></semantics></math></td><td><math><semantics><mn>35.3</mn> <annotation>35.3</annotation></semantics></math></td></tr><tr><td>â€‚â€…â€‚â€? USTC diar. <sup><a href="#fn:54">54</a></sup></td><td>â€?/td><td><math><semantics><mn>25.2</mn> <annotation>25.2</annotation></semantics></math></td><td><math><semantics><mn>27.2</mn> <annotation>27.2</annotation></semantics></math></td></tr><tr><td colspan="4">Note: Systems using close-talk mixtures as input are marked in gray.</td></tr></tbody></table>

### VIII-C Comparison with Existing Systems - Estimated Diarization

Table V reports results with estimated diarization at run time. To assess PuLSSâ€™s robustness to diarization errors, we evaluate it using diarization outputs from two existing systems with markedly different speaker-boundary quality on CHiME-6: (a) the USTC system [^54], which achieves the best Jaccard error rate (JER) [^69] on CHiME-6 ($28.0\%$ on the test set) <sup>7</sup>, and (b) the STCON system [^68], the overall winner of the CHiME-8 challenge but with substantially weaker diarization on CHiME-6 (JER $38.6\%$ on the test set). The latter therefore stress-tests the tolerance of PuLSS to speaker-activity boundaries with more errors. For both diarization outputs, we replace the oracle speaker-activity timestamps with the estimated ones when computing the input features for PuLSS (see Fig. 5). PuLSS is trained only with oracle diarization and is not re-trained when using estimated speaker-activity timestamps at inference. Even so, PuLSS achieves strong ASR performance with both diarization outputs, in both cases surpassing the previous best tcpWER on CHiME-6 (reported by IACAS-Thinkit [^55]) by a clear margin ($28.5\%$ vs. $33.5\%$ tcpWER). These results show that PuLSS generalizes robustly across diarization quality and, as a front-end method, consistently outperforms GSS even with non-oracle diarization ($28.5\%$ vs. $33.5\%$ tcpWER for GSS when USTC diarization is used).

## IX Limitations

It should be noted that our method has several limitations.

Close-talk mixtures often contain non-verbal sounds of the wearer, such as chewing, breathing, and laughing. CTRnet tends to preserve such sounds in its close-talk estimates, which can create difficulties for training PuLSS since the same non-verbal sounds are often too weak to be captured by far-field microphones. A related issue is that such sounds may not be reliably annotated as speaker activity by speaker-diarization systems or even human annotators, introducing potential inconsistencies between the timestamps used to condition PuLSS and the actual content of the close-talk pseudo-labels.

Our framework assumes that the maximum number of speakers $C$ is fixed at $4$. This is rarely a concern in practice, as the maximum number of speakers active within a $12$ -second processing segment is generally small in conversational scenarios. The same assumption also underlies widely-used speaker diarization systems such as Pyannote [^70] and EEND-VC [^71]. On the other hand, there are existing supervised speech separation algorithms [^72] that can deal with a large, unknown number of speakers. They can be adapted in a straightforward way to our setup.

A further consideration is the breadth of empirical evaluation. Although CHiME-6 is so far the most challenging real-recorded conversational benchmark, spanning unconstrained dinner-party conversations in real domestic environments with realistic noises, microphone synchronization issues, signal clipping, and moving speakers (see Section VI-A), it remains a single acoustic scenario. This work focuses on it because its difficulty makes it the most informative single benchmark for stress-testing real-data training, and because it allows direct comparison with a large body of CHiME-{7,8} challenge submissions. Extending CTRnet and PuLSS to other conversational domains such as AMI [^13] and AliMeeting [^14] is straightforward, since the framework requires only paired close-talk and far-field recordings.

Finally, two potentially beneficial training variants are not explored: training PuLSS directly with estimated (rather than oracle) speaker-activity timestamps to better match inference-time conditions, and end-to-end joint fine-tuning of PuLSS together with the downstream ASR model. We leave these as natural extensions for future work.

## X Conclusions

We have proposed CTRnet and PuLSS, a two-stage framework for far-field speech separation in real-recorded conversational scenarios. By formulating cross-talk reduction as a blind deconvolution problem, CTRnet jointly estimates close-talk speech and the RTFs to their reverberant images, and can be trained directly on real-recorded pairs of close-talk and far-field mixtures. The resulting close-talk estimates serve as effective pseudo-labels for training PuLSS, a supervised far-field speech separation model that operates on real-recorded multi-channel far-field mixtures. On the challenging CHiME-6 dataset, PuLSS achieves state-of-the-art ASR performance under both oracle and estimated diarization, surpassing all previous CHiME-{7,8} challenge submissions as well as GSS (the de-facto current state-of-the-art frontend approach for real conversational data) while remaining robust across different diarization systems. Moving forward, we plan to investigate end-to-end fine-tuning of PuLSS with downstream ASR models and improved modeling of distributed microphone arrays.

## References

![[Uncaptioned image]](https://arxiv.org/html/2605.19695v1/Zhong-Qiu_Wang.jpg)

Zhong-Qiu Wang

![[Uncaptioned image]](https://arxiv.org/html/2605.19695v1/wavlab_samuele_crop.jpg)

Samuele Cornell

[^1]: P. Comon and C. Jutten, *Handbook of Blind Source Separation: Independent component analysis and applications*.â€ƒAcademic press, 2010.

[^2]: J. H. McDermott, â€œThe Cocktail Party Problem,â€?*Current Biology*, vol. 19, no. 22, pp. 1024â€?027, 2009.

[^3]: D. Wang and J. Chen, â€œSupervised Speech Separation Based on Deep Learning: An Overview,â€?*IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 26, no. 10, pp. 1702â€?726, 2018.

[^4]: S. Araki, N. Ito, R. Haeb-Umbach, G. Wichern, Z.-Q. Wang, and Y. Mitsufuji, â€?0+ Years of Source Separation Research: Achievements and Future Challenges,â€?in *Proc. ICASSP*, 2025.

[^5]: R. Haeb-Umbach, J. Heymann, L. Drude, S. Watanabe, M. Delcroix, and T. Nakatani, â€œFar-Field Automatic Speech Recognition,â€?*Proc. IEEE*, vol. 109, no. 2, pp. 124â€?48, 2021.

[^6]: R. Haeb-Umbach, T. Nakatani, M. Delcroix, C. Boeddeker, and T. Ochiai, â€œMicrophone Array Signal Processing and Deep Learning for Speech Enhancement: Combining Model-Based and Data-Driven Approaches to Parameter Estimation and Filtering,â€?*IEEE Signal Process. Mag.*, vol. 41, no. 6, pp. 12â€?3, 2025.

[^7]: Z.-Q. Wang, S. Cornell, S. Choi, Y. Lee, B.-Y. Kim, and S. Watanabe, â€œTF-GridNet: Integrating Full- and Sub-Band Modeling for Speech Separation,â€?*IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 31, pp. 3221â€?236, 2023.

[^8]: W. Zhang, J. Shi, C. Li, S. Watanabe, and Y. Qian, â€œClosing The Gap Between Time-Domain Multi-Channel Speech Enhancement on Real and Simulation Conditions,â€?in *Proc. WASPAA*, 2021, pp. 146â€?50.

[^9]: C. Subakan, M. Ravanelli, S. Cornell, and F. Grondin, â€œReal-M: Towards Speech Separation on Real Mixtures,â€?in *Proc. ICASSP*, 2022, pp. 6862â€?866.

[^10]: I. Abramovski, A. Vinnikov, S. Shaer *et al.*, â€œSummary of the NOTSOFAR-1 challenge: Highlights and learnings,â€?*Comput. Speech Lang.*, vol. 93, p. 101796, 2025.

[^11]: S. Cornell, C. Boeddeker, T. Park, H. Huang, D. Raj, M. Wiesner, Y. Masuyama, X. Chang, Z.-Q. Wang, S. Squartini, P. Garcia, and S. Watanabe, â€œRecent Trends in Distant Conversational Speech Recognition: A Review of CHiME-7 and 8 DASR Challenges,â€?*Comput. Speech Lang.*, vol. 97, 2026.

[^12]: Y. Masuyama, X. Chang, W. Zhang, S. Cornell, Z.-Q. Wang, N. Ono, Y. Qian, and S. Watanabe, â€œAn End-to-End Integration of Speech Separation and Recognition with Self-Supervised Learning Representation,â€?*Comput. Speech Lang.*, vol. 95, p. 101813, 2026.

[^13]: J. Carletta, S. Ashby, S. Bourban, M. Flynn, M. Guillemot *et al.*, â€œThe AMI Meeting Corpus: A Pre-Announcement,â€?in *Machine Learning for Multimodal Interaction*, 2006, pp. 28â€?9.

[^14]: F. Yu, S. Zhang, P. Guo, Y. Fu, Z. Du *et al.*, â€œSummary on The ICASSP 2022 Multi-Channel Multi-Party Meeting Transcription Grand Challenge,â€?in *Proc. ICASSP*, 2022, pp. 9156â€?160.

[^15]: J. Barker, S. Watanabe, E. Vincent *et al.*, â€œThe Fifth â€™CHiMEâ€?Speech Separation and Recognition Challenge: Dataset, Task and Baselines,â€?in *Proc. Interspeech*, 2018, pp. 1561â€?565.

[^16]: Z. Wang, S. Wu, H. Chen *et al.*, â€œThe Multimodal Information Based Speech Processing (MISP) 2022 Challenge: Audio-Visual Diarization and Recognition,â€?in *Proc. ICASSP*, 2023, pp. 1â€?.

[^17]: Z.-Q. Wang, A. Kumar, and S. Watanabe, â€œCross-Talk Reduction,â€?in *Proc. IJCAI*, 2024, pp. 5171â€?180.

[^18]: J. Heymann, L. Drude, A. Chinaev, and R. Haeb-Umbach, â€œBLSTM Supported GEV Beamformer Front-End for The 3rd CHiME Challenge,â€?in *Proc. ASRU*, 2015, pp. 444â€?51.

[^19]: H. Erdogan, J. R. Hershey, S. Watanabe, I. Mandel, and J. Le Roux, â€œImproved MVDR Beamforming using Single-Channel Mask Prediction Networks,â€?in *Proc. Interspeech*, 2016, pp. 1981â€?985.

[^20]: K. Iwamoto, T. Ochiai, M. Delcroix, R. Ikeshita, H. Sato, S. Araki, and S. Katagiri, â€œHow Bad Are Artifacts?: Analyzing The Impact of Speech Enhancement Errors on ASR,â€?*Proc. Interspeech*, pp. 5418â€?422, 2022.

[^21]: N. Kanda, J. Wu, X. Wang, Z. Chen, J. Li, and T. Yoshioka, â€œVarArray Meets t-SOT: Advancing The State of The Art of Streaming Distant Conversational Speech Recognition,â€?in *Proc. ICASSP*, 2023, pp. 1â€?.

[^22]: S. Wisdom, E. Tzinis, H. Erdogan, R. Weiss, K. Wilson, and J. R. Hershey, â€œUnsupervised Sound Separation using Mixture Invariant Training,â€?*Proc. NeurIPS*, vol. 33, pp. 3846â€?857, 2020.

[^23]: J. Zhang, C. Zorila, R. Doddipatla, and J. Barker, â€œTeacher-Student MixIT for Unsupervised and Semi-supervised Speech Separation,â€?in *Proc. Interspeech*, 2021.

[^24]: K. Saijo and T. Ogawa, â€œSelf-Remixing: Unsupervised Speech Separation via Separation and Remixing,â€?in *Proc. ICASSP*, 2023, pp. 1â€?.

[^25]: C. Han, K. Wilson, S. Wisdom, and J. R. Hershey, â€œUnsupervised Multi-Channel Separation and Adaptation,â€?in *Proc. ICASSP*, 2024, pp. 721â€?25.

[^26]: A. Sivaraman, S. Wisdom, H. Erdogan, and J. R. Hershey, â€œAdapting Speech Separation to Real-World Meetings using Mixture Invariant Training,â€?in *Proc. ICASSP*, 2022, pp. 686â€?90.

[^27]: S. Wisdom, A. Jansen, R. J. Weiss, H. Erdogan, and J. R. Hershey, â€œSparse, Efficient, and Semantic Mixture Invariant Training: Taming In-the-wild Unsupervised Sound Separation,â€?in *Proc. WASPAA*, 2021, pp. 51â€?5.

[^28]: Z.-Q. Wang and S. Watanabe, â€œUNSSOR: Unsupervised Neural Speech Separation by Leveraging Over-Determined Training Mixtures,â€?in *Proc. NeurIPS*, vol. 36, 2023, pp. 34â€?21â€?4â€?42.

[^29]: K. Saijo, G. Wichern, F. G. Germain, Z. Pan, and J. Le Roux, â€œEnhanced Reverberation as Supervision for Unsupervised Speech Separation,â€?in *Proc. Interspeech*, 2024, pp. 607â€?11.

[^30]: K. Saijo and R. Scheibler, â€œSpatial Loss for Unsupervised Multi-channel Source Separation,â€?in *Proc. Interspeech*, 2022, pp. 241â€?45.

[^31]: C. Boeddeker, J. Heitkaemper, J. Schmalenstroeer, L. Drude, J. Heymann, and R. Haeb-Umbach, â€œFront-End Processing for The CHiME-5 Dinner Party Scenario,â€?in *Proc. CHiME*, vol. 1, 2018.

[^32]: T. Yoshioka, X. Wang, D. Wang, M. Tang, Z. Zhu, Z. Chen, and N. Kanda, â€œVarArray: Array-Geometry-Agnostic Continuous Speech Separation,â€?in *Proc. ICASSP*, 2022, pp. 6027â€?031.

[^33]: Z. Chen, T. Yoshioka, L. Lu, T. Zhou, Z. Meng, Y. Luo, J. Wu, X. Xiao, and J. Li, â€œContinuous speech separation: Dataset and analysis,â€?in *Proc. ICASSP*, 2020, pp. 7284â€?288.

[^34]: A. Vinnikov, A. Ivry, A. Hurvitz *et al.*, â€œNOTSOFAR-1 Challenge: New Datasets, Baseline, and Tasks for Distant Meeting Transcription,â€?in *Proc. Interspeech*, 2024.

[^35]: T. Von Neumann, C. Boeddeker, T. Cord-Landwehr, M. Delcroix, and R. Haeb-Umbach, â€œMeeting Recognition with Continuous Speech Separation and Transcription-Supported Diarization,â€?in *Proc. HSCMA*, 2024, pp. 775â€?79.

[^36]: Y. Bando, Y. Masuyama, A. A. Nugraha, and K. Yoshii, â€œNeural fast full-rank spatial covariance analysis for blind source separation,â€?in *Proc. EUSIPCO*, 2023, pp. 51â€?5.

[^37]: Y. Bando, T. Nakamura, and S. Watanabe, â€œNeural Blind Source Separation and Diarization for Distant Speech Recognition,â€?in *Proc. Interspeech*, 2024, pp. 722â€?26.

[^38]: Y. Bando, S. Cornell, S. Fukayama, and S. Watanabe, â€œInvestigation of Spatial Self-Supervised Learning and Its Application to Target Speaker Speech Recognition,â€?in *Proc. ICASSP*, 2025, pp. 1â€?.

[^39]: Z.-Q. Wang, â€œctPuLSE: Close-Talk, and Pseudo-Label Based Far-Field, Speech Enhancement,â€?*J. Acoust. Soc. Am.*, vol. 158, no. 4, pp. 2849â€?862, 2025.

[^40]: â€”â€? â€œSuperM2M: Supervised and Mixture-to-Mixture Co-Learning for Speech Enhancement and Robust ASR,â€?*Neural Networks*, vol. 188, no. 107408, pp. 1â€?6, 2025.

[^41]: â€”â€? â€œMixture to Mixture: Leveraging Close-Talk Mixtures as Weak-Supervision for Speech Separation,â€?*IEEE Signal Process. Lett.*, vol. 31, pp. 1715â€?719, 2024.

[^42]: L. Luo, L. Li, and Q. Hong, â€œSuPseudo: A Pseudo-supervised Learning Method for Neural Speech Enhancement in Far-field Speech Recognition,â€?in *Proc. Interspeech*, 2025, pp. 3404â€?408.

[^43]: L. Luo, S. Lu, L. Li, and Q. Hong, â€œPseudo Labels-Based Neural Speech Enhancement for the AVSR Task in The MISP-Meeting Challenge,â€?in *Proc. Interspeech*, 2025, pp. 1883â€?887.

[^44]: R. Talmon, I. Cohen, and S. Gannot, â€œRelative Transfer Function Identification using Convolutive Transfer Function Approximation,â€?*IEEE Trans. Audio, Speech, Lang. Process.*, vol. 17, no. 4, pp. 546â€?55, 2009.

[^45]: S. Gannot, E. Vincent *et al.*, â€œA Consolidated Perspective on Multi-Microphone Speech Enhancement and Source Separation,â€?*IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 25, pp. 692â€?30, 2017.

[^46]: A. Levin, Y. Weiss, F. Durand, and W. T. Freeman, â€œUnderstanding Blind Deconvolution Algorithms,â€?*IEEE Trans. Pattern Anal. Mach. Intell.*, vol. 33, no. 12, pp. 2354â€?367, 2011.

[^47]: Z.-Q. Wang, G. Wichern, and J. Le Roux, â€œConvolutive Prediction for Monaural Speech Dereverberation and Noisy-Reverberant Speaker Separation,â€?*IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 29, pp. 3476â€?490, 2021.

[^48]: S. Wisdom, J. R. Hershey, K. Wilson, J. Thorpe, M. Chinen, B. Patton, and R. A. Saurous, â€œDifferentiable Consistency Constraints for Improved Deep Speech Enhancement,â€?in *Proc. ICASSP*, 2019, pp. 900â€?04.

[^49]: M. KolbÃ¦k, D. Yu, Z.-H. Tan, and J. Jensen, â€œMultitalker Speech Separation with Utterance-Level Permutation Invariant Training of Deep Recurrent Neural Networks,â€?*IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 25, no. 10, pp. 1901â€?913, 2017.

[^50]: D. Raj, P. Denisov, Z. Chen, H. Erdogan, Z. Huang, M. He, S. Watanabe, J. Du, T. Yoshioka, Y. Luo *et al.*, â€œIntegration of Speech Separation, Diarization, and Recognition for Multi-Speaker Meetings: System Description, Comparison, and Analysis,â€?in *Proc. SLT*, 2021, pp. 897â€?04.

[^51]: S. Watanabe, M. Mandel, J. Barker *et al.*, â€œCHiME-6 Challenge: Tackling Multispeaker Speech Recognition for Unsegmented Recordings,â€?in *Proc. CHiME*, 2020, pp. 1â€?.

[^52]: S. Cornell, M. S. Wiesner, S. Watanabe, D. Raj, X. Chang, P. Garcia, Y. Masuyam, Z.-Q. Wang, S. Squartini, and S. Khudanpur, â€œThe CHiME-7 DASR Challenge: Distant Meeting Transcription with Multiple Devices in Diverse Scenarios,â€?in *Proc. CHiME*, 2023, pp. 1â€?.

[^53]: S. Cornell, T. J. Park, H. Huang, C. Boeddeker, X. Chang, M. Maciejewski, M. S. Wiesner, P. Garcia, and S. Watanabe, â€œThe CHiME-8 DASR Challenge for Generalizable and Array Agnostic Distant Automatic Speech Recognition and Diarization,â€?in *Proc. CHiME*, 2024, pp. 1â€?.

[^54]: R. Wang, M. He, J. Du *et al.*, â€œThe USTC-NERCSLIP Systems for the CHiME-7 DASR Challenge,â€?in *Proc. CHiME*, 2023, pp. 13â€?8.

[^55]: L. Ye, H. Lu, G. Cheng, Y. Chen, Z. Shang, and X. Li, â€œThe IACAS-Thinkit System for CHiME-7 Challenge,â€?in *Proc. CHiME*, 2023, pp. 23â€?6.

[^56]: Z.-Q. Wang, P. Wang, and D. Wang, â€œMulti-Microphone Complex Spectral Mapping for Utterance-Wise and Continuous Speech Separation,â€?*IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 29, pp. 2001â€?014, 2021.

[^57]: V. Panayotov, G. Chen, D. Povey, and S. Khudanpur, â€œLibrispeech: An ASR Corpus Based on Public Domain Audio Books,â€?*Proc. ICASSP*, pp. 5206â€?210, 2015.

[^58]: J. Richter, Y. C. Wu, S. Krenn, S. Welker, B. Lay, S. Watanabe, A. Richard, and T. Gerkmann, â€œEARS: An Anechoic Fullband Speech Dataset Benchmarked for Speech Enhancement and Dereverberation,â€?in *Proc. Interspeech*, 2024, pp. 4873â€?877.

[^59]: E. Fonseca, X. Favory, J. Pons, F. Font, and X. Serra, â€œFSD50K: An Open Dataset of Human-Labeled Sound Events,â€?*IEEE/ACM Trans. Audio, Speech, Lang. Process.*, vol. 30, pp. 829â€?52, 2022.

[^60]: K. Kinoshita, M. Delcroix, S. Gannot *et al.*, â€œA Summary of The REVERB Challenge: State-of-The-Art and Remaining Challenges in Reverberant Speech Processing Research,â€?*Eurasip J. Adv. Signal Process.*, vol. 2016, no. 1, pp. 1â€?9, 2016.

[^61]: T. von Neumann, C. Boeddeker, M. Delcroix, and R. Haeb-Umbach, â€œWord Error Rate Definitions and Algorithms for Long-Form Multi-Talker Speech Recognition,â€?*IEEE Trans. Audio, Speech, Lang. Process.*, 2025.

[^62]: M. Sekoyan, N. R. Koluguri, N. Tadevosyan, P. Zelasko, T. Bartley, N. Karpov, J. Balam, and B. Ginsburg, â€œCanary-1B-v2 & Parakeet-TDT-0.6B-v3: Efficient and High-Performance Models for Multilingual ASR and AST,â€?*arXiv preprint arXiv:2509.14128*, 2025.

[^63]: O. Kuchaiev, J. Li, H. Nguyen, O. Hrinchuk, R. Leary, B. Ginsburg, S. Kriman, S. Beliaev, V. Lavrukhin, J. Cook *et al.*, â€œNeMo: A Toolkit for Building AI Applications using Neural Modules,â€?*arXiv preprint arXiv:1909.09577*, 2019.

[^64]: M. Karafiat, K. VeselÃ½, I. Szoke, L. Mosner, K. Benes, M. Witkowski, R. G. Barchi, and L. D. Pepino, â€œBUT CHiME-7 System Description,â€?in *Proc. CHiME*, 2023, pp. 67â€?2.

[^65]: B. Mu, P. Guo, H. Wang, Y. Li, Y. Li, P. Zhou, W. Chen, and L. Xie, â€œThe NPU System for DASR Task of CHiME-7 Challenge,â€?in *Proc. CHiME*, 2023, pp. 63â€?6.

[^66]: K. Deng, X. Zheng, and P. Woodland, â€œThe University of Cambridge System for the CHiME-7 DASR Task,â€?in *Proc. CHiME*, 2023, pp. 73â€?6.

[^67]: N. Kamo, N. Tawara, A. Ando *et al.*, â€œNTT Multi-Speaker ASR System for the DASR Task of CHiME-8 Challenge,â€?in *Proc. CHiME*, 2024, pp. 69â€?4.

[^68]: A. Mitrofanov, T. Prisyach, T. Timofeeva *et al.*, â€œSTCON System for the CHiME-8 Challenge,â€?in *Proc. CHiME*, 2024, pp. 13â€?7.

[^69]: N. Ryant, K. Church, C. Cieri, A. Cristia, J. Du, S. Ganapathy, and M. Liberman, â€œThe Second DIHARD Diarization Challenge: Dataset, Task, and Baselines,â€?in *Proc. Interspeech*, 2019, pp. 978â€?82.

[^70]: H. Bredin, R. Yin, J. M. Coria, G. Gelly, P. Korshunov, M. Lavechin, D. Fustes, H. Titeux *et al.*, â€œpyannote.audio: Neural Building Blocks for Speaker Diarization,â€?in *Proc. ICASSP*, 2020, pp. 7124â€?128.

[^71]: K. Kinoshita, M. Delcroix, and N. Tawara, â€œIntegrating End-to-End Neural and Clustering-Based Diarization: Getting The Best of Both Worlds,â€?in *Proc. ICASSP*, 2021, pp. 7198â€?202.

[^72]: Y. Lee, S. Choi, B. Y. Kim, Z. Q. Wang, and S. Watanabe, â€œBoosting Unknown-Number Speaker Separation with Transformer Decoder-Based Attractor,â€?in *Proc. ICASSP*, 2024, pp. 446â€?50.
