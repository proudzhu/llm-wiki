# FAST-ULCNET: A FAST AND ULTRA LOW COMPLEXITY NETWORK FOR SINGLE-CHANNEL SPEECH ENHANCEMENT

Nicolas Arrieta Larraza, Niels de Koeijer´

Bang & Olufsen, Alle 1 7600 Struer, Denmark´

## ABSTRACT

Single-channel speech enhancement algorithms are often used in resource-constrained embedded devices, where low latency and low complexity designs gain more importance. In recent years, researchers have proposed a wide variety of novel solutions to this problem. In particular, a recent deep learning model named ULCNet is among the state-ofthe-art approaches in this domain. This paper proposes an adaptation of ULCNet, by replacing its GRU layers with FastGRNNs, to reduce both computational latency and complexity. Furthermore, this paper shows empirical evidence on the performance decay of FastGRNNs in long audio signals during inference due to internal state drifting, and proposes a novel approach based on a trainable complementary filter to mitigate it. The resulting model, Fast-ULCNet, performs on par with the state-of-the-art original ULCNet architecture on a speech enhancement task, while reducing its model size by more than half and decreasing its latency by 34% on average.

Index Terms— deep learning, speech enhancement, low complexity, low latency

## 1. INTRODUCTION

Single-channel speech enhancement is a key component of speech recognition, voice processing, and assistive hearing systems. Often, these technologies have real-time latency constraints and are deployed on resource-constrained embedded devices. Therefore, the use of very low complexity and low latency algorithms is needed to reduce the memory footprint and processing time, respectively. While traditional signal processing meets these requirements, deep learning has been shown to deliver superior audio quality [1]. In recent years, multiple approaches have been developed that propose novel architectures and methods to address these latency and memory constraints [2, 3, 4]. A state-of-the-art model in this regard is an architecture named ULCNet [5]. In this approach, a small model with a novel channel-wise feature reorientation block and power-law compression technique is proposed. As a result, ULCNet exhibits 3 to 4 times less computational cost and memory usage than prior state-ofthe-art approaches while achieving comparable or superior noise suppression performance [5]. Gated Recurrent Units (GRUs) [6] were chosen for the Recurrent Neural Network (RNN) layers. These have been a popular choice among other low-complexity architectures [2, 3] due to their relatively low number of trainable parameters and high performance [7].

This study proposes an extension of ULCNet, named Fast-ULCNet, which replaces the RNN units in ULCNet from GRUs to FastGRNNs. FastGRNN [8] is a popular Gated-RNN design, which achieves state-of-the-art accuracies while having 2 to 4 times fewer parameters and performing faster inferences than other RNNs. Although the authors of FastGRNN claim that the performance is invariant to the length of the input, our research shows empirical evidence that FastGRNN performance decays over time during inference of long audio signals. To solve this, we additionally propose Comfi-FastGRNN (complementary filter FastGRNN), an adaptation of FastGRNN to address performance decay over time of long sequences during the forward pass. This is achieved by incorporating a trainable complementary filter system that handles the RNN state drift, which we found to correlate with the drop in performance over time.

To the best of our knowledge, this is the first study that uses FastGRNN layers for speech enhancement and sheds light over the performance decay of FastGRNN over long input sequences. Additionally, the proposal of Comfi-FastGRNN represents the first implementation of a trainable complementary filter to deal with RNN state drift. Our results show that Fast-ULCNet achieves similar performance to the state-of-the-art architecture ULCNet, while reducing the number of parameters by more than a half and decreasing its computational latency by 34%, on average.

The implementations of Fast-ULCNet and Comfi-FastGRNN are publicly available as open source on GitHub <sup>1</sup>, along with an online demo <sup>2</sup>.

## 2. FAST-ULCNET

## 2.1. FastGRNN and Comfi-FastGRNN

FastGRNN was originally proposed as a lightweight and computationally efficient RNN architecture that delivers performance comparable to more sophisticated variants such as

![](figures/9ac760ded9d676728633223234cd59266619afdec4edd935a40377f6bdfe0c39.jpg)  
Fig. 1: Block diagram of Comfi-FastGRNN, comprising the original FastGRNN architecture extended with a trainable complementary filter.

GRUs [8]. Its efficiency is achieved through the introduction of a weighted residual connection, implemented as a gating mechanism that reuses the same weight matrices for both the hidden-state update and the gating operation. This design not only substantially reduces the parameter count but also promotes well-conditioned gradients, thereby stabilizing the training process and alleviating the exploding and vanishing gradient problems that commonly affect conventional RNNs.

Fig. 1 illustrates the FastGRNN architecture, and (1)–(3) express its state update equations, where σ is a non-linear activation function, W and U are weight matrices, and b is a bias vector. Through the addition of two scalar trainable parameters $0 \leq \zeta , \nu \leq 1 \in \mathbb { R }$ , it controls the influence of the current input and previous hidden state.

$$
z _ {t} = \sigma (W x _ {t} + U h _ {t - 1} + b _ {z}),\tag{1}
$$

$$
\tilde {h} _ {t} = \mathrm{tanh} (W x _ {t} + U h _ {t - 1} + b _ {h}),\tag{2}
$$

$$
h _ {t} = (\zeta (1 - z _ {t}) + \nu) \odot \tilde {h} _ {t} + z _ {t} \odot h _ {t - 1}\tag{3}
$$

FastGRNN achieves provably stable training, independent of the sequence length. However, this guarantees stability only during training and not in the forward pass at inference. To test the latter, the authors evaluated FastGRNN on datasets of different domains with varying sequence lengths, with the longest audio clip being 1.63 s [8].

We observed that, when applying FastGRNN to longer audio signals (more than 60 s) for speech enhancement, performance degraded over time. Such a behaviour correlates with a drift in the internal RNN state, as evidenced by the increasing average hidden state magnitude over time during inference, shown in Fig. 2. The drift can be traced to (3), where the internal state lacks a contraction guarantee and the coefficients do not satisfy a sum-to-one constraint, enabling state accumulation over extended inference horizons.

$$
h _ {t \mathrm{comfi}} = \gamma h _ {t} + (1 - \gamma) \lambda\tag{4}
$$

Motivated by complementary filters used in accelerometer–gyroscope systems to reduce orientation drift, we propose Comfi-FastGRNN, an extension of FastGRNN that uses a trainable complementary filtering method to mitigate state drift. Equation (4) extends the FastGRNN state update in (3) by incorporating two trainable parameters, $\lambda , \gamma \in \mathbb { R }$ . The parameter λ acts as a scalar modulation factor to compensate for state drift, while γ controls the relative contributions of the hidden state and the drift correction term. This solution preserves the original design intent of FastGRNN while mitigating drift through a parameter-efficient approach.

![](figures/5dd7a6b2a8c83ee47d77b226d2180ac9af088e25fbd3f34db64e6029ce44fc28.jpg)  
Fig. 2: Fast-ULCNet inference shows drifting on the mean RNN state $h _ { t }$ (top) and performance decay on the processed signal (bottom) over time with FastGRNN (left column), whereas Comfi-FastGRNN (right column) maintains stable mean RNN state $h _ { t c o m \mathrm { { f } } }$ and consistent performance.

## 2.2. Model architecture

The proposed deep neural network architecture, illustrated in Fig. 3, is based on the ULCNet design [5], with the GRU layers replaced by FastGRNN-based layers, implemented either as FastGRNN units or as the proposed Comfi-FastGRNN units.

In the first stage, the input features are preprocessed using a modified power-law compression applied to both real and imaginary short-time Fourier transform (STFT) components. Then, a channel-wise feature reorientation method is applied, which reduces the dimensionality of the input features for efficiency. The rest of the stage comprises a series of depthwise separable convolutional layers serving as feature extractors, followed by a bidirectional FastGRNN-based layer operating along the frequency axis to expand the receptive field. Additionally, subband-level temporal FastGRNN-based units are employed to enhance spectral modelling. A real-valued magnitude mask is subsequently predicted through a stack of two fully connected (FC) layers.

The second stage focuses on phase refinement. A convolutional neural network (CNN) is applied to intermediate representations derived from the estimated magnitude mask and the noisy phase. The final complex mask is obtained via complex ratio masking (CRM) [9], which is used to reconstruct the enhanced complex spectrogram.

![](figures/daf61a6c8e86573c3c4d2b42a04be9c2397276ce5778e20080fa97ea6a3c661c.jpg)  
Fig. 3: Architecture of Fast-ULCNet. Black boxes represent components from the original ULCNet architecture, while dotted light-blue boxes highlight the FastGRNN-based modifications introduced in this work, with or without the complementary filter. Subscripts of X (phase, mag, re, and im) indicate the phase, magnitude, real, and imaginary parts of the input features, respectively.

## 3. EXPERIMENTS

## 3.1. Implementation details

## 3.1.1. Architecture implementation

The ULCNet architecture was replicated in TensorFlow, adhering to the design specifications outlined by the original authors. For the channelwise feature reorientation, we apply an overlapping rectangular uniform window with a frequency resolution of 1.5 kHz and an overlap factor of 0.33. The Conv Block consists of four depthwise-separable convolutional layers with a kernel size of 1×3, performing convolution operations solely along the frequency axis. These layers use 32, 64, 96, and 128 filters, respectively. Except for the first convolutional layer, downsampling is applied via max-pooling with a factor of 2 in the remaining 3 layers. The Freq-FastGRNN layer contains 64 units and is followed by a pointwise convolution with 64 filters. Subsequently, 2 subband temporal Fast-GRNN blocks are employed, each comprising 2 FastGRNN layers with 128 units. These are followed by 2 FC layers, each with 257 neurons. The second stage CNN consists of two 2D convolutional layers with 32 filters and a kernel size of 1×3, followed by a pointwise convolutional layer with 2 output channels, which restores the desired output shape.

For the gating component σ in our FastGRNN and Comfi-FastGRNN implementations, we adopted the sigmoid nonlinearity, consistent with the original FastGRNN paper. The trainable scalar parameters of the complementary filter, γ and λ, were initialized to 0.999 and 0.0, respectively.

## 3.1.2. Loss function

We adopted a version of the Mean Absolute Error loss, which has been shown to perform favorably for speech enhancement in the time-frequency domain [10]. Specifically, our loss function comprises two components: the $L _ { 1 }$ norm of the difference between the magnitude spectra of the predicted and clean speech, and the $L _ { 1 }$ norm of the difference between their complex spectrogram values.

$$
\mathcal {L} = \frac {1}{T F} \sum_ {t = 1} ^ {T} \sum_ {f = 1} ^ {F} \left(\left| | S | - | \hat {S} | \right| + \left| S - \hat {S} \right|\right)\tag{5}
$$

Equation (5) defines the loss function, where S and $\hat { S }$ denote the clean and predicted spectrogram values, respectively, and T and F represent the total number of time frames and frequency bins. For brevity, the explicit dependence of $S ( t , f )$ and $\hat { S } ( t , f )$ on time and frequency indices has been omitted.

## 3.1.3. Dataset

For the experiments, we utilized the widely adopted Interspeech 2020 Deep Noise Suppression (DNS) Challenge dataset [11]. A total of 1000 hours of 10-second noisy speech mixtures were synthesized at a sampling rate of 16 kHz, with signal-to-noise ratio values randomly drawn from a uniform distribution ranging from −10 dB to 30 dB. The dataset was then partitioned into training and validation subsets using an 85/15 split. For testing, we employed the same test set as the original ULCNet paper, which is the synthetic, nonreverberant test set provided as part of the DNS challenge.

## 3.1.4. Training setup

Experiments were conducted using fixed hyperparameters, with training batches of 32 samples of 10 seconds each, and 4000 training steps and 1000 validation steps per epoch. The STFT used a 32-ms window, 16-ms hop size, and 512-point FFT. Optimization employed Adam with an initial learning rate of $1 \times 1 0 ^ { - 3 }$ , gradient clipping at 3.0, and a scheduler reducing the learning rate by half after 3 epochs without validation loss improvement. Early stopping halted training if the validation loss failed to decrease for five consecutive epochs, and the model with the lowest validation loss was selected for testing.

Table 1: Objective metric results on the original 10-second DNS Challenge 2020 synthetic non-reverberant test set and a synthetically extended 90-second version. Evaluated metrics include DNSMOS (SIGMOS, BAKMOS, OVRLMOS), PESQ, and SI-SDR.

<table><tr><td>Test signal length</td><td>Model</td><td>OVRLMOS</td><td>SIGMOS</td><td>BAKMOS</td><td>PESQ</td><td>SI-SDR</td></tr><tr><td rowspan="3">10 seconds</td><td>ULCNet</td><td>3.10</td><td>3.39</td><td>3.96</td><td>2.62</td><td>16.24</td></tr><tr><td>Fast-ULCNet (ours)</td><td>3.09</td><td>3.39</td><td>3.95</td><td>2.51</td><td>15.99</td></tr><tr><td> $Fast-ULCNet_{comfi}$ (ours)</td><td>3.09</td><td>3.39</td><td>3.97</td><td>2.50</td><td>16.01</td></tr><tr><td rowspan="3">90 seconds</td><td>ULCNet</td><td>3.09</td><td>3.39</td><td>3.95</td><td>2.66</td><td>16.89</td></tr><tr><td>Fast-ULCNet (ours)</td><td>2.93</td><td>3.39</td><td>3.62</td><td>2.24</td><td>13.58</td></tr><tr><td> $Fast-ULCNet_{comfi}$ (ours)</td><td>3.10</td><td>3.39</td><td>3.99</td><td>2.51</td><td>16.48</td></tr></table>

Table 2: Number of parameters, MACs and mean RTF measurement on the Raspberry Pi 3 B+ (Pi3) and Arm Cortex-A53 (ARM).

<table><tr><td>Model</td><td>Params (M)</td><td>MACs (M)</td><td>RTF $_{Pi3}$ </td><td>RTF $_{ARM}$ </td></tr><tr><td>ULCNet</td><td>0.685</td><td>2.057</td><td>0.976</td><td>0.927</td></tr><tr><td>Fast-ULCNet</td><td>0.338</td><td>1.691</td><td>0.657</td><td>0.604</td></tr></table>

## 3.2. Results

## 3.2.1. Objective evaluation

Recognizing the importance of evaluating model performance on longer audio sequences, we assess speech enhancement using two versions of the same test set. The first is the original set, containing 10-second audio samples. The second is an extended version, created by concatenating each sample with itself nine times, resulting in 90-second sequences.

Objective quality is assessed by predicting objective quality metrics. We used DNSMOS [12], which includes the sub-metrics for speech quality (SIGMOS), background noise quality (BAKMOS), and overall quality (OVRLMOS). In addition, we report PESQ [13] and scale-invariant signal-todistortion ratio (SI-SDR) [14] scores to provide a comprehensive evaluation.

As shown in Table 1, when evaluated on the original 10- second test set, the performance of Fast-ULCNet and Fast-$\mathrm { U L C N e t } _ { \mathrm { c o m f } }$ is comparable to that of the original ULCNet, with only minimal differences between the two Fast-ULCNet variants. This is most evident in the DNSMOS metrics, while PESQ and SI-SDR results slightly favor ULCNet.

When evaluated on the extended 90-second test set, Fast-ULCNet shows a noticeable performance drop relative to the other models, attributable to the long-term degradation effects identified in this study. In contrast, Fast-ULCNet<sub>comfi</sub> effectively mitigates this issue, achieving results on par with the original ULCNet. DNSMOS scores slightly favor this configuration, yielding modest gains in sub-metrics such as OVRLMOS and BAKMOS. However, PESQ and SI-SDR still marginally favor the original ULCNet.

## 3.2.2. Computational complexity

To evaluate the computational complexity of the models, we consider the total number of parameters, the number of multiply-accumulate operations (MACs), and the computational latency on resource-constrained platforms, measured as the mean real-time factor (RTF) over 10,000 iterations using a single thread. The embedded platforms used for this evaluation are the Arm Cortex-A53 and the Raspberry Pi 3 B+.

Table 2 compares the computational complexity of the ULCNet and Fast-ULCNet models. The variant with the complementary filter yields identical results and is therefore omitted for clarity. Fast-ULCNet reduces the parameter count to less than half that of ULCNet and decreases the number of MACs by 0.366 million. This reduction in complexity translates into significantly lower processing latency, with RTF improvements of approximately 33% on the Raspberry Pi 3 B+ and 35% on the Arm Cortex-A53.

## 4. CONCLUSION

In this work, we propose Fast-ULCNet, a fast and ultralightweight single-channel speech enhancement model. Building upon the low-complexity, state-of-the-art ULCNet architecture, we propose replacing its GRU layers with FastGRNN units to further reduce computational overhead. Additionally, we identify and empirically demonstrate a performance degradation in FastGRNN over extended time steps due to RNN state drift. To address this, we introduce Comfi-FastGRNN, an enhanced variant that incorporates a trainable complementary filter. Experimental results indicate that Fast-ULCNet achieves comparable performance to the original ULCNet, while being approximately 34% faster and requiring less than half the parameter count. Future work may explore integrating the Comfi-FastGRNN layer into diverse architectures to assess transferability of its benefits, along with conducting perceptual evaluations across models.

## 5. REFERENCES

[1] Chengshi Zheng, Huiyong Zhang, Wenzhe Liu, Xiaoxue Luo, Andong Li, Xiaodong Li, and Brian C.J. Moore, “Sixty years of frequency-domain monaural speech enhancement: From traditional to deep learning methods,” Trends in Hearing, vol. 27, pp. 23312165231209913, 2023.

[2] Hendrik Schroter, Alberto N. Escalante, Tobias Rosenkranz, and Andreas Maier, “DeepFilterNet: A low complexity speech enhancement framework for fullband audio based on deep filtering,” in ICASSP 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2022, pp. 7407–7411.

[3] Hyeong-Seok Choi, Sungjin Park, Jie Hwan Lee, Hoon Heo, Dongsuk Jeon, and Kyogu Lee, “Real-time denoising and dereverberation wtih tiny recurrent u-net,” in ICASSP 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2021, pp. 5789–5793.

[4] Weiqi Jiang, Chengli Sun, Feilong Chen, Yan Leng, Qiaosheng Guo, Jiayi Sun, and Jiankun Peng, “Low complexity speech enhancement network based on frame-level Swin transformer,” Electronics, vol. 12, no. 6, pp. 1330, 2023.

[5] Shrishti Saha Shetu, Soumitro Chakrabarty, Oliver Thiergart, and Edwin Mabande, “Ultra low complexity deep learning based noise suppression,” in ICASSP 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2024, pp. 466– 470.

[6] Kyunghyun Cho, Bart Van Merrienboer, Dzmitry Bah-¨ danau, and Yoshua Bengio, “On the properties of neural machine translation: Encoder-decoder approaches,” arXiv preprint arXiv:1409.1259, 2014.

[7] Junyoung Chung, Caglar Gulcehre, KyungHyun Cho, and Yoshua Bengio, “Empirical evaluation of gated recurrent neural networks on sequence modeling,” arXiv preprint arXiv:1412.3555, 2014.

[8] Aditya Kusupati, Manish Singh, Kush Bhatia, Ashish Kumar, Prateek Jain, and Manik Varma, “FastGRNN: A fast, accurate, stable and tiny kilobyte sized gated recurrent neural network,” Advances in neural information processing systems, vol. 31, 2018.

[9] Donald S. Williamson, Yuxuan Wang, and DeLiang Wang, “Complex ratio masking for monaural speech separation,” IEEE/ACM transactions on audio, speech, and language processing, vol. 24, no. 3, pp. 483–492, 2015.

[10] Sebastian Braun and Ivan Tashev, “A consolidated view of loss functions for supervised deep learning-based speech enhancement,” in 2021 44th International Conference on Telecommunications and Signal Processing (TSP). IEEE, 2021, pp. 72–76.

[11] Chandan K.A. Reddy, Vishak Gopal, Ross Cutler, Ebrahim Beyrami, Roger Cheng, Harishchandra Dubey, Sergiy Matusevych, Robert Aichner, Ashkan Aazami, Sebastian Braun, et al., “The interspeech 2020 deep noise suppression challenge: Datasets, subjective testing framework, and challenge results,” arXiv preprint arXiv:2005.13981, 2020.

[12] Chandan K.A. Reddy, Vishak Gopal, and Ross Cutler, “DNSMOS P. 835: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors,” in ICASSP 2022 IEEE international conference on acoustics, speech and signal processing (ICASSP). IEEE, 2022, pp. 886–890.

[13] ITU-T, “Recommendation P.862: Perceptual Evaluation of Speech Quality (PESQ): An Objective Method for End-to-End Speech Quality Assessment of Narrowband Telephone Networks and Speech Codecs,” Standard P.862, International Telecommunication Union, 2001.

[14] Jonathan Le Roux, Scott Wisdom, Hakan Erdogan, and John R Hershey, “SDR–half-baked or well done?,” in ICASSP 2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2019, pp. 626–630.