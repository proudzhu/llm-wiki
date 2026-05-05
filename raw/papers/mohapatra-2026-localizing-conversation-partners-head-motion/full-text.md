Payal Mohapatra [payal.mohapatra@nortwhestern.edu](https://arxiv.org/html/2604.23927v1/mailto:payal.mohapatra@nortwhestern.edu) Northwestern UniversityEvanstonIllinoisUSA, Calvin Murdock Meta Reality LabsRedmondUSA, Ali Aroudi Meta Reality LabsRedmondUSA, Ishwarya Ananthabhotla Meta Reality LabsRedmondUSA, Anjali Menon Meta Reality LabsRedmondUSA, Buye Xu Meta Reality LabsRedmondUSA and Morteza Khaleghimeybodi [morteza@meta.com](https://arxiv.org/html/2604.23927v1/mailto:morteza@meta.com) Meta Reality LabsRedmondUSA

(2018)

###### Abstract.

Many individuals struggle to understand their conversation partners in noisy settings, particularly amidst background speakers or due to hearing impairments. Under such circumstances, emerging wearables like smartglasses offer a transformative opportunity to enhance speech from conversation partners. Crucial to this is the ability to identify the direction in which the user is interested in listening, which we refer to as the user’s acoustic zones of interest. While current spatial audio-based methods are effective in resolving the direction of vocal input, they are agnostic to the user’s listening preferences and have limited functionality in noisy settings and when interfering speakers are present. To address this, there is a need to actively incorporate behavioral cues for inferring a user’s acoustic zones of interest. Motivated by this need, we explore the effectiveness of the user’s head-orienting behavior, captured by the Inertial Measurement Units (IMUs) on smartglasses, as a modality for localizing acoustic zones of interest in seated conversations. We introduce HALo, a head-orientation-based acoustic zone localization network that leverages smartglasses’ IMUs to non-invasively infer auditory zones of interest corresponding to conversation partner locations. By integrating an *a priori* estimate of the number of conversation partners, our approach demonstrates a 21% performance improvement over existing methods. We complement this with CoCo, which classifies the number of conversation partners using only IMU data, achieving an accuracy of 0.74; compared to rule-based and generic time-series models, this yields a 35% gain in task performance. We discuss practical considerations for feature extraction and inference and provide qualitative analyses over extended sessions. We also demonstrate a minimal end-to-end speech enhancement system and show that a head-orientation-based localization scheme can offer clear advantages in extremely noisy settings with multiple conversation partners. Our work demonstrates the feasibility of a non-visual behavioral modality for inferring users’ conversational preferences with minimal sensing requirements, and highlights its potential to enhance conversational immersiveness through smartglasses.

Smartglasses, Head Orientation from IMUs, Behavioral Speech Enhancement Selection, Acoustic Zones of Interest, Immersive Hearing, Augmented Hearing

## 1\. INTRODUCTION

![Refer to caption](figures/fig1-cover.png)

Figure 1. Concept: Using IMU sensors on smartglasses to extract the head-orienting patterns of the user during a conversational setting to identify the user’s acoustic zones of interest (which are indicative of the conversation partners’ locations). Potential use cases: Consider a large multiparty noisy setting (e.g., a restaurant) with interfering/background speakers. The user (shown wearing smartglasses) engages with a preferred subgroup. These conversation partners are shown in blue. A technology that leverages user behavior-driven localization of conversation partners as proposed in this work (1) can support hearing-impaired users through directional speech enhancement based on their listening preferences, (2) can support a user’s intentional engagement with preferred conversation partners in a large conversation group, and (3) provides robust performance under noisy acoustics and in the presence of interfering speakers.

Group conversations are central to daily social life, yet individuals with hearing impairments [^91] [^28] [^58] or hearing fatigue in noisy environments [^57] [^52] encounter significant barriers to effective communication. Traditional approaches to improving speech intelligibility typically enhance the signal-to-noise ratio (SNR) through beamforming, spatial filtering, or neural network-based speech enhancement techniques [^69] [^95] [^11] [^102]. The recent proliferation of smartglasses as a ubiquitous wearable platform presents an opportunity to redefine the conversational experience by deploying on-device beamforming or neural network-based speech enhancement algorithms [^80] [^54] [^58], which preserve signals from a target direction while attenuating those from other directions. Determining the target direction of interest—particularly accounting for the listener’s preferences for conversation partners—is crucial for the success of such technology [^12]. However, current audio-based modalities do not incorporate user preferences, may inadvertently amplify interfering speakers, and often exhibit limited functionality under noisy or non-ideal acoustic conditions [^4]. This highlights the need to explore alternative behavioral modalities that can implicitly infer listeners’ preferences and guide conversation-enhancing algorithms [^80] [^54]. Motivated by this practical need, in this work we investigate the head motion of the listener as a feasible modality to infer acoustic zones of interest using smartglasses, which approximate the locations of conversation partners. Acoustic zones of interest are defined based on a discretized representation of azimuth angles relative to the listener’s average facing direction.

Identifying the spatial locations of conversation partners is a foundational task for enabling immersiveness in conversational settings using smartglasses. Prior works [^25] [^99] [^8] largely leverage spatial audio-based techniques (captured using microphone arrays) to determine speaker locations. While these methods are generally successful, they are prone to misidentifying interfering speakers, are susceptible to background noise, and fail to account for a listener’s preferences for instance listener’s preference towards a fixed subgroup of speakers in large multi-party conversations as illustrated in Figure 1. This highlights the need to identify conversation partners specifically, rather than all speakers in the scene. Some proposed methods address these shortcomings by incorporating egocentric visual modalities for better contextualization [^13] [^43]. While these methods offer superior performance for identifying and localizing conversation partners under noisy conditions, they can be intrusive in social settings and demand significant computational resources, making them infeasible for wearable platforms.

Beyond audio-visual modalities, recent works in speaker localization have shown the benefit of incorporating behavioral modalities like head-orientation and gaze either as a proxy for ground-truth annotations to enable more large-scale self-supervised training [^71] or as a mode of understanding the visual focus of attention using gaze [^47] [^68] [^86]. This motivates us to leverage existing on-device sensors to capture orienting behaviors and provide better context for user preferences. Parallely, extensive literature [^93] [^55] [^56] [^34] [^7] in auditory neuroscience also highlight the role of head orientation as a useful modality for linguistic behaviors in controlled settings with manual annotations on small-scale datasets. Some works like [^49] have extended these neuroscience results to consider behavioral modalities independently by formulating tasks like active speaker selection from a given set of speaker locations based on head orientations, or understanding how group dynamics can help in determining accurate head orientations [^92]. However, much of this orienting information is derived from egocentric or exocentric videos, which do not address the constraints of relying on visual modalities for wearable platforms. Some works have used self-voice-based head orientation detection using external microphones [^105], which may fail under multiple speaker scenarios in a typical conversation setting. Thus, the challenge of determining acoustic zones of interest independent of prior knowledge of the number of speakers and their original precise locations remains an unexplored but important setting. In this work, we investigate this challenging question: What is the potential of using only head orientation information to determine a listener’s acoustic zones of interest in natural conversations?

We propose a novel task of leveraging commonly available sensors on smart glasses, such as IMUs, to detect conversation-focused orienting behaviors and infer the listener’s acoustic zones of interest. An overview is illustrated in Figure 1. However, there are several challenges in successfully leveraging head orientation to identify acoustic zones of interest. First, as a behavioral modality, it is inherently weak in explicitly capturing linguistic behaviors and is instead coupled with other behavioral attributes that may not be relevant to our task of acoustic zone localization (e.g., looking at one’s shoes, eating with the face down, fiddling with fingers, etc.) [^34] [^26]. Extracting patterns of interest requires careful construction of the relevant input features and target formulation. Second, IMU sensors suffer from sensor drift, which makes it challenging to rely on longer observation periods for predictions. Leveraging translational information is particularly difficult under these conditions. Finally, the relationship between a speaker talking and a listener orienting themselves in the speaker’s direction is not tightly causal, varies across individuals, and is heavily dependent on conversation dynamics [^7] [^26], which makes it generally hard to learn precise acoustic zones purely from head orientation.

Given the complex nature of head-orienting behaviors, simple rule-based statistical methods are insufficient to capture natural conversation-focused patterns. In this work, we show that by constructing suitable proxy tasks, it is possible to infer acoustic zones of interest with minimal prior assumptions. We first localize the acoustic zones of interest under the assumption that the number of conversation partners is known. We then relax this assumption by optimizing a secondary objective that classifies the number of conversation partners. Finally, we integrate these methods into an end-to-end system and demonstrate their robustness under practical conditions, including the availability of abstract audio features—coarse speaking-behavior signals such as listener speaking status and partner talkativeness, which are commonly available in speech enhancement systems [^48] and do not require spectrograms or high-dimensional feature processing—as well as shorter analysis windows and IMU sensor drift. We validate our approach on a large real-world dataset comprising diverse multiparty conversational layouts and natural listening–speaking dynamics. Our key contributions are:

(1) We propose a novel task of localizing conversation partners based on listener preferences using head orientation as a behavioral modality, captured from on-device IMUs in smart glasses to support speech-enhancement applications. We demonstrate the effectiveness of our approach on a large-scale dataset (N > 70) with unconstrained, natural conversations, designed to provide meaningful findings in practical settings.

(2) To address the challenges inherent in behavioral modalities, we propose the Head-orientation-based Acoustic-zones Localization (HALo) network, which formulates the prediction of conversation partners’ spatial locations—overlapping with the listener’s acoustic zones of interest—as a sequence-to-multilabel classification problem. HALo achieves an average accuracy of 0.78 and a macro-F1 of 0.62, representing a 24% average improvement over rule-based and general-purpose baselines. To further reduce reliance on static prior knowledge for localization, we introduce the Classifying the number of Conversation partners (CoCo) network, which attains an average accuracy of 0.74, yielding a 25% improvement over comparable baselines.

(3) Finally, we present a comprehensive evaluation of our proposed methods and introduce HALo-CoCo, an end-to-end training strategy that localizes acoustic zones by estimating the number of conversation partners in a stage-wise manner. We demonstrate the effectiveness of our approach across diverse practical scenarios through extensive ablation studies, qualitative analyses, and a minimal speech-enhancement pipeline, providing intuitive insights into our formulation and adopted methodology.

## 2\. Related Works

### 2.1. Linguistic Significance of Head-Orientations

Psychoacoustic literature extensively explores the communicative and motoric uses of head movement, ranging from its potential to indicate aggressiveness in the speaker [^24], hearing and eyesight impairments [^84], or speech pathology disorders [^32], to turn-taking behaviors [^93] [^55] [^18]. Past studies [^90] also highlight the phenomenon of undershooting in orienting behavior relative to the speaker’s location. Additionally, leveraging this modality presents challenges due to variability in the finite reaction time between orienting behavior and a conversation partner’s speaking status, as well as cultural biases [^55]. Most of these studies have been conducted in controlled settings, typically with small datasets ($N<10$) and manual annotations. Drawing inspiration from auditory neuroscience findings, this work aims to develop a data-driven method that leverages head-orienting behaviors to infer a user’s auditory attention zones. Our multilabel classification formulation, using fixed-length observation segments and discrete acoustic zones as the targets, addresses the delayed responses and undershooting tendencies established in prior behavioral studies [^90] [^55].

### 2.2. Methods for Head Orientation Estimation

Several wearable and IoT applications benefit from continuously monitoring a user’s head orientation. Audio-based methods, such as using binaural microphones [^106], multiple microphone arrays [^21] [^104], or even wall reflections [^85], have shown promise in determining the head-orientation of a person. Another class of methods involves using exocentric videos to track and determine head orientation [^33]; however, beyond privacy and energy constraints, visual modalities also suffer from occlusion effects. Some works have explored using egocentric visual data for pose estimation of the wearer [^42] [^94]. In this work, our focus is on leveraging a behavioral modality that conserves power and does not use visual modalities. Some studies have proposed dedicated methods to measure accurate head pose for medical applications, such as cephalometric analyses for diagnosis [^51]. Inspired by prior works [^1] [^5] that have validated head-mounted IMUs as a viable modality for head orientation estimates, we utilize on-device IMU sensors on smartglasses. In this study, we extract approximate head orientation sequences provide an algorithmic solution for identifying a user’s acoustic zones of interest with minimal instrumentation overhead.

### 2.3. Gaze and Head-orientation-based User Interfaces

Several studies have explored behavioral modalities, such as gaze [^107] [^87] and head orientation [^86] [^105], as user-interface gestures. In particular, head orientation has recently emerged as a promising modality for contextualizing voice-assisted devices [^105], functioning as a non-verbal command for earbuds [^40] [^29], human activity recognition [^59] [^89] and overall improving the contextual understanding of intelligent systems [^70]. Unlike prior work on gesture identification with clear labels, this study seeks to uncover implicit, conversation-driven patterns in natural head movements—which lack direct ground-truth supervision during training—in order to determine a user’s acoustic zones of interest, making the task significantly more challenging.

### 2.4. Conversation Enhancement using Smartglasses

![Refer to caption](figures/fig2-application-motivation.png)

Figure 2. Current smartglasses technologies (Left) constrain speech enhancement to the user’s frontal-facing direction, disregarding the user’s acoustic zones of interest. Our proposed approach (Right) shows that we can use natural head-orienting behavior to identify the acoustic zones of interest, enabling future applications to create a truly immersive conversational experience.

An emerging application of smartglasses is to provide conversation enhancement [^112] [^102] [^63] —enhancing sound source from a desired direction and reducing background noise. Currently, this desired direction is primarily determined using two approaches: (1) the user’s front-facing direction, or (2) a microphone array on the smart glasses to identify all speech sound sources. The first approach, which uses the user’s frontal direction as the conversation-enhancing direction, requires the user to proactively look toward the speaker they wish to focus on, which can be disruptive to the overall conversational experience. The second approach, which relies on a microphone array as described in earlier sections, faces limitations in the presence of interfering speakers and under noisy or non-ideal acoustic conditions. Additionally, for users with hearing difficulties, these existing methods pose substantial challenges, especially when smartglasses are intended to serve as hearing aids themselves [^58] in some applications. This critical limitation presents a compelling opportunity to develop more intuitive methods for inferring the direction in which users want speech enhancement. As illustrated in Figure 2, future conversational enhancement technologies must be guided by the user’s listening preferences to truly improve the immersiveness of their interaction. In this work, we propose a novel approach using head-orientation-based acoustic zones of interest localization, which addresses the fundamental challenge of identifying a suitable behavioral modality for understanding a user’s conversational focus.

## 3\. APPROACH

In this section, we present our approach, starting with an overview of the study dataset and data preparation steps, followed by an illustrative example to motivate our task formulations and describe our design methodology. We then introduce the acoustic zone localization network, HALo, and the classification network CoCo used to determine the number of conversation partners. For each component, we discuss the associated practical challenges and provide the underlying design rationale.

### 3.1. Study Dataset

We used the Reality Labs Research Conversations for Hearing Augmentation Technology (RLR-CHAT) dataset [^108] [^110] [^71] [^35] for our study. Researchers collected this data from participants aged 20 to 60 years, including individuals with mild hearing loss. The participants engaged in natural group conversations while seated in arbitrary layouts, with group sizes ranging from 2 to 5 participants. During the conversations, eight loudspeakers surrounded the participants and played cafeteria noise that changed pseudo-randomly every 25–35 seconds at four levels: no noise (quiet), 55, 65, and 75 dBA, covering a range of real-world listening conditions [^100]. The dataset included a balanced distribution of noise levels.

We used the IMU data streamed from the Aria <sup>1</sup> smart glasses [^19] as our primary input. The IMU is located on the right leg of the glasses and sampled at 1000 Hz. We used an optical motion tracking system, OptiTrack [^73] [^72], to obtain ground-truth annotations, sampled at 120 Hz. Additionally, to demonstrate the advantages of using simpler audio modalities, we included the speaking and non-speaking states of all participants, which are computationally less expensive to obtain compared to multi-channel audio processing.

To ensure alignment across modalities, we used a manually validated subset of the dataset, similar to previous works [^110] [^71], which included 71 participants from 36 unique sessions, each lasting approximately 1 hour. Here each session is aligned across different modalities in 30-second segments with standard IMU processing [^19] to compensate for time-invariant sensor differences across the smart glasses. A fisheye lens recorded video at 5 frames per second, and all modalities are downsampled to this frame rate to further processing to facilitate qualitative validation using a synchronized visual reference. Head rotation frequency of 1 Hz is physiologically considered moderate activity, while rare and vigorous head movements occur at approximately 2.6 Hz [^31]. Thus, downsampling IMU data to 5 Hz captures the relevant head motion behaviors required for conversation partners location tasks. In this work, we refer to the participant whose vantage point is considered as the focal user, while the others are referred to as conversation partners. Figure 24 in the Appendix illustrates an overview of our dataset’s organization.

Table 1 presents a comparative summary, highlighting how RLR-CHAT differs from other datasets that have used wearable devices to capture human kinematics in conversational settings. While these datasets vary in size and behavioral tasks, RLR-CHAT stands out as the only one that incorporates IMU streams from wearable smart glasses specifically designed for natural conversation scenarios at a large scale (64 hours). This distinction enables us to investigate deep-learning formulations that leverage head orientation, captured using IMU sensors, as the primary modality for identifying the focal user’s acoustic zones of interest.

Table 1. Summary of conversational datasets utilizing wearable modalities to capture human kinematics across various conversational contexts for N number of participants.

| Dataset | Form-factor: Kinematics Modality | N | Hours | Group Size | Conversation Context |
| --- | --- | --- | --- | --- | --- |
| MatchnMingle [^9] | Badge/Pendant: Tri-axial Acceleration | 92 | 20 | 2 | Free-standing speed-dating |
| SALSA [^2] | Badge/Pendant: Tri-axial Acceleration | 18 | 6 | 2-3 | Free-standing poster-sessions |
| Cattuto et al. [^10] | Badge/Pendant: Radio-Frequency Identification (RFID) | 575 | 12 | 2 | One-on-one conversations |
| Matic et al. [^53] | Mobile Phone: Tri-axial Acceleration | 50 | 8 | 2-4 | Controlled social interactions |
| Hung et al. [^39] [^30] | Custom Tri-axial Accelerometer | 9 | 2 | 2 | Controlled social interactions |
| Ferlini et al. [^23] | Earbuds: 6-axis accelerometer and gyroscope | 10 | 1 | 2 | Controlled conversation |
| RLR-Chat (ours) [^108] [^110] [^71] | Smart-glasses: 6-axis accelerometer and gyroscope | 71 | 64 | 2-5 | Natural seated conversation |

### 3.2. Overview of Data Preparation: Head Orientation Approximation from IMUs

The continuous angular velocity, $\boldsymbol{\omega}(t)$, is sampled at discrete regular intervals of $\Delta t$, where the instantaneous angular velocity at a discrete time $t_{n}=n\Delta t$ is given as, $\boldsymbol{\omega}(t_{n})=[\omega_{x},\omega_{y},\omega_{z}]^{\mathrm{T}}$. To estimate the angular displacement of the head, we leverage a simple attitude integration scheme as described by [^41] using a quaternion representation $\mathbf{q}\in\mathbb{R}^{4}$ [^88]. Leveraging key results from [^41], we can describe the change in rotation, $\Delta\mathbf{q}$, about the instantaneous axis, $\mathbf{u}=\frac{\boldsymbol{\omega}}{\|\boldsymbol{\omega}\|}$ during $\Delta t$ time units in the IMU’s local time frame (rad/seconds in this case) as:

$$
\Delta\mathbf{q}=\cos\frac{\theta}{2}+\mathbf{u}\sin\frac{\theta}{2}=\cos\frac{\|\boldsymbol{\omega}\|\Delta t}{2}+\frac{\boldsymbol{\omega}}{\|\boldsymbol{\omega}\|}\sin\frac{\|\boldsymbol{\omega}\|\Delta t}{2}.
$$

We can consider the original state as $\mathbf{q}(t)$ rotated to a new state $\mathbf{q}(t+\Delta t)=\Delta\mathbf{q}\,\mathbf{q}(t)$ [^41]. We leverage [^88] ’s results to arrive at the closed form solution for the new rotation, $\mathbf{q}_{t+1}$. A detailed derivation and implementation details, including the overall pseudocode in Algorithm 1, are provided in Section A.2 of the Appendix.

After computing the final rotation matrix (step 26 of Algorithm 1 in the Appendix), we transform a point, $\mathbf{v}_{\text{init\_xyz}}$, in the Cartesian plane to $\mathbf{v}_{\text{fin\_ae}}$ in the spherical coordinate system (as shown in Algorithm 2 in the Appendix) using standard techniques [^97] under some assumptions: assign $d$, the radius in spherical coordinates, to 1; assume the average front-facing direction of the focal user is the origin, i.e., (azimuth, elevation) = $(0^{\circ},0^{\circ})$; and do not model any translational motion. Deriving translational motion from IMUs through standard double integration of tri-axial acceleration data is known to be error-prone [^103], resulting in significant drift over time. To mitigate this, previous studies have proposed physics-guided, learnable modules for estimating global or relative translational motion [^101]. Since our study targets seated conversations and acoustic zones of interest, translational motion offers limited value. Therefore, we focus on leveraging gyroscope measurements over short durations to estimate the head orientation geometry.

![Refer to caption](figures/fig3-opt-imu-horizontal.png)

Figure 3. Illustration of a representative case a) showing drift that increases towards the end of the measurement window and b) demonstrates the overall azimuth and elevation from the ground truth optitrack and IMUs.

Obtaining orientation from gyroscope measurements also incurs drift over time, and correcting for such drift often requires device-dependent calibration of sensor-specific bias instability, scale factor errors, and temperature coefficients [^45] [^82] [^98]. In this work, we explore a device-agnostic way to leverage a modality as a cue for the focal user’s auditory zones of interest; therefore, we opt for shorter observation windows in our study. Figure 3(a) shows a comparison for a 30-second segment of the ground-truth head orientation from OptiTrack measurements and the IMU-derived head orientation for the focal user, showing minimal drift toward the end of the segment, supporting our design choice. In a later section (Section 4.6), our empirical results show that such drift is acceptable in our case. To advance our goal of identifying the focal user’s auditory zones of interest, we do not seek a precise head-pose estimate but rather aim to capture the dynamics of the head orientation and its trajectory. Figure 3(b) shows near visual agreement between the IMU- and OptiTrack-derived head orientation for the segment, thus justifying our choice of wearable behavioral modality in this study.

### 3.3. Motivation and Rationale

![Refer to caption](figures/fig4-motivating-figure.png)

Figure 4. Study Motivation Illustration: (a) Layout of the conversation group, showing the focal user and four conversation partners; (b) Density plot of conversation partners’ locations from OptiTrack measurements, transformed to the focal user’s frame of reference, with head-orientation data from the IMU on the smartglasses overlaid; (c) Cumulative voice activity of conversation partners during a 30-second segment.

Consider a scenario where the focal user is engaged in conversation with four partners, as shown in Figure 4. We obtain the ground truth locations of the conversation partners from the exocentric OptiTrack [^73] cameras that capture the absolute positions of all participants. These fixed cameras track multiple rigid bodies identified by unique markers attached to each participant’s head. The rotation matrix derived from OptiTrack measurements is transformed to spherical coordinates (azimuth and elevation) using the standard Algorithm 2 provided in the Appendix. Note that the original input from the OptiTrack measurements provides an absolute frame of reference from a third-person point of view. To map to IMU-derived coordinates, which are naturally head-locked or egocentric, similar to past works [^109], we transform the OptiTrack rotation matrix into a head-locked frame of reference. Figure 4(b) overlays the ground-truth spatial locations of the conversation partners with the focal user’s head orientation, captured by IMU sensors, and shows that the focal user’s acoustic regions of interest align with the locations of the conversation partners. This observation motivates us to leverage head orientation as a behavioral modality to localize conversation partners.

Another observation is that, although there are four conversation partners, the head-kinesis density shows two distinct clusters. Upon further inspection, when we juxtapose the talkativeness of a partner, as shown in Figure 4(c), we observe a correlation between the talkativeness of a conversation partner and the head-orienting behavior of the focal user—more frequent explicit looking in the direction of conversation partners 0 and 2, who are the more talkative partners in this segment. This motivates us to study methods for understanding another task that can be beneficial in the context of conversation scene understanding: identifying the number of conversation partners based on head orientation behavior.

Overall, this highlights that the head orientation dynamics, even during a seated conversation, are complex and influenced by various contextual factors, not just limited to talkativeness. It also reinforces our choice of the study dataset, which is collected during seated natural conversations, enabling us to be the first to investigate the role of head orientation in localizing and identifying the number of conversation partners with minimal prior knowledge in a systematic manner.

### 3.4. Localizing Acoustic Zones of Interest from IMU-derived Head-Orientations

In this section, we first outline the approach used to construct the targets, followed by the description of the tasks and the corresponding network design.

#### 3.4.1. Discrete Spatialization of Acoustic Zones of Interest

As described in Sections 3.3 and 3.2, we transform the ground-truth spatio-temporal positions of the conversation partners, obtained from OptiTrack, to the same reference frame as the focal user’s IMU-derived head orientation. Our goal is to identify the acoustic zones of interest, which overlap with the locations of the conversation partners. There are two ways to formulate this: 1) a continuous target prediction, designed as a multi-head regression task. This requires additional considerations for varying group sizes, as the target location of each talker needs to be ordered; or 2) an alternative approach, which discretizes the spatial locations under certain assumptions, framing the problem as a multilabel binary classification task. This latter approach has the advantage of being applicable to any group size without requiring architectural changes. Additionally, the speech-enhancement applications on smartglasses [^102] [^22] [^4] that stand to benefit from the integration of behavioral preferences of the focal user also apply their (beamforming) directionality towards discrete spatial zones; supporting our formulation’s practical utility. We now present our rationale for choosing this multilabel binary classification formulation.

Rationale for localization task’s target construction. We discretized the spatial locations of the conversation partners—defined as everyone present at the table with the focal user—at the segment level (30 seconds) for the following reasons:

1. Under nominal conversation settings, a focal user looks in the direction of the intended talker when they speak [^14] [^26] [^35]. Our goal is to identify such egocentric behavior patterns from IMUs on smartglasses that are relevant to the conversation and determine the location of acoustic attention. However, the causality between the intended talker’s speaking status and head orientation is not deterministic, thus imposing a frame-level prediction (0.2 seconds or 5 Hz) is infeasible for this task. Hence, we determine the locations at a segment level (30 seconds).
2. From Figure 4 (a), we observe that the intended talkers may undergo some translational motion even during a seated conversation (leaning forward, shifting sideways, etc.). This makes their locations subject to high variability; for instance, the density clusters in Figure 4 (b) are not tightly centered. Considering this, since we cannot couple head orientation with the precise dynamic location of the conversation partners, and estimating the conversation partners’ locations so precisely does not offer any benefit in downstream speech-enhancement applications that generally use a fixed beam width of approximately 20 $\degree$ –60 $\degree$ [^36] [^37] [^38], we estimate the location statistics over a segment and assign that to the particular talker.
3. Sometimes conversation partners are seated very close to each other, and it is known that head orientation exhibits bimodal behavior in one-on-one conversations or undershooting [^34] [^50], which already makes the task highly challenging. In such scenarios, devising dedicated methods to disambiguate closely seated talkers may not provide significant benefits, following the same reasoning as before: conversation-enhancement applications typically operate with a fixed beam width for signal enhancement [^36] [^37] [^38]. Therefore, we propose a multilabel formulation—where each spatial zone may contain more than one conversation partner (described in detail below)—which avoids any rule-based target assignment.

Thus, we propose discrete spatialization of the acoustic zones of interest based on the locations of the conversation partners over a segment, and construct the ground truth as follows.

![Refer to caption](figures/fig5-spat-ho-viz.png)

Figure 5. Spatial discretization of conversation partner locations. For the layout in Figure 4 (a), the bin vector will be \[101101\] for these spatial zones.

Constructing Ground-Truth Spatial Locations for Focal User’s Acoustic Zones of Interest. For each speaker $s$, we compute their median azimuth angle over a segment, $\theta_{s}=\text{median}(\Theta^{s}_{t})$, where $\Theta^{s}_{t}$ denotes the set of azimuth angles for speaker $s$ at each time step $t$ within the segment, using OptiTrack’s measurements of their true locations. We then generate a bin-vector $\mathbf{b}_{s}$ for each speaker $s$, where each element $b_{s,i}$ is defined as follows:

$$
b_{s,i}=\begin{cases}1,&\text{if }\theta_{s}\text{ falls within bin }i\\
0,&\text{otherwise}\end{cases}
$$

Here, each bin $i\in\mathbb{Z},0\leq i\leq 5$ is defined by the interval $[l_{i},r_{i}]$, where $l_{i}\in[100,-60]$ and $r_{i}\in[60,-100]$, discretized by an interval $g_{i}$, as illustrated in Figure 5 ($l_{i+1}=l_{i}+g_{i},\,r_{i+1}=r_{i}+g_{i}$). The bin definitions described by the set $\tau_{bins}=\{l_{i},r_{i},g_{i}\}$ are selected as hyperparameters (further analysis is given in Section 4.6) and are not central to our approach. They can be adjusted without loss of generality, depending on the end application. The final target bin-vector is computed by performing a logical OR operation across all speakers’ bin-vectors: $\mathcal{Z}=\bigvee_{s=1}^{S}\mathbf{b}_{s},\quad\mathbf{b}_{s}\in\{0,1\}^{n},$ where $S$ is the number of conversation partners, and $\bigvee$ denotes element-wise logical OR across all $S$ vectors with $n$ bins.

Such a construction has several advantages: 1) closely seated speakers can be assigned to the same bin, 2) highly animated speakers—those whose movements exceed the bin width across segments—can be assigned to different bins across segments within the same session, and 3) it allows the construction of bin widths in accordance with downstream speech-enhancement applications.

#### 3.4.2. HALo Network Design for Localizing Acoustic Zones of Interest

Each component of the network, illustrated in Figure 6, is described below. The input is the sequence of spherical coordinates derived in Section 3.2, and the target is $\mathcal{Z}$, as described previously.

![Refer to caption](figures/fig6-loc-arch.png)

Figure 6. Overview of the HALo network used for localizing the acoustic zones of interest: Temporal learning module, followed by the fusion block for incorporating static features, and finally the imbalanced predictors for determining the focal user’s acoustic zones of interest.

<svg id="S3.SS4.SSS2.p2.pic1" height="134.86" overflow="visible" version="1.1" viewBox="0 0 600 134.86" width="600"><g style="--ltx-stroke-color:#000000;--ltx-fill-color:#000000;" transform="translate(0,134.86) matrix(1 0 0 -1 0 0)" fill="#000000" stroke="#000000" stroke-width="0.4pt"><g style="--ltx-fill-color:#D9CFBF;" fill="#D9CFBF" fill-opacity="1.0"><path style="stroke:none" d="M 0 6.23 L 0 128.63 C 0 132.07 2.79 134.86 6.23 134.86 L 593.77 134.86 C 597.21 134.86 600 132.07 600 128.63 L 600 6.23 C 600 2.79 597.21 0 593.77 0 L 6.23 0 C 2.79 0 0 2.79 0 6.23 Z"></path></g><g style="--ltx-fill-color:#FFF3E0;" fill="#FFF3E0" fill-opacity="1.0"><path style="stroke:none" d="M 0.69 6.23 L 0.69 95.93 L 599.31 95.93 L 599.31 6.23 C 599.31 3.17 596.83 0.69 593.77 0.69 L 6.23 0.69 C 3.17 0.69 0.69 3.17 0.69 6.23 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 8.57 104.01)"><foreignObject style="--ltx-fg-color:#000000;--ltx-fo-width:42.12em;--ltx-fo-height:1.89em;--ltx-fo-depth:0.25em;" width="582.87" height="29.67" transform="matrix(1 0 0 -1 0 26.21)" overflow="visible" color="#000000"><span id="S3.SS4.SSS2.p2.pic1.6.6.6.1.1" style="width:36.63em;"><span id="S3.SS4.SSS2.p2.pic1.6.6.6.1.1.1"><span id="S3.SS4.SSS2.p2.pic1.6.6.6.1.1.1.1">Task Formulation&nbsp;1: Head-orientation based Acoustic Zones of Interest Localization (<span id="S3.SS4.SSS2.p2.pic1.6.6.6.1.1.1.1.1">HALo</span>)</span></span> </span></foreignObject></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 8.57 11.26)"><foreignObject style="--ltx-fg-color:#000000;--ltx-fo-width:42.12em;--ltx-fo-height:5.55em;--ltx-fo-depth:0.19em;" width="582.87" height="79.49" transform="matrix(1 0 0 -1 0 76.8)" overflow="visible" color="#000000"><span id="S3.SS4.SSS2.p2.pic1.5.5.5.5.5.5.5.5.5.5.5.5.5.5.5.5.5.5" style="width:42.12em;"><span id="S3.SS4.SSS2.p2.pic1.5.5.5.5.5.5.5.5.5.5.5.5.5.5.5.5.5.5.5">Given a sequence of head orientation measurements, denoted as <math data-latex="\mathbf{x}_{t}" display="inline" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><msub><mi>𝐱</mi> <mi>t</mi></msub> <annotation encoding="application/x-tex">\mathbf{x}_{t}</annotation></semantics></math> for all <math data-latex="t\in[0,T)" display="inline" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>t</mi> <mo>∈</mo> <mrow><mo stretchy="false">[</mo><mn>0</mn><mo>,</mo><mi>T</mi><mo stretchy="false">)</mo></mrow></mrow> <annotation encoding="application/x-tex">t\in[0,T)</annotation></semantics></math>, for a focal user within a group of arbitrary size <math data-latex="\mathcal{G}" display="inline" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mi>𝒢</mi> <annotation encoding="application/x-tex">\mathcal{G}</annotation></semantics></math>, the objective is to identify the acoustic zones of interest, <math data-latex="\mathcal{Z}=\{z_{1},z_{2},\ldots,z_{n}\}" display="inline" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>𝒵</mi> <mo>=</mo> <mrow><mo stretchy="false">{</mo> <msub><mi>z</mi> <mn>1</mn></msub><mo>,</mo><msub><mi>z</mi> <mn>2</mn></msub><mo>,</mo><mi mathvariant="normal">…</mi><mo>,</mo><msub><mi>z</mi> <mi>n</mi></msub> <mo stretchy="false">}</mo></mrow></mrow> <annotation encoding="application/x-tex">\mathcal{Z}=\{z_{1},z_{2},\ldots,z_{n}\}</annotation></semantics></math>, where <math data-latex="n\leq|\mathcal{G}|" display="inline" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>n</mi> <mo>≤</mo> <mrow><mo stretchy="false">|</mo> <mi>𝒢</mi> <mo stretchy="false">|</mo></mrow></mrow> <annotation encoding="application/x-tex">n\leq|\mathcal{G}|</annotation></semantics></math>. These zones correspond to the spatial locations of one or more conversation partners, inferred from the behavioral data captured by the head orientation sequence. This task is formulated as multilabel classification for a given sequence.</span></span></foreignObject></g></g></svg>

Feature Summarization. To capture the head-orientation dynamics to solve for the focal user’s acoustic zones of interest, we need a sequential learning module. We first normalize the input, $\mathrm{x}_{t}$ across the features. Then the features are summarized using 1D convolutional neural network layers (CNNs) and applying max pooling along the temporal axis resulting in embeddings, $\mathrm{E}\in\mathbb{R}^{F\times T}$, where $F$ is the feature-dimension (chosen as a hyperparameter) in the latent space and $T<150$ for a 30 second segment.

Temporal Learning. Our task of localizing acoustic zones of interest depends on the ability of the temporal learning module to differentiate between conversation-relevant features and those arising from conversation-agnostic head movements. For example, a focal user might look at their shoes or engage in eating; in such cases, merely analyzing the density of head orientation statistics could incorrectly identify locations like under or on the table as acoustic zones of interest. Our goal is to enable the model to distinguish between behaviors that are not focused on conversation and those that are. Our pilot analysis revealed the ineffectiveness of non-temporal or rule-based methods, and our results in later Sections 4.3 and 4.4 support these design choices with consistent superior performance of HALo over statistical rule-based models and other baselines. We also find transformers to be suboptimal as a sequential backbone in this case as shown in Table 2 (refer to Section 4.1 for Macro-F1 and Hamming Score definition), possibly due to their limited expressiveness in capturing dependencies across fine-grained time steps similar to prior observations in modeling IMU [^67] [^101] [^65] or time-series [^111] [^66] data.

Table 2. A brief analysis of the performance of different sequential backbones for HALo.

| Model | Macro-F1 | Hamming |
| --- | --- | --- |
| 1D CNN | 0.40 | 0.76 |
| Transformer | 0.27 | 0.82 |
| LSTM | 0.60 | 0.78 |
| BiLSTM+Attn | 0.63 | 0.80 |

Consequently, we have adopted a variant of the recurrent Long Short-Term Memory (LSTM) for temporal learning in our design. We use a bidirectional LSTM (BiLSTM), where each cell is represented by $\mathcal{L}_{\tau}$ and parameterized by the set $\tau$. We combine the forward and reverse layers’ hidden states, represented as $\overrightarrow{\mathbf{h}}^{f}$ and $\overleftarrow{\mathbf{h}}^{r}$, respectively, to obtain $\mathbf{h}^{s}=\frac{\overrightarrow{\mathbf{h}}^{f}+\overleftarrow{\mathbf{h}}^{r}}{2}$, where $\mathbf{h}^{s}\in\mathbb{R}^{H\times T}$. Then, we apply self-attention similar to [^96]. We initialize the query and key vectors, $Q_{a}$ and $K_{a}$, by performing a linear projection of $\mathbf{h}_{t}$, denoted by $\mathcal{W}$ and parameterized by the indicated subscripts to obtain the self-attention, $\mathcal{A}\in\mathbb{R}^{H\times T}$. The trainable parameters for temporal learning are contained in the set $\tau=\{\xi_{h},\xi_{q},\xi_{k}\}$. We then compute the dot product of the attention weights at each time index with the BiLSTM output, taking a weighted mean along the time axis denoted as, $\mathbf{m}=\sum_{t=0}^{T}a_{t}\cdot\mathbf{h}_{t}^{s}$, where $a_{t}\in\mathcal{A}$, before the fusion block.

Fusion of Static Features. In addition to the temporal IMU features, we incorporate contextualization of these features with time-invariant information—specifically, the number of total speakers in the conversation setting, which we refer to as static features—through late fusion in HALo to enhance the localization performance. To carry out this fusion in a meaningful manner, we reduce the dimension of the temporally collapsed representation, $\mathrm{m}$, using linear layers $\mathcal{W}(.)$ with the rectified linear unit (ReLU) as the activation function, to obtain $\mathrm{p}\in\mathbb{R}^{K}$, where $K<H//4$. This is combined with the static features to produce $\mathrm{r}\in\mathbb{R}^{K+1}$, which is normalized and passed through linear layers before being input to multi-head predictors. HALo’s has approximately 400k parameters.

Multilabel Classification Objective. To provide flexibility in weighting the penalty for mispredicting various spatial zones—whether to address a central bias in the frontal direction or to compensate for data imbalance in peripheral locations (refer to Figures 11 and 20)—we adopt an imbalanced multi-head binary classifier with deeper classifiers for peripheral zones. Thus, we use a mix of weighted loss functions and imbalanced classifier heads to optimize the task objective. Let the ground truth binary vector for the discretized spatial location being an acoustic zone of interest be denoted as $\mathbf{b}^{\text{GT}}_{i}$, and the predicted vector be given as $\mathbf{b}^{\text{p}}_{i}=\texttt{ReLU}(\mathcal{W}_{\xi_{i}}(\mathrm{r}))$ for $i\in[0,N]$. The weighted cross-entropy loss for the localization task is defined as:

$$
\mathcal{L}_{loc}=-\sum_{i=0}^{N}k_{i}\left(\mathbf{b}^{\text{GT}}_{i}\log(\mathbf{b}^{\text{p}}_{i})+(1-\mathbf{b}^{\text{GT}}_{i})\log(1-\mathbf{b}^{\text{p}}_{i})\right).
$$

Here, $k_{i}$ is the weight assigned to each acoustic zone based on class imbalance, computed as the inverse of the normalized class frequency, i.e., $k_{i}=\frac{1}{\tilde{f}_{i}}$, where $\tilde{f}_{i}=\frac{f_{i}}{\sum_{j=1}^{N}f_{j}}$, and $f_{i}$ is the number of samples belonging to class $i$.

### 3.5. Number of Conversation-partners from Head-Orientation using IMUs

We are motivated to relax the a priori assumption of knowing the number of conversation partners for fusion as static features and explore a methodology to infer it from the head-orientation features. Inspired by the statistical analyses of a focal user’s head orientation in a seated conversation setting, our intuition is that, based on the density of the clusters formed by head orientations, as shown in Figure 4 (b), it is reasonable to estimate how many conversation partners are present. We formulate this task as follows,

<svg id="S3.SS5.p2.pic1" height="85.04" overflow="visible" version="1.1" viewBox="0 0 600 85.04" width="600"><g style="--ltx-stroke-color:#000000;--ltx-fill-color:#000000;" transform="translate(0,85.04) matrix(1 0 0 -1 0 0)" fill="#000000" stroke="#000000" stroke-width="0.4pt"><g style="--ltx-fill-color:#D9CFBF;" fill="#D9CFBF" fill-opacity="1.0"><path style="stroke:none" d="M 0 6.23 L 0 78.82 C 0 82.26 2.79 85.04 6.23 85.04 L 593.77 85.04 C 597.21 85.04 600 82.26 600 78.82 L 600 6.23 C 600 2.79 597.21 0 593.77 0 L 6.23 0 C 2.79 0 0 2.79 0 6.23 Z"></path></g><g style="--ltx-fill-color:#FFF3E0;" fill="#FFF3E0" fill-opacity="1.0"><path style="stroke:none" d="M 0.69 6.23 L 0.69 61.95 L 599.31 61.95 L 599.31 6.23 C 599.31 3.17 596.83 0.69 593.77 0.69 L 6.23 0.69 C 3.17 0.69 0.69 3.17 0.69 6.23 Z"></path></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 8.57 70.04)"><foreignObject style="--ltx-fg-color:#000000;--ltx-fo-width:42.12em;--ltx-fo-height:0.75em;--ltx-fo-depth:0.25em;" width="582.87" height="13.84" transform="matrix(1 0 0 -1 0 10.38)" overflow="visible" color="#000000"><span id="S3.SS5.p2.pic1.4.4.4.1.1" style="width:36.63em;"><span id="S3.SS5.p2.pic1.4.4.4.1.1.1"><span id="S3.SS5.p2.pic1.4.4.4.1.1.1.1">Task Formulation&nbsp;2: Classifying the Number of Conversation Partners (<span id="S3.SS5.p2.pic1.4.4.4.1.1.1.1.1">CoCo</span>)</span></span> </span></foreignObject></g><g fill-opacity="1.0" transform="matrix(1.0 0.0 0.0 1.0 8.57 11.26)"><foreignObject style="--ltx-fg-color:#000000;--ltx-fo-width:42.12em;--ltx-fo-height:3.09em;--ltx-fo-depth:0.19em;" width="582.87" height="45.51" transform="matrix(1 0 0 -1 0 42.82)" overflow="visible" color="#000000"><span id="S3.SS5.p2.pic1.3.3.3.3.3.3.3.3.3.3.3.3.3.3.3.3.3.3" style="width:42.12em;"><span id="S3.SS5.p2.pic1.3.3.3.3.3.3.3.3.3.3.3.3.3.3.3.3.3.3.3">Given a sequence of head orientation measurements and speaking states denoted as <math data-latex="\mathbf{x}_{t}" display="inline" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><msub><mi>𝐱</mi> <mi>t</mi></msub> <annotation encoding="application/x-tex">\mathbf{x}_{t}</annotation></semantics></math> for all <math data-latex="t\in[0,L)" display="inline" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mrow><mi>t</mi> <mo>∈</mo> <mrow><mo stretchy="false">[</mo><mn>0</mn><mo>,</mo><mi>L</mi><mo stretchy="false">)</mo></mrow></mrow> <annotation encoding="application/x-tex">t\in[0,L)</annotation></semantics></math>, for a focal user, the objective is to identify the number of conversation partners <math data-latex="\mathcal{G}" display="inline" xmlns="http://www.w3.org/1998/Math/MathML"><semantics><mi>𝒢</mi> <annotation encoding="application/x-tex">\mathcal{G}</annotation></semantics></math>. This task is formulated as a sequence-to-one classification problem.</span></span></foreignObject></g></g></svg>

As evident from the illustrative example in Figure 4, although there are four potential conversation partners, the focal user is mostly oriented towards the central and right-side speakers. This highlights the significant challenge of accurately classifying the number of speakers solely based on head orientation data which is aggravated in larger conversational groups (discussed in later Section 4.6’s Figure 21). In this section, we describe the design of target shaping and provide details about the additional features and the design of CoCo. Section 4.4 further discusses the challenges and the benefits of incorporating additional modalities (e.g., the focal user’s speech state) or domain-specific rules (such as voice-activity-based qualification of conversation partners) for target shaping in the classification performance.

![Refer to caption](figures/fig7-clf-distiled-arch.png)

Figure 7. Illustration of the classification network to determine the number of conversation partners based on head-orientation and abstract audio features or target shaping.

We retain the Feature Summarization and Temporal Learning modules shown in Figure 7, which serve as backbones for this task. However, in the Temporal Learning we did not find self-attention particularly beneficial for this task hence omitted them. The feature embeddings, $\mathrm{m}$, are now input to a classifier head, $\mathrm{U}_{clf}$, which predicts the output probability and optimizes the following objective:

$$
\mathcal{L}_{\text{clf}}=-\frac{0}{N}\sum_{i=0}^{N}\sum_{j=1}^{C}y_{ij}\log\left(\frac{\exp(z_{ij})}{\sum_{k=1}^{C}\exp(z_{ik})}\right)
$$

where: $N$ is the number of samples, $C$ is the number of classes, $y_{ij}$ is the binary indicator (0 or 1) if class label $j$ is the correct classification for sample $i$, $z_{ij}$ is the predicted logit for class $j$ of sample $i$.

Incorporation of Abstract Audio-features. Unlike audio-based speaker localization requiring multichannel audio, here we propose using abstract audio features – speaking status – which are cheaper [^76] to obtain. We use two views of speaking status, 1) focal user’s voice-activity stream denoted as self\_vad and 2) a logical OR operation on the voice activities of all the speakers to represent an overall conversation partners’ voice activity denoted as speaker\_vad. Intuitively, these features help distinguish between speaking-state and listening-state head movements, which can facilitate learning better representations to identify the number of conversational partners.

Cumulative Voice Activity-based Label Shaping. Another perspective is to refine the target labels based on the participants’ level of talkativeness. Building on our earlier hypotheses—reflecting general human behavior, though not universally applicable—a focal user is more likely to orient their head toward a conversation partner when that partner is actively speaking. However, within a 30-second segment, if certain conversation partners contribute minimally to the conversation, the focal user has limited incentive to look in their direction impacting the performance metrics.

To address this, we adopt a thresholding mechanism, leveraging the voice-activity levels of all conversation partners and accumulating them over a 30-second segment. In the illustrative example in Figure 4, the talkativeness ranking of the speakers is as follows: Speaker 0 (10%), Speaker 1 (67%), Speaker 2 (16%) and Speaker 3 (6%). This ranking helps justify the acoustic zones of interest of the focal user. Consequently, we adopt a thresholding mechanism to count the number of participants based on their cumulative talking time within the segment.

![Refer to caption](figures/fig8-dbscan-threshold.png)

Figure 8. DBSCAN performance in empirically determining a cumulative voice activity threshold to qualify conversation partners and update targets for CoCo

The talkativeness threshold to qualify a participant is determined empirically through a small study using the Density-Based Spatial Clustering of Applications with Noise (DBSCAN) algorithm [^20]. The distance between points within a cluster and the neighborhood distances that reveal natural spatial groupings are treated as hyperparameters based on the considered threshold. For instance, with a 2-second talkativeness threshold in a 30-second window sampled at 5 Hz, the minimum number of points required to form a valid cluster is set to 10. Based on our pilot analysis, illustrated in Figure 9, we selected 8 seconds as the threshold. The original targets and the updated targets after voice-based thresholding are shown in Figure 9. As evident from the target shaping, there are scenarios where none of the speakers qualify as conversation partners, and many segments with more than three targets have been reassigned to a lower target. However, there are still cases where four conversation partners qualify even with the 8-second threshold, as overlapping speakers can occur, and we do not impose any restrictions on such scenarios; we only conduct target shaping based on a speaker’s cumulative voice activity.

## 4\. Results and Discussions

In this section, we outline our evaluation setup, including the performance metrics and baselines used for comparison. We then present our experimental results demonstrating the performance of HALo, CoCo, and HALo-CoCo, which uses estimates from CoCo to reduce the apriori for HALo under different conditions. We also present qualitative performance over complete sessions and discuss insights from model explainability. Finally, we present additional experiments to support our design choices.

### 4.1. Performance Metrics

Following standard recommendations [^78] [^62] for multilabel classification tasks, we adopt the metrics of Hamming Score <sup>1</sup>, Logit-wise Accuracy, Logit-wise F1 and Macro F1 for the localization task. For the task of identifying the number of conversation partners, we leverage the accuracy and Macro F1 metrics following their standard definitions [^78]. The formulae for the implemented metrics are provided in Section B of the Appendix.

Data Statistics. The statistics for class distribution and a representative discrete spatialization (refer to Section 3.4.1) performed in this study are shown in Figures 11 and 11, respectively.

![Refer to caption](figures/fig10-class-distribution.png)

Figure 10. Distribution of group sizes across all sessions.

### 4.2. Baselines

We carry out evaluations for both the tasks—localization and identifying the number of conversation partners—against three baseline methods on the RLR-Chat dataset. First, we consider a rule-based method, engineered based on knowledge of patterns in conversation dynamics. Next, we use a simple multi-layer perceptron-based deep learning model, which does not account for temporal ordering. Finally, we employ a state-of-the-art time-series representation learning method, Informer [^113], designed for handling long sequences which takes the downsampled 6-axis IMU data.

Rule-based. This is a simplified rule-based method to capture head-orientation dynamics, inspired by previous works [^92] [^79] that model the visual focus of attention based on speaking status, head orientation, and other contextual information [^3]. Other works [^55] have shown, through manual statistical analyses in dyadic conversations, that there is a high correlation of direction of facing with the conversation partner’s location, especially during the listening state. Although these tasks are not exactly what we are trying to accomplish, inspired by these findings, we can design a rule-based non-parametric scheme to capture a plausible dynamic: when the focal user is not speaking, they look at the actively speaking conversation partner. Thus, for each segment during the non-speaking state of the focal user, based on the density of the head-orientation coordinates, we conduct spatial clustering (following the DBSCAN algorithm). For the localization task, we take the centroids of the clusters as the spatial zones of interest, and for identifying the number of conversation partners, we count the number of naturally formed clusters. An illustration of this baseline’s working principle, applied to the layout previously demonstrated in Section 3.3 and Figure 4, is shown in Figure 12.

![Refer to caption](figures/fig12-dbscan-demo.png)

Figure 12. Performance of the rule-based method: spatial density-based clustering of the focal user’s head orientation during their non-speaking state within a segment, demonstrated for a representative setting (same scene as shown in Figure 4 ). The method identifies two conversation partners and localizes them, following the discrete spatialization strategy in Section 3.4.1, to the \[ − 30 °, 60 \] \[-30\\degree,-60\\degree\] and 0 \[0\\degree,-30\\degree\] zones in the azimuthal plane.

Segment-based. This is segment-level non-temporal approach (of approximately 200k parameters) using the azimuth information from the head-orientation computation. We feed the $L$ -dimensional azimuth as input vector to a multi-layer perceptron (MLP) with: 1) $n$ classifier heads for the multilabel classification of the localization of acoustic zones of interest task, and 2) one classifier head for the task of identifying the number of conversation partners.

Temporal-based. Informer [^113] is a transformer-based architecture specifically designed to handle long sequences encountered in the real world, enabling the model to manage long-range dependencies with computational efficiency by using sparse-probability attention. We leverage the encoder part of this architecture and take the mean along the temporal axis before feeding these learned embeddings to task-specific classifier heads [^65]. The input to this baseline is the downsampled 100 Hz 6-axis IMU data and the model has of approximately 900k parameters. We adopt this baseline to represent a time-series model with high temporal modeling capacity.

Implementation Details. All experiments are conducted using three random seeds (2711, 2712, 2713), reporting the mean and standard deviation of metrics. Data is split into training and testing sets in a 7:3 ratio, with 20% of the training data reserved for validation. Models are trained using a batch size of 64 and the ADAM optimizer. Localization models use a learning rate of $1\mathrm{e}{-5}$, while classification models use $1\mathrm{e}{-3}$. All models are trained for 20 epochs, and the best checkpoint is selected based on the lowest validation loss.

### 4.3. Evaluating the Localization of Acoustic Zones of Interest

In this section, we demonstrate the performance of HALo in localizing a focal user’s acoustic zones of interest, analyze the influence of various input features, and present qualitative analyses on longer session-wise inputs and the explainability of HALo’s predictions.

Table 3. Performance of the methods for localizing auditory zones of interest, evaluated using logit-wise F1, logit-wise accuracy, macro F1, and Hamming scores (defined in Section B of the Appendix). The best performance is shown in bold, and the second-best is underlined.

<table><thead><tr><th></th><th colspan="6">Discrete-Spatial Zones</th><th>Aggregate</th></tr><tr><th></th><th>[-100, -60]</th><th>[-60, -30]</th><th>[-30, 0]</th><th>[0, 30]</th><th>[30, 60]</th><th>[60, 100]</th><th>Scores</th></tr><tr><th>Method</th><th colspan="6">Logit-wise F1</th><th>Macro F1</th></tr></thead><tbody><tr><th>Rule-based</th><td>0.02</td><td>0.26</td><td>0.57</td><td>0.62</td><td>0.15</td><td>0.03</td><td>0.27</td></tr><tr><th>Segment-based</th><td>0.03 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.05</sub></td><td>0.08 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.08</sub></td><td>0.58 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.05</sub></td><td>0.76 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.05</sub></td><td>0.10 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.01</sub></td><td>0.07 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.02</sub></td><td>0.27 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.01</sub></td></tr><tr><th>Informer</th><td>0.31 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.01</sub></td><td>0.21 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.03</sub></td><td>0.62 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.08</sub></td><td>0.60 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.12</sub></td><td>0.51 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.07</sub></td><td>0.48 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.04</sub></td><td>0.45 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.04</sub></td></tr><tr><th>HALo (Ours)</th><td>0.57 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.04</sub></td><td>0.57 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.04</sub></td><td>0.65 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.01</sub></td><td>0.80 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.01</sub></td><td>0.42 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.03</sub></td><td>0.61 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.11</sub></td><td>0.62 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.03</sub></td></tr><tr><th>Method</th><td colspan="6">Logit-wise Accuracy</td><td>Hamming Score</td></tr><tr><th>Rule-based</th><td>0.84</td><td>0.81</td><td>0.50</td><td>0.53</td><td>0.75</td><td>0.82</td><td>0.71</td></tr><tr><th>Segment-based</th><td>0.56 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.48</sub></td><td>0.59 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.38</sub></td><td>0.52 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.03</sub></td><td>0.69 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.10</sub></td><td>0.53 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.37</sub></td><td>0.76 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.08</sub></td><td>0.73 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.02</sub></td></tr><tr><th>Informer</th><td>0.82 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.01</sub></td><td>0.83 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.03</sub></td><td>0.62 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.00</sub></td><td>0.54 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.06</sub></td><td>0.64 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.06</sub></td><td>0.63 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.13</sub></td><td>0.68 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.02</sub></td></tr><tr><th>HALo (Ours)</th><td>0.88 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.01</sub></td><td>0.85 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.03</sub></td><td>0.65 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.02</sub></td><td>0.67 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.00</sub></td><td>0.81 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.02</sub></td><td>0.86 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.02</sub></td><td>0.79 <sub><math><semantics><mo>±</mo> <annotation>\pm</annotation></semantics></math> 0.01</sub></td></tr></tbody></table>

Table 3 summarizes the performance of the rule-based, segment-based, and representative high-capacity time-series baselines against HALo. We observe that: 1) the rule-based model, despite incorporating the focal user’s speaking status as an additional attribute, performs poorly in the localization task (0.27 macro-F1 and a Hamming score of 0.71). This aligns with prior studies that relied on heuristics and have noted the inherent complexity of using behavioral modalities to infer auditory attention [^50]; 2) non-temporal models, both rule-based and deep learning-based, are suboptimal in capturing the complex head-orientation dynamics that are indicative of the focal user’s attention. This supports our sequential modeling design choice of HALo, which boosts average performance from 0.27 to 0.62 in terms of macro-F1, and from 0.72 to 0.79 in terms of Hamming score over non-temporal models; and 3) direct application of IMU data to state-of-the-art high-capacity sequential models like Informer is not suitable. Our specialized HALo, which incorporates sequential fusion of static features, outperforms Informer by an average relative improvement of 38% in F1 score and 17% in Hamming score. Overall, our proposed sequential fusion-based HALo outperforms all baseline methods by an average of 45% in macro-F1 and 10% in Hamming score. Intuitively, our approach of off-loading some of the filtering of useful semantics by preprocessing to obtain the azimuth and elevation, followed by stage-wise feature summarization, sequential learning, and a fusion module, supports achieving the high performance in the localization of discrete-spatial zones using behavioral attributes.

![Refer to caption](figures/fig13-localization-features.png)

Figure 13. Performance of conversation partners’ localization task with different input features. Knowing the number of speakers a priori provides a significant performance boost compared to adding other audio-modality-derived features, such as the self or speakers’ speech status.

A priori knowledge of the number of speakers enhances localization performance. Figure 13 illustrates the impact of different input features along with the processed IMU features on localization performance. We observe that the late fusion of the number of conversation partners enhances the localization performance by approximately 50%, as it helps in contextualizing the predictions better. In later Sections 4.4 and 4.5, we evaluate strategies to obtain this static feature of the number of conversation partners as an embedding from the CoCo network. We also evaluate the value of incorporating more affordable and abstract audio modalities, such as a stream of the focal user’s speaking status denoted as self-voice-activity-detected (self\_vad) and a binarized stream of voice activity from any of the speakers, known as speaker-voice-activity-detected (speaker\_vad). We find that these additional features do not provide any significant benefit for this task.

![Refer to caption](figures/fig14-attn-viz.png)

Figure 14. Illustration of the model’s temporal self-attention mechanism for predicting conversation partners’ locations based on head orientation from IMU data. The mechanism assigns higher weights when the focal user’s head orientation exhibits greater dynamism. Visual data is used solely for interpretability analysis.

Model explainability indicates more attention during active engagement of focal user. To interpret our proposed predictive model, we extract the attention vector from the Attention Module of the model (Figure 6). We normalize the attention vector $a_{t}\in\mathbb{R}^{H\times T}$ and approximately align the video data to its length to facilitate interpretability. Due to network non-linearities, a precise time-scale mapping is infeasible, but this approximate alignment [^74] facilitates the visualization of the temporal importance attributed to each frame in the vision data for intuitive understanding. Figure 14 illustrates a representative example, which shows higher attention values when there is more dynamism in the head orientation, i.e., the focal user looks in the direction of all the conversation partners, and less when they stagnate their attention. This observation aligns with the expectation that the trajectory of head orientation can help in inferring the conversation partners’ locations and further reinforces the value of preserving the temporal dynamics of the head orientation for auditory attention localization task.

Qualitative results across full-sessions show promising localization performance. We evaluate the overall performance of the identified conversation zones for a complete session. The RLR-Chat dataset consists of sessions which are manually aligned and split into non-consecutive but ordered 30-second segments (refer Figure 24. (b) in the Appendix). We note that although the data is collected in a seated-conversation setting, one might assume that the ground truth locations of the conversation partners, after discretization in the azimuthal plane, remain fixed across all segments for a given egocentric session, that is not the case. Due to translational movements during more animated conversations (such as laughing or lateral oscillation) may result in shifted ground truth median locations. This shift affects the ground truth bin vector, $\mathbf{b}^{\text{GT}}_{i}$, for the $i$ -th zone as:

$$
\mathbf{b}^{\text{GT}}_{i}=\begin{cases}[0,\mathbf{b}^{\text{GT}}_{0},\mathbf{b}^{\text{GT}}_{1},\ldots,\mathbf{b}^{\text{GT}}_{N-1}]&\text{(right shift)}\\
[\mathbf{b}^{\text{GT}}_{1},\mathbf{b}^{\text{GT}}_{2},\ldots,\mathbf{b}^{\text{GT}}_{N},0]&\text{(left shift)}.\end{cases}
$$
![Refer to caption](figures/fig15-qual-results.png)

Figure 15. (a, b) Sandwiched Mispredictions; (c, d) Shifted prediction for a single conversation partner; (e, f) Shifted prediction for a two conversation partners.

For each session, we obtain a count for each spatial zone being a true location of a conversation partner, given by $\mathrm{c}^{\text{GT}}_{i}=\sum_{m=1}^{M}\mathbf{b}^{\text{GT}}_{i}(m)$, where $\mathbf{b}^{\text{GT}}_{i}(m)$ is the $m$ -th element of the ground-truth bin vector for the $i$ -th segment and $M$ is the number of elements in the bin vector. Similarly, we obtain the session-wise count vector $\mathrm{c}^{\text{P}}_{i}$ from the predicted bin vectors for each segment $\mathbf{b}^{\text{P}}_{i}(m)$.

Quantitatively, an exact match between these count-vectors,$\mathrm{c}^{\text{GT}}_{i}$ and $\mathrm{c}^{\text{p}}_{i}$ is unsuitable because head orientation is a behavioral modality and does not contain immediate causality of the speaker’s motion and focal-user’s head movement. Despite challenges such as the influence of conversational context on head orientation, our investigation demonstrates that aggregating predictions from 30-second segments over the course of one-hour sessions yields overall positive results. As illustrated in Figure 15, while certain segment-level mispredictions occur, the model’s session-level predictions remain largely consistent with the ground-truth acoustic zones of interest. We highlight two representative cases: (1) mispredicting a conversation partner positioned between two others, and (2) slightly undershooting the true location of the conversation partners.

Figure 15. (a) illustrates the first case in a four-person conversation setting, where the session-wise prediction’s mean absolute error is 1.5, with a high Pearson correlation [^75] of 0.94. This indicates that head orientation behavior can reliably inform about the acoustic zones of interest of a focal user over the duration of a full-length conversation, with only short-segment level modeling to accommodate unobtrusive sensing by IMUs on smartglasses. However, at a segment level, like 15. (b), it may mispredict a sandwiched zone between the location zones of two ground truth conversation partners. This can be attributed to the segment-to-segment variability in the conversation partners’ median location and overall behavior-driven variability of the IMU-derived head orientation data, which embeds a non-deterministic causality between the head orientation of the focal user and the momentarily updated location of the conversation partner. It also highlights the overall complexity of this task.

In Figures 15. (c), and 15. (e), we illustrate a one-on-one conversation and a three-party conversation setting respectively where undershooting behavior of the head movement as noted by past works [^46] [^71] is evident. Representative segments from these sessions in Figures 15. (d, f) indicate this left-biased undershooting behavior of the focal user.

### 4.4. Performance of Identifying the Number of Conversation Partners

Figure 13 highlights that having an a priori estimate of the number of speakers in a conversation significantly enhances localization performance. In this section, we evaluate the performance of the proposed CoCo in identifying the number of conversation partners under different settings, compared to other baselines.

![Refer to caption](figures/fig17a-clf-macrof1.png)

(a) Macro-F1 scores using abstract audio features like speaking status.

![Refer to caption](figures/fig17b-clf-analysis.png)

Figure 17. Performance of classifying the number of conversation partners with additional abstract audio features and voice-activity-based target-shaping.

Abstract audio features and target shaping improve the identification of the number of conversation partners. Figure 17 shows that utilizing only the information processed from IMUs achieves an average accuracy of 0.60 for four classes. Including the self-VAD and speaker-VAD boosts the accuracy to 0.73 or by applying target shaping based on the talkativeness of the conversation partners, as described in Section 3.5, improvements up to 0.74, can be achieved.

CoCo outperforms baselines in both the settings – abstract audio features and target shaping. Figures 16(a) and 16(b) compare the classification performance of all baselines using the enhanced feature set, while Figures 16(c) and 16(d) present the performance after target-shaping. While CoCo demonstrates strong performance across these settings, it is noteworthy that target shaping significantly boosts the performance of the baselines. This highlights the promise of our simple, talkativeness-based statistical target-shaping approach and suggests the potential for incorporating more complex socio-auditory rules to design improved target representations.

Our results in Figures 16 and 17 illustrate the overall complexity of the classification task and highlights the benefits of either including abstract audio features, which are cheaper to obtain compared to a full audio-processing pipeline and intuitively help model more complex behavioral dynamics or incorporating domain-specific knowledge to qualify speakers as conversation partners by target shaping as described in Section 3.5.

### 4.5. Localization of Acoustic Zones of Interest with Relaxed Apriori Knowledge

Combining the designs for the localization and classification of conversation partners, we present results for HALo-CoCo. To enable more effective joint optimization, we adopted the standard approach of stage-wise training HALo and CoCo, inspired by other domain-specific learning network architectures [^27] [^64]. Specifically, we extract the static features, $\mathrm{d}\in\mathbb{R}^{D}$, from the penultimate layer of $\mathrm{U}_{clf}$ of the trained CoCo and fuse them with $\mathrm{p}$ embeddings from the HALo, resulting in $\mathrm{r^{\prime}}\in\mathbb{R}^{K+D}$.

Figure 19 compares the performance of the stand-alone HALo with and without the actual number of conversation partners as static features, the performance when fusing noisy static features (by adding random uniform perturbations to static features in 30% of the samples in each batch), and the performance using the estimated number of conversation partners representation from CoCo. Our pilot results showed that a shared network (motivated by the overall similarity in design blocks for both tasks) did not perform well, achieving a Macro-F1 of 0.51. This is likely due to the complexity of the tasks, which require dedicated non-linearities to optimize each task objective. While larger datasets in the future may enable convergence to a general-purpose representation for extracting linguistic features from head orientation, we find that, in this case, stagewise training for both objectives performs better—almost on par with training using noisy static features. This suggests that incorporating a learned estimate of the static features representing the number of conversation partners may compensate for missing information. Although there is a 4% decrease in performance compared to HALo with an a priori number of conversation partners, using HALo-CoCo enables inference of acoustic zones of interest with minimal a priori and additional features, which may otherwise be expensive to acquire in real-time.

### 4.6. Additional Experiments for Design Validation

![Refer to caption](figures/fig18-joint-opt.png)

Figure 18. Performance comparison of HALo and its variants—without static features, with noisy static features, and using HALo-CoCo with estimated static features.

Bland–Altman analysis of head orientation from IMUs vs. OptiTrack measurements. We leverage the Bland–Altman statistical analysis tool [^6], commonly used to assess agreement between a new method and a gold-standard reference in clinical applications, to evaluate IMU-derived head orientation measurements against OptiTrack for the focal user. As shown in Figure 19, 95% of the IMU-based head orientation measurements fall within $\pm$ 1.96 standard deviations of the differences compared to the ground truth from OptiTrack. This indicates strong agreement between the two methods for the chosen 30-second observation window. Our goal is to demonstrate the feasibility of extracting conversation-relevant features from short-duration IMU signals on smartglasses, without requiring explicit device-dependent sensor calibration.

![Refer to caption](figures/fig19-imu-vs-optitrack.png)

Figure 20. Illustration of the F1-score and logit-wise accuracy for different spatial discretizations: (a) 3 spatial zones, (b) 6 spatial zones, and (c) 8 spatial zones, with their respective data distributions shown in (d-f), respectively. The convention followed in the paper is as follows: the frontal direction is 0 ° \\degree, the right is denoted by the negative angular direction, and the left by positive angular directions.

Flexibility of azimuthal plane discretization. The choice of spatial discretization for HALo is application-specific. Figure 20 reports the performance of three variants that differ only in the predictor head of HALo (see Figure 6): (1) a simplified three-zone setup (front, left, right), (2) our original six-zone configuration, and (3) an eight-zone discretization. As expected, the three-zone discretization achieves the highest macro-F1 (0.78). Evident from Figures 20(d–f), with increasing discretization, the class imbalance at the extremities of the focal user’s field of view increases in the current dataset (refer Figures 20(a–c)), which leads to lower performance in the extremities of the spatial zones relative to the center. While we take steps to address these issues using standard techniques presented in Section 3.4.2, such as a weighted objective in the multilabel loss (Equation 1) and added non-linearity via an imbalanced classifier head, this also presents an opportunity to create more datasets with uniform seating layouts across the complete field of view of the focal user. Also, the higher performance of frontal direction may be attributed to the central bias in human head orientations during seated conversations [^71].

![Refer to caption](figures/fig20-window-length.png)

Figure 21. Comparison of IMU-only model with original targets versus proposed enhancements—(1) abstract audio features and (2) cumulative voice-activity-based target shaping—across increasing group sizes in multiparty conversations.

Impact of increasing group size with different conditioning on CoCo. We analyze the performance of CoCo with increasing group sizes, which overall exhibits a decreasing trend due to increased task complexity and fewer representative samples from the larger group sizes (> 3), as shown in Figure 11. However, Figure 21 justifies the addition of abstract audio in the input features and voice-activity-based target shaping of the output, which boost the overall performance by an average of 17% even under challenging conditions.

Minimal end-to-end speech-enhancement pipeline using head orientation. To demonstrate that head-orientation-based localization benefits real-world applications (Section 2.4 discusses these applications), we construct a minimal conversation-focusing system using a pair of smart glasses, which consists of a steering module that provides the steering direction to a beamformer and a spatial filter that enhances the signal in that direction <sup>2</sup>. For this end-to-end study, we use the publicly available EasyCom dataset [^17], as it provides Array Transfer Functions (ATFs) for the microphones on the smart glasses, enabling speech‑enhancement algorithms to evaluate end‑to‑end performance. Although this dataset does not include IMU recordings, our earlier analysis (Figure 19) shows that IMU‑based features for short segments agree closely with OptiTrack‑based signals. Therefore, this dataset is suitable for use in our minimal system demonstration study. We closely follow the experimental setup of [^17] and steer the highly directional beamformer using two modalities: (1) head-orientation-based: We use head orientation in two ways, first by using the frontal direction (where the user is looking) and second by using HALo’s estimates of the zones of conversation partners; and (2) audio-based direction-of-arrival estimates using three common signal-processing algorithms—MUSIC [^83], GCC-PHAT [^44], and SRP [^15]. We report the improved signal-to-noise ratio (SNR) values resulting from the enhanced speech using different steering methods. We present the implementation-specific details for this study in Section C of the Appendix and follow the standard definition of the performance metrics [^17].

![Refer to caption](figures/fig21-ablation.png)

Figure 22. Our proposed world-locked partner localization using HALo provides gains of +1.4 dB SNR in multiparty settings over the head-locked version, i.e., the user’s front-facing direction.

The first observation is that the front-facing direction of the focal user, which is a head-locked version of steering the beamformer, is not effective in multiparty conversations, as shown in Figure 23. This directly motivates our pursuit of a world-locked version of the system, where we can localize conversation partners irrespective of the front-facing direction of the focal user, which clearly offers greater benefit (by an absolute 1.4 dB). Additionally, it also paves the way for more naturalistic conversations, where the focal user is not tempted to proactively look in the direction of the conversation partner to enhance speech, and a world-locked beamformer can be steered based on the localization of the conversation partners.

The second observation is that, in the current state, HALo-based steering outperforms two out of three audio-based baselines by an average of $6\%$, as shown in Figure 23. The third observation is that, interestingly, for extremely noisy samples in the dataset, we can see that the basic audio steering modules are not effective (this behavior is also corroborated by previous works [^77] [^60] [^43]) and that head-orientation-based steering offers a clear advantage. This pattern likely arises from a fundamental difference between modalities: audio-based localization inevitably degrades as SNR decreases, whereas head-orientation signatures are unaffected by noise levels and may even become more informative. Under difficult listening conditions, the focal user may deliberately re‑orient toward conversation partners, producing stronger and more distinctive head‑orientation patterns that facilitate more accurate localization–features that HALo is designed to exploit.

We present the implementation details and performance metrics in Table 4 in the Appendix. These results positively indicate that fusing head-orientation information with audio has the potential to offer superior performance in conversation-focusing applications.

## 5\. Scope and Limitations

Our work studies a large dataset comprising over 71 unique sessions (yielding 7,915 samples), RLR-Chat, one of the few large-scale studies incorporating IMU data in natural, unscripted conversational contexts. However, due to the data collection timeline during 2020–2021, amid the pandemic, only family members participated in the study. We focus on seated conversational settings to balance feasibility and practicality. As a result, the scope of our evaluation is limited in terms of the diversity of social configurations, seating geometries, and room layouts considered, and does not capture conversational dynamics in fully mobile or more socially complex environments.

In this work, we assume that the conversation partners remain fixed during each segment (in this case, 30s in duration). Supporting fully dynamic conditions, such as people leaving or joining, is a practical but very difficult problem, and that is why most previous works on speaker localization using audio [^83] [^44] [^15] or audio-vision [^43] [^71] [^81] also investigate fixed conversation group settings. Recent audio-based works consider formalizing more pressing dynamic cases such as microphone-array movement, i.e., the focal user’s head motion [^60], and noise and reverberation conditions [^61] [^16]. Future efforts can construct large-scale datasets with more diverse and unconstrained scenarios and incorporate behavioral and audio multimodal cues to handle such settings suitably.

While we approached the task of identifying conversation partners as a classification problem using enhanced feature sets or targets, future work could explore advanced strategies, such as ordinal classification frameworks that penalize predictions based on the degree of error.

We will investigate other potential areas, such as inferring speaking states from head movements. Prior works, such as those by [^93] and [^55], indicate that these states manifest in distinct head-orienting behaviors. Although these studies do not directly address voice activity detection, they demonstrate a strong coupling between head orientation and linguistic behavior like turn-taking and speaking status. Manual analyses of group conversations in these works provide compelling evidence for this relationship, which could further inform our research especially CoCo network.

In this work, we demonstrate that head orientation is a promising behavioral modality for inferring a user’s acoustic zones of interest. These findings lay the foundation for the non-trivial, yet promising, integration of such behavioral cues into audio and multisensory processing pipelines. This integration can advance immersive conversation enhancement and hearing aid applications with smartglasses, particularly under challenging acoustic conditions.

## 6\. Conclusion

To develop practical conversation-enhancing technologies for wearable platforms like smart glasses, it is essential to understand users’ preferences for acoustic zones of interest. While several neuroscience studies have highlighted the importance of behavioral modalities such as head orientation for understanding conversational components in controlled settings with small datasets, and deep learning research on large multimodal datasets—particularly audio-visual modalities—has emphasized the value of visual behavioral information in identifying users’ preferred zones of auditory interest, our work explores a more challenging setting: leveraging only behavioral data from Inertial Measurement Units (IMUs) on smart glasses to infer acoustic zones of interest. We formulate and study two practical tasks on a large-scale dataset with minimal a priori information: (1) localizing acoustic zones of interest, achieving an average accuracy of 0.78 and a macro-F1 score of 0.62 for multi-label classification across six discrete zones, and (2) determining the number of conversation partners, achieving an average accuracy of 0.74 in identifying group sizes ranging from 1 to 4 conversation partners. Our results highlight the importance of designing dedicated features, learning architectures, and objective functions, rather than relying on domain-specific statistical rule-based methods or general-purpose time-series representation learning approaches. Additionally, we provide in-depth qualitative analyses of the model’s interpretability, its predictions over extended conversational settings, an end-to-end speech enhancement pipeline that clearly supports the complementary benefits of a behavioral modality like head orientation, and the role of various features and targets in performance. We present a promising direction for leveraging on-device IMU sensors on smart glasses to learn users’ acoustic zones of interest based on head orientation and to inform advanced audio-enhancement solutions on wearables.

## References

## APPENDIX

## Appendix A Additional Details on Data Preparation

### A.1. Dataset Organization

The overall dataset is organized as shown in Figure 24.

![Refer to caption](figures/fig22-dataset-illustrate.png)

Figure 24. (a) Represents the RLR-Chat dataset organization where sessions are manually validated for ordered but non-consecutive 30-second segments, each consisting of 150 frames for a group of participants. (b) illustrates the focal-user’s viewpoint and (c) the exocentric viewpoint for a frame.

### A.2. Implementation Details of Head Orientation Approximation from IMUs

Our primary behavior-modality of exploration is the 6-axis IMU data collected by sensors on smart glasses. As noted by prior works, leveraging the translation from IMUs through standard double integration is prone to errors [^103], and many works propose using physics-guided learnable modules to determine global or relative translational motion [^101]. However, in this case, we analyze seated natural conversations for auditory zones of interest, where translational motion does not offer much benefit. Since our task here is not tightly coupled with accurate head-pose estimation, instead, it focuses on the overall dynamics of head orientation, as evidenced by past neuro-speech studies. Consequently, we determine the approximate head orientation using a simple attitude integration scheme.

The IMU is placed on the legs of the smart glasses, as shown in Figure 5, and is used as a proxy for determining head rotation. The continuous angular velocity $\boldsymbol{\omega}(t)$ is sampled at discrete regular intervals of $\Delta t$, where the instantaneous angular velocity is given as $\boldsymbol{\omega}(t_{n})=[\omega_{x}\,\omega_{y}\,\omega_{z}]^{\mathrm{T}}$ at discrete time $t_{n}=n\Delta t$. To estimate the angular displacement of the head, we leverage a simple attitude integration scheme [^41].

Since the orthogonal matrix used to represent the pure rotation $\theta$ along one of the axes in a three-dimensional space has only four independent elements, a quaternion representation $\mathbf{q}\in\mathbb{R}^{4}$ is used for computational efficiency [^88]. Leveraging key results from [^41], we can describe the change in rotation $\Delta\mathbf{q}$ about the instantaneous axis, $\mathbf{u}=\frac{\boldsymbol{\omega}}{\|\boldsymbol{\omega}\|}$ during $\Delta t$ time units in the IMU’s local time frame (rad/seconds in this case) as:

$$
\Delta\mathbf{q}=\cos\frac{\theta}{2}+\mathbf{u}\sin\frac{\theta}{2}=\cos\frac{\|\boldsymbol{\omega}\|\Delta t}{2}+\frac{\boldsymbol{\omega}}{\|\boldsymbol{\omega}\|}\sin\frac{\|\boldsymbol{\omega}\|\Delta t}{2},
$$

as a quaternion. We can consider the original state as $\mathbf{q}(t)$ rotated to a new state $\mathbf{q}(t+\Delta t)=\Delta\mathbf{q}\,\mathbf{q}(t)$ [^41]. We have,

$$
\displaystyle\mathbf{q}(t+\Delta t)-\mathbf{q}(t)
$$
 
$$
\displaystyle=\left(\cos\frac{\|\boldsymbol{\omega}\|\Delta t}{2}+\frac{\boldsymbol{\omega}}{\|\boldsymbol{\omega}\|}\sin\frac{\|\boldsymbol{\omega}\|\Delta t}{2}\right)\mathbf{q}-\mathbf{q}
$$
 
$$
\displaystyle=\left(-2\sin^{2}\frac{\|\boldsymbol{\omega}\|\Delta t}{4}+\frac{\boldsymbol{\omega}}{\|\boldsymbol{\omega}\|}\sin\frac{\|\boldsymbol{\omega}\|\Delta t}{2}\right)\mathbf{q}
$$

Using the standard time-derivative property of quaternions [^41],

$$
\displaystyle\dot{\mathbf{q}}
$$
 
$$
\displaystyle=\lim_{\Delta t\to 0}\frac{\mathbf{q}(t+\Delta t)-\mathbf{q}(t)}{\Delta t}
$$
 
$$
\displaystyle=\lim_{\Delta t\to 0}\frac{1}{\Delta t}\left(-2\sin^{2}\frac{\|\boldsymbol{\omega}\|\Delta t}{4}+\frac{\boldsymbol{\omega}}{\|\boldsymbol{\omega}\|}\sin\frac{\|\boldsymbol{\omega}\|\Delta t}{2}\right)\mathbf{q}
$$
 
$$
\displaystyle=\frac{\boldsymbol{\omega}}{\|\boldsymbol{\omega}\|}\lim_{\Delta t\to 0}\frac{1}{\Delta t}\sin\left(\frac{\|\boldsymbol{\omega}\|\Delta t}{2}\right)\mathbf{q}
$$
 
$$
\displaystyle=\frac{\boldsymbol{\omega}}{\|\boldsymbol{\omega}\|}\frac{d}{dt}\sin\left(\frac{\|\boldsymbol{\omega}\|t}{2}\right)\bigg|_{t=0}\mathbf{q}
$$
 
$$
\displaystyle=\frac{1}{2}\boldsymbol{\omega}\mathbf{q}
$$
 
$$
\displaystyle=\frac{1}{2}\begin{bmatrix}-\omega_{x}q_{x}-\omega_{y}q_{y}-\omega_{z}q_{z}\\
\omega_{x}q_{w}+\omega_{y}q_{z}-\omega_{z}q_{y}\\
\omega_{y}q_{w}+\omega_{z}q_{x}-\omega_{x}q_{z}\\
\omega_{z}q_{w}+\omega_{x}q_{y}-\omega_{y}q_{x}\end{bmatrix}
$$

The definition of $\boldsymbol{\Omega}$ operator follows,

$$
\boldsymbol{\Omega}(\boldsymbol{\omega})=\begin{bmatrix}0&-\boldsymbol{\omega}^{T}\\
\boldsymbol{\omega}&-[\boldsymbol{\omega}]_{\times}\end{bmatrix}=\begin{bmatrix}0&-\omega_{x}&-\omega_{y}&-\omega_{z}\\
\omega_{x}&0&-\omega_{z}&\omega_{y}\\
\omega_{y}&\omega_{z}&0&-\omega_{x}\\
\omega_{z}&-\omega_{y}&\omega_{x}&0\end{bmatrix}
$$

We leverage [^88] ’s results to arrive at the closed form solution for the new rotation, $\mathbf{q}_{t+1}$

$$
\mathbf{q}_{t+1}=\left[\cos\left(\frac{\|\boldsymbol{\omega}\|\Delta t}{2}\right)\mathbf{I}_{4}+\frac{1}{\|\boldsymbol{\omega}\|}\sin\left(\frac{\|\boldsymbol{\omega}\|\Delta t}{2}\right)\boldsymbol{\Omega}(\boldsymbol{\omega})\right]\mathbf{q}_{t}.
$$

The overall pseudocode to implement this is shown in Algorithm 1. The device used for data collection was a pair of Aria glasses [^19], which experienced clock drift between devices. To mitigate this, the short-term audio’s cross-correlation is used to fit a linear regressor and correct for the drift. Thus in this head-orientation extraction process, we also provide an opportunity to correct for any device-specific calibrations by converting the obtained $\mathbf{q}_{t+1}$ to the $\mathbb{R}^{3}$ coordinate space and cross product with $\mathbf{R}_{\text{ref}}$, a sensor-specific correction matrix.

Algorithm 1 Overview of Quaternion Update for Rotation Matrix Computation.

Input: $\mathbf{g}$: gyroscope readings (rad/s)

Input: $\mathbf{q}_{\text{prev}}$: previous quaternion

Output: $\mathbf{q}$: updated quaternion

procedure UpdateHO($\mathbf{g},\mathbf{q}_{\text{prev}},\Delta t$)

  Initialize $\boldsymbol{\Omega}$ from $\mathbf{g}$ following Equation 2

  Compute angular velocity magnitude $w=\|\mathbf{g}\|$

  Calculate rotation matrix $\mathbf{A}$ from Equation 3: 
$$
\mathbf{A}=\cos\left(\frac{w\cdot\Delta t}{2}\right)\cdot\mathbf{I}_{4}+\frac{\sin\left(\frac{w\cdot\Delta t}{2}\right)}{w}\cdot\boldsymbol{\Omega}
$$

  Update quaternion $\mathbf{q}=\mathbf{A}\cdot\mathbf{q}_{\text{prev}}$

  Normalize quaternion $\mathbf{q}=\frac{\mathbf{q}}{\|\mathbf{q}\|}$

  return $\mathbf{q}$

end procedure

if $\mathbf{q}_{0}$ is not provided then

  Initialize $\mathbf{q}_{0}\leftarrow[0,0,0,1]$

end if

Initialize quaternion array $\mathbf{Q}\leftarrow\mathbf{0}_{N\times 4}$, where $N=\text{len}(\mathbf{g})$

for each sample $n\in\{0,\ldots,N-1\}$ do

  if $n=0$ then

    $\mathbf{q}_{\text{prev}}\leftarrow\mathbf{q}_{0}$

  else

    $\mathbf{q}_{\text{prev}}\leftarrow\mathbf{Q}[n-1,:]$

  end if

   $\mathbf{Q}[n,:]\leftarrow\textsc{UpdateHO}(\mathbf{g}[n,:],\mathbf{q}_{\text{prev}})$

end for

Retrieve IMU calibration data to compute reference rotation $\mathbf{R}_{\text{ref}}$

for each index $i\in\text{imu\_frame\_idx}$ do

  Compute rotation matrix: 
$$
\mathbf{R}_{\text{final}}=\mathbf{R}_{\text{ref}}\cdot\textsc{rotation\_from\_quat}(\mathbf{Q}[i,:])\cdot\mathbf{R}_{\text{ref}}^{-1}
$$

end for

return $\mathbf{R}_{\text{final}}$

After computing the rotation matrix, $\mathbf{R}_{\text{final}}$, we transform a point, $\mathbf{v}_{\text{init\_xyz}}$, in the Cartesian plane to $\mathbf{v}_{\text{fin\_ae}}$ in the spherical coordinate system as shown in Algorithm 2 using standard techniques [^97] under some assumptions: (1) we do not model any translational motion and keep $d=1$, (2) the front-facing direction of the participant wearing glasses is the origin, i.e., (azimuth, elevation) = $(0^{\circ},0^{\circ})$.

Algorithm 2 Overview of Head Rotation Computation.

Input: $\mathbf{v}_{\text{init}}$: initial head orientation (azimuth, elevation) = $(0,0)$

Input: $d=1$

Input: $\mathbf{R}_{\text{final}}$: output from Algorithm 1 (or supplied externally)

Output: $\mathbf{v}_{\text{fin\_ae}}$: final head orientation (azimuth, elevation)

 $\mathbf{v}_{\text{init\_xyz}}=\textsc{sph2cart}(\mathbf{v}_{\text{init}},d)$ $\mathbf{v}_{\text{fin\_xyz}}=\mathbf{R}_{\text{final}}\cdot\mathbf{v}_{\text{init\_xyz}}$ $\mathbf{v}_{\text{fin\_ae}}=\textsc{cart2sph}(\mathbf{v}_{\text{fin\_xyz}})$

## Appendix B Definitions of Performance Metrics

We use the following metrics for the localization of the conversation partners task. Consider the predicted vector, $\hat{y}\in\{0,1\}^{6}$, and the actual vector, $y\in\{0,1\}^{6}$.

$$
\text{Hamming Score}=\frac{1}{n}\sum_{i=1}^{n}\frac{|y_{i}\cap\hat{y_{i}}|}{|y_{i}\cup\hat{y_{i}}|}
$$
 
$$
\text{Logit-wise Accuracy}=\frac{1}{n}\sum_{i=1}^{n}\mathbb{1}(\hat{y_{i}}=y_{i})
$$

where $\mathbb{1}$ is the indicator that the predicted class $\hat{y_{i}}$ is equal to the true label, $y_{i}$.

$$
\text{Logit-wise F1}=\frac{2\times\text{Precision}_{\text{logit}}\times\text{Recall}_{\text{logit}}}{\text{Precision}_{\text{logit}}+\text{Recall}_{\text{logit}}}
$$
 
$$
\text{Macro F1}=\frac{1}{C}\sum_{i=1}^{C}\frac{2\times\text{Precision}_{i}\times\text{Recall}_{i}}{\text{Precision}_{i}+\text{Recall}_{i}},\text{where C=6}
$$

For the task of identifying the number of conversation partners, we leverage the accuracy metric, as

$$
\text{Accuracy}=\frac{\text{TP}+\text{TN}}{\text{TP}+\text{TN}+\text{FP}+\text{FN}}
$$

where: - TP (True Positives) are instances correctly predicted as positive, - TN (True Negatives) are instances correctly predicted as negative, - FP (False Positives) are instances incorrectly predicted as positive, - FN (False Negatives) are instances incorrectly predicted as negative.

## Appendix C Implementation Details of the Minimal Speech-Enhancement System in Section

In this section, we describe the implementation details of the minimal end-to-end system discussed in Section 2.4. We use the EasyCom dataset [^17], which provides multi-microphone recordings collected using a pair of AR smart glasses equipped with six microphones distributed around the frame. The primary reason for choosing EasyCom in this study is that it includes array transfer functions, enabling the construction of a fully functional end-to-end speech-enhancement pipeline. The dataset includes synchronized headset signals, OptiTrack-based head-pose data, and ground-truth speech labels for multi-party conversational scenes. Although EasyCom does not contain raw IMU measurements, since the IMU-based pose estimates closely approximate short-segment OptiTrack estimates (as validated in Figure 19), it is suitable for this analysis.

To compare orientation-based steering with audio-based steering, we implement three widely used direction-of-arrival (DoA) estimation methods—MUSIC [^83], GCC-PHAT [^44], and SRP-PHAT [^15]. Each of these algorithms infers the dominant sound direction by exploiting inter-microphone phase differences, but they differ in how they model spatial correlation and suppress reverberation.

Table 4 summarizes the resulting speech enhancement performance in terms of intelligibility and SNR improvements. While the absolute SNR values remain modest—consistent with the findings in the original EasyCom paper—this primarily reflects the inherently noisy conditions and complex conversational dynamics in the dataset. Our goal in this minimal implementation is not maximizing absolute enhancement scores, but demonstrating a fair, interpretable comparison between audio-driven and orientation-driven steering strategies using simple baseline components. The results confirm that orientation-informed steering remains stable under acoustically challenging conditions and can serve as an effective augmentation to conventional audio-based approaches for robust multimodal speech enhancement.

Table 4. Comparison of head-orientation-based and audio-based steering methods for speech enhancement.

<table><thead><tr><th>Metric</th><th>Raw</th><th colspan="2">Head-orientation-based</th><th colspan="3">Audio-based</th></tr><tr><th></th><th>Reference Mic</th><th>Frontal (0 <sup>∘</sup>)</th><th>Halo (Ours)</th><th>MUSIC</th><th>GCC-PHAT</th><th>SRP</th></tr></thead><tbody><tr><td>SNR (dB)</td><td>-10.55</td><td>-9.30</td><td>-8.63</td><td>-9.26</td><td>-9.11</td><td>-8.34</td></tr><tr><td>STOI</td><td>0.34</td><td>0.39</td><td>0.41</td><td>0.40</td><td>0.41</td><td>0.38</td></tr><tr><td>PESQ</td><td>1.10</td><td>1.16</td><td>1.15</td><td>1.15</td><td>1.16</td><td>1.10</td></tr></tbody></table>

[^1]: Evaluation of head posture using an inertial measurement unit. Scientific reports 11 (1), pp. 19911. Cited by: §2.2.

[^2]: Salsa: a novel dataset for multimodal group behavior analysis. IEEE transactions on pattern analysis and machine intelligence 38 (8), pp. 1707–1720. Cited by: Table 1.

[^3]: Recognizing visual focus of attention from head pose in natural meetings. IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics) 39 (1), pp. 16–33. Cited by: §4.2.

[^4]: Robust frame-level speaker localization in reverberant and noisy environments by exploiting phase difference losses. In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 1–5. Cited by: §1, §3.4.1.

[^5]: Towards sensorized glasses: a smart wearable system for head movement monitoring. In 2024 9th International Conference on Smart and Sustainable Technologies (SpliTech), pp. 1–6. Cited by: §2.2.

[^6]: Statistical methods for assessing agreement between two methods of clinical measurement. Lancet. Cited by: §4.6.

[^7]: Auditory and visual orienting responses in listeners with and without hearing-impairment. The Journal of the Acoustical Society of America 127 (6), pp. 3678–3688. Cited by: §1, §1.

[^8]: Smart room: participant and speaker localization and identification. In Proceedings.(ICASSP’05). IEEE International Conference on Acoustics, Speech, and Signal Processing, 2005., Vol. 2, pp. ii–1117. Cited by: §1.

[^9]: The matchnmingle dataset: a novel multi-sensor resource for the analysis of social interactions and group dynamics in-the-wild during free-standing conversations and speed dates. IEEE Transactions on Affective Computing 12 (1), pp. 113–130. Cited by: Table 1.

[^10]: Dynamics of person-to-person interactions from distributed rfid sensor networks. PloS one 5 (7), pp. e11596. Cited by: Table 1.

[^11]: ClearBuds: wireless binaural earbuds for learning-based speech enhancement. In Proceedings of the 20th Annual International Conference on Mobile Systems, Applications and Services, pp. 384–396. Cited by: §1.

[^12]: Hearable devices with sound bubbles. Nature Electronics, pp. 1–12. Cited by: §1.

[^13]: Probabilistic speaker localization in noisy environments by audio-visual integration. In 2006 IEEE/RSJ International Conference on Intelligent Robots and Systems, pp. 4704–4709. Cited by: §1.

[^14]: Your turn to speak? audiovisual social attention in the lab and in the wild. Visual Cognition 30 (1-2), pp. 116–134. Cited by: item 1.

[^15]: A real-time srp-phat source location implementation using stochastic region contraction (src) on a large-aperture microphone array. In 2007 IEEE International Conference on Acoustics, Speech and Signal Processing-ICASSP’07, Vol. 1, pp. I–121. Cited by: Appendix C, §4.6, §5.

[^16]: A classification-aided framework for non-intrusive speech quality assessment. In 2019 IEEE Workshop on Applications of Signal Processing to Audio and Acoustics (WASPAA), pp. 100–104. Cited by: §5.

[^17]: Easycom: an augmented reality dataset to support algorithms for easy communication in noisy environments. arXiv preprint arXiv:2107.04174. Cited by: Appendix C, §4.6.

[^18]: Some signals and rules for taking speaking turns in conversations.. Journal of personality and social psychology 23 (2), pp. 283. Cited by: §2.1.

[^19]: Project aria: a new tool for egocentric multi-modal ai research. arXiv preprint arXiv:2308.13561. Cited by: §A.2, §3.1, §3.1.

[^20]: A density-based algorithm for discovering clusters in large spatial databases with noise. In kdd, Vol. 96, pp. 226–231. Cited by: §3.5.

[^21]: Head orientation estimation from multiple microphone arrays. In 2020 28th European Signal Processing Conference (EUSIPCO), pp. 491–495. Cited by: §2.2.

[^22]: Directional source separation for robust speech recognition on smart glasses. In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 1–5. Cited by: §3.4.1.

[^23]: Head motion tracking through in-ear wearables. In Proceedings of the 1st International Workshop on Earable Computing, pp. 8–13. Cited by: Table 1.

[^24]: On head motion for recognizing aggression and negative affect during speaking and listening. In Proceedings of the 25th International Conference on Multimodal Interaction, pp. 455–464. Cited by: §2.1.

[^25]: Visual speaker localization aided by acoustic models. In Proceedings of the 17th ACM international conference on Multimedia, pp. 195–202. Cited by: §1.

[^26]: Gaze cueing of attention: visual attention, social cognition, and individual differences.. Psychological bulletin 133 (4), pp. 694. Cited by: §1, item 1.

[^27]: Digital voicing of silent speech. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), B. Webber, T. Cohn, Y. He, and Y. Liu (Eds.), Online, pp. 5521–5530. External Links: [Link](https://aclanthology.org/2020.emnlp-main.445), [Document](https://dx.doi.org/10.18653/v1/2020.emnlp-main.445) Cited by: §4.5.

[^28]: The speech, spatial and qualities of hearing scale (ssq). International journal of audiology 43 (2), pp. 85–99. Cited by: §1.

[^29]: Ehtrack: earphone-based head tracking via only acoustic signals. IEEE Internet of Things Journal. Cited by: §2.3.

[^30]: Detecting conversing groups using social dynamics from wearable acceleration: group size awareness. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 2 (4), pp. 1–24. Cited by: Table 1.

[^31]: Frequency and velocity of rotational head perturbations during locomotion. Experimental brain research 70, pp. 470–476. Cited by: §3.1.

[^32]: Speech-related body movement in aphasia: period analysis of upper arms and head movement. Brain and Language 41 (3), pp. 339–366. Cited by: §2.1.

[^33]: Evaluation of the intel realsense t265 for tracking natural human head motion. Scientific reports 11 (1), pp. 12486. Cited by: §2.2.

[^34]: Movement and gaze behavior in virtual audiovisual listening environments resembling everyday life. Trends in Hearing 23, pp. 2331216519872362. Cited by: §1, §1, item 3.

[^35]: Gaze-enhanced multimodal turn-taking prediction in triadic conversations. arXiv preprint arXiv:2505.13688. Cited by: item 1, §3.1.

[^36]: On the interaction of head and gaze control with acoustic beam width of a simulated beamformer in a two-talker scenario. Trends in Hearing 23, pp. 2331216519876795. Cited by: item 2, item 3.

[^37]: A robust adaptive beamformer for microphone arrays with a blocking matrix using constrained adaptive filters. IEEE Transactions on signal processing 47 (10), pp. 2677–2684. Cited by: item 2, item 3.

[^38]: Advances in microphone array processing and multichannel speech enhancement. In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 1–5. Cited by: item 2, item 3.

[^39]: Classifying social actions with a single accelerometer. In Proceedings of the 2013 ACM international joint conference on Pervasive and ubiquitous computing, pp. 207–210. Cited by: Table 1.

[^40]: Apple airpods. Note: Accessed: 2024-12-16 External Links: [Link](https://www.apple.com/airpods/) Cited by: §2.3.

[^41]: Quaternions. Com S 477, pp. 577. Cited by: §A.2, §A.2, §A.2, §A.2, §3.2, §3.2.

[^42]: Egocentric pose estimation from human vision span. In 2021 IEEE/CVF International Conference on Computer Vision (ICCV), pp. 10986–10994. Cited by: §2.2.

[^43]: Egocentric deep multi-channel audio-visual active speaker localization. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 10544–10552. Cited by: §1, §4.6, §5.

[^44]: The generalized correlation method for estimation of time delay. IEEE transactions on acoustics, speech, and signal processing 24 (4), pp. 320–327. Cited by: Appendix C, §4.6, §5.

[^45]: Using inertial sensors for position and orientation estimation. Foundations and Trends in Signal Processing 11 (1–2), pp. 1–153. External Links: [Document](https://dx.doi.org/10.1561/2000000094) Cited by: §3.2.

[^46]: Head-orienting behaviors during simultaneous speech detection and localization. Frontiers in Psychology 15, pp. 1425972. Cited by: §4.3.

[^47]: Learning to predict gaze in egocentric video. In Proceedings of the IEEE international conference on computer vision, pp. 3216–3223. Cited by: §1.

[^48]: Speech enhancement: theory and practice. CRC press. Cited by: §1.

[^49]: Sound source selection based on head movements in natural group conversation. Trends in Hearing 26, pp. 23312165221097789. Cited by: §1.

[^50]: Investigating age, hearing loss, and background noise effects on speaker-targeted head and eye movements in three-way conversations. The Journal of the Acoustical Society of America 149 (3), pp. 1889–1900. Cited by: item 3, §4.3.

[^51]: Natural head position and natural head orientation: basic considerations in cephalometric analysis and research. European Journal of Orthodontics 17 (2), pp. 111–120. Cited by: §2.2.

[^52]: Assessing the ease of conversation in multi-group conversation spaces: effect of background music volume on acoustic comfort in a café. Building Acoustics 27 (2), pp. 137–153. Cited by: §1.

[^53]: Analysis of social interactions through mobile phones. Mobile Networks and Applications 17, pp. 808–819. Cited by: Table 1.

[^54]: 360° sound localization support system for deaf and hard-of-hearing people using smartglasses equipped with two microphone. In 2024 IEEE/SICE International Symposium on System Integration (SII), pp. 295–300. Cited by: §1.

[^55]: Linguistic functions of head movements in the context of speech. Journal of pragmatics 32 (7), pp. 855–878. Cited by: §1, §2.1, §4.2, §5.

[^56]: Older adults show a more sustained pattern of effortful listening than young adults.. Psychology and aging 36 (4), pp. 504. Cited by: §1.

[^57]: Pragmatics of conversation and communication in noisy settings. Journal of Pragmatics 39 (12), pp. 2159–2184. Cited by: §1.

[^58]: Potential of augmented reality platforms to improve individual hearing aids and to support more ecologically valid research. Ear and hearing 41, pp. 140S–146S. Cited by: §1, §2.4.

[^59]: U-har: a convolutional approach to human activity recognition combining head and eye movements for context-aware smart glasses. Proceedings of the ACM on Human-Computer Interaction 6 (ETRA), pp. 1–19. Cited by: §2.3.

[^60]: Study of speaker localization under dynamic and reverberant environments. arXiv preprint arXiv:2311.16927. Cited by: §4.6, §5.

[^61]: Improved direction of arrival estimations with a wearable microphone array for dynamic environments by reliability weighting. EURASIP Journal on Advances in Signal Processing 2025 (1), pp. 42. Cited by: §5.

[^62]: I. MLKDD Multi-label classification. Cited by: §4.1.

[^63]: Non-verbal hands-free control for smart glasses using teeth clicks. arXiv preprint arXiv:2408.11346. Cited by: §2.4.

[^64]: Person identification with wearable sensing using missing feature encoding and multi-stage modality fusion. In ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 1–2. Cited by: §4.5.

[^65]: Can llms understand unvoiced speech? exploring emg-to-text conversion with llms. arXiv preprint arXiv:2506.00304. Cited by: §3.4.2, §4.2.

[^66]: MAESTRO: adaptive sparse attention and robust learning for multimodal dynamic time series. arXiv preprint arXiv:2509.25278. Cited by: §3.4.2.

[^67]: Imuposer: full-body pose estimation using imus in phones, watches, and earbuds. In Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems, pp. 1–12. Cited by: §3.4.2.

[^68]: Gazeformer: scalable, effective and fast prediction of goal-directed human attention. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 1441–1450. Cited by: §1.

[^69]: Personalized signal-independent beamforming for binaural hearing aids. The Journal of the Acoustical Society of America 145 (5), pp. 2971–2981. Cited by: §1.

[^70]: Head gesture recognition in intelligent interfaces: the role of context in improving recognition. In Proceedings of the 11th international conference on Intelligent user interfaces, pp. 32–38. Cited by: §2.3.

[^71]: Self-motion as supervision for egocentric audiovisual localization. In ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 7835–7839. Cited by: §1, §3.1, §3.1, Table 1, §4.3, §4.6, §5.

[^72]: Application of optitrack motion capture systems in human movement analysis: a systematic literature review. Recent Innovations in Mechatronics 5 (1), pp. 1–9. Cited by: §3.1.

[^73]: OptiTrack - motion capture systems. External Links: [Link](https://optitrack.com/) Cited by: §3.1, §3.3.

[^74]: TimeSliver: symbolic-linear decomposition for explainable time series classification. arXiv preprint arXiv:2601.21289. Cited by: §4.3.

[^75]: VII. note on regression and inheritance in the case of two parents. Proceedings of the Royal Society of London 58 (347-352), pp. 240–242. External Links: [Document](https://dx.doi.org/10.1098/rspl.1895.0041), [Link](https://royalsocietypublishing.org/doi/abs/10.1098/rspl.1895.0041), https://royalsocietypublishing.org/doi/pdf/10.1098/rspl.1895.0041 Cited by: §4.3.

[^76]: A low-power speech recognizer and voice activity detector using deep neural networks. IEEE Journal of Solid-State Circuits 53 (1), pp. 66–75. Cited by: §3.5.

[^77]: Robust audio–visual speaker localization in noisy aircraft cabins for inflight medical assistance. Sensors 25 (18), pp. 5827. Cited by: §4.6.

[^78]: Classifier chains for multi-label classification. Machine learning 85, pp. 333–359. Cited by: §4.1.

[^79]: Differences in head orientation between speakers and listeners in multi-party conversations. International Journal HCS. Cited by: §4.2.

[^80]: Foveated beamforming for augmented reality devices and wearables. Google Patents. Note: US Patent 11,967,335 Cited by: §1.

[^81]: Egocentric auditory attention localization in conversations. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pp. 14663–14674. Cited by: §5.

[^82]: Estimating three-dimensional orientation of human body parts by inertial/magnetic sensing. Sensors 11 (2), pp. 1489–1525. External Links: [Document](https://dx.doi.org/10.3390/s110201489) Cited by: §3.2.

[^83]: Multiple emitter location and signal parameter estimation. IEEE transactions on antennas and propagation 34 (3), pp. 276–280. Cited by: Appendix C, §4.6, §5.

[^84]: Turn-taking resources employed by congenitally blind conversers. Communication Studies 41 (2), pp. 161–182. Cited by: §2.1.

[^85]: Voice localization using nearby wall reflections. In Proceedings of the 26th Annual International Conference on Mobile Computing and Networking, pp. 1–14. Cited by: §2.2.

[^86]: Eye, head and torso coordination during gaze shifts in virtual reality. ACM Transactions on Computer-Human Interaction (TOCHI) 27 (1), pp. 1–40. Cited by: §1, §2.3.

[^87]: Bimodalgaze: seamlessly refined pointing with gaze and filtered gestural head movement. In ACM Symposium on Eye Tracking Research and Applications, pp. 1–9. Cited by: §2.3.

[^88]: Quaternion kinematics for the error-state kalman filter. arXiv preprint arXiv:1711.02508. Cited by: §A.2, §A.2, §3.2, §3.2.

[^89]: Recognizing activities of daily living using multi-sensor smart glasses. In 2023 46th MIPRO ICT and Electronics Convention (MIPRO), pp. 397–402. Cited by: §2.3.

[^90]: Head orientation and gaze direction in meetings. In CHI’02 Extended Abstracts on Human Factors in Computing Systems, pp. 858–859. Cited by: §2.1.

[^91]: Negative consequences of hearing impairment in old age: a longitudinal analysis. The Gerontologist 40 (3), pp. 320–326. Cited by: §1.

[^92]: Multimodal joint head orientation estimation in interacting groups via proxemics and interaction dynamics. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 5 (1), pp. 1–22. Cited by: §1, §4.2.

[^93]: Noggin nodding: head movement correlates with increased effort in accelerating speech production tasks. Frontiers in Psychology 10, pp. 2459. Cited by: §1, §2.1, §5.

[^94]: Estimating head motion from egocentric vision. In Proceedings of the 20th ACM International Conference on Multimodal Interaction, pp. 342–346. Cited by: §2.2.

[^95]: Beamforming: a versatile approach to spatial filtering. IEEE assp magazine 5 (2), pp. 4–24. Cited by: §1.

[^96]: Attention is all you need. Advances in Neural Information Processing Systems. Cited by: §3.4.2.

[^97]: Spherical coordinates. https://mathworld. wolfram. com/. Cited by: §A.2, §3.2.

[^98]: An introduction to inertial navigation. Technical report Technical Report UCAM-CL-TR-696, University of Cambridge, Computer Laboratory. External Links: [Link](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-696.pdf) Cited by: §3.2.

[^99]: Binaural audio-visual localization. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 35, pp. 2961–2968. Cited by: §1.

[^100]: Characteristics of real-world signal to noise ratios and speech listening situations of older adults with mild to moderate hearing loss. Ear and hearing 39 (2), pp. 293–304. Cited by: §3.1.

[^101]: MobilePoser: real-time full-body pose estimation and 3d human translation from imus in mobile consumer devices. In Proceedings of the 37th Annual ACM Symposium on User Interface Software and Technology, pp. 1–11. Cited by: §A.2, §3.2, §3.4.2.

[^102]: FoVNet: configurable field-of-view speech enhancement with low computation and distortion for smart glasses. In Interspeech 2024, pp. 3350–3354. External Links: [Document](https://dx.doi.org/10.21437/Interspeech.2024-2124), ISSN 2958-1796 Cited by: §1, §2.4, §3.4.1.

[^103]: RIDI: robust imu double integration. In Proceedings of the European conference on computer vision (ECCV), pp. 621–636. Cited by: §A.2, §3.2.

[^104]: Soundr: head position and orientation prediction using a microphone array. In Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems, pp. 1–12. Cited by: §2.2.

[^105]: Model-based head orientation estimation for smart devices. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 5 (3), pp. 1–24. Cited by: §1, §2.3.

[^106]: Deepear: sound localization with binaural microphones. IEEE Transactions on Mobile Computing 23 (1), pp. 359–375. Cited by: §2.2.

[^107]: Gazedock: gaze-only menu selection in virtual reality using auto-triggering peripheral menu. In 2022 IEEE Conference on Virtual Reality and 3D User Interfaces (VR), pp. 832–842. Cited by: §2.3.

[^108]: Hearing loss detection from facial expressions in one-on-one conversations. In ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 5460–5464. Cited by: §3.1, Table 1.

[^109]: Spherical world-locking for audio-visual localization in egocentric videos. In European Conference on Computer Vision (ECCV), Cited by: §3.3.

[^110]: Spherical world-locking for audio-visual localization in egocentric videos. In European Conference on Computer Vision, pp. 256–274. Cited by: §3.1, §3.1, Table 1.

[^111]: Are transformers effective for time series forecasting?. In Proceedings of the AAAI conference on artificial intelligence, Vol. 37, pp. 11121–11128. Cited by: §3.4.2.

[^112]: WearSE: enabling streaming speech enhancement on eyewear using acoustic sensing. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 9 (1), pp. 1–30. Cited by: §2.4.

[^113]: Informer: beyond efficient transformer for long sequence time-series forecasting. In Proceedings of the AAAI conference on artificial intelligence, Vol. 35, pp. 11106–11115. Cited by: §4.2, §4.2.