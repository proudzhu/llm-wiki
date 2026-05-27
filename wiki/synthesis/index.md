# Synthesis

> Cross-source analysis, comparisons, and insights that combine multiple sources.

| Page | Summary | Sources |
|------|---------|---------|
| [[synthesis/impulsive-noise-control\|Robust ANC for Impulsive Noise]] | FxLMS/F, clipped FxRLS, correntropy→MCC→GMCC, MVC, VSS, AI-driven robustness: 5 approaches + design tree | Chen 2016, Zhu 2020, Liu 2024, Huang 2017, Tian 2026 |
| [[synthesis/feedback-anc-filter-design\|Feedback ANC: Design, Stability, Adaptation]] | Fixed MVC → IMC+FxLMS → H∞ → Constrained LMS → FLNN + AFC comparison + step-size hierarchy + neural gain | Pawelczyk 1997, Vaudrey 2003, Hilgemann 2024, Zhang 2024 |
| [[synthesis/multimodal-bc-speech-enhancement\|Multimodal BC Speech Enhancement]] | Evolution of BC integration from pitch extraction to generative diffusion models and Conformer-based ASR fusion | Zhang 2022, Wang 2022, Khanagha 2026, Heitkaemper 2026 |
| [[synthesis/multichannel-anc-efficiency-and-robustness\|Multichannel ANC: Efficiency and Robustness]] | Strategies for managing O(M·L·N) complexity via decomposition, distributed nodes, and meta-learning | Kronic, GLPRCTIK, S2TMLSUP, HTIMHJJW |
| [[synthesis/personal-sound-zones-evolution-and-optimization\|Personal Sound Zones: Evolution and Optimization]] | Tracks PSZ evolution from classical optimization to modern robust control and neural rendering | 2026-04-19 |
| [[synthesis/anc-architecture-evolution\|ANC Architecture Evolution]] | FF → FB → Hybrid: how reference signal availability drives ANC design, from Kuo 1999 to Benois 2020 | Kuo 1999, Pawelczyk 1997, Wu 2014, Benois 2020 |
| [[synthesis/virtual-sensing-evolution\|Virtual Sensing Evolution]] | Development of remote quiet zones: from fixed RMT training to neural Obs-TasNet filters and DTW-based secondary path interpolation | LJDPCZ9G, WY4S7C6Z, WX2XSXDA, YHFLXFQH, ZV3BCM38 |
| [[synthesis/modern-headphone-anc-systems\|Modern Headphone ANC Systems]] | Multi-modal headphone platforms: hybrid ANC + bone conduction + VAD + transparency + open-ear dual compensation | Benois 2020, Fukumoto 2025, Masilamani 2024, Toyooka 2026 |
| [[synthesis/mpc-vs-fxlms-for-anc\|MPC vs Traditional ANC]] | QP solver vs closed-form: two MPC approaches compared with FxLMS on constraint handling, latency, cost | Wills 2008, Liang 2026 |
| [[synthesis/adaptive-algorithm-tradeoffs\|Adaptive Algorithm Trade-offs]] | Decision matrix across 6 algorithms: FxLMS, Leaky, Simplified, GMCC, MPC, VSS on performance/robustness/cost | 10+ papers |
| [[synthesis/application-specific-anc\|Application-Specific ANC]] | Drone, smart glasses, vehicle, selective attenuation — form factor drives architecture, not algorithm | Steiner 2026, Yuan 2026, Yang 2026, Huang 2026 |
| [[synthesis/ai-driven-anc\|AI-Driven ANC]] | Shift from classical FxLMS to neural-hybrid architectures and generative noise selection | MKAWB86B, XS7Z5XTN, UCJR5KDZ, Z7FUV6LL |
| [[synthesis/computational-efficiency-evolution\|Computational Efficiency Evolution]] | Fast RLS → FxLMS reductions → GPU DSP → nonlinear filters: 40 years of the shifting bottleneck | Cioffi 1984, Li & Chen 2023, Spanio 2025, Zhao & Chen 2023 |
| [[synthesis/computational-efficiency-evolution\|Computational Efficiency Evolution]] | ANC 计算复杂度演进 + RNN 内存瓶颈 (BPTT vs FEP) + 2026 效率前沿 | Zucchet 2026, Liang 2026, Kuo 1999 |
| [[synthesis/impulsive-noise-control\|Impulsive Noise Control]] | Beyond Gaussian: FxLMS/F, FxRLS clipping, MVC vs GMCC, Versoria VSS — 4 robust cost functions | Liu 2024, Zeb 2017, Huang 2017, Tian 2026 |
| [[synthesis/nonlinear-anc-approaches\|Nonlinear ANC Approaches]] | FLNN, Volterra, Kernel, Spline, Convex Combination — when linear filters aren't enough | Zhao & Zeng 2010, Zhao & Chen 2023, Song & Zhao 2019 |
| [[synthesis/feedback-anc-filter-design\|Feedback ANC Filter Design]] | MVC, IMC+FxLMS, H∞ robust, constrained LMS, reduced FLNN — stability/robustness/performance triangle | Pawelczyk 1997, Vaudrey 2003, Arablouei 2015, Morari 2002, Zhao & Zeng 2010 |
| [[synthesis/iir-filter-fitting-frequency-response\|IIR 滤波器拟合频响曲线]] | 向量拟合、最小二乘、输出误差、Hankel-SVD — 从频响测量到状态空间模型 | Liang 2026, Cioffi 1984, Lesniewski, Vaudrey 2003 |
| [[synthesis/kalman-filter-theory-and-application\|Kalman Filter Theory and Application]] | Comprehensive overview of KF, MCC-KF, and applications in MPC and audio tracking | Welch & Bishop 2006, Chen & Liu 2017, Wills 2008, Liang 2026 |
| [[synthesis/llm-wiki-best-practices|LLM Wiki Best Practices]] | Comprehensive guide to LLM Wiki architecture, workflows, and maintenance practices | schema/AGENTS.md |
| [[synthesis/iir-filter-fitting-frequency-response\|IIR Filter Fitting for Frequency Response]] | 向量拟合、SOS 参数化、峰值/谷值滤波器、梯度优化、状态空间辨识、Q&A | Liang 2026, Pawelczyk 1997 |
| [[synthesis/multi-modal-speech-enhancement\|Multi-Modal Speech Enhancement]] | Multi-modal approaches combining BC, AC, IMU for robust speech enhancement | He 2025, Kuang 2024, Wang 2022, Tagliasacchi 2020 |
| [[synthesis/secondary-path-modeling-evolution|Secondary Path Modeling Evolution]] | 离线→在线→免建模→绕过：四条技术路线的决策矩阵与演进趋势 | Kuo 1999, Benois 2020, Liang 2026, Zhu 2020 |
