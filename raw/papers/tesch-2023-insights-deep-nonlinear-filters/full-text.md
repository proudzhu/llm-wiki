# Insights Into Deep Non-linear Filters for Improved Multi-channel Speech Enhancement

Kristina Tesch , Student Member, IEEE, and Timo Gerkmann , Senior Member, IEEE

Abstract—The key advantage of using multiple microphones for speech enhancement is that spatial filtering can be used to complement the tempo-spectral processing. In a traditional setting, linear spatial filtering (beamforming) and single-channel post-filtering are commonly performed separately. In contrast, there is a trend towards employing deep neural networks (DNNs) to learn a joint spatial and tempo-spectral non-linear filter, which means that the restriction of a linear processing model and that of a separate processing of spatial and tempo-spectral information can potentially be overcome. However, the internal mechanisms that lead to good performance of such data-driven filters for multi-channel speech enhancement are not well understood.

Therefore, in this work, we analyse the properties of a nonlinear spatial filter realized by a DNN as well as its interdependency with temporal and spectral processing by carefully controlling the information sources (spatial, spectral, and temporal) available to the network. We confirm the superiority of a nonlinear spatial processing model, which outperforms an oracle linear spatial filter in a challenging speaker extraction scenario for a low number of microphones by 0.24 POLQA score. Our analyses reveal that in particular spectral information should be processed jointly with spatial information as this increases the spatial selectivity of the filter. Our systematic evaluation then leads to a simple network architecture, that outperforms state-ofthe-art network architectures on a speaker extraction task by 0.22 POLQA score and by 0.32 POLQA score on the CHiME3 data.

Index Terms—Multi-channel, speech enhancement, joint non-linear spatial and tempo-spectral filtering

## I. INTRODUCTION

In our everyday life, speech understanding often takes place in noisy environments. This can be, for example, a conversation in a crowded restaurant, a phone call in a busy train station or the use of a voice control system in a driving car. To enable devices such as hearing aids or voice-controlled assistants to function in these challenging acoustic environments, speech enhancement algorithms are employed to improve the speech quality and intelligibility of the target speech signal.

Traditionally, many algorithms utilized a short-time Fourier transform (STFT) signal representation and derived an analytical clean speech estimator from a statistical model, e.g., [1]–[4]. While this has led to many interpretable and computationally lightweight algorithms, the derivations often require restricting and simplifying assumptions, e.g., independent time-frequency bins, to keep the problem tractable. This is in contrast to DNNbased algorithms, which do not need an explicit model, but learn to recognize complex dependencies directly from training data. In the domain of single-channel speech enhancement, these DNN-based algorithms, have been dominating the state of the art for a couple of years now, e.g., [5]–[8].

![](figures/f013212dee5dae4c3c4fc216a9645a625bcce00cddc414a5434b29f648cf3b9e.jpg)  
Fig. 1: (a) The traditional two-step processing using a linear spatial filter (beamformer) followed by a single-channel postfilter. (b) A joint spatial and tempo-spectral non-linear processing scheme that we implement using DNNs in this work. (c) Two-step processing scheme, however, not only the postfilter performs non-linear filtering but also the spatial filter.

While single-channel speech enhancement approaches exploit tempo-spectral signal characteristics to perform the enhancement, multi-channel approaches can additionally leverage spatial information by using multiple microphones. Commonly, this is done by employing a linear spatial filter, a so-called beamformer. Figure 1a illustrates a traditional multichannel processing pipeline, which first applies the linear spatial filter and then adds a single-channel post-filter in a second step. The post-filter can be either linear or non-linear. In our prior work [9], [10], we have demonstrated that separation into a linear spatial filter and a post-filter is generally not optimal in the minimum mean square error (MMSE) sense unless we restrict the noise distribution to be Gaussian. However, if a non-Gaussian distribution is assumed, the resulting analytical solution is overall non-linear and joins the spatial and spectral processing as illustrated in Figure 1b. Our experimental evaluation in [10] has shown great potential for a joint nonlinear spatial-spectral filter, but has also led to the conclusion that the estimation of required higher-order parameters limits the practical applicability of the analytic estimator. However, DNNs provide a data-driven way to implement practical joint spatial and tempo-spectral non-linear filters (JNF).

A very influential paper on multi-channel speech enhancement using DNNs has been the paper by Heymann et al. [11], who propose to use a DNN for estimating the parameters of a linear spatial filter. Also others have proposed approaches along this line of research, e.g., [12]–[14]. However, using a DNN for parameter estimation does not allow for a more general non-linear processing model nor does it permit the exploitation of interdependencies between spatial and tempospectral information during processing. In contrast, a variety of data-driven multi-channel filters have been proposed recently [15]–[20]. These implicitly drop the linearity assumption and integrate spatial and tempo-spectral processing steps such that this class of joint non-linear approaches is fundamentally different and potentially more powerful than DNN-driven linear spatial filters, aka neural beamformers. Good performance as been reported for these deep non-linear filters, but the internal mechanisms that lead to good performance are not well understood. This, however, is essential for a deliberate design of a neural network architecture that fully unlocks the potential of neural networks for multi-channel speech enhancement.

In this work, we investigate the internal functioning of DNN-based (joint) non-linear filters for multi-channel speech enhancement. To learn about the role of a non-linear spatial filter and the interdependency between spatial and tempospectral information, we consider a second separated approach, which combines a non-linear spatial filter with an independent post-filter. An illustration of this setup is given in Figure 1c. A systematic comparison of the three approaches outlined in Figure 1 then allows us to assess what makes for good spatial filtering performance: Is non-linear as opposed to linear spatial filtering the main factor for good performance? Or is it rather the interdependency between spatial and tempo-spectral processing? And do temporal and spectral information have the same impact on spatial filtering performance?

This paper is based on our recent conference paper [21], but the experimental evaluation here goes far beyond the results presented previously. Specifically, we propose new experimental designs to investigate the spatial filtering performance of a DNN-based joint filter. This then allows for a discussion of the spatial selectivity of the different approaches. We include a comparison with state-of-the-art approaches, showing that the joint non-linear filter obtained by our systematic evaluation outperforms them and, furthermore, we extend our evaluations from the speaker extraction task to the CHiME3 dataset. The latter then enables us to assess the role of the dataset characteristics with respect to the previously mentioned research questions.

In a recent study, also Tan et al. [22] compare the performance of a joint spatial and tempo-spectral non-linear filter with a DNN-driven linear spatial filter plus additional post-filter (i.e. Figure 1a versus Figure 1b). While they report comparable performance for these two approaches, in this paper, in line with our theoretical findings in [10], we demonstrate the conceptual superiority of a joint non-linear spatial and tempo-spectral filter by outperforming an oracle linear spatial filter plus post-filter. Furthermore, our work adds additional value beyond a general performance comparison of the two approaches by presenting experiments that allow for insights into the internal mechanisms underlying a well-performing joint non-linear filter.

The remainder of this paper is structured as follows. Section II introduces the signal model and provides a detailed overview of traditional and DNN-based spatial filtering. In Section III, we introduce a set of DNN-based filter variants, which will be analyzed thoroughly to provide insights into the separability of spatial processing and post-filtering (Section IV-B) and the interdependency between spatial and tempo-spectral processing (Section IV-C). In Section IV, we provide a comparison with recent state-of-the-art methods and, in Section VI, we report results for the CHiME3 dataset.

## II. BACKGROUND AND RELATED WORK

## A. Signal model

We consider the task of extracting a single target speaker from a recording obtained in a noisy and reverberant environment. The noise signals may be environmental noise or concurrent speakers. The noisy mixture signals are captured by a microphone array with $C$ microphone channels. In the time-domain, the speech signal uttered by the target speaker and recorded by the \`th microphone can be written as the convolution of the non-reverberant speech signal $s ( t )$ and the room impulse response (RIR) $h _ { \ell } ( t )$ describing the propagation path between the speaker and the \`th microphone [23]:

$$
x _ {\ell} (t) = s (t) * h _ {\ell} (t).\tag{1}
$$

Note that, besides the room characteristics, $h _ { \ell } ( t )$ also allows to model the characteristics of the loudspeaker and the microphones.

We transform the time-domain signal $x _ { \ell } ( t )$ into the frequency domain using a short-time Fourier transform (STFT) to obtain complex spectral coefficients $X _ { \ell } ( k , i ) \in \mathbb { C }$ with frequency-bin index k and time-frame index i. Based on an additive signal model, the mixing process in the frequency domain is given by

$$
Y _ {\ell} (k, i) = X _ {\ell} (k, i) + V _ {\ell} (k, i).\tag{2}
$$

with $V _ { \ell } ( k , i )$ denoting the noise signal recorded at the \`th microphone. We use bold face symbols to refer to the vector stacking the STFT coefficients for all channels, $\mathrm { e . g . }$ $\mathbf { Y } ( k , i ) = [ \bar { Y _ { 1 } } ( k , i ) , . . . , Y _ { C } ( k , i ) ] ^ { T } \in \mathbb { C } ^ { C }$ and drop the time-frequency indices $( k , i )$ to denote the tensor with shape $( C \times F \times T )$ comprising the time-frequency points for all C microphones and with F and $T$ being the number of frequency-bins and time-indices respectively.

## B. Traditional spatial filtering

Most traditional multi-channel speech enhancement schemes involve a spatial filter that is usually implemented following a filter-and-sum beamforming approach [24, Sec. 12.4.2]. Such a filter-and-sum beamformer aims to suppress signal components not originating from the target direction by filtering the individual microphone signals and adding them. Using vector notation, the processing model of a filter-and-sum beamformer in the frequency domain can be formulated as

$$
\hat {S} (k, i) = \mathbf {h} (k, i) ^ {H} \mathbf {Y} (k, i)\tag{3}
$$

with $\hat { S } ( k , i ) \in \mathbb { C }$ being an estimate of the target signal, a filter $\mathbf { h } ( k , i ) \in \mathbb { C } ^ { C }$ that may or may not be depending on the time index i (time-variant vs. time-invariant filter) and $( \cdot ) ^ { H }$ denoting the Hermitian transpose.

The simplest form is a delay-and-sum beamformer [24, Sec. 12.4.1] that applies a filter to compensate for different time delays at the microphones caused by the differing lengths of propagation paths for the signal to reach each microphone. This approach implicitly assumes the noise signals recorded at the different microphones to be uncorrelated [24, Sec.12.6.1], which is a reasonable assumption for sensor noise, but not for environmental noise or interfering point sources.

Another commonly used spatial filter is the minimum variance distortionless response (MVDR) beamformer [24, Sec. 12.6.1] that takes into account the correlation between microphone channels. The filter weights $\mathbf { h } _ { \mathrm { M V D R } } ( k , i )$ are obtained by solving the optimization problem

$$
\begin{array}{c} \mathbf {h} _ {\mathrm{MVDR}} (k, i) = \underset {\mathbf {h} \in \mathbb {C} ^ {C}} {\arg \min} \mathbf {h} ^ {H} (k, i) \boldsymbol {\Phi} _ {V} (k, i) \mathbf {h} (k, i) \\ \text {s.t.} \quad \mathbf {h} (k, i) ^ {H} \mathbf {d} (k, i) = 1, \end{array}\tag{4}
$$

with the so-called steering vector $\mathbf { d } ( k , i )$ modelling the direct path of the target signal $S ( k , i )$ to the microphones and noise correlation matrix $\Phi _ { V } ( \vec { k } , i ) = \mathbb { E } [ \mathbf { V } ( k , i ) \mathbf { V } ( k , i ) ^ { H } ]$ with E denoting the statistical expectation operator. Thus, the MVDR beamformer tries to minimize the noise variance at the output of the beamformer while leaving the target signal unchanged. The latter condition is referred to as the distortionless constraint of the MVDR. The solution of the optimization problem posed in (4) is given by [24, Sec. 12.6.1]

$$
\mathbf {h} _ {\mathrm{MVDR}} (k, i) = \frac {\boldsymbol {\Phi} _ {V} ^ {- 1} (k , i) \mathbf {d} (k , i)}{\mathbf {d} ^ {H} (k , i) \boldsymbol {\Phi} _ {V} ^ {- 1} (k , i) \mathbf {d} (k , i)}.\tag{5}
$$

Adhering to the filter-and-sum processing model, and using filter weights that do not depend on the value of the noisy signal ${ \bf Y } ( k , i )$ itself as in (5), traditional spatial filtering clearly is a linear operation with respect to the noisy input.

It has been shown that the MVDR beamformer is the optimal spatial filter under a Gaussian noise assumption [10], [25]. That is, any filter jointly performing spatial filtering and postfiltering can (in theory) be decomposed into an MVDR beamformer for spatial processing followed by a single-channel postfilter. A prominent example is the multi-channel Wiener filter, which can be decomposed in an MVDR plus single-channel Wiener filter [26]. The work by Hendriks et al. [27] and our prior work [10] reveal that this is not the case for more general noise distributions. The analytic filter derived in [10], [27] joins the spatial and spectral filtering into a non-separable non-linear operation which is in contrast to the simple and linear processing model of a beamformer. Our own previous work [10] demonstrates that such a joint spatial-spectral nonlinear processing may overcome the limitations of a linear beamformer, which is restricted to suppressing M − 1 directional interfering point sources (maximum number of sources in a reverberation-free setting). However, oracle knowledge of the target and noise signals are required for accurate parameter estimation to obtain good results with the analytic joint spatial-spectral nonlinear filter.

## C. DNN-based spatial filtering

While state-of-the-art single-channel speech enhancement nowadays completely relies on DNN-based approaches, DNNbased multi-channel approaches have become a vivid research topic recently. An important step towards using the capabilities of neural networks for multi-channel speech enhancement was taken by Heymann et al. [11], who design a DNN-based parameter estimation scheme for computing estimates of the steering vector and noise correlation matrix to be used in a traditional

MVDR beamformer. This method has gained a reputation for its ease of use as well as good and robust results. Similarly, Togami [12] proposes to extract speaker masks for facilitating covariance matrix and speech power estimation to be used in a multi-channel speech separation scheme. Liu et al. [13] extend the masking-based beamforming approach of [11] by processing multi-channel instead of a collection of single-channel inputs and providing cross-channel features. Xiao et al. [14] train a network to directly estimate the time-invariant filter weights h(k) of a filter-and-sum beamformer from cross correlation features. The main drawback of a method that uses the impressive modeling capabilities of neural networks only for parameter estimation to be used in classical linear processing scheme is that the limitations of the linear model itself cannot be overcome.

In another line of research, spatial features are used as additional input to a neural network to increase speech separation or enhancement performance, e.g., [28]–[31]. The most common spatial features are inter-channel time or phase differences (ITD/IPD), inter-channel level differences (ILD), cross-correlation based features, as well as features computed with fixed beamformers. Most of these works, show notable performance improvements over single-channel approaches proving that spatial information is very valuable for speech separation and enhancement tasks. As for all approaches using hand-crafted features, a major concern is the question whether the chosen feature design is optimal for the task at hand. For example, in [32] and [33] the authors propose to estimate beam forming weights from speech and noise second-order statistics (covariance matrix estimates) using a DNN, while our analysis in [10] suggests that higher-order statistics are a valuable source of information, which can not be exploited this way.

An increasing number of recent works skips the spatial feature design part and trains a DNN-based filter to perform speech enhancement or separation based on raw multi-channel signals, either providing the time-domain signals [34]–[38] or frequency-domain signals [15]–[20] as input to the network. In many of these works, the authors claim that the network architecture has been designed with the goal in mind to implicitly learn a spatially selective filter from data. Nonetheless, the architectures proposed in these papers differ notably from each other. While some authors propose to learn a mask that is applied to a reference channel of the noisy signal, e.g., [15], [17], others propose a network that outputs the real and imaginary part of the target clean speech signal [18] or to learn a set of coefficients h and apply them to the signal adhering to the filter-and-sum processing model (cf. (3)) [19], [35].

For the last mentioned approach, it is clear that the authors have derived their architecture design from traditional linear filter-and-sum beamforming, but also others claim their architecture to be inspired be the traditional spatial filters, e.g., [17]. The authors of EaBNet [19] even propose to append the DNN-based spatial filter with a (DNN-based) post-filter following the traditional two-step procedure. However, it is important to be aware that their “spatial filter” as well as all other DNN-based approaches referenced in the last paragraph are in principle not only capable of performing non-linear spatial filtering but will likely perform spatial filtering jointly with tempo-spectral postfiltering. As a consequence, a direct comparison with a traditional linear beamformer, for example the MVDR beamformer, without a post-filter can therefore not be considered a fair comparison.

Overall, we conclude that many interesting architectures for implementing a DNN-based filter for multi-channel speech enhancement have been proposed, but also a lot of open questions remain. Most approaches haven been evaluated with respect to their overall speech enhancement performance. However, this is not very informative with regard to the internal mechanisms of the network. For example, it is unclear whether a network architecture inspired from traditional beamforming performs particularly well in spatial filtering as hypothesized by many authors, since performance improvements could also be achieved by better exploitation of tempo-spectral information. Thus, a more systematic evaluation is required to provide insights in the internal mechanisms of these DNN-based filters.

## III. PROPOSED APPROACH

In this work, we aim to investigate the contribution of different sources of information, that is spatial, spectral and temporal information, to a DNN-based filter for a speech enhancement or speech extraction problem. We are particularly interested in understanding the nature of a non-linear spatial filter and its interdependencies with temporal and spectral information. To provide insights into the “black box” of a DNN-powered filter, we use a simple network structure that allows us to easily control the integration of different sources of information and a dataset that makes it easy to assess the quality and properties of the spatial filter. This section describes the network design used in our experiments.

## A. Base network architecture (F-JNF, T-JNF)

For our experiments, we adapt the architecture proposed by Li and Horaud [15], [39], that performs speech enhancement using a mask estimated from narrow-band multi-channel inputs. The distinctive feature of their approach is that the network processes all frequency bands separately. The network weights, however, are shared between frequencies. In the following, we propose a number of alternative network architectures to enable a detailed analysis. Figure 2 depicts the base network architecture. As can be seen in the bottom part, the network consists of only three layers, two (bi-directional) long shortterm memory (LSTM) layers followed by a feed-forward (FF) layer. An LSTM layer [40] is commonly used for sequence modeling. In our setup, the feature dimension (vertical) mostly corresponds to channel information (real and imaginary parts stacked) while the sequence dimension (horizontal) is chosen according to the second source of information which could be time (narrow-band) or spectral (wide-band) information. As spatial information is processed jointly with a second source of information, we denote this network as joint non-linear filter (JNF) prefixed with T or F in the narrow-band and wide-band case respectively. Thus, the narrow-band version (T-JNF) as proposed in [15] has access to fine-grain spatial and temporal information but only global spectral statistics, while our proposed variant F-JNF can leverage fine-grained spectral information in addition to spatial information.

## B. Combining temporal and spectral information (FT-JNF)

The basic architecture described in Section III-A combines spatial information with spectral or temporal information. Next, we propose a variant that can exploit all three sources of information combining spatial with tempo-spectral processing. In order to ensure comparability of the results, we do not change the basic architecture or the number of parameters. Instead, we manipulate the data arrangement at the position marked with a circled two. The filter denoted by FT-JNF then feeds wide-band data into the first LSTM layer. The obtained features are then switched to a narrow-band arrangement before input to the second LSTM layer. This way, the FT-JNF can potentially exploit all three sources of information.

## C. Non-linear spatial filtering (T-NSF, F-NSF, FT-NSF)

To study the properties of a non-linear spatial filter (NSF) separately from the tempo-spectral processing, we define three additional variants of the the network architecture: T-NSF, F-NSF, and FT-NSF. The underlying idea is to prevent the network from employing fine-grained temporal and spectral information by randomly permuting the data along the sequence dimension before feeding it into the LSTM at position ➀. The inverse permutation operation is then applied before the FF layer at position ➂. Accordingly, only global statistics with respect to the frequency or time dimension are available but correlations between neighboring frequencies or time steps cannot be exploited. Preliminary experiments have shown that the spatial processing using a wide-band data arrangement (F-NSF) performs poorly if the frequency-bin index is unknown to the network. This is likely because the spatial characteristics of the data depend strongly on the frequency-bin index. To ensure that this information is still available after shuffling along the sequence dimension, we append the frequency-bin index to the feature dimension. We do this also for a narrowband data arrangement (T-JNF) but in this case the effect on the performance is minor. Analogous to the procedure described in Section III-B, we define a non-linear spatial filter that incorporates both global spectral and global temporal information. This is achieved by again switching from wide-band to narrowband data arrangement at position ➁ and requires both LSTM layers to be wrapped in permutation and inverse permutation operations with respect to the respective sequence dimension.

## D. DNN-based post-filtering (PF)

Finally, we introduce a single-channel post-filter that jointly processes temporal and spectral information. For consistency, we stick to the simple base architecture shown in Figure 2. Here, the real and imaginary parts of the single-channel input data are stacked along the frequency dimension to form the feature dimension. The time axis is then used as sequence dimension.

## E. Lossfunction and training details

We train the networks based on a complex ideal ratio mask (cIRM) [41] in favor of a magnitude ideal ratio mask (IRM) as in [15] to facilitate phase enhancement. For this reason, the FF layer is followed by a tanh activation function, which outputs a compressed mask estimate. We use compression parameters $K = C = 1$ as defined in [41]. The enhanced signal is then obtained by multiplication of the uncompressed target speech cIRM $\mathcal { M } _ { \mathrm { S } } ( k , i ) \in \mathbb { C }$ with the noisy recording $Y _ { 0 } ( k , i )$ using the first channel as reference, i.e.,

![](figures/fd64afc8656f525218233e5246b50a1614fbab41b62dafb0be4a7372dfadff71.jpg)  
Fig. 2: Illustration of the base system architecture. The input data is arranged according to a wide-band or narrow-band input and fed into a network with two LSTM layers, an FF layer and tanh activation to obtain an estimate of a cIRM.

$$
\hat {S} (k, i) = \mathcal {M} _ {\mathrm{S}} (k, i) \cdot Y _ {0} (k, i).\tag{6}
$$

The real and imaginary parts of the noise cIRM $\mathcal { M } _ { \mathrm { V } }$ can be obtained from the real and imaginary part of the target speech cIRM using [17]:

$$
\mathrm{Re} (\mathcal {M} _ {\mathrm{V}}) = 1 - \mathrm{Re} (\mathcal {M} _ {\mathrm{S}}),\tag{7}
$$

$$
\operatorname{Im} (\mathcal {M} _ {\mathrm{V}}) = - \operatorname{Im} (\mathcal {M} _ {\mathrm{S}}).\tag{8}
$$

The noise cIRM estimate can be used to obtain an estimate of the pure noise component contained in the signal, i.e,

$$
\hat {V} (k, i) = \mathcal {M} _ {\mathrm{V}} (k, i) \cdot Y _ {0} (k, i).\tag{9}
$$

We use the loss function proposed by Tolooshams et al. [17], which is composed of time and frequency domain $\ell _ { 1 }$ loss terms:

$$
L (s, \hat {s}) = \sum_ {u \in \{s, v \}} \alpha \| u - \hat {u} \| _ {1} + \left\| | U | - | \hat {U} | \right\| _ {1}.\tag{10}
$$

Here, the frequency-domain terms $\hat { S }$ and $\hat { V }$ are estimated as given in (6) and (9) and time-domain quantities are obtained by an inverse STFT. We set $\alpha { = } 1 0$ to equalize the contribution of either domain in the loss term.

As can be seen from the loss function, our training scheme uses the noisy observations ${ \bf y } ( t )$ , which serves as network input, as well as the ground truth noise signals v(t) recorded at the microphones and the non-reverberant signal s(t), which has been aligned with the noisy observation to include the propagation delay. If the ground truth for the noise signal is unknown, we only use the clean speech related parts of the loss function. During training, we randomly extract three seconds of audio from an utterance and compute the STFT using a 32 ms long window with 50% overlap. The Hann window is applied for analysis and synthesis. We train the networks with batch size six until convergence with maximum 250 epochs and select the best model with respect to the validation loss. The number of LSTM units is set to 256 and 128 for all networks, except PF, for which 256 units are used in both layers. The Adam optimizer [42] with learning rate 0.001 is used.

TABLE I: For each sample, the room characteristics are obtained by sampling uniformly from the value ranges given in this table.

<table><tr><td>Width</td><td>Length</td><td>Height</td><td>T60</td></tr><tr><td>2.5-5 m</td><td>3-9 m</td><td>2.2-3.5 m</td><td>0.2-0.5 s</td></tr></table>

## IV. ANALYSIS OF THE INTERPLAY

## OF SPATIAL WITH TEMPO-SPECTRAL INFORMATION

In this section, we evaluate the previously described networks in a speaker extraction scenario with a single speaker that is to be extracted and five additional interfering speech sources. Such a scenario seems particularly suitable to study the spatial filtering capabilities of a processing method since a spatially selective filter, as opposed to a filter that mainly exploits tempo-spectral information, is expected to be the key to good performance on this task. This is because the target signal has very similar tempo-spectral properties as the interfering signal (five speakers) but the signals differ decisively in their spatial properties.

## A. Dataset

We generate a simulated dataset using pyroomacoustics [43], which provides an implementation of the source-image model [44]. The setup is illustrated in Figure 3. For each sample, the room dimensions and the reverberation time are uniformly sampled from the value ranges given in Table I. We use a circular microphone array with a diameter of 10 cm and between two and five channels. The microphone array is placed at a random position in the xy-plane but at least 1 m away from the walls, and it is located at a height of 1.5 m. As depicted in Figure 3, a rotation $\varphi$ is applied to the microphone array sampled from the interval [0,2π). In our setup, the target speaker has to be identified by its spatial location. Accordingly, we place the target speaker in a fixed position relative to the microphone orientation on the blue dotted line in Figure 3. Its distance to the microphone array ranges between 0.3 m and 1 m. The five interfering sources are placed in the gray area with a minimum distance of 1 m to the microphone array location. As indicated by the white area, a room spanned by the 20<sup>◦</sup> angle to either side of the target source is also kept free of interferers. To ensure an even distribution of sources in the room, we place one interfering source per segment as indicated by the dashed gray lines. The height of the interfering speech sources is sampled from a normal distribution with mean 1.6 m and standard deviation 0.08.

![](figures/3cfbcb8331b2ef7755a25729eccd7475af2b703fcfa8870ffd51f5bea4e1f6ff.jpg)  
Fig. 3: Illustration of the simulation setup. The target source is located in a fixed orientation with respect to microphone array. The five interfering sources are placed in the gray area (one per segment). Room properties are sampled from the given ranges.

We generate 6000, 1000, and 600 samples with a sampling frequency of 16 kHz for training, validation and testing respectively using clean speech signals from the WSJ0 dataset [45]. Signals between the different sets do not overlap. The signal-tonoise ratio (SNR) is not explicitly controlled but obtained from the the simulation setup with varying distances of the sources to the microphone array. The average SNR is −4 dB and 95% of the data samples distribute between −9 dB and 2 dB SNR.

## B. Separability of spatial processing and post-filtering

Figure 1a illustrates the traditional two-step approach with a spatial filter that is applied first and a single-channel post-filter for tempo-spectral processing that is applied in a second processing step. Such a modular design is desirable as it offers flexibility and interpretability, however, the analytical MMSE solution in a non-Gaussian noise scenario is non-linear and non-separable [10]. The MMSE-optimal solution thus corresponds to the joint spatial and (tempo-)spectral filter depicted in Figure 1b. However, it is unclear if the third option of using a non-linear spatial filter as depicted in Figure 1c is a meaningful concept or if non-linear spatial processing is only useful if tempo-spectral information and spatial information are processed jointly as in Figure 1b. For this reason, in this section, we investigate if a DNN-based non-linear filter can be separated into spatial processing and single-channel tempo-spectral post-filtering by comparing the performance of all three configurations shown in Figure 1.

The left plot in Figure 4 shows the mean perceptual objective listening quality analysis (POLQA) score [46] and the 95% confidence interval for a varying number of microphones. The POLQA algorithm is the successor to the perceptual evaluation of speech quality (PESQ) measure [47]. It measures speech quality based on mean opinion score (MOS) scale ranging from one (bad) to five (excellent). The dashed lines correspond to spatial-only filters. That is the traditional MVDR beamformer (green) and the FT-NSF described in Section III-C (blue). The parameters of the MVDR beamformer are estimated from oracle data. We compute the time-varying noise covariance estimate by recursive averaging of the pure noise data and estimate the acoustic transfer function (ATF) by multiplying the principal eigenvector of the generalized eigenvalue problem for speech and noise covariance matrices with the speech covariance matrix as described in [48].

![](figures/1c1c9cccd1deeba0e11d1822da933437367bd14b1618a9dea8dbc8e13f808ece.jpg)  
Fig. 4: We report the mean POLQA and ESTOI scores along with the 95% confidence interval for a set of multi-channel filters. This figure shows that joint spatial and tempo-spectral filtering (FT-JNF) outperforms a nonlinear spatial filter plus a postfilter (FT-NSF+PF).

Even though the MVDR parameters were accurately estimated from oracle data, which means that the MVDR should be considered as an upper bound on the spatial filtering performance achievable with a linear processing model, the non-linear spatial filter excluding a tempo-spectral post-filtering yields higher POLQA scores, in particular for a small number of microphones. A spectrogram visualization for three microphones is shown in Figure 5. The results obtained with a linear spatial filter (LSF) and a non-linear spatial filter (FT-NSF) are depicted in the middle row. Differences in the behavior are clearly visible: While the MVDR is distortionless by design at the cost of little noise suppression in this difficult noise scenario, the non-linear spatial filter aggressively reduces noise, but introduces quite some speech distortions. Please find audio examples on our website<sup>1</sup>. Next, we combine each spatial filter with an independent single-channel post-filter. For this, the DNN described in Section III-D is trained using the output of the MVDR and FT-NSF evaluated on the training set as network input. The results for these two-step approaches are shown in Figure 4 using the same marker as the corresponding spatial filter but with a solid line. We find that the post-filter added to the non-linear spatial filter (FT-NSF+PF) does not result in a notable performance improvement. In effect, the purple line runs almost exactly on top of the blue dashed line. This can be explained by the fact that speech information, which was lost already during spatial processing, cannot be recovered by multiplication with the postfilter mask. In contrast, the MVDR beamformer does not distort the clean speech signal, and adding a single-channel post-filter, represented by the red solid line, is very effective. Here, we observe a performance boost between 0.18 POLQA score (two microphones) and 0.5 POLQA score (three microphones) in comparison with the linear spatial filter only.

![](figures/74af18faead01d13efcf9c72941ca6610178357bfaf73df6cb78ee40831e24e4.jpg)  
Fig. 5: Spectrogram visualization of an example utterance. The target signal and the noisy observation are displayed in the top row. The middle row shows two spatial filters, a linear MVDR on the left and a DNN-based non-linear on the right. The bottom depicts the MVDR with an independent post-filter and the joint spatial and tempo-spectral filter.

Finally, we compare with the joint non-linear spatial and tempo-spectral filter FT-JNF. As visible in Figure 1b, the separation of spatial and tempo-spectral processing has been removed, which allows the network described in Section III-B to exploit the interdependencies between spatial and tempospectral information. This joint approach, depicted by the solid orange line, clearly outperforms the separated linear spatial filter plus post-filter approach for a low number of microphones. For two microphones the difference even amounts to 0.44 POLQA score. With an increased number of microphones, the gap between the orange line (FT-JNF) and the red line (LSF+PF) decreases or inverts even for ESTOI [49] depicted in the right plot. This is not very surprising as the number of anechoic point sources that can be canceled by the oracle MVDR increases by one for every added microphone. Accordingly, the performance of the spatial filter improves considerably with every microphone added, and when combined it with a strong post-filter, it becomes increasingly difficult to outperform the oracle MVDR plus post-filter with a data-driven filter.

TABLE II: Impact of different sources of information (spectral (F) and temporal (T)) used besides spatial information. We report mean improvements and the 95% confidence interval.

<table><tr><td></td><td>Δ POLQA</td><td>ESTOI</td></tr><tr><td>F-NSF</td><td>0.78 ± 0.03</td><td>0.62 ± 0.012</td></tr><tr><td>T-NSF</td><td>0.46 ± 0.03</td><td>0.54 ± 0.013</td></tr><tr><td>FT-NSF</td><td>0.87 ± 0.03</td><td>0.64 ± 0.011</td></tr><tr><td>F-JNF</td><td>1.15 ± 0.04</td><td>0.70 ± 0.011</td></tr><tr><td>T-JNF [15]</td><td>0.74 ± 0.03</td><td>0.63 ± 0.012</td></tr><tr><td>FT-JNF (proposed)</td><td>1.43 ± 0.04</td><td>0.76 ± 0.009</td></tr></table>

Overall, two conclusions emerge from these results: First, the joint non-linear spatial and tempo-spectral filter (orange) drastically outperforms the non-linear spatial filter with an independent post-filter (purple) in terms of speech quality and intelligibility. This means that the dependencies between spatial and tempo-spectral information are successfully exploited by the neural network. And second, the DNN-based joint non-linear filter (FT-JNF) significantly outperforms the oracle MVDR with an added single-channel post-filter for a small number of microphones.

## C. Interdependency of spatial processing with spectral and temporal information

The experiment in the previous section demonstrated that spatial processing should not be separated from tempo-spectral processing, as these two seem to mutually enrich each other. In this section, we will further investigate the interdependencies between spatial processing and temporal and spectral processing.

In the top three rows of Table II, we report the results obtained with a non-linear spatial filter that has access to global spectral, temporal or tempo-spectral information using three microphones. The corresponding neural network architectures have been explained in Section III-C. As expected, we observe that the highest performance is obtained with a non-linear spatial filter that incorporates both, global temporal and spectral information, denoted by FT-NSF. However, the comparison of F-NSF and T-NSF reveals that spatial processing here benefits much more from global spectral than global temporal information. The difference even amounts to 0.32 POLQA score and is also reflected in the ESTOI measurements. A similar pattern is also observed for the joint non-linear filter that can not only exploit global statistics but also fine-grained information including correlations between neighboring frequency bins and/or time steps. The performance differences between F-JNF and T-JNF amount to 0.41 POLQA score and 0.07 ESTOI score.

The impact of different sources of information on the spatial selectivity of the filter is visualized in Figure 6 in more detail. For this, we present the trained networks with a clean speech signal originating from varying directions with 1 m distance from the microphone array. For this experiment, we use a simulated anechoic room as we want to measure the filter’s response to a signal from a specific direction. The plots in Figure 6 show the POLQA score for the filtered signals averaged over 15 examples. A high POLQA score, which is attained by all filters near 0<sup>◦</sup>, corresponds to a signal that has passed through the filter unaltered, while a low POLQA score indicates high suppression of the signal. The POLQA algorithm does not provide a result if the signal is not speech-like anymore and has very low energy. For these processed signals, which retain less then 0.1% of their original energy, we indicate high suppression with a dashed line at the minimum POLQA score.

![](figures/d49185217512a486393a915857d07e02e5f2606c408db2cfb79d997e34cea6e5.jpg)  
Fig. 6: Visualization of the spatial selectivity of the learned filters. The plots show the the mean POLQA score and 95% confidence interval for a clean and anechoic signal arriving from a given incidence angle. A low POLQA score here corresponds high suppression of the signal, while a very high POLQA score (around 0<sup>◦</sup>) means that the signal has passed through the filter unaltered. Signals for which no POLQA score can be computed are marked with a dashed line.

Comparing the two bottom plots of Figure 6, it is clearly visible that exploiting frequency information as opposed to time information increases the spatial selectivity, which can serve as an explanation of the performance differences observed before. While all plots show a “distortionless” response for signals with an incidence angle between −4<sup>◦</sup> and 4<sup>◦</sup>, signals arriving from a larger angles are much less suppressed (resulting in a higher POLQA score) for the network using temporal information. In particular, even signals that arrive from the interference region are not fully suppressed. Furthermore, considering the upper two plots, it is interesting to observe that adding fine-grained spectral information in FT-JNF and F-JNF narrows down the spatial selectivity even beyond the −20<sup>◦</sup> and 20<sup>◦</sup> angle that can be expected from the dataset configuration. Yet, a narrower selectivity pattern might be helpful to resolve the spatial characteristics in a noisy scenario.

## V. COMPARISON TO STATE-OF-THE-ART METHODS

In Table II, the overall best performance is obtained with the joint non-linear filter FT-JNF that exploits tempo-spectral in addition to spatial information. Comparing to T-JNF which has originally been proposed by Li and Horaud [15], we find that our systematic evaluation of the interplay between spatial and temporal as well as spectral information leads to a drastic performance improvement of 0.69 POLQA score in a speaker extraction scenario.

## A. Baselines

In this section, we compare the proposed FT-JNF with four additional baseline network architectures besides T-JNF. This ensures that the study we conducted with a rather simple network provides meaningful results also in comparison with recent and more elaborate state-of-the-art network architectures and it furthermore allows us to assess the question whether a network design inspired by a traditional filter-and-sum beamformer, e.g., [19], [20], [35], is likely to exhibit enhanced spatial filtering capabilities.

As our primary focus in this work is to better understand the consequences of architectural choices for implementing multichannel DNN-based filters, we train all baseline architectures following the same procedure outlined in Section III-E and using the loss function defined in (10). For most baselines, we use the code provided by the authors with the default parameter settings and focus our parameter search mostly on the learning rate. The selected values are given in Table III. It is likely that an extensive hyper-parameter tuning might lead to better results, but we nevertheless consider the results representative of their respective network architecture on the used dataset. Deviations from the training procedure or the settings described in the respective paper will be noted in the following. These are the baselines that we compare the proposed FT-JNF to:

• T-JNF: We consider the architecture T-JNF as an instance of the network proposed by Li and Horaud [15]. However, in order to facilitate phase processing, we have changed the network output from IRM to cIRM and also replaced the final output layer with a tanh layer accordingly.

• CRNN: We reimplement a variant of the convolutional recurrent neural network (CRNN) for mask estimation proposed by Chakrabarty and Habets [16]. The authors propose a convolutional neural network (CNN) for spatial feature extraction. For this small convolution kernels are used on the channel dimension such that a series of convolutional layers reduces the channel dimension to one. These spatial features are then processed with a bi-directional LSTM and fed into a FF layer to produce a mask. We use real and imaginary parts as input and estimate a cIRM.

• FaSNet+TAC: FasNet [50] is a time-domain approach mimicking a traditional filter-and-sum beamformer. The authors proposed an extension, denoted FaSNet+TAC [35], which enables variable microphone array configurations. As the authors report improved performance also for fixed array geometries, we choose to evaluate FaSNet+TAC on the speaker extraction dataset. We use the implementation provided by the authors.

• EaBNet: Li et al. [19] propose the Embedding and Beamforming Network (EaBNet). It uses a U-Net structure to estimate an embedding that incorporates spatial and tempo-spectral information and then employs a “beamformer” network to obtain weights that are applied in a filter-and-sum beamforming manner. We use the implementation provided by the authors using the LSTM branch. We do not apply a single-channel DNN (post-filter network) to the output of EaBNet and use uncompressed network inputs and targets. This baseline uses shorter STFT windows of length 20 ms and 50% overlap.

![](figures/1e143b7fa5fc33fb5c31e53f8e34f8e6453736ce2e6ae37aaf3412b7785bb0ec.jpg)  
Fig. 7: Performance comparison of the proposed architecture FT-JNF and five baselines. The two upper plots show the mean ESTOI and POLQA performance on the speaker extraction dataset and the 95% confidence interval. The bottom plot shows the CQS results obtained by a MUSHRA listening experiment on twelve randomly selected examples.

• COSPA: The Complex-valued Spatial Autoencoder (COSPA) has been proposed by Halimeh and Kellermann [20]. Similar to EaBNet it adopts a filter-and-sum approach with frequency-domain complex-valued coefficients estimated by the network. The network architecture is composed of an encoder, a compandor and a decoder part. All of these are complex-valued networks. We use the implementation provided by the authors, which uses 64 ms long STFT windows and an overlap of 50%. We train using the clean speech terms in the loss function only.

## B. Performance analysis

We train and evaluate all networks on the speaker extraction dataset. The results with respect to the POLQA improvements and ESTOI scores are displayed in the two upper plots of Figure 7. Here, we observe that the proposed FT-JNF consistently outperforms all other baselines by at least 0.22 POLQA score and 0.04 ESTOI score. In addition to using objective performance measures, we also conducted a MUSHRA [51] listening experiment with eleven participants using the webMUSHRA framework [52]. The participants have rated the overall quality of the algorithms based on twelve randomly sampled examples. The results are reported on a continuous quality scale (CQS) and pre sented in the bottom plot. The test results align very well with the objective measures and we find that FT-JNF performs best with a score of 67.9 outperforming EaBNet in second place with a score of 53.1. This is despite the fact that our proposed FT-JNF has the least number of learnable parameters. The number of parameters for each network architecture are given in Table III. It is apparent that the number of parameters is not the decisive factor for good performance here. Since all networks were trained in the same way (data, loss, optimizer etc.), we attribute the performance differences to the architectural choices of how to integrate different sources of information in the processing.

TABLE III: Baseline configurations.

<table><tr><td></td><td>LR</td><td>STFT [ms]</td><td>#Param. [M]</td><td>Implementation / Github repository</td></tr><tr><td>FT-JNF</td><td>0.001</td><td>32</td><td>1.2</td><td>own (sp-uhh/deep-non-linear-filter)</td></tr><tr><td>T-JNF</td><td>0.001</td><td>32</td><td>1.2</td><td>own</td></tr><tr><td>CRNN</td><td>0.0001</td><td>32</td><td>17.4</td><td>own</td></tr><tr><td>FaSTAC</td><td>0.0001</td><td>-</td><td>4.1</td><td>ylou42/TAC</td></tr><tr><td>EaBNet</td><td>0.001</td><td>20</td><td>2.8</td><td>Andong-Li-speech/EaBNet</td></tr><tr><td>COSPA</td><td>0.0001</td><td>64</td><td>2.1</td><td>ModarHalimeh/COSPA</td></tr></table>

![](figures/a2deeea5aacc166dbd27aa97599db183e3005539ce41f414fc5edfd9fb63ce7c.jpg)

![](figures/6bc9a861b0b9261f1531168d6a75b9be767e98a281dec66747047ed76bb81851.jpg)  
Fig. 8: Visualization of the spatial selectivity of the learned filters. The patterns are created by presenting white noise signals to the networks and averaging the resulting STFT signal along the time dimension for each incidence angle and converting to decibel.

While the architectures described in Section III as well as the CRNN adopt a mask-based approach, the baselines FasNet+TAC, EaBNet and COSPA resort to the filter-and-sum technique from traditional beamforming, where the filter weights are learned by the respective network. As the speaker extraction dataset is very challenging with low SNR and many interfering speech sources that have a similar tempo-spectral structure as the target signal, we can interpret the results in Figure 7 to reflect to a large extend the spatial selectivity of the DNN-based filters. Contrary to the common belief that a network design guided by the traditional beamforming paradigm is beneficial to spatial filtering capabilities, the best performance is obtained by FT-JNF that employs a mask-based approach, while the beamformer-inspired EaBNet only performs second best with an audible performance difference.

In order to investigate further the spatial selectivity of the different approaches, we perform an experiment similar to the one presented in Figure 6. Here, we present the trained networks

![](figures/000c535fa97bbd02e05503653510692933760c6969ba8b2a08147de23d51896f.jpg)  
Fig. 9: Visualization of the spatial selectivity of the learned filters. The plots show the the mean POLQA score and 95% confidence interval for a clean and anechoic signal arriving from a given incidence angle.

FT-JNF and EaBNet with spectrally white noise signals originating from variable directions in an anechoic room. Clearly, these signals are out-of-distribution data for a network trained on speech mixtures. However, the spatial properties are still consistent with the ones the network has seen during training. Figure 8 displays the filters’ response to these spatial cues. The incidence angle of the white noise signals is plotted on the x-axis. For each direction the STFT of eight filtered signals are averaged along the time axis. These white-noise response patterns seem to resemble the traditional directivity patterns [24, Sec. 12.5.2]. However, it must be noted that these white-noise response patterns do not allow for the same interpretation as a traditional beampattern. The reason for this is the non-linearity of the DNN-based filters. While a traditional beamformer, due to its linear nature, can in principle process all directional components of a signal separately and compose the final result after processing, this is not possible for a non-linear approach.

Bearing this in mind, the plots in Figure 8 nevertheless provide interesting insights into the spatial processing performed by the two networks. The FT-JNF shows a very clear spatial selectivity oriented towards the known position of the target source at zero degree. The width of the beam here coincides quite well with the two additional ticks at −20<sup>◦</sup> and 20<sup>◦</sup>, which mark the noise-free spatial section. On the other hand, the beam produced by EaBNet is much wider and suppression in the non-target direction does not work as well in particularly for high frequencies. What is is also noticeable is that the pattern suggest that signals near zero degree are slightly low-pass filtered, while the signal originating from an exact zero degree angle is high-pass filtered to some extend.

This loss in overall signal quality is also visible in Figure 9 for EaBNet. Here, we repeat the previously described experiment, where we present clean speech signals from different directions as input to the network (Figure 6). Comparing the orange line representing EaBNet with the blue line for FT-JNF, we find that EaBNet reduces the quality of the clean speech signal even if it is presented from the target direction. Considering this and also the width of the beam in both figures, we conclude that the performance differences that we have found in Figure 7 are well explained by the spatial properties of the filters.

## VI. IMPLICATIONS OF TRAINING

## DNN-BASED MULTI-CHANNEL FILTERS ON CHIME3

Finally, we evaluate on the CHiME3 data [53], which has been recorded in four real-world noisy environments: a cafeteria, a bus, a pedestrian area and next to a busy street. This dataset is frequently used to train and evaluate DNN-based multi-channel algorithms. The recordings have been conducted with a six-channel microphone array attached to a tablet that is held by the recorded speaker.

## A. Dataset

The T-JNF network proposed by Li and Horaud [15] has originally been trained on the CHiME3 data. The authors propose in [15] to create a simulated dataset, which combines the pure noise recordings provided in the CHiME3 dataset with clean booth recordings instead of artificially spatialized target signals. We use their data generation script to obtain 2400, 476, and 3251 utterances for training, validation and test respectively. The signals in the test set are mixed with a SNR in {−4,0,4,8} dB and we use the last four channels for our experiments.

## B. Performance analysis

First, we assess the interaction between spatial and spectral as well as temporal information also on the CHiME3 dataset. Therefore, in Table IV, we report the POLQA improvement scores for FT-JNF, F-JNF and T-JNF. As before and as expected, we find that the best performance is obtained by FT-JNF in the top row that can exploit all available sources of information, that is spatial, spectral and temporal information. However, a comparison with the bottom part of Table II showing results for the speaker extraction dataset reveals that the performance benefit of including spectral versus temporal information is reversed here. While a spatial-spectral filter performs better on the speaker extraction dataset, a spatial-temporal filter prevails on the CHiME3 dataset even though with a smaller performance gap. This behavior can be explained by considering the differences in the signal characteristics of the two datasets. While the speaker extraction dataset requires high spatial selectivity for good performance, which means that multi-channel processing is required, a single-channel filter performing tempo-spectral enhancement is expected to obtain solid results on the CHiME3 dataset. This is because the noise signals in the CHiME3 dataset have a tempospectral structure that is quite different from that of the target speech signal and are, in most cases, much more stationary.

Consistent with the results of Section IV-C, in Figure 10 we show that a spatio-temporal filter (T-JNF) has a substantially lower spatial selectivity than a spatio-spectral filter: The plots have been obtained by providing the network trained on the CHiME3 data with a clean speech input from a variable direction. For this, we simulate the CHiME3 microphone array in a room with a clean speech source in a variable position with 40 cm distance to the microphone array. Signal suppression (blue) or signal pass-through (yellow) are measured by POLQA scores. The centered yellow blob for F-JNF (right plot) corresponds to the position of target speech sources in the dataset. A speech source positioned at the origin represents a speaker that holds the recording tablet frontally at face level. Most speakers in the dataset however tilt the tablet to look at it a bit from above corresponding to a negative latitude value. The yellow blob at the left and right bottom edge shows that the filter cannot differentiate between signals impinging on the microphones attached to the tablet from front-side or back-side, which is expected for a planar microphone array. As the T-JNF has only little spatial selectivity but nevertheless obtains better performance than F-JNF, we conclude that temporal information, which is not reflected in this plot, plays an important role. However, based on the first spatial selectivity plot for FT-JNF, we find that this information can be incorporated without sacrificing a lot of the spatial selectivity, which gives a great performance boost of 0.23 POLQA score.

![](figures/6b4c0234a3233a18ac0e86ae8b61afe3c8b119df21371a3e47c879ee291ce369.jpg)  
Fig. 10: Spatial selectivity maps for filters trained on the CHiME3 data. The scatter plots show the POLQA scores for a clean and anechoic signal arriving from a given incidence angle. Examples for which POLQA could not be computed because there is so little energy retained in the signal were assigned the minimum POLQA score. The data points, which lie on a sphere of radius 40 cm, are projected into the plane using the Hammer projection.

TABLE IV: POLQA improvement scores (mean and 95% confidence interval) for the proposed network architectures and baselines evaluated on the CHiME3 data.

<table><tr><td></td><td>BUS</td><td>CAF</td><td>PED</td><td>STR</td></tr><tr><td>F-JNF</td><td>1.16±0.05</td><td>1.17±0.05</td><td>1.08±0.04</td><td>1.35±0.03</td></tr><tr><td>T-JNF</td><td>1.30±0.03</td><td>1.23±0.03</td><td>1.11±0.03</td><td>1.45±0.03</td></tr><tr><td>FT-JNF</td><td>1.53±0.04</td><td>1.56±0.04</td><td>1.45±0.04</td><td>1.76±0.03</td></tr><tr><td>CRNN</td><td>0.89±0.04</td><td>0.90±0.04</td><td>0.83±0.04</td><td>1.02±0.03</td></tr><tr><td>FaSNet+TAC</td><td>0.61±0.03</td><td>0.53±0.03</td><td>0.51±0.02</td><td>0.61±0.02</td></tr><tr><td>EaBNet</td><td>1.19±0.04</td><td>1.18±0.04</td><td>1.08±0.04</td><td>1.31±0.03</td></tr><tr><td>COSPA</td><td>0.60±0.03</td><td>0.61±0.03</td><td>0.56±0.03</td><td>0.65±0.03</td></tr></table>

In addition, we draw two more general conclusions from the above analysis: First, the plots show clearly that the CHiME3 dataset resembles a scenario with a fixed (only slightly variable) target speaker position relative to the microphone array orientation. This is easily forgotten as the target speaker positions in the CHiME3 dataset are unknown. And second, we have seen that performance improvements observed for a joint multi-channel filter evaluated on the CHiME3 dataset can not directly be attributed to an improved spatial filtering, but that a much more detailed analysis is necessary to understand the internal functioning of such a filter.

Finally, we compare our proposed algorithm with the four additional baselines described in Section V-A. The results are presented in the bottom part of Table IV. The results are consistent with the performances reported on the speaker extraction dataset. Only T-JNF [15] improves in comparison with the other baselines and now slightly outperforms EaBNet [19]. Overall, we find that our proposed architecture FT-JNF, which has been designed to use all three sources of information, outperforms all other baselines regardless of the noise type.

## VII. CONCLUSION

In this work, we have presented a detailed analysis of the internal mechanisms of a DNN-based filter for multi-channel speech enhancement. While traditional approaches combine a linear spatial filter with a separate tempo-spectral post-filter, DNN-based filters can potentially overcome the linear processing model and exploit interdependencies between spatial and tempo-spectral information. Here, we have shown that a non-linear spatial filter indeed outperforms an oracle MVDR on a challenging speaker extraction task with a low number of microphones. Furthermore, our analyses reveal that the interdependencies between spatial and spectral information can successfully be exploited by a DNN-based filter showing that additional spectral information increases the spatial selectivity of the filter. Our systematic review of this interplay of spatial and and tempo-spectral information leads to a simple network architecture with only two LSTM layers and a single feed-forward layer, that outperforms state-of-the-art network architectures for multi-channel speech enhancement by at least 0.22 POLQA score on the speaker extraction task and 0.32 POLQA score on the CHiME3 noise data.

## ACKNOWLEDGMENT

We would like to thank J. Berger and Rohde&Schwarz SwissQual AG for their support with POLQA.

## REFERENCES

[1] Y. Ephraim and D. Malah, “Speech enhancement using a minimum-mean square error short-time spectral amplitude estimator,” IEEE Trans. Audio, Speech, Language Proc., vol. 32, no. 6, pp. 1109–1121, 1984.

[2] T. Lotter and P. Vary, “Speech Enhancement by MAP Spectral Amplitude Estimation Using a Super-Gaussian Speech Model,” EURASIP J. Adv. Signal Proc., vol. 2005, no. 7, pp. 1110–1126, 2005.

[3] J. S. Erkelens, R. C. Hendriks, R. Heusdens, and J. Jensen, “Minimum mean-square error estimation of discrete Fourier coefficients with generalized Gamma priors,” IEEE Trans. Audio, Speech, Language Proc., vol. 15, pp. 1741–1752, 2007.

[4] M. Krawczyk-Becker and T. Gerkmann, “On MMSE-based estimation of amplitude and complex speech spectral coefficients under phaseuncertainty,” IEEE/ACM Trans. Audio, Speech, Language Proc., vol. 24, no. 12, pp. 2251–2262, 2016.

[5] K. Tan and D. Wang, “A convolutional recurrent neural network for real-time speech enhancement.” in ISCA Interspeech, Hyderabad, India, 2018, pp. 3229–3233.

[6] R. Giri, U. Isik, and A. Krishnaswamy, “Attention Wave-U-Net for speech enhancement,” in IEEE Workshop Applications Signal Proc. Audio, Acoustics (WASPAA), 2019, pp. 249–253.

[7] Y. Koizumi, S. Karita, S. Wisdom, H. Erdogan, J. R. Hershey, L. Jones, and M. Bacchiani, “DF-conformer: Integrated architecture of Conv-Tasnet and Conformer using linear complexity self-attention for speech enhancement,” in IEEE Workshop Applications Signal Proc. Audio, Acoustics (WASPAA), 2021, pp. 161–165.

[8] X. Hao, X. Su, R. Horaud, and X. Li, “Fullsubnet: A full-band and sub-band fusion model for real-time single-channel speech enhancement,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Toronto, Canada, 2021, pp. 6633–6637.

[9] K. Tesch, R. Rehr, and T. Gerkmann, “On nonlinear spatial filtering in multichannel speech enhancement,” in ISCA Interspeech, Graz, Austria, 2019, pp. 91–95.

[10] K. Tesch and T. Gerkmann, “Nonlinear spatial filtering in multichannel speech enhancement,” IEEE/ACM Trans. Audio, Speech, Language Proc., vol. 29, pp. 1795–1805, 2021.

[11] J. Heymann, L. Drude, A. Chinaev, and R. Haeb-Umbach, “BLSTM supported GEV beamformer front-end for the 3rd CHiME challenge,” in IEEE Workshop Autom. Speech Recog. and Underst. (ASRU), Scottsdale, USA, 2015, pp. 444–451.

[12] M. Togami, “Multi-channel Itakura Saito distance minimization with deep neural network,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Brighton, UK, 2019, pp. 536–540.

[13] Y. Liu, A. Ganguly, K. Kamath, and T. Kristjansson, “Neural network based time-frequency masking and steering vector estimation for two-channel MVDR beamforming,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Calgary, Canada, 2018, pp. 6717–6721.

[14] X. Xiao, S. Watanabe, H. Erdogan, L. Lu, J. Hershey, M. L. Seltzer, G. Chen, Y. Zhang, M. Mandel, and D. Yu, “Deep beamforming networks for multi-channel speech recognition,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Shanghai, China, 2016, pp. 5745–5749.

[15] X. Li and R. Horaud, “Multichannel speech enhancement based on time-frequency masking using subband long short-term memory,” in IEEE Workshop Applications Signal Proc. Audio, Acoustics (WASPAA), 2019, pp. 298–302.

[16] S. Chakrabarty and E. A. P. Habets, “Time–frequency masking based online multi-channel speech enhancement with convolutional recurrent neural networks,” IEEE Journal of Selected Topics in Signal Processing, vol. 13, no. 4, pp. 787–799, 2019.

[17] B. Tolooshams, R. Giri, A. H. Song, U. Isik, and A. Krishnaswamy, “Channel-attention dense U-net for multichannel speech enhancement,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Barcelona, Spain, 2020, pp. 836–840.

[18] Z.-Q. Wang, P. Wang, and D. Wang, “Complex spectral mapping for single- and multi-channel speech enhancement and robust ASR,” IEEE/ACM Trans. Audio, Speech, Language Proc., vol. 28, pp. 1778–1787, 2020.

[19] A. Li, W. Liu, C. Zheng, and X. Li, “Embedding and beamforming: All-neural causal beamformer for multichannel speech enhancement,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Singapore, 2022, pp. 6487–6491.

[20] M. M. Halimeh and W. Kellermann, “Complex-valued spatial autoencoders for multichannel speech enhancement,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Singapore, 2022, pp. 261–265.

[21] K. Tesch, N.-H. Mohrmann, and T. Gerkmann, “On the role of spatial, spectral, and temporal processing for DNN-based non-linear multi-channel speech enhancement,” in ISCA Interspeech, 2022. [Online]. Available: https://arxiv.org/abs/2206.11181

[22] K. Tan, Z.-Q. Wang, and D. Wang, “Neural spectrospatial filtering,” IEEE/ACM Trans. Audio, Speech, Language Proc., vol. 30, pp. 605–621, 2022.

[23] S. Doclo, W. Kellermann, S. Makino, and S. E. Nordholm, “Multichannel signal enhancement algorithms for assisted listening devices: Exploiting

spatial diversity using multiple microphones,” IEEE Signal Proc. Magazine, vol. 32, no. 2, pp. 18–30, 2015.

[24] P. Vary and R. Martin, Digital speech transmission: enhancement, coding and error concealment. Chichester, England Hoboken, NJ: John Wiley, 2006.

[25] R. Balan and J. P. Rosca, “Microphone Array Speech Enhancement by Bayesian Estimation of Spectral Amplitude and Phase,” in Sensor Array and Multichannel Signal Processing Workshop Proceedings, Rosslyn, Virginia, 2002, pp. 209–213.

[26] K. U. Simmer, J. Bitzer, and C. Marro, “Post-filtering techniques,” in Microphone Arrays: Signal Processing Techniques and Applications, M. Brandstein and D. Ward, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg, 2001, pp. 39–60.

[27] R. C. Hendriks, R. Heusdens, U. Kjems, and J. Jensen, “On optimal multichannel mean-squared error estimators for speech enhancement,” IEEE Signal Proc. Letters, vol. 16, pp. 885–888, Oct. 2009.

[28] S. Araki, T. Hayashi, M. Delcroix, M. Fujimoto, K. Takeda, and T. Nakatani, “Exploring multi-channel features for denoising-autoencoderbased speech enhancement,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Brisbane, Australia, 2015, pp. 116–120.

[29] Z.-Q. Wang, J. Le Roux, and J. R. Hershey, “Multi-channel deep clustering: Discriminative spectral and spatial embeddings for speakerindependent speech separation,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Brisbane, Australia, 2018, pp. 1–5.

[30] R. Gu, L. Chen, S.-X. Zhang, J. Zheng, Y. Xu, M. Yu, D. Su, Y. Zou, and D. Yu, “Neural spatial filter: Target speaker speech separation assisted with directional information,” in ISCA Interspeech, 2019, pp. 4290–4294.

[31] Z.-Q. Wang and D. Wang, “Combining spectral and spatial features for deep learning based blind speaker separation,” IEEE/ACM Trans. Audio, Speech, Language Proc., vol. 27, no. 2, pp. 457–468, 2019.

[32] Z. Zhang, Y. Xu, M. Yu, S.-X. Zhang, L. Chen, and D. Yu, “ADL-MVDR: All deep learning mvdr beamformer for target speech separation,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Toronto, Canada, 2021, pp. 6089–6093.

[33] Y. Xu, Z. Zhang, M. Yu, S.-X. Zhang, and D. Yu, “Generalized Spatio-Temporal RNN Beamformer for Target Speech Separation,” in ISCA Interspeech, Brno, Czech Republic, 2021, pp. 3076–3080.

[34] C.-L. Liu, S.-W. Fu, Y.-J. Li, J.-W. Huang, H.-M. Wang, and Y. Tsao, “Multichannel speech enhancement by raw waveform-mapping using fully convolutional networks,” IEEE/ACM Trans. Audio, Speech, Language Proc., vol. 28, pp. 1888–1900, 2020.

[35] Y. Luo, Z. Chen, N. Mesgarani, and T. Yoshioka, “End-to-end microphone permutation and number invariant multi-channel speech separation,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Barcelona, Spain, 2020, pp. 6394–6398.

[36] N. Tawara, T. Kobayashi, and T. Ogawa, “Multi-channel speech enhancement using time-domain convolutional denoising autoencoder,” in ISCA Interspeech, Graz, Austria, 2019, pp. 86–90.

[37] A. Pandey, B. Xu, A. Kumar, J. Donley, P. Calamia, and D. Wang, “TPARN: Triple-path attentive recurrent network for time-domain multichannel speech enhancement,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Sigapore, May 2022.

[38] D. Lee, S. Kim, and J.-W. Choi, “Inter-channel Conv-Tasnet for multichannel speech enhancement,” arXiv preprint:2111.04312, 2021. [Online]. Available: https://arxiv.org/abs/2111.04312

[39] X. Li and R. Horaud, “Narrow-band Deep Filtering for Multichannel Speech Enhancement,” arXiv preprint arXiv:1911.10791, 2019. [Online]. Available: http://arxiv.org/abs/1911.10791

[40] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997.

[41] D. S. Williamson, Y. Wang, and D. Wang, “Complex ratio masking for monaural speech separation,” IEEE/ACM Trans. Audio, Speech, Language Proc., vol. 24, no. 3, pp. 483–492, 2016.

[42] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” in 3rd International Conference on Learning Representations, 2015.

[43] R. Scheibler, E. Bezzam, and I. Dokmanic, “Pyroomacoustics: A python´ package for audio room simulation and array processing algorithms,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), Calgary, Canada, 2018, pp. 351–355.

[44] J. B. Allen and D. A. Berkley, “Image method for efficiently simulating small-room acoustics,” The Journal of the Acoustical Society of America, vol. 65, no. 4, pp. 943–950, 1979.

[45] J. S. Garofolo, D. Graff, D. Paul, and D. Pallett, “CSR-I (WSJ0) Complete LDC93S6A,” Linguistic Data Consortium, Philadelphia, May 2007.

[46] “P.863: Perceptual objective listening quality prediction,” International Telecommunication Union, Mar. 2018, iTU-T recommendation. [Online]. Available: https://www.itu.int/rec/T-REC-P.863-201803-I/en

[47] “P.862.3: Application guide for objective quality measurement based on Recommendations P.862, P.862.1 and P.862.2,” International Telecommunication Union, Nov. 2007, iTU-T recommendation. [Online]. Available: https://www.itu.int/rec/T-REC-P.862.3-200711-I/en

[48] N. Ito, S. Araki, M. Delcroix, and T. Nakatani, “Probabilistic spatial dictionary based online adaptive beamforming for meeting recognition in noisy and reverberant environments,” in IEEE Int. Conf. Acoustics, Speech, Signal Proc. (ICASSP), New Orleans, USA, 2017, pp. 681–685.

[49] J. Jensen and C. H. Taal, “An algorithm for predicting the intelligibility of speech masked by modulated noise maskers,” IEEE/ACM Trans. Audio, Speech, Language Proc., vol. 24, no. 11, pp. 2009–2022, 2016.

[50] Y. Luo, C. Han, N. Mesgarani, E. Ceolini, and S.-C. Liu, “FaSNet: Low-latency adaptive beamforming for multi-microphone audio processing,” in IEEE Workshop Autom. Speech Recog. and Underst. (ASRU), Sentosa, Singapore, 2019, pp. 260–267.

[51] “BS.1534 : Method for the subjective assessment of intermediate quality level of audio systems,” International Telecommunication Union, Oct. 2015, iTU-T recommendation. [Online]. Available: https://www.itu.int/rec/R-REC-BS.1534

[52] M. Schoeffler, S. Bartoschek, F.-R. Stoter, M. Roess, S. Westphal,¨ B. Edler, and J. Herre, “webMUSHRA – A comprehensive framework for web-based listening tests,” Journal of Open Research Software, vol. 6, no. 1, 2018.

[53] J. Barker, R. Marxer, E. Vincent, and S. Watanabe, “The third ‘CHiME’ speech separation and recognition challenge: Dataset, task and baselines,” in IEEE Workshop Autom. Speech Recog. and Underst. (ASRU), Scottsdale, USA, 2015, pp. 504–511.

![](figures/efefd1f9b6bdfbad9e08fbb54b89e5007bb30e60fe59352f76cee46ce66549f5.jpg)  
Kristina Tesch (S’20) received a B.Sc and M.Sc in Informatics in 2016 and 2019 from the Universitat¨ Hamburg, Hamburg, Germany. She is with the Signal Processing Group at the Universitat Hamburg¨ since 2019 and is currently working towards a doctoral degree. Her research interests include digital signal processing and machine learning algorithms for speech and audio with a focus on multichannel speech enhancement. For her master thesis on multichannel speech enhancement, she received the award for the best master thesis at a German

Informatics Department from the Fakultatentag Informatik in 2019, and her¨ prior work on nonlinear spatial filtering [10] received the VDE ITG 2022 award.

![](figures/5c7869d861de1cecacc47a9af6ea0f6f17ca330b9a22897027f48ed5f8f822b8.jpg)

Timo Gerkmann (S’08–M’10–SM’15) studied Electrical Engineering and Information Sciences at the Universitat Bremen and the Ruhr-Universit¨ at Bochum¨ in Germany. He received his Dipl.-Ing. degree in 2004 and his Dr.-Ing. degree in 2010 both in Electrical Engineering and Information Sciences from the Ruhr Universitat Bochum, Bochum, Germany. In 2005, he¨ spent six months with Siemens Corporate Research in Princeton, NJ, USA. During 2010 to 2011 Dr. Gerkmann was a postdoctoral researcher at the Sound and Image Processing Lab at the Royal Institute of

Technology (KTH), Stockholm, Sweden. From 2011 to 2015 he was a professor for Speech Signal Processing at the Universitat Oldenburg, Oldenburg, Germany.¨ During 2015 to 2016 he was a Principal Scientist for Audio & Acoustics at Technicolor Research & Innovation in Hanover, Germany. Since 2016 he is a professor for Signal Processing at the Universitat Hamburg, Germany. His main¨ research interests are on statistical signal processing and machine learning for speech and audio applied to communication devices, hearing instruments audio-visual media, and human-machine interfaces. Timo Gerkmann serves as an elected member of the IEEE Signal Processing Society Technical Committee on Audio and Acoustic Signal Processing and as an Associate Editor of the IEEE/ACM Transactions on Audio, Speech and Language Processing. His prior work on nonlinear spatial filtering [10] received the VDE ITG 2022 award.