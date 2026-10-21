# Active Noise Control for Augmented Reality Glasses using Virtual Sensing with Directional Robustness

Nitay Peled, Boaz Rafaely

School of Electrical and Computer Engineering

Ben-Gurion University of the Negev

Beer-Sheva, Israel

Email: nitaype@post.bgu.ac.il, br@bgu.ac.il

Abstract—Active noise control (ANC) is an established technique for mitigating acoustic noise, successfully implemented in various commercial applications. However, the application of ANC to augmented reality (AR) glasses remains an emerging area, where a key challenge is the lack of a microphone at the user’s ear. This paper first validates the necessity of virtual sensing techniques for this specific geometry and investigates the Auxiliary Filter (AF) method as a potential solution. We present a theoretical analysis of the method’s directional sensitivity, enabling the prediction of the system’s robustness when the noise direction deviates from the calibration angle. Simulation results confirm that while a fixed AF is effective under matched conditions, it suffers significant degradation under mismatch, consistent with the theoretical predictions. To address this limitation, we propose and evaluate a solution using a finite bank of auxiliary filters that are selected based on the noise source direction of arrival. The results demonstrate that this filter bank approach significantly recovers performance compared to a fixed filter, offering a practical alternative to continuous recalibration in dynamic acoustic environments.

Index Terms—Active noise control, Augmented reality, Virtual sensing, Auxiliary filter, Acoustic signal processing

## I. INTRODUCTION

Active noise control (ANC) is an established technique for addressing the problem of everyday acoustic noise, in which a loudspeaker cancels unwanted sound by generating antinoise of equal magnitude and opposite phase [1], [2]. Over the past few decades, significant advancements have been made in ANC algorithms, which have been successfully implemented in various practical applications [3]. These include headphones, headrests, and more [4]. While well established in some domains, the application of ANC to augmented reality (AR) glasses remains an emerging field of research.

ANC systems utilize microphones to acquire error and optionally reference signals, then process these signals to finally drive loudspeakers that aim to attenuate noise at a desired location [5]. AR glasses can include microphones and loudspeakers around the glasses’ frame, making them applicable to ANC. However, they typically do not include a microphone at the ear, as may be desired. Furthermore, the limitation of having the microphones fixed on the frame of the glasses introduces a causality issue as it allows noise to arrive from directions where the sound wave reaches the ear before reaching the microphone.

Several recent works have investigated ANC systems related to AR-glasses. The study in [6] demonstrated directional noise reduction in an AR-glasses simulation but relied on binaural error microphones, which may not be available in practice. Other studies [7], [8] examined head-mounted arrangements with certain similarities to AR glasses; however, their microphone placements and operating conditions—such as using an error microphone very close to the ear or focusing on magnetic resonance noise scenarios—differ from those feasible in actual AR-glasses designs.

While solutions to the problem of the absence of an error microphone at the ear was not studied specifically for AR glasses, it was studied quite comprehensively in the general case. This limitation is typically addressed by virtual sensing (VS) techniques. VS methods enable ANC systems to attenuate sound pressure at locations where no physical microphones are present [9]. Several recent studies have analyzed and compared different VS approaches, including the Auxiliary Filter (AF) method [10]–[13], which is the method considered here. Although it is a promising solution, the method requires calibration, or offline training, and its performance may significantly degrade with mismatch in conditions between training and control, necessitating re-training [14], [15]. Consequently, several techniques for online adaptation of the AF have been proposed in recent years [14]–[16]. Contemporary approaches rely on a bank of trained AFs to cover a range of conditions. While promising, they have not been studied previously for ANC in AR glasses.

This paper presents a comprehensive analysis of performance for ANC in simulated AR glasses, using the AF method under free-field conditions with a noise source having variable direction-of-arrival (DOA). The main contributions are: (i) highlighting the need for a virtual microphone in ANC for AR glasses, (ii) presenting the limitation of ANC with a fixed AF when noise-source direction changes, and (iii) demonstrating the advantage of using AF bank to improve robustness to a change in noise-source DOA.

## II. ANC WITH AN AUXILIARY FILTER

The ANC system assumed in this work is based on an AF and comprises a reference microphone, a monitoring microphone, a virtual microphone, and a control loudspeaker, and is based on [12]. All microphones are used during the training stage, whereas during the control stage the virtual microphone is assumed to be inaccessible. The virtual microphone signal in the frequency domain is given by

$$
E _ {v} (\omega) = P _ {v} (\omega) X (\omega) + S _ {v} (\omega) W (\omega) X (\omega),\tag{1}
$$

where $X ( \omega )$ is the reference signal; $P _ { v } ( \omega )$ and $S _ { v } ( \omega )$ denote the virtual primary and virtual secondary paths, respectively; $W ( \omega )$ is the control filter; and ω denotes frequency. The monitoring microphone signal $E _ { m } ( \omega )$ is defined analogously to (1), with $P _ { v } ( \omega )$ and $S _ { v } ( \omega )$ replaced by the monitoring primary and secondary paths, $P _ { m } ( \omega )$ and $S _ { m } ( \omega )$ . During the control stage, the controller is adapted using a modified filtered-x least mean squares (FxLMS) algorithm [1]. The error signal used for adaptation, is given by

$$
E _ {h} (\omega) = E _ {m} (\omega) - H (\omega) X (\omega),\tag{2}
$$

as shown in Fig. 1, which presents a block diagram of the system. As in the FxLMS algorithm, the reference signal used for adaptation is prefiltered using an estimate of the virtual secondary path $\hat { S } _ { m } ( \omega )$ (see Fig. 1). Additional details on the AF method can be found in [12], [13]. For the present analysis, the optimal AF in the frequency domain is given by

$$
H _ {0} (\omega) = P _ {m} (\omega) - \frac {S _ {v} (\omega)}{S _ {m} (\omega)} P _ {v} (\omega).\tag{3}
$$

With the optimal AF, $E _ { h } ( \omega )$ represents an error signal that tend to zero when the control filter converges to the optimal filter that minimizes the error at the virtual microphone, i.e.,

$$
W _ {0} (\omega) = - \frac {P _ {v} (\omega)}{S _ {v} (\omega)}.\tag{4}
$$

## III. THEORETICAL SENSITIVITY ANALYSIS OF THE OPTIMAL AF

The aim of this section is to develop a theoretical analysis that will assist in the understanding of the directional sensitivity of the AF. This will allow some prediction of the expected robustness of a fixed AF to changes in the direction of the primary noise source. To develop this theoretical insight, we consider an AR-glasses configuration equipped with microphones and a loudspeaker, arranged in accordance with the conventional AF system described in Section II and Fig. 1. A free-field acoustic environment is assumed for simplicity, in which the system is designed to attenuate noise at the wearer’s ear (the virtual microphone) originating from a single primary source with an arbitrary DOA. Both the primary and secondary sources are modeled as point sources; however, later in this section, the primary disturbance is approximated as a plane wave. Additionally, the primary noise is assumed to be observed at all microphones in the system, whereas the contribution of the secondary source at the reference microphone is neglected for simplicity. The coordinate system is centered at the reference microphone, with the glasses facing the positive x-axis such that the reference and monitor microphones lie in the xy-plane. Furthermore, the primary source is restricted to the xy-plane, where its DOA is given by the azimuthal angle ϕ, defined from the positive x-axis toward the positive y-axis. The geometric arrangement used for the analysis is shown in Fig. 2.

![](figures/09f248babab91e321f2c39df1ee1a19dd9749118fe31923139cbf81ab7153a46.jpg)  
Fig. 1: Block diagram of the ANC system including the AF.

![](figures/0670fdb03cc6014bb15896305ae10df0ab79489dd3077e23682cdc0608214326.jpg)  
Fig. 2: AR glasses setup illustrating the positions of the microphones, along with the primary and secondary sources. This arrangement is used throughout the analysis and simulations.

Applying this model to the transfer functions in Eq. (3), we can express the optimal AF as

$$
H _ {o} (\omega , \phi) = e ^ {- j \frac {\omega}{c} d _ {m} \cos (\phi_ {m})} - G (\omega) e ^ {- j \frac {\omega}{c} d _ {v} \cos (\phi_ {v})}\tag{5}
$$

where $\phi _ { m }$ and $\phi _ { v }$ denote primary source angles relative to the reference–monitor and reference–virtual axes, respectively (see Fig. 2), both of which are implicit functions of ϕ; $d _ { m }$ and $d _ { v }$ are the distances separating the reference-monitor and reference-virtual microphone pairs, respectively; $G ( \omega ) \triangleq$ $\frac { S _ { v } ( \omega ) } { S _ { m } ( \omega ) }$ ; and c is the speed of sound.

Defining $\phi _ { 0 }$ as the reference–monitor axis angle relative to the positive x-direction, see Fig. 2, we obtain $\phi _ { m } = \phi -$ ϕ . Furthermore, we assume that the monitor microphone is placed on the glasses frame above the ear, as in the Project Aria design [17], such that $\phi _ { m } \approx \phi _ { v }$ . Given this geometric framework, taking the derivative of the optimal AF in Eq. (5) with respect to the noise source DOA and collecting common terms yields:

$$
\begin{array}{r l} & {\frac {\partial H _ {0}}{\partial \phi} \approx j \frac {\omega}{c} \sin (\phi - \phi_ {0}) e ^ {- j \frac {\omega}{c} d _ {m} \cos (\phi - \phi_ {0})}} \\ & {\qquad \times \left[ d _ {m} - G (\omega) d _ {v} e ^ {- j \frac {\omega}{c} (d _ {v} - d _ {m}) \cos (\phi - \phi_ {0})} \right]} \end{array}\tag{6}
$$

Assuming that

$$
\frac {\omega}{c} \left| d _ {v} - d _ {m} \right| \ll 1,\tag{7}
$$

i.e., that the difference between the distances is small compared to the wavelength, we obtain

$$
\frac {\partial H _ {0}}{\partial \phi} \approx j \frac {\omega}{c} \sin (\phi - \phi_ {0}) e ^ {- j \frac {\omega}{c} d _ {m} \cos (\phi - \phi_ {0})} \Big [ d _ {m} - G (\omega) d _ {v} \Big ].\tag{8}
$$

Accordingly, the magnitude of the derivative can be approximated as

$$
\left| \frac {\partial H _ {0}}{\partial \phi} \right| \approx | F (\omega) | | \sin (\phi - \phi_ {0}) |,\tag{9}
$$

where

$$
| F (\omega) | = \frac {\omega}{c} \left| d _ {m} - G (\omega) d _ {v} \right|.\tag{10}
$$

Equation (9) clearly shows that the AF is more sensitive to changes in the primary source direction around $\phi = \phi _ { 0 } + 9 0 ^ { \circ }$ compared to $\phi = \phi _ { 0 }$

## IV. EXPERIMENTAL STUDY

This section presents a simulation study conducted under simplified acoustic conditions aiming to: (i) demonstrate the necessity of the virtual microphone technique for ANC in AR glasses, (ii) evaluate the performance degradation caused by AF–DOA mismatch while demonstrating the associated theoretical sensitivity analysis, and (iii) show the advantage of using a finite AF bank during online control as a practical alternative to per-DOA AF calibration.

## A. Simulation Setup

The microphone positions used in the simulations are taken from the Project Aria specifications [17]. For visualization purposes, all Aria microphones are shown in Fig. 3, although only a subset is used in the simulation, as denoted by the colored marks on the figure. A loudspeaker, serving as the secondary source, is assumed to be mounted on the frame, and a virtual microphone is positioned at the ear location.

A free-field environment is assumed, and both the primary and secondary sources are modeled as point sources. Simulations are performed at a sampling rate of 24 kHz, and no additional processing or hardware delay is included.

For each source azimuth $\phi$ in the x-y plane (fixed elevation), we simulate a 5 s realization where the noise source is positioned at a distance of $d _ { p } = 3$ m from the reference microphone (see Fig. 2). This distance allows the simulated point source to reasonably approximate the plane wave behavior assumed in the theoretical analysis. The primary disturbance is generated as Gaussian white noise, band-limited to 100–800 Hz using a 4th-order Butterworth filter, reflecting the low-frequency range where ANC is most effective.

## B. Methodology and Evaluation

Simulations are conducted using the normalized FxLMS (NFxLMS) [1] and AF-based ANC frameworks. Following the procedure in [12], the AF is calibrated using the LMS algorithm and the noise signal described in IV-A before being fixed for the control stage. All adaptive filters are finite impulse response filters with 256 coefficients and are initialized with a value of zero. This length provides a sufficient time window to model the relevant acoustic paths at the 24 kHz sampling rate. For simplicity, the secondary path estimate is assumed to be perfectly known. For each control filter adaptation, the reported attenuation corresponds to the best performance obtained over the step sizes $\mu \in \{ 1 0 ^ { - 4 } , 1 0 ^ { - 3 } , 1 0 ^ { - 2 } , 1 0 ^ { - 1 } \}$ The performance metric used throughout the simulations is the mean-squared attenuation in dB, computed from the disturbance and error signals of the virtual microphone over the last 15% of each 5 s realization to reflect steady-state convergence.

## C. Necessity of the Virtual Microphone

To investigate the necessity of the virtual microphone technique, we compare the attenuation at the virtual microphone achieved by three configurations: (i) monitor-based NFxLMS (where adaptation is driven by the monitor microphone signal), (ii) virtual-based NFxLMS (the ”ground truth” case with adaptation directly at the virtual microphone), and (iii) the AF method calibrated separately for each azimuth. Figure 4 displays the attenuation results as a polar plot, where the angular coordinate corresponds to the noise source DOA. This visualization format is utilized for all subsequent experiments. The disparity in performance between the monitor-based NFxLMS and the virtual NFxLMS highlights the necessity of implementing a virtual microphone technique. The AF method proved effective in bridging this gap, achieving attenuation levels that approach the performance of the virtual NFxLMS. Consequently, the AF method presents a promising potential solution for practical implementation.

![](figures/a74f442a0a1155df562f67435eb9f3103fe378541219de9f5222e986591d6147.jpg)  
Fig. 3: Geometric layout based on the Project Aria glasses geometry [17], including the loudspeaker and virtual microphone. Coordinates are provided in the legend in centimeters.

![](figures/e8eb8c92a9ba7a4789b01cd1157ed5bb49258a8d5acc4b7eb2738069e61930e3.jpg)  
Fig. 4: Polar plot of attenuation at the virtual microphone (at the ear) versus source azimuth. Comparison between NFxLMS control using the monitoring microphone, NFxLMS control using the virtual microphone, and AF control calibrated separately for each azimuth.

The attenuation exhibits approximate symmetry around $\phi ~ \approx ~ \phi _ { 0 } ~ \approx ~ 3 2 7 ^ { \circ }$ , corresponding to the direction of the reference–monitor axis $( \phi _ { 0 } )$ . At this azimuth, the relative propagation delay between the reference and the monitor/virtual microphones is maximal, resulting in favorable causality conditions for control. When the azimuth deviation exceeds approximately $\pm 9 0 ^ { \circ }$ , the noise reaches the monitor/virtual microphone before the reference, requiring a noncausal controller. In this region, all algorithms degrade significantly.

## D. AF sensitivity to DOA mismatch

We evaluate the performance degradation caused by AF mismatch between calibration and control, by applying an AF calibrated at a single DOA of the primary source, to other source DOAs. As shown in Fig. 5, the angular region around the calibration DOA in which the fixed AF achieves performance comparable to the fully calibrated AF is wider for the AF calibrated at $\phi _ { 0 }$ than for the one calibrated at $\phi _ { 0 } + 6 0 ^ { \circ }$ This indicates that the AF exhibits greater robustness to DOA mismatch in the angular region of the reference–monitor axis than at more distant azimuths.

![](figures/ffbb7f5660f48db6a40fe84d83a0a1645c080772a8d3e1e307fbc583b3f992a2.jpg)  
Fig. 5: Polar plot of attenuation at the virtual microphone (at the ear) versus source azimuth. Comparison between AF control calibrated separately for each ϕ and AF control using a single $\mathrm { A F }$ calibrated at ϕ<sub>0</sub> or $\phi _ { 0 } + 3 0 ^ { \circ }$ or $\phi _ { 0 } + 7 0 ^ { \circ }$

This behavior is consistent with the analysis presented in section III. In the analysis, the sensitivity term is proportional to $| \sin ( \phi - \phi _ { 0 } ) |$ |, which attains its minimum at $\phi = \phi _ { 0 }$ , (the reference–monitor axis). As the noise source azimuth deviates from this axis within the range $[ \phi _ { 0 } - 9 0 ^ { \circ } , \phi _ { 0 } + 9 0 ^ { \circ } ]$ , the sensitivity of the optimal AF increases, implying that such a DOA mismatch may induce a larger variation in the AF.

## E. Finite AF Bank

To provide a practical alternative to per-DOA AF calibration, we examine the performance obtained when selecting the AF from a finite bank based on the primary source direction. Given the significant performance degradation observed in the non-causal regions (where the azimuth deviation exceeds $\pm 9 0 ^ { \circ }$ relative to $\phi _ { 0 } )$ , the AF bank is constructed by calibrating AFs at uniformly spaced DOAs within $\left[ \phi _ { 0 } - 9 0 ^ { \circ } , \phi _ { 0 } + 9 0 ^ { \circ } \right]$ . For each azimuth, the AF is selected from the bank according to the calibration DOA closest to the noise source direction.

As observed in Fig. 6, selecting the AF from a finite bank significantly improves the performance compared to using a single fixed AF, while still not fully matching the performance achieved with per-azimuth calibration. To quantify how closely the finite bank performance approaches the fully calibrated case, Table I compares the achieved attenuation averaged over the azimuth range $\phi _ { 0 } \pm 9 0 ^ { \circ } \ : ( \mathrm { i . e . }$ ., where the controller operates under causal conditions), for different bank sizes.

![](figures/970d6a8ed392e7cdb48dde3b949021bb0e52537068bd6070a9a6cc894f01f249.jpg)  
Fig. 6: Polar plot of attenuation at the virtual microphone (at the ear) versus source azimuth. Performance obtained when the AF is selected from a finite AF bank of size 5, compared to fully calibrated AF control for each ϕ.

TABLE I: Attenuation in dB at the virtual microphone, averaged over primary source DOA at the causal azimuth range $\phi _ { 0 } \pm 9 0 ^ { \circ }$ for different AF bank sizes compared to fully calibrated AF control.

<table><tr><td>AF Bank Size</td><td>Mean Attenuation [dB]</td><td>Gap to Fully Calibrated [dB]</td></tr><tr><td>3</td><td>22.7</td><td>6.3</td></tr><tr><td>4</td><td>24.0</td><td>5.0</td></tr><tr><td>5</td><td>25.3</td><td>3.7</td></tr><tr><td>6</td><td>26.0</td><td>3.0</td></tr><tr><td>7</td><td>26.5</td><td>2.5</td></tr><tr><td>Fully calibrated</td><td>29.1</td><td>0</td></tr></table>

## V. CONCLUSIONS

This study validates the necessity of the virtual microphone technique for effective ANC in AR glasses. We further established a theoretical framework that characterizes the performance degradation caused by the mismatch between calibration and control due to a change in the noise arrival directions. To mitigate this sensitivity, we proposed an AF bank strategy; simulations demonstrate that using a bank of just 5 filters leads to only a small degradation in averaged performance, offering a robust practical alternative to full recalibration. While this work focused on a single-channel implementation with a single noise source in free-field conditions, future research is proposed to extend this evaluation to more realistic conditions including reverberation, multiple noise sources, and multichannel control strategies.

[1] S. Kuo and D. Morgan, “Active noise control: a tutorial review,” Proceedings of the IEEE, vol. 87, no. 6, pp. 943–973, Jun. 1999. [Online]. Available: https://ieeexplore.ieee.org/document/763310

[2] P. A. Nelson and S. J. Elliott, Active control of sound. Academic Press, Aug. 1991. [Online]. Available: https://eprints.soton.ac.uk/354428/

[3] L. Lu, K.-L. Yin, R. C. de Lamare, Z. Zheng, Y. Yu, X. Yang, and B. Chen, “A survey on active noise control in the past decade—Part I: Linear systems,” Signal Processing, vol. 183, p. 108039, Jun. 2021. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0165168421000785

[4] C.-Y. Chang, A. Siswanto, C.-Y. Ho, T.-K. Yeh, Y.-R. Chen, and S. M. Kuo, “Listening in a Noisy Environment: Integration of active noise control in audio products,” IEEE Consumer Electronics Magazine, vol. 5, no. 4, pp. 34–43, Oct. 2016. [Online]. Available: https://ieeexplore.ieee.org/document/7574427

[5] S. M. Kuo and D. Morgan, Active Noise Control Systems: Algorithms and DSP Implementations, 1st ed. USA: John Wiley & Sons, Inc., 1995.

[6] T. Xiao, B. Xu, and C. Zhao, “Spatially selective active noise control systems,” The Journal of the Acoustical Society of America, vol. 153, no. 5, p. 2733, May 2023. [Online]. Available: https://doi.org/10.1121/10.0019336

[7] T. Miyake, K. Iwai, and Y. Kajikawa, “Head-Mounted Multi-Channel Feedforward Active Noise Control System for Reducing Noise Arriving From Various Directions,” IEEE Access, vol. 11, pp. 6935–6943, 2023. [Online]. Available: https://ieeexplore.ieee.org/document/10019286/authorsfull-text-header

[8] N. Miyazaki and Y. Kajikawa, “Head-mounted active noise control system with virtual sensing technique,” Journal of Sound and Vibration, vol. 339, pp. 65–83, Mar. 2015. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0022460X14009201

[9] L. Liu, S. M. Kuo, and M. Zhou, “Virtual sensing techniques and their applications,” in 2009 International Conference on Networking, Sensing and Control, Mar. 2009, pp. 31–36. [Online]. Available: https://ieeexplore.ieee.org/document/4919241/referencesreferences

[10] M. Pawelczyk, “Adaptive noise control algorithms for active headrest system,” Control Engineering Practice, vol. 12, no. 9, pp. 1101–1112, Sep. 2004. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0967066103002569

[11] J. Zhang, S. J. Elliott, and J. Cheer, “Robust performance of virtual sensing methods for active noise control,” Mechanical Systems and Signal Processing, vol. 152, p. 107453, May 2021. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0888327020308396

[12] C. Shi, Z. Jia, R. Xie, and H. Li, “An active noise control casing using the multi-channel feedforward control system and the relative path based virtual sensing method,” Mechanical Systems and Signal Processing, vol. 144, p. 106878, Oct. 2020. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0888327020302648

[13] Y. Kajikawa and C. Shi, “Comparison of Virtual Sensing Techniques for Broadband Feedforward Active Noise Control,” in 2019 International Conference on Control, Automation and Information Sciences (ICCAIS), Oct. 2019, pp. 1–5, iSSN: 2475-7896. [Online]. Available: https://ieeexplore.ieee.org/document/9074640

[14] C. Shi, R. Xie, N. Jiang, H. Li, and Y. Kajikawa, “Selective Virtual Sensing Technique for Multi-channel Feedforward Active Noise Control Systems,” IEEE International Conference on Acoustics, Speech, and Signal Processing, pp. 8489–8493, May 2019.

[15] R. Xie, A. Tu, C. Shi, S. Elliott, H. Li, and L. Zhang, “Cognitive Virtual Sensing Technique for Feedforward Active Noise Control,” in ICASSP 2024 - 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Apr. 2024, pp. 981–985, iSSN: 2379-190X. [Online]. Available: https://ieeexplore.ieee.org/document/10446463

[16] B. Wang, D. Shi, Z. Luo, X. Shen, J. Ji, and W.-S. Gan, “Transferable Selective Virtual Sensing Active Noise Control Technique Based on Metric Learning,” in ICASSP 2025 - 2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Apr. 2025, pp. 1–5, iSSN: 2379-190X. [Online]. Available: https://ieeexplore.ieee.org/document/10887958

[17] CHiME-8 MMCSG Task 3: Microphone Geometry for Aria Glasses. [Online]. Available: https://www.chimechallenge.org/challenges/chime8/task3/data