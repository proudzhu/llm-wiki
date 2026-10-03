Weilong Huang    Srikanth Raj Chetupalli    Mhd Modar Halimeh Affiliation: Oliver Thiergart, and Emanuël A. P. Habets,

###### Abstract

Beamforming with desired directivity patterns using compact microphone arrays is essential in many audio applications. Directivity patterns achievable using traditional beamformers depend on the number of microphones and the array aperture. Generally, their effectiveness degrades for compact arrays. To overcome these limitations, we propose a neural directional filtering (NDF) approach that leverages deep neural networks to enable sound capture with a predefined directivity pattern. The NDF computes a single-channel complex mask from the microphone array signals, which is then applied to a reference microphone to produce an output that approximates a virtual directional microphone with the desired directivity pattern. We introduce training strategies and propose data-dependent metrics to evaluate the directivity pattern and directivity factor. We show that the proposed method: i) achieves a frequency-invariant directivity pattern even above the spatial aliasing frequency, ii) can approximate diverse and higher-order patterns, iii) can steer the pattern in different directions, and iv) generalizes to unseen conditions. Lastly, experimental comparisons demonstrate superior performance over conventional beamforming and parametric approaches.

DNN

deep neural network

$\Delta$ SDR

improvement in [SDR](#id25) ([SDR](#id25)) over the unprocessed signal

DMA

differential microphone array

DNN

deep neural network

DOA

direction-of-arrival

iSTFT

inverse short-time Fourier transform

CDMA

circular [DMA](#id3) ([DMA](#id3))

LDMA

linear [DMA](#id3)

LS

least-squares

LSTM

long short-term memory

BiLSTM

bidirectional LSTM

UniLSTM

unidirectional LSTM

WNG

white noise gain

RIR

room impulse response

RTF

room transfer function

ATF

acousitc transfer function

DPIR

direct-path impulse response

MVDR

minimum variance distortionless response

LCMV

linear-constraint minimum-variance

PMWF

parametric multichannel wiener filter

GSC

Generalized sidelobe canceller

JNF

joint spatial and temporal-spectral non-linear filtering

FT-JNF

joint spatial and temporal-spectral non-linear filtering

DSB

delay-and-sum beamformer

SDR

signal-to-distortion ratio

reference microphone

[SDR](#id25) of the unprocessed omnidirectional reference microphone

SNR

signal-to-noise ratio

STFT

short-time Fourier transform

MAE

mean absolute error

TF

time-frequency

SA- $\varepsilon$ -tSDR

source-aggregated and regularized thresholded [SDR](#id25)

STOI

short term objective intelligibility

PESQ

perceptual evaluation of speech quality

UCA

uniform circular array

NDF

neural directional filtering

WNG

white noise gain

DF

directivity factor

DI

directivity index

HRTF

head-related transfer function

ILD

interaural level difference

FiLM

feature-wise linear modulation

VDM

virtual directional microphone

## I INTRODUCTION

Beamforming is a widely used technique to selectively attenuate interfering sources [^44], thereby improving speech quality and intelligibility. Furthermore, beamforming with an appropriate directivity pattern enables precise spatial rendering of sound sources, preserving essential spatial cues when multiple sources are present. For example, a first-order [DMA](#id3) can generate first-order Ambisonics [^24] without specialized recording systems, such as a SoundField microphone or an Eigenmike used in [^6]. This demonstrates that spatial rendering via beamforming with an appropriate directivity pattern is an effective and flexible solution for capturing spatial sound.

Fixed beamforming is a technique that can target a specific directivity pattern using data-independent linear filters to achieve a time-invariant spatial response [^13] [^5] [^3]. The performance of fixed beamformers is typically evaluated in terms of their directivity pattern, [WNG](#id36) ([WNG](#id36)), and [DF](#id37) ([DF](#id37)). For instance, [DSB](#id24) maximize [WNG](#id36) but generally provide limited directivity. In contrast, superdirective beamformers enhance [DF](#id37) at the cost of reduced [WNG](#id36) [^5]. Differential microphone arrays ([DMA](#id3)) [^13] [^4] and [LS](#id9) ([LS](#id9)) beamformers [^30] offer a compromise between [WNG](#id36) and [DF](#id37). However, [DMA](#id3) often suffer from white-noise amplification at low frequencies when attempting to achieve highly directive patterns [^3]. [LS](#id9) beamformers can approximate a desired directivity pattern while ensuring a specified minimum [WNG](#id36), but when the number of microphones is small or when aiming for high directivity, significant deviations from the desired pattern can occur. Overall, achieving a highly directive pattern with fixed beamformers often requires a large number of microphones and a sufficiently large array.

Unlike fixed beamforming, parametric spatial filtering [^33] [^22] [^36] [^38] [^41] [^23] [^10] [^40] offers a data-dependent approach to achieve a desired directivity pattern. Conventional parametric filters [^33] [^22] [^36] employ a relatively simple signal model, where the direct sound is modeled as a single plane wave per time-frequency bin and the reverberant sound is modeled as a time-varying diffuse sound field [^21]. These filters are typically computed based on instantaneous estimates of model parameters, such as the [DOA](#id5) ([DOA](#id5)) or diffuseness of the sound. However, the single-wave assumption is easily violated in practical scenarios [^37], resulting in inaccurate spatial capture and audible artifacts. To overcome these limitations, parametric spatial filters [^38] [^41] [^40], which unify classical beamforming and parametric filters, extend the signal model to include multiple plane waves per time-frequency bin. Although violations of the signal model are less likely to occur, these methods rely heavily on accurate multiple-source [DOA](#id5) and diffuse-sound power estimation, which can be challenging, particularly in reverberant or multi-source environments containing non-speech signals [^37]. Nevertheless, these methods offer valuable functionality in applications such as acoustic zooming [^39] and automatic spatial gain control [^7].

With the rise of deep learning, more [DNN](#id4) ([DNN](#id4))-based spatial filters have been proposed [^53] [^55] [^17] [^14] [^34] [^35] [^50]. Some studies [^53] [^55] [^17] compute multichannel masks and employ filter-and-sum processing. Others [^14] [^34] [^35] [^50] estimate a single-channel mask and apply it to a reference or selected microphone. Typically, these methods perform spatial filtering based on an angular region. They treat sound sources in that region as targets and suppress others outside it. This results in a rectangular directivity pattern with a sharp separation between the desired and undesired sources. As a result, sensitivity to directional errors increases, leading to discontinuities near the boundary. These methods do not offer explicit control over the directivity pattern and mainly focus on noise reduction or speaker extraction. To study the capability of neural spatial filters, such as the [FT-JNF](#id23) ([FT-JNF](#id23)) [^34], to extract and represent spatial information, works like [^8] [^9] use the [DSB](#id24) output as the [DNN](#id4) training target. This approach implicitly guides the [DNN](#id4) to learn the directivity pattern of a [DSB](#id24). However, the [DSB](#id24) usually has a frequency-variant directivity pattern and limited directivity at low frequencies.

Recently, [NDF](#id35) ([NDF](#id35)) has been proposed to enable explicit control over the directivity pattern for spatial filtering [^49]. This preliminary study in [^49] demonstrates that [NDF](#id35) can approximate fixed $1^{\textrm{st}}$ - and $3^{\textrm{rd}}$ -order [DMA](#id3) directivity patterns in anechoic environments. However, these patterns are non-steerable, and the underlying processing mechanism and potential capabilities remain unclear. In this paper, we extend [NDF](#id35) to be steerable for arbitrary continuous steering directions and to realize versatile patterns. The main contributions are as follows: 1) Steerability: We propose a method to enable arbitrary continuous steerability of the [NDF](#id35). 2) Pattern controllability: We demonstrate the ability of [NDF](#id35) to flexibly realize frequency-invariant higher-order or arbitrary predefined directivity patterns. 3) Evaluation methods: We extend [NDF](#id35) to reverberant environments, and propose generalized methods to evaluate the directivity pattern and directivity factor for any masking-based method, enabling separate analysis of the effects on the direct and reverberant components. 4) Performance enhancements: We propose a batch-aggregated normalized L1 loss function for training, which achieves superior performance compared to [^49]. 5) In-depth study: We investigate the [NDF](#id35) model’s behavior, including its ability to maintain frequency-invariant directivity patterns even above the spatial aliasing frequency, as well as its generalization to unseen non-speech and moving-source scenarios. Finally, we present an application of [NDF](#id35) to stereo sound recording using a compact microphone array.

The remainder of this paper is organized as follows: Section II formulates the problem. Section III details the proposed method, and the corresponding evaluation methods are presented in Section IV. Section V outlines the experimental setup. Section VI and Section VII present the experimental study conducted in anechoic and reverberant conditions, respectively. Section VIII investigates the [NDF](#id35) performance for previously unseen moving sources. Finally, Section IX concludes the paper.

## II Problem Formulation

Fig. 1: Three directivity pattern examples on the $x$ - $y$ plane. Steering direction $\theta_{\textrm{s}}=0$ is used for the illustration.

We consider a scenario in which a compact array with $Q$ omnidirectional microphones captures an acoustic scene comprising $N$ sound sources in the far field. Let $X_{q,n}[f,t]$ represent the $n$ -th source signal at the $q$ -th microphone in the [STFT](#id28) ([STFT](#id28)) domain, where $f$ and $t$ denote the frequency and time indices, respectively. The mixture signal at the $q$ -th microphone, denoted by $Y_{q}[f,t]$, can be expressed as

$$
Y_{q}[f,t]=\sum_{n=1}^{N}X_{q,n}[f,t]+V_{q}[f,t],~q\in\{1,2,\ldots,Q\},
$$

where $V_{q}[f,t]$ represents the sensor noise that is spatially uncorrelated across the microphones. Furthermore, we have $X_{q,n}[f,t]=H_{\mathbf{p}_{q},\mathbf{p}_{n}}[f]\,X_{n}[f,t]$ [^1], where $X_{n}[f,t]$ represents the $n$ -th source signal and $H_{\mathbf{p}_{q},\mathbf{p}_{n}}[f]$ models the [ATF](#id16) ([ATF](#id16)) between the $n$ -th source at position $\mathbf{p}_{n}$ and the $q$ -th microphone located at position $\mathbf{p}_{q}$.

The objective of the directional filtering task is to capture the acoustic scene and apply spatial filtering according to a specified directivity pattern. The directivity pattern describes the directional sensitivity of a beamformer or directional microphone, reflecting its spatial response to sounds arriving from various directions [^13] [^12]. For example, a $1^{\textrm{st}}$ -order [DMA](#id3) directivity pattern [^13] is defined as

$$
\Lambda_{1^{\textrm{st}}}(\theta,\phi)=\mu+(1-\mu)(\sin\phi\sin\phi_{\textrm{s}}\cos(\theta-\theta_{\textrm{s}})+\cos\phi\cos\phi_{\textrm{s}}),
$$

where $\theta$ and $\phi$ represent the azimuth and polar angles of the incident sound, respectively. The parameter $\mu$, a real value in the interval $[0,1]$, determines the null position; for instance, $\mu=0.5$ yields a Cardioid pattern. Generally, a higher-order [DMA](#id3) directivity pattern can be the product of multiple $1^{\textrm{st}}$ -order [DMA](#id3) patterns [^13]. In this study, we assume that all $1^{\textrm{st}}$ -order [DMA](#id3) patterns in the product are identical. This assumption ensures that the higher-order [DMA](#id3) directivity pattern retains the same null positions as the $1^{\textrm{st}}$ -order pattern and avoids additional sidelobes, since mainlobe control is the primary objective for sound capture. Therefore, a high-order [DMA](#id3) directivity pattern can be expressed as

$$
\Lambda(\theta,\phi)=(\Lambda_{1^{\textrm{st}}}(\theta,\phi))^{J},
$$

where $J$ is the order number. Figure 1 presents examples of $1^{\textrm{st}}$ -, $3^{\textrm{rd}}$ -, and $6^{\textrm{th}}$ -order Cardioid directivity patterns, corresponding to $J\in\{1,3,6\}$. For these patterns, the mainlobe width decreases as the order increases.

One possible approach for directional filtering is to mimic a [VDM](#id42) ([VDM](#id42)) with the desired directivity pattern. In the following, we assume that [VDM](#id42) position, denoted by $\mathbf{p}_{\textrm{VDM}}$, is equal to the position of the first microphone ($q=1$). The target signal for the directional filtering is the [VDM](#id42) signal $Z[f,t]$ given by

$$
Z[f,t]=\sum_{n=1}^{N}H_{\mathbf{p}_{\textrm{VDM}},\mathbf{p}_{n}}[f,\Lambda(\theta,\phi)]\,X_{n}[f,t],
$$

where $H_{\mathbf{p}_{\textrm{VDM}},\mathbf{p}_{n}}[f,\Lambda(\theta,\phi)]$ denotes the [RTF](#id15) ([RTF](#id15)) between the $n$ -th source at position $\mathbf{p}_{n}$ and the [VDM](#id42), which is given by

$$
H_{\mathbf{p}_{\textrm{VDM}},\mathbf{p}_{n}}[f,\Lambda(\theta,\phi)]=\sum_{i=1}^{\infty}\Lambda(\theta_{i},\phi_{i})\,\rho^{(i)}_{\mathbf{p}_{\textrm{VDM}},\mathbf{p}_{n}}[f],
$$

where $\rho^{(i)}_{\mathbf{p}_{\textrm{VDM}},\mathbf{p}_{n}}[f]$ represents the transfer function of the $i$ -th sound propagation path between the $n$ -th source and the [VDM](#id42) in a reverberant environment. In other words, every reflection is weighted with the assigned gain based on the directivity pattern in the corresponding direction. Here, the incident angles $\theta_{i}$ and $\phi_{i}$ correspond to the angles of arrival of the $i$ -th propagation path. For simplicity, this paper focuses on a scenario where all sound sources are located in the $x$ - $y$ plane, and we restrict the steering direction of the directivity pattern to the $x$ - $y$ plane.

In an anechoic environment, there is only one direct-path transfer function $\rho_{\mathbf{p}_{\textrm{VDM}},\mathbf{p}_{n}}[f]$ between the $n$ -th source and the [VDM](#id42) which simplifies (4) as

$$
Z[f,t]=\sum_{n=1}^{N}\Lambda(\theta_{n})\,\rho_{\mathbf{p}_{\textrm{VDM}},\mathbf{p}_{n}}[f]\,X_{n}[f,t],
$$

where $\theta_{n}$ represents the direction of arrival for the $n$ -th source signal. This paper considers a [DNN](#id4) -based approach to estimate a target [VDM](#id42) signal using the microphone array signals.

## III Proposed Method

This section presents the proposed neural directional filtering method, which includes the [DNN](#id4) architecture, loss function, and training strategy.

![[raw/papers/huang-2026-neural-directional-filtering/figures/fig1.png|Refer to caption]]

Fig. 2: DNN architecture for neural directional filtering: FT-JNF 34 for static steering direction; The proposed FiLM-JNF for continuous steering direction.

### III-A DNN Architecture

In this work, we adopt the [FT-JNF](#id23) [^34] as the [DNN](#id4) architecture for the [NDF](#id35) to learn a static directivity pattern, i.e., with a fixed steering direction (e.g., $\theta_{s}=0$). The architecture and intermediate feature map dimensions are shown on the left side of the Figure 2. In [FT-JNF](#id23), the real and imaginary parts of the $Q$ microphone signals in the [STFT](#id28) domain are stacked along the channel dimension and then processed by two distinct [LSTM](#id10) ([LSTM](#id10)) modules. The first [LSTM](#id10) is a [BiLSTM](#id11) ([BiLSTM](#id11)) operating on the stacked [STFT](#id28) input along the frequency dimension. Its output is then processed by a [UniLSTM](#id12) ([UniLSTM](#id12)) module. This module treats the frequency dimension as the batch dimension and processes along the temporal dimension, thereby modeling all frequencies independently and capturing the causal temporal relationships. Notably, unlike two [BiLSTM](#id11) in [^34], the unidirectional configuration of the second [LSTM](#id10) enables causal processing. Finally, a linear layer with a hyperbolic tangent activation function computes a complex-valued single-channel mask, denoted by $\mathcal{M}[f,t]$. To use this [DNN](#id4) to approximate the input-output behavior of a directional microphone in a signal-dependent manner, we compute an estimate for the target [VDM](#id42) signal by masking the reference microphone signal:

$$
\widehat{Z}[f,t]=\mathcal{M}[f,t]Y_{1}[f,t].
$$

To enable steerability of the directivity pattern during inference, the steering angle $\theta_{\textrm{s}}$ can be hot-vector encoded and used to reinitialize the [BiLSTM](#id11) ’s hidden state in the [FT-JNF](#id23) architecture. This mechanism was initially proposed for speaker extraction in [^35] and has also been shown to work for the [NDF](#id35) [^19]. However, the inherent limitation of hot-vector encoding restricts steerability to predefined discrete steering angles, rather than supporting continuous steering directions that may not have been observed during training. To overcome this limitation, we propose the FiLM-JNF architecture, which introduces a [FiLM](#id41) ([FiLM](#id41)) [^28] layer as a conditioning layer between the [BiLSTM](#id11) and [UniLSTM](#id12) layers in the [FT-JNF](#id23) architecture [^34], as illustrated on the right side of Figure 2.

In the proposed FiLM-JNF architecture, the desired steering direction is represented by an angle $\theta_{\mathrm{s}}$ (radians). We map $\theta_{\mathrm{s}}$ to an angle embedding $\mathbf{e}_{\theta_{\mathrm{s}}}\in\mathbb{R}^{d_{\mathrm{emb}}}$ with $d_{\mathrm{emb}}=72$, following the sinusoidal encoding of [^45] applied to the continuous angle instead of a discrete position. Concretely, for $i\in\{0,\ldots,d_{\mathrm{emb}}/2-1\}$, $\mathbf{e}_{\theta_{\mathrm{s}}}[2i]=\sin(\frac{\theta_{\mathrm{s}}}{10000^{2i/d_{\mathrm{emb}}}}),\mathbf{e}_{\theta_{\mathrm{s}}}[2i+1]=\cos(\frac{\theta_{\mathrm{s}}}{10000^{2i/d_{\mathrm{emb}}}}),$ so that the batch of angles yields an embedding tensor of shape $[B,72]$, which is then used to condition the network. The [FiLM](#id41) layer computes per-feature affine parameters $\boldsymbol{\alpha}$ and $\boldsymbol{\beta}$ (dimensions $[B,512]$) through two separate linear layers derived from the angle embeddings. It then applies element-wise modulation $\bf{y}=\boldsymbol{\alpha}\odot\bf{x}+\boldsymbol{\beta}$, shared across both time and frequency, where $\bf{y}$ is the output of the [FiLM](#id41) layer, matching the dimension of $\bf{x}$. The output is reshaped to $[B\times F,T,512]$ to fit the input requirements of the subsequent [UniLSTM](#id12) layer. The remaining processing steps are identical to those in the [FT-JNF](#id23).

### III-B Loss Function

In [^49], the [tsdr](#id31) ([tsdr](#id31)) [^47] was used as the loss function, which is given by

$$
\mathcal{L}_{\textrm{SDR}}(\mathbf{z},\widehat{\mathbf{z}})=10\log_{10}\left(\frac{\sum_{b=1}^{B}\left\|\mathbf{z}^{(b)}-\widehat{\mathbf{z}}^{(b)}\right\|_{2}^{2}}{\sum_{b=1}^{B}\left\|\mathbf{z}^{(b)}\right\|_{2}^{2}+\epsilon}+\tau\right),
$$

where $B$ is the batch size, $\epsilon$ is a small constant value, $\tau=10^{-\frac{\textrm{SDR}_{\textrm{max}}}{10}}$ ($\textrm{SDR}_{\textrm{max}}$ is 40 $\mathrm{dB}$ as the maximum SDR threshold), and ${\mathbf{z}}$ and $\widehat{\mathbf{z}}$ are the time-domain target and estimated [VDM](#id42) signals, respectively.

It is often reported that the $L_{1}$ loss can outperform the $L_{2}$ loss for speech processing tasks in terms of metrics such as SDR, PESQ, and STOI [^48] [^27]. Therefore, we adopt a batch-aggregated normalized $L_{1}$ loss function in this work:

$$
\mathcal{L}_{\textrm{1}}(\mathbf{z},\widehat{\mathbf{z}})=\frac{\sum_{b=1}^{B}\left\|\mathbf{z}^{(b)}-\widehat{\mathbf{z}}^{(b)}\right\|_{1}}{\sum_{b=1}^{B}\left\|\mathbf{z}^{(b)}\right\|_{1}+\epsilon}.
$$

A performance comparison between the models trained with (8) and (9) is presented in Section VI-A1.

### III-C Training Strategy

#### III-C1 Training simulation for anechoic environment

We set a fixed source-array distance $d$ for learning a far-field directivity pattern in the anechoic scenario, and assume the array to be placed at the origin of the coordinate system, and $P$ discrete candidate source positions are obtained by uniformly sampling the azimuth angle along a circle of radius $d$. The array and the source positions are assumed to be co-planar. We define a particular source-array setup as one acoustic scene. Within each scene, we randomly select $N$ positions from the $P$ source positions for $N$ speech sources. We then simulate direct-path transfer functions $\rho_{{\mathbf{p}_{\textrm{q}}},\mathbf{p}_{n}}[f]$ for all $Q$ microphones and $N$ sources using the [RIR](#id14) ([RIR](#id14)) generator [^15] with a reflection order of zero. Following this, we obtain $Q$ microphone signals using (1).

#### III-C2 Training simulation for reverberant environment

First, we randomly select $N$ [DOA](#id5) for the $N$ sources from $P$ candidate source [DOA](#id5). To obtain a source-array setup, each source has a random source-array distance. Second, we define a room with a random size and a random reverberation time. Third, we randomly place the source-array setup in the room described in Sec.V-C2. The source-array setup lies in the room’s $x$ - $y$ plane. Lastly, based on the current positions of the microphones and sources, we generate the corresponding [RIR](#id14) and compute the microphone signals.

#### III-C3 Static or steerable

For a static directivity pattern, we simulate one target [VDM](#id42) signal $Z[f,t]$ with a fixed steering direction for each acoustic scene using (6) in anechoic conditions or using (4) in reverberant conditions. For a steerable directivity pattern, we simulate $M$ target [VDM](#id42) signals for steering directions uniformly spanning $0^{\circ}$ to $360^{\circ}$ degrees, where $M=\frac{360^{\circ}}{\vartheta}$ with $\vartheta$ denoting the angular resolution. The $m$ -th [VDM](#id42) target signal is also obtained using (4) or (6) corresponding to the $m$ -th steering direction. During training, we treat each microphone signal from an acoustic scene paired with a single [VDM](#id42) target signal as a *training sample*. When learning steerable directivity patterns, the same microphone signals are repeated $M$ times to train on $M$ [VDM](#id42) target signals, yielding $M$ distinct training samples. Similarly, a *test sample* is defined in the same way as the training sample.

#### III-C4 Mini-batch sampling

Training samples with all sources near the null direction lead to excessively large losses, impacting stability. While batch-aggregated loss helps, the problem persists if a mini-batch consists entirely of samples around the null direction. Thus, we propose an enhanced mini-batch sampling strategy in which training samples are selected so that each mini-batch contains at least one example from the target direction or its vicinity ($\pm 20^{\circ}$). This prevents the normalization term in (8) or (9) from becoming excessively large, thereby improving training robustness.

## IV Performance Measures

The performance of conventional linear beamformers is commonly evaluated using the [WNG](#id36), [DF](#id37), and directivity pattern. As the [NDF](#id35) is both data-dependent and non-linear, we propose a method to estimate the directivity pattern and the [DF](#id37) that is suitable for non-linear processing methods. These analyze the spatial filtering of direct and reverberant sounds, respectively.

To introduce the calculation of the proposed performance metrics, we let $X^{(k)}_{1,n}[f,t]$ be the [STFT](#id28) representation of the $n$ -th source signal in the $k$ -th test sample at the reference microphone. In a reverberant environment, $X^{(k)}_{1,n}[f,t]$ can be decomposed as

$$
X^{(k)}_{1,n}[f,t]=X^{(k)}_{1,n,\textrm{dir}}[f,t]+X^{(k)}_{1,n,\textrm{rvb}}[f,t],
$$

where $X^{(k)}_{1,n,\textrm{dir}}[f,t]$ represents the direct-path component and $X^{(k)}_{1,n,\textrm{rvb}}[f,t]$ represents the reverberant component (including all reflections) related to the $n$ -th source. Consequently, we have $Y^{(k)}_{1,\textrm{dir}}[f,t]=\sum_{n=1}^{N}X^{(k)}_{1,n,\textrm{dir}}[f,t]$ and $Y^{(k)}_{1,\textrm{rvb}}[f,t]=\sum_{n=1}^{N}X^{(k)}_{1,n,\textrm{rvb}}[f,t]$, which represent the cumulative direct and reverb components at the reference microphone, respectively.

### IV-A Directivity Pattern

A directivity pattern describes the spatial responses of a spatial filter or directional microphone to sounds from different directions. In the following, we focus on estimating the power pattern, which equals the squared magnitude of the directivity pattern [^43].

To estimate the power pattern obtained by a specific model, we apply the estimated mask $\mathcal{M}^{(k)}[f,t]$ for the $k$ -th test sample separately to the direct-path part of each source signal as received by the reference microphone. The corresponding narrowband power ratio $\xi_{n}^{(k)}[f]$ of the masked source signals to the unmasked source signals is then calculated as

$$
\xi_{n}^{(k)}[f]=\frac{\sum_{t=1}^{T}\left|\mathcal{M}^{(k)}[f,t]\;X^{(k)}_{1,n,\textrm{dir}}[f,t]\right|^{2}}{\sum_{t=1}^{T}\left|X^{(k)}_{1,n,\textrm{dir}}[f,t]\right|^{2}},
$$

and the wideband power ratio $\bar{\xi}_{n}^{k}$ is given as

$$
\bar{\xi}_{n}^{(k)}=\frac{\sum_{f=1}^{F}\sum_{t=1}^{T}\left|\mathcal{M}^{(k)}[f,t]\;X^{(k)}_{1,n,\textrm{dir}}[f,t]\right|^{2}}{\sum_{f=1}^{F}\sum_{t=1}^{T}\left|X^{(k)}_{1,n,\textrm{dir}}[f,t]\right|^{2}},
$$

where $T$ represents the number of time frames and $F$ denotes the number of frequency bins. It should be noted that the mask is computed from the reverberant input and applied only to the direct sound. Therefore, the power ratio is more accurate when the direct-to-reverberant ratio is high.

After obtaining the power ratios, the power pattern for the [NDF](#id35) model is estimated using the entire test set: each source is associated with a direction, and the magnitude-squared spatial response is obtained by averaging across all sources from that direction. Mathematically, the narrowband power pattern for angle $\theta_{p}$ and frequency $f$ is given by

$$
\widehat{\mathcal{P}}[\theta_{p},f]=\frac{1}{|\mathcal{H}_{\theta_{p}}|}\sum_{{(k,n)}\in\mathcal{H}_{\theta_{p}}}\xi_{n}^{(k)}[f],
$$

where $\theta_{p}$ with $p=\{1,2,\ldots,P\}$ is one of $P$ candidate source [DOA](#id5) contained in the test dataset. Similarly, the wideband power pattern $\widehat{\mathcal{P}}[\theta_{p}]$ is given by

$$
\widehat{\mathcal{P}}[\theta_{p}]=\frac{1}{|\mathcal{H}_{\theta_{p}}|}\sum_{(k,n)\in\mathcal{H}_{\theta_{p}}}\bar{\xi}_{n}^{(k)},
$$

where $\mathcal{H}_{\theta_{p}}$ is a set of indices ($k$, $n$) that include all sources in the test dataset that are located in the direction $\theta_{p}$, i.e.,

$$
\mathcal{H}_{\theta_{p}}=\left\{(k,n)\mid\theta^{(k)}_{n}=\theta_{p}\right\},
$$

and $|\mathcal{H}_{\theta_{p}}|$ represents the cardinality of the set $\mathcal{H}_{\theta_{p}}$.

### IV-B Directivity Factor

The original definition of [DF](#id37) describes a fixed beamformer’s ability to suppress a diffuse noise field, and it is defined [^5] as

$$
\widehat{\mathcal{DF}}_{\textrm{original}}=\frac{\left|\mathbf{w}^{H}\mathbf{d}\right|^{2}}{\mathbf{w}^{H}\boldsymbol{\Gamma}\mathbf{w}},
$$

where $\mathbf{w}$ denotes the weights of the conventional beamformer under test, $\mathbf{d}$ is the steering vector of the beamformer, and $\boldsymbol{\Gamma}$ is the spatial coherence matrix for a diffuse noise field. It is often assumed that the late reverberation can be modelled as a diffuse sound field. Consequently, the [DF](#id37) is a measure for the amount of reverberation reduction.

If the beamformer is assumed to be distortionless so that $\left|\mathbf{w}^{H}\mathbf{d}\right|^{2}=1$ [^43], thus (16) can be written as

$$
\begin{split}\widehat{\mathcal{DF}}_{\textrm{original}}&=\frac{1}{\mathbf{w}^{H}\boldsymbol{\Gamma}\mathbf{w}}=\frac{\psi}{\mathbf{w}^{H}\psi\,\boldsymbol{\Gamma}\mathbf{w}},\end{split}
$$

where $\psi$ is the diffuse noise power at the (unprocessed) first microphone, and $\mathbf{w}^{H}\psi\,\boldsymbol{\Gamma}\mathbf{w}$ is the diffuse noise power at the output.

Assuming the [NDF](#id35) is distortionless, we propose the computation method for [DF](#id37) as below

$$
\widehat{\mathcal{DF}}\left[f\right]=\frac{\sum_{k=1}^{K}\sum_{t=1}^{T}\left|Y^{(k)}_{1,\textrm{rvb}}[f,t]\right|^{2}}{\sum_{k=1}^{K}\sum_{t=1}^{T}\left|\mathcal{M}^{(k)}[f,t]Y^{(k)}_{1,\textrm{rvb}}[f,t]\;\right|^{2}},
$$

where $K$ is the number of test samples. The right-hand side of (18) describes the ratio of the power of the reverberant components at the input to that at the output, reflecting the mask’s suppression of reverberant components. It is worth noting that the directivity factor is estimated only from the reverberant component, and the mask is computed from the entire microphone signals. Therefore, the [DF](#id37) is more accurate when the reverberant component and the microphone signals are more similar, i.e., when the direct-to-reverberation ratio is low.

In addition, we can obtain an estimation of [DF](#id37) for the target [VDM](#id42) signal using

$$
\widehat{\mathcal{DF}}_{\mathrm{target}}\left[f\right]=\frac{\sum_{k=1}^{K}\sum_{t=1}^{T}\left|Y^{(k)}_{1,\textrm{rvb}}[f,t]\right|^{2}}{\sum_{k=1}^{K}\sum_{t=1}^{T}\left|Z^{(k)}[f,t]\right|^{2}},
$$

where $Z^{(k)}[f,t]$ is the [VDM](#id42) signal for the $k$ -th test sample.

### IV-C Signal Estimation Quality

We use the standard [SDR](#id25) [^46], SCOREQ [^29], and [PESQ](#id33) ([PESQ](#id33)) [^42], averaged over the test set, to measure the estimated signals’ quality compared to the target [VDM](#id42) signals.

## V Experimental Setup

This section provides a detailed description of the experimental setup, encompassing the array geometry, the target [DMA](#id3) directivity patterns, the datasets, and the training details.

### V-A Array Geometry and DMA Directivity Patterns

We employed a four-microphone array ($Q=4$) comprising three microphones arranged in a [UCA](#id34) ([UCA](#id34)) and an additional microphone at the array center. In this paper, we considered the center microphone as the reference microphone. Unless stated otherwise, all models were trained and tested using a [UCA](#id34) with a diameter of $3\text{\,}\mathrm{cm}$. In this paper, $1^{\textrm{st}}$, $3^{\textrm{rd}}$, and $6^{\textrm{th}}$ order Cardioid directivity patterns in Figure 1, were used to investigate [NDF](#id35).

### V-B Baselines

![[raw/papers/huang-2026-neural-directional-filtering/figures/fig2.png|Refer to caption]]

Refer to caption

To the best of our knowledge, fixed beamformers and parametric spatial filtering are the only effective spatial filtering methods that achieve the desired directivity pattern. Fixed beamformers [^13] [^5] [^3] are designed to capture the sound field using a predefined directivity pattern. However, the achievable pattern is fundamentally limited by the array aperture and the number of microphones. For example, Figure 3 shows the resulting pattern obtained with a least-squares beamformer (LS beamformer) [^30] to target a $3^{\textrm{rd}}$ -order Cardioid pattern, using the microphone array described in Section V-A. The LS beamformer incorporates a minimum [WNG](#id36) constraint of $-15$ $\mathrm{dB}$. As shown, the LS beamformer does not achieve the desired frequency-invariant response, as it suffers from spatial aliasing at high frequencies and exhibits a wider mainlobe at low frequencies, thereby reducing spatial selectivity. For a circular array, the highest achievable order for [DMA](#id3) is limited to $\lfloor\frac{M-1}{2}\rfloor$ [^2], where $M$ is the number of microphones; thus, only the $1^{\textrm{st}}$ -order is achievable for such an array. Therefore, the LS beamformer and a null-constraint [DMA](#id3) [^4] are considered as baselines for the $1^{\textrm{st}}$ -order Cardioid pattern.

Alternatively, parametric directional filtering [^33] [^22] [^36] [^38] [^41] [^23] [^10] [^40] can indeed approximate arbitrary directivity patterns. However, the performance of these approaches highly relies on the accuracy of the [DOA](#id5) and coherence-to-diffuse power ratio estimates, which cannot be precisely obtained above the spatial aliasing frequency. To set aside the influence of estimation errors, we consider a simplified oracle parametric filter as our baseline for experiments in a simulated anechoic environment. Specifically, the parametric filter is computed using oracle DOA estimates that avoid potential artifacts from spatial aliasing, thereby providing an upper bound on its performance.

### V-C Datasets

The training, validation, and test datasets were generated by convolving single-channel source signals with simulated [RIR](#id14). The source signals for the training and validation sets were speech signals taken from the ‘train-clean-360’ and ‘dev-clean’ subsets of the LibriSpeech database [^26], respectively. Finally, all source signals were trimmed/padded (with zeros) to a length of four seconds prior to convolution by the [RIR](#id14).

We used both speech and non-speech test sets to investigate the performance of [NDF](#id35). For the speech test sets, speech utterances were selected from the EARS dataset [^32] with the criterion that their loudness is at least $-42$ dBFS [^20]. To achieve a relatively low proportion of silence within a speech segment, each utterance was then trimmed to a four-second segment that had a higher loudness level than the average loudness level of the original utterance. The non-speech test set used noise signals from the WHAM! dataset [^51] as the source signals. If any sources are shorter than four seconds, we extended them by zero-padding. However, for acoustic scenes containing multiple non-speech sources, the individual signals were trimmed to the length of the shortest source.

Similarly to [^49] [^11], we normalized all convolved signals to have a loudness within $\left[-33,-25\right]$ dBFS. Additionally, we added white Gaussian noise to the array’s microphone signals as self-noise. Unless otherwise specified, the [SNR](#id27) ([SNR](#id27)) for training and testing is $30$ $\mathrm{dB}$ with respect to the mixture of all sources.

#### V-C1 Anechoic environment

We set a fixed source-array distance with $d=1.5$ $\mathrm{m}$ for the anechoic environment.

##### Training datasets

We followed the training strategy described in Section III-C, and used the following parameters. The number of candidate source [DOA](#id5) s for the training and validation sets was restricted to $P_{\textrm{{train}}}$ = 72 with $\theta\in\{0^{\circ},5^{\circ},\ldots,355^{\circ}\}$ and $P_{\textrm{{val}}}$ = 72 with $\theta\in\{2.5^{\circ},7.5^{\circ},\ldots,357.5^{\circ}\}$. For training a static directivity pattern with $\theta_{s}=0$, the training and validation sets for a static directivity pattern consisted of $11520$ and $2880$ training samples, respectively. For training a steerable directivity pattern potential steering directions with $\theta_{\textrm{s}}\in\{0^{\circ},5^{\circ},\ldots,355^{\circ}\}$, we generated $M=72$ target [VDM](#id42) signals for each scene, corresponding to a total of $1440\times 72$ training samples in the training set and $360\times 72$ training samples in the validation set.

##### Test datasets

The number of candidate source [DOA](#id5) s for a test set was restricted to $P_{\textrm{{test}}}=144$ with $\theta\in\{1.25^{\circ},3.75^{\circ},\ldots,358.75^{\circ}\}$. To ensure equal testing for each candidate speaker direction, we generated the test samples by uniformly sampling all candidate directions. Each test sample contained two concurrent speakers. To test the models trained for a static directivity pattern, we generated $3240$ testing samples. To test the models trained for a steerable directivity pattern, we generated six target [VDM](#id42) signals with $\theta_{\textrm{s}}\in\{0^{\circ},30^{\circ},32.5^{\circ},60^{\circ},67.5^{\circ},90^{\circ}\}$.

#### V-C2 Reverberant environment

TABLE I: Ranges for reverberant room acoustic settings

| Length | Width | Height | $\textrm{RT}_{60}$ | Source-array dist. |
| --- | --- | --- | --- | --- |
| 6 - 10 $\mathrm{m}$ | 4 - 8 $\mathrm{m}$ | 3 - 5 $\mathrm{m}$ | 0.2 - 0.5 $\mathrm{s}$ | 0.5 - 2.5 $\mathrm{m}$ |

We simulated each reverberant training sample using the strategy described in Section III-C2 for training, validation, and test sets. The candidate speaker [DOA](#id5) s for the training, validation, and test sets were the same as those in an anechoic environment setting. The source-array distance, room size (length, width, and height), and the $\textrm{RT}_{60}$ are uniformly sampled from the ranges in Table I. The array position in the room was chosen based on the Monte Carlo Room Impulse Response simulation [^16], while ensuring that the sampled position is at least 1.2 $\mathrm{m}$ away from all walls. For the experimental study under reverberant conditions, we only train the models with a static pattern. For a static pattern with $\theta_{s}=0$, the training and validation sets consisted of 50000 and 6000 training samples, respectively. The test sets contained $3240$ test samples. Each test sample contained two concurrent speakers.

### V-D Training Settings and Complexity Analysis

Our earlier research, as described in [^49], has shown that the [NDF](#id35) model trained with two or more concurrently active speakers can generalize to scenarios involving up to six speakers. Since training with more than three speakers did not significantly enhance the model’s performance, we trained our models in this study using mixtures of up to three speakers.

In anechoic environments, [NDF](#id35) models for a static directivity pattern were trained to a maximum of $250$ epochs, while [NDF](#id35) models for steerable directivity patterns or reverberant environments were trained up to $150$ epochs. The learning rate starts at 0.001 and drops by 0.75 every 40 epochs (anechoic) or 20 epochs (others). Training uses a batch size of $10$. To ensure stability, maximum null attenuation is limited to $30$ $\mathrm{dB}$, with $\epsilon$ in (8) and (9) set to $10^{-7}$.

In all the NDF models, the [BiLSTM](#id11) layer contained $256$ hidden units, while the [UniLSTM](#id12) layer contained $128$. The [STFT](#id28) was computed on signal frames of $32$ $\mathrm{ms}$ duration, using a square-root Hann window with a $50\%$ overlap at a sampling frequency of $16$ $\mathrm{kHz}$, resulting in $32$ $\mathrm{ms}$ algorithmic latency. For current settings, the complexity is analyzed in Table II. The complexity for FiLM-JNF (14.121 G) was measured in multiply-accumulate operations (MACs) per second.

TABLE II: Model complexity and RTF: FT-JNF and FiLM-JNF. Python implementation with an ONNX model on an Apple MacBook Pro 2022 M2.

| Model | Total Parameters | Model Size | MACs/s | RTF |
| --- | --- | --- | --- | --- |
| FT-JNF | 874 K | 3.33 MB | 14.116 G | 0.706 |
| FiLM-JNF | 948 K | 3.62 MB | 14.121 G | 0.740 |

## VI Evaluation in Simulated Anechoic Environments

In this section, we analyze the ability of [NDF](#id35) models, trained in simulated anechoic environments, to learn the static [DMA](#id3) patterns and explore mechanisms to achieve a frequency-invariant directivity pattern without spatial aliasing. Furthermore, we demonstrate the steerability of the models and their ability to learn user-defined patterns as well.

### VI-A Static DMA Patterns

Static pattern learning in an anechoic environment, by excluding additional challenges such as steerability and reverberation, provides an ideal experimental setup to explore the underlying processing mechanisms of [NDF](#id35).

#### VI-A1 Loss Function and Baseline Comparison

TABLE III: SDR ($\mathrm{dB}$, $\uparrow$ higher is better), Reference-based SCOREQ  
($\downarrow$ lower is better), and PESQ ($\uparrow$ higher is better) for baseline methods and NDF with two loss functions.

<table><tbody><tr><td></td><td colspan="3">1st-order</td><td colspan="3">3rd-order</td><td colspan="3">6th-order</td></tr><tr><td>Method</td><td>SDR</td><td>SCOREQ</td><td>PESQ</td><td>SDR</td><td>SCOREQ</td><td>PESQ</td><td>SDR</td><td>SCOREQ</td><td>PESQ</td></tr><tr><td>DMA <sup><a href="#fn:4">4</a></sup></td><td>6.25</td><td>1.10</td><td>2.33</td><td>–</td><td>–</td><td>–</td><td>–</td><td>–</td><td>–</td></tr><tr><td>LS Beamformer <sup><a href="#fn:30">30</a></sup></td><td>10.32</td><td>1.22</td><td>2.14</td><td>–</td><td>–</td><td>–</td><td>–</td><td>–</td><td>–</td></tr><tr><td>Parametric Filtering <sup><a href="#fn:23">23</a></sup></td><td>19.80</td><td>0.98</td><td>3.67</td><td>18.62</td><td>0.83</td><td>3.69</td><td>19.03</td><td>0.77</td><td>3.67</td></tr><tr><td>NDF (<math><semantics><msub><mi>ℒ</mi> <mi>SDR</mi></msub> <annotation>\mathcal{L}_{\mathrm{SDR}}</annotation></semantics></math>) <sup><a href="#fn:49">49</a></sup></td><td>27.55</td><td>0.89</td><td>4.43</td><td>25.71</td><td>0.74</td><td>4.39</td><td>25.68</td><td>0.69</td><td>4.38</td></tr><tr><td>NDF (<math><semantics><msub><mi>ℒ</mi> <mn>1</mn></msub> <annotation>\mathcal{L}_{1}</annotation></semantics></math>)</td><td>27.70</td><td>0.89</td><td>4.45</td><td>26.93</td><td>0.74</td><td>4.42</td><td>27.31</td><td>0.69</td><td>4.41</td></tr></tbody></table>

Table III shows the [SDR](#id25), SCOREQ, and [PESQ](#id33) performance of the [NDF](#id35) models trained with the two loss functions described in Section III-B and the baseline systems ([LS](#id9) beamformer and parametric filtering) as described in Section V-B. We observe that the NDF models consistently outperform the baseline methods. The $3^{\textrm{rd}}$ - and $6^{\textrm{th}}$ -order patterns cannot be accurately approximated using the LS beamformer or DMA for the chosen compact array geometry as discussed in Section V-B; hence, the corresponding entries are left blank, but the [NDF](#id35) models can learn these higher-order patterns, as shown in Figure 4. Table III also shows that the [NDF](#id35) model trained with the proposed batch-aggregated, normalized $\mathcal{L}_{\textrm{1}}$ -loss function has better [SDR](#id25) and [PESQ](#id33) compared to the model trained with $\mathcal{L}_{\textrm{SDR}}$ for the $3^{\textrm{rd}}$ - and $6^{\textrm{th}}$ -order patterns, while the two models have similar performance for the $1^{\textrm{st}}$ -order pattern. Consequently, we use the $\mathcal{L}_{\textrm{1}}$ loss function for training the [NDF](#id35) models in the following experiments.

![[raw/papers/huang-2026-neural-directional-filtering/figures/fig3.png|Refer to caption]]

Refer to caption

#### VI-A2 Power Patterns and Frequency Processing Mechanisms

Fig. 5: Bandpass analysis of the [NDF](#id35) models to study the frequency processing mechanisms.

![[raw/papers/huang-2026-neural-directional-filtering/figures/fig4.png|Refer to caption]]

Refer to caption

Figure 4 shows the power pattern estimates for the $3^{\textrm{rd}}$ - and $6^{\textrm{th}}$ -order patterns. The [NDF](#id35) effectively learns the mainlobe of these highly directive patterns, demonstrating strong spatial modeling capabilities. However, the null positions exhibit larger deviations. The narrowband results further indicate that the learned mainlobe patterns are largely frequency-invariant. This observation motivates a closer examination of the [NDF](#id35) model’s frequency processing mechanisms. Specifically, we aim to determine whether the model processes each frequency band primarily using local information or exploiting cross-band spectral structure. Furthermore, we investigate whether the observed frequency invariance of the learned patterns persists at frequencies well above the aliasing limit, thereby mitigating spatial aliasing effects. To this end, we employ a microphone array with a diameter of 6 $\mathrm{cm}$ for the subsequent experiments. With this configuration, spatial aliasing begins above 5.6 $\mathrm{kHz}$, allowing us to test the model’s performance under narrowband conditions both below and above this frequency. The model is trained and evaluated using data corresponding to this larger array.

We designed the experiment shown in Figure 5. We use the speech test sets described in Section V-C, and the corresponding microphone array signals undergo bandpass filtering before being processed by the [NDF](#id35) model, which was trained using broadband speech signals. Based on preliminary studies, we set the bandwidth of the bandpass filter to 500 $\mathrm{Hz}$. The mask provided by the [NDF](#id35) model is then applied to the unprocessed reference microphone signal. In this way, we can force the [NDF](#id35) model to use limited frequency bands.

As shown in Figures 6 (a) and (b), when a bandpass signal centered at $1$ $\mathrm{kHz}$ is input into the [NDF](#id35) model, the estimated patterns, using this narrowband spectral information, successfully match a desired $1^{\textrm{st}}$ -order pattern. However, when a bandpass signal at $7$ $\mathrm{kHz}$ is provided, as shown in Figures 6 (c) and (d), the [NDF](#id35) model fails to approximate a target $1^{\textrm{st}}$ -order pattern rendering a distorted power pattern due to spatial aliasing and a deformed mainlobe. In the following experiment, we provide the model with a signal featuring a band at 7 $\mathrm{kHz}$ and the entire spectral information below 5.6 $\mathrm{kHz}$. Figures 6 (e) and (f) show that the [NDF](#id35) output no longer exhibits spatial aliasing at 7 $\mathrm{kHz}$ and effectively yields the target pattern. However, as demonstrated in Figures 6 (g) and (h), when the model is provided a signal with two bands at $1$ $\mathrm{kHz}$ and $7$ $\mathrm{kHz}$, spatial aliasing is observed at $7$ $\mathrm{kHz}$.

These experiments show that the NDF model can effectively achieve a frequency-invariant pattern, and that information below the spatial aliasing frequency facilitates this. At higher frequencies where spatial aliasing occurs, the model appears to resolve ambiguities when broadband spectral context is available, suggesting frequency-dependent processing. Leveraging low-frequency components to mitigate aliasing at high frequencies is found in classical signal processing; e.g., [^31] adopts a low-to-high subband multistage scheme, in which outputs from lower-frequency stages are propagated to higher-frequency stages to resolve high-frequency aliasing. Although the underlying mechanism of these behaviors in the DNN model is not yet fully understood, two factors may contribute. First, the model may exploit spectral source characteristics: cross-band dependencies in broadband sources, analogous to those in single-channel source separation, could provide contextual cues that help resolve ambiguous inter-microphone phase relationships at individual frequencies. Second, the model may exploit the geometry of aliasing itself: while inter-microphone phase differences no longer map uniquely to incident angles above the aliasing frequency, each angle still produces a distinct phase difference at each frequency, and the set of aliased angles varies with frequency while the true angle remains constant. Consequently, integrating phase information across frequencies may geometrically constrain the true angle of arrival. We emphasize that these are hypothesized contributing factors; the observed robustness of the learned patterns above the aliasing frequency is an empirical finding rather than a theoretical guarantee that spatial aliasing has been resolved. The ability of [FT-JNF](#id23) for spatial aliasing reduction is also studied in the context of target speaker extraction in [^25].

#### VI-A3 Non-Speech Sources

![[raw/papers/huang-2026-neural-directional-filtering/figures/fig5.png|Refer to caption]]

Refer to caption

To verify if [NDF](#id35) models may generalize to signals with unseen spectral characteristics in the training, we evaluate the [NDF](#id35) models on non-speech test sets defined in Section V-C. Figure 7 shows the narrowband and wideband power patterns estimated using non-speech test sets for $3^{\textrm{rd}}$ -order and $6^{\textrm{th}}$ -order patterns. Although the deviations of the estimated patterns in Figure 7 are greater than those observed in Figure 4 (which was obtained using speech sources), the estimated power patterns maintain a good mainlobe approximation. This result demonstrates that speech-trained [NDF](#id35) models can still perform directional filtering with the desired pattern, even for previously unseen non-speech noise sources. Thus, we conclude that the NDF models generalize to unseen sources during training. In other words, even when the spectral features of speech are absent, the NDF models can still extract and exploit the necessary spatial features based on the spectrum of non-speech signals.

#### VI-A4 Array Aperture

![[raw/papers/huang-2026-neural-directional-filtering/figures/fig6.png|Refer to caption]]

Refer to caption

TABLE IV: SDR ($\mathrm{dB}$) and PESQ of NDF models trained for arrays with different diameters (SNR = $30\text{\,}\mathrm{dB}$).

<table><tbody><tr><td></td><td colspan="2"><math><semantics><mrow><mn>3</mn> <mi>cm</mi></mrow> <annotation>3\text{\,}\mathrm{cm}</annotation></semantics></math></td><td colspan="2"><math><semantics><mrow><mn>6</mn> <mi>cm</mi></mrow> <annotation>6\text{\,}\mathrm{cm}</annotation></semantics></math></td><td colspan="2"><math><semantics><mrow><mn>9</mn> <mi>cm</mi></mrow> <annotation>9\text{\,}\mathrm{cm}</annotation></semantics></math></td></tr><tr><td>Power Pattern</td><td>SDR</td><td>PESQ</td><td>SDR</td><td>PESQ</td><td>SDR</td><td>PESQ</td></tr><tr><td>1st-order</td><td>27.70</td><td>4.45</td><td>29.61</td><td>4.47</td><td>30.43</td><td>4.48</td></tr><tr><td>3rd-order</td><td>26.93</td><td>4.42</td><td>28.85</td><td>4.45</td><td>29.45</td><td>4.46</td></tr><tr><td>6th-order</td><td>27.31</td><td>4.41</td><td>28.93</td><td>4.44</td><td>29.49</td><td>4.45</td></tr></tbody></table>

We investigate spatial aliasing in Section VI-A2 for a [UCA](#id34) with a diameter of 6 $\mathrm{cm}$. Since the array diameter often affects the performance of fixed beamforming [^18] [^54], we investigated how the array diameter affects the performance of the [NDF](#id35) models. To this end, we trained [NDF](#id35) models with array diameters of 3 $\mathrm{cm}$, 6 $\mathrm{cm}$, and 9 $\mathrm{cm}$, and evaluated each model using test sets generated for the corresponding diameter. For both training and testing, the [SNR](#id27) was set to 30 $\mathrm{dB}$.

Table IV shows that the [SDR](#id25) and [PESQ](#id33) improve as the diameter increases. This observation raises the question: Is a larger diameter always better? To investigate this further, we increase the microphone sensor noise in the test sets, reducing the [SNR](#id27) to 20 $\mathrm{dB}$ and 10 $\mathrm{dB}$ while maintaining the models trained at a [SNR](#id27) of 30 $\mathrm{dB}$. As depicted in Figure 8, using the $1$ st-order pattern as an example, we observe that at an SNR of $20$ $\mathrm{dB}$, the estimated patterns remain consistent across different diameters. At an [SNR](#id27) of $10$ $\mathrm{dB}$, the [NDF](#id35) renders an omnidirectional response at very low frequencies, and its response is actually larger than 0 $\mathrm{dB}$ (e.g., up to 3.5 $\mathrm{dB}$ for $r=3$ $\mathrm{cm}$). This phenomenon is similar to the white-noise amplification issue observed in some fixed beamformers, such as [DMA](#id3) and superdirective beamformers [^3]. It is noted that the 3 $\mathrm{cm}$ diameter array has a more severe amplification problem than the 9 $\mathrm{cm}$ diameter array. However, as the diameter increases, particularly at $9$ $\mathrm{cm}$, the [NDF](#id35) model no longer maintains a frequency-invariant pattern at high frequencies for an [SNR](#id27) of $10$ $\mathrm{dB}$. Therefore, under low [SNR](#id27) conditions, a smaller diameter preserves the frequency-invariant shape of the estimated patterns at high frequencies. In comparison, a larger diameter enhances the robustness of low frequencies and exhibits better SDR.

### VI-B Steerable DMA Patterns

TABLE V: Performance of steerable [NDF](#id35) models across various orders.

<table><tbody><tr><td></td><td colspan="9">Pattern</td></tr><tr><td>Angle</td><td colspan="3">1st-order</td><td colspan="3">3rd-order</td><td colspan="3">6th-order</td></tr><tr><td></td><td>SDR</td><td>SCOREQ</td><td>PESQ</td><td>SDR</td><td>SCOREQ</td><td>PESQ</td><td>SDR</td><td>SCOREQ</td><td>PESQ</td></tr><tr><td><math><semantics><msup><mn>0</mn> <mo>∘</mo></msup> <annotation>0^{\circ}</annotation></semantics></math></td><td>27.67</td><td>0.89</td><td>4.45</td><td>24.75</td><td>0.74</td><td>4.40</td><td>25.73</td><td>0.69</td><td>4.39</td></tr><tr><td><math><semantics><msup><mn>30</mn> <mo>∘</mo></msup> <annotation>30^{\circ}</annotation></semantics></math></td><td>27.72</td><td>0.89</td><td>4.45</td><td>25.17</td><td>0.74</td><td>4.40</td><td>26.25</td><td>0.69</td><td>4.39</td></tr><tr><td><math><semantics><msup><mn>32.5</mn> <mo>∘</mo></msup> <annotation>32.5^{\circ}</annotation></semantics></math></td><td>27.70</td><td>0.89</td><td>4.45</td><td>25.16</td><td>0.74</td><td>4.40</td><td>26.25</td><td>0.69</td><td>4.39</td></tr><tr><td><math><semantics><msup><mn>60</mn> <mo>∘</mo></msup> <annotation>60^{\circ}</annotation></semantics></math></td><td>27.66</td><td>0.89</td><td>4.45</td><td>24.94</td><td>0.74</td><td>4.39</td><td>26.22</td><td>0.69</td><td>4.38</td></tr><tr><td><math><semantics><msup><mn>67.5</mn> <mo>∘</mo></msup> <annotation>67.5^{\circ}</annotation></semantics></math></td><td>27.68</td><td>0.89</td><td>4.45</td><td>24.92</td><td>0.74</td><td>4.39</td><td>26.19</td><td>0.69</td><td>4.38</td></tr><tr><td><math><semantics><msup><mn>90</mn> <mo>∘</mo></msup> <annotation>90^{\circ}</annotation></semantics></math></td><td>27.67</td><td>0.89</td><td>4.45</td><td>24.72</td><td>0.74</td><td>4.40</td><td>26.21</td><td>0.69</td><td>4.39</td></tr></tbody></table>

![[raw/papers/huang-2026-neural-directional-filtering/figures/fig7.png|Refer to caption]]

Refer to caption

We trained three [NDF](#id35) models with steering mechanism for the $1^{\textrm{st}}$ -, $3^{\textrm{rd}}$ -, and $6^{\textrm{th}}$ -order patterns. Table V shows the [SDR](#id25), SCOREQ, and [PESQ](#id33) performance of the models with the main lobe steered towards $\theta_{\textrm{s}}\in\{0^{\circ},30^{\circ},32.5^{\circ},60^{\circ},67.5^{\circ},90^{\circ}\}$. The narrowband power pattern estimates for the $6^{\textrm{th}}$ -order pattern for $\theta_{\textrm{s}}\in\{32.5^{\circ},90^{\circ}\}$ are shown in Figure 9. We observe that the steerable [NDF](#id35) models achieve similar performance across different steering directions and maintain frequency-invariance, even though $32.5^{\circ}$ and $67.5^{\circ}$ are not included during training.

### VI-C Patterns with User-defined Shapes

![[raw/papers/huang-2026-neural-directional-filtering/figures/fig8.png|Refer to caption]]

Refer to caption

The shape of a specific pattern trained for [NDF](#id35) is determined solely by the target [VDM](#id42) signal, and the architecture or the loss function is not confined to one particular pattern. To illustrate this, we explore the learning of patterns with user-defined shapes. Figure 10 shows the explored target patterns. The first pattern in Figures 10 (a) and (b) has two mainlobes of widths $20^{\circ}$ and $30^{\circ}$ with $0$ $\mathrm{dB}$ attenuation, and a broad null region, while the second pattern in Figures 10 (c) and (d) has a step-like spatial pattern with sharp transitions in the attenuation levels and a null towards $180^{\circ}$. From Figure 10, we observe that the unattenuated regions in both patterns are well approximated in a frequency-invariant manner, with a gradual transition at the boundaries. However, the attenuation towards the null direction is limited to $-25$ $\mathrm{dB}$, and the variance of the estimated pattern increases for attenuation levels beyond $-15$ $\mathrm{dB}$, similar to the observations made for the DMA patterns.

## VII Evaluation in Simulated Reverberant Environment

In this section, we present a comparative study of the [NDF](#id35) models trained on anechoic and reverberant datasets, referred to as A-Model and R-Model, respectively. The study utilizes the directivity factor to measure the mask’s impact on reverberant components, in conjunction with the power pattern and metrics reported in previous sections.

### VII-A Signal Estimation Quality

TABLE VI: SDR ($\mathrm{dB}$), SCOREQ, and PESQ on reverberant test sets.

<table><tbody><tr><td colspan="2"></td><td colspan="9"><math><semantics><msub><mi>RT</mi> <mn>60</mn></msub> <annotation>\mathrm{RT}_{60}</annotation></semantics></math> (s)</td></tr><tr><td>Method</td><td>Pattern</td><td colspan="3">0.2</td><td colspan="3">0.4</td><td colspan="3">0.6</td></tr><tr><td></td><td></td><td>SDR</td><td>SCOREQ</td><td>PESQ</td><td>SDR</td><td>SCOREQ</td><td>PESQ</td><td>SDR</td><td>SCOREQ</td><td>PESQ</td></tr><tr><td>DMA <sup><a href="#fn:4">4</a></sup></td><td>1st-order</td><td><math><semantics><mn>6.82</mn> <annotation>6.82</annotation></semantics></math></td><td>0.97</td><td>2.48</td><td><math><semantics><mn>7.71</mn> <annotation>7.71</annotation></semantics></math></td><td>0.80</td><td>2.77</td><td><math><semantics><mn>7.92</mn> <annotation>7.92</annotation></semantics></math></td><td>0.71</td><td>2.88</td></tr><tr><td>LS Beamformer <sup><a href="#fn:30">30</a></sup></td><td>1st-order</td><td><math><semantics><mn>10.83</mn> <annotation>10.83</annotation></semantics></math></td><td>1.13</td><td>2.30</td><td><math><semantics><mn>11.62</mn> <annotation>11.62</annotation></semantics></math></td><td>0.98</td><td>2.67</td><td><math><semantics><mn>11.78</mn> <annotation>11.78</annotation></semantics></math></td><td>0.87</td><td>2.86</td></tr><tr><td rowspan="3">NDF A-Models</td><td>1st-order</td><td><math><semantics><mn>19.43</mn> <annotation>19.43</annotation></semantics></math></td><td>0.79</td><td>4.26</td><td><math><semantics><mn>18.23</mn> <annotation>18.23</annotation></semantics></math></td><td>0.61</td><td>4.31</td><td><math><semantics><mn>17.75</mn> <annotation>17.75</annotation></semantics></math></td><td>0.52</td><td>4.31</td></tr><tr><td>3rd-order</td><td><math><semantics><mn>11.81</mn> <annotation>11.81</annotation></semantics></math></td><td>0.72</td><td>3.84</td><td><math><semantics><mn>9.27</mn> <annotation>9.27</annotation></semantics></math></td><td>0.60</td><td>3.83</td><td><math><semantics><mn>8.59</mn> <annotation>8.59</annotation></semantics></math></td><td>0.52</td><td>3.83</td></tr><tr><td>6th-order</td><td><math><semantics><mn>8.34</mn> <annotation>8.34</annotation></semantics></math></td><td>0.68</td><td>3.54</td><td><math><semantics><mn>5.64</mn> <annotation>5.64</annotation></semantics></math></td><td>0.61</td><td>3.35</td><td><math><semantics><mn>4.90</mn> <annotation>4.90</annotation></semantics></math></td><td>0.53</td><td>3.31</td></tr><tr><td rowspan="3">NDF R-Models</td><td>1st-order</td><td><math><semantics><mn>22.12</mn> <annotation>22.12</annotation></semantics></math></td><td>0.78</td><td>4.38</td><td><math><semantics><mn>20.37</mn> <annotation>20.37</annotation></semantics></math></td><td>0.60</td><td>4.40</td><td><math><semantics><mn>19.70</mn> <annotation>19.70</annotation></semantics></math></td><td>0.51</td><td>4.40</td></tr><tr><td>3rd-order</td><td><math><semantics><mn>14.30</mn> <annotation>14.30</annotation></semantics></math></td><td>0.69</td><td>4.06</td><td><math><semantics><mn>11.59</mn> <annotation>11.59</annotation></semantics></math></td><td>0.56</td><td>4.05</td><td><math><semantics><mn>10.74</mn> <annotation>10.74</annotation></semantics></math></td><td>0.49</td><td>4.03</td></tr><tr><td>6th-order</td><td><math><semantics><mn>10.58</mn> <annotation>10.58</annotation></semantics></math></td><td>0.65</td><td>3.79</td><td><math><semantics><mn>7.77</mn> <annotation>7.77</annotation></semantics></math></td><td>0.55</td><td>3.65</td><td><math><semantics><mn>6.92</mn> <annotation>6.92</annotation></semantics></math></td><td>0.48</td><td>3.59</td></tr></tbody></table>

Table VI shows a comparison of the [SDR](#id25), SCOREQ, and [PESQ](#id33) achieved by the R-Model, A-Model, and the baselines (DMA and [LS](#id9) beamformer [^30]) for reverberation times 0.2 $\mathrm{s}$   0.4 $\mathrm{s}$, and 0.6 $\mathrm{s}$. We observe that both the R-Model and A-Model outperform baselines under various reverberation conditions, underscoring the effectiveness of the [NDF](#id35) models, and the R-Models consistently achieved better performance than the A-Models across different reverberation conditions, regardless of the order of the learned patterns. This illustrates the effectiveness of our training strategy for reverberant environments. However, the [SDR](#id25) and [PESQ](#id33) performance greatly depends on the order of the pattern, and the reverberation time has a relatively small effect.

### VII-B Power Patterns

(a) $\textrm{RT}_{60}=0.2$ $\mathrm{s}$

(b) $\textrm{RT}_{60}=0.6$ $\mathrm{s}$

(c) $\textrm{RT}_{60}=0.2$ $\mathrm{s}$

(d) $\textrm{RT}_{60}=0.6$ $\mathrm{s}$

Fig. 11: Comparison of the estimated wideband power patterns for the A-Model and R-Model. The source-array distances were fixed at 1 $\mathrm{m}$. The top and bottom rows correspond to the $1^{\textrm{st}}$ -order and $6^{\textrm{th}}$ -order patterns, respectively.

![[raw/papers/huang-2026-neural-directional-filtering/figures/fig9.png|Refer to caption]]

Refer to caption

We further analyze the obtained power patterns of R-Models and A-Models in environments with low reverberation ($\textrm{RT}_{60}$ = $0.2$ $\mathrm{s}$) and high reverberation ($\textrm{RT}_{60}$ = $0.6$ $\mathrm{s}$). To effectively investigate the impact of masks on the direct-path components used to estimate the power patterns, we set the two concurrent speakers in each test sample at a fixed source-array distance of 1 $\mathrm{m}$. This distance results in a positive direct-to-reverberation ratio (DRR). Figure 11 compares the estimated wideband power patterns for the A-Model and R-Model, respectively. For the $1^{\textrm{st}}$ -order pattern, the pattern estimation performance of both models is similar, which suggests that for lower-order patterns (and thus easier to learn), the A-Model, trained in non-reverberant conditions, has a similar capability to handle direct-path components as the R-Model. This phenomenon is also observed for a reverberation time of 0.2 $\mathrm{s}$. However, for the $6^{\textrm{th}}$ -order patterns in longer reverberation time (0.6 $\mathrm{s}$), the R-Models demonstrate a higher suppression of direct-path sound in the region surrounding the null position than the A-Model. Figure 12 shows the approximated narrowband power patterns for $1^{\textrm{st}}$ -order under $\textrm{RT}_{60}=0.2$ $\mathrm{s}$ and for $6^{\textrm{th}}$ -order under $\textrm{RT}_{60}=0.6$ $\mathrm{s}$, which represent the easiest and most challenging setting, respectively. These results also show that the estimated power patterns in reverberant environments remain frequency-invariant.

(a) $1^{\textrm{st}}$ -order pattern, $\textrm{RT}_{60}=0.2$ $\mathrm{s}$

(b) $6^{\textrm{th}}$ -order pattern, $\textrm{RT}_{60}=0.2$ $\mathrm{s}$

(c) $1^{\textrm{st}}$ -order pattern, $\textrm{RT}_{60}=0.6$ $\mathrm{s}$

(d) $6^{\textrm{th}}$ -order pattern, $\textrm{RT}_{60}=0.6$ $\mathrm{s}$

Fig. 13: Estimated DF comparison between R-Model and A-Model. The source-array distances are fixed at 2.5 $\mathrm{m}$.

### VII-C Directivity Factor

We now focus on the [DF](#id37) obtained by the [NDF](#id35) models. As the [DF](#id37) is computed based on the reverberant components, we set the source-array distance to 2.5 $\mathrm{m}$ (low DRR condition). Figure 13 shows the frequency-dependent [DF](#id37) of the A-Models and R-Models trained for $1^{\textrm{st}}$ -order and $6^{\textrm{th}}$ -order patterns and evaluated in simulated rooms with a reverberation time of $0.2$ and $0.6$ $\mathrm{s}$. We observe the following: Firstly, the R-Model mostly outperforms the A-Model in terms of [DF](#id37), particularly for higher reverberation time, which aligns with the signal quality results in Table VI. Secondly, as the reverberation time increases, the [DF](#id37) of both models tends to increase; however, the R-Model exhibits a higher increase. Under the condition of $\textrm{RT}_{60}=0.6~$\mathrm{s}$$, the [DF](#id37) of the R-Model tends to approach or even surpass the [DF](#id37) of the [VDM](#id42) target. This indicates that the R-Model tends to slightly over-suppress reverberation under $\textrm{RT}_{60}=0.6~$\mathrm{s}$$ that is more reverberant than the highest $\textrm{RT}_{60}=0.5~$\mathrm{s}$$ encountered during its training. Notably, the [DF](#id37) estimates are expected to be more accurate in higher reverberation conditions. Therefore, this further demonstrates that the R-Model has better capabilities to handle reverberation. Thirdly, the [DF](#id37) calculated for the target [VDM](#id42) closely matched the theoretical [DF](#id37) values of the various target patterns, particularly the $1^{\textrm{st}}$ -order pattern or $\textrm{RT}_{60}=0.6~$\mathrm{s}$$. This demonstrates the accuracy of the proposed DF computation for the target [VDM](#id42).

## VIII Applications with Moving Sources

In the [NDF](#id35) training strategy presented in Section III, the speech sources are assumed to be stationary during training. Therefore, the evaluation in Sections V-VII focused on stationary source scenarios. In this section, we illustrate the performance of [NDF](#id35) models trained using static sources in a moving source scenario. We consider two application scenarios: a mono audio recording in a simulated environment and a stereo audio recording in a real room. Audio examples can be found online <sup>1</sup>.

### VIII-A Mono Audio Recording

Fig. 14: Simulated two-source scenario with a static speech source and a moving music source. The source at $0^{\circ}$ was static, while the moving source completes a full circle around the array in the clockwise direction.The source-array distance was $1.5$ $\mathrm{m}$.

![[raw/papers/huang-2026-neural-directional-filtering/figures/fig10.png|Refer to caption]]

Fig. 15: Spectrograms comparison for a simulated moving scenario.

The acoustic scene and recording setup for this scenario are depicted in Figure 14, which contains two sources: a stationary speech source and a moving music source, both coplanar with the microphone array, at a fixed distance of $1.5$ $\mathrm{m}$ from the array center. The stationary source is located at $0^{\circ}$, and the moving source completes one full rotation around the array in approximately $18$ $\mathrm{s}$ at a constant speed. The simulated room is 5 $\mathrm{m}$ x 4 $\mathrm{m}$ x 3.5 $\mathrm{m}$ and has an $\textrm{RT}_{60}$ of 0.15 $\mathrm{s}$. The [NDF](#id35) model, trained in anechoic environments with a static $1^{\textrm{st}}$ -order Cardioid pattern pointing at $0^{\circ}$, is used for demonstration.

Figures 15 (a) and (b) show the spectrograms of the mixture signal at the reference microphone and the target [VDM](#id42) signal, respectively. In the target [VDM](#id42) signal, we observe that the amplitude of the music signal gradually decreases as it moves towards the null direction ($180^{\circ}$), followed by a gradual restoration to the original levels as it completes a full rotation, consistent with the desired spatial response. Figure 15 (c) shows the [NDF](#id35) output, which follows the target [VDM](#id42) signal, except for a slightly stronger suppression of the music source at higher frequencies and near the null direction. Notably, the speech signals at the desired direction for both (b) and (c) remain undistorted.

### VIII-B Stereo Audio Recording

A stereo audio recording can be made using two co-located $1^{\textrm{st}}$ -order Cardioid microphones pointing to $45^{\circ}$ and $135^{\circ}$ [^52]. We investigate the application of the [NDF](#id35) to perform a stereo audio recording. To this end, we enacted the acoustic scene in a real room ($4.6~$\mathrm{m}$\times 4.5~$\mathrm{m}$\times 2.6~$\mathrm{m}$$) with $\textrm{RT}_{60}=0.23$ $\mathrm{s}$, depicted in Figure 16. As shown, the scene consisted of a real male speaker going from $0^{\circ}$ to $180^{\circ}$ in a clockwise direction, moving for approximately 8 $\mathrm{s}$ while maintaining an approximate distance of 1.5 $\mathrm{m}$ from the array center. The recording was processed with the $1^{\textrm{st}}$ -order Cardioid steerable NDF model steered towards $45^{\circ}$ and $135^{\circ}$, and the resulting audio outputs were assigned to the left and right channels of the stereo audio.

Figure 17 shows the segmental amplitude difference between the left and right channels, computed using segments of duration 1 $\mathrm{s}$ with a $75\%$ overlap between successive segments. We see that the level differences between the left and right channels of the stereo recording are effectively captured in the [NDF](#id35) outputs, with a measured difference of 16 $\mathrm{dB}$. However, there is still a gap compared to the theoretical value. Theoretically, a Cardioid pattern could exhibit strong suppression near the null positions, a capability that is not fully realized in practice.

Fig. 16: The scenario for stereo audio recording. One active speaker is moving from $0^{\circ}$ to $180^{\circ}$ with a fixed distance of $1.5$ m. $\theta_{\textrm{L}}=45^{\circ}$ and $\theta_{\textrm{R}}=135^{\circ}$ stand for two different steering directions of the power pattern. The power pattern learned by [NDF](#id35) is $1^{\textrm{st}}$ -order Cardioid pattern.

Fig. 17: Amplitude difference between left channel and right channel. In a real room with $\textrm{RT}_{60}=0.23$ $\mathrm{s}$.

## IX Conclusions

Neural directional filtering (NDF) offers a viable solution for a challenging task: capturing sound with a controllable directivity pattern using a compact microphone array. In this paper, we introduce an effective training strategy that enables the NDF model to learn different patterns and enhances its ability to operate in reverberant environments. We analyzed the performance of [NDF](#id35) on both direct-path components and reverberant components of reverberant signals, utilizing estimated direction patterns and directivity factors. Additionally, we conduct a comprehensive study on the processing mechanisms and characteristics, including its pattern learning capabilities (such as the ability to maintain frequency-invariant patterns, mitigate spatial aliasing, learn high-order DMA patterns, and user-defined patterns), as well as its applications to moving sources.

## Acknowledgments

The authors gratefully acknowledge the scientific support and HPC resources provided by the Erlangen National High Performance Computing Center (NHR@FAU) of the Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU). The hardware is funded by the German Research Foundation (DFG). The authors thank Mr. Julian Wechsler for his contributions to the initial work.

[^1]: Y. Avargel and I. Cohen (2007) On multiplicative transfer function approximation in the short-time fourier transform domain. IEEE Sig. Proc. Lett. 14 (5), pp. 337–340. Cited by: §II.

[^2]: J. Benesty, J. Chen, and I. Cohen (2015) Design of circular differential microphone arrays. Vol. 12, Springer. Cited by: §V-B.

[^3]: J. Benesty, I. Cohen, and J. Chen (2018) Fixed beamforming. Fundamentals of Signal Enhancement and Array Signal Processing, pp. 237–282. Cited by: §I, §V-B, §VI-A4.

[^4]: J. Benesty and C. Jingdong (2012) Study and design of differential microphone arrays. Vol. 6, Springer Science & Business Media. Cited by: §I, §V-B, TABLE III, TABLE VI.

[^5]: M. Brandstein and D. Ward (2001) Microphone arrays: signal processing techniques and applications. Springer Science & Business Media. Cited by: §I, §IV-B, §V-B.

[^6]: S. Braun and M. Frank (2011) Localization of 3d ambisonic recordings and ambisonic virtual sources. In 1st International Conference on Spatial Audio,(Detmold), Cited by: §I.

[^7]: S. Braun, O. Thiergart, and E. A. P. Habets (2014) Automatic spatial gain control for an informed spatial filter. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 830–834. Cited by: §I.

[^8]: A. Briegleb, T. Haubner, V. Belagiannis, and W. Kellermann (2023) Localizing spatial information in neural spatiospectral filters. In 2023 31st European Signal Processing Conference (EUSIPCO), pp. 920–924. Cited by: §I.

[^9]: A. Briegleb and W. Kellermann (2024) Analysis of spatial filtering in neural spatiospectral filters and its dependence on training target characteristics. EURASIP Journal on Audio, Speech, and Music Processing 2024 (1), pp. 61. Cited by: §I.

[^10]: S. Chakrabarty and E. A. P. Habets (2017) A Bayesian approach to informed spatial filtering with robustness against DOA estimation errors. IEEE Trans. Aud., Sp., Lang. Proc. 26 (1), pp. 145–160. Cited by: §I, §V-B.

[^11]: J. Cosentino, M. Pariente, S. Cornell, A. Deleforge, and E. Vincent (2020) LibriMix: an open-source dataset for generalizable speech separation. External Links: [Document](https://dx.doi.org/10.48550/arXiv.2005.11262) Cited by: §V-C.

[^12]: J. Eargle (2012) The microphone book: from mono to stereo to surround-a guide to microphone design and application. Routledge. Cited by: §II.

[^13]: G. W. Elko (2000) Superdirectional microphone arrays. Acoustic signal processing for telecommunication, pp. 181–237. Cited by: §I, §II, §II, §V-B.

[^14]: R. Gu, S. Zhang, Y. Zou, and D. Yu (2021) Complex neural spatial filter: enhancing multi-channel target speech separation in complex domain. IEEE Sig. Proc. Lett. 28, pp. 1370–1374. Cited by: §I.

[^15]: E. A. P. Habets (2020) RIR generator. Note: [https://github.com/ehabets/RIR-Generator](https://github.com/ehabets/RIR-Generator) commit 3cf914d Cited by: §III-C1.

[^16]: E. A. P. Habets (2026) Monte carlo RIR simulation. Note: [https://github.com/audiolabs/MonteCarloRIRSimulation](https://github.com/audiolabs/MonteCarloRIRSimulation) commit d464a10 Cited by: §V-C2.

[^17]: M. M. Halimeh and W. Kellermann (2022) Complex-valued spatial autoencoders for multichannel speech enhancement. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 261–265. Cited by: §I.

[^18]: W. Huang and J. Feng (2020) Differential beamforming for uniform circular array with directional microphones. In Proc. Interspeech, pp. 71–75. Cited by: §VI-A4.

[^19]: W. Huang, M. M. Halimeh, S. R. Chetupalli, O. Thiergart, and E. A. Habets (2025) Steerable neural directional filtering. In Proc. of the Forum Acusticum Euronoise, European Acoustics Association, Cited by: §III-A.

[^20]: ITU-R (2023) Recommendation ITU-R BS.1770-5: algorithms to measure audio programme loudness and true-peak audio level. Cited by: §V-C.

[^21]: F. Jacobsen and T. Roisin (2000) The coherence of reverberant sound fields. J. Ac. Soc. Am. 108 (1), pp. 204–210. Cited by: §I.

[^22]: M. Kallinger, G. Del Galdo, F. Kuech, D. Mahne, and R. Schultz-Amling (2009) Spatial filtering using directional audio coding parameters. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 217–220. Cited by: §I, §V-B.

[^23]: K. Kowalczyk, O. Thiergart, M. Taseska, G. Del Galdo, V. Pulkki, and E. A. P. Habets (2015) Parametric Spatial Sound Processing: a flexible and efficient solution to sound scene acquisition, modification, and reproduction. IEEE Sig. Proc. Mag. 32 (2), pp. 31–42. External Links: [Document](https://dx.doi.org/10.1109/MSP.2014.2369531) Cited by: §I, §V-B, TABLE III.

[^24]: F. Kuech, M. Kallinger, R. Schultz-Amling, G. del Galdo, J. Ahonen, and V. Pulkki (2008) Directional audio coding using planar microphone arrays. In 2008 Hands-Free Speech Communication and Microphone Arrays, Vol., pp. 37–40. External Links: [Document](https://dx.doi.org/10.1109/HSCMA.2008.4538682) Cited by: §I.

[^25]: A. Mannanova, J. Kienegger, and T. Gerkmann (2025) An analysis of joint nonlinear spatial filtering for spatial aliasing reduction. arXiv preprint arXiv:2509.25982. Cited by: §VI-A2.

[^26]: V. Panayotov, G. Chen, D. Povey, and S. Khudanpur (2015) LibriSpeech: an ASR corpus based on public domain audio books. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 5206–5210. External Links: [Document](https://dx.doi.org/10.1109/ICASSP.2015.7178964) Cited by: §V-C.

[^27]: A. Pandey and D. Wang (2018) On adversarial training and loss functions for speech enhancement. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 5414–5418. Cited by: §III-B.

[^28]: E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville (2018) FiLM: visual reasoning with a general conditioning layer. In Proc. AAAI Conference on Artificial Intelligence, Vol. 32. Cited by: §III-A.

[^29]: A. Ragano, J. Skoglund, and A. Hines (2024) SCOREQ: speech quality assessment with contrastive regression. Advances in Neural Information Processing Systems 37, pp. 105702–105729. Cited by: §IV-C.

[^30]: E. Rasumow et al. (2016) Regularization approaches for synthesizing HRTF directivity patterns. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 24 (2), pp. 215–225. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2015.2504874) Cited by: §I, §V-B, TABLE III, §VII-A, TABLE VI.

[^31]: V. V. Reddy, A. W. H. Khong, and B. P. Ng (2014) Unambiguous speech doa estimation under spatial aliasing conditions. IEEE Trans. Aud., Sp., Lang. Proc. 22 (12), pp. 2133–2145. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2014.2344856) Cited by: §VI-A2.

[^32]: J. Richter, Y. Wu, S. Krenn, S. Welker, B. Lay, S. Watanabe, A. Richard, and T. Gerkmann (2024) EARS: an anechoic fullband speech dataset benchmarked for speech enhancement and dereverberation. In Proc. Interspeech, pp. 4873–4877. Cited by: §V-C.

[^33]: I. Tashev, M. Seltzer, and A. Acero (2005) Microphone array for headset with spatial noise suppressor. In Proc. Intl. W. Ac. Sig. Enh. (IWAENC), Cited by: §I, §V-B.

[^34]: K. Tesch and T. Gerkmann (2023) Insights into deep non-linear filters for improved multi-channel speech enhancement. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 31, pp. 563–575. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2022.3221046) Cited by: §I, Fig. 2, §III-A, §III-A.

[^35]: K. Tesch and T. Gerkmann (2023) Spatially selective deep non-linear filters for speaker extraction. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), External Links: [Document](https://dx.doi.org/10.1109/ICASSP49357.2023.10096098) Cited by: §I, §III-A.

[^36]: O. Thiergart, G. Del Galdo, M. Taseska, and E. A. P. Habets (2013) Geometry-based spatial sound acquisition using distributed microphone arrays. IEEE Trans. Aud., Sp., Lang. Proc. 21 (12), pp. 2583–2594. Cited by: §I, §V-B.

[^37]: O. Thiergart and E. A. P. Habets (2012) Sound field model violations in parametric spatial sound processing. In Proc. Intl. W. Ac. Sig. Enh. (IWAENC), pp. 1–4. Cited by: §I.

[^38]: O. Thiergart and E. A. P. Habets (2013) An informed LCMV filter based on multiple instantaneous direction-of-arrival estimates. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 659–663. Cited by: §I, §V-B.

[^39]: O. Thiergart, K. Kowalczyk, and E. A. P. Habets (2014) An acoustical zoom based on informed spatial filtering. In Proc. Intl. W. Ac. Sig. Enh. (IWAENC), pp. 109–113. Cited by: §I.

[^40]: O. Thiergart, G. Milano, and E. A. P. Habets (2019) Combining linear spatial filtering and non-linear parametric processing for high-quality spatial sound capturing. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), Vol., pp. 571–575. External Links: [Document](https://dx.doi.org/10.1109/ICASSP.2019.8683515) Cited by: §I, §V-B.

[^41]: O. Thiergart, M. Taseska, and E. A. P. Habets (2014) An informed parametric spatial filter based on instantaneous direction-of-arrival estimates. IEEE Trans. Aud., Sp., Lang. Proc. 22 (12), pp. 2182–2196. Cited by: §I, §V-B.

[^42]: M. Torcoli, M. M. Halimeh, and E. A. P. Habets (2025) PESQ for P.862.2. Note: [https://github.com/audiolabs/PESQ](https://github.com/audiolabs/PESQ) commit d11671a Cited by: §IV-C.

[^43]: H. L. Van Trees (2002) Optimum array processing. New York: Wiley. Cited by: §IV-A, §IV-B.

[^44]: B. D. Van Veen and K. M. Buckley (1988) Beamforming: a versatile approach to spatial filtering. IEEE Sig. Proc. Mag. 5 (2), pp. 4–24. Cited by: §I.

[^45]: A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin (2017) Attention is all you need. Advances in neural information processing systems 30. Cited by: §III-A.

[^46]: E. Vincent, R. Gribonval, and C. Févotte (2006) Performance measurement in blind audio source separation. IEEE Trans. Aud., Sp., Lang. Proc. 14 (4), pp. 1462–1469. Cited by: §IV-C.

[^47]: T. von Neumann, K. Kinoshita, C. Boeddeker, M. Delcroix, and R. Haeb-Umbach (2022) SA-SDR: a novel loss function for separation of meeting style data. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 6022–6026. External Links: [Document](https://dx.doi.org/10.1109/ICASSP43922.2022.9746757) Cited by: §III-B.

[^48]: Z. Wang and D. Wang (2017) Recurrent deep stacking networks for supervised speech separation. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), Vol., pp. 71–75. External Links: [Document](https://dx.doi.org/10.1109/ICASSP.2017.7952120) Cited by: §III-B.

[^49]: J. Wechsler, S. R. Chetupalli, M. M. Halimeh, O. Thiergart, and E. A. P. Habets (2024) Neural Directional Filtering: far-field directivity control with a small microphone array. In Proc. Intl. W. Ac. Sig. Enh. (IWAENC), pp. 459–463. Cited by: §I, §III-B, §V-C, §V-D, TABLE III.

[^50]: W. Wen, Q. Zhou, Y. Xi, H. Li, Z. Gong, and K. Yu (2025) Neural directed speech enhancement with dual microphone array in high noise scenario. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), Vol., pp. 1–5. External Links: [Document](https://dx.doi.org/10.1109/ICASSP49660.2025.10889345) Cited by: §I.

[^51]: G. Wichern, J. Antognini, M. Flynn, L. R. Zhu, E. McQuinn, D. Crow, E. Manilow, and J. Le Roux (2019) WHAM!: Extending speech separation to noisy environments. In Proc. Interspeech, Cited by: §V-C.

[^52]: M. Williams (2002) The stereophonic zoom. Rycote Microphone Windshields Ltd and Human Computer Interface, Gloucestershire (UK). Cited by: §VIII-B.

[^53]: X. Xiao, S. Watanabe, H. Erdogan, L. Lu, J. Hershey, M. L. Seltzer, G. Chen, Y. Zhang, M. Mandel, and D. Yu (2016) Deep beamforming networks for multi-channel speech recognition. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), Vol., pp. 5745–5749. External Links: [Document](https://dx.doi.org/10.1109/ICASSP.2016.7472778) Cited by: §I.

[^54]: L. F. Yan, W. Huang, T. D. Abhayapala, J. Feng, and W. B. Kleijn (2025) Neural optimisation of fixed beamformers with flexible geometric constraints. IEEE Trans. Aud., Sp., Lang. Proc.. Cited by: §VI-A4.

[^55]: Z. Zhang, Y. Xu, M. Yu, S. Zhang, L. Chen, and D. Yu (2021) ADL-mvdr: all deep learning mvdr beamformer for target speech separation. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), Vol., pp. 6089–6093. External Links: [Document](https://dx.doi.org/10.1109/ICASSP39728.2021.9413594) Cited by: §I.