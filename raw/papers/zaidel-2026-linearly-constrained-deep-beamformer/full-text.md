###### Abstract

We propose a deep beamforming framework for enhancing target speaker(s) in multi-speaker environments. A deep neural network (DNN) is trained to estimate beamforming weights directly from noisy multichannel inputs while satisfying linear spatial constraints through an adaptive multi-term loss inspired by the augmented Lagrangian framework. The loss combines signal reconstruction with penalties that enforce a distortionless response toward the target and suppress the interference subspace. The model is further guided by the target relative transfer function (RTF) and the estimated interference subspace. The proposed model can direct a beam toward the target speaker while directing nulls toward the interfering sources, achieving superior overall enhancement performance compared with the classical LCMV beamformer constructed by the same estimated spatial signatures. Furthermore, compared with the LCMV beamformer, the proposed model produces more controlled sidelobes and improved background-noise attenuation.

## 1 Introduction

Multichannel beamforming enables spatial filtering of concurrent speakers using microphone arrays and is widely used for speech enhancement in complex acoustic environments. In multi-speaker scenarios, the challenge is not only to enhance the desired speaker but also to suppress interfering sources using directional filtering and null steering. In this work, we propose a fully DNN-based beamforming framework that combines deep neural networks with linearly constrained spatial objectives for multi-speaker enhancement.

Linearly constrained beamforming provides a principled framework for controlling the spatial response of microphone arrays through explicit constraints on the beamformer weights. A special-case formulation is the minimum variance distortionless response (MVDR) beamformer [^8] [^9], which enforces a distortionless response to a desired speaker while minimizing the output noise and interference power. In the more general case, the linearly constrained minimum variance (LCMV) beamformer [^7] extends this formulation by incorporating multiple linear constraints, enabling explicit control over the spatial response, including preservation of the target signal(s) and placement of nulls toward interfering sources [^15] [^21] [^16].

These formulations rely on accurate knowledge of the sources’ spatial signatures, which define the desired constraints. In practice, such spatial information is commonly represented using the relative transfer function (RTF), which captures both direct-path and reverberant propagation effects. Several studies have shown that RTF-based beamforming yields improved speech quality compared with approaches that rely solely on direct-path models [^8] [^22]. In principle, LCMV beamforming can achieve perfect interference cancellation when accurate target RTFs and either accurate interfering-speaker RTFs or an accurate interference subspace are available. However, in practice, its performance critically depends on reliable estimation of these spatial signatures, motivating the use of robust RTF-based formulations [^17].

Recently, DNN-based beamformers have achieved strong performance by jointly learning spatial and spectral representations from data [^14] [^19]. However, these methods are often not directly interpretable, motivating approaches that explicitly analyze and encourage spatial selectivity in multichannel processing [^3] [^23] [^5] [^12]. Prior works have incorporated RTF information either by estimating classical beamformer coefficients [^9] [^20] [^2] or by embedding it as a spatial filter within deep architectures [^13]. Building on these ideas, our previous work [^25] demonstrated that guiding a DNN-based beamformer with time-varying RTF estimates improves the spatial consistency and directional behavior of learned beamformers. Nevertheless, such approaches only enforce spatial guidance toward the desired speaker, without explicitly constraining the response toward interfering sources, and therefore cannot reliably guarantee directional null steering.

Several works have explored incorporating directional constraints and null steering into learning-based beamforming frameworks. Works such as [^4] [^24] combine deep learning with classical constrained beamforming formulations, where neural networks estimate spatial or statistical quantities required for beamforming and interference representations, while the final spatial filtering is still performed using analytical model-based beamformers. In parallel, works such as [^10], proposed in the context of wireless communications, train DNNs to directly predict beamforming weights that imitate the behavior of constrained beamformers and achieve directional null control. However, in such approaches, spatial constraints are not explicitly incorporated into the learning objective; instead, they are either enforced analytically via a separate beamforming stage or approximated implicitly through supervised training.

Our work builds upon the frameworks presented in [^5] [^25], which learn beamforming weights using a DNN while preserving the beamforming structure. While both works demonstrate strong enhancement capabilities, including dynamic binaural beamforming in [^25], they do not explicitly enforce spatial constraints and therefore cannot reliably achieve directional null steering toward interfering sources.

In contrast, we propose a fully DNN-based beamformer optimized to satisfy linear constraints for target speaker extraction and interference suppression. Specifically, we design an adaptive multi-term loss function, reminiscent of the LCMV criterion, that combines a signal reconstruction objective with constraint-driven penalties that enforce a distortionless response toward the target and null out the interference subspace. The training process follows an augmented Lagrangian-inspired approach, where the weights of the constraint terms are gradually increased during training, enabling the network to learn both accurate signal reconstruction and spatially selective filtering. To further guide the learning process, the model is provided with spatial information in the form of the target RTF and an estimated interference subspace, which together define the constraint structure and encourage spatially selective beamforming behavior.

Throughout this work, we evaluate the learned beamformer under three configurations: (i) guidance using estimated target RTFs and interference subspaces (referred to as the “Estimated RTF” model), (ii) a model without RTF guidance (“No RTF”), and (iii) guidance using the oracle RTFs of the target and interfering speakers (“Oracle RTF”).

## 2 Problem Formulation

In the short-time Fourier transform (STFT) domain, the multichannel mixture signal is modeled as

$$
\mathbf{y}(l,k)=\mathbf{H}(k)\mathbf{s}(l,k)+\mathbf{n}(l,k)\in\mathbb{C}^{M\times 1},
$$

where $l$ and $k$ denote the time-frame and frequency-bin indices, respectively, and $M$ is the number of microphones. Here,

$$
\mathbf{s}(l,k)=\begin{bmatrix}s_{1}(l,k),\dots,s_{J}(l,k)\end{bmatrix}^{\top},
$$

represents the $J\leq M$ active speakers, and

$$
\mathbf{H}(k)=\begin{bmatrix}\mathbf{h}_{1}(k),\dots,\mathbf{h}_{J}(k)\end{bmatrix}
$$

comprises the acoustic transfer functions (ATFs) from each source to the microphones. The vector $\mathbf{n}(l,k)$ denotes additive noise. We apply the time-invariant spatial filter

$$
\hat{s}(l,k)=\mathbf{w}^{\mathrm{H}}(k)\mathbf{y}(l,k),
$$

where $\mathbf{w}(k)$ denotes the DNN based beamformer weights and $\hat{s}(l,k)$ is the beamformer output. The output is designed to estimate, through the optimization of a suitable loss function, a target signal defined as a linear combination of the sources of interest:

$$
s_{\rm target}(l,k)=\mathbf{g}^{\top}\mathbf{s}(l,k),
$$

where $\mathbf{g}\in\mathbb{R}^{J\times 1}$ is a weighting vector. Typically, the entries of $\mathbf{g}$ are ‘1’ for the desired source(s) and ‘0’ for all interference sources. In the proposed method, the beamformer weights are chosen to minimize the loss between $\hat{s}$ and $s_{\rm target}$, while satisfying a set of linear constraints.

## 3 Proposed Method

This section describes the proposed DNN-based beamforming framework. The model follows the U-Net architecture of [^5] [^25] and incorporates spatial guidance via estimates of the target speaker’s RTF and an interference subspace corresponding to the interfering speakers. The full architecture is shown in Fig. 1.

![Refer to caption](https://arxiv.org/html/2605.21141v1/figures/communication.png)

Multichannel noisy inputs STFT 𝐲 \\mathbf{y} RTF Estimation Attn. U - Net s ^ \\hat{s} ISTFT 𝐰 \\mathbf{w}

### 3.1 U-Net Model with Attention Fusion

We employ a U-Net architecture with an attention-based fusion frontend to integrate the spatial guidance information with the multichannel mixture. The target RTF and interference subspace are fused with the mixture signal through shared local attention blocks, and the resulting features are concatenated with the raw mixture to form the encoder input. The U-Net follows an encoder-decoder structure with skip connections and transposed-convolution decoder blocks, where attention is also applied over the skip connections [^5]. The final layer applies a fully connected projection along the frequency dimension, followed by complex-valued normalization and a learnable global gain scaling to produce the beamforming weights.

### 3.2 RTF Estimation

To estimate the static spatial signatures of the speakers, we employ the covariance whitening (CW) method for RTF estimation [^17]. Although the formulation in 5 is general, in this work we focus on single target extraction. Given $J$ active speakers, the objective is to preserve the target speaker while suppressing the remaining $J-1$ interfering speakers. To this end, the same CW procedure is applied to frame sets corresponding to different source activity patterns, assuming such frame annotations are available. Frames in which only the target speaker is active are used to estimate the target RTF, whereas frames containing only interfering speakers are used to estimate the interference subspace. In addition, noise-only frames are assumed to be available for estimating the noise covariance matrix.

#### 3.2.1 Covariance-Whitening

Let $\mathcal{V}_{n}$ denote the set of frames in which only noise is present. The noise covariance matrix is then estimated as

$$
\hat{\mathbf{\Phi}}_{\mathbf{nn}}(k)=\frac{1}{|\mathcal{V}_{n}|}\sum_{l\in\mathcal{V}_{n}}\mathbf{y}(l,k)\mathbf{y}^{\mathrm{H}}(l,k).
$$

The whitening operation is defined as:

$$
\mathbf{y_{w}}(l,k)=\hat{\mathbf{\Phi}}^{-1/2}_{\mathbf{nn}}(k)\,\mathbf{y}(l,k),
$$

where $\hat{\mathbf{\Phi}}^{-1/2}_{\mathbf{nn}}(k)$ is computed via eigenvalue decomposition (EVD) of $\hat{\mathbf{\Phi}}_{\mathbf{nn}}(k)$.

Let $\mathcal{V}_{t}$ denote the set of frames in which only the target speaker is active, and let $\mathcal{V}_{i}$ denote the set of frames in which only interfering speakers are active. The set $\mathcal{V}_{i}$ includes multiple active sources of the interference group, but not the target source. For a given frame set $\mathcal{V}$, the corresponding noisy covariance matrix is estimated as:

$$
\hat{\mathbf{\Phi}}_{\mathbf{yy}}^{(\mathcal{V})}(k)=\frac{1}{|\mathcal{V}|}\sum_{l\in\mathcal{V}}\mathbf{y}(l,k)\mathbf{y}^{\mathrm{H}}(l,k),
$$

and the whitened covariance matrix is defined by

$$
\hat{\mathbf{\Phi}}_{\mathbf{y_{w}y_{w}}}^{(\mathcal{V})}(k)=\hat{\mathbf{\Phi}}^{-1/2}_{\mathbf{nn}}(k)\,\hat{\mathbf{\Phi}}_{\mathbf{yy}}^{(\mathcal{V})}(k)\,(\hat{\mathbf{\Phi}}^{-1/2}_{\mathbf{nn}})^{\mathrm{H}}(k).
$$

Applying this procedure to $\mathcal{V}_{t}$, the target RTF is obtained from the dominant eigenvector of $\hat{\mathbf{\Phi}}_{\mathbf{y_{w}y_{w}}}^{(\mathcal{V}_{t})}(k)$, denoted by $\hat{\bm{\psi}}^{(t)}$, as

$$
\hat{\mathbf{a}}^{(t)}(k)=\frac{\hat{\mathbf{\Phi}}^{\mathrm{H}/2}_{\mathbf{nn}}(k)\hat{\bm{\psi}}^{(t)}}{\mathbf{e}^{\top}_{\mathrm{ref}}\hat{\mathbf{\Phi}}^{\mathrm{H}/2}_{\mathbf{nn}}(k)\hat{\bm{\psi}}^{(t)}},
$$

with $\mathbf{e}_{{\mathrm{ref}}}$ the selection vector for the chosen reference microphone.

Applying the same procedure to $\mathcal{V}_{i}$, the interference subspace is estimated by taking the $J-1$ dominant eigenvectors of $\hat{\mathbf{\Phi}}_{\mathbf{y_{w}y_{w}}}^{(\mathcal{V}_{i})}(k)$. Denoting these eigenvectors by $\{\hat{\bm{\psi}}^{(i)}_{j}\}_{j=1}^{J-1}$, the corresponding interference basis vectors are obtained:

$$
\hat{\mathbf{u}}^{(i)}_{j}(k)=\frac{\hat{\mathbf{\Phi}}^{\mathrm{H}/2}_{\mathbf{nn}}(k)\hat{\bm{\psi}}^{(i)}_{j}}{\mathbf{e}^{\top}_{\mathrm{ref}}\hat{\mathbf{\Phi}}^{\mathrm{H}/2}_{\mathbf{nn}}(k)\hat{\bm{\psi}}^{(i)}_{j}},\qquad j=1,\dots,J-1.
$$

Thus, the same CW procedure is used for both estimations: the dominant eigenvector from $\mathcal{V}_{t}$ provides the target RTF, while the dominant eigensubspace from $\mathcal{V}_{i}$ provides a basis that spans the interfering speakers’ RTF subspace.

### 3.3 Loss Function and Training Process

In this work, we propose to minimize the SI-SDR between the estimated source and the target combination of the sources of interest. We discuss a single desired source and $J-1$ interference sources, namely $\mathbf{g}^{\top}=[1,0,\ldots,0]$ (assuming, without loss of generality, that the desired source is source #1). An extension to multiple desired sources is straightforward. To impose a distortionless response toward the target source and suppress the interference sources, we define the following loss function inspired by the LCMV criterion.

We adopt a procedure inspired by the augmented Lagrangian framework [^1], in which the constraint terms are incorporated into the objective as weighted penalties. The corresponding penalty coefficients are progressively increased during training, thereby encouraging gradual satisfaction of the spatial constraints.

The network predicts frequency-dependent time-varying beamforming weights, which are averaged along the time-frame axis to obtain the final time-invariant beamformer weights $\mathbf{w}(k)\in\mathbb{C}^{M}$. The enhanced signal $\hat{s}$ and the target signal $s_{\mathrm{target}}$, defined in 4 and 5, respectively, are considered here in the time domain. The training objective is given by:

$$
\displaystyle\mathcal{L}
$$
 
$$
\displaystyle=-\mathrm{SI\text{-}SDR}(\hat{s},s_{\mathrm{target}})
$$
 
$$
\displaystyle\qquad+\lambda_{\mathrm{pass}}\,\mathbb{E}_{k}\!\left[\left|\mathbf{w}^{\mathrm{H}}(k)\mathbf{a}_{\mathrm{target}}(k)-1\right|^{2}\right]
$$
 
$$
\displaystyle\qquad+\lambda_{\mathrm{null}}\,\mathbb{E}_{k}\!\left[10\log_{10}\!\left(\left\|\mathbf{w}^{\mathrm{H}}(k)\mathbf{A}_{\mathrm{interf}}(k)\right\|^{2}+\epsilon\right)\right],
$$

which jointly promotes target reconstruction, enforces a distortionless response toward the desired direction, and encourages null steering toward the interference subspace. Here, $\mathbf{a}_{\mathrm{target}}(k)\in\mathbb{C}^{M}$ denotes the oracle RTF of the target speaker used for supervised training, and $\mathbf{A}_{\mathrm{interf}}(k)\in\mathbb{C}^{M\times(J-1)}$ contains the oracle RTFs of the interfering speakers. Applying the null penalty on a logarithmic scale increases the sensitivity to low-level residual interference, thereby encouraging deeper nulls compared with linear-domain penalties. The penalty weights $\lambda_{\mathrm{pass}}$ and $\lambda_{\mathrm{null}}$ are gradually increased during training according to a predefined schedule, and are activated only after an initial warm-up period of 10 epochs. In this work, the target speaker was selected at random from the $J$ speakers.

It is important to note that the network is trained to optimize the loss function in 12 using oracle spatial information for supervision. However, during inference, oracle RTFs are not available. Instead, the network is guided by the estimated target RTF in 10 and the estimated interference subspace in 11, which are provided as inputs to the network.

## 4 Experimental Study

This section details the dataset generation process and presents the results of the proposed model.

### 4.1 Dataset Generation and Noise Environment

Multichannel multi-speaker recordings were simulated in randomly generated acoustic environments. Each sample corresponds to a room with width and length uniformly drawn in $[6,9]$ m and a fixed height of $3$ m. An $8$ -microphone linear array was placed at a height of $1.3$ m and randomly tilted within $[-45^{\circ},45^{\circ}]$ (see Fig. 3 in [^5] for the array configuration). Speech signals were drawn from the LibriSpeech dataset [^18] and positioned at a distance of $1$ – $1.5$ m from the array center. Each sample includes $J\in\{2,3\}$ static speakers immersed in a stationary babble-noise environment, with one target speaker and $J-1$ interfering speakers. Both anechoic and reverberant target/interference conditions were considered. For each sample, stationary babble noise was pre-generated by summing $20$ randomly chosen active speakers positioned near the room walls using the room impulse response (RIR) generator [^11], and was introduced to enable noise covariance estimation. The same simulator was used for the anechoic target/interfering speakers. Reverberant target/interference conditions with $T_{60}\in[0.3,0.55]$ s were simulated only for the target and interfering speakers using the GPU-RIR package [^6] to reduce computational cost. Each recording contains an initial $4$ s segment used for beamformer estimation: the first $0.5$ s contains only babble noise, followed by a $1$ s target-only segment and a $1$ s interference-only segment, while the final $1.5$ s contains the full mixture with all speakers simultaneously active. The estimated time-invariant beamforming weights are then applied to an additional $4$ s fully overlapped mixture segment, resulting in final $8$ s recordings used for evaluation. The training set contains $20{,}000$ multichannel recordings.

### 4.2 Results

This section reports the results of the proposed linearly constrained DNN beamformer. Audio samples, beam-patterns, and implementation code are available in our online repository.<sup>1</sup>

Enhancement Performance: We evaluate the proposed method using SI-SDR, SNR, and SIR, computed over the active mixture frames spanning $2.5$ – $8$ s of the $8$ s recordings, during which all speakers are simultaneously active. In addition, we report the power ratio $\mathrm{Pwr~Ratio}=10\log_{10}\!\left(\frac{\mathbb{E}|x_{\mathrm{out}}|^{2}}{\mathbb{E}|x_{\mathrm{in}}|^{2}}\right)$, which is computed by applying the learned beamformer weights separately to each signal component and measuring its average energy before and after beamforming. All outputs are normalized to preserve the target speaker power.

The analytical LCMV beamformer is constructed using the estimated spatial signatures and is given by:

$$
\mathbf{w}_{\mathrm{LCMV}}(k)=\hat{\mathbf{\Phi}}_{nn}^{-1}(k)\mathbf{C}(k)\left(\mathbf{C}^{H}(k)\hat{\mathbf{\Phi}}_{nn}^{-1}(k)\mathbf{C}(k)\right)^{-1}\mathbf{g},
$$

where $\mathbf{C}(k)=\left[\hat{\mathbf{a}}^{(t)}(k),\hat{\mathbf{u}}^{(i)}_{1}(k),\ldots,\hat{\mathbf{u}}^{(i)}_{J-1}(k)\right]$, $\hat{\mathbf{\Phi}}_{nn}(k)$ defined in 6, and the spatial signatures are defined in 10 and 11 for the target source and the interference subspace, respectively.

Tables 1 and 2 summarize the performance of the proposed beamformer under both anechoic and reverberant conditions for two- and three-speaker mixtures ($J\in\{2,3\}$). Although the LCMV beamformer explicitly enforces spatial constraints, the proposed learned models achieve superior overall enhancement performance together with stronger background-noise attenuation. In particular, the proposed models achieve substantially higher SI-SDR and SNR values than the LCMV baseline in both the anechoic and reverberant scenarios, while maintaining competitive interference suppression. The “Estimated RTF” and “No RTF” models achieve similar enhancement metrics in the evaluated scenarios.

On the Importance of RTF Guidance: To further examine the role of spatial guidance, Table 3 presents a conceptual fully overlapped scenario in which all speakers remain simultaneously active throughout the recording. Since the proposed CW-based estimation method requires separated source activity patterns, this experiment serves only to illustrate the importance of spatial guidance. In this setting, the unguided model (“No RTF”) fails to achieve meaningful enhancement or interference suppression, whereas the “Oracle RTF” model maintains strong directional filtering and null steering. These results motivate the development of spatial-guidance methods that do not rely on separated source activity patterns.

Beampattern Analysis: The narrowband beampattern is defined as $B(k,\theta)=\mathbf{w}^{\rm H}(k)\mathbf{h}(k,\theta)$, where $\mathbf{h}(k,\theta)$ is the steering vector corresponding to the direction of arrival $\theta$. Figure 2 presents the corresponding wideband beampower, computed as $P(\theta)=\sum_{k}|B(k,\theta)|^{2}$. Compared with the LCMV beamformer, the proposed learned models produce more directional and spatially selective responses, with lower sidelobe levels and improved background-noise suppression. While the LCMV beamformer exhibits a less spatially selective response with stronger sidelobes, the learned beamformers maintain focused main lobes toward the target direction together with clear attenuation toward the interfering speakers. In addition, the RTF-guided beamformers produce more spatially coherent beampatterns than the unguided model, which exhibits a less structured spatial response despite achieving similar enhancement metrics.

Table 1: Three-speaker scenario (anechoic target/interference).

<table><tbody><tr><th>Metric [dB]</th><td>Input</td><td>Est. RTF</td><td>No RTF</td><td>Oracle RTF</td><td>LCMV</td></tr><tr><th colspan="6">Target speaker (enhancement)</th></tr><tr><th>SI-SDR</th><td>-4.65</td><td>0.63</td><td>0.62</td><td>1.04</td><td>-1.94</td></tr><tr><th>SNR</th><td>1.46</td><td>5.74</td><td>6.16</td><td>6.02</td><td>2.96</td></tr><tr><th>SIR</th><td>-3.39</td><td>4.90</td><td>5.15</td><td>5.49</td><td>6.70</td></tr><tr><th>Pwr Ratio</th><td>–</td><td>0.00</td><td>0.00</td><td>0.00</td><td>0.00</td></tr><tr><th colspan="6">Interferer 1 (suppression)</th></tr><tr><th>Pwr Ratio</th><td>–</td><td>-10.18</td><td>-10.69</td><td>-10.89</td><td>-10.31</td></tr><tr><th colspan="6">Interferer 2 (suppression)</th></tr><tr><th>Pwr Ratio</th><td>–</td><td>-8.53</td><td>-9.02</td><td>-9.58</td><td>-9.96</td></tr><tr><th colspan="6">Background noise (suppression)</th></tr><tr><th>Pwr Ratio</th><td>–</td><td>-4.28</td><td>-4.69</td><td>-4.56</td><td>-1.50</td></tr></tbody></table>

Table 2: Two-speaker scenario (reverberant target/interference).

<table><tbody><tr><th>Metric [dB]</th><td>Input</td><td>Est. RTF</td><td>No RTF</td><td>Oracle RTF</td><td>LCMV</td></tr><tr><th colspan="6">Target speaker (enhancement)</th></tr><tr><th>SI-SDR</th><td>-1.81</td><td>0.33</td><td>0.05</td><td>0.40</td><td>-3.50</td></tr><tr><th>SNR</th><td>3.30</td><td>5.61</td><td>6.33</td><td>6.11</td><td>5.24</td></tr><tr><th>SIR</th><td>-0.03</td><td>4.78</td><td>4.62</td><td>5.00</td><td>5.58</td></tr><tr><th>Pwr Ratio</th><td>–</td><td>0.00</td><td>0.00</td><td>0.00</td><td>0.00</td></tr><tr><th colspan="6">Interferer 1 (suppression)</th></tr><tr><th>Pwr Ratio</th><td>–</td><td>-4.81</td><td>-4.66</td><td>-5.03</td><td>-5.61</td></tr><tr><th colspan="6">Background noise (suppression)</th></tr><tr><th>Pwr Ratio</th><td>–</td><td>-2.31</td><td>-3.03</td><td>-2.81</td><td>-1.94</td></tr></tbody></table>

Table 3: Three-speaker scenario (fully overlapped, anechoic).

<table><tbody><tr><th>Metric [dB]</th><td>Input</td><td>Oracle RTF</td><td>No RTF</td></tr><tr><th colspan="4">Target speaker (enhancement)</th></tr><tr><th>SI-SDR</th><td>-4.65</td><td>1.28</td><td>-4.62</td></tr><tr><th>SNR</th><td>1.46</td><td>5.85</td><td>1.52</td></tr><tr><th>SIR</th><td>-3.39</td><td>5.74</td><td>-3.34</td></tr><tr><th>Pwr Ratio</th><td>–</td><td>0.00</td><td>0.00</td></tr><tr><th colspan="4">Interferer 1 (suppression)</th></tr><tr><th>Pwr Ratio</th><td>–</td><td>-10.91</td><td>-0.02</td></tr><tr><th colspan="4">Interferer 2 (suppression)</th></tr><tr><th>Pwr Ratio</th><td>–</td><td>-9.81</td><td>-0.04</td></tr><tr><th colspan="4">Background noise (suppression)</th></tr><tr><th>Pwr Ratio</th><td>–</td><td>-4.39</td><td>-0.05</td></tr></tbody></table>

![Refer to caption](https://arxiv.org/html/2605.21141v1/x1.png)

(a) Estimated RTF

## 5 Conclusions

In this work, we propose a fully DNN-based beamforming framework for target-speaker enhancement in multi-speaker environments that leverages explicit spatial guidance. The proposed method combines RTF-based guidance with an adaptive loss inspired by constrained optimization, enabling the network to jointly preserve the target speaker and suppress interfering speakers within a fully learned beamforming framework. The results demonstrate that the proposed approach learns spatially selective filtering behavior, producing focused beampatterns and effective interference suppression that outperform those of a classical LCMV beamformer constructed from the estimated spatial signatures in several evaluated scenarios. Moreover, the proposed method exhibits lower sidelobe levels, thereby improving background noise attenuation. Overall, the proposed framework highlights the potential of incorporating explicit spatial constraints and priors into interpretable and robust DNN-based multichannel speech enhancement systems.

[^1]: D. P. Bertsekas (2014) Constrained optimization and lagrange multiplier methods. Academic press. Cited by: §3.3.

[^2]: G. Bologni, R. C. Hendriks, and R. Heusdens (2025) Wideband relative transfer function (RTF) estimation exploiting frequency correlations. IEEE Trans. Audio, Speech, Lang. Process. 33 (), pp. 731–747. Cited by: §1.

[^3]: A. Briegleb, M. M. Halimeh, and W. Kellermann (2023) Exploiting spatial information with the informed complex-valued spatial autoencoder for target speaker extraction. In Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), Cited by: §1.

[^4]: S. E. Chazan, J. Goldberger, and S. Gannot (2018) DNN-based concurrent speakers detector and its application to speaker extraction with LCMV beamforming. In Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), pp. 6712–6716. Cited by: §1.

[^5]: A. Cohen, D. Wong, J. Lee, and S. Gannot (Jul. 2025) Explainable DNN-based beamformer with postfilter. IEEE/ACM Trans. Audio, Speech, Lang. Process. 33, pp. 3070–3085. External Links: [Document](https://dx.doi.org/10.1109/TASLPRO.2025.3581110) Cited by: §1, §1, §3.1, §3, §4.1.

[^6]: D. Diaz-Guerra, A. Miguel, and J. R. Beltran (2021) gpuRIR: a python library for room impulse response simulation with GPU acceleration. Multimedia Tools Appl. 80 (4), pp. 5653–5671. Cited by: §4.1.

[^7]: M. Er and A. Cantoni (1983) Derivative constraints for broad-band element space antenna array processors. IEEE Trans. Acoust., Speech, Signal Process. 31 (6), pp. 1378–1393. External Links: [Document](https://dx.doi.org/10.1109/TASSP.1983.1164219) Cited by: §1.

[^8]: S. Gannot, D. Burshtein, and E. Weinstein (2001-08) Signal enhancement using beamforming and nonstationarity with applications to speech. IEEE Trans. Signal Process. 49 (8), pp. 1614–1626. Cited by: §1, §1.

[^9]: S. Gannot, E. Vincent, S. Markovich-Golan, and A. Ozerov (2017-04) A consolidated perspective on multimicrophone speech enhancement and source separation. IEEE/ACM Trans. Audio, Speech, and Lang. Process. 25 (4), pp. 692–730. Cited by: §1, §1.

[^10]: Y. Gong, M. Karimi, and T. Le-Ngoc (2025) Near-field nulling control beamfocusing optimization for multi-user interference suppression. IEEE Open J. Commun. Soc. 6 (), pp. 1727–1746. External Links: [Document](https://dx.doi.org/10.1109/OJCOMS.2025.3548457) Cited by: §1.

[^11]: E. A. Habets (2006) Room impulse response generator. Technische Universiteit Eindhoven, Tech. Rep. 2 (2.4), pp. 1. Cited by: §4.1.

[^12]: W. Huang, L. F. Yan, and E. A.P. Habets (2025) Robust superdirective beamforming using a uniform circular array with directional microphones. In Proc. Asia-Pacific Signal Inf. Process. Assoc. Annu. Summit Conf. (APSIPA ASC), Vol., pp. 89–94. External Links: [Document](https://dx.doi.org/10.1109/APSIPAASC65261.2025.11249246) Cited by: §1.

[^13]: C. Lee, C. Yang, Y. M. Saidutta, R. S. Srinivasa, Y. Shen, and H. Jin (2025) Better exploiting spatial separability in multichannel speech enhancement with an align-and-filter network. In Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), Cited by: §1.

[^14]: Y. Luo, C. Han, N. Mesgarani, E. Ceolini, and S. Liu (2019) FaSNet: Low-latency adaptive beamforming for multi-microphone audio processing. In IEEE Automatic Speech Recognition and Understanding Workshop (ASRU), pp. 260–267. Cited by: §1.

[^15]: S. Markovich, S. Gannot, and I. Cohen (2009) Multichannel eigenspace beamforming in a reverberant noisy environment with multiple interfering speech signals. IEEE Trans. Audio, Speech, Lang. Process. 17 (6), pp. 1071–1086. External Links: [Document](https://dx.doi.org/10.1109/TASL.2009.2016395) Cited by: §1.

[^16]: S. Markovich-Golan, S. Gannot, and W. Kellermann (2017) Combined LCMV-TRINICON beamforming for separating multiple speech sources in noisy and reverberant environments. IEEE/ACM Trans. Audio, Speech, Lang. Process. 25 (2), pp. 320–332. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2016.2633806) Cited by: §1.

[^17]: S. Markovich-Golan, S. Gannot, and W. Kellermann (2018) Performance analysis of the covariance-whitening and the covariance-subtraction methods for estimating the relative transfer function. In European Signal Proc. Conf. (EUSIPCO), Rome, Italy, pp. 2499–2503. Cited by: §1, §3.2.

[^18]: V. Panayotov, G. Chen, D. Povey, and S. Khudanpur (2015) Librispeech: an ASR corpus based on public domain audio books. In Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), pp. 5206–5210. Cited by: §4.1.

[^19]: X. Ren, X. Zhang, L. Chen, X. Zheng, C. Zhang, L. Guo, and B. Yu (2021-08) A causal U-Net based neural beamforming network for real-time multi-channel speech enhancement. In Interspeech, pp. 1832–1836. Cited by: §1.

[^20]: O. Ronai, Y. Sitton, A. Bar, and R. Talmon (2025) RTF estimation using Riemannian geometry for speech enhancement in the presence of interferences. In Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), Cited by: §1.

[^21]: O. Schwartz, S. Gannot, and E. A. P. Habets (2017) Multispeaker LCMV beamformer and postfilter for source separation and noise reduction. IEEE/ACM Trans. Audio, Speech, Lang. Process. 25 (5), pp. 940–951. External Links: [Document](https://dx.doi.org/10.1109/TASLP.2017.2655258) Cited by: §1.

[^22]: O. Shmaryahu and S. Gannot (2022) On the importance of acoustic reflections in beamforming. In Proc. Int. Workshop Acoust. Signal Enhancement (IWAENC), Cited by: §1.

[^23]: K. Tesch and T. Gerkmann (2022) Insights into deep non-linear filters for improved multi-channel speech enhancement. IEEE/ACM Trans. Audio, Speech, Lang. Process. 31, pp. 563–575. Cited by: §1.

[^24]: Y. Yang, N. Pan, W. Zhang, C. Pan, J. Benesty, and J. Chen (2024) Interference-controlled maximum noise reduction beamformer based on deep-learned interference manifold. IEEE/ACM Trans. Audio, Speech, Lang. Process. 32, pp. 4676–4690. Cited by: §1.

[^25]: I. Zaidel and S. Gannot (2026) Interpretable binaural deep beamforming guided by time-varying relative transfer function. arXiv:2511.10168. Cited by: §1, §1, §3.