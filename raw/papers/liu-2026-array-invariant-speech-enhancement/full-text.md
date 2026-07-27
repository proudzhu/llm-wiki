# Towards Array-Invariant Speech Enhancement via Geometry-Aware Dynamic Convolution

Zhenglong Liu <sup>ID</sup> <sup>1</sup>, Wangyou Zhang <sup>ID</sup> <sup>1,2</sup>, Chenda Li <sup>ID</sup> <sup>1,2</sup>, Yanmin Qian <sup>ID</sup> <sup>1,2</sup>

<sup>1</sup> Auditory Cognition and Computational Acoustics Lab Shanghai Jiao Tong University, Shanghai, China <sup>2</sup> VUI Labs

zhenglong.liu@sjtu.edu.cn, wyz-97@sjtu.edu.cn, lichenda1996@sjtu.edu.cn, yanminqian@sjtu.edu.cn

## Abstract

Multi-channel speech enhancement (SE) systems exhibit superior performance over single-channel methods but are constrained to fixed microphone array configurations. This restricts their real-world deployment across devices with diverse array geometries. While recent array-agnostic SE methods address variable microphone numbers and permutations, they largely fail to exploit explicit array geometry priors when available, missing a crucial cue for optimal spatial filtering. A Geometry-Aware Dynamic Convolution (Geo-DConv) framework is proposed, which explicitly leverages microphone coordinates to transform standard fixed-array SE models into robust arrayinvariant systems. Experiments are conducted on the recent real-recorded RealMAN multi-channel speech dataset. Results demonstrate that the proposed architecture enables two widely used fixed-array models to adapt to array-invariant settings, with consistent performance improvements across diverse array topologies.

Index Terms: Multi-channel speech enhancement, microphone array invariant, dynamic convolution

## 1. Introduction

While multi-channel speech enhancement (SE) theoretically offers a higher performance upper bound than single-channel approaches, its real-world applicability is often hindered by its reliance on fixed microphone array geometries. The geometric variations across different arrays make it difficult to merge existing datasets into a unified, large-scale training corpus. As a result, models frequently require device-specific retraining. This contrasts sharply with single-channel SE models, which can achieve robust generalization across various distortions [1, 2] by scaling up the training data.

Array-agnostic SE has been proposed to overcome this limitation. These approaches must address two primary challenges: the variable microphone numbers and their arbitrary permutations. Existing solutions generally fall into two categories. In the first category, multi-channel inputs are processed through batch operations, then extracted cross-channel relationships by dimension-independent mechanisms, and merged into a single-channel output by setting a reference channel or taking the average. Representative methods are Transform-Average-Concatenate (TAC) [3], self-attention-based models [4], and Transform-Attention-Concatenate (TA C) [5]. The second category transforms arbitrary array inputs into fixed-dimensional multi-channel signals before processing. For instance, converting recordings into First-Order Ambisonics (FOA) [6] results in a fixed 4-channel representation, regardless of the number of microphones employed. However, this method cannot be utilized for arrays consisting of fewer than four microphones, as underdetermined conversion equations are produced. Recently, UniArray [7] introduced virtual microphone estimation to map an arbitrary number of signals to a fixed dimensionality via interpolation-based upscaling. While this design ensures consistent input dimensions for the subsequent neural network, it still requires input order permutation as an essential preprocessing step.

Despite their flexibility, array-agnostic SE models generally perform worse than fixed-array models for two main reasons. Firstly, in fixed-array methods, cross-channel feature extraction typically begins from the very first layer, and many effective modules have been designed to model these relationships. In contrast, array-agnostic SE models initially extract time-frequency features for each channel separately through batch operations, which leads to a lack of methodological diversity in modeling cross-channel relations. Secondly, during the training of fixed-array models, all recordings share the same array geometry, allowing the model to learn a favorable spatial bias corresponding to the specific device. However, existing array-agnostic methods fail to exploit explicit array geometry information, relying mostly on generic time-frequency features and implicit inter-channel correlations.

The immense value of explicit geometric information, however, has been well-established across various speech processing domains. In traditional signal processing, the Minimum Variance Distortionless Response (MVDR) [8] algorithm explicitly utilizes microphone array spacing to formulate the steering vector, demonstrating the fundamental benefit of geometry for SE. More recently, in the deep learning domain, array geometry cues have been successfully leveraged in geometryinvariant Direction-of-Arrival (DOA) estimation. For instance, GI-DOAEnet [9] employs microphone positional encodings (MPEs) to inject unique spatial information by modulating microphone spherical coordinates via sinusoidal functions. Despite these proven benefits, explicit array geometry cues remain largely unexploited in the design of array-agnostic SE models. Furthermore, since recording devices are commonly specified in multi-channel speech datasets, acquiring such geometric configurations requires absolutely no additional annotation effort, making it a highly feasible yet neglected direction for SE improvement.

In this work, we explicitly leverage the array geometry as additional input of the network through the proposed geometryaware dynamic convolution block, which enables arbitrary fixed-array SE models to be converted to array-invariant models. Furthermore, by training on real-recorded array datasets, we avoid the common issue of mismatch between simulated data and real-world environments in array-based speech enhancement.

![](figures/c82a207e32d645f4b7e2d0af7e70a913d88a8eeca0398c8a6b1a7a73f2e23d40.jpg)  
Figure 1: Architecture of the proposed Geo-DConv. The left part illustrates the Geometry-Aware Dynamic Kernel Generation based on the Topology-Aware Coordinate Transformer (TACT). The right part shows the Dynamic Convolution process applied to input acoustic features.

## 2. Methods

In common fixed-array SE, cross-channel modeling typically begins at the very first convolutional layer. Input features are stacked along the channel dimension, and inter-channel information is fused within the layer to form the output [10, 11]. However, a fundamental limitation of conventional convolutional layer is its strict requirement for a fixed input dimension. This inherent rigidity prevents the direct application of standard convolutions in array-invariant SE systems. To bridge this gap, a dynamic convolution mechanism is designed to accommodate arbitrary input channel dimensions and spatial permutations.

The overall architecture of the proposed method is depicted in Figure 1. First, the relative coordinates of the arbitrary microphone array are transformed using Fourier positional encoding. These encoded representations are subsequently fed into a novel Topology-Aware Coordinate Transformer (TACT) module, which yields a dynamic transformation matrix. By applying matrix multiplication, this matrix dynamically adapts the weights of the fixed-dimension convolution kernels to align with the specific input configuration of the target array. Following this geometry-guided adaptation, the features are processed through Layer Normalization (LN) and an activation function before being propagated to the subsequent neural network layers. By leveraging explicit array geometry, this mechanism serves as a universal adapter, effectively transforming conventional fixed-array algorithms into array-invariant models.

## 2.1. Problem Formulation

Without loss of generality, the enhancement is assumed to operate in the time-frequency domain. Let $\boldsymbol { X } \in \mathbb { R } ^ { C \times F \times T }$ denote the multi-channel acoustic feature (the real and imaginary parts of STFT complex spectrograms are concatenated along the frequency dimension), where C represents the variable number of microphones, and $F , T$ represent the frequency and time dimensions, respectively. Each microphone is associated with a relative coordinates $\boldsymbol { j } _ { i } ~ \in ~ \mathbb { R } ^ { 3 }$ , forming a coordinate matrix $G = \left[ g _ { 1 } , g _ { 2 } , \ldots , g _ { C } \right] ^ { \top } \in \mathbb { R } ^ { C \times 3 }$ . The coordinates can be formatted in either Cartesian $( x , y , z )$ or Spherical $( r , \theta , \phi )$ systems. A Geometry-Aware Dynamic Convolution (Geo-DConv)

layer is designed to handle variable-channel inputs and incorporate array geometry information, as formulated below,

$$
O u t = \operatorname{Geo-DyncConv} (G, X)\tag{1}
$$

## 2.2. Geometry-Aware Dynamic Convolution (Geo-DConv)

To process an arbitrary number of microphones without structural constraints, Geo-DConv is proposed. A typical convolution kernel is defined as $\boldsymbol { K } \in \mathbb { R } ^ { \boldsymbol { b } \times \boldsymbol { O } ^ { \star } \boldsymbol { K } _ { f } \times \boldsymbol { K } _ { t } }$ , where b denotes the basis input dimension, O is the fixed output channel size, and $K _ { f } , K _ { t }$ are the kernel size in frequency and time dimen sions.

The dynamic convolutional weight $\mathcal { W } _ { d y n }$ for a specific array geometry is generated through a linear combination of the basis kernels $\kappa ,$ , guided by a dynamic transformation coefficient matrix $M \in \mathbb { R } ^ { C \times b }$ . Specifically, the combined kernel is formulated as:

$$
\mathcal {W} _ {d y n} ^ {(c, o,:,:)} = \sum_ {j = 1} ^ {b} M _ {c, j} \cdot \mathcal {K} ^ {(j, o,:,:)}\tag{2}
$$

where $\mathcal { W } _ { d y n } \in \mathbb { R } ^ { C \times O \times K _ { f } \times K _ { t } }$ . The core challenge therefore lies in designing a robust mechanism to generate the matrix M from the relative coordinates of the array G, which must capture complex spatial interactions while maintaining adaptability to variable array configurations.

## 2.3. Topology-Aware Coordinate Transformer (TACT)

Inspired by Implicit Neural Representations (INR) in NeRF [12] and NAF [13], Fourier Positional Encoding (PE) is introduced to better characterize fine-grained variations in coordinates:

$$
\begin{array}{c} \gamma (g _ {i}) = \big [ g _ {i}, \sin (2 ^ {0} \pi g _ {i}), \cos (2 ^ {0} \pi g _ {i}), \ldots , \\ \sin (2 ^ {L - 1} \pi g _ {i}), \cos (2 ^ {L - 1} \pi g _ {i}) \big ] \end{array}\tag{3}
$$

where L is the number of frequency bands, yielding an encoded matrix $G _ { p e } \in \mathbb { R } ^ { C \times d _ { p e } } ( d _ { p e } \overset { \cdot } { = } 3 \overset { \cdot } { + } 6 L )$

The Topology-Aware Coordinate Transformer (TACT) is proposed to perform global array topology modeling. The encoded coordinate matrix $G _ { p e }$ is first projected into the hidden dimension d :

$$
G ^ {(0)} = G _ {p e} W _ {i n}, \quad W _ {i n} \in \mathbb {R} ^ {d _ {p e} \times d _ {\mathrm{hidden}}}\tag{4}
$$

The projected matrix $G ^ { ( 0 ) }$ is treated as a sequence of C tokens and fed into a Transformer Encoder block. The topology-aware feature representation $Z$ is computed via the Multi-Head Self-Attention (MHSA) mechanism:

$$
Q = G ^ {(l)} W _ {Q}, \quad K = G ^ {(l)} W _ {K}, \quad V = G ^ {(l)} W _ {V}\tag{5}
$$

$$
Z ^ {(l + 1)} = \text { LayerNorm } \left(Z ^ {(l)} + \text { MHSA } (Q, K, V)\right)\tag{6}
$$

Subsequently, the final transformation coefficient matrix M is obtained through a linear output projection after $L _ { l a y e r s }$ encoding layers:

$$
M = Z ^ {(L _ {l a y e r s})} W _ {o u t}, \quad W _ {o u t} \in \mathbb {R} ^ {d _ {h i d d e n} \times b}\tag{7}
$$

Permutation Equivariance and Stability: A critical property of the TACT module is its ability to maintain output stability under varying input channel permutations. Let $P \in$ $\{ 0 , \dot { 1 } \} ^ { C \times C }$ be a permutation matrix representing a specific spatial ordering of the microphones. If the input coordinates are permuted as P G, the point-wise nature of the Fourier PE and the permutation-equivariant property of the MHSA mechanism ensure that the generated transformation matrix becomes $P M$ According to Eq. 2, the resulting dynamic convolution kernel is correspondingly permuted to $P { \mathcal { W } } _ { d y n }$ along its input channel dimension. When performing the convolution operation, the dot product between the permuted input features ${ \bar { P } } X$ and the permuted weights $P { \mathcal { W } } _ { d y n }$ remains mathematically invariant $\bar { ( P X \circledast P ) } \mathcal { W } _ { d y n } = X \circledast \bar { \mathcal { W } } _ { d y n } )$ . This inherently guarantees that the extracted feature representations remain stable and consistent, regardless of the random ordering of input channels in practical scenarios.

## 2.4. Overall Architecture and Integration

For compatibility with downstream fixed-array algorithms, LN and PReLU activation are adopted, with the overall architecture formulated as follows.

$$
Y = \text { PReLU } (\text { LayerNorm } (\text { Geo - DyncConv } (G, X)))\tag{8}
$$

This design maps variable-dimensional inputs to fixeddimensional outputs, which are then processed by subsequent fixed-array algorithms.

## 3. Experiments

## 3.1. Datasets

Simulated microphone-array datasets often suffer from severe real-world domain mismatch, which leads to performance degradation when models trained on such data are deployed in real acoustic scenarios. To improve model generalization, the Real-recorded and Annotated Microphone Array Speech&Noise (RealMAN) dataset [14] is used to mitigate the simulation-to-real mismatch commonly observed in multichannel speech enhancement and localization. RealMAN provides large-scale real-world recordings captured with a 32-channel high-fidelity microphone array across diverse acoustic environments.

The dataset contains 83.7 hours of multichannel speech (divided into 64.0, 8.1, and 11.6 hours for training, validation, and test) recorded in 32 scenes and 144.5 hours of background noise (divided into 106.3, 16.0 and 22.2 hours for training, validation and test) recorded in 31 scenes. Recording environments include indoor, outdoor, semi-outdoor, and transportation scenarios. Sub-arrays extracted from the 32-channel array enable training and evaluation under variable array configurations.

Recording environments include indoor, outdoor, semioutdoor, and transportation scenarios. Speaker locations are annotated using an omnidirectional fisheye camera that automatically tracks the loudspeaker. For SE, the direct-path signal—obtained by filtering the source speech with an estimated direct-path propagation filter—is used as the target clean speech.

## 3.2. Implementation Setup

All models are trained on the same RealMAN dataset. For computational efficiency, all recordings are resampled to 8 kHz. A 256-point window and 128-sample frame shift are used to compute the STFT. During both training and evaluation, the input signals are segmented into 4-second utterances. To ensure a fair comparison, the segmentation boundaries are kept strictly identical across all models during testing.

BSRNN [15] is selected as the representative singlechannel speech enhancement (SE) baseline. For array-agnostic models, FaSNet-TAC [3] and USES2-comp [5] are adopted for comparison. In addition, SpatialNet [16] and TF-GridNet [17] are included as representative fixed-array SE baselines.

For the proposed Geo-DConv architecture, the basis dimension b is set to 8, the number of output channels O is 16, and spherical coordinates are adopted. The number of frequency bands in PE is configured as 6. For the TACT block, d<sub>hidden</sub> is set to 64, and a Transformer layer with 4 heads and 2 layers is employed. SDR, SI-SDR [18], PESQ [19], STOI [20], and DNSMOS [21] are employed as evaluation metrics in the subsequent experiments.

## 4. Results and Analysis

## 4.1. Impact of Fixed vs. Random Array Training

Two data-feeding strategies are used to evaluate the impact of array geometry configuration during training: utilizing a random 4-mic array versus a fixed-geometry 4-mic array. During the testing phase, all models are evaluated on the same fixedgeometry 4-mic array (microphone indices [0, 1, 5, 9]). As demonstrated in Table 1 (Nos. 3–10), fixed-array methods such as SpatialNet and TF-GridNet show the upper bound after training with the specific array. However, these models lead to a significant degradation in enhancement performance, especially in signal-level metrics like SDR and SI-SDR, when trained with random arrays, as they fail to reliably leverage the array structure.

For array-agnostic models like FaSNet-TAC and USES2- comp, random arrays occasionally yield slightly superior results. Because the structural design of these models predominantly focuses on single-channel spectra, they are inherently insensitive to variations in array geometry. Consequently, training with random arrays acts as a form of data regularization, subtly enhancing overall performance. In contrast, for fixedarray algorithms, training with a fixed-geometry array allows the model to implicitly capture the geometric information embedded within the data, thereby enabling more effective spatial modeling.

## 4.2. Performance Comparison of Array-Invariant Methods

Previous studies have confirmed that fixed-array algorithms yield superior enhancement for specific configurations, as geometric information is crucial for their performance. By incorporating the proposed Geo-DConv structure, the fixed-array algorithm can be adapted to handle randomized array configurations. As shown in Table 1, the proposed SpatialNet-Geo-DConv and TF-GridNet-Geo-DConv outperform the previous FaSNet-TAC previous FaSNet-TAC and USES2-comp models. In particular, SpatialNet-Geo-DConv achieves performance comparable to USES2-comp, but with significantly lower computational cost and fewer parameters. Through the comparison between Nos.11–12 and Nos.15–16, performance is further bolstered by training with a randomized number of microphones. This demonstrates that variable input channel counts help the model better learn to generate dynamic convolution weights.

To evaluate the adaptability of different Geometry-Invariant methods to various array structures, experiments are performed on varying numbers of microphones and array geometries, as shown in Table 2.When only a single microphone is used, all methods reduce to single-channel SE.The proposed SpatialNet-Geo-DConv and TF-GridNet-Geo-DConv achieve

Table 1: Performance and efficiency comparison on the RealMAN dataset. Models are grouped by their training and application sce narios. In the Geometry-Invariant setting (our main focus), the best results are highlighted in bold, and the second-best are underlined Our proposed methods are denoted in bold with ‘(Ours)’. Fixed-array methods serve as a geometry-specific upper bound.

<table><tr><td rowspan="2">No.</td><td rowspan="2">Model</td><td rowspan="2">#Params (M)</td><td rowspan="2">MACs (G/s)</td><td colspan="8">Evaluation Metrics</td></tr><tr><td>SDR</td><td>SI-SDR</td><td>PESQ</td><td>STOI</td><td>P808</td><td>SIG</td><td>BAK</td><td>OVRL</td></tr><tr><td colspan="12">Single-Channel Processing</td></tr><tr><td>1</td><td>No processing</td><td>-</td><td>-</td><td>-2.11</td><td>-9.47</td><td>1.54</td><td>0.72</td><td>2.39</td><td>1.99</td><td>1.84</td><td>1.49</td></tr><tr><td>2</td><td>BSRNN</td><td>16.9</td><td>21.15</td><td>5.31</td><td>-1.38</td><td>1.94</td><td>0.79</td><td>2.62</td><td>2.61</td><td>3.29</td><td>2.18</td></tr><tr><td colspan="12">Fixed-Array (Geometry-Specific Upper Bound)</td></tr><tr><td>3</td><td>FaSNet-TAC</td><td>2.7</td><td>9.76</td><td>5.13</td><td>-1.03</td><td>1.69</td><td>0.72</td><td>2.46</td><td>2.36</td><td>3.14</td><td>1.95</td></tr><tr><td>4</td><td>USES2-comp</td><td>2.5</td><td>70.26</td><td>9.36</td><td>4.78</td><td>2.56</td><td>0.87</td><td>2.77</td><td>3.14</td><td>3.49</td><td>2.65</td></tr><tr><td>5</td><td>SpatialNet</td><td>1.2</td><td>5.99</td><td>10.06</td><td>5.23</td><td>2.56</td><td>0.87</td><td>2.75</td><td>3.11</td><td>3.58</td><td>2.67</td></tr><tr><td>6</td><td>TF-GridNet</td><td>8.2</td><td>73.03</td><td>9.77</td><td>5.29</td><td>2.72</td><td>0.88</td><td>2.84</td><td>3.13</td><td>3.63</td><td>2.71</td></tr><tr><td colspan="12">Random 4-Mics Array</td></tr><tr><td>7</td><td>FaSNet-TAC</td><td>2.7</td><td>9.76</td><td>5.82</td><td>-1.09</td><td>1.72</td><td>0.73</td><td>2.46</td><td>2.41</td><td>3.04</td><td>1.95</td></tr><tr><td>8</td><td>USES2-comp</td><td>2.5</td><td>70.26</td><td>9.56</td><td>4.86</td><td>2.66</td><td>0.87</td><td>2.79</td><td>2.99</td><td>3.67</td><td>2.62</td></tr><tr><td>9</td><td>SpatialNet</td><td>1.2</td><td>5.99</td><td>9.41</td><td>3.77</td><td>2.55</td><td>0.87</td><td>2.76</td><td>3.13</td><td>3.50</td><td>2.64</td></tr><tr><td>10</td><td>TF-GridNet</td><td>8.2</td><td>73.03</td><td>9.00</td><td>3.78</td><td>2.57</td><td>0.87</td><td>2.79</td><td>3.06</td><td>3.55</td><td>2.63</td></tr><tr><td>11</td><td>SpatialNet-Geo-DConv (Ours)</td><td>1.3</td><td>6.08</td><td>9.77</td><td>3.92</td><td>2.46</td><td>0.87</td><td>2.73</td><td>3.19</td><td>3.28</td><td>2.59</td></tr><tr><td>12</td><td>TF-GridNet-Geo-DConv (Ours)</td><td>8.3</td><td>73.12</td><td>8.83</td><td>3.56</td><td>2.46</td><td>0.87</td><td>2.77</td><td>3.03</td><td>3.50</td><td>2.59</td></tr><tr><td colspan="12">Geometry-Invariant (primary comparison)</td></tr><tr><td>13</td><td>FaSNet-TAC</td><td>2.7</td><td>9.76</td><td>5.76</td><td>-0.81</td><td>1.74</td><td>0.73</td><td>2.48</td><td>2.48</td><td>3.18</td><td>2.05</td></tr><tr><td>14</td><td>USES2-comp</td><td>2.5</td><td>70.26</td><td>8.62</td><td>4.17</td><td>2.52</td><td>0.86</td><td>2.76</td><td>3.02</td><td>3.50</td><td>2.56</td></tr><tr><td>15</td><td>SpatialNet-Geo-DConv (Ours)</td><td>1.3</td><td>6.08</td><td>9.72</td><td>4.22</td><td>2.48</td><td>0.86</td><td>2.77</td><td>3.16</td><td>3.51</td><td>2.68</td></tr><tr><td>16</td><td>TF-GridNet-Geo-DConv (Ours)</td><td>8.3</td><td>73.12</td><td>9.05</td><td>3.90</td><td>2.59</td><td>0.87</td><td>2.83</td><td>3.21</td><td>3.62</td><td>2.77</td></tr></table>

Table 2: Generalization across array topologies (RealMAN) and cross-dataset evaluation (CHiME-4). The unprocessed ChiME-4 OVRL score is 1.42.

<table><tr><td>Array Config</td><td>SI-SDR(dB)</td><td>PESQ</td><td>OVRL</td></tr><tr><td colspan="4">USES2-comp</td></tr><tr><td>1 mic: {0}</td><td>-4.16</td><td>1.81</td><td>1.90</td></tr><tr><td>2 mics: {0,1}</td><td>3.55</td><td>2.46</td><td>2.54</td></tr><tr><td>5 mics: {0,1,3,5,7}</td><td>4.91</td><td>2.60</td><td>2.59</td></tr><tr><td>CHiME-4 (cross-dataset)</td><td>-</td><td>-</td><td>2.55</td></tr><tr><td colspan="4">SpatialNet-Geo-DConv (Ours)</td></tr><tr><td>1 mic: {0}</td><td>2.30</td><td>2.15</td><td>2.57</td></tr><tr><td>2 mics: {0,1}</td><td>3.97</td><td>2.45</td><td>2.66</td></tr><tr><td>5 mics: {0,1,3,5,7}</td><td>4.65</td><td>2.53</td><td>2.69</td></tr><tr><td>CHiME-4 (cross-dataset)</td><td>-</td><td>-</td><td>2.64</td></tr><tr><td colspan="4">TF-GridNet-Geo-DConv (Ours)</td></tr><tr><td>1 mic: {0}</td><td>2.76</td><td>2.37</td><td>2.70</td></tr><tr><td>2 mics: {0,1}</td><td>4.12</td><td>2.62</td><td>2.77</td></tr><tr><td>5 mics: {0,1,3,5,7}</td><td>4.54</td><td>2.67</td><td>2.79</td></tr><tr><td>CHiME-4 (cross-dataset)</td><td>-</td><td>-</td><td>2.73</td></tr></table>

significantly better enhancement performance than USES2- comp. As the number of microphones increases, all methods exhibit consistent performance improvements.Notably, the Geometry-Invariant methods are trained with a maximum of 4 microphones but can generalize well to 5-microphone and 6- microphone setups, including the 6-microphone real-recorded CHiME-4 test set [22]. The results demonstrate excellent generalization ability, with the DNSMOS OVRL improved from 1.42 to 2.64 and 2.73 for the two proposed methods on CHiME-4, respectively.

Although the models are trained only on the RealMAN dataset with a maximum of 4 microphones, it can generalize well to the 6-microphone real-world setup in CHiME-4 without any fine-tuning. This confirms that the proposed architecture can effectively capture general geometry-aware spatial patterns rather than overfitting to a specific array structure. Moreover, training on real-recorded data alleviates the sim-to-real domain mismatch, which is critical for practical deployment in real acoustic environments.

## 5. Conclusions

This paper reveals that while traditional fixed-array algorithms are inherently constrained by specific geometries, they can more effectively exploit spatial information. Building upon these insights, we propose the Geometry-Aware Dynamic Convolution module, which not only addresses the limitation of conventional convolutional layers for variable input dimensions but also explicitly incorporates array geometric priors. By introducing this module, conventional fixed-array methods can be converted into array-invariant SE systems, achieving performance improvements over existing array-invariant approaches. This work provides a new perspective for achieving array-invariant SE and represents an initial attempt to leverage explicit array structure information to assist multi-channel SE.

## 6. Acknowledgments

This work was supported in part by China NSFC project under Grants No. U25A20409, and in part by SJTU Med-X (Medicine & Engineering) Translational Research Grant (YG2025LC09).

## 7. Generative AI Use Disclosure

Generative AI tools were used solely for language polishing and grammatical improvement in the writing process. All scientific content, ideas, analysis, and conclusions are original and fully authored by the researchers. The authors take full responsibility for the final manuscript.

## 8. References

[1] X. Li, H. Xie, Z. Wang, Z. Zhang, L. Xiao, and L. Xie, “SenSE: Semantic-aware high-fidelity universal speech enhancement,” 2025. [Online]. Available: https://arxiv.org/abs/2509.24708

[2] J. Zhang, J. Yang, Z. Fang, Y. Wang, Z. Zhang, Z. Wang, F. Fan, and Z. Wu, “AnyEnhance: A unified generative model with prompt-guidance and self-critic for voice enhancement,” IEEE Transactions on Audio, Speech and Language Processing, vol. 33, pp. 3085–3098, 2025.

[3] Y. Luo, Z. Chen, N. Mesgarani, and T. Yoshioka, “End-toend microphone permutation and number invariant multi-channel speech separation,” in IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, pp. 6394– 6398.

[4] A. Pandey, B. Xu, A. Kumar, J. Donley, P. Calamia, and D. Wang, “TPARN: Triple-path attentive recurrent network for time-domain multichannel speech enhancement,” in IEEE International Con ference on Acoustics, Speech and Signal Processing (ICASSP), 2022, pp. 6497–6501.

[5] W. Zhang, J.-w. Jung, and Y. Qian, “Improving design of input condition invariant speech enhancement,” in IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2024, pp. 10 696–10 700.

[6] M. Tatarjitzky and B. Rafaely, “AmbiDrop: Array-agnostic speech enhancement using ambisonics encoding and dropoutbased learning,” Sep. 2025. [Online]. Available: http://arxiv.org/ abs/2509.14855

[7] W. Chen, J. Zhang, J. Yang, E. S. Chng, and X. Zhong, “UniArray: Unified spectral-spatial modeling for array-geometry-agnostic speech separation,” IEEE Signal Processing Letters, vol. 32, pp. 2164–2168, 2025.

[8] S. Darzi, T. Sieh Kiong, M. Tariqul Islam, H. Rezai Soleymanpour, and S. Kibria, “A memory-based gravitational search algorithm for enhancing minimum variance distortionless response beamforming,” Applied Soft Computing, vol. 47, pp. 103–118, 2016.

[9] M.-S. Baek, J.-H. Chang, and I. Cohen, “DNN-based geometryinvariant DOA estimation with microphone positional encoding and complexity gradual training,” IEEE Transactions on Audio, Speech and Language Processing, vol. 33, pp. 2360–2376, 2025.

[10] T. Ochiai, M. Delcroix, R. Ikeshita, K. Kinoshita, T. Nakatani, and S. Araki, “Beam-TasNet: Time-domain audio separation net work meets frequency-domain beamformer,” in IEEE Interna tional Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, pp. 6384–6388.

[11] W. Zhang, J. Shi, C. Li, S. Watanabe, and Y. Qian, “Closing the gap between time-domain multi-channel speech enhancement on real and simulation conditions,” in IEEE Workshop on Applica tions of Signal Processing to Audio and Acoustics (WASPAA), 2021, pp. 146–150.

[12] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, “NeRF: Representing scenes as neural radiance fields for view synthesis,” in European Conference on Computer Vision (ECCV), 2020.

[13] A. Luo, Y. Du, M. Tarr, J. Tenenbaum, A. Torralba, and C. Gan, “Learning neural acoustic fields,” in Advances in Neural Information Processing Systems, S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, Eds., vol. 35. Curran Associates, Inc., 2022, pp. 3165–3177.

[14] B. Yang, C. Quan, Y. Wang, P. Wang, Y. Yang, Y. Fang, N. Shao, H. Bu, X. Xu, and X. Li, “RealMAN: A real-recorded and annotated microphone array dataset for dynamic speech enhancement and localization,” in Advances in Neural Information Processing Systems, A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang, Eds., vol. 37. Curran Associates, Inc., 2024, pp. 105 997–106 019.

[15] Y. Luo and J. Yu, “Music source separation with band-split RNN,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 31, pp. 1893–1901, 2023.

[16] C. Quan and X. Li, “SpatialNet: Extensively learning spatial information for multichannel joint speech separation, denoising and dereverberation,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 32, pp. 1310–1323, 2024.

[17] Z.-Q. Wang, S. Cornell, S. Choi, Y. Lee, B.-Y. Kim, and S. Watanabe, “TF-GridNet: Integrating full- and sub-band modeling for speech separation,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 31, pp. 3221–3236, 2023.

[18] S. D. Jepsen, M. G. Christensen, and J. R. Jensen, “A study of the scale invariant signal to distortion ratio in speech separation with noisy references,” arXiv preprint arXiv:2508.14623, 2025. [Online]. Available: https://arxiv.org/abs/2508.14623

[19] A. Rix, J. Beerends, M. Hollier, and A. Hekstra, “Perceptual evaluation of speech quality (PESQ)-a new method for speech quality assessment of telephone networks and codecs,” in IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), vol. 2, 2001, pp. 749–752 vol.2.

[20] C. H. Taal, R. C. Hendriks, R. Heusdens, and J. Jensen, “A shorttime objective intelligibility measure for time-frequency weighted noisy speech,” in IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2010, pp. 4214–4217.

[21] C. K. Reddy, V. Gopal, and R. Cutler, “DNSMOS P. 835: A nonintrusive perceptual objective speech quality metric to evaluate noise suppressors,” in IEEE international conference on acoustics, speech and signal processing (ICASSP). IEEE, 2022, pp. 886–890.

[22] E. Vincent, S. Watanabe, A. A. Nugraha, J. Barker, and R. Marxer, “An analysis of environment, microphone and data simulation mismatches in robust speech recognition,” Computer Speech & Language, vol. 46, pp. 535–557, 2017.