DF

directivity factor

DRR

direct-to-reverberant ratio

NDF

neural directional filtering

PESQ

perceptual evaluation of speech quality

RIR

room impulse response

RTF

room transfer function

SDR

signal-to-distortion ratio

CDR

coherent-to-diffuse ratio

STFT

short-time Fourier transform

VDM

virtual directional microphone

WPE

weighted prediction error

FBF

fixed beamformer

DNN

deep neural network

$\Delta$ SDR

improvement in [SDR](#id38) ([SDR](#id38)) over the unprocessed signal

DMA

differential microphone array

DNN

deep neural network

DOA

direction-of-arrival

iSTFT

inverse short-time Fourier transform

CDMA

circular [DMA](#id15) ([DMA](#id15))

LDMA

linear [DMA](#id15)

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

RIRs

room impulse responses

RIR

room impulse response

RTF

room transfer function

RTFs

room transfer functions

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

FT-JNF

joint spatial and temporal-spectral non-linear filtering

JNF

joint non-linear filtering

SSF

spatially selective deep non-linear filter

SDR

signal-to-distortion ratio

reference microphone

[SDR](#id38) of the unprocessed omnidirectional reference microphone

SNR

signal-to-noise ratio

STFT

short-time Fourier transform

MAE

mean absolute error

TF

time-frequency

SA- $\varepsilon$ -tSDR

source-aggregated and regularized thresholded [SDR](#id38)

STOI

short term objective intelligibility

PESQ

perceptual evaluation of speech quality

UCA

uniform circular array

NDF

neural directional filtering

SHONDC

steerable high-order neural directional coding

NDSC

neural directional speech coding

NDC

neural directional coding

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

PESQ

perceptual evaluation of speech quality

UNDF

neural directional filtering with user-defined directivity patterns

VDM

virtual directional microphone

DirAC

directional audio coding

FOA

first-order ambisonics

HOA

high-order ambisonics

ATF

acousitc transfer function

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

NDBF

high-order frequency-invariant neural beamforming

DPTF

direct-path transfer function

CMA

circular microphone array

LMA

linear microphone array

NDBF

steerable high-order neural beamformer

SI-SDR

scale-invariant signal-to-distortion ratio

DBF

differential beamformer

NDBF

neural differential beamformer

<sup><math data-latex="\ast" display="inline" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mo mathsize="0.900em">∗</mo> <annotation>\ast</annotation></semantics></math></sup> A joint institution of Fraunhofer IIS and Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU), Germany. The authors gratefully acknowledge the scientific support and HPC resources provided by the Erlangen National High Performance Computing Center (NHR@FAU) of the Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU). The hardware is funded by the German Research Foundation (DFG).

###### Abstract

Linear arrays of omnidirectional microphones produce beampatterns that are symmetric about the array axis. For these arrays, a beamformer is considered steerable if its beampattern maintains the same shape in the semicircular plane across all look directions from 0° to 180°. For dual-microphone arrays, conventional differential beamformers are generally non-steerable and restricted to first-order, which significantly limits spatial selectivity. To address these limitations, this study presents a neural differential beamformer (NDBF) with a dual-microphone array. The contributions are as follows: (i) NDBF is steerable; (ii) NDBF achieves high-order frequency-invariant beampatterns; and (iii) NDBF enables stereo recording using only two closely spaced omnidirectional microphones. Experimental results demonstrate that NDBF outperforms existing methods while overcoming the limitations of classical differential beamforming.

Weilong Huang, Emanuël A. P. HabetsInternational Audio Laboratories Erlangen <sup><math data-latex="\ast" display="inline" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mo>∗</mo> <annotation>\ast</annotation></semantics></math></sup>, Am Wolfsmantel 33, 91058 Erlangen, Germany

## 1 Introduction

Recently, differential beamformers for linear arrays have received significant attention in [DMA](#id15) research [^2] [^3] [^13]. The largest order of such beamformers is $Q-1$, where $Q$ denotes the number of microphones [^2]. A dual-microphone array, which constitutes the minimum number of microphones for a linear array, restricts the [DMA](#id15) to first order and substantially limits spatial filtering capability.

The steerability of beamformers for a circular array is readily attainable and has been extensively studied [^25] [^9] [^11]. In contrast, most differential beamformers designed for a linear array are generally assumed to have a look direction at $0^{\circ}$ (endfire) [^2] [^3], as this configuration typically yields the highest [DF](#id66) ([DF](#id66)). However, the ability to steer the look direction away from $0^{\circ}$ while maintaining the same beampattern is essential for practical applications of a linear array, including televisions, tablets, and laptops. For a linear array, “steerability” refers to the ability of a beamformer to maintain a consistent beampattern across look directions from $0^{\circ}$ to $180^{\circ}$ in the semicircular plane, as described in [^13].

Two situations fall short of full steerability: (1) partially steerable, where the beampattern achieves 0 $\mathrm{dB}$ at the look direction and does not exceed 0 $\mathrm{dB}$ elsewhere, but varies across look directions; and (2) non-steerable, where the beampattern achieves 0 $\mathrm{dB}$ at the look direction, but exceeds 0 $\mathrm{dB}$ in some other directions [^13]. For a differential beamformer with a linear array, achieving steerable beampatterns is feasible only with high-order designs and requires that the null positions satisfy specific conditions [^13]. Therefore, a first-order differential beamformer with dual microphones is hardly steerable. Recent linear superarrays [^14] [^15] [^10] [^17] enable differential beamformers to achieve steerability, but their core concept relies on a hybrid usage of omnidirectional and directional microphones. Therefore, developing a steerable differential beamformer for a linear array, particularly with only two omnidirectional microphones, remains an open research problem.

Most [DNN](#id16) ([DNN](#id16))-based methods have been proposed for performing spatial filtering within an angular region [^30] [^27] or directly focusing on speech separation or extraction [^20] [^29], where the beampattern is not explicitly controlled. Recently, [NDF](#id48) ([NDF](#id48)) [^26] proposed to estimate a single-channel mask for nonlinear spatial filtering based on a predefined beampattern using a circular array. This approach paves the way for beampattern-oriented neural spatial filtering and has the potential to address the limitations in differential beamforming. However, [NDF](#id48) has so far been studied only for circular arrays, and its single-channel masking strategy may not fully exploit the spatial information available for beamforming, particularly for dual-microphone arrays, where spatial degrees of freedom are very limited. As an extension of [NDF](#id48) to beamforming for a dual-microphone array, we propose a [NDBF](#id78) ([NDBF](#id78)) that, using a [DNN](#id16), produces beampatterns similar to those of classical [DMA](#id15). Experimental results demonstrate that [NDBF](#id78) with a dual-microphone array achieves steerable high-order beampatterns and surpasses existing methods. Leveraging the steerability and beampattern-oriented spatial filtering of NDBF, we demonstrate that stereo recording can be achieved with only two closely spaced omnidirectional microphones.

![[raw/papers/huang-2026-dual-mic-steerable-neural-beamformer/figures/fig1.png|Refer to caption]]

Fig. 1: The goal of the steerable high-order neural differential beamforming with dual-omnidirectional microphones.

## 2 Problem Formulation

We consider a dual-microphone array comprising two omnidirectional microphones to capture $N$ sound sources in an anechoic environment. The corresponding microphone array signals in [STFT](#id41) ([STFT](#id41)) domain are denoted by $\textbf{y}(f,t)=[Y_{1}(f,t),Y_{2}(f,t)]$, where $f$ and $t$ denote the frequency and time indices, respectively. The mixture signal on the first microphone $Y_{1}(f,t)$ can be decomposed as

$$
Y_{1}(f,t)=\sum_{n=1}^{N}X_{1,n}(f,t)+V_{1}(f,t),
$$

where $V_{1}(f,t)$ is spatially uncorrelated sensor noise and $X_{1,n}(f,t)=H_{\mathbf{p}_{1},n}(f)\,X_{n}(f,t)$, where $H_{\mathbf{p}_{1},n}(f)$ models the [DPTF](#id72) ([DPTF](#id72)) between the $n$ -th source $X_{n}(f,t)$ and the first microphone at position $\mathbf{p}_{1}$.

For this dual-microphone array, the goal of the [NDBF](#id78) is to capture the $N$ sound sources using a steerable high-order [DMA](#id15) beampattern (see Fig. 1). This beampattern is denoted by $\Lambda_{\theta_{\textrm{s}}}(\theta_{\textrm{n}})$, where ${\theta_{\textrm{s}}}$ is the steering direction of the beampattern and $\theta_{\textrm{n}}$ denotes the [DOA](#id17) ([DOA](#id17)) of the $n$ -th source with respect to the position $\mathbf{p}_{\textrm{c}}$ (the center of the dual-microphone array). The target signal of the [NDBF](#id78) is expressed as

$$
Z_{\theta_{\textrm{s}}}(f,t)=\sum_{n=1}^{N}\Lambda_{\theta_{\textrm{s}}}(\theta_{\textrm{n}})\,H_{{\mathbf{p}_{\textrm{c}}},n}(f)\,X_{n}(f,t),
$$

where $H_{{\mathbf{p}_{\textrm{c}}},n}(f)$ models the [DPTF](#id72) between the $n$ -th source $X_{n}(f,t)$ and the position $\mathbf{p}_{\textrm{c}}$. In this work, we propose a [DNN](#id16) based method to obtain the beamformer weights $\textbf{w}_{\theta_{\textrm{s}}}(f)$ given any steering direction ${\theta_{\textrm{s}}}$ at inference.

## 3 Proposed Method

Fig. 2: Extended version of the JNF-SSF architecture [^22], which outputs two complex weights per time $t$ and frequency $f$.

### 3.1 DNN Architecture and Loss Function

The JNF-SSF [^22] is adopted as [DNN](#id16) architecture for the [NDBF](#id78) task, with a modification in which the single-channel complex mask is replaced by a vector of complex weights at the output of the final linear layer (see the left side in Fig. 2). The real and imaginary components of the dual-microphone signals in the [STFT](#id41) domain are stacked along the channel dimension, resulting in an input with dimensions of $[B,T,F,4]$, where $B$ indicates the batch size, $T$ represents the number of time frames, and $F$ denotes the number of frequency bins. The stacked inputs are processed by two distinct [LSTM](#id22) ([LSTM](#id22)) modules. The first [LSTM](#id22) is bidirectional and operates along the frequency dimension, thereby modeling instantaneous spectro-spatial relationships in the input [^21]. Its output is subsequently processed by a unidirectional [LSTM](#id22) module that captures temporal relationships, treating the frequency dimension as the batch dimension and thus modeling all frequencies independently [^21]. As in [^22], the desired look direction of the beampattern is encoded as a one-hot vector, which is mapped to an embedding of the same dimension as the first [LSTM](#id22) hidden states via a linear layer. The output of this layer is then used to initialize the [LSTM](#id22) ’s states for each time frame. Finally, a linear layer with a hyperbolic tangent activation function computes the [NDBF](#id78) weights $\textbf{w}_{\theta_{\textrm{s}}}(f)$. These weights are applied to the microphone array signals $\textbf{y}(f,t)$ to obtain an estimate of the target signal, i.e., $\widehat{Z}_{\theta_{\textrm{s}}}(f,t)=\textbf{w}_{\theta_{\textrm{s}}}^{H}(f)\ \textbf{y}(f,t)$.

The training loss is based on a batch-aggregated normalized $\mathcal{L}_{\textrm{1}}$ -loss function [^11] [^8] [^7], expressed as:

$$
\mathcal{L}_{\textrm{1}}=\frac{\sum_{b=1}^{B}\left\lVert\mathbf{z}^{b}-\hat{\mathbf{z}}^{b}\right\rVert_{1}}{\sum_{b=1}^{B}\left\lVert\mathbf{z}^{b}\right\rVert_{1}+\epsilon},
$$

where the time-domain signals $\hat{z}$ and ${z}$ correspond to [STFT](#id41) representations $\widehat{Z}$ and ${Z}$, respectively.

### 3.2 Training Strategy

Fig. 3: Target beampatterns (left side) and a source-array setup example (right side).

A $J$ th-order [DMA](#id15) beampattern [^4] is defined as follows $\Lambda_{\theta_{\textrm{s}}}=\sum_{j=0}^{J}a_{j}\,\cos^{j}(\theta-\theta_{\textrm{s}})$, where $\theta_{\textrm{s}}$ represents the steering direction of the pattern, while $a_{j}$, where $j\in\{0,1,\ldots,J\}$, are real-valued coefficients that define the pattern’s shape, particularly affecting the sidelobes. In sound capture scenarios, primary attention is given to controlling the mainlobe of the patterns. Therefore, a simplified [DMA](#id15) pattern is considered as follows:

$$
\Lambda(\theta)=(\mu+(1-\mu)\cos(\theta-\theta_{\textrm{s}}))^{J},
$$

where $\mu$ is a real-valued parameter within $[0,1]$ that determines the null position. The patterns described by (4) emphasize mainlobe shape, which is governed by the order $J$ and $\mu$. In this paper, two example beampatterns were employed as the target beampatterns in Fig. 3. The first target pattern is a $1^{\textrm{st}}$ -order Cardioid with $\mu=0.5,J=1$. The second is a $3^{\textrm{rd}}$ -order Cardioid pattern with $\mu=0.5,J=3$.

To learn the [DMA](#id15) beampattern with a linear array in the free field, the sound sources are positioned along a semicircle, with the microphone array located along the $0^{\circ}$ - $180^{\circ}$ axis and being concentric with the semicircle (an example is shown in Fig. 3). To simulate a source-array setup with $N$ source positions, $N$ source positions are randomly selected on the semicircle, and [DPTF](#id72) are simulated for all microphones and sources using the RIR generator [^5] with a reflection order of zero. Microphone array signals are then obtained using (1). For each source-array setup, we simulate $M$ target signals for look directions uniformly spanning $0$ to $180$ degrees, resulting in a steering angular resolution of $\frac{180^{\circ}}{M}$. The $m$ -th target signal $Z_{\theta^{m}_{\textrm{s}}}[f,t]$ corresponding to the steering direction $\theta^{m}_{\textrm{s}}$ is obtained using (2). During training, we treat microphone-array signals from each acoustic scene, paired with a target signal, as one training sample.

## 4 Experimental Setup

### 4.1 Datasets

Speech signals from the ‘train-clean-360’ and ‘dev-clean’ subsets of the LibriSpeech corpus [^18] served as source signals for training and validation, respectively. For the test sets, speech signals were selected from the EARS dataset [^19] using a minimum loudness of $-42$ dBFS [^12]. The parameter $M$ was set to 36, resulting in a steering resolution of $5^{\circ}$. A total of 1440 random source-array setups were simulated, yielding $1440\times 36$ samples for the training set. The test set contains 3240 samples. Each sample in all datasets has a duration of 4 seconds. In each sample, the concurrent sources were randomly drawn from the setup’s source positions, with up to three for training and exactly two for testing. Source positions for training and validation were selected from $\theta_{\textrm{n}}\in\{0^{\circ},5^{\circ},\ldots,175^{\circ}\}$ and $\theta_{\textrm{n}}\in\{2.5^{\circ},7.5^{\circ},\ldots,177.5^{\circ}\}$, respectively. The source positions in test sets were selected from $\theta_{\textrm{n}}\in\{1.25^{\circ},3.75^{\circ},\ldots,178.75^{\circ}\}$. The distance between the two microphones was set to $3\text{\,}\mathrm{cm}$, and the source-array distance for all speakers was fixed at $1.5\text{\,}\mathrm{m}$. Microphone sensor noise was added with an SNR of $30$ dB. STFT settings and training details followed [NDF](#id48) [^26].

### 4.2 Performance Measures

Estimated Beampattern: For each test sample, the array signals for the $n$ -th source is denoted by $\textbf{x}_{n}(f,t)=[X_{1,n}(f,t),X_{2,n}(f,t)]$. Then, the estimated beamformer $\textbf{h}(f)$ is applied separately to the array signals for each source. Subsequently, the wideband power ratio $\xi[\theta_{\textrm{n}}]$ for the $n$ -th source is calculated as follows:

$$
\xi[\theta_{\textrm{n}}]=\frac{\sum_{f=1}^{F}\sum_{t=1}^{T}\left|\textbf{h}^{H}(f)\textbf{x}_{n}(f,t)\right|^{2}}{\sum_{f=1}^{F}\sum_{t=1}^{T}\left|X_{1,n}[f,t]\right|^{2}}.
$$

The arithmetic mean of the ratios ($\xi[\theta_{\textrm{n}}]$) is then computed over all test samples from the same direction $\theta_{\textrm{n}}$ to obtain the final estimated wideband beampattern. Similarly, by removing the frequency-based summation from both the numerator and denominator in (5), the narrowband beampattern is computed.

SDR: The [SDR](#id38) [^24], averaged over the test set, is used to measure the distortion in the estimated signals compared to the target signals.

## 5 Experimental Results

### 5.1 Performance Analysis

Table 1: SDR ($\mathrm{dB}$) performance: comparison of proposed method with baseline for the end-fire direction.

| Method | $1^{\textrm{st}}$ -order Pattern | $3^{\textrm{rd}}$ -order Pattern |
| --- | --- | --- |
| DMA [^2] | \-0.99 | N/A |
| Parametric spatial filter [^23] | 13.77 | 10.32 |
| NDF [^26] | 25.85 | 23.13 |
| Proposed NDBF | 25.93 | 23.24 |

(a) $\theta_{\textrm{s}}=0^{\circ}$, $1^{\textrm{st}}$ -order.

(b) $\theta_{\textrm{s}}=0^{\circ}$, $3^{\textrm{rd}}$ -order.

(c) $\theta_{\textrm{s}}=30^{\circ}$, $1^{\textrm{st}}$ -order.

(d) $\theta_{\textrm{s}}=30^{\circ}$, $3^{\textrm{rd}}$ -order.

(e) $\theta_{\textrm{s}}=60^{\circ}$, $1^{\textrm{st}}$ -order.

(f) $\theta_{\textrm{s}}=60^{\circ}$, $3^{\textrm{rd}}$ -order.

(g) $\theta_{\textrm{s}}=90^{\circ}$, $1^{\textrm{st}}$ -order.

(h) $\theta_{\textrm{s}}=90^{\circ}$, $3^{\textrm{rd}}$ -order.

Fig. 4: Steerability study of the NDBF for various look directions $\theta_{\textrm{s}}$ and compared with the baselines.

![[raw/papers/huang-2026-dual-mic-steerable-neural-beamformer/figures/fig2.png|Refer to caption]]

Fig. 5: Estimated 3 rd 3^{\\textrm{rd}} -order narrowband beampatterns. (a) Baseline NDF 26 at θ s = 0 ∘ \\theta\_{\\textrm{s}}=0^{\\circ}. (b)-(d) Proposed NDBF at steering angles, 30 30^{\\circ}, and 60 60^{\\circ}.

To the best of our knowledge, three methods can perform spatial filtering exactly based on a predefined beampattern: the classic [DMA](#id15) [^2], the [NDF](#id48) [^26], and the parametric spatial filter [^23]. For a fair comparison, [NDF](#id48) was trained for a dual-microphone array using the same training strategy and dataset as the [NDBF](#id78).

As shown in Table 1, the proposed NDBF achieves the highest SDR. The performance of the [DMA](#id15) and the parametric spatial filter is significantly lower than that of the two neural network-based methods. The [DMA](#id15) is subject to the well-known white-noise amplification problem at low frequencies [^1] and spatial aliasing above 5.7 $\mathrm{kHz}$ due to an inter-microphone spacing of $3\text{\,}\mathrm{cm}$, which substantially reduces its SDR. The parametric spatial filter is also impacted by spatial aliasing. To further compare NDF and the proposed NDBF, the estimated beampatterns produced by both methods were analyzed, as shown in Figs. 4(a) and (b) (wideband beampattern) and Figs. 5(a) and (b) (narrowband beampattern). Figs. 4(a) and (b) demonstrate that both methods effectively approximate the mainlobe of the target beampattern, while [NDBF](#id78) provides stronger suppression near the null position. This finding explains the SDR improvement of [NDBF](#id78) over [NDF](#id48) in Table 1, and also aligns with Figs. 5(a) and (b), which show that [NDBF](#id78) produces a cleaner suppression region in the narrowband beampattern. Additionally, both NDBF and NDF achieve a frequency-invariant beampattern without spatial aliasing for the broadband speech signals under test. The capability of NDF to achieve frequency-invariant beampattern has been previously analyzed in [^8] [^16], and the present study confirms that the proposed NDBF also exhibits this property.

Since the [DMA](#id15) does not guarantee a frequency-invariant beampattern, we analyze its beampattern at 1 $\mathrm{kHz}$ for comparison to investigate the steerability of the [NDBF](#id78). We present estimated wideband beampatterns of [NDBF](#id78) for four different look directions (0°, 30°, 60°, and 90°) as illustrated in Fig. 4, where (a), (c), (e), and (g) corresponds to the $1^{\textrm{st}}$ -order target beampattern and (b), (d), (f), and (h) corresponds to the $3^{\textrm{rd}}$ -order target beampattern. The [NDBF](#id78) effectively approximates the target beampattern, and its beampattern remains consistent across different look directions, indicating that [NDBF](#id78) is steerable. In contrast, the [DMA](#id15) often achieves a response of 0 $\mathrm{dB}$ in the target direction but exceeds 0 $\mathrm{dB}$ in other directions, which is a typical non-steerable characteristic [^13]. Figs. 5(c) and (d) show the estimated $3^{\textrm{rd}}$ -order narrowband beampatterns of the NDBF for look directions at $30^{\circ}$ and $60^{\circ}$. These results demonstrate that steerable high-order beampatterns maintain frequency-invariant properties similar to those observed in the endfire direction.

### 5.2 Application to Stereo Recording

Fig. 6: Stereo recording using two omnidirectional microphones by the proposed steerable NDBF.

(a) NDBF stereo outputs.

(b) VDM stereo outputs.

(c) Difference between the left and the right channel.

Fig. 7: Stereo output comparison between the proposed [NDBF](#id78) and desired virtual directional microphones (VDM).

We simulated a reverberant room with $\textrm{RT}_{60}$ of 0.15 $\mathrm{s}$ and a size of 6 $\mathrm{m}$ $\times$ 4 $\mathrm{m}$ $\times$ 3.5 $\mathrm{m}$. As shown in the left side of Fig. 6, a speech source moved steadily in a clockwise direction from $180^{\circ}$ to $0^{\circ}$ over approximately 12 seconds, with a fixed source-array distance of 1.5 m. The array consisted of two omnidirectional microphones spaced 3 cm apart. This simulated scene, generated using Dynamic Acoustic Scene Generator [^6], is used to evaluate [NDBF](#id78) ’s stereo recording capability.

To the best of our knowledge, neither classical differential beamformers nor existing neural beamformers enable stereo recording with only two closely spaced omnidirectional microphones. Traditionally, stereo recording using the X-Y technique requires two first-order directional microphones, most commonly each with a cardioid beampattern, arranged at look directions of $45^{\circ}$ and $135^{\circ}$ [^28]. In contrast, we trained a steerable [NDBF](#id78) model with a first-order cardioid beampattern as the training target. The right side of Fig. 6 illustrates a configuration in which two-microphone signals are processed by two parallel steerable [NDBF](#id78) models. One model is steered to $\theta_{\mathrm{L}}=135^{\circ}$, while the other is steered to $\theta_{\mathrm{R}}=45^{\circ}$. The resulting beamformed outputs are assigned to the left and right channels, respectively, thereby producing the stereo output of [NDBF](#id78), shown in Fig. 7(a). For comparison, we simulate the X-Y technique using two [VDM](#id60) located at the array center with the same look directions as the [NDBF](#id78) models. The stereo output of [VDM](#id60) is presented in Fig. 7(b). This waveform comparison indicates that the stereo output of [NDBF](#id78) closely matches that of [VDM](#id60). Figure 7(c) presents the segmental energy differences between the left and right channels for [NDBF](#id78) and [VDM](#id60); the two curves are quite close, indicating highly similar inter-channel level differences. This qualitative example demonstrates that [NDBF](#id78), even with a compact dual-microphone array, effectively captures the inter-channel level differences essential for stereo recording.

## 6 Conclusions

This paper presents a [DNN](#id16) -based differential beamformer, termed NDBF, which achieves steerable high-order [DMA](#id15) beampatterns using a dual-microphone array. Experimental results indicate that NDBF outperforms existing methods, particularly in approximating a target beampattern. This beampattern learning capability enables NDBF to overcome the limitations of traditional differential beamformers, which are typically first-order and non-steerable for such arrays. Furthermore, NDBF’s steerability and beampattern-oriented spatial filtering enable stereo recording using only two closely spaced omnidirectional microphones.

[^1]: J. Benesty, J. Chen, C. Pan, et al. (2016) Fundamentals of differential beamforming. Springer. Cited by: §5.1.

[^2]: J. Benesty and C. Jingdong (2012) Study and design of differential microphone arrays. Vol. 6, Springer Science & Business Media. Cited by: §1, §1, §5.1, Table 1.

[^3]: J. Chen, J. Benesty, and C. Pan (2014) On the design and implementation of linear differential microphone arrays. J. Ac. Soc. Am. 136 (6), pp. 3097–3113. Cited by: §1, §1.

[^4]: G. W. Elko (2000) Superdirectional microphone arrays. Acoustic signal processing for telecommunication, pp. 181–237. Cited by: §3.2.

[^5]: E. A. P. Habets (2020) RIR generator. Note: [https://github.com/ehabets/RIR-Generator](https://github.com/ehabets/RIR-Generator) commit 3cf914d Cited by: §3.2.

[^6]: E. A. P. Habets (2025) DAS generator. Note: [https://github.com/ehabets/das-generator](https://github.com/ehabets/das-generator) commit 6f2cd6d Cited by: §5.2.

[^7]: W. Huang, S. R. Chetupalli, and E. A. Habets (2025) Neural directional filtering with configurable directivity pattern at inference. arXiv preprint arXiv:2510.20253. Cited by: §3.1.

[^8]: W. Huang, S. R. Chetupalli, M. M. Halimeh, O. Thiergart, and E. A. Habets (2025) Neural directional filtering using a compact microphone array. arXiv preprint arXiv:2511.07185. Cited by: §3.1, §5.1.

[^9]: W. Huang and J. Feng (2022) Robust steerable differential beamformer for concentric circular array with directional microphones. In Sig. and Inf. Proc. Assoc. An. Sum. and Conf. (APSIPA), Vol., pp. 319–323. External Links: [Document](https://dx.doi.org/10.23919/APSIPAASC55919.2022.9980184) Cited by: §1.

[^10]: W. Huang and E. A. Habets (2025) Robust differential beamformers for linear superarrays with non-uniformly oriented directional microphones. In Proc. European Sig. Processing Conf. (EUSIPCO), pp. 191–195. Cited by: §1.

[^11]: W. Huang, M. M. Halimeh, S. R. Chetupalli, O. Thiergart, and E. A. P. Habets (2025) Steerable neural directional filtering. In Proc. Forum Acusticum Euronoise, European Acoustics Association, Cited by: §1, §3.1.

[^12]: ITU-R (2023) Recommendation ITU-R BS.1770-5: algorithms to measure audio programme loudness and true-peak audio level. Cited by: §4.1.

[^13]: J. Jin, G. Huang, X. Wang, J. Chen, J. Benesty, and I. Cohen (2021) Steering study of linear differential microphone arrays. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 29 (), pp. 158–170. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2020.3038566) Cited by: §1, §1, §1, §5.1.

[^14]: X. Luo, J. Jin, G. Huang, J. Chen, and J. Benesty (2023) Design of steerable linear differential microphone arrays with omnidirectional and bidirectional sensors. IEEE Signal Processing Letters 30 (), pp. 463–467. External Links: [Document](https://dx.doi.org/10.1109/LSP.2023.3267969) Cited by: §1.

[^15]: X. Luo, J. Jin, G. Huang, J. Chen, and J. Benesty (2024) Design of fully steerable differential beamformers with linear superarrays. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 32 (), pp. 3076–3089. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2024.3407513) Cited by: §1.

[^16]: A. Mannanova, J. Kienegger, and T. Gerkmann (2025) An analysis of joint nonlinear spatial filtering for spatial aliasing reduction. arXiv preprint arXiv:2509.25982. Cited by: §5.1.

[^17]: F. Miotello, D. Albertini, and A. Bernardini (2026) On the extension of differential beamforming theory to arbitrary planar arrays of first-order elements. IEEE Trans. Aud., Sp., Lang. Proc. 34 (), pp. 1815–1825. External Links: [Document](https://dx.doi.org/10.1109/TASLPRO.2026.3675799) Cited by: §1.

[^18]: V. Panayotov, G. Chen, D. Povey, and S. Khudanpur (2015) LibriSpeech: An ASR corpus based on public domain audio books. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 5206–5210. External Links: [Document](https://dx.doi.org/10.1109/ICASSP.2015.7178964) Cited by: §4.1.

[^19]: J. Richter, Y. Wu, S. Krenn, S. Welker, B. Lay, S. Watanabe, A. Richard, and T. Gerkmann (2024) EARS: an anechoic fullband speech dataset benchmarked for speech enhancement and dereverberation. In Proc. Interspeech, pp. 4873–4877. Cited by: §4.1.

[^20]: K. Tesch and T. Gerkmann (2021) Nonlinear spatial filtering in multichannel speech enhancement. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 29, pp. 1795–1805. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2021.3076372) Cited by: §1.

[^21]: K. Tesch and T. Gerkmann (2023) Insights into deep non-linear filters for improved multi-channel speech enhancement. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 31, pp. 563–575. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2022.3221046) Cited by: §3.1.

[^22]: K. Tesch and T. Gerkmann (2023) Multi-channel speech separation using spatially selective deep non-linear filters. IEEE/ACM Trans. Audio, Speech, Lang. Process. 32, pp. 542–553. Cited by: Figure 2, §3.1.

[^23]: O. Thiergart, M. Taseska, and E. A. P. Habets (2014) An informed parametric spatial filter based on instantaneous direction-of-arrival estimates. IEEE Trans. Aud., Sp., Lang. Proc. 22 (12), pp. 2182–2196. Cited by: §5.1, Table 1.

[^24]: E. Vincent, R. Gribonval, and C. Févotte (2006) Performance measurement in blind audio source separation. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 14 (4), pp. 1462–1469. Cited by: §4.2.

[^25]: J. Wang, F. Yang, and J. Yang (2023) A perspective on fully steerable differential beamformers for circular arrays. IEEE Signal Processing Letters 30 (), pp. 648–652. External Links: [Document](https://dx.doi.org/10.1109/LSP.2023.3280852) Cited by: §1.

[^26]: J. Wechsler, S. R. Chetupalli, M. M. Halimeh, O. Thiergart, and E. A. P. Habets (2024) Neural Directional Filtering: far-field directivity control with a small microphone array. In Proc. Intl. W. Ac. Sig. Enh. (IWAENC), pp. 459–463. Cited by: §1, §4.1, Figure 5, Figure 5, §5.1, Table 1.

[^27]: W. Wen, Q. Zhou, Y. Xi, H. Li, Z. Gong, and K. Yu (2025) Neural directed speech enhancement with dual microphone array in high noise scenario. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 1–5. Cited by: §1.

[^28]: M. Williams (2002) The stereophonic zoom. Rycote Microphone Windshields Ltd and Human Computer Interface, Gloucestershire (UK). Cited by: §5.2.

[^29]: Y. Yang, C. Quan, and X. Li (2023) MCNET: fuse multiple cues for multichannel speech enhancement. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), External Links: [Document](https://dx.doi.org/10.1109/ICASSP49357.2023.10095509) Cited by: §1.

[^30]: M. Yu and D. Yu (2023) Deep audio zooming: beamwidth-controllable neural beamformer. arXiv preprint arXiv:2311.13075. Cited by: §1.