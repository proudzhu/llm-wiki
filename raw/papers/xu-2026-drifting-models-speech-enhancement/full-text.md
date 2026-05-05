Liang    Diego    Bastiaan    Longfei Felix    Rasmus Kongsgaard <sup>1</sup> Victoria University of Wellington, New Zealand  
<sup>2</sup> GN Audio A/S, Denmark [liang.xu,bastiaan.kleijn,felix.yan@vuw.ac.nz,dcnozal,rkolsson@gn.com](https://arxiv.org/html/2604.24199v1/mailto:liang.xu,bastiaan.kleijn,felix.yan@vuw.ac.nz,dcnozal,rkolsson@gn.com)

###### Abstract

We propose Speech Enhancement based on Drifting Models (DriftSE), a novel generative framework that formulates denoising as an equilibrium problem. Rather than relying on iterative sampling, DriftSE natively achieves one-step inference by evolving the pushforward distribution of a mapping function to directly match the clean speech distribution. This evolution is driven by a Drifting Field, a learned correction vector that guides samples toward the high-density regions of the clean distribution, which naturally facilitates training on unpaired data by matching distributions rather than paired samples. We investigate the framework under two formulations: a direct mapping from the noisy observation, and a stochastic conditional generative model from a Gaussian prior. Experiments on the VoiceBank-DEMAND benchmark demonstrate that DriftSE achieves high-fidelity enhancement in a single step, outperforming multi-step diffusion baselines and establishing a new paradigm for speech enhancement.

###### keywords:

speech enhancement, drifting models, diffusion models, consistency models

## 1 Introduction

The field of Speech Enhancement (SE) has evolved significantly over recent decades, progressing from classical statistical signal processing techniques like Wiener filtering \[meyer1997multi, chua2024effective\] to modern deep learning. Discriminative models, such as RNNs \[Weninger2015LVA\], LSTMs \[tan18\_interspeech\], and complex spectral mapping \[hu2020dccrn\], effectively suppress noise but often yield spectral oversmoothing and robotic artifacts due to regression-based objectives. Generative Adversarial Networks (GANs) \[pascual2017segan, fu2019metricgan, su2021hifi\] improve perceptual quality but suffer from training instability and mode collapse. Recently, Score-based Diffusion Models \[richter2023speech\] have established state-of-the-art performance by modeling the gradient of the log-density of the clean speech distribution. These models define a forward process that gradually degrades data into noise, and a reverse process for generation. The reverse dynamics can be formulated as either a Stochastic Differential Equation (SDE) \[song2021scorebased\] or a deterministic Probability Flow ODE (PF-ODE) sharing the same marginal probability densities. However, their inference is inherently iterative. Numerically integrating these highly curved reverse-time trajectories requires 10–100 discretization steps, resulting in a high Number of Function Evaluations (NFE) that imposes a critical latency bottleneck for real-time applications.

To address the computational inefficiency of diffusion models, recent research broadly falls into two lines of work: trajectory compression and trajectory linearization. Compression approaches accelerate sampling by reducing the number of steps. For instance, hybrid approaches \[lemercier2023storm, trachu24\_interspeech\] combine predictive models with a small number of diffusion refinement steps, while diffusion-GAN hybrids \[han25b\_interspeech\] further reduce steps via adversarial training. Similarly, distillation-based one-step generators such as Consistency Models \[song2023consistency, kim2024consistency, xu2025rosecd, nishigori2025schrodinger\] enforce self-consistency along the PF-ODE to distill a multi-step sampler into a single-step mapping.

In parallel, Flow Matching \[lipman2023flow, wang2025flowse\] techniques seek to linearize the generative trajectory. Rectified Flow \[rectflow2023\] explicitly straightens the transport path to minimize the curvature of the ODE. MeanFlow \[geng2025meanflow, geng2025improved\] learns a continuous mean velocity field to model probability paths. However, these methods remain fundamentally trajectory-based. They rely on continuous transport dynamics that must be discretized at inference, and accurately approximating these paths with only a few steps remains challenging.

Recently, Drifting Models \[deng2026generative\] were proposed as a powerful new paradigm that reformulates generation as a distributional equilibrium problem. By mapping high-dimensional data into a semantic latent space during training, the framework learns a kernelized drifting field where generated samples are simultaneously attracted to the true data distribution and repelled by the evolving model distribution. Minimizing this drift directly aligns the generator's pushforward distribution with the target data. Operating natively in a single step, this latent equilibrium approach has achieved state-of-the-art results in large-scale image generation (FID 1.54 on ImageNet).

Our contribution is the introduction of Speech Enhancement based on Drifting Models (DriftSE), a novel generative framework for one-step denoising. We redefine enhancement as learning a direct projection onto the clean speech manifold without predefined trajectory constraints. Unlike the original formulation which focused on noise-to-data generation \[deng2026generative\], we adapt DriftSE for two distinct enhancement paradigms: a direct mapping that pushes the noisy speech distribution toward the clean speech distribution, and a stochastic conditional generative approach that generates clean speech from a Gaussian noise prior. To construct a perceptually meaningful drifting field, we project the audio into a semantic latent space using a pre-trained Self-Supervised Learning (SSL) encoder. Aligning the generated and clean speech distributions within this latent space ensures effective noise suppression and high-frequency structural recovery.

Extensive experiments on the VoiceBank-DEMAND (VB-DMD) dataset demonstrate that DriftSE achieves competitive perceptual quality with single-step inference. Specifically, the direct mapping variant achieves PESQ 3.15 and SI-SDR 16.1 dB, while the conditional variant achieves SCOREQ 4.33. Both achieve high-fidelity enhancement without iterative sampling or predefined trajectories. Evaluation on real-world recordings from the DNS Challenge 2020 blind test set demonstrates state-of-the-art generalization performance.

## 2 Drifting Models

We briefly review Drifting Models \[deng2026generative\], which formulate generative modeling as the training-time evolution of a pushforward distribution.

### 2.1 Pushforward and Equilibrium

Given a simple source distribution $p_{\epsilon}$ (e.g., standard Gaussian noise $\mathcal{N}(\mathbf{0},\mathbf{I})$), the drift approach takes a sample $\epsilon\sim p_{\epsilon}$ with $\epsilon\in\mathbb{R}^{d}$, and maps it through a parameterized function $f_{\theta}:\mathbb{R}^{d}\rightarrow\mathbb{R}^{d}$ in a single step to produce a target variable $\mathbf{x}\in\mathbb{R}^{d}$

$$
\mathbf{x}=f_{\theta}(\epsilon).
$$

This defines the pushforward distribution $q_{\theta}=(f_{\theta})_{\#}p_{\epsilon}$, meaning that sampling $\epsilon\sim p_{\epsilon}$ and applying $f_{\theta}$ yields samples distributed as $q_{\theta}$. For conditional generation, (1) extends to $\mathbf{x}=f_{\theta}(\epsilon,\mathbf{c})$, where $\mathbf{c}$ is a condition (e.g., a class label or noisy speech).

To drive $q_{\theta}$ toward the target data distribution $p_{\text{data}}$, the framework introduces a Drifting Field $\mathbf{V}_{p,q}:\mathbb{R}^{d}\rightarrow\mathbb{R}^{d}$ that acts as a correction vector at each generated sample of $q_{\theta}$, pointing in the direction that reduces the discrepancy between $q_{\theta}$ and $p_{\text{data}}$. Concretely, a drifting target is defined as

$$
\mathbf{x}_{\text{target}}\leftarrow\mathbf{x}+\mathbf{V}_{p,q}(\mathbf{x}),
$$

and the generator is trained to map $\epsilon$ to $\mathbf{x}_{\text{target}}$. As training progresses, the pushforward distribution $q_{\theta}$ evolves until it reaches a state of distributional equilibrium where the drift vanishes

$$
q_{\theta}=p_{\text{data}}\quad\Longrightarrow\quad\mathbf{V}_{p,q}(\mathbf{x})=\mathbf{0},\ \forall\mathbf{x}.
$$

### 2.2 Designing the Drifting Field

Inspired by mean-shift theory \[meanshift1995\], the total drift $\mathbf{V}_{p,q}(\mathbf{x})$ decomposes into two opposing forces

$$
\mathbf{V}_{p,q}(\mathbf{x})=\mathbf{V}^{+}_{p}(\mathbf{x})-\mathbf{V}^{-}_{q}(\mathbf{x}),
$$

where $\mathbf{V}^{+}_{p}$ attracts samples toward the data distribution $p_{\text{data}}$, and $\mathbf{V}^{-}_{q}$ repels samples away from high-density regions of the current model distribution $q_{\theta}$. Both terms take the form of a kernel-weighted mean shift

$$
\displaystyle\mathbf{V}^{+}_{p}(\mathbf{x})
$$
 
$$
\displaystyle=\frac{1}{Z_{p}(\mathbf{x})}\mathbb{E}_{\mathbf{y}^{+}\sim p}\left[k(\mathbf{x},\mathbf{y}^{+})(\mathbf{y}^{+}-\mathbf{x})\right],
$$
$$
\displaystyle\mathbf{V}^{-}_{q}(\mathbf{x})
$$
 
$$
\displaystyle=\frac{1}{Z_{q}(\mathbf{x})}\mathbb{E}_{\mathbf{y}^{-}\sim q}\left[k(\mathbf{x},\mathbf{y}^{-})(\mathbf{y}^{-}-\mathbf{x})\right],
$$

with similarity kernel $k(\mathbf{x},\mathbf{y})$ and normalizers $Z_{p}(\mathbf{x})=\mathbb{E}_{\mathbf{y}^{+}\sim p}[k(\mathbf{x},\mathbf{y}^{+})]$ and $Z_{q}(\mathbf{x})=\mathbb{E}_{\mathbf{y}^{-}\sim q}[k(\mathbf{x},\mathbf{y}^{-})]$.

In practice, these expectations are approximated with mini-batch averages, drawing positives $\mathbf{y}^{+}$ from $p_{\text{data}}$ and negatives $\mathbf{y}^{-}$ from the current model distribution $q_{\theta}$. By substituting the normalizers and combining the forces into a joint expectation over $p$ and $q$, the self-referential $-\mathbf{x}$ terms elegantly cancel out. This yields the exact unified formulation

$$
\mathbf{V}_{p,q}(\mathbf{x})=\frac{1}{Z_{p}Z_{q}}\mathbb{E}_{p,q}\left[k(\mathbf{x},\mathbf{y}^{+})k(\mathbf{x},\mathbf{y}^{-})(\mathbf{y}^{+}-\mathbf{y}^{-})\right].
$$

To measure the similarity between a generated sample $\mathbf{x}$ and any reference feature $\mathbf{y}\in\{\mathbf{y}^{+},\mathbf{y}^{-}\}$, an exponential similarity kernel with temperature $\tau$ is employed

$$
k_{\tau}(\mathbf{x},\mathbf{y})=\exp\left(-\frac{\left\|\mathbf{x}-\mathbf{y}\right\|_{2}}{\tau}\right),
$$

where $\tau$ controls the interaction bandwidth.

### 2.3 Training Objective

In practice, the drifting field is computed in a latent space using a pretrained extractor $\phi(\cdot)$. To optimize the generator $f_{\theta}$, its outputs $\mathbf{x}=f_{\theta}(\epsilon)$ are driven along the field $\mathbf{V}$ via the objective

$$
\mathcal{L}_{\text{drift}}=\mathbb{E}_{\epsilon}\left[\Big\|\phi(\mathbf{x})-\text{sg}\left(\phi(\mathbf{x})+\mathbf{V}\big(\phi(\mathbf{x})\big)\right)\Big\|_{2}^{2}\right],
$$

where $\text{sg}(\cdot)$ is the stop-gradient operator. Regressing toward this fixed target minimizes the magnitude of $\mathbf{V}$, progressively transporting the pushforward distribution $q_{\theta}$ toward the target data distribution $p_{\text{data}}$.

![Refer to caption](https://arxiv.org/html/2604.24199v1/figures/interspeech2026.drawio.png)

Figure 1: Overview of the DriftSE framework (illustrating the Direct Mapping formulation).

## 3 Speech Enhancement via Latent Drifting

We propose DriftSE, which formulates speech enhancement as an equilibrium problem (Fig. 1). By evolving the mapping function's pushforward distribution to match the clean speech distribution, DriftSE achieves native one-step denoising (1 NFE).

### 3.1 Two Enhancement Paradigms

Let $\mathbf{y}\in\mathbb{C}^{F\times T}$ denote the complex spectrogram of the noisy speech, with $F$ frequency bins and $T$ time frames, and let $\mathbf{x}\in\mathbb{C}^{F\times T}$ be the clean speech target. To produce the enhanced speech $\hat{\mathbf{x}}$, we investigate two distinct formulations for the mapping function $f_{\theta}$:

Direct Mapping: Defined as $\hat{\mathbf{x}}=f_{\theta}(\mathbf{y}+\sigma\bm{\epsilon})$, where $\bm{\epsilon}\sim\mathcal{N}(\mathbf{0},\mathbf{I})$ and $\sigma$ controls the noise injection strength. During training, when $\sigma=0$, this acts as a strictly deterministic mapping $\hat{\mathbf{x}}=f_{\theta}(\mathbf{y})$. When $\sigma>0$, the injected noise smooths the acoustic distribution, aiding the estimation of the drifting field.

Conditional Generator: Defined as $\hat{\mathbf{x}}=f_{\theta}(\bm{\epsilon},\mathbf{y})$, where the network maps a standard Gaussian noise prior $\bm{\epsilon}$ to the target distribution conditioned on $\mathbf{y}$.

### 3.2 Speech Latent Encoder

Applying the drifting field in the time-frequency domain is suboptimal, as Euclidean distances on raw spectrograms are dominated by high-amplitude harmonics, neglecting the low-energy transients critical for phonetic intelligibility. Following \[deng2026generative\], we instead compute drift in a semantic latent space and apply multi-layer latent supervision, which provides a richer and more stable training signal. For speech enhancement, we selected self-supervised speech models. In particular, we employed HuBERT, WavLM and DistilHuBERT \[hsu2021hubert, chen2022wavlm, chang2022distilhubert\], which exhibit a well-documented layer hierarchy: shallow layers capture low-level acoustic structure, while deeper layers encode phonetic and semantic content. We therefore define a frozen self-supervised learning (SSL) encoder $\Phi:\mathbb{R}^{L}\rightarrow\mathbb{R}^{T^{\prime}\times D}$ that maps a waveform of length $L$ to $T^{\prime}$ frame-level latent features of dimension $D$. To capture the hierarchical speech structures, the drifting field is computed and aggregated across a selected set of layers $\mathcal{S}$.

### 3.3 Frame-Wise Latent Drifting and Inference

Latent Drifting: As detailed in Fig. 1, we dynamically construct a positive set of samples $\mathcal{Z}^{+}$ from clean reference frames $\Phi(\mathbf{x})$ and a negative set of samples $\mathcal{Z}^{-}$ from the current batch of generated frames $\Phi(\hat{\mathbf{x}})$. For any generated frame $\mathbf{z}_{i}\in\mathcal{Z}^{-}$, the frame-wise Drifting Field $\mathbf{V}(\mathbf{z}_{i})$ is computed by instantiating (7) in the speech latent space, using the multi-temperature kernel ${k}_{\tau}$ from (8). The resulting field combines an attraction force pulling $\mathbf{z}_{i}$ toward the clean distribution $\mathcal{Z}^{+}$ and a repulsion force pushing it away from the current generated distribution $\mathcal{Z}^{-}$, driving $f_{\theta}$ toward equilibrium.

Training Objective: To capture hierarchical speech structures, the base drifting loss from (9) is computed and aggregated across multiple layers $l\in\mathcal{S}$ of the latent encoder, where $\mathcal{S}$ is the set of selected layers, with each layer equally weighted.

Inference: At inference time, the direct mapping approach uses $\sigma=0$ for deterministic denoising, while the conditional generator draws a fresh $\bm{\epsilon}$ to generate diverse enhanced outputs.

Overview of DriftSE: Fig. 1 illustrates the method. The mapping function $f_{\theta}$ processes the noisy speech spectrogram alongside injected Gaussian noise $\bm{\epsilon}$, which acts as a distribution smoother, to produce a denoised spectrogram in a single step. After iSTFT, both the enhanced waveform $\hat{\mathbf{x}}$ and the clean reference $\mathbf{x}$ are projected into a frame-wise latent space via a frozen encoder $\Phi$. For frame-wise latent drifting at each training iteration, we dynamically construct a mini-batch positive set ${\color[rgb]{0,0,1}\definecolor[named]{pgfstrokecolor}{rgb}{0,0,1}\mathcal{Z}^{+}}$ sampled from the clean feature frames $\Phi(\mathbf{x})$, and a mini-batch negative set ${\color[rgb]{1,.5,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,.5,0}\mathcal{Z}^{-}}$ sampled from the mapped feature frames $\Phi(\hat{\mathbf{x}})$. The total Drifting Field ${\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\mathbf{V}}$ for a mapped frame is composed of an attraction force ${\color[rgb]{0,0,1}\definecolor[named]{pgfstrokecolor}{rgb}{0,0,1}\mathbf{V}_{p}^{+}}$ that pulls it toward high-density regions of the empirical target distribution ${\color[rgb]{0,0,1}\definecolor[named]{pgfstrokecolor}{rgb}{0,0,1}\mathcal{Z}^{+}}$, and a repulsion force ${\color[rgb]{1,.5,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,.5,0}\mathbf{V}_{q}^{-}}$ that pushes it away from its neighbors in the current model distribution ${\color[rgb]{1,.5,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,.5,0}\mathcal{Z}^{-}}$. As training progresses, the mapping function minimizes ${\color[rgb]{1,0,0}\definecolor[named]{pgfstrokecolor}{rgb}{1,0,0}\mathbf{V}}$, dynamically evolving the pushforward distribution until it matches the clean latent distribution at equilibrium (epoch 100).

## 4 Experiments

In this section, we evaluate DriftSE against state-of-the-art iterative and one-step baselines, and perform ablation studies to analyze the contribution of each design choice.

### 4.1 Experimental Setup

Datasets: We train on clean speech from the VoiceBank corpus \[botinhao2016investigating\] and noise recordings from the DEMAND dataset \[thiemann2013diverse\]. During training, we employ dynamic mixing where 10,802 clean utterances are mixed on-the-fly with 18 distinct noise types \[richter2023speech\]. To ensure robust generalization and prevent overfitting to specific acoustic conditions, Signal-to-Noise Ratios (SNRs) are sampled randomly from $\{0,5,10,15\}$ dB.

For evaluation, we utilize the standard pre-mixed VB-DMD test set (824 utterances) to ensure fair benchmarking. To assess real-world generalization, we further evaluate on the DNS Challenge 2020 blind test set \[reddy2020interspeech\], which contains 300 real-world noisy recordings without clean references.

Evaluation: Following previous studies \[richter2023speech, xu2025rosecd\], we report pairwise metrics including PESQ \[rix2001perceptual\], ESTOI \[jensen2016algorithm\] and SI-SDR \[le2019sdr\]. To assess perceptual quality without clean reference, we also report non-intrusive metrics: SCOREQ \[ragano2024scoreq\], DNSMOS \[reddy2021dnsmos, reddy2022dnsmos\], and WV-MOS \[andreev2023hifipp\].

Implementation Details: We employ the NCSN++V2 architecture \[richter2023speech\] as our backbone, omitting the time embedding. Audio samples are processed at 16 kHz using a Short-Time Fourier Transform (STFT) with a window size of 510, a hop length of 128, and a Hann window, followed by the spectral compression strategy from \[richter2023speech\]. For the mapping DriftSE variant, we empirically sample the noise level $\sigma$ from a truncated log-normal distribution, i.e., $\log\sigma\sim\mathcal{N}(-3.0,1.2)$, truncated to $\sigma\in[0.01,0.3]$. For the conditional generative variant, the STFT spectrogram of the noisy observation $\mathbf{y}$ is provided as a conditioning embedding into the generator at each resolution level. For the SSL latent encoder $\Phi$, we utilize the pre-trained HuBERT-Large, WavLM-Large, and DistilHuBERT checkpoints. The extracted latent frames have a 20ms hop size and 25ms receptive field. We aggregate features from layers $\mathcal{S}=\{6,12,24\}$ for WavLM-Large and HuBERT-Large, and layers $\mathcal{S}=\{0,1,2\}$ for DistilHuBERT, with all layers equally weighted. We use a multi-temperature exponential kernel ( (8)) with temperatures $\tau\in\{0.1,0.5,1.0\}$. The model was trained on a single NVIDIA RTX A6000 GPU (48GB VRAM) for 100 epochs. We utilized a batch size of 16 and optimized the network using the AdamW optimizer with a learning rate of $5\times 10^{-4}$ and a weight decay of $0.01$.

### 4.2 Results

In-domain Evaluation: As shown in Table 1, DriftSE (DistilHuBERT, $\sigma{=}0$) achieves high-fidelity enhancement and outperforms the 30-step SGMSE+ \[richter2023speech\] and the one-step MeanFlowSE \[li2026meanflowse\], reaching PESQ 3.15 and confirming that latent drifting effectively maps noisy observations onto the distribution support of the clean speech. While distillation methods such as ROSE-CD \[xu2025rosecd\] and SBCTM \[nishigori2025schrodinger\] report higher PESQ, they utilize auxiliary losses. When we incorporate the same losses, DriftSE <sup>1†</sup> attains competitive performance.

Generalization Evaluation: We evaluate the generalization capability of DriftSE on the DNS Challenge 2020 blind test set in Table 2. We achieve state-of-the-art WV-MOS 2.65 and SCOREQ 2.97, outperforming other baselines while delivering highly competitive perceptual scores (DNSMOS SIG, BAK, and OVRL). This confirms that the drifting equilibrium learns a highly generalizable distribution projection.

![Refer to caption](figures/fig2-distribution-evolution.png)

Figure 2: Evolution of frame-level distributions in the DistilHuBERT semantic space for a fixed test utterance. Each panel displays 2D density contours (PCA projection) derived from all frames across different training epochs. Stars denote the corresponding centroids, which represent the mean of all projected frames. As training progresses, the generated distribution shifts from the noisy distribution toward the clean distribution.

### 4.3 Ablations and Analysis

Impact of the Latent Encoder: We evaluate the impact of different encoders and layer selections on latent drifting. Using only the deepest semantic layer (WavLM, Layer 24) degrades performance, suggesting that highly abstract features miss fine acoustic details. With multi-layer drifting, DistilHuBERT (768-d) is competitive with both HuBERT and WavLM (1024-d), achieving the best SI-SDR while maintaining similar perceptual quality. Therefore, we use DistilHuBERT as the default encoder in subsequent experiments.

Conditional Drifting Models (DriftSE <sup>∗</sup> <sup>2</sup>): As shown in Table 1, DriftSE <sup>∗</sup> successfully reduces generative ambiguity, delivering superior reference-free perceptual metrics (DNSMOS 3.64, SCOREQ 4.33) while maintaining competitive pairwise fidelity. This demonstrates that incorporating a stochastic prior enables the generator's pushforward distribution to better capture the inherent variance of the clean speech distribution, leading to more natural generation.

Effect of Noise Injection: For the direct mapping variant, omitting the noise prior ($\sigma=0$) during training enforces a deterministic mapping with higher fidelity (PESQ 3.15, SI-SDR 16.10 dB), whereas injecting Gaussian noise smooths the acoustic distribution to improve reference-free perceptual quality (SCOREQ from 4.08 to 4.15). This distributional smoothing trades marginal waveform precision for more natural generation, providing a promising direction for adapting to narrow or shifted target distributions in future work.

Unpaired Training: Here, \`\`unpaired'' means the model lacks access to noisy-clean audio pairs during training. For DriftSE (Unpaired, map to DNS), each mini-batch is formed by independently sampling noisy speech from VoiceBank and clean targets from the DNS training set. This still achieves strong reference-free quality (DNSMOS 3.61, SCOREQ 3.92). The expected drop in pairwise fidelity (PESQ 2.00, SI-SDR 6.60 dB) occurs because mini-batch drift estimation is inherently less precise than exact paired setting. Nevertheless, the strong non-intrusive scores indicate that the model can still drift its outputs toward the clean speech distribution without access to paired clean targets.

For DriftSE (Unpaired, map to VB-Female), noisy inputs contain mixed-gender speech from VoiceBank, while clean targets consist of female speech. This forces the model to learn a female-only target distribution, leading to systematic changes in speaker characteristics. As a result, standard pairwise metrics are omitted since clean references are no longer aligned with the shifted outputs. The perceptual scores (DNSMOS 3.40, SCOREQ 3.72) indicate successful distribution drift.

Table 1: Comparison on VB-DMD. NFE: Number of Function Evaluations. Bold indicates the best performing metric within each respective group.

| Method | NFE | PESQ | SI-SDR | ESTOI | DNSMOS | SCOREQ |
| --- | --- | --- | --- | --- | --- | --- |
| MetricGAN+ \[fu2021metricganplus\] | 1 | 3.13 | 8.50 | 0.83 | 3.22 | 3.82 |
| UNIVERSE++ \[scheibler2024universeplusplus\] | 8 | 2.91 | 18.00 | 0.85 | 3.45 | 4.35 |
| SGMSE+ \[richter2023speech\] | 30 | 2.90 | 16.90 | 0.85 | 3.48 | 3.98 |
| ROSE-CD \[xu2025rosecd\] | 1 | 3.49 | 17.80 | 0.87 | 3.49 | 4.23 |
| SBCTM \[nishigori2025schrodinger\] | 1 | 3.56 | 12.70 | 0.87 | 3.55 | 4.35 |
| MeanFlowSE \[li2026meanflowse\] | 1 | 2.81 | 19.97 | 0.88 | 3.58 | 4.25 |
| DriftSE (WavLM, L24) | 1 | 2.90 | 12.60 | 0.84 | 3.36 | 3.93 |
| DriftSE (WavLM) | 1 | 3.03 | 14.00 | 0.85 | 3.54 | 4.17 |
| DriftSE (HuBERT) | 1 | 2.94 | 12.50 | 0.84 | 3.49 | 4.14 |
| DriftSE (DistilHuBERT) | 1 | 3.00 | 15.60 | 0.85 | 3.48 | 4.15 |
| DriftSE (DistilHuBERT, $\sigma=0$) | 1 | 3.15 | 16.10 | 0.86 | 3.47 | 4.08 |
| DriftSE <sup>∗</sup> (DistilHuBERT) | 1 | 2.99 | 17.98 | 0.86 | 3.64 | 4.33 |
| DriftSE <sup>†</sup> (DistilHuBERT) | 1 | 3.45 | 20.60 | 0.87 | 3.49 | 4.11 |
| DriftSE (Unpaired, map to DNS) | 1 | 2.00 | 6.60 | 0.74 | 3.61 | 3.92 |
| DriftSE (Unpaired, map to VB-Female) | 1 | \- | \- | \- | 3.40 | 3.72 |

Table 2: Real-world recordings evaluation on DNS Challenge 2020 Blind Test Set. Bold indicates the best performing metric within each respective group.

| Method | NFE | WV-MOS | SCOREQ | SIG | BAK | OVRL |
| --- | --- | --- | --- | --- | --- | --- |
| MetricGAN+ \[fu2021metricganplus\] | 1 | 1.23 | 2.08 | 3.28 | 3.45 | 2.70 |
| UNIVERSE++ \[scheibler2024universeplusplus\] | 8 | 1.99 | 2.27 | 3.45 | 3.52 | 2.93 |
| SGMSE+ \[richter2023speech\] | 30 | 2.34 | 2.95 | 4.12 | 3.94 | 3.62 |
| ROSE-CD \[xu2025rosecd\] | 1 | 2.37 | 2.81 | 4.01 | 3.80 | 3.42 |
| SBCTM \[nishigori2025schrodinger\] | 1 | 2.24 | 2.78 | 3.83 | 3.88 | 3.33 |
| MeanFlowSE \[li2026meanflowse\] | 1 | 2.20 | 2.79 | 3.88 | 3.51 | 3.21 |
| DriftSE (WavLM) | 1 | 2.62 | 2.67 | 3.85 | 3.94 | 3.42 |
| DriftSE (HuBERT) | 1 | 2.56 | 2.74 | 3.92 | 3.79 | 3.40 |
| DriftSE (DistilHuBERT) | 1 | 2.65 | 2.97 | 3.78 | 3.84 | 3.31 |
| DriftSE <sup>∗</sup> (DistilHuBERT) | 1 | 2.45 | 2.78 | 4.01 | 3.68 | 3.43 |
| DriftSE <sup>†</sup> (DistilHuBERT) | 1 | 2.51 | 2.86 | 4.00 | 3.82 | 3.47 |

Distributional Convergence Visualization: We qualitatively verify the latent drifting mechanism by tracking a fixed test utterance's evolution in the DistilHuBERT semantic space. Figure 2 reveals a clear transition from a noise distribution toward the clean distribution. While the generated audio initially overlaps with the noisy distribution, optimization of the drifting field enables the model to capture the structural characteristics of the clean distribution. The converged contours and centroids demonstrate that DriftSE successfully maps noisy observations to the high-density regions of the clean speech distribution at equilibrium.

## 5 Conclusion

In this paper, we introduced Speech Enhancement based on Drifting Models (DriftSE), a novel paradigm that reformulates denoising as an equilibrium problem to enable native one-step generation. By utilizing a latent drifting field, DriftSE evolves the mapping function's pushforward distribution to directly match the clean speech distribution during training. We demonstrated that computing this drift within a multi-scale semantic latent space provides a robust learning signal that supports high-fidelity reconstruction. Extensive evaluations confirm that DriftSE achieves state-of-the-art perceptual quality and generalization, outperforming multi-step diffusion baselines.

## 6 Generative AI Use Disclosure

We acknowledge the ISCA policy stating that generative AI tools cannot serve as co-authors and should only be used for editing or polishing rather than producing significant parts of this paper. Although the proposed method is a novel generative model for speech enhancement, the authors declare that no generative AI tools were used to develop the source code, but AI tools were used to correct text grammar.