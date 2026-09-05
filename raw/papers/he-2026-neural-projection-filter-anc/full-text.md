

<!-- PAGE 1 -->

IEEE SIGNAL PROCESSING LETTERS
1

Neural Projection Filter Generation for

Multi-Reference Active Noise Control

Yiming He, Kai Chen, Member, IEEE, Haishan Zou, Jiancheng Tao, and Xiaojun Qiu

Abstract—High-dimensional and correlated reference signals
make multi-reference active noise control (ANC) computationally
demanding, prone to slow convergence, and difficult to deploy
in real-time applications. This letter introduces condition-aware
projection filtering (CAPF), implemented by CAPFNet, which
generates causal block-wise linear FIR projection filters for
reference signal compression. The generated filters reduce 42
reference channels to 4 projected references while preserving
the information required for effective ANC and maintaining
compatibility with conventional adaptive algorithms. Simulations
with measured in-vehicle road-noise recordings show that CAPF-
Newton improves the average attenuation over FDFxNLMS by
2.6 dBA and achieves performance comparable to the neural
reference projection-based filtered-x affine projection algorithm
(NRP-FxAP), with a 48× reduction in online computational
complexity.

Index Terms—Active noise control, adaptive filtering, multi-
reference active noise control, projection filter generation, deep
learning.

I. INTRODUCTION
A

CTIVE noise control (ANC) is effective for suppressing
low-frequency noise in practical applications [1], [2], [3].
Automotive feedforward ANC systems typically use multi-
ple reference sensors to capture road-noise-related structural
vibrations [4], [5]. More reference channels can improve
attainable attenuation [6], but at the cost of increased inter-
channel correlation, higher computational complexity, and
slower adaptive convergence [7], [8].

Existing remedies include filtered-x least mean squares
(FxLMS)-based algorithms [9], [10], [11], filtered-x affine
projection (FxAP) algorithms [12], [13], Newton-type meth-
ods [14], reference preconditioning methods based on decorre-
lation or subspace transformation [15], [16], [17], and online
frequency-domain schemes [18], [19]. While such precondi-
tioning methods can improve adaptation by mitigating inter-
channel correlation, their reliance on fixed linear transforma-
tions may limit their ability to capture complex correlation
structures in high-dimensional multichannel scenarios, espe-
cially under time-varying operating conditions.

Deep learning has been introduced to ANC for model-
ing complex acoustic relationships [20], [21], [22]. Existing
neural ANC methods mainly generate control signals [23],
[24], [25], [26] or control filters [27], [28]. While these

This work was supported by the National Natural Science Foundation of
China under Grant 11874218.

Yiming He, Kai Chen, Haishan Zou, Jiancheng Tao, and Xiaojun
Qiu
are
with
the
Key
Laboratory
of
Modern
Acoustics,
Institute
of
Acoustics,
Nanjing
University,
Nanjing
210093,
China
(emails:
ymhe@smail.nju.edu.cn,
chenkai@nju.edu.cn,
hszou@nju.edu.cn,
jctao@nju.edu.cn, xjqiu@nju.edu.cn).

approaches improve nonlinear modeling capability, they do
not explicitly address the strong inter-channel correlation
and high-dimensional redundancy in multi-reference ANC
systems. The neural reference projection-based FxAP (NRP-
FxAP) method [29] performs neural reference projection by
directly generating projected reference signals from multichan-
nel inputs. By enabling dimensionality reduction and implicit
whitening while retaining adaptive control, NRP-FxAP has
demonstrated strong noise-reduction and convergence perfor-
mance in multi-reference ANC. Nevertheless, its point-wise
neural projection incurs high online complexity compared with
conventional adaptive controllers.

This letter proposes condition-aware projection filtering
(CAPF) for multi-reference ANC. CAPFNet generates block-
wise projection filters that convert high-dimensional correlated
references into compact projected references for conventional
ANC algorithms. Compared with NRP-FxAP, which directly
generates projected references sample by sample, CAPF gen-
erates block-wise causal FIR projection filters and obtains
the projected references through linear filtering, substantially
reducing the neural inference rate and online complexity.

II. PROPOSED METHOD

This section presents the CAPF-based ANC framework in
Fig. 1, where CAPFNet generates block-wise projection filters,
while causal reference projection and control filtering are
performed sample-wise using the latest filter coefficients to
avoid block-processing latency.

A. CAPF-Based ANC Framework

Let x(n) ∈RP be the multichannel reference signal, where
n is the time-domain sample index and P is the number of
reference channels. The projection stage maps x(n) to a lower-
dimensional projected reference signal v(n) ∈RQ, where
Q < P. The tapped reference vector is

˜x(n) =



xT(n), xT(n −1), · · · , xT(n −Lp + 1)

T ,
(1)

where Lp is the projection filter length. For n ∈Bk, where Bk
denotes the sample block processed by the kth projection-filter
update, CAPFNet generates Wproj(k) ∈RQ×P Lp, and

v(n) = Wproj(k)˜x(n).
(2)

The projected reference signals are fed into a conventional
ANC controller:

y(n) = Wctrl(n)˜v(n),
(3)

This article has been accepted for publication in IEEE Signal Processing Letters. This is the author's version which has not been fully edited and

content may change prior to final publication. Citation information: DOI 10.1109/LSP.2026.3728398

© 2026 IEEE. All rights reserved, including rights for text and data mining and training of artificial intelligence and similar technologies. Personal use is permitted,

but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information.

Authorized licensed use limited to: Jaypee Insituite of Information Technology-Noida Sec 128 (L3). Downloaded on September 05,2026 at 05:56:36 UTC from IEEE Xplore.  Restrictions apply.

<!-- PAGE 2 -->

IEEE SIGNAL PROCESSING LETTERS
2

Fig. 1: Overview of the proposed CAPF-based ANC framework.

![[raw/papers/he-2026-neural-projection-filter-anc/figures/fig1.png|Figure 1]]

where ˜v(n) ∈RQLc, Lc is the back-end control filter length,
Wctrl(n) ∈RC×QLc, and C is the number of secondary
loudspeakers. The residual error is

e(n) = d(n) + S˜y(n),
(4)

where ˜y(n)
∈
RCLs, Ls is the secondary-path length,
d(n) ∈RM is the primary noise at the error microphones,
M is the number of error microphones, and S ∈RM×CLs is
the secondary-path convolution matrix. Thus, CAPF reduces
the back-end input dimension from P to Q and improves
conditioning through decorrelation-oriented training.

B. Architecture of CAPFNet

CAPFNet first extracts time–frequency features from the
real and imaginary components of the complex STFT coef-
ficients,

U(ℓ, f) = [gcv (STFT{x})] (ℓ, f),
(5)

where gcv(·) is a depthwise separable convolution-based en-
coder, ℓis the short-time Fourier transform (STFT) frame
index, and f is the frequency-bin index. For brevity, U(ℓ)
denotes the feature representation at the ℓth STFT frame over
all frequency bins. Encoder and condition features, where the
latter represents the vehicle operating condition characterized
by driving speed, road surface, and environment, are obtained
as

zenc(ℓ) = genc(U(ℓ)),
hcond(ℓ) = gcond(U(ℓ)).
(6)

At the kth projection-filter update, the N-frame aggregates
over the preceding frames are

¯zenc(k) = 1

N

kN−1
X

ℓ=(k−1)N

zenc(ℓ),
(7)

zcond(k) = softmax



1

N

kN−1
X

ℓ=(k−1)N

hcond(ℓ)



,
(8)

the projection filter for block k is generated using only
previously observed frames and is applied to the kth sample
block.

The fused representation is obtained as

zf(k) = [¯zenc(k); ϕcond(zcond(k))] ,
(9)

where ϕcond(·) is a two-layer fully connected mapping. The
projection filter is decomposed as

Wproj(k) = Wbase + Wexp(k) + Wres(k),
(10)

where Wbase is a global learnable component capturing the
common projection structure, Wexp(k) models condition-
dependent variations, and Wres(k) provides block-wise resid-
ual correction.

The expert component is

Wexp(k) =

J
X

j=1

zcond,j(k)Wj,
(11)

where J is the number of expert filters, and each expert filter
is represented in a low-rank form as

Wj = ¯Ae

j(IP ⊗Be),
(12)

with
¯Ae

j
∈RQ×P Ke, Be
∈RKe×Lp, and Ke
= 24;
IP denotes the P-dimensional identity matrix and ⊗the
Kronecker product. Similarly,

Wres(k) = ¯Ar(k)(IP ⊗Br),
(13)

where ¯Ar(k) ∈RQ×P Kr, Br ∈RKr×Lp, and Kr = 12.
The expert factors are global parameters jointly optimized
with CAPFNet, with ¯Ae

j zero-initialized and Be Gaussian-
initialized. In the residual branch, Br is also Gaussian-
initialized and jointly optimized, while ¯Ar(k) is generated
block-wise from zf(k) by the trainable mapping ψ, which
consists of two linear layers with an ELU activation.

C. Training Objective

The training objective contains an error loss, a decorrelation
regularization term, and a condition classification loss. The
error loss is

Lerr = 10 log10(∥fA(ew)∥2

2/∥fA(d)∥2
2),
(14)

This article has been accepted for publication in IEEE Signal Processing Letters. This is the author's version which has not been fully edited and

content may change prior to final publication. Citation information: DOI 10.1109/LSP.2026.3728398

© 2026 IEEE. All rights reserved, including rights for text and data mining and training of artificial intelligence and similar technologies. Personal use is permitted,

but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information.

Authorized licensed use limited to: Jaypee Insituite of Information Technology-Noida Sec 128 (L3). Downloaded on September 05,2026 at 05:56:36 UTC from IEEE Xplore.  Restrictions apply.

<!-- PAGE 3 -->

IEEE SIGNAL PROCESSING LETTERS
3

where ∥· ∥2 denotes the Euclidean norm, and fA(·) denotes
the A-weighting filter [30]. For each training segment, an
offline least-squares Wiener controller Ww ∈RC×QLc is
computed from the generated projected reference signals, the
identified secondary paths, and the primary-noise sequence.
The corresponding control signal is yw(n) = Ww˜v(n), and
the Wiener residual is ew(n) = d(n)+S˜yw(n), where ˜yw(n)
is the tapped vector of yw(n).

The decorrelation regularization is

Lreg = ∥R/ρ −I∥2

F ,
(15)

where ∥· ∥F denotes the Frobenius norm, R ∈RQCLc×QCLc
is the autocorrelation matrix of the secondary-path-filtered
projected reference signals, I ∈RQCLc×QCLc is the identity
matrix, and ρ = tr(R)/(QCLc) is the average signal power.

The condition classification loss is

Lcls = −mean

k

J
X

j=1

pj(k) log zcond,j(k),
(16)

where the mean is taken over all blocks in each training
segment. Here, pj(k) is the jth entry of the one-hot ground-
truth label determined from the known operating condition of
each training block.

The overall training objective is

Ltrain = Lerr + αLreg + βLcls,
(17)

where α and β are weighting coefficients.

III. EXPERIMENTS

A. Experimental Setup

The simulations were conducted using a measured in-
vehicle road-noise dataset with a total duration of 21 h. The
system contains 42 reference channels, 2 secondary sound
sources, and 2 error microphones. The error microphones,
denoted as M1 and M2, are placed near the passenger. The
secondary paths are identified offline and modeled by 512-tap
finite impulse response (FIR) filters. The recordings cover 7
predefined operating conditions formed by combinations of
driving speed, road surface, and driving environment, with
driving speeds of 50, 80, and 100 km/h. Accordingly, seven
expert filters are adopted to represent different operating
conditions. The data are resampled to 4 kHz and split into
10-s clips, with 19.5 h for training and 1.5 h for testing.
The STFT frame length is 512 samples with 50% overlap.
Unless otherwise specified, the projection filter is updated
every N = 8 frames, with Lp = 256 and Q = 4. CAPFNet
has 500.0k parameters, with computational complexities of
83.0 MMAC/s for filter generation and 172.0 MMAC/s for
projection filtering. On an Intel Core i7-10875H CPU, CAPF
requires 132.2 µs per sample for the delayless filtering path
and 18.2 ms per asynchronous projection-filter update, with
an estimated DSP memory requirement of 2.65 MiB and a
conservative upper bound of 9.51 MiB.

The model is trained with Adam for 30 epochs on two
NVIDIA RTX 4070 GPUs using a batch size of 16. The initial
learning rate is set to 4×10−3 and is decayed by a factor of 0.2
every 10 epochs. The loss weighting coefficients are α = 0.1

TABLE I: Performance (noise reduction level in dBA).

Method
Mic.
50 km/h
80 km/h
100 km/h
Complexity
(dBA)
(dBA)
(dBA)
(MAC/s)

Wiener
M1
-9.64 (1.06)
-7.36 (0.75)
-7.92 (0.85)
—
M2
-10.60 (1.09)
-7.70 (0.78)
-7.94 (0.89)

FDFxNLMS
M1
-5.91 (1.37)
-5.48 (0.99)
-5.66 (0.86)
199.0M
M2
-6.52 (1.32)
-5.93 (1.03)
-5.75 (0.85)

BCD-Newton
M1
-8.38 (1.70)
-6.38 (1.22)
-6.43 (1.16)
440.2M
M2
-9.35 (1.87)
-6.85 (1.29)
-6.60 (1.19)

iSVD-VR
M1
-6.41 (1.18)
-4.80 (1.01)
-4.74 (1.00)
699.0M
M2
-6.91 (1.21)
-5.21 (1.02)
-5.07 (0.96)

NRP-FxAP
M1
-10.69 (1.71)
-7.73 (1.14)
-7.91 (1.04)
17.9G
M2
-10.86 (1.70)
-7.53 (1.09)
-7.50 (1.04)

CAPF-FDFxNLMS
M1
-9.27 (1.78)
-7.19 (1.37)
-7.37 (1.23)
265.8M
M2
-9.90 (1.73)
-7.30 (1.28)
-7.17 (1.12)

CAPF-Newton
M1
-10.24 (1.72)
-7.46 (1.17)
-7.78 (1.19)
374.0M
M2
-10.63 (1.71)
-7.50 (1.24)
-7.52 (1.10)

and β = 0.2. The step sizes of the conventional adaptive ANC
algorithms are individually tuned for stable convergence and
strong steady-state NR.

B. ANC Performance Evaluation

The proposed CAPF front end is paired with frequency-
domain
filtered-x
normalized
least
mean
squares
(FD-
FxNLMS) [31] and the least mean squares (LMS)-Newton al-
gorithm [14], yielding CAPF-FDFxNLMS and CAPF-Newton,
respectively. The baselines include conventional FDFxNLMS,
block coordinate descent (BCD)-Newton [32], the incremental
singular value decomposition-based virtual reference method
(iSVD-VR) [17], an offline Wiener reference, and NRP-
FxAP [29], which serves as a neural reference-projection
baseline.

For conventional ANC algorithms, the control filter length
is set to 512. CAPF-based systems use a reduced back-end
adaptive filter length of 256 after projection. BCD-Newton
uses 5 inner iterations with an update interval of 30 × 512
samples, whereas CAPF-Newton updates the adaptive filter
every 2048 samples. For iSVD-VR, following the original
methodology, the number of virtual reference channels is
determined via principal component analysis (PCA) by re-
taining 95% cumulative contribution, resulting in 28 virtual
references; the transfer matrix is updated every 4000 samples.
For NRP-FxAP, the projection dimension is set to 4 to match
CAPF-based systems, and the control filter length is set to
512.
The test set consists of approximately 5-min recordings,
with noise reduction (NR) computed over each complete
recording and averaged within each speed condition; standard
deviations are evaluated over non-overlapping 10-s segments.
Table I reports the A-weighted NR, defined as the residual-
to-primary level difference, where more negative values in-
dicate stronger attenuation. Across the six speed–microphone
cases, CAPF-Newton achieves 8.52 dBA average attenuation,
comparable to the Wiener reference and NRP-FxAP, while
requiring only 374.0 MMAC/s compared with 17.9 GMAC/s
for NRP-FxAP. It also outperforms BCD-Newton by 1.19 dBA
with 15.0% lower complexity.

The scenario consists of 50 km/h for 0–30 s, acceleration
from 50 to 60 km/h for 30–60 s, and 80 km/h after 60 s.

This article has been accepted for publication in IEEE Signal Processing Letters. This is the author's version which has not been fully edited and

content may change prior to final publication. Citation information: DOI 10.1109/LSP.2026.3728398

© 2026 IEEE. All rights reserved, including rights for text and data mining and training of artificial intelligence and similar technologies. Personal use is permitted,

but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information.

Authorized licensed use limited to: Jaypee Insituite of Information Technology-Noida Sec 128 (L3). Downloaded on September 05,2026 at 05:56:36 UTC from IEEE Xplore.  Restrictions apply.

<!-- PAGE 4 -->

IEEE SIGNAL PROCESSING LETTERS
4

Fig. 2: Noise reduction results. (a) Convergence curves over the 50→60→80 km/h driving scenario, (b) spectra for the 50 km/h steady segment (20–30 s), (c)

![[raw/papers/he-2026-neural-projection-filter-anc/figures/fig2.png|Figure 2]]

spectra for the 80 km/h steady segment (80–90 s).

TABLE II: Parameter analysis and component ablation of
CAPF-Newton.

Variant
Mic.
50 km/h
80 km/h
100 km/h
Complexity
(dBA)
(dBA)
(dBA)
(MAC/s)
Baseline

Default†
M1
-10.24
-7.46
-7.78
374.0M
M2
-10.63
-7.50
-7.52
Parameter changes

Q = 6
M1
-10.33
-7.55
-7.79
701.8M
M2
-10.73
-7.59
-7.54

Lp = 128
M1
-9.55
-7.10
-7.21
418.0M
M2
-9.93
-7.12
-6.97

Lp = 384
M1
-9.99
-7.38
-7.78
382.1M
M2
-10.53
-7.52
-7.58
Component ablation

w/o Wbase
M1
-10.06
-7.32
-7.60
374.0M
M2
-10.48
-7.39
-7.37

w/o Wexp
M1
-9.80
-7.24
-7.47
366.1M
M2
-10.20
-7.34
-7.37

w/o both
M1
-9.34
-6.80
-6.98
366.1M
M2
-9.79
-6.89
-6.75
† Default denotes the full CAPFNet with Q = 4 and Lp = 256, used as
the common baseline.

Since the training data only include 50, 80, and 100 km/h
conditions, the intermediate 60 km/h segment represents an
unseen operating condition, allowing evaluation of the model’s
generalization capability across driving speeds. CAPF-Newton
reaches stable attenuation within about 20 s, adapts after the
speed transition, and approaches the offline Wiener reference
in steady-state spectra.

C. Discussion

Table II summarizes the parameter and component analyses
of CAPF-Newton. The default setting corresponds to the full
CAPFNet with Q = 4 and Lp = 256.

1) Effect of Projection Dimension: Increasing Q from
4 to 6 improves the average attenuation magnitude by

only 0.07 dBA, while increasing complexity from 374.0 to
701.8 MMAC/s. This indicates that Q = 4 already captures
the dominant reference information for the tested driving
conditions.

2) Effect of Projection Filter Length: With the effective
reference-to-control memory fixed at 512 samples, increasing
Lp from 128 to the default value of 256 improves the average
attenuation magnitude by 0.54 dBA. Further increasing Lp to
384 slightly degrades performance by 0.06 dBA. The non-
monotonic complexity mainly results from the corresponding
change in the back-end adaptive filter length; thus, Lp = 256
provides the best overall balance.

3) Component Ablation: Removing Wbase, Wexp, or both
reduces the average attenuation magnitude by 0.15, 0.29, and
0.76 dBA, respectively. This suggests that both components
contribute to performance, consistent with the intended roles of
the shared base in modeling condition-independent projection
patterns and the expert branch in enabling condition-dependent
adaptation.

IV. CONCLUSION

This letter proposed CAPF, a neural projection-filter front
end for multi-reference active noise control. Measurement-
based simulations show that CAPF-Newton improves the aver-
age attenuation over FDFxNLMS by 2.6 dBA while achieving
performance comparable to NRP-FxAP with a 48× reduction
in online computational complexity. These results demonstrate
that filter-level projection generation is an effective low-
complexity front end for conventional ANC algorithms. Future
work will focus on a more rigorous analytical characterization
of CAPF, real-time experimental validation, and robustness
evaluation under a broader range of vehicle operating and
acoustic conditions.

This article has been accepted for publication in IEEE Signal Processing Letters. This is the author's version which has not been fully edited and

content may change prior to final publication. Citation information: DOI 10.1109/LSP.2026.3728398

© 2026 IEEE. All rights reserved, including rights for text and data mining and training of artificial intelligence and similar technologies. Personal use is permitted,

but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information.

Authorized licensed use limited to: Jaypee Insituite of Information Technology-Noida Sec 128 (L3). Downloaded on September 05,2026 at 05:56:36 UTC from IEEE Xplore.  Restrictions apply.

<!-- PAGE 5 -->

IEEE SIGNAL PROCESSING LETTERS
5

REFERENCES

[1] S. J. Elliott and P. A. Nelson, “The active control of sound,” Electronics

& Communication Engineering Journal, vol. 2, no. 4, pp. 127–136,
1990.
[2] S. M. Kuo and D. R. Morgan, “Active noise control: a tutorial review,”

Proceedings of the IEEE, vol. 87, no. 6, pp. 943–973, 1999.
[3] C. Hansen and S. Snyder, Active control of noise and vibration.
CRC
Press, 1996.
[4] J. Cheer and S. J. Elliott, “Multichannel control systems for the

attenuation of interior road noise in vehicles,” Mechanical Systems and
Signal Processing, vol. 60, pp. 753–769, 2015.
[5] N. Zafeiropoulos, A. Moorhouse, A. Mackay, and M. Ballatore, “Active

control of road noise: the relation between the reference sensor locations
and the effect on the controller’s performance,” in ICSV22: The 22nd
International Congress of Sound and Vibration, 2015.
[6] L. Sujbert, “Multiple reference active noise control–the attainable sup-

pression,” Applied Acoustics, vol. 217, p. 109846, 2024.
[7] S. J. Elliott, Signal processing for active control.
Elsevier, 2000.
[8] B. Farhang-Boroujeny, Adaptive filters: theory and applications.
John
Wiley & Sons, 2013.
[9] S. J. Elliott, I. M. Stothers, and P. A. Nelson, “A multiple error

LMS algorithm and its application to the active control of sound
and vibration,” IEEE Transactions on Acoustics, Speech, and Signal
Processing, vol. 35, no. 10, pp. 1423–1434, 1987.
[10] F. Yang, Y. Cao, M. Wu, F. Albu, and J. Yang, “Frequency-domain

filtered-x LMS algorithms for active noise control: A review and new
insights,” Applied Sciences, vol. 8, no. 11, p. 2313, 2018.
[11] T. Li, S. Lian, S. Zhao, J. Lu, and I. S. Burnett, “Distributed active noise

control based on an augmented diffusion FxLMS algorithm,” IEEE/ACM
Transactions on Audio, Speech, and Language Processing, vol. 31, pp.
1449–1463, 2023.
[12] M. Bouchard, “Multichannel affine and fast affine projection algorithms

for active noise control and acoustic equalization systems,” IEEE Trans-
actions on Speech and Audio Processing, vol. 11, no. 1, pp. 54–60, 2003.
[13] M. Ferrer, M. de Diego, and A. Gonzalez, “Filtered-x quasi affine

projection algorithm for active noise control networks,” IEEE/ACM
Transactions on Audio, Speech, and Language Processing, vol. 32, pp.
4237–4252, 2024.
[14] L. Zhu, X. Qiu, D. Mao, S. Wu, and X. Zhong, “Efficient segment-

update block LMS-Newton algorithm for active control of road noise,”
Mechanical Systems and Signal Processing, vol. 198, p. 110436, 2023.
[15] M. R. Bai and S. J. Elliott, “Preconditioning multichannel adaptive

filtering algorithms using EVD- and SVD-based signal prewhitening and
system decoupling,” Journal of Sound and Vibration, vol. 270, no. 4,
pp. 639–655, 2004. [Online]. Available: https://www.sciencedirect.com/
science/article/pii/S0022460X03001500
[16] Y. Wang, Y. Zhuang, and Y. Liu, “Causal preconditioning filters

design for real-time multichannel active noise control,” Applied
Acoustics, vol. 240, p. 110950, 2025. [Online]. Available: https:
//www.sciencedirect.com/science/article/pii/S0003682X25004220
[17] Z.
Xia,
Y.
He,
Z.
Zhang,
H.
Chen,
and
X.
Fu,
“A
multi-
channel active road noise control system using incremental SVD
based virtual references and local-clustered control strategy,” Applied
Acoustics, vol. 245, p. 111216, 2026. [Online]. Available: https:
//www.sciencedirect.com/science/article/pii/S0003682X25006887
[18] S. Lian, T. Li, J. Gu, Y. Hu, C. Zhu, S. Wang, and J. Lu, “An online

decoupling-whitening frequency domain filtered-error least mean square
algorithm for active road noise control,” The Journal of the Acoustical
Society of America, vol. 156, no. 2, pp. 1413–1424, 2024.
[19] S. Lian, J. Gu, S. Wang, K. Chen, Y. Hu, C. Zhu, and J. Lu, “A

coherence-based robust frequency-dependent variable step size method
for active road noise control,” The Journal of the Acoustical Society of
America, vol. 158, no. 2, pp. 1254–1267, 2025.
[20] H. Zhang and D. Wang, “Deep ANC: A deep learning approach to active

noise control,” Neural Networks, vol. 141, pp. 1–10, 2021.
[21] H. Zhang and D. Wang, “Deep MCANC: A deep learning approach

to multi-channel active noise control,” Neural Networks, vol. 158, pp.
318–327, 2023.
[22] Y.-J. Cha, A. Mostafavi, and S. S. Benipal, “DNoiseNet: Deep learning-

based feedback active noise control in various noisy environments,”
Engineering Applications of Artificial Intelligence, vol. 121, p. 105971,
2023.
[23] A. Mostafavi and Y.-J. Cha, “Deep learning-based active noise control

on construction sites,” Automation in Construction, vol. 151, p. 104885,
2023.

[24] L.
Bai,
S.
Lian,
M.
Li,
Y.
He,
L.
Rao,
X.
Zeng,
R.
Sun,
K. Chen, and J. Lu, “WaveNet-Volterra neural network for active
noise control: A fully causal approach,” Mechanical Systems and
Signal Processing, vol. 241, p. 113486, 2025. [Online]. Available:
https://www.sciencedirect.com/science/article/pii/S0888327025011872
[25] L. Bai, J. Xue, S. Lian, Y. He, Y. Liang, L. Rao, S. Wang, and J. Lu, “An

adaptive deep neural network for active road noise control,” The Journal
of the Acoustical Society of America, vol. 159, no. 4, pp. 3674–3685,
2026.
[26] T. Ge, L. An, N. Han, and T. Zhang, “U-shaped WaveNet with

adaptive Volterra neural networks for active noise control,” IEEE Signal
Processing Letters, vol. 33, pp. 3029–3033, 2026.
[27] Z. Luo, D. Shi, and W.-S. Gan, “A hybrid SFANC-FxNLMS algorithm

for active noise control based on deep learning,” IEEE Signal Processing
Letters, vol. 29, pp. 1102–1106, 2022.
[28] Z. Luo, J. Ji, B. Wang, D. Shi, H. Ma, and W.-S. Gan, “Deep learning-

based generative fixed-filter active noise control: Transferability and
implementation,” Mechanical Systems and Signal Processing, vol. 238,
p. 113207, 2025.
[29] Y. He, L. Bai, L. Rao, K. Chen, J. Tao, and X. Qiu, “A neural

reference projection-based method for multi-reference active noise
control (L),” The Journal of the Acoustical Society of America,
vol. 159, no. 5, pp. 4482–4486, 05 2026. [Online]. Available:
https://doi.org/10.1121/10.0043891
[30] M. E. Nilsson, “A-weighted sound pressure level as an indicator of short-

term loudness or annoyance of road-traffic sound,” Journal of Sound
and Vibration, vol. 302, no. 1, pp. 197–207, 2007. [Online]. Available:
https://www.sciencedirect.com/science/article/pii/S0022460X06008522
[31] S. Zhang, Y. S. Wang, H. Guo, C. Yang, X. L. Wang, and N. N. Liu,

“A normalized frequency-domain block filtered-x LMS algorithm for
active vehicle interior noise control,” Mechanical Systems and Signal
Processing, vol. 120, pp. 150–165, 2019.
[32] Y. He, W. Chen, K. Chen, J. Tao, and X. Qiu, “A modified least mean

square Newton algorithm based on block coordinate descent for multi-
reference active noise control,” The Journal of the Acoustical Society of
America, vol. 158, no. 3, pp. 2377–2388, 2025.

This article has been accepted for publication in IEEE Signal Processing Letters. This is the author's version which has not been fully edited and

content may change prior to final publication. Citation information: DOI 10.1109/LSP.2026.3728398

© 2026 IEEE. All rights reserved, including rights for text and data mining and training of artificial intelligence and similar technologies. Personal use is permitted,

but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information.

Authorized licensed use limited to: Jaypee Insituite of Information Technology-Noida Sec 128 (L3). Downloaded on September 05,2026 at 05:56:36 UTC from IEEE Xplore.  Restrictions apply.

