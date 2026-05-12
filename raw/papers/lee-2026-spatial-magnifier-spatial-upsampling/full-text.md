Lee Pandey Parekh Wong Donley Xu Azcarreta

Dongheon    Ashutosh    Sanjeel     
Daniel    Jacob    Buye    Juan <sup>1</sup> Meta Reality Labs Research  
<sup>2</sup> Korea Advanced Institute of Science and Technology (KAIST) [donghen0115@gmail.com, jazcarretao@meta.com](https://arxiv.org/html/2605.04749v2/mailto:donghen0115@gmail.com,%20jazcarretao@meta.com)

###### Abstract

While the spatial directivity of multichannel speech enhancement algorithms improves with the number of microphones, fitting large capture arrays into real-world edge devices is typically limited by physical constraints. To overcome this limitation, we propose Spatial-Magnifier, a neural network designed to generate virtual microphone (VM) signals from a limited set of real microphone (RM) measurements. Moreover, we introduce the Spatial Audio Representation Learning (SARL) framework, which leverages estimated VM signals and features to condition a downstream speech enhancement system. Experimental results demonstrate that the proposed framework outperforms existing spatial upsampling baselines across various speech extraction systems, including end-to-end multichannel speech enhancement and neural beamforming. The proposed method nearly recovers the oracle performance achieved when all microphones are available.

###### keywords:

Spatial upsampling, multichannel speech enhancement, virtual microphone estimation, generative adversarial network <sup>†</sup> <sup>†</sup>

## 1 Introduction

Increasing the spatial diversity of microphone arrays by expanding the physical distance between sensors or adding more capture points can significantly boost the performance of multichannel speech enhancement (MC-SE) algorithms \[benesty2008microphone, VanVeen:1988, wang2020complex\]. However, the spatial capture capabilities of consumer devices such as augmented reality (AR) glasses, earbuds, and hearing aids are strictly limited by physical constraints, preventing the integration of large-scale arrays.

To overcome these physical limitations, recent work has proposed neural network-based virtual microphone estimation (Neural-VME) \[ochiai2021neural, segawa2022neural, segawa2024neural\]. In this context, a Virtual Microphone (VM) is defined as a captured signal that is available during the training phase but is absent during inference. By training a model to estimate these missing signals from a sparse set of Real Microphone (RM) measurements, Neural-VME can effectively increase the array's spatial diversity without requiring additional hardware. Previous studies have successfully applied Neural-VME to source separation by combining the estimated VM signals with RM recordings to control a mask-based beamformer \[ochiai2021neural, segawa2022neural, segawa2024neural\]. Similarly, spatial upsampling has been utilized for Universal Acoustic Vision \[roman2024robust\] to increase the ambisonic order by leveraging super-resolution architectures originally designed for image upscaling \[haris2018deep\].

Despite these advances, there has been no comprehensive study on how to condition downstream speech tasks optimally on interpolated VM signals. We argue that the primary advantage of Neural-VME lies in its ability to decouple spatial representation learning from spectral enhancement. While balancing spectral and spatial information is an intrinsic challenge in MC-SE, estimating VM signals can force the system to learn robust spatial representations that directly benefit downstream MC-SE performance. To maximize this potential, a generic framework applicable to the varied array geometries found in consumer electronics is essential.

Notably, previous speech processing Neural-VME works have repurposed architectures originally designed for standard speech enhancement \[segawa2024neural, wang2024unsupervised, qiu2024transformer\]. However, the distinct nature of spatial upsampling creates a pressing need for specialized models tailored to upsample microphone recordings. To this end, we introduce Spatial-Magnifier, a GAN-based generative network incorporating two efficient modules: a Selection Module capable of isolating the most relevant spatial features, and a Dynamic Channel Allocation (DCA) module that adaptively determines the spatial filters' importance to facilitate efficient information compression.

Furthermore, we propose Spatial Audio Representation Learning (SARL), a framework that integrates Neural-VME to improve both neural beamforming and end-to-end speech enhancement. Unlike traditional virtual microphone-based Beamforming (VM-BF) \[segawa2024neural\], SARL can condition a downstream MC-SE model on both estimated VM signals and learned VM features. This approach enables a task we term virtual microphone-based speech enhancement (VM-SE), which improves end-to-end models directly without requiring a beamforming backend.

Extensive experiments demonstrate that the proposed approach robustly estimates VM signals across various array geometries. This expands upon existing methods that have primarily focused on linear arrays. The Spatial-Magnifier model and SARL framework achieve superior beamforming and speech extraction performance compared to conventional Neural-VME baselines. Furthermore, these performance gains are achieved with lower computational costs compared to existing Neural-VME baselines.

![Figure 1: Architecture of the Spatial-Magnifier generator](figures/fig1-spatial-magnifier.png)

Figure 1: Architecture of the Spatial-Magnifier generator. The network jointly generates VM signals and VM features.

## 2 Proposed method

### 2.1 Mathematical modeling of neural beamforming

MC-SE is the task of estimating a direct-path speech signal $\mathbf{x}_{ref}\in\mathbb{R}^{1\times N}$ given multichannel noisy speech $\mathbf{y}\in\mathbb{R}^{M\times N}$ consisting of $M$ channels and $N$ samples, which can be expressed as

$$
\displaystyle\begin{aligned} \mathbf{y}&=\mathbf{x}+\mathbf{x}_{rev}+\mathbf{n},\end{aligned}
$$

where $\mathbf{x}\in\mathbb{R}^{M\times N}$, $\mathbf{x}_{rev}\in\mathbb{R}^{M\times N}$, and $\mathbf{n}\in\mathbb{R}^{M\times N}$ denote the multichannel waveforms of the direct-path speech, its reverberation, and additive noise, respectively. The target signal $\mathbf{x}_{ref}$ corresponds to a selected reference channel from $\mathbf{x}$.

We utilize a discriminative multichannel neural network to estimate the target signal at the reference microphone:

$$
\displaystyle\hat{\mathbf{x}}^{se}_{ref}=\text{MC-SE}(\mathbf{y}).
$$

In our framework, we leverage the estimated $\hat{\mathbf{x}}^{se}_{ref}$ as an approximation of the target signal to derive adaptive coefficients $\bm{W}\in\mathbb{C}^{M\times T\times F}$ for frequency-domain beamforming:

$$
\displaystyle\hat{\bm{X}}_{ref}^{bf}
$$
 
$$
\displaystyle=\bm{W}^{\mathsf{H}}\bm{Y},
$$

where $\bm{Y}\in\mathbb{C}^{M\times T\times F}$ denotes the STFT of the input signal across $M$ microphones, $T$ frames, and $F$ frequency bins. $(\cdot)^{\mathsf{H}}$ denotes the Hermitian operator. The output $\hat{\bm{X}}_{ref}^{bf}\in\mathbb{C}^{T\times F}$ is the frequency-domain estimated target signal. The weights $\bm{W}$ can be calculated in closed-form using classical beamformers such as the multichannel Wiener filter (MCWF) \[benesty2008microphone\] or the minimum variance distortionless response (MVDR) \[souden2009optimal\]. Linear filtering effectively mitigates non-linear distortions introduced by neural networks, which can be beneficial for multi-stage processing \[pandey2025ultra, wang2022stft, wang2020derev\] and to enhance the performance of ASR applications \[jahn2016\].

### 2.2 Neural-VME for speech enhancement

Neural-VME leverages a neural network to estimate missing Virtual Microphone (VM) signals from a sparse set of Real Microphone (RM) measurements. During training, all microphone signals $\mathbf{y}=[\mathbf{r},\mathbf{v}]$ are available, where $\mathbf{r}\in\mathbb{R}^{M_{r}\times N}$ and $\mathbf{v}\in\mathbb{R}^{M_{v}\times N}$ denote the $M_{r}$ real and $M_{v}$ virtual channels, respectively. Hence, the task of Neural-VME is to produce an estimate $\hat{\mathbf{v}}\in\mathbb{R}^{M_{v}\times N}$ of the VM signals given $\mathbf{r}$:

$$
\hat{\mathbf{v}}=\text{Neural-VME}(\mathbf{r}).
$$

We leverage virtual microphone-based beamforming (VM-BF) \[segawa2024neural\], where the augmented signal $\bar{\mathbf{y}}=[\mathbf{r},\hat{\mathbf{v}}]\in\mathbb{R}^{M\times N}$ (with $M=M_{r}+M_{v}$) is used to calculate the Spatial Covariance Matrices (SCM) for a beamforming back-end \[benesty2008microphone\] to derive the filters $\bm{W}$, which are then applied to $\bar{\bm{Y}}$ following Eq. 3. VM-BF jointly optimizes a multi-task objective for Neural-VME and beamforming, learning how to generate VM signals that aim to increase the numerical rank of the SCM from $M_{r}$ to $M$ for SE.

### 2.3 Spatial-Magnifier model

The proposed Spatial-Magnifier model is a generative adversarial network (GAN) \[goodfellow2014generative\] that consists of convolutions designed to exploit inter-channel relationships. Figure 1 depicts the architecture of the Spatial-Magnifier generator, which is inspired by the deep back-projection network (DBPN) for image super-resolution \[haris2018deep\]. Spatial-Magnifier processes the RM signals $\bm{R}\in\mathbb{C}^{M_{r}\times T\times F}$ in the frequency-domain by treating the microphone indices as the channel dimension and concatenating real and imaginary components. An initial 2D convolution expands the input $2\times M_{r}$ to $D_{1}$ channels. Features then undergo $N_{b}$ stages of alternating up-blocks, down-blocks, and our proposed DCA modules. The DCA module utilizes dynamic convolutions \[chen2020dynamic\] to compute channel-wise attention scores, weighting a pointwise convolution that adaptively reduces dimensionality from $D_{1}$ to $D_{2}$ for efficient information compression.

Previously, up-blocks and down-blocks utilized simple addition and subtraction, applying identical operations across all channels, which limited their flexibility. To address this, we introduce a selection module (SM) that incorporates pointwise convolution followed by Mish activation \[misra2019mish\] to form a gating mechanism \[lee2025deft\] before the addition operation. This approach extracts features channel-wise adaptively, enhancing performance with minimal computational overhead. Furthermore, since conventional DBPN architectures resemble dense blocks, they often incur high computational costs. Given that Neural-VME targets real-world devices, maximizing performance gains while minimizing computational load is essential. For additional efficiency, group convolution is employed in the down-blocks. Finally, we adopt the discriminator from the conformer-based MetricGAN (CMGAN) \[abdulatif2024cmgan\].

![Refer to caption](https://arxiv.org/html/2605.04749v2/figure/training_method.png)

Figure 2: Overall framework of Spatial Audio Representation Learning (SARL): (a) SARL-Signal and (b) SARL-Feature frameworks. Spatial-Magnifier serves as the Neural-VME model, while SARL represents the conditioning method for the MC-SE model.

### 2.4 Spatial Audio Representation Learning

We propose Spatial Audio Representation Learning (SARL) to condition the MC-SE model on the estimated VM signals. As illustrated in Figure 2, SARL encompasses two paradigms: SARL-signal (SARL-S) and SARL-feature (SARL-F). Both strategies aim to optimize the enhanced signal $\hat{\mathbf{x}}^{se}_{ref}$ by augmenting the RM observations with virtual spatial information, a task that we call virtual microphone-based speech enhancement (VM-SE). VM-SE improves end-to-end MC-SE performance without relying on an augmented adaptive beamformer as a back-end. Within the SARL framework, we utilize a pre-trained MC-SE model originally trained with the overall microphone signals $\mathbf{y}$. We then fine-tune this model while training the Neural-VME model from scratch, notably maintaining the same computational cost during inference.

#### 2.4.1 SARL-S: Signal-Level Augmentation

SARL-S is a direct spatial upsampling approach where the Spatial-Magnifier estimates explicit VM signals that are concatenated with the RM signals to form the augmented signal $\bar{\mathbf{y}}=[\mathbf{r},\hat{\mathbf{v}}]$. This augmented signal is then directly processed by an MC-SE model as in Equation 2. By providing raw waveforms, SARL-S allows the downstream model to utilize improved spatial information across the expanded array geometry.

#### 2.4.2 SARL-F: Feature-Level Augmentation

In contrast, SARL-F operates in a latent space to provide robust conditioning. Since common MC-SE models can be decomposed into an encoder-separator-decoder topology \[quan2024spatialnet, luo2019conv, lee2024deftan\], by defining the encoder as $h_{\phi}(\cdot)$, and the separator+decoder modules as $\text{MC-SE}_{\textit{sep.}+\textit{dec.}}(\cdot)$, the enhanced signal is given by:

$$
\displaystyle\hat{\mathbf{x}}^{se_{\bar{\mathbf{y}}}}
$$
 
$$
\displaystyle=\text{MC-SE}_{\textit{sep.}+\textit{dec.}}(h_{\phi}(\mathbf{r})+f_{\hat{\mathbf{v}}}),
$$

where $f_{\hat{\mathbf{v}}}\in\mathbb{R}^{H\times T\times F}$ denotes the estimated VM features by Spatial-Magnifier, where $H$ is the embeddings size. In SARL-F, Spatial-Magnifier estimates representations equivalent to an encoded spatial embedding, which are fused with the encoded RM signals $h_{\phi}(\mathbf{r})\in\mathbb{R}^{H\times T\times F}$ via element-wise addition \[yang2024self, hong2025efficient\]. This latent fusion allows the separator to exploit spatial diversity even when the raw VM waveform reconstruction is challenging, acting as a high-level spatial regularizer.

## 3 Experiments

### 3.1 Datasets

We used the Interspeech 2020 DNS challenge speech and noise corpora \[reddy2020interspeech\] to simulate 50,000, 2,000, and 3,000 clips of 10 s duration for training, validation, and testing, respectively. Spatial data were simulated via Pyroomacoustics \[scheibler2018pyroomacoustics\] using the image source method with an order of six. The six-channel array consisted of a four-channel circular array with a radius of 10 cm and two vertical microphones placed 10 cm above and below the center. The length, width, and height of the room were uniformly distributed within \[3, 10\], \[3, 10\], and \[2, 5\] m, respectively, with an absorption coefficient sampled from the range \[0.1, 0.5\], resulting in reverberation time (RT60) in the range \[0.15, 1.75\] s. The signal-to-noise ratio (SNR) and signal-to-interference ratio (SIR) were sampled within \[$-$ 10, 5\] dB, with sources placed \[0.5, 2.5\] m from the array center. The experiments covered both conventional omnidirectional SE (omni-SE) and Field-of-View SE (FoV-SE) tasks \[xufovnet\]. For FoV-SE, the target was within $\pm 20^{\circ}$ (azimuth and elevation) relative to the front axis. Up to four interfering talkers were placed outside this FoV area. The number of babble talkers and noise ranged from \[0, 10\] for omni-SE and from \[0, 5\] for FoV-SE.

### 3.2 Experimental setup

We computed the short-time Fourier transform (STFT) with a 16 ms square-root Hanning window, an 8 ms hop size, and a 16 kHz sampling rate. Time-varying beamformer weights were computed in a block-wise using a 25-frame window \[wang2022mf\]. For the Spatial-Magnifier, we set $N_{b}=5$ and channel dimensions $[D_{1},\dots,D_{5}]=[128,96,64,48,32]$. The loss function combined time-domain SNR losses for Neural-VME and VM-BF, along with adversarial losses \[kong2020hifi\] for the generator and discriminator with weights of 0.3:0.7:0.01:0.01, respectively. The first RM channel is utilized as the target reference signal. The model was trained using the Adam optimizer with a learning rate of 0.001 for 100 epochs, with a batch size of 64 across 32 H100 GPUs. Performance was evaluated using SI-SDR \[le2019sdr\], SNR, narrowband PESQ \[rix2001perceptual\], and STOI \[taal2010short\].

Table 1: Ablation study on training methods, RM: 2ch, VM: 4ch

<table><tbody><tr><th rowspan="2">Model type</th><th rowspan="2">Training method</th><td colspan="2">Neural-VME</td><td colspan="4">VM-BF</td></tr><tr><td>SI-SDR</td><td>SNR</td><td>SI-SDR</td><td>SNR</td><td>PESQ</td><td>STOI</td></tr><tr><th colspan="2">unprocessed</th><td>-</td><td>-</td><td>-11.0</td><td>-9.97</td><td>1.29</td><td>50.1</td></tr><tr><th colspan="2">SpatialNet + MCWF 2ch</th><td>-</td><td>-</td><td>2.19</td><td>4.57</td><td>1.97</td><td>70.4</td></tr><tr><th rowspan="8">Spatial- Magnifier</th><th>Neural-VME (freeze)</th><td>3.55</td><td>5.27</td><td>4.01</td><td>5.71</td><td>2.08</td><td>75.1</td></tr><tr><th>Neural-VME (unfreeze)</th><td>3.45</td><td>5.20</td><td>5.30</td><td>6.71</td><td>2.14</td><td>76.9</td></tr><tr><th>gray!30SARL-F</th><td>gray!303.45</td><td>gray!305.20</td><td>gray!306.10</td><td>gray!307.27</td><td>gray!302.33</td><td>gray!3080.4</td></tr><tr><th>- w/o VM loss</th><td>-</td><td>-</td><td>5.29</td><td>6.68</td><td>2.21</td><td>77.9</td></tr><tr><th>- w/o VM signals</th><td>3.54</td><td>5.27</td><td>2.74</td><td>4.87</td><td>2.02</td><td>72.1</td></tr><tr><th>gray!30SARL-S</th><td>gray!303.44</td><td>gray!305.20</td><td>gray!307.10</td><td>gray!308.09</td><td>gray!302.40</td><td>gray!3082.1</td></tr><tr><th>- w/o VM loss</th><td>-</td><td>-</td><td>6.89</td><td>7.91</td><td>2.39</td><td>81.9</td></tr><tr><th>- w/o VM signals</th><td>3.65</td><td>5.34</td><td>3.12</td><td>5.12</td><td>2.04</td><td>73.3</td></tr><tr><th colspan="2">SpatialNet + MCWF 6ch</th><td>-</td><td>-</td><td>8.35</td><td>9.06</td><td>2.41</td><td>84.6</td></tr></tbody></table>

Table 2: Ablation on Spatial-Magnifier, RM: 2ch, VM: 4ch

<table><tbody><tr><th rowspan="2">Training method</th><th rowspan="2">Model type</th><td colspan="2">Neural-VME</td><td colspan="4">VM-BF</td></tr><tr><td>SI-SDR</td><td>SNR</td><td>SI-SDR</td><td>SNR</td><td>PESQ</td><td>STOI</td></tr><tr><th colspan="2">SpatialNet + MCWF 2ch</th><td>-</td><td>-</td><td>2.19</td><td>4.57</td><td>1.97</td><td>70.4</td></tr><tr><th rowspan="4">SARL-F</th><th>gray!30Spatial-Magnifier</th><td>gray!303.45</td><td>gray!305.20</td><td>gray!306.10</td><td>gray!307.27</td><td>gray!302.33</td><td>gray!3080.4</td></tr><tr><th>- w/o GAN</th><td>3.47</td><td>5.21</td><td>6.27</td><td>7.40</td><td>2.33</td><td>80.6</td></tr><tr><th>- w/o selection module</th><td>3.39</td><td>5.16</td><td>5.98</td><td>7.18</td><td>2.30</td><td>79.7</td></tr><tr><th>- w/o DCA</th><td>3.40</td><td>5.17</td><td>5.54</td><td>6.87</td><td>2.16</td><td>76.9</td></tr><tr><th rowspan="4">SARL-S</th><th>gray!30Spatial-Magnifier</th><td>gray!303.44</td><td>gray!305.20</td><td>gray!307.10</td><td>gray!308.09</td><td>gray!302.40</td><td>gray!3082.1</td></tr><tr><th>- w/o GAN</th><td>3.49</td><td>5.23</td><td>7.06</td><td>8.06</td><td>2.39</td><td>81.8</td></tr><tr><th>- w/o selection module</th><td>3.39</td><td>5.16</td><td>6.82</td><td>7.85</td><td>2.35</td><td>81.5</td></tr><tr><th>- w/o DCA</th><td>3.41</td><td>5.16</td><td>7.01</td><td>8.00</td><td>2.38</td><td>81.9</td></tr><tr><th colspan="2">SpatialNet + MCWF 6ch</th><td>-</td><td>-</td><td>8.35</td><td>9.06</td><td>2.41</td><td>84.6</td></tr></tbody></table>

Table 3: VM-BF comparison against baseline models

<table><tbody><tr><th></th><td colspan="6">RM: 2ch, VM: 1ch</td><td colspan="6">RM: 2ch, VM: 4ch</td><td rowspan="3">Param.</td><td rowspan="3">MAC/s</td></tr><tr><th></th><td colspan="2">Neural-VME</td><td colspan="4">VM-BF</td><td colspan="2">Neural-VME</td><td colspan="4">VM-BF</td></tr><tr><th></th><td>SI-SDR</td><td>SNR</td><td>SI-SDR</td><td>SNR</td><td>PESQ</td><td>STOI</td><td>SI-SDR</td><td>SNR</td><td>SI-SDR</td><td>SNR</td><td>PESQ</td><td>STOI</td></tr><tr><th>SpatialNet + MCWF 2ch</th><td>-</td><td>-</td><td>3.14</td><td>4.96</td><td>2.13</td><td>75.5</td><td>-</td><td>-</td><td>3.14</td><td>4.96</td><td>2.13</td><td>75.5</td><td>1.2 M</td><td>19.8 G</td></tr><tr><th>  + MC Conv-TasNet (STL) <cite>[ochiai2021neural]</cite></th><td>2.85</td><td>4.81</td><td>3.37</td><td>5.10</td><td>2.14</td><td>76.1</td><td>2.84</td><td>4.80</td><td>3.69</td><td>5.31</td><td>2.16</td><td>76.8</td><td>+13.0 M</td><td>+20.5 G</td></tr><tr><th>  + MC Conv-TasNet (MTL) <cite>[segawa2024neural]</cite></th><td>2.83</td><td>4.79</td><td>3.78</td><td>5.37</td><td>2.17</td><td>76.9</td><td>2.76</td><td>4.75</td><td>4.89</td><td>6.16</td><td>2.24</td><td>79.3</td><td>+13.0 M</td><td>+20.5 G</td></tr><tr><th>  + SpatialNet-VME</th><td>2.90</td><td>4.84</td><td>4.80</td><td>5.39</td><td>2.17</td><td>76.9</td><td>2.40</td><td>4.50</td><td>4.87</td><td>6.15</td><td>2.23</td><td>79.2</td><td>+1.2 M</td><td>+19.8 G</td></tr><tr><th>  + Spatial-Magnifier (VME)</th><td>2.77</td><td>4.76</td><td>5.58</td><td>6.69</td><td>2.31</td><td>80.6</td><td>2.89</td><td>4.83</td><td>5.84</td><td>6.88</td><td>2.36</td><td>81.6</td><td>+1.2 M</td><td>+19.2 G</td></tr><tr><th>  gray!30+ Spatial-Magnifier (SARL-F)</th><td>gray!302.61</td><td>gray!304.66</td><td>gray!306.32</td><td>gray!307.27</td><td>gray!302.36</td><td>gray!3082.4</td><td>gray!302.78</td><td>gray!304.76</td><td>gray!307.72</td><td>gray!308.37</td><td>gray!302.51</td><td>gray!3085.1</td><td>gray!30+1.5 M</td><td>gray!30+24.4 G</td></tr><tr><th>  gray!30+ Spatial-Magnifier (SARL-S)</th><td>gray!302.69</td><td>gray!304.70</td><td>gray!306.87</td><td>gray!307.70</td><td>gray!302.40</td><td>gray!3083.1</td><td>gray!302.78</td><td>gray!304.76</td><td>gray!308.37</td><td>gray!308.98</td><td>gray!302.57</td><td>gray!3086.5</td><td>gray!30+1.2 M</td><td>gray!30+19.2 G</td></tr><tr><th>SpatialNet + MCWF 3/6 ch</th><td>-</td><td>-</td><td>5.41</td><td>6.57</td><td>2.25</td><td>80.6</td><td>-</td><td>-</td><td>9.49</td><td>9.91</td><td>2.57</td><td>88.9</td><td>1.2 M</td><td>19.8 G</td></tr><tr><th>Oracle MCWF 3/6 ch</th><td>-</td><td>-</td><td>6.65</td><td>7.55</td><td>2.41</td><td>84.6</td><td>-</td><td>-</td><td>11.78</td><td>12.06</td><td>2.70</td><td>92.4</td><td>-</td><td>-</td></tr></tbody></table>

## 4 Results

For the ablation study and baseline comparison, we employed SpatialNet-small \[quan2024spatialnet\] as the MC-SE model combined with an MCWF \[benesty2008microphone, wang2022stft\] beamformer. Neural network computation load is reported as Multiply Accumulates per second (MAC/s).

### 4.1 Ablation study

This analysis focuses on the FoV-SE task suitable for MC-SE. First, in Table 1 we show that while joint VM-BF and Neural-VME fine-tuning of a petrained MC-SE model improves VM-BF performance, it remained inferior to the proposed SARL methods. This demonstrates that conditioning the MC-SE model directly on VM features outperforms standard fine-tuning. Second, removing the VM loss drops the performance of both SARL methods. The performance drop without VM loss confirms the necessity of virtual spatial information, suggesting that leveraging generated spatial information for VF-BF is crucial. Notably, even when excluding the VM signals from the adaptive beamforming the VM-BF improves with respect to the Spatialnet+MCWF system that utilizes only 2ch-RM, which suggests the effectiveness of SARL conditioning.

We report the Spatial-Magnifier architecture ablation study in Table 2. While GAN provides the highest Neural-VME performance, its effectiveness for VM-BF seems modest. In contrast, VM-BF performance degrades significantly without the selection or DCA modules. Both modules are highly efficient, each adding only 0.1M parameters and 0.1 GMAC/s.

The results for the selection module suggest that weighted sums per convolutional channel enhance the flexibility of spatial information utilization. Similarly, the performance gain from DCA reveals that attention scores play a crucial role in effectively compressing spatial information.

### 4.2 Comparison with existing Neural-VME models

For comparisons with previous work \[segawa2024neural\] in the omni-SE task, Table 3 shows that simply employing a high-performance MC-SE model is not the optimal approach for VM-BF. We confirm this finding by also utilizing SpatialNet \[quan2024spatialnet\] as an architecture for the Neural-VME task. Overall, the proposed Spatial-Magnifier achieves superior VM-BF results with lower computational cost. When estimating multiple VM signals Spatial-Magnifier, outperforms other baselines also in the Neural-VME task, highlighting the necessity of a specialized network that exploits spatial information across the channel dimension design for spatial upsampling is critical. Also, the SARL training frameworks enables joint optimization of Neural-VME accuracy while concurrently achieving the highest VM-BF performance through learned spatial audio representations.

Interestingly, the 2ch-RM/1ch-VM SpatialNet+MCWF with SARL outperforms the 3ch-RM SpatialNet+MCWF, proving the joint multi-task loss creates effective spatial representations for downstream enhancement. Furthermore, the 2ch-RM/1ch-VM SARL-S configuration synthesizes virtual channels with non-linear spatial priors, acting as an optimized spatial regularizer that achieves better noise suppression than the 3ch-RM oracle MCWF. However, all the 2ch-RM/4ch-VM setup still trails the 6ch-RM oracle MCWF, indicating room for further improvement in complex spatial upsampling scenarios.

### 4.3 Versatility across various processing strategies

The performance across variants involving different processing strategies is depicted in Table 4 for the FoV-SE task. To evaluate the versatility of our approach, we expanded the experiments to include a challenging 2ch-RM/8ch-VM scenario. We also assessed the reliability on core processing components by adopting a mask-based Souden MVDR \[souden2009optimal\] as the adaptive beamformer and switching the MC-SE model to a multichannel recurrent neural network (MC-RNN) \[pandey2023simple\]. Furthermore, we validated the method on a simulated 7-channel generated using measured Array Transfer Functions (ATFs) from an array comprising 5 microphones mounted in smart glasses (RM) and 2 channels representing HRTF responses (VM).

In the challenging 2ch-RM/8ch-VM configuration, the model achieved performance near that of a physical 10-channel system, indicating it generates substantial spatial information for VM-BF even from limited data. The framework's robustness across different back-ends was demonstrated by switching from MCWF to MVDR while maintaining competitive results. Similarly, replacing the backbone MC-SE model with MC-RNN preserved performance gains, confirming the architecture-agnostic nature of the approach. Finally, the method achieved results comparable to a 7ch-RM model on the smart glasses form-factor with HRTF recordings suggests broad applicability to diverse real-world array geometries.

Finally, we verified whether Neural-VME could augment a state-of-the-art end-to-end model, such as SpatialNet \[quan2024spatialnet\]. As a result, by performing the VM-SE task using the combination of SpatialNet-small and the proposed Spatial-Magnifier, our approach achieved a higher speech quality than SpatialNet-large 2ch-RM, despite the significantly lower computational costs of our configuration (parameter size: 2.7M vs. 6.5M, computational complexity: 44.2 GMAC/s vs. 110 GMAC/s). This suggests that when the number of microphones is constrained, leveraging virtual spatial information is a more effective strategy for enhancing performance than simply increasing the model size.

Table 4: Variants involving different processing strategies

<table><tbody><tr><th>Variant</th><th></th><td colspan="2">Neural-VME</td><td colspan="4">VM-BF (or VM-SE)</td></tr><tr><th>types</th><th></th><td>SI-SDR</td><td>SNR</td><td>SI-SDR</td><td>SNR</td><td>PESQ</td><td>STOI</td></tr><tr><th></th><th>SpatialNet + MCWF 2ch</th><td>-</td><td>-</td><td>2.19</td><td>4.57</td><td>1.97</td><td>70.4</td></tr><tr><th></th><th>gray!30  + SARL-F</th><td>gray!305.51</td><td>gray!306.71</td><td>gray!306.59</td><td>gray!307.62</td><td>gray!302.37</td><td>gray!3081.6</td></tr><tr><th></th><th>gray!30  + SARL-S</th><td>gray!305.57</td><td>gray!306.75</td><td>gray!307.06</td><td>gray!308.05</td><td>gray!302.40</td><td>gray!3082.4</td></tr><tr><th>VM 8ch</th><th>SpatialNet + MCWF 10ch</th><td>-</td><td>-</td><td>9.56</td><td>10.10</td><td>2.56</td><td>88.3</td></tr><tr><th></th><th>SpatialNet + MVDR 2ch</th><td>-</td><td>-</td><td>3.07</td><td>5.09</td><td>2.11</td><td>74.6</td></tr><tr><th></th><th>gray!30  + SARL-F</th><td>gray!303.45</td><td>gray!305.20</td><td>gray!306.72</td><td>gray!307.75</td><td>gray!302.39</td><td>gray!3081.7</td></tr><tr><th></th><th>gray!30  + SARL-S</th><td>gray!303.37</td><td>gray!305.14</td><td>gray!306.32</td><td>gray!307.45</td><td>gray!302.35</td><td>gray!3080.6</td></tr><tr><th>MVDR</th><th>SpatialNet + MVDR 6ch</th><td>-</td><td>-</td><td>8.03</td><td>8.78</td><td>2.52</td><td>85.2</td></tr><tr><th></th><th>MC-RNN + MCWF 2ch</th><td>-</td><td>-</td><td>-2.66</td><td>2.38</td><td>1.67</td><td>59.4</td></tr><tr><th></th><th>gray!30  + SARL-F</th><td>gray!303.54</td><td>gray!305.26</td><td>gray!30-1.31</td><td>gray!303.02</td><td>gray!301.80</td><td>gray!3064.7</td></tr><tr><th></th><th>gray!30  + SARL-S</th><td>gray!303.50</td><td>gray!305.24</td><td>gray!301.15</td><td>gray!304.17</td><td>gray!301.99</td><td>gray!3070.3</td></tr><tr><th>MC- RNN</th><th>MC-RNN + MCWF 6ch</th><td>-</td><td>-</td><td>2.79</td><td>4.95</td><td>2.01</td><td>72.3</td></tr><tr><th></th><th>SpatialNet + MCWF 3ch</th><td>-</td><td>-</td><td>2.48</td><td>4.83</td><td>1.92</td><td>72.6</td></tr><tr><th></th><th>gray!30  + SARL-F</th><td>gray!303.97</td><td>gray!305.56</td><td>gray!304.97</td><td>gray!306.48</td><td>gray!302.10</td><td>gray!3079.1</td></tr><tr><th></th><th>gray!30  + SARL-S</th><td>gray!304.31</td><td>gray!305.80</td><td>gray!305.90</td><td>gray!307.22</td><td>gray!302.28</td><td>gray!3082.1</td></tr><tr><th>Smart glasses</th><th>SpatialNet + MCWF 7ch</th><td>-</td><td>-</td><td>7.34</td><td>8.26</td><td>2.36</td><td>85.9</td></tr><tr><th></th><th>SpatialNet-small 2ch</th><td>-</td><td>-</td><td>8.16</td><td>8.99</td><td>2.62</td><td>86.2</td></tr><tr><th></th><th>gray!30  + SARL-F</th><td>gray!303.54</td><td>gray!305.26</td><td>gray!309.04</td><td>gray!309.73</td><td>gray!302.72</td><td>gray!3087.6</td></tr><tr><th></th><th>gray!30  + SARL-S</th><td>gray!303.58</td><td>gray!305.29</td><td>gray!308.80</td><td>gray!309.43</td><td>gray!302.62</td><td>gray!3086.5</td></tr><tr><th></th><th>SpatialNet-large 2ch</th><td>-</td><td>-</td><td>9.33</td><td>9.93</td><td>2.62</td><td>87.5</td></tr><tr><th>VM-SE</th><th>SpatialNet-small 6ch</th><td>-</td><td>-</td><td>12.1</td><td>12.4</td><td>2.92</td><td>92.3</td></tr></tbody></table>

## 5 Conclusion

This paper introduces Spatial-Magnifier, a dedicated network for audio spatial upsampling, and SARL, a novel training framework for virtual microphone-based beamforming (VM-BF) and speech enhancement (VM-SE). The proposed method achieves high VM-BF performance by effectively leveraging spatial information to estimate multiple VM representations to condition a downstream task. Furthermore, the method showcases robustness across various speech enhancement tasks, array geometries, and downstream model architectures.

## 6 Generative AI Use Disclosure

Generative AI tools (Gemini, ChatGPT) were used for editing and polishing the manuscript. All scientific content, experimental design, and results were produced by the authors.