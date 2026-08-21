Lu Bai    Yiming He    Xiaofeng Nan    Kai Chen    Jing Lu

###### Abstract

In active noise control (ANC) systems, adaptive approaches may suffer from instability or divergence, limiting their practical deployment. Consequently, fixed-parameter controllers are widely adopted, but their performance degrades under varying noise characteristics and acoustic path conditions. This paper proposes a feedback-guided DNN-based controller fusion framework for robust fixed-parameter ANC. The proposed method combines a causal WaveNet controller with a feedback-guided mixture-of-experts (MoE) module, where a gating network estimates the weights of multiple pre-trained FIR experts according to the current acoustic condition. The proposed approach improves robustness to varying acoustic conditions without online parameter updating. Furthermore, the model is fully causal and supports sample-wise streaming inference, with computational costs evenly distributed across sampling points to reduce peak computational load. Experimental results on headphone ANC demonstrate substantial low-frequency noise reduction with negligible noise amplification over 1–8 kHz.

<sup>†</sup> <sup>†</sup>

## 1 Introduction

Active noise control (ANC) mitigates unwanted noise by generating anti-noise signals that produce destructive interference in the target region [^10]. With the growing demand for acoustic comfort and quieter environments, ANC has been widely adopted in applications such as headphones [^9] [^20], automotive cabins [^11] [^7], aircraft [^4], and other fields [^21].

Conventional ANC systems widely employ adaptive filters as controllers, which update their parameters according to the measured error signals to accommodate changing acoustic environments. Although numerous adaptive algorithms have been developed to improve convergence speed and computational efficiency [^11] [^8], online adaptation still requires a convergence process and may raise stability concerns under secondary-path modeling errors or rapidly varying acoustic conditions [^12]. To improve the response speed and stability, fixed-parameter ANC controllers are widely adopted in systems for headphones [^5], windows [^3] and rooms [^6]. However, their performance can degrade when the actual noise characteristics or acoustic path conditions differ from those considered during controller optimization [^13].

Recently, deep learning has been introduced into ANC systems to develop fixed-parameter controllers with stronger modeling capabilities [^23] [^22] [^1] [^24]. Early DNN-based ANC methods [^23] [^22] adopted deep neural networks (DNNs) as ANC controllers, but their non-causal architectures and limited noise reduction performance hindered practical deployment. The fully causal WaveNet-VNN [^1] further improved DNN-based ANC controller by integrating the temporal modeling capability of WaveNet with the nonlinear modeling capability of Volterra neural networks (VNNs), achieving superior noise reduction performance under various noise types and acoustic conditions. More recently, the causal MVNet [^24] incorporated time- and frequency-domain information to further enhance ANC performance in road noise control. Nevertheless, existing DNN-based ANC controllers are generally trained offline and their performance remains dependent on the noise characteristics and acoustic conditions included in the training data. When the test conditions differ significantly from the training distribution, their noise reduction performance may degrade substantially [^2].

To improve the robustness of fixed-parameter ANC under diverse noise conditions, Luo et al. proposed a series of Selective Fixed-Filter ANC (SFANC) [^16] [^17] [^19] and Generative Fixed-Filter ANC (GFANC) [^18] [^15] [^14] [^13] frameworks. These approaches employ multiple pre-trained control filters and utilize deep neural networks to select or generate appropriate control filters according to the characteristics of the input noise, thereby improving the robustness of fixed-parameter ANC without online controller adaptation. However, their controller selection or generation is primarily based on reference-side noise features, which characterize the input noise but do not directly reflect the actual control outcome under the current acoustic system. Therefore, their ability to respond to acoustic-path mismatch may remain limited.

![[raw/papers/bai-2026-feedback-guided-anc/figures/fig1.png|Refer to caption]]

Figure 1: Overall architecture of the proposed feedforward–feedback hybrid ANC system, including the feedforward WaveNet controller branch, the gating network, and the filter experts.

To address these limitations, this paper proposes a feedback-guided DNN-based controller fusion framework for robust fixed-parameter ANC. Unlike existing SFANC and GFANC approaches that determine the controller primarily from reference-side features, the proposed framework further exploits the control and residual-error signals to characterize the actual control outcome under the current acoustic system. Specifically, a causal WaveNet provides a general control component, while a feedback-guided gating network dynamically combines multiple pre-trained FIR experts for condition-specific correction. A frequency-aware loss jointly promotes one-third-octave-band noise reduction and suppresses high-frequency rebound, while a staged training strategy progressively optimizes the WaveNet, path-specific FIR experts, and gating network. In addition, a fully causal streaming implementation distributes the computational cost across sampling points to reduce the peak computational load. Numerical simulations on headphone ANC under various noise and acoustic-path conditions demonstrate the effectiveness of the proposed framework.

## 2 THEORY

Fig. 1 illustrates the overall architecture of the proposed method. The proposed method replaces the conventional control filter with a DNN-based controller. Let $\mathbf{p}(n)$ and $\mathbf{s}(n)$ denote the primary and secondary paths, respectively. The reference signal $\mathbf{x}(n)$ is processed by the proposed DNN-based controller to generate the control signal $\mathbf{y}(n)$. The primary noise signal $\mathbf{d}(n)$ and error signal $\mathbf{e}(n)$ are expressed as

$$
\displaystyle\mathbf{d}(n)
$$
 
$$
\displaystyle=\mathbf{p}(n)*\mathbf{x}(n),
$$
$$
\displaystyle\mathbf{e}(n)
$$
 
$$
\displaystyle=\mathbf{d}(n)+\mathbf{s}(n)*\mathbf{y}(n),
$$

where $*$ denotes linear convolution.

Specifically, the proposed DNN-based controller consists of two parallel branches: a feedforward WaveNet controller branch and a feedback-guided MoE branch. The outputs of the two branches are weighted and summed to generate the final anti-noise signal, which is formulated as

$$
\mathbf{y}(n)=\alpha\mathbf{y_{\mathrm{W}}}(n)+(1-\alpha)\mathbf{y_{\mathrm{M}}}(n),
$$

where $\mathbf{y_{W}}(n)$ and $\mathbf{y_{M}}(n)$ denote the outputs of the feedforward WaveNet controller branch and the feedback-guided MoE branch, respectively, and $\alpha$ represents the fusion coefficient between the two branches.

### 2.1 Feedforward WaveNet Controller

The feedforward controller branch directly maps the reference signal sequence to the control signal sequence through a DNN. This branch exploits the nonlinear modeling capability of neural networks and provides a stable baseline controller. Its parameters are optimized using the entire training dataset, resulting in an averaged optimal solution over different acoustic conditions. Since the controller parameters remain fixed during operation and are independent of the current reference or error signals, this branch provides a stable performance baseline for the proposed adaptive fusion framework.

In this paper, we adopt WaveNet as the feedforward controller branch, as previous studies have demonstrated its effectiveness in various ANC tasks [^1]. The VNN module is not incorporated because the nonlinear effects in the considered task are relatively limited, while avoiding the additional computational cost introduced by the higher-order nonlinear modeling. For scenarios involving stronger nonlinear distortions, this branch can be readily replaced by a more expressive architecture, such as WaveNet-VNN or other suitable nonlinear neural controllers.

As shown in Fig. 1, the WaveNet controller takes the reference signal sequence $\mathbf{x}(n)$ as input and directly generates the control signal sequence $\mathbf{y}_{\mathrm{W}}(n)$. Two one-dimensional convolutional (Conv1d) layers are applied after the input and before the output to adjust the number of channels. The backbone consists of a stack of residual blocks, each consisting of a dilated one-dimensional convolution (Dilated Conv1d) layer, a gated unit, and a Conv1d layer. The dilated convolution enlarges the receptive field without significantly increasing the number of parameters, enabling the network to capture long-term temporal dependencies in the reference signal. Within each residual block, the output of the Dilated Conv1d is further processed by the gated activation unit to enhance the nonlinear modeling capability of the network. Specifically, the gated activation unit is formulated as

$$
\mathbf{z}=\tanh\left(W_{f,k}*\mathbf{a}\right)\odot\sigma\left(W_{g,k}*\mathbf{a}\right),
$$

where $\ast$ denotes the convolution operation, $\odot$ represents the element-wise multiplication operator, $\sigma(\cdot)$ is the sigmoid function, $k$ is the layer index, $f$ and $g$ correspond to the filter and gate, respectively, and $W$ is a learnable convolution kernel.

### 2.2 Feedback-Guided MoE

As shown in Fig. 1, the feedback-guided MoE module consists of a gating network and multiple filter experts. The gating network estimates the fusion weights of different experts based on the current acoustic condition, while the filter experts consist of multiple pre-trained finite impulse response (FIR) filter controllers with different coefficients. The coefficients of these experts are dynamically weighted and combined to obtain the MoE controller:

$$
\mathbf{w}_{\mathrm{M}}(n)=\sum_{i=1}^{N}\beta_{i}(n-1)\mathbf{w}_{i},
$$

where $N$ represents the total number of experts, $\mathbf{w}_{i}$ denotes the coefficients of the $i$ -th filter expert, and $\beta_{i}(n-1)$ represents the corresponding fusion weight estimated at the previous sampling point. The output of the MoE controller is then obtained as

$$
\mathbf{y_{\mathrm{M}}}(n)=\mathbf{w}_{\mathrm{M}}(n)*\mathbf{x}(n).
$$

#### 2.2.1 Gating Network

The gating network aims to estimate the fusion weights of different FIR controller experts according to the current acoustic condition. As shown in Fig. 1, the inputs of the gating network include the reference signal $\mathbf{x}(n)$, control signal $\mathbf{y}(n)$, and error signal $\mathbf{e}(n-1)$. At sampling point $n$, the current control signal $\mathbf{y}(n)$ is first generated using the fusion weights $\boldsymbol{\beta}(n-1)$ estimated at the previous sampling point. The gating network then uses $\mathbf{x}(n)$, $\mathbf{y}(n)$, and $\mathbf{e}(n-1)$ to update the fusion weights to $\boldsymbol{\beta}(n)$, which are applied to generate the control signal at sampling point $n+1$. Therefore, no current output depends on gating weights computed from that same output, and the proposed feedback-guided fusion remains causal. These signals are first concatenated along the channel dimension and then processed by two parallel feature extraction branches. The one-sample delay of the error signal is introduced because $\mathbf{e}(n)$ becomes available only after $\mathbf{y}(n)$ has propagated through the secondary path. Although the error signal is not exactly aligned with the reference and control signals, the introduced delay has negligible influence on the performance, as verified by experimental results.

The first branch employs three cascaded convolutional blocks to extract temporal features from the input sequences. Each convolutional block consists of a one-dimensional convolution (Conv1d) layer, a layer normalization (Layer Norm) operation, and a SiLU activation function. After the convolutional blocks, a temporal mean operation is applied to obtain a global temporal representation. The second branch calculates the logarithmic root mean square (Log RMS) features to characterize the amplitude statistics of the input signals. The features extracted from the two branches are then concatenated and fed into an MLP consisting of two linear layers and a SiLU activation function. Finally, a Softmax layer is applied to generate the fusion weights of different FIR controller experts.

#### 2.2.2 Filter Experts

The filter experts consist of multiple pre-trained FIR filter controllers with different coefficients. In this work, each filter expert is directly implemented using a Conv1d layer with a kernel size of $2048$. This implementation is equivalent to a 2048-tap FIR filter without coefficient flipping. The coefficients of these filter experts are dynamically weighted according to the fusion weights estimated by the gating network, generating the final MoE controller.

### 2.3 Loss Function and Training Strategy

We employ a frequency-aware ANC loss based on one-third-octave-band analysis. The noise-reduction metric is the equally weighted mean noise reduction over 50 Hz–5 kHz, while the rebound metric is the largest noise amplification over 1 kHz–8 kHz and is set to zero when no band is amplified. Accordingly, $\mathcal{L}_{\mathrm{NR}}$ is defined as the negative noise-reduction metric. For a more conservative constraint, $\mathcal{L}_{\mathrm{RB}}$ extends the upper frequency of the rebound metric to 16 kHz. Both terms are calculated from the disturbance $\mathbf{d}$ and residual $\mathbf{e}$ using an 8192-point STFT with a Hann window and a hop size of 2048. A broadband NMSE term is further included to constrain the overall residual energy:

$$
\mathcal{L}_{\mathrm{NMSE}}=10\log_{10}\frac{\sum_{n}e^{2}(n)}{\sum_{n}d^{2}(n)}.
$$

The batch-averaged ANC objective is

$$
\mathcal{L}_{\mathrm{ANC}}=\mathcal{L}_{\mathrm{NR}}+\lambda\mathcal{L}_{\mathrm{RB}}+\mathcal{L}_{\mathrm{NMSE}},
$$

where $\lambda$ is a weighting coefficient that balances noise reduction and rebound suppression.

Training proceeds in three stages. First, the WaveNet controller is trained on all training conditions for 180 epochs. Second, each FIR expert is trained independently for 180 epochs using the data associated with its acoustic path; these two pre-training stages can be performed in parallel. Third, the pre-trained WaveNet and FIR experts are frozen, and only the gating network is optimized for 100 epochs. For this stage, a cross-entropy loss $\mathcal{L}_{\mathrm{cls}}$ supervised by the acoustic-path labels, with a label-smoothing factor of 0.05, is added as

$$
\mathcal{L}_{\mathrm{total}}=\mathcal{L}_{\mathrm{ANC}}+\gamma\mathcal{L}_{\mathrm{cls}},
$$

where $\gamma$ is a weighting coefficient that balances the contributions of the ANC loss and the classification loss. Here, $\mathcal{L}_{\mathrm{cls}}$ establishes the correspondence between acoustic paths and their associated FIR experts, while $\mathcal{L}_{\mathrm{ANC}}$ refines the soft fusion weights according to the resulting ANC performance.

## 3 NUMERICAL SIMULATIONS

### 3.1 Simulation Setup

The simulations are conducted using the headphone ANC dataset provided by the second track of the CCF Audio and Acoustic Technology Challenge (CCF-AATC), available at [https://ccf-aatc.org.cn/](https://ccf-aatc.org.cn/). This dataset is designed for evaluating headphone ANC systems under diverse noise and acoustic conditions. Specifically, the dataset contains eight noise scenarios, 80 primary noise recordings, and ten sets of secondary paths. Each noise scenario includes a 30-min reference signal, resulting in eight 30-min reference recordings. The primary noise dataset consists of 80 30-min recordings corresponding to different path conditions, while the ten secondary paths are provided to model the acoustic transfer responses from the loudspeaker to the error microphone. All data are subsampled to 48 kHz.

The first eight paths and six noise scenarios form the training set, with one FIR expert trained for each path. Primary noise recordings and the corresponding secondary paths are randomly sampled during training. The remaining two paths and two noise scenarios are reserved to evaluate robustness to unseen conditions.

### 3.2 Simulation Results

We first evaluate the noise reduction performance under unseen noise conditions with seen and unseen acoustic paths. The official CCF 2026 ANC baseline model provided by the challenge organizers ([https://github.com/CCF2026ANC/CCF\_DEEPANC\_2026](https://github.com/CCF2026ANC/CCF_DEEPANC_2026)) and a standalone feedforward WaveNet branch are adopted as comparison methods. The official CCF 2026 ANC baseline model provided by the challenge organizers is trained using the original NMSE loss and training strategy provided by the challenge. In contrast, the feedforward WaveNet branch and the proposed hybrid ANC network are trained using the optimized loss function and training strategy introduced in this work. The numbers of parameters of the official baseline, the feedforward WaveNet branch, and the proposed hybrid ANC network are 42.76k, 10.08k, and 28.57k, respectively. Their corresponding computational costs are 2.04 GMac/s, 483.84 MMac/s, and 672.83 MMac/s, respectively.

Fig. 2 presents the noise reduction spectra of different ANC methods under seen acoustic paths with unseen noise. Although the standalone feedforward WaveNet branch has fewer parameters and lower computational cost than the official baseline, it achieves superior performance when trained with the optimized loss function and training strategy proposed in this work. However, the standalone feedforward WaveNet controller still exhibits limited robustness to acoustic path variations. In particular, under the seventh seen path, it provides almost no noise reduction because this path has a significantly different acoustic response from the other training paths. Since the feedforward WaveNet controller is trained with a single set of parameters shared across all acoustic paths, it can only approximate an average optimal solution over multiple path conditions. Consequently, its performance is significantly degraded for acoustic paths with large acoustic differences from the others.

The proposed method further integrates the feedback-guided MoE branch, which achieves substantially improved low-frequency noise reduction compared with the standalone feedforward WaveNet branch, particularly under the seventh acoustic path. However, the feedback-guided MoE branch may introduce larger high-frequency amplification under certain acoustic paths. For example, under the sixth acoustic path, its high-frequency noise amplification is slightly higher than that of the standalone WaveNet branch. By combining the feedforward WaveNet branch and the feedback-guided MoE branch, the proposed hybrid architecture effectively exploits their complementary advantages, improving low-frequency noise reduction while alleviating high-frequency amplification. Fig. 3 presents the noise reduction spectra of different ANC methods under unseen acoustic paths. It can be observed that the proposed method achieves superior noise reduction performance on both unseen acoustic paths, demonstrating its robustness to acoustic path variations.

![[raw/papers/bai-2026-feedback-guided-anc/figures/fig2.png|Refer to caption]]

Figure 2: Noise reduction spectra of different ANC methods under seen acoustic paths with unseen noise.

![[raw/papers/bai-2026-feedback-guided-anc/figures/fig3.png|Refer to caption]]

Figure 3: Noise reduction spectra of different ANC methods under unseen acoustic paths with unseen noise.

Furthermore, we train a ten-expert model on the complete dataset, with one FIR expert for each path. It is evaluated on three randomly selected paths and two noise conditions per path, forming six 5-s cases (30 s in total). Fig. 4 shows that the model maintains stable noise reduction across condition switches without convergence time. The corresponding third-octave-band result in Fig. 5 shows an average noise reduction of 19.00 dB from 50 Hz to 5 kHz with negligible noise amplification over 1–8 kHz.

![[raw/papers/bai-2026-feedback-guided-anc/figures/fig4.png|Refer to caption]]

Figure 4: Time-domain noise reduction performance of the proposed ANC model under different acoustic paths and noise conditions.

![[raw/papers/bai-2026-feedback-guided-anc/figures/fig5.png|Refer to caption]]

Figure 5: Third-octave band noise reduction performance of the proposed ANC model.

For the ten-expert model, we further develop a fully streaming implementation with peak-MAC optimization. It contains 32.69k parameters, compared with 28.57k for the eight-expert model, due to two additional 2048-tap FIR experts and their gating outputs. Its cost is 672.93 MMac/s, versus 672.83 MMac/s for the eight-expert model. Compared with standard streaming inference, peak-MAC optimization reduces the peak MAC from 34.62k to 14.15k while leaving the overall complexity essentially unchanged.

## 4 CONCLUSION

This paper proposes a feedback-guided DNN-based controller fusion framework for robust fixed-parameter ANC. The proposed framework integrates a causal WaveNet controller with a feedback-guided MoE module, where residual-error and control signals are utilized to dynamically fuse multiple pre-trained FIR experts according to the current acoustic condition. By incorporating the effects of acoustic transfer paths into controller fusion, the proposed method improves the robustness of fixed-parameter ANC without online parameter updating. Furthermore, a fully causal sample-wise streaming implementation is developed to enable efficient sample-wise inference, and the computational cost is evenly distributed across sampling points to reduce the peak computational load. Numerical simulations on headphone ANC demonstrate that the proposed framework consistently outperforms baseline methods under different noise conditions and acoustic paths, achieving substantial low-frequency noise reduction with negligible noise amplification over 1–8 kHz.

[^1]: L. Bai, S. Lian, M. Li, Y. He, L. Rao, X. Zeng, R. Sun, K. Chen, and J. Lu (2025) WaveNet-volterra neural network for active noise control: a fully causal approach. Mechanical Systems and Signal Processing 241, pp. 113486. Cited by: §1, §2.1.

[^2]: L. Bai, J. Xue, S. Lian, Y. He, Y. Liang, L. Rao, S. Wang, and J. Lu (2026) An adaptive deep neural network for active road noise control. The Journal of the Acoustical Society of America 159 (4), pp. 3674–3685. Cited by: §1.

[^3]: L. Bhan, T. Murao, C. Shi, W. Gan, and S. Elliott (2016) Feasibility of the full-rank fixed-filter approach in the active control of noise through open windows. In INTER-NOISE and NOISE-CON Congress and Conference Proceedings, Vol. 253, pp. 3548–3555. Cited by: §1.

[^4]: S. J. Elliot, P. A. Nelson, I. M. Stothers, and C. C. Boucher (1990) In-flight experiments on the active control of propeller-induced cabin noise. Journal of Sound and Vibration 140 (2), pp. 219–238. Cited by: §1.

[^5]: J. Fabry, F. König, S. Liebich, and P. Jax (2019) Acoustic equalization for headphones using a fixed feed-forward filter. In ICASSP 2019-2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 980–984. Cited by: §1.

[^6]: R. Haasjes and A. P. Berkhoff (2024) An efficient offline scheme to compute an fir controller for active reduction of acoustic reflections in an anechoic chamber. Journal of Sound and Vibration 573, pp. 118198. Cited by: §1.

[^7]: Y. He, L. Bai, L. Rao, K. Chen, J. Tao, and X. Qiu (2026) A neural reference projection-based method for multi-reference active noise control (l). The Journal of the Acoustical Society of America 159 (5), pp. 4482–4486. Cited by: §1.

[^8]: Y. He, W. Chen, K. Chen, J. Tao, and X. Qiu (2025) A modified least mean square newton algorithm based on block coordinate descent for multi-reference active noise control. The Journal of the Acoustical Society of America 158 (3), pp. 2377–2388. Cited by: §1.

[^9]: S.M. Kuo, S. Mitra, and W. Gan (2006) Active noise control system for headphone applications. IEEE Trans. Control Syst. Technol. 14 (2), pp. 331–335. Cited by: §1.

[^10]: S. M. Kuo and D. R. Morgan (1999) Active noise control: a tutorial review. Proc. IEEE 87 (6), pp. 943–973. Cited by: §1.

[^11]: S. Lian, T. Li, J. Gu, Y. Hu, C. Zhu, S. Wang, and J. Lu (2024) An online decoupling-whitening frequency domain filtered-error least mean square algorithm for active road noise control. J. Acoust. Soc. Am. 156 (2), pp. 1413–1424. Cited by: §1, §1.

[^12]: L. Lu, K. Yin, R. C. de Lamare, Z. Zheng, Y. Yu, X. Yang, and B. Chen (2021) A survey on active noise control in the past decade–part ii: nonlinear systems. Signal Processing 181, pp. 107929. Cited by: §1.

[^13]: Z. Luo, J. Ji, B. Wang, D. Shi, H. Ma, and W. Gan (2025) Deep learning-based generative fixed-filter active noise control: transferability and implementation. Mechanical Systems and Signal Processing 238, pp. 113207. Cited by: §1, §1.

[^14]: Z. Luo, H. Ma, D. Shi, and W. Gan (2024) Gfanc-rl: reinforcement learning-based generative fixed-filter active noise control. Neural Networks 180, pp. 106687. Cited by: §1.

[^15]: Z. Luo, D. Shi, W. Gan, and Q. Huang (2023) Delayless generative fixed-filter active noise control based on deep learning and bayesian filter. IEEE/ACM Transactions on Audio, Speech, and Language Processing 32, pp. 1048–1060. Cited by: §1.

[^16]: Z. Luo, D. Shi, and W. Gan (2022) A hybrid sfanc-fxnlms algorithm for active noise control based on deep learning. IEEE Signal Processing Letters 29, pp. 1102–1106. Cited by: §1.

[^17]: Z. Luo, D. Shi, J. Ji, X. Shen, and W. Gan (2024) Real-time implementation and explainable ai analysis of delayless cnn-based selective fixed-filter active noise control. Mechanical Systems and Signal Processing 214, pp. 111364. Cited by: §1.

[^18]: Z. Luo, D. Shi, X. Shen, J. Ji, and W. Gan (2023) Deep generative fixed-filter active noise control. In Icassp 2023-2023 ieee international conference on acoustics, speech and signal processing (icassp), pp. 1–5. Cited by: §1.

[^19]: Z. Luo, D. Shi, X. Su, and W. Gan (2025) Frequency-direction aware multichannel selective fixed-filter active noise control based on multi-task learning. IEEE Transactions on Audio, Speech and Language Processing 33, pp. 3137–3147. Cited by: §1.

[^20]: X. Shen, D. Shi, W. Gan, and S. Peksi (2022) Adaptive-gain algorithm on the fixed filters applied for active noise control headphone. Mechanical Systems and Signal Processing 169, pp. 108641. Cited by: §1.

[^21]: S. Wang, J. Tao, X. Qiu, and I. S. Burnett (2022) Improving the performance of an active staggered window with multiple resonant absorbers. J. Acoust. Soc. Am. 151 (3), pp. 1661–1671. Cited by: §1.

[^22]: H. Zhang A. Pandey et al. (2023) Low-latency active noise control using attentive recurrent network. IEEE/ACM transactions on audio, speech, and language processing 31, pp. 1114–1123. Cited by: §1.

[^23]: H. Zhang and D. Wang (2021) Deep anc: a deep learning approach to active noise control. Neural Networks 141, pp. 1–10. Cited by: §1.

[^24]: Z. Zhang, Y. Li, B. Yang, S. Qi, X. Ding, X. Sun, Y. Luo, and S. Zheng (2026) A causal time–frequency mamba architecture with volterra nonlinear modeling for multi-channel automotive road noise control. Engineering Applications of Artificial Intelligence 181, pp. 115517. Cited by: §1.