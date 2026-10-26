## Neural Directional Filtering with Configurable Directivity Pattern at InferenceThanks: ⋆A joint institution of Fraunhofer IIS and Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU), Germany.

Weilong Huang <sup>1</sup>   Srikanth Raj Chetupalli <sup>2</sup>   Emanuël A. P. Habets <sup>1</sup> Affiliation: <sup>1</sup> International Audio Laboratories Erlangen <sup>⋆</sup>, Erlangen, Germany.  
<sup>2</sup> Indian Institute of Technology Bombay, Mumbai, India.

###### Abstract

Spatial filtering with a desired directivity pattern is advantageous for many audio applications. In this work, we propose neural directional filtering with user-defined directivity patterns (UNDF), enabling spatial filtering with directivity patterns that users can configure during inference. To achieve this, we propose a DNN architecture that integrates feature-wise linear modulation (FiLM), allowing user-defined patterns to serve as conditioning inputs. Through analysis, we demonstrate that the FiLM-based architecture enables the UNDF to generalize to unseen user-defined patterns during inference with higher directivities, scaling variations, and different steering directions. Furthermore, we progressively refine training strategies to enhance pattern approximation and enable UNDF to approximate irregular shapes. Lastly, experimental comparisons show that UNDF outperforms conventional methods.

DNN

deep neural network

$\Delta$ SDR

improvement in [SDR](#id26) ([SDR](#id26)) over the unprocessed signal

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

bidirectional long short-term memory

UniLSTM

unidirectional long short-term memory

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

SNR

signal-to-noise ratio

STFT

short-time Fourier transform

MAE

mean absolute error

TF

time-frequency

SA- $\varepsilon$ -tSDR

source-aggregated and regularized thresholded [SDR](#id26)

STOI

short term objective intelligibility

PESQ

perceptual evaluation of speech quality

UCA

uniform circular array

NDF

neural directional filtering

UNDF

neural directional filtering with user-defined directivity patterns

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

## I Introduction

Spatial filtering with a desired directivity pattern is beneficial to many audio applications. Traditional fixed beamforming [^4] [^2] [^1] can achieve spatial filtering with a predefined directivity pattern by linearly filtering microphone array signals, but it requires a large number of microphones and a large array aperture not only to ensure adequate performance, as measured by [WNG](#id37) ([WNG](#id37)) and [DF](#id38) ([DF](#id38)), but also to approximate the predefined directivity pattern accurately. More importantly, any change of the directivity pattern requires recomputing the spatial filter. Alternatively, parametric filtering methods [^10] [^18] [^20] [^21] [^11] utilize instantaneous parametric estimates, such as [DOA](#id5) ([DOA](#id5)), to compute a filter based on any given directivity pattern. However, these methods rely heavily on accurate [DOA](#id5) estimation, which can be challenging, particularly in multi-source environments containing non-speech signals [^19].

In recent years, many [DNN](#id4) ([DNN](#id4))-based approaches have been proposed for extracting sound sources from a predefined [^5] [^9] [^26] or user-defined angular [^27] [^25] region. Notable among these methods are the [JNF](#id24) ([JNF](#id24))-based methods [^16] [^17], which utilize [DNN](#id4) -estimated masks to extract a single target speaker from an angular region of interest. Notably, source separation or extraction is the primary focus in all these approaches, and the directivity pattern is not explicitly controlled.

Recently, [NDF](#id35) ([NDF](#id35)) [^24] has been proposed to achieve spatial filtering with a desired directivity pattern for a compact array and extended to steerable [NDF](#id35) in [^7]. Here, we aim to generate a spatial recording of the acoustic scene based on a specified directivity pattern, rather than extracting a single sound source or reducing noise. In [^24] [^7], we have shown that the architecture used by the aforementioned [JNF](#id24) -based methods [^16] [^17] can also be used for this task. However, the [NDF](#id35) model learns one fixed directivity pattern that can only be steered in different directions during inference.

In this paper, we propose [UNDF](#id36) ([UNDF](#id36)), which enables spatial filtering with directivity patterns that the user can configure during inference. To achieve this, the user-defined pattern is sampled and fed as conditioning information to the [DNN](#id4). For this, we explore two mechanisms: one inspired by the conditioning approach from [^17] and the other using a FiLM approach [^13]. We demonstrate that the FiLM-based approach enables [UNDF](#id36) to generalize to unseen user-defined patterns with higher directivities, scaling variations, and different steering directions. Additionally, we enhance pattern approximation by progressively refining training strategies, enabling [UNDF](#id36) to approximate irregular shapes.

## II Problem Formulation

We consider an acoustic scene in an anechoic environment, where $N$ sound sources are recorded by a compact array equipped with $Q$ omnidirectional microphones. Let $Y_{q}[f,t]$ represent the mixture signal at the $q$ -th microphone in the [STFT](#id28) ([STFT](#id28)) domain, where $f$ and $t$ denote the frequency and time indices, respectively. The mixture signal can be decomposed as

$$
Y_{q}[f,t]=\sum_{n=1}^{N}X_{q,n}[f,t]+V_{q}[f,t],~q\in\{1,2,\ldots,Q\},
$$

where $X_{q,n}[f,t]$ represents the signal component due to the $n$ -th source at the $q$ -th microphone, $V_{q}[f,t]$ represents the sensor noise at the $q$ -th microphone.

The objective of the [UNDF](#id36) task is to capture the acoustic scene based on a user-defined directivity pattern. A directivity pattern represents the directional sensitivity of a microphone array or a directional microphone [^4] [^3], showing the spatial response to sound from different incident angles. This paper focuses on the scenario where all sound sources are located in the $x$ - $y$ plane, meaning that all incident sounds have zero elevation angles. In the following, we assume the pattern to be frequency-invariant. As a result, each pattern can be represented as a vector applicable to all frequency bands. The user-defined pattern at time $t$ is given by $\Lambda_{t}(\theta)$, where $\theta$ is the azimuth angle of the incident sound. Finally, the target signal of the [UNDF](#id36) task is expressed as

$$
Z[f,t]=\sum_{n=1}^{N}\Lambda_{t}(\theta_{n})\,X_{1,n}[f,t],
$$

where the $\theta_{n}$ is the direction of arrival for the $n$ -th source, and $q=1$ is used as the reference microphone. In this work, we propose a [DNN](#id4) -based method to estimate the target signal using the microphone array signals.

## III Proposed method

### III-A DNN architecture and loss function

We propose two [DNN](#id4) architectures (see Figure 1), which are adaptations of the [FT-JNF](#id23) ([FT-JNF](#id23)) [^16] for the [UNDF](#id36) task. For both architectures, the real and imaginary parts of the $Q$ microphone signals in the [STFT](#id28) domain are stacked along the channel dimension, resulting in an input of size $[B,T,F,2Q]$, where $T$ represents the number of time frames, $F$ denotes the number of frequency bins, and $B$ indicates the batch size. This input is reshaped to $[B\times T,F,2Q]$, before a [BiLSTM](#id11) ([BiLSTM](#id11)) is applied with the *frequency* axis $F$ as the recurrent sequence dimension. In addition to the microphone signals, a user-defined directivity pattern is also fed as a conditioning input. The pattern is sampled uniformly at $L$ discrete angles over the range \[$0$, $2\pi$\], resulting in a pattern input vector of size \[B, L\].

The proposed PV-JNF architecture (left-hand side in Figure 1) is developed by modifying the [SSF](#id25) ([SSF](#id25)) framework [^17]. Original [SSF](#id25) consisted of the [FT-JNF](#id23) [^16] and a one-hot encoding-based conditioning module for a steering angle input. In the PV-JNF, we replace the one-hot encoding with the user-defined sampled pattern vector as the input to the linear layer. The output of this linear layer serves as the initial state for the [BiLSTM](#id11) layer at each time step.

The proposed FiLM-JNF architecture (right-hand side in Figure 1) adds a dedicated condition layer between the [BiLSTM](#id11) layer and the [UniLSTM](#id12) ([UniLSTM](#id12)) to the [FT-JNF](#id23) architecture [^16]. Here, the condition is implemented using the [FiLM](#id42) ([FiLM](#id42)) [^13] mechanism. The [FiLM](#id42) layer computes per-feature affine parameters $\boldsymbol{\alpha}$ and $\boldsymbol{\beta}$ (with dimensions of $[B,512]$) through two distinct linear layers from the user-defined pattern vector. Then, it applies element-wise modulation $\bf{y}=\boldsymbol{\alpha}\odot\bf{x}+\boldsymbol{\beta}$, shared across time and frequency, where $\bf{y}$ is the output of [FiLM](#id42) layer, with the same dimension as $\bf{x}$. The output of the [FiLM](#id42) layer is reshaped to $[B\times F,T,512]$ and then fed to the [UniLSTM](#id12) layer. Details of the remaining ‘Reshape’ operations in Figure 1 can be found in [^17] [^7].

Both PV-JNF and FiLM-JNF architectures compute a complex-valued single-channel mask, denoted $\mathcal{M}[f,t]$. The estimated signal is then computed by applying this mask to the reference microphone signal, i.e., $\widehat{Z}[f,t]=\mathcal{M}[f,t]Y_{1}[f,t]$. Subsequently, we adopt a batch-aggregated normalized $\mathcal{L}_{\mathrm{1}}$ -loss function for training, given by

$$
\mathcal{L}_{\mathrm{1}}=\frac{\sum_{b=1}^{B}\left\|\mathbf{z}^{b}-\hat{\mathbf{z}}^{b}\right\|_{1}}{\sum_{b=1}^{B}\left\|\mathbf{z}^{b}\right\|_{1}+\epsilon},
$$

where $\epsilon$ is a small constant value, and the time-domain signals $\hat{\mathbf{z}}$ and $\mathbf{z}$ correspond to [STFT](#id28) representations $\widehat{Z}$ and ${Z}$, respectively.

![[raw/papers/huang-2026-undf-configurable-directivity/figures/architectures.png|Refer to caption]]

Fig. 1: Proposed DNN Architectures. Left: PV-JNF, incorporating a pattern vector as the conditioning input in the FT-JNF 16 architecture. Right: FiLM-JNF architecture, integrating FiLM 13 conditioning into the architecture.

### III-B Training strategy

The directivity pattern of a $J$ th-order [DMA](#id3) can be defined as $\Lambda(\theta)=\sum_{j=0}^{J}\left(a_{j}\right.$ $\left.\times\cos^{j}(\theta-\theta_{\mathrm{s}})\right)$, where $a_{j}$, $j\in\{0,1,\ldots,J\}$ are real-valued coefficients that determine the pattern’s shape [^4]. Since [NDF](#id35) approximates the shape of the mainlobe better than the sidelobes [^24], and given that in sound capture scenarios users are primarily concerned with mainlobe control for the patterns while sidelobes and negative polarities are often disregarded, we consider a simplified [DMA](#id3) pattern given by

$$
\Lambda(\theta)=\lvert\mu+(1-\mu)\cos(\theta-\theta_{\mathrm{s}})\rvert^{J},
$$

where $\mu$ is a real-valued number with $\mu\in[0,1]$, which determines the null position. The patterns described by (4) fulfill $\Lambda(\theta)\in[0,1]$ (no negative polarity) and focus on the shape of the mainlobe, which is controlled by the order $J$ and $\mu$. Another widely used pattern, especially in the context of neural spatial filtering, is the rectangular pattern, defined as $\Lambda(\theta)=1$ if $\theta\in[\theta_{\mathrm{start}},\theta_{\mathrm{end}}]$, otherwise $0$.

The microphone array is positioned in a simulated anechoic room. For a source-array setup, we randomly select $N$ [DOA](#id5) for $N$ sources. The sources and array are co-planar with a fixed source-array distance of $d$. We then simulate direct-path transfer functions for all $Q$ microphones and $N$ speakers using the RIR generator [^6] with a reflection order of zero. Subsequently, we obtain microphone signals. During training, a gain is assigned for each source signal according to the pattern vector, and the target signal is generated during training using (2). This target signal, along with its corresponding pattern and microphone signals, is input as a training sample to the model. Each source-array setup has $P$ patterns for training, meaning there are $P$ training samples per source-array setup. The $P$ patterns are composed according to the following recipes:

$\bf{Recipe\ A}$: First-order patterns generated with $J=1$, $\mu\in\{0,0.1,\ldots,0.9\}$, and $\theta_{s}\in\{0^{\circ},60^{\circ},\ldots,300^{\circ}\}$, amounting to a total of 60 distinct patterns.

$\bf{Recipe\ B}$: Patterns generated by a linear combination of up to $C=4$ random [DMA](#id3) patterns, given by

$$
\Lambda_{t}(\theta)=\frac{\sum_{c=1}^{C}\Lambda_{t,c}(\theta)}{\max\limits_{i}\left[\sum_{c=1}^{C}\Lambda_{t,c}(\theta)\right]_{i}},\quad\forall t,
$$

where each random DMA pattern $\Lambda_{t,c}(\theta)$ is generated using (4) with a random $\mu$ from $\{0,0.1,\ldots,0.9\}$, a random angle $\theta_{s}$ from $\theta_{s}\in[0,2\pi]$, and a random integer $J$ from $[1,11]$.

$\bf{Recipe\ B+}$: An extended version of Recipe B, which contains patterns from the DMA and rectangular patterns. In particular, 33.3% of patterns are generated using Recipe B, 33.3% of the patterns are linear combinations of random rectangular patterns (random $\theta_{\mathrm{start}}$ and $\theta_{\mathrm{end}}$), and the remaining patterns are linear combinations of random DMA and rectangular patterns.

## IV Experimental Setup

### IV-A Datasets and configurations

We used speech signals from the ‘train-clean-360’ and ‘dev-clean’ subsets of the LibriSpeech corpus [^12] as the source signals for training and validation, respectively. For the test sets, speech samples were selected from the EARS dataset [^15] with minimum loudness of $-42$ dBFS [^8] as the selection criterion. The number of source-array setups for training and validation was $4320$ and $1080$, and each source-array setup corresponds to $P=60$ user-defined patterns, resulting in a total of $4320\times 60$ and $1080\times 60$ samples for the training set and validation set, respectively. The number of test samples was $3240$ for each pattern under test. The duration per sample was 4 $\mathrm{s}$ for all training datasets. We set up to three concurrent sources per training sample, while fixing two concurrent sources per test sample [^24] [^7]. The source [DOA](#id5) for training and validation are selected from $\theta_{n}\in\{0^{\circ},5^{\circ},\ldots,355^{\circ}\}$ and $\theta_{n}\in\{2.5^{\circ},7.5^{\circ},\ldots,357.5^{\circ}\}$ respectively. For testing, $\theta_{n}\in\{1.25^{\circ},3.75^{\circ},\ldots,358.75^{\circ}\}$. The source-array distance $d=1.5$ $\mathrm{m}$. We set $L=72$ for the pattern vectors. All models were trained for $100$ epochs with a batch size of $10$ and an initial learning rate of $0.001$. Maximum suppression for all patterns was set to $-20$ $\mathrm{dB}$. $\epsilon$ in loss function (3) was set to $10^{-7}$. We employed a four-microphone array ($Q=4$) with a diameter of $3\text{\,}\mathrm{cm}$, consisting of three microphones arranged in a [UCA](#id34) ([UCA](#id34)) and an additional microphone at the array’s center. For the remaining settings, we used the configurations in [^7].

### IV-B Performance measures

Directivity pattern: For each test sample, we apply the estimated mask $\mathcal{M}[f,t]$ separately to each source at the reference microphone. Subsequently, a wideband power ratio $\xi[\theta_{n}]$ for the $n$ -th source is then calculated as

$$
\xi[\theta_{n}]=\frac{\sum_{f=1}^{F}\sum_{t=1}^{T}\left|\mathcal{M}[f,t]\;X_{1,n}[f,t]\right|^{2}}{\sum_{f=1}^{F}\sum_{t=1}^{T}\left|X_{1,n}[f,t]\right|^{2}}.
$$

We then compute the arithmetic mean of the ratios ($\xi[\theta_{n}]$) over all the test samples from the same direction $\theta_{n}$ to obtain the final estimated wideband directivity pattern. A narrowband directivity pattern is obtained by removing the summations over the frequency index $f$ in (6).

SDR: We use the [SDR](#id26) [^22] [^23], averaged over the test set, to measure the distortion in the estimated signals compared to the target signals.

## V Results and Analysis

To the best of our knowledge, parametric filtering [^21] and the [LS](#id9) ([LS](#id9)) beamformer [^14] remain the only effective methods for spatial filtering with configurable directivity patterns. Since parametric filtering significantly outperforms the [LS](#id9) beamformer [^24], we use it as a baseline for comparison. The parametric filter is computed using oracle DOA estimates, providing an upper bound on its performance.

### V-A Conditioning methods

(a) $1^{\mathrm{st}}$ -order pattern ($60^{\circ}$)

(b) $1^{\mathrm{st}}$ -order pattern ($90^{\circ}$)

(c) $3^{\mathrm{rd}}$ -order pattern ($90^{\circ}$)

(d) Scaled pattern

Fig. 2: Estimated wideband directivity patterns obtained using all samples in the test set comparing PV-JNF and FiLM-JNF. Conditions: [UNDF](#id36) models are trained using the training strategy ‘Recipe A’. The scaled pattern is $-5$ $\mathrm{dB}$ scaled version of the $1^{\mathrm{st}}$ -order pattern.

TABLE I: SDR ($\mathrm{dB}$) performance: comparison of proposed method with conditioning variants and baseline.

|  | $1^{\mathrm{st}}$ -order ($60^{\circ}$) | $1^{\mathrm{st}}$ -order    ($90^{\circ}$) | $3^{\mathrm{rd}}$ -order ($90^{\circ}$) | Scaled |
| --- | --- | --- | --- | --- |
| Parametric filtering [^21] | 20.37 | 20.34 | 20.37 | 21.35 |
| PV-JNF (Recipe A) | 26.50 | 20.87 | 10.40 | 8.11 |
| FiLM-JNF (Recipe A) | 26.30 | 24.31 | 17.34 | 19.54 |
| FiLM-JNF (Recipe B) | 26.83 | 26.30 | 24.54 | 26.80 |

We study and compare the two conditioning methods in FiLM-JNF and PV-JNF using Recipe A, which consists only of a finite number of specific $1^{\mathrm{st}}$ -order patterns. Figure 2 (a) shows the pattern estimates for a $1^{\mathrm{st}}$ -order cardioid pattern steered towards $\theta_{s}=60^{\circ}$, which is seen in the training. The estimated patterns of the two methods closely follow the target, except for limited attenuation towards the null, which was also observed in [^24]. Figure 2 (b) shows the pattern estimates for $\theta_{s}=90^{\circ}$ (unseen $\theta_{s}$ during training). We observe a slight steering bias for the PV-JNF while FiLM-JNF maintains a good approximation. Figure 2 (c) illustrates the generalization performance for a $3^{\mathrm{rd}}$ -order cardioid pattern (unseen order and $\theta_{s}$ during training). We observe that PV-JNF exhibits a larger steering error and poorer pattern approximation than FiLM-JNF, indicating the superiority of FiLM-based conditioning. Figure 2 (d) shows the estimates for a scaled pattern, where the gain in the target direction is not unity. We see that PV-JNF deviates significantly from the target, whereas FiLM-JNF does not. The [SDR](#id26) results in Table I reflect the above observations, where the FiLM-JNF has significantly better performance (up to 11 $\mathrm{dB}$) than PV-JNF for the unseen scenarios. Thus, we conclude that FiLM conditioning enables the [UNDF](#id36) to generalize to unseen higher-order patterns, unseen scaling, and unseen steering directions. In the following, we report the results for the [UNDF](#id36) models using the FiLM-JNF architecture.

### V-B Training strategies

(a) Multi-scaled pattern

(b) Irregular pattern

Fig. 3: Estimated wideband directivity patterns for the models using training strategies: Recipe B-, Recipe B, and Recipe B+. Conditions: NDF models are trained using FiLM-JNF.

![[raw/papers/huang-2026-undf-configurable-directivity/figures/narrowband-multiscaled.png|Refer to caption]]

Refer to caption

TABLE II: SDR ($\mathrm{dB}$) performance on different training strategies.

|  | Recipe B- | Recipe B | Recipe B+ |
| --- | --- | --- | --- |
| Multi-scaled pattern | 12.98 | 19.75 | 17.61 |
| Irregular pattern | 14.20 | 14.81 | 20.39 |

We trained the FiLM-JNF using Recipe B and compared it with the parametric filter. As shown in Table I, Recipe B outperforms Recipe A and the parametric filtering. Recipe B differs from Recipe A in two main ways. First, Recipe B uses random [DMA](#id3) patterns, which intuitively provide broader coverage of orders and steering directions during training. Second, Recipe B involves linear combinations of DMA patterns. To better understand the impact of these combinations, we created a variant called Recipe B-, which contains only one random [DMA](#id3) pattern, i.e., with $C=1$ in (5).

We compare Recipes B-, B, and B+ based on pattern approximation in Figure 3. For the multi-scaled pattern in Figure 3, Recipe B shows substantial improvement over Recipe B-, while Recipe B+ performs comparably to Recipe B. We attribute this to the linear combination operation in Recipes B and B+, which exposes the model to a broader range of pattern variations. For the irregular pattern in Figure 3 (b), Recipe B+ achieves the best approximation, demonstrating that rectangular pattern mixing in Recipe B+ further enhances the approximation of irregular shapes. The [SDR](#id26) in Table II aligns with the observation in the pattern approximation. Furthermore, Figure 4 shows the estimated narrowband directivity patterns for strategy Recipe B+, where the estimated patterns exhibit frequency invariance.

### V-C Application for time-varying directivity patterns

To illustrate the application of a time-varying directivity pattern, we considered a sound scene of duration $20$ $\mathrm{s}$ involving two concurrent sound sources in a reverberant room, a speech source located at an angle of $60^{\circ}$ and a music source located at an angle of $230^{\circ}$, both at a distance of $d=1.5$ $\mathrm{m}$ from the array center. The simulated room [^6] was 6 $\mathrm{m}$ x 4 $\mathrm{m}$ x 3.5 $\mathrm{m}$ and had an $\mathrm{RT}_{60}$ of 0.15 $\mathrm{s}$. Audio samples can be found online <sup>1</sup>. The spectrogram of the unprocessed mixture signal at the reference microphone is shown in Figure 5(a). The entire simulation was divided into three equal time periods. The patterns shown in Figure 5 (c) are used as conditioning inputs for each of these consecutive periods. This process yields the spectrogram of the [UNDF](#id36) output in Figure 5(b). We used the [UNDF](#id36) model, trained with the FiLM-JNF architecture using Recipe B+ for this illustration. In the first $6.7$ $\mathrm{s}$, the music components in the mixture are preserved, and the speech components are suppressed to a certain level. In the middle $6.7$ $\mathrm{s}$, the speech components recover immediately, and the music components are partly suppressed. In the last $6.7$ $\mathrm{s}$, the retained music components are suppressed further. These results are in agreement with the expected results given the patterns shown in Figure 5(c). Hence, this qualitative example illustrates that users can adjust the proportions of each component in the processed mixture by varying the input directivity pattern. Because conditioning is applied to every frame and the model is causal [^16] [^24], changes in the input pattern are reflected immediately in the output in our simulation. This experiment also demonstrates that the [UNDF](#id36) model, despite being trained solely on anechoic speech signals, generalizes to non-speech signals and low-reverberant acoustic conditions.

![[raw/papers/huang-2026-undf-configurable-directivity/figures/spectrogram-input.png|Refer to caption]]

Refer to caption

## VI Conclusions

We propose UNDF, a spatial filtering method with configurable directivity patterns at inference. To achieve this, we integrate the FiLM layer into the JNF architecture, enabling conditioning on user-defined patterns. We demonstrated that the proposed FiLM-JNF architecture enables UNDF to generalize to unseen higher orders, scaling variations, and steering directions. Progressive evolution of training strategies improves pattern approximation, enabling the approximation of irregular shapes.

## VII Acknowledgment

The authors gratefully acknowledge the scientific support and HPC resources provided by the Erlangen National High Performance Computing Center (NHR@FAU) of the Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU). The hardware is funded by the German Research Foundation (DFG).

[^1]: J. Benesty, I. Cohen, and J. Chen (2018) Fixed beamforming. Fundamentals of Signal Enhancement and Array Signal Processing, pp. 237–282. Cited by: §I.

[^2]: M. Brandstein and D. Ward (2001) Microphone arrays: signal processing techniques and applications. Springer Science & Business Media. Cited by: §I.

[^3]: J. Eargle (2012) The microphone book: from mono to stereo to surround-a guide to microphone design and application. Routledge. Cited by: §II.

[^4]: G. W. Elko (2000) Superdirectional microphone arrays. Acoustic signal processing for telecommunication, pp. 181–237. Cited by: §I, §II, §III-B.

[^5]: R. Gu and Y. Luo (2024) ReZero: Region-Customizable Sound Extraction. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 32, pp. 2576–2589. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2024.3393713) Cited by: §I.

[^6]: E. A. P. Habets (2020) RIR generator. Note: [https://github.com/ehabets/RIR-Generator](https://github.com/ehabets/RIR-Generator) commit 3cf914d Cited by: §III-B, §V-C.

[^7]: W. Huang, M. M. Halimeh, S. R. Chetupalli, O. Thiergart, and E. A. P. Habets (2025) Steerable neural directional filtering. In Proc. Forum Acusticum Euronoise, EAA, Cited by: §I, §III-A, §IV-A.

[^8]: ITU-R (2023) Recommendation ITU-R BS.1770-5: algorithms to measure audio programme loudness and true-peak audio level. ITU. Cited by: §IV-A.

[^9]: T. Jenrungrot, V. Jayaram, S. Seitz, and I. Kemelmacher-Shlizerman (2020) The cone of silence: speech separation by localization. In Proc. Advances in Neural Information Processing Systems (NeurIPS), Vol. 33, pp. 20925–20938. Cited by: §I.

[^10]: M. Kallinger, G. Del Galdo, F. Kuech, D. Mahne, and R. Schultz-Amling (2009) Spatial filtering using directional audio coding parameters. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 217–220. Cited by: §I.

[^11]: K. Kowalczyk, O. Thiergart, M. Taseska, G. Del Galdo, V. Pulkki, and E. A. P. Habets (2015) Parametric spatial sound processing: a flexible and efficient solution to sound scene acquisition, modification, and reproduction. IEEE Sig. Process. Mag. 32 (2), pp. 31–42. External Links: [Document](https://dx.doi.org/10.1109/MSP.2014.2369531) Cited by: §I.

[^12]: V. Panayotov, G. Chen, D. Povey, and S. Khudanpur (2015) LibriSpeech: An ASR corpus based on public domain audio books. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp.. External Links: [Document](https://dx.doi.org/10.1109/ICASSP.2015.7178964) Cited by: §IV-A.

[^13]: E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville (2018) FiLM: visual reasoning with a general conditioning layer. In Proc. AAAI Conference on Artificial Intelligence, Cited by: §I, Fig. 1, §III-A.

[^14]: E. Rasumow, M. Hansen, S. van de Par, D. Püschel, V. Mellert, S. Doclo, and M. Blau (2015) Regularization approaches for synthesizing hrtf directivity patterns. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 24 (2), pp. 215–225. Cited by: §V.

[^15]: J. Richter, Y. Wu, S. Krenn, S. Welker, B. Lay, S. Watanabe, A. Richard, and T. Gerkmann (2024) EARS: an anechoic fullband speech dataset benchmarked for speech enhancement and dereverberation. In Proc. Interspeech, pp. 4873–4877. Cited by: §IV-A.

[^16]: K. Tesch and T. Gerkmann (2023) Insights into deep non-linear filters for improved multi-channel speech enhancement. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 31, pp. 563–575. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2022.3221046) Cited by: §I, §I, Fig. 1, §III-A, §III-A, §III-A, §V-C.

[^17]: K. Tesch and T. Gerkmann (2023) Multi-channel speech separation using spatially selective deep non-linear filters. IEEE/ACM Trans. Audio, Speech, Lang. Process. 32, pp. 542–553. Cited by: §I, §I, §I, §III-A, §III-A.

[^18]: O. Thiergart, G. Del Galdo, M. Taseska, and E. A. P. Habets (2013) Geometry-based spatial sound acquisition using distributed microphone arrays. IEEE Trans. Aud., Sp., Lang. Proc. 21 (12), pp. 2583–2594. Cited by: §I.

[^19]: O. Thiergart and E. A. P. Habets (2012) Sound field model violations in parametric spatial sound processing. In Proc. Intl. W. Ac. Sig. Enh. (IWAENC), pp. 1–4. Cited by: §I.

[^20]: O. Thiergart and E. A. P. Habets (2013) An informed LCMV filter based on multiple instantaneous direction-of-arrival estimates. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp.. Cited by: §I.

[^21]: O. Thiergart, M. Taseska, and E. A. P. Habets (2014) An informed parametric spatial filter based on instantaneous direction-of-arrival estimates. IEEE Trans. Aud., Sp., Lang. Proc. 22 (12), pp. 2182–2196. Cited by: §I, TABLE I, §V.

[^22]: E. Vincent, R. Gribonval, and C. Févotte (2006) Performance measurement in blind audio source separation. IEEE/ACM Trans. Aud., Sp., Lang. Proc. 14 (4), pp. 1462–1469. Cited by: §IV-B.

[^23]: T. von Neumann, K. Kinoshita, C. Boeddeker, M. Delcroix, and R. Haeb-Umbach (2022) SA-SDR: a novel loss function for separation of meeting style data. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 6022–6026. Cited by: §IV-B.

[^24]: J. Wechsler, S. R. Chetupalli, M. M. Halimeh, O. Thiergart, and E. A. P. Habets (2024) Neural Directional Filtering: far-field directivity control with a small microphone array. In Proc. Intl. W. Ac. Sig. Enh. (IWAENC), pp. 459–463. Cited by: §I, §III-B, §IV-A, §V-A, §V-C, §V.

[^25]: W. Wen, Q. Zhou, Y. Xi, H. Li, Z. Gong, and K. Yu (2025) Neural directed speech enhancement with dual microphone array in high noise scenario. In Proc. IEEE Intl. Conf. on Ac., Sp. and Sig. Proc. (ICASSP), pp. 1–5. Cited by: §I.

[^26]: A. Xu and R. R. Choudhury (2022) Learning to separate voices by spatial regions. In Proc. Intl. Conf. on Machine Learning, Vol., pp.. Cited by: §I.

[^27]: M. Yu and D. Yu (2023) Deep audio zooming: beamwidth-controllable neural beamformer. arXiv preprint arXiv:2311.13075. Cited by: §I.