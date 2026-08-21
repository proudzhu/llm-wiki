Yufeng Yang <sup>1,2∗</sup>, Yiteng Huang <sup>2</sup>, Yong Xu <sup>2</sup>, Li Wan <sup>2</sup>, Suwon Shon <sup>2</sup>, Yang Liu <sup>2</sup>, Yifeng Fan <sup>2</sup>, Zhaojun Yang <sup>2</sup>, Olivier Siohan <sup>2</sup>, Yue Liu <sup>2</sup>, Ming Sun <sup>2</sup>, Florian Metze <sup>2</sup> Thanks: \*Work done during internship at Meta

###### Abstract

With the growing adoption of wearable devices such as smart glasses for AI assistants, wearer speech recognition (WSR) is becoming increasingly critical to next-generation human-computer interfaces. However, in real environments, interference from side-talk speech remains a significant challenge to WSR and may cause accumulated errors for downstream tasks such as natural language processing. In this work, we introduce a novel multi-channel differential automatic speech recognition (ASR) method for robust WSR on smart glasses. The proposed system takes differential inputs from different frontends that complement each other to improve the robustness of WSR, including a beamformer, microphone selection, and a lightweight side-talk detection model. Evaluations on both simulated and real datasets demonstrate that the proposed system outperforms the traditional approach, achieving up to an 18.0% relative reduction in word error rate.

<sup>†</sup>

## 1 Introduction

Automatic speech recognition (ASR) systems have seen remarkable progress in recent years, driven by advances in deep learning and end-to-end (E2E) neural network architectures [^1] [^2] [^3]. Despite these advancements, wearer speech recognition (WSR) on wearable devices such as smart glasses remains underexplored. As a critical part of an emerging next-generation human-computer interface [^4] [^5], WSR on smart glasses requires microphones to remain active for long and continuous interactions. Unlike traditional close-talk systems, microphones on smart glasses operate in open-field conditions, making WSR particularly vulnerable to bystander side-talk in real environments. Improving WSR robustness is essential to ensure a reliable user experience on smart glasses and other wearable devices.

Smart glasses are equipped with multiple microphones, enabling the integration of a beamformer in an ASR system for smart glasses. Non-linearly constrained minimum variance (NLCMV) beamforming [^6] was proposed for smart glasses, which incorporates white noise gain and null direction control, to project multi-channel microphone inputs into predefined directions. This technique was adopted in several subsequent studies [^7] [^8] [^9] [^10] [^11] [^12] [^13] for conversational ASR on smart glasses. However, when only recognizing the wearer in the presence of a bystander, the traditional approach cannot fully suppress the degradation caused by the side-talk in WSR.

Traditional frontends such as speech enhancement [^14] and talker-independent speaker separation [^15] can effectively improve the speech intelligibility and quality. However, even with causal models, the added latency by integrating such models makes it impractical for real applications. Other frontend methods, such as speaker diarization [^16] and target speaker extraction [^17], have the same problem. Moreover, the application of WSR on smart glasses constrains frontend design, since modeling speaker information may raise privacy concerns. Consequently, a new ASR system design is required to improve WSR performance on smart glasses.

In this work, we propose multi-channel differential ASR, a novel method that takes inputs from different frontends that complement each other, for robust WSR on smart glasses. Unlike the traditional approach, we incorporate frontends alongside a beamformer to provide complementary spatial cues for the ASR model. We utilize microphone selection to choose the channel with the highest signal-to-noise ratio (SNR), thereby minimizing additional latency. We also integrate a lightweight streaming side-talk detection (STD) model to distinguish between the wearer and bystander without modeling speaker identity. For the beamformer, we utilize an adjusted minimum variance distortionless response (MVDR) beamformer. The ASR backbone is based on a low-latency streaming recurrent neural network transducer (RNN-T) network [^18]. Evaluations on both simulated and real recorded datasets demonstrate that combining microphone selection, beamforming, and STD outperforms the traditional approach that relies solely on beamforming as the frontend, with up to 18.0% relative reduction in word error rate (WER).

We make several contributions to the field. We propose a novel multi-channel differential ASR for robust WSR. With a careful design, the outputs from different frontends with different frame rates can be combined. We also create a real recorded dataset to analyze the WSR performance for different bystander angles, distances, and heights. The proposed differential ASR system has the potential to be extended to other ASR applications as well.

## 2 Proposed Method

![[raw/papers/yang-2025-mc-differential-asr-smart-glasses/figures/fig1.png|Refer to caption]]

Figure 1: Diagram of the proposed multi-channel differential ASR system for robust WSR on smart glasses.

### 2.1 Microphone Array Beamforming

Microphone array beamforming is a spatial filtering technique in speech processing that leverages a microphone array to enhance the speech signal from desired directions while suppressing noise and interference from other spatial locations [^19] [^20]. The technique works by applying filter weights to signals from multiple microphones, effectively steering the array’s sensitivity toward the target speech source while suppressing unwanted acoustic sources. Traditional beamforming approaches include delay-and-sum beamforming, MVDR beamforming, and others [^19] [^20] [^21]. For smart glasses, NLCMV beamformer [^6] has shown good performance on ASR. In this work, we adopt an internal MVDR-based beamformer that directs the beam to the wearer’s mouth. This beamformer is more suitable for WSR than NLCMV because it focuses solely on the wearer.

### 2.2 RNN-T Based Streaming ASR

For wearable devices such as smart glasses, a low-latency streaming ASR model is essential to ensure continuous transcription throughout extended usage sessions. The RNN-T model [^18] is particularly well suited for this task, as it enables fully streaming, E2E processing with three integrated components: an acoustic encoder that extracts features from audio input, a prediction network that functions like an internal language model, and a joint network that merges their outputs to generate predictions. In this work, we build our RNN-T on the Emformer [^22] architecture, which features an efficient memory Transformer designed for low-latency streaming ASR.

### 2.3 Side-Talk Detection

STD is a novel task for WSR on smart glasses. It distinguishes between wearer and bystander speech without modeling speaker identity, thereby protecting privacy. The task was introduced in [^23] to build a Whisper [^24] model robust to side-talk speech. In this work, we design a streaming STD model that operates at the audio sample level and outputs logit scores indicating voice activity from the wearer, bystander, or non-speech segments. The STD model is based on a temporal convolutional network (TCN) [^25], and is lightweight, with approximately 2M parameters.

### 2.4 Multi-Channel Differential ASR

We propose multi-channel differential ASR, a novel ASR system designed to improve the robustness of WSR to side-talk. Unlike the traditional approach, where the ASR model relies solely on a beamformer as the frontend to process multi-channel microphone inputs, differential ASR leverages different frontend modules that provide complementary or contrastive information to each other. The diagram of the proposed differential ASR is shown in Fig. 1.

In the proposed differential ASR system, we adopt a microphone selection module, a beamformer, and an STD model. The microphone selection module chooses the channel with the highest SNR from the input microphone array. The selection is fixed and based on the microphones’ physical location relative to the wearer’s mouth. Given a pair of smart glasses, the closest microphone to the wearer’s mouth will be selected. Thus, we denote the output of the microphone selection as ch-0. For the beamformer, the internal modified MVDR beamformer is utilized, which takes all microphone signals as input and generates a single-channel beamformed audio as output, which we denote as ch-x. Based on the STD model logits, we generate an embedding (denoted as embed), which is concatenated with the log-Mel feature of ch-0 and ch-x as input to the RNN-T model. All frontends are frozen, so the number of additional trainable parameters remains under 1M compared to the traditional system.

## 3 Experimental Setup

![[raw/papers/yang-2025-mc-differential-asr-smart-glasses/figures/fig2.png|Refer to caption]]

Figure 2: Microphone location on a pair of smart glasses.

### 3.1 Datasets

We designed a setup to evaluate the performance of robust WSR on smart glasses. The experiments are based on the LibriSpeech [^26] dataset. We first simulate multi-channel LibriSpeech using room impulse responses (RIRs) measured on a pair of Ray-Ban Meta smart glasses. The microphone location of the smart glasses is shown in Fig 2. There are 5 microphones in total, with one near the nose and two pairs of microphones on the front and mid temples. We prepare two categories of datasets: wearer-only (clean) and wearer with side-talk (noisy). The clean data does not contain noise or side-talk speech. For the simulated noisy data, side-talk speech from a bystander is added as noise, with wearer-to-bystander SNRs ranging from 10 to 25 dB. We prepare a clean training set and a noisy training set with 500554 utterances each. The wearer and bystander speech are sourced from all LibriSpeech training sets. In each wearer and bystander mixture, bystander speech is randomly sampled other than the wearer speech, and added to the wearer speech with a random overlap ratio from 0% to 100%. Validation data is clean only, sourced from all LibriSpeech validation sets with 6747 utterances. For simulated evaluation, we test on both clean and noisy test-clean and test-other sets, with 3558 and 3502 utterances, respectively. In each noisy test set, two overlap ratios of 0% and 50% are utilized.

To evaluate the WSR performance in real environments, we set up a head and torso simulator (HATS) and loudspeakers to collect a real dataset for evaluation. A pair of Ray-Ban Meta smart glasses is mounted on the HATS to capture multi-channel data. The wearer’s speech is played back via the HATS mouth simulator, and the bystander speech is played from loudspeakers placed around the HATS, as shown in Fig. 3. The bystander loudspeaker covers 72 distinct locations, including 8 different angles of {0, 45, 90, 135, 180, 225, 270, 315} degrees to the HATS, 3 different relative heights of {-0.5, 0.0, 0.5} m to the wearer, and 3 different distances of {0.5, 1.0, 2.0} m to the wearer. The wearer and bystander speech are sourced from test-clean and test-other sets, respectively. The wearer and side-talk speech are recorded separately and mixed during post-processing. The mixing process follows the same procedure as for the simulated test data. On real data, we distinguish the order of the first speaker. Either the wearer speaks first (wearer-bystander) or the bystander speaks first (bystander-wearer). For each speaker order and overlap ratio, the resulting evaluation set has 188640 utterances for all 72 bystander locations.

![[raw/papers/yang-2025-mc-differential-asr-smart-glasses/figures/fig3.png|Refer to caption]]

Figure 3: Recording setup for data collection with HATS.

### 3.2 Implementation Details

Based on the physical locations of the microphones on the smart glasses, the nose microphone is closest to the wearer’s mouth, and is selected as ch-0 in the microphone selection module. The beamformer takes in all 5-ch inputs and generates a 1-ch beamformed audio. The STD model is trained on real non-user data and produces logits for the wearer at the audio sample level. As shown in Fig. 1, only uncolored modules are trainable and all frontends are frozen.

The feature extraction module extracts an 80-dimensional log-Mel feature when only ch-x is fed as input. When ch-x is coupled with ch-0, the feature extraction module concatenates their log-Mel features and uses two streaming 2D convolutional layers (Conv2D) with a kernel size of \[2, 5\], a stride of \[1, 2\], and a gated linear unit (GLU) activation function. The log-Mel feature of each channel is halved in dimension, then concatenated as the output of the feature extraction module. The embedding generation module contains two Conv2D layers with a kernel size of \[20, 1\] and a stride of \[10, 1\] and \[16, 1\] for each layer, respectively. After this processing, the frame rate matches the output of the feature extraction module. The intermediate number of channels is 3, and the final embedding dimension is 5. Afterwards, the extracted ch-x and ch-0 features and embed are concatenated and fed to the RNN-T model. All Conv2D layers in the feature extraction and embedding generation module are followed by a 2D batch normalization layer.

The RNN-T model first reduces the input frame size by 6. Then, 20 layers of Emformer are configured with an input dimension of 320, number of heads of 4, feedforward dimension of 2048, context of 10 past frames, segment size of 2, activation function of Gaussian error linear unit (GELU), and a convolutional kernel of \[7, 0\] with Swish activation. The encoder output dimension is 768. The output units are 4096 sentence pieces [^27] with byte pair encoding (BPE) [^28] as the segmentation algorithm. In the predictor, the tokens are first represented by 256-dimensional embeddings and processed by two long short-term memory (LSTM) layers with 256 hidden nodes, followed by a linear projection to a 768-dimensional feature. The joint network projects the input to the number of sentence pieces.

We built five systems for comparison. Following the traditional approach, we only take the beamformer as the frontend and use ch-x for ASR to serve as our baselines. Two baselines are trained, one on clean data and the other on noisy data, denoted by clean-trained ch-x and noisy-trained ch-x, respectively. For the proposed differential ASR system, we try different combinations of ch-x, ch-0, and embed, and denote them as ch-x + embed, ch-x + ch-0, and ch-x + ch-0 + embed, respectively representing the system leveraging beamformer and STD model, beamformer and microphone selection, and all three frontends. All differential ASR systems are trained on the noisy data since side-talk resistance is our main focus. For all five systems, the trainable parameters are $\sim$ 70M with a 120 ms ASR latency. All models are trained on 32 NVIDIA H100 GPUs with a batch size of 3600. The Adam optimizer was used with betas of (0.9, 0.98), epsilon of 1 $e^{-8}$, and weight decay of 1 $e^{-6}$. A tri-stage learning rate schedule was used with a peak learning rate of 0.0005, warmed up for 20k steps. The models are trained with the RNN-T loss, and the final checkpoint is selected based on the validation WER.

## 4 Results and Discussion

Table 1: ASR (%WER) results on the simulated multi-channel LibriSpeech test set.

<table><tbody><tr><td rowspan="2">System</td><td colspan="3">Wearer-only</td><td colspan="5">Wearer with Side-talk</td></tr><tr><td>test-clean</td><td>test-other</td><td>Avg</td><td colspan="2">test-clean</td><td colspan="2">test-other</td><td>Avg</td></tr><tr><td>OVERLAP RATIO</td><td>-</td><td>-</td><td>-</td><td>0%</td><td>50%</td><td>0%</td><td>50%</td><td>-</td></tr><tr><td>Clean-trained ch-x</td><td>5.70</td><td>14.75</td><td>10.23</td><td>88.62</td><td>46.07</td><td>89.75</td><td>51.23</td><td>68.92</td></tr><tr><td>Noisy-trained ch-x</td><td>6.46</td><td>16.48</td><td>11.68</td><td>6.37</td><td>6.63</td><td>16.72</td><td>17.42</td><td>11.79</td></tr><tr><td>Noisy-trained ch-x + embed</td><td>6.06</td><td>15.99</td><td>11.14</td><td>5.98</td><td>6.20</td><td>16.01</td><td>16.57</td><td>11.19</td></tr><tr><td>Noisy-trained ch-x + ch-0</td><td>6.21</td><td>16.30</td><td>11.39</td><td>6.07</td><td>6.46</td><td>16.34</td><td>16.96</td><td>11.46</td></tr><tr><td>Noisy-trained ch-x + ch-0 + embed</td><td>6.07</td><td>16.08</td><td>11.21</td><td>6.03</td><td>6.21</td><td>16.11</td><td>16.78</td><td>11.28</td></tr></tbody></table>

Table 2: ASR (%WER) results on the real recorded multi-channel LibriSpeech test set.

<table><tbody><tr><td rowspan="2">System</td><td rowspan="2">Wearer-only</td><td colspan="5">Wearer with Side-talk</td></tr><tr><td colspan="2">wearer-bystander</td><td colspan="2">bystander-wearer</td><td>Avg</td></tr><tr><td>OVERLAP RATIO</td><td>-</td><td>0%</td><td>50%</td><td>0%</td><td>50%</td><td>-</td></tr><tr><td>Clean-trained ch-x</td><td>6.30</td><td>29.20</td><td>15.28</td><td>40.96</td><td>23.81</td><td>27.31</td></tr><tr><td>Noisy-trained ch-x</td><td>7.20</td><td>7.19</td><td>7.41</td><td>7.22</td><td>7.63</td><td>7.36</td></tr><tr><td>Noisy-trained ch-x + embed</td><td>6.82</td><td>6.79</td><td>7.02</td><td>6.85</td><td>7.06</td><td>6.93</td></tr><tr><td>Noisy-trained ch-x + ch-0</td><td>6.51</td><td>6.50</td><td>6.57</td><td>6.38</td><td>6.50</td><td>6.49</td></tr><tr><td>Noisy-trained ch-x + ch-0 + embed</td><td>6.29</td><td>6.28</td><td>6.37</td><td>6.30</td><td>6.26</td><td>6.30</td></tr></tbody></table>

### 4.1 Results on Simulated Data

Evaluation results on simulated data are presented in Table 1. We compare five systems on different test data. Clean-trained ch-x and noisy-trained ch-x serve as our baselines, and different combinations of ch-0 and embed with ch-x are investigated. The clean-trained ch-x performs the best on all clean test sets with 10.23% WER on average, because of the matched training condition. All proposed systems outperform the noisy-trained ch-x. When evaluating on the noisy data, the performance of the clean-trained ch-x degrades significantly due to the side-talk speech. The noisy-trained ch-x outperforms the clean-trained ch-x with an 82.8% relative WER reduction (WERR) on average, which shows the importance of training data augmentation. Trained on the same data, the proposed systems outperform noisy-trained ch-x, and the best results come from ch-x + embed, with 5.1% relative WERR. The results highlight the effectiveness of both data augmentation and the differential ASR system compared to the traditional approach.

### 4.2 Results on Real Recorded Data

Table 2 shows the WER comparison on the real data. For noisy test data, we present the average WER across all 72 bystander heights, angles, and distances. On clean data, clean-trained ch-x achieves 6.30% WER, which is expected to perform the best. However, the proposed system ch-x + ch-0 + embed achieves a comparable 6.29% WER, demonstrating that even trained on noisy data, the differential ASR system can perform even better than the clean-trained model on clean data, showing the effectiveness of the proposed system. All proposed systems outperform noisy-trained ch-x. On noisy test data, clean-trained ch-x has a lower WER compared with that on simulated noisy data. The noisy-trained ch-x outperforms the clean-trained ch-x with a 73.1% relative WERR on average. All proposed systems outperform noisy-trained ch-x, and we notice ch-x + ch-0 + embed outperforms ch-x + ch-0, which outperforms ch-x + embed. This result suggests that for the RNN-T model, embed contains complementary information to ch-x, and so does ch-0. Moreover, ch-x + ch-0 outperforms ch-x + embed by 6.3% relatively on side-talk data, indicating ch-0 contains more differential information than embed to ch-x. Lastly, by combining all three inputs, the system’s performance is further elevated, showing that ch-0 and embed have contrastive information to each other. On average, our best system outperforms the strong noisy-trained ch-x baseline with an average 14.4% relative WERR, reaching up to 18.0%. The improvement is larger than that on simulated data because real data matches the training condition of the STD model. It is worth noting that, in Table 1 and 2, on noisy data with 0% overlap, some WERs are lower than those on clean data, which is due to their matched train–test conditions.

![[raw/papers/yang-2025-mc-differential-asr-smart-glasses/figures/fig4.png|Refer to caption]]

Figure 4: WER comparison on real data for different bystander angles on: (A) wearer-bystander 0% overlap; (B) wearer-bystander 50% overlap; (C) bystander-wearer 0% overlap; (D) bystander-wearer 50% overlap. All systems are trained on noisy data.

To better understand the model’s performance from different angles, we visualize the average WER across all bystander distances and heights on different angles in the noisy test data in Fig. 4. In each plot, we compare four ASR systems in 8 different angles with WER ranging in \[6.0%, 8.0%\], denoted by distinct colors. With 0% overlap, the WERs from different angles are relatively stable. However, with 50% overlap, WERs of angle 270 <sup>∘</sup>, 315 <sup>∘</sup>, and 0 <sup>∘</sup> of wearer-bystander are higher than other angles, and for bystander-wearer, 225 <sup>∘</sup> is also challenging for all systems. This finding suggests a new direction for beamformer design to reduce the performance gap between different bystander angles.

## 5 Concluding Remarks

In this work, we focus on the challenging side-talk problem in ASR for robust WSR on smart glasses, and propose differential ASR, a novel design that leverages different frontends that complement each other. We record a real dataset with HATS and loudspeakers to evaluate the proposed systems. Our best system utilizes beamforming, microphone selection, and an STD model. Through this integration, the proposed system outperforms a strong baseline with up to 18.0% relative WERR, demonstrating the effectiveness of the proposed system. The concept of differential ASR can be extended to other ASR tasks with different frontends. Future work includes improving the STD model against noise and additional bystanders, deploying the proposed system on devices, and developing a frontend to better handle challenging angles for robust WSR.

[^1]: Geoffrey Hinton, Li Deng, Dong Yu, George E Dahl, Abdel-rahman Mohamed, Navdeep Jaitly, Andrew Senior, Vincent Vanhoucke, Patrick Nguyen, Tara N Sainath, et al., “Deep neural networks for acoustic modeling in speech recognition: The shared views of four research groups,” IEEE Signal Process. Mag., vol. 29, pp. 82–97, 2012.

[^2]: Yann LeCun, Yoshua Bengio, and Geoffrey Hinton, “Deep learning,” Nature, vol. 521, no. 7553, pp. 436–444, 2015.

[^3]: Rohit Prabhavalkar, Takaaki Hori, Tara N Sainath, Ralf Schlüter, and Shinji Watanabe, “End-to-end speech recognition: A survey,” IEEE/ACM Trans. Audio, Speech, Language Process., vol. 32, pp. 325–351, 2023.

[^4]: Lik-Hang Lee and Pan Hui, “Interaction methods for smart glasses: A survey,” IEEE Access, vol. 6, pp. 28712–28732, 2018.

[^5]: Jakob Engel, Kiran Somasundaram, Michael Goesele, Albert Sun, Alexander Gamino, Andrew Turner, Arjang Talattof, Arnie Yuan, Bilal Souti, Brighid Meredith, et al., “Project Aria: A new tool for egocentric multi-modal AI research,” arXiv preprint arXiv:2308.13561, 2023.

[^6]: Ju Lin, Niko Moritz, Yiteng Huang, Ruiming Xie, Ming Sun, Christian Fuegen, and Frank Seide, “AGADIR: Towards array-geometry agnostic directional speech recognition,” in Proc. IEEE ICASSP, 2024, pp. 11951–11955.

[^7]: Katerina Zmolikova, Simone Merello, Kaustubh Kalgaonkar, Ju Lin, Niko Moritz, Pingchuan Ma, Ming Sun, Honglie Chen, Antoine Saliou, Stavros Petridis, Christian Fuegen, and Michael Mandel, “The CHiME-8 MMCSG Challenge: Multi-modal conversations in smart glasses,” in Proc. CHiME-8, 2024, pp. 7–12.

[^8]: Tiantian Feng, Ju Lin, Yiteng Huang, Weipeng He, Kaustubh Kalgaonkar, Niko Moritz, Li Wan, Xin Lei, Ming Sun, and Frank Seide, “Directional source separation for robust speech recognition on smart glasses,” in Proc. IEEE ICASSP, 2025, pp. 1–5.

[^9]: Yufeng Yang, Desh Raj, Ju Lin, Niko Moritz, Junteng Jia, Gil Keren, Egor Lakomkin, Yiteng Huang, Jacob Donley, Jay Mahadeokar, and Ozlem Kalinli, “M-BEST-RQ: A multi-channel speech foundation model for smart glasses,” in Proc. IEEE ICASSP, 2025, pp. 1–5.

[^10]: Ya Jiang, Hongbo Lan, Qing Wang, and Shutong Niu, “Multi-modal streaming ASR in cross-talk scenario for smart glasses,” in Proc. IEEE ICASSP, 2025, pp. 1–5.

[^11]: Hongbo Lan, Ya Jiang, Jun Du, and Qing Wang, “Exploring knowledge distillation for low-resource multi-modal streaming ASR in the CHiME-8 MMCSG challenge,” Computer Speech & Language, vol. 95, pp. 101837, 2026.

[^12]: Ju Lin, Yiteng Huang, Ming Sun, Frank Seide, and Florian Metze, “Directional speech recognition with full-duplex capability,” in Proc. Interspeech, 2025, pp. 2570–2574.

[^13]: Jiamin Xie, Ju Lin, Yiteng Huang, Tyler Vuong, Zhaojiang Lin, Zhaojun Yang, Peng Su, Prashant Rawat, Sangeeta Srivastava, Ming Sun, et al., “Thinking in directivity: Speech large language model for multi-talker directional speech recognition,” in Proc. Interspeech, 2025, pp. 3898–3902.

[^14]: Philipos C Loizou, Speech Enhancement: Theory and Practice, CRC press, Boca Raton, FL, USA, 2 edition, 2013.

[^15]: DeLiang Wang and Jitong Chen, “Supervised speech separation based on deep learning: An overview,” IEEE/ACM Trans. Audio, Speech, Language Process., vol. 26, pp. 1702–1726, 2018.

[^16]: Tae Jin Park, Naoyuki Kanda, Dimitrios Dimitriadis, Kyu J Han, Shinji Watanabe, and Shrikanth Narayanan, “A review of speaker diarization: Recent advances with deep learning,” Computer Speech & Language, vol. 72, pp. 101317, 2022.

[^17]: Katerina Zmolikova, Marc Delcroix, Tsubasa Ochiai, Keisuke Kinoshita, Jan Černockỳ, and Dong Yu, “Neural target speech extraction: An overview,” IEEE Signal Processing Magazine, vol. 40, no. 3, pp. 8–29, 2023.

[^18]: Alex Graves, “Sequence transduction with recurrent neural networks,” in Proc. ICML, 2012.

[^19]: Barry D Van Veen and Kevin M Buckley, “Beamforming: A versatile approach to spatial filtering,” IEEE ASSP Magazine, vol. 5, no. 2, pp. 4–24, 1988.

[^20]: Jacob Benesty, Jingdong Chen, and Yiteng Huang, Microphone Array Signal Processing, Springer, 2008.

[^21]: Gongping Huang, Jesper R Jensen, Jingdong Chen, Jacob Benesty, Mads G Christensen, Akihiko Sugiyama, Gary Elko, and Tomas Gaensler, “Advances in microphone array processing and multichannel speech enhancement,” in Proc. IEEE ICASSP, 2025, pp. 1–5.

[^22]: Yangyang Shi, Yongqiang Wang, Chunyang Wu, Ching-Feng Yeh, Julian Chan, Frank Zhang, Duc Le, and Mike Seltzer, “Emformer: Efficient memory Transformer based acoustic model for low latency streaming speech recognition,” in Proc. IEEE ICASSP, 2021, pp. 6783–6787.

[^23]: Yang Liu, Li Wan, Yiteng Huang, Yong Xu, Yangyang Shi, Saurabh Adya, Ming Sun, and Florian Metze, “MMW: Side talk rejection multi-microphone Whisper on smart glasses,” To appear in Proc. IEEE ASRU, 2025.

[^24]: Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya Sutskever, “Robust speech recognition via large-scale weak supervision,” in Proc. ICML, 2023, pp. 28492–28518.

[^25]: Shaojie Bai, J Zico Kolter, and Vladlen Koltun, “An empirical evaluation of generic convolutional and recurrent networks for sequence modeling,” arXiv preprint arXiv:1803.01271, 2018.

[^26]: Vassil Panayotov, Guoguo Chen, Daniel Povey, and Sanjeev Khudanpur, “LibriSpeech: an ASR corpus based on public domain audio books,” in Proc. IEEE ICASSP, 2015, pp. 5206–5210.

[^27]: Taku Kudo and John Richardson, “SentencePiece: A simple and language independent subword tokenizer and detokenizer for neural text processing,” in Proc. EMNLP, 2018, pp. 66–71.

[^28]: Karel Veselỳ, Arnab Ghoshal, Lukás Burget, and Daniel Povey, “Sequence-discriminative training of deep neural networks,” in Proc. Interspeech, 2013, pp. 2345–2349.