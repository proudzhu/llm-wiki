Jiatong Li    Simon Doclo

###### Abstract

Recently, spatially selective non-linear filter (SSF) was proposed for target speaker extraction, utilizing the direction-of-arrival (DOA) of the target speaker as a spatial cue. To overcome its dependency on a fixed microphone array geometry, geometry-conditioned SSF (GCSSF) was proposed, which maps the target DOA and the microphone positions into abstract high-dimensional embeddings using positional encoding. As an alternative to these high-dimensional embeddings, in this paper we propose utilizing two spatial features incorporating acoustic propagation principles for geometry conditioning: 1) the steering vector of the target speaker, which captures inter-microphone phase differences, and 2) a spatial mask based on GCC-PHAT, which quantifies presence of the target speaker per time-frequency bin. These features are used as input to a geometry-conditioning encoder and integrated via a FiLM layer into the GCSSF system. Experimental results on circular and random arrays demonstrate that conditioning with spatial features improves target extraction performance compared to abstract high-dimensional embeddings, maintaining a clear performance advantage across a wide range of target DOA errors.

<sup>†</sup>

## 1 Introduction

Extracting a target speaker from a mixture of speakers and background noise remains a fundamental challenge in acoustic signal processing [^28]. To discriminate the target speaker from interfering sources, various cues have been proposed, such as enrollment utterances [^27] [^20], visual information [^12], and spatial features [^4] [^24] [^8] [^19]. In this paper, we focus on the spatially selective non-linear filter (SSF) proposed in [^24]. The SSF utilizes the target direction-of-arrival (DOA) as a spatial cue and uses Long Short-Term Memory (LSTM) layers to estimate a complex-valued mask that is applied to the reference microphone signal to extract the target speaker.

Despite its effectiveness, a limitation of the standard SSF is its inherent dependency on the fixed microphone array geometry considered during training. Recently, geometry-agnostic systems have been proposed for noise reduction [^7] [^22] [^26] [^10], blind speaker separation [^11], and target speaker extraction [^23] [^9]. While the system in [^23] is restricted to a fixed look direction, the geometry-conditioned SSF (GCSSF) system in [^9] allows for arbitrary DOA-steered extraction. The GCSSF system utilizes microphone positional encoding (MPE) [^2] to map the target DOA and microphone positions into abstract high-dimensional sinusoidal embeddings.

![[raw/papers/li-2026-geometry-conditioned-tse/figures/fig1.png|Refer to caption]]

Figure 1: Geometry-conditioned spatially selective filter (GCSSF) system using different features for array geometry conditioning. The gray block highlights the computation of these features ( 𝐏 MPE \\mathbf{P}\_{\\text{MPE}}, TSV \\mathbf{P}\_{\\text{TSV}}, and Mask \\mathbf{P}\_{\\text{Mask}} ). The features are encoded and then integrated via a FiLM layer.

As an alternative to these abstract embeddings, in this paper we propose utilizing two spatial features for geometry conditioning, which incorporate acoustic propagation principles into the conditioning mechanism (see Fig. 1). The spatial features are: 1) the target steering vector (TSV), calculated from the time differences of arrival, which captures the phase shifts of the target signal across the microphones; and 2) a spatial mask based on the generalized cross-correlation with phase transform (GCC-PHAT) [^1], which quantifies target presence per time-frequency bin. Similar to the MPE features in [^9], these features are used as input to the geometry-conditioning branch of the GCSSF, which includes an encoder and a Feature-wise Linear Modulation (FiLM) layer [^14]. In the experimental evaluation, the proposed GCSSF systems using the proposed spatial features as well as the baseline SSF and the GCSSF-MPE system are trained on random arrays and evaluated on both circular and random arrays. Experimental results demonstrate that conditioning the network with explicit spatial features consistently outperforms the baselines across all evaluated metrics, with the TSV feature yielding the best performance. Furthermore, a sensitivity analysis demonstrates that the proposed systems maintain better target speaker extraction performance than the baseline systems for target DOA errors up to $20^{\circ}$.

## 2 Geometry-conditioned Spatially Selective Non-linear Filter

In this section, we review the geometry-conditioned spatially selective non-linear filter (GCSSF) for target speaker extraction [^9]. We consider an acoustic scenario with $J$ speakers and background noise in a reverberant room, where one of the speakers is considered as the target speaker. The sound sources are recorded by an arbitrary planar array with $M$ omni-directional microphones, where the polar coordinates of the $m$ -th microphone relative to the array centroid are denoted by $(d_{m},\varphi_{m})$.

In the short-time Fourier transform (STFT) domain, the observed noisy speech signal at the $m$ -th microphone for frequency bin $k\in[1,K]$ and time frame $l\in[1,L]$ is denoted by $Y_{m}(k,l)$, where $K$ and $L$ denote the number of frequency bins and time frames, respectively. By stacking the signals from all microphones, the noisy speech vector $\mathbf{Y}(k,l)=[Y_{1}(k,l),Y_{2}(k,l),...,Y_{M}(k,l)]^{\text{T}}\in\mathbb{C}^{M}$ is given by

$$
\mathbf{Y}(k,l)=\mathbf{X}(k,l)+\mathbf{V}(k,l),
$$

where $\mathbf{X}(k,l)\in\mathbb{C}^{M}$ denotes the target speech vector and $\mathbf{V}(k,l)\in\mathbb{C}^{M}$ represents the combination of interfering speakers and background noise. Both vectors are defined similarly to $\mathbf{Y}(k,l)$.

The goal is to recover the reverberant target speech component $X_{1}(k,l)$ from the noisy speech vector $\mathbf{Y}(k,l)$, with the first microphone chosen as the reference microphone without loss of generality. To achieve this, the GCSSF estimates a complex mask $\mathcal{M}(k,l)$, which is applied to the noisy reference microphone signal $Y_{1}(k,l)$, i.e.,

$$
\hat{X}_{1}(k,l)=\mathcal{M}(k,l)Y_{1}(k,l).
$$

Fig. 1 depicts the block diagram of the GCSSF system, which consists of an extraction branch and a geometry-conditioning branch. The extraction branch has the same structure as the baseline SSF system [^24], i.e., a frequency-domain LSTM (F-LSTM), a time-domain LSTM (T-LSTM), and a linear layer to jointly process spatial, spectral, and temporal information. In addition, the target DOA $\theta$ is used as a conditioning input to the F-LSTM layer. To enable generalization to different microphone array geometries, the geometry-conditioning branch processes features based on the array geometry by an encoder, whose output is utilized by a FiLM layer after F-LSTM to modulate the intermediate representations within the extraction branch. In [^9], a microphone positional encoding (MPE) scheme directly maps the microphone coordinates and the target DOA into high-dimensional sinusoidal embeddings without requiring learnable parameters. The positional encodings for the $m$ -th microphone and the target DOA are given by

$$
\mathbf{p}_{m}=d_{m}\begin{bmatrix}\cos(2\pi\sigma\mathbf{v}+\varphi_{m})\\
\sin(2\pi\sigma\mathbf{v}+\varphi_{m})\end{bmatrix}\in\mathbb{R}^{Q},
$$
 
$$
\mathbf{p}_{\text{DOA}}=\begin{bmatrix}\cos(2\pi\sigma\mathbf{v}+\theta)\\
\sin(2\pi\sigma\mathbf{v}+\theta)\end{bmatrix}\in\mathbb{R}^{Q},
$$

where $\mathbf{v}=\frac{2}{Q}[0,1,...,\frac{Q}{2}-1]^{\text{T}}$, and $\sigma$ and $Q$ are constant hyperparameters. The MPE feature $\mathbf{P}_{\text{MPE}}$ is formed by concatenating the positional encodings for all microphones with the positional encoding for the target DOA, i.e.,

$$
\boxed{\mathbf{P}_{\text{MPE}}=[\mathbf{p}_{1},\mathbf{p}_{2},\dots,\mathbf{p}_{M},\mathbf{p}_{\text{DOA}}]\in\mathbb{R}^{Q\times(M+1)}}
$$

For a given batch size $B$, the MPE feature is reshaped to $[B,M+1,Q]$ before being passed to the geometry-conditioning branch.

While this feature provides the network with spatial coordinates, it does not explicitly utilize spatial features derived from acoustic propagation principles. Consequently, the network may need to implicitly learn the relationship between inter-microphone phase differences, the target DOA and the array geometry, potentially limiting extraction performance.

## 3 Explicit Spatial Features for Geometry Conditioning

To address the potential limitations of the positional encodings, in this paper we propose utilizing two explicit spatial features incorporating acoustic propagation principles for geometry conditioning. The first feature is the target steering vector (section 3.1), whereas the second feature is a spatial mask based on GCC-PHAT (section 3.2).

### 3.1 Target Steering Vector

To capture the physical relationship between the target speaker and the microphone array, the target steering vector is computed from the array geometry and the target DOA. Assuming a far-field propagation model, the time difference of arrival (TDOA) between the $m$ -th microphone and the centroid of the microphone array for a target speaker at DOA $\theta$ is given by $\tau_{m}=\frac{d_{m}\cos(\varphi_{m}-\theta)}{c}$, where $c$ is the speed of sound. Relative to the reference microphone, the target steering vector at frequency $f_{k}$ for the $k$ -th frequency bin is given by:

$$
\boxed{\mathbf{d}(k)=[1,e^{\jmath 2\pi f_{k}(\tau_{2}-\tau_{1})},...,e^{\jmath 2\pi f_{k}(\tau_{M}-\tau_{1})}]^{\text{T}}\in\mathbb{C}^{M}}
$$

where $\jmath$ denotes the imaginary unit. This vector describes the frequency-dependent phase differences across the array for the direct path of the target speaker. As is well known from array signal processing [^25], this steering vector can be used in a delay-and-sum beamformer that spatially aligns and extracts the target speaker via the linear operation $\mathbf{d}^{H}\mathbf{Y}$. This demonstrates that the complex conjugate of the steering vector, $\mathbf{d}^{*}(k)$, defines the phase compensation required to spatially align the microphone signals to the target DOA. Our first geometry-conditioning feature $\mathbf{P}_{\text{TSV}}$ is constructed by computing and stacking $\mathbf{d}^{*}(k)$ across all $K$ frequency bins. This yields a tensor of shape $[B,M,K]$, explicitly guiding the neural network to focus on the target DOA.

### 3.2 GCC-PHAT Spatial Mask

The target steering vector provides a purely geometric feature because it only relies on the microphone coordinates and the target DOA. It is calculated independently of the observed multichannel microphone signals, meaning it cannot capture target speaker activity. To explore whether the network benefits from a signal-dependent spatial feature that indicates the presence of the target speaker in each time-frequency bin, we propose to utilize the GCC-PHAT spatial mask [^1] as an alternative conditioning feature. This feature is conceptually related to classical spectral post-filtering [^5].

To construct the spatial mask, the microphone signals are first spatially aligned toward the target DOA by applying the complex conjugate of the target steering vector in (6). The TDOA-compensated signal, denoted as $\mathbf{S}(k,l)=[S_{1}(k,l),S_{2}(k,l),...,S_{M}(k,l)]^{\text{T}}\in\mathbb{C}^{M}$, is computed as

$$
\mathbf{S}(k,l)=\mathbf{d}^{*}(k)\odot\mathbf{Y}(k,l),
$$

where $\odot$ denotes element-wise multiplication. Subsequently, for any given pair of TDOA-compensated microphone channels $i$ and $j$, the instantaneous GCC-PHAT $\Psi_{ij}(k,l)$ is computed as

$$
\Psi_{ij}(k,l)=\frac{S_{i}(k,l)S_{j}^{*}(k,l)}{|S_{i}(k,l)||S_{j}(k,l)|}.
$$

To aggregate these phase correlations across the entire array, the GCC-PHAT spatial mask $I(k,l)$ is obtained by averaging the real part of $\Psi_{ij}(k,l)$ over all $\frac{M(M-1)}{2}$ unique microphone pairs, i.e.,

$$
\boxed{I(k,l)=\frac{2}{M(M-1)}\text{Re}\left(\sum_{i=1}^{M}\sum_{j=i+1}^{M}\Psi_{ij}(k,l)\right)}
$$

Theoretically, $I(k,l)$ serves as an indicator of the target presence within a specific time-frequency bin. When the target speaker is the dominant active source, the aligned signals $S_{i}(k,l)$ and $S_{j}(k,l)$ are in-phase, causing $I(k,l)$ to approach $1$. Conversely, when a time-frequency bin is dominated by interfering speakers from a different DOA than the target speaker, reverberation or noise, the phase alignment degrades, and $I(k,l)$ decreases. The second geometry-conditioning feature, $\mathbf{P}_{\text{Mask}}$, aggregates $I(k,l)$ across the $K$ frequency bins for each individual time step. To ensure online processing, the network processes this feature frame-by-frame, which corresponds to an input tensor of shape $[BL,1,K]$ where all $L$ frames are treated independently.

## 4 Experiments

This section first presents the experimental setup, including the training and evaluation datasets, the network structure, and the training procedure. Then, the experimental results are presented and discussed, evaluating the target speaker extraction performance of the GCSSF systems utilizing the explicit spatial features for geometry conditioning. The performance is compared against two baseline systems: the original SSF system without geometry conditioning [^24] and the GCSSF system using the MPE feature in (5) for geometry conditioning (GCSSF-MPE) [^9].

### 4.1 Datasets

To evaluate the proposed systems, acoustic environments were simulated using the pyroomacoustics library [^18], with room dimensions and reverberation times ($T_{60}$) uniformly sampled from the ranges in Fig. 2 (right). To assess target speaker extraction performance, circular and random arrays with $M=5$ microphones were considered (see Fig. 3). These arrays were positioned randomly in the horizontal plane at a height of 1.6 m with a random rotation. For the circular arrays, the microphones were evenly spaced along a circle with a diameter of $10$ cm. For the random arrays, microphone positions were sampled uniformly within a 10 cm × 10 cm region with a minimum microphone spacing of 2 mm, and a reference microphone was randomly chosen. As illustrated in Fig. 2 (left), two to six speakers were placed at a height of 1.6 m, ensuring a minimum $20^{\circ}$ angular separation between the target and all interfering speakers. The remaining angular space outside this target exclusion zone was divided into equal sectors corresponding to the number of interferers, with the DOA of each interferer randomly sampled within a distinct sector. Additionally, all speakers were positioned at least 50 cm apart from one another. Acoustic datasets were generated using 16 kHz speech signals from the Wall Street Journal (WSJ0) corpus [^6], which was divided into disjoint speaker sets following the split defined in [^24]. The training and validation sets comprise 30 h and 1 h of data, respectively. Similarly, 1 h of data was generated for each array geometry for evaluation. The mixture signals were generated such that the reverberant signal-to-interference ratio at the reference microphone was between -5 dB and 10 dB. In addition, diffuse noise synthesized from the QUT noise dataset [^3] using the ANF generator [^13] was added such that the signal-to-noise ratio at the reference microphone was 15 dB.

### 4.2 Network and Training

Following the framework in [^9], the STFT is computed using a frame length of 512 (corresponding to 32 ms) with 50% overlap and a square-root Hann window for both analysis and synthesis. The network architecture for all considered systems is the same as that of the GCSSF-MPE system in [^9], except for the number of encoder output channels, which matches the dimensions of the input geometry-conditioning features. Specifically, for the proposed $\mathbf{P}_{\text{TSV}}$ and $\mathbf{P}_{\text{Mask}}$ features, the output channels of the three 1D convolutional (Conv1d) layers are set to 64, 512 and 1024, respectively. For the baseline GCSSF-MPE system, the positional encoding hyperparameters are set to $\sigma=4$ and $Q=514$, and the Conv1d output channels are adjusted to 64, 1024, and 514. This adjustment results in a comparable number of parameters in GCSSF systems for a fair evaluation.

The training procedure follows the strategy in [^9]. All networks were trained to minimize a joint time- and frequency-domain loss function [^24], i.e.,

$$
\mathcal{L}\hskip-1.42262pt=\hskip-1.42262pt\frac{\beta}{N}\hskip-2.84526pt\sum_{n=1}^{N}\hskip-1.42262pt|x_{1}(n)\hskip-0.56905pt-\hskip-0.56905pt\hat{x}_{1}(n)|\hskip-0.28453pt+\hskip-0.28453pt\frac{1}{KL}\hskip-2.84526pt\sum_{l=1}^{L}\hskip-1.99168pt\sum_{k=1}^{K}\hskip-1.42262pt\left||X_{1}(k,l)|\hskip-2.27621pt-\hskip-2.27621pt|\hat{X}_{1}(k,l)|\right|,\hskip-2.84526pt
$$

where $x_{1}(n)$ denotes the reverberant time-domain target speech signal at the reference microphone, and $\hat{x}_{1}(n)$ denotes its estimate reconstructed via inverse STFT and overlap-add. Here, $n$ is the time sample index, $N$ is the total number of samples, and the scalar weighting factor is set to $\beta=10$. All networks were trained on random arrays, while performance was evaluated on circular and random arrays. To improve robustness against target DOA errors and microphone position mismatches, random perturbations were introduced during training: the target DOA was corrupted by an angular error drawn from $\mathcal{U}(-4^{\circ},4^{\circ})$, and each microphone position was perturbed by an error drawn from $\mathcal{U}(-4\penalty\ \text{mm},4\penalty\ \text{mm})$. All networks were trained for 500 epochs with a batch size of 16 using the Adam optimizer (initial learning rate 0.001). A multi-step scheduler decayed the learning rate by a factor of 0.75 every 50 epochs up to epoch 400, and gradients were clipped to a maximum $l_{2}$ -norm of 1 to ensure stable convergence.

![[raw/papers/li-2026-geometry-conditioned-tse/figures/fig2.png|Refer to caption]]

Figure 2: Illustration of the simulation setup and the room characteristics. The speakers are located in the gray region.

![[raw/papers/li-2026-geometry-conditioned-tse/figures/fig3.jpg|Refer to caption]]

Refer to caption

Table 1: Average SI-SDR (dB), PESQ, ESTOI, and DNSMOS overall scores (with standard deviations) for the unprocessed microphone signals, the baseline systems (SSF and GCSSF-MPE) and the proposed GCSSF systems using explicit spatial features (GCSSF-TSV and GCSSF-Mask). All systems are trained on random arrays and evaluated on both random and circular arrays.

<table><tbody><tr><td rowspan="2">System</td><td colspan="4">Random</td><td colspan="4">Circular</td></tr><tr><td>SI-SDR</td><td>PESQ</td><td>ESTOI</td><td>DNSMOS</td><td>SI-SDR</td><td>PESQ</td><td>ESTOI</td><td>DNSMOS</td></tr><tr><td>Unprocessed</td><td>2.21 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>4.24)</td><td>1.27 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.19)</td><td>0.52 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.14)</td><td>1.18 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.19)</td><td>2.19 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>4.28)</td><td>1.27 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.20)</td><td>0.52 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.14)</td><td>1.21 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.22)</td></tr><tr><td>SSF <sup><a href="#fn:24">24</a></sup></td><td>6.78 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>5.26)</td><td>1.79 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.49)</td><td>0.66 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.16)</td><td>1.85 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.56)</td><td>7.00 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>5.25)</td><td>1.80 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.50)</td><td>0.66 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.16)</td><td>1.86 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.56)</td></tr><tr><td>GCSSF-MPE <sup><a href="#fn:9">9</a></sup></td><td>7.77 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>5.01)</td><td>1.96 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.55)</td><td>0.69 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.16)</td><td>1.95 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.58)</td><td>7.79 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>4.93)</td><td>1.95 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.55)</td><td>0.69 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.15)</td><td>1.93 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.57)</td></tr><tr><td>GCSSF-TSV (Proposed)</td><td>9.43 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>3.96)</td><td>2.27 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.55)</td><td>0.75 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.12)</td><td>2.07 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.59)</td><td>9.87 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>3.52)</td><td>2.33 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.54)</td><td>0.77 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.11)</td><td>2.08 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.59)</td></tr><tr><td>GCSSF-Mask (Proposed)</td><td>8.45 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>4.33)</td><td>2.10 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.54)</td><td>0.72 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math> 0.14)</td><td>1.99 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.60)</td><td>8.86 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>4.00)</td><td>2.17 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.54)</td><td>0.74 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math> 0.13)</td><td>2.02 (<math><semantics><mo>±</mo> <annotation>\pm\,</annotation></semantics></math>0.58)</td></tr></tbody></table>

### 4.3 Experimental Results

In this section, we present an experimental evaluation of the proposed GCSSF system utilizing explicit spatial features. First, we compare their target speaker extraction performance against the baseline SSF and GCSSF-MPE systems. Second, we analyze their robustness against inaccuracies in the input target DOA. Target extraction performance is evaluated using three standard intrusive metrics: the scale-invariant signal-to-distortion ratio (SI-SDR) [^17], the wide-band perceptual evaluation of speech quality (PESQ) [^16], and the extended short-time objective intelligibility (ESTOI) [^21]. For these metrics, the reverberant target speech component at the reference microphone is used as the ground-truth reference signal. Furthermore, to evaluate perceptual speech quality without a reference, the overall deep noise suppression mean opinion score (DNSMOS) [^15] is reported.

Table 1 compares the performance of the proposed systems (GCSSF-TSV and GCSSF-Mask) against the baseline systems (SSF and GCSSF-MPE) for random and circular arrays. Compared to the baseline SSF system, the GCSSF-MPE system achieves better performance across all metrics, indicating that mapping the target DOA and the microphone coordinates into sinusoidal embeddings helps the network to infer the relationship between inter-microphone phase differences, target DOA, and array geometry. Despite these improvements, providing the network with explicit spatial features yields significantly better results. Both proposed systems, GCSSF-TSV and GCSSF-Mask, consistently outperform the baseline systems across all metrics. Because the explicit spatial features are derived from acoustic propagation principles, they provide a highly informative representation that explicitly connects the inter-microphone phase differences in the multichannel signals with the target DOA and the array geometry. This simplifies the network’s learning task, yielding a fundamental performance advantage. Most notably, the GCSSF-TSV system achieves the best overall performance. On random arrays, it delivers substantial improvements of 1.66 dB in SI-SDR, 0.31 in PESQ, 0.06 in ESTOI, and 0.12 in DNSMOS over the GCSSF-MPE baseline. Although the spatial mask $\mathbf{P}_{\text{Mask}}$ incorporates additional input multichannel signal and indicates the presence of the target speaker, it performs worse than the target steering vector $\mathbf{P}_{\text{TSV}}$. This is likely because the TDOA compensation assumes direct-path propagation; consequently, reverberation degrades the phase alignment, leading to an inaccurate mask that suppresses time-frequency bins containing valid target speech. Furthermore, $\mathbf{P}_{\text{Mask}}$ is aggregated into a single-channel representation. Unlike the multichannel feature $\mathbf{P}_{\text{TSV}}$, it does not preserve inter-microphone phase information across the array, limiting the spatial information available to the network. Evaluation on circular arrays demonstrates similar results to random arrays.

Aiming at investigating the robustness against target DOA errors, Fig. 4 shows the average PESQ scores of all considered systems evaluated on random arrays for different target DOA errors. The results demonstrate that the proposed systems (GCSSF-TSV and GCSSF-Mask) maintain a clear performance advantage over the baseline systems for target DOA errors up to $20^{\circ}$. As the target DOA error increases beyond $20^{\circ}$, the PESQ scores of the proposed systems are lower than those of the baseline systems. Because the proposed features are explicitly derived from the input target DOA, significant target DOA errors introduce severe phase mismatches and incorrect signal alignments in the target steering vector and the spatial mask. Consequently, the network is explicitly guided to focus on an incorrect DOA, suppressing the true target speaker. In contrast, the baseline GCSSF-MPE system does not rely on acoustic propagation principles, thereby avoiding the severe performance degradation caused by signal misalignments under large target DOA errors. Overall, while the proposed spatial features introduce a sensitivity to large target DOA errors, they achieve better target speaker extraction performance for target DOA errors up to $20^{\circ}$.

![[raw/papers/li-2026-geometry-conditioned-tse/figures/fig4.png|Refer to caption]]

Figure 4: Average PESQ of the baseline systems (SSF and GCSSF-MPE) and the proposed GCSSF systems using explicit spatial features (GCSSF-TSV and GCSSF-Mask) for different target DOA errors. All systems are trained and evaluated on the random arrays.

## 5 Conclusions

In this paper, we addressed the limitations of abstract positional encodings in geometry-conditioned target speaker extraction by utilizing spatial features derived from acoustic propagation principles: the target steering vector (TSV) and the GCC-PHAT spatial mask. Unlike the baseline GCSSF-MPE system, which implicitly infers physical relationships from abstract encodings, the proposed systems use these explicit features to directly connect multichannel phase differences, the target DOA, and the array geometry. Experimental results demonstrate that the proposed systems consistently outperform the SSF and GCSSF-MPE baselines on both random and circular arrays. Furthermore, a sensitivity analysis on target DOA errors shows that the proposed systems maintain better target speaker extraction performance for target DOA errors up to $20^{\circ}$.

[^1]: D. Ayllón, A. Levi, and H. Silverman (2011) Real-time phase-isolation algorithm for speech separation. In Proc. European Signal Processing Conference, Barcelona, Spain, pp. 1342–1346. Cited by: §1, §3.2.

[^2]: M. Baek, J. Chang, and I. Cohen (2025) DNN-based geometry-invariant DOA estimation with microphone positional encoding and complexity gradual training. IEEE Trans. on Audio, Speech and Language Processing 33, pp. 2360–2376. Cited by: §1.

[^3]: D. Dean, S. Sridharan, R. Vogt, and M. Mason (2010) The QUT-NOISE-TIMIT corpus for the evaluation of voice activity detection algorithms. In Proc. Interspeech, Makuhari, Japan, pp. 3110–3113. Cited by: §4.1.

[^4]: M. Elminshawi, S. Raj Chetupalli, and E. A. P. Habets (2023) Beamformer-guided target speaker extraction. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing, Rhodes Island, Greece, pp. 1–5. Cited by: §1.

[^5]: S. Gannot and I. Cohen (2008) Adaptive beamforming and postfiltering. In Springer Handbook of Speech Processing, J. Benesty, M. M. Sondhi, and Y. A. Huang (Eds.), pp. 945–978. Cited by: §3.2.

[^6]: J. S. Garofolo, D. Graff, D. Paul, and D. Pallett (2007) CSR-I (WSJ0) Complete LDC93S6A. Linguistic Data Consortium, Philadelphia. Cited by: §4.1.

[^7]: A. Jukić, J. Balam, and B. Ginsburg (2023) Flexible multichannel speech enhancement for noise-robust frontend. In Proc. IEEE Workshop on Applications of Signal Processing to Audio and Acoustics, New Paltz, USA, pp. 1–5. Cited by: §1.

[^8]: J. Kienegger, A. Mannanova, H. Fang, and T. Gerkmann (2025) Self-steering deep non-linear spatially selective filters for efficient extraction of moving speakers under weak guidance. In Proc. IEEE Workshop on Applications of Signal Processing to Audio and Acoustics, Tahoe City, USA, pp. 1–5. Cited by: §1.

[^9]: J. Li, W. Middelberg, and S. Doclo (2026) Flexible multi-channel target speaker extraction using geometry-conditioned spatially selective non-linear filters. In Proc. International Workshop on Acoustic Signal Enhancement, Cremona, Italy. Cited by: §1, §1, §2, §2, §4.2, §4.2, Table 1, §4.

[^10]: Z. Liu, W. Zhang, C. Li, and Y. Qian (2026) Towards array-invariant speech enhancement via geometry-aware dynamic convolution. In Proc. Interspeech, Sydney, Australia. Cited by: §1.

[^11]: Y. Masuyama, K. Saijo, F. Paissan, J. Han, M. Delcroix, R. Aihara, F. G. Germain, G. Wichern, and J. Le Roux (2026) FlexIO: flexible single- and multi-channel speech separation and enhancement. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing, Barcelona, Spain, pp. 14417–14421. Cited by: §1.

[^12]: D. Michelsanti, Z. Tan, S. Zhang, Y. Xu, M. Yu, D. Yu, and J. Jensen (2021) An overview of deep-learning-based audio-visual speech enhancement and separation. IEEE/ACM Trans. on Audio, Speech, and Language Processing 29, pp. 1368–1396. Cited by: §1.

[^13]: D. Mirabilii, S. J. Schlecht, and E. A. P. Habets (2021) Generating coherence-constrained multisensor signals using balanced mixing and spectrally smooth filters. The Journal of the Acoustical Society of America 149, pp. 1425–1433. Cited by: §4.1.

[^14]: E. Perez, F. Strub, H. de Vries, V. Dumoulin, and A. Courville (2018) FiLM: visual reasoning with a general conditioning layer. Proc. AAAI Conference on Artificial Intelligence 32. Cited by: §1.

[^15]: C. K. A. Reddy, V. Gopal, and R. Cutler (2021) DNSMOS: a non-intrusive perceptual objective speech quality metric to evaluate noise suppressors. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing, Toronto, Canada, pp. 6493–6497. Cited by: §4.3.

[^16]: A. W. Rix, J. G. Beerends, M. P. Hollier, and A. P. Hekstra (2001) Perceptual evaluation of speech quality (PESQ)-a new method for speech quality assessment of telephone networks and codecs. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing, Salt Lake City, USA, pp. 749–752. Cited by: §4.3.

[^17]: J. L. Roux, S. Wisdom, H. Erdogan, and J. R. Hershey (2019) SDR – half-baked or well done?. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing, Brighton, UK, pp. 626–630. Cited by: §4.3.

[^18]: R. Scheibler, E. Bezzam, and I. Dokmanić (2018) Pyroomacoustics: a python package for audio room simulation and array processing algorithms. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing, Calgary, Canada, pp. 351–355. Cited by: §4.1.

[^19]: S. S. Shetu, E. A. P. Habets, and A. Brendel (2026) GAN-based multi-microphone spatial target speaker extraction. In Proc. International Workshop on Acoustic Signal Enhancement, Cremona, Italy. Cited by: §1.

[^20]: R. Sinha, C. Rollwage, and S. Doclo (2025) Real-time single-channel speaker-conditioned target speaker extraction using TCN-conformer with efficient self-attention mechanisms. In Proc. European Signal Processing Conference, Palermo, Italy, pp. 476–480. Cited by: §1.

[^21]: C. H. Taal, R. C. Hendriks, R. Heusdens, and J. Jensen (2010) A short-time objective intelligibility measure for time-frequency weighted noisy speech. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing, Dallas, Texas, USA, pp. 4214–4217. Cited by: §4.3.

[^22]: M. Tammen, T. Ochiai, M. Delcroix, T. Nakatani, S. Araki, and S. Doclo (2024) Array geometry-robust attention-based neural beamformer for moving speakers. In Proc. Interspeech, Kos, Greece, pp. 3345–3349. Cited by: §1.

[^23]: M. Tatarjitzky and B. Rafaely (2026) AmbiDrop: array-agnostic speech enhancement using ambisonics encoding and dropout-based learning. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing, Barcelona, Spain, pp. 14732–14736. Cited by: §1.

[^24]: K. Tesch and T. Gerkmann (2024) Multi-channel speech separation using spatially selective deep non-linear filters. IEEE/ACM Trans. on Audio, Speech, and Language Processing 32, pp. 542–553. Cited by: §1, §2, §4.1, §4.2, Table 1, §4.

[^25]: B.D. Van Veen and K.M. Buckley (1988) Beamforming: a versatile approach to spatial filtering. IEEE ASSP Magazine 5 (2), pp. 4–24. Cited by: §3.1.

[^26]: D. Zhang, A. I. Mezza, F. Miotello, J. Chen, M. Wang, F. Antonacci, and A. Bernardini (2026) Eigenbeam-feature-based multi-order encoder for geometry-agnostic speech enhancement. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing, Barcelona, Spain, pp. 22192–22196. Cited by: §1.

[^27]: K. Zhang, J. Li, S. Wang, Y. Wei, Y. Wang, Y. Wang, and H. Li (2025) Multi-level speaker representation for target speaker extraction. In Proc. IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Hyderabad, India, pp. 1–5. Cited by: §1.

[^28]: K. Zmolikova, M. Delcroix, T. Ochiai, K. Kinoshita, J. Černocký, and D. Yu (2023) Neural target speech extraction: an overview. IEEE Signal Processing Magazine 40, pp. 8–29. Cited by: §1.