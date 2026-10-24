Nils L. Westhausen    Bernd T. Meyer

###### Abstract

This paper introduces a real-time time-domain packet loss concealment (PLC) neural-network (tPLCnet). It efficiently predicts lost frames from a short context buffer in a sequence-to-one (seq2one) fashion. Because of its seq2one structure, a continuous inference of the model is not required since it can be triggered when packet loss is actually detected. It is trained on 64 h of open-source speech data and packet-loss traces of real calls provided by the Audio PLC Challenge. The model with the lowest complexity described in this paper reaches a robust PLC performance and consistent improvements over the zero-filling baseline for all metrics. A configuration with higher complexity is submitted to the PLC Challenge and shows a performance increase of 1.07 compared to the zero-filling baseline in terms of PLC-MOS on the blind test set and reaches a competitive 3rd place in the challenge ranking.

<sup>†</sup> <sup>†</sup>

## 1 Introduction

Several crucial processing steps for virtual communication have immensely profited from deep learning, e.g., speech enhancement (SE) [^1] [^2] and acoustic echo cancellation (AEC) [^3] [^4]. The underlying models can be created with deep-learning tools alone or based on a combination with ”classic“ signal-processing approaches such as adaptive filters and with deep-learning models [^3] [^5]. Another important challenge is to improve communication systems with effective packet loss concealment (PLC) using deep learning. The task of PLC is to conceal or predict lost packets during packet-based transmissions. A well-performing PLC system is especially important for poor network connections, since more packets are lost or overly delayed and therefore discarded. A robust PLC system could also decrease listening fatigue and effort in situations with poor audio quality and therefore result in overall improved communication channels. PLC systems should work efficiently so they can be used for many device classes without fully utilizing the processing power and sacrificing battery run-time on mobile devices.

Packet loss concealment is a sequence problem since missing frames from an audio sequence must be predicted from past information. An early deep approach [^6] utilized feed-forward neural networks for predicting the magnitude and phase from a number of past frames using mean-squared-error based loss in time-frequency domain. Another approach is a causal sequence to sequence model such as RNNs as used for SE [^7] [^2] [^8]. In related research, RNN-based models have been applied to PLC [^9] [^10] [^11]. In [^10] a recurrent model with online adaptation is proposed by exploiting the recent past of the signal. [^9] used an LSTM-based PLC model to increase the performance of speech emotion recognition trained with a concordance correlation coefficient as cost function. A convolutional recurrent structure for time-domain PLC was introduced in [^11] trained with a mean absolute error cost in time domain. Alternative deep approaches utilizing generative adversarial networks (GAN) [^12] [^13] [^14], which were shown in the past to be able to predict speech frames.

A comparison between these studies is difficult because of the lack of a common training and test set, and therefore Microsoft proposed a deep PLC Challenge for Interspeech 2022 [^15]. The authors provided a large amount of speech data, traces of lost frames from real calls and a deep model for predicting mean opinion scores (MOS), indicating PLC performance of enhanced audio. The challenge evaluations will be performed as in previous challenges organized by Microsoft [^16] [^17] [^18] with a crowd-sourcing approach on the Amazon Mechanical Turk.

For the first time, to the best of our knowledge, we propose in the context of the PLC Challenge a time-domain sequence-to-one (seq2one) RNN model for PLC trained with a combined magnitude and complex mean absolute error (MAE) loss in time-frequency domain. In contrast to previous RNN approaches [^9] [^10] [^11], the model predicts only lost frames from a short context buffer similar as in [^6] in a non-continuous way instead of running inference for each incoming audio frame to update internal states. This seq2one approach can decrease, depending on the complexity of the model, the computational load of the host system and probably increase the battery run-time of a mobile device.

## 2 Methods

### 2.1 Deep PLC Strategy

The proposed PLC seq2one system is based on a context buffer of length $n$ that contains non-overlapping frames of length $m$. For $m$ 10 ms (160 samples at 16 kHz sampling rate) are chosen. It is therefore possible to use one look-ahead frame and still comply with the PLC-Challenge rules, which specify a maximum delay of 20 ms [^15]. The use of look-ahead frames has been shown to be beneficial in [^11] to connect predicted frames better to available audio. When no packet loss is detected, the current and the look-ahead frames are concatenated to a frame with 320 samples and subsequently hann windowed. When a packet loss is detected, the dPLC model predicts a 320 sample long frame that is windowed as well. With an overlap-add procedure the current 10 ms output frame is predicted which is time-aligned to the current input frame. The current output frame is written back to the context buffer. This procedure, especially the windowing and overlap-add, was chosen to reduce artifacts on the edges of lost packets and connect the predicted content better to the available frames and so pursues a similar goal as the cross-fading shown in [^6]. The proposed PLC system is also illustrated in Figure 1.

![PLC_system](figures/PLC_system.png)

Figure 1: Illustration of the proposed PLC system. Incoming audio is written to a context buffer. When no frame is lost, the current frame and the look-ahead frame are concatenated and hann-windowed. If the the frame on position $x$ or $x+1$ is lost, the dPLC predicts an audio frame which is also hann-windowed. The resulting windowed frames are processed by an overlap-add procedure returning the current frame $y$ time aligned to input frame $x$.

### 2.2 Model Architectures

The model is build as seq2one model predicting one time domain frame from a context buffer. The general architecture is inspired by the NSnet2 architecture [^7] and an architecture proposed in [^11]. It was adapted to seq2one task and working completely in the time domain.

First, the frames of the context buffer are processed by a fully-connected (FC) layer with relu activation that maps the time-domain frames to a non negative feature space, as has been proposed with the TasNet approach [^19] [^20] [^21]. Second, all frames are processed by another FC layer with leaky-relu activation. The resulting intermediate representation sequence is processed by two consecutive Conv1D layers with leaky relu-activation and kernel size 4 and 2, to extract local patterns from the sequence. The sequence is padded so that the resulting sequence has still the same length. The sequence is subsequently processed by two bidirectional Gated Recurrent Unit (GRU) [^22] layers, which enables the use of information about the whole sequence. The final hidden state of the second BGRU is forwarded to two FC mapping layers with leaky-relu activation. A last FC layer without activation predicts the time-domain frame. To construct a feed-forward baseline (FF-Baseline) the Conv1Ds and BGRUs layers are replaced by a flatten operation to remove the sequence dimension and 3 FC layers with 512 units and leaky-relu activation.

In total, three different size configurations are tested for the proposed tPLCnet to explore the scaling properties of the model (*Small, Medium and Large*). The number of units or filters are listed in Table 1. Additionally, Table 2 shows the number of Multiply Accumulates (MACs) and execution time for predicting one 10 ms frame on an Intel i5-7267U dual-core processor clocked at 3.1 GHz.

Table 1: Number of units/filters of each layer for the configurations *Small, Medium and Large* of the proposed deep PLC model.

<table><thead><tr><th>Layer</th><th>Small</th><th>Medium</th><th>Large</th></tr></thead><tbody><tr><td>FC encoding</td><td colspan="3">512</td></tr><tr><td>FC embedding</td><td>128</td><td>256</td><td>512</td></tr><tr><td>Conv1x4</td><td>128</td><td>256</td><td>512</td></tr><tr><td>Conv1x2</td><td>128</td><td>256</td><td>512</td></tr><tr><td>BGRU 1</td><td>64</td><td>128</td><td>256</td></tr><tr><td>BGRU 2</td><td>64</td><td>128</td><td>256</td></tr><tr><td>FC mapping 1</td><td colspan="3">512</td></tr><tr><td>FC mapping 2</td><td colspan="3">512</td></tr><tr><td>FC decoding</td><td colspan="3">320</td></tr><tr><td></td><td></td><td></td><td></td></tr></tbody></table>

### 2.3 Loss Functions

Recent studies have shown that the loss function is crucial to perceived audio quality in speech enhancement [^23], but at the same time, relatively simple loss functions are surpassing more complex ones [^24]. To quantify the effect loss functions for PLC, our study compared three loss functions, which are all applied to the whole enhanced utterance.

[^11] proposed to use a simple mean absolute error (MAE) in time domain which shown promising results.

$$
\mathrm{MAE_{time}}=|\hat{x}-x|
$$

where the loss calculated as the mean absolute difference of the clean audio $x$ and the predicted audio $\hat{x}$. Due to its definition in time domain, MAE is phase sensitive and is - in comparison to the mean squared error - less sensitive to outliers.

In [^23], it was shown that the MAE in time-frequency domain (TF-domain) produces competitive results for speech enhancement. MAE has also been explored for speech synthesis [^25], which in some aspects is related to PLC. To calculate the MAE in TF-domain, the clean and predicted utterances are subject to an STFT which results in the complex TF representations $X(t,f)$ and $\hat{X}(t,f)$. The magnitude MAE loss is given by

$$
\mathrm{MAE_{mag}}=||\hat{X}|-|X||.
$$

Results of related studies indicate that integrating a phase component in the loss function can be beneficial [^26] [^23], which can be implemented by using a complex distance. The combined TF-domain MAE loss is given by

$$
\mathrm{MAE_{comb}}=(1-\alpha)||\hat{X}|-|X||+\alpha|\hat{X}-X|,
$$

where $\alpha$ is a weighting factor for the amount of phase sensitivity. In this study, $\alpha=0.1$ is chosen, which was found to be a good trade-off between some phase sensitivity and a good magnitude reconstruction in preliminary experiments.

Table 2: Results on the known test-set in terms of PESQ \[MOS\], PLC-MOS \[MOS\] and DNS-MOS P.835. For PESQ and PLC-MOS the data is also shown for the three loss subsets low (up to 120 ms), med. (120 to 320 ms) and high (320 to 1000 ms). For DNS-MOS all three metrics are shown. Additionally the number Multiply Accumulates (MACs) and the execution time \[ms\] for one 10 ms frame are shown.

<table><thead><tr><th></th><th></th><th>exec.</th><th colspan="4">PESQ</th><th></th><th colspan="4">PLC-MOS</th><th></th><th colspan="3">DNS-MOS</th></tr></thead><tbody><tr><th>Method</th><th># MACs</th><td>Time</td><td>low</td><td>med.</td><td>high</td><td>ovr.</td><td></td><td>low</td><td>med.</td><td>high</td><td>ovr.</td><td></td><td>nSIG</td><td>nBAK</td><td>nOVR</td></tr><tr><th>Baseline</th><th></th><td></td><td>2.59</td><td>1.75</td><td>1.73</td><td>2.19</td><td></td><td>3.15</td><td>2.46</td><td>2.77</td><td>2.87</td><td></td><td>3.47</td><td>3.61</td><td>2.97</td></tr><tr><th>FF baseline</th><th>2.49 M</th><td>0.47</td><td>3.24</td><td>2.13</td><td>1.91</td><td>2.68</td><td></td><td>4.05</td><td>3.52</td><td>3.63</td><td>3.81</td><td></td><td>4.15</td><td>4.23</td><td>3.75</td></tr><tr><th><math><semantics><msub><mi>tPLCnet</mi> <mi>S</mi></msub> <annotation>\mathrm{tPLCnet_{S}}</annotation></semantics></math></th><th>2.96 M</th><td>0.57</td><td>3.28</td><td>2.14</td><td>1.97</td><td>2.71</td><td></td><td>4.09</td><td>3.57</td><td>3.72</td><td>3.86</td><td></td><td>4.14</td><td>4.23</td><td>3.74</td></tr><tr><th><math><semantics><msub><mi>tPLCnet</mi> <mi>M</mi></msub> <annotation>\mathrm{tPLCnet_{M}}</annotation></semantics></math></th><th>7.85 M</th><td>1.41</td><td>3.31</td><td>2.15</td><td>1.98</td><td>2.74</td><td></td><td>4.12</td><td>3.61</td><td>3.79</td><td>3.90</td><td></td><td>4.17</td><td>4.25</td><td>3.78</td></tr><tr><th><math><semantics><msub><mi>tPLCnet</mi> <mi>L</mi></msub> <annotation>\mathrm{tPLCnet_{L}}</annotation></semantics></math></th><th>26.18 M</th><td>3.95</td><td>3.36</td><td>2.18</td><td>1.99</td><td>2.77</td><td></td><td>4.16</td><td>3.66</td><td>3.82</td><td>3.95</td><td></td><td>4.18</td><td>4.27</td><td>3.79</td></tr><tr><th></th><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></tbody></table>

### 2.4 Datasets and Augmentation

The challenge organizers are providing a training set, a known test set and a blind test set. The training set contains around 64 h of clean speech and packet loss traces from real calls. The traces are vectors of ones and zeros indicating for each 20 ms frame/packet of an audio file if it is lost (one) or not (zero). The speech is sampled from public available podcast audio. Each utterance is around 10 s long. During training, the speech files and PLC traces are cut to 8 s with a random start and end. The order of speech files and traces are shuffled for each epoch. The traces are time-reversed with 50 % probability to further increase the variance and increase robustness. To create the degraded audio the lost segments are set to zero according to the corresponding trace. The level of the speech is sampled from a normal distribution with a mean of -26 dB and a standard deviation 10 dB.

The known test set contains around 2.7 h of clean speech, degraded speech and PLC traces. As in the training set, each file is around 10 s long. The data is divided in three subsets by the organizers depending on the maximum burst loss length of the traces. The categories are: low loss up to 120 ms (52 % of the data), medium loss from 120 to 320 ms (32 % of the data) and high loss from 320 to 1000 ms (16 % of the data).

The blind test set has the same properties, but does not contain the clean speech files. Further details on the data can be found in the challenge description [^15].

### 2.5 Training Setup

The models are trained over 200 epochs with a batch size of 16 and a learning rate of 5e-4. The learning rate is multiplied by 0.8 when the loss on the test set does not decrease for three consecutive epochs. The Adam optimizer is used in combination with a gradient norm clipping of 3. The context buffer size was set to a value of 6 as a trade-off between complexity and performance. During training, the four most recent frames of the context buffer are sampled from the degraded signal, as well as the last two frames from the clean signal. We found that this strategy improves performance compared to training on the degraded audio only. The training for the medium-size model takes around 6 h on an Nvidia RTX A5000.

### 2.6 Objective and Challenge Evaluation

The first objective metric used is the wide band perceptual evaluation of speech quality (PESQ) [^27], which was originally built to evaluate the quality of transmitted speech. The second one is DNS-MOS P.835 [^28] which is a single-ended/blind measure based on a deep-learning approach for estimating Mean Opinions Scores (MOS) of speech quality (nSIG), background noise quality (nBAK) and an overall quality (nOVR). DNS-MOS was trained with ratings from previous deep-noise suppression challenges organized by Microsoft [^18]. The last measure PLC-MOS [^15] is provided by the challenge organizers. PLC-MOS utilizes a similar approach as DNS-MOS but can be used as double-ended or single-ended measure. It predicts MOS scores indicating the quality of the PLC system.

The challenge organizers evaluate the improved audio created from blind test with four metrics: Double-ended PLC-MOS, second, the DNS-MOS P.808 [^29], which returns an overall quality rating. Third, a crowd-sourced Comparison Category Rating (CCR MOS) is used, for which the participants are asked to rate the enhanced audio compared to the clean reference. This evaluation is run on the Amazon Mechanical Turk. Fourth, the word accuracy calculated by the Microsoft Azure cognitive services speech recognition is used. The final score is calculated from CCR MOS and word accuracy.

## 3 Experiments and Results

In the following the experiments and results are described:  
Objective results on complexity comparison: Table 2 shows the objective results for the zero filling baseline, the feed-forward baseline trained on the same setup, as well as three complexity configurations of the tPLCnet (cf. Table 1). The FF baseline already reaches a good performance increase for all metrics. Performance increases with model size for all metrics. The total improvement in terms of PLC-MOS for $\mathrm{tPLCnet_{Large}}$ is 1.08. The PESQ improvement over the zero filling baseline is 0.58 and for DNS-MOS nOVR 0.82. The PESQ and PLC-MOS improvements are constant over all subsets.  
Objective results on loss functions and loss function configurations: We compared $\mathrm{MAE_{t}ime}$, $\mathrm{MAE_{m}ag}$ and $\mathrm{MAE_{c}omb}$; for the latter, three different window sizes with 50 % overlap were tested to identify an optimal configuration for the PLC task. All results were acquired with $\mathrm{tPLCnet_{Medium}}$. The results are shown in Table 3. The lowest performance in all metrics is achieved with the time-domain $\mathrm{MAE_{t}ime}$ loss. The highest PESQ (2.76) and DNS-MOS (3.85) values are reached with $\mathrm{MAE_{c}omb}$ loss with 20 ms window size. The highest PLC loss (3.90) is achieved with $\mathrm{MAE_{c}omb}$ and 32 ms window size.

Table 3: Objective scores for different loss functions. For DNS-MOS, only nOVR is shown.

|  |  | PLC- | DNS- |
| --- | --- | --- | --- |
| loss | PESQ | MOS | MOS |
| $\mathrm{MAE_{time}}$ | 2.43 | 3.30 | 3.54 |
| $\mathrm{MAE_{mag}}$ (32 ms, 50%) | 2.75 | 3.88 | 3.79 |
| $\mathrm{MAE_{comb}}$ (64 ms, 50%) | 2.61 | 3.53 | 3.66 |
| $\mathrm{MAE_{comb}}$ (32 ms, 50%) | 2.73 | 3.90 | 3.78 |
| $\mathrm{MAE_{comb}}$ (20 ms, 50%) | 2.76 | 3.71 | 3.85 |
|  |  |  |  |

Comparison of context buffer lengths: The length of the context buffer is a major factor for complexity in terms of operations for our seq2one model, since the whole buffer must be processed each time by the convolutional and the BGRU layers. Hence, we explore the effect of different buffer lengths on performance. Figure 2 shows the performance in terms of PLC-MOS and DNS-MOS against the buffer length. The optimal lengths for PLC-MOS and DNS-MOS are 7 and 6, respectively, while the lowest performance is reached with 20 frames (PLC-MOS) or 15 frames (DNS-MOS).

![buffer_len_emb](figures/buffer_len_emb.png)

Figure 2: Performance in terms of PLC-MOS and OVR DNS-MOS P.835 versus the number of 10 ms frames in the context buffer length.

Results of the challenge evaluations: The challenge results for the zero-filling baseline and all approaches submitted to the challenge are shown in Table 4. $\mathrm{tPLCnet_{Large}}$ with $\mathrm{MAE_{comb}}$ using a loss window length of 32 ms ranked 3rd in the challenge. It improves on all metrics except for word accuracy. The 1st and 2nd ranked entries improve on all metrics (including word accuracy). Our tPLCnet achieves the second-best score in terms of PLC-MOS.

Table 4: 2022 INTERSPEECH Audio Deep PLC Challenge Results. Teams marked as ”tied”: Difference not significant ($p\geq 0.05$).

|  | PLC- | DNS- | CCR- | Word | Final |
| --- | --- | --- | --- | --- | --- |
| Rank | MOS | MOS | MOS | acc. | score |
| 7 | 2.896 | 3.474 | \-1.309 | 0.860 | 0.712 |
| Baseline | 2.904 | 3.444 | \-1.231 | 0.861 | 0.725 |
| 6 | 3.478 | 3.738 | \-1.042 | 0.825 | 0.739 |
| 5 | 3.277 | 3.513 | \-1.102 | 0.863 | 0.748 |
| 3 (tied) (ours) | 3.976 | 3.688 | \-0.838 | 0.859 | 0.790 |
| 3 (tied) | 3.829 | 3.684 | \-0.812 | 0.868 | 0.798 |
| 2nd | 3.744 | 3.788 | \-0.638 | 0.882 | 0.835 |
| 1st | 4.282 | 3.797 | \-0.552 | 0.875 | 0.845 |
|  |  |  |  |  |  |

## 4 Discussion

In the following some aspects of the results are discussed. While an increase in complexity of tPLCnet also results in a performance increase, the gain seems to saturate compared to the negative aspects of increased complexity. The FF baseline already produces a robust PLC performance, indicating that a large portion of the performance comes from our general approach in combination with the training setup. This implies that for real on-device applications the PLC model can be chosen reasonable depending on the available resources and it must not be the largest possible model. In [^8] a similar saturation was found for NSNET2 architecture for SE, i.e., a larger amount of RNN units heavily increases the complexity, but only slightly increases the noise reduction performance.

Regarding the comparison of loss functions, the spectral MAE emerged as the best choice, with the time-domain MAE achieving clearly lower scores. The magnitude-only loss reaches comparable performance to the combined version which is in line with observations in [^23]. Interestingly, the highest PLC-MOS is observed for a window size of 32 ms, while the best choice for other metrics was a value of 20 ms. Also, the higher spectral resolution achieved with the 64 ms window seems not to be helpful for PLC.

The evaluation of the length of the context buffer shows that a short context buffer with only 4 frames already reaches a good PLC performance while very long context buffers even seem detrimental. A similar effect for longer input buffers was observed in [^6]. This suggests that the main information required for robust PLC is temporally localized around the lost frame and long-term dependencies only weakly influence overall performance. However, the observed performance differences between the context buffer lengths are not very large, which also means a short buffer length can be chosen without sacrificing performance.

One observation from the challenge result is that a high PLC-MOS does not necessarily result in a high CCR-MOS. Our model reached a higher PLC-MOS than the 2nd place, but the the 2nd ranked model reached a significantly better result in the crowd-sourced CCR-MOS. We assume this can be caused by addtional speech enhancement used by the 2nd-ranked model, which modifies the spectrum such that PLC-MOS is decreased but perceived audio quality is increased. Word accuracies for the baseline and the tPLCnet are very close to each other (0.861 and 0.859, respectively), i.e., the PLC improvement perceived by the raters does not help the speech recognition system. We assume this is due to a slight deterioration of clean speech in the vicinity of the edges of lost frames, since our algorithm smooths the transition between these areas. It also seems that the speech recognition system used by challenge organizers can already handle missing packets relatively well.

## 5 Conclusions

This study introduced tPLCnet, a straightforward real-time approach for predicting lost packets from a short context buffer in the time-domain. It achieves state-of-the-art performance and ranks 3rd in the deep PLC Challenge. The training was performed with open-source data which resulted in a robust and reproducible approach which can be easily applied in the real-world.

## 6 Acknowledgements

This work was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) under Germany’s Excellence Strategy – EXC 2177/1 - Project ID 390895286 and by - Project-ID 352015383 - SFB 1330.

[^1]: J.-M. Valin, U. Isik, N. Phansalkar, R. Giri, K. Helwani, and A. Krishnaswamy, “A Perceptually-Motivated Approach for Low-Complexity, Real-Time Enhancement of Fullband Speech,” in *Proc. Interspeech 2020*, 2020, pp. 2482–2486.

[^2]: N. L. Westhausen and B. T. Meyer, “Dual-Signal Transformation LSTM Network for Real-Time Noise Suppression,” in *Proc. Interspeech 2020*, 2020, pp. 2477–2481.

[^3]: J.-M. Valin, S. Tenneti, K. Helwani, U. Isik, and A. Krishnaswamy, “Low-complexity, real-time joint neural echo control and speech enhancement based on percepnet,” in *ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2021, pp. 7133–7137.

[^4]: N. L. Westhausen and B. T. Meyer, “Acoustic echo cancellation with the dual-signal transformation lstm network,” in *ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2021, pp. 7138–7142.

[^5]: M. M. Halimeh, T. Haubner, A. Briegleb, A. Schmidt, and W. Kellermann, “Combining adaptive filtering and complex-valued deep postfiltering for acoustic echo cancellation,” in *ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2021, pp. 121–125.

[^6]: B.-K. Lee and J.-H. Chang, “Packet loss concealment based on deep neural networks for digital speech transmission,” *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, vol. 24, no. 2, pp. 378–387, 2016.

[^7]: S. Braun and I. Tashev, “Data augmentation and loss normalization for deep noise suppression,” in *Speech and Computer*, A. Karpov and R. Potapova, Eds. Cham: Springer International Publishing, 2020, pp. 79–86.

[^8]: S. Braun, H. Gamper, C. K. Reddy, and I. Tashev, “Towards efficient models for real-time deep noise suppression,” in *ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2021, pp. 656–660.

[^9]: M. M. Mohamed and B. W. Schuller, “Concealnet: An end-to-end neural network for packet loss concealment in deep speech emotion recognition,” *arXiv preprint arXiv:2005.07777*, 2020.

[^10]: R. Lotfidereshgi and P. Gournay, “Speech prediction using an adaptive recurrent neural network with application to packet loss concealment,” in *2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2018, pp. 5394–5398.

[^11]: J. Lin, Y. Wang, K. Kalgaonkar, G. Keren, D. Zhang, and C. Fuegen, “A time-domain convolutional recurrent network for packet loss concealment,” in *ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2021, pp. 7148–7152.

[^12]: J. Wang, Y. Guan, C. Zheng, R. Peng, and X. Li, “A temporal-spectral generative adversarial network based end-to-end packet loss concealment for wideband speech transmission,” *The Journal of the Acoustical Society of America*, vol. 150, no. 4, pp. 2577–2588, 2021. \[Online\]. Available: [https://doi.org/10.1121/10.0006528](https://doi.org/10.1121/10.0006528)

[^13]: H. Zhou, Z. Liu, X. Xu, P. Luo, and X. Wang, “Vision-infused deep audio inpainting,” in *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, October 2019.

[^14]: Y. Shi, N. Zheng, Y. Kang, and W. Rong, “Speech loss compensation by generative adversarial networks,” in *2019 Asia-Pacific Signal and Information Processing Association Annual Summit and Conference (APSIPA ASC)*, 2019, pp. 347–351.

[^15]: L. Diener, S. Sootla, S. Branets, A. Saabas, R. Aichner, and R. Cutler, “Interspeech 2022 audio deep packet loss concealment challenge,” in *INTERSPEECH 2022 - 23rd Annual Conference of the International Speech Communication Association*, 2022 (submitted).

[^16]: C. K. Reddy, V. Gopal, R. Cutler, E. Beyrami, R. Cheng, H. Dubey, S. Matusevych, R. Aichner, A. Aazami, S. Braun, P. Rana, S. Srinivasan, and J. Gehrke, “The INTERSPEECH 2020 Deep Noise Suppression Challenge: Datasets, Subjective Testing Framework, and Challenge Results,” in *Proc. Interspeech 2020*, 2020, pp. 2492–2496.

[^17]: K. Sridhar, R. Cutler, A. Saabas, T. Parnamaa, M. Loide, H. Gamper, S. Braun, R. Aichner, and S. Srinivasan, “Icassp 2021 acoustic echo cancellation challenge: Datasets, testing framework, and results,” in *ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2021, pp. 151–155.

[^18]: Z. Xu, M. Strake, and T. Fingscheidt, “Deep Noise Suppression with Non-Intrusive PESQNet Supervision Enabling the Use of Real Training Data,” in *Proc. Interspeech 2021*, 2021, pp. 2806–2810.

[^19]: Y. Luo and N. Mesgarani, “Tasnet: Time-domain audio separation network for real-time, single-channel speech separation,” in *2018 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2018, pp. 696–700.

[^20]: ——, “Conv-tasnet: Surpassing ideal time–frequency magnitude masking for speech separation,” *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, vol. 27, no. 8, pp. 1256–1266, 2019.

[^21]: C. Li, Y. Luo, C. Han, J. Li, T. Yoshioka, T. Zhou, M. Delcroix, K. Kinoshita, C. Boeddeker, Y. Qian, S. Watanabe, and Z. Chen, “Dual-path rnn for long recording speech separation,” in *2021 IEEE Spoken Language Technology Workshop (SLT)*, 2021, pp. 865–872.

[^22]: J. Chung, C. Gulcehre, K. Cho, and Y. Bengio, “Empirical evaluation of gated recurrent neural networks on sequence modeling,” *arXiv preprint arXiv:1412.3555*, 2014.

[^23]: S. Braun and I. Tashev, “A consolidated view of loss functions for supervised deep learning-based speech enhancement,” in *2021 44th International Conference on Telecommunications and Signal Processing (TSP)*, 2021, pp. 72–76.

[^24]: S. Braun and H. Gamper, “Effect of noise suppression losses on speech distortion and asr performance,” *arXiv preprint arXiv:2111.11606*, 2021.

[^25]: Y. Wang, R. Skerry-Ryan, D. Stanton, Y. Wu, R. J. Weiss, N. Jaitly, Z. Yang, Y. Xiao, Z. Chen, S. Bengio, Q. Le, Y. Agiomyrgiannakis, R. Clark, and R. A. Saurous, “Tacotron: Towards End-to-End Speech Synthesis,” in *Proc. Interspeech 2017*, 2017, pp. 4006–4010.

[^26]: B. Patton, J. Skoglund, J. Thorpe, J. Hershey, K. Wilson, M. Chinen, R. F. Lyon, and R. A. Saurous, “Exploring tradeoffs in models for low-latency speech enhancement,” in *Proceedings of the 16th International Workshop on Acoustic Signal Enhancement*, 2018.

[^27]: “ITU-T P.862: Perceptual evaluation of speech quality (PESQ): An objective method for end-to-end speech quality assessment of narrow-band telephone networks and speech codecs.” 2001.

[^28]: C. K. Reddy, V. Gopal, and R. Cutler, “Dnsmos p.835: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors,” in *ICASSP*, 2022.

[^29]: C. K. A. Reddy, V. Gopal, and R. Cutler, “Dnsmos: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors,” in *ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2021, pp. 6493–6497.