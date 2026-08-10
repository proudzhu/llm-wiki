# The Intel Neuromorphic DNS Challenge

Jonathan Timcheck<sup>∗</sup>, Sumit Bam Shrestha<sup>∗</sup>, Daniel Ben Dayan Rubin<sup>∗</sup>, Adam Kupryjanow<sup>†</sup>, Garrick Orchard<sup>∗‡</sup>,

Lukasz Pindor<sup>†</sup>, Timothy Shea<sup>∗</sup>, and Mike Davies<sup>∗</sup>

<sup>∗</sup>Neuromorphic Computing Lab, Intel Labs

<sup>†</sup>Design Engineering Group Poland, Intel

<sup>‡</sup>Work done during Intel employment

ndns@intel.com

Abstract—A critical enabler for progress in neuromorphic computing research is the ability to transparently evaluate different neuromorphic solutions on important tasks and to compare them to state-of-the-art conventional solutions. The Intel Neuromorphic Deep Noise Suppression Challenge (Intel N-DNS Challenge), inspired by the Microsoft DNS Challenge, tackles a ubiquitous and commercially relevant task: real-time audio denoising. Audio denoising is likely to reap the benefits of neuromorphic computing due to its low-bandwidth, temporal nature and its relevance for low-power devices. The Intel N-DNS Challenge consists of two tracks: a simulation-based algorithmic track to encourage algorithmic innovation, and a neuromorphic hardware (Loihi 2) track to rigorously evaluate solutions. For both tracks, we specify an evaluation methodology based on energy, latency, and resource consumption in addition to output audio quality. We make the Intel N-DNS Challenge dataset scripts and evaluation code freely accessible, encourage community participation with monetary prizes, and release a neuromorphic baseline solution which shows promising audio quality, high power efficiency, and low resource consumption when compared to Microsoft NsNet2 and a proprietary Intel denoising model used in production. We hope the Intel N-DNS Challenge will hasten innovation in neuromorphic algorithms research, especially in the area of training tools and methods for real-time signal processing. We expect the winners of the challenge will demonstrate that for problems like audio denoising, significant gains in power and resources can be realized on neuromorphic devices available today compared to conventional state-of-the-art solutions.

## I. INTRODUCTION

N <sup>EUROMORPHIC</sup> <sup>computing</sup> <sup>achieves</sup> <sup>excellent</sup> <sup>perfor-</sup> mance with power and latency savings for certain algorithms [1], and the field stands to greatly benefit from focusing on well-defined neuromorphic challenge problems motivated by recent progress. Challenge problems facilitate the consistent evaluation and comparison of different approaches to solving important classes of problems and can help align researchers toward the most promising directions, thus accelerating progress. Historically, challenge problems have often spurred breakthroughs in the field of machine learning, e.g., MNIST [2], CIFAR-10 [3], and ImageNet [4]. However, the less-mature field of neuromorphic computing lacks unifying challenge problems. Most results of benchmarking neuromorphic systems are bespoke, where custom tasks are conceived chiefly to highlight the capabilities of a given neuromorphic system, making it difficult to compare across different systems and solutions, whether neuromorphic or conventional [5].

Any neuromorphic challenge problem must be chosen and structured carefully. A poorly-selected problem could direct focus in the wrong direction, on tasks for which neuromorphic hardware is unlikely to provide advantages over conventional hardware. This includes many existing popular machine learning tasks, such as those involving static image processing. Similarly, defining a challenge problem without an accompanying methodology for comprehensively evaluating neuromorphic compute cost makes it difficult to rigorously compare different solutions.

![](figures/7851b7b1adbfb1cb1a4f58722b4ee329e4c0bf45833851fe836c88c31cff1bd7.jpg)  
Figure 1. The audio denoising task. Audio denoising is ubiquitous and has many attributes that are likely to reap benefits from neuromorphic hardware

Researchers have discussed at length what makes for good neuromorphic challenge problems and benchmarks [6], identify ing qualities such as easy access and use, freely available data, not computationally prohibitive, representative of an important real-world task, and unsaturated [7]. Existing neuromorphic benchmarks support these goals, but they are few in number and have key shortcomings. We briefly discuss several existing neuromorphic challenge problems in the following section.

## A. Past neuromorphic challenge problems

One of the first prominent neuromorphic challenge problems was image classification on the N-MNIST or N-Caltech101 datasets [8]. N-MNIST and N-Caltech101 are neuromrophic versions of the classic MNIST [2] and Caltech101 [9] datasets: the neuromorphic datasets were captured using an event-based camera moving in a precise saccadic motion while pointed at a computer monitor displaying an MNIST or Caltech101 static image. While N-MNIST and N-Caltech101 were instrumental in advancing neuromorphic vision research and provided common datasets to compare various neuromorphic algorithms, the inherent source of information is a static image and lacks spatiotemporal information content [10], especially once the saccadic motion is compensated. Thus these datasets are generally not ideal for showcasing the full potential of neuromorphic computational models which aim to exploit neuronal dynamics inspired by biological neurons for efficient temporal signal processing (Section III).

Another popular neuromorphic vision challenge problem is gesture recognition on the DVS Gesture dataset [11]. The DVS Gesture dataset is naturally matched to neuromorphic computing—the sparse, event-based, and spatiotemporal nature of dynamic vision sensor data naturally lends itself to neuromorphic processors that also possess these attributes. Evaluated as a neuromorphic challenge problem, however, DVS Gesture uses specialized event-based sensor data which limits widespread applicability, and the dataset is small (1,342 instances). Neuromorphic solutions on DVS Gesture achieve a latency of 104ms [11] on TrueNorth and 12.5ms on Loihi [1] processing at 1ms per step. Further study shows that the accuracy on the task improves with a coarser timestep of up to 25ms [12]. This indicates that the fine-grained temporal information in the DVS Gesture dataset may not be vital in this task; intuitively, common gestures are likely slow enough to be sufficiently captured on a slower timescale.

A popular neuromorphic audio challenge problem is keyword spotting on the Spiking Heidelberg Datasets [7]. The Spiking Heidelberg Datasets target the widely-applicable task of keyword spotting, and importantly, audio is pre-processed with a neuroscience-inspired cochlea model. This provides a consistent neuromorphic encoding to spikes upon which researchers can build their keyword spotting algorithms, thus facilitating simple and fair task performance comparisons across different spiking neural network (SNN) algorithms. However, the cochlear encoding of the Spiking Heidelberg Datasets presents some critical shortcomings when viewed from the greater context of more general and more difficult audio processing tasks. Firstly, the information preservation of the cochlear encoding is unquantified, thus this encoding could artificially bottleneck the performance of keyword spotting, and perhaps severely bottleneck performance for more sophisticated audio processing tasks. Secondly, the power cost of computing the cochlear encoding is also unquantified, yet power is an important factor in real-world low-power audio processing systems. Indeed, how to encode an audio signal efficiently and faithfully for processing in a neuromorphic system is an open research question which plays an important role in our definition of the Intel N-DNS Challenge.

Other neuromorphic benchmarks have been proposed that target applications that are also well-matched to the spatiotemporal event-based neuromorphic computing style, such as Braille letter reading [13] and gesture recognition using electromyograph and dynamic vision sensor fusion [14]. However, these benchmarks involve niche sensors and applications, limiting their real-world impact and interest compared to more mainstream AI problems dealing with images, video, text, or

audio.

## B. Audio denoising as a neuromorphic challenge

In this work, we identify audio denoising as an excellent neuromorphic challenge task. As detailed in subsequent sections, audio denoising has ubiquitous real-world applicability and plays to the strengths of neuromorphic computing. We have developed the Intel N-DNS Challenge to make the task easily accessible, free to all, unsaturated, and designed specifically to make it easy to compare solutions over a comprehensive set of metrics.

The Intel N-DNS Challenge is inspired by the Microsoft DNS Challenge, an audio denoising challenge that has been running since 2020 [15]–[18]. At a basic level, the Microsoft DNS Challenge has focused on improving speech denoising solutions as measured by human perceptual audio quality metrics and the Challenge included a track with the constraint that solutions must run in real-time on an Intel i5 or equivalent processor; essentially, the goal was to obtain the highest audio quality possible under the compute architecture constraint. In contrast, in the Intel N-DNS Challenge, we are changing this architecture constraint and taking a more holistic approach to evaluating solutions by defining metrics for power and latency in addition to audio quality metrics.

The spirit of the Intel N-DNS Challenge is to achieve production-level (near-SOTA) denoising performance in a system with at least an order of magnitude reduction in power, while also reducing latency, compared to real-time denoising solutions on conventional architectures. Our belief is that the neuromorphic computing features of Intel’s Loihi 2 chip— representative of future commercial neuromorphic devices— will enable the realization of such gains. Thus in the Intel N-DNS Challenge we define one track focusing on evaluating solutions on existing neuromorphic hardware (Loihi 2) and another track focusing on neuromorphic algorithm development, which may motivate new features in future neuromorphic hardware.

The Intel N-DNS Challenge has a 1-year timeline, but we invite the community to continue using the Intel N-DNS Challenge as a benchmark after the challenge ends. More broadly, we view the N-DNS challenge as a single iteration in a continuing effort to develop challenge problems that help to advance neuromorphic computing to commercial maturity.

We define the audio denoising task in Section II, discuss neuromorphic computing as it pertains to this work in Section III, overview the Intel Neuromorphic DNS Challenge in Section IV, describe the data in Section V, specify evaluation criteria in Section VI, describe our baseline solution in Section VII, address additional clarifications in Section VIII, and summarize our contributions in Section IX. We make our code publicly available for obtaining the challenge data, evaluation pipeline, and the example baseline solution in the Intel N-DNS Challenge Github Repository (https://github.com/IntelLabs/IntelNeuromorphicDNSChallenge) with a permissive MIT license.

## II. PRIMER ON AUDIO DENOISING

Digital audio signal denoising, also called audio signal enhancement, is a fast-growing research area, but its origin can be traced back to the late 70’s and early 80’s when Spectral Subtraction [19] and Wiener filter [20] algorithms were introduced. Subsequently, beamforming techniques were successfully adopted [21], [22]. While a significant advance, beamforming was not practical due to several limitations, namely, that multiple microphones are needed to perform noise reduction, Signal-to-Noise Ratio (SNR) improvement is highly correlated with the number of microphones, and compute complexity increases with the square of the number of microphones. Furthermore, in the last few years, there has been an increased research interest in single microphone denoising. Single-microphone device configurations are omnipresent, and the utilization of Deep Neural Networks has enabled very successful single-microphone denoising [23]–[25]. We address the single-microphone audio denoising task in the Intel N-DNS Challenge (Figure 1).

Typically, the signal captured by a microphone contains a source signal, like speech or music, and stationary or nonstationary noises. Stationary noises change amplitude and frequency profile slowly in time, whereas non-stationary noises vary quickly over time. Some examples of the former are an air conditioner, dishwasher, fan, or engine noises. Examples of the latter are a baby crying, a dog barking, or keyboard typing. Notably, reduction of stationary noises is a significantly simpler task than the removal of non-stationary noises. Noise is an additive distortion defined in the time domain according to

$$
y (t) = x (t) + n (t),\tag{1}
$$

where $x ( t )$ is the amplitude of the source signal for time index $t , n ( t )$ is the noise signal, and $y ( t )$ is the noisy signal captured by the microphone.

Furthermore, most recordings are conducted in a reverberant environment; $e . g .$ , in indoor conditions, the signal is contaminated by reverb. Noisy reverberant signals can be expressed as

$$
y (t) = h (t) * x (t) + n (t),\tag{2}
$$

where $h ( t )$ represents impulse response and only a single noise source is represented. Since reverb is a multiplicative distortion, most denoising algorithms will focus on noise removal [26]. There are alternative approaches that perform reverb reduction and noise removal in one shot [27] or use a cascade of processing with reverb reduction [22] in a first stage, followed by a denoising stage. Audio denoising refers specifically to the process of enhancing an audio signal by subtracting noise from it; this is the task in the Intel N-DNS Challenge (Figure 1).

Audio denoising is commonly utilized in both real-time and non-real-time scenarios. An example of a real-time scenario is a voice call which is performed on an end-user device, such as a PC, phone, headset, or smart device, or inside applications like Microsoft Teams or Zoom. In this use case, algorithms must not introduce latency greater than 40ms. Furthermore, the compute load must be light enough to fit into existing power and memory constraints without degrading user experience. Another example of a real-time application is speech enhancement in human to-computer communication, where denoising is performed to improve the accuracy of downstream processing such as keyword spotting or Automatic Speech Recognition (ASR). There are other use cases, such as transcribing meeting minutes, where denoising can be performed offline. These are viewed as non-real-time scenarios that impose fewer restrictions on the algorithm, $e . g .$ , permitting non-causal filtering.

## A. Current state-of-the-art solutions

Recently neural networks (NN) based algorithms have been extensively applied to audio denoising problems. Initial solutions focused exclusively on denoising quality and used large models to solve the problem with great breakthroughs in accuracy. However, as the models become more and more accurate, the focus has shifted to real-time denoising performance. In fact, the most recent Microsoft DNS Challenges have dropped the non-real-time track [15], [17], [18].

Non-real-time solutions focus purely on the quality of denoising and are typically non-causal. Non-real-time solutions from the speech enhancement and source separation literature include attention architectures [28], temporal convolutional networks (TCN) [29], the Convolutional Time-domain audio separation Network (Conv TasNet) [24], convolutional phase and amplitude processing (PHASEN) [30], and audio source separation with nested depthwise convolutional downsampling (SuDoRM-RF) [31]. For the denoising task in speech enhancement, the desired enhancement is the removal of noise, and in source separation, the desired separation is between speech and noise. Real-time solutions focus on making the network lightweight and causal while maintaining denoising performance. Some examples include causal forms of TCN, Conv TasNet [29], and recurrent topologies with stacked LSTM or GRU [32].

The most common encoding-decoding method of choice is STFT-ISTFT [28], [30], [32] or its similar spectrogram transformation like DCT [33], while methods like SuDoRM RF [31] directly process the raw audio samples. There are different approaches for processing the complex STFT input in the literature. Some methods only make use of the magnitude information [24], [29], [32], some process the magnitude and phase separately and combine them [34], while some process the complex spectrum directly using complex convolutional filters [28].

The majority of the solutions use backpropagation-based supervised training. However, a wide variety of losses have been used in different works. The most common ones are the mean-square error of the resulting spectrum or maximization of the signal-to-noise ratio. A survey of various loss metrics used in audio denoising with their benefits is described in [35]. Some solutions even prioritize speech over suppression with an additional loss penalty term [34]. In addition, unsupervised or semi-supervised training methods have also been investigated to achieve a general solution even on out-of-distribution datasets. A particularly interesting method is the teacher-student training method proposed in RemixIT [36] where a teacher network trained on out-of-distribution data is used to bootstrap the noisy signals to multiply the variety of in-distribution data samples.

It is evident that noise suppression with deep neural networks is an active area of research with new methods being introduced regularly. Recent efforts have not only focused on the quality of denoising but also on the size of models and satisfying real-time requirements. There is a vast body of research from which to borrow for neuromorphic audio denoising.

## III. NEUROMORPHIC AUDIO DENOISING

We chose the audio denoising task for this challenge because it presents an excellent opportunity for neuromorphic algorithm innovation (Figure 1). Audio denoising is a ubiquitous power-constrained task with commercial relevance. It is often performed on mobile devices, and every Intel Core™ CPU in production now includes AI hardware acceleration support for it. Given the significant compute load of today’s denoising solutions, lowering the power with a neuromorphic solution could not only lead to longer battery lives and smaller form factors but could bring the functionality to even more powerconstrained devices such as headsets, earbuds, hearing aids, and cochlear implants. Moreover, it is a temporal signal processing task, which neuromorphic systems are expected to excel at [6]. Indeed, commercial neuromorphic vendors are already targeting speech-enhancing hearing aids, promising orders-of-magnitude gains [37]. Looking forward, the audio denoising task represents a starting point for the development of more general neuromorphic audio processing algorithms that operate in real time with imperceptible latency, such as audio environment emulation, speech separation, voice morphing, and speech-to-speech language translation.

Furthermore, audio denoising is especially timely as a neuromorphic research vector. It is a generative task unsolved in neuromorphic computing, and audio is a low data-rate signal that is well-matched to current neuromorphic chips and designs that generally target low-power edge processing. Solutions can be readily compared to recent conventional machine learning advances, including models deployed in production, and can leverage insights, methods, and datasets from those recent efforts.

## A. Neuromorphic computing and Loihi 2

Neuromorphic computing aims to apply fundamental principles of the brain’s information processing mechanisms to engineered computing devices. The brain consumes a mere 20 watts of power yet can execute remarkable feats of perception, planning, control, and learning while operating in real time processing sequential data streams. In contrast, our conventional computer systems today struggle to emulate even a narrow subset of such feats with much larger power budgets, even though they have the advantage of precisely engineered ultrafast nanoscale transistors as a computational substrate [38]. Indeed, biological inspiration is compelling. However, when computer architects go about designing neuromorphic systems, they face a fundamental question: What biology-inspired computational strategies unlock neuromorphic performance advantages versus conventional architectures?

Neuromorphic researchers have identified several promising strategies, such as analog computation, sparse connectivity, spike-based communication, in-memory computation, local synaptic learning rules, recurrent feedback, and stateful, dynamic neuron models [39]. Subsets of these computational strategies are being implemented in hardware, $e . g .$ , novel analog devices [40], analog computation in conventional circuits [41]– [44], digital processing with spike-based communication [45]– [49], and many others.

In the Intel Neuromorphic Computing Lab, we focus on designing all-digital neuromorphic processors that can be manufactured in state-of-the-art semiconductor process technology. The SOTA process enables direct comparisons to SOTA conventional architectures, and the all-digital character allows a broad range of architectural features to be rapidly prototyped with fully deterministic and repeatable execution. While the all-digital character sacrifices some efficiency benefits of analog computation, we believe it is most important to first rapidly explore the architecture-algorithm co-design space before undertaking the more difficult, slower, and currently less area-efficient path of analog circuit design and novel device engineering. We believe the subset of neuromorphic computational principles supported by our latest chip, Loihi $^ { 2 , }$ are sufficient to show significant gains in power and latency compared to conventional computer architectures, and that this will motivate further optimizations via more nascent neuromorphic computing principles.

Loihi 2 is a state-of-the-art neuromorphic chip designed to efficiently compute temporal dynamics in sparse networks using sparse, event-based communication [50]. Like its predecessor [46], Loihi 2 consists of neuron cores that compute the temporal dynamics of stateful neural models and a communication mesh optimized for spike-based communication. Loihi 2 implements a number of generalizations and optimizations motivated by the learnings and pain points of its predecessor. These include microcode-programmed neuron models, which enable a much wider variety of neurons as seen in the brain [51] as well as in novel neuromorphic algorithms [52] and promising computational benefits in heterogeneous networks [53]. Loihi 2 also features graded spikes, i.e., spikes that carry an integer value, rather than binary spikes. While not biologically motivated, graded spikes are only marginally more costly to support than binary spikes in digital neuromorphic hardware and offer straightforward gains in algorithmic precision and processing speed. Loihi 2 also enhances Loihi 1’s learning support so arbitrary local modulating factors (“third factors”) may be computed by postsynaptic neuron microcode. We believe Loihi 2’s rich feature set is sufficient to unveil significant performance gains in tasks well-suited to temporal dynamics processing, hence the spirit of using Loihi 2 as a model for neuromorphic processing in the Intel N-DNS Challenge.

## B. Neuromorphic audio processing and promising directions

The computational model implemented by neuromorphic processors such as Loihi 2 is that of a discretized dynamical system. Unlike conventional artificial neurons from machine learning, the state variables of a dynamical system evolve and process inputs in time—i.e., time is a fundamental ingredient of the computation. Thus we expect neuromorphic processors to naturally excel in temporal processing tasks, such as audio processing. Indeed, precisely-timed spiking codes are wellknown to underlie audio processing in the brain [54]–[56], and cochleas perform sophisticated transformations to encode incoming audio for effective processing [55], [56]. These insights from neuroscience provide clear hope for the feasibility and success of neuromorphic audio processing, and recent progress on tasks such as keyword spotting provide some evidence thereof [7], [52], [57], [58].

One can immediately ascertain three critical research questions when designing a neuromorphic audio processing system: (1) How to efficiently represent an audio waveform with high fidelity in the neuromorphic domain? (2) How to efficiently perform the desired audio processing (denoising) on this neuromorphic representation? and (3) How to efficiently invert the neuromorphic representation to yield an output (waveform)?

A natural place to start answering these questions is to start with the first: how to efficiently represent a waveform in the neuromorphic domain. There exist a variety of possibilities for representing data neuromorphicly—e.g., binary spikes, graded spikes, population codes, sparse distributed codes, and phase codes—and a variety of encoding algorithms— e.g., biology-inspired cochleogram models [7], [52], Short-Time Fourier Transforms (STFT) [59], and Mel-frequency cepstral coefficients (MFCCs) [60]. Taking inspiration from biology, in developing our baseline solution for the Intel N-DNS Challenge, we initiated our study of neuromorphic audio encodings on cochleogram models, which can provide sparse representations in binary spikes, high sensitivity, frequency selectivity, large dynamic range, pitch-shifting, and self-peak normalization [52], [56], [61], [62]. However, we quickly realized that cochleogram models such as [7], [63] are generally computationally expensive to invert with high fidelity, which is prohibitive for a low-power denoising system. As an alternative, we developed our initial baseline solution for the Intel N-DNS Challenge using a more conventional audio encoding, the Shorttime Fourier Transform (STFT) [59], which is easy to invert and has perfect fidelity (aside from quantization and numerical error); furthermore, the STFT encoding can take advantage of graded spikes which are supported on Loihi 2.

While we select an STFT encoding for our baseline, we emphasize that new solutions to the Intel N-DNS Challenge have a wide range of encoding strategies to explore, e.g., designing invertible bio-inspired cochleogram models, utilizing sparse STFTs [52], or even encoding schemes that depend on feedback from other portions of the neuromorphic denoising system, much like the recurrent feedback connections from deeper areas of the brain to more low-level sensory encoding areas. Importantly, the encoding used in a neuromorphic audio processing system must be co-designed with the task for efficient operation; indeed, such synergistic design is observed in biology [64], [65].

Secondly, after audio is encoded, the actual execution of the audio processing in the neuromorphic domain is a very open research opportunity. Neuromorphic audio processing systems can employ a wide variety of strategies to perform processing in the neuromorphic domain, such as simplistic DNN conversion [66], using a network of feedforward or recurrent leaky integrate-and-fire neurons [7], [67], [68], a network of complex resonate-and-fire neurons [52], or a sigma-delta neural network as we describe in the following subsection for our baseline solution. Methodologies inspired by conventional deep learning, e.g., multi-timescale networks [29], [31], [36] or attention [28], if mapped efficiently to the neuromorphic domain, could be promising directions as well. And finally for completeness—to address the third question posed above—decoding the output of the neuromorphicallyprocessed audio again depends on the processing used and must be tailored appropriately to operate in an efficient manner.

Thus we see much opportunity for innovation throughout a neuromorphic processing pipeline—encoding, processing, and decoding. Furthermore, the audio denoising task represents just one potential audio processing task that opens the door to tackling many others with methods that are transferable to other signal processing domains such as wireless, biosensors, and control.

## C. Baseline neuromorphic solution

We have developed a simple baseline neuromorphic solution to the audio denoising task, and we already begin to see evidence of significant energy efficiency gains from using neuromorphic features. The baseline solution uses a sigma-delta neural network (SDNN), an adaptation of a conventional feedforward ReLU neural network architecture that exploits sparse message passing with graded spikes and stateful neurons— computational strategies that can be implemented efficiently in neuromorphic architectures and that are supported by Loihi 2 in particular. The SDNN baseline solution achieves similar audio quality to a conventional baseline solution NsNet2 from the Micrsoft DNS Challenge 2022, but with an order of magnitude fewer operations and less than half its latency. We provide a more detailed overview of the baseline solution architecture and its performance in Section VII.

Importantly, our SDNN baseline solution is a very basic feedforward architecture, and does not exploit several of the aforementioned neuromorphic features that perform well on Loihi 2 (Table I). As new solutions incorporate more of these features, such as recurrent and sparse connectivity, we anticipate further significant improvements in power and model size.

Table I  
NEUROMORPHIC FEATURES THAT ARE PERFORMANT ON LOIHI 2 AND THEIR UTILIZATION IN OUR N-DNS BASELINE SOLUTION.

<table><tr><td>Neuromorphic feature</td><td>In baseline solution</td></tr><tr><td>Sparse activity</td><td>√</td></tr><tr><td>Sparse connectivity</td><td>✗</td></tr><tr><td>Recurrence</td><td>✗</td></tr><tr><td>Stateful neurons</td><td>√</td></tr><tr><td>Neuron temporal dynamics</td><td>✗</td></tr><tr><td>Synaptic plasticity</td><td>✗</td></tr><tr><td>Graded spikes</td><td>√</td></tr><tr><td>Delay as computational element</td><td>√</td></tr></table>

## IV. INTEL NEUROMORPHIC DNS CHALLENGE

Just like the Microsoft DNS Challenge, The objective of the Intel Neuromorphic DNS Challenge is to create a system that removes the noise from noisy human speech in real-time. However, in contrast to the denoising system that runs on a conventional CPU in the Microsoft DNS Challenge, the Intel N-DNS Challenge targets the Loihi 2 neuromorphic processor aiming to realize the neuromorphic system’s potential for power and latency improvements. To this end, the Intel N-DNS Challenge hosts two tracks:

1) Algorithmic. The objective in Track 1 is to develop a highquality audio denoising solution that operates efficiently on a neuromorphic system. The algorithm is not required to run on actual neuromorphic hardware, but rather will be simulated on conventional hardware. Latency and a neuromorphic proxy power are estimated.

2) Loihi 2. The objective in Track 2 is to develop a highquality audio denoising system that operates efficiently on Loihi 2 [50]. The power and latency of the denoising solution will be measured by running it on actual Loihi 2 hardware.

Track 1 provides freedom to explore a wide range of neuromorphic denoising solutions, without the need to demonstrate the solutions on actual neuromorphic hardware; this track is intended for rapid development and potentially to inspire future neuromorphic hardware features. Track 2 guarantees that neuromorphic denoising solutions can indeed run on actual neuromorphic hardware. This track provides a rigorous demonstration of power and latency benefits realized by neuromorphic hardware.

Both tracks follow the same structure: noisy audio is encoded into a form suitable for processing on a neuromorphic system, processed on a neuromorphic system (simulated for Track 1, or real hardware system for Track 2), and decoded into a clean output audio waveform (Figure 2). Solutions are evaluated by an audio quality metric and a computational resource usage metric and are subject to a minimum audio quality and maximum latency (real-time) requirement.

The selection procedure for the winner of each track is described in the Intel N-DNS Challenge Github Repository, along with challenge logistics and timeline. Solutions will be judged not only on the measured or estimated computational metrics, but also on commercial relevance, broader research impact, and quality of solution write-up. We describe the dataset, evaluation metrics, and an example baseline solution in the following sections.

## V. DATASET

The Intel N-DNS dataset is derived from the Microsoft DNS Challenge dataset, which is a corpus of human speech audio samples of various categories including but not limited to English, German, French, Spanish, Russian and various categories of noises (DNS Challenge Github Repository). We provide a synthesizer script that generates 30-second segments of clean (ground truth), noise (additive), and noisy (ground truth + noise) audio data for both the training and validation dataset in the challenge repository. For training the network, participants are free to choose and/or tweak the data synthesis parameters or choose only a subset of the Microsoft DNS Dataset language and noise categories, or even include additional speech and noise corpus for synthesis. The default is 500 total hours (60,000 samples) of audio data with the synthesized SNR between 20dB to -5dB at 16kHz with a bit depth of 16 bits. The validation set, on the other hand, is generated using the default settings in the audio synthesis script.

The testing data for Intel N-DNS Challengewill be provided at a later point after participant models are frozen. Thereafter, there can be no changes to the submitted models in order to ensure a fair evaluation on the test set. The characteristics of the testing data will be similar to the training and validation set. Note that this model freeze is only a feature for administering the challenge in a fixed timeline with blinded test set, and we encourage the continued use of the Intel N-DNS Challenge resources and framework as a general, non-time-bound challenge problem for neuromorphic research.

In addition, we include general dataloader modules in the Intel N-DNS Challenge that load the clean, noise, and noisy audio from the training, validation, and testing samples. Optionally, the dataloader also provides metadata about synthesized audio samples like the clean audio sources, noise sources, the noise mixture level and so on.

## VI. EVALUATION

There is no single metric that captures the overall performance of a solution in the Intel N-DNS Challenge. Instead, there are multiple metrics that characterize different dimensions of performance. Naturally, we must quantify the output audio quality of the N-DNS system, and so we define metrics for this related to signal-to-noise ratio and perceptual audio quality. Equally important for the objective of the challenge is to assess computational resource costs: latency to ensure realtime processing, power to quantify energy efficiency, and chip resources required to support the solution on neuromorphic hardware. With these four performance dimensions covered, we can comprehensively evaluate each solution. We also consider certain derived figures of merit, such as power-delay product, a common quantity used to represent the tradeoff between speed and energy efficiency in electronics systems.

This collection of metrics allows us to compare solutions designed for different points in performance space, i.e., its positioning on a Pareto frontier with top-performing solutions designed for low-power or high-power, with correspondingly lower or higher audio quality.

A. Audio quality metrics and minimum audio quality improvement

1) SI-SNR metric: Task performance in the N-DNS Challenge is measured as the output audio quality; we use the Scale-Invariant Source-to-Noise Ratio (SI-SNR)—SI-SNR is a common metric in the audio processing literature (e.g., [69], [70]). SI-SNR measures how clear the human speech is above the noise in the output of the N-DNS system, similar to a Source-to-Noise Ratio (SNR) [70]. But importantly, SI-SNR is also scale-invariant—i.e., changing the overall magnitude (volume) of the output does not change the SI-SNR; intuitively, we do not wish to favor solutions over others’ that simply increase the output volume.

![](figures/6d2216ea8f2e7ae2fcfc85d0cbfe8075acd0f0336904ef3ac5cc3a18d49cd67f.jpg)  
Figure 2. Intel Neuromorphic DNS Challenge Solution Structure. Input noisy audio is encoded before it enters the neuromorphic denoiser (N-DNS). The neuromorophic denoiser processes its input, and the output of the neuromorphic denoiser is decoded to produce the final output clean audio. The encoder, decoder, and neuromorphic denoiser are the constituents of a solution to the Intel N-DNS Challenge and their power and latency are evaluated, in addition to the output audio quality. In Track 1, all components run on CPU, while in Track 2, the neuromorphic denoiser runs on Loihi 2.

For a single input waveform, a real-valued zero-mean vector $s ,$ and the corresponding output waveform from the N-DNS system ${ \hat { s } } ,$ the SI-SNR is defined as

$$
\mathrm{SI-SNR} := 1 0 \log_ {1 0} \frac {| | s _ {\mathrm{target}} | | ^ {2}}{| | e _ {\mathrm{noise}} | | ^ {2}},\tag{3}
$$

where $\begin{array} { r } { s _ { \mathrm { t a r g e t } } : = \frac { \langle \hat { s } , s \rangle s } { | | s | | ^ { 2 } } } \end{array}$ and $e _ { \mathrm { n o i s e } } : = \hat { s } - s _ { \mathrm { t a r g e t } } .$

We choose SI-SNR as one of our metrics for its simplicity and generality, rather than more complicated audio quality metrics, such as speech-to-text word accuracy used in the Microsoft DNS Challenge [18]. The focus of the N-DNS challenge is on neuromorphic algorithm innovation; this in itself constitutes a sufficiently challenging task. Moreover, we view the audio denoising task as a representative of a general audio processing workload, and some commercial applications may not specifically prioritize human-listener perceptual quality. Finally, the SI-SNR can be conveniently used as a loss function for machine learning approaches.

The mean SI-SNR on the test set will be used to compare solutions. A script for computing mean SI-SNR is provided in the Intel N-DNS Challenge Github Repository.

2) Minimum SI-SNR improvement: Since solutions in the Intel N-DNS Challenge are evaluated holistically, solutions may target high audio quality by using a large amount of power, or lower audio quality using a smaller amount of power, or any audio quality-power point in between. However, to ensure that the audio denoising task is being solved to some significant extent, we require solutions to achieve a minimum audio quality improvement over the noisy input audio quailty. Moreover, per our emphasis on neuromorphic computing, we require that the neuromorphic component of the N-DNS system be responsible for a significant portion of the audio quality improvement; a solution may optionally perform some denoising in the encoder and decoder, but the spirit of the Intel N-DNS Challenge is in performing neuromorphic denoising.

Therefore, we define two measures of audio quality (SI-SNR) improvement (i) relative to (1) the noisy data $\left( \mathrm { S I - S N R i _ { \mathrm { d a t a } } } \right)$

and (2) the encode+decode processing $\mathbf { ( S I { - } S N R i _ { e n c o d e + } d e c o d e ) }$ expressed by the following inequalities:

$$
\mathrm{SI-SNRi} _ {\text { data }} > 3 \mathrm{dB}\tag{4}
$$

$$
\mathrm{SI-SNRi} _ {\text { enc + dec }} > 3 \mathrm{dB},\tag{5}
$$

where

$$
\text { SI - SNRi } _ {\text { data }} = \text { SI - SNR } _ {\text { full   system }} - \text { SI - SNR } _ {\text { data }},
$$

• SI-SNRi<sub>enc+dec</sub> = SI-SNR<sub>full</sub> <sub>system</sub> − SI-SNR<sub>enc+dec</sub>,

• SI-SNR<sub>full system</sub> is the mean test-set SI-SNR from the full N-DNS system (input audio → encode → neuromorphic denoiser → decode → output audio),

$\mathrm { S I - S N R } _ { \mathrm { e n c + d e c } }$ is the mean test-set SI-SNR from running only encoder and decoder (input audio → encode → decode → output audio), and

• SI- ${ \bf - S N R _ { \mathrm { { d a t a } } } }$ is the mean test-set SI-SNR on the noisy input audio (no transformations).

Equation (4) ensures that the solution achieves a minimum audio quality improvement, and Equation (5) ensures that the neuromorphic denoiser itself is responsible for a minimum audio quality improvement. These definitions allow for some amount of denoising to occur in the encoder and decoder, but critically, adding the neuromrophic denoiser must further improve audio quality. Similarly, additional pre/post-processing could be performed within the neuromorphic denoiser itself, to reduce the amount of computation in the encoder and decoder. But importantly, the computations allocated to the encoder/decoder or the neuromorphic denoiser are accounted for differently in the computational resource and chip usage metrics, as described in later sections.

3) DNSMOS metric: For audio signals, the perceptual quality of the audio signal is important in addition to the signal quality measured by SI-SNR. We use the widely adopted DNSMOS [71] metric to evaluate the perceptual quality of the solution. In DNSMOS, the perceptual quality score is predicted by a deep network that is trained to reflect the human perceptual quality expressed in Mean Opinion Score (MOS)

in its training corpus. MOS score ranges from 1 to 5, where 1 corresponds to poor quality, and 5 corresponds to excellent quality. DNSMOS is particularly effective because it has been shown to generate scores that are highly correlated with human perceptual assessment [71] compared to other similar methods like Perceptual Evaluation of Speech Quality (PESQ) [72], Perceptual Objective Listening Quality Analysis (POLQA) [73], or VisQL [74]. There exist commercial alternatives like 3QUEST, but its use is limited due to its proprietary nature.

A DNSMOS score consists of three values: speech signal quality (SIG), background noise quality (BAK), and overall audio quality (OVRL). From the perspective of speech enhance ment, the SIG score reflects the change in speech quality due to processing. Usually, most denoising algorithms do not improve SIG score significantly compared to the unprocessed signal. BAK score reflects the degree of noise present in the signal. Thus, after a speech enhancement, a significant improvement in this score is expected. Finally, OVRL score reflects the general audio quality assessment. It is not a simple average of SIG and BAK scores, but rather a general assessment of audio quality. After denoising, a signal should have a higher OVRL score.

DNSMOS provides a valuable additional facet in evaluating audio quality in the Intel N-DNS Challenge. In addition, it gives another point of comparison to existing denoising systems; namely, DNSMOS (OVRL) was used in the Microsoft DNS Challenge [18]. However, we note that while DNSMOS is an important metric, we emphasize that it is not the only metric used for the evaluation of audio quality in the Intel N-DNS Challenge; indeed, the spirit of the Intel N-DNS Challenge is directed toward holistic innovation on neuromorphic denoising systems. Furthermore, to minimize the complexity of the Intel N-DNS Challenge, we choose to not introduce additional audio quality metrics, such as STOI [75], as the pairing of SI-SNR and DNSMOS already provides an objective and a perceptual audio quality evaluation.

## B. Computational resource usage and real-time requirement

Computational resource cost is evaluated in terms of power, latency, number of parameters, and model size. To qualify as a real-time solution, the end-to-end latency must not be greater than 40ms. We measure power and latency on neuromorphic hardware in Track 2, but for Track 1, we introduce proxy metrics.

1) Latency: An audio denoising system takes some amount of time to process input audio as the audio streams into the system; this results in the output human speech being delayed relative to the input human speech. This delay is the latency of the denoising system. For the denoising system to be considered real-time, the latency must be less than some human perceptual threshold, which in our case we choose to be 40ms.

We define latency as the maximum time difference between any corresponding segment of audio in the input and output of the N-DNS system. Intuitively, the longest delay in any segment of audio is the overall delay the output must be presented at in order to not introduce playback speed fluctuations in the output audio.

Latency should be calculated by considering a real-time input propagating through an entire N-DNS system (Figure 3).

This includes data buffer latency, encoder-decoder latency, and network latency (N-DNS latency):

1) Data buffer latency is the time required to collect the audio stream to process one discrete timestep, however that may be defined for a given encoding scheme. For the STFT encoder in our SDNN baseline solution, the data buffer latency is equal to the STFT window length.

2) Encoder-decoder latency is the wall clock processing time to encode one discrete timestep-worth of the audio data, to be processed by the N-DNS network, and decode it back.

3) Network latency (N-DNS latency) is the latency introduced by the neuromorphic denoising network. It is measured by the maximum cross-correlation between the clean target audio and the denoised audio from the network.

In Track 1, notably, the (CPU) processing time for the neuromorphic denoiser (N-DNS) portion of the solution is not included in the latency calculation. We assume that the neuromorphic processing time will be small relative to the real-time timestep due to the high degree of parallelization in neuromorphic algorithms and hardware. In the case of the baseline SDNN, for example, the network must process a new STFT frame every 8 milliseconds, whereas Loihi 2 circuits typically complete all spike processing and neuron evaluations for a timestep within microseconds. We provide an example Track 1 latency calculation in Section VII.

For Track 2, latency is simply measured on a reference CPU + Loihi 2 system. The measurement methodology and an example will be provided in the Intel N-DNS Challenge Github Repository later in the challenge.

2) Power: For Track 1, we calculate a power proxy by estimating the effective number of synaptic operations per second:

$$
P _ {\text { proxy }} = \text { Effective   SynOPS } = \text { SynOPS } + 1 0 \times \text { NeuronOPS },\tag{6}
$$

where SynOPS and NeuronOPS are the mean number of synaptic operations and mean number of neuron updates, respectively, per second of audio processed in the N-DNS stage. Synaptic operations and neuron operations can be considered the computational primitives of a neuromorphic system, and energy usage is roughly proportional to their number, with the approximate weighting of the energy of one neuron operation being equal to that of about 10 synaptic operations in our experience with the Loihi architecture [46]. While $P _ { \mathrm { p r o x y } }$ gives only a crude power estimate, it provides a simple and sufficiently reliable assessment of a neuromorphic power advantage without needing to run on neuromorphic hardware.

The power consumption of the encoder and decoder is not taken into account in Track 1. We make this choice for simplicity, in expectation of the neuromorphic power dominating in realistic solutions. Note that the real-time requirement implicitly bounds the amount of computation that can be performed in the encoder and decoder.

In Track 2, the encoder and decoder are implemented on a CPU and the N-DNS stage is implemented on a Loihi 2 system. The power is simply measured on a reference CPU and Loihi 2 system. Note that since both CPU and Loihi 2 power components will be measured, any attempt to implement a disproportionate amount of the denoising functionality inside the encoding/decoding CPU stages will result in a very high power result. Details for measuring power on a reference system will be provided in the Intel N-DNS Challenge Github Repository.

![](figures/ff8fc6416acfc9b9f7c7cb9c7c22365325fa041dce466088c413ed9d0cd562e8.jpg)  
Figure 3. Real-time N-DNS pipeline. Latency is calculated by considering a real-time input propagating through an entire N-DNS system. This includes latency from buffering the input data, latency from CPU processing time of the encoder and decoder, and any latency introduced by the N-DNS component (e.g., a network that was trained to output audio delayed relative to the input).

3) Power delay product: The Power Delay Product (PDP) metric combines both latency and power efficiency in one number that allows comparing between different solutions that make different tradeoffs between running faster at higher power versus running slower at lower power. For Track 1, a proxy PDP measure is given by

$$
P D P _ {\mathrm{proxy}} = P _ {\mathrm{proxy}} \times L,\tag{7}
$$

which is in units of Ops because $P _ { \mathrm { p r o x y } }$ (Equation (6)) has units of Ops/s and the latency, L, has units of seconds.

For Track 2, PDP is directly calculated from the measured power as

$$
P D P = P _ {\mathrm{Track2}} \times L.\tag{8}
$$

4) Chip resources: The physical resource cost of mapping networks into neuromorphic architectures is an important evaluation metric since chip resources impose a hard constraint on network complexity. Compared to conventional architectures that scale through the use of bountiful off-chip memory, neuromorphic architectures embed all network configuration on-chip, hence are limited by available state for representing synaptic weights, network routing tables, neuron parameters, and other configuration parameters.

For Loihi 2 and similar architectures, the ultimate measure of a workload’s chip resource cost is core count. For Track 2, this is the definitive chip resource utilization metric used in this challenge.

Before networks are successfully mapped to chip, it is difficult to reliably estimate core count requirements, so for Track 1, we assess solutions by indirect measures of resource cost: parameter count and total model size.

A network’s parameter count includes its total synaptic state (e.g., weights and delays) and neuron parameters such as decay factors. Only unique parameters are to be counted, as expected to be uniquely configured in on-chip memories and tables leveraging convolutional and other network compression features. Note that a network’s trainable parameters will be a subset of its total unique configuration parameters.

Model size is the sum over the bit widths of all unique parameters, measured in bytes. Since Loihi 2 supports a range of synaptic weights from one to eight bits, it is possible for two networks with the same parameter counts to have very different model sizes. All else being equal, solutions with smaller model sizes are preferred.

## VII. BASELINE SOLUTION

We provide a baseline solution for Track 1 of the Intel N-DNS Challenge, available in the Intel N-DNS Challenge Github Repository. In this section, we outline the baseline solution architecture, a sigma-delta neural network, and the evaluation of the baseline solution on the metrics defined in Section VI. Later in the challenge, we will provide a Loihi 2 version of the baseline solution and evaluate it on a Loihi 2 system; we will also release the Track 2 baseline associated code.

## A. Sigma-delta neural network architecture

The proposed neuromorphic solution is a simple feedforward sigma-delta ReLU neural network (SDNN). The solution makes use of two neuromorphic computation ideologies:

sparse message passing using sigma-delta neuron and temporal computation using axonal delays.

The delta encoding exploits the temporal similarity in the data. It sparsifies the data communicated to the next layer by sending only a change that is higher in magnitude than a certain threshold. The sigma encoding, on the other hand, reconstructs the original signal at the receiving end. A combination of sigma and delta units wrapped around a dynamics or a non-linearity (ReLU in this case) is a sigma-delta neuron [76]. Sigmadelta neurons make use of the sparse messaging paradigm in neuromorphic hardware and result in a significant reduction in synaptic computations.

The axonal delays endow the network with a short-term memory capability that allows the interaction of audio/features originating at different points in time. Learnable axonal delays have been shown to increase the expressivity and performance of networks, particularly for applications with spatio-temporal features [68], [77]. Audio denoising is one such application.

The structure of the SDNN baseline solution is illustrated in Figure 4, and we describe the solution in the following.

Encoder: The encoder is a straightforward Short-Time Fourier Transform (STFT) [59] of the noisy audio waveform followed by delta encoding of the STFT magnitude. The STFT uses a window length of 512 with a hop length of 128 (<sup>1</sup>/ window length), leading to 8ms per time-step, as the signal is at 16kHz. These parameters are user-configurable. The delta encoding sparsifies the STFT magnitude which is then fed to the N-DNS network.

N-DNS: The neuromorphic denoiser (N-DNS) network is a three-layer feedforward sigma-delta ReLU network with axonal delays. The sigma-delta layer efficiently performs denoising in the sparse domain. The axonal delays provide the network with short term memory which can be used to incorporate previous temporal patterns during denoising. The N-DNS network predicts a multiplicative mask at some delay which is then used to mask the STFT magnitude. The STFT phase and magnitude from the encoder need to be delayed accordingly during the decoding phase.

Decoder: The decoder combines the multiplicative mask predicted by the N-DNS network with the delayed STFT phase and magnitude of the noisy audio signal and performs inverse STFT with the same window length and hop length as the encoder. The resulting output is the clean reconstruction (denoised) audio waveform.

The SDNN baseline network was trained with Lava-dl<sup>1</sup>, which includes the extended version of the SNN backpropagation training tool SLAYER [77]. Lava-dl SLAYER uses a surrogate gradient method (e.g., see [78]) to address the critical challenge in training spiking neural networks—the nondifferentiability of spikes. The baseline network was trained with Loihi 2’s fixed precision computation in mind and trained with appropriate quantization for synapse and neuron dynamics. We used a combination of negative SI-SNR and a mean-square error measuring the STFT magnitude reconstruction quality as the minimization loss and a RADAM optimizer for training.

The detailed training procedure, as well as Lava<sup>2</sup> evaluation of the baseline network, are available in Intel N-DNS Challenge Github Repository.

## B. Evaluation Metrics

We evaluated the SDNN baseline solution, Microsoft NsNet2 (the baseline network for Microsoft DNS 2022), and Intel DNS network using Track 1 metrics on the validation set. The metrics are summarized in Table II. All three networks use STFT encoding and ISTFT decoding.

Intel DNS network is an Intel proprietary network used in production. The model is causal, operates in real-time, and is built from LSTM and 2D convolution layers. Power metrics for this network are not available. The network was trained using proprietary datasets and augmentation techniques, and as such we view its audio quality results as upper-bound aspirational targets for challenge submissions.

The audio quality metrics include DNSMOS scores, SI-SNR, and improvement in SI-SNR (SI-SNRi). The encoder and decoder for all three networks perform lossless transformation using STFT and ISTFT. As a result, relative performance differences across models in SI-SNR and SI-SNRi are equal.

The latency was calculated by summing data buffer latency, encoder-decoder latency, and network latency (N-DNS latency), as described in Section VI.

Power proxy and PDP proxy metrics provide some measure of the relative power and power-delay-product across the three networks suitable for Track 1 comparisons. For the SDNN baseline, these are calculated according to Equations (6) and (7), respectively. For the conventional Microsoft NsNet2 network, Ops refer to Multiply–accumulate operations (MACs) without considering the negligible cost of per-neuron ReLU evaluation.

We see that our SDNN baseline is a promising neuromorphic solution to the audio denoising problem. In terms of audio quality, the SDNN baseline has a higher SI-SNR relative to the NsNet2 baseline solution from the Microsoft DNS Challenge 2022, and lower relative DNSMOS scores. Notably, our baseline solution training targeted an SI-SNR loss, thus better relative SI-SNR performance may be expected. Nonetheless, it is encouraging to see substantial DNSMOS improvement over the unprocessed noisy input in a system not trained specifically for perceptual quality. And importantly, the SDNN solution is an order of magnitude more efficient than the NsNet2 baseline in terms of the power proxy even though it processes data at a throughput 1.25× higher than the NsNet2 baseline, and it uses 5× fewer parameters. The quantization-aware training of the baseline SDNN solution further reduces the model size by 22× compared to NsNet2.

Naturally, the NsNet2 solution is a baseline and does not represent state-of-the-art for audio denoising today. For example, the Intel production DNS model (Intel DNS network) achieves higher SI-SNR and DNSMOS than both NsNet2 and the SDNN baseline solution (Table II). Given the simplicity of our SDNN baseline solution as a starting point for neuromorphic audio denoising, we believe it will be possible to significantly improve its denoising quality while also reducing its computational resources with further algorithmic innovations in the Intel N-DNS Challenge.

![](figures/f7ae816676794ab710402694e4449781a7386d2c6198056e3e9f937f986cdb5f.jpg)  
Figure 4. Sigma-delta neural network baseline solution structure.

Table II  
EVALUATION METRICS COMPARISON.

<table><tr><td rowspan="2">Network</td><td rowspan="2">SI-SNR dB</td><td colspan="2">SI-SNRi</td><td colspan="3">DNSMOS $^{\ddagger}$ </td><td colspan="2">Latency</td><td rowspan="2">Power proxy M-Ops/s</td><td rowspan="2">PDP proxy M-Ops</td><td rowspan="2">Param count  $\times 10^{3}$ </td><td rowspan="2">Model size KB</td></tr><tr><td>data dB</td><td>enc+dec dB</td><td>OVRL</td><td>SIG</td><td>BAK</td><td>enc+dec $^{\dagger}$  ms</td><td>total ms</td></tr><tr><td>Microsoft NsNet2</td><td>11.89</td><td>4.26</td><td>4.26</td><td>2.95</td><td>3.27</td><td>3.94</td><td>0.024</td><td>20.024</td><td>136.13</td><td>2.72</td><td>2,681</td><td>10,500</td></tr><tr><td>Intel DNS network</td><td>12.71</td><td>5.09</td><td>5.09</td><td>3.09</td><td>3.35</td><td>4.08</td><td>0.036</td><td>32.036</td><td>-</td><td>-</td><td>1,901</td><td>3,802</td></tr><tr><td>SDNN baseline</td><td>12.50</td><td>4.88</td><td>4.88</td><td>2.71</td><td>3.21</td><td>3.46</td><td>0.036</td><td>32.036</td><td>14.54</td><td>0.44</td><td>525</td><td>465</td></tr><tr><td>Validation set (noisy)</td><td>7.62</td><td>-</td><td>-</td><td>2.45</td><td>3.19</td><td>2.72</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td></tr><tr><td></td><td colspan="6">higher is better ( $\uparrow$ )</td><td colspan="6">lower is better ( $\downarrow$ )</td></tr></table>

lower is better (↓)  
<sup>†</sup> Latency results measured on a system with Intel(R) Xeon(R) Platinum 8280 CPU @ 2.70GHz and 32 GB RAM as of Feb 2023 and may not reflect all publicly available security updates. Results may vary.  
<sup>‡</sup> Please note that the DNSMOS scores in this table are not directly comparable to the DNSMOS scores presented in the results of the Microsoft DNS Challenge due to differing composition of validation/test sets.

Notably, the sigma-delta approach in our baseline solution is quite general. Sigma-delta sparsification can be applied to any conventional ReLU-like nonlinearity as well as to the dynamics present in typical neuromorphic neuron models such as leaky integrators and resonators. Furthermore, sigma-delta sparsification represents just one neuromorphic feature available of many to exploit by participants in the challenge. We see a wide space of uncharted waters to explore for the Intel N-DNS Challenge. Our baseline solution represents just a first step, and we find it encouraging that it already provides promising results.

## VIII. ADDITIONAL INFORMATION

Please see the Intel N-DNS Challenge Github Repository for the official competition rules, timeline, registration procedure, metrics boards, code, and datasets. Any additional clarifications that may arise during the challenge will be posted there.

## IX. CONCLUSION

We introduce the Intel Neuromorphic DNS Challenge to fulfill a vital need for a widely-applicable challenge problem that facilities algorithm innovation leading to a clear demonstration of neuromorphic hardware benefits.

We include two tracks to encourage (1) algorithmic innovation and (2) demonstration on neuromorphic hardware, and we specify task performance metrics and computational cost metrics to make it easy to compare different solutions. Furthermore, we provide permissively-licensed dataloader scripts, evaluation scripts, and an example neuromorphic baseline solution for accessibility, convenience, consistency, and extensibility. We also offer a monetary prize to encourage participation.

We look forward to the learnings that we gain as a community through the Intel N-DNS Challenge, both in terms of the innovation that occurs in the solution space, as well as the insights that can inform the development of future neuromorphic challenge problems.

## REFERENCES

[1] M. Davies, A. Wild, G. Orchard, Y. Sandamirskaya, G. A. F. Guerra, P. Joshi, P. Plank, and S. R. Risbud, “Advancing neuromorphic computing with Loihi: A survey of results and outlook,” Proceedings of the IEEE, vol. 109, no. 5, pp. 911–934, 2021.

[2] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,” Proceedings of the IEEE, vol. 86, no. 11, pp. 2278–2324, 1998.

[3] A. Krizhevsky, G. Hinton, et al., “Learning multiple layers of features from tiny images,” 2009.

[4] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, “ImageNet: A large-scale hierarchical image database,” in 2009 IEEE conference on computer vision and pattern recognition, pp. 248–255, 2009.

[5] C. Tan, S. Lallee, and G. Orchard, “Benchmarking neuromorphic vision: lessons learnt from computer vision,” Frontiers in neuroscience, vol. 9, p. 374, 2015.

[6] M. Davies, “Benchmarks for progress in neuromorphic computing,” Nature Machine Intelligence, vol. 1, no. 9, pp. 386–388, 2019.

[7] B. Cramer, Y. Stradmann, J. Schemmel, and F. Zenke, “The Heidelberg spiking data sets for the systematic evaluation of spiking neural networks,” IEEE Transactions on Neural Networks and Learning Systems, pp. 1–14, 2020.

[8] G. Orchard, A. Jayawant, G. K. Cohen, and N. Thakor, “Converting static image datasets to spiking neuromorphic datasets using saccades,” Frontiers in neuroscience, vol. 9, p. 437, 2015.

[9] L. Fei-Fei, R. Fergus, and P. Perona, “Learning generative visual models from few training examples: An incremental bayesian approach tested on 101 object categories,” Computer Vision and Pattern Recognition Workshop, 2004.

[10] L. R. Iyer, Y. Chua, and H. Li, “Is neuromorphic MNIST neuromorphic? analyzing the discriminative power of neuromorphic datasets in the time domain,” Frontiers in neuroscience, vol. 15, p. 608567, 2021.

[11] A. Amir, B. Taba, D. Berg, T. Melano, J. McKinstry, C. D. Nolfo, T. Nayak, A. Andreopoulos, G. Garreau, M. Mendoza, J. Kusnitz, M. Debole, S. Esser, T. Delbruck, M. Flickner, and D. Modha, “A low power, fully event-based gesture recognition system,” in Proceedings of the IEEE conference on computer vision and pattern recognition, pp. 7243–7252, 2017.

[12] M. Yao, H. Gao, G. Zhao, D. Wang, Y. Lin, Z. Yang, and G. Li, “Temporal-wise attention spiking neural networks for event streams classification,” in Proceedings of the IEEE/CVF International Conference on Computer Vision, pp. 10221–10230, 2021.

[13] S. F. Muller-Cleve, V. Fra, L. Khacef, A. Pequeno-Zurro, D. Klepatsch, E. Forno, D. G. Ivanovich, S. Rastogi, G. Urgese, F. Zenke, et al., “Braille letter reading: A benchmark for spatio-temporal pattern recognition on neuromorphic hardware,” arXiv preprint arXiv:2205.15864, 2022.

[14] E. Ceolini, C. Frenkel, S. B. Shrestha, G. Taverni, L. Khacef, M. Payvand, and E. Donati, “Hand-gesture recognition based on EMG and eventbased camera sensor fusion: A benchmark in neuromorphic computing,” Frontiers in Neuroscience, p. 637, 2020.

[15] C. K. Reddy, V. Gopal, R. Cutler, E. Beyrami, R. Cheng, H. Dubey, S. Matusevych, R. Aichner, A. Aazami, S. Braun, et al., “The INTERSPEECH 2020 deep noise suppression challenge: Datasets, subjective testing framework, and challenge results,” arXiv preprint arXiv:2005.13981, 2020.

[16] C. K. A. Reddy, H. Dubey, V. Gopal, R. Cutler, S. Braun, H. Gamper, R. Aichner, and S. Srinivasan, “Icassp 2021 deep noise suppression challenge,” in ICASSP 2021-2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 6623–6627, 2021.

[17] C. K. A. Reddy, H. Dubey, K. Koishida, A. Nair, V. Gopal, R. Cutler, S. Braun, H. Gamper, R. Aichner, and S. Srinivasan, “INTERSPEECH 2021 deep noise suppression challenge,” arXiv preprint arXiv:2101.01902, 2021.

[18] H. Dubey, V. Gopal, R. Cutler, A. Aazami, S. Matusevych, S. Braun, S. E. Eskimez, M. Thakker, T. Yoshioka, H. Gamper, et al., “ICASSP 2022 deep noise suppression challenge,” in ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 9271–9275, 2022.

[19] S. Boll, “Suppression of acoustic noise in speech using spectral subtraction,” IEEE Trans. Acoust., Speech, Signal Processing, vol. 27, no. 2, pp. 113–120, 1979.

[20] Y. Ephraim and D. Malah, “Speech enhancement using a minimum-mean square error short-time spectral amplitude estimator,” IEEE Transactions on acoustics, speech, and signal processing, vol. 32, no. 6, pp. 1109–1121, 1984.

[21] T. Higuchi, N. Ito, T. Yoshioka, and T. Nakatani, “Robust MVDR beamforming using time-frequency masks for online/offline ASR in noise,” in 2016 IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2016, Shanghai, China, March 20-25, 2016, pp. 5210–5214, IEEE, 2016.

[22] T. Nakatani, T. Yoshioka, K. Kinoshita, M. Miyoshi, and B.-H. Juang, “Speech dereverberation based on variance-normalized delayed linear prediction.,” IEEE Trans. Speech Audio Process., vol. 18, no. 7, pp. 1717– 1731, 2010.

[23] D. Rethage, J. Pons, and X. Serra, “A wavenet for speech denoising,” 2017.

[24] Y. Luo and N. Mesgarani, “Conv-tasnet: Surpassing ideal time–frequency magnitude masking for speech separation,” IEEE/ACM transactions on audio, speech, and language processing, vol. 27, no. 8, pp. 1256–1266, 2019.

[25] Y. Hu, Y. Liu, S. Lv, M. Xing, S. Zhang, Y. Fu, J. Wu, B. Zhang, and L. Xie, “DCCRN: Deep complex convolution recurrent network for phase-aware speech enhancement,” 2020.

[26] P. Ochieng, “Deep neural network techniques for monaural speech enhancement: state of the art analysis,” 2022.

[27] T. Nakatani, C. Boeddeker, K. Kinoshita, R. Ikeshita, M. Delcroix, and R. Haeb-Umbach, “Jointly optimal denoising, dereverberation, and source separation,” IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 28, pp. 2267–2282, 2020.

[28] S. Zhao, T. H. Nguyen, and B. Ma, “Monaural speech enhancement with complex convolutional block attention module and joint time frequency losses,” in ICASSP 2021-2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 6648–6652, IEEE, 2021.

[29] Y. Koyama, T. Vuong, S. Uhlich, and B. Raj, “Exploring the best loss function for DNN-based low-latency speech enhancement with temporal convolutional networks,” arXiv preprint arXiv:2005.11611, 2020.

[30] D. Yin, C. Luo, Z. Xiong, and W. Zeng, “PHASEN: A phase-and harmonics-aware speech enhancement network,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 34, pp. 9458–9465, 2020.

[31] E. Tzinis, Z. Wang, and P. Smaragdis, “SuDo RM-RF: Efficient networks for universal audio source separation,” in 2020 IEEE 30th International Workshop on Machine Learning for Signal Processing (MLSP), pp. 1–6, IEEE, 2020.

[32] S. Braun and I. Tashev, “Data augmentation and loss normalization for deep noise suppression,” in Speech and Computer: 22nd International Conference, SPECOM 2020, St. Petersburg, Russia, October 7–9, 2020, Proceedings 22, pp. 79–86, Springer, 2020.

[33] Q. Li, F. Gao, H. Guan, and K. Ma, “Real-time monaural speech enhancement with short-time discrete cosine transform,” arXiv preprint arXiv:2102.04629, 2021.

[34] S. Braun and M. L. Valero, “Task splitting for DNN-based acoustic echo and noise removal,” in 2022 International Workshop on Acoustic Signal Enhancement (IWAENC), pp. 1–5, IEEE, 2022.

[35] S. Braun and I. Tashev, “A consolidated view of loss functions for supervised deep learning-based speech enhancement,” in 2021 44th International Conference on Telecommunications and Signal Processing (TSP), pp. 72–76, IEEE, 2021.

[36] E. Tzinis, Y. Adi, V. K. Ithapu, B. Xu, P. Smaragdis, and A. Kumar, “Remixit: Continual self-training of speech enhancement models via bootstrapped remixing,” IEEE Journal of Selected Topics in Signal Processing, vol. 16, no. 6, pp. 1329–1341, 2022.

[37] Femtosense Inc., “AI speech enhancement for hearing aids,” 2022. https: //femtosense.ai/ai-speech-enhancement-for-hearing-aids/.

[38] A. Mehonic and A. J. Kenyon, “Brain-inspired computing needs a master plan,” Nature, vol. 604, no. 7905, pp. 255–260, 2022.

[39] C. D. Schuman, S. R. Kulkarni, M. Parsa, J. P. Mitchell, B. Kay, et al., “Opportunities for neuromorphic computing algorithms and applications,” Nature Computational Science, vol. 2, no. 1, pp. 10–19, 2022.

[40] W. Wan, R. Kubendran, C. Schaefer, S. B. Eryilmaz, W. Zhang, D. Wu, S. Deiss, P. Raina, H. Qian, B. Gao, et al., “A compute-in-memory chip based on resistive random-access memory,” Nature, vol. 608, no. 7923, pp. 504–512, 2022.

[41] A. Neckar, S. Fok, B. V. Benjamin, T. C. Stewart, N. N. Oza, A. R. Voelker, C. Eliasmith, R. Manohar, and K. Boahen, “Braindrop: A mixed-signal neuromorphic architecture with a dynamical systems-based programming model,” Proceedings of the IEEE, vol. 107, no. 1, pp. 144– 164, 2018.

[42] C. Frenkel, M. Lefebvre, J.-D. Legat, and D. Bol, “A 0.086-mm<sup>2</sup> 12.7- pj/sop 64k-synapse 256-neuron online-learning digital spiking neuromorphic processor in 28-nm cmos,” IEEE transactions on biomedical circuits and systems, vol. 13, no. 1, pp. 145–158, 2018.

[43] J. Schemmel, S. Billaudelle, P. Dauer, and J. Weis, “Accelerated analog neuromorphic computing,” in Analog Circuits for Machine Learning, Current/Voltage/Temperature Sensors, and High-speed Communication: Advances in Analog Circuit Design 2021, pp. 83–102, Springer, 2021.

[44] N. Qiao, H. Mostafa, F. Corradi, M. Osswald, F. Stefanini, D. Sumislawska, and G. Indiveri, “A reconfigurable on-line learning spiking neuromorphic processor comprising 256 neurons and 128k synapses,” Frontiers in neuroscience, vol. 9, p. 141, 2015.

[45] F. Akopyan, J. Sawada, A. Cassidy, R. Alvarez-Icaza, J. Arthur, P. Merolla, N. Imam, Y. Nakamura, P. Datta, G.-J. Nam, et al., “TrueNorth: Design and tool flow of a 65 mw 1 million neuron programmable neurosynaptic chip,” IEEE transactions on computer-aided design of integrated circuits and systems, vol. 34, no. 10, pp. 1537–1557, 2015.

[46] M. Davies, N. Srinivasa, T.-H. Lin, G. Chinya, Y. Cao, S. H. Choday, G. Dimou, P. Joshi, N. Imam, S. Jain, et al., “Loihi: A neuromorphic manycore processor with on-chip learning,” Ieee Micro, vol. 38, no. 1, pp. 82–99, 2018.

[47] J. Pei, L. Deng, S. Song, M. Zhao, Y. Zhang, S. Wu, G. Wang, Z. Zou, Z. Wu, W. He, et al., “Towards artificial general intelligence with hybrid Tianjic chip architecture,” Nature, vol. 572, no. 7767, pp. 106–111, 2019.

[48] S. B. Furber, F. Galluppi, S. Temple, and L. A. Plana, “The SpiNNaker project,” Proceedings of the IEEE, vol. 102, no. 5, pp. 652–665, 2014.

[49] S. Furber and P. Bogdan, SpiNNaker-a spiking neural network architecture. Now publishers, 2020.

[50] Intel Corporation, “Technology Brief Intel Labs’ Loihi 2 neuromorphic research chip and the Lava software framework,” 2021. https://download.intel.com/newsroom/2021/new-technologies/ neuromorphic-computing-loihi-2-brief.pdf.

[51] E. R. Kandel, J. H. Schwartz, T. M. Jessell, S. Siegelbaum, A. J. Hudspeth, S. Mack, et al., Principles of neural science, vol. 4. McGraw-hill New York, 2000.

[52] G. Orchard, E. P. Frady, D. Rubin Ben Dayan, S. Sanborn, S. B. Shrestha, F. T. Sommer, and M. Davies, “Efficient neuromorphic signal processing with Loihi 2,” in 2021 IEEE Workshop on Signal Processing Systems (SiPS), pp. 254–259, IEEE, 2021.

[53] N. Perez-Nieves, V. C. Leung, P. L. Dragotti, and D. F. Goodman, “Neural heterogeneity promotes robust learning,” Nature communications, vol. 12, no. 1, p. 5791, 2021.

[54] C. Kayser, N. K. Logothetis, and S. Panzeri, “Millisecond encoding precision of auditory cortex neurons,” Proc Natl Acad Sci U S A, vol. 107, pp. 16976–16981, Sept. 2010.

[55] W. Bialek and H. P. Wit, “Quantum limits to oscillator stability: Theory and experiments on acoustic emissions from the human ear,” Physics Letters A, vol. 104, no. 3, pp. 173–178, 1984.

[56] S. Martignoli, F. Gomez, and R. Stoop, “Pitch sensation involves stochastic resonance,” Sci Rep, vol. 3, p. 2676, 2013.

[57] J. Anumula, D. Neil, T. Delbruck, and S.-C. Liu, “Feature representations for neuromorphic audio spike streams,” Frontiers in neuroscience, vol. 12, p. 23, 2018.

[58] S. Y. A. Yarga, J. Rouat, and S. Wood, “Efficient spike encoding algorithms for neuromorphic speech recognition,” in Proceedings of the International Conference on Neuromorphic Systems 2022, (New York, NY, USA), Association for Computing Machinery, 2022.

[59] K. Grö, chenig, Foundations of time-frequency analysis. Springer Science Business Media, 2001.

[60] L. Rabiner and B.-H. Juang, Fundamentals of speech recognition. Prentice-Hall, Inc., 1993.

[61] M. O. Magnasco, “A wave traveling over a hopf instability shapes the cochlear tuning curve,” Phys. Rev. Lett., vol. 90, p. 058101, Feb 2003.

[62] A. J. Hudspeth, F. Jülicher, and P. Martin, “A critique of the critical cochlea: Hopf—a bifurcation—is better than none,” Journal of Neurophysiology, vol. 104, no. 3, pp. 1219–1229, 2010.

[63] M. S. Zilany, I. C. Bruce, and L. H. Carney, “Updated parameters and expanded simulation options for a model of the auditory periphery,” The Journal ofthe Acoustical Society ofAmerica, vol. 135, no. 1, pp. 283–286, 2014.

[64] M. R. DeWeese, M. Wehr, and A. M. Zador, “Binary spiking in auditory cortex,” J Neurosci, vol. 23, pp. 7940–7949, Aug. 2003.

[65] E. Smith and M. S. Lewicki, “Efficient coding of time-relative structure using spikes,” Neural Comput, vol. 17, pp. 19–45, Jan. 2005.

[66] P. Blouw, X. Choo, E. Hunsberger, and C. Eliasmith, “Benchmarking keyword spotting efficiency on neuromorphic hardware,” in Proceedings of the 7th annual neuro-inspired computational elements workshop, pp. 1– 8, 2019.

[67] B. Yin, F. Corradi, and S. M. Bohté, “Effective and efficient computation with multiple-timescale spiking recurrent neural networks,” in International Conference on Neuromorphic Systems 2020, pp. 1–8, 2020.

[68] S. B. Shrestha, L. Zhu, and P. Sun, “Spikemax: Spike-based loss methods for classification,” in 2022 International Joint Conference on Neural Networks (IJCNN), pp. 1–7, 2022.

[69] F. Bahmaninezhad, J. Wu, R. Gu, S.-X. Zhang, Y. Xu, M. Yu, and D. Yu, “A comprehensive study of speech separation: spectrogram vs waveform separation,” arXiv preprint arXiv:1905.07497, 2019.

[70] J. Le Roux, S. Wisdom, H. Erdogan, and J. R. Hershey, “SDR–half-baked or well done?,” in ICASSP 2019-2019 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 626–630, IEEE, 2019.

[71] C. K. Reddy, V. Gopal, and R. Cutler, “DNSMOS P. 835: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors,” in ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 886–890, IEEE, 2022.

[72] A. W. Rix, J. G. Beerends, M. P. Hollier, and A. P. Hekstra, “Perceptual evaluation of speech quality (PESQ)-a new method for speech quality assessment of telephone networks and codecs,” in 2001 IEEE international conference on acoustics, speech, and signal processing. Proceedings (Cat. No. 01CH37221), vol. 2, pp. 749–752, IEEE, 2001.

[73] J. G. Beerends, C. Schmidmer, J. Berger, M. Obermann, R. Ullmann, J. Pomy, and M. Keyhl, “Perceptual objective listening quality assessment (POLQA) , the third generation itu-t standard for end-to-end speech quality measurement part ii – perceptual model,” 2013.

[74] A. Hines, J. Skoglund, A. Kokaram, and N. Harte, “ViSQOL: an objective speech quality model,” EURASIP Journal on Audio, Speech, and Music Processing, vol. 2015 (13), pp. 1–18, 2015.

[75] C. H. Taal, R. C. Hendriks, R. Heusdens, and J. Jensen, “An algorithm for intelligibility prediction of time–frequency weighted noisy speech,” IEEE Transactions on Audio, Speech, and Language Processing, vol. 19, no. 7, pp. 2125–2136, 2011.

[76] P. O’Connor and M. Welling, “Sigma delta quantized networks,” in International Conference on Learning Representations, 2017.

[77] S. B. Shrestha and G. Orchard, “SLAYER: Spike layer error reassignment in time,” in Advances in Neural Information Processing Systems 31 (S. Bengio, H. Wallach, H. Larochelle, K. Grauman, N. Cesa-Bianchi, and R. Garnett, eds.), pp. 1412–1421, Curran Associates, Inc., 2018.

[78] E. O. Neftci, H. Mostafa, and F. Zenke, “Surrogate gradient learning in spiking neural networks: Bringing the power of gradient-based optimization to spiking neural networks,” IEEE Signal Processing Magazine, vol. 36, no. 6, pp. 51–63, 2019.