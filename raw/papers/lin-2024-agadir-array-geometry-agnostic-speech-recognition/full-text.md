###### Abstract

Wearable devices like smart glasses are approaching the compute capability to seamlessly generate real-time closed captions for live conversations. We build on our recently introduced directional Automatic Speech Recognition (ASR) for smart glasses that have microphone arrays, which fuses multi-channel ASR with serialized output training, for wearer/conversation-partner disambiguation as well as suppression of cross-talk speech from non-target directions and noise.

When ASR work is part of a broader system-development process, one may be faced with changes to microphone geometries as system development progresses.

This paper aims to make multi-channel ASR insensitive to limited variations of microphone-array geometry. We show that a model trained on multiple similar geometries is largely agnostic and generalizes well to new geometries, as long as they are not too different. Furthermore, training the model this way improves accuracy for seen geometries by 15 to 28% relative. Lastly, we refine the beamforming by a novel Non-Linearly Constrained Minimum Variance criterion.

## 1 Introduction

Automatically transcribing a conversation partner at a distance of several feet is an important emerging ASR scenario. Consider a wearable device that automatically generates captions for deaf or hearing-impaired users. Background noise, reverberation, overlapping speech, and interfering speakers make this challenging. To remedy, one can capture the speech with a microphone array—like we humans do with binaural hearing. Microphone-array methods traditionally aim to improve the SNR of target speech—but one can do better by multi-channel Automatic Speech Recognition (ASR).

This paper extends our recently proposed directional speech-recognition system for real-time closed captions of conversations on smart glasses. That model receives multiple beamformed signals simultaneously, allowing the ASR model itself, in an end-to-end fashion, to disambiguate who is speaking between the wearer, the conversation partner, and unrelated bystanders, while also being more noise-robust than ASR on single-channel beamformed signals [^1].

This paper aims to make the multi-channel model less sensitive to minute details of the specific microphone-array geometry, striving for Array-Geometry Agnostic Directional Speech Recognition, or AGADIR. Why? On smart glasses, the mic array competes with other components in terms of space and other considerations. During system development, consecutive prototypes tend to undergo alterations of microphone placement. A multi-channel ASR model that is agnostic to limited geometry changes could be shared across a sequence of prototypes, e.g. for user studies, saving time and energy consumption. It would allow predicting system accuracy for new configurations without new test data. Our experiments on both simulated and real test data show that a model that is simply trained on multiple similar geometries is indeed agnostic to limited geometry variations and even leads to better WER (although it finds its limits for larger geometry changes).

Related work on geometry agnosticity includes [^2], which proposes a causal geometry-agnostic multi-channel speech enhancement system that leverages speaker embeddings and spatial features serving as the front-end for speech recognition. An array geometry-agnostic speech separation neural network model named VarArray, was proposed in [^3], which could be seamlessly integrated into diverse array configurations for streaming multi-talker ASR in [^4].

MIMO-speech [^5] is a multichannel end-to-end neural network that defines source-specific time-frequency masks as latent variables in the network, which in turn are used to transcribe the individual sources. This was improved by incorporating an explicit localization sub-network. Recent studies [^6] [^7] in ASR and speaker separation have investigated direct incorporation of spatial features instead of using explicit sub-modules jointly trained with the ASR module. For example, [^8] proposed to estimate a target-speaker mask with multi-aspect features to extract the target speaker from a speech mixture. The extracted speech is then fed to ASR. Recently neural beamforming was also explored for multi-channel ASR [^9] [^10].

## 2 Directional ASR System Architecture

Fig. 1 illustrates the system architecture of our directional speech-recognition system. It is comprised of beamformers, feature front-end, and a streaming RNN-T based ASR system trained with serialized output training, or SOT. We will describe these components in detail in the following subsections.

### 2.1 NLCMV: Non-Linearly Constrained Minimum-Variance beamforming

Beamforming is one key component of our system for both speaker-tag detection and cross-talk suppression. Hence, our first stage is to process the raw multi-channel audio by a set of $K+1$ fixed beamformers; $K$ horizontal steering directions around the smart-glasses device plus one towards the speaker’s mouth direction. These beamformers use predetermined coefficients. This converts the problem from comparing raw phase differences to one of comparing magnitudes and feature characteristics across multiple steering directions.

![Refer to caption](figures/x1.png)

Fig. 1: Proposed Array-geometry agnostic directional speech recognition architecture.

Our previous work [^1] used a conventional beamformer algorithm, Minimum variance distortionless response (MVDR) [^11], which aims to minimize the estimated beamformer output level while preserving the integrity of the desired signal. That approach lacks control over null directions, which can vary significantly across different frequencies, and neglects white noise during optimization. In this paper, we refine the beamformer by introducing a novel Non-Linearly Constrained Minimum Variance (NLCMV) criterion, which incorporates white noise gain and null direction control into its formulation. Specifically, NLCMV optimizes the beamformer weights $\bm{{h}}(jw)$ of each steering direction by minimizing

$$
\displaystyle\footnotesize{\bm{{h}}^{H}(j\omega)\left[\bm{{\Phi}}_{dd}(j\omega%
)+\underbrace{\phi_{pp}(w)\sum_{n=1}^{N}\alpha_{p,n}\cdot\bm{{g}}_{n}(j\omega)%
\bm{{g}}_{n}^{H}(j\omega)}_{\text{soft control of null directions}}\right]\bm{%
{h}}(j\omega)}
$$

which is subject to the linear equality and nonlinear inequality constraints, which are simplified to the following form:

$$
\left\{\begin{aligned} &\bm{{h}}^{H}{(j\omega)}\bm{{g}}{(j\omega)}=1,\\
&c(w)\triangleq\underbrace{\bm{{h}}^{H}({j\omega})\bm{{\Psi}}(j\omega)\bm{{h}}%
(j\omega)<=0}_{\text{constraint on white noise gain.}},\end{aligned}\right.
$$

where $\bm{{\Phi}}_{dd}(jw)$ is the covariance matrix of diffuse noise,

$$
\footnotesize{\bm{{\Psi}}(j\omega)\triangleq\textbf{I}-\bm{{g}}(j\omega)\bm{{g%
}}^{H}(j\omega)\cdot M\left/\left[\sum_{m=1}^{M}|G_{m}(j\omega)|^{2}\right]%
\right.,}
$$

The $G_{m}(j\omega)$ are measured channel responses from the target speech source to the $m$ -th of $M$ microphones (ATFs), $N$ is the number of point noise sources, $\phi_{pp}(w)$ is the PSD of point noise, $\alpha_{p,n}$ is the $n$ th point noise weight, and I is the identity matrix.

For illustration, Fig. 2 compares NLCMV beam patterns to conventional delay-and-sum and super-directive ones [^12] [^13] [^14]. Compared to super-directive, NLCMV achieves a superior 10dB gain at the designated look direction, such as backwards, and early ASR tests on real data showed roughly a 0.7% absolute WER gain.

### 2.2 Convolutional front-end

From the multiple channels received from the beamformers, we next extract per-channel log-Mel features (which are normalized w.r.t. corpus mean/variance for better convergence). I.e. instead of feature vectors as in regular single-channel ASR, we have feature tensors, where the second dimension represents the steering direction. Note that log-Mel processing removes phase information which in raw audio carries the directional information. That is OK, since this information has already been perused by the beamformers, and is therefore at this point reflected as amplitude information.

![Refer to caption](figures/x2.png)

Fig. 2: Beam patterns at 1000Hz for Aria glasses on 4 directions.

Unlike our previous work [^1], we add two convolutional blocks to further refine the extracted log-mel features. Each convolutional block is composed of a 2-D convolutional layer, succeeded by batch normalization [^15], and utilizes gated linear units (GLU) [^16] as the activation function. I.e., while our previous system [^1] just concatenated all features from all beams and linearly projected then, we now leverage a convolutional front-end aiming to retain more directional information by keeping the channels separate for a few more layers, while simultaneously reducing the feature dimension through a stride of 2. On a setup similar to this paper’s results section, this improved the speaker-attributed WER by an absolute 1.3%.

<table><tbody><tr><th rowspan="2">Model</th><th rowspan="2">Data</th><td colspan="3">WER%, Aria <math><semantics><msub><mi>A</mi></msub> <apply><ci>A</ci></apply> <annotation>{}_{\mathrm{A}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_A end_FLOATSUBSCRIPT</annotation></semantics></math></td><td colspan="3">WER%, Comp <math><semantics><msub><mi>A</mi></msub> <apply><ci>A</ci></apply> <annotation>{}_{\mathrm{A}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_A end_FLOATSUBSCRIPT</annotation></semantics></math></td><td colspan="3">WER%, Comp <math><semantics><msub><mi>B</mi></msub> <apply><ci>B</ci></apply> <annotation>{}_{\mathrm{B}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_B end_FLOATSUBSCRIPT</annotation></semantics></math></td><td colspan="3">WER%, Comp <math><semantics><msub><mi>C</mi></msub> <apply><ci>C</ci></apply> <annotation>{}_{\mathrm{C}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_C end_FLOATSUBSCRIPT</annotation></semantics></math></td><td colspan="3">WER%, Comp <math><semantics><msub><mi>D</mi></msub> <apply><ci>D</ci></apply> <annotation>{}_{\mathrm{D}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_D end_FLOATSUBSCRIPT</annotation></semantics></math></td></tr><tr><td>u/a</td><td>self</td><td>other</td><td>u/a</td><td>self</td><td>other</td><td>u/a</td><td>self</td><td>other</td><td>u/a</td><td>self</td><td>other</td><td>u/a</td><td>self</td><td>other</td></tr><tr><th colspan="17">w/o noise and w/o bystanders</th></tr><tr><th>Matching geometry</th><th>100%</th><td>8.0</td><td>8.0</td><td>8.1</td><td>8.4</td><td>8.2</td><td>8.6</td><td>8.3</td><td>8.1</td><td>8.4</td><td>8.0</td><td>8.2</td><td>7.9</td><td>8.0</td><td>8.0</td><td>7.9</td></tr><tr><th>Multi-geometry</th><th>5 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> 20%</th><td>6.1</td><td>6.2</td><td>6.5</td><td>6.2</td><td>6.1</td><td>6.4</td><td>6.1</td><td>6.0</td><td>6.2</td><td>6.1</td><td>6.0</td><td>6.1</td><td>6.1</td><td>6.1</td><td>6.3</td></tr><tr><th>Geometry-agnostic</th><th>5 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> 20%</th><td>6.3</td><td>6.5</td><td>6.5</td><td>6.3</td><td>6.3</td><td>6.3</td><td>6.0</td><td>6.2</td><td>5.8</td><td>6.1</td><td>6.2</td><td>6.1</td><td>6.2</td><td>6.2</td><td>6.2</td></tr><tr><th colspan="17">w/ noise and w/ bystanders, overlap ratio 0%</th></tr><tr><th>Matching geometry</th><th>100%</th><td>20.5</td><td>12.0</td><td>27.6</td><td>19.1</td><td>11.2</td><td>25.7</td><td>19.8</td><td>11.5</td><td>26.6</td><td>18.8</td><td>10.9</td><td>25.3</td><td>18.8</td><td>11.1</td><td>25.1</td></tr><tr><th>Mismatching geometry</th><th>100%</th><td>36.5</td><td>53.5</td><td>50.1</td><td>31.1</td><td>18.8</td><td>41.6</td><td>34.4</td><td>22.2</td><td>51.4</td><td>22.0</td><td>12.3</td><td>30.2</td><td>19.6</td><td>11.1</td><td>26.6</td></tr><tr><th>Multi-geometry</th><th>5 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> 20%</th><td>16.3</td><td>8.9</td><td>22.7</td><td>16.2</td><td>8.4</td><td>22.6</td><td>15.2</td><td>8.1</td><td>21.2</td><td>15.3</td><td>8.2</td><td>21.3</td><td>15.2</td><td>8.2</td><td>21.0</td></tr><tr><th>Geometry-agnostic</th><th>5 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> 20%</th><td>16.7</td><td>9.6</td><td>23.2</td><td>16.7</td><td>8.8</td><td>22.9</td><td>15.6</td><td>8.5</td><td>21.6</td><td>15.6</td><td>8.5</td><td>21.4</td><td>15.7</td><td>8.4</td><td>21.6</td></tr><tr><th colspan="17">w/ noise and w/ bystanders, overlap ratio 50%</th></tr><tr><th>Matching geometry</th><th>100%</th><td>21.6</td><td>12.6</td><td>28.9</td><td>20.5</td><td>11.7</td><td>27.9</td><td>21.2</td><td>12.1</td><td>28.6</td><td>19.6</td><td>11.2</td><td>26.5</td><td>20.5</td><td>11.7</td><td>27.9</td></tr><tr><th>Multi-geometry</th><th>5 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> 20%</th><td>17.0</td><td>9.4</td><td>23.5</td><td>17.3</td><td>8.7</td><td>24.4</td><td>16.4</td><td>8.5</td><td>23.0</td><td>16.0</td><td>8.4</td><td>22.3</td><td>16.3</td><td>8.4</td><td>22.7</td></tr><tr><th>Geometry-agnostic</th><th>5 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> 20%</th><td>17.6</td><td>9.9</td><td>24.2</td><td>17.8</td><td>9.1</td><td>24.9</td><td>16.8</td><td>8.9</td><td>23.4</td><td>16.2</td><td>8.6</td><td>22.6</td><td>16.6</td><td>8.6</td><td>23.1</td></tr></tbody></table>

Table 1: Speaker un-attributed (”u/a”) and attributed (”self”, ”other”) word error rates (WER) on simulated test data for five different array geometries, with ”Matching geometry” (same array in training and test), ”Multi-geometry” (multiple geometries with matching array-id embedding, applied to 20% of the data, resp.), and ”Geometry-agnostic” (multiple without array id). ”Mismatching geometry” uses a model trained on the respective geometry one column to the left (or on Comp ${}_{\mathrm{D}}$ for Aria ${}_{\mathrm{A}}$).

### 2.3 Streaming ASR with Serialized Output Training

Our streaming ASR model is the same as [^1]: a Neural Transducer [^17] [^18] [^19] [^20], specifically a Recurrent Neural Network Transducer, or RNN-T, that consists of three components: an encoder, a prediction network, and a joiner network. There is no external language model. As in [^1], multi-talker overlapped speech is handled via serialized output training, or SOT [^21] [^22], where the model is trained to insert tags marking speaker changes—in our case between the wearer and a target speaker (other). The training process uses the ”alignment-restricted RNN-T” (AR-RNN-T) technique [^17] for acceleration.

## 3 Experiments and Results

### 3.1 Dataset

Models are trained on an in-house dataset of 14.6k hours of de-identified video data that is publicly shared by Facebook users—single-channel audio. As real multi-channel training data of sufficient amounts is not available, all multi-channel training data for all microphone-array geometries must be simulated. We first generate 1M multi-channel room impulse responses (RIRs) using image-source methods (ISM) [^23] via the “pyroomacoustics” library [^24]. Room sizes range from \[5, 5, 2\] to \[10, 10, 6\] meters. We then simulate training data by placing single-channel audio clips in space as the wearer (”self”), the conversation partner (”other”), and unrelated bystanders, simulating a conversation between self and other with some overlap, and bystander crosstalk. The ”other” speech is located at forward-facing angles of -60 to +60 ${}^{\circ}$, while the bystander is positioned at random locations outside that range (i.e. left, right, or behind the wearer). (In [^1], this configuration is labeled V4.)

We evaluate our proposed methods on both real and simulated test sets. The simulated set consists of an additional 3.7 hours of in-house video, converted to multi-channel via simulation like the training data, except using different simulated RIRs. Additionally, real test data was collected consisting of conversations between a wearer wearing Project Aria prototyping glasses (Section 3.2) and a conversation partner at a distance of around 4 to 6 feet. All data is bilingual (”self” speaks English while ”other” speaks Spanish).

Lastly, noise from the DNS Challenge [^25] was added to the clean audio segments in training and test, at SNRs ranging from $-5$ to 30 dB w.r.t. the combined audio of wearer and partner, at intervals of 1 dB. Three overlap configurations between bystanders and main speakers are investigated: no crosstalk, crosstalk not overlapping (0%), and 50% overlap with the main speakers (self or other).

### 3.2 Devices

Two hardware devices were used in this work, the publicly available Project Aria glasses [^26] and a composite hardware prototype that combines several microphone geometries for evaluating microphone placements. For both, measurements of Acoustic Transfer Functions (ATFs) for all microphones were available to us and were used for the beamformer design (Section 2.1). Unfortunately, unlike Aria, the composite prototype is mechanically not suitable for collecting real conversations, relegating us to simulated test data for it.

![Refer to caption](figures/x3.png)

Fig. 3: Microphone locations on Project Aria glasses 26.

For our application, we target microphone arrays of 5 channels. Both hardware devices have more microphones than that. This way, we can experiment with multiple 5-channel configurations by dropping different sets of microphones. We define two 5-channel subsets for Aria named Aria ${}_{\mathrm{A}}$ (seen in training, using Mic2, Mic3, Mic4, Mic5, and Mic6 per Fig. 3) and Aria ${}_{\mathrm{B}}$ (not seen in training, substituting nose Mic0 in place of Mic2). From the composite prototype, we derive five meaningful configurations labeled Comp ${}_{\mathrm{A}}$, Comp ${}_{\mathrm{B}}$, Comp ${}_{\mathrm{C}}$, and Comp ${}_{\mathrm{D}}$ (seen in training) as well as and Comp ${}_{\mathrm{E}}$ (not seen in training), which differ to the order of several cm in where on the temple arm microphones are placed, as well as nose-microphone location. The 4-channel configuration in the contrast experiment in Section 3.4.2 is based on configuration A except that the nose microphone is dropped entirely, leaving only 4 channels.

### 3.3 Model configuration

The model configuration is similar to [^1]. For each beamformer direction, 80-dimensional log-Mel filterbank features are extracted. Input features from all channels (steering directions) are then fed into the Convolutional front-end, which consists of 2 conv2d blocks each with 5 channels, filters of size ${\text{2}}{\times}{\text{5}}$ and a stride setting of ${\text{1}}{\times}{\text{2}}$. Then, six consecutive frames are stacked to form a 320-dimensional vector, reducing the sequence length by 6x. This is followed by 20 Emformer layers [^27], each with 4 attention heads and 2048-dimensional feed-forward layers. The RNN-T’s prediction network contains one 256-dimensional LSTM layer with layer normalization and dropout. Lastly, the encoder and predictor outputs are both projected to 768 dimensions and passed to an additive joiner network, which contains a ReLU followed by linear layer with 9001 output SentencePiece-based units.

Furthermore, for the ”multi-geometry” system trained on multiple geometries, we incorporate array ids encoded as a one-hot embedding that gets concatenated with the output of the convolutional front-end. The array-id is used to switch beamformer parameters. Such system can distinguish multiple devices used during training, but does not support previously unseen devices. On the other hand, the ”Geometry-agnostic” variant is trained on the same multiple geometries but without array ids, remaining adaptable for handling previously unseen devices. We want to clarify that ”agnostic” is in terms of the ASR model, not the beamformers which are still created for the actual target device, seen in training or not.

Lastly, all models are trained for 8 epochs, with an Adam ${}_{\mathrm{sam}}$ optimizer, a tri-stage learning-rate scheduler with a base learning rate of 0.0005, and a warmup of 10,000 batches.

<table><thead><tr><th rowspan="2">Model Type</th><th rowspan="2">Data</th><th rowspan="2">Test Device</th><th colspan="3">WER%</th></tr><tr><th>u/a</th><th>self</th><th>other</th></tr></thead><tbody><tr><td>Matching geometry</td><td>100%</td><td>Aria <math><semantics><msub><mi>A</mi></msub> <apply><ci>A</ci></apply> <annotation>{}_{\mathrm{A}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_A end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>22.9</td><td>13.3</td><td>26.1</td></tr><tr><td>Mismatching geometry</td><td>100%</td><td>Aria <math><semantics><msub><mi>B</mi></msub> <apply><ci>B</ci></apply> <annotation>{}_{\mathrm{B}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_B end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>23.0</td><td>16.4</td><td>27.7</td></tr><tr><td>Multi-geometry</td><td>5 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> 20%</td><td>Aria <math><semantics><msub><mi>A</mi></msub> <apply><ci>A</ci></apply> <annotation>{}_{\mathrm{A}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_A end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>20.1</td><td>10.0</td><td>21.8</td></tr><tr><td>Geometry-agnostic</td><td>5 <math><semantics><mo>×</mo> <annotation>\times</annotation> <annotation>×</annotation></semantics></math> 20%</td><td>Aria <math><semantics><msub><mi>A</mi></msub> <apply><ci>A</ci></apply> <annotation>{}_{\mathrm{A}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_A end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>20.4</td><td>10.1</td><td>22.2</td></tr></tbody></table>

Table 2: Word error rates on the real test dataset.

<table><tbody><tr><td rowspan="2">Test Device</td><td>Seen/</td><td rowspan="2">Data Type</td><td colspan="3">WER%</td></tr><tr><td>Unseen</td><td>u/a</td><td>self</td><td>other</td></tr><tr><td>Aria <math><semantics><msub><mi>A</mi></msub> <apply><ci>A</ci></apply> <annotation>{}_{\mathrm{A}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_A end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>seen</td><td>real</td><td>20.4</td><td>10.1</td><td>22.2</td></tr><tr><td>Aria <math><semantics><msub><mi>B</mi></msub> <apply><ci>B</ci></apply> <annotation>{}_{\mathrm{B}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_B end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>unseen</td><td>real</td><td>20.7</td><td>10.1</td><td>22.8</td></tr><tr><td>Comp <math><semantics><msub><mi>B</mi></msub> <apply><ci>B</ci></apply> <annotation>{}_{\mathrm{B}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_B end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>seen</td><td>simulated</td><td>15.6</td><td>8.5</td><td>21.6</td></tr><tr><td>Comp <math><semantics><msub><mi>D</mi></msub> <apply><ci>D</ci></apply> <annotation>{}_{\mathrm{D}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_D end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>seen</td><td>simulated</td><td>15.7</td><td>8.4</td><td>21.6</td></tr><tr><td>Comp <math><semantics><msub><mi>E</mi></msub> <apply><ci>E</ci></apply> <annotation>{}_{\mathrm{E}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_E end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>unseen</td><td>simulated</td><td>15.9</td><td>8.5</td><td>22.0</td></tr><tr><td>Comp <math><semantics><msub><mi>A</mi></msub> <apply><ci>A</ci></apply> <annotation>{}_{\mathrm{A}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_A end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>seen</td><td>simulated</td><td>16.7</td><td>8.8</td><td>22.9</td></tr><tr><td>Comp <math><semantics><msub><mrow><mi>A</mi><mo>,</mo><mrow><mn>4</mn> <mo>⁢</mo> <mi>m</mi> <mo>⁢</mo> <mi>i</mi> <mo>⁢</mo> <mi>c</mi></mrow></mrow></msub> <apply><list><ci>A</ci> <apply><cn>4</cn> <ci>m</ci> <ci>i</ci> <ci>c</ci></apply></list></apply> <annotation>{}_{\mathrm{A,4mic}}</annotation> <annotation>start_FLOATSUBSCRIPT roman_A, 4 roman_m roman_i roman_c end_FLOATSUBSCRIPT</annotation></semantics></math></td><td>unseen</td><td>simulated</td><td>26.0</td><td>27.9</td><td>32.6</td></tr></tbody></table>

Table 3: Performance in terms of WER on seen vs. unseen devices, for the ”Geometry-agnostic” model which did not include ”Unseen” device geometries in the training. Noise and bystanders are added for the simulated test sets and overlap ratio is 0%.

### 3.4 Results

All results show two types of WER: speaker-unattributed (denoted ”u/a”) and speaker-attributed (denoted ”self” and ”other”). ”u/a” scores the sequence of words, irrespective of which speaker they were attributed to, while ”self” and ”other” score only words attributed to the respective speaker in ASR output and reference. The ”u/a” metric is not the average of ”self” and ”other”—a word attributed to the wrong speaker counts as an insertion for one speaker and a deletion for the other.

#### 3.4.1 Training on multiple geometries, test devices seen in training

Table 1 shows results on simulated test data, which we can create for all relevant combinations. First, we see that training on multiple geometries at once (”Multi-geometry” and ”Geometry-agnostic”) not only works (the original purpose of this work), but outperforms training on matched geometries only, by as much as 28% relative (e.g. from 8.3% to 6.0% for the clean Comp ${}_{\mathrm{B}}$ /”Geometry-agnostic”). We speculate that the incorporation of more devices/geometries in the data simulation contributes to the robustness, e.g. discouraging the model from over-indexing to fine structure in the beam patterns.

Secondly, compared to ”Multi-geometry,” the exclusion of array-id information, with the goal of being ”Geometry-agnostic” model, led to only a slight WER increases bounded by roughly 0.5% absolute with few exceptions. This is consistent across three different settings, e.g. with and without bystanders.

Similar results are shown in Table 2, but for real data instead. The method generalizes well to real data, achieving a 2.5% absolute gain by going from matching geometry to ”Geometry-agnostic.”

#### 3.4.2 Geometry-agnostic model with unseen devices

How about unseen geometries? In Table 1, shows under ”Mismatched geometry” a drastic accuracy hit for models trained on one geometry but naively tested on another, with WERs of almost 40%.

This is, however, not so if we train on multiple geometries. Table 3 shows WERs for the ”Geometry-agnostic” model when tested with devices not seen vs. seen in training. In the first two sections (Aria ${}_{\mathrm{A}}$ (seen) vs. Aria ${}_{\mathrm{B}}$ (unseen) real data; Comp ${}_{\mathrm{B}}$ /Comp ${}_{\mathrm{D}}$ (seen) vs. Comp ${}_{\mathrm{E}}$ (unseen) simulated data), WERs deviate by no more than 0.6% absolute. (Both Aria ${}_{\mathrm{A}}$ vs. Aria ${}_{\mathrm{B}}$ and Comp ${}_{\mathrm{B}}$ vs. Comp ${}_{\mathrm{E}}$ differ only in the nose microphone, while Comp ${}_{\mathrm{D}}$ and Comp ${}_{\mathrm{E}}$ differ in three microphones, but note that moving even one microphone changes all beamformer weights.)

In this condition, the model is indeed geometry-agnostic. Although not yet tested for explicitly, this also gives some confidence that the Geometry-agnostic system will robustly accommodate variations in head sizes/shapes, hair, headwear, etc.

We also tested a more extreme case, simulating the situation where system designers decide to drop the nose microphone altogether, denoted by ”Comp ${}_{\mathrm{A}}$ (4-mic)”. Here, the method reaches its limits: This significant deviation from the 5-channel geometries used during training causes a noticeable drop in performance, pushing all WERs above 25%. The goal of agnosticity is not achieved here. Maybe one should not expect this to work in the first place, as there is nothing in beamformer objective to explicitly encourage beamformers across geometries to be similar. Investigating such a constraint is future work.

## 4 Conclusion

This paper addresses an important practical problem of microphone arrays being a ”moving target” during system development. We propose a first step towards Array-Geometry Agnostic Directional Speech Recognition (AGADIR): As long as geometry variations are moving around microphones by a few mm to cm and do not change the fundamental nature of the array, we find that training the directional ASR model with multiple geometries not only works but also generalizes to new unseen variations, indeed exhibiting the desired geometry-agnostic behavior in this case. Furthermore, it improves the baseline WER by on the order of 20% relative (up to 28%). However, more work is needed to achieve agnosticity to more extreme geometry variations such as dropping a microphone altogether, possibly via an additional constraint to explicitly keep beamformers consistent across geometries. In addition, the paper introduces an innovative beamformer design tailored for directional speech recognition, demonstrating superiority over conventional methods.

[^1]: Ju Lin, Niko Moritz, Ruiming Xie, Kaustubh Kalgaonkar, Christian Fuegen, and Frank Seide, “Directional speech recognition for speaker disambiguation and cross-talk suppression,” Proc. INTERSPEECH 2023, pp. 3522–3526, 2023.

[^2]: Hassan Taherian, Sefik Emre Eskimez, Takuya Yoshioka, Huaming Wang, Zhuo Chen, and Xuedong Huang, “One model to enhance them all: array geometry agnostic multi-channel personalized speech enhancement,” in ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2022, pp. 271–275.

[^3]: Takuya Yoshioka, Xiaofei Wang, Dongmei Wang, Min Tang, Zirun Zhu, Zhuo Chen, and Naoyuki Kanda, “Vararray: Array-geometry-agnostic continuous speech separation,” in ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2022, pp. 6027–6031.

[^4]: Naoyuki Kanda, Jian Wu, Xiaofei Wang, Zhuo Chen, Jinyu Li, and Takuya Yoshioka, “Vararray meets t-sot: Advancing the state of the art of streaming distant conversational speech recognition,” in ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2023, pp. 1–5.

[^5]: Xuankai Chang, Wangyou Zhang, Yanmin Qian, Jonathan Le Roux, and Shinji Watanabe, “MIMO-speech: End-to-end multi-channel multi-speaker speech recognition,” in 2019 IEEE Automatic Speech Recognition and Understanding Workshop (ASRU). IEEE, 2019, pp. 237–244.

[^6]: Zhong-Qiu Wang, Jonathan Le Roux, and John R Hershey, “Multi-channel deep clustering: Discriminative spectral and spatial embeddings for speaker-independent speech separation,” in 2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2018, pp. 1–5.

[^7]: Yiwen Shao, Shi-Xiong Zhang, and Dong Yu, “Multi-channel multi-speaker ASR using 3D spatial feature,” in ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2022, pp. 6067–6071.

[^8]: Zhuo Chen, Xiong Xiao, Takuya Yoshioka, Hakan Erdogan, Jinyu Li, and Yifan Gong, “Multi-channel overlapped speech recognition with location guided speech extraction network,” in 2018 IEEE Spoken Language Technology Workshop (SLT). IEEE, 2018, pp. 558–565.

[^9]: Tara N Sainath, Ron J Weiss, Kevin W Wilson, Arun Narayanan, and Michiel Bacchiani, “Factored spatial and spectral multichannel raw waveform cldnns,” in 2016 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2016, pp. 5075–5079.

[^10]: Weipeng He, Lu Lu, Biqiao Zhang, Jay Mahadeokar, Kaustubh Kalgaonkar, and Christian Fuegen, “Spatial attention for far-field speech recognition with deep beamforming neural networks,” in ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2020, pp. 7499–7503.

[^11]: Jack Capon, “High-resolution frequency-wavenumber spectrum analysis,” Proceedings of the IEEE, vol. 57, no. 8, pp. 1408–1418, 1969.

[^12]: Gary W Elko, SL Gay, and J Benesty, “Superdirectional microphone arrays,” Kluwer International Series in Engineering and Computer Science, pp. 181–238, 2000.

[^13]: Gongping Huang, Jacob Benesty, and Jingdong Chen, “Superdirective beamforming based on the krylov matrix,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 24, no. 12, pp. 2531–2543, 2016.

[^14]: Simon Doclo and Marc Moonen, “Superdirective beamforming robust against microphone mismatch,” IEEE Transactions on Audio, Speech, and Language Processing, vol. 15, no. 2, pp. 617–631, 2007.

[^15]: Sergey Ioffe and Christian Szegedy, “Batch normalization: Accelerating deep network training by reducing internal covariate shift,” in International conference on machine learning. PMLR, 2015, pp. 448–456.

[^16]: Yann N Dauphin, Angela Fan, Michael Auli, and David Grangier, “Language modeling with gated convolutional networks,” in International conference on machine learning. PMLR, 2017, pp. 933–941.

[^17]: Jay Mahadeokar, Yuan Shangguan, Duc Le, Gil Keren, Hang Su, Thong Le, Ching-Feng Yeh, Christian Fuegen, and Michael L Seltzer, “Alignment restricted streaming recurrent neural network transducer,” in 2021 IEEE Spoken Language Technology Workshop (SLT). IEEE, 2021, pp. 52–59.

[^18]: Niko Moritz, Frank Seide, Duc Le, Jay Mahadeokar, and Christian Fuegen, “An investigation of monotonic transducers for large-scale automatic speech recognition,” arXiv preprint arXiv:2204.08858, 2022.

[^19]: Tara N Sainath, Yanzhang He, Bo Li, Arun Narayanan, Ruoming Pang, Antoine Bruguier, Shuo-yiin Chang, Wei Li, Raziel Alvarez, Zhifeng Chen, et al., “A streaming on-device end-to-end model surpassing server-side conventional model quality and latency,” in ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2020, pp. 6059–6063.

[^20]: Jinyu Li, Rui Zhao, Zhong Meng, Yanqing Liu, Wenning Wei, Sarangarajan Parthasarathy, Vadim Mazalov, Zhenghao Wang, Lei He, Sheng Zhao, et al., “Developing rnn-t models surpassing high-performance hybrid models with customization capability,” arXiv preprint arXiv:2007.15188, 2020.

[^21]: Naoyuki Kanda, Jian Wu, Yu Wu, Xiong Xiao, Zhong Meng, Xiaofei Wang, Yashesh Gaur, Zhuo Chen, Jinyu Li, and Takuya Yoshioka, “Streaming multi-talker ASR with token-level serialized output training,” arXiv preprint arXiv:2202.00842, 2022.

[^22]: Xuankai Chang, Niko Moritz, Takaaki Hori, Shinji Watanabe, and Jonathan Le Roux, “Extended graph temporal classification for multi-speaker end-to-end ASR,” in 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2022, pp. 7322–7326.

[^23]: Eric A Lehmann and Anders M Johansson, “Prediction of energy decay in room impulse responses simulated with an image-source model,” The Journal of the Acoustical Society of America, vol. 124, no. 1, pp. 269–277, 2008.

[^24]: Robin Scheibler, Eric Bezzam, and Ivan Dokmanić, “Pyroomacoustics: A python package for audio room simulation and array processing algorithms,” in 2018 IEEE international conference on acoustics, speech and signal processing (ICASSP). IEEE, 2018, pp. 351–355.

[^25]: Chandan KA Reddy, Vishak Gopal, Ross Cutler, Ebrahim Beyrami, Roger Cheng, Harishchandra Dubey, Sergiy Matusevych, Robert Aichner, Ashkan Aazami, Sebastian Braun, et al., “The interspeech 2020 deep noise suppression challenge: Datasets, subjective testing framework, and challenge results,” in INTERSPEECH, 2020.

[^26]: Kiran Somasundaram, Jing Dong, Huixuan Tang, Julian Straub, Mingfei Yan, Michael Goesele, et al., “Project aria: A new tool for egocentric multi-modal ai research,” arXiv preprint arXiv:2308.13561, 2023.

[^27]: Yangyang Shi, Yongqiang Wang, Chunyang Wu, Ching-Feng Yeh, Julian Chan, Frank Zhang, Duc Le, and Mike Seltzer, “Emformer: Efficient memory transformer based acoustic model for low latency streaming speech recognition,” in ICASSP 2021-2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2021, pp. 6783–6787.