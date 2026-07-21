# LISTEN FIRST: OUTPUT–BASED MULTI–MICROPHONE SPEECH ENHANCEMENT

Panos Apostolidis<sup>1,2</sup>, Svend Feldt<sup>2</sup>, Zheng-Hua Tan<sup>1</sup>, Jan Østergaard<sup>1</sup>, Jesper Jensen<sup>1,2</sup>

<sup>1</sup> Aalborg University, Department of Electronic Systems, Aalborg, 9220, Denmark <sup>2</sup> Eriksholm Research Centre, Snekkersten, 3070, Denmark

## ABSTRACT

Traditionally, hearing-aid speech enhancement (SE) algorithms rely on input-based feature estimation, often derived by a voice activity detector (VAD), to configure beamformers. Yet features extracted from noisy microphone signals can become unreliable in challenging acoustic scenes where users most need help. We introduce a novel paradigm in which the settings of a sound processing system are determined by evaluating characteristics of its output. To demonstrate this idea, we employ an output-based system that selects among a set of minimum power distortionless response (MPDR) beamformers. Although MPDR beamformers are typically avoided due to their sensitivity to steering errors, we show that they become effective within an output-based framework. We compare the proposed system to a conventional input-based minimum variance distortionless response (MVDR) baseline. Experimental results show that the proposed system consistently outperforms the MVDR baseline, particularly at low SNRs, in terms of SNR, ESTOI and PESQ.

Index Terms— Beamforming, microphone arrays, multimicrophone speech enhancement, voice activity detection.

## 1. INTRODUCTION

Multi-channel speech enhancement (SE) is widely used in audio applications, including hearing-aid (HA) systems [1], which aim to improve speech intelligibility (SI) and sound quality (SQ) by attenuating noise and reverberation [2]. Conventional HA-oriented SE algorithms, illustrated in Fig. 1a, often rely on acoustic features such as voice-activity-detection (VAD) cues indicating where speech is present in the time-frequency (T-F) domain. Because these features are derived directly from microphone signals, we refer to such systems as input-based. As HAs are low-power devices, the features are often extracted using signal-processing methods [3, 4], while deeplearning-based feature extractors have also been explored [5, 6].

In a conventional input-based paradigm, the SE algorithm is decomposed into a multi-channel and a single-channel stage, e.g. a Minimum Variance Distortionless Response (MVDR) beamformer and a post-filter, respectively [7]. The beamformer relies on estimates of the noise cross-power spectral density and the relative transfer functions (RTFs) from the target to each microphone [4], often provided by a VAD. Since the VAD operates directly on noisy microphone signals, the quality of the estimated speech statistics degrades in challenging acoustic conditions, precisely when HA-users need most support.

Instead, we propose an alternative paradigm in which a speechprocessing system is configured by evaluating the SI or SQ of its output rather than extracting features from its input, as illustrated in Fig. 1(b). Related studies have explored output-driven mechanisms [8, 9, 10]. For instance, [8] uses output-based SQ estimates for direction-of-arrival (DOA) correction, while [9] leverages enhanced outputs for target tracking. These approaches modify individual processing components, whereas the proposed paradigm is more general, selecting among any candidate SE system configurations.

![](figures/9279ffbceb75d11f03cb7685f8f36fcd00b5a7883e7b8d964f2a045f10ac2994.jpg)  
Fig. 1: (a) input-based SE and (b) proposed output-based paradigm.

As an example of the proposed paradigm, we introduce a SE system that selects from a discrete set of fixed candidate beamformer settings, the one maximizing a speech-intelligibility-related glimpse proportion (GP) measure [11] computed from each candidate’s output. This represents an output-based form of processing because all estimates of SI are made after the SE stage, allowing the output itself to guide the settings of the beamforming system. To enable a fair comparison between the proposed system and conventional input-based approaches, we use the same VAD in both systems, ensuring that performance differences arise from the structural distinction between output- and input-based processing rather than from differences in the architecture and complexity of the VAD itself.

In this paper, we demonstrate the potential of the proposed output-based paradigm using a set of candidate minimum power distortionless response (MPDR) beamformers. In particular, we show that the optimal candidate can be reliably selected solely from its output signals, even in low SNR, where input-based MVDR systems often struggle to estimate speech statistics. Although MPDR beamformers are rarely used due to their sensitivity to steering errors, we find that in an output-based approach they become effective. Across multiple objective measures, the proposed system consistently outperforms the input-based baseline. Importantly, the output-based system retains a performance advantage over the input-based baseline even under RTF mismatch, highlighting the robustness and practical potential of output-driven SE for real-world applications.

## 2. OUTPUT-BASED MULTI-MICROPHONE SE SYSTEM

## 2.1. Signal model

We model the noisy microphone signal in the STFT domain as:

$$
\mathbf {X} (k, l) \approx S (k, l) \mathbf {H} (k) + \mathbf {V} (k, l),\tag{1}
$$

where $S ( k , l )$ is the STFT of the target signal, and $\mathbf { H } ( k )$ and $\mathbf { V } ( k , l )$ are the M-dimensional Head-Related Transfer Function (HRTF), and noise vectors [12]. The indices $k \in \{ 0 , \ldots , K - 1 \}$ and l ∈ $\{ 0 , \ldots , L - 1 \}$ denote frequency bin and time frame, respectively.

## 2.2. Output-based MPDR beamforming

To demonstrate the proposed output-based paradigm, we introduce a beamforming system that selects an MPDR beamformer configuration from a discrete set of candidates based on their output signals. The weights of an MPDR beamformer are given by [13]

$$
\mathbf {W} _ {M P D R} (k, l) = \frac {\mathbf {C} _ {\mathbf {X}} ^ {- 1} (k , l) \mathbf {d} _ {\theta_ {i}} (k)}{\mathbf {d} _ {\theta_ {i}} ^ {H} (k) \mathbf {C} _ {\mathbf {X}} ^ {- 1} (k , l) \mathbf {d} _ {\theta_ {i}} (k)},\tag{2}
$$

where $\mathbf { C } \mathbf { x } ( k , l ) \in \mathit { C } ^ { M \times M }$ is the covariance matrix of the noisy signal $\mathbf { X } ( k , l )$ and $\mathbf { d } _ { \theta _ { i } } ( k )$ denotes the RTF vector with respect to the reference microphone to a target position with direction $\theta _ { i }$

To enable an output-based MPDR beamformer system, we assume access to a dictionary $\mathbf { d } _ { \theta } ( k )$ of N time-invariant candidate RTF vectors $\mathbf { d } _ { \theta _ { i } } ( k )$ , each corresponding to a candidate target direction $\theta _ { i }$ at a fixed distance as

$$
\mathbf {d} _ {\theta} (k) = \{\mathbf {d} _ {\theta_ {1}} (k), \mathbf {d} _ {\theta_ {2}} (k),..., \mathbf {d} _ {\theta_ {N}} (k) \}.\tag{3}
$$

This dictionary, together with an estimate of $\mathbf { C } _ { \mathbf { X } } ( k , l )$ , is used to create candidate MPDR beamformers using Eq. (2), one per candidate target direction, without requiring input-based clean speech or noise statistics. Each candidate MPDR beamformer uses a single direction $\theta _ { i }$ across all frequency bins. The optimal candidate MPDR beamformer is chosen by evaluating the outputs of all candidates and selecting the one that maximizes a performance metric (e.g. a perception-inspired measure, see Section 2.3). This choice of MPDR beamforming is crucial, as it allows each candidate to be constructed without relying on VAD-based input covariance estimates, enabling purely output-driven selection among fixed beamformer settings.

## 2.3. Output-based speech intelligibility prediction

In our output-based system the optimal MPDR beamformer is selected from the candidate set so that a speech-intelligibility-inspired measure is maximized. The evaluation of all candidates is performed on features extracted by a VAD applied to each candidate output.

We express the T-F SNR at the reference microphone as

$$
\mathrm{SNR} (k, l) = 2 0 \log_ {1 0} \left(\frac {| \tilde {S} _ {\alpha} (k , l) |}{| V _ {\alpha} (k , l) |}\right) [ \mathrm{dB} ],\tag{4}
$$

where $\tilde { S } _ { \alpha } ( k , l )$ is the clean target signal at microphone $\alpha ,$ , and $V _ { \alpha } ( k , l )$ is the corresponding noise. A T-F audibility measure $\mathrm { A U D } ( k , l )$ is adopted from the Speech Intelligibility Index (SII) [14, 15] and defined by clipping the T-F SNR to the range $[ - 1 5 , 1 5 ]$ dB and linearly mapping it to [0, 1].

Subsequently, the output-based system includes a SI estimation stage to select the optimal candidate beamformer. For each candidate MPDR beamformer, AUD(k, l) is estimated from its output signal. For this purpose, we employ a neural VAD, see Section 4.2, i.e. a neural network that during inference estimates AUD(k, l) without access to separated speech or noise signals. Since the VAD produces a per–T-F audibility estimate $\widehat { \mathrm { A U D } } ( k , l )$ , we use an intelligibility measure that operates on these audibility patterns. Inspired by the Glimpse Proportion (GP) index [11], we compute a SI measure as:

$$
\mathrm{GP} = \frac {1}{K L} \sum_ {k} ^ {K} \sum_ {l} ^ {L} U (\widehat {\mathrm{AUD}} (k, l) - \gamma_ {\mathrm{GP}}),\tag{5}
$$

where $U ( x )$ is the unit step function and γ<sub>GP</sub> is a configurable threshold. Essentially, GP measures the proportion of T-F tiles that contain glimpses of speech, i.e. T-F tiles where the estimated audibility, and thus the SNR, exceeds a selected threshold. Finally, the candidate whose output yields the highest GP score is selected as the optimal candidate MPDR beamformer. GP as defined in Eq. (5) is suitable for this purpose because it emphasizes speech-dominant T–F regions, making it more sensitive to the target direction than measures dominated by noise. In an initial comparison study (omitted here due to space constraints), GP consistently outperformed other SI and SQ measures estimated from the beamformer outputs.

## 3. INPUT-BASED MVDR BASELINE

As a baseline, we use a conventional input-based MVDR beamformer, which aims to minimize the output noise variance while enforcing a unity gain in the target direction. The weights of the MVDR beamformer are given by [16]

$$
\mathbf {W} _ {M V D R} (k, l) = \frac {\mathbf {C} _ {\mathbf {V}} ^ {- 1} (k , l) \mathbf {d} (k)}{\mathbf {d} ^ {H} (k) \mathbf {C} _ {\mathbf {V}} ^ {- 1} (k , l) \mathbf {d} (k)},\tag{6}
$$

where $\mathbf { C } _ { \mathbf { V } } ( k , l )$ is the noise covariance matrix.

The MVDR beamformer is equivalent to the MPDR if the estimated RTF d(k) is exact and statistics (i.e. $\mathbf { C } \mathbf { v } ( k , l )$ and $\mathbf { C x } ( k , l )$ for MVDR and MPDR beamforming respectively) are known [17]. However, if the RTF is mismatched, e.g. due to estimation errors or incorrect target-direction prediction, the MPDR beamformer may cancel the target signal, causing a substantial performance degradation [18]. Thus, practical MPDR performance tends to be worse than MVDR performance, depending on RTF-estimation accuracy.

For this input-based MVDR baseline, we use the same VAD as in Section 2.3 to identify speech- and noise-dominated T-F tiles, ensuring a fair comparison. Following a common approach [5, 6], ideal binary masks are formed by applying thresholds to the Audibility function. The ideal binary mask for speech is defined as

$$
\widehat {M} _ {S} (k, l) = \left\{ \begin{array}{l l} 0, & \text {if} \quad \widehat {\mathrm{AUD}} (k, l) \leq \gamma_ {S} \\ 1, & \text {if} \quad \widehat {\mathrm{AUD}} (k, l) > \gamma_ {S}, \end{array} \right.\tag{7}
$$

where $\gamma _ { S }$ is a speech threshold. A noise mask $M _ { V } ( k , l )$ is obtained analogously by applying a noise threshold $\gamma _ { V }$ . The speech covariance matrix $\mathbf { C _ { S } }$ can be estimated using, e.g. [5],

$$
\widehat {\mathbf {C}} _ {\mathbf {S}} (k, l) = \sum_ {l = 1} ^ {L} \widehat {M} _ {S} (k, l) \mathbf {X} (k, l) \mathbf {X} ^ {H} (k, l).\tag{8}
$$

The noise covariance matrix $\widehat { \mathbf { C } } _ { \mathbf { V } } ( \boldsymbol { k } , \boldsymbol { l } )$ is calculated similarly using the noise mask $\widehat { M } _ { V } ( \boldsymbol { k } , \boldsymbol { l } )$ . Subsequently, the RTF vector is estimated from $\widehat { \mathbf { C } } _ { \mathbf { S } } ( \boldsymbol { k } , \boldsymbol { l } )$ using the principal eigenvector method [19]. The estimated $\mathbf { C } _ { \mathbf { V } } ( k , l )$ and RTF vector $\mathbf { d } ( k )$ are then inserted into Eq. (6) to compute the MVDR weights.

## 4. EXPERIMENTAL SETUP

## 4.1. Acoustic scene generation

To generate the source signals used in our simulated acoustic scenes, we use speech signals from the Librispeech Corpus [20], and point noise sources from a 10-class subset of the ESC-50 dataset [21] of spatially localized sources (e.g. vacuum cleaner).

![](figures/202c0b925825fdac25bb8ce854e3c2bbae3841dd6af44e28c17ba324313df152.jpg)

![](figures/e68ee2e70e4c808213d0661f8743c346ec15a8f42ff28599ae0318852295a655.jpg)

![](figures/d7ca0dd673c7d4a5c69b6578ba33ea0af8f0321d7ee95e6ebae61d12ff881ab2.jpg)  
Fig. 2: Performance improvements of input-based and output-based systems with respect to the unprocessed noisy input signal, for SN $R _ { i } = $ −5 dB. Lines correspond to mean performance, while the shading represents 25th and 75th quantiles.

![](figures/b4b3bd06fa1cd8b75fa1706ab1214c7e3d7b591bd462578b1d96e064a2df14d8.jpg)

![](figures/17ffdb4745a933b9a60fb16c8cf26d6744b1e1ebc3ba2aa4fbee32f2f2b0dba3.jpg)  
Fig. 3: Performance improvements of input-based and output-based systems for $D _ { T } = 0 . 6 \ \mathrm { s }$

![](figures/49bde92b58de78ac5486ec45f3888d0b86020990b16e3c95ba9e8b535e30c891.jpg)

We then construct acoustic scenes consisting of a HA user, wearing bilateral HAs, i.e. one device on each ear. Each HA is equipped with two microphones, and the left front microphone is arbitrarily selected as the reference microphone. A target talker and one to three point noise sources are placed at random positions on a ring in the horizontal plane of the HAs, with a radius of 1.9 m around the HA user. Isotropic speech-shaped noise (SSN) is also present.

The HA microphone signals are generated by convolving each clean speech and point-noise source with the HA Head-Related Impulse Responses (HRIRs) from the OTIMP dataset [22], which provides HRIRs from 46 individuals with late reverberations removed. For the acoustic scene considered here, we use HRIRs sampled at 48 azimuth angles (7.5° resolution) and at an elevation of 0°.

The convolved signals are summed with isotropic SSN, simulated as a sum of SSN point sources, at the HA microphones. For each mixture, the point-source noise is level-adjusted at the reference microphone to be 5–15 dB above the isotropic SSN floor. Each 5-s utterance uses a new acoustic scene by randomly selecting a HA user (and thus a set of HRIRs), a target location, and one to three point-noise sources, each with a random position. All signals are processed at a sampling rate of 16 kHz, and the STFT is computed using a 128-point FFT, an 8 ms Hann window, and a 4 ms hop size.

## 4.2. VAD model and training procedure

Based on the acoustic scenes described in Section 4.1, we construct a dataset for training a neural VAD model that estimates AUD(k, l) for every T-F tile. The total duration of this dataset is 1 hour, which is split into a 90% train set and 10% test set. Training segments are 1- second-long and are created by dividing the simulated mixtures into non-overlapping 1 s excerpts, while the input SNR is uniformly sampled between -15 and 15 dB. For each utterance, a randomly selected microphone m is used, which serves as a form of data augmentation by exposing the VAD to the variability across microphone channels. Subsequently, min-max scaling is applied, and the stacked real and imaginary parts of X(k, l) form the network input.

The neural VAD is implemented as a Convolutional Recurrent Network (CRN) [23], combining a convolutional encoder-decoder architecture with an LSTM on the encoder’s latent space. The network is trained using the Mean Squared Error (MSE) loss function

$$
L _ {\mathrm{MSE}} = \frac {1}{K L} \sum_ {k} ^ {K} \sum_ {l} ^ {L} (\mathrm{AUD} (k, l) - \widehat {\mathrm{AUD}} (k, l)) ^ {2}.\tag{9}
$$

The architecture is determined in a hyperparameter tuning stage using Bayesian optimization [24], yielding a model with 2.9M parameters. Using the resulting architecture, the network is trained for 300 epochs using the Adam optimizer with a learning rate of 0.016, and a batch size of 32. The encoder and decoder contain five causal convolution layers with kernel size $( k , l ) = ( 3 , 2 )$ , ELU activations [25], batch normalization, and a stride of 2 along the frequency axis. Skip connections link the encoder and decoder, while four stacked LSTM layers are inserted between them. A sigmoid activation on the output maps values to [0, 1].

## 4.3. Implementation details of beamforming systems

The beamforming systems are evaluated using the acoustic scenes described in Section 4.1. The dataset used for beamforming evaluation has a duration of 2 hours and is divided into a validation set and a test set using a 50%-50% split. The validation set is used to tune the hyperparameters $\gamma _ { S } , \gamma _ { V }$ , and $\gamma _ { \mathrm { G P } }$ (defined in Eq. (7) and Eq. (5), respectively) with the goal of maximizing the output SNR of both the proposed and the baseline system.

Table 1: Performance of the input-based MVDR and three output-based MPDR variants under RTF mismatch a $S N R _ { i } = - 5 \mathrm { d B }$ . Bold-faced values indicate significant improvements over the MVDR baseline (Wilcoxon signed-rank test, $p = 0 . 0 5 )$ .

<table><tr><td> $D_T$ </td><td colspan="4">ΔSNR [dB]</td><td colspan="4">ΔESTOI</td><td colspan="4">ΔPESQ</td></tr><tr><td></td><td>Input MVDR</td><td>Output MPDRU</td><td>Output MPDRS</td><td>Output MPDRF</td><td>Input MVDR</td><td>Output MPDRU</td><td>Output MPDRS</td><td>Output MPDRF</td><td>Input MVDR</td><td>Output MPDRU</td><td>Output MPDRS</td><td>Output MPDRF</td></tr><tr><td>0.2</td><td>6.33</td><td>7.40</td><td>7.65</td><td>9.21</td><td>-0.09</td><td>0.02</td><td>0.02</td><td>0.14</td><td>0.00</td><td>0.02</td><td>0.04</td><td>0.07</td></tr><tr><td>0.4</td><td>6.42</td><td>7.69</td><td>7.73</td><td>10.19</td><td>-0.04</td><td>0.11</td><td>0.10</td><td>0.23</td><td>0.02</td><td>0.02</td><td>0.04</td><td>0.09</td></tr><tr><td>0.6</td><td>6.69</td><td>7.88</td><td>7.87</td><td>10.64</td><td>-0.02</td><td>0.15</td><td>0.14</td><td>0.26</td><td>0.02</td><td>0.03</td><td>0.03</td><td>0.10</td></tr><tr><td>0.8</td><td>6.78</td><td>7.95</td><td>7.89</td><td>10.88</td><td>0.00</td><td>0.17</td><td>0.15</td><td>0.28</td><td>0.03</td><td>0.04</td><td>0.03</td><td>0.11</td></tr><tr><td>1.0</td><td>6.78</td><td>7.97</td><td>7.90</td><td>11.00</td><td>0.00</td><td>0.17</td><td>0.16</td><td>0.28</td><td>0.04</td><td>0.03</td><td>0.04</td><td>0.11</td></tr></table>

Each utterance is segmented into non-overlapping segments of duration $D _ { T } .$ , during which beamformer weights remain fixed. As both approaches have access to the full segment before selecting or applying beamformer weights, they are non-causal. A causal implementation would be possible by basing the beamformer selection for each segment on estimates computed from previous segments.

## 5. RESULTS

## 5.1. Output-based MPDR vs. input-based MVDR performance

In this section, we evaluate the proposed output-based MPDR system in comparison with the conventional input-based MVDR baseline across different experimental conditions. Fig. 2 shows the performance of the proposed output-based system and input-based baseline as a function of segment duration $D _ { T }$ , for an input SNR of $\mathrm { S N R } _ { i } = - 5 ~ \mathrm { d B }$ . The evaluation is performed in terms of SNR, ESTOI [26], and PESQ [27]. Across all metrics and durations, the output-based MPDR consistently outperforms the input-based MVDR baseline. A Wilcoxon signed-rank test $( p < 0 . 0 5 )$ was conducted for each performance measure and value of $D _ { T }$ separately, confirming that the observed differences are statistically significant.

The figure also includes the performance of two oracle systems, each representing the upper performance bound for its respective system. The oracle MVDR beamformer has access to the clean speech and noise signals, enabling it to compute the ideal noise covariance matrix $C _ { V }$ and RTF vector. Therefore, this model reflects the maximum performance a time-invariant MVDR beamformer can achieve. In contrast, the oracle MPDR beamformer uses the true RTF corresponding to the target location and thus represents the upper bound for the output-based approach. The performance gap between these two oracle models is mainly due to the duration $D _ { T }$ , as for sufficiently long segments the two models’ performance converge.

A comparison with the oracle models further illustrates the proposed system’s effectiveness. For durations $D _ { T } > 0 . 5 ~ \mathrm { s }$ , the performance of the output-based MPDR beamformer approaches that of the oracle MPDR, indicating that the GP-based selection reliably identifies the optimal beamformer even in challenging conditions.

Fig. 3 presents the systems’ performance for $D _ { T } = 0 . 6 \ \mathrm { s } ,$ i.e. relatively slowly-changing beamformer systems, and input SNR values from -10 dB to +5 dB. A Wilcoxon signed-rank test $( p < 0 . 0 5 )$ shows that performance differences are statistically significant for all metrics, except for PESQ, for $\mathrm { S N R } _ { i } \ \leq \ - 8$ dB. For both SNR and ESTOI, the proposed output-based MPDR beamforming system clearly outperforms the input-based MVDR beamformer, especially at low input SNRs. This behavior reflects the fact that, under such challenging conditions, the input-based VAD struggles to identify speech-dominated T-F tiles correctly, whereas the output-based system can still reliably select the MPDR candidate beamformer pointing towards the correct target direction.

## 5.2. Robustness to RTF mismatch

In Fig. 2 the RTF dictionary was matched, containing that user’s HRTFs, including the one matching the target location. To investigate the robustness of the proposed output-based system under realistic conditions, we introduce two mismatches in the RTF dictionary. In the first case, denoted $\mathbf { M P D R } _ { \mathbf { U } } ,$ , the dictionary contains a lower spatial resolution, i.e. RTFs are spaced 15° apart, with the target between entries. In the second case, denoted MPDR , we use non-individualized RTFs measured on a HATS mannequin, meaning that the RTF dictionary does not match the user. For comparison, MPDR denotes the matched condition, where the dictionary includes the true target RTF, corresponding to the results in Fig. 2.

Table 1 shows the performance of the input-based MVDR beamformer and the three output-based MPDR beamformer variants at $\mathrm { S N R } _ { i } = - 5$ dB. As expected, performance decreases for MPDR and MPDR compared to the fully matched RTFs in MPDR . Nevertheless, despite these mismatches, the output-based MPDR beamformers with mismatched RTFs still outperform the input-based MVDR beamformer in terms of SNR and ESTOI for all values of $D _ { T }$ . A Wilcoxon signed-rank test $( p \ : = \ : 0 . 0 5 )$ confirms that, for both mismatch conditions, the output-based MPDR significantly outperforms the input-based baseline in terms of SNR and ESTOI.

## 6. CONCLUSION

In this work, we introduced a novel output-based processing paradigm in which a speech-processing system is configured by evaluating the quality of its output, rather than relying on features extracted from its noisy input. We demonstrated this paradigm using a beamforming example, proposing an output-based MPDR system for hearing-aid applications. Unlike conventional input-based beamforming, which depends on VAD decisions derived from noisy microphone signals, the proposed approach evaluates candidate beamformers directly from their output, enabling more reliable decisions in adverse acoustic conditions. By incorporating a neural VAD trained to estimate an audibility measure, the system can identify the beamformer configuration that maximizes an estimate of speech intelligibility, even at low input SNRs where input-based methods often fail. Moreover, the proposed system maintains its advantage under RTF mismatch conditions, demonstrating robustness when the dictionary is coarse or non-individualized.

## 7. REFERENCES

[1] Poul Hoang, Jan Mark de Haan, Zheng-Hua Tan, and Jesper Jensen, “Multichannel speech enhancement with own voicebased interfering speech suppression for hearing assistive devices,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 30, pp. 706–720, 2022.

[2] Tim Green, Gaston Hilkhuysen, Mark Huckvale, Stuart Rosen, Mike Brookes, Alastair Moore, Patrick Naylor, Leo Lightburn, and Wei Xue, “Speech recognition with a hearingaid processing scheme combining beamforming with maskinformed speech enhancement,” Trends in Hearing, vol. 26, pp. 23312165211068629, 2022.

[3] Zheng-Hua Tan, Najim Dehak, et al., “rvad: An unsupervised segment-based robust voice activity detection method,” Computer speech & language, vol. 59, pp. 1–21, 2020.

[4] Sharon Gannot, Emmanuel Vincent, Shmulik Markovich-Golan, and Alexey Ozerov, “A consolidated perspective on multimicrophone speech enhancement and source separation,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 25, no. 4, pp. 692–730, 2017.

[5] Jahn Heymann, Lukas Drude, and Reinhold Haeb-Umbach, “A generic neural acoustic beamforming architecture for robust multi-channel speech processing,” Computer Speech & Language, vol. 46, pp. 374–385, 2017.

[6] Minseung Kim, Sein Cheong, and Jong Won Shin, “Dnnbased parameter estimation for mvdr beamforming and postfiltering,” Proceedings of the INTERSPEECH, Dublin, Ireland, pp. 20–24, 2023.

[7] Jesper Jensen and Michael Syskind Pedersen, “Analysis of beamformer directed single-channel noise reduction system for hearing aid applications,” in 2015 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2015, pp. 5728–5732.

[8] Caleb Rascon, “Direction of arrival correction through speech quality feedback,” Digital Signal Processing, vol. 158, pp. 104960, 2025.

[9] Jakob Kienegger, Alina Mannanova, Huajian Fang, and Timo Gerkmann, “Self-steering deep non-linear spatially selective filters for efficient extraction of moving speakers under weak guidance,” arXiv preprint arXiv:2507.02791, 2025.

[10] Sina Hafezi, Alastair H Moore, Pierre H Guiraud, Patrick A Naylor, Jacob Donley, Vladimir Tourbabin, and Thomas Lunner, “Subspace hybrid mvdr beamforming for augmented hearing,” arXiv preprint arXiv:2311.18689, 2023.

[11] Martin Cooke, “A glimpsing model of speech perception in noise,” The Journal of the Acoustical Society of America, vol. 119, no. 3, pp. 1562–1573, 2006.

[12] Mojtaba Farmani, Michael Syskind Pedersen, Zheng-Hua Tan, and Jesper Jensen, “Maximum likelihood approach to “informed” sound source localization for hearing aid applications,” in 2015 IEEE international conference on acoustics, speech and signal processing (ICASSP). IEEE, 2015, pp. 16– 20.

[13] Jack Capon, “High-resolution frequency-wavenumber spectrum analysis,” Proceedings of the IEEE, vol. 57, no. 8, pp. 1408–1418, 1969.

[14] Benjamin WY Hornsby, “The speech intelligibility index: What is it and what’s it good for?,” The Hearing Journal, vol. 57, no. 10, pp. 10–17, 2004.

[15] Caslav Pavlovic, “Sii—speech intelligibility index standard: Ansi s3. 5 1997,” the Journal of the Acoustical Society of America, vol. 143, no. 3 Supplement, pp. 1906–1906, 2018.

[16] Joerg Bitzer and K. Uwe Simmer, Superdirective Microphone Arrays, pp. 19–38, Springer Berlin Heidelberg, Berlin, Heidelberg, 2001.

[17] Harry L Van Trees, “Optimum waveform estimation,” Optimum Array Processing, vol. 4, pp. 428–709, 2002.

[18] Henry Cox, “Resolving power and sensitivity to mismatch of optimum array processors,” The Journal of the acoustical society of America, vol. 54, no. 3, pp. 771–785, 1973.

[19] Xingwei Sun, Ziteng Wang, Risheng Xia, Junfeng Li, and Yonghong Yan, “Effect of steering vector estimation on mvdr beamformer for noisy speech recognition,” in 2018 IEEE 23rd International Conference on Digital Signal Processing (DSP). IEEE, 2018, pp. 1–5.

[20] Vassil Panayotov, Guoguo Chen, Daniel Povey, and Sanjeev Khudanpur, “Librispeech: an asr corpus based on public domain audio books,” in 2015 IEEE international conference on acoustics, speech and signal processing (ICASSP). IEEE, 2015, pp. 5206–5210.

[21] Karol J Piczak, “Esc: Dataset for environmental sound classification,” in Proceedings of the 23rd ACM international conference on Multimedia, 2015, pp. 1015–1018.

[22] Alastair H Moore, Jan Mark de Haan, Michael Syskind Pedersen, Patrick A Naylor, Mike Brookes, and Jesper Jensen, “Personalized signal-independent beamforming for binaural hearing aids,” The Journal of the Acoustical Society of America, vol. 145, no. 5, pp. 2971–2981, 2019.

[23] Ke Tan and DeLiang Wang, “A convolutional recurrent neural network for real-time speech enhancement.,” in Interspeech, 2018, vol. 2018, pp. 3229–3233.

[24] Ian Dewancker, Michael McCourt, and Scott Clark, “Bayesian optimization primer,” URL https://app. sigopt. com/static/pdf/SigOpt Bayesian Optimization Primer. pdf, 2015.

[25] Djork-Arne Clevert, Thomas Unterthiner, and Sepp Hochreiter,´ “Fast and accurate deep network learning by exponential linear units (elus),” arXiv preprint arXiv:1511.07289, vol. 4, no. 5, pp. 11, 2015.

[26] Jesper Jensen and Cees H Taal, “An algorithm for predicting the intelligibility of speech masked by modulated noise maskers,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 24, no. 11, pp. 2009–2022, 2016.

[27] Antony W Rix, John G Beerends, Michael P Hollier, and Andries P Hekstra, “Perceptual evaluation of speech quality (pesq)-a new method for speech quality assessment of telephone networks and codecs,” in 2001 IEEE international conference on acoustics, speech, and signal processing. Proceedings (Cat. No. 01CH37221). IEEE, 2001, vol. 2, pp. 749–752.