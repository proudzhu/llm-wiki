# IMPROVING PERFORMANCE OF REAL-TIME FULL-BAND BLIND PACKET-LOSS CONCEALMENT WITH PREDICTIVE NETWORK

Viet-Anh Nguyen<sup>1</sup>, Anh H. T. Nguyen<sup>1</sup>, and Andy W. H. Khong<sup>2</sup>

<sup>1</sup>Crystalsound Team, NamiTech JSC, Ho Chi Minh City, Vietnam

<sup>2</sup>Nanyang Technological University, Singapore

{vietanh.nguyen, anh.nguyen}@namitech.io, andykhong@ntu.edu.sg

## ABSTRACT

Packet loss concealment (PLC) is a tool for enhancing speech degradation caused by poor network conditions or underflow/overflow in audio processing pipelines. We propose a real-time recurrent method that leverages previous outputs to mitigate artefact of lost packets without the prior knowledge of loss mask. The proposed full-band recurrent network (FRN) model operates at 48 kHz, which is suitable for high-quality telecommunication applications. Experiment results highlight the superiority of FRN over an offline non-causal baseline and a top performer in a recent PLC challenge.

Index Terms— Blind packet loss concealment, real-time, speech enhancement, VoIP

## 1. INTRODUCTION

The advent of technology for remote communication devices coupled with the recent pandemic has resulted in the rise in demand for voice over Internet Protocol (VoIP) in many communication systems. Besides the need to deal with network echoes [1, 2, 3], packet loss may occur leading to artefacts and distortion at the receiver end. Packet loss concealment (PLC) aims to mitigate these effects by filling in the gaps due to lost packets.

There are two types of PLC algorithms—informed and blind PLC [4]. The former requires prior information pertaining to which audio packets have been lost during transmission. In this regard, conventional methods employ linear or statistical models to conceal unavailable audio packets [5, 6]. Deep learning methods, on the other hand, can conceal faulty chunks from its representation in the time- [7] or time-frequency domain [8, 4] without the need of feature engineering. In the recent PLC challenge [9], deep neural networks such as [10, 11, 12] have been successfully adopted for informed PLC, achieving promising results.

As opposed to the informed approach, blind PLC, or audio in-painting, improves lossy signals without the need of loss traces and is suitable when packet metadata may not be readily available. In addition, these algorithms do not require the alignment of audio input with its packet stream resulting in their ability to handle arbitrary packet sizes. An end-toend speech inpainting network has been proposed to recover losses in both time and frequency axes of the spectrogram representation [4]. Generative adversarial networks (GANs) have also shown promising results for this task [13]. It is useful to note that most of existing PLC methods operate at 16 kHz sampling rate, which presents a limitation for fullband 48 kHz transmission. Furthermore, in-painting models [4, 13] are non-causal, rendering them unsuitable for realtime communication.

We propose a full-band recurrent network (FRN) for blind PLC of 48 kHz speech signals. The proposed FRN algorithm is frame-causal due to the use of short-time Fourier transform (STFT) and does not require any additional information (e.g., loss mask or packet size) of the packet stream. As opposed to conventional networks [4, 7, 14], and inspired by the recurrent neural network (RNN)-transducer model [15] in speech recognition, our proposed FRN model includes a log Melscale predictor to address practical challenges posed by high sample-rate, unavailable packet-loss metadata, and causal frame-wise inference. The predictor employs the previous output to improve prediction of the current output, which is essential to achieve better concealment when several consecutive packets are lost. It is worth noting that the employment of previous output in speech enhancement algorithms has a long history, e.g., in the celebrated decision-directed SNR estimator [16]. Experiment results demonstrate that FRN outperforms an informed PLC model and an offline GAN-based model despite being a blind frame-causal algorithm.

## 2. THE PROPOSED FULL-BAND RECURRENT NETWORK (FRN)

We assume that the content of each input chunk may be partially or completely lost in the time domain and that information pertaining to which part of the input signal has been lost is unavailable. To conceal such audio loss in online manner, we propose a time-frequency model consisting of an encoder Enc and a predictor Pred as shown in Fig. 1(a). Input signal x is represented via T frames and F frequency components by employing STFT, resulting a complex timefrequency (TF) representation $\langle \Re ^ { F \times T } , \Im ^ { F \times T } \rangle ^ { \intercal } \ = \ \mathrm { S T F T } ( x )$ At a time step i, the encoder reconstructs audio loss in the current input $\left. \Re _ { i } ^ { F } , \Im _ { i } ^ { F } \right. ^ { \intercal }$ while the pretrained predictor leverages previous output $\big \langle \hat { \mathfrak { R } } _ { i - 1 } ^ { F } , \hat { \mathfrak { I } } _ { i - 1 } ^ { F } \big \rangle ^ { \intercal }$ and exploits predictable patterns in speech signals to yield further improvement. Finally, the enhanced TF frame $\left. \hat { \Re } _ { i } ^ { F } , \hat { \Im } _ { i } ^ { F } \right. ^ { \intercal }$ is generated via a joiner that combines the encoder output and the predictor output.

![](figures/28394cbbe95b1aca151172b0515a48aae673a826bf257504e81dc23a74a0a9ee.jpg)  
(a)

![](figures/ce5c90aa89458221c3e3f3f06dd78e9156ee9e38f1f945d39791afcb0adc5377.jpg)  
(b)

![](figures/660761a5b19c06ccb187eb835512f4d90e33b6a44b689706287fddffadefcde1.jpg)  
(c)

![](figures/9aece7cf70ebfc3d9e72b6a659851dd78941617c9a31416dc49ec8682eb8a4dd.jpg)  
(d)  
Fig. 1: Full-band recurrent network (FRN) (a) that processes time-frequency frames sequentially. The architecture consists of an encoder (b) that enhances the current input, a predictor (c) that infers output from the previous step, and a joiner (d) that combines outputs of the two modules.

The detailed architecture of our encoder is illustrated in Fig. 1(b). In essence, the proposed encoder models interframe information via an RNN for causality and models intraframe information via a multi-layer perceptron (MLP) with fusible affine normalization layers. Such a network arrangement can be seen as an efficient hybrid between ResMLP [17] and dual path RNN [18]. The complex-value STFT of the input is first flattened into $\Re \Im ^ { 2 F \times T } = \langle \Re ^ { F \times T } , \Im ^ { F \times T } \rangle$ and projected from the dimension 2F (real and imaginary) to a lower dimension dim for computational efficiency. This projection is achieved via a linear layer followed by a Gaussian error linear unit (GELU) resulting in feature

$$
x ^ {d i m \times T} = \operatorname{GELU} (W _ {1} ^ {d i m \times 2 F} \cdot \mathfrak {R I} ^ {2 F \times T} + b _ {1}),\tag{1}
$$

where $W _ { 1 } ^ { d i m \times 2 F }$ and $b _ { 1 }$ are weights and bias of the linear layer, respectively. The subsequent residual module Res consists of N blocks with each block comprising an RNN layer that models the inter-frame correlation and linear layers that model intra-frame features. Features of the residual module Res is then projected back to dimension of 2F giving the encoder output

$$
\left\langle \mathfrak {R} ^ {F \times T}, \mathfrak {J} ^ {F \times T} \right\rangle = W _ {2} ^ {2 F \times d i m} \cdot \operatorname{Res} (x ^ {d i m \times T}) + b _ {2},\tag{2}
$$

where $W _ { 2 } ^ { 2 F \times d i m }$ and $b _ { 2 }$ are weights and bias of the projection layer, respectively.

The architecture of the predictor Pred is shown in Fig. 1(c). It predicts the magnitude $\mathring { A } _ { i } ^ { F }$ of the current frame i from that of the previous complex output frame via

$$
A _ {i - 1} ^ {F} = \sqrt {(\mathfrak {R} _ {i - 1} ^ {F}) ^ {2} + (\mathfrak {I} _ {i - 1} ^ {F}) ^ {2}},\tag{3}
$$

$$
\acute {A} _ {i} ^ {F} = \mathrm{Pred} (A _ {i - 1} ^ {F}).\tag{4}
$$

Since significant amount of speech energy is concentrated in the lower frequency-bin indices, the predictor is simplified and made efficient by applying a long short-term memory (LSTM) on the log Mel-scale magnitude input. Here, the LSTM models the temporal dynamics of the signal and a subsequent linear layer projects the LSTM output back to the Mel-scale dimension. Finally, a learnable inverse Mel layer consisting of an exponential function, a linear layer, and an absolute activation transforms the Mel magnitude into STFT magnitude of F dimension. To ensure stability during training and to ensure the prediction from the previous input frame, the predictor is pre-trained on the target audios of the training PLC dataset before being jointly trained with the encoder network. This pre-training step allows the model to achieve modest improvement in performance.

To combine magnitude feature from the predictive branch with the complex feature from the encoder, we employ a joiner based on the convolutional neural network (CNN). Since the two features have the same shape $F \times T$ but differ in the number of channels, CNNs serve as an effective tool for feature fusion. Features are stacked along its channel axis, forming a 3-channel input x including $\mathring { \Re } _ { i } ^ { F } , \mathring { \Im } _ { i } ^ { F }$ , and $\not A _ { i } ^ { F }$ which denote, respectively, the real, imaginary parts of the encoder output, and the magnitude output of the predictor.

Two causal grouped convolution layers are used to transform the three channels into two channels representing the real $\Re _ { i } ^ { F }$ and imaginary $\hat { \Im } _ { i } ^ { F }$ of the final output before being transformed into waveform $\hat { y }$ by inverse STFT (iSTFT), i.e,

$$
\langle \hat {\mathfrak {R}} _ {i} ^ {F}, \hat {\mathfrak {I}} _ {i} ^ {F} \rangle^ {\intercal} = \operatorname{Joiner} \bigl (\langle \acute {\mathfrak {R}} _ {i} ^ {F}, \acute {\mathfrak {I}} _ {i} ^ {F}, \acute {A} _ {i} ^ {F} \rangle^ {\intercal} \bigr),\tag{5}
$$

$$
\hat {y} = \mathrm{iSTFT} (\langle \hat {\mathfrak {R}} _ {i} ^ {F}, \hat {\mathfrak {I}} _ {i} ^ {F} \rangle^ {\intercal}).\tag{6}
$$

## 2.1. Learning objective

We employ multi-resolution STFT loss [19] as the learning objective. Given a signal s, its compressed STFT magnitude $\mathcal C ( s )$ is defined as

$$
\mathcal {C} (s) = | \mathrm{STFT} (s) | ^ {\alpha},\tag{7}
$$

where $| \operatorname { S T F T } ( s ) |$ denotes the STFT magnitude of $s ,$ and α is a compression rate that equalizes energy across frequency bands [20]. The multi-resolution STFT loss $\ell _ { \mathrm { M R } }$ between the generated signal $\hat { y }$ and its corresponding target signal $y$ over M resolutions is then given by

$$
\ell_ {\mathrm{MR}} (\hat {y}, y) = \frac {1}{M} \sum_ {m = 1} ^ {M} \left(\frac {\| \mathcal {C} (y) - \mathcal {C} (\hat {y}) \| _ {\mathrm{F}}}{\| \mathcal {C} (y) \| _ {\mathrm{F}}} + \frac {1}{N} \| \mathcal {C} (y) - \mathcal {C} (\hat {y}) \| _ {1}\right),\tag{8}
$$

where the first term within the brackets corresponds to spectral convergence while the second term is for spectral magnitude loss, $\left\| . \right\| _ { F } , \left\| . \right\| _ { 1 }$ , and N are the Frobenius norm, L1 norm, and total number of frequency bins, respectively.

## 2.2. Packet loss generation

To simulate realistic packet loss sequences, a two-state Markov chain algorithm consisting of ‘loss’ (L), ‘non-loss’ (N), and transition probabilities are used to control the behaviour of the output sequence [7]. Defining $p _ { N }$ and $p _ { L }$ as the intra-state transition probabilities of state N and $L ,$ respectively, a two-state Markov chain can be defined as a $( p _ { N } , p _ { L } )$ pair. We can modify these probabilities to achieve different expected loss rates of the packet sequences.

## 3. EXPERIMENT SETUP AND RESULTS

## 3.1. Setup

The dataset was generated from the VCTK Corpus [21] by selecting three-second segments randomly from each audio file to create the target signal. The lossy input signal was created by splitting the target signal into packets with size chosen arbitrarily from the set {256, 512, 768, 1024, 1536}. A loss mask generated from the procedure in Section 2.2 is then applied on the packetized signal. The dataset consists of 109 English speakers from which audio clips of the first 100 speakers are for training and the remainder for testing. Loss masks were generated, for each audio output, using one of the four Markov chains in Table 1. Besides, we also use loss masks provided in the PLC challenge [9] for realistic evaluation. These loss traces are collected from real calls and reflects the behaviour of lost packets in the real-world.

<table><tr><td> $p_N$ </td><td> $p_L$ </td><td>Expected loss</td></tr><tr><td>0.9</td><td>0.1</td><td>10%</td></tr><tr><td>0.9</td><td>0.5</td><td>16.7%</td></tr><tr><td>0.5</td><td>0.1</td><td>35.7%</td></tr><tr><td>0.5</td><td>0.5</td><td>50%</td></tr></table>

Table 1: Transition probabilities of Markov chain models

To evaluate performance, we used four metrics: PLCMOS [9], log-spectral distance (LSD), short-time objective intelligibility (STOI), and perceptual evaluation of speech quality (PESQ). While STOI, PLCMOS, and PESQ only evaluate frequency bands of up to 5 kHz, 8 kHz, and 8 kHz, respectively, LSD evaluates the entire 24 kHz frequency band of the full-band speech. PLCMOS is the average score of two independent deep learning models that predict intrusive and nonintrusive mean-opinion-score (MOS) of human raters specifically for PLC task. LSD, STOI, and PESQ, on the other hand, rely on feature engineering to capture characteristics of speech signals associated with auditory quality. Higher PLCMOS, STOI, and PESQ scores imply better quality while a lower LSD score is more ideal.

We applied 960-point STFT with window size of 20 ms and 50% overlapping on the audio waveform, resulting in the dimension of $F = 4 8 0$ for each STFT frame. While lookahead was not applied to reduce overall algorithmic latency, it can be used if performance is prioritized. For the encoder, the projection dimension dim and RNN state dimension are equivalent to 384 while the hidden dimension of the subsequent linear layers and the number of layers are $N = 7 6 8$ and $^ { 4 , }$ respectively. For the predictor, we used 64-bin Mel filter banks, and the LSTM consists of a single layer with a hidden size of 512. The hyperparameters of convolution layers in the joiner, including output channel $c ,$ kernel size $k ,$ and number of group g, are shown in Fig. 1(d). The STFT paramaters for the resolutions in our loss function is set to default values of the auraloss library [22], and the compression ratio is set to $\alpha = 0 . 3$ . For the PLC training as well as predictor pretraining, we trained the models for 150 epochs with 90 in samples each data batch. Weights of the models are optimized by the Adam optimizer with $\mathrm { \bar { 1 } \times 1 0 ^ { - 4 } }$ learning rate.

## 3.2. Results

For comparison, we implemented two baselines:

• tPLCnet [12]: a real-time informed PLC method that was ranked third in the recent PLC challenge. We employed the ‘Large’ model, which is the largest version proposed by the authors.

<table><tr><td rowspan="2">Model</td><td colspan="4">PLCMOS</td><td colspan="4">LSD</td><td colspan="4">STOI</td><td colspan="4">PESQ</td></tr><tr><td>10%</td><td>20%</td><td>40%</td><td>Real trace</td><td>10%</td><td>20%</td><td>40%</td><td>Real trace</td><td>10%</td><td>20%</td><td>40%</td><td>Real trace</td><td>10%</td><td>20%</td><td>40%</td><td>Real trace</td></tr><tr><td>Input (zero fill)</td><td>3.505</td><td>2.754</td><td>1.931</td><td>3.517</td><td>1.156</td><td>1.811</td><td>3.267</td><td>1.984</td><td>0.842</td><td>0.748</td><td>0.592</td><td>0.797</td><td>1.931</td><td>1.393</td><td>1.126</td><td>2.484</td></tr><tr><td>tPLC</td><td>3.417</td><td>2.863</td><td>2.417</td><td>3.463</td><td>1.201</td><td>1.611</td><td>2.073</td><td>1.216</td><td>0.831</td><td>0.776</td><td>0.704</td><td>0.838</td><td>1.981</td><td>1.629</td><td>1.386</td><td>2.532</td></tr><tr><td>TFGAN</td><td>3.902</td><td>3.675</td><td>3.019</td><td>3.645</td><td>2.081</td><td>3.181</td><td>3.714</td><td>2.314</td><td>0.823</td><td>0.751</td><td>0.641</td><td>0.760</td><td>1.716</td><td>1.321</td><td>1.116</td><td>1.339</td></tr><tr><td>FRN (proposed)</td><td>4.032</td><td>3.573</td><td>2.623</td><td>3.655</td><td>0.783</td><td>1.117</td><td>1.682</td><td>0.946</td><td>0.920</td><td>0.862</td><td>0.746</td><td>0.889</td><td>2.336</td><td>1.799</td><td>1.422</td><td>2.797</td></tr></table>

Table 2: Score comparison with baselines. The ‘10%’, ‘20%’, and ‘40%’ columns indicate test sets with simulated loss mask while the ‘Real trace’ column indicates test set with loss traces (approx. loss rate of 10.27%) from real calls. LSD lower is better while the other three higher is better.

• TFGAN [13]: an offline blind PLC model based on generative adversarial networks (GANs). Since the model was designed for concealing 16 kHz audios, chunk size and discriminator linear head were increased from 2,560 to 7,680 to better adapt to 48 kHz signals.

The models were evaluated on the VCTK test set with the packet size fixed at 20 ms (i.e., 960 samples). The loss mask was generated by three Markov chains, forming three simulated test sets with expected loss rates being 10%, 20%, and 40%. Another test set is ‘Real trace’, which corresponds to the real loss traces derived from the PLC challenge dataset applied on the VCTK test set.

With reference to Table 2 and compared to the informed tPLCnet method [12], the proposed model achieved significantly higher scores across all benchmarks and loss rates despite the lack of loss trace information. We also note that although the offline GAN-based TFGAN model achieved higher PLCMOS scores, especially at higher loss rates such as 40%, our model outperforms TFGAN by approximately 250%, 12%, and 30% in terms of LSD, STOI, and PESQ measures, respectively. To evaluate the listening quality, we have also provided audio samples along with our source code for comparison<sup>1</sup>.

We evaluated the inference time of the models via a single Intel Core-i9 3.0 GHz CPU thread and the ONNX inference engine. Since TFGAN is a non-causal model, we only evaluated the latency of our model and tPLCnet. As shown in Table 3, although our proposed model suffers from a modest 1.4 ms increase in inference time than tPLCnet, its increase in performance outweighs the higher inference time. In particular, the proposed FRN model requires 4.1 ms to process a 10 ms chunk – 20ms windows with 50% overlapping – achieving a real-time factor of 0.41.

<table><tr><td>Model</td><td>Causal</td><td>Blind</td><td>Model size</td><td>Inference time</td><td>Real-time factor</td></tr><tr><td>tPLCnet</td><td>√</td><td></td><td>5.7M</td><td>2.7 ms</td><td>0.27</td></tr><tr><td>TFGAN (generator)</td><td></td><td>√</td><td>1.9M</td><td>N/A</td><td>N/A</td></tr><tr><td>FRN (proposed)</td><td>√</td><td>√</td><td>9.1M</td><td>4.1 ms</td><td>0.41</td></tr></table>

Table 3: Model size, inference time, and real-time factor of the algorithms. ‘Causal’ column indicates causality of the models, and ‘Blind’ column indicates blind PLC algorithms

<table><tr><td>Model</td><td>PLCMOS</td><td>LSD</td><td>PESQ</td><td>STOI</td></tr><tr><td>Input</td><td>3.517</td><td>1.984</td><td>2.484</td><td>0.797</td></tr><tr><td>Encoder</td><td>3.639</td><td>1.081</td><td>2.687</td><td>0.862</td></tr><tr><td>FRN</td><td>3.655</td><td>0.946</td><td>2.797</td><td>0.889</td></tr></table>

Table 4: Results of a variation from our proposed model on the ‘Real trace’ test set.

To gain insight into the impact of the predictor, we conduct experiments on the ‘Real trace’ test set to compare FRN with the encoder only. With reference to Table 4, although the encoder alone achieved good performance, the predictor and joiner provides additional performance improvement. This result also implies that reusing the previous output is beneficial for this task.

## 4. CONCLUSIONS

We proposed a deep recurrent model for blind packet loss concealment at 48 kHz. Despite the lack of loss trace information and being a frame-causal model, our method outperforms one of the informed models in the PLC challenge. The proposed FRN exhibits performance improvement over an offline model across the evaluation benchmarks by a significant margin.

## 5. REFERENCES

[1] A. W. H. Khong, P. A. Naylor, and J. Benesty, “A low delay and fast converging improved proportionate algorithm for sparse system identification,” J. Audio, Speech, and Music Process., vol. 2007, pp. 1–8, Apr. 2007.

[2] S. Zhang, Z. Wang, Y. Ju, Y. Fu, Y. Na, Q. Fu, and L. Xie, “Personalized acoustic echo cancellation for full-duplex communications,” in Proc. Interspeech, 2022, pp. 2518–2522.

[3] A. W. H. Khong, X. Lin, M. Doroslovacki, and P. A. Naylor, “Frequency domain selective tap adaptive algorithms for sparse system identification,” in Proc. IEEE Int’l Conf. Acoust., Speech, Signal Process. (ICASSP), 2008, pp. 229–232.

[4] M. Kegler, P. Beckmann, and M. Cernak, “Deep speech inpainting of time-frequency masks,” in Proc. Interspeech. Oct 2020, ISCA.

[5] L. Koenig, R. Andre-Obrecht, C. Mailhes, and S. Fabre,´ “A new feature vector for HMM-based packet loss concealment,” in Proc. 17th European Signal Process. Conf., 2009, pp. 2519–2523.

[6] S. Kay and S. Marple, “Spectrum analysis—a modern perspective,” in Proc. IEEE, 1981, vol. 69, pp. 1380– 1419.

[7] J. Lin, Y. Wang, K. Kalgaonkar, G. Keren, D. Zhang, and C. Fuegen, “A time-domain convolutional recurrent network for packet loss concealment,” in Proc. IEEE Int’l Conf. Acoust., Speech, Signal Process. (ICASSP), 2021, pp. 7148–7152.

[8] B.-K. Lee and J.-H. Chang, “Packet loss concealment based on deep neural networks for digital speech transmission,” IEEE/ACM Trans. Audio, Speech, Lang. Process., vol. 24, no. 2, pp. 378–387, Feb. 2016.

[9] L. Diener, S. Sootla, S. Branets, A. Saabas, R. Aichner, and R. Cutler, “INTERSPEECH 2022 Audio deep packet loss concealment challenge,” in Proc. Interspeech 2022, 2022, pp. 580–584.

[10] N. Li, X. Zheng, C. Zhang, L. Guo, and B. Yu, “Endto-end multi-loss training for low delay packet loss concealment,” in Proc. Interspeech 2022, 2022, pp. 585– 589.

[11] J.-M. Valin, A. Mustafa, C. Montgomery, T. B. Terriberry, M. Klingbeil, P. Smaragdis, and A. Krishnaswamy, “Real-time packet loss concealment with mixed generative and predictive model,” in Proc. Interspeech 2022, 2022, pp. 570–574.

[12] N. L. Westhausen and B. T. Meyer, “tPLCnet: Real-time deep packet loss concealment in the time domain using a short temporal context,” in Proc. Interspeech 2022, 2022, pp. 2903–2907.

[13] J. Wang, Y. Guan, C. Zheng, R. Peng, and X. Li, “A temporal-spectral generative adversarial network based end-to-end packet loss concealment for wideband speech transmission,” J. Acoust. Soc. Am., vol. 150, no. 4, pp. 2577–2588, Oct. 2021.

[14] V.-A. Nguyen, A. H. T. Nguyen, and A. W. H. Khong, “TUNet: A block-online bandwidth extension model based on transformers and self-supervised pretraining,” in Proc. IEEE Int’l Conf. Acoust., Speech, Signal Process. (ICASSP), 2022, pp. 161–165.

[15] A. Graves, “Sequence transduction with recurrent neural networks,” arXiv preprint arXiv:1211.3711, 2012.

[16] Y. Ephraim and D. Malah, “Speech enhancement using a minimum-mean square error short-time spectral amplitude estimator,” IEEE Trans. Acoust., Speech, Signal Process., vol. 32, no. 6, pp. 1109–1121, 1984.

[17] H. Touvron, P. Bojanowski, M. Caron, M. Cord, A. El-Nouby, E. Grave, G. Izacard, A. Joulin, G. Synnaeve, J. Verbeek, and H. J’egou, “ResMLP: Feedforward networks for image classification with data-efficient training,” IEEE Trans. Pattern Analy. Machine Intell., 2022.

[18] Y. Luo, Z. Chen, and T. Yoshioka, “Dual-Path RNN: Efficient long sequence modeling for time-domain singlechannel speech separation,” in Proc. IEEE Int’l Conf. Acoust., Speech, Signal Process. (ICASSP), 2020, pp. 46–50.

[19] R. Yamamoto, E. Song, and J.-M. Kim, “Parallel Wave-GAN: A fast waveform generation model based on generative adversarial networks with multi-resolution spectrogram,” in Proc. IEEE Int’l Conf. Acoust., Speech, Signal Process. (ICASSP), 2020.

[20] A. Ephrat, I. Mosseri, O. Lang, T. Dekel, K. Wilson, A. Hassidim, W. T. Freeman, and M. Rubinstein, “Looking to listen at the cocktail party: A speaker-independent audio-visual model for speech separation,” ACM Trans. Graph., vol. 37, no. 4, Jul. 2018.

[21] J. Yamagishi, C. Veaux, and K. MacDonald, “CSTR VCTK Corpus: English multi-speaker corpus for CSTR voice cloning toolkit (version 0.92),” University of Edinburgh. The Centre for Speech Technology Research (CSTR), 2019.

[22] C. J. Steinmetz and J. D. Reiss, “auraloss: Audio focused loss functions in PyTorch,” in Proc. Digit. Music Res. Netw. One-day Workshop (DMRN+15), 2020.