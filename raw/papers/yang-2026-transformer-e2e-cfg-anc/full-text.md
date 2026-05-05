# Transformer-based End-to-End Control Filter Generation for Active Noise Control1

Ziyi Yang, Zhengding Luo,Yisong Zou, Boxiang Wang, Qirui Huang, and Woon-Seng Gan

# ABSTRACT

To address the limitations of existing Generative Fixed-Filter Active Noise Control (GFANC) methods, which rely on filter decomposition and recombination and require supervised learning with labeled data, this paper proposes a Transformer-based End-to-End Control-Filter Generation (E2E-CFG) framework. Unlike previous approaches that predict combination weights of sub control filters, the proposed method directly generates control filters in an unsupervised manner by integrating the coprocessor and real-time controller into a fully differentiable ANC system, where the accumulated error signal is used as the training objective. By abandoning the decomposition–reconstruction process, the proposed design simplifies the control pipeline and avoids error accumulation, while the Transformer architecture effectively captures global and dynamic noise characteristics through its attention mechanism. Numerical simulations on real-recorded noises demonstrate that the proposed method achieves improved noise reduction performance and adaptability to different types of noises compared with the original GFANC framework.

# 1. INTRODUCTION

Active noise control (ANC) reduces unwanted sound through destructive interference and has been studied for decades in applications such as ducts, vehicles, headsets, window, and enclosed spaces [1–3]. Classical feedforward and feedback ANC systems, especially those based on the filtered-x least mean square (FxLMS) algorithm and its variants, remain fundamental because of their clear physical interpretation and practical effectiveness [4–7]. However, adaptive ANC is still sensitive to causality constraints, secondary-path modeling, and convergence behavior, which limits its performance in rapidly changing acoustic conditions, particularly when low-latency implementation is required [8].

As an alternative to continuously adapting controllers, fixed-filter ANC has been widely considered in practical systems because it provides immediate response without the slow convergence associated with online adaptation [9–11]. Based on this idea, selective fixed-filter active noise control (SFANC) was proposed to select a suitable pre-trained filter according to the incoming noise condition, and later learning-based SFANC methods used convolutional neural networks (CNNs) to automate filter selection and improve practicality [12–14]. While these methods improve the flexibility of fixed-filter ANC, selecting one candidate from a limited filter set may still be insufficient when the incoming noise differs substantially from the design conditions.

To address this limitation, generative fixed-filter active noise control (GFANC) was developed to generate a more suitable control filter by combining sub-control filters rather than selecting only one candidate [15]. Existing studies showed that this strategy improves the adaptability of fixed-filter ANC, and temporal smoothing mechanisms such as Bayesian or Kalman filtering can further enhance robustness under dynamic noise conditions [15, 16]. Nevertheless, current GFANC frameworks still generate the control filter indirectly through a decomposition-and-recombination process, which increases pipeline complexity and makes performance dependent on the intermediate filter representation. In addition, the co-processor is typically trained in a supervised manner, requiring labelled targets and extra offline data preparation. Recently, Luo et al. proposed an

unsupervised GFANC framework, where the co-processor and real-time controller are integrated into a differentiable ANC system and the accumulated squared error is used directly as the training objective [17]. This result suggests that GFANC can be trained without labelled data while remaining directly aligned with the physical objective of noise cancellation.

In parallel, neural-network-based ANC has been increasingly explored beyond conventional adaptive filtering [18–21]. Under the end-to-end unsupervised GFANC formulation, the remaining question is whether the sequence modeling capability of the co-processor can be further improved. Existing GFANC methods mainly rely on one-dimensional CNNs, which are efficient but primarily operate through local receptive fields [17]. For control-filter generation, however, the appropriate filter may depend on more time-varying characteristics of the incoming noise. Transformer architectures provide a different mechanism through self-attention and have shown strong performance in sequential speech and audio tasks [22–24]. Motivated by these results, this paper investigates a Transformer-based End-to-End Control-Filter Generation (E2E-CFG) framework. Building on the unsupervised GFANC formulation, we replace the CNN-based co-processor with a Transformerbased architecture and directly generate the control filter within a fully differentiable ANC system. Numerical simulations on real-recorded noises show that the proposed method achieves improved noise reduction performance and better adaptability across different noise types than the original GFANC framework. The main contributions of this work are:

• End-to-end control-filter generation: we develop a differentiable ANC system in which the control-filter coefficients are directly generated for each input noise frame, without relying on sub-filter decomposition and recombination, thereby reducing the gap between the generated filters and the optimal control filters.   
• Transformer-based unsupervised learning: we introduce a Transformer-based co-processor and train it in an unsupervised manner by directly minimizing the accumulated residual error, without requiring labelled target filters.   
• Generalization to unseen noises: under the same end-to-end training paradigm and with training conducted only on synthetic noises, we compare the proposed method with the previous GFANC baseline [17] and show that the proposed method yields more consistent improvement on unseen real-noise conditions.

# 2. PROPOSED E2E-CFG FRAMEWORK

This paper proposes a Transformer-based End-to-End Control-Filter Generation (E2E-CFG) framework. The proposed method differs from previous GFANC approaches [17, 25] in two aspects. First, the CNN-based co-processor is replaced by a Transformer-based architecture for frame-wise control-filter generation. Second, instead of generating the final control filter through sub-filter decomposition and recombination, the proposed method directly predicts the control-filter coefficients from buffered input frames. The framework follows a two-rate structure: the physical ANC path operates at the sampling rate, while the neural co-processor updates the control filter at the frame rate.

# 2.1. Overall framework

Figure 1 illustrates the proposed framework. Let $x ( n )$ denote the reference signal, where $n$ is the discrete-time sample index. Through the primary path $P ( z )$ , the disturbance signal at the error position is denoted by $d ( n )$ . In parallel, the control filter $W ( z )$ drives the secondary path $S \left( z \right)$ to produce the anti-noise signal $y ( n )$ . The residual error is

$$
e (n) = d (n) - y (n), \tag {1}
$$

where $e ( n )$ denotes the remaining noise after cancellation.

Instead of updating the controller sample by sample, the proposed method buffers the reference signal into frames and feeds each frame to a Transformer-based co-processor. For every input frame, the co-processor generates one control-filter coefficient vector, which is then assigned to the real-time controller. In this way, the physical ANC path remains sample-wise, while the control filter is updated frame-wise.

![](figures/53c3fac581018178b6709e591a897528318388cf62918ccb05e4fcb74fe49339.jpg)  
Figure 1: Overview of the proposed Transformer-based End-to-End Control-Filter Generation framework.

# 2.2. Transformer-based co-processor

Let $\mathbf { x } _ { f } \in \mathbb { R } ^ { L }$ denote one buffered input frame of length $L$ . The proposed co-processor consists of a Conv1d layer, positional encoding, a Transformer encoder, and two fully connected (FC) layers. The Conv1d layer extracts local temporal patterns from the waveform, while the Transformer encoder captures longer-range temporal dependencies within the frame. The network output is the controlfilter coefficient vector

$$
\mathbf {w} = \mathcal {F} _ {\theta} (\mathbf {x} _ {f}), \tag {2}
$$

where $\mathcal { F } _ { \theta } ( \cdot )$ denotes the Transformer-based network with parameters $\theta$ , and

$$
\mathbf {w} = \left[ w _ {0}, w _ {1}, \dots , w _ {N - 1} \right] ^ {\mathrm {T}} \in \mathbb {R} ^ {N} \tag {3}
$$

is the generated control filter of length $N = 5 1 2$ .

In implementation, the front-end consists of a Conv1d layer with 1 input channel, 256 output channels, kernel size 64, stride 4, and padding 30, followed by batch normalization, ReLU, and max pooling with stride 4. This results in an overall temporal downsampling factor of 16. Positional encoding with maximum length 912 is added before a Transformer encoder with $d _ { \mathrm { m o d e l } } = 2 5 6 ,$ 8 attention heads, 1 encoder layer, feedforward dimension 1024, dropout 0.1, and pre-normalization. The output head consists of Linear $( 2 5 6 ~  ~ 5 1 2 )$ ), ReLU, Dropout(0 1), and Linear $( 5 1 2  5 1 2 )$ , producing a control filter of length $N = 5 1 2$ .. The total number of trainable parameters is 1,201,152.

Compared with previous GFANC methods, the proposed co-processor introduces a Transformer architecture for control-filter generation and directly outputs the final control-filter coefficients. The first design allows the network to model broader temporal dependencies than a purely convolutional co-processor, while the second removes the decomposition–recombination stage and avoids the dependence on an intermediate sub-filter representation. The trade-off is that the network must regress a higher-dimensional target directly, which may potentially require more training data.

# 2.3. End-to-end differentiable training

During training, the co-processor and the ANC forward path are integrated into one differentiable system. Let $\hat { s } ( n )$ denote the estimated secondary-path impulse response used in training. The filtered reference is

$$
x ^ {\prime} (n) = x (n) * \hat {s} (n), \tag {4}
$$

where $^ *$ denotes linear convolution. For a generated control filter w, the anti-noise is computed as

$$
y (n) = \sum_ {k = 0} ^ {N - 1} w _ {k} x ^ {\prime} (n - k), \tag {5}
$$

where $w _ { k }$ is the $k$ -th control-filter coefficient. The residual error is therefore

$$
e (n) = d (n) - \sum_ {k = 0} ^ {N - 1} w _ {k} x ^ {\prime} (n - k). \tag {6}
$$

For one frame containing $T$ samples, the unsupervised training objective is defined directly from the residual error:

$$
\mathcal {L} = \frac {1}{T} \sum_ {n = 0} ^ {T - 1} e ^ {2} (n), \tag {7}
$$

where $\mathcal { L }$ denotes the training loss. A weighted version can also be used:

$$
\mathcal {L} = \frac {1}{T} \sum_ {n = 0} ^ {T - 1} \alpha_ {n} e ^ {2} (n), \tag {8}
$$

where $\alpha _ { n }$ is the weighting coefficient at sample n. In our implementation, these weights are generated αfrom a forgetting-factor scheme with $\lambda = 0 . 9 9 9$ .

λThe key point here is that the mapping

$$
\mathbf {x} _ {f} \rightarrow \mathbf {w} \rightarrow y (n) \rightarrow e (n) \rightarrow \mathcal {L} \tag {9}
$$

is differentiable. Therefore, the network parameters can be updated by backpropagation:

$$
\theta \leftarrow \theta - \eta \nabla_ {\theta} \mathcal {L}, \tag {10}
$$

where $\eta$ is the learning rate. In contrast to supervised GFANC, no labelled target filters are required; ηthe co-processor is trained directly by minimizing the residual noise after cancellation.

# 2.4. Inference and deployment

After training, only the forward part of the co-processor is retained. In deployment, each buffered reference frame is fed into the Transformer-based network to generate the current control-filter coefficients according to Eq. (2). The generated filter is then assigned to the controller and used for sample-wise noise cancellation until the next frame update arrives.

Overall, the proposed framework combines a frame-wise Transformer co-processor with a sampling-rate ANC controller in a unified end-to-end learning architecture. This design enables direct learning of control-filter generation from the residual-noise objective while preserving the practical real-time structure of fixed-filter ANC systems.

# 3. EXPERIMENTAL SETUP

This section describes the datasets, acoustic paths, model configurations, baselines, and evaluation protocol used to assess the proposed Transformer-based E2E-CFG method. Because the proposed model is trained only on synthetic noises, its performance on unseen real-world noises is of particular interest.

# 3.1. Datasets and acoustic paths

The proposed model is trained using 83,977 synthetic band-limited noise samples. Each sample has a duration of 1 s and a sampling rate of $1 3 \mathrm { \ k H z }$ . The synthetic noises are generated by applying bandpass filters with random center frequencies and bandwidths to white noise, with effective frequency content covering $2 0 { - } 1 9 0 0 \ \mathrm { H z }$ . The dataset is divided into 79,977 training samples, 2,000 validation samples, and 2,000 test samples. During training, additive Gaussian noise with an SNR of $1 0 ~ \mathrm { d B }$ is further added to the filtered reference signal to simulate sensor noise.

The acoustic paths are also synthetically generated. A band-limited acoustic path covering 10– $3 0 0 0 \mathrm { H z }$ is used, and the same acoustic path is adopted in both training and testing.

To evaluate generalization ability, the trained model is tested on two groups of unseen noises:

– Real noises: aircraft, compressor, genset, handheld drill, large SUV pass-by, mixed aircraft traffic, motorbike, and traffic.   
– Synthetic band-limited noises: 20–490 Hz, 490–960 Hz, 20–960 Hz, and 1430–1900 Hz.

# 3.2. Model configurations and training hyperparameters

The proposed Transformer-based model uses the configuration described in Section 2, with input frame length $L = 1 3 \small { , } 0 0 0$ samples and control-filter length $N = 5 1 2$ . It is trained with Adam, weight decay $1 0 ^ { - 4 }$ ,, initial learning rate $5 \times 1 0 ^ { - 4 }$ , batch size 128, and 40 epochs. A StepLR scheduler is used with step size 5 and decay factor 0.5.

As a baseline, GFANC uses a Conv1d front-end with 128 output channels, kernel size 80, stride 4, and padding 38, followed by batch normalization, ReLU, max pooling, two residual blocks, adaptive average pooling, and a Linear $1 2 8  1 5$ ) layer with sigmoid activation. It uses $M = 1 5$ sub-filters obtained by uniformly partitioning a wideband pre-trained control filter in the frequency domain, with the same control-filter length $N = 5 1 2$ . The initial learning rate is $1 0 ^ { - 2 }$ , training runs for 10 epochs, and the StepLR scheduler uses step size 3 with decay factor 0.5. The total number of trainable parameters is 211,215.

The proposed method is compared with two baselines:

– FxNLMS: the conventional adaptive ANC baseline, with filter length 512 and step size $\mu ~ =$ 0 001.   
.– GFANC: the unsupervised GFANC framework [17] with a CNN-based co-processor.

The main evaluation metric is the noise reduction (NR) level in dB. For each test noise, the controller is run for 5 s, and the NR is computed over the last 1 s. The reported average NR values are arithmetic means over the corresponding test noises.

# 4. RESULTS

# 4.1. Comparison on unseen noises

Table 1 reports the NR results on all tested real noises and all four tested synthetic noises. On the realnoise set, the proposed Transformer-based E2E-CFG outperforms GFANC in six out of eight cases and achieves the highest average NR of 18.36 dB, compared with 16.63 dB for GFANC and 11.13 dB for FxNLMS. On the synthetic-noise set, the results are more mixed across the three methods, and FxNLMS achieves the highest average NR of 19.06 dB, slightly higher than 18.50 dB for the proposed method and 16.29 dB for GFANC.

These results suggest that the proposed E2E-CFG is more advantageous on unseen real-noise conditions, whereas FxNLMS remains competitive on several synthetic band-limited noises with relatively regular spectral structure.

# 4.2. Time-domain performance

Figure 2 compares the proposed E2E-CFG with GFANC and FxNLMS in both waveform and averaged time-domain views. The waveform comparison shows that both learning-based methods

Table 1: Noise reduction (NR) results in dB on unseen real and synthetic noises. All tested real noises and tested synthetic noises are reported. The best result in each row is shown in bold. For each test noise, the controller is run for 5 s and the NR is computed over the last 1 s.   

<table><tr><td>Category</td><td>Noise</td><td>GFANC</td><td>E2E-CFG</td><td>FxNLMS</td></tr><tr><td>Real</td><td>Aircraft</td><td>15.88</td><td>17.83</td><td>9.17</td></tr><tr><td>Real</td><td>Compressor</td><td>21.96</td><td>19.88</td><td>14.78</td></tr><tr><td>Real</td><td>Genset</td><td>12.32</td><td>17.03</td><td>9.01</td></tr><tr><td>Real</td><td>Handheld drill</td><td>20.65</td><td>22.83</td><td>16.96</td></tr><tr><td>Real</td><td>Large SUV pass-by</td><td>14.84</td><td>17.77</td><td>9.70</td></tr><tr><td>Real</td><td>Mix aircraft traffic</td><td>13.03</td><td>16.67</td><td>8.40</td></tr><tr><td>Real</td><td>Motorbike</td><td>21.28</td><td>17.94</td><td>10.02</td></tr><tr><td>Real</td><td>Traffic</td><td>13.09</td><td>16.90</td><td>10.96</td></tr><tr><td colspan="2">Real noise average</td><td>16.63</td><td>18.36</td><td>11.13</td></tr><tr><td>Synthetic</td><td>20–490 Hz</td><td>21.24</td><td>19.35</td><td>21.15</td></tr><tr><td>Synthetic</td><td>490–960 Hz</td><td>13.07</td><td>15.32</td><td>21.50</td></tr><tr><td>Synthetic</td><td>20–960 Hz</td><td>16.23</td><td>20.29</td><td>12.43</td></tr><tr><td>Synthetic</td><td>1430–1900 Hz</td><td>14.63</td><td>19.02</td><td>21.14</td></tr><tr><td colspan="2">Synthetic noise average</td><td>16.29</td><td>18.50</td><td>19.06</td></tr></table>

![](figures/aa30efd68a5612871ddb8641fd02b433170ccec09ea12c502a3bc52e120ad0a5.jpg)

![](figures/8944e58a0e1aab4d2f229b781f376cca0f9a61b3d497e0a0e2bfdb21276dd083.jpg)  
Figure 2: Comparison of the proposed E2E-CFG with GFANC and FxNLMS. The two panels show the waveform-level residual signals and the averaged noise reduction level in each second, respectively.

suppress the disturbance more effectively than FxNLMS under the tested case, while the proposed E2E-CFG generally yields lower residual magnitude than GFANC. The averaged noise reduction curve further shows that the proposed method achieves consistently higher noise reduction over most time intervals.

Figure 3 further illustrates the behavior of different methods when the noise type changes over time. The proposed E2E-CFG maintains lower NMSE than both GFANC and FxNLMS across most segments, and its advantage remains visible after abrupt switches between different real-noise conditions.

![](figures/ebf4d3b4f7e0a3c59e5367f7e4e2790023419cac15f31b7c6d61bd9f3ed48c1e.jpg)  
Figure 3: Time-varying NMSE curves under sequential noise-type changes. The test signal contains several real-noise segments with abrupt transitions, including aircraft, large SUV pass-by, genset, and handheld drill.

# 5. DISCUSSION

# 5.1. Real-noise robustness

An important observation from Table 1 is that the proposed method shows its clearest advantage on the real-noise set. In terms of average NR, E2E-CFG achieves 18.36 dB, which is higher than both GFANC and FxNLMS. By contrast, on the synthetic band-limited noises, the three methods are more competitive and FxNLMS achieves the highest average NR. This suggests that the main advantage of the proposed method lies not in uniformly outperforming all baselines on every test case, but in handling unseen real-world noises with stronger nonstationarity and more complex temporal variation.

This observation is also consistent with Fig. 3. When the noise type changes over time, the proposed E2E-CFG maintains lower NMSE than both GFANC and FxNLMS across most segments, and its advantage remains visible after abrupt switches between different real-noise conditions. A possible reason is that the proposed method combines Transformer-based sequence modeling with direct control-filter generation. The Transformer-based co-processor can exploit longer-range temporal dependencies within each buffered frame, while the direct prediction of the full controlfilter coefficients avoids the intermediate restriction introduced by sub-filter decomposition and recombination. Together, these two design choices appear to be more beneficial for real-world nonstationary noises than for relatively regular synthetic band-limited test cases.

# 5.2. Model complexity

The stronger real-noise performance of the proposed E2E-CFG is accompanied by increased model complexity. Compared with GFANC, the proposed model has a substantially larger parameter count and storage footprint, increasing from about 0.21M to 1.20M trainable parameters and from 876.7 KB to 5.48 MB in model storage. By contrast, the increase in computational cost per frame is more moderate, with the floating-point operations (FLOPs) rising from $3 8 5 . 9 \mathrm { ~ M ~ }$ to $7 8 2 . 5 \mathrm { ~ M ~ }$ . A further breakdown shows that most of the additional computation is introduced by the attention module.

Therefore, the proposed method should be viewed as a performance–complexity trade-off. In the present experiments, the added complexity is associated with stronger results on the real-noise set and more stable behavior under noise-type changes, as shown in Fig. 3. Future work may reduce this complexity through lightweight model design or more efficient sequence modeling architectures [26], while preserving the advantage of direct control-filter generation under complex real-noise conditions.

# 6. CONCLUSION

This paper presented a Transformer-based End-to-End Control-Filter Generation (E2E-CFG) framework for active noise control. Compared with previous GFANC approaches, the proposed

method employs a Transformer-based co-processor for control-filter generation and directly predicts the final control-filter coefficients, without relying on sub-filter decomposition and recombination. This design enables end-to-end unsupervised training that is directly aligned with the physical objective of residual-noise reduction.

Experimental results on unseen real and synthetic noises showed that the proposed method achieved the strongest average performance on the real-noise set among the tested methods. Together with its more stable behavior under noise-type changes, these results suggest that combining Transformer-based sequence modeling with direct control-filter generation is a promising direction for active noise control under more realistic and time-varying noise conditions.

One limitation of the present work is that the proposed model is developed and evaluated under a fixed acoustic path setting. When the system is transferred to a different acoustic environment, the network generally needs to be retrained. Extending the framework to more diverse acoustic environments therefore remains an important direction for future study. Future work will also explore more efficient model designs.

# REFERENCES

1. J. C. Burgess. Active adaptive sound control in a duct: A computer simulation. The Journal of the Acoustical Society of America, 70(3):715–726, 1981.   
2. P. A. Nelson and S. J. Elliott. Active Control of Sound. Academic Press, London, 1992.   
3. Ziyi Yang, Shuping Wang, Jiancheng Tao, and Xiaojun Qiu. Active control of sound transmission through a floor-level slit. The Journal of the Acoustical Society of America, 154(5):2746–2756, 2023.   
4. Sen M. Kuo and Dennis R. Morgan. Active noise control: A tutorial review. Proceedings of the IEEE, 87(6):943–973, 1999.   
5. Junwei Ji, Dongyuan Shi, and Woon-Seng Gan. Mixed-gradients distributed filtered reference least mean square algorithm–a robust distributed multichannel active noise control algorithm. IEEE Transactions on Audio, Speech and Language Processing, 2025.   
6. Yoshinobu Kajikawa, Woon-Seng Gan, and Sen M. Kuo. Recent advances on active noise control: Open issues and innovative applications. APSIPA Transactions on Signal and Information Processing, 1:e3, 2012.   
7. Tianyou Li, Sipei Zhao, Li Rao, Haishan Zou, Kai Chen, Jing Lu, and Ian S Burnett. Experimental study of a distributed active noise control system with multi-device nodes based on augmented diffusion strategy. The Journal of the Acoustical Society of America, 156(5):3246– 3259, 2024.   
8. Stephen J. Elliott. Signal Processing for Active Control. Academic Press, London, 2001.   
9. Yurii Iotov, Sidsel Marie Nørholm, Valiantsin Belyi, Mads Dyrholm, and Mads Græsbøll Christensen. Computationally efficient fixed-filter ANC for speech based on long-term prediction for headphone applications. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pages 906–910, 2022.   
10. Yurii Iotov, Sidsel Marie Nørholm, Valiantsin Belyi, and Mads Græsbøll Christensen. Nonstationary prediction for addressing the non-causality problem in fixed-filter ANC headphones for speech reduction. In Proc. European Signal Processing Conference (EUSIPCO), pages 1008– 1012, 2023.   
11. Xiaoyi Shen, Dongyuan Shi, Woon-Seng Gan, and Santi Peksi. Adaptive-gain algorithm on the fixed filters applied for active noise control headphone. Mechanical Systems and Signal Processing, 169:108641, 2022.   
12. Dongyuan Shi, Woon-Seng Gan, Bhan Lam, and Shulin Wen. Feedforward selective fixed-filter active noise control: Algorithm and implementation. IEEE/ACM Transactions on Audio, Speech,

and Language Processing, 28:1479–1492, 2020.   
13. Dongyuan Shi, Bhan Lam, Kenneth Ooi, Xiaoyi Shen, and Woon-Seng Gan. Selective fixedfilter active noise control based on convolutional neural network. Signal Processing, 190:108317, 2022.   
14. Zhengding Luo, Dongyuan Shi, and Woon-Seng Gan. A hybrid SFANC-FxNLMS algorithm for active noise control based on deep learning. IEEE Signal Processing Letters, 29:1102–1106, 2022.   
15. Zhengding Luo, Dongyuan Shi, Woon-Seng Gan, and Qirui Huang. Delayless generative fixedfilter active noise control based on deep learning and Bayesian filter. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 32:1048–1060, 2024.   
16. Zhengding Luo, Dongyuan Shi, Xiaoyi Shen, Junwei Ji, and Woon-Seng Gan. GFANC-Kalman: Generative fixed-filter active noise control with CNN-Kalman filtering. IEEE Signal Processing Letters, 31:276–280, 2024.   
17. Zhengding Luo, Dongyuan Shi, Xiaoyi Shen, and Woon-Seng Gan. Unsupervised learning based end-to-end delayless generative fixed-filter active noise control. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pages 1041–1045, 2024.   
18. Hao Zhang and DeLiang Wang. Deep ANC: A deep learning approach to active noise control. Neural Networks, 141:1–10, 2021.   
19. Hao Zhang, Ashutosh Pandey, and DeLiang Wang. Low-latency active noise control using attentive recurrent network. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 31:1114–1123, 2023.   
20. Lu Bai, Siyuan Lian, Mengtong Li, Yiming He, Li Rao, Xiaofeng Zeng, Ruquan Sun, Kai Chen, and Jing Lu. Wavenet-volterra neural network for active noise control: A fully causal approach. Mechanical Systems and Signal Processing, 224:111956, 2025.   
21. Boxiang Wang, Dongyuan Shi, Zhengding Luo, Xiaoyi Shen, Junwei Ji, and Woon-Seng Gan. Transferable selective virtual sensing active noise control technique based on metric learning. In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pages 1–5. IEEE, 2025.   
22. Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Advances in Neural Information Processing Systems (NeurIPS), volume 30, 2017.   
23. Anmol Gulati, James Qin, Chung-Cheng Chiu, Niki Parmar, Yu Zhang, Jiahui Yu, Wei Han, Shibo Wang, Zhengdong Zhang, Yonghui Wu, and Ruoming Pang. Conformer: Convolutionaugmented Transformer for Speech Recognition. In Proc. Interspeech, pages 5036–5040, 2020.   
24. Cem Subakan Subakan, Mirco Ravanelli, Samuele Cornell, Mirko Bronzi, and Jianyuan Zhong. Attention is all you need in speech separation. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pages 21–25, 2021.   
25. Zhengding Luo, Junwei Ji, Boxiang Wang, Dongyuan Shi, Haozhe Ma, and Woon-Seng Gan. Deep learning-based generative fixed-filter active noise control: Transferability and implementation. Mechanical Systems and Signal Processing, 238:113207, 2025.   
26. Albert Gu and Tri Dao. Mamba: Linear-time sequence modeling with selective state spaces. arXiv preprint arXiv:2312.00752, 2023.
