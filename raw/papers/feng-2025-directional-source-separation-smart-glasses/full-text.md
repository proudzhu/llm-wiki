Tiantian Feng <sup>‚ã?/sup>, Ju Lin <sup>‚Ä?/sup>, Yiteng Huang <sup>‚Ä?/sup>, Weipeng He <sup>‚Ä?/sup>, Kaustubh Kalgaonkar <sup>‚Ä?/sup>  
Niko Moritz <sup>‚Ä?/sup>, Li Wan <sup>‚Ä?/sup>, Xin Lei <sup>‚Ä?/sup>, Ming Sun <sup>‚Ä?/sup>, Frank Seide <sup>‚Ä?/sup>  
  
<sup>‚ã?/sup> University of Southern California, Los Angeles, USA <sup>‚Ä?/sup> Meta Platforms, Inc., USA

###### Abstract

Modern smart glasses leverage machine learning to offer real-time transcriptions, considerably enriching human communication experiences. However, such systems frequently encounter challenges related to environmental noises, leading to decreased speech recognition. To improve voice quality, this work investigates directional source separation using the multi-microphone array. We explore multiple beamformers to assist source separation by strengthening the directional properties of speech signals. In addition to relying on predetermined beamformers, we investigate neural beamforming in multi-channel source separation, demonstrating that automatic learning directional characteristics effectively improves separation quality. Furthermore, we investigate the training strategies for ASR when utilizing separated outputs. Our results suggest that jointly training a directional speech separation and ASR model achieves the best overall performance while balancing the wearer and conversation partner‚Äôs performance.

## I Introduction

Recent advances in audio sensing [^1] [^2] and augmented reality (AR) [^3] have empowered novel applications for smart glasses, enriching the human experience in daily communications by offering robust and efficient speech-understanding systems [^4] [^5]. Specifically, this work explores the microphone array applications on recently introduced Project Aria smart glasses [^4], embedded with diverse sensors, including a 7-channel microphone array as shown in Figure 1. Despite the rich and diverse speech cues the advanced smart glasses capture, these in-the-wild signals are frequently coupled with noises from multiple sources, such as background noises, reverberation, and interfering speakers. Such noises can substantially reduce speech intelligibility, leading to decreased speech recognition. An effective solution to improve voice quality is source separation [^6], which separates relevant speech from ambient sources.

In this paper, we present a comprehensive study of directional source separation on smart glasses. Specifically, we are interested in disambiguating speech by the wearer (SELF), the conversation partner (PARTNER), and unrelated bystanders. Here, the wearer is the person wearing the glasses. There are several applications for this technology, such as live captioning and live translation. Unlike prior works [^7] [^8] that focus on single-channel setup, our work leverages multi-channel microphones to perform source separation. Multi-channel microphone arrays have advantages over mono-channel setups in providing spatial information to the received speech signals that are beneficial to disambiguating ambient sources. Along with the multi-channel setup, we integrate multiple beamformers as the front-end processor to strengthen the sound sources‚Ä?directional information. Specifically, this study involves answering the following research questions:

![Refer to caption](figures/fig1.png)

Figure 1: 7-channel microphone arrays on Project Aria glasses.

Is more directional information beneficial for source separation? In addition to spatial properties embedded in the multi-channel microphone arrays, we propose to utilize the multiple beamformers to enhance directional information from speech signals, enabling the system to implicitly perform speaker disambiguation and noise suppression. Beamforming [^9] [^10] is an efficient front-end component aiming to amplify the signal from a specific direction. In a beamformer-based speech pipeline, the beamformer typically provides enhanced speech signals to subsequent systems such as ASR [^11].

![Refer to caption](figures/fig2.png)

Figure 2: Proposed directional source separation architecture. In the above example, the 7-ch audio input is processed by the beamforming front end, which consists of a 5-ch NLCMV beamformer (steering directions K = 4 and the mouth direction). The source separation back-end takes multi-channel beamformed audio through an encoder-decoder framework.

Can neural beamforming improve source separation? Conventional beamformers rely heavily on ideal assumptions about the environments, making them often limited in practice. Instead of drawing unrealistic hypotheses about the environment, neural beamforming [^12] [^13] [^14] [^15] [^16] [^17] is an emerging technique to learn the beamformer weights from the immense volume of microphone array signals accessible from real-life recordings or by simulation. This motivates us to probe neural beamforming in multi-channel source separation [^18] [^19].

Can source separation improve speech recognition on smart glasses? One primary goal of source separation is to enhance speech recognition. Here, we investigate the impact of source separation on ASR leveraging separation outputs. Increasingly, we explore whether the joint training of the source separation and ASR model would further benefit speech recognition.

In summary, our contributions are summarized as follows:

- We investigate the neural beamforming in source separation, discovering that automatic learning directional characteristics open up possibilities for further enhancing voice quality.
- We conduct comprehensive studies quantifying the impact of source separation on ASR. Our results show that source separation benefits the ASR performance for the wearer (1.63% WER reduction) but decreases speech recognition for the conversational partner. Moreover, combining the separation and beamformed outputs provides competitive ASR performance.
- We study joint training of source separation and ASR, demonstrating that joint training achieves the best overall ASR.

## II Source Separation Modeling

Fig 2 shows the our proposed directional source separation. It consists of front-end multiple beamformers and a source separation neural network. The source separation network receives beamformed outputs and is trained to separate the main speakers, the wearer (SELF), and the partner (PARTNER) in a conversational. The wearer indicates the person wearing the glasses, and the partner is the person who speaks directly to the wearer. The PARTNER speaker is located at forward-facing angles of -60 to +60 degrees and cross-talk is simulated from other directions. This configuration is labeled V4 in [^11].

### II-A Beamforming Front-end

In this work, the multiple beamformers preprocess the raw multi-channel audio into $K$ horizontal steering directions around the smart glasses device, plus one in the speaker‚Äôs mouth direction. Here, we use the predetermined beamformer weights with horizontal steering directions $K=4$ and $K=12$, leading to 5-channel and 13-channel beamformed outputs, respectively. In neural beamforming, we treat multiple beamformers as a convolutional layer, where we load predetermined beamformer weights as the model weights and update the weight using back-propagation. Specifically, we use BF and Neural BF to indicate pre-determined and neural beamformer, respectively.

### II-B Beamforming Design - NLCMV: Non-Linearly Constrained Minimum-Variance Beamforming

As shown in Fig 2, beamforming is one key component of the proposed system. A conventional beamformer algorithm, e.g., Minimum variance distortionless response (MVDR) [^10], aims to minimize the estimated beamformer output level while preserving the integrity of the desired signal. However, that approach neglects white noise during optimization and lacks control over null directions. To address these limitations, researchers have recently introduced a novel Non-Linearly Constrained Minimum Variance (NLCMV) beamforming [^20]. The NLCMV combines white noise gain and null direction control into its formulation. Here, given the number of point noise sources $N$, the weight of $n^{th}$ point noise, power spectral density (PSD) of point noise $\phi_{pp}$, beamformer weights $\bm{{h}}(j\omega)$ of each steering direction are optimized by minimizing the following:

$$
\displaystyle\scriptsize{\bm{{h}}^{H}(j\omega)\left[\bm{{\Phi}}_{dd}(j\omega)+%
\phi_{pp}(\omega)\sum_{n=1}^{N}\alpha_{p,n}\cdot\bm{{g}}_{n}(j\omega)\bm{{g}}_%
{n}^{H}(j\omega)\right]\bm{{h}}(j\omega)}
$$

which is subject to linear equality where $\bm{{h}}^{H}(j\omega)\cdot\bm{{g}}_{n}(j\omega)=1$ and a nonlinear inequality constraint that sets the limit on white noise gain $c(\omega)=\bm{{h}}^{H}(j\omega)\bm{{\Psi}}(j\omega)\bm{{h}}(j\omega)<=0$. Moreover, $\bm{{\Phi}}_{dd}(jw)$ is the covariance matrix of diffuse noise,

$$
\scriptsize{\bm{{\Psi}}(j\omega)=\textbf{I}-\bm{{g}}(j\omega)\bm{{g}}^{H}(j%
\omega)\cdot M\left/\left[\sum_{m=1}^{M}|G_{m}(j\omega)|^{2}\right]\right.,}
$$

where $G_{m}(j\omega)$ is the channel response from the target speech to the $m$ th of $M$ microphones and I is the identity matrix. The details of the beamformer design are described in [^20]. In this work, we adopt the NLCMV as our beamforming design.

### II-C Source Separation Back-end

Our source separation neural network follows an encoder-decoder architecture. From the $K+1$ beamformed channels, we first extract the STFT features. Next, we feed these time-frequency features to the encoder module consisting of multiple convolutional blocks with gated linear units (GLU) [^21] activation function and Dropout layers in between. Subsequently, the encoding output is applied to a 3-layer LSTM, which is then passed to a set of convolutional decoding layers. Then, we send the decoder output to a gating function that returns the STFT masks associated with the wearer and the partner speech from reference audio. In our proposed source separation architecture, we directly apply the first audio channel as the reference audio. Lastly, we compute the masked time-frequency outputs corresponding to the wearer and partner, which are then converted into the wearer and partner speech using the inverse STFT. The optimization objective in source separation modeling combines L1 loss, STFT loss, and Log SI-SDR loss [^22].

![Refer to caption](figures/fig3.png)

Figure 3: Two stage ASR and joint training ASR. Here, BF is multiple beamformers with K steering directions. In two-stage ASR, only the ASR model is trained, and in joint training, both source separation and ASR models are trained.

## III ASR Modeling

We further evaluate the source separation modeling through two ASR methods: two-stage ASR and joint ASR modeling.

### III-A Two-stage ASR Modeling with Source Separation

The two-stage ASR first extracts the wearer and the partner speech using the pre-trained source separation model. We then compute the log-mel from separate audios, which are subsequently fed into the ASR model. Our ASR network follows the Neural Transducer architecture [^23] [^24] [^25], including an encoder, a prediction network, and a joiner network. Our ASR modeling integrates serialized output training (SOT) [^26] [^27] and uses the alignment-restricted RNN-T loss [^23] as the training objective. In addition to relying solely on separate audio, we study combining the beamformed outputs with the separation output as the ASR input, resulting in $K+3$ -channel audio (3=2 separated audio signals + 1 speaker‚Äôs mouth direction).

### III-B Joint ASR Modeling with Source Separation

We investigate the joint training of ASR and source separation in addition to two-stage ASR training. Instead of training both models from scratch, we load the pre-trained ASR weights from two-stage ASR training and pre-trained source separation weights. We combine the ASR training objective with source separation loss to optimize both models in joint training.

## IV Experimental Setups

### IV-A Dataset Details

We conduct experiments using the open-source Librispeech corpus, which consists of 960 hours of speech from audiobooks in the LibriVox project [^28]. To simulate the training data, we generate 100,000 multichannel room impulse responses (RIRs) for rooms with sizes ranging from \[5, 5, 2\] to \[10, 10, 6\] meters. We apply the geometry of Aria glasses to simulate multi-channel data. Aria has 7 microphones. We generate the multi-channel signals using image-source methods (ISM) [^29]. The data simulation framework is adapted from [^11] [^20]. To better understand the impact of cross-talk and background noises on speech recognition, we generate several test scenarios varying the number of bystanders and SNR range, each containing 3367 utterances from Librispeech.

Furthermore, we add noise from the public noise set [^30] to the clean audio segments in both the training and test sets. The SNRs of the mixed audio range from -8 dB to 40 dB relative to the combined audio of the wearer and partner, with an incremental level of 1 dB. Increasingly, we select overlap ratios between the bystanders and the primary speakers, ranging from 5% to 50%. With an overlap ratio of 0%, there is no overlap between bystanders and main speakers (wearer and partner).

![Refer to caption](figures/fig4.png)

Figure 4: ASR baselines. BF is multiple beamformers.

### IV-B Directional Source Separation Training

Our source separation training uses Librispeech data. We perform different source separation training with the same architecture except for a different input dimension. We extracted 257-dimensional complex SFTF for each beamformer direction or raw microphone channel. Input features from multiple directions or channels are concatenated. We use an Adam optimizer with a tri-stage learning-rate scheduler. We trained the source separation models for 60 epochs, with a learning rate of 4e-4, a warmup of 10k iterations, and forced annealing after 10 epochs.

### IV-C ASR Training

We perform the ASR training in baseline and two-stage systems for 120 epochs. Like source separation training, ASR training uses an Adam optimizer, a base learning rate of 0.001, and a warmup of 10,000 iterations. On the other hand, we perform 30 epochs of joint training with the pre-trained ASR model and pre-trained source separation model on Librispeech data. We choose a learning rate of 1e-4 and use the equal weights of 1 in combining ASR loss and the source separation loss. We further compare ASR modeling relying on source separation with the following baseline ASR methods, as shown in Figure 4:

Directional ASR: We apply the directional ASR reported in [^11] as a baseline. Like the beamformer source separation, the directional ASR processes the multi-channel audio into $K+1$ beamformed channels, which are then fed into the ASR model.

Interchannel phase differences (IPDs): In addition to directional ASR, we design the baseline model using IPD features as the ASR input. IPDs capture the variations in phase between different audio channels, providing spatial properties of sound sources. We use the IPDs ASR system implemented in [^11].

TABLE I: Source separation performance comparisons, where the evaluation set includes only one bystander.

<table><thead><tr><th></th><th colspan="2">PESQ</th><th colspan="2">SI-SDR (dB)</th></tr><tr><th></th><th>Wearer</th><th>Partner</th><th>Wearer</th><th>Partner</th></tr><tr><th>Without BF - Baseline</th><th><math><semantics><mn>2.89</mn> <cn>2.89</cn> <annotation>2.89</annotation> <annotation>2.89</annotation></semantics></math></th><th><math><semantics><mn>1.80</mn> <cn>1.80</cn> <annotation>1.80</annotation> <annotation>1.80</annotation></semantics></math></th><th><math><semantics><mn>18.17</mn> <cn>18.17</cn> <annotation>18.17</annotation> <annotation>18.17</annotation></semantics></math></th><th><math><semantics><mn>8.50</mn> <cn>8.50</cn> <annotation>8.50</annotation> <annotation>8.50</annotation></semantics></math></th></tr></thead><tbody><tr><th>BF-5</th><td><math><semantics><mn>2.88</mn> <cn>2.88</cn> <annotation>2.88</annotation> <annotation>2.88</annotation></semantics></math></td><td><math><semantics><mn>1.82</mn> <cn>1.82</cn> <annotation>1.82</annotation> <annotation>1.82</annotation></semantics></math></td><td><math><semantics><mn>18.09</mn> <cn>18.09</cn> <annotation>18.09</annotation> <annotation>18.09</annotation></semantics></math></td><td><math><semantics><mn>8.55</mn> <cn>8.55</cn> <annotation>8.55</annotation> <annotation>8.55</annotation></semantics></math></td></tr><tr><th>BF-13</th><td><math><semantics><mn>2.95</mn> <cn>2.95</cn> <annotation>2.95</annotation> <annotation>2.95</annotation></semantics></math></td><td><math><semantics><mn>1.86</mn> <cn>1.86</cn> <annotation>1.86</annotation> <annotation>1.86</annotation></semantics></math></td><td><math><semantics><mn>18.33</mn> <cn>18.33</cn> <annotation>18.33</annotation> <annotation>18.33</annotation></semantics></math></td><td><math><semantics><mn>8.83</mn> <cn>8.83</cn> <annotation>8.83</annotation> <annotation>8.83</annotation></semantics></math></td></tr><tr><th>Neural BF-13(Ours)</th><td><math><semantics><mrow><mn>3.11</mn> <mo>‚Ü?/mo></mrow> <apply><ci>‚Ü?/ci> <cn>3.11</cn> <csymbol>absent</csymbol></apply> <annotation>\mathbf{3.11}\uparrow</annotation> <annotation>bold_3.11 ‚Ü?/annotation></semantics></math></td><td><math><semantics><mrow><mn>1.89</mn> <mo>‚Ü?/mo></mrow> <apply><ci>‚Ü?/ci> <cn>1.89</cn> <csymbol>absent</csymbol></apply> <annotation>\mathbf{1.89}\uparrow</annotation> <annotation>bold_1.89 ‚Ü?/annotation></semantics></math></td><td><math><semantics><mrow><mn>20.44</mn> <mo>‚Ü?/mo></mrow> <apply><ci>‚Ü?/ci> <cn>20.44</cn> <csymbol>absent</csymbol></apply> <annotation>\mathbf{20.44}\uparrow</annotation> <annotation>bold_20.44 ‚Ü?/annotation></semantics></math></td><td><math><semantics><mrow><mn>9.51</mn> <mo>‚Ü?/mo></mrow> <apply><ci>‚Ü?/ci> <cn>9.51</cn> <csymbol>absent</csymbol></apply> <annotation>\mathbf{9.51}\uparrow</annotation> <annotation>bold_9.51 ‚Ü?/annotation></semantics></math></td></tr></tbody></table>

![Refer to caption](figures/fig5.png)

Figure 5: Source separation varying number of bystanders.

## V Source Separation Findings

### V-A Directional Information Benefits Source Separation

We first compare the source separation with and without directional information in Table I, quantified using the perceptual evaluation of speech quality (PESQ) [^31] and Scale-Invariant Signal-to-Distortion Ratio (SI-SDR) [^32]. The baseline system employs a similar encoder and decoder architecture as depicted in Fig.2, but it utilizes the complex short-time Fourier transform (STFT) features of 7-channel raw microphone signals without beamforming. We refer to the directional source separation as BF-5 and BF-13, where 5 and 13 indicate the number of beamformed channels. The results show that increasing beamforming directions improves the source separation, and BF-13 achieves approximately 0.25 dB performance gain over BF-5 in both wearer and partner output. Moreover, BF-13 with directional information yields higher voice quality than the baseline multi-channel source separation in both PESQ and SI-SDR.

![Refer to caption](figures/fig6.png)

Figure 6: Beam patterns at f = 250 ùëì f=250 italic\_f = 250 Hz

### V-B Improve Source Separation by Neural Beamforming

Next, we study the source separation using neural beamforming, as shown in Table I. We find that neural BF-13 substantially improves separation quality, leading to a 2.27 dB and a 1.01 dB SI-SDI increase in the wearer and partner signals, respectively. We also observe an increase in PESQ for wearer and partner separation outputs. In addition to evaluating the condition with one bystander, we compare the voice quality varying (2 and 3) bystanders nearby. The results in Fig. 5 show that neural BF-13 is more robust against increased bystanders than multi-channel and non-neural beamformer methods.

### V-C Interpreting Neural Beamforming

Neural beamforming offers encouraging source separation performance, as shown in Table I, but it is unclear why it improves source separation. To unfold what neural beamforming learns, we perform a detailed beamformer analysis as shown in Fig 6. The plot depicts the beam patterns of the beamformers in 3 distinct directions. We find that neural beamformers have substantial gains (over 10 dB) in the lateral directions (left and right), potentially leading to improved overall source separation.

TABLE II: ASR performance comparisons on LibriSpeech data, where the evaluation set includes only one bystander.

<table><tbody><tr><th>ASR</th><th>Source</th><td colspan="3">WER</td></tr><tr><th>Training</th><th>Separation</th><td>Overall</td><td>Wearer</td><td>Partner</td></tr><tr><th>IPDs</th><th>N.A.</th><td><math><semantics><mn>15.12</mn> <cn>15.12</cn> <annotation>15.12</annotation> <annotation>15.12</annotation></semantics></math></td><td><math><semantics><mn>7.99</mn> <cn>7.99</cn> <annotation>7.99</annotation> <annotation>7.99</annotation></semantics></math></td><td><math><semantics><mn>22.33</mn> <cn>22.33</cn> <annotation>22.33</annotation> <annotation>22.33</annotation></semantics></math></td></tr><tr><th>Dir. ASR BF-13</th><th>N.A.</th><td><math><semantics><mn>14.14</mn> <cn>14.14</cn> <annotation>14.14</annotation> <annotation>14.14</annotation></semantics></math></td><td><math><semantics><mn>8.28</mn> <cn>8.28</cn> <annotation>8.28</annotation> <annotation>8.28</annotation></semantics></math></td><td><math><semantics><mn>20.12</mn> <cn>20.12</cn> <annotation>20.12</annotation> <annotation>20.12</annotation></semantics></math></td></tr><tr><th>Two-stage</th><th>Without BF</th><td><math><semantics><mn>17.28</mn> <cn>17.28</cn> <annotation>17.28</annotation> <annotation>17.28</annotation></semantics></math></td><td><math><semantics><mn>6.79</mn> <cn>6.79</cn> <annotation>6.79</annotation> <annotation>6.79</annotation></semantics></math></td><td><math><semantics><mn>27.69</mn> <cn>27.69</cn> <annotation>27.69</annotation> <annotation>27.69</annotation></semantics></math></td></tr><tr><th>Two-stage</th><th>BF-13</th><td><math><semantics><mn>17.06</mn> <cn>17.06</cn> <annotation>17.06</annotation> <annotation>17.06</annotation></semantics></math></td><td><math><semantics><mn>7.13</mn> <cn>7.13</cn> <annotation>7.13</annotation> <annotation>7.13</annotation></semantics></math></td><td><math><semantics><mn>27.07</mn> <cn>27.07</cn> <annotation>27.07</annotation> <annotation>27.07</annotation></semantics></math></td></tr><tr><th>Two-stage</th><th>Neural BF-13</th><td><math><semantics><mn>16.04</mn> <cn>16.04</cn> <annotation>16.04</annotation> <annotation>16.04</annotation></semantics></math></td><td><math><semantics><mn>6.51</mn> <cn>6.51</cn> <annotation>\mathbf{6.51}</annotation> <annotation>bold_6.51</annotation></semantics></math></td><td><math><semantics><mn>25.46</mn> <cn>25.46</cn> <annotation>25.46</annotation> <annotation>25.46</annotation></semantics></math></td></tr><tr><th>Two-stage Fusion</th><th>Neural BF-13</th><td><math><semantics><mn>13.70</mn> <cn>13.70</cn> <annotation>13.70</annotation> <annotation>13.70</annotation></semantics></math></td><td><math><semantics><mn>6.65</mn> <cn>6.65</cn> <annotation>6.65</annotation> <annotation>6.65</annotation></semantics></math></td><td><math><semantics><mn>20.66</mn> <cn>20.66</cn> <annotation>20.66</annotation> <annotation>20.66</annotation></semantics></math></td></tr><tr><th>Joint Train Fusion</th><th>Neural BF-13</th><td><math><semantics><mn>13.25</mn> <cn>13.25</cn> <annotation>\mathbf{13.25}</annotation> <annotation>bold_13.25</annotation></semantics></math></td><td><math><semantics><mn>8.06</mn> <cn>8.06</cn> <annotation>{8.06}</annotation> <annotation>8.06</annotation></semantics></math></td><td><math><semantics><mn>18.89</mn> <cn>18.89</cn> <annotation>\mathbf{18.89}</annotation> <annotation>bold_18.89</annotation></semantics></math></td></tr></tbody></table>

## VI ASR Findings

### VI-A Source Separation Benefits ASR on Smart Glasses

This paragraph compares the ASR performance between baselines and two-stage ASR systems, as demonstrated in Tab. II. Here, two-stage fusion refers to the two-stage ASR that combines beamformed outputs with the separation outputs, and the two-stage represents the ASR model using only separation outputs. The results show that two-stage ASR outperforms IPDs and directional ASR for wearer speech, indicating improved quality of the wearer speech from source separation. We also observe that the source separation with neural beamforming (Neural BF) yields lower WER than baseline source separation (without BF). However, partner speech suffers a substantial WER increase among all two-stage systems. This result implies far-field speech separation remains a challenging task, and the relatively lower separation quality for partner speech causes performance decreases in the ASR. We perform the two-stage fusion ASR modeling (with neural BF-13), which combines raw multi-channel audio with separation output, to resolve this quality issue from source separation, resulting in overall and wearer ASR performance improvements (WER: 13.70%) compared to the directional ASR system (WER: 14.14%).

![Refer to caption](figures/fig7.png)

Figure 7: ASR performance varying number of bystanders.

### VI-B Improve ASR Performance by Joint Training

Table II reveals that joint training with the best ASR system from the two-stage fusion training (with Neural BF-13) would improve ASR performance, reducing overall WER to 13.25% compared to 14.14% using directional ASR. Increasingly, we identify that joint training yields an increased WER for the wearer but reduces WER for partner speech compared to two-stage ASR. Unlike source separation modeling that only yields ASR improvements for wearer speech, joint training strikes a delicate balance in improving speech recognition in all main speakers. We further compare the ASR performance using joint training to other ASR models with varying bystanders, as shown in Figure 7. The comparisons indicate that joint training also yields more robust partner ASR performance with increasing bystanders, creating a larger relative WER difference (WER difference increases from 1.76% to 2.86%) with 3 bystanders.

## VII Conclusion

In this work, we conduct a comprehensive study of directional source separation with the multi-channel microphone array on the geometry of smart glasses, demonstrating the effectiveness of incorporating directional information in source separation. In addition. Our experiments also imply that learning directional properties as a part of the neural network further improves voice quality. Lastly, we demonstrate that source separation benefits ASR performance, with joint training of source separation and ASR yields the lowest WER. One future work would investigate fairness and efficiency [^33] in source separation.

[^1]: Nicky Kern, Bernt Schiele, Holger Junker, Paul Lukowicz, and Gerhard Troster, ‚ÄúWearable sensing to annotate meeting recordings,‚Ä?in Proceedings. Sixth International Symposium on Wearable Computers,. IEEE, 2002, pp. 186‚Ä?93.

[^2]: Tiantian Feng, Amrutha Nadarajan, et al., ‚ÄúTiles audio recorder: an unobtrusive wearable solution to track audio activity,‚Ä?in Proc. of the 4th ACM Workshop on Wearable Systems and Applications, 2018, pp. 33‚Ä?8.

[^3]: Arindam Dey, Mark Billinghurst, Robert W Lindeman, and J Edward Swan, ‚ÄúA systematic review of 10 years of augmented reality usability studies: 2005 to 2014,‚Ä?Frontiers in Robotics and AI, vol. 5, pp. 37, 2018.

[^4]: Kiran Somasundaram, Jing Dong, Huixuan Tang, Julian Straub, Mingfei Yan, et al., ‚ÄúProject aria: A new tool for egocentric multi-modal ai research,‚Ä?arXiv preprint arXiv:2308.13561, 2023.

[^5]: Yanzhang He, Tara N Sainath, Rohit Prabhavalkar, Ian McGraw, et al., ‚ÄúStreaming end-to-end speech recognition for mobile devices,‚Ä?in 2019 IEEE International Conf. on Acoustics, Speech and Signal Processing (ICASSP), pp. 6381‚Ä?385.

[^6]: DeLiang Wang and Jitong Chen, ‚ÄúSupervised speech separation based on deep learning: An overview,‚Ä?IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 26, no. 10, pp. 1702‚Ä?726, 2018.

[^7]: Cem Subakan, Mirco Ravanelli, Samuele Cornell, Mirko Bronzi, and Jianyuan Zhong, ‚ÄúAttention is all you need in speech separation,‚Ä?in IEEE International Conf. on Acoustics, Speech and Signal Processing (ICASSP), 2021, pp. 21‚Ä?5.

[^8]: Yi Luo, Zhuo Chen, and Takuya Yoshioka, ‚ÄúDual-path rnn: efficient long sequence modeling for time-domain single-channel speech separation,‚Ä?in 2020 IEEE International Conf. on Acoustics, Speech, and Signal Processing, pp. 46‚Ä?0.

[^9]: Jacob Benesty, Jingdong Chen, and Yiteng Huang, Microphone array signal processing, vol. 1, Springer Science & Business Media, 2008.

[^10]: Jack Capon, ‚ÄúHigh-resolution frequency-wavenumber spectrum analysis,‚Ä?Proc. of the IEEE, vol. 57, no. 8, pp. 1408‚Ä?418, 1969.

[^11]: Ju Lin, Niko Moritz, Ruiming Xie, Kaustubh Kalgaonkar, Christian Fuegen, and Frank Seide, ‚ÄúDirectional Speech Recognition for Speaker Disambiguation and Cross-talk Suppression,‚Ä?in Proc. INTERSPEECH, 2023, pp. 3522‚Ä?526.

[^12]: Bo Li, Tara N Sainath, Ron J Weiss, Kevin W Wilson, and Michiel Bacchiani, ‚ÄúNeural network adaptive beamforming for robust multichannel speech recognition,‚Ä?2016.

[^13]: Tsubasa Ochiai, Shinji Watanabe, Takaaki Hori, John R Hershey, and Xiong Xiao, ‚ÄúUnified architecture for multichannel end-to-end speech recognition with neural beamforming,‚Ä?IEEE Journal of Selected Topics in Signal Processing, vol. 11, no. 8, pp. 1274‚Ä?288, 2017.

[^14]: Tara N Sainath, Ron J Weiss, Kevin W Wilson, Arun Narayanan, and Michiel Bacchiani, ‚ÄúFactored spatial and spectral multichannel raw waveform cldnns,‚Ä?in 2016 IEEE International Conf. on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2016, pp. 5075‚Ä?079.

[^15]: Weipeng He, Lu Lu, Biqiao Zhang, Jay Mahadeokar, Kaustubh Kalgaonkar, and Christian Fuegen, ‚ÄúSpatial attention for far-field speech recognition with deep beamforming neural networks,‚Ä?in 2020 IEEE International Conf. on Acoustics, Speech and Signal Processing (ICASSP), pp. 7499‚Ä?503.

[^16]: Xiong Xiao, Shinji Watanabe, Hakan Erdogan, Liang Lu, John Hershey, Michael L Seltzer, et al., ‚ÄúDeep beamforming networks for multi-channel speech recognition,‚Ä?in IEEE International Conf. on Acoustics, Speech and Signal Processing (ICASSP), 2016, pp. 5745‚Ä?749.

[^17]: Stefan Braun, Daniel Neil, Jithendar Anumula, Enea Ceolini, and Shih-Chii Liu, ‚ÄúAttention-driven multi-sensor selection,‚Ä?in 2019 International Joint Conf. on Neural Networks (IJCNN). IEEE, 2019, pp. 1‚Ä?.

[^18]: Bo Li, Tara N Sainath, Arun Narayanan, Joe Caroselli, Michiel Bacchiani, Ananya Misra, Izhak Shafran, et al., ‚ÄúAcoustic modeling for google home.,‚Ä?in Interspeech, 2017, pp. 399‚Ä?03.

[^19]: Aditya Arie Nugraha, Antoine Liutkus, and Emmanuel Vincent, ‚ÄúMultichannel audio source separation with deep neural networks,‚Ä?IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 24, no. 9, pp. 1652‚Ä?664, 2016.

[^20]: Ju Lin, Niko Moritz, Yiteng Huang, Ruiming Xie, Ming Sun, Christian Fuegen, and Frank Seide, ‚ÄúAgadir: Towards array-geometry agnostic directional speech recognition,‚Ä?arXiv preprint arXiv:2401.10411, 2024.

[^21]: Yann N Dauphin, Angela Fan, Michael Auli, and David Grangier, ‚ÄúLanguage modeling with gated convolutional networks,‚Ä?in International conference on machine learning. PMLR, 2017, pp. 933‚Ä?41.

[^22]: Ju Lin, Kaustubh Kalgaonkar, Qing He, and Xin Lei, ‚ÄúSpeech enhancement for low bit rate speech codec,‚Ä?in ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2022, pp. 7777‚Ä?781.

[^23]: Jay Mahadeokar, Yuan Shangguan, Duc Le, Gil Keren, Hang Su, Thong Le, Ching-Feng Yeh, Christian Fuegen, and Michael L Seltzer, ‚ÄúAlignment restricted streaming recurrent neural network transducer,‚Ä?in 2021 IEEE Spoken Language Technology Workshop (SLT). IEEE, 2021, pp. 52‚Ä?9.

[^24]: Niko Moritz, Frank Seide, Duc Le, Jay Mahadeokar, and Christian Fuegen, ‚ÄúAn investigation of monotonic transducers for large-scale automatic speech recognition,‚Ä?in 2022 IEEE Spoken Language Technology Workshop (SLT), pp. 324‚Ä?30.

[^25]: Tara N Sainath, Yanzhang He, Bo Li, Arun Narayanan, Ruoming Pang, et al., ‚ÄúA streaming on-device end-to-end model surpassing server-side conventional model quality and latency,‚Ä?in 2020 IEEE International Conference on Acoustics, Speech and Signal Processing, pp. 6059‚Ä?063.

[^26]: Naoyuki Kanda, Jian Wu, Yu Wu, Xiong Xiao, Zhong Meng, Xiaofei Wang, Yashesh Gaur, Zhuo Chen, Jinyu Li, and Takuya Yoshioka, ‚ÄúStreaming multi-talker asr with token-level serialized output training,‚Ä?arXiv preprint arXiv:2202.00842, 2022.

[^27]: Xuankai Chang, Niko Moritz, Takaaki Hori, Shinji Watanabe, and Jonathan Le Roux, ‚ÄúExtended graph temporal classification for multi-speaker end-to-end asr,‚Ä?in 2022 IEEE International Conf. on Acoustics, Speech and Signal Processing, pp. 7322‚Ä?326.

[^28]: Vassil Panayotov, Guoguo Chen, Daniel Povey, and Sanjeev Khudanpur, ‚ÄúLibrispeech: an asr corpus based on public domain audio books,‚Ä?in 2015 IEEE International Conf. on Acoustics, Speech and Signal Processing, pp. 5206‚Ä?210.

[^29]: Eric A Lehmann and Anders M Johansson, ‚ÄúPrediction of energy decay in room impulse responses simulated with an image-source model,‚Ä?The Journal of the Acoustical Society of America, vol. 124, no. 1, pp. 269‚Ä?77, 2008.

[^30]: Chandan KA Reddy, Vishak Gopal, Ross Cutler, Ebrahim Beyrami, Roger Cheng, Harishchandra Dubey, et al., ‚ÄúThe interspeech 2020 deep noise suppression challenge: Datasets, subjective testing framework, and challenge results,‚Ä?in INTERSPEECH, 2020.

[^31]: Antony W Rix, John G Beerends, Michael P Hollier, and Andries P Hekstra, ‚ÄúPerceptual evaluation of speech quality - a new method for speech quality assessment of telephone networks and codecs,‚Ä?in 2001 IEEE International Conf. on Acoustics, Speech and Signal Processing, vol. 2, pp. 749‚Ä?52.

[^32]: Jonathan Le Roux, Scott Wisdom, Hakan Erdogan, and John R Hershey, ‚ÄúSdr‚Äìhalf-baked or well done?,‚Ä?in 2019 IEEE International Conf. on Acoustics, Speech and Signal Processing, pp. 626‚Ä?30.

[^33]: Tiantian Feng, Rajat Hebbar, Nicholas Mehlman, Xuan Shi, Aditya Kommineni, and Shrikanth Narayanan, ‚ÄúA review of speech-centric trustworthy machine learning: Privacy, safety, and fairness,‚Ä?APSIPA Trans. on Signal and Information Processing, vol. 12, no. 3, 2023.
