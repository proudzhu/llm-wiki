Boxiang Wang1, Zhengding Luo1, Haowen Li1, Dongyuan Shi2, Junwei Ji1, Ziyi Yang1, Woon-Seng Gan1 1 School of Electrical and Electronic Engineering, Nanyang Technological University, Singapore  
Email: {boxiang001, luoz0021, junwei002, ziyi016}@e.ntu.edu.sg, {haowen.li, ewsgan}@ntu.edu.sg 2 Center of Intelligent Acoustics and Immersive Communications, Northwestern Polytechnical University, China  
E-mail: dongyuan.shi@nwpu.edu.cn

###### Abstract

Selective fixed-filter active noise control (SFANC) is a novel approach capable of mitigating noise with varying frequency characteristics. It offers faster response and greater computational efficiency compared to traditional adaptive algorithms. However, spatial factors, particularly the influence of the noise source location, are often overlooked. Some existing studies have explored the impact of the direction-of-arrival (DoA) of the noise source on ANC performance, but they are mostly limited to free-field conditions and do not consider the more complex indoor reverberant environments. To address this gap, this paper proposes a learning-based directional SFANC method that incorporates the DoA of the noise source in reverberant environments. In this framework, multiple reference signals are processed by a convolutional neural network (CNN) to estimate the azimuth and elevation angles of the noise source, as well as to identify the most appropriate control filter for effective noise cancellation. Compared to traditional adaptive algorithms, the proposed approach achieves superior noise reduction with shorter response times, even in the presence of reverberations.

## 1 Introduction

Active noise control (ANC) is an advanced technique that effectively attenuates low-frequency noise, offering a more compact and lightweight alternative to traditional passive noise control methods [^3]. In an ANC system, a secondary source is driven by the control signal to generate anti-noise with equal amplitude but opposite phase as the unwanted noise, thereby reducing the disturbance through the sound destructive interference principle [^8]. Owing to its compact size and effective noise reduction capabilities, ANC has been widely applied in various applications [^18] [^7]. To address time-varying noise and dynamic acoustic environments, adaptive algorithms such as the filtered-x least mean squared (FxLMS) algorithm are commonly employed to update the control filter in real time [^15] [^5]. However, these algorithms often involve high computational complexity, slow convergence speed, and are at risk of divergence [^24] [^6]. To ensure simplicity and stability, many commercial ANC systems utilize pre-trained control filters with fixed coefficients [^18]. Nevertheless, the performance of such fixed-filter approaches is highly sensitive to variations in noise source type and direction-of-arrival (DoA), leading to suboptimal results when either of these factors changes.

To address these limitations, the selective fixed-filter ANC (SFANC) method has been proposed to select the most appropriate control filter for various incoming noise types, utilizing either traditional signal processing techniques [^20] [^19] or deep learning-based approaches [^13] [^25] [^26]. This method provides a more robust solution for noise sources with diverse frequency characteristics, while maintaining low computational cost and fast response time. However, SFANC methods mainly focus on the frequency content of the noise and overlook spatial information, such as DoA, which has also been proven to be critical for the performance of ANC systems [^11].

To date, several researchers have developed methods to incorporate the influence of DoA into ANC systems. Some studies have aimed to enhance noise cancellation from various directions by improving the causality of the ANC system [^29]. Others have focused on achieving spatial selectivity, in which unwanted noise is suppressed while the desired sound is preserved. This has been accomplished either by initially canceling both the noise and the desired sound and subsequently reproducing the desired sound [^16] [^28], or by selectively controlling the unwanted noise while leaving the desired sound unaffected [^27]. However, these techniques rely on adaptive algorithms for real-time control filter updates. Toyooka et al. proposed a method that selects fixed filters corresponding to different noise source locations [^23]. Su et al. proposed an alternative approach that considers both the frequency and directional information of the noise source for control filter selection in a multichannel ANC system [^22] [^21]. However, these methods are limited to free-field environments and rely on traditional signal processing techniques for DoA estimation, which are ineffective in handling noise sources under complex reverberant environments. In contrast, deep neural networks (DNNs) are powerful models for accurate source locations without requiring specific modeling assumptions, making them well-suited for such challenging acoustic conditions [^10].

To address this limitation, this paper proposes a convolutional neural network (CNN)-based directional SFANC method that incorporates DoA information of the noise source in reverberant environments. To achieve this, a CNN trained using multi-task learning is deployed on a co-processor to estimate the elevation and azimuth angles of the noise source based on multiple reference signals, and to select the most appropriate control filter at the frame level. The selected control filter is then applied on a sample-by-sample basis to enable delayless noise control.

The remainder of this paper is organized as follows. Section II introduces the fundamentals of DNN-based DoA estimation and the multi-reference ANC system. Section III describes the overall framework and details of the proposed directional SFANC method. Section IV evaluates the performance of the proposed algorithm through numerical simulations. Finally, Section V concludes the paper with future research directions.

## 2 Preliminaries of DNN-based Directional ANC

### 2.1 General Principle of DNN-based DoA Estimation

DNN-based DoA estimation depends on the multichannel signals recorded with an array of $J$ microphones spatially distributed in the environment, which collectively capture the directional information of the sound source. In reverberant environments, the signal received at the $j$ -th microphone can be modeled as

$$
{r_{j}}(n)={q_{j}}(n)*x(n),
$$

where ${r_{j}}(n)$ denotes the signal received at the $j$ -th microphone, $x(n)$ is the source signal, ${q_{j}}(n)$ represents the room impulse responses (RIRs) between the source and the $j$ -th microphone and $*$ denotes the linear convolution operator.

Due to differences in source location, microphone location, and room acoustics, each microphone captures a version of the source signal convolved with a distinct RIR. These variations result in interchannel differences in delay and amplitude, which encode spatial information about the DoA of the sound source relative to the microphone array. DNNs can automatically identify the relationship between the multichannel signal features and the sound source location. This offers a significant advantage over traditional DoA estimation techniques, which often rely on specific modeling assumptions and tend to perform poorly in complex indoor environments. Accordingly, the proposed directional SFANC framework employs a CNN to estimate the DoA, specifically the azimuth angle $\theta$ and elevation angle $\phi$ of the noise source.

### 2.2 Multi-Reference Active Noise Control System

In addition to DoA estimation, the multichannel signals can also serve as reference inputs for the ANC system. Figure 1 illustrates the block diagram of the multi-reference ANC system that consists of $J$ reference microphones, $1$ secondary source and $1$ error microphone. The control signal utilized to drive the secondary source is expressed as

$$
y(n)=\sum\limits_{j=1}^{J}{{\mathbf{r}}_{j}^{\rm T}(n)}{{\mathbf{w}}_{j}}(n),
$$

where ${{\mathbf{r}}_{j}}(n)={[{r_{j}}(n),{r_{j}}(n-1),\cdots,{r_{j}}(n-L+1)]^{\rm{T}}}$ is the $j$ -th reference signal vector, ${{\mathbf{w}}_{j}}(n)={[{w_{j,1}}(n),{w_{j,2}}(n),\cdots,{w_{j,L}}(n)]^{\rm{T}}}$ is the $j$ -th control filter vector, $L$ is the control filter length and $\rm T$ denotes the matrix transpose operator.

The error signal picked up by the error microphone is stated as

$$
e(n)=d(n)-{{\mathbf{y}}^{\rm T}}(n){\mathbf{s}}(n),
$$

where $d(n)$ is the disturbance at the error microphone, ${\mathbf{y}}(n)={[y(n),y(n-1),\cdots,y(n-{L_{s}}+1)]^{\rm{T}}}$ is the control signal vector, ${\mathbf{s}}(n)={[{s_{1}}(n),{s_{2}}(n),\cdots,{s_{{L_{s}}}}(n)]^{\rm{T}}}$ is the secondary path impulse response and $L_{s}$ is the secondary path length.

According to the FxLMS algorithm, the $j$ -th control filter coefficient is updated by

$$
{{\mathbf{w}}_{j}}(n+1)={{\mathbf{w}}_{j}}(n)+\mu{{{\mathbf{r}}}_{j}^{\prime}}(n)e(n),
$$

where $\mu$ is the stepsize, ${{{\mathbf{r}}}_{j}^{\prime}}(n)$ is the filtered reference signal generated by passing the reference signal through the estimated secondary path as

$$
{{{\mathbf{r}}}_{j}^{\prime}}(n)=\hat{s}(n)*{{\mathbf{r}}_{j}}(n)
$$

However, the adaptive FxLMS algorithm requires time to converge and an inappropriate step size may even lead to noise amplification. To improve response time and enhance system stability, the proposed directional SFANC method selects a pre-trained fixed-filter based on the DoA of the noise source.

![Figure 1: Block diagram of the multi-reference active noise control system.](figures/multirefernec.png)

Figure 1: Block diagram of the multi-reference active noise control system.

## 3 Proposed Directional SFANC Method

The block diagram of the proposed directional SFANC technique is shown in Fig. 2. The system consists of two main components: a real-time controller for noise cancellation and a co-processor for control filter selection. As illustrated in Fig. 2, the controller operates at the sampling rate to generate the control signal. Meanwhile, reference signals are collected at each frame and transmitted to the co-processor. The objective is to estimate the azimuth and elevation angles of the noise source relative to the reference microphone array, using information embedded in the reference signals. Based on these inputs, the CNN outputs the predicted probabilities for each azimuth and elevation class as

$$
({{{\mathbf{\hat{p}}}}}_{\rm{azim}},{{{\mathbf{\hat{p}}}}}_{\rm{elev}})=CNN({{\mathbf{R}}};{\Theta^{*}})
$$

where ${{\mathbf{R}}}$ is the short-term fourier transform (STFT) spectrograms of $J$ -channel reference signals at one frame, ${\Theta^{*}}$ is the trained CNN parameters, ${{{\mathbf{\hat{p}}}}}_{\rm{azim}}=[{{\hat{p}}}_{\rm{azim},1},{{\hat{p}}}_{\rm{azim},2},...,{{\hat{p}}}_{\rm{azim},A}]$ is the predicted probability distribution over the $A$ azimuth angle classes, ${{{\mathbf{\hat{p}}}}}_{\rm{elev}}=[{{\hat{p}}}_{\rm{elev},1},{{\hat{p}}}_{\rm{elev},2},...,{{\hat{p}}}_{\rm{elev},B}]$ is the predicted probability distribution over the $B$ elevation angle classes.

Then, the estimated azimuth index $\hat{a}$ can be obtained as

$$
\hat{a}=\mathop{\arg\max}\limits_{i\in\{1,2,...,A\}}{{\hat{p}}_{\rm{azim},i}}.
$$

where ${{\hat{p}}_{\rm{azim},i}}$ denotes the predicted probability of the $i$ -th azimuth class.

And the estimated elevation index $\hat{b}$ can be obtained as

$$
\hat{b}=\mathop{\arg\max}\limits_{k\in\{1,2,...,B\}}{{\hat{p}}_{\rm{elev},k}}.
$$

where ${{\hat{p}}_{\rm{elev},k}}$ denotes the predicted probability of the $k$ -th elevation class.

Finally, based on the predicted azimuth index and elevation index, the coefficients of the selected control filter are updated at the frame rate. By facilitating cooperation between the real-time noise controller and the co-processor, the proposed directional SFANC method enables delayless noise control.

![Figure 2: Block diagram of the proposed directional SFANC method.](figures/control.png)

Figure 2: Block diagram of the proposed directional SFANC method.

### 3.1 Pre-trained Control Filter Library

Prior to the online execution of the directional SFANC method, a control filter library must be pre-trained to account for various combinations of azimuth and elevation angles of the noise source. Specifically, the horizontal plane of the reference microphone array is divided into $A$ azimuth classes, and the vertical plane is divided into $B$ elevation classes. At each discrete direction defined by this grid, the FxLMS algorithm is used to pre-train a control filter for broadband noise. These control filters are then stored in a library for deployment.

### 3.2 CNN Trained Using a Multi-Task Learning Strategy

In this work, a CNN is employed for DoA estimation, which has been found to be effective for this task [^4]. The architecture of the proposed CNN is illustrated in Fig. 3. The input consists of a one-frame, $J$ -channel reference signal, which is transformed into $J$ magnitude spectrograms and $J$ phase spectrograms using the STFT for feature extraction. The pre-processed data is passed through three convolutional modules, each comprising a convolutional layer followed by group normalization, ReLU activation, and max-pooling. Adaptive average pooling is then applied to reduce the feature maps by averaging over both frequency and time. These pooled features are subsequently fed into two fully connected (FC) layers to estimate the class probabilities for $A$ azimuth and $B$ elevation angles. Final predictions are obtained through softmax layers.

![Figure 3: Architecture of the proposed CNN.](figures/cnn.png)

Figure 3: Architecture of the proposed CNN.

As previously discussed, the selected control filter is determined by the azimuth and elevation angle indices predicted by the CNN. To enable this, the CNN is trained using a multi-task learning strategy that simultaneously performs azimuth and elevation classification. The loss functions for both tasks are cross-entropy loss functions, denoted as $Loss{{}_{\rm{azim}}}$ and $Loss{{}_{\rm{elev}}}$ respectively. The joint loss function used to train the CNN is formulated as

$$
Loss=Loss{{}_{\rm{azim}}}+Loss{{}_{\rm{elev}}}
$$

This joint loss allows the network to learn shared representations while balancing the learning of both tasks, offering a more efficient alternative to training separate models [^30].

## 4 Numerical Simulations

The effectiveness of the proposed directional SFANC method is evaluated in a 4×1×1 multi-reference ANC system in reverberant environments, where a four-channel tetrahedral microphone array with a diameter of 2.5 cm is employed as the reference microphone array to effectively capture the spatial characteristics of the noise source [^9]. For the construction of the pre-trained control filter library, as illustrated in Fig. 4, the horizontal plane of the microphone array is divided into six azimuth classes: 0°, 60°, 120°, 180°, 240°, and 300°, while the vertical plane is divided into three elevation classes: 90°, 30°, and -30°. The distance between the noise source and the microphone array is fixed at 0.2 m. At each discrete direction defined by this spatial grid, a control filter is pre-trained using the FxLMS algorithm with broadband noise in the 20–2020 Hz range, targeting the low-frequency band typically addressed by ANC systems. A total of 13 control filters are trained and stored in the library. The STFT is computed using a Hann window of 1024 samples, a hop size of 64 samples, and the system operates at a sampling frequency of 16 kHz.

![Figure 4: Pre-trained control filter library.](figures/cflibrary.png)

Figure 4: Illustration of the pre-trained control filter library: (a) azimuth angle classes defined in the horizontal plane, and (b) elevation angle classes defined in the vertical plane.

Table 1: Configurations for training, validation and testing datasets.

<table><thead><tr><th colspan="2">Training and Validation Datasets</th></tr></thead><tbody><tr><th>Noise signal</th><td>Synthesized noises <math><semantics><mo>&</mo> <annotation>\&</annotation></semantics></math> real noises</td></tr><tr><th>Room size (m)</th><td>R1: (6x4x3); R2: (12x8x3.5); R3: (16x14x4)</td></tr><tr><th>Array positions</th><td>8 arbitrary positions in each room</td></tr><tr><th>RT <sub>60</sub> (s)</th><td>R1: 0.1, 0.2, 0.3; R2: 0.4, 0.5, 0.6; R3: 0.7, 0.8, 0.9</td></tr><tr><th>SNR (dB)</th><td>Uniformly sampled from 30 to 50</td></tr><tr><th colspan="2">Testing Dataset</th></tr><tr><th>Noise signal</th><td>Synthesized noises <math><semantics><mo>&</mo> <annotation>\&</annotation></semantics></math> real noises</td></tr><tr><th>Room size (m)</th><td>(11x9x3.2)</td></tr><tr><th>Array positions</th><td>4 arbitrary positions in each room</td></tr><tr><th>RT <sub>60</sub> (s)</th><td>0.48</td></tr><tr><th>SNR (dB)</th><td>30, 40, 50</td></tr></tbody></table>

Table 2: The classification accuracy of the CNN with different SNRs.

| Metrics | SNR = 30 dB | SNR = 40 dB | SNR = 50 dB |
| --- | --- | --- | --- |
| Azimuth angle Acc. | 96.4% | 96.4% | 96.4% |
| Elevation angle Acc. | 90.7% | 90.8% | 91.0% |

### 4.1 DoA Estimation with CNN

#### 4.1.1 Dataset generation

A noise dataset consisting of both synthetic and real noise signals is first constructed. The synthetic noises are generated as bandlimited white noise with varying bandwidths, while the real noises are sourced from the UrbanSound8K dataset [^17]. The generated noise signals are then convolved with a variety of RIRs to produce reference signals captured by the tetrahedral microphone array, with additive noise included. The azimuth angle of the noise source relative to the microphone array is randomly selected from the range \[0°, 360°\], the elevation angle from \[-60°, 90°\], and the source-to-array distance from \[0.1 m, 0.6 m\], with the array-to-surface distance maintained at over 1 m. The nearest azimuth and elevation angle classes, as defined in Fig. 4, are assigned as the corresponding labels. To enhance the system’s robustness under adverse acoustic conditions, the training and validation datasets incorporate variations of the RIRs made with different room sizes, array positions, reverberation time (RT <sub>60</sub>), and signal-to-noise ratio (SNR) levels. For the testing dataset, both the noise types and acoustic environments are distinct from those used during training, ensuring a fair evaluation of generalization performance. A summary of the dataset configuration is provided in Table I. The RIRs are generated using the gpuRIR library [^2] based on the image method [^1].

In total, the dataset includes 46080 training samples (38400 synthetic, 7680 real), 5760 validation samples (4800 synthetic, 960 real), and 4800 test samples (4000 synthetic, 800 real). Each sample is a four-channel, 0.5-second frame.

#### 4.1.2 Classification accuracy under unseen acoustic environments and noise types

As shown in Table II, the proposed CNN achieves a classification accuracy of approximately 96% for azimuth angle and 91% for elevation angle under varying SNR levels. Notably, these results are obtained using unseen noise types and acoustic environments during testing, highlighting the model’s strong generalization capability and robustness to real-world variability. In addition, the CNN is computationally efficient, with only 0.03 million parameters, a CPU runtime of 7.83 ms, and 119.86 million multiply-accumulate operations (MACs), making it suitable for deployment on embedded devices. These findings demonstrate the effectiveness of the proposed method in selecting appropriate control filters for noise sources with different DoAs, thereby enabling efficient noise control in reverberant environments.

### 4.2 Noise Cancellation based on DoA Estimation

Noise cancellation simulations are conducted in the testing environments summarized in Table 1 with the arrangement of the 4x1x1 multi-reference ANC system shown in Fig. 5. The proposed directional SFANC method is compared with several baseline methods, including the conventional FxLMS algorithm, standard SFANC [^14], and generative fixed-filter ANC (GFANC) [^12]. For both the standard SFANC and GFANC methods, the pre-trained control filters are trained using a noise source located at $(\theta=0^{\circ},\phi=30^{\circ})$, corresponding to the center of the reference microphone array.

![Figure 5: Simulation arrangement of the 4x1x1 multi-reference ANC system.](figures/simulationdia2.png)

Figure 5: Simulation arrangement of the 4x1x1 multi-reference ANC system.

#### 4.2.1 Broadband Noise Cancellation

To evaluate the noise reduction performance of the proposed directional SFANC method for broadband noise, a primary noise signal in the 100–700 Hz range is first positioned at $(\theta=120^{\circ},\phi=30^{\circ})$ corresponding to the reference microphone array. The power spectral density (PSD) of the residual noise after applying the FxLMS, SFANC, GFANC, and directional SFANC methods is shown in Fig. 6(a). The PSD is computed by averaging across the entire duration of the signal and the step size of the FxLMS algorithm is set to $1\times{10^{-4}}$. Additionally, the averaged noise reduction levels per 0.5 second achieved by the four methods are presented in Fig. 6(b). A similar evaluation is conducted for a noise source located at $(\theta=0^{\circ},\phi=-30^{\circ})$ corresponding to the reference microphone array, with the results shown in Fig. 7. As shown in Fig. 6 and Fig. 7, the proposed directional SFANC method outperforms the conventional FxLMS algorithm in terms of both response time and noise reduction performance. Furthermore, when the azimuth or elevation angle of the noise source deviates from the pre-trained filter location used in the SFANC and GFANC methods, these approaches exhibit limited noise reduction capability or may even amplify the noise. This degradation is attributed to their inability to track changes in the DoA of the noise source.

![Figure 6: PSD and noise reduction for broadband noise at (θ=120°, ϕ=30°).](figures/sim1.png)

Figure 6: (a) PSD and (b) averaged noise reduction level per 0.5 second attenuated by different ANC algorithms for 100–700 Hz broadband noise located at ( θ = 120 ∘, ϕ 30 ) (\\theta=120^{\\circ},\\phi=30^{\\circ}) relative to the reference microphone array.

![Figure 7: PSD and noise reduction for broadband noise at (θ=0°, ϕ=-30°).](figures/sim2.png)

Figure 7: (a) PSD and (b) averaged noise reduction level per 0.5 second attenuated by different ANC algorithms for 100–700 Hz broadband noise located at ( θ = 0 ∘, ϕ − 30 ) (\\theta=0^{\\circ},\\phi=-30^{\\circ}) relative to the reference microphone array.

#### 4.2.2 Real-world Noise Cancellation

To evaluate the noise reduction performance of the proposed directional SFANC method on real-world noise, a washing machine noise source is positioned at $(\theta=110^{\circ},\phi=-15^{\circ})$ corresponding to the reference microphone array. The PSD of the residual noise after applying the FxLMS, SFANC, GFANC, and directional SFANC methods is shown in Fig. 8(a). In addition, the average noise reduction levels per 0.5-second interval achieved by the four methods are presented in Fig. 8(b). It can be observed that the proposed directional SFANC method continues to achieve superior noise reduction performance and faster response time compared to the FxLMS algorithm, even when the noise source is located at a position not included in the pre-trained control filter library. In contrast, the SFANC and GFANC methods tend to amplify the noise due to their inability to adapt to variations in the DoA of the noise source.

![Figure 8: PSD and noise reduction for washing machine noise at (θ=110°, ϕ=-15°).](figures/sim3.png)

Figure 8: (a) PSD and (b) averaged noise reduction level per 0.5 second attenuated by different ANC algorithms for washing machine noise located at ( θ = 110 ∘, ϕ − 15 ) (\\theta=110^{\\circ},\\phi=-15^{\\circ}) relative to the reference microphone array.

## 5 Conclusions

This paper proposes a novel directional SFANC method to tackle noise sources with varying DoA in complex reverberant environments. A lightweight CNN, trained via multi-task learning, is employed to dynamically select the optimal control filter based on the reference signals. Simulation results show that the proposed method significantly outperforms the conventional FxLMS algorithm for both broadband and real-world noises across various DoAs, offering faster response and superior noise reduction under reverberant conditions. In contrast, many existing learning-based ANC approaches struggle to adapt to directional variations in the noise source.

Despite its advantages, the current method does not consider the source-to-array distance, which may also affect ANC performance. Future work will address this by integrating distance estimation into the control framework.

[^1]: J. B. Allen and D. A. Berkley (1979) Image method for efficiently simulating small-room acoustics. The Journal of the Acoustical Society of America 65 (4), pp. 943–950. Cited by: §4.1.1.

[^2]: D. Diaz-Guerra, A. Miguel, and J. R. Beltran (2021) GpuRIR: a python library for room impulse response simulation with gpu acceleration. Multimedia Tools and Applications 80 (4), pp. 5653–5671. Cited by: §4.1.1.

[^3]: S. J. Elliott and P. A. Nelson (1993) Active noise control. IEEE signal processing magazine 10 (4), pp. 12–35. Cited by: §1.

[^4]: P. Grumiaux, S. Kitić, L. Girin, and A. Guérin (2022) A survey of sound source localization with deep learning methods. The Journal of the Acoustical Society of America 152 (1), pp. 107–151. Cited by: §3.2.

[^5]: J. Ji, D. Shi, Z. Luo, B. Wang, and W. Gan (2025) Self-boosted weight-constrained fxlms: a robustness distributed active noise control algorithm without internode communication. IEEE Signal Processing Letters. Cited by: §1.

[^6]: J. Ji, D. Shi, B. Wang, X. Shen, Z. Luo, and W. Gan (2025) Preventing output saturation in active noise control: an output-constrained kalman filter approach. In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 1–5. Cited by: §1.

[^7]: W. Jung, S. J. Elliott, and J. Cheer (2019) Local active control of road noise inside a vehicle. Mechanical Systems and Signal Processing 121, pp. 144–157. Cited by: §1.

[^8]: S. M. Kuo and D. R. Morgan (1999) Active noise control: a tutorial review. Proceedings of the IEEE 87 (6), pp. 943–973. Cited by: §1.

[^9]: S. S. Kushwaha, I. R. Roman, M. Fuentes, and J. P. Bello (2023) Sound source distance estimation in diverse and dynamic acoustic conditions. In 2023 IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA), pp. 1–5. Cited by: §4.

[^10]: H. Li, W. Zhang, and L. Zhang (2023) DoA estimation of room reflections using nn-based music algorithm. In 2023 Asia Pacific Signal and Information Processing Association Annual Summit and Conference (APSIPA ASC), pp. 1960–1965. Cited by: §1.

[^11]: S. Liebich, J. Richter, J. Fabry, C. Durand, J. Fels, and P. Jax (2018) Direction-of-arrival dependency of active noise cancellation headphones. In Noise Control and Acoustics Division Conference, Vol. 51425, pp. V001T08A003. Cited by: §1.

[^12]: Z. Luo, J. Ji, B. Wang, D. Shi, H. Ma, and W. Gan (2025) Deep learning-based generative fixed-filter active noise control: transferability and implementation. Mechanical Systems and Signal Processing 238, pp. 113207. Cited by: §4.2.

[^13]: Z. Luo, D. Shi, and W. Gan (2022) A hybrid sfanc-fxnlms algorithm for active noise control based on deep learning. IEEE Signal Processing Letters 29, pp. 1102–1106. Cited by: §1.

[^14]: Z. Luo, D. Shi, J. Ji, X. Shen, and W. Gan (2024) Real-time implementation and explainable ai analysis of delayless cnn-based selective fixed-filter active noise control. Mechanical Systems and Signal Processing 214, pp. 111364. Cited by: §4.2.

[^15]: D. Morgan (1980) An analysis of multiple correlation cancellation loops with a filter in the auxiliary path. IEEE Transactions on Acoustics, Speech, and Signal Processing 28 (4), pp. 454–467. Cited by: §1.

[^16]: V. Patel, J. Cheer, and S. Fontana (2019) Design and implementation of an active noise control headphone with directional hear-through capability. IEEE Transactions on Consumer Electronics 66 (1), pp. 32–40. Cited by: §1.

[^17]: J. Salamon, C. Jacoby, and J. P. Bello (2014) A dataset and taxonomy for urban sound research. In Proceedings of the 22nd ACM international conference on Multimedia, pp. 1041–1044. Cited by: §4.1.1.

[^18]: X. Shen, D. Shi, W. Gan, and S. Peksi (2022) Adaptive-gain algorithm on the fixed filters applied for active noise control headphone. Mechanical Systems and Signal Processing 169, pp. 108641. Cited by: §1.

[^19]: C. Shi, R. Xie, N. Jiang, H. Li, and Y. Kajikawa (2019) Selective virtual sensing technique for multi-channel feedforward active noise control systems. In ICASSP 2019-2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 8489–8493. Cited by: §1.

[^20]: D. Shi, W. Gan, B. Lam, and S. Wen (2020) Feedforward selective fixed-filter active noise control: algorithm and implementation. IEEE/ACM Transactions on Audio, Speech, and Language Processing 28, pp. 1479–1492. Cited by: §1.

[^21]: X. Su, D. Shi, B. Wu, L. Ye, and W. Gan (2025) Co-forecasting of time-varying spatial-frequency map for selective fixed-filter multichannel anc based on dynamic factor graph. IEEE Transactions on Audio, Speech and Language Processing. Cited by: §1.

[^22]: X. Su, D. Shi, Z. Zhu, W. Gan, and L. Ye (2024) Spatial-frequency-based selective fixed-filter algorithm for multichannel active noise control. IEEE Signal Processing Letters. Cited by: §1.

[^23]: S. Toyooka and Y. Kajikawa (2025) Active noise control systems with sound source localization robust to noise source movement. IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences 108 (2), pp. 160–164. Cited by: §1.

[^24]: B. Wang, J. Ji, X. Shen, D. Shi, and W. Gan (2024) Computation-efficient virtual sensing approach with multichannel adjoint least mean square algorithm. In INTER-NOISE and NOISE-CON Congress and Conference Proceedings, Vol. 270, pp. 1638–1650. Cited by: §1.

[^25]: B. Wang, M. Misol, Z. Luo, J. Ji, X. Shen, D. Shi, and W. Gan (2025) DEEP learning-based active trim panels for enhanced aircraft interior noise control. In Proceedings of the 31st International Congress on Sound and Vibration, Cited by: §1.

[^26]: B. Wang, D. Shi, Z. Luo, X. Shen, J. Ji, and W. Gan (2025) Transferable selective virtual sensing active noise control technique based on metric learning. In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 1–5. Cited by: §1.

[^27]: T. Xiao, B. Xu, and C. Zhao (2023) Spatially selective active noise control systems. The Journal of the Acoustical Society of America 153 (5), pp. 2733–2733. Cited by: §1.

[^28]: H. Zhang, J. Zhang, F. Ma, H. Sun, and P. N. Samarasinghe (2023) A directional spatial active noise control system with a sound field separation algorithm. The Journal of the Acoustical Society of America 154 (4\_supplement), pp. A162–A162. Cited by: §1.

[^29]: L. Zhang and X. Qiu (2014) Causality study on a feedforward active noise control headset with different noise coming directions in free field. Applied Acoustics 80, pp. 36–44. Cited by: §1.

[^30]: Y. Zhang and Q. Yang (2021) A survey on multi-task learning. IEEE transactions on knowledge and data engineering 34 (12), pp. 5586–5609. Cited by: §3.2.