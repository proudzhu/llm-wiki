###### Abstract

Recent studies focus on developing efficient systems for acoustic scene classification (ASC) using convolutional neural networks (CNNs), which typically consist of consecutive kernels. This paper highlights the benefits of using separate kernels as a more powerful and efficient design approach in ASC tasks. Inspired by the time-frequency nature of audio signals, we propose TF-SepNet, a CNN architecture that separates the feature processing along the time and frequency dimensions. Features resulted from the separate paths are then merged by channels and directly forwarded to the classifier. Instead of the conventional two dimensional (2D) kernel, TF-SepNet incorporates one dimensional (1D) kernels to reduce the computational costs. Experiments have been conducted using the TAU Urban Acoustic Scene 2022 Mobile development dataset. The results show that TF-SepNet outperforms similar state-of-the-arts that use consecutive kernels. A further investigation reveals that the separate kernels lead to a larger effective receptive field (ERF), which enables TF-SepNet to capture more time-frequency features.

## 1 Introduction

Acoustic scene classification (ASC) [^1] is a basic audio processing task that identifies and classifies audio signals into predefined environmental sound scenes such as airports, parks and urban streets. ASC systems usually require a delicate balance between accuracy and computational efficiency, especially when aiming for real-time processing and deployment on resource-constrained devices [^2].

![Refer to caption](figures/x1.png)

Fig. 1: Simplified diagrams of two 1D-kernel-based design approaches in CNNs. x 𝑥 italic\_x denotes the input features.

In response to the demand for efficient ASC systems, researchers predominantly focus on harnessing the power of convolutional neural networks (CNNs) [^3]. Traditional approaches develop CNN-based ASC systems by stacking multiple two-dimensional (2D) kernels [^2] [^4] [^5], while recent studies [^6] [^7] [^8] [^9] have explored the use of one-dimensional (1D) kernel as a potential alternative. The 1D kernel is initially introduced to address the overfitting problem in ASC tasks [^6], which uses two consecutive 1D kernels with size of $k\times 1$ and $1\times k$ as depicted in (a) of Fig. 1. It is worth noting that the number of parameters of two 1D ($k\times 1$ and $1\times k$) kernels is less than that of a 2D $k\times k$ kernel. Therefore, the consecutive 1D kernels are then employed by subsequent studies [^7] [^8] [^9] for the design of efficient ASC models.

![Refer to caption](figures/x2.png)

Fig. 2: Left: Visualization of the Time-Frequency Separate Convolutions (TF-SepConvs) module. Right: Transformation of features maps. DWConv represents the depthwise convolution and PWConv denotes the pointwise convolution. Freq/Temp prefix denotes the 1D operation on the frequential or temporal axis. Shuffle indicates the channel shuffle unit 10. The dashed line or box means corresponding operation only exists when the channel number changes. The input feature x 𝑥 italic\_x is in ℝ C × F T superscript 𝐶 𝐹 𝑇 \\mathbb{R}^{C\\times F\\times T} blackboard\_R start\_POSTSUPERSCRIPT italic\_C × italic\_F × italic\_T end\_POSTSUPERSCRIPT, where, C,F,T italic\_C, italic\_F, italic\_T respectively denotes channel, frequency and time dimensions.

The inspiration behind this paper stems from the time-frequency nature of audio signals. A recent work [^11] introduces Harmonic-Percussive Source Separation (HPSS) to disentangle the time and frequency information from the audio spectrograms, which effectively helps CNNs to learn crucial time–frequency features. However, the additional HPSS preprocessing requires considerable computational cost. Instead of appending a preprocessing component, we apply the principle of disentanglement to design a novel CNN architecture, Time-Frequency Separate Network (TF-SepNet). Specifically, our proposed network incorporates two independent paths for extracting features along the time and frequency dimensions. As illustrated in (b) of Fig. 1, the $k\times 1$ kernel is responsible for extracting frequency features, while the $1\times k$ kernel focuses on temporal features. The resulted features are then concatenated in the channel dimension and directly forwarded to the classifier. Our network generally adheres to the macro architecture of BC-ResNet [^7], with the integration of depthwise separable convolution [^9] and broadcasting operation [^7] to further reduce the model complexity.

To evaluate the effectiveness of TF-SepNet, experiments were conducted using the TAU Urban Acoustic Scene 2022 Mobile development dataset [^12], a benchmark widely used in the ASC research community. The results reveal that TF-SepNet gets higher accuracy than similar approaches of consecutive kernels [^7] [^8] while exhibiting lower computational complexity. To examine the rationale behind the improvements observed in TF-SepNet, we conduct an in-depth analysis of Effective Receptive Fields (ERF) [^13] for the models being compared. The ERF refers to the region within input features that a particular neuron is sensitive to. Achieving a larger receptive field typically involves the adjustment of hyperparameters in CNNs such as kernel size and down-sampling layers [^4]. Our investigation reveals that the design of separate kernels in TF-SepNet results in a notably larger ERF compared to the approaches that use consecutive kernels. We believe the larger ERF of TF-SepNet substantially improves the model’s capacity to capture vital time-frequency features within acoustic scene sounds.

## 2 Proposed Method

### 2.1 Time-Frequency Separate Convolutions

Inspired by the time-frequency attention mechanism [^11], our study introduces a novel 1D-kernel-based module, Time-Frequency Separate Convolutions (TF-SepConvs), for separating the processing of feature maps in CNNs. Different from the approaches presented in [^7] [^8] [^9], the 1D kernels in TF-SepConvs independently deal with two halves of feature maps so as to capture distinct information in the time and frequency dimensions. The consistency of channel numbers is ensured by the division and subsequent concatenation of feature maps in the channel dimension. In addition, depthwise separable convolution [^9] and broadcasting operation [^7] are integrated into TF-SepConvs for further reducing the parameters and computational overheads. To offer a comprehensive understanding of the structure of TF-SepConvs, we provide a detailed explanation below.

As illustrated in Fig. 2, TF-SepConvs begin with a transition layer, consisting of a $1\times 1$ convolution. The transition layer serves the purpose of expanding or shrinking the number of channels from $C$ to $C^{\prime}$, $x\in\mathbb{R}^{C\times F\times T}\rightarrow\mathbb{R}^{C^{\prime}\times F%
\times T}$. After the transition layer, a shuffle unit [^10] is introduced to establish connections of the feature maps between channels. Following the shuffle unit, the feature maps are evenly divided into two halves by channels: $x^{(f)},x^{(t)}\in\mathbb{R}^{C^{\prime}/2\times F\times T}$. $x^{(f)}$ and $x^{(t)}$ are then separately processed by operations in the frequential path and temporal path. As shown in equation (1) (2), these two paths consist of a ($3\times 1$ or $1\times 3$) depthwise convolution denoted as $d_{3\times 1}$ or $d_{1\times 3}$, an (frequency or time) average pool and a $1\times 1$ pointwise convolution denoted as $p_{1\times 1}$, where $v^{(f)}\in\mathbb{R}^{C^{\prime}/2\times 1\times T}$ and $v^{(t)}\in\mathbb{R}^{C^{\prime}/2\times F\times 1}$. All convolutions mentioned above are followed by batch normalization (BN) and relu activation (ReLu).

$$
v^{(f)}=p_{1\times 1}(\frac{1}{F}\sum\nolimits_{i=1}^{F}d_{3\times 1}(x_{ij}^{%
(f)}))
$$
 
$$
v^{(t)}=p_{1\times 1}(\frac{1}{T}\sum\nolimits_{j=1}^{T}d_{1\times 3}(x_{ij}^{%
(t)}))
$$

The 1D features $v^{(f)}$ and $v^{(t)}$ are then respectively expanded to 2D shape as shown in equation (3) (4), where $\hat{x}^{(f)},\hat{x}^{(t)}\in\mathbb{R}^{C^{\prime}/2\times F\times T}$. The process of averaging and expanding is known as the broadcasting operation [^7]. The broadcasting operation effectively decreases the size of feature maps for the pointwise convolution $p_{1\times 1}$, consequently resulting in a reduction in computational costs.

$$
\hat{x}^{(f)}=\sum\nolimits_{j=1}^{T}(x_{ij}^{(f)}+v_{j}^{(f)})
$$
 
$$
\hat{x}^{(t)}=\sum\nolimits_{i=1}^{F}(x_{ij}^{(t)}+v_{i}^{(t)})
$$

Finally, the feature maps coming from the time and frequency separate paths, $\hat{x}^{(f)}$ and $\hat{x}^{(t)}$, are concatenated together by channels to get the output feature $y$ in $\mathbb{R}^{C^{\prime}\times F\times T}$.

| Output Shape | Architecture | $k$ | $s$ | $p$ |
| --- | --- | --- | --- | --- |
| $1,F,T$ | Input | \- | \- | \- |
| $C/2,F/2,T/2$ | ConvBnRelu | 3 | 2 | 1 |
| $2C,F/4,T/4$ | ConvBnRelu, $g$ = $C/2$ | 3 | 2 | 1 |
| $C,F/4,T/4$ | TF-SepCovs $\times 2$ | \- | \- | \- |
| $C,F/8,T/8$ | MaxPool | 2 | 2 | 0 |
| $1.5C,F/8,T/8$ | TF-SepCovs $\times 2$ | \- | \- | \- |
| $1.5C,F/16,T/16$ | MaxPool | 2 | 2 | 0 |
| $2C,F/16,T/16$ | TF-SepCovs $\times 2$ | \- | \- | \- |
| $2.5C,F/16,T/16$ | TF-SepCovs $\times 3$ | \- | \- | \- |
| $10,F/16,T/16$ | Conv | 1 | 1 | 0 |
| $10,1,1$ | Avgpool | \- | \- | \- |

Table 1: Architecture of TF-SepNet. $C$, $F$, and $T$ respectively represent channels, frequency bins, and time clips of feature maps. $k$, $s$, $p$ and $g$ separately denote kernel size, stride, padding and group.

### 2.2 Network Architecture

Time-Frequency Separate Network (TF-SepNet) is a deep CNN architecture tailored specifically for ASC tasks, which aims at a balance between model complexity and classification accuracy. The model architecture is depicted in Table 1, and a detailed explanation is provided below.

The input spectrogram is in $\mathbb{R}^{1\times F\times T}$. The TF-SepNet starts from two $3\times 3$ convolution kernels with 2 strides for initial downsampling. After that, a total of 9 TF-SepConvs described in Section 2.1 are followed. In addition, two $2\times 2$ maxpooling layers with 2 strides are inserted between the TF-SepConvs for intermediate downsampling, enabling the network to capture more high-level representations. The last phase involves a $1\times 1$ convolutional layer followed by a global average pooling, allowing the model to obtain multi-class probabilities as the output. Moreover, adaptive residual normalization [^14] is also plugged in after the initial downsampling block and after every block of TF-SepConvs.

The channel width of TF-SepNet, denoted as $\tau$, serves as a hyperparameter to adjust the complexity of the model [^7]. By tuning $\tau$, TF-SepNet- $\tau$ can be customized to meet specific needs, ranging from resource-constrained environments to high-performance computing systems.

| Model | Acc/ $\%$ | MACs/M | Param/K |
| --- | --- | --- | --- |
| DCASE Baseline [^2] | 42.9 | 29.2 | 46.5 |
| BC-ResNet-40 [^7] | 57.1 | 17.2 | 88.1 |
| BC-Res2Net-40 [^8] | 59.1 | 17.2 | 85.8 |
| TF-SepNet-40 (ours) | 60.0 | 7.0 | 53.4 |
| BC-ResNet-80 [^7] | 58.4 | 45.8 | 315.0 |
| BC-Res2Net-80 [^8] | 59.6 | 42.7 | 307.0 |
| TF-SepNet-80 (ours) | 61.6 | 24.2 | 196.7 |

Table 2: Evaluation results on the test set of TAU Urban Acoustic Scene 2022 Mobile development dataset [^12]. Acc denotes the top-1 accuracy on test set. MACs (Multiply-Accumulate Operations) indicates the computational costs per inference. Param represents the number of parameters.

## 3 Experiments

### 3.1 Dataset and Preprocessing

The experiments are conducted with the TAU Urban Acoustic Scene 2022 Mobile development dataset [^12], which is a widely recognized benchmark for the task of low-complexity ASC. We follow the official training/test split of 7:3. The recordings in this dataset were captured by various mobile devices across multiple cities worldwide, introducing challenges to the generalization ability of ASC model.

All audio segments are down-sampled to 32kHz [^15]. Short-Time Fourier Transform (STFT) is employed to extract time-frequency representations, with a window size of 3072 and a hop size of 500. Following the STFT, a Mel-scaled filter bank with 256 frequency bins and 4096 FFT is applied to transform the spectrograms into a Log-Mel spectrograms.

### 3.2 Training Setup

The proposed model is trained for 100 epochs using the Adam optimizer with default settings in the Pytorch environment. The batch size is set to 32. A warmup [^16] strategy is introduced for fast convergence and stable training. The learning rate is linearly increased from 0 to 0.01 over the first five epochs, subsequently decayed to 0 for the remaining epochs using cosine annealing [^17]. In addition, Mixup [^18] and Freq-MixStyle [^15] are introduced to improve the overfitting problem. The $\alpha$ of Mixup is set to 0.3 and the $\alpha$ and $p$ of Freq-MixStyle are respectively set to 0.3 and 0.7.

![Refer to caption](figures/erf.png)

Fig. 3: Visualization of Effective Receptive Fields (ERF). The color intensity at each point signifies the contribution score of the corresponding pixel in the input image to the central point of the feature map generated by the final layer. A broader and darker region indicates a larger ERF.

### 3.3 Results

Two consecutive-kernels-based CNNs, BC-ResNet [^7] and BC-Res2Net [^8], are chosen for comparison with TF-SepNet due to the same scaling mechanism and similar architectures. Notably, BC-ResNet ranked the first in the DCASE2021 Challenge and BC-Res2Net won the second place in 2022. As depicted in Table 2, with the channel width $\tau$ being set to 40, TF-SepNet-40 achieves the highest accuracy with 59 $\%$ lower computational costs than BC-ResNet-40 and BC-Res2Net-40. Moreover, the parameter number of TF-SepNet-40 is 39 $\%$ smaller than BC-ResNet-40 and 38 $\%$ less than BC-Res2Net-40. Even with $\tau$ set to 80, TF-SepNet still shows superiority on the performance and efficiency.

The underlying reason for such improvements observed in TF-SepNet is further investigated with the Effective Receptive Field (ERF) [^13]. Following [^19], we conducted visualizations and statistical analyses of ERF for BC-ResNet-40, BC-Res2Net-40 and TF-SepNet-40. As illustrated in Fig. 3, BC-ResNet and BC-Res2Net show concentrated high-intensity regions around the central point, indicating limited ERF coverage for outer points. In contrast, TF-SepNet exhibited more uniformly distributed high-intensity regions along both the time and frequency dimensions. Table 3 further corroborates these findings, revealing that TF-SepNet consistently achieved larger ERFs compared to BC-ResNet and BC-Res2Net, irrespective of whether $t$ was set to 20 $\%$, 30 $\%$, or 50 $\%$. With a larger ERF, TF-SepNet is able to capture more time-frequency features from the input audio spectrograms, leading to an improved performance.

### 3.4 Ablation Study

Table 4 shows the impacts of key components within the TF-SepNet architecture. The shuffle unit slightly enhances the accuracy without introducing additional parameters or computation by establishing information flow between channel groups. ‘w/o freq/temp path’ means the channels are not split into two halves in the TF-SepConvs module and the entire frequential or temporal path described in Equation (1) or (2) is removed. Specially, due to the asymmetrical shape of input spectrogram, with $F$ =256 and $T$ =64 in our experiments, the frequency and time path inherently incur different computational costs. The accuracy witnesses drastic drops and the system complexity increases regardless of whether the frequential or temporal path is eliminated. The findings underscore the vital contribution of combining information flows in both the time and frequency domains to enhance model performance for ASC. Lastly, the adaptive residual normalization (AdaResNorm) also plays an crucial role, giving rise to 1.5 $\%$ accuracy gain by introducing only 2 $\%$ parameters.

<table><thead><tr><th rowspan="2">Model</th><th><math><semantics><mrow><mi>t</mi> <mo>=</mo> <mrow><mn>20</mn> <mo>%</mo></mrow></mrow> <apply><ci>𝑡</ci> <apply><csymbol>percent</csymbol> <cn>20</cn></apply></apply> <annotation>t=20\%</annotation> <annotation>italic_t = 20 %</annotation></semantics></math></th><th><math><semantics><mrow><mi>t</mi> <mo>=</mo> <mrow><mn>30</mn> <mo>%</mo></mrow></mrow> <apply><ci>𝑡</ci> <apply><csymbol>percent</csymbol> <cn>30</cn></apply></apply> <annotation>t=30\%</annotation> <annotation>italic_t = 30 %</annotation></semantics></math></th><th><math><semantics><mrow><mi>t</mi> <mo>=</mo> <mrow><mn>50</mn> <mo>%</mo></mrow></mrow> <apply><ci>𝑡</ci> <apply><csymbol>percent</csymbol> <cn>50</cn></apply></apply> <annotation>t=50\%</annotation> <annotation>italic_t = 50 %</annotation></semantics></math></th></tr><tr><th><math><semantics><mi>r</mi> <ci>𝑟</ci> <annotation>r</annotation> <annotation>italic_r</annotation></semantics></math></th><th><math><semantics><mi>r</mi> <ci>𝑟</ci> <annotation>r</annotation> <annotation>italic_r</annotation></semantics></math></th><th><math><semantics><mi>r</mi> <ci>𝑟</ci> <annotation>r</annotation> <annotation>italic_r</annotation></semantics></math></th></tr></thead><tbody><tr><th>BC-ResNet-40 <sup><a href="#fn:7">7</a></sup></th><td>9.6 <math><semantics><mo>%</mo> <csymbol>percent</csymbol> <annotation>\%</annotation> <annotation>%</annotation></semantics></math></td><td>17.3 <math><semantics><mo>%</mo> <csymbol>percent</csymbol> <annotation>\%</annotation> <annotation>%</annotation></semantics></math></td><td>39.3 <math><semantics><mo>%</mo> <csymbol>percent</csymbol> <annotation>\%</annotation> <annotation>%</annotation></semantics></math></td></tr><tr><th>BC-Res2Net-40 <sup><a href="#fn:8">8</a></sup></th><td>9.9 <math><semantics><mo>%</mo> <csymbol>percent</csymbol> <annotation>\%</annotation> <annotation>%</annotation></semantics></math></td><td>18.9 <math><semantics><mo>%</mo> <csymbol>percent</csymbol> <annotation>\%</annotation> <annotation>%</annotation></semantics></math></td><td>39.8 <math><semantics><mo>%</mo> <csymbol>percent</csymbol> <annotation>\%</annotation> <annotation>%</annotation></semantics></math></td></tr><tr><th>TF-SepNet-40 (ours)</th><td>13.9 <math><semantics><mo>%</mo> <csymbol>percent</csymbol> <annotation>\%</annotation> <annotation>%</annotation></semantics></math></td><td>22.5 <math><semantics><mo>%</mo> <csymbol>percent</csymbol> <annotation>\%</annotation> <annotation>%</annotation></semantics></math></td><td>43.8 <math><semantics><mo>%</mo> <csymbol>percent</csymbol> <annotation>\%</annotation> <annotation>%</annotation></semantics></math></td></tr></tbody></table>

Table 3: Statistical Analysis of ERF. The threshold ($t$) denotes the selected proportion of all pixel contributions. The high-contribution area ratio ($r$) is the percentage of area around the central point contributing to corresponding $t$ of all pixel contributions. A larger $r$ indicates a more uniform distribution of pixel contributions, in other words, a larger ERF.

| Model | Acc/ $\%$ | MACs/M | Param/K |
| --- | --- | --- | --- |
| TF-SepNet-40 | 60.0 | 7.03 | 53.4 |
| w/o shuffle | 59.5 | 7.03 | 53.4 |
| w/o freq path | 56.7 | 7.80 | 80.0 |
| w/o temp path | 57.5 | 6.96 | 80.0 |
| w/o AdaResNorm | 58.5 | 7.03 | 52.3 |

Table 4: Ablation Study. ‘w/o’ means without corresponding component from TF-SepNet-40.

## 4 Conclusion

This paper addresses the crucial challenge of achieving low system complexity in ASC tasks by introducing TF-SepNet, a novel CNN architecture that leverages separate 1D kernels to independently capture features of audio spectrograms in the time and frequency dimensions. The experimental results show that TF-SepNet achieves better accuracy with lower complexity than the state-of-the-arts that employ consecutive kernels. A study of effective receptive field (ERF) further demonstrates the benefits of separate kernels in the ASC task. For future works, we believe the separate kernels present a huge potential in other audio pattern recognition tasks.

## 5 Acknowledgement

This project is supported partly by the National Natural Science Foundation of China (No: 62001038) and Gusu Innovation and Entrepreneurship Leading Talents Programme (No: ZXL2022472). We also thank Dr. Yin Cao and Dr. Jimin Xiao for their valuable advice on this paper.

[^1]: Daniele Barchiesi, Dimitrios Giannoulis, Dan Stowell, and Mark D Plumbley, “Acoustic scene classification: Classifying environments from the sounds they produce,” IEEE Signal Processing Magazine, vol. 32, no. 3, 2015.

[^2]: Irene Martín-Morató, Francesco Paissan, Alberto Ancilotto, Toni Heittola, Annamaria Mesaros, Elisabetta Farella, Alessio Brutti, and Tuomas Virtanen, “Low-complexity acoustic scene classification in DCASE 2022 Challenge,” in Proceedings of the Detection and Classification of Acoustic Scenes and Events (DCASE) Workshop, 2022.

[^3]: Jakob Abeßer, “A review of deep learning based methods for acoustic scene classification,” Applied Sciences, vol. 10, no. 6, 2020.

[^4]: Khaled Koutini, Hamid Eghbal-zadeh, and Gerhard Widmer, “Receptive-field-regularized CNN variants for acoustic scene classification,” in Proceedings of the Detection and Classification of Acoustic Scenes and Events (DCASE) Workshop, 2019, pp. 124–128.

[^5]: Hu Hu, Chao-Han Huck Yang, Xianjun Xia, Xue Bai, Xin Tang, Yajian Wang, Shutong Niu, Li Chai, Juanjuan Li, et al., “A two-stage approach to device-robust acoustic scene classification,” in Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2021, pp. 845–849.

[^6]: Janghoon Cho, Sungrack Yun, Hyoungwoo Park, Jungyun Eum, and Kyuwoong Hwang, “Acoustic scene classification based on a large-margin factorized CNN,” in Proceedings of the Detection and Classification of Acoustic Scenes and Events (DCASE) Workshop, 2019, pp. 45–49.

[^7]: Byeonggeun Kim, Simyung Chang, Jinkyu Lee, and Dooyong Sung, “Broadcasted Residual Learning for Efficient Keyword Spotting,” in Proceedings of the Conference of the International Speech Communication Association (INTERSPEECH). ISCA, 2021, pp. 4538–4542.

[^8]: Joo-Hyun Lee, Jeong-Hwan Choi, Pil Moo Byun, and Joon-Hyuk Chang, “Multi-scale architecture and device-aware data-random-drop based fine-tuning method for acoustic scene classification,” in Proceedings of the Detection and Classification of Acoustic Scenes and Events (DCASE) Workshop, 2022.

[^9]: Duc H Phan and Douglas L Jones, “Low-complexity acoustic scene classification using time frequency separable convolution,” Electronics, vol. 11, no. 17, 2022.

[^10]: Xiangyu Zhang, Xinyu Zhou, Mengxiao Lin, and Jian Sun, “ShuffleNet: An extremely efficient convolutional neural network for mobile devices,” in Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 6848–6856.

[^11]: Wenjie Mu, Bo Yin, Xianqing Huang, Jiali Xu, and Zehua Du, “Environmental sound classification using temporal-frequency attention based convolutional neural network,” Scientific Reports, vol. 11, no. 1, 2021.

[^12]: Annamaria Mesaros, Toni Heittola, and Tuomas Virtanen, “A multi-device dataset for urban acoustic scene classification,” in Proceedings of the Detection and Classification of Acoustic Scenes and Events (DCASE) Workshop, 2018, pp. 9–13.

[^13]: Wenjie Luo, Yujia Li, Raquel Urtasun, and Richard Zemel, “Understanding the effective receptive field in deep convolutional neural networks,” Advances in Neural Information Processing Systems, vol. 29, 2016.

[^14]: Yiqiang Cai, Minyu Lin, Chenyang Zhu, Shengchen Li, and Xi Shao, “DCASE2023 task1 submission: Device simulation and time-frequency separable convolution for acoustic scene classification,” Tech. Rep., Detection and Classification of Acoustic Scenes and Events (DCASE) Challenge, 2023.

[^15]: Florian Schmid, Shahed Masoudian, Khaled Koutini, and Gerhard Widmer, “CP-JKU submission to DCASE22: Distilling knowledge for low-complexity convolutional neural networks from a patchout audio transformer,” Tech. Rep., Detection and Classification of Acoustic Scenes and Events (DCASE) Challenge, 2022.

[^16]: Priya Goyal, Piotr Dollár, Ross Girshick, Pieter Noordhuis, Lukasz Wesolowski, Aapo Kyrola, Andrew Tulloch, Yangqing Jia, and Kaiming He, “Accurate, large minibatch SGD: Training imagenet in 1 hour,” arXiv preprint arXiv:1706.02677, 2017.

[^17]: Ilya Loshchilov and Frank Hutter, “SGDR: Stochastic gradient descent with warm restarts,” in Proceedings of the International Conference on Learning Representations (ICLR), 2017.

[^18]: Hongyi Zhang, Moustapha Cisse, Yann N. Dauphin, and David Lopez-Paz, “mixup: Beyond empirical risk minimization,” in Proceedings of the International Conference on Learning Representations (ICLR), 2018.

[^19]: Xiaohan Ding, Xiangyu Zhang, Jungong Han, and Guiguang Ding, “Scaling up your kernels to 31x31: Revisiting large kernel design in CNNs,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2022, pp. 11963–11975.