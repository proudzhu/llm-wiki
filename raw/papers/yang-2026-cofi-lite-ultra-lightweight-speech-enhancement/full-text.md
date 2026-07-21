# CoFi-Lite: Pushing the Limits of Ultra-Lightweight Speech Enhancement

Leyan Yang, Dahan Wang, Xiaobin Rong, Jiadong Zhao, Jing Lu, Senior Member, IEEE

Abstract—Ultra-lightweight models are essential for the deployment of deep learning-based speech enhancement algorithms on edge devices. Although recent approaches have achieved a certain balance between computational complexity and performance, pushing the complexity limits further demands more sophisticated designs. In this letter, we propose CoFi-Lite, a highly efficient model that decouples spectral modeling into coarse- and fine-grained streams. By leveraging two parallel and symmetric encoder-decoder paths, it simultaneously extracts fullband envelopes and low-frequency details for complementary enhancement. In addition, a novel Cross-Path Fusion (CPF) module is introduced to bridge the distinct paths, facilitating efficient feature interaction. Remarkably, CoFi-Lite requires extremely low computational resources, featuring only 12.87M MACs/s and 83.12k parameters. Experimental results demonstrate that our proposed model outperforms the ultra-lightweight baseline GTCRN while requiring only 40.26% of its computational complexity. Its scaled-up variant also delivers performance on par with that of the SOTA ultra-lightweight model AdaptCRN alongside a 19.34% reduction in computational cost. Audio examples are available at https://acceleration123.github.io/CoFiLite-demo/.

Index Terms—speech enhancement, ultra-lightweight model, computational complexity

## I. INTRODUCTION

PEECH enhancement (SE) aims to restore clean speech S from noisy and reverberant signals [1]. With the progress of deep learning, the field of SE has achieved remarkable breakthroughs, with algorithms generally categorized into time domain [2]–[5] and time-frequency (T-F) domain [6]–[11] methods. Despite significantly surpassing traditional signal processing methods, deep learning-based approaches typically demand heavy computational resources, hindering their deployment on low-compute edge devices. To address this issue, a recent line of research centers on ultra-lightweight SE model development, which typically adopts the T-F domain convolutional recurrent network (CRN) [6] architecture, integrating various designs and techniques to reduce the overall computational cost [12]–[16]. With only 30M to 100M multiplyaccumulate operations per second (MACs/s), these approaches deliver promising performance, even rivaling models with substantially higher computational demands.

For resource-constrained edge devices, further reducing computational complexity remains a meaningful yet challenging task. To achieve this within the aforementioned CRNbased frameworks, a straightforward strategy is to compress the whole network (e.g., layers, channels, and spectral resolutions). However, our preliminary experiments reveal that naive downscaling may lead to rapid performance degradation, particularly in the low-frequency bands where noise compo nents are insufficiently suppressed. This observation suggests that a more refined architecture is needed to allocate modeling capacity across low- and high-frequency regions more effectively, thereby further reducing computational complexity while preserving low-frequency performance. One feasible solution is to employ full/sub-band [13], [17] or multi-scale spectral processing [18], but these works lack explicit emphasis on low-frequency recovery. [19] adopts two sub-networks to process the full-band and low-frequency regions sequentially. Unfortunately, its strictly cascaded structure prevents the sub-networks from achieving mutual and synergistic feature fusion, and is prone to error accumulation. [20] uses two parallel branches to model the magnitude spectrum and phase details with cross-domain interaction in multi-channel settings, but such architectural designs remain under-explored in ultralightweight monaural SE.

To this end, we propose CoFi-Lite, an ultra-lightweight SE model that operates in parallel at Coarse- and Fine-grained spectral scales while requiring only 12.87M MACs/s and 83.12k parameters. Specifically, CoFi-Lite employs two dedicated encoder-decoder paths to process full-band envelopes and low-frequency details, respectively, thereby achieving synergistic SE performance. We also introduce a novel Cross-Path Fusion (CPF) module, which is inserted at the bottlenecks of the two parallel paths, allowing efficient mutual feature interaction. Extensive experiments confirm the superiority of these design choices.

## II. METHODOLOGY

## A. Model Overview

As depicted in Fig. 1 (a), CoFi-Lite mainly comprises two parallel coarse and fine paths, bridged by the CPF module. Each path adopts the standard CRN framework, including an encoder, a decoder, and two inter-frame RNNs (Inter-RNNs) [8] as the bottleneck enhancers. Given a noisy mixture x, it is first transformed into the complex spectrum $\dot { \mathbf { X } } \in \mathbb { C } ^ { T \times F }$ via short-time Fourier transform (STFT), where $T ,$ F denote the time and frequency dimensions, respectively. X is then pre-processed into two distinct inputs $\mathbf { I } _ { \mathrm { c } }$ and $\mathbf { I } _ { \mathrm { f } }$ for each path.

![](figures/44ad400d7063952cadcbc305668a927c65634d5419d0809afa3c58ea54b46e24.jpg)  
Fig. 1: (a) The overall diagram of the proposed CoFi-Lite, where Re(·) and Im(·) denote the operations of extracting real and imaginary parts, respectively. (b) The details of the MB block. (c) The details of the CPF module.

These features are processed by their respective encoders and the first Inter-RNN modules; the resulting representations $\mathbf { E } _ { \mathrm { c } }$ and $\mathbf { E } _ { \mathrm { f } }$ are then fed into CPF to obtain the interacted and enhanced features $\mathbf { D } _ { \mathrm { c } }$ and $\mathbf { D } _ { \mathrm { f } } .$ . By mapping these output features through the remaining modules, the model predicts two ideal ratio masks (IRMs) [21], denoted as $\mathbf { M } _ { \mathrm { c } }$ and $\mathbf { M } _ { \mathrm { f } } .$ They are applied sequentially to recover the full-band magnitude envelope and refine low-frequency details, formulated as:

$$
| \tilde {\mathbf {S}} (t, f) | = \left\{ \begin{array}{l l} | \mathbf {X} (t, f) | \otimes \mathbf {M} _ {\mathrm{c}} (t, f) \otimes \mathbf {M} _ {\mathrm{f}} (t, f), & f \leq f _ {\text {low}} \\ | \mathbf {X} (t, f) | \otimes \mathbf {M} _ {\mathrm{c}} (t, f), & f > f _ {\text {low}} \end{array} \right.\tag{1}
$$

where $| \tilde { \bf S } |$ denotes the restored magnitude spectrum, and $t , f$ denote the frame index and frequency bin, respectively. The operator $\otimes$ represents element-wise multiplication, and $f _ { \mathrm { l o w } }$ is the cutoff frequency index separating low and high frequency bands. Notably, the target does not involve phase recovery, as ultra-lightweight models generally lack sufficient capacity for accurate phase modeling [15]. Although this choice imposes an upper bound on the theoretical performance [22], it ensures an effective performance-complexity trade-off. The enhanced complex spectrum $\tilde { \bf S }$ is formed by combining |S<sup>˜</sup>| with the noisy phase $\angle \mathbf { X }$ , followed by the inverse STFT (iSTFT) to generate the final output ˜s. For model training, we adopt the same loss function as in [12].

## B. Coarse Path

The coarse encoder aims to capture compact features that represent coarse-grained spectral structures. Prior to encoding, we employ the band merging (BM) module [12] to compress the sparse high-frequency information by condensing components above $f _ { \mathrm { l o w } }$ with an equivalent rectangular bandwidth (ERB) filter bank, formulating the coarse input $\mathbf { I } _ { \mathrm { c } }$ as:

$$
\mathbf {I} _ {\mathrm{c}} = \mathcal {F} _ {\mathrm{SFE}} \left(\log_ {1 0} \left(\mathcal {F} _ {\mathrm{ERB}} \left(| \mathbf {X} |\right)\right)\right)\tag{2}
$$

where $\mathcal { F } _ { \mathrm { E R B } } ( \cdot )$ denotes the BM operation, and $\mathcal { F } _ { \mathrm { S F E } } ( \cdot )$ represents the subband feature extraction (SFE) module from [12] to boost efficient spectral utilization. Within the encoder, three MB blocks shown in Fig. 1 (b) are stacked to progressively reduce the frequency resolution by a factor of 2. Derived from [15] for its proven efficacy, the MB block consists of a sequence of a point-wise convolution (PW-Conv), a depth-wise convolution (DW-Conv), and another PW-Conv, integrated with a temporal recurrent attention (TRA) module [12]. Notably, we replace the original causal time-frequency attention (cTFA) module with TRA for simplicity and computational efficiency. The configurations for Batch Normalization (BN) and affine PReLU (APReLU) are kept consistent with the original design. The coarse decoder adopts an architecture symmetric to the encoder, utilizing transposed convolution in each DW-Conv. Skip connections are employed between corresponding MB blocks of the encoder and decoder. After sigmoid activation, the output undergoes the band splitting (BS) module to generate $\mathbf { M _ { c } }$ by reversing the BM operation.

## C. Fine Path

As deep compression and restricted channel count compromise the coarse path’s capacity in low-frequency modeling, the fine path is introduced to recover these fine-grained details. Unlike the coarse path, which exploits the full-band magnitude, the fine path focuses on low-frequency bands and leverages both magnitude and phase information, with its input $\mathbf { I } _ { \mathrm { f } }$ calculated as:

$$
\mathbf {I} _ {\mathrm{f}} = \mathcal {F} _ {\mathrm{SFE}} \left(\left[ \log_ {1 0} | \mathbf {X} ^ {1} |, \frac {\mathbf {X} _ {\mathrm{r}} ^ {1}}{| \mathbf {X} ^ {1} | ^ {0 . 7}}, \frac {\mathbf {X} _ {\mathrm{i}} ^ {1}}{| \mathbf {X} ^ {1} | ^ {0 . 7}} \right]\right)\tag{3}
$$

where $\mathbf { X } ^ { \mathrm { { I } } }$ refers to the low-frequency bands of X truncated at the cutoff index $f _ { \mathrm { l o w } }$ . The subscripts r, i represent the real and imaginary parts of the complex spectrum, respectively. Dynamic range compression with an empirical exponent set of 0.7 is applied to the input components for effective feature extraction [14], [16], [23]. Within the encoder, only a single MB block is used for feature extraction, with a (1,2) stride to downsample along the frequency dimension. This design choice preserves the high resolution essential to low-frequency details while keeping the computational burden of subsequent modules manageable. Analogous to the coarse path, the fine decoder mirrors the encoder’s structure, and the final output utilizes a sigmoid activation to yield $\mathbf { M } _ { \mathrm { f } }$

## D. Cross-Path Fusion

To facilitate cross-path feature interaction, we introduce the CPF module. As shown in Fig. 1 (c), the preceding representations $\mathbf { E } _ { \mathrm { c } }$ and $\mathbf { E } _ { \mathrm { f } }$ are reshaped from $C _ { i } \times T \times F _ { i } ^ { \prime }$ to $T \times \left( C _ { i } \cdot F _ { i } ^ { \prime } \right)$ where $C _ { i }$ and $F _ { i } ^ { \prime }$ denote the channel and compressed frequency dimensions, respectively, and subscript $i ~ \in ~ \{ 1 , 2 \}$ corresponds to the coarse and fine paths. The flattened features are then concatenated to form a unified high-dimensional representation $\mathbf { E } _ { \mathrm { i n } } \in \mathbb { R } ^ { T \times D }$ , where $D = ( C _ { 1 } \cdot F _ { 1 } ^ { \prime } ) + ( C _ { 2 } \cdot F _ { 2 } ^ { \prime } )$ To control the computational complexity, the CPF module first compresses $\mathbf { E _ { \mathrm { { i n } } } }$ into an H-dimensional latent space using a fully connected (FC) layer. The resulting feature is then processed by layer normalization (LN) and an exponential linear unit (ELU), after which an RNN module captures the temporal patterns of the fused feature Z. Another FC layer is subsequently applied to restore the feature dimension to the original size D. The final output is split into two parts and reshaped back to $C _ { i } \times T \times F _ { i } ^ { \prime } , i \in \{ 1 , 2 \}$ }. Additionally, skip connections are incorporated to retain previous spectral information before obtaining $\mathbf { D } _ { \mathrm { c } }$ and $\mathbf { D } _ { \mathrm { f } }$ for each path.

## III. EXPERIMENTAL SETUP

## A. Dataset

We train and evaluate our proposed model using the DNS3 dataset [24], with the Mandarin corpus from DiDiSpeech [25] as additional speech material. Noisy mixtures are generated by convolving clean speech with a random room impulse response (RIR) and adding a randomly selected noise clip with the SNR uniformly sampled from [-5, 15] dB. The training target is the speech signal containing early reverberation within the first 100 ms. For training, 72,000 noisy-clean pairs of 10-second duration (amounting to 200 hours) are generated, while 1,000 pairs are generated for validation and testing, respectively.

To further validate the generalization capability of the proposed model in different acoustic environments, we conduct additional evaluations on the official DNS Challenge 2020 test set [26], covering both non-reverberant and reverberant scenarios. All utterances are sampled at 16 kHz.

## B. Implementation Details

1) Parameter configuration: The STFT is computed using a 32 ms square-root Hanning window with a hop length of 16 ms and an FFT size of 512. The kernel size of both SFE modules is set to 3. $f _ { \mathrm { l o w } }$ is set to 65, corresponding to a physical frequency of 2 kHz. The BM module preserves the first 65 frequency bands unaltered and compresses the 192 high-frequency bands to 64 bands. With subsequent MB blocks introducing a compression factor of 8, the coarse path reaches a total full-band compression ratio of 16. In the coarse encoder, the first MB block uses a (3,5) kernel, while the remaining two use (1,5). The fine encoder employs a (3,3) kernel for finer extraction. All MB blocks have 6 output channels, and all Inter-RNN modules utilize GRUs. CPF employs a grouped GRU (2 groups) with a latent dimension H of 76. We also investigate a scaled-up variant, CoFi-Lite (Large), where H is increased to 102, and the output channels of the coarse and fine encoders are expanded to [6, 12, 14] and 14, respectively. All other settings remain unchanged.

2) Training configuration: The models are trained using the Adam optimizer [27] with a linear warmup scheduler followed by cosine annealing. The training procedures last for 200 epochs, where each epoch contains 1,250 iterations with a batch size of 8. The learning rate increases linearly from $1 0 ^ { - 6 } ~ \mathrm { t o } ~ 1 0 ^ { - 3 }$ over the initial 25,000 iterations and then decays following a cosine schedule until 250,000 iterations.

## C. Baseline Models and Evaluation Metrics

We select the latest ultra-lightweight SE models as our baselines, including GTCRN [12], LiSenNet [14], UL-UNAS [15], and AdaptCRN [16]. In addition, we include their scaled-down variants to provide a fairer comparison. Where available, we use reported statistics from the original papers. For missing results, we retrain the models using original codebases and parameter configurations, whereas for scaled-down variants, we proportionally reduce the number of channels for model compression. All retrained models use our own training configuration—except for AdaptCRN and its variant, which follow the settings from the original work.

Considering the real-time requirements of edge devices, we measure the real-time factor (RTF) using ONNX Runtime [28] on an Intel(R) Core(TM) i5-14600KF with streaming inference. STFT and iSTFT operations are excluded, and no future frames are used, ensuring zero algorithmic delay. To evaluate the SE performance, three intrusive metrics are employed, including scale-invariant signal-to-noise ratio (SI-SNR) [29], wide-band perceptual evaluation of speech quality (PESQ) [30] and extended short-time objective intelligibility (ESTOI) [31]. Additionally, two non-intrusive metrics, DNS-MOS P.808 [32] and DNSMOS P.835 [33], are utilized to assess the enhanced speech quality. DNSMOS P.835 includes three sub-metrics: OVRL for overall speech quality, SIG for signal quality, and BAK for background noise quality.

## IV. EXPERIMENTAL RESULTS

## A. Comparison With the Baseline Models

The results on the simulated DNS3 test set are summarized in Table I, categorized by complexity levels<sup>1</sup> (Level I/II). In Level I, CoFi-Lite demonstrates a distinct advantage over the scaled-down variants of baselines. It also clearly outperforms the Level II baseline GTCRN in PESQ (+0.09), OVRL (+0.07), and SIG (+0.07), while requiring only 40.26% of its computational cost and reducing RTF by 34.00%. In Level II, CoFi-Lite (Large) maintains competitive efficacy against AdaptCRN with a 19.34% reduction in computational demands, while also recording one of the lowest RTFs. Despite exhibiting a higher parameter count, it remains within an acceptable range for deployment on most edge devices [34].

Results on the official DNS 2020 test set are shown in Table II. Notably, intrusive metrics are excluded due to a mismatch between the anechoic reference and our training objective, which includes early reverberation. As shown, the performance trends align closely with the results observed on the DNS3 dataset.

TABLE I: Performance comparison on the simulated DNS3 test set. Only UL-UNAS uses the statistics reported in its original paper.

<table><tr><td rowspan="2">Models</td><td rowspan="2">Params (k)</td><td rowspan="2">MACs/s (M)</td><td rowspan="2">RTF</td><td rowspan="2">PESQ</td><td rowspan="2">ESTOI (×100)</td><td rowspan="2">SI-SNR</td><td rowspan="2">DNSMOS P.808</td><td colspan="3">DNSMOS P.835</td></tr><tr><td>OVRL</td><td>SIG</td><td>BAK</td></tr><tr><td>Noisy</td><td>-</td><td>-</td><td>-</td><td>1.40</td><td>66.90</td><td>5.61</td><td>2.82</td><td>1.63</td><td>2.05</td><td>1.86</td></tr><tr><td colspan="11">Level I: Below 20M MACs/s</td></tr><tr><td>GTCRN (Small)</td><td>7.91</td><td>13.63</td><td>0.040</td><td>1.88</td><td>72.18</td><td>10.07</td><td>3.38</td><td>2.53</td><td>2.88</td><td>3.76</td></tr><tr><td>LiSenNet (Small)</td><td>12.46</td><td>15.57</td><td>0.031</td><td>1.94</td><td>72.74</td><td>10.49</td><td>3.36</td><td>2.58</td><td>2.93</td><td>3.80</td></tr><tr><td>UL-UNAS (Small)</td><td>56.43</td><td>13.63</td><td>0.054</td><td>2.05</td><td>74.87</td><td>11.16</td><td>3.47</td><td>2.60</td><td>2.94</td><td>3.81</td></tr><tr><td>AdaptCRN (Small)</td><td>34.98</td><td>12.97</td><td>0.047</td><td>2.06</td><td>75.15</td><td>11.19</td><td>3.50</td><td>2.65</td><td>2.99</td><td>3.85</td></tr><tr><td>CoFi-Lite</td><td>83.12</td><td>12.87</td><td>0.033</td><td>2.16</td><td>76.10</td><td>11.80</td><td>3.53</td><td>2.70</td><td>3.05</td><td>3.85</td></tr><tr><td colspan="11">Level II: Over 30M MACs/s</td></tr><tr><td>GTCRN</td><td>23.67</td><td>31.97</td><td>0.050</td><td>2.07</td><td>75.11</td><td>11.30</td><td>3.48</td><td>2.63</td><td>2.98</td><td>3.81</td></tr><tr><td>LiSenNet</td><td>36.78</td><td>55.77</td><td>0.035</td><td>2.17</td><td>76.19</td><td>11.74</td><td>3.53</td><td>2.69</td><td>3.03</td><td>3.85</td></tr><tr><td>UL-UNAS</td><td>171.33</td><td>34.91</td><td>0.066</td><td>2.25</td><td>77.69</td><td>12.07</td><td>3.55</td><td>2.69</td><td>3.01</td><td>3.86</td></tr><tr><td>AdaptCRN</td><td>134.51</td><td>40.80</td><td>0.053</td><td>2.30</td><td>78.15</td><td>12.35</td><td>3.59</td><td>2.75</td><td>3.08</td><td>3.88</td></tr><tr><td>CoFi-Lite (Large)</td><td>221.31</td><td>32.91</td><td>0.036</td><td>2.30</td><td>77.94</td><td>12.43</td><td>3.56</td><td>2.75</td><td>3.09</td><td>3.88</td></tr></table>

TABLE II: Performance comparison on the DNS Challenge 2020 test set. We retrain all baselines and their variants to obtain the statistics.

<table><tr><td rowspan="2">Models</td><td colspan="3">No Reverb</td><td colspan="3">With Reverb</td></tr><tr><td>OVRL</td><td>SIG</td><td>BAK</td><td>OVRL</td><td>SIG</td><td>BAK</td></tr><tr><td>Noisy</td><td>2.48</td><td>3.39</td><td>2.62</td><td>1.39</td><td>1.76</td><td>1.50</td></tr><tr><td colspan="7">Level I: Below 20M MACs/s</td></tr><tr><td>GTCRN (Small)</td><td>2.99</td><td>3.31</td><td>3.91</td><td>2.33</td><td>2.72</td><td>3.55</td></tr><tr><td>LiSenNet (Small)</td><td>3.00</td><td>3.32</td><td>3.95</td><td>2.35</td><td>2.76</td><td>3.49</td></tr><tr><td>UL-UNAS (Small)</td><td>3.08</td><td>3.36</td><td>4.01</td><td>2.39</td><td>2.79</td><td>3.52</td></tr><tr><td>AdaptCRN (Small)</td><td>3.11</td><td>3.39</td><td>4.02</td><td>2.46</td><td>2.85</td><td>3.63</td></tr><tr><td>CoFi-Lite</td><td>3.15</td><td>3.43</td><td>4.03</td><td>2.48</td><td>2.89</td><td>3.57</td></tr><tr><td colspan="7">Level II: Over 30M MACs/s</td></tr><tr><td>GTCRN</td><td>3.09</td><td>3.38</td><td>4.01</td><td>2.43</td><td>2.86</td><td>3.52</td></tr><tr><td>LiSenNet</td><td>3.09</td><td>3.37</td><td>4.02</td><td>2.47</td><td>2.89</td><td>3.55</td></tr><tr><td>UL-UNAS</td><td>3.13</td><td>3.40</td><td>4.05</td><td>2.44</td><td>2.84</td><td>3.56</td></tr><tr><td>AdaptCRN</td><td>3.20</td><td>3.45</td><td>4.10</td><td>2.51</td><td>2.92</td><td>3.57</td></tr><tr><td>CoFi-Lite (Large)</td><td>3.19</td><td>3.44</td><td>4.09</td><td>2.50</td><td>2.92</td><td>3.57</td></tr></table>

## B. Ablation Study

1) Effect of key design choices: In this section, we investigate two key designs of our model: (i) the architecture of the two parallel paths, and (ii) the CPF module. The results are presented in Table III (IDs 1–5). For a fair comparison, we align the complexity across all models by adjusting the hidden size of the Inter-RNNs. Specifically, ID4 scales up ID3 to match the parameters of our proposed ID5. As shown, ID3 outperforms single-path models (IDs 1-2). Crucially, ID5 achieves a substantial PESQ gain (+0.14) over ID3 by integrating CPF. Ruling out the impact of increased parameters, it still yields a PESQ advantage (+0.10) over ID4. This indicates that $\mathbf { E } _ { \mathrm { c } }$ and $\mathbf { E } _ { \mathrm { f } }$ are highly complementary, and their interaction creates a strong synergy that boosts model performance.

2) Investigation of different compression settings: Table III (IDs 6–9) details the performance across different spectral compression ratios. Let $\mathbf { R } _ { \mathrm { c } }$ and $\mathbf { R } _ { \mathrm { f } }$ denote the compression ratios of the coarse and fine paths, respectively. Based on ID5, $\mathbf { R } _ { \mathrm { c } }$ and $\mathbf { R } _ { \mathrm { f } }$ are adjusted by adding or removing MB blocks with a (1,5) kernel and a (1,2) stride in the corresponding encoder and decoder. It can be observed that the model performance rapidly degrades as $\mathbf { R } _ { \mathrm { f } }$ increases (IDs 5–7). We attribute this degradation to the severe information loss caused by deep compression, which is unsuitable for the fine path designed to model low-frequency details. Conversely, increasing the frequency resolution in the coarse path results in marginal or negligible improvements (IDs 8–9 vs. ID5). This aligns with intuition, as envelope enhancement does not require capturing excessive fine-grained spectral details.

TABLE III: Ablation study results of the coarse/fine path design, the CPF module, different compression ratio and cutoff frequency settings. $^ { 6 6 } - ^ { 5 5 }$ indicates that the corresponding path is removed.

<table><tr><td>IDs</td><td> $R_c$ </td><td> $R_f$ </td><td> $f_{low}$ </td><td>CPF</td><td>Params (k)</td><td>MACs/s (M)</td><td>PESQ</td><td>ESTOI ( $\times 100$ )</td><td>SI-SNR</td></tr><tr><td>1</td><td>16</td><td>-</td><td>65</td><td>✗</td><td>19.71</td><td>12.37</td><td>1.97</td><td>73.73</td><td>10.68</td></tr><tr><td>2</td><td>-</td><td>2</td><td>65</td><td>✗</td><td>9.24</td><td>12.05</td><td>1.53</td><td>70.14</td><td>8.41</td></tr><tr><td>3</td><td>16</td><td>2</td><td>65</td><td>✗</td><td>21.23</td><td>12.24</td><td>2.02</td><td>74.06</td><td>10.81</td></tr><tr><td>4</td><td>16</td><td>2</td><td>65</td><td>✗</td><td>90.80</td><td>13.44</td><td>2.06</td><td>74.98</td><td>11.20</td></tr><tr><td>5</td><td>16</td><td>2</td><td>65</td><td>√</td><td>83.12</td><td>12.87</td><td>2.16</td><td>76.10</td><td>11.80</td></tr><tr><td>6</td><td>16</td><td>4</td><td>65</td><td>√</td><td>71.18</td><td>11.89</td><td>2.12</td><td>75.72</td><td>11.55</td></tr><tr><td>7</td><td>16</td><td>8</td><td>65</td><td>√</td><td>66.20</td><td>11.46</td><td>2.09</td><td>75.31</td><td>11.41</td></tr><tr><td>8</td><td>8</td><td>2</td><td>65</td><td>√</td><td>95.06</td><td>13.84</td><td>2.16</td><td>76.10</td><td>11.73</td></tr><tr><td>9</td><td>32</td><td>2</td><td>65</td><td>√</td><td>78.14</td><td>12.44</td><td>2.14</td><td>76.01</td><td>11.77</td></tr><tr><td>10</td><td>16</td><td>2</td><td>17</td><td>√</td><td>58.79</td><td>11.51</td><td>2.08</td><td>75.30</td><td>11.39</td></tr><tr><td>11</td><td>16</td><td>2</td><td>33</td><td>√</td><td>66.90</td><td>11.90</td><td>2.11</td><td>75.69</td><td>11.58</td></tr><tr><td>12</td><td>16</td><td>2</td><td>97</td><td>√</td><td>99.35</td><td>14.09</td><td>2.15</td><td>76.25</td><td>11.72</td></tr></table>

3) Study of various cutoff frequency settings: The impact of varying $f _ { \mathrm { l o w } }$ settings on performance is explored in Table III (IDs 10–12). $\mathbf { R } _ { \mathrm { c } }$ remains unchanged by adjusting the compression ratio of the BM module. Notably, increasing $f _ { \mathrm { l o w } }$ from 17 to 65 consistently yields performance gains, as it allows the fine path to capture more low-frequency details. However, no additional gains are obtained when increasing $f _ { \mathrm { l o w } }$ to $9 7 .$ since salient speech structures are concentrated below 2 kHz, leaving higher bands with sparse informative content.

## V. CONCLUSION

In this letter, we present CoFi-Lite, a highly efficient SE model requiring extremely low computational resources. The architecture effectively decouples full-band envelopes and lowfrequency details via parallel and symmetric paths for complementary enhancement. In addition, a novel CPF module is introduced to facilitate mutual feature interaction. Remarkably, CoFi-Lite outperforms GTCRN with significantly reduced computational complexity. Its scaled-up variant also achieves competitive performance among existing ultra-lightweight SE models, further confirming the potential of our proposed method. However, current measurements (e.g., RTF on a desktop CPU) might not directly reflect real-world deployment on platforms such as ARM Cortex-M and DSP, and closing this gap is our future work.

[1] J. Benesty, S. Makino, and J. Chen, Speech Enhancement, ser. Signals and Communication Technology. Springer Berlin Heidelberg, 2006.

[2] A. Pandey and D. Wang, “Tcnn: Temporal convolutional neural network for real-time speech enhancement in the time domain,” in ICASSP 2019 - 2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2019, pp. 6875–6879.

[3] Y. Luo and N. Mesgarani, “Conv-tasnet: Surpassing ideal time–frequency magnitude masking for speech separation,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 27, no. 8, pp. 1256–1266, 2019.

[4] Y. Luo, Z. Chen, and T. Yoshioka, “Dual-path rnn: Efficient long sequence modeling for time-domain single-channel speech separation,” in ICASSP 2020 - 2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, pp. 46–50.

[5] K. Wang, B. He, and W.-P. Zhu, “Tstnn: Two-stage transformer based neural network for speech enhancement in the time domain,” in ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2021, pp. 7098–7102.

[6] K. Tan and D. Wang, “A convolutional recurrent neural network for realtime speech enhancement,” in Interspeech 2018, 2018, pp. 3229–3233.

[7] Y. Hu, Y. Liu, S. Lv, M. Xing, S. Zhang, Y. Fu, J. Wu, B. Zhang, and L. Xie, “Dccrn: Deep complex convolution recurrent network for phaseaware speech enhancement,” in Interspeech 2020, 2020, pp. 2472–2476.

[8] X. Le, H. Chen, K. Chen, and J. Lu, “Dpcrn: Dual-path convolution recurrent network for single channel speech enhancement,” in Interspeech 2021, 2021, pp. 2811–2815.

[9] J. Yu and Y. Luo, “Efficient monaural speech enhancement with universal sample rate band-split rnn,” in ICASSP 2023 - 2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2023, pp. 1–5.

[10] Z.-Q. Wang, S. Cornell, S. Choi, Y. Lee, B.-Y. Kim, and S. Watanabe, “Tf-gridnet: Integrating full- and sub-band modeling for speech separation,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 31, pp. 3221–3236, 2023.

[11] H. Wang and B. Tian, “Zipenhancer: Dual-path down-up samplingbased zipformer for monaural speech enhancement,” in ICASSP 2025 - 2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2025, pp. 1–5.

[12] X. Rong, T. Sun, X. Zhang, Y. Hu, C. Zhu, and J. Lu, “Gtcrn: A speech enhancement model requiring ultralow computational resources,” in ICASSP 2024 - 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2024, pp. 971–975.

[13] L. Yang, W. Liu, R. Meng, G. Lee, S. Baek, and H.-G. Moon, “Fspen: an ultra-lightweight network for real time speech enahncment,” in ICASSP 2024 - 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2024, pp. 10 671–10 675.

[14] H. Yan, J. Zhang, C. Fan, Y. Zhou, and P. Liu, “Lisennet: Lightweight sub-band and dual-path modeling for real-time speech enhancement,” in ICASSP 2025 - 2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2025, pp. 1–5.

[15] X. Rong, L. Yang, D. Wang, Y. Hu, C. Zhu, K. Chen, and J. Lu, “Ul-unas: Ultra-lightweight u-nets for real-time speech enhancement via network architecture search,” IEEE Transactions on Audio, Speech and Language Processing, pp. 1–13, 2026.

[16] D. Wang, X. Rong, S. Sun, Y. Hu, C. Zhu, and J. Lu, “Adaptive convolution for cnn-based speech enhancement models,” IEEE Transactions on Audio, Speech and Language Processing, vol. 33, pp. 4400–4413, 2025.

[17] X. Hao, X. Su, R. Horaud, and X. Li, “Fullsubnet: A full-band and subband fusion model for real-time single-channel speech enhancement,” in ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2021, pp. 6633–6637.

[18] Z. Lin, J. Wang, R. Li, F. Shen, and X. Xuan, “Primek-net: Multi-scale spectral learning via group prime-kernel convolutional neural networks for single channel speech enhancement,” in ICASSP 2025 - 2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2025, pp. 1–5.

[19] F. Dang, H. Chen, Q. Hu, P. Zhang, and Y. Yan, “First coarse, fine afterward: A lightweight two-stage complex approach for monaural speech enhancement,” Speech Communication, vol. 146, pp. 32–44, 2023.

[20] X. Shen, R. Wang, W.-P. Zhu, and B. Champagne, “Dual-path statespace modeling with cross-domain interaction for multichannel speech enhancement,” IEEE Transactions on Audio, Speech and Language Processing, vol. 33, pp. 4239–4252, 2025.

[21] A. Narayanan and D. Wang, “Ideal ratio mask estimation using deep neural networks for robust speech recognition,” in 2013 IEEE International Conference on Acoustics, Speech and Signal Processing, 2013, pp. 7092–7096.

[22] K. Paliwal, K. Wojcicki, and B. Shannon, “The importance of phase´ in speech enhancement,” Speech Communication, vol. 53, no. 4, pp. 465–494, 2011.

[23] A. Li, C. Zheng, R. Peng, and X. Li, “On the importance of power compression and phase estimation in monaural speech dereverberation,” JASA Express Letters, vol. 1, no. 1, p. 014802, 01 2021.

[24] C. K. Reddy, H. Dubey, K. Koishida, A. Nair, V. Gopal, R. Cutler, S. Braun, H. Gamper, R. Aichner, and S. Srinivasan, “Interspeech 2021 deep noise suppression challenge,” in Interspeech 2021, 2021, pp. 2796– 2800.

[25] T. Guo, C. Wen, D. Jiang, N. Luo, R. Zhang, S. Zhao, W. Li, C. Gong, W. Zou, K. Han, and X. Li, “Didispeech: A large scale mandarin speech corpus,” in ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2021, pp. 6968– 6972.

[26] C. K. A. Reddy, V. Gopal, R. Cutler, E. Beyrami, R. Cheng, H. Dubey, S. Matusevych, R. Aichner, A. Aazami, S. Braun, P. Rana, S. Srinivasan, and J. Gehrke, “The interspeech 2020 deep noise suppression challenge: Datasets, subjective testing framework, and challenge results,” 2020.

[27] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” CoRR, vol. abs/1412.6980, 2014.

[28] O. R. developers, “Onnx runtime,” https://onnxruntime.ai/, 2021, version: 1.22.1.

[29] J. L. Roux, S. Wisdom, H. Erdogan, and J. R. Hershey, “Sdr – half-baked or well done?” in ICASSP 2019 - 2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2019, pp. 626– 630.

[30] A. Rix, J. Beerends, M. Hollier, and A. Hekstra, “Perceptual evaluation of speech quality (pesq)-a new method for speech quality assessment of telephone networks and codecs,” in 2001 IEEE International Conference on Acoustics, Speech, and Signal Processing. Proceedings (Cat. No.01CH37221), vol. 2, 2001, pp. 749–752 vol.2.

[31] J. Jensen and C. H. Taal, “An algorithm for predicting the intelligibility of speech masked by modulated noise maskers,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 24, no. 11, pp. 2009–2022, 2016.

[32] C. K. A. Reddy, V. Gopal, and R. Cutler, “Dnsmos: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors,” in ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2021, pp. 6493–6497.

[33] ——, “Dnsmos p.835: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors,” in ICASSP 2022 - 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2022, pp. 886–890.

[34] A. Pandey and J. Azcarreta, “Ultra low-compute complex spectral masking for multichannel speech enhancement,” in ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2025, pp. 1–5.