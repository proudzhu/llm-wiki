# EchoFree: Towards Ultra Lightweight and Efficient Neural Acoustic Echo Cancellation

Xingchen Li<sup>†</sup>, Boyi Kang<sup>†</sup>, Ziqian Wang, Zihan Zhang, Mingshuai Liu, Zhonghua Fu<sup>∗</sup>, Lei Xie

Audio, Speech and Language Processing Group (ASLP@NPU), School of Computer Science

Northwestern Polytechnical University, Xi’an, China

{lixingchen, beaukang, zq wang, zhzhang, liumingshuai}@mail.nwpu.edu.cn, {mailfzh, lxie}@nwpu.edu.cn

Abstract—In recent years, neural networks (NNs) have been widely applied in acoustic echo cancellation (AEC). However, existing approaches struggle to meet real-world low-latency and computational requirements while maintaining performance. To address this challenge, we propose EchoFree, an ultra lightweight neural AEC framework that combines linear filtering with a neural post filter. Specifically, we design a neural postfilter operating on Bark-scale spectral features. Furthermore, we introduce a two-stage optimization strategy utilizing selfsupervised learning (SSL) models to improve model performance. We evaluate our method on the blind test set of the ICASSP 2023 AEC Challenge. The results demonstrate that our model, with only 278K parameters and 30 MMACs computational complexity, outperforms existing low-complexity AEC models and achieves performance comparable to that of state-of-the-art lightweight model DeepVQE-S. The audio examples are available <sup>1</sup>.

Index Terms—component, formatting, style, styling, insert

## I. INTRODUCTION

Acoustic echo cancellation (AEC) is a critical front-end task in far-field and hands-free speech communication systems. It aims to suppress echoes resulting from the feedback of far-end speech captured by local microphones, which can severely degrade user experience and downstream performance in automatic speech recognition (ASR) and speaker verification systems. Typically, AEC systems are categorized into traditional digital signal processing (DSP)-based approaches, modern neural network (NN)-based methods, and hybrid systems that combine both.

Traditional digital signal processing (DSP) based AEC approaches employ adaptive filtering algorithms to estimate the near-end speech [1] or echo path [2]–[4]. Such algorithms struggle to handle nonlinear echoes [5] and require residual echo cancellation algorithms, resulting in poor generalization ability in complex real-world scenarios.

Recent advancements in deep learning have significantly improved AEC performance, enabling the suppression of nonlinear echo components and achieving superior results compared to conventional linear filtering techniques [6]– [17]. Nevertheless, existing deep learning-based AEC models are often characterized by large parameter sizes and high computational complexity, posing significant challenges for deployment on resource-constrained devices.

![](figures/8573cf52d1668f2e976a690b336b433d020544162e23d61fa94fe79faf9e30bc.jpg)  
Fig. 1: The hybrid approach combines a linear acoustic echo canceller with a proposed neural post filter designed for residual echo suppression. Model details are provided in Fig. 2.

To address these challenges, we propose EchoFree, an ultra lightweight AEC model designed for real-world applications on resource-limited edge devices. EchoFree adopts a hybrid and efficient approach that combine linear filtering with a neural post filter shown in Fig. 1. The neural post filter leverages a compressed power spectrum representation in the Bark-scale, which has been proven to effectively reduce computational complexity while preserving critical speech information [14]. Furthermore, the embeddings produced by self-supervised learning (SSL) models have been proved to have rich acoustic and semantic information [18], which has been adopted to further improve the capabilities of speech enhancement models [19]. Inspired by this, we propose and apply a two-stage optimization strategy based on a SSL model. By utilizing the SSL model to guide the neural network in a progressive learning manner—from coarse-grained to fine-grained spectral representations—the proposed method enhances the model’s ability to perform effective echo suppression.

In this work, we perform comprehensive ablation studies to validate the effectiveness of the proposed two-stage optimization strategy, and systematically compare EchoFree with several representative state-of-the-art AEC models in terms of performance and efficiency. Experimental results demonstrate that EchoFree achieves performance comparable to the stateof-the-art DeepVQE-S, using only 278K parameters and 30 MMACs/s, establishing a superior trade-off between efficiency and performance.

## II. RELATED WORK

## A. DSP-based method

Traditional DSP based AEC approaches employ adaptive filtering algorithms to estimate the near-end speech [1] or echo path [2]–[4], such as the normalized least mean squares (NLMS), affine projection (APA), or recursive least squares (RLS) algorithms. However, these algorithms inherently assume a linear and stationary echo path, making them inadequate for handling nonlinear distortions introduced by loudspeakers or hardware imperfections. These methods typically rely on handcrafted residual echo suppression modules to mitigate remaining echo components [5], but such modules struggle to distinguish residual echo from speech, often leading to speech distortion or echo leakage. The problem is inherently challenging due to the dynamic nature of acoustic environments, including time-varying echo paths caused by changes in room geometry, user movement, or device placement. As a result, DSP-based AEC systems exhibit poor generalization in real-world scenarios with dynamic acoustics and varying noise conditions.

## B. NN-based method

On the other hand, recent advancements in deep learning have significantly improved AEC performance, enabling the suppression of nonlinear echo components and achieving superior results compared to conventional linear filtering techniques [6]–[17]. A common strategy involves combining DSP methods with neural networks to form hybrid frameworks. For example, Ma et al. [6] proposed a system where an adaptive digital filter removes most of the linear echo, while a recurrent neural network (RNN) targets the residual nonlinear components. To enhance temporal modeling capabilities, Zhang et al. [8] introduced a complex-valued neural network architecture that employs frequency-time LSTM (F-T-LSTM) layers, effectively capturing dependencies across both time and frequency domains.

In addition to hybrid frameworks, end-to-end neural architectures have also demonstrated promising performance in acoustic echo cancellation. Zhang et al. [10] introduced a multi-task residual echo suppression framework that cascades a linear AEC front-end with a gated convolutional F-T-LSTM neural post-filter, trained jointly with a voice activity detection (VAD) module and optimized using an echo-aware loss function to enhance echo suppression while mitigating speech distortion. Ma et al. [12] proposed EchoFilter, an end-to-end neural AEC system that directly operates on time-domain waveforms using temporal convolution and LSTM modules, and incorporates a local attention mechanism to address time delays and reverberation, with multitask learning employed to enhance robustness under double-talk and nonlinear distortion. Indenbom et al. [13] proposed $\mathrm { D e e p V Q E } ,$ a unified real-time speech enhancement framework that integrates acoustic echo cancellation, noise suppression, and dereverberation using a residual convolutional neural network (CNN) combined with recurrent layers and a cross-attention mechanism to jointly model multiple interference sources in the time-frequency domain.

However, existing AEC systems often face a significant trade-off between performance and computational complexity, prompting extensive research into lightweight solutions. For example, Valin et al. [14] presented a hybrid architecture that integrates a traditional linear acoustic echo canceller with a lightweight neural post-filter based on PercepNet, designed to jointly suppress residual echo and background noise in real time using perceptually motivated features and lowcomplexity recurrent-convolutional layers. Shetru et al. [15] proposed a hybrid joint AEC and noise reduction framework that integrates the ultra-low complexity ULCNet model into a traditional linear AEC pipeline, enabling residual echo and noise suppression with minimal computational cost while maintaining competitive performance in low-resource environments. Chen et al. [17] Chen et al. employed a Bark-scale auditory filterbank to enhance the fidelity of the near-end speech, thereby enabling neural post-filtering with extremely low computational complexity.

## III. PROPOSED METHOD

## A. Problem Formulation

We consider a full-duplex communication scenario, where the far-end signal x is played through a loudspeaker, undergoes transformations such as room reflections, and is then recaptured by the near-end microphone. The recorded signal consists of two components: near-end signal and far-end echo. Thus, the signal model can be expressed as:

$$
y (n) = s (n) + e (n)\tag{1}
$$

where n represents the time index of the sample points, $s ( n )$ represents the near-end received signal (composed of a mixture of speech and background noise), and $e ( n )$ denotes the echo signal captured by the microphone after transformation.

In this work, we focus solely on eliminating the echo signal from the far-end while ignoring background noise. The objective is to estimate the near-end signal $s ( n )$ given the mixed microphone signal $y ( n )$ and the far-end reference signal $x ( n )$ . As illustrated in Fig. 1, our approach employs a cascaded framework consisting of linear filtering followed by neural post filter. Initially, the linear filter estimates the echo signal $\boldsymbol { \hat { e } } ( \boldsymbol { n } )$ by modeling the transformation of the far-end signal $x ( n )$ , thereby producing the error signal $z ( n )$ as follows:

$$
\begin{array}{r l} z (n) & = y (n) - \hat {e} (n) \\ & = s (n) + \{e (n) - \hat {e} (n) \} \\ & = s (n) + r (n) \end{array}\tag{2}
$$

where $r ( n )$ represents the residual echo, i.e., the discrepancy between the actual echo signal $e ( n )$ and the estimated echo signal $\boldsymbol { \hat { e } } ( \boldsymbol { n } )$

The neural post filter module is designed to further refine the echo suppression by estimating the residual echo $r ( n )$ based on the mixed microphone signal $y ( n )$ and the estimated echo $\boldsymbol { \hat { e } } ( \boldsymbol { n } )$ obtained from the linear filtering stage.

![](figures/b6324b6c8293570da7e81f812f8384d1f1659efbaa127521b28ba7c463742fbd.jpg)

(a) Overall architecture of neural post filter.  
![](figures/8b8930707d3046e87f06645f46c04886757eef4957f8073387c11145d4b84612.jpg)  
Fig. 2: Neural network architecture of our proposed neurual post filter. (a) provides an overall architecture of the neural post filter of EchoFree, (b) shows the structure of bark-scale feature extractor, (c) shows the structure of decoder layer.

## B. Linear Filtering

We use the partitioned-block-frequency-domain-adaptive Kalman filter [20] as the linear filtering preprocessing module. This linear filtering algorithm takes the mixed microphone signal y(n) and the far-end reference signal x(n) as inputs, producing the estimated echo signal eˆ(n) and the residual signal z(n).

## C. Neural Post Filter

Fig. 2a shows our neural post filter architecture,which consists of a Bark-based feature extractor module, the main structure of the neural network, and a post-processing module. Feature Extraction Module: We first apply the short-time Fourier transform (STFT) to the mixed microphone signal y(n) and the estimated echo eˆ(n), obtaining their corresponding spectrogram matrices Y and E<sup>ˆ</sup> with dimensions [T, F]. Following the Bark-scale partitioning method from [6], we compute the logarithmic Bark-scale power spectrum of these spectrograms, compressing them into lower-dimensional feature maps. As shown in Fig. 2b, the squared magnitude spectrum of the input audio is computed initially. This spectrum is then multiplied by the mapping matrix B. Finally, the logarithm of the result from the linear transformation is computed, producing the logarithmic power spectrum on the Bark scale. Additionally, as in [6], we incorporate the firstand second-order derivatives of the Bark-scale feature maps to provide the model with sufficient prior knowledge while maintaining a compact architecture. The Bark-scale power spectrum features and their derivatives are concatenated along the feature dimension, forming the final input representation of shape [T, D].

Neural Network Architecture: Fig. 2a shows our neural network architecture, which improves upon previous work using fully connected layers and stacked GRU layers [6], [21]. We adopt a new U-Net [22] structure as the core of the neural network. This architecture has been proven to achieve better performance with a smaller computational cost. The neural network consists of an encoder/bottleneck layer and a decoder.

The encoder includes two branches. The branch for the mixed microphone signal consists of 4 depthwise separable convolution layers [22] with filter sizes of 8, 16, 24, 32. The branch for the echo signal consists of a single depthwise separable convolution layer with 8 filters. As shown in 2a, after the echo signal is encoded, its features are concatenated with the features from the mixed microphone signal branch and passed through the subsequent encoder layers.

To balance performance and computational efficiency, the bottleneck layer includes a unidirectional GRU instead of a more complex LSTM module followed by a linear layer. The decoder is composed of four decoder modules, as shown in Fig. 2c. Similar to [13], we employ a skip-block mechanism for skip connections. Additionally, we incorporate an optional Residual Block to enhance upsampling performance, which is applied only in the last decoder module. For upsampling, we use a SubPixelConv module, which provides lower computational complexity. Finally, BatchNorm [23] and the

Exponential Linear Unit (ELU) activation function [24] are applied to the output of each layer. The decoder module filter sizes, mirroring the encoder, are 24, 16, 8, 1.

To predict the frequency band gain in the Bark-scale, we apply a final linear layer followed by a sigmoid activation function, ensuring that the output gain values remain constrained between 0 and 1.

Post Process. In the post-processing stage, the gain obtained in the previous phase is multiplied by the transpose of the mapping matrix B, resulting in the magnitude spectrum mask. This mask is then multiplied by the magnitude spectrum of the mixed signal to obtain the estimated magnitude spectrum of the near-end speech, which is used to derive the estimated near-end speech.

## D. Loss Function

The embeddings produced by SSL model have been proved to have rich acoustic and semantic information [18], and various SSL-based training strategies are explored in speech enhancement models [19]. Inspired by this, We adopt a twostage training strategy, as illustrated in Fig. 3, to optimize the model more effectively. In the first stage, we use an enhanced loss function based on SSL model’s embeddings. We refer to this loss as the SSL loss throughout the rest of the paper. Specifically, we compute the MSE loss between the SSL embeddings of the ground truth and the estimated signals as shown in Fig. 2a. These embeddings are extracted using a pre-trained WavLM-Large model <sup>2</sup> [25], whose parameters are frozen during training, ensuring that our model aligns effectively with ground truth representations across multiple speech dimensions. The SSL loss is formulated as:

$$
\mathcal {L} _ {S S L} = \frac {1}{L} \sum_ {l = 1} ^ {L} \| \mathbf {e} _ {l} - \hat {\mathbf {e}} _ {l} \| ^ {2}\tag{3}
$$

where L denotes the total number of layers in the WavLM model, $\hat { e } _ { i , l }$ represents the estimated signal embedding for the i-th sample at the l-th layer, and $e _ { i , l }$ is the ground truth embedding for the same sample at the l-th layer.

In the second stage, to encourage fine-grained improvements that are aligned with human auditory perception, we introduce the Bark-scale gain loss $\mathcal { L } _ { B a r k }$ . This loss function penalizes both the squared and quartic root-mean discrepancies between the predicted gain ˆg and the target gain g. Specifically, we formulate the loss as follows:

$$
\begin{array}{c} \mathcal {L} _ {B a r k} = 1 0 (| \hat {\mathbf {g}} | ^ {c} - | \mathbf {g} | ^ {c}) ^ {4} + (| \hat {\mathbf {g}} | ^ {c} - | \mathbf {g} | ^ {c}) ^ {2} + \\ 0. 0 1 * \text { CrossEntropy } (\hat {\mathbf {g}}, \mathbf {g}) \end{array}\tag{4}
$$

Where c represents the compression coefficient, here $c = 0 . 5$ The fourth-order term emphasizes larger deviations in the Bark-scale gain, ensuring significant perceptual errors are strongly penalized. The second-order term provides general stability, while the cross-entropy term adds a regularization effect based on distributional consistency between predicted and target gain patterns.

The second-stage objective is formulated as a weighted combination of the SSL loss and the Bark-scale gain loss. In this stage, the model is optimized toward improving the Bark-scale gain performance, with the SSL loss serving as a regularization term to preserve the learned representation fidelity.

![](figures/8337a47c39c70c0f4ddbe1d0cdd5213c4f08c95b92ead6a664f46ca01cf211f3.jpg)  
Fig. 3: The proposed two-stage training strategy: the first stage uses only the SSL loss, while the second stage employs a combination of Bark-scale gain loss and SSL loss. During training, the parameters of WavLM are kept frozen.

We denote the loss functions used in the two training stages as follows:

$$
\begin{array}{l} \mathcal {L} _ {s t a g e - 1} = \mathcal {L} _ {S S L} \\ \mathcal {L} _ {s t a g e - 2} = 1 0 * \mathcal {L} _ {B a r k} + 0. 5 * \mathcal {L} _ {S S L} \end{array}\tag{5}
$$

(6)

## IV. EXPERIMENTS AND RESULTS

## A. Training Datasets

We use the clean speech data provided by the ICASSP 2021 DNS Challenge [26] to train the model. We selected nearly 90,000 high-quality clean speech samples with a total duration of 573 hours from this dataset. We used 80,000 samples for training, totaling 506 hours of speech, and the remaining 10,000 samples for the validation set, with a total duration of 67 hours. All speech samples have a sampling rate of 16 kHz.

To enhance acoustic diversity, we adopt a dynamic simulation pipeline. Each training instance is assigned parameters such as signal-to-echo ratio (SER), echo delay, room impulse response (RIR) characteristics, and nonlinear distortion profiles. The signal processing chain operates as follows: 1) Near-end speech: Convolved with randomly selected RIR from acoustic database; 2) Far-end reference: Subjected to nonlinear distortion simulation followed by RIR convolution and timedomain delay ranging from 10ms to 512ms; 3) Signal mixing: Combined under controlled SER ranging from -15 dB to 15 dB.

To account for different communication scenarios, including near-end single talk, far-end single talk, and double talk, we introduce additional randomness into the data generation process. Specifically, the near-end speech signal is set to zero with a 10% probability to simulate far-end single talk. Similarly, near-end single talk scenarios naturally occur within the duplex samples, eliminating the need for separate explicit inclusion. This dynamic and stochastic simulation strategy ensures that the training data effectively covers a broad range of real-world AEC conditions, thereby enhancing model robustness.

TABLE I: Trained on the same dataset, a comparison between EchoFree and state-of-the-art low-complexity AEC models is presented, along with the performance of EchoFree under different training strategies.

<table><tr><td>Method</td><td># Param.</td><td>Macs/s</td><td>ST FE EchoMOS</td><td>ST NE DegMOS</td><td>DT EchoMOS</td><td>DT DegMOS</td></tr><tr><td>ULCNet-AER [15]</td><td>1.12M</td><td>173M</td><td>2.89</td><td>3.04</td><td>2.68</td><td>3.77</td></tr><tr><td>Bark-AEC [21]</td><td>1.62M</td><td>107M</td><td>3.16</td><td>2.83</td><td>2.96</td><td>3.27</td></tr><tr><td>DeepVQE-S [13]</td><td>0.82M</td><td>315M</td><td>4.13</td><td>3.24</td><td>3.96</td><td>3.69</td></tr><tr><td>Linear AEC only</td><td>-</td><td>-</td><td>2.91</td><td>3.02</td><td>2.68</td><td>3.76</td></tr><tr><td>EchoFree-cost loss only</td><td>0.28M</td><td>30M</td><td>4.15</td><td>3.13</td><td>3.74</td><td>3.52</td></tr><tr><td>EchoFree-SSL loss only</td><td>0.28M</td><td>30M</td><td>4.15</td><td>3.18</td><td>3.91</td><td>3.46</td></tr><tr><td>EchoFree-proposed</td><td>0.28M</td><td>30M</td><td>4.20</td><td>3.27</td><td>3.88</td><td>3.53</td></tr></table>

## B. Experimental Setup

For the linear filtering algorithm, we employ the partitionedblock frequency-domain adaptive Kalman filter described in [20]. Throughout both training and inference, we consistently use 10 partitions and set the FFT length to 256 samples for models utilizing linear filtering as a preprocessing step.

In the feature extraction module, for 16 kHz audio signals, we apply the STFT transformation with a window length of 512 samples, a hop size of 256 samples, and an FFT length of 512 samples, yielding an STFT spectrum with 257 frequency bins. To compress the input feature dimension, we extract Bark-scale features using 100 Bark-scale filters. Additionally, following [6], we incorporate the first- and second-order derivatives of the first six features. Consequently, the total input feature dimension is 112.

In the neural network module, the microphone branch encoder consists of four encoder layers, each with a convolution kernel size of (4, 3) and a stride of (4, 3). The reference branch encoder includes a single convolutional layer with the same kernel size and stride. The bottleneck layer comprises a GRU with 192 units and a fully connected layer with 192 units. The decoder consists of four decoder modules, where both the skip block and sub-pixel block utilize 1 × 1 convolution kernels. The final decoder module also includes a residual convolution module.

For EchoFree training, we adopt the Adam optimizer [27] with an initial learning rate of 0.001, which is reduced by a factor of 0.5 if the validation loss does not improve for five consecutive epochs and the minimum value of the learning rate is set to 10<sup>−5</sup>. We use a batch size of 128 and train on 10-second speech segments. Training continues until the validation loss fails to improve for ten consecutive epochs. In the second stage, we resume training with a reduced learning rate while keeping the same optimizer, stopping when the validation loss again stagnates for ten epochs. For the SSL model, the pre-trained WavLM-large is employed to compute the SSL loss.

## C. Evaluation Dataset and Metrics

We evaluate our method using the blind test set from the ICASSP 2023 AEC Challenge [28], which comprises 800 test samples. These include 300 double-talk cases, 300 far-end single-talk cases, and 200 near-end single-talk cases. Since our model operates at a 16 kHz sampling rate, we resample the blind test set audio to 16 kHz before processing.

For performance evaluation, we adopt AECMOS [29], which includes two key metrics: EchoMOS, assessing echo cancellation performance, and DegMOS, measuring the preservation of near-end speech quality. We follow the open-source AECMOS implementation, using the model Run 1668423760 Stage 0.onnx for evaluation. As this model is designed for 48 kHz audio, we upsample our processed outputs to 48 kHz before computing AECMOS scores.

## D. Results and Analysis

To benchmark our approach, we compare it against three state-of-the-art low-complexity AEC models: 1) ULCNet-AER [15], a recently proposed lightweight AEC model optimized for low computational complexity. 2) Bark-scale feature-based AEC [21], which employs Bark-scale features as input for the NN post-filter, making it a suitable baseline for evaluating the advantages of our approach. In the following, we refer to this method as Bark-AEC. 3) DeepVQE-S [13], a state-ofthe-art end-to-end AEC model with significantly higher computational complexity, serving as an upper-bound comparison. Table I presents the results of the comparative experiments. It is evident that EchoFree not only outperforms ULCNet-AER and Ernst et al. proposed AEC model by a substantial margin with a lower computational load and fewer parameters, but also surpasses DeepVQE-S with significantly more parameters and MACs in terms of EchoMOS for the ST FE scenarios and DegMOS for the ST NE scenarios.

It is worth noting that to ensure a fair comparison, we retrain all reference models using our training dataset. Additionally, we maintain consistent STFT configurations across all methods, as specified in Section 3.1. For cascaded approaches integrating linear filtering with neural post filter, we utilize the same linear filtering algorithm detailed in Section 3.1 as the preprocessing step. We reproduce ULCNet-AER following the description in [15]. For the Bark-scale feature-based AEC model, we extract features using 100 Bark-scale filters while keeping all other hyperparameters consistent with its original implementation. For DeepVQE-S, we implement the model according to [13], including the alignment block and CCM block.

![](figures/3a9e432184c43860355f138fa38afe85d8c425b6b259e1c93d2b88b78cf03f24.jpg)  
(a) input

![](figures/42fad54bd962f2478e4822fa6bb6f832b69307301754379f959cdae1243305a7.jpg)  
(b) EchoFree stage1

![](figures/a9c66177ab8962559bba1e4a28c6eb26d7e25f8af227c3ad9cb0464b1c1d539c.jpg)  
(c) EchoFree stage2  
Fig. 4: Visualization of the output at each stage. The input audio (a) contains acoustic echo. The output of the first stage (b) initially suppresses the echo but introduces spectral distortions, which are further corrected in the second stage (c).

## E. Ablation Study

We conduct an ablation study to analyze the impact of different training strategies on the proposed model. Table I presents the results of our ablation experiments, comparing four configurations: 1) Only using linear AEC. 2) Training with the conventional gain loss function. 3) Training with SSL loss. 4) Two-stage training: first optimizing with SSL loss, followed by fine-tuning with a combination of SSL loss and the gain loss function.

The ablation test results are presented in Table 1. All configurations with NN module outperform the one with linear AEC only. and our findings reveal that models trained with SSL loss outperform those trained with the conventional gain loss function, particularly in EchoMOS for the DT scenarios, where a substantial improvement is observed. Furthermore, the two-stage training strategy yields superior results compared to direct SSL loss training. While a minor reduction in EchoMOS is observed under DT scenarios, all other evaluation metrics demonstrate notable improvements, validating the effectiveness of our proposed training strategy.

To evaluate the effectiveness of the proposed two-stage training strategy, we visualize the model outputs at each stage. As shown in Fig. 4, the model trained in the first stage is capable of initially suppressing the echo; however, noticeable distortions occasionally occur in the high-frequency regions. These issues are substantially mitigated after the second-stage training.

## V. CONCLUSION

In this paper, we propose EchoFree, an ultra lightweight AEC model that supports streaming inference. Our model employs a cascaded framework integrating linear filtering with neural post filter. The neural post filter utilizes Bark-scale features as input and is trained using a two-stage optimization strategy based on SSL loss. Experimental results demonstrate that EchoFree achieves superior performance while maintaining a lower parameter count and reduced computational complexity compared to state-of-the-art low-complexity AEC models. In future work, we will focus on further improving EchoFree’s performance and extending its capabilities to endto-end joint acoustic echo cancellation and noise suppression.

## REFERENCES

[1] D. L. Duttweiler, “Proportionate normalized least-mean-squares adaptation in echo cancelers,” IEEE Trans. Speech Audio Process., 2000.

[2] Z. Luo, Z. Yu, F. Kang, F. Yang, and J. Yang, “Performance analysis of unconstrained partitioned-block frequency-domain adaptive filters in under-modeling scenarios,” EURASIP J. Adv. Signal Process., 2024.

[3] J. Soo and K. K. Pang, “Multidelay block frequency domain adaptive filter,” IEEE Trans. Acoust. Speech Signal Process., 1990.

[4] C. Paleologu, J. Benesty, and S. Ciochina, “Study of the general kalman filter for echo cancellation,” IEEE Trans. Speech Audio Process., 2013.

[5] D. A. Bendersky, J. W. Stokes, and H. S. Malvar, “Nonlinear residual acoustic echo suppression for high levels of harmonic distortion,” in Proceedings of the IEEE International Conference on Acoustics, Speech, and Signal Processing, ICASSP 2008, March 30 - April 4, 2008, Caesars Palace, Las Vegas, Nevada, USA, 2008.

[6] L. Ma, H. Huang, P. Zhao, and T. Su, “Acoustic echo cancellation by combining adaptive digital filter and recurrent neural network,” CoRR, 2020.

[7] Y. Zhang, M. Yu, H. Zhang, D. Yu, and D. Wang, “Neuralkalman: A learnable kalman filter for acoustic echo cancellation,” in IEEE Automatic Speech Recognition and Understanding Workshop, ASRU 2023, Taipei, Taiwan, December 16-20, 2023, 2023.

[8] S. Zhang, Y. Kong, S. Lv, Y. Hu, and L. Xie, “F-T-LSTM based complex network for joint acoustic echo cancellation and speech enhancement,” in 22nd Annual Conference of the International Speech Communication Association, Interspeech 2021, Brno, Czechia, August 30 - September 3, 2021, H. Hermansky, H. Cernocky, L. Burget, L. Lamel, O. Scharenborg,´ and P. Motl´ıcek, Eds., 2021.

[9] G. Zhang, C. Wang, L. Yu, and J. Wei, “Multi-scale temporal frequency convolutional network with axial attention for multi-channel speech enhancement,” in IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2022, Virtual and Singapore, 23-27 May 2022, 2022.

[10] S. Zhang, Z. Wang, J. Sun, Y. Fu, B. Tian, Q. Fu, and L. Xie, “Multitask deep residual echo suppression with echo-aware loss,” in IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2022, Virtual and Singapore, 23-27 May 2022, 2022.

[11] J. Sun, D. Luo, Z. Li, J. Li, Y. Ju, and Y. Li, “Multi-task sub-band network for deep residual echo suppression,” in IEEE International Conference on Acoustics, Speech and Signal Processing ICASSP 2023, Rhodes Island, Greece, June 4-10, 2023. IEEE, 2023.

[12] L. Ma, S. Yang, Y. Gong, X. Wang, and Z. Wu, “Echofilter: Endto-end neural network for acoustic echo cancellation,” arXiv preprint arXiv:2105.14666, 2021.

[13] N. Ristea, E. Indenbom, A. Saabas, T. Parnamaa, J. Guzvin, and¨ R. Cutler, “Deepvqe: Real time deep voice quality enhancement for joint acoustic echo cancellation, noise suppression and dereverberation,” in 24th Annual Conference of the International Speech Communication Association, Interspeech 2023, Dublin, Ireland, August 20-24, 2023, N. Harte, J. Carson-Berndsen, and G. Jones, Eds., 2023.

[14] J. Valin, S. V. Tenneti, K. Helwani, U. Isik, and A. Krishnaswamy, “Lowcomplexity, real-time joint neural echo control and speech enhancement based on percepnet,” in IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2021, Toronto, ON, Canada, June 6-11, 2021, 2021.

[15] S. S. Shetu, N. K. Desiraju, J. M. M. Aponte, E. A. P. Habets, and E. Mabande, “A hybrid approach for low-complexity joint acoustic echo and noise reduction,” in 18th International Workshop on Acoustic Signal Enhancement, IWAENC 2024, Aalborg, Denmark, September 9- 12, 2024, 2024.

[16] S. S. Shetu, N. K. Desiraju, W. Mack, and E. A. P. Habets, “Align-ulcnet: Towards low-complexity and robust acoustic echo and noise reduction,” CoRR, 2024.

[17] H. Chen, J. Yu, Y. Luo, R. Gu, W. Li, Z. Lu, and C. Weng, “Ultra dualpath compression for joint echo cancellation and noise suppression,” in 24th Annual Conference of the International Speech Communication Association, Interspeech 2023, Dublin, Ireland, August 20-24, 2023, N. Harte, J. Carson-Berndsen, and G. Jones, Eds., 2023.

[18] X. Zhu, Y. Lv, Y. Lei, T. Li, W. He, H. Zhou, H. Lu, and L. Xie, “Vec-tok speech: speech vectorization and tokenization for neural speech generation,” CoRR, vol. abs/2310.07246, 2023.

[19] R. Shankar, K. Tan, B. Xu, and A. Kumar, “A closer look at wav2vec2 embeddings for on-device single-channel speech enhancement,” in IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2024, Seoul, Republic of Korea, April 14-19, 2024, 2024.

[20] F. Kuech, E. Mabande, and G. Enzner, “State-space architecture of the partitioned-block-based acoustic echo controller,” in IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2014, Florence, Italy, May 4-9, 2014, 2014.

[21] E. Seidel, P. Mowlaee, and T. Fingscheidt, “Efficient high-performance bark-scale neural network for residual echo and noise suppression,” in IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2024, Seoul, Republic of Korea, April 14-19, 2024, 2024.

[22] O. Ronneberger, P. Fischer, and T. Brox, “U-net: Convolutional networks for biomedical image segmentation,” in Medical Image Computing and Computer-Assisted Intervention - MICCAI 2015 - 18th International Conference Munich, Germany, October 5 - 9, 2015, Proceedings, Part III, N. Navab, J. Hornegger, W. M. W. III, and A. F. Frangi, Eds., 2015.

[23] S. Ioffe and C. Szegedy, “Batch normalization: Accelerating deep network training by reducing internal covariate shift,” in Proceedings of the 32nd International Conference on Machine Learning, ICML 2015, Lille, France, 6-11 July 2015, F. R. Bach and D. M. Blei, Eds., 2015.

[24] D. Clevert, T. Unterthiner, and S. Hochreiter, “Fast and accurate deep network learning by exponential linear units (elus),” in 4th International Conference on Learning Representations, ICLR 2016, San Juan, Puerto Rico, May 2-4, 2016, Conference Track Proceedings, Y. Bengio and Y. LeCun, Eds., 2016.

[25] S. Chen, C. Wang, Z. Chen, Y. Wu, S. Liu, Z. Chen, J. Li, N. Kanda, T. Yoshioka, X. Xiao, J. Wu, L. Zhou, S. Ren, Y. Qian, Y. Qian, J. Wu, M. Zeng, X. Yu, and F. Wei, “Wavlm: Large-scale self-supervised pretraining for full stack speech processing,” 2022.

[26] A. Li, W. Liu, X. Luo, C. Zheng, and X. Li, “ICASSP 2021 deep noise suppression challenge: Decoupling magnitude and phase optimization with a two-stage deep network,” in IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2021, Toronto, ON, Canada, June 6-11, 2021, 2021.

[27] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” in 3rd International Conference on Learning Representations, ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings, Y. Bengio and Y. LeCun, Eds., 2015.

[28] R. Cutler, A. Saabas, T. Parnamaa, M. Purin, E. Indenbom, N. Ristea,¨ J. Guzvin, H. Gamper, S. Braun, and R. Aichner, “ICASSP 2023 acoustic echo cancellation challenge,” CoRR, vol. abs/2309.12553, 2023.

[29] M. Purin, S. Sootla, M. Sponza, A. Saabas, and R. Cutler, “AECMOS: A speech quality assessment metric for echo impairment,” in IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2022, Virtual and Singapore, 23-27 May 2022, 2022.