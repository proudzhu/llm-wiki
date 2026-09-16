# Music Source Separation with Band-split RNN

Yi Luo, Jianwei Yu

Abstract—The performance of music source separation (MSS) models has been greatly improved in recent years thanks to the development of novel neural network architectures and training pipelines. However, recent model designs for MSS were mainly motivated by other audio processing tasks or other research fields, while the intrinsic characteristics and patterns of the music signals were not fully discovered. In this paper, we propose bandsplit RNN (BSRNN), a frequency-domain model that explictly splits the spectrogram of the mixture into subbands and perform interleaved band-level and sequence-level modeling. The choices of the bandwidths of the subbands can be determined by a priori knowledge or expert knowledge on the characteristics of the target source in order to optimize the performance on a certain type of target musical instrument. To better make use of unlabeled data, we also describe a semi-supervised model finetuning pipeline that can further improve the performance of the model. Experiment results show that BSRNN trained only on MUSDB18-HQ dataset significantly outperforms several top-ranking models in Music Demixing (MDX) Challenge 2021, and the semi-supervised finetuning stage further improves the performance on all four instrument tracks.

Keywords—Music separation, Neural network, Deep learning

## I. INTRODUCTION

The task of music source separation (MSS) has drawn more and more attention in the community due to its wide application in music remixing [1]–[3], music information retrieval (MIR) [4]–[8], and music education [9], [10]. The advances in MSS models can also shed light on the investigation of novel model designs for other related tasks such as speech enhancement and speech separation [11]–[15]. Moreover, since music signals are typically recorded at a higher sample rate than signals in telecommunication systems (e.g., 44.1k Hz) and have been artificially edited or manipulated by professionals, MSS is in general more challenging than narrow-band or wideband speech enhancement and separation tasks. Developing high-quality MSS models is thus important and necessary towards building a robust universal source separation system in diverse and complicated real-world scenarios.

Modern MSS models are generally built upon deeper and more complicated neural network architectures. While frequency-domain systems are the mainstream [16]–[26], recent works have also focused on time-domain systems [27]– [30] as well as the fusion of time-domain and frequencydomain systems [31], [32]. However, many of the MSS models were motivated by existing system architectures in other research fields. For example, models in speech separation can be directly applied to MSS without modifications [18], [30], [33]–[36], and architectures in image segmentation [37], human pose estimation [38] and image recognition [39] have been directly utilized in various recent MSS models. Although many of those prior arts have proven effective in terms of the separation performance, the question of why they are effective in music data and how they can be modified to better explore the intrinsic characteristics of music signals is not easy to answer. Moreover, since existing works in speech enhancement and separation typically only considers narrow-band and wide-band signals, how to adjust them to super wide-band music signals is also worth investigating. The characteristics of singing voice and speech can also be different in terms of fundamental frequency, loudness and formants [40], and speech separation models may have the potential to be further improved on singing voice if such properties could be considered in the modification of the models.

In this paper, we propose band-split RNN (BSRNN), a frequency-domain MSS model that is specially designed for high sample rate signals with flexible and explicit segregation and modeling of different frequency bands. BSRNN splits a spectrogram into a series of subband spectrograms with a set of predefined bandwidths, and the bandwidths are adjusted for different instrument types accordingly. The subband spectrograms are then transformed to generate a series of features with a same feature dimension, and stacked residual recurrent neural network (RNN) layers are utilized to perform interleaved cross-band and cross-sequence modeling similar to dual-path networks for speech separation [41]. Each subband feature in the output of the last residual RNN layer is then transformed by a multilayer perceptron (MLP) to generate its corresponding complex-valued time-frequency mask, and the mask is applied to the corresponding subband mixture spectrogram to generate the estimated target source spectrogram. All estimated subband spectrograms are then concatenated to form the full spectrogram of the target source. The most important module in BSRNN is the band-splitting module, which enable us to incorporate prior knowledge on the target source into the model design. For example, if we know in advance that the target source mainly lies in lower frequency parts with a relatively low fundamental frequency, we can perform fine-grained bandsplitting scheme at lower frequency parts to increase the frequency resolution and coarse-grained band-splitting scheme at higher frequency parts to save the computational complexity. We show by experiments that band-splitting schemes do play an important role in the separation performance, and different musical instruments do have their own band-splitting scheme to obtain a performance gain. By properly selecting the bandsplitting bandwidths, BSRNN trained only on MUSDB18-HQ dataset [42] is able to significantly outperform top-ranking models in Music Demixing (MDX) Challenge 2021.

It is well-known that the performance and generalization ability of many MSS models can be limited by the size of available high-quality clean training data. Several existing works have proposed methods for digging valid segments from unlabeled data by a source activity detector and using them for data augmentation purpose during training [29], [43], and several other works attempted to perform separation on the unlabeled data with a pre-trained model to generate pseudo labels [44], [45]. We also describe a semi-supervised finetuning pipeline that can be viewed as a mixed pipeline of recent works, which bypasses the requirement of a separately trained source activity detector by directly using a strong pre-trained model as both its own source activity detector and pseudolabel generator. A self-boosting scheme is applied to gradually improve the quality of the generated pseudo-label signals by continuously replacing the pre-trained model by the new best model found in the finetuning stage. This setting allows us to use both the clean and noisy signals in the unlabeled data in the finetuning stage. Experiments show that the semi-supervised finetuning pipeline can further improve the performance of the model in all instrument tracks.

The rest of the paper is organized as follows. Section II introduces the BSRNN architecture. Section III describes the semi-supervised data finetuning pipeline. Section IV provides the detailed configurations for training and evaluation. Section V presents the experiment results and analysis. Section VI concludes the paper.

## II. BAND-SPLIT RNN

Figure 1 (A) shows the overall pipeline of the BSRNN model, which contains a band split module, a band and sequence modeling module, and a mask estimation module.

## A. Band Split Module

Figure 1 (B) shows the design of the band split module. The module takes the complex-valued spectrogram $\mathbf { X } \in \mathbb { C } ^ { F \times T }$ generated by short-time Fourier transform (STFT) as input, where F and $T$ are the frequency and temporal dimensions, respectively, and split it into K subband spectrograms $\mathbf { B } _ { i } \in $ $\mathbb { C } ^ { \dot { G _ { i } } \times T } , i \ \stackrel { \bullet } { = } \ 1 , \ldots , K$ with predefined bandwidth $\{ G _ { i } \} _ { i = 1 } ^ { K }$ satisfying $\textstyle \sum _ { i = 1 } ^ { K } G _ { i } = F$ . The real and imaginary part of each subband spectrogram B<sub>i</sub> is then concatenated and passed to a layer normalization module [46] and a fully-connected (FC) layer to generated a real-valued subband feature $\mathbf { Z } _ { i } \in \mathbb { R } ^ { N \times T }$ Note that since $\{ G _ { i } \} _ { i = 1 } ^ { K }$ can all be different, each subband spectrogram has its own normalization module and FC layer. All K subband features $\{ \mathbf { Z } _ { i } \} _ { i = 1 } ^ { K }$ are then merged to generate a transformed fullband feature tensor $\mathbf { Z } \in \mathbb { R } ^ { N \times K \times T }$

## B. Band and Sequence Modeling Module

Figure 1 (C) shows the band and sequence modeling module. Similar to the dual-path RNN architecture [41], BSRNN performs interleaved sequence-level and band-level modeling via two different residual RNN layers. The sequence-level RNN is first applied to Z across the temporal dimension T, where the K subband features share a same RNN since they have the same feature dimension N. This is to save the model size and allow parallel processing across subbands. The bandlevel RNN is then applied to Z across the band dimension $K ,$ where the RNN is assumed to capture the intra-band feature dependencies across the K subbands at each frame. Both sequence-level and band-level RNNs share a same design, where a group normalization module is first applied to the input of the module, and then a BLSTM layer followed by an FC layer is applied to perform the actual modeling. Residual connection is added between the input and the output of the FC layer. Multiple such RNNs can be stacked to create a deeper architecture, and the output of the last layer is denoted by $\mathbf { Q } \in \mathbb { R } ^ { N \times K \times T }$

## C. Mask Estimation Module

The mask estimation module calculates a complex-valued time-frequency (T-F) mask to extract the target source. Q is first split into K features $\{ \mathbf { Q } _ { i } \} _ { i = 1 } ^ { K } \in \mathbb { R } ^ { N \times \top }$ where each feature corresponds to the transformed feature for a subband, and each subband feature is passed to a layer normalization module followed by a multilayer perceptron (MLP) with one hidden layer to generate the real and imaginary parts of the T-F masks $\mathbf { M } _ { i } \in \mathbb { C } ^ { \mathbf { \tilde { { G } } } _ { i } \times T } , i = 1 , \dots , K$ . The use of MLP follows the observation in [47] where it was reported that a simple MLP can effectively estimate better T-F masks compared to a plain FC layer. Similar to the band split module, each subband feature has its own normalization module and MLP. All M are then merged into the fullband T-F mask M $\in \mathbb { C } ^ { F \times \bar { T } }$ and multiplied with X to generate the target spectrogram $\mathbf { S } \in \mathbb { C } ^ { F \times T }$

## D. Discussion

It is easy to observe that BSRNN can be connected to recent works on dual-path and multi-path networks [48]–[52], groupsplitting modules [53], [54], and super wideband models [55], [56]. Most dual-path architectures split a sequential feature into chunks and perform interleaved local and global processing, and the additional paths in multi-path models were proposed to either split the sequential feature into finer-scale chunks or to apply on extra dimensions such as the spatial dimension in multi-channel signals. However, as the dual-path architecture was originally proposed for time-domain separation systems with relatively small window and hop size [41], its necessity and importance become less crucial in the successful optimization of the model. We also empirically find that replacing the plain BLSTM by dual-path RNN for the sequence modeling module does not lead to a performance gain in BSRNN.

Group-splitting modules were mainly proposed to build lightweight models with fewer model parameters and computational cost, where the main idea was to split a feature vector into groups and perform group-level sequential modeling and intra-group dependency modeling [53], [54]. Such group splitting and communication scheme was originally proposed for time-domain systems where the feature vectors do not have a clear frequency-dependent pattern, hence the intra-group dependency modeling module was designed to ignore the sequential order of the grouped sub-features. Such group-splitting scheme might not be as effective as in speech separation, since different instruments may have significantly different frequency range and timbres and an explicit frequency-dependent feature extraction scheme can be helpful. This serves as the main motivation for us to explicitly split the frequency components to subband features and use a sequential-order-sensitive module to capture the intra-band dependencies. Similar to the group communication models in time-domain systems, we still share the sequence modeling layer across all subbands, as it allows parallel processing across the subbands, saves the model size, and empirically leads to better performance compared to using a separate layer for each subband.

![](figures/d60d5275510eae52c832124744005715f1c184b8120153d37d7fad7c953057fa.jpg)  
Fig. 1. (A) The overall pipeline for the BSRNN model, which consists of a band split module, a sequence and band modeling module, and a mask estimation module. (B) The design of the band split module. (C) The design of the sequence and band modeling module. (D) The design of the mask estimation module.

Current models for super wideband speech enhancement split the frequency componenets into low-frequency and highfrequency bands and use either parallel or sequential network building blocks to process them [55], [56]. Such bandsplitting schemes are simple and coarse, and the intra-band dependencies are not explicitly modeled. BSRNN performs a fine-grained band-splitting scheme that attempts to cover more detailed harmonic patterns in the music signals. On the other hand, BSRNN does not perform strict frequency-binlevel modeling as prior works on automatic speech recognition [57], [58] and fullband speech enhancement [59], [60] in order to save the model complexity, memory footprint and processing speed.

## III. SEMI-SUPERVISED FINETUNING PIPELINE

Collecting high-quality realistic training data with all clean target sources is challenging for not only music signals but a wide range of other types of signals such as environmental sounds. More importantly, as the choice of musical instruments and their arrangements can be completely different in different songs, it is hard to collect clean sources for all possible musical instruments with a satisfying quality. However, a model trained with a limited amount of labeled data may fail in songs with different genres and choices of musical instruments. In this section, we describe how we finetune the model trained with labeled data on additional unlabeled data with semi-supervised data sampling.

## A. Semi-supervised Data Sampling

Given a model P trained on a small-scale labeled dataset L and a large-scale unlabeled dataset U, we generate new training samples by the sampling pipeline described in Figure 2. The core concept of our semi-supervised data sampling pipeline is that we treat the pre-trained model as both a pseudolabel generator [43] and a source activity detector [61]. We sample a segment of clean target and residual signals from L as the supervised training pipeline, where the “residual” signal is defined as the signal that does not contain the target source (e.g., accompaniment when vocal track is the target). We also sample a segment of mixture signal from U and pass it to the pre-trained model P to generate the separated target and residual signals, where the residual signal is defined by subtracting the separated target signal from the mixture. We then use an energy-based data filtering method to detect whether the separated signals are clean or noisy/distorted:

![](figures/ef5fe6258b80482f0e850b6492d4536c12c3957d819b82b60f6dc6a21b1e9971.jpg)  
Fig. 2. The semi-supervised data sampling pipeline for model finetuning.

1) If the energy difference between the mixture and separated target signals, measured on decibel scale, is larger than 30 dB, then the mixture segment is treated as a clean residual segment.

2) If the energy difference between the mixture and separated residual signals, measured on decibel scale, is larger than 30 dB, then the mixture segment is treated as a clean target segment.

This simple energy-based method directly used the pre-trained model as the target source activity detector. The separated signals are not used when the mixture signal is treated as a clean target or residual segment, and they are treated as pseudo labels when the mixture signal contains both the target and residual signals. All clean and pseudo signals are then gathered and one target and one residual signal are resampled from them. Optional data augmentation and mixing process can be applied to the signals, and then the transformed target and residual signals are summed to generate the mixture signal used for the finetuning stage.

During the finetuning stage, we define a new model Q initialize it by P and train it on samples generated by the aforementioned data sampling pipeline. The pre-trained model P can be fixed or sequentially updated by the new Q [44], and we replace P by the new Q whenever Q achieves a better performance than P on the validation set.

## B. Discussion

The data sampling pipeline described here can be connected to a wide range of existing works on knowledge distillation [62]–[65], pseudo label generation [66]–[69], and teacherstudent learning [70]–[72], where a teacher model is used to generate pseudo training targets from a large unlabeled dataset to improve the performance of a student model. More specifically, existing pipelines for source separation include silent source detection [29], pseudo label generation and filtering [43], and self-boosting [44], [45]. The first one trains a classifier on segments of unlabeled data to detect whether the target source is absent, and if so the segment is used as a clean residual signal for data augmentation. However, as the activation of different musical instruments can be sparse in time, the performance of the classifier may highly dependent on whether the training data is balanced, and when the classifier fails the model may use a mixture segment that also contains the target source as the residual. The second one performs standard pseudo label generation pipeline to extract pseudo labels from unlabeled data, and trains a framelevel separate source activity detector to evaluate whether the extracted pseudo labels are high-quality samples. However, the experiments were only conducted on 16k Hz sample rate data on the vocal-accompaniment separation task, and the configuration of the source activity detector was not described in detail. Moreover, as the separated pseudo-label signals may contain distortions, it may require extra data augmentation and training tricks on the optimization of the detectors in order to allow them work well on a specific pre-trained separator. The last one also generates pseudo labels for data augmentation, while it also continuously improves the teacher by sequentially replacing the teacher by the latest student and double the size of the student model during training. The robustness against the noisy teacher outputs is obtained by generating a large batch of noisy samples with a more diverse data remixing paradigm, together with an unsupervised training objective. However, it was only evaluated on speech enhancement task with 16k Hz sample rate either, and the use of large number of pseudo label samples as well as the increase of the student model size may introduce additional difficulties in the application of the pipeline on large-scale models.

As described above, the data sampling pipeline we use can be viewed as a combination of all existing pipelines – we use both detected clean segments and generated pseudo-label signals in the unlabeled dataset via a strong pre-trained model. This allows us to not only alleviate the need of an external classifier or source activity detector while still able to detect clean segments within an unlabeled song, but also make use of the pseudo label signals in a similar way as existing pipelines.

## IV. EXPERIMENT CONFIGURATIONS

## A. Supervised Training

1) Data Preprocessing: Similar to existing works, we use the MUSDB18-HQ dataset [42] for all experiments. During the preparation of the training data, we apply a source activity detector (SAD) to remove the silent regions in the sound tracks and only lead the salient ones for data mixing. Although any existing SAD systems can be directly applied, here we introduce a simple unsupervised energy-based thresholding method to select salient segments from a full track.

Given a unsegmented track and a segment length L measured by duration (e.g., second), we first split the sound track into overlapped segments of length L with an overlap ratio of 50%. For each segment, we further split it into 10 chunks of length $L / 1 0$ and calculate the energy of them. For silent chunks, we set their energy to a small value $\epsilon = 1 e - 5$ . We then calculate an energy threshold of the full sound track by calculating the maximum value of the 15% quantile of the energy of all chunks and another small value $\gamma = 1 e - 3$ . If there are more than 50% of the chunks in a segment having their energy higher than the threshold, then we define the segment as a salient segment and save it as a valid training data segment. In our training configuration, we set $L = 6$ seconds.

2) On-the-fly Data Simulation: We apply batch-level on-thefly data simulation by randomly mixing sound tracks from different songs [73]. Given a training data length $T \ \leq \ L$ and the type of target source (e.g., vocal, bass, drum or other in MUSDB dataset), we first randomly sample 1 SADpreprocessed salient segment of length L for all tracks, and then randomly select a chunk of length T (We set $T = 3$ seconds by default). For each chunk, we randomly rescale its energy between [−10, 10] dB compared to its original energy. We then randomly drop the each chunk with probability 0.1 to mimic the segments where the target source is inactive. We add up all chunks to form the mixture. To ensure all samples are in the same scale, we rescale both the mixture and the target by the maximum of the maximum absolute value of their samples.

3) Training Objective: The training objective is defined as the sum of a frequency-domain mean-absolute-error (MAE) loss and a time-domain MAE loss:

$$
\mathcal {L} _ {o b j} = \left| \mathrm{S} _ {r} - \bar {\mathrm{S}} _ {r} \right| _ {1} + \left| \mathrm{S} _ {i} - \bar {\mathrm{S}} _ {i} \right| _ {1} + \left| \mathrm{iSTFT} (\mathrm{S}) - \mathrm{iSTFT} (\bar {\mathrm{S}}) \right| _ {1} \tag {1}
$$

where $\bar { \mathbf { S } } \in \mathbb { C } ^ { F \times T }$ denotes the complex-valued spectrogram of the clean target, subscript r and l denote the real and imaginary parts, respectively, and iSTFT denotes the inverse STFT operator.

4) Hyperparameter Configuration: We set the window size and hop size of STFT to 2048 and 512, respectively, and use a Hanning window. We set the feature dimension N to be 128 in all experiments, and use 12 band and sequence modeling modules with a total of 24 residual BLSTM layers. We set the hidden unit of BLSTM layers to be 2N = 256, the hidden size in the mask estimation MLP to be 4N = 512, and use the hyperbolic tangent function as the nonlinear activation function in the MLP. We use a gated linear unit (GLU) [74] for the output layer of the MLP. The band split bandwidth will be discussed in Section V-A.

We train individual models for each of the target tracks, which means that we treat the MSS problem as a source extraction problem with only one signal-of-interest. All models are trained for 100 epochs with the Adam optimizer [75] with an initial learning rate of $1 e - 3 .$ , and each epoch contains 10000 batches of samples with a batch size of 2 and number of GPUs of 8. The learning rate is decayed by 0.98 for every two epochs, and gradient clipping by a maximum gradient norm of 5 is applied. Early stopping is applied when the best validation is not found in 10 consecutive epochs.

## B. Semi-supervised Finetuning

We use another private dataset of 1750 songs for the semisupervised finetuning stage. The data sampling process in the on-the-fly simulation pipeline follows the one we described in Section III-A, where we set the MUSDB18-HQ dataset as L and the private dataset as U. The private dataset is also passed to the source activity detector to remove silent segments before training. We set the initial learning rate for the finetuning stage to $1 e - 4 ,$ , and all other configurations are kept identical to the supervised training stage.

## C. Evaluation

During the evaluation phase, we split the full song into chunks of length $T$ and hop size of $P \leq T$ , and perform zeropadding of length $L - P$ at the beginning and the end. All chunks are then processed by the trained model, and overlapadd is applied to all separated outputs to form the final output with the original duration. We set $\mathrm { \dot { \it P } = 0 . 5 }$ seconds by default and discuss the effect of different P in Section V-B. We report the model performance on both MUSDB18-HQ and MUSDB18 dataset [76].

## D. Metrics

We evaluate the models with two metrics:

1) uSDR: uSDR corresponds to the modified utterancelevel signal-to-distortion ratio metric proposed in [77] and used as the default evaluation metric in the Music Demixing (MDX) Challenge 2021. The definition of uSDR is identical to the standard signal-to-noise ratio (SNR). We report the mean across the SDR scores of all songs.

2) cSDR: cSDR corresponds to the chunk-level SDR calculated by the standard SDR metric in bss eval metrics [78] and served as the default evaluation metric in the Signal Separation Evaluation Campaign (SiSEC) [79]. We use the official implementation<sup>1</sup> which reports the median across the median SDR over all 1 second chunks in each song.

Both metrics are reported on decibel scale.

## V. RESULTS AND ANALYSIS

## A. Effect of Band Split Bandwidth

The band split bandwidth $\{ G _ { i } \} _ { i = 1 } ^ { K }$ needs to be manually defined and may affect the performance. We first select seven different options for $\{ G _ { i } \} _ { i = 1 } ^ { K }$ and compare the models:

1) V1: We evenly split the entire spectrogram by a 1k Hz bandwidth (remainders are merged to the last subband). This results in 22 subbands.

2) V2: We split the frequency band below 16k Hz by a 1k Hz bandwidth, the frequency band between 16k Hz and 20k Hz by a 2k Hz bandwidth, and treat the rest as one subband. This results in 19 subbands.

3) V3: We split the frequency band below 8k Hz by a 1k Hz bandwidth, split the frequency band between 8k Hz and 16k Hz by a 2k Hz bandwidth, treat the frequency band between 16k Hz and 20k Hz as one subband, and treat the rest as another subband. This results in 14 subbands.

4) V4: We split the frequency band below 1k Hz by a 100 Hz bandwidth, split the frequency band between 1k Hz and 8k Hz by a 1k Hz bandwidth, split the frequency band between 8k Hz and 16k Hz by a 2k Hz bandwidth, treat the frequency band between 16k Hz and 20k Hz as one subband, and treat the rest as another subband. This results in 23 subbands.

5) V5: We split the frequency band below 1k Hz by a 100 Hz bandwidth, split the frequency band between 1k Hz and 16k Hz by a 1k Hz bandwidth, split the frequency band between 16k Hz and 20k Hz by a 2k Hz bandwidth, and treat the rest as one subband. This results in 28 subbands.

6) V6: We split the frequency band below 1k Hz by a 100 Hz bandwidth, split the frequency band between 1k Hz and 4k Hz by a 500 Hz bandwidth, split the frequency band between 4k Hz and 8k Hz by a 1k Hz bandwidth, split the frequency band between 8k Hz and 16k Hz by a 2k Hz bandwidth, treat the frequency band between 16k Hz and 20k Hz as one subband, and treat the rest as another subband. This results in 26 subbands.

7) V7: We split the frequency band below 1k Hz by a 100 Hz bandwidth, split the frequency band between 1k Hz and 4k Hz by a 250 Hz bandwidth, split the frequency band between 4k Hz and 8k Hz by a 500 Hz bandwidth, split the frequency band between 8k Hz and 16k Hz by a 1k Hz bandwidth, split the frequency band between 16k Hz and 20k Hz by a 2k Hz bandwidth, and treat the rest as one subband. This results in 41 subbands.

Table I provides the vocal extraction performance evaluated by the uSDR metric across the MUSDB18-HQ test set. We can see that the performance of V1 to V3 remain on par, but V4 provides a significant gain. Given that the main difference between V3 and V4 is the split of finer subbands below 1k Hz, it shows that lower frequency bands are important for the model to successfully estimate more accurate spectrograms, and a possible explanation is that the frequency band below 1k Hz typically covers the fundamental frequency and the first few harmonics of the vocal track, which enables the band modeling RNN to better capture the F0 information and to better estimate higher frequency components. As more subbands are split at lower frequency parts from V4 to V7, the performance continues to improve, further showing that a fine-grained band-splitting scheme is essential for BSRNN to get better performance. Moreover, we further perform a smallscale grid search and use the following band split bandwidths for the bass, drum and other tracks in MUSDB18:

1) Bass: We split the frequency band below 500 Hz by a 50 Hz bandwidth, split the frequency band between 500 Hz and 1k Hz by a 100 Hz bandwidth, split the frequency band between 1k Hz and 4k Hz by a 500 Hz bandwidth, split the frequency band between 4k Hz and 8k Hz by a 1k Hz bandwidth, split the frequency band between 8k Hz and 16k Hz by a 2k Hz bandwidth, and treat the rest as one subband. This results in 30 subbands.

2) Drum: We split the frequency band below 1k Hz by a 50 Hz bandwidth, split the frequency band between 1k Hz and 2k Hz by a 100 Hz bandwidth, split the frequency band between 2k Hz and 4k Hz by a 250 Hz bandwidth, split the frequency band between 4k Hz and 8k Hz by a 500 Hz bandwidth, split the frequency band between 8k Hz and 16k Hz by a 1k Hz bandwidth, and treat the rest as one subband. This results in 55 subbands.

3) Other: We use the same band split scheme as vocals (i.e., V7 above).

We empirically find that different instrument tracks may have their own superior band split schemes than that for vocals. Given that different instruments can have different frequency ranges, harmonic patterns and mixing techniques, the observation shows that such a priori knowledge or expert knowledge may play an important role in exploring intrinsic characteristics of different musical instruments. Note that adjusting the band split bandwidths may further improve the model performance, and here we do not perform exhaustive grid search for the sake of simplicity.

TABLE I. PERFORMANCE ON VOCAL EXTRACTION FOR BSRNN MODELS WITH DIFFERENT BAND SPLIT BANDWIDTHS.

<table><tr><td>Bandwidth</td><td>V1</td><td>V2</td><td>V3</td><td>V4</td><td>V5</td><td>V6</td><td>V7</td></tr><tr><td>uSDR</td><td>8.15</td><td>8.21</td><td>8.06</td><td>9.51</td><td>9.57</td><td>9.78</td><td>10.04</td></tr></table>

TABLE II. PERFORMANCE ON VOCAL EXTRACTION FOR BSRNN MODELS WITH DIFFERENT EVALUATION SEGMENT HOP SIZES.

<table><tr><td>Hop size (s)</td><td>0.5</td><td>1</td><td>1.5</td><td>3</td></tr><tr><td>uSDR</td><td>10.04</td><td>10.00</td><td>9.94</td><td>9.75</td></tr></table>

## B. Effect of Evaluation Segment Hop Size

Table I reports model performance with the default evaluation segment hop size of $P \ = \ 0 . 5$ seconds. We also report the model performance with different segment hop sizes here. Table II shows the uSDR scores with models with four different hop sizes and a fixed segment size of

TABLE III. COMPARISON WITH EXISTING MODELS ON MUSDB18-HQ (HQ) AND MUSDB18 (NHQ) DATASET.

<table><tr><td rowspan="3">Model</td><td colspan="4">Vocals</td><td colspan="4">Bass</td><td colspan="4">Drum</td><td colspan="4">Other</td><td colspan="4">All</td></tr><tr><td colspan="2">uSDR</td><td colspan="2">cSDR</td><td colspan="2">uSDR</td><td colspan="2">cSDR</td><td colspan="2">uSDR</td><td colspan="2">cSDR</td><td colspan="2">uSDR</td><td colspan="2">cSDR</td><td colspan="2">uSDR</td><td colspan="2">cSDR</td></tr><tr><td>HQ</td><td>nHQ</td><td>HQ</td><td>nHQ</td><td>HQ</td><td>nHQ</td><td>HQ</td><td>nHQ</td><td>HQ</td><td>nHQ</td><td>HQ</td><td>nHQ</td><td>HQ</td><td>nHQ</td><td>HQ</td><td>nHQ</td><td>HQ</td><td>nHQ</td><td>HQ</td><td>nHQ</td></tr><tr><td>ResUNetDecouple+ [25]</td><td>-</td><td>-</td><td>-</td><td>8.98</td><td>-</td><td>-</td><td>-</td><td>6.04</td><td>-</td><td>-</td><td>-</td><td>6.62</td><td>-</td><td>-</td><td>-</td><td>5.29</td><td>-</td><td>-</td><td>-</td><td>6.73</td></tr><tr><td>CWS-PResUNet [26]</td><td>-</td><td>-</td><td>8.92</td><td>-</td><td>-</td><td>-</td><td>5.93</td><td>-</td><td>-</td><td>-</td><td>6.38</td><td>-</td><td>-</td><td>-</td><td>5.84</td><td>-</td><td>-</td><td>-</td><td>6.77</td><td>-</td></tr><tr><td>KUIELab-MDX-Net [32]</td><td>-</td><td>-</td><td>8.97</td><td>9.00</td><td>-</td><td>-</td><td>7.83</td><td>7.86</td><td>-</td><td>-</td><td>7.20</td><td>7.33</td><td>-</td><td>-</td><td>5.90</td><td>5.95</td><td>-</td><td>-</td><td>7.47</td><td>7.54</td></tr><tr><td>Hybrid Demucs [31]</td><td>-</td><td>-</td><td>8.13</td><td>8.04</td><td>-</td><td>-</td><td>8.76</td><td>8.67</td><td>-</td><td>-</td><td>8.24</td><td>8.58</td><td>-</td><td>-</td><td>5.59</td><td>5.59</td><td>-</td><td>-</td><td>7.68</td><td>7.72</td></tr><tr><td>BSRNN</td><td>10.04</td><td>9.92</td><td>10.01</td><td>10.21</td><td>6.80</td><td>6.77</td><td>7.22</td><td>7.51</td><td>8.92</td><td>8.68</td><td>9.01</td><td>8.58</td><td>6.01</td><td>5.97</td><td>6.70</td><td>6.62</td><td>7.94</td><td>7.84</td><td>8.24</td><td>8.23</td></tr><tr><td>+ finetuning</td><td>10.47</td><td>10.36</td><td>10.47</td><td>10.53</td><td>7.20</td><td>7.17</td><td>8.16</td><td>8.30</td><td>9.66</td><td>9.46</td><td>10.15</td><td>9.65</td><td>6.33</td><td>6.27</td><td>7.08</td><td>7.00</td><td>8.42</td><td>8.32</td><td>8.97</td><td>8.87</td></tr></table>

$T = 3$ seconds. We can see that choosing any $P \leq T$ can result in a performance improvement, and the reason can be because the overlap-add operation smooths the outputs and mitigates the noise or distortion introduced. We can also find that decreasing P from 1.5 to 0.5 does not provide significant gain while linearly increases the processing time with the extra segments. This shows that although we choose $P = 0 . 5$ for the experiments here, in practice one can choose $P = 1 . 5$ for a balance between processing speed and performance.

## C. Comparison with State-of-the-art Systems

Here we compare the BSRNN model with existing stateof-the-art systems on both MUSDB18 and MUSDB18-HQ dataset. We choose the top-ranking systems in the Music Demixing (MDX) Challenge 2021 [77] as the baselines. We report the results before and after the semi-supervised finetuning stage for BSRNN for all the four tracks. For the other systems, the best reported numbers found in all available literatures are reported. Table III presents the results on both MUSDB18 and MUSDB18-HQ dataset on both uSDR and cSDR metrics. We can observe that BSRNN trained only on MUSDB18-HQ dataset outperforms all existing systems on vocal, drum and other tracks on both MUSDB18 and MUSDB18-HQ dataset, and performs slightly worse on bass track. Possible explanations for this observation are that the energy rescaling process in our data mixing procedure might not be well suited for bass as empirically bass is not as strong as other instruments in a song, and the band-split scheme needs further investigation to better capture low- and mid-frequency range information where bass lies in. Regarding the semisupervised finetuning stage, we observe that all tracks are able to obtain a performance gain, especially for bass and drum tracks where we can observe an around 1 dB improvement on the cSDR metric. Compared to existing semi-supervised methods described in Section III, our self-boosting finetuning pipeline is evaluated on all instrument tracks instead of a vocal or speech only task, and the experiments are also conducted on 44.1k Hz sample rate signals instead of 16k Hz sample rate signals. Moreover, our pipeline does not lead to a gradually increased model size as [44], and does not need external modules that require separate training procedures as [29], [43]. This proves that the proposed semi-supervised finetuning stage has the potential to become a more universal pipeline for general source extraction or separation tasks.

## VI. CONCLUSION AND FUTURE WORKS

In this paper, we proposed band-split RNN (BSRNN), a model architecture that was designed for music source separation and general high-sample-rate source separation that can take a priori knowledge on the characteristics of the source to be separated into account when determining the model hyperparameters. BSRNN split the complex-valued spectrogram of the input mixture in multiple subbands with differend bandwidths, and performed interleaved sequencelevel and band-level processing via recurrent neural networks. We also described a semi-supervised data sampling pipeline for finetuning the model trained on a small-scale labeled dataset on a large-scaled unlabeled dataset. Experiment results on MUSDB18 and MUDSB18-HQ dataset showed that BSRNN can surpass the performance of existing state-of-the-art music source separation systems, and the semi-supervised finetuning pipeline can further improve the performance and the robustness on songs with various genres. Future works include the investigation of better and cleverer ways to incorporate a prior source-specific knowledge into the choice of band-splitting schemes rather than large-scale grid search, and the validation of the model and the pipeline on more types of musical instruments and universal audio extraction and separation tasks. Moreover, the size of the private dataset we used for the semi-supervised finetuning stage is not large compared to prior works [29], and we only used lossless data with .wav or .flac formats and removed the songs with all other lossy compression formats (e.g., .mp3). As there exists a wide range of songs encoded with lossy compression formats, adding such data to the pipeline may allow the band-level RNN layer to learn to deal with the signals with a distorted higher frequency component, and further improve the model performance on both the MUSDB18 dataset (with .mp4 format) and other realworld recordings. The effects of additional data size and data type in both supervised training and semi-supervised finetuning stages are also left for future study.

## REFERENCES

[1] O. Gillet and G. Richard, “Extraction and remixing of drum tracks from polyphonic music signals,” in IEEE Workshop on Applications ofSignal Processing to Audio and Acoustics, 2005. IEEE, 2005, pp. 315–318.

[2] J. F. Woodruff, B. Pardo, and R. B. Dannenberg, “Remixing stereo music with score-informed source separation.” in ISMIR, 2006, pp. 314– 319.

[3] J. Pons, J. Janer, T. Rode, and W. Nogueira, “Remixing music using source separation algorithms to improve the musical experience of cochlear implant users,” The Journal of the Acoustical Society of America, vol. 140, no. 6, pp. 4338–4349, 2016.

[4] N. Ono, K. Miyamoto, H. Kameoka, J. L. Roux, Y. Uchiyama, E. Tsunoo, T. Nishimoto, and S. Sagayama, “Harmonic and percussive sound separation and its application to MIR-related tasks,” in Advances in music information retrieval. Springer, 2010, pp. 213–236.

[5] A. Mesaros and T. Virtanen, “Automatic recognition of lyrics in singing,” EURASIP Journal on Audio, Speech, and Music Processing, vol. 2010, pp. 1–11, 2010.

[6] K. Itoyama, M. Goto, K. Komatani, T. Ogata, and H. G. Okuno, “Queryby-example music information retrieval by score-informed source separation and remixing technologies,” EURASIP journal on Advances in Signal Processing, vol. 2010, pp. 1–14, 2011.

[7] A. Rosner, B. Kostek, and B. Schuller, “Classification of music genres based on music separation into harmonic and drum components,” Archives of Acoustics, pp. 629–638, 2014.

[8] L. Lin, Q. Kong, J. Jiang, and G. Xia, “A unified model for zero-shot music source separation, transcription and synthesis,” in Proceedings of 21st International Conference on Music Information Retrieval, ISMIR, 2021.

[9] C. Dittmar, E. Cano, J. Abeßer, and S. Grollmisch, “Music information retrieval meets music education,” in Dagstuhl Follow-Ups, vol. 3. Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik, 2012.

[10] E. Cano, G. Schuller, and C. Dittmar, “Pitch-informed solo and accompaniment separation towards its use in music education applications,” EURASIP Journal on Advances in Signal Processing, vol. 2014, no. 1, pp. 1–19, 2014.

[11] C. Macartney and T. Weyde, “Improved speech enhancement with the wave-u-net,” arXiv preprint arXiv:1811.11307, 2018.

[12] R. Giri, U. Isik, and A. Krishnaswamy, “Attention wave-u-net for speech enhancement,” in 2019 IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA). IEEE, 2019, pp. 249–253.

[13] A. Defossez, G. Synnaeve, and Y. Adi, “Real time speech enhancement ´ in the waveform domain,” Proc. Interspeech, pp. 3291–3295, 2020.

[14] T. Jenrungrot, V. Jayaram, S. Seitz, and I. Kemelmacher-Shlizerman, “The cone of silence: Speech separation by localization,” Advances in Neural Information Processing Systems, vol. 33, pp. 20 925–20 938, 2020.

[15] H. Liu, Q. Kong, Q. Tian, Y. Zhao, D. Wang, C. Huang, and Y. Wang, “VoiceFixer: Toward general speech restoration with neural vocoder,” arXiv preprint arXiv:2109.13731, 2021.

[16] A. A. Nugraha, A. Liutkus, and E. Vincent, “Multichannel music separation with deep neural networks,” in 2016 24th European Signal Processing Conference (EUSIPCO). IEEE, 2016, pp. 1748–1752.

[17] A. Jansson, E. Humphrey, N. Montecchio, R. Bittner, A. Kumar, and T. Weyde, “Singing voice separation with deep U-net convolutional networks.” in ISMIR, 2017, pp. 745–751.

[18] Y. Luo, Z. Chen, J. R. Hershey, J. Le Roux, and N. Mesgarani, “Deep clustering and conventional networks for music separation: Stronger together,” in Acoustics, Speech and Signal Processing (ICASSP), 2017 IEEE International Conference on. IEEE, 2017, pp. 61–65.

[19] P. Chandna, M. Miron, J. Janer, and E. Gomez, “Monoaural audio´ source separation using deep convolutional neural networks,” in International conference on latent variable analysis and signal separation. Springer, 2017, pp. 258–266.

[20] S. Park, T. Kim, K. Lee, and N. Kwak, “Music source separation using stacked hourglass networks.” in ISMIR, 2018, pp. 289–296.

[21] N. Takahashi, N. Goswami, and Y. Mitsufuji, “MMDenseLSTM: An efficient combination of convolutional and recurrent neural networks for audio source separation,” in 2018 16th International Workshop on Acoustic Signal Enhancement (IWAENC). IEEE, 2018, pp. 106–110.

[22] N. Takahashi and Y. Mitsufuji, “D3Net: Densely connected multidilated DenseNet for music source separation,” arXiv preprint arXiv:2010.01733, 2020.

[23] R. Hennequin, A. Khlif, F. Voituret, and M. Moussallam, “Spleeter: a

fast and efficient music source separation tool with pre-trained models,” Journal of Open Source Software, vol. 5, no. 50, p. 2154, 2020.

[24] T. Li, J. Chen, H. Hou, and M. Li, “Sams-net: A sliced attention-based neural network for music source separation,” in 2021 12th International Symposium on Chinese Spoken Language Processing (ISCSLP). IEEE, 2021, pp. 1–5.

[25] Q. Kong, Y. Cao, H. Liu, K. Choi, and Y. Wang, “Decoupling magnitude and phase estimation with deep resunet for music source separation,” arXiv preprint arXiv:2109.05418, 2021.

[26] H. Liu, Q. Kong, and J. Liu, “CWS-PResUNet: Music source separation with channel-wise subband phase-aware resunet,” arXiv preprint arXiv:2112.04685, 2021.

[27] D. Stoller, S. Ewert, and S. Dixon, “Wave-U-Net: A multi-scale neural network for end-to-end audio source separation.” in ISMIR, 2018, pp. 334–340.

[28] A. Defossez, N. Usunier, L. Bottou, and F. Bach, “Music source´ separation in the waveform domain,” arXiv preprint arXiv:1911.13254, 2019.

[29] ——, “Demucs: Deep extractor for music sources with extra unlabeled data remixed,” arXiv preprint arXiv:1909.01174, 2019.

[30] D. Samuel, A. Ganeshan, and J. Naradowsky, “Meta-learning extractors for music source separation,” in Acoustics, Speech and Signal Processing (ICASSP), 2020 IEEE International Conference on. IEEE, 2020, pp. 816–820.

[31] A. Defossez, “Hybrid spectrogram and waveform source separation,” in´ Proceedings of the ISMIR 2021 Workshop on Music Source Separation, 2021.

[32] M. Kim, W. Choi, J. Chung, D. Lee, and S. Jung, “KUIELab-MDX-Net: A two-stream neural network for music demixing,” arXiv preprint arXiv:2111.12203, 2021.

[33] P.-S. Huang, M. Kim, M. Hasegawa-Johnson, and P. Smaragdis, “Deep learning for monaural speech separation,” in Acoustics, Speech and Signal Processing (ICASSP), 2014 IEEE International Conference on. IEEE, 2014, pp. 1562–1566.

[34] ——, “Joint optimization of masks and deep recurrent neural networks for monaural source separation,” IEEE/ACM Transactions on Audio, Speech and Language Processing (TASLP), vol. 23, no. 12, pp. 2136– 2147, 2015.

[35] J. R. Hershey, Z. Chen, J. Le Roux, and S. Watanabe, “Deep clustering: Discriminative embeddings for segmentation and separation,” in Acoustics, Speech and Signal Processing (ICASSP), 2016 IEEE International Conference on. IEEE, 2016, pp. 31–35.

[36] Y. Luo and N. Mesgarani, “Conv-TasNet: Surpassing ideal time– frequency magnitude masking for speech separation,” IEEE/ACM Transactions on Audio, Speech, and Language Processing (TASLP), vol. 27, no. 8, pp. 1256–1266, 2019.

[37] O. Ronneberger, P. Fischer, and T. Brox, “U-net: Convolutional networks for biomedical image segmentation,” in International Conference on Medical image computing and computer-assisted intervention. Springer, 2015, pp. 234–241.

[38] A. Newell, K. Yang, and J. Deng, “Stacked hourglass networks for human pose estimation,” in European conference on computer vision. Springer, 2016, pp. 483–499.

[39] G. Huang, Z. Liu, L. Van Der Maaten, and K. Q. Weinberger, “Densely connected convolutional networks,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2017, pp. 4700–4708.

[40] S. R. Livingstone, K. Peck, and F. A. Russo, “Acoustic differences in the speaking and singing voice,” in Proceedings of Meetings on Acoustics ICA2013, vol. 19, no. 1. Acoustical Society of America, 2013, p. 035080.

[41] Y. Luo, Z. Chen, and T. Yoshioka, “Dual-path RNN: efficient long sequence modeling for time-domain single-channel speech separation,” in Acoustics, Speech and Signal Processing (ICASSP), 2020 IEEE International Conference on. IEEE, 2020, pp. 46–50.

[42] Z. Rafii, A. Liutkus, F.-R. Stoter, S. I. Mimilakis, and R. Bittner,¨ “Musdb18-hq - an uncompressed version of musdb18,” Aug. 2019. [Online]. Available: https://doi.org/10.5281/zenodo.3338373

[43] Z. Wang, R. Giri, U. Isik, J.-M. Valin, and A. Krishnaswamy, “Semisupervised singing voice separation with noisy self-training,” in Acoustics, Speech and Signal Processing (ICASSP), 2021 IEEE International Conference on. IEEE, 2021, pp. 31–35.

[44] E. Tzinis, Y. Adi, V. K. Ithapu, B. Xu, P. Smaragdis, and A. Kumar, “Remixit: Continual self-training of speech enhancement models via bootstrapped remixing,” IEEE Journal of Selected Topics in Signal Processing, 2022.

[45] E. Tzinis, Y. Adi, V. K. Ithapu, B. Xu, and A. Kumar, “Continual self-training with bootstrapped remixing for speech enhancement,” in Acoustics, Speech and Signal Processing (ICASSP), 2022 IEEE International Conference on. IEEE, 2022, pp. 6947–6951.

[46] J. L. Ba, J. R. Kiros, and G. E. Hinton, “Layer normalization,” arXiv preprint arXiv:1607.06450, 2016.

[47] K. Li and Y. Luo, “On the use of deep mask estimation module for neural source separation systems,” Proc. Interspeech, 2022.

[48] K. Kinoshita, T. von Neumann, M. Delcroix, T. Nakatani, and R. Haeb-Umbach, “Multi-path RNN for hierarchical modeling of long sequential data and its application to speaker stream separation,” Proc. Interspeech 2020, pp. 2652–2656, 2020.

[49] J. Chen, Q. Mao, and D. Liu, “Dual-path transformer network: Direct context-aware modeling for end-to-end monaural speech separation,” Proc. Interspeech, pp. 2642–2646, 2020.

[50] C. Subakan, M. Ravanelli, S. Cornell, M. Bronzi, and J. Zhong, “Attention is all you need in speech separation,” in Acoustics, Speech and Signal Processing (ICASSP), 2021 IEEE International Conference on. IEEE, 2021, pp. 21–25.

[51] F. Dang, H. Chen, and P. Zhang, “DPT-FSNet: Dual-path transformer based full-band and sub-band fusion network for speech enhancement,” in Acoustics, Speech and Signal Processing (ICASSP), 2022 IEEE International Conference on. IEEE, 2022, pp. 6857–6861.

[52] A. Pandey, B. Xu, A. Kumar, J. Donley, P. Calamia, and D. Wang, “TPARN: Triple-path attentive recurrent network for time-domain multichannel speech enhancement,” in Acoustics, Speech and Signal Processing (ICASSP), 2022 IEEE International Conference on. IEEE, 2022, pp. 6497–6501.

[53] Y. Luo, C. Han, and N. Mesgarani, “Ultra-lightweight speech separation via group communication,” in Acoustics, Speech and Signal Processing (ICASSP), 2021 IEEE International Conference on. IEEE, 2021, pp. 16–20.

[54] ——, “Group communication with context codec for lightweight source separation,” IEEE/ACM Transactions on Audio, Speech, and Language Processing (TASLP), vol. 29, pp. 1752–1761, 2021.

[55] X. Zhang, L. Chen, X. Zheng, X. Ren, C. Zhang, L. Guo, and B. Yu, “A two-step backward compatible fullband speech enhancement system,” in Acoustics, Speech and Signal Processing (ICASSP), 2022 IEEE International Conference on. IEEE, 2022, pp. 7762–7766.

[56] S. Lv, Y. Fu, M. Xing, J. Sun, L. Xie, J. Huang, Y. Wang, and T. Yu, “S-DCCRN: Super wide band DCCRN with learnable complex feature for speech enhancement,” in Acoustics, Speech and Signal Processing (ICASSP), 2022 IEEE International Conference on. IEEE, 2022, pp. 7767–7771.

[57] J. Li, A. Mohamed, G. Zweig, and Y. Gong, “LSTM time and frequency recurrence for automatic speech recognition,” in Automatic Speech Recognition and Understanding (ASRU), 2015 IEEE Workshop on. IEEE, 2015, pp. 187–191.

[58] ——, “Exploring multidimensional LSTMs for large vocabulary ASR,” in Acoustics, Speech and Signal Processing (ICASSP), 2016 IEEE International Conference on. IEEE, 2016, pp. 4940–4944.

[59] X. Hao, X. Su, R. Horaud, and X. Li, “Fullsubnet: A full-band and subband fusion model for real-time single-channel speech enhancement,”

in Acoustics, Speech and Signal Processing (ICASSP), 2021 IEEE International Conference on. IEEE, 2021, pp. 6633–6637.

[60] J. Chen, Z. Wang, D. Tuo, Z. Wu, S. Kang, and H. Meng, “Fullsubnet+: Channel attention fullsubnet with complex spectrograms for speech enhancement,” in Acoustics, Speech and Signal Processing (ICASSP), 2022 IEEE International Conference on. IEEE, 2022, pp. 7857–7861.

[61] R. Kumar, Y. Luo, and N. Mesgarani, “Music source activity detection and separation using deep attractor network,” in Proc. Interspeech, 2018, pp. 347–351.

[62] G. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” arXiv preprint arXiv:1503.02531, 2015.

[63] T. Asami, R. Masumura, Y. Yamaguchi, H. Masataki, and Y. Aono, “Domain adaptation of DNN acoustic models using knowledge distillation,” in Acoustics, Speech and Signal Processing (ICASSP), 2017 IEEE International Conference on. IEEE, 2017, pp. 5185–5189.

[64] G. Xu, Z. Liu, X. Li, and C. C. Loy, “Knowledge distillation meets selfsupervision,” in European Conference on Computer Vision. Springer, 2020, pp. 588–604.

[65] J. Gou, B. Yu, S. J. Maybank, and D. Tao, “Knowledge distillation: A survey,” International Journal of Computer Vision, vol. 129, no. 6, pp. 1789–1819, 2021.

[66] D.-H. Lee et al., “Pseudo-label: The simple and efficient semisupervised learning method for deep neural networks,” in Workshop on challenges in representation learning, ICML, vol. 3, no. 2, 2013, p. 896.

[67] Q. Xie, M.-T. Luong, E. Hovy, and Q. V. Le, “Self-training with noisy student improves imagenet classification,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2020, pp. 10 687–10 698.

[68] E. Arazo, D. Ortego, P. Albert, N. E. O’Connor, and K. McGuinness, “Pseudo-labeling and confirmation bias in deep semi-supervised learning,” in 2020 International Joint Conference on Neural Networks (IJCNN). IEEE, 2020, pp. 1–8.

[69] H. Pham, Z. Dai, Q. Xie, and Q. V. Le, “Meta pseudo labels,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2021, pp. 11 557–11 568.

[70] J. Li, M. L. Seltzer, X. Wang, R. Zhao, and Y. Gong, “Large-scale domain adaptation via teacher-student learning,” Proc. Interspeech, pp. 2386–2390, 2017.

[71] T. Matiisen, A. Oliver, T. Cohen, and J. Schulman, “Teacher–student curriculum learning,” IEEE Transactions on Neural Networks and Learning Systems, vol. 31, no. 9, pp. 3732–3740, 2019.

[72] J. Zhang, C. Zorila, R. Doddipatla, and J. Barker, “Teacher-student MixIT for unsupervised and semi-supervised speech separation,” arXiv preprint arXiv:2106.07843, 2021.

[73] S. Uhlich, M. Porcu, F. Giron, M. Enenkl, T. Kemp, N. Takahashi, and Y. Mitsufuji, “Improving music source separation based on deep neural networks through data augmentation and network blending,” in Acoustics, Speech and Signal Processing (ICASSP), 2017 IEEE International Conference on. IEEE, 2017, pp. 261–265.

[74] Y. N. Dauphin, A. Fan, M. Auli, and D. Grangier, “Language modeling with gated convolutional networks,” arXiv preprint arXiv:1612.08083, 2016.

[75] D. Kingma and J. Ba, “Adam: A method for stochastic optimization,” arXiv preprint arXiv:1412.6980, 2014.

[76] Z. Rafii, A. Liutkus, F.-R. Stoter, S. I. Mimilakis, and R. Bittner,¨ “The MUSDB18 corpus for music separation,” Dec. 2017. [Online]. Available: https://doi.org/10.5281/zenodo.1117372

[77] Y. Mitsufuji, G. Fabbro, S. Uhlich, and F.-R. Stoter, “Music demixing¨ challenge 2021,” arXiv preprint arXiv:2108.13559, 2021.

[78] E. Vincent, R. Gribonval, and C. Fevotte, “Performance measurement´ in blind audio source separation,” IEEE/ACM Transactions on Audio, Speech, and Language Processing (TASLP), vol. 14, no. 4, pp. 1462– 1469, 2006.

[79] F.-R. Stoter, A. Liutkus, and N. Ito, “The 2018 signal separation eval-¨ uation campaign,” in Latent Variable Analysis and Signal Separation: 14th International Conference, LVA/ICA 2018, Surrey, UK, 2018, pp. 293–305.