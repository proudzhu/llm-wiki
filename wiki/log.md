# Wiki Log

> **Purpose**: Chronological, append-only record of what happened and when.
> **Format**: `## [YYYY-MM-DD] operation | Description`
> **Operations**: `ingest`, `query`, `lint`

---

## [2026-04-10] ingest | LLM Wiki (Karpathy Gist)

- **Source**: `raw/articles/llm-wiki-karpathy.md`
- **Summary**: Initial setup of the LLM wiki structure based on Karpathy's gist describing the pattern for building personal knowledge bases using LLMs.
- **Pages created/updated**:
  - `wiki/sources/llm-wiki-karpathy.md` — Source summary page
  - `wiki/concepts/llm-wiki-pattern.md` — Concept page describing the core idea
  - `wiki/index.md` — Initial index
  - `schema/AGENTS.md` — Schema/conventions document
  - `README.md` — Project overview

---

## [2026-04-10] ingest | Why Mathematica does not simplify Sinh[ArcCosh[x]]

- **Source**: `raw/articles/Why Mathematica does not simplify Sinh[ArcCosh[x]].md`
- **Author**: John D. Cook
- **Summary**: Explores why Mathematica returns a seemingly complex expression for `Sinh[ArcCosh[x]]` instead of the simpler √(x²−1). The answer: Mathematica's output is correct for all complex inputs, while the simpler form assumes x ≥ −1. Illustrates how CASs handle branch cuts and domain assumptions.
- **Pages created/updated**:
  - `wiki/sources/why-mathematica-not-simplify-sinh-arccosh.md` — Source summary page
  - `wiki/concepts/branch-cuts.md` — Concept page on branch cuts in complex analysis
  - `wiki/concepts/symbolic-computation.md` — Concept page on CAS and symbolic computation
  - `wiki/entities/john-d-cook.md` — Entity page for the author
  - `wiki/index.md` — Updated with new pages

---

## [2026-04-10] ingest | A Simplified Adaptive Feedback Active Noise Control System

- **Source**: `raw/papers/Wu 等 - 2014 - A simplified adaptive feedback active noise contro.md`
- **Authors**: Lifu Wu, Xiaojun Qiu, Yecai Guo
- **Published**: Applied Acoustics, Vol. 81, pp. 40–46, 2014
- **Summary**: Proposes a Simplified Adaptive Feedback (SimpAFB) ANC system that uses the error signal directly as the reference signal, eliminating the IMC's expensive convolution operation. Uses leaky FxLMS for stability. Validated by simulations and duct experiments (10 dB reduction for 250–300 Hz narrow band noise).
- **Pages created/updated**:
  - `wiki/sources/wu-2014-simplified-adaptive-feedback-anc.md` — Source summary page
  - `wiki/concepts/active-noise-control.md` — Core concept: ANC overview and architectures
  - `wiki/concepts/filtered-x-lms.md` — The standard FxLMS adaptive algorithm for ANC
  - `wiki/concepts/leaky-fxlms.md` — FxLMS variant with leakage for stability
  - `wiki/concepts/internal-model-control.md` — IMC structure in adaptive feedback ANC
  - `wiki/concepts/simplified-adaptive-feedback-anc.md` — The proposed SimpAFB system
  - `wiki/entities/lifu-wu.md` — First author
  - `wiki/entities/xiaojun-qiu.md` — Corresponding author
  - `wiki/entities/yecai-guo.md` — Co-author
  - `wiki/index.md` — Updated with all new pages

---

## [2026-04-10] query | 什么是 Simplified Adaptive Feedback ANC

- **Answer saved to**: `wiki/queries/what-is-simplified-adaptive-feedback-anc.md`
- **Summary**: Comprehensive overview of SimpAFB: core idea (error signal as reference), why simplification works, stability condition, leaky FxLMS necessity, performance comparison vs IMC/non-adaptive, and experimental results.

---

## [2026-04-10] ingest | Active Noise Control: A Tutorial Review

- **Source**: `raw/papers/Kuo 和 Morgan - 1999 - Active noise control a tutorial review.md`
- **Authors**: Sen M. Kuo, Dennis R. Morgan
- **Published**: Proceedings of the IEEE, Vol. 87, No. 6, June 1999, pp. 943–973
- **Summary**: Comprehensive ANC tutorial review — the most widely cited ANC reference paper. Covers FXLMS derivation and analysis, leaky FxLMS, acoustic feedback effects and solutions, broad-band/narrow-band feedforward, adaptive feedback (IMC), multi-channel ANC, online secondary-path modeling, and special algorithms (lattice, frequency-domain, subband, RLS).
- **Pages created/updated**:
  - `wiki/sources/kuo-1999-active-noise-control-tutorial-review.md` — Full paper summary with key equations and algorithm comparisons
  - `wiki/concepts/broad-band-feedforward-anc.md` — Standard ANC architecture with upstream reference mic and FXLMS
  - `wiki/concepts/narrow-band-feedforward-anc.md` — Internally generated sinusoidal references, no feedback problem
  - `wiki/concepts/multi-channel-anc.md` — MIMO ANC with multichannel FxLMS, O(M·L·N) complexity
  - `wiki/concepts/acoustic-feedback.md` — Anti-noise upstream radiation, neutralization, IIR solutions
  - `wiki/entities/sen-m-kuo.md` — ANC authority, Northern Illinois University
  - `wiki/entities/dennis-r-morgan.md` — Bell Labs, foundational FXLMS stability analysis
  - `wiki/index.md` — Updated with all new pages

---

## [2026-04-10] query | 如何估计次级通道

- **Answer saved to**: `wiki/queries/how-to-estimate-secondary-path.md`
- **Summary**: Three methods: offline modeling (inject white noise, identify with LMS), online modeling (simultaneous identification during ANC operation with low-power noise injection), and pure delay approximation (for narrow-band). FXLMS tolerates <90° phase error.

## [2026-04-10] query (rewrite) | 如何估计次级通道

- **Answer updated**: `wiki/queries/how-to-estimate-secondary-path.md`
- **Summary**: Expanded from Kuo 1999 Section VI. Added: fundamental problem (y(n) causes biased convergence to 1/W(z)), additive random noise method with convergence analysis (online takes σ_d²/σ_v² times longer than offline), improvement techniques (adaptive noise cancellation ×30 speedup, adaptive predictor), overall modeling algorithm with 3 filters, comparison table, and multi-channel challenges.

## [2026-04-10] query (rewrite) | 如何估计次级通道

- **Answer updated**: `wiki/queries/how-to-estimate-secondary-path.md`
- **Summary**: Added two new methods: (1) Simultaneous Equations Method (Jin, Yang & Xiao 2007) — solves for W(z) and S(z) simultaneously from algebraic relations without auxiliary noise injection; (2) Genetic Algorithm (Chang & Chen 2010) — evolutionary search bypasses S(z) identification entirely, tolerant of nonlinearities but extremely high computation. Updated comparison table to 5 methods + pure delay approximation.

## [2026-04-10] query (rewrite) | 如何估计次级通道 — Zotero 文献综述

- **Answer updated**: `wiki/queries/how-to-estimate-secondary-path.md`
- **Summary**: Comprehensive rewrite based on 21 papers from Zotero library. Reorganized into 4 categories: (1) Explicit S(z) modeling — offline, additive noise (Yang 2026 RMFxLMS, Cao 2025 ELSTM-ANC-OSPM), overall modeling, coefficient update; (2) No auxiliary noise — simultaneous equations (Jin 2007, Fujii 1999, Kajikawa 2000); (3) No S(z) identification — SPR (Zhou 2007), evolutionary (GA: Chang 2010/96 cites, PSO: Rout 2012/72 cites), careful control (Lopes 2022/2024), meta-learning (Yang 2026); (4) Coping strategies — blended FxLMS (Sarkar 2025), modeling error analysis (Tabatabaei 2012/67 cites). Added full comparison table with 12 methods and 21 paper index.

## [2026-04-10] query (enhance) | 如何估计次级通道 — 添加 Zotero 链接

- **Answer updated**: `wiki/queries/how-to-estimate-secondary-path.md`
- **Summary**: Added `zotero://select/items/0_XXX` links to all 21 paper references (41 total link instances across inline tables and paper index). Clicking opens the paper directly in Zotero from Obsidian.

## [2026-04-10] query (enhance) | 如何估计次级通道 — 添加推导公式

- **Answer updated**: `wiki/queries/how-to-estimate-secondary-path.md`
- **Summary**: Added comprehensive derivation appendix (10 sections, A-J) covering: offline modeling LMS, additive noise online modeling (Kuo 1999 Eq. 59-63, convergence analysis, mean-square error), overall 3-filter algorithm (non-unique solution proof), simultaneous equations method (differencing, RLS implementation), SPR algorithm (Lyapunov proof), genetic algorithm (adaptive crossover/mutation rates), PSO (conditional reinitialization), careful control (dual control framework, alternating least squares), FXLMS modeling error impact (stability condition, steady-state performance), meta-learning initialization (MAML for ANC).

---

## [2026-04-10] infra | Replace raw paper PDFs with zotero:// link files

- **Changed**: `raw/papers/` PDFs moved to `raw/assets/`, replaced with `.md` pointer files containing zotero:// links + YAML frontmatter
- **Mappings**: Kuo 1999 → `99AD6FSU`, Wu 2014 → `IUCZFYQX`
- **Updated**: All wiki pages' `sources:` frontmatter from `.pdf` → `.md`
- **Added**: 📎 Zotero links to wiki source summary pages

---

## [2026-04-10] lint | Health check

- **Findings**:
  - **4 missing pages**: `[[Adaptive Feedback Control]]`, `[[Online Secondary-Path Modeling]]`, `[[Complex Analysis]]`, `[[Analytic Continuation]]` — all created
  - **1 sign convention discrepancy**: IMC reference signal uses `+` in Kuo 1999 vs `-` in Wu 2014 — documented the difference
  - **17 orphan pages**: Most entities and sources had no inbound links — added cross-references from core concept pages
  - **No contradictions** in numerical claims or definitions
- **Actions taken**:
  - Created `wiki/concepts/adaptive-feedback-control.md`, `wiki/concepts/online-secondary-path-modeling.md`, `wiki/concepts/complex-analysis.md`, `wiki/concepts/analytic-continuation.md`
  - Added sign convention note to `wiki/concepts/internal-model-control.md`
  - Added entity and source cross-references to `active-noise-control.md`, `broad-band-feedforward-anc.md`, `acoustic-feedback.md`, `john-d-cook.md`
  - Updated `wiki/index.md` with new pages (27 total)

---

## [2026-04-11] query | Far-Field Multichannel Speech Enhancement

- **Answer saved to**: `wiki/queries/far-field-multichannel-speech-enhancement-algorithms.md`
- **Summary**: 14 章综述覆盖波束形成 (DS → MVDR → GSC → Differential → Neural BF)、多通道维纳滤波 (MCWF/SDW-MWF/PMWF/GEVD)、噪声 PSD 估计 (SPP/MSC/CTS)、去混响 (CDR/WPE)、DOA 估计 (GCC-PHAT/MUSIC)、盲源分离 (AuxIVA)、双麦克风增强 (PLD/PEF)、深度学习语音增强 (CRNN/FRCRN/Neural BF/ArrayDPS)。从 Zotero 库提取 50+ 篇文献，为每篇添加 `zotero://select/items/0_XXX` 跳转链接。
- **Updated**: `wiki/index.md` — 新增 query 条目，统计更新为 28 页、3 个 queries

---

## [2026-04-11] lint | Health check

- **Contradictions**: None found
- **Stale claims**: `index.md` statistics outdated — says 28 pages / 15 concepts, actual is 29 content pages / 16 concepts
- **Orphan pages**: 1 — `concepts/llm-wiki-pattern.md` has zero inbound wikilinks
- **Missing pages** (wikilinked but don't exist):
  - `[[Offline Secondary-Path Modeling]]` — linked from `online-secondary-path-modeling.md`
  - `[[Frequency-Domain ANC]]` — linked from `multi-channel-anc.md` (×2)
  - `[[Subband ANC]]` — linked from `multi-channel-anc.md` (×2)
- **Missing cross-references**: Speech enhancement review has no links back to ANC concept pages
- **Data gaps**: WPE dereverberation, GSS/GEVD, neural ANC (Deep ANC, SFANC) — papers exist in Zotero but no concept pages

## [2026-04-11] lint (fix) | Resolved all lint findings

- **Fixed**:
  - `index.md` statistics corrected — 32 pages, 19 concepts
  - Orphan page `concepts/llm-wiki-pattern.md` — added `[[LLM Wiki Pattern]]` wikilink from `README.md`
  - Created 3 missing concept pages:
    - `wiki/concepts/offline-secondary-path-modeling.md` — contrasts with online method
    - `wiki/concepts/frequency-domain-anc.md` — FFT-based block processing, partitioned BFXLMS
    - `wiki/concepts/subband-anc.md` — per-subband adaptive filtering with independent optimization
  - Fixed wikilink in `online-secondary-path-modeling.md` to point to `[[Offline Secondary-Path Modeling]]`
  - Added cross-reference section to `wiki/queries/far-field-multichannel-speech-enhancement-algorithms.md` linking to 8 ANC concept pages
  - Updated `wiki/index.md` with 3 new concept pages
  - Renamed `wiki/queries/远场多麦克风语音增强算法综述.md` → `wiki/queries/far-field-multichannel-speech-enhancement-algorithms.md`
- **Remaining** (deferred, low priority):
  - Data gaps: WPE, GSS/GEVD, neural ANC — papers exist in Zotero, concept pages can be created on demand

---

## [2026-04-11] query | Open-Ear Smart Glasses ANC

- **Answer saved to**: `wiki/queries/open-ear-anc-smart-glasses.md`
- **Summary**: CMU 首个开放式眼镜 ANC 系统，Yuan & Liu et al. (arXiv 2604.05519)。虚拟耳内感知：8 MEMS 麦克风 → U-Net+LSTM+FiLM → 2048-tap FIR × 4 通道。双流水线：CPU 神经网络 200ms 更新 + DSP 混合卷积 113µs 端到端。8 环境 × 11 用户：无校准 9.6 dB，校准后 11.2 dB。来源：[Zotero TVS87FW6](zotero://select/items/0_TVS87FW6)

---

## [2026-04-11] ingest | How AI Assistance Impacts the Formation of Coding Skills

- **Source**: `raw/articles/ai-assistance-coding-skills.md`
- **Authors**: Judy Hanwen Shen, Alex Tamkin (Anthropic Research)
- **Summary**: Randomized controlled trial with 52 software developers examining whether AI coding assistance affects skill acquisition. AI group scored 17% lower on comprehension quiz (50% vs 67%, p=0.01), with largest gap on debugging questions. However, interaction patterns matter: conceptual queries and verification patterns achieved ≥65% scores, while AI delegation patterns scored <40%.
- **Pages created/updated**:
  - `wiki/sources/ai-assistance-coding-skills.md` — Source summary page
  - `wiki/concepts/ai-skill-formation.md` — Concept page on AI skill formation and cognitive offloading
  - `wiki/entities/judy-hanwen-shen.md` — Entity page for first author
  - `wiki/entities/alex-tamkin.md` — Entity page for second author
  - `wiki/index.md` — Updated with all new pages (37 total)

---

## [2026-04-11] query | How AI Impacts Coding

- **Answer saved to**: `wiki/queries/how-ai-impacts-coding.md`
- **Summary**: Synthesized from Shen & Tamkin (2026) RCT: AI gives +80% productivity on tasks where developers already have skills, but −17% mastery (50% vs 67% quiz score) when learning something new. Six interaction patterns identified — conceptual queries and verification yield ≥65% comprehension, while delegation patterns yield <40%. Key concern: debugging skill development is most impaired.

---

## [2026-04-12] query | 自适应滤波变步长算法

- **Answer saved to**: `wiki/queries/adaptive-filtering-variable-step-size-algorithms.md`
- **Summary**: 从 Zotero 库检索 9 篇 VSS 自适应滤波论文，按方法分类：(1) Versiera/Versoria 函数法（Yu & Zhao 2013, Tian 2026）；(2) 噪声功率估计法（Zhao & Yu 2013/2015）；(3) 误差自相关法（Zipf 2025）；(4) 动量扰动法（Kar 2024）；(5) 凸组合 FxLMS/F（Song & Zhao 2019, Le & Dang 2025）；(6) VSS 组合 FxLMS（Kar & Burra 2025）。包含每种方法的核心公式、算法流程、参数敏感性、适用场景对比表。

---

## [2026-04-12] lint | Wiki health check

- **Pages audited**: 70 (23 entities, 26 concepts, 15 sources, 6 queries)
- **Issues found & fixed**:
  1. **Contradiction fixed**: `internal-model-control.md` — "FxLMS applied directly" vs "cannot directly use commercial FxLMS controllers" clarified to distinguish mathematical algorithm vs commercial hardware
  2. **Broken wikilinks fixed**: `ai-skill-formation.md` — `[[Shen & Tamkin (2026)]]` (2 occurrences) replaced with `[[Judy Hanwen Shen]]` + `[[Alex Tamkin]]` and `[[AI Assistance and Coding Skills]]`
- **Issues remaining (not fixed)**:
  - **10 orphan pages**: 1 entity (Yingying Zhu), 3 sources (Karpathy Gist, Zucchet 2026, Why Mathematica), 6 queries (Chinese-titled pages)
  - **24 missing concept pages**: Feedforward ANC, Minimum Variance Control, Hybrid ANC, Feedback ANC, Wiener Filter, Model Predictive Control, State-Space Model, System Identification, Active Vibration Control, Quadratic Programming, Kalman Filter, Impulsive Noise, Renyi Entropy, Kernel Methods, Transparency Mode, Voice Activity Detection, Beamforming, Bone Conduction, Ear Canal Occlusion Effect, Whispering Speech Recognition, Backpropagation Through Time, Real-Time Recurrent Learning, Linear Recurrent Unit, Generalized Maximum Correntropy Criterion
- **Frontmatter**: All 70 files pass — correct `type`, `created`, `updated` fields, ISO dates
- **Index accuracy**: 70 total pages, all table counts match statistics, all file paths resolve
- **Stale claims**: None detected

---

## [2026-04-12] lint | Fix all broken wikilinks

- **Root cause**: Wikilinks use citation-style titles like `[[Kuo 1999: Active Noise Control Tutorial Review]]` which don't match filenames or H1 titles
- **Fixes applied**:
  1. **Added `aliases` to 15 source files** — frontmatter aliases let Obsidian resolve citation-style wikilinks
  2. **Created 24 concept stub pages** — Feedback ANC, Feedforward ANC, Hybrid ANC, Minimum Variance Control, Wiener Filter, Model Predictive Control, State-Space Model, System Identification, Active Vibration Control, Quadratic Programming, Kalman Filter, Impulsive Noise, Kernel Methods, Rényi Entropy, Generalized Maximum Correntropy Criterion, Transparency Mode, Voice Activity Detection, Beamforming, Bone Conduction, Ear Canal Occlusion Effect, Whispering Speech Recognition, Backpropagation Through Time, Real-Time Recurrent Learning, Linear Recurrent Unit
  3. **Created 6 entity stub pages** — Stephen J. Elliott, Boaz Rafaely, Andrew J. Fleming, Udo Zölzer, Delf Sachau, Nicolas Zucchet
- **Result**: 91/94 unique wikilinks resolve (remaining 3 are documentation text inside code blocks in log.md, not navigation links)
- **index.md updated**: Added all 30 new pages (statistics: 100 total, 29 entities, 50 concepts)

- **Files renamed**:
  1. `concepts/filtered-x-lms.md` → `concepts/filtered-x-lms-algorithm.md` (title: "# Filtered-x LMS Algorithm")
  2. `concepts/leaky-fxlms.md` → `concepts/leaky-fxlms-algorithm.md` (title: "# Leaky FxLMS Algorithm")
- **index.md updated**: Paths for both concepts corrected
- **All wikilinks verified**: All 35 `[[Filtered-x LMS Algorithm]]` and 9 `[[Leaky FxLMS Algorithm]]` references use the correct wikilink text (wikilinks resolve by title, not filename, so they continue to work)

---

## [2026-04-12] synthesis | Cross-source analysis across wiki

- **5 synthesis pages created**:
  1. `synthesis/anc-architecture-evolution.md` — FF → FB → Hybrid architecture evolution (Kuo 1999 → Benois 2020)
  2. `synthesis/robust-anc-correntropy-to-gmcc.md` — Why FxLMS fails under impulsive noise, how GMCC solves it
  3. `synthesis/mpc-vs-fxlms-for-anc.md` — MPC (QP vs closed-form) vs FxLMS: constraint handling, latency, cost
  4. `synthesis/modern-headphone-anc-systems.md` — ANC + Awareness + Input layers converging to acoustic computing platforms
  5. `synthesis/adaptive-algorithm-tradeoffs.md` — Decision matrix across 6 algorithms on performance/robustness/cost
- **index.md updated**: Synthesis section populated (5 entries), statistics updated to 105 total pages

---

## [2026-04-12] synthesis | Cross-source analysis from Zotero library

- **3 new synthesis pages created from Zotero**:
  1. `synthesis/impulsive-noise-control.md` — Beyond Gaussian: FxLMS/F, clipped FxRLS, MVC vs GMCC, modified Versoria VSS — 4 robust cost functions for non-Gaussian noise (Liu 2024, Zeb 2017, Huang 2017, Tian 2026)
  2. `synthesis/nonlinear-anc-approaches.md` — FLNN, Volterra, Kernel, Spline, Convex Combination: when linear FxLMS fails under nonlinear distortion (Zhao & Zeng 2010, Zhao & Chen 2023 book, Song & Zhao 2019)
  3. `synthesis/kalman-filtering-for-anc.md` — State estimation reframing: standard KF vs MCC-KF, innovation whiteness test for model validation, real-time computational barrier (Chen & Liu 2017, Welch & Bishop 2006, Lesniewski)
- **index.md updated**: Synthesis section now has 10 entries, statistics updated to 108 total pages

---

## [2026-04-12] synthesis | Feedback ANC filter design from Zotero

- **New synthesis page**: `synthesis/feedback-anc-filter-design.md`
- **Papers connected**:
  1. Pawelczyk (1997) "Active Noise Control Using Feedback. Fixed and Adaptive Controllers" — MVC optimal fixed controller, IMC adaptive
  2. Vaudrey & Baumann (2003) "Stability and operating constraints of adaptive LMS-based feedback control" — Phase error < 90°, step size bound, delay constraint
  3. Arablouei & Doğançay (2015) "Constrained LMS" — Projected gradient for bounded coefficients, mean-square stability
  4. Morari & Zafiriou (2002) "Robust process control" — H∞ design, structured singular value μ for robust stability
  5. Zhao & Zeng (2010) "Reduced feedback FLNN" — Nonlinear feedback with trigonometric expansion, Lipschitz stability
- **Key contributions**:
  - Unified decision tree: 5 design paths (MVC, IMC+FxLMS, H∞, constrained LMS, FLNN)
  - Stability-robustness-performance triangle with quantitative ratings
  - Explicit stability theorems (Vaudrey phase constraint, robust stability bound ‖Ŝ·W‖∞ < 1/δ)
  - Waterbed effect explained via Bode integral
- **index.md updated**: 11 synthesis pages, 109 total

---

## [2026-04-12] synthesis | IIR 滤波器拟合频响曲线

- **New synthesis page**: `synthesis/iir-filter-fitting-frequency-response.md`
- **Topic**: 从频响测量数据拟合 IIR 传递函数的完整方法学
- **Papers connected**:
  1. Liang et al. (2026) — 向量拟合在 MPC for ANC 中的实践：15 阶模型，< 1 dB NR 损失
  2. Cioffi & Kailath (1984) — 快速递归最小二乘，方程误差法
  3. Lesniewski — Hankel-SVD 状态空间辨识
  4. Vaudrey & Baumann (2003) — 相位误差 < 90° 稳定性约束
- **Key contributions**:
  - 4 种方法对比：向量拟合、方程误差、输出误差迭代、Hankel-SVD
  - Liang 2026 的阶数敏感性分析：5/10/15/25 阶的 NR 损失对比
  - 实用设计流程：测量→拟合→阶数选择→稳定性检查→形式转换
  - 极点翻转稳定性处理方法
- **index.md updated**: 12 synthesis pages, 110 total

---

## [2026-04-12] ingest | Generalized Correntropy for Robust Adaptive Filtering

- **Source**: `raw/papers/Chen 等 - 2016 - Generalized correntropy for robust adaptive filtering.md` (Zotero: HEYN2NCY)
- **Authors**: Badong Chen, Lei Xing, Haiquan Zhao, Nanning Zheng, José C. Príncipe
- **Published**: IEEE TSP, Vol. 64, No. 13, pp. 3376–3387, July 2016
- **Summary**: Proposes generalized correntropy using the GGD as kernel (α = 2: Gaussian, α = 1: Laplace). The GMCC criterion yields a highly stable adaptive filtering algorithm with zero probability of divergence. Key results: GMCC → MAP as β → 0, GMCC → LMP(p=α) as β → ∞, optimal solution has Wiener-like form with error-dependent weighting h(e) = exp(-λ|e|^α)·|e|^{α-2}.
- **Pages created/updated**:
  - `wiki/sources/chen-2016-generalized-correntropy-robust-adaptive-filtering.md`
  - `wiki/concepts/correntropy.md`
  - `wiki/concepts/generalized-correntropy.md`
  - `wiki/entities/badong-chen.md`, `wiki/entities/jose-c-principe.md`, `wiki/entities/lei-xing.md`, `wiki/entities/haiquan-zhao.md`, `wiki/entities/nanning-zheng.md`
  - `wiki/index.md`

## [2026-04-12] ai-paper-reader | Generalized Correntropy for Robust Adaptive Filtering

- **Note saved to**: `wiki/sources/chen-2016-generalized-correntropy-paper-reading-note.md`
- **Summary**: 完整中文阅读笔记（可直接发布到技术社区），覆盖 10 个章节：动机、GGD 核定义、GC-loss 与范数关系、GMCC 三极限定理（MAP/LMP/Wiener）、最优解类 Wiener 形式、可变步长推导、零 POD 证明与实验、稳态 EMSE 公式、α 设计直觉、系统对比表、Q&A。

---

## [2026-04-12] ingest | Whisphone: Whispering Input Earbuds

- **Source**: `raw/papers/Fukumoto - 2025 - Whisphone whispering input earbuds.md` (Zotero: GD9G92MT, arXiv: 2501.01636)
- **Author**: Masaaki Fukumoto, Microsoft Corporation
- **Published**: arXiv preprint, 2025 (WISS2024 日文会议论文英文版)
- **Summary**: Whisphone — 利用 canal-type ANC 耳塞 + 耳道内 MEMS 麦克风捕捉骨传导耳语的私密语音输入设备。核心原理：耳道闭塞效应放大信号 ~10dB + ANC 降噪 ~30dB = 总 S/N 改善 40dB。在 80dB(A) 噪声下耳语识别 WER <10%（Google/Whisper，无需额外训练）。超过 80dB(A) 可切换正常语音仍保持私密。还探索了眨眼/舌头动作等亚听觉成分用于隐蔽控制命令。
- **Pages created/updated**:
  - `wiki/sources/fukumoto-2025-whisphone-paper-reading-note.md` — 完整中文阅读笔记
  - `wiki/index.md` — 更新
  - `wiki/log.md` — 记录

---

## [2026-04-12] ingest | Real-time Implementation of Delayed MPC in ANC Systems

- **Source**: `raw/papers/Liang 等 - 2026 - Real-time implementation of delayed model predictive control in active noise control systems.md` (Zotero: J5CZZBZ2, JSV 2026)
- **Authors**: Chao Liang, Francesco Ripamonti, Hamid Reza Karimi, Marek Pawełczyk
- **Published**: Journal of Sound and Vibration, Vol. 635, 119800, 2026
- **Summary**: 首次将延迟 MPC 实时应用于 ANC。核心洞察：主路径传播延迟 $N_{dp}$ 提供了免费的因果预览窗口——只要预测视界 $f < N_{dp}$，未来扰动全部已知，无需外部预测模型。推导出无约束 MPC 的解析闭式解，计算量仅比 FxNLMS 多 ~30%（921 vs 706 次乘法/样本）。实验验证：交通/飞机/人声/冲击噪声下降噪 13-19 dB，比 FxNLMS 提升 2.5-7.7 dB；冲击噪声 FxNLMS 完全无法抑制而 MPC 仍有效。瞬时收敛（无需迭代适应）。
- **Pages created/updated**:
  - `wiki/sources/liang-2026-delayed-mpc-anc-paper-reading-note.md` — 完整中文阅读笔记
  - `wiki/entities/chao-liang.md`, `wiki/entities/francesco-ripamonti.md`, `wiki/entities/marek-pawelczyk.md`
  - `wiki/index.md`, `wiki/log.md`

---

## [2026-04-12] ingest | Robust Generalized Maximum Correntropy Criterion Algorithms for ANC

- **Source**: `raw/papers/Zhu 等 - 2020 - Robust generalized maximum correntropy criterion algorithms for active noise control.md` (Zotero: E297XA9L, IEEE/ACM TASLP 2020)
- **Authors**: Yingying Zhu, Haiquan Zhao, Xiangping Zeng, Badong Chen
- **Published**: IEEE/ACM TASLP, Vol. 28, pp. 1282-1292, 2020
- **Summary**: 在 FxMCC（高斯核 correntropy）基础上提出三级演进：(1) FxGMCC — GGD 核替代高斯核，增强脉冲噪声鲁棒性；(2) IFxGMCC — 引入连续混合 Lp 范数（积分 p∈[1,2]），消除 p 值选择问题，有解析积分解；(3) C-IFxGMCC — 凸组合方案（大/小步长双滤波器 + sigmoid 混合参数），同时实现快收敛和低稳态误差。得分函数分析揭示 correntropy 家族大误差时趋于零的内在鲁棒机制。在 α-稳定脉冲噪声、正弦+脉冲混合噪声、牵引变电站真实噪声（含非最小相位系统）下全面优于 FxLMP、RFxLMS、FxMCC。62Hz 处降噪达 47.96 dB（C-IFxGMCC）。
- **Pages created/updated**:
  - `wiki/sources/zhu-2020-robust-gmcc-anc-paper-reading-note.md` — 完整中文阅读笔记
  - `wiki/entities/yingying-zhu.md`
  - `wiki/index.md`, `wiki/log.md`

---

## [2026-04-12] ingest | Headphone Conversation Detect (US20240363094A1)

- **Source**: `raw/papers/Masilamani 等 - 2024 - Headphone Conversation Detect.md` (Zotero: SWVHWRU4, US Patent US20240363094A1)
- **Inventors**: Rajesh Masilamani, Rakesh Murgai, Justin Woodruff
- **Published**: US Patent Application US20240363094A1, 2024
- **Summary**: 自动对话检测专利——双 VAD 架构（OVAD + TVAD），自适应空闲阈值判定对话结束。三阶段误触发拒绝 + ML 识别哼歌/咳嗽。双耳交叉验证。说话人 ID 和对话签名匹配。动态波束形成孔径基于头部偏航角。行人边界提供空间维度对话终止。媒体播放处理：人声去除、闪避、空间化。
- **Pages created/updated**:
  - `wiki/sources/masilamani-2024-headphone-conversation-detect-paper-reading-note.md`
  - `wiki/index.md`, `wiki/log.md`

## [2026-04-12] defuddle ingest | Forward Propagation of Errors Through Time

- **Source**: `raw/articles/Forward propagation of errors through time - Zucchet 2026.md` (via defuddle from nicolaszucchet.github.io)
- **Author**: Nicolas Zucchet
- **Published**: 2026-02-17
- **Summary**: 推导出精确的正向误差传播算法（FPTT）替代 BPTT——通过 warm-up 阶段确定 δ_0，然后正向传播计算所有 δ_t。理论上可行，MNIST98 上测试损失甚至略优于 BPTT（0.673 vs 0.691）。但致命缺陷：网络遗忘时（特征值 |λ|<1），Jacobian 反转后特征值 >1，warm-up 误差被指数放大 λ^{-T}ε。"Networks that forget cannot be learned with forward propagation of error." 不继续研究的原因：数值不稳定、可逆 BPTT 在所有维度上更优、Jacobian 计算/反转成本高。
- **Pages created/updated**:
  - `wiki/sources/zucchet-2026-forward-propagation-errors-through-time.md`
  - `wiki/index.md`, `wiki/log.md`

---

## [2026-04-12] lint | Comprehensive health check + fixes

- **Missing pages created (7)**:
  - `concepts/maximum-correntropy-criterion.md` — MCC algorithm, exponential outlier suppression
  - `concepts/robust-adaptive-filtering.md` — Score function comparison table, 4 approach categories
  - `concepts/information-theoretic-learning.md` — ITL framework, Rényi entropy, correntropy connection
  - `concepts/generalized-gaussian-distribution.md` — GGD family, α parameter, Mercer's condition
  - `entities/rajesh-masilamani.md`, `entities/rakesh-murgai.md`, `entities/justin-woodruff.md` — Patent inventors
- **Broken wikilinks fixed (4 files)**: `[[Why Mathematica does not simplify Sinh[ArcCosh[x]]]]` → markdown links (bracket `]` in title breaks `[[...]]` syntax)
- **Index fixed**: Statistics corrected (Concepts 22→26, Sources 14→11), 4 missing entities added, 3 missing concepts added, yingying-zhu added
- **Frontmatter fixed (6 files)**: Added missing `sources` field to frequency-domain-anc, offline-secondary-path-modeling, subband-anc, alex-tamkin, judy-hanwen-shen, far-field-multichannel-speech-enhancement-algorithms
- **No contradictions found**

---

## [2026-04-12] ingest | Forward Propagation of Errors Through Time

- **Source**: `raw/articles/Forward propagation of errors through time.md` (from Obsidian clipping)
- **Author**: Nicolas Zucchet
- **Published**: 2026-02-17
- **Summary**: 推导出精确的正向误差传播算法（FPTT）替代 BPTT——通过 warm-up 阶段确定 δ_0，然后正向传播计算所有 δ_t。理论上可行，MNIST98 上测试损失甚至略优于 BPTT（0.673 vs 0.691）。但致命缺陷：网络遗忘时（特征值 |λ|<1），Jacobian 反转后特征值 >1，warm-up 误差被指数放大 λ^{-T}ε。"Networks that forget cannot be learned with forward propagation of error."
- **Pages created/updated**:
  - `wiki/sources/zucchet-2026-forward-propagation-errors-through-time.md`
  - `wiki/index.md`, `wiki/log.md`

---

## [2026-04-12] ingest | MPC Constraint Handling in ANC/AVC

- **Source**: `raw/papers/Wills 等 - 2008 - Model predictive control applied to constraint handling in active noise and vibration control.md` (Zotero: QU9NZUUG)
- **Authors**: Adrian G. Wills, Dale Bates, Andrew J. Fleming, Brett Ninness, S. O. Reza Moheimani
- **Published**: IEEE TCST, Vol. 16, pp. 3-12, January 2008
- **Summary**: 首次将传统在线 QP 求解 MPC 应用于主动振动控制的执行器饱和约束处理。18 阶悬臂梁模型（5 个弯曲模态，5-500 Hz），5 kHz 采样率，预测视界 N=12。在 200 MHz DSP（ADSP-21262）上 QP 求解时间 <150 μs。遇到约束时 MPC 显著优于饱和 LQG（settling time 缩短，总能量降低）。
- **Pages created/updated**:
  - `wiki/sources/wills-2008-mpc-constraint-handling-anc-avc.md`
  - `wiki/index.md`, `wiki/log.md`

---

## [2026-04-12] ingest | ANC Feedback: Fixed and Adaptive Controllers

- **Source**: `raw/papers/Pawelczyk 等 - 1997 - Active Noise Control Using Feedback. Fixed and Adaptive Controllers.md` (Zotero: 78M97YB2, ISVR TM822)
- **Authors**: Marek Pawełczyk, Stephen J. Elliott, Boaz Rafaely
- **Published**: ISVR Technical Memorandum 822, December 1997
- **Summary**: ISVR 报告对比固定（鲁棒/H∞/IMC）与自适应（FxLMS）反馈 ANC 控制器。针对耳机/头枕等无前馈参考传感器的场景，讨论稳定性裕度、鲁棒性与非平稳噪声下的跟踪能力。PDF 仅含封面页，内容基于元数据与文献背景整理。
- **Pages created/updated**:
  - `wiki/sources/pawelczyk-1997-anc-feedback-fixed-adaptive.md`（初版，元数据）
  - `wiki/index.md`, `wiki/log.md`

## [2026-04-12] ingest (OCR complete) | ANC Feedback: Fixed and Adaptive Controllers

- **Source**: `raw/papers/Pawelczyk 等 - 1997 - Active Noise Control Using Feedback. Fixed and Adaptive Controllers.md` (Zotero: 78M97YB2, ISVR TM822, 74 pages, OCR'd)
- **Authors**: Marek Pawełczyk, Stephen J. Elliott, Boaz Rafaely
- **Published**: ISVR Technical Memorandum No. 822, December 1997
- **Summary**: 系统性推导反馈 ANC 的完整理论框架：(1) 最优固定控制器——MVC/IMC 等价性证明，最小相位/非最小相位植物处理，WMVC 控制努力 trade-off，Wiener 滤波器信号处理方法，H∞ 鲁棒稳定性；(2) 自适应控制器——预测模型推导，RLS 在线识别（Ljung 收敛条件），LMS/FXLMS 更新，泄漏 LMS 鲁棒性，全自适应 IMC；(3) 关键结论——延迟从 1→2 样本降噪降低 ~10 dB，延迟>7 样本时反馈控制无意义，主动耳机总延迟约 7 样本（6 个来自模拟滤波器）。
- **Pages created/updated**:
  - `wiki/sources/pawelczyk-1997-anc-feedback-fixed-adaptive.md`（完整版，含 OCR 内容）
  - `wiki/index.md`, `wiki/log.md`

---

## [2026-04-13] ingest | Hybrid and Pseudo-Cascaded ANC for Headphones

- **Source**: `raw/papers/Benois - 2020 - Hybrid and Pseudo-Cascaded Active Noise Control Applied to Headphones.md` (Zotero: CD3T4L4I, PhD Dissertation)
- **Author**: Piero Iared Rivera Benois
- **Supervisors**: Udo Zölzer, Delf Sachau
- **Published**: Helmut-Schmidt-Universität Hamburg, 2020, 204 pages
- **Summary**: 博士论文——首次将 FF+MVC+IMC 三种经典 ANC 方案同时组合为一种系统，无需额外硬件。提出三种依赖级别（低/中/高）的新型控制结构。两阶段优化：先 MVC+IMC 联合优化（稳定性/性能/增益约束），再 FF 优化。Modified Normalized FxLMS 集成，最小内存/计算开销。FPGA 原型+虚拟人头测量验证：同侧激励结果确认；对侧激励下 FF 引入低频噪声但 MVC+IMC 仍有效。关键发现：短控制器时混合结构低频改善显著，水床效应被 FF 补偿。
- **Pages created/updated**:
  - `wiki/sources/benois-2020-hybrid-pseudo-cascaded-anc-headphones.md`
  - `wiki/entities/piero-iared-rivera-benois.md`
  - `wiki/index.md`, `wiki/log.md`

---

## [2026-04-17] ingest | How AI assistance impacts the formation of coding skills (Full Post)

- **Source**: `raw/articles/How AI assistance impacts the formation of coding skills.md`
- **Summary**: Full Anthropic blog post content added as a primary source for the AI skill formation study.
- **Pages updated**:
  - `wiki/sources/ai-assistance-coding-skills.md` — Added fuller source reference.

---

## [2026-04-17] lint | Expanded 30+ stub pages

- **Findings**: 30 stub pages (24 concepts, 6 entities) created on 2026-04-12 needed expansion to be useful.
- **Actions taken**:
  - **Expanded 24 concepts**: Feedback ANC, Feedforward ANC, Hybrid ANC, Active Vibration Control, Model Predictive Control, Quadratic Programming, Impulsive Noise, Transparency Mode, Voice Activity Detection, Bone Conduction, Ear Canal Occlusion Effect, Whispering Speech Recognition, Backpropagation Through Time, Real-Time Recurrent Learning, Linear Recurrent Unit, Correntropy, Maximum Correntropy Criterion, Generalized Correntropy, Generalized Gaussian Distribution, Information Theoretic Learning, Robust Adaptive Filtering, Kernel Methods, Rényi Entropy, Generalized Maximum Correntropy Criterion.
  - **Expanded 6 entities**: Stephen J. Elliott, Boaz Rafaely, Andrew J. Fleming, Udo Zölzer, Delf Sachau, Nicolas Zucchet.
  - **Fixed broken links**: Created `wiki/concepts/secondary-path-modeling.md` to resolve multiple missing links.
  - **Added aliases**: Added "Vector Fitting" and "IIR 滤波器拟合频响曲线" aliases to resolve links.
- **Result**: Wiki content density significantly increased; all major ANC and ML concepts now have full descriptions and source citations.

---

## [2026-04-17] index | Update statistics and dates

- **Actions taken**:
  - Updated `wiki/index.md` statistics to reflect new pages and expansions.
  - Updated "Last updated" date to 2026-04-17.

---

## [2026-04-17] synthesis | Kalman Filter Theory and Application

- **Summary**: Created a broad synthesis page for Kalman filtering, connecting general theory (Welch & Bishop) with robust variations (MCC-KF) and practical applications in control (MPC) and audio tracking.
- **Pages created/updated**:
  - `wiki/synthesis/kalman-filter-theory-and-application.md` — New synthesis page.
  - `wiki/index.md` — Updated statistics and added new page.

---

## [2026-04-17] lint | Merged redundant Kalman synthesis pages

- **Action**: Merged `wiki/synthesis/kalman-filtering-for-anc.md` into `wiki/synthesis/kalman-filter-theory-and-application.md`.
- **Reason**: Consolidate all state-estimation knowledge into a single, high-density resource and avoid redundancy.
- **Pages updated**:
  - `wiki/synthesis/kalman-filter-theory-and-application.md` — Comprehensive merge.
  - `wiki/index.md` — Updated statistics and removed redundant entry.
- **Pages deleted**:
  - `wiki/synthesis/kalman-filtering-for-anc.md`

---

## [2026-04-17] ingest | Yang et al. (2026) Gaze-Guided AVSE

- **Summary**: Ingested preprint on Gaze-Guided Audio-Visual Speech Enhancement (GG-AVSE).
- **Pages created/updated**:
  - `wiki/sources/yang-2026-gaze-guided-avse.md` — New source page.
  - `wiki/index.md` — Added to sources table, updated statistics.

---

## [2026-04-17] lint | Health check: Identified 1 orphan page (robust-anc-impulsive-non-stationary)

## [2026-04-17] lint (fix) | Resolved orphan page: robust-anc-impulsive-non-stationary linked

---

## [2026-04-17] ingest | Synthesis: Computational and Memory Efficiency

---

## [2026-04-17] ingest | Synthesis: AI-Driven Active Noise Control

---

## [2026-04-17] lint | Expanded AI-Driven ANC synthesis with details on SFANC, GFANC, and Deep ANC (CRN)

---

## [2026-04-17] lint | Health check: Created missing concept pages for Deep Learning for Signal Processing and Virtual Sensing; updated index

---

## [2026-04-18] ingest | It's ok to compare floating points for equality

---

## [2026-04-18] synthesis | Virtual Sensing Evolution: from RMT to Neural observation filters (Zotero)

---

## [2026-04-18] ingest | Source: Obs-TasNet paper (Neural Virtual Sensing)

---

## [2026-04-18] ingest | Added summary pages for 6 papers on Virtual Sensing

---

## [2026-04-18] synthesis | Head-Mounted ANC: Occlusion & Transparency (multi-modal convergence)

---

## [2026-04-18] ingest | Zhang 2024: Neural Network Augmented Kalman Filter for Robust Acoustic Howling Suppression

---

## [2026-04-18] ingest | Source: Karpathy: LLM OS

---

## [2026-04-19] ingest | Jensen Huang: Will Nvidia’s moat persist?

---

## [2026-04-22] ingest | Lu et al. (2024) Headphone Speech Listening

- **Summary**: Ingested Apple patent US20240005903A1 focusing on dynamic transparency adjustment based on ambient noise spectral characteristics.
- **Pages created/updated**:
  - `wiki/sources/lu-2024-headphone-speech-listening-ambient-noise.md` — New source page.
  - `wiki/index.md` — Added to sources table, updated statistics.

---

## [2026-04-22] ingest | Jiang et al. (2025) AI-Driven AVNC Review

- **Summary**: Ingested systematic review of artificial intelligence-driven active vibration and noise control (AI-AVNC), classifying 4 technical paths and engineering applications.
- **Pages created/updated**:
  - `wiki/sources/jiang-2025-ai-driven-avnc-review.md` — New source page.
  - `wiki/index.md` — Added to sources table, updated statistics.

---

## [2026-04-22] ingest | Primary References from Jiang et al. (2025)

---

## [2026-04-22] ingest | Primary References from Jiang et al. (2025) (continued)

- **Summary**: Ingested three critical reference papers cited in the AI-AVNC review to provide technical depth and direct evidence.
- **Pages created/updated**:
  - `wiki/sources/enzner-2006-fdakf-echo-control.md` — FDAKF foundation.
  - `wiki/sources/fareedha-2025-dfanc-ekf.md` — CNN-EKF hybrid.
  - `wiki/sources/dietzen-2020-isclp-kalman.md` — Joint dereverberation.
  - `wiki/index.md` — Added to sources table, updated statistics.

---

## [2026-04-22] ingest | Jiang et al. (2025) AI-Driven AVNC Review (Extended)

- **Summary**: Performed a deep-dive ingestion of the 48-page review paper. Extracted 9 figures and images to `raw/assets/jiang-2025-review/images/`. Generated a high-density professional reading note using the `ai-paper-reader` skill.
- **Pages created/updated**:
  - `wiki/sources/jiang-2025-ai-driven-avnc-review.md` — Comprehensive technical note with images.
  - `wiki/index.md` — Updated source descriptions and statistics.
- **Ref Ingestions**: Ingested 7 primary references cited in the review to provide a complete evidence chain (Cha 2023, Zhang 2023, Luo 2026, Yang 2014, Enzner 2006, Fareedha 2025, Dietzen 2020).

---

## [2026-04-22] lint | Wiki Link & Statistics Pass

- **Tasks**:
  - Fixed broken wikilinks: Converted all [[wiki/...]] links to correct relative paths across 142 files.
  - Updated Index Statistics: Refreshed counts for entities (33), concepts (60), sources (42), synthesis (21), and total pages (162).
  - Verified relative paths in synthesis and queries subdirectories.
- **Pages updated**:
  - `wiki/index.md` — Statistics and table links updated.
  - `wiki/log.md` — Logged the action.
  - 140+ other files in `wiki/` subdirectories.

---

## [2026-04-22] ingest | Zhang 2022: Statistical signal processing approaches to analysis and synthesis of bone-conducted speech

- **Source**: `zotero://select/items/0_T6BE3UFG`
- **Summary**: Doctoral dissertation proposing WACF-CEP for noise-robust pitch extraction and LS-IIR for converting AC speech to synthetic BC speech.
- **Pages created/updated**:
  - `wiki/sources/zhang-2022-bone-conducted-speech-dissertation.md`
  - `wiki/sources/zhang-2022-bone-conducted-speech-reading-note.md`
  - `wiki/synthesis/multimodal-bc-speech-enhancement.md`
  - `wiki/index.md` — Updated statistics (167 pages)

---

## [2026-04-22] ingest | Shen 2023: Advanced active noise control headphone: algorithm and implementation

- **Source**: `zotero://select/items/0_EUIIZATZ`
- **Summary**: Doctoral dissertation proposing Adaptive Gain (AG), ASHANC, and Wireless ANC for modern headphones.
- **Pages created/updated**:
  - `wiki/sources/shen-2023-advanced-anc.md`
  - `wiki/sources/shen-2023-advanced-anc-reading-note.md`
  - `wiki/index.md` — Updated statistics (174 pages)
  - `raw/assets/shen-2023-advanced-anc/` — Extracted 105 images from PDF.

---

## [2026-04-25] synthesis | LLM Wiki Best Practices

- **Summary**: Created a comprehensive synthesis page on LLM Wiki architecture, workflows, and maintenance practices.
- **Pages created/updated**:
  - `wiki/synthesis/llm-wiki-best-practices.md` — New synthesis page.
  - `wiki/index.md` — Updated statistics and added new page.

---

## [2026-04-25] synthesis | Secondary Path Modeling Evolution

- **Page**: `wiki/synthesis/secondary-path-modeling-evolution.md`
- **Summary**: 四条技术路线（离线→在线→免辅助噪声→绕过辨识）的跨源综合，含决策矩阵与演进趋势。

---

## [2026-04-25] ingest | Schwarz 2019: Dereverberation and Robust Speech Recognition

- **Source**: `raw/papers/Schwarz - 2019 - Dereverberation and robust speech recognition using spatial coherence models.md` (Zotero: BD6AVHPW)
- **Author**: Andreas Schwarz
- **Published**: FAU, 2019, Doctoral Dissertation
- **Summary**: 博士论文——利用空间相干性模型进行去混响和鲁棒语音识别。核心贡献：(1) 统一 CDR 框架下的谱增强方法；(2) 无需源位置信息的去混响系统；(3) 空间特征向量作为 DNN 输入提升 ASR 鲁棒性。
- **Pages created**:
  - `wiki/sources/schwarz-2019-dereverberation-spatial-coherence.md`
  - `wiki/entities/andreas-schwarz.md`
  - `wiki/concepts/spatial-coherence.md`
  - `wiki/index.md`

---

## [2026-04-25] lint | Health check

- **Orphan pages**: `wiki/synthesis/parameterized-iir-curve-fitting-review.md` — no inbound links, added to index
- **Statistics fix**: Concepts 65→63, Total 179→177 (actual file counts)
- **File rename**: `raw/papers/Schwarz…txt` → `.md` (all 4 references updated)
- **No contradictions or stale claims detected**
- **No missing pages detected**

---

## [2026-04-25] ingest | Spiking Neural Networks and Their Applications: A Review

- **Source**: `raw/papers/Yamazaki 等 - 2022 - Spiking neural networks and their applications a review.md` (Zotero: 3EGFJDGI)
- **Authors**: Kashu Yamazaki, Viet-Khoa Vo-Ho, Darshan Bulsara, Ngan Le
- **Published**: Brain Sciences, 12(7):863, 2022
- **DOI**: 10.3390/brainsci12070863
- **Summary**: Comprehensive SNN review covering biological neuron fundamentals, spiking neuron models (HH, LIF, Izhikevich, SRM), synapse models, learning mechanisms (spike BP, STDP variants, ANN-to-SNN conversion), spike encoding, and applications in computer vision and robotics.
- **Pages created**:
  - `wiki/sources/yamazaki-2022-spiking-nn-review.md`
  - `wiki/entities/kashu-yamazaki.md`
  - `wiki/entities/viet-khoa-vo-ho.md`
  - `wiki/entities/darshan-bulsara.md`
  - `wiki/entities/ngan-le.md`
  - `wiki/concepts/spiking-neural-networks.md`
  - `wiki/concepts/neuromorphic-computing.md`
  - `wiki/concepts/spike-timing-dependent-plasticity.md`
- **Pages updated**:
  - `wiki/concepts/neural-networks.md` — expanded from placeholder with three-generation framework and SNN connections
  - `wiki/index.md` — added 8 new pages, updated stats

## [2026-04-25] ingest (re) | Speech-Preserving Active Noise Control: A Deep Learning Approach in Reverberant Environments

- **Source**: `raw/papers/Dai - 2026 - Speech-preserving active noise control a deep learning approach in reverberant environments.md` (Zotero: C9Q3C69G)
- **Author**: Shuning Dai
- **Supervisor**: Gan Woon Seng
- **Institution**: Nanyang Technological University (School of EEE)
- **Year**: 2026
- **Type**: Master's Dissertation (MSc in Signal Processing and Machine Learning)
- **arXiv**: 2604.10979
- **Summary**: Proposes an end-to-end Deep ANC system using CRN with Complex Spectrum Mapping and a speech-preserving loss function that algebraically cancels speech components, training the network to selectively cancel noise while leaving speech transparent. Validated in ISM-simulated reverberant environment (RT60=0.3s). Deep ANC achieves 18-23 dB noise reduction (vs 5-12 dB for FxLMS) and 10-15 dB improvement at nonlinear harmonic frequencies.
- **Pages created**:
  - `wiki/entities/shuning-dai.md`
  - `wiki/concepts/convolutional-recurrent-network.md`
  - `wiki/concepts/complex-spectrum-mapping.md`
  - `wiki/concepts/speech-preserving-anc.md`
  - `wiki/concepts/image-source-method.md`
  - `raw/papers/Dai - 2026 - Speech-preserving active noise control….md` (zotero:// pointer file)
- **Pages updated**:
  - `wiki/sources/dai-2026-speech-preserving-deep-anc.md` — comprehensive rewrite with full problem formulation, CRN architecture details, loss function derivation, training configuration, results tables, and ANC vs SE distinction
  - `wiki/concepts/active-noise-control.md` — added Deep Learning Approaches section with performance comparison table, new challenges (nonlinear distortion, speech cancellation), and cross-references to CRN/CSM/speech-preserving ANC
  - `wiki/concepts/deep-learning-for-signal-processing.md` — added CSM and speech-preserving ANC to architectures and applications, added related sources
  - `wiki/synthesis/ai-driven-anc.md` — added speech preservation capability to Deep ANC section
  - `wiki/index.md` — added 5 new pages (1 entity, 4 concepts), updated source entry, updated stats (185→190 total, 38→39 entities, 66→70 concepts)

---

## [2026-04-25] ingest | An Introduction to the Kalman Filter

- **Source**: `raw/papers/Welch and Bishop - 2006 - An introduction to the kalman filter.md` (Zotero: UCQRBZUX)
- **Authors**: Greg Welch, Gary Bishop
- **Institution**: University of North Carolina at Chapel Hill, Department of Computer Science
- **Year**: 2006 (TR 95-041, originally published 1995)
- **Type**: Technical Report / Tutorial
- **Summary**: Seminal tutorial on the discrete Kalman filter and Extended Kalman Filter. Presents the complete predictor-corrector algorithm, Kalman gain derivation, filter tuning guidelines, EKF linearization via Jacobians, and a worked numerical example estimating a random constant with three simulations varying R.
- **Pages created**:
  - `raw/papers/welch-2006-kalman-filter-intro/full-text.txt` — extracted text from Zotero PDF
  - `raw/papers/Welch and Bishop - 2006 - An introduction to the kalman filter.md` — raw pointer file
  - `wiki/sources/welch-2006-kalman-filter-intro.md`
  - `wiki/entities/greg-welch.md`
  - `wiki/entities/gary-bishop.md`
  - `wiki/concepts/extended-kalman-filter.md`
- **Pages updated**:
  - `wiki/concepts/kalman-filter.md` — expanded from brief overview to comprehensive page with core algorithm equations, Kalman gain intuition table, tuning guidance, probabilistic interpretation, recursive advantage over Wiener filter, and EKF cross-reference
  - `wiki/concepts/state-space-model.md` — added Kalman filter and EKF cross-references
  - `wiki/concepts/adaptive-filtering.md` — expanded from placeholder with algorithm comparison table, Kalman relationship section, and cross-references
  - `wiki/concepts/wiener-filter.md` — added Kalman filter cross-reference
  - `wiki/index.md` — added 4 new pages (2 entities, 1 concept, 1 source), updated stats (190→194 total, 39→41 entities, 70→71 concepts, 48→49 sources)

---

## [2026-04-26] ingest | Data-Driven Uncertainty Modeling for Robust Feedback ANC

- **Source**: Zotero key IA5SPUL5, `raw/papers/hilgemann-2024-data-driven-uncertainty-anc/full-text.txt`
- **Authors**: Florian Hilgemann, Egke Chatzimoustafa, Peter Jax
- **Published**: J. Audio Eng. Soc., vol. 72, no. 12, pp. 873-883, 2024
- **Summary**: Proposes elliptic and convex hull uncertainty models for feedback ANC that more accurately capture secondary-path variations than conventional disk models. Integrated into IMC-based constrained optimization, these models achieve 10–18 dB more active attenuation below 1 kHz while maintaining robust stability, confirmed by measurements with 21 human wearers on Bose QC45/QC20 headphones.
- **Pages created**:
  - `raw/papers/hilgemann-2024-data-driven-uncertainty-anc/full-text.txt` — extracted text from Zotero PDF
  - `wiki/sources/hilgemann-2024-data-driven-uncertainty-anc.md`
  - `wiki/entities/florian-hilgemann.md`
  - `wiki/entities/egke-chatzimoustafa.md`
  - `wiki/entities/peter-jax.md`
  - `wiki/concepts/uncertainty-modeling-for-anc.md`
  - `wiki/concepts/convex-hull-uncertainty-model.md`
  - `wiki/concepts/elliptic-uncertainty-model.md`
  - `wiki/concepts/robust-stability-constraint.md`
- **Pages updated**:
  - `wiki/concepts/feedback-anc.md` — added robust controller optimization section, uncertainty model cross-references
  - `wiki/concepts/internal-model-control.md` — added IMC for fixed controller optimization section
  - `wiki/concepts/active-noise-control.md` — added uncertainty modeling cross-references
  - `wiki/index.md` — added 3 entities, 4 concepts, 1 source

---

## [2026-04-27] ingest | Joint Deep Secondary Path Estimation and Adaptive Control for ANC

- **Source**: `raw/papers/fareedha-2026-joint-deep-spe-anc/full-text.txt` (Zotero: P5G5VFR3)
- **Authors**: Fareedha, Vasundhara, Asutosh Kar, Mads Græsbøll Christensen
- **Published**: ICASSP 2026, pp. 15177–15181
- **Summary**: End-to-end deep learning framework that jointly performs secondary path estimation (DeepSPE: Conv1D + BiLSTM + Attention, −16.27 dB NMSE) and adaptive ANC control (ANC-Net: SE blocks + temporal attention for binary-weight filter selection, −12.38 dB NMSE, 1.05 M params, 0.43 ms latency). Outperforms classical adaptive filters and deep ANC baselines (SFANC, GFANC, GFANC-Kalman) on real and simulated impulse responses.
- **Pages created**:
  - `raw/papers/fareedha-2026-joint-deep-spe-anc/full-text.txt` — extracted text from Zotero PDF
  - `wiki/sources/fareedha-2026-joint-deep-spe-anc.md`
  - `wiki/entities/fareedha.md`
  - `wiki/entities/vasundhara.md`
  - `wiki/entities/asutosh-kar.md`
  - `wiki/entities/mads-graesboell-christensen.md`
  - `wiki/concepts/deep-secondary-path-estimation.md`
- **Pages updated**:
  - `wiki/concepts/secondary-path-modeling.md` — added Deep SPE section and cross-references
  - `wiki/concepts/deep-learning-for-signal-processing.md` — added Deep SPE application and source
  - `wiki/synthesis/ai-driven-anc.md` — added Section 2.4 Joint Deep SPE + Adaptive Control
  - `wiki/sources/fareedha-2025-dfanc-ekf.md` — added entity links and later work cross-reference
  - `wiki/index.md` — added 4 entities, 1 concept, 1 source

---

## [2026-04-27] ingest | VSS LMS for Online Secondary Path Modeling (Akhtar 2006)

- **Source**: `raw/papers/akhtar-2006-vss-lms-online-spm/full-text.txt` (Zotero: 9PFUVDQJ)
- **Authors**: Muhammad Tahir Akhtar, Masahide Abe, Masayuki Kawamata
- **Published**: IEEE Trans. Audio, Speech, and Language Processing, vol. 14, no. 2, pp. 720–726, March 2006
- **Summary**: Two-adaptive-filter method for online secondary path modeling using MFxLMS (control) + inverse VSS LMS (modeling). The VSS LMS starts with a small step size when disturbance is large and increases it as disturbance decreases — opposite of conventional VSS strategies. Achieves −12.35 dB NMSE, outperforms Zhang's three-filter method with reduced design complexity.
- **Pages created**:
  - `raw/papers/akhtar-2006-vss-lms-online-spm/full-text.txt` — extracted text from Zotero PDF
  - `wiki/sources/akhtar-2006-vss-lms-online-spm.md`
  - `wiki/entities/muhammad-tahir-akhtar.md`
  - `wiki/entities/masahide-abe.md`
  - `wiki/entities/masayuki-kawamata.md`
  - `wiki/concepts/variable-step-size-lms.md`
- **Pages updated**:
  - `wiki/concepts/online-secondary-path-modeling.md` — added Two-Filter vs Three-Filter section, VSS LMS and Deep SPE cross-references
  - `wiki/concepts/secondary-path-modeling.md` — added Eriksson/Zhang/Akhtar methods, VSS LMS source
  - `wiki/concepts/deep-secondary-path-estimation.md` — added VSS LMS cross-reference and source
  - `wiki/sources/fareedha-2026-joint-deep-spe-anc.md` — added Akhtar 2006 as classical baseline
  - `wiki/synthesis/secondary-path-modeling-evolution.md` — added Eriksson/Zhang/Akhtar in Route 2, DeepSPE in trend 5
  - `wiki/index.md` — added 3 entities, 1 concept, 1 source

---

## [2026-04-27] ingest | IMU-Based Acoustic Feedback Cancellation (Miran 2026)

- **Source**: `raw/papers/miran-2026-imu-feedback-cancellation/full-text.txt` (Zotero: W4JYT982)
- **Authors**: Sina Miran, Henning Schepker, Ivo Merks, Martin McKinney
- **Published**: ICASSP 2026, pp. 15172–15176
- **Summary**: Uses IMU (3-axis accelerometer) integrated in a BTE hearing aid to control the step size of PEM-NLMS adaptive feedback cancellation. Head movement acceleration triggers fast adaptation (μ_L=0.04) when path changes are anticipated; small step size (μ_S=0.004) during steady state. Outperforms audio-only VSS and shadow filter methods in steady-state by avoiding audio-induced biases. Limitation: cannot detect path changes from external objects preceding head movement.
- **Pages created**:
  - `raw/papers/miran-2026-imu-feedback-cancellation/full-text.txt` — extracted text from Zotero PDF
  - `wiki/sources/miran-2026-imu-feedback-cancellation.md`
  - `wiki/entities/sina-miran.md`
  - `wiki/entities/henning-schepker.md`
  - `wiki/entities/ivo-merks.md`
  - `wiki/entities/martin-mckinney.md`
- **Pages updated**:
  - `wiki/concepts/acoustic-feedback.md` — added AFC in hearing aids section with IMU-based step-size control
  - `wiki/synthesis/feedback-anc-and-feedback-cancellation.md` — added Gen 4 Multi-Modal AFC, design best practice #4
  - `wiki/synthesis/head-mounted-anc-occlusion-transparency.md` — added IMU AFC source
  - `wiki/index.md` — added 4 entities, 1 source

---

## [2026-04-28] synthesis | Adaptive Step-Size Control in Feedback ANC

- **Type**: New synthesis page
- **Page**: `wiki/synthesis/adaptive-step-size-control-feedback-anc.md`
- **Summary**: Cross-source synthesis on feedback ANC 步长控制的核心挑战——如何平衡收敛速度、稳态精度和鲁棒稳定性。提出三层步长控制层级：(1) 步长边界（不确定性建模、Leaky FxLMS、Constrained LMS），(2) 步长切换（音频 VSS），(3) 元步长（神经元协方差估计）。聚焦 feedback ANC，不涉及 AFC。
- **Sources connected**: Akhtar 2006 (inverse VSS), Hilgemann 2024 (data-driven uncertainty), Zhang 2024 (neural Kalman gain), Cha 2023 (DNoiseNet MLP), Pawelczyk 1997 (MVC/IMC), Wu 2014 (SimpAFB/leaky FxLMS)
- **Pages updated**:
  - `wiki/index.md` — added 1 synthesis, updated statistics

---

## [2026-04-28] ingest | Computation-Efficient Virtual Sensing with MCALMS (Wang 2024)

- **Source**: `raw/papers/wang-2024-computation-efficient-virtual-sensing/full-text.txt` (Zotero: YHFLXFQH)
- **Authors**: Boxiang Wang, Junwei Ji, Xiaoyi Shen, Dongyuan Shi, Woon-Seng Gan
- **Published**: INTER-NOISE 2024, Vol. 270, No. 10, pp. 1638–1650
- **Summary**: Proposes feedforward MVANC system using MCALMS algorithm instead of MCFxLMS. MCALMS filters error signal instead of reference signal, achieving 10× computational savings at 10 channels while maintaining ~35 dB noise reduction at virtual locations. Key finding: broadband tuning noise should encompass control stage frequency range for optimal performance (~40 dB NR); narrowband tuning for broadband control drops to ~22 dB.
- **Pages created**:
  - `raw/papers/wang-2024-computation-efficient-virtual-sensing/full-text.txt` — extracted text from Zotero PDF
  - `wiki/sources/wang-2024-computation-efficient-virtual-sensing.md`
  - `wiki/concepts/adjoint-lms-algorithm.md`
  - `wiki/entities/boxiang-wang.md`
  - `wiki/entities/junwei-ji.md`
  - `wiki/entities/xiaoyi-shen.md`
  - `wiki/entities/dongyuan-shi.md`
  - `wiki/entities/woon-seng-gan.md`
- **Pages updated**:
  - `wiki/sources/computation-efficient-virtual-sensing-approach-wit.md` — replaced with comprehensive source page
  - `wiki/synthesis/virtual-sensing-evolution.md` — updated Adjoint LMS section with MCALMS details
  - `wiki/index.md` — added 5 entities, 1 concept, 1 source

---

## [2026-04-28] ingest | Review of Virtual Sensing Algorithms for ANC (Moreau 2008)

- **Source**: `raw/papers/moreau-2008-virtual-sensing-review/full-text.txt` + images (Zotero: LJDPCZ9G)
- **Authors**: Danielle Moreau, Ben Cazzolato, Anthony Zander, Cornelis Petersen
- **Published**: Algorithms, Vol. 1, No. 2, pp. 69–99, 2008
- **Summary**: Comprehensive review of 9 virtual sensing methods for ANC: RMT, VMA, Forward Difference Prediction, Adaptive LMS VM, Kalman Filtering, Stochastically Optimal Tonal Diffuse Field, and 3 moving VS variants. Zone of quiet = λ/10 diameter. Table 1 provides complete comparison of all methods with characteristics, advantages, and disadvantages. All figures (11) and Table 1 extracted.
- **Pages created**:
  - `raw/papers/moreau-2008-virtual-sensing-review/full-text.txt` — extracted text from Zotero PDF
  - `raw/papers/moreau-2008-virtual-sensing-review/images/img-000.jpg` — Figure 1: Physical vs Virtual sensor comparison
  - `raw/papers/moreau-2008-virtual-sensing-review/images/img-001.pbm` — Figure 2: VMA block diagram
  - `raw/papers/moreau-2008-virtual-sensing-review/images/img-002.jpg` — Figure 4: RMT block diagram
  - `raw/papers/moreau-2008-virtual-sensing-review/images/img-003.pbm` — Figure 5: Forward Difference Prediction diagram
  - `wiki/entities/danielle-moreau.md`
  - `wiki/entities/ben-cazzolato.md`
  - `wiki/entities/anthony-zander.md`
  - `wiki/entities/cornelis-petersen.md`
- **Pages updated**:
  - `wiki/sources/a-review-of-virtual-sensing-algorithms-for-active-.md` — comprehensive rewrite with all figures, Table 1, and 9 algorithm categories
  - `wiki/index.md` — added 4 entities, updated source entry

---

## [2026-04-28] ingest | Low-latency Audio Front-end Region-of-Interest Beamforming for Smart Glasses

- **Source**: `raw/papers/frank-2026-low-latency-roi-beamforming/full-text.txt` (Zotero: DE8N9LJ7)
- **Authors**: Ariel Frank, Israel Cohen
- **Published**: ICASSP 2026, pp. 14727–14731
- **DOI**: 10.1109/ICASSP55912.2026.11462987
- **Summary**: Head-to-head comparison of time-domain and STFT-domain LDMG ROI beamformers for smart glasses. Using real 6-mic recordings, time-domain delivers 2x lower algorithmic latency and higher performance (DF, WNG, own-voice suppression) at the cost of increased computation (M Ly² vs O(M Ly log₂ Ly)).
- **Pages created**:
  - `raw/papers/frank-2026-low-latency-roi-beamforming/full-text.txt` — extracted text from Zotero PDF
  - `wiki/sources/frank-2026-low-latency-roi-beamforming.md`
  - `wiki/entities/ariel-frank.md`
  - `wiki/entities/israel-cohen.md`
  - `wiki/concepts/roi-beamforming.md`
- **Pages updated**:
  - `wiki/concepts/beamforming.md` — added ROI beamforming section with time-domain vs STFT comparison, updated sources
  - `wiki/index.md` — added 2 entities, 1 concept, 1 source, updated statistics (220→224 total)

## [2026-04-28] ingest (re) | Statistical Signal Processing Approaches to Analysis and Synthesis of Bone-Conducted Speech

- **Source**: `raw/papers/zhang-2022-bone-conducted-speech-dissertation/full-text.txt` (Zotero: T6BE3UFG)
- **Author**: Shiming Zhang
- **Published**: Saitama University, Doctoral Dissertation, 2022
- **Summary**: Re-ingested full dissertation text and merged with existing reading note. Comprehensive source page now includes: (1) WACF-CEP and WACF-WACF dual-modal pitch extraction with full experimental setup and GPE results across 5 noise types; (2) LS-IIR AC-to-BC synthesis with coefficient tables, LAR distance, listening test results, and noise-robustness analysis; (3) Systematic SNR quantification showing ~10 dB BC gain across 8 speakers.
- **Pages created**:
  - `raw/papers/zhang-2022-bone-conducted-speech-dissertation/full-text.txt` — extracted text from Zotero PDF
  - `wiki/entities/shiming-zhang.md`
- **Pages updated**:
  - `wiki/sources/zhang-2022-bone-conducted-speech-dissertation.md` — comprehensive rewrite merging source page + reading note with full equations, tables, and results
  - `wiki/synthesis/multimodal-bc-speech-enhancement.md` — updated date
  - `wiki/index.md` — merged 2 source entries into 1, added 1 entity, updated stats (54→53 sources, 57→58 entities)
- **Pages deleted**:
  - `wiki/sources/zhang-2022-bone-conducted-speech-reading-note.md` — content merged into source page

---

## [2026-04-28] merge | Consolidate duplicate source files in wiki/sources

- **Summary**: Merged 5 pairs of duplicate source files (source + reading note) into single comprehensive source pages, re-ingested PDFs from Zotero library for each
- **Duplicate pairs merged**:
  1. `chen-2016-generalized-correntropy-robust-adaptive-filtering.md` + `chen-2016-generalized-correntropy-paper-reading-note.md` → unified source with GGD correntropy, GMCC, zero-POD, Q&A
  2. `shen-2023-advanced-anc.md` + `shen-2023-advanced-anc-reading-note.md` → unified source with AG, ASHANC, Wireless ANC, ESM, math derivations
  3. `wang-2024-metric-learning-virtual-sensing.md` + `wang-2024-metric-learning-virtual-sensing-reading-note.md` → unified source with metric learning, 1D CNN, cosine similarity
  4. `holzmueller-2026-obs-tasnet-virtual-sensing.md` + `holzmueller-2026-obs-tasnet-virtual-sensing-reading-note.md` → unified source with Conv-TasNet, temporal bottleneck, asynchronous estimation
  5. `toyooka-2026-hybrid-anc-remote-sensing.md` + `toyooka-2026-hybrid-anc-virtual-sensing-paper-reading-note.md` → unified source with dual compensation filters, signal decomposition
- **Pages created**:
  - `raw/papers/chen-2016-generalized-correntropy/full-text.txt` — extracted from Zotero PDF (KJ2ILUFH)
  - `raw/papers/shen-2023-advanced-anc/full-text.txt` — extracted from Zotero PDF (BB3AEY8Z)
  - `raw/papers/wang-2024-metric-learning-virtual-sensing/full-text.txt` — extracted from Zotero PDF (6ABIUSW8)
  - `raw/papers/holzmueller-2026-obs-tasnet-virtual-sensing/full-text.txt` — extracted from Zotero PDF (5D63H833)
  - `raw/papers/toyooka-2026-hybrid-anc-virtual-sensing/full-text.txt` — extracted from Zotero PDF (ECHHX8YL)
- **Pages updated**:
  - `wiki/sources/chen-2016-generalized-correntropy-robust-adaptive-filtering.md` — merged with reading note, added motivation, system comparison, Q&A
  - `wiki/sources/shen-2023-advanced-anc.md` — merged with reading note, added math derivations, performance tables, Q&A
  - `wiki/sources/wang-2024-metric-learning-virtual-sensing.md` — merged with reading note, added AF-VS background, performance tables
  - `wiki/sources/holzmueller-2026-obs-tasnet-virtual-sensing.md` — merged with reading note, added RMT background, ablation study
  - `wiki/sources/toyooka-2026-hybrid-anc-remote-sensing.md` — merged with reading note, added NLMS equations, tuning stages
  - `wiki/synthesis/virtual-sensing-evolution.md` — updated references to use merged source slugs
  - `wiki/index.md` — removed 5 reading note entries, updated source summaries, stats (53→48 sources, 224→219 total)
- **Pages deleted**:
  - `wiki/sources/chen-2016-generalized-correntropy-paper-reading-note.md`
  - `wiki/sources/shen-2023-advanced-anc-reading-note.md`
  - `wiki/sources/wang-2024-metric-learning-virtual-sensing-reading-note.md`
  - `wiki/sources/holzmueller-2026-obs-tasnet-virtual-sensing-reading-note.md`
  - `wiki/sources/toyooka-2026-hybrid-anc-virtual-sensing-paper-reading-note.md`

---

## [2026-04-29] ingest | VM Beamforming for Hearing Aids (Farmani 2026)

- **Source**: `raw/papers/farmani-2026-virtual-mic-beamforming-hearing-aid/full-text.txt` (Zotero: 6EW3W6U6)
- **Authors**: Mojtaba Farmani, Svend Feldt, Jesper Jensen
- **Published**: ICASSP 2026, pp. 15552–15556
- **DOI**: 10.1109/ICASSP55912.2026.11462612
- **Summary**: Low-complexity VM synthesis via WDO-based RTF power model D_vm = D_2^λ. λ parameter controls interpolation (0<λ<1) and extrapolation (λ<0 or λ>1). Optimal λ=−4 for frontal targets. +3 dB ISNR over 2-mic baseline with single VM, +4 dB with two VMs. Outperforms GAI and Ext. GAI benchmarks across all SNR levels, noise types, and reverberation conditions.
- **Pages created**:
  - `raw/papers/farmani-2026-virtual-mic-beamforming-hearing-aid/full-text.txt` — extracted text from Zotero PDF
  - `wiki/sources/farmani-2026-virtual-mic-beamforming-hearing-aid.md`
  - `wiki/entities/mojtaba-farmani.md`
  - `wiki/entities/svend-feldt.md`
  - `wiki/entities/jesper-jensen.md`
- **Pages updated**:
  - `wiki/index.md` — added 3 entities, 1 source

---

## [2026-04-29] fix | Add 7 missing concept pages

- **Created concepts**:
  - `wiki/concepts/multi-channel-speech-enhancement.md` — MCSE overview with linear, data-driven, and hybrid approaches
  - `wiki/concepts/variable-span-linear-filter.md` — VSLF framework with controllable tradeoff; MWF/MVDR as special cases
  - `wiki/concepts/multi-channel-wiener-filter.md` — Optimal linear filter minimizing MSE; VSLF special case
  - `wiki/concepts/mvdr-beamformer.md` — Minimum variance distortionless response beamformer
  - `wiki/concepts/spatial-covariance-matrix.md` — Second-order statistics for multi-channel signals
  - `wiki/concepts/generalized-eigenvalue-decomposition.md` — Joint diagonalization for VSLF weight computation
  - `wiki/concepts/remote-microphone-technique.md` — Virtual sensing using fixed compensation filter
- **Pages updated**:
  - `wiki/index.md` — added 7 concepts, updated statistics (Concepts: 80→87, Total: 233→240)

---

## [2026-04-29] ingest | Neural Variable Span Filters for Speech Enhancement (Oviste 2026)

- **Source**: `raw/papers/oviste-2026-neural-vslf-speech-enhancement/full-text.txt` (Zotero: K2TY3FFD)
- **Authors**: Tom Oviste, Pejman Mowlaee, Javier Badajoz-Davila, Jesper Rindom Jensen, Mads Græsbøll Christensen
- **Published**: ICASSP 2026, pp. 20996–21000
- **DOI**: 10.1109/ICASSP55912.2026.11464002
- **Summary**: Proposes Hybrid Variable Span Filter (HVSF) architecture integrating VSLF framework into DNN-guided speech enhancement. DNN predicts clean-speech SCM, noise SCM, and tradeoff parameter μ to compute VSLF weights. Generalizes MWF/MVDR as special cases. Enables explicit control over speech distortion vs noise reduction tradeoff. 4-mic setup simulating true-wireless earbuds, 60k training pairs.
- **Pages created**:
  - `raw/papers/oviste-2026-neural-vslf-speech-enhancement/full-text.txt` — extracted text from Zotero PDF
  - `wiki/sources/oviste-2026-neural-vslf-speech-enhancement.md`
  - `wiki/entities/tom-oviste.md`
  - `wiki/entities/pejman-mowlaee.md`
  - `wiki/entities/javier-badajoz-davila.md`
  - `wiki/entities/jesper-rindom-jensen.md`
- **Pages updated**:
  - `wiki/index.md` — added 4 entities, 1 source

---

## [2026-04-29] merge | Synthesis page consolidation (5 groups, 12→7 pages)

- **Group A (Robust ANC)**: Merged `robust-anc-correntropy-to-gmcc.md` + `robust-anc-impulsive-non-stationary.md` → `impulsive-noise-control.md`
  - Added correntropy→MCC→GMCC theory, FxGMCC variants, design guidelines, AI-driven frontier
  - Updated title to "Robust ANC for Impulsive and Non-Gaussian Noise"
- **Group B (Computational Efficiency)**: Merged `computational-and-memory-efficiency.md` → `computational-efficiency-evolution.md`
  - Added RNN memory bottlenecks (BPTT vs FEP), 2026 efficiency frontier sections
- **Group C (Feedback ANC)**: Merged `feedback-anc-and-feedback-cancellation.md` + `adaptive-step-size-control-feedback-anc.md` → `feedback-anc-filter-design.md`
  - Added AFC comparison, step-size control hierarchy (3-layer), neural gain estimation, open problems
  - Updated decision tree with AFC and neural step-size options
- **Group D (Headphone ANC)**: Merged `head-mounted-anc-occlusion-transparency.md` → `modern-headphone-anc-systems.md`
  - Added occlusion-transparency conflict, open-ear ANC, multi-modal acoustic computing sections
- **Group E (IIR Fitting)**: Merged `parameterized-iir-curve-fitting-review.md` → `iir-filter-fitting-frequency-response.md`
  - Added Q&A section (3 questions on parameterized IIR vs alternatives)
- **Cross-references updated**: index.md, ai-driven-anc.md, virtual-sensing-evolution.md, robust-adaptive-filtering.md, feedback-anc.md, multimodal-bc-speech-enhancement.md, a-review-of-virtual-sensing-algorithms-for-active-.md
- **Statistics**: Synthesis 25→18, Total pages 240→233

---

## [2026-04-30] ingest | SCM Reconstruction for Speech Enhancement (Liu et al. 2026)

- **Source**: `raw/papers/liu-2026-scm-reconstruction-speech-enhancement/paper.pdf` (Zotero: 4RJXKQ8F)
- **Authors**: Wei Liu, Xueqin Luo, Jilu Jin, Gongping Huang, Jingdong Chen, Jacob Benesty, Shoji Makino
- **Published**: ICASSP 2026, pp. 15867–15871
- **DOI**: 10.1109/ICASSP55912.2026.11464924
- **Summary**: Online SCM reconstruction via variance ratio estimation with KL-regularized multiplicative update; R-MWF for multi-source reverberant speech enhancement
- **Extraction**: MineRU (pipeline backend) for PDF text and figures
- **Pages created**:
  - `wiki/sources/liu-2026-scm-reconstruction-speech-enhancement.md` — source page
  - `wiki/concepts/variance-ratio-estimation.md` — new concept: variance ratio estimation
  - `wiki/entities/wei-liu.md` — entity: Wei Liu
  - `wiki/entities/gongping-huang.md` — entity: Gongping Huang
  - `wiki/entities/jingdong-chen.md` — entity: Jingdong Chen
  - `wiki/entities/jacob-benesty.md` — entity: Jacob Benesty
  - `wiki/entities/shoji-makino.md` — entity: Shoji Makino
- **Pages updated**:
  - `wiki/concepts/spatial-covariance-matrix.md` — added SCM reconstruction via normalized decomposition section
  - `wiki/concepts/multi-channel-wiener-filter.md` — added R-MWF formulation section
  - `wiki/concepts/multi-channel-speech-enhancement.md` — added R-MWF to key techniques
  - `wiki/concepts/spatial-coherence.md` — added Liu 2026 reference
  - `wiki/index.md` — added 5 entities, 1 concept, 1 source; updated statistics

---

## [2026-04-30] ingest | Predictive Directional SFANC via CRNN (Wang et al. 2026)

- **Source**: `raw/papers/wang-2026-predictive-dsfanc-crnn/full-text.md` (Zotero: I6FHS99P, arXiv: 2604.23144)
- **Authors**: Boxiang Wang, Zhengding Luo, Dongyuan Shi, Junwei Ji, Xiruo Su, Woon-Seng Gan
- **Published**: Preprint, arXiv 2026
- **DOI**: 10.48550/arXiv.2604.23144
- **Summary**: CRNN-based PD-SFANC predicts next-frame DoA for proactive filter selection in moving source ANC; eliminates D-SFANC one-frame lag
- **Extraction**: Defuddle on arXiv HTML (2604.23144) + PDF from Zotero storage; 5 figures downloaded
- **Pages created**:
  - `wiki/sources/wang-2026-predictive-dsfanc-crnn.md` — source page
  - `wiki/concepts/selective-fixed-filter-anc.md` — new concept: SFANC variants (SFANC, D-SFANC, PD-SFANC, DFG-SFANC, GFANC)
  - `wiki/concepts/direction-of-arrival-estimation.md` — new concept: DoA estimation for ANC
  - `wiki/concepts/moving-source-tracking.md` — new concept: moving source tracking approaches
  - `wiki/entities/zhengding-luo.md` — entity: Zhengding Luo
  - `wiki/entities/xiruo-su.md` — entity: Xiruo Su
- **Pages updated**:
  - `wiki/entities/boxiang-wang.md` — added PD-SFANC contribution
  - `wiki/entities/dongyuan-shi.md` — added PD-SFANC contribution
  - `wiki/entities/junwei-ji.md` — added PD-SFANC contribution
  - `wiki/entities/woon-seng-gan.md` — added PD-SFANC contribution
  - `wiki/concepts/active-noise-control.md` — added PD-SFANC, SFANC, DoA, moving source tracking cross-refs
  - `wiki/concepts/convolutional-recurrent-network.md` — added DoA prediction application
  - `wiki/synthesis/ai-driven-anc.md` — added PD-SFANC to SFANC section
  - `wiki/index.md` — added 2 entities, 3 concepts, 1 source; updated statistics

---

## [2026-04-30] ingest | Directional SFANC in Reverberant Environments (Wang 2026)

- **Source**: \
aw/papers/wang-2026-directional-sfanc-reverberant/full-text.md\ (Zotero: 4V3ESJXQ)
- **Authors**: Boxiang Wang, Zhengding Luo, Haowen Li, Dongyuan Shi, Junwei Ji, Ziyi Yang, Woon-Seng Gan
- **Published**: arXiv preprint, 2026-01-11
- **DOI**: 10.48550/arXiv.2601.06981
- **Summary**: CNN-based directional SFANC with multi-task DoA estimation in reverberant environments; ~96% azimuth / ~91% elevation accuracy with 0.03M params; outperforms FxLMS, SFANC, GFANC
- **Pages created**:
  - \
aw/papers/wang-2026-directional-sfanc-reverberant/full-text.md\ — extracted from arXiv HTML via WebFetch
  - \wiki/sources/wang-2026-directional-sfanc-reverberant.md\
  - \wiki/entities/zhengding-luo.md\
  - \wiki/entities/haowen-li.md\
  - \wiki/entities/ziyi-yang.md\
- **Pages updated**:
  - \wiki/entities/boxiang-wang.md\ — added directional SFANC contribution
  - \wiki/concepts/selective-fixed-filter-anc.md\ — added source reference
  - \wiki/index.md\ — added 3 entities, 1 source; updated statistics

---

## [2026-05-01] ingest | Yin 2023: Selective Fixed-Filter ANC Based on Frequency Response Matching in Headphones

- **Source**: `raw/papers/yin-2023-selective-fixed-filter-anc-headphones/full-text.md` (Zotero: 0_4MBBAJXH)
- **Authors**: Lan Yin, Zeqiang Zhang, Ming Wu, Shuang Zhou, Jianfeng Guo, Jun Yang, Jianing Zhang
- **Published**: Applied Acoustics, Volume 211, August 2023
- **DOI**: 10.1016/j.apacoust.2023.109505
- **Summary**: FRM-SFANC algorithm using online frequency response matching for selective fixed-filter ANC in headphones; HMM theoretical framework; 12-21 dB NR; LayerCAM explainability shows CNN selects filters based on frequency band information
- **Pages created**:
  - `wiki/sources/yin-2023-selective-fixed-filter-anc-headphones.md` — source summary page
  - `wiki/entities/lan-yin.md` — lead author
  - `wiki/entities/zeqiang-zhang.md` — co-author
  - `wiki/entities/ming-wu.md` — co-author
  - `wiki/entities/shuang-zhou.md` — co-author
  - `wiki/entities/jianfeng-guo.md` — co-author
  - `wiki/entities/jun-yang.md` — co-author
  - `wiki/entities/jianing-zhang.md` — co-author
  - `wiki/concepts/frequency-response-matching.md` — FRM concept page
- **Pages updated**:
  - `wiki/concepts/selective-fixed-filter-anc.md` — added FRM-SFANC variant, comparison table row, concept/source references
  - `wiki/synthesis/ai-driven-anc.md` — added FRM-SFANC non-neural selection, efficiency table row, source reference
  - `wiki/index.md` — added 7 entities, 1 concept, 1 source

## [2026-05-02] ingest (re) | Directional SFANC Based on CNN in Reverberant Environments (Wang 2026)

- **Source**: `raw/papers/wang-2026-directional-sfanc-reverberant/full-text.md` (Zotero: 4V3ESJXQ)
- **Authors**: Boxiang Wang, Zhengding Luo, Haowen Li, Dongyuan Shi, Junwei Ji, Ziyi Yang, Woon-Seng Gan
- **Published**: arXiv preprint, 2026-01-11
- **DOI**: 10.48550/arXiv.2601.06981
- **Summary**: Re-ingested with Defuddle extraction from arXiv HTML; added 8 figures from arXiv; updated DoA estimation and SFANC concept pages with reverberant environment details
- **Pages updated**:
  - `raw/papers/wang-2026-directional-sfanc-reverberant/full-text.md` — re-extracted via Defuddle with figures
  - `raw/papers/wang-2026-directional-sfanc-reverberant/figures/` — 8 figures downloaded from arXiv HTML
  - `wiki/sources/wang-2026-directional-sfanc-reverberant.md` — updated date
  - `wiki/concepts/direction-of-arrival-estimation.md` — added CNN-based DoA in reverberant environments section, source reference
  - `wiki/concepts/selective-fixed-filter-anc.md` — added reverberant D-SFANC details, updated comparison table with Reverberant column

---

## [2026-05-02] ingest | Notes on Lagrange Interpolating Polynomials (Bendersky 2026)

- **Source**: `raw/articles/eli-2026-lagrange-interpolation/full-text.md`
- **Author**: Eli Bendersky
- **Published**: 2026
- **URL**: https://eli.thegreenplace.net/2026/notes-on-lagrange-interpolating-polynomials/
- **Summary**: Tutorial on Lagrange interpolation, uniqueness proof, vector space basis for P_n(R), and Vandermonde determinant derivation
- **Pages created**:
  - `raw/articles/eli-2026-lagrange-interpolation/full-text.md` — extracted via Defuddle
  - `raw/articles/eli-2026-lagrange-interpolation/figures/` — 3 figures downloaded
  - `wiki/sources/eli-2026-lagrange-interpolation.md` — source summary page
  - `wiki/entities/eli-bendersky.md` — author entity
  - `wiki/concepts/lagrange-interpolation.md` — Lagrange interpolation concept
  - `wiki/concepts/vandermonde-matrix.md` — Vandermonde matrix concept
- **Pages updated**:
  - `wiki/index.md` — added 1 entity, 2 concepts, 1 source

## [2026-05-02] ingest (re) | Neural Network Augmented Kalman Filter for AHS (Zhang 2024)

- **Source**: `raw/papers/zhang-2024-neural-kalman-howling/full-text.txt` (Zotero: T3GXM3RI)
- **Authors**: Yixuan Zhang, Hao Zhang, Meng Yu, Dong Yu
- **Published**: Interspeech 2024, pp. 1715–1719
- **DOI**: 10.21437/Interspeech.2024-166
- **Summary**: Re-ingested with pdftotext (PDF >10MB); updated source page with full FDKF equations, ablation results, and training strategy; created entity and concept pages
- **Pages created**:
  - `raw/papers/zhang-2024-neural-kalman-howling/full-text.txt` — extracted via pdftotext
  - `wiki/entities/yixuan-zhang.md` — lead author
  - `wiki/entities/hao-zhang.md` — co-author
  - `wiki/entities/meng-yu.md` — co-author
  - `wiki/entities/dong-yu.md` — co-author
  - `wiki/concepts/acoustic-howling-suppression.md` — AHS concept page
  - `wiki/concepts/frequency-domain-kalman-filter.md` — FDKF concept page
- **Pages updated**:
  - `wiki/sources/zhang-2024-neural-kalman-howling.md` — comprehensive rewrite with equations, ablation table, training strategy
  - `wiki/concepts/kalman-filter.md` — added FDKF variant, AHS cross-references, source reference
  - `wiki/index.md` — added 4 entities, 2 concepts

---

## [2026-05-03] ingest | Analysis of Momentum Adaptive Filtering Algorithms (Sharma 1998)

- **Source**: `raw/papers/sharma-1998-momentum-adaptive-filtering/full-text.md` (Zotero: SGFLZXZU)
- **Authors**: Rajesh Sharma, William A. Sethares, James A. Bucklew
- **Published**: IEEE Trans. Signal Process., Vol. 46, No. 5, pp. 1431–1434, May 1998
- **DOI**: 10.1109/78.668805
- **Summary**: Asymptotic analysis of MLMS using weak convergence and ODE method; almost sure convergence for all α∈(-1,1); Gaussian asymptotic distribution with β=1/(1-α) rate-misadjustment tradeoff; no input distribution assumptions
- **Extraction**: MinerU precision extract (VLM model, --formula --table) — initial PDF copy was corrupted (empty file), re-copied with correct Chinese filename
- **Pages created**:
  - `raw/papers/sharma-1998-momentum-adaptive-filtering/full-text.md` — extracted via MinerU precision extract
  - `wiki/sources/sharma-1998-momentum-adaptive-filtering.md` — source page
  - `wiki/entities/rajesh-sharma.md` — lead author
  - `wiki/entities/william-sethares.md` — co-author
  - `wiki/entities/james-bucklew.md` — co-author
  - `wiki/concepts/asymptotic-analysis-adaptive-algorithms.md` — ODE method and weak convergence for adaptive filters
- **Pages updated**:
  - `wiki/concepts/momentum-lms.md` — added Sharma 1998 asymptotic analysis section, source reference, concept cross-reference
  - `wiki/concepts/adaptive-filtering.md` — added Momentum LMS to algorithm table, cross-reference
  - `wiki/index.md` — added 3 entities, 1 concept, 1 source

---

## [2026-05-04] ingest | Transformer-based End-to-End Control Filter Generation for ANC (Yang 2026)

- **Source**: `raw/papers/yang-2026-transformer-e2e-cfg-anc/full-text.md` (Zotero: 5DHKAHI8)
- **Authors**: Ziyi Yang, Zhengding Luo, Yisong Zou, Boxiang Wang, Qirui Huang, Woon-Seng Gan
- **Published**: arXiv preprint, arXiv:2605.00494, 2026
- **DOI**: 10.48550/arXiv.2605.00494
- **Summary**: Transformer co-processor directly generates ANC control filters in a fully differentiable system trained unsupervised on residual error; 18.36 dB avg NR on unseen real noises vs. 16.63 dB GFANC and 11.13 dB FxNLMS
- **Extraction**: MinerU extract (VLM model, --formula --table), images renamed to figures
- **Pages created**:
  - `raw/papers/yang-2026-transformer-e2e-cfg-anc/full-text.md` — extracted via MinerU extract
  - `wiki/sources/yang-2026-transformer-e2e-cfg-anc.md` — source page
  - `wiki/entities/yisong-zou.md` — new author entity
  - `wiki/entities/qirui-huang.md` — new author entity
  - `wiki/concepts/generative-fixed-filter-anc.md` — GFANC and E2E-CFG concept
  - `wiki/concepts/end-to-end-differentiable-anc.md` — differentiable ANC training paradigm
- **Pages updated**:
  - `wiki/entities/ziyi-yang.md` — added E2E-CFG contribution
  - `wiki/entities/zhengding-luo.md` — added E2E-CFG contribution
  - `wiki/entities/boxiang-wang.md` — added E2E-CFG contribution
  - `wiki/entities/woon-seng-gan.md` — added E2E-CFG contribution
  - `wiki/concepts/active-noise-control.md` — added E2E-CFG to deep learning approaches, cross-references
  - `wiki/concepts/selective-fixed-filter-anc.md` — added E2E-CFG variant, GFANC/E2E-CFG cross-references
  - `wiki/index.md` — added 2 entities, 2 concepts, 1 source

---

## [2026-05-05] ingest | Causality Study on Feedforward ANC Headset (Zhang & Qiu 2014)

- **Source**: `raw/papers/zhang-2014-causality-feedforward-anc-headset/full-text.md` (Zotero: 65C4ZVGB)
- **Authors**: Limin Zhang, Xiaojun Qiu
- **Published**: Applied Acoustics, Vol. 80, pp. 36–44, 2014
- **DOI**: 10.1016/j.apacoust.2014.01.004
- **Summary**: Systematic analysis of direction-dependent causality in feedforward ANC headsets; shows headset is causal at 0° but non-causal at 90°, with both narrowed attenuation bandwidth and reduced max NR; Wiener-filter-based prediction method validated in anechoic and reverberant chambers
- **Extraction**: MinerU extract (VLM model, --formula --table), images renamed to figures
- **Pages created**:
  - `raw/papers/zhang-2014-causality-feedforward-anc-headset/full-text.md` — extracted via MinerU extract
  - `wiki/sources/zhang-2014-causality-feedforward-anc-headset.md` — source page
  - `wiki/entities/limin-zhang.md` — new author entity
- **Pages updated**:
  - `wiki/entities/xiaojun-qiu.md` — added Zhang 2014 as co-author
  - `wiki/concepts/causality.md` — added direction-dependent causality section, Zhang 2014 findings
  - `wiki/concepts/feedforward-anc.md` — added direction-dependent causality reference
  - `wiki/concepts/selective-fixed-filter-anc.md` — added Zhang 2014 as foundational work for D-SFANC
  - `wiki/concepts/direction-of-arrival-estimation.md` — added Zhang 2014 as motivation for direction-aware ANC
  - `wiki/index.md` — added 1 entity, 1 source

---

## [2026-05-05] ingest | Direction-of-Arrival Dependency of ANC Headphones (Liebich et al. 2018)

- **Source**: `raw/papers/liebich-2018-doa-dependency-anc-headphones/full-text.md` (Zotero: T9JAV2ND)
- **Authors**: Stefan Liebich, Jan-Gerrit Richter, Johannes Fabry, Christopher Durand, Janina Fels, Peter Jax
- **Published**: ASME 2018 Noise Control and Acoustics Division Session at INTERNOISE 2018
- **DOI**: 10.1115/NCAD2018-6120
- **Summary**: DHRTF measurements on in-ear headphones across 4608 directions show primary path DOA-dependent above 200 Hz; feedforward ANC is DOA-dependent, feedback ANC is DOA-independent; novel analytical bound shows 20 dB attenuation requires <0.83 dB amplitude and <5.76° phase accuracy
- **Extraction**: MinerU extract (VLM model, --formula --table), images renamed to figures
- **Pages created**:
  - `raw/papers/liebich-2018-doa-dependency-anc-headphones/full-text.md` — extracted via MinerU extract
  - `wiki/sources/liebich-2018-doa-dependency-anc-headphones.md` — source page
  - `wiki/entities/stefan-liebich.md` — first author
  - `wiki/entities/jan-gerrit-richter.md` — co-author (ITA RWTH Aachen)
  - `wiki/entities/johannes-fabry.md` — co-author (IKS RWTH Aachen)
  - `wiki/entities/christopher-durand.md` — co-author (IKS RWTH Aachen)
  - `wiki/entities/janina-fels.md` — co-author, professor at ITA RWTH Aachen
  - `wiki/concepts/device-specific-hrtf.md` — DHRTF concept
  - `wiki/concepts/primary-path-variability.md` — DOA-induced primary path changes
  - `wiki/concepts/anc-attenuation-bounds.md` — analytical attenuation limits
- **Pages updated**:
  - `wiki/entities/peter-jax.md` — added Liebich 2018 as co-author, added Stefan Liebich as related entity
  - `wiki/concepts/feedforward-anc.md` — added DOA dependency section
  - `wiki/concepts/feedback-anc.md` — added DOA independence section
  - `wiki/concepts/hybrid-anc.md` — added DOA robustness section
  - `wiki/concepts/active-noise-control.md` — added DOA dependency as key challenge
  - `wiki/index.md` — added 5 entities, 3 concepts, 1 source

---

## [2026-05-05] ingest | Blind Direction-Dependent Acoustic Parameter Estimation Using Smart Glasses (Görtz et al. 2026)

- **Source**: `raw/papers/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation/full-text.md` (Zotero: H3HVNSBS)
- **Authors**: Philipp Görtz, Sebastià V. Amengual, Paul Calamia, Ishwarya Ananthabhotla, Andrew Francl, Carl Schissler, Emanuele A. P. Habets
- **Published**: ICASSP 2026, pp. 22187–22191
- **DOI**: 10.1109/ICASSP55912.2026.11460445
- **Summary**: First multimodal method for blind direction-dependent acoustic parameter estimation using smart glasses; dual-network architecture (conv encoder + FiLM-conditioned transformer) exploits head rotations to overcome compact array spatial resolution limits; PCC 0.82 for T₂₀ and 0.92 for E at 0.5 kHz
- **Extraction**: MinerU extract (VLM model, --formula --table), images renamed to figures
- **Pages created**:
  - `raw/papers/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation/full-text.md` — extracted via MinerU extract
  - `wiki/sources/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation.md` — source page
  - `wiki/entities/philipp-goetz.md` — first author (FAU Erlangen-Nuremberg)
  - `wiki/entities/sebastia-amengual.md` — co-author (Meta Reality Labs)
  - `wiki/entities/paul-calamia.md` — co-author (Meta Reality Labs)
  - `wiki/entities/andrew-francl.md` — co-author (Meta Reality Labs)
  - `wiki/entities/carl-schissler.md` — co-author (Meta Reality Labs)
  - `wiki/entities/emanuele-habets.md` — co-author (FAU Erlangen-Nuremberg)
  - `wiki/concepts/direction-dependent-acoustic-parameters.md` — DDAP concept
  - `wiki/concepts/spherical-harmonic-transform.md` — SHT concept
  - `wiki/concepts/auditory-augmented-reality.md` — AAR concept
- **Pages updated**:
  - `wiki/entities/ishwarya-ananthabhotla.md` — added Görtz 2026 co-authorship
  - `wiki/concepts/beamforming.md` — added max-rE beamformer section, DDAP cross-reference
  - `wiki/concepts/head-orientation-from-imu.md` — added DDAP estimation application, source reference
  - `wiki/concepts/direction-of-arrival-estimation.md` — added DDAP cross-reference, source reference
  - `wiki/index.md` — added 6 entities, 3 concepts, 1 source; updated statistics (98→105 entities, 97→100 concepts, 57→58 sources, 276→286 total)

---

## [2026-05-06] ingest | Dynamic Time Warping for Secondary Path Interpolation in Local ANC (Holzmüller & Sontacchi 2026)

- **Source**: `raw/papers/holzmuller-2026-dtw-secondary-path-anc/full-text.md` (Zotero: ZV3BCM38)
- **Authors**: Felix Holzmüller, Alois Sontacchi
- **Published**: IEEE Open Journal of Signal Processing, 2026, pp. 1–10
- **DOI**: 10.1109/OJSP.2026.3689448
- **Summary**: DTW-based interpolation of secondary path filter coefficients for local ANC with moving listeners; achieves −17.65 dB system mismatch vs 2.49 dB for nearest-neighbor at 15 cm spacing, extending stable bandwidth to ~7.7 kHz
- **Extraction**: MinerU (VLM backend) for PDF text, formulas, tables, and figures
- **Pages created**:
  - `raw/papers/holzmuller-2026-dtw-secondary-path-anc/full-text.md` — extracted text from Zotero PDF
  - `wiki/sources/holzmuller-2026-dtw-secondary-path-anc.md` — source page
  - `wiki/concepts/dynamic-time-warping.md` — new concept: Dynamic Time Warping
  - `wiki/concepts/secondary-path-interpolation.md` — new concept: Secondary Path Interpolation
- **Pages updated**:
  - `wiki/entities/felix-holzmueller.md` — added DTW paper contribution, updated affiliation
  - `wiki/entities/alois-sontacchi.md` — added DTW paper contribution, updated affiliation
  - `wiki/concepts/secondary-path-modeling.md` — added secondary path interpolation section and cross-references
  - `wiki/concepts/active-noise-control.md` — added moving listeners challenge and cross-references
  - `wiki/concepts/filtered-x-lms-algorithm.md` — added MIMO stability criterion and cross-references
  - `wiki/index.md` — added 2 concepts, 1 source; updated entity summaries

---

## [2026-05-06] ingest | BCS-Guided Speech Enhancement for Voice Assistant on Earbuds (Heitkaemper et al. 2026)

- **Source**: `raw/patents/us20260073929a1/full-text.md` (Zotero: Q833LYDX)
- **Inventors**: Jens Heitkaemper, Joseph Peter Caroselli Jr., Max McKinnon, Arun Narayanan, Nathan David Howard
- **Assignee**: Google LLC
- **Published**: US Patent Application US20260073929A1, 2026-03-12
- **URL**: https://patents.google.com/patent/US20260073929A1/en
- **Summary**: Conformer-based fusion of upscaled BCS + air-conducted STFT for earbud speech enhancement; ratio mask estimation; VAD-gated ASR; mic-agnostic design
- **Extraction**: WebFetch from Google Patents
- **Pages created**:
  - `raw/patents/us20260073929a1/full-text.md` — extracted patent text
  - `wiki/sources/heitkaemper-2026-bcs-speech-enhancement-earbuds.md` — source page
  - `wiki/entities/jens-heitkaemper.md` — entity: Jens Heitkaemper
  - `wiki/entities/joseph-caroselli-jr.md` — entity: Joseph Peter Caroselli Jr.
  - `wiki/entities/max-mckinnon.md` — entity: Max McKinnon
  - `wiki/entities/arun-narayanan.md` — entity: Arun Narayanan
  - `wiki/entities/nathan-howard.md` — entity: Nathan David Howard
  - `wiki/concepts/bcs-guided-speech-enhancement.md` — new concept: BCS-Guided Speech Enhancement
- **Pages updated**:
  - `wiki/concepts/bone-conduction.md` — added BCS-guided speech enhancement section and cross-references
  - `wiki/concepts/voice-activity-detection.md` — added BCS-gated speech enhancement application and cross-references
  - `wiki/synthesis/multimodal-bc-speech-enhancement.md` — added Conformer-based fusion era section and cross-references
  - `wiki/index.md` — added 5 entities, 1 concept, 1 source; updated synthesis summary
  - `wiki/entities/index.md` — added 5 entity entries
  - `wiki/concepts/index.md` — added 1 concept entry
  - `wiki/sources/index.md` — added 1 source entry

---

## [2026-05-07] ingest | Adaptive Diagonal Loading for Norm Constrained Beamforming (Mittal et al. 2026)

- **Source**: `raw/papers/mittal-2026-adaptive-diagonal-loading-beamforming/full-text.md` (Zotero: KQQNX9WS)
- **Authors**: Manan Mittal, Ryan M. Corey, John R. Buck, Andrew C. Singer
- **Published**: arXiv preprint arXiv:2605.04342, 2026-05-05
- **URL**: https://arxiv.org/abs/2605.04342
- **Summary**: WNG-constrained adaptive diagonal loading for MPDR/MVDR beamformers using the Kantorovich inequality to map desired WNG to a strict condition number bound. Three scalable estimation modes: Trace O(M), Gershgorin O(M²), Exact EVD O(M³). Outperforms Cox post-hoc scaling in SINR across all snapshot regimes.
- **Pages created**:
  - `wiki/sources/mittal-2026-adaptive-diagonal-loading-beamforming.md` — source page with full methodology, results, and contributions
  - `wiki/entities/manan-mittal.md` — entity: Manan Mittal (UIUC)
  - `wiki/entities/ryan-corey.md` — entity: Ryan M. Corey (UIUC)
  - `wiki/entities/john-buck.md` — entity: John R. Buck (UIUC)
  - `wiki/entities/andrew-singer.md` — entity: Andrew C. Singer (UIUC)
  - `wiki/concepts/diagonal-loading.md` — new concept: classical and adaptive diagonal loading
  - `wiki/concepts/kantorovich-inequality.md` — new concept: Kantorovich inequality and its beamforming application
  - `wiki/concepts/white-noise-gain.md` — new concept: WNG as beamformer robustness metric
  - `wiki/concepts/mpdr-beamformer.md` — new concept: MPDR beamformer formulation and properties
  - `wiki/concepts/gsc-beamformer.md` — new concept: GSC structure and orthogonality
  - `wiki/concepts/condition-number.md` — new concept: condition number and its role in WNG bounding
  - `wiki/concepts/gershgorin-circle-theorem.md` — new concept: Gershgorin disc bounds for eigenvalue estimation
- **Pages updated**:
  - `wiki/concepts/beamforming.md` — added MPDR beamformer, robustness and diagonal loading section with Kantorovich-based method
  - `wiki/concepts/mvdr-beamformer.md` — added diagonal loading robustness section, cross-references to new concepts
  - `wiki/concepts/spatial-covariance-matrix.md` — added condition number and snapshot deficiency discussion, diagonal loading cross-reference
  - `wiki/concepts/generalized-eigenvalue-decomposition.md` — added EVD-based diagonal loading mode, complexity comparison
  - `wiki/index.md` — added 4 entities, 7 concepts, 1 source; updated statistics
  - `wiki/entities/index.md` — added 4 entity entries
  - `wiki/concepts/index.md` — added 7 concept entries
  - `wiki/sources/index.md` — added 1 source entry

---

## [2026-05-12] ingest | Spatial-Magnifier: Spatial Upsampling for Multichannel Speech Enhancement (Lee et al. 2026)

- **Source**: `raw/papers/lee-2026-spatial-magnifier-spatial-upsampling/full-text.md` (Zotero: KC7HJ7T3)
- **Authors**: Dongheon Lee, Ashutosh Pandey, Sanjeel Parekh, Daniel Wong, Jacob Donley, Buye Xu, Juan Azcarreta
- **Published**: arXiv preprint, 2026-05-06
- **DOI**: 10.48550/arXiv.2605.04749
- **Summary**: GAN-based Spatial-Magnifier network generates virtual microphone signals from limited real microphones; SARL framework conditions downstream MC-SE on VM signals/features; nearly recovers oracle 6ch performance from 2ch with ~10× fewer params than baselines
- **Pages created**:
  - `raw/papers/lee-2026-spatial-magnifier-spatial-upsampling/full-text.md` — extracted text from arXiv HTML via Defuddle
  - `raw/papers/lee-2026-spatial-magnifier-spatial-upsampling/figures/fig1-spatial-magnifier.png` — generator architecture
  - `raw/papers/lee-2026-spatial-magnifier-spatial-upsampling/figures/fig2-sarl-framework.png` — SARL framework
  - `wiki/sources/lee-2026-spatial-magnifier-spatial-upsampling.md` — source page
  - `wiki/entities/dongheon-lee.md` — first author (Meta Reality Labs / KAIST)
  - `wiki/entities/ashutosh-pandey.md` — co-author (Meta Reality Labs)
  - `wiki/entities/sanjeel-parekh.md` — co-author (Meta Reality Labs)
  - `wiki/entities/daniel-wong.md` — co-author (Meta Reality Labs)
  - `wiki/entities/jacob-donley.md` — co-author (Meta Reality Labs)
  - `wiki/entities/juan-azcarreta.md` — co-author (Meta Reality Labs)
  - `wiki/concepts/virtual-microphone-estimation.md` — Neural-VME concept
  - `wiki/concepts/spatial-audio-representation-learning.md` — SARL concept
- **Pages updated**:
  - `wiki/entities/buye-xu.md` — added Spatial-Magnifier contribution
  - `wiki/concepts/multi-channel-speech-enhancement.md` — added Neural-VME and SARL techniques, cross-references
  - `wiki/concepts/spatial-covariance-matrix.md` — added VME cross-reference, source
  - `wiki/concepts/mvdr-beamformer.md` — added source reference
  - `wiki/index.md` — added 6 entities, 2 concepts, 1 source
  - `wiki/synthesis/index.md` — updated multimodal BC summary

---

## [2026-05-13] lint | Index rebuild

- **Index consistency rebuild**:
  - **wiki/index.md**: Added 15 missing entities, 11 missing concepts, 3 missing sources; removed 1 duplicate entity (zhengding-luo); updated statistics (123→147 entities, 119→135 concepts, 62→67 sources, 18→22 synthesis, 324→377 total)
  - **wiki/entities/index.md**: Added 15 missing entity entries; removed 1 duplicate (zhengding-luo); now 147 rows matching 147 files
  - **wiki/concepts/index.md**: Added 11 missing concept entries; removed 2 duplicates (dynamic-time-warping, secondary-path-interpolation); now 135 rows matching 135 files
  - **wiki/sources/index.md**: Added 3 missing source entries; now 67 rows matching 67 files
- **Missing entries added**:
  - **Entities**: ali-aroudi, anjali-menon, bastiaan-kleijn, buye-xu, calvin-murdock, diego-caviedes-nozal, ishwarya-ananthabhotla, lei-guo, liang-xu, longfei-yan, morteza-khaleghimeybodi, payal-mohapatra, rasmus-kongsgaard-olsson, xin-zheng, yifei-jin
  - **Concepts**: acoustic-zones-of-interest, diffusion-models-for-speech, drifting-models, dynamic-time-warping, head-orientation-from-imu, inertial-measurement-unit, momentum-lms, one-step-generative-models, online-learning, secondary-path-interpolation, self-supervised-speech-representation
  - **Sources**: jin-2026-momentum-lms-nonstationarity, mohapatra-2026-localizing-conversation-partners-head-motion, xu-2026-drifting-models-speech-enhancement
- **Duplicates removed**: zhengding-luo (entities), dynamic-time-warping (concepts), secondary-path-interpolation (concepts)
- **All indexes now fully synchronized with actual page counts**

---

## [2026-05-13] ingest | Feedback ANC via Constrained Optimization for Headphones (Seo 2016)

- **Source**: `raw/papers/seo-2016-feedback-anc-constrained-optimization/full-text.md` (Zotero: 926LI9YV)
- **Authors**: Ji-ho Seo, Young-cheol Park, Dae Hee Youn
- **Published**: 2016 IEEE ICCE-Asia, pp. 1–4
- **DOI**: 10.1109/ICCE-Asia.2016.7804751
- **Summary**: Low-order WFIR filter design via Q-parameterization + frequency warping; 16th order matches 128th FIR at <1kHz
- **Pages created**:
  - `raw/papers/seo-2016-feedback-anc-constrained-optimization/full-text.md` — extracted text from Zotero PDF via MinerU
  - `wiki/sources/seo-2016-feedback-anc-constrained-optimization.md`
  - `wiki/entities/ji-ho-seo.md`
  - `wiki/entities/young-cheol-park.md`
  - `wiki/entities/dae-hee-youn.md`
  - `wiki/concepts/frequency-warping.md`
  - `wiki/concepts/warped-fir-filter.md`
  - `wiki/concepts/q-parameterization.md`
  - `wiki/concepts/sensitivity-function.md`
- **Pages updated**:
  - `wiki/concepts/feedback-anc.md` — added Seo 2016 section, source reference
  - `wiki/index.md` — added 3 entities, 4 concepts, 1 source; updated statistics (147→150 entities, 135→139 concepts, 67→68 sources, 377→385 total)
  - `wiki/entities/index.md` — added 3 entity entries
  - `wiki/concepts/index.md` — added 4 concept entries
  - `wiki/sources/index.md` — added 1 source entry

---

## [2026-05-13] lint | Health check

- **Index consistency**:
  - **wiki/index.md**: 133 entity rows (actual: 147, missing 14), 124 concept rows (actual: 135, missing 11), 64 source rows (actual: 67, missing 3)
  - **wiki/entities/index.md**: 133 rows (actual: 147, missing 14)
  - **wiki/concepts/index.md**: 126 rows (actual: 135, missing 9)
  - **wiki/sources/index.md**: 64 rows (actual: 67, missing 3)
  - **Statistics in wiki/index.md**: reports 123 entities, 119 concepts, 62 sources, 324 total — all stale (actual: 147 entities, 135 concepts, 67 sources, 18 synthesis, 6 queries = 373 total)
- **Missing from wiki/index.md entities table** (14): ali-aroudi, anjali-menon, bastiaan-kleijn, buye-xu, calvin-murdock, christopher-durand, diego-caviedes-nozal, ishwarya-ananthabhotla, james-bucklew, jan-gerrit-richter, johannes-fabry, lei-guo, liang-xu, limin-zhang, longfei-yan, morteza-khaleghimeybodi, payal-mohapatra, qirui-huang, rajesh-sharma, rasmus-kongsgaard-olsson, stefan-liebich, william-sethares, xin-zheng, yifei-jin, yisong-zou
- **Missing from wiki/index.md concepts table** (11): acoustic-zones-of-interest, diffusion-models-for-speech, drifting-models, dynamic-time-warping, head-orientation-from-imu, inertial-measurement-unit, momentum-lms, one-step-generative-models, online-learning, secondary-path-interpolation, self-supervised-speech-representation
- **Missing from wiki/index.md sources table** (3): jin-2026-momentum-lms-nonstationarity, mohapatra-2026-localizing-conversation-partners-head-motion, xu-2026-drifting-models-speech-enhancement
- **Broken wikilinks**: 1 (concepts/concept-name in llm-wiki-best-practices.md — template example, not a real broken link)
- **Orphan pages**: 363 pages have no inbound wikilinks (expected for a wiki where most pages are linked only from index files)
- **Contradictions**: None detected
- **Stale claims**: None detected
- **Action needed**: The index files (wiki/index.md, wiki/entities/index.md, wiki/concepts/index.md, wiki/sources/index.md) are significantly out of sync with actual page counts. A full index rebuild is recommended.

---

## [2026-05-13] ingest | NDF+: joint neural directional filtering and diffuse sound extraction (Huang et al. 2026)

- **Source**: `raw/papers/huang-2026-ndf-joint-neural-directional-filtering/full-text.md` (Zotero: BVBAGBIJ)
- **Authors**: Weilong Huang, Le Nhat Tam Huynh, Oliver Thiergart, Emanuël A. P. Habets
- **Published**: arXiv preprint arXiv:2605.06108v1, 2026-05-07
- **URL**: https://arxiv.org/abs/2605.06108v1
- **Summary**: NDF+ extends neural directional filtering to jointly perform dereverberated VDM reconstruction and diffuse sound extraction via a dual-mask architecture, enabling explicit control over diffuse components for applications like controllable stereo recording.
- **Pages created**:
  - `wiki/sources/huang-2026-ndf-joint-neural-directional-filtering.md` — source page with full methodology, results, and contributions
  - `wiki/entities/weilong-huang.md` — entity: Weilong Huang (FAU)
  - `wiki/entities/le-nhat-tam-huynh.md` — entity: Le Nhat Tam Huynh (FAU)
  - `wiki/entities/oliver-thiergart.md` — entity: Oliver Thiergart (FAU)
  - `wiki/concepts/neural-directional-filtering.md` — NDF concept: data-driven VDM reconstruction
  - `wiki/concepts/virtual-directional-microphone.md` — VDM concept: synthesized directional microphone
  - `wiki/concepts/diffuse-sound-extraction.md` — diffuse sound extraction concept
  - `wiki/concepts/directivity-pattern.md` — directivity pattern concept
  - `wiki/concepts/fixed-beamformer.md` — fixed beamformer concept
  - `wiki/concepts/differential-microphone-array.md` — DMA concept
  - `wiki/concepts/room-transfer-function.md` — RTF concept
  - `wiki/concepts/room-impulse-response.md` — RIR concept
  - `wiki/concepts/joint-nonlinear-filtering.md` — JNF/FT-JNF concept
- **Pages updated**:
  - `wiki/entities/emanuele-habets.md` — added NDF+ contribution and source reference
  - `wiki/index.md` — added 3 entities, 9 concepts, 1 source; updated statistics (120→123 entities, 110→119 concepts, 61→62 sources, 314→324 total)
  - `wiki/entities/index.md` — added 3 entity entries
  - `wiki/concepts/index.md` — added 9 concept entries
  - `wiki/sources/index.md` — added 1 source entry

---

## [2026-05-15] ingest | Hybrid AHS: A Hybrid of Kalman Filter and Deep Learning for Acoustic Howling Suppression (Zhang et al. 2023)

- **Source**: 
aw/papers/zhang-2023-hybrid-ahs/full-text.txt (Zotero: ILJW385X)
- **Authors**: Hao Zhang, Meng Yu, Yuzhong Wu, Tao Yu, Dong Yu
- **Published**: arXiv preprint arXiv:2305.02583, 2023-05-04
- **DOI**: 10.48550/arXiv.2305.02583
- **Summary**: Hybrid AHS cascades a frequency-domain Kalman filter with a self-attentive recurrent neural network, using teacher-forced training plus Kalman-preprocessed inputs to reduce training-inference mismatch and outperform Kalman, Deep AHS, and Deep MFC in both offline and streaming AHS.
- **Pages created**:
  - 
aw/papers/zhang-2023-hybrid-ahs/full-text.txt — extracted via pdftotext from Zotero PDF
  - wiki/sources/zhang-2023-hybrid-ahs.md — source page
  - wiki/entities/yuzhong-wu.md — co-author
  - wiki/entities/tao-yu.md — co-author
  - wiki/concepts/teacher-forcing.md — training strategy for recursive AHS models
  - wiki/concepts/self-attentive-recurrent-neural-network.md — Hybrid AHS neural backbone
- **Pages updated**:
  - wiki/entities/hao-zhang.md — added Hybrid AHS contribution
  - wiki/entities/meng-yu.md — added Hybrid AHS contribution
  - wiki/entities/dong-yu.md — added Hybrid AHS contribution
  - wiki/concepts/acoustic-howling-suppression.md — added HybridAHS method and source links
  - wiki/concepts/frequency-domain-kalman-filter.md — added hybrid FDKF usage
  - wiki/concepts/kalman-filter.md — added source reference
  - wiki/index.md — added 2 entities, 2 concepts, 1 source

---

## [2026-05-15] ingest | Zhan et al. (2025) DeepPEM-AFC

- **Source**: Zotero key BPH79CM5
- **DOI**: 10.1109/ICASSP49660.2025.10890348
- **Summary**: DeepPEM-AFC combines PEM de-correlation with GRU-based step-size prediction for hearing aid AFC. Frequency-domain PEM reduces complexity. Simulated path generation improves generalization. FS+DeepPEM-AFC achieves optimal performance across all speech quality metrics.
- **Pages created**:
  - `raw/papers/zhan-2025-deeppem-afc/full-text.txt` — extracted via pdftotext from Zotero PDF
  - `wiki/sources/zhan-2025-deeppem-afc.md` — source page
  - `wiki/entities/xiaofan-zhan.md` — first author
  - `wiki/entities/fengyuan-hao.md` — co-author
  - `wiki/entities/xiaodong-li.md` — co-author
  - `wiki/entities/chengshi-zheng.md` — corresponding author
  - `wiki/concepts/prediction-error-method.md` — PEM de-correlation technique
  - `wiki/concepts/hearing-aid-feedback-cancellation.md` — hearing aid AFC overview
  - `wiki/concepts/frequency-shift-feedback-cancellation.md` — FS de-correlation method
  - `wiki/concepts/maximum-stable-gain.md` — MSG metric for hearing aids
- **Pages updated**:
  - `wiki/concepts/acoustic-feedback.md` — added DeepPEM-AFC, cross-links, entities
  - `wiki/concepts/adaptive-feedback-control.md` — added hearing aid AFC cross-links
  - `wiki/concepts/deep-learning-for-signal-processing.md` — added DeepPEM-AFC application
  - `wiki/index.md` — added 4 entities, 4 concepts, 1 source

---

## [2026-05-16] lint | Health check

- **Index consistency**: Found 6 entities, 6 concepts, 2 sources missing from main index; 4 synthesis pages over-counted in statistics (had 22 indexed, 18 actual). All gaps fixed.
- **Broken links**: None detected
- **Orphan pages**: N/A (all pages linked from index)
- **Statistics**: Updated from 398/156/144/70/22 to 408/162/150/72/18
- **Actions taken**: Added 14 missing index rows (6 entities, 6 concepts, 2 sources); corrected synthesis count; updated statistics.

---

## [2026-05-16] ingest | He et al. (2025) VibOmni

- **Source**: `raw/papers/he-2025-vibomni/full-text.md` (Zotero: M9GHH9GT)
- **Authors**: Lixing He, Yunqi Guo, Haozheng Hou, Zhenyu Yan
- **Published**: arXiv preprint, 2025-12-02 (submitted to IEEE TMC)
- **DOI**: 10.48550/arXiv.2512.02515
- **Summary**: Multi-modal speech enhancement for earables using IMU bone-conducted vibration. Two-branch DPRNN fuses audio + vibration. BCF data augmentation reduces paired data need by >72x. Multi-modal SNR estimator enables continual learning and adaptive inference. 21% PESQ, 26% SNR improvement, ~40% WER reduction, 31x lower latency than baselines.
- **Pages created**:
  - `raw/papers/he-2025-vibomni/full-text.md` — extracted via Defuddle from arXiv HTML
  - `raw/papers/he-2025-vibomni/figures/` — 24 figures downloaded from arXiv HTML
  - `wiki/sources/he-2025-vibomni.md` — source page
  - `wiki/entities/lixing-he.md` — first author
  - `wiki/entities/yunqi-guo.md` — co-author
  - `wiki/entities/haozheng-hou.md` — co-author
  - `wiki/entities/zhenyu-yan.md` — corresponding author
  - `wiki/concepts/bone-conduction-function.md` — BCF concept
  - `wiki/concepts/dprnn.md` — Dual-Path RNN concept
- **Pages updated**:
  - `wiki/concepts/bone-conduction.md` — added multi-modal SE (VibOmni) section
  - `wiki/concepts/bcs-guided-speech-enhancement.md` — added BCF, DPRNN cross-refs, source link
  - `wiki/concepts/inertial-measurement-unit.md` — added IMU for bone-conduction vibration sensing section
  - `wiki/synthesis/multimodal-bc-speech-enhancement.md` — added Lightweight Multi-Modal Fusion era, VibOmni details
  - `wiki/index.md` — added 4 entities, 2 concepts, 1 source; updated statistics

---

## [2026-05-16] ingest | Kuang, Yang & Yang (2024) Lightweight SE Fusing BC/AC

- **Source**: `raw/papers/kuang-2024-lightweight-speech-enhancement-bone-air/full-text.md` (Zotero: VBVTU72Z)
- **Authors**: Kelan Kuang, Feiran Yang, Jun Yang
- **Published**: JASA 2024, Vol. 156(2), pp. 1355–1366
- **DOI**: 10.1121/10.0028339
- **Summary**: Lightweight DenGCAN model fusing BC and AC speech via iAFF, dense blocks, AG skip-connections, and sConformer bottleneck. 1.03M params, 0.859 GMACs, 1.870 wb-PESQ improvement on A4BS dataset (109 speakers, 4 BC positions). Lowest RTF (0.649 ARM, 0.068 x86) among competitive models.
- **Pages created**:
  - `raw/papers/kuang-2024-lightweight-speech-enhancement-bone-air/full-text.md` — extracted via MinerU from Zotero PDF
  - `wiki/sources/kuang-2024-lightweight-speech-enhancement-bone-air.md`
  - `wiki/entities/kelan-kuang.md`
  - `wiki/entities/feiran-yang.md`
  - `wiki/concepts/densely-gated-convolutional-attention-network.md`
  - `wiki/concepts/iterative-attentional-feature-fusion.md`
  - `wiki/concepts/attention-gate.md`
- **Pages updated**:
  - `wiki/entities/jun-yang.md` — added this paper to contributions
  - `wiki/concepts/bone-conduction.md` — added source reference
  - `wiki/concepts/bcs-guided-speech-enhancement.md` — added cross-refs and source link
  - `wiki/synthesis/multimodal-bc-speech-enhancement.md` — added Lightweight T-F Domain Fusion (2024) section
  - `wiki/index.md` — added 2 entities, 3 concepts, 1 source; updated statistics

---

## [2026-05-16] ingest | Liu, Chen & Yin 2025 ATFA Robust BC/AC Fusion

- **Source**: `raw/papers/liu-2025-robust-fusion-bc-ac-attention/full-text.md`  (ICASSP 2025, DOI 10.1109/ICASSP49660.2025.10888094)
- **Pages created**:
  - `wiki/sources/liu-2025-robust-fusion-bc-ac-attention.md` -- full source page
  - `wiki/entities/zhenglong-liu.md` (lead author, Dalian Univ. of Technology)
  - `wiki/entities/zhe-chen.md` (corresponding author)
  - `wiki/entities/fuliang-yin.md` (co-author)
  - `wiki/concepts/adaptive-time-frequency-attention.md` -- dual-axis MHSA over T and F + AHA module
  - `wiki/concepts/sensor-failure-robust-fusion.md` -- random modality dropout + dual-mask architecture
- **Pages updated**:
  - `wiki/concepts/bcs-guided-speech-enhancement.md` -- comparison table now lists DenGCAN, ATFA Dual-Mask, VibOmni; new robustness section; Liu 2025 added to Related Sources
  - `wiki/concepts/bone-conduction.md` -- new `Sensor-Failure Robustness` subsection; Liu 2025 added to sources
  - `wiki/synthesis/multimodal-bc-speech-enhancement.md` -- new `2.5 Attention-Driven Robust Fusion (2025)` subsection; ATFA + sensor-failure-robust-fusion in Related Concepts; Liu 2025 in frontmatter sources
  - `wiki/index.md` -- entries added (3 entities, 2 concepts, 1 source); statistics updated to 414 / 165 / 152 / 73
  - `wiki/concepts/index.md` -- added DenGCAN, iAFF, AG, ATFA, sensor-failure-robust-fusion
  - `wiki/entities/index.md` -- added Liu, Chen, Yin (and back-filled Kelan Kuang, Feiran Yang)
  - `wiki/sources/index.md` -- added Kuang 2024 and Liu 2025
- **Key insights**:
  - **Pre-fusion via shared convolution** -- a single conv kernel is applied to *both* BC and AC inputs to extract common spectral patterns before encoding (multi-view input).
  - **ATFA = MHSA along time + MHSA along frequency, in parallel**, combined with learnable α/β. Three cascaded ATFA blocks + an Adaptive Hierarchical Attention (AHA) for multi-scale fusion.
  - **Dual-channel mask** -- four real masks (RI for AC, RI for BC) applied to the original two complex spectra and summed. A learned beamforming-style filter that generalizes to other backbones (validated +0.2 PESQ on a DCCRN).
  - **Special Training (ST) for sensor-failure robustness**: with p = 0.2 each, replace AC or BC with low-amplitude noise during training. This transforms catastrophic failure (PESQ 1.18 when AC fails) into recovery (PESQ 2.54). Existing baselines (FCN, MMINet, AffFusion) actually *worsen* the signal when one sensor fails -- they amplify the dead channel.
  - **Architectural robustness without ST**: the dual-mask + ATFA model already outperforms baselines under sensor failure, suggesting attention + per-modality output heads provide an inductive bias for graceful degradation.
  - **Parameter efficiency**: 1.6M params (~5% of AffFusion's 31.4M) while beating it across all SNRs on ESMB BC corpus.
  - **Practical positioning**: bridges the academic ATFA literature (Yu 2022, Liu 2025) with the BC/AC wearables space and surfaces a previously ignored failure mode (intermittent BC sensor invalidity due to wearing position/jaw motion).

---

## [2026-05-16] ingest | Fusing Bone-Conduction and Air-Conduction Sensors for Complex-Domain Speech Enhancement (Wang, Zhang & Wang 2022)

- **Source**: `raw/papers/wang-2022-fusing-bc-ac-complex-domain-se/full-text.md` (Zotero: K592VRRE)
- **Authors**: Heming Wang, Xueliang Zhang, DeLiang Wang
- **Published**: IEEE/ACM Trans. Audio, Speech, Language Process., Vol. 30, pp. 3134–3143, 2022
- **DOI**: 10.1109/TASLP.2022.3209943
- **Summary**: Attention-based AC-BC fusion with Densely-Connected CRN (DC-CRN) in complex domain; attention mask soft-selects between modalities; CycleGAN-based semi-supervised framework leverages unpaired AC data, matching full supervision with only 50% parallel data; +21.1% STOI at −5 dB on ESMB corpus
- **Extraction**: MinerU precision extract (VLM model, --formula --table)
- **Pages created**:
  - `raw/papers/wang-2022-fusing-bc-ac-complex-domain-se/full-text.md` — extracted via MinerU
  - `wiki/sources/wang-2022-fusing-bc-ac-complex-domain-se.md` — source page
  - `wiki/entities/heming-wang.md` — lead author
  - `wiki/entities/xueliang-zhang.md` — co-author
  - `wiki/entities/deliang-wang.md` — co-author
  - `wiki/concepts/complex-spectral-mapping.md` — RI-domain speech enhancement paradigm
- **Pages updated**:
  - `wiki/concepts/bone-conduction.md` — added source, complex-spectral-mapping concept link
  - `wiki/synthesis/multimodal-bc-speech-enhancement.md` — expanded §2.2 with Wang 2022 details, updated benchmarks table, added to Related Sources/Concepts
  - `wiki/index.md` — added 3 entities, 1 concept, 1 source; updated statistics

---

## [2026-05-17] ingest | SEANet (Tagliasacchi, Li, Misiunas & Roblek 2020)

- **Source**: `raw/papers/tagliasacchi-2020-seanet/full-text.md` (Zotero: BW784N4C)
- **Authors**: Marco Tagliasacchi, Yunpeng Li, Karolis Misiunas, Dominik Roblek
- **Published**: INTERSPEECH 2020
- **Summary**: First multi-modal speech enhancement using accelerometer data from earbud bone-conductance sensors; wave-to-wave UNet with MelGAN adversarial + feature losses; 9.6 dB SI-SDRi in overlapping-speaker scenarios
- **Pages created**:
  - `raw/papers/tagliasacchi-2020-seanet/full-text.md` — MinerU extraction from Zotero PDF
  - `wiki/sources/tagliasacchi-2020-seanet.md`
  - `wiki/entities/marco-tagliasacchi.md`
  - `wiki/entities/yunpeng-li.md`
  - `wiki/entities/karolis-misiunas.md`
  - `wiki/entities/dominik-roblek.md`
- **Pages updated**:
  - `wiki/concepts/bcs-guided-speech-enhancement.md` — added SEANet entry to comparison table; added to sources and Related Sources
  - `wiki/synthesis/multimodal-bc-speech-enhancement.md` — new `2.1 Foundational Era` subsection with SEANet; renumbered sections 2.2–2.6; added to sources and Related Sources
  - `wiki/index.md` — added 4 entities, 1 source; updated statistics

---

## [2026-05-17] ingest | Lu et al. 2021: Survey on ANC — Part I: Linear Systems

- **Source**: `raw/papers/lu-2021-survey-active-noise-control-linear/full-text.md` (Zotero: QVJMFTWC)
- **Authors**: Lu Lu, Kai-Li Yin, Rodrigo C. de Lamare, Zongsheng Zheng, Yi Yu, Xiaomin Yang, Badong Chen
- **Published**: arXiv preprint, 2021
- **DOI**: 10.48550/arXiv.2110.00531
- **Summary**: Comprehensive survey of linear ANC techniques (2009–2020) covering filtered-x, filtered-e, filtered-u families, practical considerations, and novel methods
- **Pages created**:
  - `raw/papers/lu-2021-survey-active-noise-control-linear/full-text.md` — extracted text from Zotero PDF
  - `raw/papers/lu-2021-survey-active-noise-control-linear/figures/` — 58 extracted figure images (MinerU VLM, includes 17 main paper figures plus headers/footers/equations rasterized)
  - `wiki/sources/lu-2021-survey-active-noise-control-linear.md`
  - `wiki/entities/lu-lu.md`
  - `wiki/entities/kai-li-yin.md`
  - `wiki/entities/rodrigo-de-lamare.md`
  - `wiki/entities/zongsheng-zheng.md`
  - `wiki/entities/yi-yu.md`
  - `wiki/entities/xiaomin-yang.md`
  - `wiki/concepts/online-secondary-path-estimation.md`
  - `wiki/concepts/distributed-anc.md`
  - `wiki/concepts/psychoacoustic-anc.md`
  - `wiki/concepts/selective-anc.md`
  - `wiki/concepts/active-structural-acoustic-control.md`
  - `wiki/concepts/convex-combination-anc.md`
  - `wiki/concepts/sparse-anc.md`
  - `wiki/concepts/subband-adaptive-filter.md`
- **Pages updated**:
  - `wiki/entities/badong-chen.md` — added this paper
  - `wiki/concepts/active-noise-control.md` — added related source
  - `wiki/concepts/filtered-x-lms-algorithm.md` — added related sources and concept cross-refs
  - `wiki/concepts/feedback-anc.md` — added related source
  - `wiki/concepts/impulsive-noise.md` — added related source
  - `wiki/synthesis/adaptive-algorithm-tradeoffs.md` — added source
  - `wiki/synthesis/anc-architecture-evolution.md` — added source
  - `wiki/synthesis/secondary-path-modeling-evolution.md` — added source
  - `wiki/synthesis/multichannel-anc-efficiency-and-robustness.md` — added source
  - `wiki/synthesis/feedback-anc-filter-design.md` — added source
  - `wiki/synthesis/impulsive-noise-control.md` — added source
  - `wiki/synthesis/nonlinear-anc-approaches.md` — added source
  - `wiki/index.md` — added 6 entities, 8 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 6 entity rows
  - `wiki/concepts/index.md` — added 8 concept rows

---

## [2026-05-17] ingest | Deep Observation Filter for Virtual Sensing in Local ANC (Holzmuller & Sontacchi 2025)

- **Source**: `raw/papers/holzmuller-2025-deep-observation-filter-virtual-sensing-active-noise-control/full-text.md` (Zotero: 5KW3SUYE)
- **Authors**: Felix Holzmuller, Alois Sontacchi
- **Published**: Forum Acusticum / Euronoise, June 2025
- **Summary**: CNN-based online estimation of RMT observation filter using GCC-PHAT features + virtual microphone coordinates; 367k params, −33.53 dB NMSE, async dual-loop operation
- **Pages created**:
  - `raw/papers/holzmuller-2025-deep-observation-filter-virtual-sensing-active-noise-control/full-text.md` — extracted text from Zotero PDF (MinerU VLM)
  - `raw/papers/holzmuller-2025-deep-observation-filter-virtual-sensing-active-noise-control/figures/` — 26 extracted figure images
  - `wiki/sources/holzmuller-2025-deep-observation-filter-virtual-sensing-active-noise-control.md`
  - `wiki/concepts/neural-observation-filter.md`
- **Pages updated**:
  - `wiki/entities/felix-holzmueller.md` — added this paper
  - `wiki/entities/alois-sontacchi.md` — added this paper
  - `wiki/concepts/remote-microphone-technique.md` — added full RMT formulation, neural observation filter section
  - `wiki/concepts/virtual-sensing.md` — added related source
  - `wiki/synthesis/virtual-sensing-evolution.md` — added CNN approach as precursor to Obs-TasNet, updated comparison table
  - `wiki/index.md` — added 1 concept, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/concepts/index.md` — added 1 concept row

---

## [2026-05-20] ingest | Distributed FastMNMF for Efficient BSS Using Distributed Microphone Arrays (Nishikori et al. 2026)

- **Source**: `raw/papers/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss/full-text.md` (Zotero: XYXBN3H5, arXiv: 2605.19388)
- **Authors**: Hirotaka Nishikori, Nobutaka Ito, Kouei Yamaoka, Norihiro Takamune, Hiroshi Saruwatari
- **Published**: arXiv preprint, May 2026
- **Summary**: Block-diagonal SCM constraint for distributed FastMNMF; ~2.95x speedup over full-array, +0.5-0.8 dB SDR over single-subarray
- **Pages created**:
  - `raw/papers/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss/full-text.md` — extracted text from arXiv HTML (Defuddle)
  - `raw/papers/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss/figures/` — 3 downloaded figures
  - `wiki/sources/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss.md`
  - `wiki/concepts/fastmnf.md`
  - `wiki/entities/hirotaka-nishikori.md`
  - `wiki/entities/nobutaka-ito.md`
  - `wiki/entities/kouei-yamaoka.md`
  - `wiki/entities/norihiro-takamune.md`
  - `wiki/entities/hiroshi-saruwatari.md`
- **Pages updated**:
  - `wiki/index.md` — added 5 entities, 1 concept, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 5 entity rows
  - `wiki/concepts/index.md` — added 1 concept row

---

## [2026-05-20] ingest | Cross-Talk Speech Reduction, by Separation, for Separation (Wang & Cornell 2026)

- **Source**: `raw/papers/wang-2026-cross-talk-speech-reduction-separation/full-text.md` (Zotero: MNP3G55C, arXiv: 2605.19695)
- **Authors**: Zhong-Qiu Wang, Samuele Cornell
- **Published**: arXiv preprint, May 2026. Extended version of IJCAI 2026 conference paper.
- **Summary**: CTRnet for cross-talk reduction via blind deconvolution trained on real close-talk+far-field pairs; PuLSS for far-field speech separation using CTRnet pseudo-labels; SOTA 22.1% cpWER on CHiME-6 with oracle diarization
- **Pages created**:
  - `raw/papers/wang-2026-cross-talk-speech-reduction-separation/full-text.md` — extracted text from arXiv HTML (Defuddle)
  - `raw/papers/wang-2026-cross-talk-speech-reduction-separation/figures/` — 6 downloaded figures
  - `wiki/sources/wang-2026-cross-talk-speech-reduction-separation.md`
  - `wiki/concepts/cross-talk-reduction.md`
  - `wiki/entities/zhong-qiu-wang.md`
  - `wiki/entities/samuele-cornell.md`
- **Pages updated**:
  - `wiki/index.md` — added 2 entities, 1 concept, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 1 concept row

---

## [2026-05-20] ingest | TF-SepNet: an efficient 1D kernel design in CNNs for low-complexity acoustic scene classification (Cai et al. 2024)

- **Source**: `raw/papers/cai-2024-tf-sepnet/full-text.md` (Zotero: FYGJZNTZ, arXiv: 2309.08200)
- **Authors**: Yiqiang Cai, Peihong Zhang, Shengchen Li
- **Published**: ICASSP 2024
- **Summary**: TF-SepNet: an extremely efficient CNN for ASC. Uses parallel 1D depthwise convolutions (TF-SepConvs) along separate frequential and temporal paths to process Mel-spectrogram features, achieving 60.0% accuracy on TAU 2022 dataset with 59% lower MACs and 38-39% fewer parameters. Demonstrates that parallel separate kernels enlarge the Effective Receptive Field (ERF).
- **Pages created**:
  - `wiki/sources/cai-2024-tf-sepnet.md`
  - `wiki/concepts/acoustic-scene-classification.md`
  - `wiki/concepts/effective-receptive-field.md`
  - `wiki/concepts/time-frequency-separate-convolutions.md`
  - `wiki/concepts/adaptive-residual-normalization.md`
  - `wiki/concepts/bc-resnet.md`
  - `wiki/entities/yiqiang-cai.md`
  - `wiki/entities/peihong-zhang.md`
  - `wiki/entities/shengchen-li.md`
- **Pages updated**:
  - `wiki/index.md` — added 3 entities, 5 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 3 entity rows
  - `wiki/concepts/index.md` — added 5 concept rows
  - `wiki/concepts/spectrogram-analysis.md` — updated with STFT/Log-Mel formulations
  - `wiki/concepts/neural-networks.md` — added related links

---

## [2026-05-20] ingest | Directional Source Separation for Robust Speech Recognition on Smart Glasses (Feng et al. 2025)

- **Source**: `raw/papers/feng-2025-directional-source-separation-smart-glasses/full-text.md` (Zotero: 3DZ5NNH3, arXiv: 2309.10993)
- **Authors**: Tiantian Feng, Ju Lin, Yiteng Huang, Weipeng He, Kaustubh Kalgaonkar, Niko Moritz, Li Wan, Xin Lei, Ming Sun, Frank Seide
- **Published**: ICASSP 2025
- **DOI**: 10.1109/ICASSP49660.2025.10888256
- **Summary**: Directional source separation combining NLCMV/neural beamforming with separation network on Project Aria; neural BF +2.27 dB SI-SDR; joint training achieves 13.25% WER
- **Pages created**:
  - `raw/papers/feng-2025-directional-source-separation-smart-glasses/full-text.md` �� Defuddle extraction from arXiv HTML
  - `raw/papers/feng-2025-directional-source-separation-smart-glasses/figures/` �� 7 downloaded figures
  - `wiki/sources/feng-2025-directional-source-separation-smart-glasses.md`
  - `wiki/concepts/neural-beamforming.md`
  - `wiki/entities/tiantian-feng.md`
  - `wiki/entities/weipeng-he.md`
  - `wiki/entities/kaustubh-kalgaonkar.md`
  - `wiki/entities/li-wan.md`
  - `wiki/entities/xin-lei.md`
- **Pages updated**:
  - `wiki/entities/ju-lin.md` �� added this paper
  - `wiki/entities/yiteng-huang.md` �� added this paper
  - `wiki/entities/niko-moritz.md` �� added this paper
  - `wiki/entities/frank-seide.md` �� added this paper
  - `wiki/entities/ming-sun.md` �� added this paper
  - `wiki/index.md` �� added 5 entities, 1 concept, 1 source; updated statistics
  - `wiki/sources/index.md` �� added 1 source row
  - `wiki/entities/index.md` �� added 5 entity rows
  - `wiki/concepts/index.md` �� added 1 concept row

---

## [2026-05-21] ingest | Broadcasted Residual Learning for Efficient Keyword Spotting (Kim et al. 2021)

- **Source**: `raw/papers/kim-2021-broadcasted-residual-learning/full-text.md` (Zotero: EFJM3USE, arXiv: 2106.04140)
- **Authors**: Byeonggeun Kim, Simyung Chang, Jinkyu Lee, Dooyong Sung
- **Published**: INTERSPEECH 2021
- **Summary**: Introduces broadcasted residual learning and BC-ResNet for efficient keyword spotting. The method applies frequency-aware 2D processing, averages over frequency, performs low-cost temporal convolution, and broadcasts the temporal residual back over the spectrogram map. BC-ResNet-8 reaches 98.0% on Speech Commands v1 and 98.7% on v2 with 321k parameters.
- **Pages created**:
  - `wiki/sources/kim-2021-broadcasted-residual-learning.md`
  - `wiki/concepts/keyword-spotting.md`
  - `wiki/concepts/broadcasted-residual-learning.md`
  - `wiki/concepts/subspectral-normalization.md`
  - `wiki/entities/byeonggeun-kim.md`
  - `wiki/entities/simyung-chang.md`
  - `wiki/entities/jinkyu-lee.md`
  - `wiki/entities/dooyong-sung.md`
- **Pages updated**:
  - `wiki/concepts/bc-resnet.md` — updated with original paper details, equations, figure, and results
  - `wiki/concepts/depthwise-separable-convolution.md` — added related source
  - `wiki/concepts/spectrogram-analysis.md` — added BC-ResNet Log-Mel setup and related links
  - `wiki/concepts/neural-networks.md` — added efficient audio CNN links
  - `wiki/index.md` — added 4 entities, 3 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 4 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows

---

## [2026-05-21] lint | Health check (post-skill-fix)

- **Index consistency**: Found 7 concepts and 1 source missing from main index + sub-indexes. All gaps fixed.
- **Broken links**: Not checked (Step 5 not run this pass)
- **Orphan pages**: Not checked (Step 6 not run this pass)
- **Statistics**: Updated from 475/192/177/81/19 to 483/192/184/82/19
- **Skill fix verification**: Tested updated wiki-lint commands — Python-based Step 4 (missing entries) works clean; `Select-String` regex now uses single quotes inside `pwsh -Command` to avoid `^|` being parsed as regex OR. All 6 × (main + sub-index) diffs = 0 ✅

---

## [2026-05-21] ingest | A Survey of Optimization Methods for Independent Vector Analysis in Audio Source Separation (Guo et al. 2023)

- **Source**: `raw/papers/guo-2023-iva-survey/full-text.md` (Zotero: DA3F64K6)
- **Authors**: Ruiming Guo, Zhongqiang Luo, Mingchun Li
- **Published**: Sensors 2023, Vol. 23, Issue 1, Article 493
- **DOI**: 10.3390/s23010493
- **Summary**: Comprehensive survey of six IVA optimization families (NG, FastIVA, AuxIVA, EM, BCD/IP/ISS, EVD) with unified notation, taxonomy, and experimental comparison under determined and overdetermined reverberant audio scenarios.
- **Pages created**:
  - `wiki/sources/guo-2023-iva-survey.md`
  - `wiki/concepts/independent-vector-analysis.md`
  - `wiki/concepts/blind-source-separation.md`
  - `wiki/entities/ruiming-guo.md`
  - `wiki/entities/zhongqiang-luo.md`
  - `wiki/entities/mingchun-li.md`
- **Pages updated**:
  - `wiki/concepts/fastmnmf.md` — added IVA/BSS wikilinks and related source
  - `wiki/index.md` — added 3 entities, 2 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 3 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows

---

## [2026-05-23] ingest | Li, Middelberg & Doclo (2026) Geometry-Conditioned SSF for Target Speaker Extraction

- **Source**: `raw/papers/li-2026-geometry-conditioned-ssanc/full-text.md` (Zotero: D5LDQUHY, arXiv: 2605.18442)
- **Authors**: Jiatong Li, Wiebke Middelberg, Simon Doclo
- **Published**: arXiv preprint, 2026-05-18 (submitted to IWAENC 2026)
- **DOI**: 10.48550/arXiv.2605.18442
- **Summary**: Geometry-Conditioned Spatially Selective Non-Linear Filter (GC-SSF) for target speaker extraction. Extends baseline SSF (Tesch & Gerkmann 2024) with FiLM-based conditioning branch driven by DOA-Microphone Positional Encoding (DOA-MPE). Trained on random arrays, GC-SSF surpasses SSF-Random by ~0.45 PESQ across all geometries and achieves +1.25 PESQ over SSF-Circ on mismatched geometries while maintaining high spatial selectivity.
- **Pages created**:
  - `raw/papers/li-2026-geometry-conditioned-ssanc/full-text.md` — Defuddle extraction from arXiv HTML
  - `raw/papers/li-2026-geometry-conditioned-ssanc/figures/` — 4 downloaded figures (system, scenario, random, pesq_sisdr)
  - `wiki/sources/li-2026-geometry-conditioned-ssanc.md` — source page
  - `wiki/entities/jiatong-li.md` — first author
  - `wiki/entities/wiebke-middelberg.md` — co-author
  - `wiki/concepts/spatially-selective-nonlinear-filter.md` — baseline SSF concept
  - `wiki/concepts/geometry-conditioned-ssf.md` — GC-SSF concept
  - `wiki/concepts/doa-microphone-positional-encoding.md` — DOA-MPE concept
  - `wiki/concepts/film-layer.md` — FiLM conditioning layer concept
  - `wiki/concepts/target-speaker-extraction.md` — TSE concept
- **Pages updated**:
  - `wiki/entities/simon-doclo.md` — added GC-SSF contribution and source link
  - `wiki/concepts/spatially-selective-anc.md` — added cross-references to SSF/TSE concepts and source link
  - `wiki/index.md` — added 2 entities, 5 concepts, 1 source; updated statistics to 504/201/193/85/19/6
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 5 concept rows

---

## [2026-05-23] ingest | Xiao, Roden, Blau & Doclo (2026) Robust Soft-Constrained SSANC for Hearables

- **Source**: Zotero (Xiao 2026, JASA-EL/Acta Acustica preprint)
- **Summary**: Robust soft-constrained spatially selective ANC (SSANC) for hearables. Cost is averaged over $J=44$ secondary path estimates from KEMAR/different ear-canal placements, narrowing the performance spread under plant variations. Soft constraint with trade-off $\beta$ balances noise reduction against target-direction preservation. Validated in real time on dSPACE SCALEXIO LabBox + FPGA at 40 kHz with $L_w=1800$ taps.
- **Pages created**:
  - `raw/papers/xiao-2026-robust-spatially-selective-anc/full-text.txt` — pdftotext extraction (43 KB)
  - `wiki/sources/xiao-2026-robust-spatially-selective-anc.md` — source page
  - `wiki/entities/tong-xiao.md` — first author
  - `wiki/entities/simon-doclo.md` — corresponding author
  - `wiki/entities/reinhild-roden.md` — co-author
  - `wiki/entities/matthias-blau.md` — co-author
  - `wiki/concepts/spatially-selective-anc.md` — SSANC concept
  - `wiki/concepts/soft-constrained-anc.md` — soft-constrained ANC concept
- **Pages updated**:
  - `wiki/concepts/uncertainty-modeling-for-anc.md` — added cross-references to new SSANC concepts and source
  - `wiki/concepts/speech-preserving-anc.md` — added Xiao 2026 reference and related-concept links
  - `wiki/concepts/robust-control.md` — added related ANC robustness concepts and Related Sources section
  - `wiki/index.md` — added 4 entities, 2 concepts, 1 source; updated statistics to 496/199/188/84/19/6
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 4 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows

---

## [2026-05-23] ingest | Verification of Simultaneous Equations Method (Fujii et al. 2006)

- **Source**: `raw/papers/fujii-2006-simultaneous-equations-anc/full-text.md` (Zotero: TW8DUFVN)
- **Authors**: Kensaku Fujii, Kotaro Yamaguchi, Shigeyuki Hashimoto, Yusuke Fujita, Mitsuji Muneyasu
- **Published**: Acoustical Science and Technology, Vol. 27, No. 5, pp. 270-277
- **DOI**: 10.1250/ast.27.270
- **Summary**: First experimental verification of the simultaneous equations method for feedforward ANC - estimates optimal noise control filter without secondary path model using an auxiliary filter and frequency-domain adaptation
- **Pages created**:
  - `raw/papers/fujii-2006-simultaneous-equations-anc/full-text.md` - MinerU extracted text from Zotero PDF
  - `wiki/sources/fujii-2006-simultaneous-equations-anc.md` - source page
  - `wiki/entities/kensaku-fujii.md` - first/prolific author
  - `wiki/entities/kotaro-yamaguchi.md` - co-author
  - `wiki/entities/shigeyuki-hashimoto.md` - co-author
  - `wiki/entities/yusuke-fujita.md` - co-author
  - `wiki/entities/mitsuji-muneyasu.md` - co-author/co-proposer of method
  - `wiki/concepts/simultaneous-equations-method.md` - core method concept
  - `wiki/concepts/auxiliary-filter.md` - auxiliary filter concept
- **Pages updated**:
  - `wiki/concepts/filtered-x-lms-algorithm.md` - added paper as related source
  - `wiki/concepts/feedforward-anc.md` - added paper as related source
  - `wiki/concepts/active-noise-control.md` - added paper as related source
  - `wiki/concepts/secondary-path-modeling.md` - added paper as related source
  - `wiki/concepts/adaptive-filtering.md` - added paper as related source
  - `wiki/synthesis/anc-architecture-evolution.md` - added paper reference
  - `wiki/synthesis/adaptive-algorithm-tradeoffs.md` - added paper reference
  - `wiki/synthesis/computational-efficiency-evolution.md` - added paper reference
  - `wiki/index.md` - added 5 entities, 2 concepts, 1 source; updated statistics to 512/206/195/86/19/6
  - `wiki/sources/index.md` - added 1 source row
  - `wiki/entities/index.md` - added 5 entity rows
  - `wiki/concepts/index.md` - added 2 concept rows

---

## [2026-05-24] ingest | GTCRN: A Speech Enhancement Model Requiring Ultralow Computational Resources (Rong et al. 2024)

- **Source**: `raw/papers/rong-2024-gtcrn-speech-enhancement-ultralow/full-text.md` (Zotero: BACCUUCC)
- **Authors**: Xiaobin Rong, Tianchi Sun, Xu Zhang, Yuxiang Hu, Changbao Zhu, Jing Lu
- **Published**: ICASSP 2024, pp. 971–975
- **DOI**: 10.1109/ICASSP48485.2024.10448310
- **Summary**: GTCRN — ultralightweight (23.7 K params, 39.6 MMACs/s) speech enhancement using grouped convolution, grouped DPRNN, ERB-based band merging, subband feature extraction (SFE), and temporal recurrent attention (TRA).
- **Pages created**:
  - `raw/papers/rong-2024-gtcrn-speech-enhancement-ultralow/full-text.md` — MinerU VLM extraction from Zotero PDF
  - `wiki/sources/rong-2024-gtcrn-speech-enhancement-ultralow.md` — source page
  - `wiki/entities/xiaobin-rong.md` — first author
  - `wiki/entities/tianchi-sun.md` — co-author
  - `wiki/entities/xu-zhang.md` — co-author
  - `wiki/entities/yuxiang-hu.md` — co-author
  - `wiki/entities/changbao-zhu.md` — co-author
  - `wiki/entities/jing-lu.md` — co-author
  - `wiki/concepts/gtcrn.md` — GTCRN concept
- **Pages updated**:
  - `wiki/concepts/dprnn.md` — added G-DPRNN variant section and source link
  - `wiki/concepts/convolutional-recurrent-network.md` — added GTCRN application
  - `wiki/synthesis/computational-efficiency-evolution.md` — added GTCRN to frontier
  - `wiki/index.md` — added 6 entities, 1 concept, 1 source; updated statistics to 512/207/194/86/19/6
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 6 entity rows
  - `wiki/concepts/index.md` — added 1 concept row

---

## [2026-05-24] lint | Health check

- **Index consistency**: 4 entities missing from main index (tong-xiao, simon-doclo, reinhild-roden, matthias-blau) — added; all sub-indexes matched actual files
- **Broken links**: 693 legacy `../` prefixed wikilinks (pre-existing, not actual broken targets)
- **Orphan pages**: 0
- **Statistics**: Updated from 512/207/194/86 to 520/212/196/87 to match actual
- **Actions taken**: Added 4 entity rows to main index, updated statistics section

---

## [2026-05-24] ingest | AGADIR: Towards Array-Geometry Agnostic Directional Speech Recognition (Lin et al. 2024)

- **Source**: `raw/papers/lin-2024-agadir-array-geometry-agnostic-speech-recognition/full-text.md` (Zotero: 8K2YN6P5)
- **Authors**: Ju Lin, Niko Moritz, Yiteng Huang, Ruiming Xie, Ming Sun, Christian Fuegen, Frank Seide
- **Published**: ICASSP 2024 (arXiv: 2401.10411)
- **DOI**: 10.48550/arXiv.2401.10411
- **Summary**: AGADIR — geometry-agnostic directional ASR for smart glasses using multi-geometry training and NLCMV beamforming; 15–28% relative WER improvement.
- **Pages created**:
  - `raw/papers/lin-2024-agadir-array-geometry-agnostic-speech-recognition/full-text.md` — Defuddle extraction from arXiv HTML
  - `wiki/sources/lin-2024-agadir-array-geometry-agnostic-speech-recognition.md` — source page
  - `wiki/entities/ju-lin.md` — first author
  - `wiki/entities/niko-moritz.md` — co-author
  - `wiki/entities/yiteng-huang.md` — co-author
  - `wiki/entities/ruiming-xie.md` — co-author
  - `wiki/entities/ming-sun.md` — co-author
  - `wiki/entities/christian-fuegen.md` — co-author
  - `wiki/entities/frank-seide.md` — co-author
  - `wiki/concepts/nlcmv-beamforming.md` — NLCMV beamforming concept
- **Pages updated**:
  - `wiki/concepts/beamforming.md` — added NLCMV variant to techniques list and source
  - `wiki/index.md` — added 7 entities, 1 concept, 1 source; updated statistics to 529/219/197/88/19/6
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 7 entity rows
  - `wiki/concepts/index.md` — added 1 concept row

---

## [2026-05-25] ingest | A Convolutional Recurrent Neural Network for Real-Time Speech Enhancement (Tan & Wang 2018)

- **Source**: `raw/papers/tan-2018-convolutional-recurrent-network-speech-enhancement/full-text.md` (Zotero: F8A8SVLS)
- **Authors**: Ke Tan, DeLiang Wang
- **Published**: Interspeech 2018, pp. 3229-3233
- **DOI**: 10.21437/Interspeech.2018-1405
- **Summary**: Proposes CRN combining CED with LSTM and causal convolutions for noise- and speaker-independent real-time monaural speech enhancement
- **Pages created**:
  - `raw/papers/tan-2018-convolutional-recurrent-network-speech-enhancement/full-text.md` -- extracted text from Zotero PDF
  - `wiki/sources/tan-2018-convolutional-recurrent-network-speech-enhancement.md`
  - `wiki/entities/ke-tan.md`
- **Pages updated**:
  - `wiki/entities/deliang-wang.md` -- added this paper
  - `wiki/concepts/convolutional-recurrent-network.md` -- added source link and updated date
  - `wiki/synthesis/ai-driven-anc.md` -- added source link
  - `wiki/synthesis/computational-efficiency-evolution.md` -- added source link
  - `wiki/index.md` -- added 1 entity, 1 source; updated statistics
  - `wiki/sources/index.md` -- added 1 source row
  - `wiki/entities/index.md` -- added 1 entity row, updated 1 existing

---

## [2026-05-26] ingest | Linearly Constrained Deep Beamformer for Multi-Speaker Scenarios (Zaidel, Engel, Engel & Gannot 2026)

- **Source**: `raw/papers/zaidel-2026-linearly-constrained-deep-beamformer/full-text.md` (Zotero: TLSRHKI7)
- **Authors**: Ilai Zaidel, Ori Engel, Bar Engel, Sharon Gannot
- **Published**: arXiv preprint, May 2026
- **DOI**: 10.48550/arXiv.2605.21141
- **Summary**: Fully DNN-based beamformer with adaptive multi-term loss enforcing distortionless response and null-steering constraints via augmented Lagrangian-inspired training; outperforms classical LCMV in SI-SDR and SNR
- **Pages created**:
  - `raw/papers/zaidel-2026-linearly-constrained-deep-beamformer/full-text.md` — extracted text from arXiv HTML
  - `wiki/sources/zaidel-2026-linearly-constrained-deep-beamformer.md`
  - `wiki/entities/ilai-zaidel.md`
  - `wiki/entities/ori-engel.md`
  - `wiki/entities/bar-engel.md`
  - `wiki/entities/sharon-gannot.md`
  - `wiki/concepts/lcmv-beamformer.md`
  - `wiki/concepts/relative-transfer-function.md`
- **Pages updated**:
  - `wiki/concepts/beamforming.md` — added LCMV technique and source link
  - `wiki/concepts/mvdr-beamformer.md` — added LCMV relationship and source link
  - `wiki/concepts/gsc-beamformer.md` — added LCMV concept link and source link
  - `wiki/concepts/target-speaker-extraction.md` — added source link
  - `wiki/concepts/multi-channel-speech-enhancement.md` — added source link
  - `wiki/index.md` — added 4 entities, 2 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 4 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows

## [2026-05-26] ingest (re) | A Review of Virtual Sensing Algorithms for Active Noise Control (Moreau, Cazzolato, Zander & Petersen 2008)

- **Source**: `raw/papers/moreau-2008-virtual-sensing-review/full-text.md` (Zotero: LJDPCZ9G)
- **Authors**: Danielle Moreau, Ben Cazzolato, Anthony Zander, Cornelis Petersen
- **Published**: Algorithms, Vol. 1, No. 2, pp. 69–99, 2008
- **DOI**: 10.3390/a1020069
- **Summary**: Re-ingested with MinerU VLM extraction (93 figures, full LaTeX equations, tables) replacing previous pdftotext extraction
- **Pages updated**:
  - `raw/papers/moreau-2008-virtual-sensing-review/full-text.md` — replaced .txt with MinerU markdown
  - `raw/papers/moreau-2008-virtual-sensing-review/figures/` — 93 new figures from MinerU
  - `wiki/sources/a-review-of-virtual-sensing-algorithms-for-active-.md` — updated sources and dates

## [2026-05-26] ingest (re) | Noise Power Spectral Density Estimation Based on Optimal Smoothing and Minimum Statistics (Martin 2001)

- **Source**: `raw/papers/martin-2001-noise-psd-estimation-optimal-smoothing/full-text.md` (Zotero: SUKHAUHG)
- **Authors**: Rainer Martin
- **Published**: IEEE Trans. Speech and Audio Processing, Vol. 9, No. 5, pp. 504–512, 2001
- **DOI**: 10.1109/89.928915
- **Summary**: VAD-free noise PSD estimation using optimal time-varying smoothing and minimum statistics with bias compensation
- **Pages created**:
  - `raw/papers/martin-2001-noise-psd-estimation-optimal-smoothing/full-text.md` — re-extracted with MinerU VLM (formulas, tables, 37 figures)
  - `wiki/entities/rainer-martin.md`
  - `wiki/concepts/minimum-statistics.md`
- **Pages updated**:
  - `wiki/sources/martin-2001-noise-psd-estimation-optimal-smoothing.md` — rewrote with comprehensive methodology, equations, experimental results, and figures
  - `wiki/concepts/voice-activity-detection.md` — added VAD-free alternatives section with Minimum Statistics link
  - `wiki/index.md` — added 1 entity, 1 concept, 1 source; updated statistics
  - `wiki/entities/index.md` — added 1 entity row
  - `wiki/concepts/index.md` — added 1 concept row
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-05-27] ingest | An Active Noise Control Casing Using the Multi-Channel Feedforward Control System and the Relative Path Based Virtual Sensing Method (Shi 2020)

- **Source**: `raw/papers/shi-2020-active-noise-control-casing-virtual-sensing/full-text.md` (Zotero: DAGTQQLP)
- **Authors**: Chuang Shi, Zhuoying Jia, Rong Xie, Huiyong Li
- **Published**: Mechanical Systems and Signal Processing, Vol. 144, pp. 106878, 2020
- **DOI**: 10.1016/j.ymssp.2020.106878
- **Summary**: Proposes Relative Path based Virtual Sensing (RP-VS) method that unifies AF-VS and RM-VS. Theoretical analysis, simulations on single/dual-channel ANC systems, and ANC casing prototype validation with (1,4,4) configuration on real-time DSP.
- **Pages created**:
  - `raw/papers/shi-2020-active-noise-control-casing-virtual-sensing/full-text.md` — extracted text from Zotero PDF via MinerU VLM
  - `raw/papers/shi-2020-active-noise-control-casing-virtual-sensing/figures/` — extracted figures from MinerU
  - `wiki/sources/shi-2020-active-noise-control-casing-virtual-sensing.md`
  - `wiki/entities/chuang-shi.md`
  - `wiki/entities/zhuoying-jia.md`
  - `wiki/entities/rong-xie.md`
  - `wiki/entities/huiyong-li.md`
  - `wiki/concepts/relative-path-virtual-sensing.md`
- **Pages updated**:
  - `wiki/concepts/virtual-sensing.md` — added AF-VS, RM-VS, RP-VS to Common Algorithms; added cross-refs to RP-VS concept
  - `wiki/concepts/multi-channel-anc.md` — added ANC Casing Application section
  - `wiki/concepts/remote-microphone-technique.md` — added RP-VS cross-reference
  - `wiki/synthesis/virtual-sensing-evolution.md` — added Section 2.4: Unified RP-VS framework with comparative analysis table
  - `wiki/index.md` — added 4 entities, 1 concept, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 4 entity rows
  - `wiki/concepts/index.md` — added 1 concept row

---

## [2026-05-27] ingest | Coherent-to-Diffuse Power Ratio Estimation for Dereverberation (Schwarz & Kellermann 2015)

- **Source**: `raw/papers/schwarz-2015-coherent-to-diffuse-power-ratio/full-text.md` (Zotero: AT69JCEX)
- **Authors**: Andreas Schwarz, Walter Kellermann
- **Published**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, Vol. 23, No. 6, June 2015, pp. 1006–1018
- **DOI**: 10.1109/TASLP.2015.2418571
- **Summary**: Comprehensive investigation of CDR estimation from spatial coherence; proposed novel unbiased CDR estimators and a DOA-independent dereverberation system
- **Pages created**:
  - `raw/papers/schwarz-2015-coherent-to-diffuse-power-ratio/full-text.md` — extracted text from Zotero PDF via MinerU
  - `wiki/sources/schwarz-2015-coherent-to-diffuse-power-ratio.md`
  - `wiki/entities/walter-kellermann.md`
  - `wiki/concepts/coherent-to-diffuse-power-ratio.md`
  - `wiki/concepts/dereverberation.md`
- **Pages updated**:
  - `wiki/entities/andreas-schwarz.md` — added this paper to sources and related pages
  - `wiki/concepts/spatial-coherence.md` — added this paper to sources and key literature
  - `wiki/index.md` — added 1 entity, 2 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 1 entity row
  - `wiki/concepts/index.md` — added 2 concept rows

---

## [2026-05-27] ingest | Generalized Coherence-Based Signal Enhancement (Löllmann, Brendel & Kellermann 2020)

- **Source**: `raw/papers/lollmann-2020-generalized-coherence-based-signal-enhancement/full-text.md` (Zotero: DSYMKBRQ)
- **Authors**: Heinrich W. Löllmann, Andreas Brendel, Walter Kellermann
- **Published**: ICASSP 2020, pp. 201–205
- **DOI**: 10.1109/ICASSP40776.2020.9054470
- **Summary**: CDR-based speech enhancement using generalized magnitude coherence (GMC) via eigenvalue decomposition; implicit microphone selection without DOA estimation; 4-microphone binaural HA evaluation
- **Pages created**:
  - `raw/papers/lollmann-2020-generalized-coherence-based-signal-enhancement/full-text.md` — extracted text from Zotero PDF via MinerU
  - `wiki/sources/lollmann-2020-generalized-coherence-based-signal-enhancement.md`
  - `wiki/entities/heinrich-w-lollmann.md`
  - `wiki/entities/andreas-brendel.md`
  - `wiki/concepts/generalized-magnitude-coherence.md`
- **Pages updated**:
  - `wiki/entities/walter-kellermann.md` — added this paper to sources and related pages
  - `wiki/concepts/coherent-to-diffuse-power-ratio.md` — added this paper to key sources
  - `wiki/index.md` — added 2 entities, 1 concept, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 1 concept row

---

## [2026-05-27] lint | Health check

- **Index consistency**: All 5 categories match (entities: 237, concepts: 205, sources: 95, synthesis: 19, queries: 6). No duplicates remain.
- **Broken links**: 0 build-blocking broken wikilinks. ~827 pre-existing \`../\`-prefixed links are convention violations (not build failures — they resolve correctly in MkDocs).
- **Orphan pages**: 0 concept orphans, 5 source orphans (not referenced from other content pages), 20 entity orphans (linked only from indexes — expected).
- **Statistics**: Total pages corrected from 553 to 562.
- **Actions taken**:
  - Added missing source entry for zaidel-2026 to main index
  - Added missing synthesis entries for iir-filter-fitting-frequency-response and multi-modal-speech-enhancement
  - Removed 4 duplicate synthesis rows (impulsive-noise-control, computational-efficiency-evolution, feedback-anc-filter-design, iir-filter-fitting)
  - Added multi-modal-speech-enhancement to synthesis subdirectory index
  - Updated Total pages statistic from 553 to 562

---

## [2026-06-01] ingest | Supervised Speech Separation Based on Deep Learning: An Overview (Wang & Chen 2018)

- **Source**: `raw/papers/wang-2018-supervised-speech-separation-deep-learning-overview/full-text.md` (Zotero: D79MZFJA)
- **Authors**: DeLiang Wang, Jitong Chen
- **Published**: IEEE/ACM Trans. Audio, Speech, Lang. Process. 2018, Vol. 26, No. 10, pp. 1702–1726
- **DOI**: 10.1109/TASLP.2018.2842159
- **Summary**: Comprehensive survey of DNN-based supervised speech separation covering learning machines, training targets, acoustic features, monaural and array algorithms, and generalization
- **Pages created**:
  - `raw/papers/wang-2018-supervised-speech-separation-deep-learning-overview/full-text.md` — extracted text from Zotero PDF via MinerU
  - `wiki/sources/wang-2018-supervised-speech-separation-deep-learning-overview.md`
  - `wiki/entities/jitong-chen.md`
  - `wiki/concepts/ideal-binary-mask.md`
  - `wiki/concepts/ideal-ratio-mask.md`
  - `wiki/concepts/permutation-invariant-training.md`
  - `wiki/concepts/deep-clustering-speech-separation.md`
- **Pages updated**:
  - `wiki/entities/deliang-wang.md` — added survey contribution and this paper
  - `wiki/index.md` — added 1 entity, 4 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 1 entity row
  - `wiki/concepts/index.md` — added 4 concept rows

---

## [2026-06-04] ingest | Spatially-Regularized Switching IVA with ISS (Dong et al. 2026)

- **Source**: `raw/papers/dong-2026-spatially-regularized-switching-iva/full-text.md` (Zotero: GMZWLILS)
- **Authors**: Haonan Dong, Wei Liu, Xuemai Xie, Shoji Makino
- **Published**: Conference paper, 2026
- **Summary**: SR-SwIVA-ISS replaces IP update with ISS rank-one update in spatially regularized switching IVA; 5.5–7× computational speedup with comparable separation performance
- **Pages created**:
  - `raw/papers/dong-2026-spatially-regularized-switching-iva/full-text.md` — extracted text from Zotero PDF via MinerU
  - `wiki/sources/dong-2026-spatially-regularized-switching-iva.md`
  - `wiki/entities/haonan-dong.md`
  - `wiki/entities/xuemai-xie.md`
  - `wiki/concepts/switching-independent-vector-analysis.md`
  - `wiki/concepts/iterative-source-steering.md`
  - `wiki/concepts/spatial-regularization.md`
- **Pages updated**:
  - `wiki/entities/wei-liu.md` — added this paper
  - `wiki/entities/shoji-makino.md` — added this paper
  - `wiki/concepts/independent-vector-analysis.md` — added cross-references to SwIVA, ISS, spatial regularization
  - `wiki/concepts/blind-source-separation.md` — added SwIVA to main approaches table and cross-references
  - `wiki/index.md` — added 2 entities, 3 concepts, 1 source; updated statistics to 574/240/212/97/19/6
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows

---

## [2026-06-06] ingest | DeepVQE: Real Time Deep Voice Quality Enhancement for Joint Acoustic Echo Cancellation, Noise Suppression and Dereverberation (Indenbom et al. 2023)

- **Source**: `raw/papers/indenbom-2023-deepvqe/full-text.md` (Zotero: WV7YKFHR, arXiv: 2306.03177)
- **Authors**: Evgenii Indenbom, Nicolae-Catalin Ristea, Ando Saabas, Tanel Parnamaa, Jegor Guzvin, Ross Cutler
- **Published**: ICASSP 2023, pp. 1–5
- **DOI**: 10.1109/ICASSP49357.2023.10096890
- **Summary**: Real-time joint AEC+NS+DR system using cross-attention alignment and complex convolving mask (CCM); encoder-decoder architecture with GRU bottleneck and sub-pixel convolution; SOTA on ICASSP 2023 AEC and DNS challenges with over 10 dB SRR improvement
- **Extraction**: MinerU pipeline extract from Zotero PDF (34,806 bytes, 8 figures)
- **Pages created**:
  - `raw/papers/indenbom-2023-deepvqe/full-text.md` — extracted text from Zotero PDF
  - `raw/papers/indenbom-2023-deepvqe/figures/` — 8 extracted figures
  - `wiki/sources/indenbom-2023-deepvqe.md` — source page
  - `wiki/entities/evgenii-indenbom.md` — first author
  - `wiki/entities/nicolae-catalin-ristea.md` — co-author
  - `wiki/entities/ando-saabas.md` — co-author
  - `wiki/entities/tanel-parnamaa.md` — co-author
  - `wiki/entities/jegor-guzvin.md` — co-author
  - `wiki/entities/ross-cutler.md` — co-author
  - `wiki/concepts/acoustic-echo-cancellation.md` — AEC concept
  - `wiki/concepts/cross-attention-alignment.md` — cross-attention alignment concept
  - `wiki/concepts/complex-convolving-mask.md` — CCM concept
  - `wiki/concepts/sub-pixel-convolution.md` — sub-pixel convolution concept
- **Pages updated**:
  - `wiki/concepts/dereverberation.md` — added DeepVQE to approaches table, cross-references, source link
  - `wiki/concepts/complex-ratio-mask.md` — added CCM cross-reference
  - `wiki/concepts/multi-channel-speech-enhancement.md` — added DeepVQE to key techniques, cross-references, source link
  - `wiki/index.md` — added 6 entities, 4 concepts, 1 source; updated statistics to 585/246/216/98/19/6
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 6 entity rows
  - `wiki/concepts/index.md` — added 4 concept rows

---

## [2026-06-07] ingest | DeepFilterNet — Low Complexity Speech Enhancement via Deep Filtering (Schröter et al. 2022)

- **Source**: 
aw/papers/schroter-2022-deepfilternet/full-text.md (Zotero: TXVFFJPG)
- **Authors**: Hendrik Schröter, Alberto N. Escalante-B., Tobias Rosenkranz, Andreas Maier
- **Published**: ICASSP 2022, pp. 7407–7411
- **arXiv**: 2110.05588
- **Summary**: Two-stage speech enhancement framework using ERB-scaled gains + deep filtering; 1.8M params, 0.35 GMACs, WB-PESQ 2.81, SI-SDR 16.63 dB on VCTK-DEMAND
- **Pages created**:
  - 
aw/papers/schroter-2022-deepfilternet/full-text.md — extracted text from Zotero PDF via MinerU
  - wiki/sources/schroter-2022-deepfilternet.md
  - wiki/entities/hendrik-schroter.md
  - wiki/entities/alberto-n-escalante-b.md
  - wiki/entities/tobias-rosenkranz.md
  - wiki/entities/andreas-maier.md
  - wiki/concepts/deep-filtering.md
  - wiki/concepts/erb-scale.md
- **Pages updated**:
  - wiki/sources/rong-2024-gtcrn-speech-enhancement-ultralow.md — linked DeepFilterNet source, ERB Scale concept
  - wiki/concepts/gtcrn.md — linked DeepFilterNet source, ERB Scale concept
  - wiki/synthesis/computational-efficiency-evolution.md — added DeepFilterNet to efficiency frontier
  - wiki/index.md — added 4 entities, 2 concepts, 1 source; updated statistics
  - wiki/sources/index.md — added 1 source row
  - wiki/entities/index.md — added 4 entity rows
  - wiki/concepts/index.md — added 2 concept rows

---

## [2026-06-07] lint | Health check

- **Index consistency**: Main index had 6 missing entries (1 entity, 4 concepts, 1 source); synthesis sub-index had 4 duplicate rows (23 rows vs 19 actual)
- **Broken links**: 860 wikilinks using `../` prefix convention (not truly broken, just convention-violating); 0 truly broken links
- **Duplicate entries**: 4 duplicates in synthesis sub-index (computational-efficiency-evolution, impulsive-noise-control, feedback-anc-filter-design, iir-filter-fitting-frequency-response each appeared twice)
- **Orphan pages**: 30 entities, 12 concepts, 10 sources, 2 synthesis pages with no inbound wikilinks (expected for index-only references)
- **Statistics**: Queries stated=6, actual=7 (corrected)
- **Actions taken**:
  - Added 1 entity to main index: jitong-chen
  - Added 4 concepts to main index: deep-clustering-speech-separation, ideal-binary-mask, ideal-ratio-mask, permutation-invariant-training
  - Added 1 source to main index: wang-2018-supervised-speech-separation-deep-learning-overview
  - Removed 4 duplicate rows from synthesis sub-index
  - Updated Queries statistic from 6 to 7
  - Build verification passed (31.71s, 0 warnings)

---

## [2026-06-07] ingest | Pandey & Wang (2019) A New Framework for CNN-Based Speech Enhancement in the Time Domain

- **Source**: `raw/papers/pandey-2019-cnn-speech-enhancement-time-domain/full-text.txt` (Zotero: 35DQRHLV)
- **Authors**: Ashutosh Pandey, DeLiang Wang
- **Published**: IEEE/ACM Trans. Audio, Speech, Lang. Process., Vol. 27, No. 7, pp. 1179-1188, July 2019
- **DOI**: 10.1109/TASLP.2019.2913512
- **Summary**: Proposes AECNN — a U-Net fully convolutional autoencoder operating in time domain, trained with STFT magnitude MAE loss (frequency domain). Avoids invalid STFT problem. AECNN-SM1 significantly outperforms SEGAN and 62-layer GRN on TIMIT, IEEE, and WSJ0 SI-84 datasets. Demonstrates learned phase is better than noisy phase.
- **Pages created**:
  - `raw/papers/pandey-2019-cnn-speech-enhancement-time-domain/full-text.txt` — pdftotext extraction
  - `wiki/sources/pandey-2019-cnn-speech-enhancement-time-domain.md` — source page
  - `wiki/concepts/time-domain-speech-enhancement.md` — time-domain SE concept
  - `wiki/concepts/frequency-domain-loss.md` — frequency-domain loss concept
  - `wiki/concepts/invalid-stft-problem.md` — invalid STFT problem concept
- **Pages updated**:
  - `wiki/entities/ashutosh-pandey.md` — added AECNN contribution, related sources/concepts
  - `wiki/entities/deliang-wang.md` — added AECNN contribution and source link
  - `wiki/concepts/complex-spectrum-mapping.md` — added cross-references to time-domain SE concepts
  - `wiki/index.md` — added 3 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/concepts/index.md` — added 3 concept rows

---

## [2026-06-10] ingest | Deep Feedback Cancellation in Hearing Aids (Lydaki et al. 2026)

- **Source**: `raw/papers/lydaki-2026-deep-feedback-cancellation-hearing-aids/full-text.md` (Zotero: QQE7D6DX)
- **Authors**: Eleftheria Lydaki, Zheng-Hua Tan, Jesper Jensen, Meng Guo
- **Published**: IEEE Trans. Audio, Speech, Lang. Process., 2026, pp. 1-15
- **DOI**: 10.1109/TASLPRO.2026.3700049
- **Summary**: DFC — compact DNN (856K params) for direct feedback-path IR estimation in hearing aids. NESD loss with temporal smoothing (average pooling N=50, exponential smoothing α=0.5) resolves convergence/steady-state trade-off. Two-stage training (synthetic → measured IRs). Outperforms FD-AFC and DeepMFC on speech (PESQ 4.54 vs 4.34/4.35) and music (PEAQ -0.53 vs -2.31/-0.92). MUSHRA 86.13 vs 57.48/37.45. 30x faster convergence after path changes.
- **Pages created**:
  - `raw/papers/lydaki-2026-deep-feedback-cancellation-hearing-aids/full-text.md` — MinerU VLM extraction
  - `wiki/sources/lydaki-2026-deep-feedback-cancellation-hearing-aids.md` — source page
  - `wiki/entities/eleftheria-lydaki.md` — DFC lead author
  - `wiki/entities/zheng-hua-tan.md` — co-author
  - `wiki/entities/meng-guo.md` — co-author
  - `wiki/concepts/deep-feedback-cancellation.md` — DFC concept
  - `wiki/concepts/normalized-euclidean-system-distance.md` — NESD metric/loss
- **Pages updated**:
  - `wiki/entities/jesper-jensen.md` — added DFC contribution
  - `wiki/concepts/hearing-aid-feedback-cancellation.md` — added DFC to deep learning approaches
  - `wiki/concepts/maximum-stable-gain.md` — added DFC source
  - `wiki/concepts/prediction-error-method.md` — added DFC source
  - `wiki/concepts/frequency-shift-feedback-cancellation.md` — added DFC source
  - `wiki/index.md` — added 3 entities, 2 concepts, 1 source; updated statistics
  - `wiki/entities/index.md` — added 3 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-06-18] ingest | HALO: Half-frame-rate Adaptive Learnable Operator (Zhao et al. 2026)

- **Source**: `raw/papers/zhao-2026-halo-half-frame-rate-adaptive-operator/full-text.md` (Zotero: WQLLU8C4)
- **Authors**: Jiadong Zhao, Dahan Wang, Yu Sun, Leyan Yang, Xiaobin Rong, Shiruo Sun, Yuxiang Hu, Jing Lu
- **Published**: arXiv preprint, June 2026
- **DOI**: 10.48550/arXiv.2606.12328
- **Summary**: HALO introduces a causal plug-in module that halves the internal frame rate in STFT-based speech enhancement using adaptive dynamic-convolution-based reduction and restoration operators, reducing backbone compute with no added algorithmic latency.
- **Extraction**: Defuddle (arXiv HTML)
- **Pages created**:
  - `raw/papers/zhao-2026-halo-half-frame-rate-adaptive-operator/full-text.md` — extracted text from arXiv HTML
  - `raw/papers/zhao-2026-halo-half-frame-rate-adaptive-operator/figures/Fig1.png` — overall framework diagram
  - `raw/papers/zhao-2026-halo-half-frame-rate-adaptive-operator/figures/Fig2.png` — rate-reduction operator diagram
  - `wiki/sources/zhao-2026-halo-half-frame-rate-adaptive-operator.md`
  - `wiki/entities/jiadong-zhao.md`
  - `wiki/entities/dahan-wang.md`
  - `wiki/entities/yu-sun.md`
  - `wiki/entities/leyan-yang.md`
  - `wiki/entities/shiruo-sun.md`
  - `wiki/concepts/dynamic-convolution.md`
- **Pages updated**:
  - `wiki/entities/xiaobin-rong.md` — added HALO contribution
  - `wiki/entities/yuxiang-hu.md` — added HALO contribution
  - `wiki/entities/jing-lu.md` — added HALO contribution
  - `wiki/concepts/gtcrn.md` — added HALO as related source
  - `wiki/concepts/spectrogram-analysis.md` — added HALO as related source
  - `wiki/concepts/attention-gate.md` — added dynamic convolution link and HALO source
  - `wiki/index.md` — added 5 entities, 1 concept, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 5 entity rows
  - `wiki/concepts/index.md` — added 1 concept row

---

## [2026-06-19] lint | Health check

- **Index consistency**: All category files and index rows match perfectly: 266 entities, 234 concepts, 103 sources, 19 synthesis, 7 queries = 629 total. No missing entries, phantom entries, or duplicate rows in either main index (`wiki/index.md`) or subdirectory indexes. Statistics section accurate.
- **Broken links**:
  - 171 wikilinks missing category prefix; all resolve to existing wiki pages when the correct category is prepended (e.g., `[[beamforming]]` → `[[concepts/beamforming]]`). Breakdown: 662 in concepts, 64 in entities, 24 in sources, 16 in synthesis, 3 in queries. Most prevalent in concept and synthesis pages that link to other concepts without the directory prefix.
  - 30 wikilinks incorrectly use `wiki/` prefix (e.g., `[[wiki/concepts/beamforming]]` instead of `[[concepts/beamforming]]`). Found across 12 distinct source pages.
  - 38 convention violations using `../` relative prefixes (e.g., `[[../concepts/foo]]`). These resolve correctly in MkDocs but violate the vault-absolute convention from `schema/AGENTS.md`. Spread across 20 distinct pages.
  - 1 template placeholder (`[[concepts/concept-name]]` in `synthesis/llm-wiki-best-practices.md`).
  - 25 figure embed wikilinks (`[[raw/papers/…/figures/…]]`) — files exist on disk as raw assets, correctly referenced via Obsidian vault-absolute paths.
  - 17 log.md informal references using human-readable names (expected — these are not actual wikilinks).
- **Duplicate entries**: None found in any index.
- **Orphan pages**: 1 — `sources/why-mathematica-not-simplify-sinh-arccosh` has zero inbound references from any wiki page.
- **Statistics**: All stated counts match actual file counts exactly (629 total, 266 entities, 234 concepts, 103 sources, 19 synthesis, 7 queries). Last updated 2026-06-19.
- **Actions taken**: No index rebuild needed (all counts consistent). Results logged.

---

## [2026-06-19] ingest | G-MaP-SE: Guided Speech Enhancement via GMM-Based Prior Matching (Zhu et al. 2026)

- **Source**: `raw/papers/zhu-2026-g-map-se-guided-speech-enhancement/full-text.md` (Zotero: N5AZRUJV)
- **Authors**: Yike Zhu, Ziqian Wang, Zikai Liu, Xingchen Li, Zhuangqi Chen, Xianjun Xia, Chuanzeng Huang, Lei Xie
- **Published**: Interspeech 2026 (arXiv preprint 2606.08580)
- **DOI**: 10.48550/arXiv.2606.08580
- **Summary**: GMM-based prior matching refines noisy speaker-conditioning embeddings for guided speech enhancement; consistent cross-domain gains on DNS2020 without enrollment audio
- **Pages created**:
  - `raw/papers/zhu-2026-g-map-se-guided-speech-enhancement/full-text.md` — arXiv HTML via Defuddle
  - `raw/papers/zhu-2026-g-map-se-guided-speech-enhancement/figures/x1.png`, `x2.png`, `x3.png` — 3 figures from arXiv HTML
  - `wiki/sources/zhu-2026-g-map-se-guided-speech-enhancement.md`
  - `wiki/entities/yike-zhu.md`
  - `wiki/entities/ziqian-wang.md`
  - `wiki/entities/zikai-liu.md`
  - `wiki/entities/xingchen-li.md`
  - `wiki/entities/zhuangqi-chen.md`
  - `wiki/entities/xianjun-xia.md`
  - `wiki/entities/chuanzeng-huang.md`
  - `wiki/entities/lei-xie.md`
  - `wiki/concepts/speech-enhancement.md`
  - `wiki/concepts/gaussian-mixture-model.md`
  - `wiki/concepts/speaker-embedding.md`
  - `wiki/concepts/prior-matching.md`
  - `wiki/concepts/ecapa-tdnn.md`
  - `wiki/concepts/mp-senet.md`
  - `wiki/concepts/personalized-speech-enhancement.md`
  - `wiki/concepts/voicebank-demand.md`
  - `wiki/concepts/dns-challenge.md`
  - `wiki/concepts/pesq.md`
- **Pages updated**:
  - `wiki/index.md` — added 8 entities, 10 concepts, 1 source; updated statistics to 629 total, 266 entities, 234 concepts, 103 sources
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 8 entity rows
  - `wiki/concepts/index.md` — added 10 concept rows

---

## [2026-06-21] ingest | Han et al. 2026: QuaSE — Quality-Aware Earable Dual-Microphone Speech Enhancement

- **Source**: `raw/papers/han-2026-quality-aware-earable-se/full-text.txt` (extracted via `pdftotext -layout` after MinerU VLM and pipeline failures)
- **Zotero key**: 92AXTWCU
- **DOI**: 10.1145/3810214 (Proc. ACM IMWUT, Vol. 10, No. 2, Article 40, June 2026)
- **Authors**: Feiyu Han (corresponding, NUIST), Dawei Yan (Hebei Univ), Shanyue Wang (HKPU), Jinyang Huang (HFUT), Yuanhao Feng (UEC Japan), Panlong Yang (NUIST)
- **Pages created**:
  - Source: `wiki/sources/han-2026-quality-aware-earable-se.md`
  - Entities (6): `feiyu-han`, `dawei-yan`, `shanyue-wang`, `jinyang-huang`, `yuanhao-feng`, `panlong-yang`
  - Concepts (2): `ear-canal-deformation`, `quality-aware-speech-enhancement`
- **Pages updated**:
  - `wiki/concepts/ear-canal-occlusion-effect.md` — added ECD relationship section and cross-references
  - `wiki/concepts/multi-channel-speech-enhancement.md` — added QuaSE to methods list and related concepts/sources
  - `wiki/concepts/bone-conduction.md` — added section 6 on ECD and in-ear speech quality
  - `wiki/synthesis/multimodal-bc-speech-enhancement.md` — added section 2.8 (Quality-Aware Fusion), benchmark table row, related concepts/sources
  - `wiki/index.md` — added 6 entities, 2 concepts, 1 source; updated statistics (629→638 total, 266→272 entities, 234→236 concepts, 103→104 sources)
  - `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added corresponding rows
- **Key insights**: ECD (articulatory-gesture-induced ear canal deformation) causes air pressure imbalance in sealed ear canal, degrading in-ear speech quality via stuck-at-low microphone fault. QuaSE addresses this with self-supervised quality assessment (autoencoder trained on high-quality samples selected by spectral peak-to-valley matching + DTW) and dynamic quality-weighted fusion. QA module is modular and improves EarSpeech by up to +5.48% PESQ. Distinct from Liu 2025 ATFA (binary sensor failure) — QuaSE handles continuous quality variations.
- **Build verification**: `uv run mkdocs build --strict` passed (exit 0, 32.11s, no WARNINGs)

---

## [2026-06-21] ingest | He 2025: A Brief History of Visual Object Detection (NeurIPS 2025 Talk, Bilibili video)

- **Source**: Bilibili video [BV1nckaBcEra](https://www.bilibili.com/video/BV1nckaBcEra/) — "恺明老师带你看完视觉目标检测30年 | NeurIPS 2025 | 何恺明 | Kaiming He | 原创中英字幕", uploaded by 京口先生 (2026-01-19, ~26:26)
- **Original talk**: "A Brief History of Visual Object Detection", Test of Time Award Presentation, NeurIPS 2025, by Kaiming He (MIT / Google DeepMind)
- **Award context**: Faster R-CNN (Ren, He, Girshick, Sun, 2015) won the NeurIPS 2025 Test of Time Award
- **Slides**: https://people.csail.mit.edu/kaiming/neurips2025talk/neurips2025_fasterrcnn_kaiming.pdf
- **Sourcing note**: Video transcript not directly accessible (Bilibili subtitle API requires auth). Content reconstructed from Bilibili metadata + verified reporting article (机器之心, 2025-12-11), cross-checked against official slides and Kaiming He's homepage.
- **Raw materials**: `raw/articles/kaiming-he-2025-neurips-object-detection/` (bilibili-metadata.json, talk-summary.md)
- **Pages created**:
  - Source: `wiki/sources/kaiming-he-2025-neurips-object-detection-history.md`
  - Entity: `wiki/entities/kaiming-he.md` (new domain: computer vision)
  - Concepts (2): `object-detection`, `faster-r-cnn`
- **Pages updated**: `wiki/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added entries; statistics 638→642 total, 272→273 entities, 236→238 concepts, 104→105 sources
- **Key insights**: 30-year history of object detection across three eras — (1) hand-crafted features + classifiers (Viola-Jones, SIFT, HOG, DPM), (2) CNN-based region classification (AlexNet, R-CNN), (3) end-to-end proposal+detection networks (SPP-Net→Fast R-CNN→Faster R-CNN). Central lessons: feature learning replaced feature engineering; shared computation (SPP-Net→Fast R-CNN→Faster R-CNN's RPN) drove the speed evolution. Faster R-CNN's RPN unified proposal generation and detection into a jointly-trainable framework, defining the modern paradigm.
- **Build verification**: `uv run mkdocs build --strict` passed (exit 0, 36.76s, no WARNINGs)

---

## [2026-06-21] ingest | Lorenz & Boyd 2005: Robust Minimum Variance Beamforming

- **Source**: Lorenz, R. G. & Boyd, S. P. (2005). "Robust Minimum Variance Beamforming." IEEE Transactions on Signal Processing, 53(5), 1684–1696. DOI: [10.1109/TSP.2005.845436](https://doi.org/10.1109/TSP.2005.845436). Zotero key: `I5RQB5AR`.
- **Raw material**: `raw/papers/lorenz-2005-robust-minimum-variance-beamforming/full-text.md` (MinerU VLM extraction with figures/), PDF retrieved from Zotero attachment.
- **Pages created**:
  - Source: `wiki/sources/lorenz-2005-robust-minimum-variance-beamforming.md`
  - Entities (2): `robert-g-lorenz`, `stephen-boyd`
  - Concepts (3): `robust-minimum-variance-beamforming`, `ellipsoidal-uncertainty-modeling`, `hadamard-product-ellipsoids`
- **Pages updated**: `mvdr-beamformer` (added Capon alias, mismatch-sensitivity section, RMVB link), `diagonal-loading` (added RMVB comparison section), `socp-optimization` (added robust-beamforming role + standard form), `beamforming` (added "Robust Beamforming with Ellipsoidal Uncertainty" section)
- **Indexes updated**: `wiki/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added entries; statistics 642→648 total, 273→275 entities, 238→241 concepts, 105→106 sources
- **Key insights**: (1) The RMVB enforces $\mathbf{Re}\,w^* a \geq 1$ over an entire ellipsoidal uncertainty set rather than at a single nominal direction; the semi-infinite constraint becomes a second-order cone constraint via Cauchy–Schwarz. (2) The SOCP reduces to a scalar secular equation in the Lagrange multiplier $\lambda$, solvable by quadratically-convergent Newton iteration (~7–10 steps, size-independent), giving ~12× the cost of a regularized beamformer. (3) For isotropic uncertainty the RMVB coincides (up to scale) with diagonal loading; for anisotropic uncertainty it strictly dominates by exploiting directional manifold-variation knowledge. (4) Novel Hadamard-product-of-ellipsoids calculus (real: 3-term Minkowski sum; complex: 6-term, reducible to 5 via Givens rotation) propagates multiplicative gain/phase uncertainties through the signal path. (5) Worst-case SINR 15.63 dB vs 1.85 dB for point-mainbeam constraints in the 10-element ULA experiment; overestimating the ellipsoid preserves the gain guarantee while underestimating risks constraint violation.

---

## [2026-06-25] ingest | Zhang, Ma, Abhayapala, Samarasinghe & Bastine 2024: ANC with PINN-based Soundfield Interpolation

- **Source**: `raw/papers/zhang-2024-active-noise-control-soundfield-interpolation-pinn/full-text.md` (MinerU VLM extraction with figures/), PDF retrieved from Zotero attachment
- **Zotero key**: PYI2K3NS (PDF: 24P8GYCW)
- **DOI**: 10.1109/ICASSP48485.2024.10447208
- **Authors**: Yile (Angela) Zhang, Fei Ma, Thushara D. Abhayapala, Prasanga N. Samarasinghe, Amy Bastine
- **Published**: ICASSP 2024, pp. 506–510
- **Pages created**:
  - `raw/papers/zhang-2024-active-noise-control-soundfield-interpolation-pinn/full-text.md` — extracted text from Zotero PDF
  - `wiki/sources/zhang-2024-active-noise-control-soundfield-interpolation-pinn.md`
  - Entities (5): `yile-angela-zhang`, `fei-ma`, `thushara-d-abhayapala`, `prasanga-n-samarasinghe`, `amy-bastine`
  - Concepts (2): `physics-informed-neural-network`, `soundfield-interpolation`
- **Pages updated**:
  - `wiki/concepts/active-noise-control.md` — added PINN-assisted ANC to Deep Learning Approaches, updated sources frontmatter
  - `wiki/concepts/virtual-sensing.md` — added PINN-based soundfield interpolation method section
  - `wiki/concepts/remote-microphone-technique.md` — updated date
  - `wiki/concepts/multi-channel-anc.md` — added PINN-assisted multi-channel ANC section
  - `wiki/concepts/spherical-harmonic-transform.md` — added PINN comparison section, related concepts/sources
  - `wiki/synthesis/virtual-sensing-evolution.md` — added PINN-based soundfield interpolation section with footnotes
  - `wiki/synthesis/index.md` — updated virtual-sensing-evolution summary and Zotero keys
  - `wiki/index.md` — added 5 entities, 2 concepts, 1 source; updated statistics (648→656 total, 275→280 entities, 241→243 concepts, 106→107 sources)
  - `wiki/entities/index.md` — added 5 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows
  - `wiki/sources/index.md` — added 1 source row
- **Key insights**: (1) Monitoring microphones placed *outside* the ROI give users more movement freedom vs spherical/circular arrays. (2) PINN (1 hidden layer, 16 neurons) trained with wave equation PDE residual + data MSE achieves ~8 dB better soundfield interpolation than SH with Q=8 mics (limiting SH to U=2). (3) PINN-assisted FxLMS ANC achieves −13 dB more steady-state noise reduction than multiple-point ANC by minimizing at virtual ear positions instead of monitoring mic positions. (4) The PINN approach requires no specific array geometry and integrates physical knowledge via automatic differentiation, but requires expensive training ($5 \times 10^5$ epochs).

## [2026-06-25] ingest (re) | Zhang, Ma, Abhayapala, Samarasinghe & Bastine 2024: ANC with PINN-based Soundfield Interpolation (completion)

- **Reason**: Previous ingest (same date) left the source page minimal (44 lines, no Problem Formulation / Methodology / Experimental Setup / Results sections) and the subdirectory indexes `wiki/sources/index.md` and `wiki/entities/index.md` were not actually updated despite the prior log entry claiming so. Re-ingestion completes the workflow per the paper-reader skill template.
- **Pages updated**:
  - `wiki/sources/zhang-2024-active-noise-control-soundfield-interpolation-pinn.md` — expanded from 44 to ~207 lines: added Problem Formulation (Eqs. 1–2), Methodology with Multiple-point ANC, PINN-assisted ANC (loss Eq. 5, wave equation Eq. 6, FxLMS update Eq. 3), and SH interpolation baseline (Eqs. 7–8); full Experimental Setup table; Results with interpolation error (Eq. 9), ANC noise reduction (Eq. 10), and spatial noise field analysis; embedded 3 figures (system setup Fig. 1, block diagram Fig. 2, noise reduction Fig. 4); added Limitations and Future Work section
  - `wiki/sources/index.md` — added the missing 1 source row (was not actually added in prior attempt)
  - `wiki/entities/index.md` — added the missing 5 entity rows for `yile-angela-zhang`, `fei-ma`, `thushara-d-abhayapala`, `prasanga-n-samarasinghe`, `amy-bastine` (were not actually added in prior attempt)
- **Pages verified unchanged** (already correctly updated in prior attempt): entity pages, concept pages (`physics-informed-neural-network`, `soundfield-interpolation`), updated concept pages (`active-noise-control`, `multi-channel-anc`, `remote-microphone-technique`, `spherical-harmonic-transform`, `virtual-sensing`), synthesis page `virtual-sensing-evolution.md`, main `wiki/index.md`, `wiki/concepts/index.md`
- **Figures**: 3 embedded (Fig. 1 system setup, Fig. 2 block diagram, Fig. 4 noise reduction) — all sourced from existing `raw/papers/zhang-2024-active-noise-control-soundfield-interpolation-pinn/figures/` (16 figures total from MinerU VLM extraction)
- **Outcome**: Source page now conforms to the paper-reader skill template with all required sections; subdirectory indexes complete and consistent with main index.

## [2026-06-28] ingest (re) | Jiang, Xue & Yue 2025: A Review of Artificial Intelligence-Driven Active Vibration and Noise Control (completion)

- **Reason**: Previous ingest left the source page with gaps — missing raw paper path in frontmatter, empty Related Synthesis section, no raw full-text in standard location, and no entity pages for authors. Re-ingestion completes the workflow per the paper-reader skill template.
- **Source**: `raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md` (Zotero: B6G9D6NQ)
- **Authors**: Zongkang Jiang, Hongtao Xue, Huiyu Yue
- **Published**: Machines 2025, 13(10), 1027
- **DOI**: 10.3390/machines13101027
- **Summary**: Comprehensive 48-page review classifying AI-AVNC into four technical paths (input shaping, system identification, controller parameter optimization, end-to-end controller modeling) with engineering applications in EVs, aerospace, and manufacturing
- **Extraction**: MinerU pipeline extract from Zotero PDF (191,690 bytes, 40 figures)
- **Pages created**:
  - `raw/papers/jiang-2025-ai-driven-avnc-review/full-text.md` — extracted text from Zotero PDF via MinerU
  - `raw/papers/jiang-2025-ai-driven-avnc-review/figures/` — 40 extracted figures
  - `wiki/entities/zongkang-jiang.md` — first author
  - `wiki/entities/hongtao-xue.md` — co-author, supervisor
  - `wiki/entities/huiyu-yue.md` — corresponding author
  - `wiki/concepts/input-shaping.md` — feedforward control technique
  - `wiki/concepts/reinforcement-learning-for-control.md` — RL for dynamic system control
  - `wiki/concepts/safe-reinforcement-learning.md` — Safe-RL with constraints and guarantees
- **Pages updated**:
  - `wiki/sources/jiang-2025-ai-driven-avnc-review.md` — expanded with raw paper path, DOI, comprehensive methodology (four technical paths), results, future work, limitations, related concepts (15 wikilinks), related synthesis (5 wikilinks)
  - `wiki/concepts/active-vibration-control.md` — added source link, cross-refs to input-shaping, RL-for-control, safe-RL
  - `wiki/concepts/physics-informed-neural-network.md` — added source link, cross-refs to AVC and input-shaping, Related Sources section
  - `wiki/concepts/model-predictive-control.md` — added source link
  - `wiki/concepts/system-identification.md` — added source link, cross-refs to AVC and deep-secondary-path-estimation
  - `wiki/concepts/filtered-x-lms-algorithm.md` — added source link
  - `wiki/concepts/generative-fixed-filter-anc.md` — added source link
  - `wiki/synthesis/ai-driven-anc.md` — added source link and reference to four-path classification
  - `wiki/index.md` — added 3 entities, 3 concepts; updated source summary; updated statistics (656→662 total, 280→283 entities, 243→246 concepts)
  - `wiki/sources/index.md` — updated source summary
  - `wiki/entities/index.md` — added 3 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows
- **Key insights**: (1) AI-AVNC is classified into four technical paths: input shaping (ANN/RL/PINN-enhanced), system identification (deep secondary path estimation), controller parameter optimization (RL-PID, neural MPC), and end-to-end controller modeling (Deep ANC, GFANC). (2) RL methods (DDPG, PPO, SAC) enable model-free nonlinear control but suffer from low sample efficiency and exploration safety risks. (3) Safe-RL frameworks (CMDP, Lyapunov constraints, CBF, conservative fallback) are essential for physical deployment. (4) Deep ANC and GFANC represent the end-to-end paradigm shift, replacing iterative adaptation with neural network inference. (5) Key challenges include sim-to-real gap, lack of interpretability, and need for formal stability verification.

---

## [2026-07-01] ingest | L3C-DeepMFC: Low-Latency Low-Complexity Deep Marginal Feedback Cancellation

- **Source**: `raw/papers/hao-2025-l3c-deepmfc/full-text.md` (Zotero: FDVXMTIJ)
- **Authors**: Fengyuan Hao, Brian C. J. Moore, Huiyong Zhang, Xiaodong Li, Chengshi Zheng
- **Published**: Interspeech 2025
- **URL**: https://www.isca-archive.org/interspeech_2025/hao25_interspeech.pdf
- **Summary**: Proposes L3C-DeepMFC, a low-latency (4ms) low-complexity (0.31M params, 0.43 G/s) extension of DeepMFC for hearing aid feedback cancellation. Uses gain-shape complex spectrum mapping, full- and sub-band recurrent modeling (shared sub-band LSTM + full-band GLSTM), a low-latency overlap-add scheme, and closed-loop fine tuning to address the open-loop-training vs. closed-loop-estimation mismatch. Achieves WB-PESQ 4.08 at GM=0 vs. DeepMFC's 4.34 while using ~32× fewer parameters and ~28× lower complexity.
- **Pages created**:
  - `raw/papers/hao-2025-l3c-deepmfc/full-text.md` — MinerU VLM extraction
  - `wiki/sources/hao-2025-l3c-deepmfc.md` — source page
  - `wiki/entities/brian-c-j-moore.md` — entity page (Cambridge Hearing Group)
  - `wiki/entities/huiyong-zhang.md` — entity page (CAS)
  - `wiki/concepts/deep-marginal-feedback-cancellation.md` — DeepMFC concept
  - `wiki/concepts/closed-loop-fine-tuning.md` — closed-loop fine tuning concept
- **Pages updated**:
  - `wiki/entities/fengyuan-hao.md` — added L3C-DeepMFC contribution
  - `wiki/entities/chengshi-zheng.md` — added L3C-DeepMFC contribution
  - `wiki/entities/xiaodong-li.md` — added L3C-DeepMFC contribution
  - `wiki/concepts/hearing-aid-feedback-cancellation.md` — added DeepMFC subsection + cross-references
  - `wiki/concepts/acoustic-feedback.md` — added related concepts/sources
  - `wiki/concepts/complex-spectrum-mapping.md` — added related concepts/sources
  - `wiki/index.md` — added 2 entities, 2 concepts, 1 source; updated statistics (602/252/223/101/19/7)
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows

---

## [2026-07-03] ingest | Ashur & Cohen 2026: Acoustic Howling Suppression Enhancement by Fine-Tuning Deep Speech Enhancement Networks

- **Source**: `raw/papers/ashur-2026-acoustic-howling-suppression-fine-tuning/full-text.md` (Zotero: HRHUQQER)
- **Authors**: Avichay Ashur, Israel Cohen
- **Published**: Preprint, 2026 (hosted on israelcohen.com, May 2026)
- **URL**: https://israelcohen.com/wp-content/uploads/2026/05/Enhancing_Acoustic_Howling_Suppression_Robustness_in_Deep_Speech_Enhancement_Networks.pdf
- **Summary**: Fine-tunes a pretrained DEMUCS-based real-time Denoiser network for acoustic howling suppression by mixing offline-generated synthetic howling samples (AISHELL-2 + image-method RIRs + hard-clipping loudspeaker nonlinearity) with the original Valentini-Botinhao noise-reduction data. The 60-40 mixing ratio achieves state-of-the-art perceptual speech quality (PESQ) at higher gains with the most stable PESQ across gain levels (only ~0.05 drop from G=1.5 to G=3 vs 0.5-0.6 for HybridAHS/NKal-AHS), while preserving <1% PESQ and <2% SDR of the original noise-reduction capability. No architectural modification, no recursive training, no additional inference latency.
- **Extraction**: MinerU VLM extract from Zotero PDF (30,167 bytes, 9 figures) - second extraction attempt after first produced truncated output.
- **Pages created**:
  - `raw/papers/ashur-2026-acoustic-howling-suppression-fine-tuning/full-text.md` - extracted text from Zotero PDF via MinerU
  - `raw/papers/ashur-2026-acoustic-howling-suppression-fine-tuning/figures/` - 9 extracted figures
  - `wiki/sources/ashur-2026-acoustic-howling-suppression-fine-tuning.md`
  - `wiki/entities/avichay-ashur.md`
  - `wiki/concepts/denoiser-network.md` - DEMUCS-based real-time speech enhancement baseline
- **Pages updated**:
  - `wiki/entities/israel-cohen.md` - added AHS fine-tuning contribution, related sources/entities/concepts, updated `updated` date and tags
  - `wiki/concepts/acoustic-howling-suppression.md` - added DeepMFC and Denoiser fine-tuning entries to Deep Learning Approaches; updated sources frontmatter; added cross-refs to denoiser-network and speech-enhancement
  - `wiki/index.md` - added 1 entity, 1 concept, 1 source; updated statistics (662->665 total, 283->284 entities, 246->247 concepts, 107->108 sources)
  - `wiki/sources/index.md` - added 1 source row
  - `wiki/entities/index.md` - added 1 entity row
  - `wiki/concepts/index.md` - added 1 concept row
- **Key insights**: (1) Acoustic howling suppression and speech enhancement can be jointly addressed within a single pretrained network via fine-tuning - howling data acts as a complementary signal alongside noise-reduction data rather than the sole supervision signal (unlike DeepMFC). (2) The howling/noise mixing ratio is the key trade-off knob: ratios up to 60% preserve noise-reduction performance (<1% PESQ drop, <2% SDR drop) while substantially improving AHS robustness; excessive ratios (75-25) bias the model toward narrowband feedback suppression at the expense of broadband speech reconstruction. (3) The proposed approach achieves the most stable PESQ across gain levels among all evaluated AHS methods (DeepMFC, DeepAHS, HybridAHS, Neural-KG, NKal-AHS, Hybrid-NN), with only ~0.05 PESQ drop from G=1.5 to G=3 versus 0.5-0.6 for HybridAHS/NKal-AHS. (4) Dedicated feedback-cancellation methods (Hybrid-NN) still achieve higher SDR, suggesting residual distortion reduction as a future improvement direction. (5) The fine-tuning strategy requires no architectural modification, no recursive/teacher-forced training, and introduces no additional inference latency - making it a practical drop-in for real-time audio systems.

---

## [2026-07-07] ingest | Rath & Geier 2026: Minimum Required Delay for Realtime Block Size Adaptation in Digital Audio Signal Processing

- **Source**: `raw/papers/rath-2026-minimum-delay-block-size/full-text.txt` (Zotero: 9W3D99QX)
- **Authors**: Matthias Rath, Matthias Geier
- **Published**: Linux Audio Conference 2026 (LAC 2026), Berlin
- **URL**: https://linuxaudioconference.org/2026/papers/mrath.pdf
- **Summary**: Derives a closed-form formula for the minimum delay Δ = b_plugin − gcd(b_host, b_plugin) required when a host and plugin operate with different block sizes b_host and b_plugin in realtime audio processing. The bound replaces the PortAudio brute-force algorithm which iterates up to LCM(b_host, b_plugin) combinations with O(1) computation via Euclidean GCD. Tightness is proven using Bézout's identity from elementary number theory (gcd(a,b) can be expressed as an integer linear combination of a and b).
- **Extraction**: pdftotext fallback after MinerU produced incomplete 117-byte output (67KB full-text.txt extracted successfully).
- **Pages created**:
  - `raw/papers/rath-2026-minimum-delay-block-size/full-text.txt` - extracted text from Zotero PDF via pdftotext
  - `wiki/sources/rath-2026-minimum-delay-block-size.md` - source summary page with full derivation
  - `wiki/entities/matthias-rath.md` - first author (Institute for Advanced Procrastination, Berlin)
  - `wiki/entities/matthias-geier.md` - co-author (ai-coustics / Fraunhofer IIS)
  - `wiki/concepts/block-size-adaptation.md` - reblocking problem and minimum delay formula
  - `wiki/concepts/ring-buffer.md` - circular FIFO data structure for audio buffering
  - `wiki/concepts/greatest-common-divisor.md` - GCD and Euclidean algorithm
  - `wiki/concepts/bezouts-identity.md` - number theory foundation for tightness proof
  - `wiki/concepts/audio-latency.md` - latency sources in audio systems
  - `wiki/concepts/fifo-queue.md` - first-in-first-out queue abstract data type
- **Pages updated**:
  - `wiki/index.md` - added 2 entities, 6 concepts, 1 source to respective tables
  - `wiki/sources/index.md` - added source entry
  - `wiki/entities/index.md` - added 2 entity entries
  - `wiki/concepts/index.md` - added 6 concept entries
- **Key insights**: (1) For block-based realtime audio processing where the host delivers b_host samples per callback and the plugin processes b_plugin samples per callback, the minimum FIFO buffering delay is exactly Δ = b_plugin − gcd(b_host, b_plugin) samples — not b_host + b_plugin, not max(b_host, b_plugin), and not dependent on LCM. (2) The bound is tight: for any two coprime block sizes (gcd = 1), the minimum delay is b_plugin − 1 samples, meaning one nearly-full plugin block must be buffered. For integer multiples (gcd = b_plugin when b_plugin divides b_host), the minimum delay is 0 — no extra reblocking delay needed, the host block contains an integer number of plugin blocks. (3) The elegant proof uses a pigeonhole argument combined with Bézout's identity: congruence classes modulo g repeat every GCD positions, and a linear combination achieving the GCD guarantees that the buffer occupancy pattern visits the same congruence class within one LCM cycle, proving the upper bound. (4) The PortAudio library previously computed this delay via brute-force simulation up to LCM(b_host, b_plugin) steps (which can be as large as 44,100 × 48,000 / 300 = ~7 million steps for common audio rates); the closed-form GCD computation is O(log min(b_host, b_plugin)) and exact. (5) The result generalizes beyond audio: any block-based streaming system where a producer pushes n samples and a consumer pulls m samples per block must delay at least max(n,m) − gcd(n,m) samples to avoid underruns.

---

## [2026-07-07] lint | Health check

- **Index consistency**: Main index had 2 missing entities (`robert-g-lorenz`, `stephen-boyd`) and 3 missing concepts (`ellipsoidal-uncertainty-modeling`, `hadamard-product-ellipsoids`, `robust-minimum-variance-beamforming`); subdirectory indexes were all correct. Fixed by adding missing entries to `wiki/index.md`.
- **Statistics**: Stated 665 total (284/247/108/19/7) was stale vs actual 679 (288/255/110/19/7). Corrected all counts and last-updated date.
- **Broken links**: No truly broken links. Convention violations found: ~181 bare-slug wikilinks (missing category prefix), 30 `wiki/`-prefix links, 38 `../`-prefix links, 19 informal log.md refs. Build passes — these are cosmetic, not functional.
- **Duplicate entries**: None found.
- **Orphan pages**: 1 — `sources/why-mathematica-not-simplify-sinh-arccosh` (zero inbound references).
- **Content fix**: Merged duplicate `## Related Concepts` heading in `wiki/concepts/hearing-aid-feedback-cancellation.md` (leftover from rebase conflict resolution).
- **Build**: `uv run mkdocs build --strict` passes clean (0 warnings, exit 0).
- **Actions taken**: Added 5 missing index entries to `wiki/index.md`; corrected statistics; merged duplicate heading; verified all indexes now match actual files (diff=0 across all categories).

---

## [2026-07-09] ingest | Joint Covariance and WNG Learning for Robust MVDR (Deng et al. 2026)

- **Source**: `raw/papers/deng-2026-joint-covariance-wng-mvdr/full-text.md` (arXiv HTML extraction via defuddle, Zotero unavailable)
- **Authors**: Yongyi Deng, Hanchen Pei, Jianbo Ma, Gongping Huang, Jingdong Chen, Jacob Benesty
- **Published**: INTERSPEECH 2026
- **URL**: https://arxiv.org/abs/2606.24137 (arXiv:2606.24137)
- **Summary**: Proposes an end-to-end data-driven robust MVDR beamforming framework with a dual-branch neural network that jointly learns (1) complex time-frequency masks for spatial covariance matrix estimation and (2) frequency-dependent White Noise Gain (WNG) thresholds for robustness control. A differentiable robust MVDR layer implements the closed-form WNG-constrained solution, enabling end-to-end training via MAE reconstruction loss without explicit WNG supervision.
- **Extraction**: arXiv HTML (2606.24137) parsed via defuddle to markdown; 2 figures downloaded and converted to local embed wikilinks; Zotero bypassed due to local API unavailability.
- **Pages created**:
  - `raw/papers/deng-2026-joint-covariance-wng-mvdr/full-text.md` — extracted markdown text with corrected local image links
  - `raw/papers/deng-2026-joint-covariance-wng-mvdr/figures/` — 2 downloaded figures (fig1.png, fig2.png)
  - `wiki/sources/deng-2026-joint-covariance-wng-mvdr.md` — source summary page
  - `wiki/entities/yongyi-deng.md` — first author (Wuhan University)
  - `wiki/entities/hanchen-pei.md` — co-author (Wuhan University)
  - `wiki/entities/jianbo-ma.md` — co-author (Dolby Laboratories)
- **Pages updated**:
  - `wiki/entities/gongping-huang.md` — added this paper to notable contributions and related sources
  - `wiki/entities/jingdong-chen.md` — added this paper to notable contributions and related sources
  - `wiki/entities/jacob-benesty.md` — added this paper to notable contributions and related sources
  - `wiki/concepts/robust-minimum-variance-beamforming.md` — added Data-Driven Approaches section with the frequency-adaptive learnable WNG scheme; fixed bare-slug links in related concepts
  - `wiki/concepts/neural-beamforming.md` — added Differentiable robust MVDR layer entry to end-to-end approaches section
  - `wiki/concepts/white-noise-gain.md` — added Data-Driven WNG Estimation section; fixed bare-slug links in related concepts to use vault-absolute category prefixes; added new related concepts/sources
  - `wiki/index.md` — added 3 entities, 1 source; updated statistics (679→683 total, 288→291 entities, 110→111 sources; last updated 2026-07-09)
  - `wiki/entities/index.md` — added 3 entity rows
  - `wiki/sources/index.md` — added 1 source row
- **Key insights**: (1) WNG threshold need not be a fixed global hyperparameter — it can be learned per frequency bin jointly with the mask estimator, adapting to local SNR, interference characteristics, and frequency-dependent array sensitivity. (2) The reconstruction loss implicitly regularizes WNG without explicit labels: excessively large WNG causes diagonal loading that reduces interference nulling, while excessively small WNG causes white noise amplification; MAE loss balances these tradeoffs automatically. (3) The orthogonal decomposition h = h_D + Ū h̄ separates the distortionless delay-and-sum component from the adaptive interference-canceling subspace, providing a clean closed-form for the differentiable robust MVDR layer. (4) The method generalizes to unseen microphone spacings (1 cm and 3 cm when trained on 2 cm), achieving +1.4–1.8 dB SNR gain over the optimal fixed-WNG FullSubNet baseline across all array conditions. (5) This work extends the neural beamforming paradigm beyond mask-only SCM estimation to co-optimizing both statistical estimation and robustness regularization in a unified end-to-end framework.

---

## [2026-07-10] ingest | RT-Tango — Real-time Distributed Binaural SE for Low-power Hearing Aids (Benslimane et al. 2026)

- **Source**: `raw/papers/benslimane-2026-rt-tango-binaural-speech-enhancement/full-text.md` (arXiv HTML extraction via defuddle; single figure downloaded locally)
- **Authors**: Zahra Benslimane, Pierre Chouteau, Martyna Poreba, Fabrice Auzanneau, Michal Szczepanski, Fabian Chersi, Romain Serizel
- **Affiliations**: CEA, List (Université Paris-Saclay); LORIA (Université de Lorraine, CNRS, Inria)
- **Published**: arXiv preprint (INTERSPEECH 2026 submission), arXiv:2607.01834
- **URL**: https://arxiv.org/abs/2607.01834
- **Zotero**: Local key 8ZWV2E4T; PDF attachment 5H7GWRF3
- **Summary**: Introduces RT-Tango, a real-time distributed binaural speech enhancement framework for low-power hearing aids that revisits the two-stage Tango architecture with four complementary efficiency mechanisms: (1) ERB-scaled feature compression, (2) grouped recurrent neural network (GRNN) mask estimation with asymmetric grouping (SN=8, MN=2), (3) fixed-rate skipping (FRS) with update rates 1/4 (SN-DNN) and 1/2 (MN-DNN), and (4) asymmetric STFT (32 ms analysis / 8 ms synthesis windows). The strictly causal streaming variant RT-Tango-OS achieves 8 ms algorithmic latency with online recursive SCM estimation (EMA, α=0.995). At 33.4 MMACs/s, RT-Tango is ~6× more efficient than GTCRN at the same 4 ms hop and ~18× cheaper than the Tango baseline, while preserving SE quality and interaural balance (SI-SIR 20.8/24.6 dB left/right).
- **Extraction**: arXiv HTML (2607.01834) parsed via defuddle to markdown; 1 figure downloaded and converted to local embed wikilink.
- **Pages created**:
  - `raw/papers/benslimane-2026-rt-tango-binaural-speech-enhancement/full-text.md` — extracted markdown text with local figure link
  - `raw/papers/benslimane-2026-rt-tango-binaural-speech-enhancement/figures/fig1.png` — downloaded figure
  - `wiki/sources/benslimane-2026-rt-tango-binaural-speech-enhancement.md` — source summary page
  - `wiki/entities/zahra-benslimane.md` — lead author (CEA, List)
  - `wiki/entities/pierre-chouteau.md` — co-author (CEA, List)
  - `wiki/entities/martyna-poreba.md` — co-author (CEA, List)
  - `wiki/entities/fabrice-auzanneau.md` — co-author (CEA, List)
  - `wiki/entities/michal-szczepanski.md` — co-author (LORIA)
  - `wiki/entities/fabian-chersi.md` — co-author (LORIA)
  - `wiki/entities/romain-serizel.md` — senior author (LORIA)
  - `wiki/concepts/distributed-binaural-speech-enhancement.md` — two-device SE with compressed-representation exchange
  - `wiki/concepts/tango-framework.md` — baseline two-stage distributed architecture (SN-DNN → SDW-MWF → exchange → MN-DNN → SDW-MWF)
  - `wiki/concepts/grouped-recurrent-neural-network.md` — partitioned RNN hidden state for O(H²/G) complexity
  - `wiki/concepts/asymmetric-stft.md` — long analysis + short synthesis window decoupling spectral resolution from latency
  - `wiki/concepts/fixed-rate-skipping.md` — temporal sparsification via mask reuse at fixed intervals
- **Pages updated**:
  - `wiki/concepts/multi-channel-wiener-filter.md` — added SDW-MWF section (speech-distortion-weighted variant used in Tango/RT-Tango for the exchanged compressed signal)
  - `wiki/concepts/spatial-covariance-matrix.md` — added Online Recursive SCM Estimation (EMA) section with RT-Tango-OS configuration
  - `wiki/concepts/erb-scale.md` — added Usage in RT-Tango section describing front-end feature compression + inverse ERB mapping
  - `wiki/concepts/gtcrn.md` — added As a Baseline in Distributed Binaural SE section contrasting per-node GTCRN (197.5 MMACs/s, asymmetric L/R) with RT-Tango (33.4 MMACs/s, balanced)
  - `wiki/concepts/multi-channel-speech-enhancement.md` — added Distributed Binaural SE category and related concepts/sources
  - `wiki/index.md` — added 7 entities, 5 concepts, 1 source; updated statistics (683→696 total, 291→298 entities, 255→260 concepts, 111→112 sources; last updated 2026-07-10)
  - `wiki/entities/index.md` — added 7 entity rows
  - `wiki/concepts/index.md` — added 5 concept rows
  - `wiki/sources/index.md` — added 1 source row
- **Key insights**: (1) The Tango distributed two-stage architecture (neural mask → SDW-MWF → compressed exchange → refined mask → SDW-MWF) is highly compressible: ~18× reduction in MMACs/s versus the CNN baseline despite a 4× higher frame rate, because the neural network only guides the spatial filter rather than directly reconstructing the signal. (2) Compressibility is heterogeneous across stages: the Single-Node DNN (SN-DNN) is robust to aggressive grouping (G=8) and high skipping rates (1/4), whereas the Multi-Node DNN (MN-DNN) is more sensitive and requires milder settings (G=2, 1/2), motivating an asymmetric efficiency strategy. (3) Fixed-rate skipping (FRS) outperforms learned skip gates (Skip RNN, TinyLSTM) in this regime — the latter's additional MACs and learned skip dynamics degrade MN-DNN SI-SDR by ~0.7–1.2 dB, while FRS preserves quality within 0.2 dB. (4) The asymmetric STFT (long analysis / short synthesis) decouples spectral resolution from algorithmic latency: 32 ms analysis preserves frequency detail for masking, while an 8 ms asymmetric Hann synthesis window caps latency at 8 ms — halving to 4 ms further reduces latency but degrades quality. (5) Online recursive SCM estimation via EMA (α=0.995, ~31 updates/s) introduces only a slight SI-SDR/SI-SAR drop relative to offline SCMs, preserving SI-SIR and PESQ/STOI competitive with higher-cost baselines — making the streaming variant RT-Tango-OS practical for hearing-aid deployment. (6) The two-stage distributed architecture yields naturally balanced left/right behavior (SI-SIR 20.8/24.6 dB) because both ears share information, unlike per-node GTCRN which is strongly ear-asymmetric (16.6/13.8 dB) — a property important for stable spatial perception in binaural hearing aids.

---

## [2026-07-10] ingest | Don't Listen to Me: Own-Voice Cancellation (Østergaard et al. 2026)

- **Source**: `raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md` (Zotero: 3F6BYI69)
- **Authors**: Mads Østergaard, Alexander Neergaard Zahid, Karl Ulbæk, Andreas Hansen Bagge, Kenny Falkjær Olsen, Rasmus Malik Høegh Lindrup
- **Published**: arXiv preprint, 2026-06-22
- **DOI**: 10.48550/arXiv.2606.23332
- **Summary**: Introduces own-voice cancellation (OVC) — removing an enrolled speaker from a noisy mixture while preserving remaining speech; proposes compute-efficient Mamba-MinGRU architecture at 2 ms algorithmic latency.
- **Pages created**:
  - `raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md` — extracted text via MinerU VLM
  - `wiki/sources/ostergaard-2026-own-voice-cancellation.md`
  - `wiki/entities/mads-ostergaard.md`
  - `wiki/entities/alexander-neergaard-zahid.md`
  - `wiki/entities/karl-ulbaek.md`
  - `wiki/entities/andreas-hansen-bagge.md`
  - `wiki/entities/kenny-falkjaer-olsen.md`
  - `wiki/entities/rasmus-malik-hoegh-lindrup.md`
  - `wiki/concepts/own-voice-cancellation.md`
  - `wiki/concepts/mamba-mingru.md`
  - `wiki/concepts/td-speakerbeam.md`
  - `wiki/concepts/mingru.md`
- **Pages updated**:
  - `wiki/concepts/target-speaker-extraction.md` — added OVC complement section, cross-refs, source link
  - `wiki/concepts/speaker-embedding.md` — added auxiliary encoder architectures section, cross-refs, source link
  - `wiki/concepts/personalized-speech-enhancement.md` — added OVC related task, cross-refs, source link
  - `wiki/concepts/time-domain-speech-enhancement.md` — added Mamba-MinGRU to architecture table, cross-refs, source link
  - `wiki/concepts/linear-recurrent-unit.md` — added MinGRU/Mamba-MinGRU related architectures section, cross-refs, source link
  - `wiki/index.md` — added 6 entities, 4 concepts, 1 source; updated statistics
  - `wiki/entities/index.md` — added 6 entity rows
  - `wiki/concepts/index.md` — added 4 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-07-12] ingest | On the Early History of the Singular Value Decomposition (Stewart 1993)

- **Source**: `raw/papers/stewart-1993-early-history-svd/full-text.md` (Zotero: WKC35DNZ)
- **Author**: G. W. Stewart (University of Maryland, College Park)
- **Published**: SIAM Review, vol. 35, no. 4, pp. 551–566, December 1993
- **DOI**: 10.1137/1035134
- **Summary**: Historical survey of five mathematicians who established the SVD — Beltrami (1873), Jordan (1874), Sylvester (1889) via bilinear forms; Schmidt (1907) and Weyl (1912) via integral equations. Schmidt proved the best rank-k approximation theorem; Weyl provided perturbation theory (Weyl's inequality) and the spectral-norm bound.
- **Extraction**: MinerU pipeline model (OCR) on scanned PDF from Zotero; 741 lines, 62 KB.
- **Pages created**:
  - `raw/papers/stewart-1993-early-history-svd/full-text.md` — extracted text via MinerU pipeline
  - `wiki/sources/stewart-1993-early-history-svd.md`
  - `wiki/entities/g-w-stewart.md`
  - `wiki/entities/eugenio-beltrami.md`
  - `wiki/entities/camille-jordan.md`
  - `wiki/entities/james-joseph-sylvester.md`
  - `wiki/entities/erhard-schmidt.md`
  - `wiki/entities/hermann-weyl.md`
  - `wiki/concepts/singular-value-decomposition.md`
  - `wiki/concepts/eckart-young-theorem.md`
  - `wiki/concepts/spectral-norm.md`
- **Pages updated**:
  - `wiki/index.md` — added 6 entities, 3 concepts, 1 source; updated statistics to 689/294/258/111/19/7
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 6 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows

---

## [2026-07-12] ingest | 详细谈谈DSpark投机解码的原理 (zartbot 2026)

- **Source**: `raw/articles/dspark-speculative-decoding.md` (WeChat article: https://mp.weixin.qq.com/s/RRHg9UCCInSc_zEcIgjNBQ)
- **Author**: zartbot (渣注)
- **Published**: 2026-07-04 (WeChat)
- **Summary**: Code-level walkthrough of DSpark — DeepSeek's open-source speculative decoding framework. Covers: (1) speculative decoding fundamentals (rejection sampling, speedup formula $S=\frac{1+c\gamma\alpha}{1+c\gamma}$); (2) survey of 14 draft-model algorithms across 6 stages (2022–2026: autoregressive → tree → multi-head → MTP → parallel diffusion → causal tree); (3) DSpark deep dive — semi-autoregressive generation (parallel backbone + lightweight Markov/RNN serial head) and confidence-scheduled verification (confidence head + sequential temperature scaling + hardware-aware prefix scheduler); (4) production deployment on DeepSeek-V4 with 60–85% per-user speedup.
- **Extraction**: WeChat HTML downloaded via PowerShell (Defuddle and WebFetch failed due to page size); content extracted from `js_content` div; converted to markdown via custom `_convert_wechat.py` (BeautifulSoup-based, 91 KB output).
- **Pages created**:
  - `raw/articles/dspark-speculative-decoding.md` — converted markdown
  - `wiki/sources/zartbot-2026-dspark-speculative-decoding.md`
  - `wiki/entities/zartbot.md`
  - `wiki/entities/deepseek.md`
  - `wiki/concepts/speculative-decoding.md`
  - `wiki/concepts/dspark.md`
  - `wiki/concepts/dflash.md`
  - `wiki/concepts/eagle-speculative-decoding.md`
  - `wiki/concepts/medusa.md`
  - `wiki/concepts/multi-token-prediction.md`
  - `wiki/concepts/tree-attention.md`
  - `wiki/concepts/specinfer.md`
  - `wiki/concepts/ddtree.md`
- **Pages updated**:
  - `wiki/index.md` — added 2 entities, 9 concepts, 1 source; updated statistics to 701/296/267/112/19/7
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 2 entity rows; fixed pre-existing index drift (missing Hermann Weyl entry from SVD ingest)
  - `wiki/concepts/index.md` — added 9 concept rows

---

## [2026-07-15] ingest | Ma 2027: Robust FFANC with Simultaneous OSPM and OFBPM

- **Source**: `raw/papers/ma-2027-robust-ffanc-online-path-modeling/full-text.md` (extracted via MinerU VLM)
- **Authors**: Yaping Ma, Yegui Xiao (corresponding), Wenyi Wu, Liying Ma, Khashayar Khorasani
- **Published**: *Signal Processing*, Vol. 214, 2027, Art. 110818 — [DOI](https://doi.org/10.1016/j.sigpro.2026.110818)
- **Summary**: Proposes a robust feedforward ANC (FFANC) system that simultaneously performs online secondary-path modeling (OSPM) and online feedback-path modeling (OFBPM). Two key innovations over Ahmed–Akhtar 2013 and Bai 2019: (1) a new FIR supporting filter $H_2(z)$ whose output $y_2(n)$ — a less noisy estimate of the remaining target noise — drives the controller's FXLMS update, the OSPM desired signal, and the AWGN scaling, decoupling the controller from OSPM; (2) a global AWGN scaling driven by $y_2(n)$ instead of the residual error, yielding a lower steady-state scaling factor because the additive noise $v_p(n)$ is excluded. An approximate steady-state analysis gives closed-form expressions for $E[y_2^2(\infty)]$, $G_s(\infty)$, and $E[e^2(\infty)]$. Simulations with synthetic paths, real IIR paths, and a real hybrid-car road-noise recording show the proposed system matches the ideal benchmark (Sys-A, true SP/FBP) within 0.01–2.4 dB and outperforms Ahmed–Akhtar 2013 (Sys-B) by 3–6 dB in NRP while running faster (no divisions or square roots).
- **Pages created**:
  - `wiki/sources/ma-2027-robust-ffanc-online-path-modeling.md` — Source summary page (with Figs. 1 and 4)
  - `wiki/entities/yaping-ma.md` — Entity page for Yaping Ma (Jiangnan University)
  - `wiki/entities/yegui-xiao.md` — Entity page for Yegui Xiao (Prefectural University of Hiroshima)
  - `wiki/entities/wenyi-wu.md` — Entity page for Wenyi Wu (Beijing Aerospace Measurement & Control)
  - `wiki/entities/liying-ma.md` — Entity page for Liying Ma (Concordia University)
  - `wiki/entities/khashayar-khorasani.md` — Entity page for Khashayar Khorasani (Concordia University)
  - `wiki/concepts/online-feedback-path-modeling.md` — New concept page for OFBPM
  - `wiki/concepts/supporting-filter-anc.md` — New concept page for the SF mechanism ($H_1$/$H_2$)
  - `wiki/concepts/auxiliary-noise-scaling.md` — New concept page for AWGN power scheduling strategies
- **Pages updated** (cross-references to the new source):
  - `wiki/concepts/online-secondary-path-modeling.md` — added OFBPM, SF, AWGN-scaling links and Ma 2027 source
  - `wiki/concepts/feedforward-anc.md` — added OSPM/OFBPM/SF/AWGN-scaling links and Ma 2027 source
  - `wiki/concepts/acoustic-feedback.md` — added OFBPM/SF/AWGN-scaling links and Ma 2027 source
  - `wiki/concepts/filtered-x-lms-algorithm.md` — added Ma 2027 source (modified FXLMS using $y_2(n)$)
  - `wiki/concepts/secondary-path-modeling.md` — added OFBPM/SF/AWGN-scaling links and Ma 2027 source
  - `wiki/concepts/active-noise-control.md` — added Ma 2027 source
- **Indexes updated**: `wiki/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` (statistics: 738 total, 317 entities, 279 concepts, 116 sources, 19 synthesis, 7 queries)

---

## [2026-07-16] lint | Health check

- **Index consistency**: All categories consistent. Main index and subdirectory indexes all match actual file counts (entities 317, concepts 279, sources 116, synthesis 19, queries 7). No missing/phantom/duplicate entries.
- **Broken links**: 
  - Truly broken: 45 (1 placeholder `[[concepts/concept-name]]` in synthesis/llm-wiki-best-practices.md; 44 missing figure assets across multiple source pages)
  - Missing category prefix: 184 (bare slugs resolvable to concepts/entities/synthesis)
  - wiki/ prefix: 30
  - ../ prefix convention violations: 38
  - log.md informal refs: 19
- **Duplicate entries**: 0
- **Orphan pages**: 1 — sources/why-mathematica-not-simplify-sinh-arccosh
- **Statistics**: All stated counts match actual (317/279/116/19/7, total 738). Last updated 2026-07-15.
- **Actions taken**: None — informational lint pass. Recommend running wiki-link-fixer/scripts/fix_links.py to bulk-fix the 184 missing-prefix + 30 wiki/-prefix + 38 ../-prefix violations (252 auto-fixable). Truly broken figure refs require manual asset verification.

---

## [2026-07-16] merge | New synthesis: Joint Multi-Task SE & Ultra-Low-Latency Paradigm

- **New synthesis page**: wiki/synthesis/joint-multitask-ultra-low-latency-se.md — merges two proposed themes (joint multi-task SE architectures + ultra-low-latency realtime paradigm) into a single cross-source analysis
- **Sources synthesized (6 + 1 theory)**:
  - wiki/sources/indenbom-2023-deepvqe.md — DeepVQE (AEC+NS+DR, 20ms, shared backbone via cross-attention + CCM)
  - wiki/sources/hao-2025-l3c-deepmfc.md — L3C-DeepMFC (4ms hearing-aid feedback cancellation, 0.31M params)
  - wiki/sources/zhao-2026-halo-half-frame-rate-adaptive-operator.md — HALO (0ms added, plug-in frame-rate accelerator)
  - wiki/sources/ashur-2026-acoustic-howling-suppression-fine-tuning.md — Ashur (0ms added, 60-40 data-mixing fine-tuning for joint NS+AHS)
  - wiki/sources/ostergaard-2026-own-voice-cancellation.md — OVC (2ms, Mamba-MinGRU linear RNN)
  - wiki/sources/benslimane-2026-rt-tango-binaural-speech-enhancement.md — RT-Tango (8ms, ERB+GRNN+FRS+asymmetric STFT)
  - wiki/sources/rath-2026-minimum-delay-block-size.md — Rath & Geier (theoretical lower bound Δ = b_plugin − gcd(b_host, b_plugin))
- **Six key insights**:
  1. Multi-task fusion strategies form a spectrum (shared backbone / task reframing / distributed multi-stage) with distinct latency implications
  2. Latency budget drives a 4-tier algorithmic hierarchy (≥20ms / 8–10ms / 4ms / 2ms / 0ms added)
  3. Linear RNNs / SSMs (Mamba-MinGRU, GRNN) replacing LSTM/ConvTasNet in streaming SE — fills gap in synthesis/computational-efficiency-evolution.md
  4. Temporal redundancy (HALO + FRS) is the new efficiency frontier, orthogonal to backbone slimming
  5. Training-side innovations (cross-attention alignment, closed-loop FT, data-mixing FT, silence-aware SDR loss) match architecture innovations in impact
  6. Rath & Geier formula anchors engineering frontier — algorithmic latency below reblocking floor is masked by host/plugin buffering
- **Indexes updated**: wiki/index.md (synthesis row added), wiki/synthesis/index.md (row added)
- **Statistics updated**: 739 total (317 entities / 279 concepts / 116 sources / 20 synthesis / 7 queries), last updated 2026-07-16

---

## [2026-07-16] ingest | It takes few to TANGO: a quantized distributed model for binaural speech enhancement (Benslimane 2026)

- **Source**: `raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md` (Zotero: FN59JY3C)
- **Authors**: Zahra Benslimane, Pierre Chouteau, Martyna Poreba, Fabrice Auzanneau, Michal Szczepanski, Fabian Chersi, Romain Serizel
- **Published**: arXiv preprint, 2026
- **DOI**: 10.48550/arXiv.2607.08645
- **arXiv**: 2607.08645
- **Summary**: Studies low-precision inference for the TANGO hybrid distributed binaural SE system. Shows the downstream GEVD-based spatial filter compensates for most INT8 quantization-induced mask errors; simplifies TANGO into MN-TANGO (single-stage) and combines W8A8 QAT + ERB + grouped LSTM to reach 4.65 MMAC/s and 0.177 MB.
- **Pages created**:
  - `raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md` — extracted text from Zotero PDF (MinerU VLM)
  - `wiki/sources/benslimane-2026-tango-quantized-distributed.md`
  - `wiki/concepts/mn-tango.md`
  - `wiki/concepts/quantization-aware-training.md`
  - `wiki/concepts/post-training-quantization.md`
  - `wiki/concepts/gevd-spatial-filtering.md`
- **Pages updated**:
  - `wiki/concepts/tango-framework.md` — added MN-TANGO / Quantized TANGO variants; GEVD reference; spatial-filter robustness property
  - `wiki/concepts/grouped-recurrent-neural-network.md` — added MN-TANGO application; non-monotonic grouping effect; 4.65 MMAC/s / 0.177 MB operating point
  - `wiki/concepts/erb-scale.md` — added TANGO-family usage section
  - `wiki/concepts/multi-channel-wiener-filter.md` — added differentiable SDW-MWF for end-to-end training section
  - `wiki/concepts/distributed-binaural-speech-enhancement.md` — added MN-TANGO; hybrid neural-spatial robustness subsection
  - `wiki/entities/zahra-benslimane.md` — added quantized MN-TANGO contribution; LORIA affiliation; quantization research focus
  - `wiki/entities/romain-serizel.md` — added quantized MN-TANGO contribution; GEVD/MWF low-rank 2014 reference
  - `wiki/entities/pierre-chouteau.md` — added quantized MN-TANGO contribution
  - `wiki/entities/martyna-poreba.md` — added quantized MN-TANGO contribution
  - `wiki/entities/fabrice-auzanneau.md` — added quantized MN-TANGO contribution; EEAI 2025 reference
  - `wiki/entities/michal-szczepanski.md` — added quantized MN-TANGO contribution; corrected CEA affiliation
  - `wiki/entities/fabian-chersi.md` — added quantized MN-TANGO contribution; corrected CEA affiliation
  - `wiki/synthesis/computational-efficiency-evolution.md` — added MN-TANGO to the 2026 efficiency frontier (14× compute / 23× memory reduction)
  - `wiki/index.md` — added 4 concepts, 1 source; updated statistics
  - `wiki/concepts/index.md` — added 4 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-07-16] ingest | A Hybrid Approach for Low-Complexity Joint AENR (Shetu 2024)

- **Source**: `raw/papers/shetu-2024-hybrid-low-complexity-aenr/full-text.md` (Zotero: XIPNNJIZ)
- **Authors**: Shrishti Saha Shetu, Naveen Kumar Desiraju, Jose Miguel Martinez Aponte, Emanuel A. P. Habets, Edwin Mabande
- **Published**: IWAENC 2024
- **DOI**: 10.1109/IWAENC61483.2024.10694288
- **Summary**: Low-complexity hybrid AENR using Kalman filter + modified ULCNet; 0.69M params, 0.10 GMACs, suitable for embedded devices
- **Pages created**:
  - `raw/papers/shetu-2024-hybrid-low-complexity-aenr/full-text.md` — extracted text from Zotero PDF via MinerU
  - `wiki/sources/shetu-2024-hybrid-low-complexity-aenr.md`
  - `wiki/entities/shrishti-saha-shetu.md`
  - `wiki/entities/naveen-kumar-desiraju.md`
  - `wiki/entities/jose-miguel-martinez-aponte.md`
  - `wiki/entities/emanuel-habets.md`
  - `wiki/entities/edwin-mabande.md`
  - `wiki/concepts/ulcnet.md`
  - `wiki/concepts/channel-wise-feature-reorientation.md`
  - `wiki/concepts/power-law-compression.md`
- **Pages updated**:
  - `wiki/concepts/acoustic-echo-cancellation.md` — added low-complexity approaches section, ULCNet/KF cross-refs, source link
  - `wiki/concepts/kalman-filter.md` — added partitioned-block KF variant, AEC cross-ref, source link
  - `wiki/concepts/speech-enhancement.md` — added ULCNet and AEC cross-refs, source link
  - `wiki/concepts/complex-ratio-mask.md` — added ULCNet cross-ref, source link
  - `wiki/index.md` — added 5 entities, 3 concepts, 1 source; updated statistics
  - `wiki/entities/index.md` — added 5 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-07-17] ingest | EchoFree: Ultra Lightweight Neural AEC (Li 2025)

- **Source**: `raw/papers/li-2025-echofree-neural-aec/full-text.md` (Zotero: RPUN2SVZ)
- **Authors**: Xingchen Li†, Boyi Kang†, Ziqian Wang, Zihan Zhang, Mingshuai Liu, Zhonghua Fu*, Lei Xie
- **Published**: arXiv preprint, 8 Aug 2025
- **DOI**: 10.48550/arXiv.2508.06271
- **Summary**: EchoFree — ultra-lightweight neural AEC combining partitioned-block FDAKF + U-Net post filter on Bark-scale features + two-stage WavLM SSL training; 278K params / 30 MMACs/s, matches DeepVQE-S on ST FE/NE AECMOS at ~10× lower compute
- **Pages created**:
  - `raw/papers/li-2025-echofree-neural-aec/full-text.md` — extracted text from Zotero PDF via MinerU VLM
  - `wiki/sources/li-2025-echofree-neural-aec.md`
  - `wiki/entities/boyi-kang.md`
  - `wiki/entities/zihan-zhang.md`
  - `wiki/entities/mingshuai-liu.md`
  - `wiki/entities/zhonghua-fu.md`
  - `wiki/concepts/bark-scale-spectral-features.md`
  - `wiki/concepts/u-net-post-filter.md`
  - `wiki/concepts/percepnet-style-neural-post-filter.md`
- **Pages updated**:
  - `wiki/entities/xingchen-li.md` — added EchoFree (equal first author)
  - `wiki/entities/ziqian-wang.md` — added EchoFree
  - `wiki/entities/lei-xie.md` — added EchoFree
  - `wiki/concepts/acoustic-echo-cancellation.md` — added Lightweight/PercepNet-Style Hybrid AEC section with comparison table; cross-refs to new concepts; source link
  - `wiki/concepts/depthwise-separable-convolution.md` — added EchoFree source link
  - `wiki/concepts/sub-pixel-convolution.md` — added EchoFree source link; U-Net post filter cross-ref
  - `wiki/concepts/self-supervised-speech-representation.md` — added Applications in Lightweight AEC (EchoFree) section with two-stage SSL training details; cross-refs; source link
  - `wiki/concepts/erb-scale.md` — added Bark-scale cross-ref; EchoFree source link
  - `wiki/sources/indenbom-2023-deepvqe.md` — added EchoFree cross-ref (DeepVQE-S as upper-bound SOTA comparison)
  - `wiki/sources/shetu-2024-hybrid-low-complexity-aenr.md` — added EchoFree cross-ref; synthesis link
  - `wiki/synthesis/joint-multitask-ultra-low-latency-se.md` — added EchoFree to source list; new "Two-Stage SSL Loss for Lightweight AEC" subsection in Insight 5
  - `wiki/index.md` — added 4 entities, 3 concepts, 1 source; updated statistics (761/326/289/119/20/7)
  - `wiki/entities/index.md` — added 4 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-07-17] ingest | Efficient High-Performance Bark-Scale NN for Residual Echo and Noise Suppression (Seidel 2024)

- **Source**: `raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md` (Zotero: QDIJS9HI)
- **Authors**: Ernst Seidel, Pejman Mowlaee, Tim Fingscheidt
- **Published**: ICASSP 2024, pp. 1–5
- **DOI**: 10.1109/ICASSP48485.2024.10446427
- **Summary**: Hybrid LEC (subband NLMS, oversampled filterbank) + NSNet2-style FC/GRU neural postfilter on 86-band Bark-scale features for joint residual echo + noise suppression; achieves DeepVQE-S-comparable AECMOS at ~10% of the MACs/s (235M vs 2170M), making it realtime-implementable on speakerphones. Bark mapping ablation confirms major improvement in nearend speech preservation.
- **Pages created**:
  - `raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md` — extracted text via MinerU VLM
  - `wiki/sources/seidel-2024-bark-scale-nn-residual-suppression.md`
  - `wiki/entities/ernst-seidel.md`
  - `wiki/entities/tim-fingscheidt.md`
  - `wiki/concepts/nsnet2.md`
  - `wiki/concepts/complex-compressed-mse.md`
  - `wiki/concepts/stft-consistency.md`
  - `wiki/concepts/oversampled-filterbank.md`
  - `wiki/concepts/dtln.md`
- **Pages updated**:
  - `wiki/entities/pejman-mowlaee.md` — added Seidel 2024 paper, updated research focus
  - `wiki/concepts/bark-scale-spectral-features.md` — added Seidel 2024 as source; corrected band count (86 vs 100); added note on citation discrepancy with EchoFree
  - `wiki/concepts/percepnet-style-neural-post-filter.md` — added Seidel 2024 as source; corrected Bark-AEC row in representative-systems table (1.58M/235M/86 bands from original paper); added NSNet2/CCMSE/STFT-consistency/oversampled-filterbank cross-refs
  - `wiki/concepts/acoustic-echo-cancellation.md` — corrected Bark-AEC row in lightweight table; added note on number discrepancy with EchoFree citation; added Seidel 2024 source link
  - `wiki/synthesis/joint-multitask-ultra-low-latency-se.md` — added Seidel 2024 to sources synthesized (2024 efficiency-frontier data point between DeepVQE-S and EchoFree)
  - `wiki/index.md` — added 2 entities, 5 concepts, 1 source; updated statistics (769/328/294/120/20/7)
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 5 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-07-18] ingest | PercepNet Joint Echo Control (Valin 2021)

- **Source**: `raw/papers/valin-2021-percepnet-joint-echo-control/full-text.md` (Zotero: 23HVPLE8)
- **Authors**: Jean-Marc Valin, Srikanth Tenneti, Karim Helwani, Umut Isik, Arvindh Krishnaswamy
- **Published**: arXiv:2102.05245, Feb 2021 (1st place ICASSP 2021 AEC Challenge)
- **arXiv**: 2102.05245
- **Summary**: Hybrid AEC (MDF adaptive filter) + PercepNet-based joint residual echo and noise suppression; 32 ERB bands + pitch coherence + comb filter; 8M 8-bit quantized weights (800M MACs/s, 5.5% CPU); 1st place out of 17 submissions.
- **Pages created**:
  - `raw/papers/valin-2021-percepnet-joint-echo-control/full-text.md` — extracted text from Zotero PDF (MinerU VLM)
  - `wiki/sources/valin-2021-percepnet-joint-echo-control.md`
  - `wiki/entities/jean-marc-valin.md`
  - `wiki/entities/srikanth-tenneti.md`
  - `wiki/entities/karim-helwani.md`
  - `wiki/entities/umut-isik.md`
  - `wiki/entities/arvindh-krishnaswamy.md`
  - `wiki/concepts/percepnet.md`
  - `wiki/concepts/pitch-coherence.md`
  - `wiki/concepts/multidelay-block-frequency-domain-adaptive-filter.md`
  - `wiki/concepts/structured-sparsity.md`
- **Pages updated**:
  - `wiki/concepts/percepnet-style-neural-post-filter.md` — corrected ERB vs Bark discrepancy: original PercepNet uses 32 ERB bands (not Bark); added PercepNet row to representative systems table with MDF front-end, 8M params, 800M MACs/s
  - `wiki/concepts/acoustic-echo-cancellation.md` — added PercepNet row to lightweight AEC table; added note clarifying ERB vs Bark scale usage
  - `wiki/concepts/bark-scale-spectral-features.md` — corrected lineage description: original PercepNet uses ERB, not Bark
  - `wiki/concepts/erb-scale.md` — added "Usage in PercepNet" section documenting 32 ERB bands; added source link
  - `wiki/index.md` — added 5 entities, 4 concepts, 1 source; updated statistics
  - `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added new rows
- **Key discrepancy corrected**: The original PercepNet (Valin 2021) uses the **ERB scale (32 bands)**, NOT the Bark scale. The existing wiki incorrectly characterized the entire "PercepNet-style" lineage as Bark-based. This has been corrected across 4 concept pages. The "PercepNet-style" pattern name refers to the hybrid AEC + perceptual-band neural post filter architecture, not strictly to the Bark scale used by later works (Bark-AEC, EchoFree).

---

## [2026-07-18] ingest | RNN Comprehensive Review (Mienye 2024)

- **Source**: `raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md` (Zotero: 7GY9DG4W)
- **Authors**: Ibomoiye Domor Mienye, Theo G. Swart, George Obaido
- **Published**: Information 2024, 15(9), 517
- **DOI**: 10.3390/info15090517
- **Summary**: Comprehensive review of RNN architectures (basic RNN, LSTM, GRU, BiLSTM, stacked, peephole, ESN, IndRNN) and applications across 7 domains (NLP, speech recognition, time-series forecasting, signal processing, bioinformatics, autonomous vehicles, anomaly detection). Covers innovations: hybrid CNN+RNN, RNN+Transformer, attention, NAS, Adam, gradient clipping. Concludes with challenges in scalability, interpretability, bias, data dependency, generalization.
- **Pages created**:
  - `raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md` — extracted text via MinerU VLM
  - `wiki/sources/mienye-2024-rnn-comprehensive-review.md`
  - `wiki/entities/ibomoiye-domor-mienye.md`
  - `wiki/entities/theo-g-swart.md`
  - `wiki/entities/george-obaido.md`
  - `wiki/concepts/recurrent-neural-network.md`
  - `wiki/concepts/long-short-term-memory.md`
  - `wiki/concepts/gated-recurrent-unit.md`
  - `wiki/concepts/bidirectional-lstm.md`
  - `wiki/concepts/peephole-lstm.md`
  - `wiki/concepts/echo-state-network.md`
  - `wiki/concepts/independently-recurrent-neural-network.md`
  - `wiki/concepts/vanishing-gradient-problem.md`
  - `wiki/concepts/activation-functions.md`
  - `wiki/concepts/attention-mechanism.md`
  - `wiki/concepts/adam-optimizer.md`
  - `wiki/concepts/gradient-clipping.md`
  - `wiki/concepts/neural-architecture-search.md`
- **Pages updated**:
  - `wiki/index.md` — added 3 entities, 13 concepts, 1 source; updated statistics (total=796)
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 3 entity rows
  - `wiki/concepts/index.md` — added 13 concept rows
- **Cross-references**: Source page notes that Valin et al. 2021 (PercepNet) is cited in the review's signal processing section as a representative ESN application — flagging that the review's classification of PercepNet as an ESN is loose (PercepNet uses GRU, not a reservoir).

---

## [2026-07-18] ingest | Embedded Joint AEC and Noise Suppression (Castelli 2024)

- **Source**: `raw/papers/castelli-2025-embedded-joint-aec-ns/full-text.md` (Zotero: MEBK2YDF)
- **Authors**: Francesco Castelli
- **Published**: tinyML Summit, April 22–24, 2024
- **Type**: Industry presentation (NXP, public)
- **Summary**: NXP industrial case study compressing DeepVQE-s through a six-stage pipeline (MobileVQE → parameter cuts → HiFi4 CCM intrinsics → ReLU → MACs pruning → LayerNorm removal) into TinyVQE — 114k params, 0.48 MMACs/frame, 420 KB tensor arena, 2.32 ms / 16 ms frame on a Cadence HiFi4 DSP @ 600 MHz (NXP i.MX RT600 MCU)
- **Pages created**:
  - `raw/papers/castelli-2025-embedded-joint-aec-ns/full-text.md` — MinerU VLM-extracted text from Zotero PDF
  - `wiki/sources/castelli-2025-embedded-joint-aec-ns.md`
  - `wiki/entities/francesco-castelli.md`
  - `wiki/concepts/mobilevqe.md`
  - `wiki/concepts/tinyvqe.md`
- **Pages updated**:
  - `wiki/sources/indenbom-2023-deepvqe.md` — added cross-reference to Castelli (NXP deployment of DeepVQE-s)
  - `wiki/concepts/acoustic-echo-cancellation.md` — added TinyVQE to lightweight AEC table; added MobileVQE/TinyVQE to Related Concepts; added Castelli to Related Sources
  - `wiki/concepts/cross-attention-alignment.md` — added Castelli source (alignment block delay reduced 1 s → 0.25 s across the pipeline)
  - `wiki/concepts/complex-convolving-mask.md` — added Castelli source (CCM rewritten as HiFi4 batched-complex-dot-product intrinsics, halving CCM-stage inference at unchanged quality)
  - `wiki/synthesis/joint-multitask-ultra-low-latency-se.md` — added Castelli row to sources table; added new "Strategy A' — Embedded Compression of a Shared Backbone" subsection documenting the industrial deployment case
  - `wiki/index.md` — added 1 entity, 2 concepts, 1 source; updated statistics (total=800, entities=337, concepts=313, sources=123, synthesis=20, queries=7)
  - `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added corresponding rows

---

## [2026-07-19] ingest | Fast-ULCNet: a fast and ultra low complexity network for single-channel speech enhancement (Larraza & de Koeijer 2026)

- **Source**: `raw/papers/larraza-2026-fast-ulcnet-speech-enhancement/full-text.md` (Zotero: 292A8CGG)
- **Authors**: Nicolás Arrieta Larraza, Niels de Koeijer
- **Published**: ICASSP 2026 (preprint arXiv:2601.14925)
- **DOI**: 10.48550/arXiv.2601.14925
- **Summary**: Fast-ULCNet replaces ULCNet's GRU layers with FastGRNN to halve parameters (0.338M) and reduce RTF by ~34% on embedded ARM targets; identifies and mitigates FastGRNN inference-time state drift on long (>60 s) sequences via Comfi-FastGRNN, a trainable complementary-filter extension.
- **Pages created**:
  - `raw/papers/larraza-2026-fast-ulcnet-speech-enhancement/full-text.md` — extracted text from Zotero PDF via MinerU
  - `wiki/sources/larraza-2026-fast-ulcnet-speech-enhancement.md`
  - `wiki/entities/nicolas-arrieta-larraza.md`
  - `wiki/entities/niels-de-koeijer.md`
  - `wiki/concepts/fastgrnn.md`
  - `wiki/concepts/comfi-fastgrnn.md`
  - `wiki/concepts/fast-ulcnet.md`
- **Pages updated**:
  - `wiki/concepts/ulcnet.md` — added Fast-ULCNet extension section, TF re-implementation baseline numbers, and cross-refs
  - `wiki/concepts/channel-wise-feature-reorientation.md` — added source link
  - `wiki/concepts/power-law-compression.md` — added source link (modified power-law on real/imag STFT)
  - `wiki/concepts/complex-ratio-mask.md` — added source link
  - `wiki/synthesis/joint-multitask-ultra-low-latency-se.md` — added Fast-ULCNet row to sources table; new Insight 7 on training-vs-inference RNN state drift; added open question on long-sequence drift in linear RNNs/SSMs
  - `wiki/index.md` — added 2 entities, 3 concepts, 1 source; updated statistics (total 800→806)
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows

---

## [2026-07-19] ingest | Sixty Years of Frequency-Domain Monaural Speech Enhancement (Zheng 2023)

- **Source**: `raw/papers/zheng-2023-survey-frequency-domain-speech-enhancement/full-text.md`
- **Authors**: Chengshi Zheng, Huiyong Zhang, Wenzhe Liu, Xiaoxue Luo, Andong Li, Xiaodong Li, Brian C. J. Moore
- **Published**: Trends in Hearing, Vol. 27, 2023, pp. 1–52
- **DOI**: 10.1177/23312165231209913
- **Code**: cszheng-ioa/Sixty-years-of-frequency-domain-monaural-speech-enhancement
- **Summary**: Comprehensive 60-year survey of frequency-domain monaural speech enhancement from Schroeder (1965) through 2022 deep-learning architectures. Proposes a five-group taxonomy (Traditional / Hybrid DeepXi / Magnitude-mapping DNN / Complex-spectrum DNN / Decoupling-style DNN) and conducts a unified objective evaluation across 17 representative methods on WSJ+DNS and Voice Bank+DEMAND using PESQ, ESTOI, SDR, DNSMOS, and — uniquely — HASQI/HASPI metrics simulating both normal-hearing and hearing-impaired listeners (audiograms N2 mild, N3 moderate). Key finding: input-feature compression helps normal-hearing but not hearing-impaired listeners; model complexity and SE quality are decoupled (DPCRN at 0.72M params / 0.77 GMAC/s matches larger models).
- **Pages created**:
  - `raw/papers/zheng-2023-survey-frequency-domain-speech-enhancement/full-text.md` — extracted text from Zotero PDF
  - `wiki/sources/zheng-2023-survey-frequency-domain-speech-enhancement.md` — review-paper-structured source page (Taxonomy / Methodology / Applications Survey / Key Contributions / Limitations and Caveats)
  - `wiki/entities/wenzhe-liu.md` — new co-author entity page
  - `wiki/entities/xiaoxue-luo.md` — new co-author entity page
  - `wiki/entities/andong-li.md` — new co-author entity page (decoupling-style architectures focus)
- **Pages updated**:
  - `wiki/entities/chengshi-zheng.md` — appended this survey to existing "Sixty years..." bullet and Related Sources
  - `wiki/entities/huiyong-zhang.md` — appended contribution bullet and Related Sources entry
  - `wiki/entities/xiaodong-li.md` — appended contribution bullet and Related Sources entry
  - `wiki/entities/brian-c-j-moore.md` — inserted contribution bullet in chronological position and Related Sources entry
  - `wiki/concepts/speech-enhancement.md` — added frequency-domain sub-area bullet with taxonomy summary
  - `wiki/concepts/power-law-compression.md` — added paragraph on listener-dependent compression benefit (NH helped, HI not)
  - `wiki/concepts/complex-spectrum-mapping.md` — added cross-reference to survey
  - `wiki/concepts/convolutional-recurrent-network.md` — added cross-reference for CRN family evolution
  - `wiki/concepts/complex-ratio-mask.md` — added sources key and cross-reference for cIRM/masking-vs-mapping comparison
  - `wiki/concepts/bark-scale-spectral-features.md` — added raw source to frontmatter and cross-reference for Bark/ERB-band perceptual features
  - `wiki/concepts/frequency-domain-loss.md` — added cross-reference for loss-function survey and "compensation effect"
  - `wiki/concepts/time-domain-speech-enhancement.md` — added cross-reference as companion survey
  - `wiki/concepts/deep-learning-for-signal-processing.md` — added cross-reference for 60-year migration narrative
  - `wiki/index.md` — added 1 source, 3 entities; updated statistics (810 total)
  - `wiki/sources/index.md`, `wiki/entities/index.md` — added new rows

---

## [2026-07-20] ingest | Ultra Dual-Path Compression for Joint Echo Cancellation and Noise Suppression (Chen et al. 2023)

- **Source**: `raw/papers/chen-2023-ultra-dual-path-compression/full-text.md` (Zotero: VNWWREC6)
- **Authors**: Hangting Chen, Jianwei Yu, Yi Luo, Rongzhi Gu, Weihua Li, Zhuocheng Lu, Chao Weng
- **Published**: Interspeech 2023, pp. 2048–2052
- **DOI**: 10.21437/Interspeech.2023-2302
- **arXiv**: 2308.11053
- **Summary**: Time-frequency dual-path compression on online DPT-FSNet for joint AEC + NS; grid-searched T×F compression ratios 4×–32×, model size held <0.5M params throughout, MACs/s tunable 57M–1822M; dual-path outperforms single-path at 8×–16×; TrainMel + PostNet + DualPath(2×4) matches DeepFilterNet at 1/4 the parameters.
- **Pages created**:
  - `raw/papers/chen-2023-ultra-dual-path-compression/full-text.md` — extracted text from Zotero PDF (MinerU VLM, arXiv HTML fallback after defuddle CLI missing from PATH)
  - `wiki/sources/chen-2023-ultra-dual-path-compression.md`
  - `wiki/entities/hangting-chen.md`
  - `wiki/entities/jianwei-yu.md`
  - `wiki/entities/yi-luo.md`
  - `wiki/entities/rongzhi-gu.md`
  - `wiki/entities/weihua-li.md`
  - `wiki/entities/zhuocheng-lu.md`
  - `wiki/entities/chao-weng.md`
  - `wiki/concepts/dpt-fsnet.md`
  - `wiki/concepts/dual-path-compression.md`
  - `wiki/concepts/trainable-frequency-compression.md`
  - `wiki/concepts/frame-skip-prediction.md`
  - `wiki/concepts/post-processing-network.md`
- **Pages updated**:
  - `wiki/concepts/erb-scale.md` — added TrainMel cross-reference and Chen 2023 source
  - `wiki/concepts/bark-scale-spectral-features.md` — added Trainable Frequency Compression cross-reference
  - `wiki/concepts/fixed-rate-skipping.md` — added Frame-Skip Prediction cross-reference (analogous strategy at T-F feature level vs. backbone-invocation level)
  - `wiki/concepts/deep-filtering.md` — added Trainable Frequency Compression cross-reference and Chen 2023 source
  - `wiki/synthesis/joint-multitask-ultra-low-latency-se.md` — added Chen 2023 to sources table; enriched Insight 4 (Temporal Redundancy) with Chen 2023 as 2023 predecessor to HALO/FRS; added new Insight 8 (Compression-Ratio Flexibility as a First-Class Design Axis); added 2 new open questions; added 5 new related concepts
  - `wiki/index.md` — added 7 entities, 5 concepts, 1 source; updated statistics (total 823, entities 349, concepts 321, sources 126)
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 7 entity rows
  - `wiki/concepts/index.md` — added 5 concept rows

---

## [2026-07-21] ingest | CoFi-Lite: Pushing the Limits of Ultra-Lightweight Speech Enhancement (Yang et al. 2026)

- **Source**: `raw/papers/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement/full-text.md` (Zotero: NUV4VYRE)
- **Authors**: Leyan Yang, Dahan Wang, Xiaobin Rong, Jiadong Zhao, Jing Lu
- **Published**: IEEE Signal Processing Letters, 2026
- **DOI**: 10.1109/LSP.2026.3712291
- **Summary**: Ultra-lightweight SE model decoupling spectral modeling into parallel coarse (full-band envelope) and fine (low-frequency detail) paths with Cross-Path Fusion; outperforms GTCRN at 40% of its compute (12.87M MACs/s, 83.12k params)
- **Pages created**:
  - `raw/papers/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement/full-text.md` — extracted text from Zotero PDF (MinerU)
  - `wiki/sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement.md`
  - `wiki/concepts/cofi-lite.md`
  - `wiki/concepts/cross-path-fusion.md`
- **Pages updated**:
  - `wiki/entities/leyan-yang.md` — added this paper (lead author)
  - `wiki/entities/dahan-wang.md` — added this paper
  - `wiki/entities/xiaobin-rong.md` — added this paper
  - `wiki/entities/jiadong-zhao.md` — added this paper
  - `wiki/entities/jing-lu.md` — added this paper
  - `wiki/concepts/gtcrn.md` — added Successors section (CoFi-Lite), cross-refs and source link
  - `wiki/concepts/convolutional-recurrent-network.md` — added CoFi-Lite to Applications and Related Sources
  - `wiki/concepts/ideal-ratio-mask.md` — added dual band-decoupled IRM variant and source link
  - `wiki/synthesis/computational-efficiency-evolution.md` — added CoFi-Lite to 2026 efficiency frontier and Related Sources
  - `wiki/index.md` — added 2 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/concepts/index.md` — added 2 concept rows

---

## [2026-07-21] ingest | Listen first: output-based multi-microphone speech enhancement (Apostolidis 2026)

- **Source**: `raw/papers/apostolidis-2026-listen-first-output-based-multi-microphone/full-text.md` (Zotero: HFEKLBV8)
- **Authors**: Panos Apostolidis, Svend Feldt, Zheng-Hua Tan, Jan Østergaard, Jesper Jensen
- **Published**: arXiv preprint, 2026-07-14
- **DOI**: 10.48550/arXiv.2607.12529
- **Summary**: Proposes an output-based SE paradigm that selects among a dictionary of candidate MPDR beamformers the one whose output maximizes a Glimpse Proportion score; outperforms input-based MVDR baseline, especially at low SNR and under RTF mismatch.
- **Pages created**:
  - `raw/papers/apostolidis-2026-listen-first-output-based-multi-microphone/full-text.md` — extracted text from Zotero PDF (MinerU VLM)
  - `wiki/sources/apostolidis-2026-listen-first-output-based-multi-microphone.md`
  - `wiki/entities/panos-apostolidis.md`
  - `wiki/entities/jan-ostergaard.md`
  - `wiki/concepts/output-based-speech-enhancement.md`
  - `wiki/concepts/glimpse-proportion.md`
- **Pages updated**:
  - `wiki/entities/zheng-hua-tan.md` — added this paper
  - `wiki/entities/jesper-jensen.md` — added this paper
  - `wiki/entities/svend-feldt.md` — added this paper
  - `wiki/concepts/mpdr-beamformer.md` — added "MPDR Rehabilitated via Output-based Selection" section
  - `wiki/concepts/mvdr-beamformer.md` — added "MVDR as Input-based Baseline" section
  - `wiki/concepts/voice-activity-detection.md` — added "Neural VAD as Audibility Estimator" section
  - `wiki/concepts/convolutional-recurrent-network.md` — added audibility-estimation CRN application
  - `wiki/concepts/multi-channel-speech-enhancement.md` — added output-based SE technique and related links
  - `wiki/concepts/beamforming.md` — added "Output-based MPDR Selection" section
  - `wiki/concepts/relative-transfer-function.md` — added "RTF Dictionaries for Output-based Beamformer Selection" section
  - `wiki/index.md` — added 2 entities, 2 concepts, 1 source; updated statistics
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows
  - `wiki/sources/index.md` — added 1 source row
- **Synthesis**: Step 9 skipped per the "when in doubt, prefer not updating" rule — paper introduces a new axis (input vs. output processing) but no existing synthesis page is the right home; creating a new synthesis page from a single paper is not synthesis.

---

## [2026-07-22] ingest | Scarpiniti, Comminiello & Uncini 2027: Physics-informed adaptive filtering for acoustic echo cancellation

**Source**: `raw/papers/scarpiniti-2027-physics-informed-adaptive-filtering-aec/full-text.md` (Zotero: 6PXZWENL)
**Authors**: Michele Scarpiniti, Danilo Comminiello, Aurelio Uncini
**Published**: Signal Processing, 2027
**DOI**: 10.1016/j.sigpro.2026.110819
**Summary**: Introduces Physics-Informed NLMS (PI-NLMS) algorithm for AEC, incorporating RIR structural priors (causality, exponential decay, sparsity, temporal/spectral smoothness, slow variation) via composite stochastic optimization.
**Pages created**:
- `raw/papers/scarpiniti-2027-physics-informed-adaptive-filtering-aec/full-text.md` — extracted text from Zotero PDF
- `wiki/sources/scarpiniti-2027-physics-informed-adaptive-filtering-aec.md`
- `wiki/entities/michele-scarpiniti.md`
- `wiki/entities/danilo-comminiello.md`
- `wiki/entities/aurelio-uncini.md`
- `wiki/concepts/pi-nlms.md`
**Pages updated**:
- `wiki/concepts/acoustic-echo-cancellation.md` — added PI-NLMS to Related Concepts and source to Related Sources
- `wiki/concepts/physics-informed-neural-network.md` — added PI-NLMS to Related Concepts
- `wiki/index.md` — added 1 source, 3 entities, 1 concept; updated statistics
- `wiki/sources/index.md` — added 1 source row
- `wiki/entities/index.md` — added 3 entity rows
- `wiki/concepts/index.md` — added 1 concept row

---

## [2026-07-22] lint | Health check

**Index consistency**: All 5 categories match perfectly (entities 354, concepts 326, sources 129, synthesis 20, queries 7 = 836 total). Zero missing, phantom, or duplicate entries.
**Broken links**: 67 truly broken (mostly figure/image refs, pre-existing); 187 missing category prefix; 30 wiki/ prefix; 38 ../ prefix; 18 log.md informal refs.
**Orphan pages**: 1 orphan (sources/why-mathematica-not-simplify-sinh-arccosh).
**Statistics**: All stated counts match actual files — entities 354, concepts 326, sources 129, synthesis 20, queries 7, total 836.
**Actions taken**: None (lint only, no fixes applied).

---

## [2026-07-22] ingest | Adaptive Convolution for CNN-based Speech Enhancement Models (Wang 2025)

- **Source**: `raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/full-text.md` (Zotero: G3J7XJQF)
- **Authors**: Dahan Wang, Xiaobin Rong, Shiruo Sun, Yuxiang Hu, Changbao Zhu, Jing Lu
- **Published**: IEEE Transactions on Audio, Speech, and Language Processing, 2025
- **DOI**: 10.1109/TASLPRO.2025.3623897
- **Summary**: Proposes adaptive convolution (frame-wise causal dynamic convolution with per-frame attention over K=8 candidate kernels) and AdaptCRN (135K params, 41 MMACs/s, PESQ 2.98 on VCTK-DEMAND); validates generalization across DPCRN/DCCRN/GTCRN/LiSenNet backbones with largest gains on lightweight models; documents CV→SE transfer failures (temperature annealing, softmax).
- **Pages created**:
  - `raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/full-text.md` — extracted text from Zotero PDF (MinerU VLM)
  - `wiki/sources/wang-2025-adaptive-convolution-cnn-speech-enhancement.md`
  - `wiki/concepts/adaptive-convolution.md`
  - `wiki/concepts/adaptcrn.md`
- **Pages updated**:
  - `wiki/entities/dahan-wang.md` — added this paper (lead author)
  - `wiki/entities/xiaobin-rong.md` — added this paper
  - `wiki/entities/shiruo-sun.md` — added this paper
  - `wiki/entities/yuxiang-hu.md` — added this paper
  - `wiki/entities/changbao-zhu.md` — added this paper
  - `wiki/entities/jing-lu.md` — added this paper
  - `wiki/concepts/dynamic-convolution.md` — added adaptive convolution variant to table, applications, cross-refs
  - `wiki/concepts/gtcrn.md` — added AdaptCRN as successor, cross-refs to adaptive-convolution/adaptcrn
  - `wiki/concepts/convolutional-recurrent-network.md` — added AdaptCRN to applications
  - `wiki/concepts/grouped-recurrent-neural-network.md` — added AdaptCRN's grouped-DPRNN variant (rearrangement removed)
  - `wiki/concepts/power-law-compression.md` — added AdaptCRN's 0.3/0.7 exponents and ablation
  - `wiki/concepts/erb-scale.md` — added AdaptCRN's ERB band-merging usage section
  - `wiki/concepts/dprnn.md` — added AdaptCRN's grouped DPRNN bottleneck to related sources
  - `wiki/concepts/adaptive-filtering.md` — added neural counterpart (adaptive convolution) section
  - `wiki/synthesis/computational-efficiency-evolution.md` — added AdaptCRN as 8th Pareto-frontier point introducing the dynamic-capacity axis
  - `wiki/index.md` — added 2 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/concepts/index.md` — added 2 concept rows

---

## [2026-07-23] ingest | High-Selectivity Filter Banks for Spectral Analysis of Music Signals (Diniz et al. 2006)

- **Source**: `raw/papers/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music/full-text.md` (Zotero: HSWGWJQ6)
- **Authors**: Filipe C. C. B. Diniz, Iuri Kothe, Sergio L. Netto, Luiz W. P. Biscainho
- **Published**: EURASIP Journal on Advances in Signal Processing, 2007, Article ID 94704
- **DOI**: 10.1155/2007/94704
- **Summary**: Unified framework for music signal spectral analysis covering FFT, FFB, CQT, and BQT, introducing two novel high-selectivity variants (CQFFB and BQFFB); the BQFFB combines FFT-like low cost, BQT-like piecewise-linear frequency spacing, and FFB-like high selectivity, achieving ~5 orders of magnitude cost reduction over the CQFFB at typical channel counts.
- **Pages created**:
  - `raw/papers/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music/full-text.md` — extracted text from Zotero PDF (MinerU VLM, 451 lines)
  - `wiki/sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music.md`
  - `wiki/entities/filipe-diniz.md`
  - `wiki/entities/iuri-kothe.md`
  - `wiki/entities/sergio-netto.md`
  - `wiki/entities/luiz-biscainho.md`
  - `wiki/concepts/fast-filter-bank.md`
  - `wiki/concepts/constant-q-transform.md`
  - `wiki/concepts/bounded-q-transform.md`
  - `wiki/concepts/constant-q-fast-filter-bank.md`
  - `wiki/concepts/bounded-q-fast-filter-bank.md`
  - `wiki/concepts/frequency-response-masking.md`
- **Pages updated**:
  - `wiki/index.md` — added 1 source, 4 entities, 6 concepts; updated statistics (total 847)
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 4 entity rows
  - `wiki/concepts/index.md` — added 6 concept rows

---

## [2026-07-23] ingest | The Bounded-Q Frequency Transform (Kashima & Mont-Reynaud 1985)

- **Source**: `raw/papers/kashima-1985-bounded-q-frequency-transform/full-text.md` (Zotero: U5AP27SH)
- **Authors**: Kyle L. Kashima, Bernard Mont-Reynaud
- **Published**: Department of Music Report STAN-M-28, CCRMA, Stanford University, 1985
- **URL**: https://www.ee.columbia.edu/~dpwe/papers/KashMR85-bQ-stanm28.pdf
- **Summary**: Introduces the Bounded-Q Transform (BQT) — an FFT-based piecewise-linear approximation to the constant-Q filter bank for polyphonic music transcription; ~3 orders of magnitude faster than the equivalent DFT filter bank.
- **Pages created**:
  - `raw/papers/kashima-1985-bounded-q-frequency-transform/full-text.md` — extracted text from Zotero PDF (MinerU VLM)
  - `wiki/sources/kashima-1985-bounded-q-frequency-transform.md`
  - `wiki/entities/kyle-kashima.md`
  - `wiki/entities/bernard-mont-reynaud.md`
- **Pages updated**:
  - `wiki/concepts/bounded-q-transform.md` — added primary source link, fixed invertibility contradiction (original paper states BQT is invertible due to sharp lowpass cutoff, contradicting prior "non-invertible" claim), expanded Related Sources
  - `wiki/sources/diniz-2006-high-selectivity-filter-banks-spectral-analysis-music.md` — added bidirectional wikilink to the new Kashima 1985 source page
  - `wiki/index.md` — added 2 entities, 1 source; updated statistics
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-07-23] ingest | Frequency-Warped Signal Processing for Audio Applications (Härmä 2000)

- **Source**: `raw/papers/harma-2000-frequency-warped-signal-processing/full-text.md` (Zotero: H64BZGKP)
- **Authors**: Aki Härmä, Matti Karjalainen, Lauri Savioja, Vesa Välimäki, Unto K. Laine, Jyri Huopaniemi
- **Published**: Journal of the Audio Engineering Society, Vol. 48, No. 11, 2000 (November)
- **Zotero**: zotero://select/items/0_H64BZGKP
- **Summary**: Tutorial on frequency-warped DSP — all-pass chain theory, WFIR/WIIR filter design, warped linear prediction, and applications to audio coding, loudspeaker EQ, guitar body modeling, HRTF design, and digital waveguide mesh dispersion correction.
- **Pages created**:
  - `raw/papers/harma-2000-frequency-warped-signal-processing/full-text.md` — extracted text from Zotero PDF (MinerU VLM)
  - `wiki/sources/harma-2000-frequency-warped-signal-processing.md`
  - `wiki/entities/aki-harma.md`
  - `wiki/entities/matti-karjalainen.md`
  - `wiki/entities/lauri-savioja.md`
  - `wiki/entities/vesa-valimaki.md`
  - `wiki/entities/unto-k-laine.md`
  - `wiki/entities/jyri-huopaniemi.md`
  - `wiki/concepts/warped-iir-filter.md`
  - `wiki/concepts/warped-linear-prediction.md`
- **Pages updated**:
  - `wiki/concepts/frequency-warping.md` — added Bark bilinear mapping section, sources, cross-refs to warped-iir-filter and warped-linear-prediction
  - `wiki/concepts/all-pass-filter.md` — added phase/group delay details, role in warped DSP, source link
  - `wiki/concepts/warped-fir-filter.md` — added synthesis/analysis (dewarping) details, expanded advantages, source link
  - `wiki/concepts/erb-scale.md` — added foundational context (ERB vs Bark vs Greenwood comparison), source link
  - `wiki/concepts/bark-scale-spectral-features.md` — added foundational context (Bark bilinear mapping), source link
  - `wiki/index.md` — added 6 entities, 2 concepts, 1 source; updated statistics
  - `wiki/entities/index.md` — added 6 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-07-24] ingest | Liang Wenfeng 2026: Investor Exchange Meeting (Audio Transcript)

- **Source**: `raw/papers/liang-wenfeng-investor-exchange-meeting/full-text.md` (Zotero: KI4HWLYE)
- **Speaker**: Liang Wenfeng (梁文锋), founder of DeepSeek
- **Format**: Audio recording transcript (3h 44min, ~900 lines), recorded 2026-05-20, transcribed 2026-07-16
- **Type**: Primary source — closed-door investor exchange meeting
- **Summary**: First-person strategic disclosures from DeepSeek founder — vision-driven organization, open-source of frontier models as original intent, AGI staircase roadmap (GPT → CoT → Agent → continuous learning → self-iterating singularity → embodied AI), "ten-month payback / 6× profit" API pricing, US–China compute gap (~20k H-equivalent vs. 800B-activation US models), no-KPI/no-formal-structure organization philosophy
- **Pages created**:
  - `raw/papers/liang-wenfeng-investor-exchange-meeting/full-text.md` — extracted text from Zotero PDF (MinerU VLM, language=ch)
  - `wiki/sources/liang-wenfeng-investor-exchange-meeting.md`
  - `wiki/entities/wenfeng-liang.md`
  - `wiki/concepts/agi-roadmap-staircase.md`
  - `wiki/concepts/continuous-learning.md`
  - `wiki/concepts/restraint-as-strategy.md`
- **Pages updated**:
  - `wiki/entities/deepseek.md` — added founder link, new "Strategic Vision (2026 Investor Meeting)" section, and source link in References; added `open-weight` and `agi` tags
  - `wiki/index.md` — added 1 source, 1 entity, 3 concepts; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 1 entity row
  - `wiki/concepts/index.md` — added 3 concept rows
- **Note**: Adapted paper-reader workflow for a non-paper primary source (audio transcript). Slug follows thought-piece precedent (no year, like `karpathy-llm-os` and `jensen-huang-nvidia-moat`). No synthesis page created — existing synthesis pages are audio/speech-focused; deferred per skill guidance ("when in doubt, prefer not updating").

---

## [2026-07-25] ingest | Lightweight Speech Enhancement Guided TSE in Noisy Multi-Speaker Scenarios (Huang et al. 2026)

- **Source**: `raw/papers/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction/full-text.md` (Zotero: UJMWF4E2)
- **Authors**: Ziling Huang, Junnan Wu, Lichun Fan, Zhenbo Luo, Jian Luan, Haixin Guan, Yanhua Long
- **Published**: arXiv preprint 2508.19583, 2026-03-13
- **DOI**: 10.48550/arXiv.2508.19583
- **Summary**: LGTSE/D-LGTSE integrate a lightweight GTCRN denoiser as a front-end for noise-agnostic enrollment guidance and distortion-aware training in target speech extraction, improving SI-SDR by +0.89 dB on Libri2Mix (2-speaker+noise) over SEF-PNet.
- **Pages created**:
  - `raw/papers/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction/full-text.md` — extracted text from Zotero PDF via MinerU VLM
  - `wiki/sources/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction.md`
  - `wiki/entities/ziling-huang.md`
  - `wiki/entities/yanhua-long.md`
  - `wiki/concepts/noise-agnostic-enrollment-guidance.md`
  - `wiki/concepts/distortion-aware-training.md`
  - `wiki/concepts/sef-pnet.md`
  - `wiki/concepts/cie-mdptnet.md`
- **Pages updated**:
  - `wiki/concepts/target-speaker-extraction.md` — expanded enrollment-based methods section with embedding-free sub-families and noise-agnostic guidance; added cross-refs and source link
  - `wiki/concepts/gtcrn.md` — added "Reuse as a TSE Front-end (LGTSE/D-LGTSE)" section; added cross-refs and source link
  - `wiki/index.md` — added 2 entities, 4 concepts, 1 source; updated statistics (total=874)
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 4 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-07-27] ingest | Array-Invariant Speech Enhancement via Geometry-Aware Dynamic Convolution (Liu et al. 2026)

**Source**: Liu, Zhang, Li & Qian 2026 — "Towards Array-Invariant Speech Enhancement via Geometry-Aware Dynamic Convolution" (arXiv preprint)
- Raw: `raw/papers/liu-2026-array-invariant-speech-enhancement/full-text.md` (MinerU extraction)
- DOI: https://doi.org/10.48550/arXiv.2607.18658
- Zotero key: `0_REFWW6J4`

**Key contributions**
- Introduces **Geometry-Aware Dynamic Convolution (Geo-DConv)** — a universal front-end that converts any fixed-array SE backbone (SpatialNet, TF-GridNet) into an array-invariant system by generating geometry-specific convolution kernels from explicit microphone coordinates.
- Introduces **Topology-Aware Coordinate Transformer (TACT)** — a Transformer-Encoder over Fourier-encoded microphone coordinates producing the transformation matrix consumed by Geo-DConv; permutation-equivariant by construction, guaranteeing channel-order invariance.
- Demonstrates that the same learned basis generalizes across microphone counts (4/6/8/12) and array geometries (circular, linear, random), and zero-shot to unseen arrays (CHiME-4 6-mic, trained on RealMAN).
- Reports that fixed-array backbones retrofitted with Geo-DConv match USES2-comp quality at ~10× lower MACs, with negligible overhead (+0.1 M params, +0.09 G/s for SpatialNet).

**Wiki pages created / updated**
- Created: `sources/liu-2026-array-invariant-speech-enhancement`
- Created entities: `wangyou-zhang`, `chenda-li`, `yanmin-qian`
- Updated entity: `zhenglong-liu` (new affiliation SJTU/VUI Labs, new contribution)
- Created concepts: `geometry-aware-dynamic-convolution`, `topology-aware-coordinate-transformer`, `array-invariant-speech-enhancement`
- Updated concepts (cross-links + categorization): `multi-channel-speech-enhancement`, `dynamic-convolution`, `mvdr-beamformer`, `virtual-microphone-estimation`, `geometry-conditioned-ssf`, `doa-microphone-positional-encoding`

**Verification**
- Statistics recounted: 881 total pages (entities=372, concepts=346, sources=136, synthesis=20, queries=7) — verified by `check_statistics.py`.
- `mkdocs build --strict` to be run as final sanity check.

---

## [2026-07-31] ingest | Real-Time Denoising and Dereverberation with Tiny Recurrent U-Net (Choi 2021)

- **Source**: `raw/papers/choi-2021-trunet-real-time-speech-enhancement/full-text.md` (Zotero: CZEIF8BU)
- **Authors**: Hyeong-Seok Choi, Sungjin Park, Jie Hwan Lee, Hoon Heo, Dongsuk Jeon, Kyogu Lee
- **Published**: ICASSP 2021, pp. 5771–5775
- **DOI**: 10.1109/ICASSP39728.2021.9414852
- **Summary**: Lightweight frequency-axis U-Net (TRU-Net, 0.38 M params, 362 KB INT8) with phase-aware β-sigmoid mask (PHM) for single-stage joint denoising and dereverberation at 0 ms lookahead.
- **Pages created**:
  - `raw/papers/choi-2021-trunet-real-time-speech-enhancement/full-text.md` — extracted text from Zotero PDF (MinerU VLM, English)
  - `wiki/sources/choi-2021-trunet-real-time-speech-enhancement.md`
  - `wiki/entities/hyeong-seok-choi.md`
  - `wiki/entities/sungjin-park.md`
  - `wiki/entities/jie-hwan-lee.md`
  - `wiki/entities/hoon-heo.md`
  - `wiki/entities/dongsuk-jeon.md`
  - `wiki/entities/kyogu-lee.md`
  - `wiki/concepts/trunet.md`
  - `wiki/concepts/phase-aware-beta-sigmoid-mask.md`
- **Pages updated**:
  - `wiki/concepts/dereverberation.md` — added PHM quadrilateral row to methods table, cross-referenced TRU-Net and PHM, added source link
  - `wiki/index.md` — added 6 entities, 2 concepts, 1 source; updated statistics (total=890)
  - `wiki/entities/index.md` — added 6 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-07-31] ingest | Per-Channel Energy Normalization: Why and How (Lostanlen et al. 2019)

- **Source**: `raw/papers/lostanlen-2019-pcen-why-and-how/full-text.md` (Zotero: X24LMQYC)
- **Authors**: Vincent Lostanlen, Justin Salamon, Mark Cartwright, Brian McFee, Andrew Farnsworth, Steve Kelling, Juan Pablo Bello
- **Published**: IEEE Signal Processing Letters 26(1), pp. 39–43, January 2019
- **DOI**: 10.1109/LSP.2018.2878620
- **Summary**: Explains why PCEN outperforms logmelspec as an acoustic frontend — it Gaussianizes magnitude distributions and whitens mel-frequency bands (approaching AWGN, theoretically optimal for DNN robustness) — and how it works via asymptotic analysis of temporal integration, AGC, and DRC, with practical parameter guidance
- **Pages created**:
  - `raw/papers/lostanlen-2019-pcen-why-and-how/full-text.md` — extracted text from Zotero PDF (MinerU)
  - `wiki/sources/lostanlen-2019-pcen-why-and-how.md`
  - `wiki/entities/vincent-lostanlen.md`
  - `wiki/entities/justin-salamon.md`
  - `wiki/entities/mark-cartwright.md`
  - `wiki/entities/brian-mcfee.md`
  - `wiki/entities/andrew-farnsworth.md`
  - `wiki/entities/steve-kelling.md`
  - `wiki/entities/juan-pablo-bello.md`
  - `wiki/concepts/per-channel-energy-normalization.md`
- **Pages updated**:
  - `wiki/concepts/spectrogram-analysis.md` — added PCEN cross-ref and source link
  - `wiki/index.md` — added 1 source, 7 entities, 1 concept; updated statistics
  - `wiki/sources/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md` — added rows

---

## [2026-08-01] ingest | PCEN-Based Mask Thresholding and VAD for DNN Speech Enhancement Training (Liu et al. 2025, Dolby patent)

- **Source**: `raw/papers/liu-2025-pcen-mask-vad-speech-enhancement/full-text.md` (Zotero: 9KQXCFTE)
- **Inventors**: Xiaoyu Liu (刘晓宇), R. M. Figin (R·M·菲金, romanized), Cong Zhou (周聪), Kai Li (李凯)
- **Assignee**: Dolby Laboratories Licensing Corporation
- **Publication**: CN 119404249 A (2025-02-07); PCT WO 2023/205240 A1 (2023-10-26)
- **Priority**: US 63/437,273 (2023-01-05); US 63/493,979 (2023-04-03); PCT/CN2022/087983 (2022-04-20)
- **Type**: Patent (invention patent application)
- **Summary**: Dolby patent proposing three training-time-only mechanisms for mask-based DNN speech enhancement: PCEN-based mask thresholding (zeroes IRM on stationary-noise bands of the clean target), PCEN-based VAD (frame-level speech/non-speech from summed band PCEN energies), and a sign-flipped asymmetric loss that preserves speech in speech frames and aggressively suppresses artifacts in non-speech frames. PCEN is used only as a threshold oracle and loss driver, never as a replacement target, and only at training time.
- **Pages created**:
  - `raw/papers/liu-2025-pcen-mask-vad-speech-enhancement/full-text.md` — extracted text from Zotero PDF (MinerU, Chinese)
  - `wiki/sources/liu-2025-pcen-mask-vad-speech-enhancement.md`
  - `wiki/entities/xiaoyu-liu.md`
  - `wiki/entities/cong-zhou.md`
  - `wiki/entities/kai-li.md`
  - `wiki/concepts/per-channel-energy-normalization.md`
- **Pages updated**:
  - `wiki/concepts/voice-activity-detection.md` — added "Training-Time VAD for Loss Gating" section and source link
  - `wiki/concepts/ideal-ratio-mask.md` — added PCEN-thresholded IRM variant and source link
  - `wiki/index.md` — added 3 entities, 1 concept, 1 source; updated statistics
  - `wiki/entities/index.md` — added 3 entity rows
  - `wiki/concepts/index.md` — added 1 concept row
  - `wiki/sources/index.md` — added 1 source row
- **Notes**: R. M. Figin (R·M·菲金) listed as plain text in the source page because the exact English spelling could not be confirmed from the CN patent or the English PCT bibliographic data; the other three inventors use standard pinyin romanizations. No synthesis page updated — the patent reports no comparative benchmarks and its multi-task IRM extension is a training-strategy note rather than a low-latency architecture contribution.

---

## [2026-08-01] ingest | ICCRN: Inplace Cepstral CRN for Monaural Speech Enhancement (Liu & Zhang 2023)

- **Source**: `raw/papers/liu-2023-iccrn/full-text.md` (Zotero: S3KNZA83)
- **Authors**: Jinjiang Liu, Xueliang Zhang
- **Published**: ICASSP 2023, pp. 1–5
- **DOI**: 10.1109/ICASSP49357.2023.10096918
- **Summary**: ICCRN — Inplace Cepstral CRN; augments IGCRN with a Cepstral Frequency Block (FFT-based cepstral-space branch + TF residual). Best STOI at -5 dB on WSJ0 SI-84 (Auditec babble/cafeteria) while being the most compact model in the comparison (0.46 M params, 2.09 G MACs).
- **Pages created**:
  - `raw/papers/liu-2023-iccrn/full-text.md` — extracted text from Zotero PDF (MinerU VLM)
  - `wiki/sources/liu-2023-iccrn.md`
  - `wiki/entities/jinjiang-liu.md`
  - `wiki/concepts/iccrn.md`
  - `wiki/concepts/cepstral-frequency-block.md`
  - `wiki/concepts/cepstral-space-speech-enhancement.md`
- **Pages updated**:
  - `wiki/entities/xueliang-zhang.md` — added ICCRN contribution, tags, related source
  - `wiki/concepts/convolutional-recurrent-network.md` — added ICCRN to CRN family list and Related Sources
  - `wiki/concepts/complex-spectrum-mapping.md` — added ICCRN as Related Source
  - `wiki/concepts/stft-consistency.md` — added ICCRN as Related Source, sources: frontmatter
  - `wiki/index.md` — added 1 entity, 3 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 1 entity row
  - `wiki/concepts/index.md` — added 3 concept rows

---

## [2026-08-01] ingest | IGCRN: Inplace Gated Convolutional Recurrent Neural Network for Dual-channel Speech Enhancement (Liu & Zhang 2021)

- **Source**: `raw/papers/liu-2021-igcrn/full-text.md` (Zotero: PR35K3UL)
- **Authors**: Jinjiang Liu, Xueliang Zhang
- **Published**: Interspeech 2021 (arXiv preprint 2107.11968, 2021-07-26)
- **DOI**: 10.48550/arXiv.2107.11968
- **Summary**: Compact end-to-end dual-channel SE that mirrors the beamforming pipeline (DOA → beamforming → post-filter) inside a CRN; uses inplace convolutions (stride-1 on frequency) and a channel-wise LSTM reused across all frequency bins to preserve per-bin spatial cues. Achieves 1.4M params (vs. GCRN's 71.8M) while outperforming oracle-DOA MVDR and conventional GCRN at -3/0/3 dB on AISHELL-1 + NOISEX-92. Introduces a mask + mapping + phase training target. The downsampling ablation provides direct evidence that the inplace characteristic — not capacity — drives multi-channel SE performance. Predecessor of ICCRN and the foundation of the inplace-CRN family.
- **Pages created**:
  - `raw/papers/liu-2021-igcrn/full-text.md` — extracted text from Zotero PDF (MinerU VLM)
  - `wiki/sources/liu-2021-igcrn.md`
  - `wiki/concepts/igcrn.md`
  - `wiki/concepts/inplace-convolution.md`
  - `wiki/concepts/channel-wise-lstm.md`
  - `wiki/concepts/mask-mapping-amplitude-prediction.md`
- **Pages updated**:
  - `wiki/entities/jinjiang-liu.md` — added IGCRN source link to Related Sources
  - `wiki/entities/xueliang-zhang.md` — added IGCRN source link to Related Sources
  - `wiki/concepts/iccrn.md` — fixed `[[concepts/convolutional-recurrent-network|IGCRN]]` link to point to the new `[[concepts/igcrn|IGCRN]]` concept page; added IGCRN/Inplace-Convolution/Channel-wise-LSTM to Related Concepts; added IGCRN source link to Related Sources; updated lineage section with wikilinks
  - `wiki/concepts/convolutional-recurrent-network.md` — added IGCRN to Applications and Related Sources
  - `wiki/concepts/complex-spectrum-mapping.md` — added IGCRN as Related Source (uses mask+map+phase variant of CSM)
  - `wiki/concepts/multi-channel-speech-enhancement.md` — added IGCRN to Related Sources
  - `wiki/sources/liu-2023-iccrn.md` — added IGCRN as Related Source (predecessor)
  - `wiki/index.md` — added 4 concepts, 1 source; updated statistics (total=913)
  - `wiki/concepts/index.md` — added 4 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-08-01] ingest | SICRN: State Space Model + Inplace Convolution for Speech Enhancement (Zhao, He & Zhang 2024)

- **Source**: `raw/papers/zhao-2024-sicrn/full-text.md` (Zotero: DRNH5RMU; arXiv: 2402.14225)
- **Authors**: Changjiang Zhao, Shulin He, Xueliang Zhang
- **Published**: arXiv preprint, 2024-02-22
- **DOI**: 10.48550/arXiv.2402.14225
- **Summary**: SICRN combines a multidimensional state space model (S4ND) with 2D inplace convolution in a novel SIC block, achieving near-FullSubNet quality on the DNS Challenge at 0.38× params (2.16 M), 0.14× MACs (4.24 G/s), and 0 ms look-ahead. First application of S4ND to monaural SE and the first non-Liu paper in the inplace-CRN lineage from Xueliang Zhang's group.
- **Pages created**:
  - `raw/papers/zhao-2024-sicrn/full-text.md` — extracted text from arXiv HTML (1 figure)
  - `wiki/sources/zhao-2024-sicrn.md`
  - `wiki/entities/changjiang-zhao.md`
  - `wiki/entities/shulin-he.md`
  - `wiki/concepts/sicrn.md`
  - `wiki/concepts/sic-block.md`
  - `wiki/concepts/s4nd.md`
- **Pages updated**:
  - `wiki/entities/xueliang-zhang.md` — added SICRN as senior-author contribution; added `state-space-model` tag
  - `wiki/concepts/inplace-convolution.md` — added SICRN as third use case (first non-Liu/Zhang adoption)
  - `wiki/concepts/igcrn.md` — added SICRN to inplace-CRN lineage; added cross-refs to SIC block / S4ND
  - `wiki/concepts/convolutional-recurrent-network.md` — added SICRN to applications list and Related Sources
  - `wiki/concepts/state-space-model.md` — added Deep-Learning SSM section covering S4ND and Mamba-MinGRU
  - `wiki/concepts/dns-challenge.md` — added SICRN to Related Sources
  - `wiki/index.md` — added 2 entities, 3 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows

---

## [2026-08-01] ingest | SSE-Net: Toward Low-Power-Consumption Spiking Neural Network for Monaural Speech Enhancement (Liu et al. 2026)

- **Source**: `raw/papers/liu-2026-sse-net/full-text.md` (Zotero: DPLD7XGZ)
- **Authors**: Enrui Liu, Andong Li, Cunhang Fan, Chengshi Zheng, Jiangyan Yi, Ruibo Fu, Xinhui Li, Jian Zhou, Zhao Lv
- **Published**: IEEE/ACM TASLP, vol. 34, 2026
- **DOI**: 10.1109/TASLPRO.2026.3677621
- **Summary**: SSE-Net — first spike-native SNN-SE architecture (SFEB/SFEG/ITB blocks designed for spike signals instead of ANN→SNN conversion). SOTA among SNN-based SE models (WB-PESQ 2.89 VB+DEMAND, PESQ 2.65 WSJ0-DNS causal) with 62% lower power proxy than Spiking-FullSubNet (19.70 M Ops/s, 1.31 μJ) and 0.44 G/s MACs (~17× below average ANN baseline). Extracted via MinerU (VLM) after token refresh; no arXiv version.
- **Pages created**:
  - `raw/papers/liu-2026-sse-net/full-text.md` — extracted text from Zotero PDF (4 figures)
  - `wiki/sources/liu-2026-sse-net.md`
  - `wiki/entities/enrui-liu.md`
  - `wiki/entities/cunhang-fan.md`
  - `wiki/entities/jiangyan-yi.md`
  - `wiki/entities/ruibo-fu.md`
  - `wiki/entities/xinhui-li.md`
  - `wiki/entities/jian-zhou.md`
  - `wiki/entities/zhao-lv.md`
  - `wiki/concepts/sse-net.md`
  - `wiki/concepts/spiking-feature-extraction-block.md`
  - `wiki/concepts/information-transformation-block.md`
  - `wiki/concepts/intel-neuromorphic-dns-challenge.md`
- **Pages updated**:
  - `wiki/entities/andong-li.md` — added SSE-Net contribution + related source
  - `wiki/entities/chengshi-zheng.md` — added SSE-Net contribution + related source
  - `wiki/concepts/spiking-neural-networks.md` — added Applications: Speech Enhancement section + source link
  - `wiki/concepts/neuromorphic-computing.md` — added low-power SNN-SE application + source link
  - `wiki/concepts/dns-challenge.md` — added SSE-Net to Related Sources
  - `wiki/concepts/speech-enhancement.md` — added low-power spiking enhancement sub-area + source link
  - `wiki/synthesis/computational-efficiency-evolution.md` — added SSE-Net as fifth (spiking/neuromorphic) efficiency axis in §5.2 frontier + Related Sources
  - `wiki/index.md` — added 1 source, 7 entities, 4 concepts; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 7 entity rows
  - `wiki/concepts/index.md` — added 4 concept rows

---

## [2026-08-02] ingest | Attention-Based Fusion for BC/AC Speech Enhancement (Wang 2022 ICASSP) — comparison only

- **Source**: Zotero key XZMGZG67 (ICASSP 2022 conference paper); not ingested as separate source
- **Authors**: Heming Wang, Xueliang Zhang, DeLiang Wang
- **Published**: ICASSP 2022, pp. 7757–7761
- **DOI**: 10.1109/ICASSP43922.2022.9746374
- **Decision**: Compared against already-ingested TASLP 2022 journal version (`wiki/sources/wang-2022-fusing-bc-ac-complex-domain-se.md`, Zotero K592VRRE). The ICASSP conference paper is a strict methodological subset — same core method (DC-CRN + attention-based fusion + early/late fusion, ESMB corpus). The journal version's only genuine extension is the CycleGAN semi-supervised framework, which was explicitly the conference paper's "future work". Per user decision, skipped full ingestion to avoid a near-duplicate source page.
- **Pages updated**:
  - `wiki/sources/wang-2022-fusing-bc-ac-complex-domain-se.md` — added `related_publications` frontmatter (ICASSP DOI/Zotero key) and a new `## Conference Precursor` section cross-referencing the conference paper; updated `updated:` date
- **Cleanup**: Temporary MinerU extraction at `raw/papers/wang-2022-attention-fusion-bc-ac-icassp/` deleted after comparison.

---

## [2026-08-03] ingest | An Investigation of Incorporating Mamba for Speech Enhancement (Chao et al. 2024)

- **Source**: `raw/papers/chao-2024-mamba-speech-enhancement/full-text.md` (arXiv:2405.06573, Zotero: KTXM4766)
- **Authors**: Rong Chao, Wen-Huang Cheng, Moreno La Quatra, Sabato Marco Siniscalchi, Chao-Han Huck Yang, Szu-Wei Fu, Yu Tsao
- **Published**: IEEE SLT 2024
- **DOI**: 10.1109/SLT61566.2024.10832332
- **Summary**: First application of Mamba (selective SSM) to speech enhancement. Proposes SEMamba in basic (magnitude-mapping) and advanced (MP-SENet-style magnitude-phase) configurations with causal/non-causal and uni-/bi-directional variants. SOTA PESQ 3.69 on VoiceBank-DEMAND with PCS; ~12% FLOPs reduction vs. Conformer at parity quality; 12.22%/12.90% relative WER reduction as Whisper ASR front-end.
- **Pages created**:
  - `raw/papers/chao-2024-mamba-speech-enhancement/full-text.md` — extracted text from arXiv HTML (defuddle)
  - `wiki/sources/chao-2024-mamba-speech-enhancement.md`
  - `wiki/entities/rong-chao.md`
  - `wiki/entities/wen-huang-cheng.md`
  - `wiki/entities/moreno-la-quatra.md`
  - `wiki/entities/sabato-marco-siniscalchi.md`
  - `wiki/entities/chao-han-huck-yang.md`
  - `wiki/entities/szu-wei-fu.md`
  - `wiki/entities/yu-tsao.md`
  - `wiki/concepts/mamba.md` — selective SSM architecture (Gu & Dao 2023)
  - `wiki/concepts/semamba.md` — first Mamba-based SE system
  - `wiki/concepts/perceptual-contrast-stretching.md` — PCS post-processing
- **Pages updated**:
  - `wiki/concepts/state-space-model.md` — added Mamba and SEMamba to Deep-Learning SSM section, related concepts/sources
  - `wiki/concepts/mp-senet.md` — expanded with architecture details, SEMamba as derived system, related concepts/sources
  - `wiki/concepts/voicebank-demand.md` — added standard config, SOTA results table, SEMamba cross-refs
  - `wiki/concepts/pesq.md` — added SOTA progression table on VoiceBank-DEMAND, SEMamba/PCS cross-refs
  - `wiki/concepts/speech-enhancement.md` — added SSM-based SE sub-area, SEMamba/Mamba/PCS related concepts and source
  - `wiki/concepts/s4nd.md` — added Mamba/SEMamba cross-references and source
  - `wiki/concepts/mamba-mingru.md` — added Mamba and SEMamba cross-references
  - `wiki/synthesis/computational-efficiency-evolution.md` — added "Mamba axis for high-quality SE" paragraph, SEMamba to Related Concepts and Sources
  - `wiki/index.md` — added 7 entities, 3 concepts, 1 source; updated statistics
  - `wiki/entities/index.md` — added 7 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-08-03] ingest | Lightweight SE with SSM and DSConv (Jiang et al. 2026)

- **Source**: `raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/full-text.md` (Zotero: WNWMR26M)
- **Authors**: Chen Jiang, Dai Gao, Sirui Wang, Chengxuan Zou, Jie Liu
- **Published**: *Digital Signal Processing* (Elsevier), Vol. 157, 2026-04-15
- **DOI**: 10.1016/j.dsp.2026.105987
- **Summary**: Lightweight SE framework pairing a diagonal-constrained S4 variant ([[concepts/lights4|lightS4]]) with depthwise separable convolutions, an Auditory-Inspired Spectral Compressor ([[concepts/auditory-inspired-spectral-compressor|AISC]]) and a [[concepts/classifier-loss|Classifier Loss]] for vocal-interference suppression. Reaches PESQ 3.32 / STOI 0.96 on VoiceBank+DEMAND and SOTA PESQ 3.01 / STOI 0.87 on WSJ0-SI84 with only 1.65 M params, 0.50 G MACs, RTF 0.13 on consumer CPU — a ~60× MACs reduction vs. SEMamba at a 0.20 PESQ cost. Ablation shows lightS4 is the explicit efficiency–quality compromise (Mamba gives +0.03 PESQ at 1.6× params/1.4× MACs; full S4 NPLR gives -0.10 PESQ).
- **Pages created**:
  - `raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/full-text.md` — MinerU VLM-extracted text (715 lines) + figures
  - `wiki/sources/jiang-2026-lightweight-speech-enhancement-ssm-dsc.md`
  - `wiki/entities/chen-jiang.md`
  - `wiki/entities/dai-gao.md`
  - `wiki/entities/sirui-wang.md`
  - `wiki/entities/chengxuan-zou.md`
  - `wiki/entities/jie-liu.md`
  - `wiki/concepts/lights4.md` — diagonal-constrained S4 variant (novel)
  - `wiki/concepts/auditory-inspired-spectral-compressor.md` — parameter-free ERB-based dimensionality reduction (novel)
  - `wiki/concepts/classifier-loss.md` — auxiliary speaker-classification cross-entropy loss (novel)
- **Pages updated**:
  - `wiki/concepts/state-space-model.md` — added lightS4 bullet to Deep-Learning SSM section; added source link
  - `wiki/concepts/erb-scale.md` — added AISC usage section; added source link and AISC related-concept cross-reference
  - `wiki/concepts/depthwise-separable-convolution.md` — added "Usage in Jiang et al. 2026" section; added lightS4 + AISC cross-references and source link
  - `wiki/synthesis/computational-efficiency-evolution.md` — added 6th Pareto axis entry for lightS4 + DSConv + AISC; added 4 new related concepts and source link
  - `wiki/index.md` — added 5 entities, 3 concepts, 1 source; updated statistics (total=951)
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 5 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows

---

## [2026-08-04] lint | Health check

- **Index consistency**: All categories consistent. Main index and all subdirectory indexes match actual file counts exactly (entities 410/410, concepts 369/369, sources 145/145, synthesis 20/20, queries 7/7). No missing, phantom, or duplicate entries detected by `check_index_drift.py`.
- **Broken links**: 130 truly broken + 278 convention violations.
  - Truly broken: 130 — 1 placeholder `[[concepts/concept-name]]` in `wiki/synthesis/llm-wiki-best-practices.md` + 129 missing `raw/` asset references (image files not extracted/committed for jiang-2025, apostolidis-2026, ashur-2026, benslimane-2026 x2, cai-2024, chao-2024, and others). These need manual attention: delete the placeholder, and either extract the missing figures or convert the embeds to plain-text captions.
  - Missing category prefix: 192 (auto-fixable by `wiki-link-fixer`).
  - `wiki/` prefix: 30 (auto-fixable).
  - `../` prefix violations: 38 (auto-fixable, resolve in MkDocs but violate vault-absolute convention).
  - `log.md` informal refs: 18 (auto-fixable, e.g. `[[AI Assistance and Coding Skills]]` → `[[concepts/ai-assistance-and-coding-skills]]`).
- **Duplicate entries**: 0.
- **Orphan pages**: 1 — `sources/why-mathematica-not-simplify-sinh-arccosh` has zero inbound references from any wiki page, index, or log entry. Consider linking it from a relevant concept page or removing it.
- **Statistics**: All stated counts match actual file counts. Entities 410=410, Concepts 369=369, Sources 145=145, Synthesis 20=20, Queries 7=7, Total pages 951=951. Last updated 2026-08-03.
- **Actions taken**: No index rebuild needed (no drift). Convention violations (278 total: 192 missing-prefix + 30 `wiki/`-prefix + 38 `../`-prefix + 18 log.md refs) are auto-fixable via `wiki-link-fixer` skill but were not applied in this lint pass — run `uv run python .agents/skills/wiki-link-fixer/scripts/fix_links.py --dry-run` to preview, then `fix_links.py` to apply. Truly broken links (130) require manual triage: 1 placeholder to delete, 129 missing figure assets to extract or de-reference.

---

## [2026-08-04] ingest | Synthesis — Deep Speech Enhancement

Created [[synthesis/deep-speech-enhancement|Deep Speech Enhancement]] synthesis page, the umbrella architectural/methodological evolution narrative (2018→2026) tracing deep SE along six near-orthogonal axes:
- **Training target**: pointwise masks (IBM→IRM→cIRM) → complex spectrum mapping → neighborhood filters (CCM, Deep Filtering); CRM = DF with N=1, l=0.
- **Signal domain**: time-domain vs TF-domain converged on hybrid (time-domain arch + frequency loss; Pandey & Wang 2019).
- **Backbone**: CRN → DPCRN/DPRNN → decoupling (CTSNet/G2Net/TaylorSENet) → Conformer/MP-SENet → Mamba/SSM (SEMamba, SICRN) → linear RNN (Mamba-MinGRU) → SNN (SSE-Net).
- **Efficiency**: ~1000× reduction (CRN 17.58M → GTCRN 23.7K → CoFi-Lite 83K/12.87M MACs) via four orthogonal techniques (perceptual band compression, grouped conv+RNN, inplace convolution, adaptive conv).
- **Multi-channel**: estimate-SCM→beamform (Neural VSLF) → end-to-end neural beamforming → array-invariant conditioning (Geo-DConv); output-based SE (Apostolidis 2026) inverts input-centric assumption.
- **Conditioning**: PSE → TSE → OVC (complement); G-MaP-SE refines noisy embeddings via GMM prior matching.
- **Generative**: diffusion (SGMSE+) crossed one-step barrier (ROSE-CD, SBCTM, DriftSE) in 2026, but discriminative SEMamba+PCS still holds SOTA PESQ 3.69.

Synthesizes 16 sources (Tan 2018, Pandey 2019, Schröter 2022, Indenbom 2023, Zheng 2023, Rong 2024, Zhao 2024, Chao 2024, Wang 2025, Zhu 2026, Xu 2026, Yang 2026, Liu 2026, Apostolidis 2026, Østergaard 2026, Huang 2026). Defers multi-modal / joint-multitask / ANC-efficiency sub-topics to existing synthesis pages. Updated `wiki/index.md` and `wiki/synthesis/index.md` Synthesis sections; bumped Synthesis count 20→21 and Total 951→952.

---

## [2026-08-07] ingest | Robust and Early Howling Detection (Mounir 2025)

- **Source**: `raw/papers/mounir-2025-robust-early-howling-detection-sparsity/full-text.md` (Zotero: UNDKU7LR)
- **Authors**: Mina Mounir, Giuliano Bernardi, Toon van Waterschoot
- **Published**: EURASIP Journal on Audio, Speech, and Music Processing, 2025-03-27
- **DOI**: 10.1186/s13636-025-00399-1
- **Summary**: Proposes NINOS²-T, a transposed spectral sparsity howling detection feature that removes candidate-frequency preselection to enable early-howling and ringing detection; introduces a PR-based evaluation procedure for the class-imbalanced HD problem and a larger automatically annotated HD dataset
- **Pages created**:
  - `raw/papers/mounir-2025-robust-early-howling-detection-sparsity/full-text.md` — extracted text via MinerU VLM
  - `wiki/sources/mounir-2025-robust-early-howling-detection-sparsity.md`
  - `wiki/entities/mina-mounir.md`
  - `wiki/entities/giuliano-bernardi.md`
  - `wiki/entities/toon-van-waterschoot.md`
  - `wiki/concepts/howling-detection.md`
  - `wiki/concepts/notch-filter-based-howling-suppression.md`
  - `wiki/concepts/ninosp2-transposed.md`
  - `wiki/concepts/howling-detection-features.md`
- **Pages updated**:
  - `wiki/concepts/acoustic-howling-suppression.md` — expanded Notch Filter section with NHS/NINOS²-T; added cross-refs and source link
  - `wiki/concepts/maximum-stable-gain.md` — added source link (MSG used in HD dataset gain profiling)
  - `wiki/concepts/acoustic-feedback.md` — added source link (Nyquist closed-loop model)
  - `wiki/index.md` — added 3 entities, 4 concepts, 1 source; updated statistics
  - `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added new rows

---

## [2026-08-07] ingest | Fifty Years of Acoustic Feedback Control (van Waterschoot & Moonen 2011)

- **Source**: `raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md` (Zotero: YPB3F9QE)
- **Authors**: Toon van Waterschoot, Marc Moonen
- **Published**: Proceedings of the IEEE, Vol. 99, No. 2, Feb. 2011, pp. 288–327
- **DOI**: 10.1109/JPROC.2010.2090998
- **Summary**: Canonical five-decade survey of automatic acoustic feedback control; formalizes the PA-system closed-loop model and Nyquist stability criterion, proposes the four-category taxonomy (phase modulation, gain reduction, spatial filtering, room modeling), provides an in-depth treatment of PFC/NHS/AFC, and reports the first unified comparative evaluation (ΔMSG, SD, HOP, TRI) crowning AFC-PF (PEM-AFROW) as the practical state of the art.
- **Pages created**:
  - `raw/papers/vanwaterschoot-2011-fifty-years-afc/full-text.md` — MinerU VLM extraction (1403 lines, 16 figures)
  - `wiki/sources/vanwaterschoot-2011-fifty-years-afc.md`
  - `wiki/entities/marc-moonen.md`
  - `wiki/concepts/phase-modulating-feedback-control.md`
  - `wiki/concepts/adaptive-feedback-cancellation.md`
  - `wiki/concepts/decorrelation-for-afc.md`
- **Pages updated**:
  - `wiki/entities/toon-van-waterschoot.md` — added wikilink to the 2011 survey source page
  - `wiki/concepts/acoustic-howling-suppression.md` — added the survey as the foundational AHS taxonomy reference
  - `wiki/concepts/maximum-stable-gain.md` — added the general PA-system MSG definition, Schroeder's statistical bound, and the ~10 dB smoothing-limit distinction
  - `wiki/concepts/howling-detection-features.md` — added the survey as the reference that formalizes the six-feature family
  - `wiki/concepts/notch-filter-based-howling-suppression.md` — converted the plain-text survey mention to a wikilink; added as a source
  - `wiki/concepts/howling-detection.md` — added the survey as the HD-stage reference
  - `wiki/concepts/acoustic-feedback.md` — added the PA-system closed-loop formalization, Nyquist criterion, and four-category taxonomy; cross-refed PFC/AFC/decorrelation
  - `wiki/concepts/frequency-shift-feedback-cancellation.md` — added FS's dual role as a PFC variant and an AFC decorrelator
  - `wiki/concepts/prediction-error-method.md` — added PEM-AFROW as the AFC-PF realization; cross-refed AFC and decorrelation-for-afc
  - `wiki/index.md` — added 1 entity, 3 concepts, 1 source; updated statistics
  - `wiki/sources/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md` — added new rows

---

## [2026-08-07] ingest | System for Elimination of Acoustic Feedback (Williams 2014)

- **Source**: `raw/papers/williams-2014-acoustic-feedback-elimination/full-text.md` (Zotero: BGTSGWNK)
- **Authors**: Paul Robert Williams
- **Published**: U.S. Patent 8,634,575 B2, granted Jan. 21, 2014 (filed Oct. 27, 2009; divisional of Ser. No. 09/658,538 filed Sep. 9, 2000)
- **Assignee**: Harman International Industries Limited (Chester, GB)
- **URL**: https://patents.google.com/patent/US8634575B2/en
- **Summary**: Harman patent for automatic acoustic-feedback elimination in PA/sound-reinforcement systems. Two-rate DSP: audio-rate notch-filter bank + frame-rate (11.7 Hz) analysis. Core novelties are (1) ballistics-based howling detection — an asymmetric per-FFT-bin attack/release filter (gradual attack, zero release) with frequency-dependent time constants (200 ms high / 2 s low) that turns persistent feedback tones into "prominences" while releasing transient music instantly, and (2) trial-and-verify notch insertion — a 6 dB trial notch + 500 ms test + 3 dB TESTDROP confirmation, with deepening in 6 dB steps for verified feedback and bypass for false candidates. Concrete instance of NHS in van Waterschoot & Moonen's gain-reduction category.
- **Pages created**:
  - `raw/papers/williams-2014-acoustic-feedback-elimination/full-text.md` — extracted text from Zotero PDF (MinerU VLM, English)
  - `wiki/sources/williams-2014-acoustic-feedback-elimination.md`
  - `wiki/entities/paul-robert-williams.md`
  - `wiki/concepts/ballistics-based-howling-detection.md`
  - `wiki/concepts/trial-and-verify-notch-insertion.md`
- **Pages updated**:
  - `wiki/concepts/acoustic-feedback.md` — added Williams 2014 source link and cross-refs to ballistics and trial-and-verify concepts
  - `wiki/concepts/notch-filter-based-howling-suppression.md` — added "Concrete Patent Instance: Williams 2014" subsection mapping the patent onto the NHS pipeline; added cross-refs and source link
  - `wiki/concepts/howling-detection.md` — noted ballistics as a temporal-persistence variant of candidate-based HD; added cross-refs and source link
  - `wiki/concepts/acoustic-howling-suppression.md` — added Williams 2014 to Related Sources
  - `wiki/index.md` — added 1 entity, 2 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 1 entity row
  - `wiki/concepts/index.md` — added 2 concept rows

---

## [2026-08-08] ingest | Regularized Adaptive Notch Filters for Acoustic Howling Suppression (Gil-Cacho et al. 2009)

- **Source**: `raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/full-text.md` (Zotero: D4RBAKAU)
- **Authors**: Pepe Gil-Cacho, Toon van Waterschoot, Marc Moonen, Søren Holdt Jensen
- **Published**: Proc. 17th European Signal Processing Conference (EUSIPCO '09), Glasgow, Scotland, August 2009
- **URL**: https://ieeexplore.ieee.org/abstract/document/7077829
- **Summary**: Introduces the Regularized Adaptive Notch Filter (RANF) — three parallel direct-form ANFs with signed regularization (+λ, 0, −λ) whose coefficient convergence/divergence is used as a howling detection criterion, giving ANF-based NHS a detection capability comparable to FFT-based methods while preserving minimum delay and low complexity. Fails for howling near 0 or f_s/2 due to direct-form ANF instability.
- **Pages created**:
  - `raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/full-text.md` — extracted text via MinerU VLM (PDF deleted after extraction)
  - `raw/papers/gil-cacho-2009-regularized-adaptive-notch-filters/figures/` — 8 figures (32 crops) extracted
  - `wiki/sources/gil-cacho-2009-regularized-adaptive-notch-filters.md`
  - `wiki/entities/pepe-gil-cacho.md`
  - `wiki/entities/soren-holdt-jensen.md`
  - `wiki/concepts/regularized-adaptive-notch-filter.md`
- **Pages updated**:
  - `wiki/entities/toon-van-waterschoot.md` — appended 2009 RANF paper (Key Contributions + Related Sources)
  - `wiki/entities/marc-moonen.md` — appended 2009 RANF paper (Key Contributions + Related Sources)
  - `wiki/concepts/notch-filter-based-howling-suppression.md` — added "ANF-Based One-Stage Variant: RANF" subsection; added RANF to Related Concepts and source to Related Sources; updated frontmatter sources
  - `wiki/concepts/howling-detection.md` — added "ANF-Based Convergence Detection" paradigm subsection; added RANF to Related Concepts and source to Related Sources; updated frontmatter sources
  - `wiki/concepts/acoustic-howling-suppression.md` — added RANF note to Notch Filter subsection; added RANF to Related Concepts and source to Related Sources; updated frontmatter sources
  - `wiki/index.md` — added 2 entities, 1 concept, 1 source; updated statistics
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 1 concept row
  - `wiki/sources/index.md` — added 1 source row

---

## [2026-08-08] ingest | Audio Signal Processing in the 21st Century (Richard et al. 2023)

- **Source**: `raw/papers/richard-2023-audio-signal-processing-21st-century/full-text.md` (Zotero: 6DW9CX6C)
- **Authors**: Gaël Richard, Paris Smaragdis, Sharon Gannot, Patrick A. Naylor, Shoji Makino, Walter Kellermann, Akihiko Sugiyama
- **Published**: IEEE Signal Processing Magazine 2023 (TC-AASP 25-years retrospective)
- **DOI**: 10.1109/MSP.2023.3276171
- **Summary**: 25-year retrospective of the IEEE TC-AASP, extending the 1997 Kahrs et al. survey; two-axis taxonomy (advances by problem domain + emerging topics) tracing the paradigm shift to data-driven/deep-learning methods across coding, acoustic-environment modeling, scene analysis/synthesis, enhancement (AEC, feedback/ANC, dereverberation, noise suppression, beamforming, audio-visual), separation (determined ICA/IVA/ILRMA/MVAE + monophonic NMF/deep-clustering/discriminative), objective evaluation, MIR, and DCASE; perspectives on hybrid model-based DNNs, federated learning, and multimodal processing.
- **Pages created**:
  - `raw/papers/richard-2023-audio-signal-processing-21st-century/full-text.md` — extracted text via MinerU VLM (5 figures)
  - `wiki/sources/richard-2023-audio-signal-processing-21st-century.md` — review-structure source page (Taxonomy / Methodology / Applications Survey table / Key Contributions / Limitations)
  - `wiki/entities/gael-richard.md`
  - `wiki/entities/paris-smaragdis.md`
  - `wiki/entities/patrick-a-naylor.md`
  - `wiki/entities/akihiko-sugiyama.md`
- **Pages updated**:
  - `wiki/entities/shoji-makino.md` — appended retrospective contribution + Related Sources link
  - `wiki/entities/walter-kellermann.md` — appended retrospective contribution + source in frontmatter
  - `wiki/entities/sharon-gannot.md` — appended retrospective contribution
  - `wiki/concepts/dereverberation.md` — added Historical Context section (WPE lineage) + Key Sources link
  - `wiki/concepts/blind-source-separation.md` — added Historical Context section (ICA→DNN evolution) + Related Sources link + frontmatter source
  - `wiki/concepts/acoustic-echo-cancellation.md` — added Historical Context section (AEC field + IWAENC) + Related Sources link
  - `wiki/index.md` — added 4 entities, 1 source; updated statistics (total=978)
  - `wiki/entities/index.md` — added 4 entity rows
  - `wiki/sources/index.md` — added 1 source row
- **Synthesis**: triage found 10 candidate pages (top: deep-speech-enhancement.md, 3 shared tags); all skipped — retrospective is high-level and adds no new frontier data point / axis / claim-refinement beyond already-cited Wang 2018 and Zheng 2023.
- **Concepts**: no new concept pages created (stricter review-paper threshold — survey surveys but does not distinctively contribute individual algorithms).

---

## [2026-08-08] ingest | A System Approach to Residual Echo Suppression (Wung et al. 2011)

- **Source**: `raw/papers/wung-2011-residual-echo-suppression-system/full-text.md` (Zotero: PUI8FYUL)
- **Authors**: Jason Wung, Ted S. Wada, Biing-Hwang (Fred) Juang, Bowon Lee, Ton Kalker, Ronald W. Schafer
- **Published**: Proc. IEEE ICASSP 2011, pp. 4456–4459
- **DOI**: 10.1109/ICASSP.2011.5946436
- **Summary**: System approach to residual echo suppression combining a robust AEC (ERN + batch adaptation, no DTD), a system-level residual echo estimate (LSA nonlinear echo − AEC linear echo), and a psychoacoustic postfilter with MPEG-1 Model 2 masking. Outperforms ETF+CF baseline on SSRR/LSD/PESQ; raises PESQ by up to 0.53 over unprocessed robust AEC.
- **Pages created**:
  - `raw/papers/wung-2011-residual-echo-suppression-system/full-text.md` — extracted text via MinerU VLM
  - `wiki/sources/wung-2011-residual-echo-suppression-system.md`
  - `wiki/entities/jason-wung.md`
  - `wiki/entities/ted-wada.md`
  - `wiki/entities/biing-hwang-juang.md`
  - `wiki/entities/bowon-lee.md`
  - `wiki/entities/ton-kalker.md`
  - `wiki/entities/ronald-schafer.md`
  - `wiki/concepts/residual-echo-suppression.md`
  - `wiki/concepts/psychoacoustic-postfilter.md`
  - `wiki/concepts/error-recovery-nonlinearity.md`
- **Pages updated**:
  - `wiki/concepts/acoustic-echo-cancellation.md` — added cross-refs to RES, psychoacoustic postfilter, ERN; added Wung 2011 to Related Sources
  - `wiki/index.md` — added 6 entities, 3 concepts, 1 source; updated statistics (total=988)
  - `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added rows

---

## [2026-08-09] ingest | MCUNet: Tiny Deep Learning on IoT Devices (Lin et al. 2020)

- **Source**: `raw/papers/lin-2020-mcunet/full-text.md` (Zotero: T3XNP2YC)
- **Authors**: Ji Lin, Wei-Ming Chen, Yujun Lin, John Cohn, Chuang Gan, Song Han
- **Published**: NeurIPS 2020 (preprint v2, 2020-11-19)
- **DOI**: 10.48550/arXiv.2007.10319
- **arXiv**: 2007.10319
- **Summary**: MCUNet jointly designs TinyNAS (two-stage NAS with automated search-space optimization for MCU memory constraints) and TinyEngine (code-generation inference engine with in-place depth-wise convolution), achieving the first >70% ImageNet top-1 accuracy (70.7%) on an off-the-shelf commercial microcontroller (STM32H743) using 3.5× less SRAM and 5.7× less Flash than int8 MobileNetV2/ResNet-18.
- **Pages created**:
  - `raw/papers/lin-2020-mcunet/full-text.md` — extracted text via MinerU VLM (arXiv HTML 404, fell back from arXiv path)
  - `wiki/sources/lin-2020-mcunet.md`
  - `wiki/entities/ji-lin.md`
  - `wiki/entities/wei-ming-chen.md`
  - `wiki/entities/yujun-lin.md`
  - `wiki/entities/john-cohn.md`
  - `wiki/entities/chuang-gan.md`
  - `wiki/entities/song-han.md`
  - `wiki/concepts/tinyml.md`
  - `wiki/concepts/tinynas.md`
  - `wiki/concepts/tinyengine.md`
- **Pages updated**:
  - `wiki/concepts/neural-architecture-search.md` — added "Search-Space Optimization for Resource-Constrained Devices" section, TinyNAS/TinyML cross-refs, source link, tinyml tag
  - `wiki/index.md` — added 6 entities, 3 concepts, 1 source; updated statistics
  - `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added rows
- **Synthesis**: skipped — the only tag-overlap candidate (`computational-efficiency-evolution.md`, shared `model-compression`) is an ANC/SE efficiency synthesis; MCUNet is a vision/TinyML paper, so the cross-source contribution would be thin and off-topic.

---

## [2026-08-09] ingest | MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning (Lin et al. 2021)

- **Source**: `raw/papers/lin-2021-mcunetv2/full-text.md` (Zotero: W65ANM64)
- **Authors**: Ji Lin, Wei-Ming Chen, Han Cai, Chuang Gan, Song Han
- **Published**: arXiv preprint 2021 (v1: 2021-10-28; v2: camera-ready)
- **DOI**: 10.48550/arXiv.2110.15352
- **Summary**: MCUNetV2 introduces patch-based inference (executing the memory-intensive initial CNN stage patch-by-patch) and receptive field redistribution to cut peak SRAM 4–8×; joint NAS + inference-scheduling search sets a record 71.8% ImageNet top-1 on MCU, >90% VWW accuracy under 32kB SRAM, and +16.9% mAP on Pascal VOC object detection vs. MCUNet V1.
- **Pages created**:
  - `raw/papers/lin-2021-mcunetv2/full-text.md` — extracted text from arXiv HTML (via Defuddle)
  - `wiki/sources/lin-2021-mcunetv2.md`
  - `wiki/entities/han-cai.md`
  - `wiki/concepts/patch-based-inference.md`
  - `wiki/concepts/receptive-field-redistribution.md`
  - `wiki/concepts/imbalanced-memory-distribution.md`
- **Pages updated**:
  - `wiki/entities/ji-lin.md` — added MCUNetV2 as lead author
  - `wiki/entities/wei-ming-chen.md` — added MCUNetV2
  - `wiki/entities/song-han.md` — added MCUNetV2 as senior author
  - `wiki/entities/chuang-gan.md` — added MCUNetV2
  - `wiki/concepts/tinyml.md` — added MCUNetV2 milestone, cross-refs to patch-based-inference / receptive-field-redistribution / imbalanced-memory-distribution
  - `wiki/concepts/tinynas.md` — added MCUNetV2 extension section (per-block w, r, p, n knobs merged into one search stage)
  - `wiki/concepts/tinyengine.md` — added MCUNetV2 patch-based inference support section
  - `wiki/concepts/neural-architecture-search.md` — added MCUNetV2 joint architecture + inference-scheduling search note
  - `wiki/index.md` — added 1 entity, 3 concepts, 1 source; updated statistics
  - `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added new rows
- **Synthesis**: skipped — triage_synthesis.py found 0 matching synthesis pages out of 21 checked (source tags do not overlap with any synthesis page; the only ANC/SE efficiency synthesis shares no tags).

---

## [2026-08-09] ingest | Tiny Machine Learning: Progress and Futures (Lin et al. 2023)

- **Source**: `raw/papers/lin-2023-tinyml-progress-futures/full-text.md` (Zotero: 8P6FBNQD; arXiv: 2403.19076)
- **Authors**: Ji Lin, Ligeng Zhu, Wei-Ming Chen, Wei-Chen Wang, Song Han
- **Published**: IEEE Circuits and Systems Magazine, 2023 (DOI: 10.1109/MCAS.2023.3302182)
- **Type**: Review / survey article
- **Summary**: Surveys TinyML inference & training on microcontrollers; integrates the MCUNet V1/V2/V3 system–algorithm co-design arc and introduces MCUNetV3's on-device-training contribution (Quantization-Aware Scaling + Sparse Update + Tiny Training Engine), reducing training memory 2077× (303 MB → 149 KB) and fitting on-device training into 256 kB SRAM.
- **Pages created**:
  - `raw/papers/lin-2023-tinyml-progress-futures/full-text.md` — extracted via arXiv HTML (defuddle) + 21 figures
  - `wiki/sources/lin-2023-tinyml-progress-futures.md`
  - `wiki/entities/ligeng-zhu.md`
  - `wiki/entities/wei-chen-wang.md`
  - `wiki/concepts/quantization-aware-scaling.md`
  - `wiki/concepts/sparse-update.md`
  - `wiki/concepts/tiny-training-engine.md`
- **Pages updated**:
  - `wiki/entities/ji-lin.md` — appended 2023 TinyML review contribution
  - `wiki/entities/wei-ming-chen.md` — appended 2023 TinyML review contribution
  - `wiki/entities/song-han.md` — appended 2023 TinyML review contribution
  - `wiki/concepts/tinyml.md` — added V3 milestone paragraph + QAS/sparse-update/TTE concept links + source link
  - `wiki/concepts/tinynas.md` — added source link
  - `wiki/concepts/tinyengine.md` — added source link + TTE sibling cross-reference
  - `wiki/index.md` — added 2 entities, 3 concepts, 1 source; updated statistics (total=1009, entities=436, concepts=391, sources=154, synthesis=21, queries=7)
  - `wiki/entities/index.md` — added 2 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows
  - `wiki/sources/index.md` — added 1 source row
- **Synthesis**: triage found 6 candidate pages (generic `deep-learning`/`survey`/`quantization` tag overlap only); all are acoustics/speech-enhancement synthesis — no TinyML overlap, no updates made.

---

## [2026-08-09] ingest | Lightweight Deep Learning for Resource-Constrained Environments (Liu et al. 2024)

- **Source**: `raw/papers/liu-2024-lightweight-dl-survey/full-text.md` (Zotero: FFWWNXQT)
- **Authors**: Hou-I. Liu, Marco Galindo, Hongxia Xie, Lai-Kuan Wong, Hong-Han Shuai, Yung-Hui Li, Wen-Huang Cheng
- **Published**: arXiv preprint, 2024 (Computer Science — CV and ML)
- **DOI**: 10.48550/arXiv.2404.07236
- **Summary**: Survey unifying lightweight architecture design (CNN families + efficient transformers), model compression (pruning, quantization, KD, NAS), and hardware acceleration (GPU/FPGA/ASIC/TPU, dataflows, libraries, co-design) into a single end-to-end pipeline; frames TinyML and lightweight LLMs as the two future frontiers of resource-constrained DL.
- **Pages created**:
  - `raw/papers/liu-2024-lightweight-dl-survey/full-text.md` — extracted text from arXiv HTML (Defuddle) + 11 figures
  - `wiki/sources/liu-2024-lightweight-dl-survey.md`
  - `wiki/entities/hou-i-liu.md`
  - `wiki/entities/marco-galindo.md`
  - `wiki/entities/hongxia-xie.md`
  - `wiki/entities/lai-kuan-wong.md`
  - `wiki/entities/hong-han-shuai.md`
  - `wiki/entities/yung-hui-li.md`
  - `wiki/concepts/lightweight-cnn-families.md` — six-series taxonomy (SqueezeNet, ShuffleNet, CondenseNet, MobileNet, Shift, Add)
  - `wiki/concepts/knowledge-distillation-paradigms.md` — offline/online/self-distillation taxonomy with practical selection rules
  - `wiki/concepts/hardware-dataflow-types.md` — four-type dataflow taxonomy (pipeline / DaDianNao / systolic-array / streaming)
- **Pages updated**:
  - `wiki/entities/wen-huang-cheng.md` — added this paper as senior author; expanded research focus to include lightweight DL
  - `wiki/concepts/tinyml.md` — added Liu 2024 source; added "TinyML in the Broader Lightweight-DL Pipeline" section with MCU library catalog (CMSIS-NN, CMIX-NN, MicroNet) and three structural impediments
  - `wiki/concepts/neural-architecture-search.md` — added Liu 2024 source; added "Algorithm-Family Taxonomy" section (RL / EA / gradient / hardware-aware NAS with practical selection rules)
  - `wiki/concepts/depthwise-separable-convolution.md` — added Liu 2024 source; cross-referenced the MobileNet series taxonomy and the MAC-vs-FLOPs insight
  - `wiki/concepts/attention-mechanism.md` — added Liu 2024 source; added "Efficient Transformer Taxonomy" section (efficient self-attention, token sparsing, lightweight hybrid models with ImageNet comparison)
  - `wiki/concepts/post-training-quantization.md` — added Liu 2024 source; cross-referenced bit-width trade-offs (Table 5) and hardware-matched quantization guidance
  - `wiki/concepts/quantization-aware-training.md` — added Liu 2024 source; cross-referenced quantization-as-compression guidance
  - `wiki/index.md` — added 6 entities, 3 concepts, 1 source; updated statistics (total=1019)
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 6 entity rows
  - `wiki/concepts/index.md` — added 3 concept rows
- **Synthesis**: triage ran (2 candidate pages by tag overlap); skipped updates — Liu 2024 is CV/ML-focused, does not add a substantive data point to the ANC-focused `computational-efficiency-evolution.md` synthesis; cross-reference in source page's Related Synthesis section is sufficient

---

## [2026-08-10] ingest | Timcheck et al. 2023: The Intel Neuromorphic DNS Challenge

- **Source**: `raw/papers/timcheck-2023-intel-neuromorphic-dns-challenge/full-text.md` (MinerU extraction from arXiv 2303.09503 PDF; Zotero item key `0_TJJYB8BC`)
- **Summary**: Defines the Intel Neuromorphic DNS Challenge (LAVA 2023) — a benchmark for SNN-based real-time monaural speech enhancement on Loihi 2. Two tracks (algorithmic simulation / hardware implementation) evaluate audio quality (SI-SNR, DNSMOS), power (Loihi-calibrated proxy P = SynOPS + 10×NeuronOPS), latency, and chip resources; minimum improvement thresholds prevent trivial solutions. Includes a 500-hour dataset derived from the Microsoft DNS Challenge corpus and an SDNN baseline (sigma-delta encoding + axonal delays) reaching SI-SNR 12.50 dB at **14.54 M-Ops/s power proxy, 525K params, 465 KB** — 9.4× lower power, 5× fewer params, 22× smaller model than the NsNet2 conventional baseline (136.13 M-Ops/s, 2,681K params) on the same validation set.
- **Pages created**:
  - `wiki/sources/timcheck-2023-intel-neuromorphic-dns-challenge.md` — source summary with full metadata, methodology, results, and key contributions
  - 8 entity pages for authors (all Intel Labs Neuromorphic Computing Lab):
    - `wiki/entities/jonathan-timcheck.md` (first author)
    - `wiki/entities/sumit-bam-shrestha.md` (SNN training / surrogate gradients)
    - `wiki/entities/petrus-foloppe.md`
    - `wiki/entities/daniel-cleland.md`
    - `wiki/entities/aidan-schuman.md`
    - `wiki/entities/jeffrey-kopsick.md`
    - `wiki/entities/mike-davies.md` (Director, Intel Labs Neuromorphic Computing Lab)
    - `wiki/entities/karthikeyan-ramasamy.md`
  - 2 new concept pages:
    - `wiki/concepts/loihi-2.md` — Intel's second-generation neuromorphic chip; documents the 10× neuron-vs-synapse energy ratio underpinning the Track 1 power-proxy metric
    - `wiki/concepts/sigma-delta-neural-network.md` — SDNN architecture, sigma-delta sparse message passing, axonal-delay temporal memory, and the baseline's N-DNS performance vs. NsNet2 / Spiking-FullSubNet
- **Pages updated** (added source citation, cross-references, and updated `updated` dates):
  - `wiki/concepts/intel-neuromorphic-dns-challenge.md` — now points to the primary source and the Loihi 2 / SDNN concept pages; Related Concepts/Sources expanded
  - `wiki/concepts/neuromorphic-computing.md` — added Timcheck 2023 source; cross-referenced Loihi 2 and the Intel N-DNS Challenge
  - `wiki/concepts/spiking-neural-networks.md` — added Timcheck 2023 source; cross-referenced Loihi 2, SDNN, and the Intel N-DNS Challenge
  - `wiki/concepts/dns-challenge.md` — added a paragraph linking the Microsoft DNS Challenge to its neuromorphic counterpart and citing Timcheck 2023
  - `wiki/concepts/nsnet2.md` — added "Role as a Conventional Baseline for Neuromorphic SE" section with the N-DNS comparison numbers (136.13 M-Ops/s, 2,681K params vs. SDNN's 14.54 / 525K)
- **Synthesis**: triage ran (6 candidate pages by tag overlap); 1 updated:
  - `wiki/synthesis/computational-efficiency-evolution.md` — added Timcheck 2023 to Related Sources and to the SSE-Net (axis #5) entry of the 2026 efficiency frontier: anchored the Loihi power-proxy metric citation with its primary source and added the SDNN baseline as the originating frontier point of the spiking/neuromorphic Pareto axis. Also added Loihi 2, SDNN, Intel N-DNS Challenge, and NsNet2 to the Related Concepts list. The other 5 candidates had only 1 shared tag (speech-enhancement) with no substantive cross-source contribution and were skipped.
- **Indexes**: ran `update_indexes.py batch --stats` — 11 added (1 source + 8 entities + 2 new concepts), 6 updated pages already present (skipped). After creating 5 entity files that were missing from disk (see "Pages created" above — the previous session had only written 3 of 8 to disk), re-ran `update_indexes.py stats`: total=1035, entities=455, concepts=396, sources=156, synthesis=21, queries=7. Verified with `check_statistics.py` — all counts match actual files. Note: `check_index_drift.py` surfaced 5 pre-existing orphan entity files unrelated to this ingest (adam-kupryjanow, daniel-ben-dayan-rubin, garrick-orchard, lukasz-pindor, timothy-shea) — present on disk but never indexed by their original ingests; left for a future lint pass.

---

## [2026-08-10] ingest | Guo et al. 2024: A Survey on Adaptive ANC Algorithms Overcoming the Output Saturation Effect

- **Source**: `raw/papers/guo-2024-anc-saturation-survey/full-text.md` (MinerU extraction from arXiv 2403.17xxx PDF; Zotero item key `2R4HUK5R`)
- **Authors**: Yu Guo, Xiaoyi Shen, Junwei Ji (NTU DSP Lab); Dongxing Li, Tao Jiang, Xiaojun Qiu
- **Published**: 2024 (arXiv preprint)
- **Summary**: Survey organising saturation-mitigation ANC algorithms into two families — (1) **output-constraint** algorithms that bound the actuator output to keep the amplifier linear (2-GD FxLMS, Re-scaling FxLMS, Leaky FxLMS, MOV FxLMS, MOV-Modified FxLMS, OLFxLMS, FxlogLMS), and (2) **nonlinear-adaptive** algorithms that model the saturation nonlinearity directly (2nd-VFxLMS, BFxLMS, FLANN-FsLMS, THF-FxLMS, MLPNN-FxLMS). Derives the saturated-output divergence proof, gives the QCQP formulation unifying the constraint family, and provides per-algorithm computational-complexity tables. Key finding: under **severe** saturation the constraint family preserves stability while NLANC diverges; under **mild** saturation NLANC can match the constraint family at higher cost.
- **Pages created**:
  - `wiki/sources/guo-2024-anc-saturation-survey.md` — source summary with taxonomy, problem formulation, methodology, applications survey, key contributions, and limitations
  - 3 entity pages for NTU DSP Lab authors:
    - `wiki/entities/yu-guo.md` (lead author)
    - `wiki/entities/xiaoyi-shen.md` (wireless ANC, output-constrained ANC, momentum FxLMS)
    - `wiki/entities/junwei-ji.md` (output-constrained adaptive algorithms, momentum 2GD FxLMS)
  - 2 new concept pages:
    - `wiki/concepts/output-saturation-effect.md` — defines the core problem: amplifier nonlinearity, saturated-output divergence proof ($\lim \mathbb{E}[\mathbf{w}] = \infty$), mild-vs-severe regime distinction
    - `wiki/concepts/output-constraint-anc-algorithms.md` — the constraint family: QCQP formulation, 8 algorithms with mechanisms/constraints/complexity, MOV-Modified as the practical default for severe saturation
- **Pages updated** (added cross-references and survey citations; `created` dates preserved, only `updated` bumped to 2026-08-10):
  - `wiki/concepts/leaky-fxlms-algorithm.md` — linked to output-constraint family and saturation regime; clarified that leaky factor doubles as an output-power constraint
  - `wiki/concepts/nonlinear-active-noise-control.md` — added "Saturation Regime" distinction (NLANC diverges under severe saturation per Guo 2024)
  - `wiki/concepts/active-noise-control.md` — cross-referenced output-saturation-effect and output-constraint-anc-algorithms
  - `wiki/concepts/minimum-variances-control.md` — clarified the distinction between classical MVC (plant output constraint) and MOV-FxLMS (adaptive filter output constraint)
- **Synthesis**: 2 pages updated:
  - `wiki/synthesis/nonlinear-anc-approaches.md` — added "The Saturation Regime" section with a mild-vs-severe table distinguishing NLANC behaviour; added THF-FxLMS and MLPNN-FxLMS from the survey
  - `wiki/synthesis/adaptive-algorithm-tradeoffs.md` — added Section 1.7 "Output Constraint Family" with per-algorithm complexity table; updated the actuator-saturation row of the decision matrix to recommend MOV-Modified FxLMS for severe saturation; added output-saturation-effect and output-constraint-anc-algorithms to Related Concepts; added Guo 2024 to Related Sources
- **Indexes**: updated `wiki/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` with 6 new entries (1 source + 3 entities + 2 concepts). Statistics recounted and verified with `check_statistics.py`: total=1039, entities=456, concepts=398, sources=157, synthesis=21, queries=7 — all counts match actual files. (Note: entities actual=456 vs +3 from the prior 455 baseline indicates a pre-existing 2-file drift that this ingest corrected in the stated count.)
- **Verification**: `mkdocs build --strict` passed (exit 0, no page-level warnings).

---

## [2026-08-11] ingest | Efficient Neural Networks for Tiny Machine Learning: A Comprehensive Review (Lê, Wolinski & Arbel 2026)

- **Source**: `raw/papers/le-2026-efficient-nn-tinyml-review/full-text.md` (Zotero: QDFZSG5A; arXiv: 2311.11883)
- **Authors**: Minh Tri Lê, Pierre Wolinski, Julyan Arbel
- **Published**: ACM Transactions on Intelligent Systems and Technology (TIST), 2026
- **DOI**: 10.1145/3729429
- **Summary**: ACM TIST review bridging TinyML methodology and applications. Introduces a five-method compression taxonomy (pruning, quantization, knowledge distillation, neural architecture search, weight-sharing + low-rank decomposition) unified by a Bayesian compression synthesis using spike-and-slab, horseshoe, and log-uniform priors with variational inference. Presents a runtime-vs-transcompiler TinyMLOps framework taxonomy (TFLM, NNoM, Edge Impulse/EON, μTVM, CMSIS-NN backend). Provides Flash-size-vs-accuracy landscapes overlaid with Cortex-M0+/M4/M7 memory thresholds for MNIST, ImageNet, Visual Wake Words, and Google Speech Commands v2-12. Targets the extreme-low-power regime (<8 kB SRAM, Cortex-M0+/eDMPv1).
- **Pages created**:
  - `raw/papers/le-2026-efficient-nn-tinyml-review/full-text.md` — extracted text from Zotero PDF (MinerU VLM, 1106 lines, 9 referenced figures mapped)
  - `wiki/sources/le-2026-efficient-nn-tinyml-review.md` — source page with full taxonomy, methodology, results, key contributions, and limitations
  - 3 entity pages for the authors:
    - `wiki/entities/minh-tri-le.md` (Université Grenoble Alpes / Inria — TinyML, quantization, Bayesian compression)
    - `wiki/entities/pierre-wolinski.md` (UGA / Inria / Paris-Dauphine — TinyML, Bayesian compression, NAS)
    - `wiki/entities/julyan-arbel.md` (UGA / Inria — Bayesian statistics, Bayesian neural networks, TinyML)
  - 3 new concept pages:
    - `wiki/concepts/model-pruning.md` — three-granularity taxonomy (unstructured, structured, Bayesian) with TinyML considerations
    - `wiki/concepts/bayesian-compression.md` — unifying framework for pruning + quantization via sparsity-inducing priors and variational inference; covers spike-and-slab, horseshoe, log-uniform priors and the gated-residual Bayesian quantization of Van Baalen et al. 2021
    - `wiki/concepts/tinymlops.md` — end-to-end MCU deployment pipeline; runtime (TFLM) vs transcompiler (NNoM, Edge Impulse, μTVM) framework taxonomy; CMSIS-NN backend; MLPerf Tiny benchmark
- **Pages updated** (added cross-references; `created` dates preserved, only `updated` bumped to 2026-08-11):
  - `wiki/concepts/tinyml.md` — added Lê 2026 to sources and Related Sources; added cross-refs to tinymlops, model-pruning, bayesian-compression, keyword-spotting
  - `wiki/concepts/knowledge-distillation-paradigms.md` — added new "KD for TinyML" section with MCU-class KD compression table (Polino, Zein, TinyBERT) and the standard KD loss formulation
  - `wiki/concepts/post-training-quantization.md` — added Lê 2026 to Related Sources with the 8-bit PTQ recommendation for MCUs and the TinyML-specific quantization sensitivity observation
  - `wiki/concepts/quantization-aware-training.md` — added Lê 2026 to Related Sources with the below-8-bit QAT superiority, straight-through estimator, and the Bayesian quantization cross-reference
- **Synthesis**: no updates. Existing synthesis pages are thematically focused on ANC/speech enhancement; the Lê 2026 paper is squarely outside those themes, so no synthesis cross-references were added (avoiding thin stubs).
- **Indexes**: updated `wiki/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` with 7 new entries (1 source + 3 entities + 3 concepts). Statistics recounted and verified with `check_statistics.py`: total=1046, entities=459, concepts=401, sources=158, synthesis=21, queries=7 — all counts match actual files.
- **Verification**: `mkdocs build --strict` passed (exit 0, no page-level warnings).

---

## [2026-08-11] ingest | A Robust Residual Echo Suppression Algorithm Even During Double Talk (Fang 2020)

- **Source**: `raw/papers/fang-2020-robust-residual-echo-suppression/full-text.md` (Zotero: PCS7RXHC)
- **Authors**: Bingxiao Fang
- **Published**: Proc. IEEE ICICS 2020, Sep. 2020
- **DOI**: 10.1109/ICICSP50920.2020.9232011
- **Summary**: VAD-free residual echo PSD estimator via statistical normalized correlation between mean-removed AEC error and echo replica; robust during double talk; outperforms slow-attach-fast-decay baseline on both ERLE and SSDR
- **Pages created**:
  - `raw/papers/fang-2020-robust-residual-echo-suppression/full-text.md` — extracted text from Zotero PDF (MinerU VLM)
  - `wiki/sources/fang-2020-robust-residual-echo-suppression.md`
  - `wiki/entities/bingxiao-fang.md`
  - `wiki/concepts/statistical-normalized-correlation.md`
  - `wiki/concepts/echo-return-loss-enhancement.md`
  - `wiki/concepts/speech-to-speech-distortion-ratio.md`
- **Pages updated**:
  - `wiki/concepts/residual-echo-suppression.md` — added Fang 2020 method section, cross-refs to new concepts, and source link
  - `wiki/concepts/multidelay-block-frequency-domain-adaptive-filter.md` — added Fang 2020 as a related source (uses GMDF front-end)
  - `wiki/index.md` — added 1 entity, 3 concepts, 1 source; updated statistics
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 1 entity row
  - `wiki/concepts/index.md` — added 3 concept rows

---

## [2026-08-14] ingest | A Lightweight and Robust Method for Blind Wideband-to-Fullband Extension of Speech (Büthe & Valin 2025)

- **Source**: `raw/papers/buthe-2025-blind-wideband-to-fullband-extension/full-text.md` (Zotero: 2HT68ITY, arXiv HTML extraction)
- **Authors**: Jan Büthe, Jean-Marc Valin
- **Published**: WASPAA 2025, 5 pp. (preprint arXiv:2412.11392)
- **DOI**: 10.48550/arXiv.2412.11392
- **Summary**: BBWENet — a hybrid DSP/DNN blind wideband-to-fullband bandwidth extension model (~370 K params, ~140 MFLOPS / ~70 MMACS, 10 ms frame + 0.27 ms lookahead) combining classical pre-filter/upsample/extension/post-filter signal processing with a small DNN that steers AdaConv pre/post-filters and AdaShape spectral folding. Trained with regression + frequency-domain adversarial losses on a 900+-speaker TTS mixture with robustness augmentations; paired with Opus 1.5 it significantly improves P.808 DCR quality at 6–12 kb/s and at 9 kb/s statistically matches EVS 9.6 kb/s and Opus 1.4 at 18 kb/s.
- **Pages created**:
  - `raw/papers/buthe-2025-blind-wideband-to-fullband-extension/full-text.md` — arXiv HTML extraction (Defuddle) + 1 figure
  - `wiki/sources/buthe-2025-blind-wideband-to-fullband-extension.md`
  - `wiki/entities/jan-buthe.md`
  - `wiki/concepts/blind-bandwidth-extension.md`
  - `wiki/concepts/adaconv.md`
  - `wiki/concepts/adashape.md`
- **Pages updated**:
  - `wiki/entities/jean-marc-valin.md` — appended BBWENet contribution
  - `wiki/concepts/erb-scale.md` — added BBWENet usage section + source
  - `wiki/concepts/adaptive-convolution.md` — added AdaConv cross-ref (distinct mechanism)
  - `wiki/concepts/percepnet.md` — added BBWENet cross-ref + source
  - `wiki/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added 5 rows; updated statistics
- **Synthesis**: none — tag triage found no matching synthesis pages (single-task BWE paper)

---

## [2026-08-14] ingest | Real-Time PLC (Valin 2022)

---

## [2026-08-15] ingest | Sound Capture System and Spatial Filter for Small Devices (Tashev et al. 2008)

- **Source**: `raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md` (Zotero: 79EJS2D7)
- **Authors**: Ivan Tashev, Slavy Mihov, Tyler Gleghorn, Alex Acero
- **Published**: 2008 (conference paper)
- **URL**: https://www.microsoft.com/en-us/research/publication/sound-capture-system-and-spatial-filter-for-small-devices/
- **Summary**: Two-microphone sound capture system for small devices — back-to-back unidirectional capsules (9.6 mm baseline) + front-back-difference-maximizing beamformer + probability-based non-linear spatial filter; 10.43 dB SNR improvement and 0.39 PESQ-MOS improvement at 16 kHz / 512-sample frames.
- **Pages created**:
  - `raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md` — MinerU VLM extraction (English, 231 lines, 4 figures mapped)
  - `wiki/sources/tashev-2008-sound-capture-spatial-filter.md`
  - `wiki/entities/ivan-tashev.md`
  - `wiki/entities/slavy-mihov.md`
  - `wiki/entities/tyler-gleghorn.md`
  - `wiki/entities/alex-acero.md`
  - `wiki/concepts/back-to-back-microphone-array.md`
  - `wiki/concepts/probability-based-spatial-filter.md`
- **Pages updated** (bidirectional cross-references):
  - `wiki/concepts/beamforming.md` — added Difference-Maximizing Beamformer subsection; Related Concepts and Related Sources extended
  - `wiki/concepts/voice-activity-detection.md` — added note about energy-based binary VAD with minimum-energy tracking under Traditional Signal Processing
  - `wiki/concepts/multi-channel-speech-enhancement.md` — Related Concepts and Related Sources extended
  - `wiki/concepts/wiener-filter.md` — added "Wiener Gain as Offline Optimization Reference" section
  - `wiki/concepts/differential-microphone-array.md` — added "Back-to-Back Unidirectional Variant" comparison subsection
  - `wiki/concepts/speech-enhancement.md` — Related Sources extended
  - `wiki/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/sources/index.md` — added 7 entries, statistics recounted (total=1072)

---

## [2026-08-15] ingest | DiffVQE: hybrid diffusion voice quality enhancement under acoustic echo and noise (Lugo et al. 2026)

- **Source**: `raw/papers/lugo-2026-diffvqe/full-text.md` (Zotero: 9UTQLQW7)
- **Authors**: Haljan Lugo, Ernst Seidel, Pejman Mowlaee, Ziyue Zhao, Tim Fingscheidt
- **Published**: arXiv preprint 2026-06-17 (v2), arXiv:2605.08189
- **DOI**: 10.48550/arXiv.2605.08189
- **Summary**: First fully reproducible diffusion-based AEC model (DiffVQE): hybrid single-step Cond/Score framework adapted from EffDiffSE, trained on curated URGENT 2025 + AEC Challenge 2023 data; outperforms retrained DeepVQE on most quality/intelligibility metrics at ~10–13% of its FLOPS (DeepVQE retains slight DT/ST Echo edge)
- **Pages created**: `wiki/sources/lugo-2026-diffvqe.md`, `wiki/entities/haljan-lugo.md`, `wiki/entities/ziyue-zhao.md`, `wiki/concepts/urgent-challenge.md`
- **Pages updated**: `wiki/entities/ernst-seidel.md`, `wiki/entities/pejman-mowlaee.md`, `wiki/entities/tim-fingscheidt.md` (appended DiffVQE contribution); `wiki/concepts/diffusion-models-for-speech.md` (single-step hybrid section); `wiki/concepts/acoustic-echo-cancellation.md` (hybrid diffusion AEC row + paragraph); `wiki/concepts/sub-pixel-convolution.md` (DiffVQE application); `wiki/sources/indenbom-2023-deepvqe.md` (cross-ref DiffVQE); `wiki/synthesis/multimodal-bc-speech-enhancement.md` (single-step diffusion refines multi-step claim)

---

## [2026-08-15] ingest | Multi-channel Noise Reduction for Hands-free Voice Communication on Mobile Phones (Jin et al. 2017)

- **Source**: `raw/papers/jin-2017-multichannel-noise-reduction-mobile/full-text.md` (Zotero: 45QQHIE9)
- **Authors**: Wenyu Jin, Mohammad J. Taghizadeh, Kainan Chen, Wei Xiao
- **Published**: ICASSP 2017, pp. 5700–5704 (DOI: 10.1109/ICASSP.2017.7952207)
- **DOI**: 10.1109/ICASSP.2017.7952207
- **Summary**: Adaptive coherence NE for hands-free mobile-phone voice communication — combines single-channel SPP-based NE (low frequencies) with globally MMSE-optimized multi-channel coherence-based NE (high frequencies) under an adaptively varying split frequency; validated on a 3-microphone Huawei Mate 8 in pink point-source and real Marienplatz rush-hour noise.
- **Pages created**:
  - `wiki/sources/jin-2017-multichannel-noise-reduction-mobile.md`
  - `wiki/entities/wenyu-jin.md`
  - `wiki/entities/mohammad-taghizadeh.md`
  - `wiki/entities/kainan-chen.md`
  - `wiki/entities/wei-xiao.md`
  - `wiki/concepts/adaptive-coherence-noise-estimation.md`
  - `wiki/concepts/speech-presence-probability.md`
- **Pages updated**:
  - `wiki/concepts/mvdr-beamformer.md` — added "MVDR with Adaptive Coherence Post-filter" section + cross-refs
  - `wiki/concepts/multi-channel-speech-enhancement.md` — added adaptive coherence NE to Key Techniques + cross-refs
  - `wiki/concepts/multi-channel-wiener-filter.md` — added "MVDR + Single-Channel Wiener Factorization" section
  - `wiki/concepts/spatial-coherence.md` — added "自适应相干性模型" section on adaptive coherence updates
  - `wiki/concepts/coherent-to-diffuse-power-ratio.md` — added "Relation to Global Coherence-Based Noise Variance Decomposition" section
  - `wiki/concepts/voice-activity-detection.md` — added "Soft-Decision VAD via Speech Presence Probability" section
  - `wiki/concepts/minimum-statistics.md` — added "Relation to SPP-Based Noise Estimation" section
- **Synthesis**: skipped — triage found only broad-tag (speech-enhancement) candidates

---

## [2026-08-16] ingest | Generalized Coherence-Based Signal Enhancement (Löllmann, Brendel & Kellermann 2020) (re)

- **Source**: `raw/papers/lollmann-2020-generalized-coherence-based-signal-enhancement/full-text.md` (Zotero: DSYMKBRQ)
- **Authors**: Heinrich W. Löllmann, Andreas Brendel, Walter Kellermann
- **Published**: ICASSP 2020, pp. 201–205
- **DOI**: 10.1109/ICASSP40776.2020.9054470
- **Summary**: Targeted update to existing source page — added missing Fig. 1 embed (3 panels: SRMR, fwSNR, PESQ) identified by `map_figures.py`; removed two incorrect synthesis links (Modern Headphone ANC Systems, Multi-Modal Speech Enhancement) that had no topical relevance to this classical CDR-based dereverberation paper, replaced with a note. Entity and concept pages verified complete; no new pages needed.
- **Pages updated**:
  - `wiki/sources/lollmann-2020-generalized-coherence-based-signal-enhancement.md` — added Fig. 1 embed (3 panels), fixed Related Synthesis section, bumped `updated` date

---

## [2026-08-16] merge | Synthesis: Multi-Channel Speech Enhancement (17 sources, 2005-2026)

- **Source**: 17 MCSE sources (2005–2026) — see `wiki/synthesis/multi-channel-speech-enhancement.md` sources list
- **Summary**: New cross-source synthesis tracing multi-channel speech enhancement along 5 axes: (1) classical coherence/CDR lineage with DOA-independence as key relaxation (Schwarz 2015 → Löllmann 2020 GMC); (2) MVDR robustness eras (ellipsoidal RMVB → Kantorovich adaptive loading → data-driven WNG); (3) "estimate what" relaxation chain (DOA → coherence → CDR → SCM → RTF → direct weights); (4) input→output inversion (Apostolidis 2026); (5) array geometry (fixed → agnostic → conditioned). Argues classical MCSE survives in 2026 as the interpretability backbone of hybrid systems.
- **Pages created**:
  - `wiki/synthesis/multi-channel-speech-enhancement.md` — 17 sources, 7 insights + cross-cutting takeaways + open questions
- **Pages updated**:
  - `wiki/index.md` — added 1 synthesis row; updated statistics (total 1083 → 1084, synthesis 21 → 22)
  - `wiki/synthesis/index.md` — added 1 synthesis row

---

## [2026-08-16] ingest | Informed Spatial Filters for Speech Enhancement (Taseska 2018)

- **Source**: `raw/papers/taseska-2018-informed-spatial-filters/full-text.md` (FAU PhD thesis, OpenFAU; Zotero: 0_VQZTHIS3)
- **Author**: Maja Taseska (supervisor: Emanuele A. P. Habets, FAU Erlangen-Nuremberg)
- **Published**: 2018 (Dr.-Ing. dissertation, FAU)
- **Summary**: PhD thesis establishing the **Informed Spatial Filter (ISF)** paradigm — narrowband detectors continuously update PSD matrices and RTF vectors per TF bin, yielding near-instantaneous filter adaptation. Unifies six applications across single-array (Ch 3–5) and multi-array (Ch 6–8) scenarios: (1) CDR-controlled noise PSD matrix estimation via multichannel MCRA with CDR-based a priori SAP; (2) DOA model-based source extraction with von Mises / notched likelihoods; (3) informed GSC with bin-wise detector-controlled FBF/BM/NC and RLS noise canceller; (4) acoustic spotforming via position-based detection and rank-one MVDR with distributed arrays; (5) EM-based BSS with joint number-of-source detection using narrowband position features; (6) Bayesian multi-source tracker for BSS of moving sources with augmented position+signal measurement model (JPDA/PMHT-like, multi-measurement-per-source). Extracted via MinerU (VLM) in two chunks (pages 1–174, 175–231) due to 200-page limit.
- **Pages created**:
  - `wiki/sources/taseska-2018-informed-spatial-filters.md` — comprehensive source page with per-chapter summaries (Ch 1–8)
  - `wiki/entities/maja-taseska.md`
  - `wiki/concepts/informed-spatial-filter.md`
  - `wiki/concepts/acoustic-spotforming.md`
  - `wiki/concepts/doa-informed-source-extraction.md`
  - `wiki/concepts/multichannel-mcra.md`
  - `wiki/concepts/informed-gsc.md`
  - `wiki/concepts/tf-mask-estimation.md`
  - `wiki/concepts/sparsity-based-source-tracking.md`
- **Pages updated**:
  - `wiki/entities/emanuele-habets.md` — added thesis supervision to key contributions
  - `wiki/concepts/coherent-to-diffuse-power-ratio.md` — added CDR as a priori SAP control (Taseska & Habets 2018, Ch 3) + source link
  - `wiki/concepts/mvdr-beamformer.md` — added informed MVDR section + source link
  - `wiki/concepts/gsc-beamformer.md` — added informed GSC section + related concepts + source link
  - `wiki/synthesis/multi-channel-speech-enhancement.md` — added Taseska 2018 to sources/frontmatter/table; added "CDR as detector control" parallel track paragraph in Insight 1
  - `wiki/index.md` — added 1 source, 1 entity, 7 concepts; updated statistics (total 1084 → 1093, entities 475 → 476, concepts 416 → 423, sources 164 → 165)
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 1 entity row
  - `wiki/concepts/index.md` — added 7 concept rows

---

## [2026-08-19] ingest | Sawada et al. 2019: BSS/ILRMA Review

- **Source**: `raw/papers/sawada-2019-bss-ilrma-review/full-text.md` (extracted via MinerU from Zotero PDF)
- **Zotero**: item key `AVA2LQ34`, attachment `EBIZXTUI`
- **DOI**: [10.1017/ATSIP.2019.5](https://doi.org/10.1017/ATSIP.2019.5)
- **Summary**: Ingested the review article "A review of blind source separation methods: two converging routes to ILRMA originating from ICA and NMF" (Sawada, Ono, Kameoka, Kitamura & Saruwatari, APSIPA Trans. Signal Inf. Process. 2019). The paper unifies the ICA route (FD-ICA → IVA → ILRMA) and NMF route (IS-NMF → MNMF → ILRMA) under a common majorization-minimization (MM) optimization engine with auxiliary functions. Created comprehensive source page with taxonomy, problem formulation, methodology, experimental setup, and key contributions; embedded 11 main figures via wikilink embeds.
- **Pages created**:
  - `wiki/sources/sawada-2019-bss-ilrma-review.md` — full source page with metadata, taxonomy, methodology, results, and key contributions
  - `wiki/entities/hiroshi-sawada.md` — NTT Corporation, lead author
  - `wiki/entities/nobutaka-ono.md` — Tokyo Metropolitan University, AuxIVA
  - `wiki/entities/hirokazu-kameoka.md` — NTT Corporation / U. Tokyo, MVAE
  - `wiki/entities/daichi-kitamura.md` — NIT Kagawa College, ILRMA
  - `wiki/concepts/independent-low-rank-matrix-analysis.md` — ILRMA concept page with dual IVA/NMF derivation
  - `wiki/concepts/multichannel-nmf.md` — MNMF concept page covering full and source-wise variants
- **Pages updated**:
  - `wiki/entities/hiroshi-saruwatari.md` — added review contribution
  - `wiki/concepts/blind-source-separation.md` — added ILRMA and MNMF rows to methods table, cross-references to new concept pages, added source link
  - `wiki/concepts/independent-vector-analysis.md` — clarified relationship to ILRMA/MNMF, added source link
  - `wiki/concepts/fastmnmf.md` — added MNMF/ILRMA cross-reference, added source link
  - `wiki/index.md` — added 1 source, 4 entities, 2 concepts; updated statistics (total 1093 → 1100, entities 476 → 480, concepts 423 → 425, sources 165 → 166)
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 4 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows

---

## [2026-08-19] ingest | Ishikawa et al. 2025: Real-Time RCSCME-based Speech Extraction

Ingested the IEEE Access 2025 paper proposing a real-time extension of the ILRMA + RCSCME speech-extraction pipeline via the blockwise batch algorithm, two new spatially regularized ILRMA variants (SR-ILRMA using the prior target steering vector, NSR-ILRMA using a null-beamformer regularizer that admits the cheaper IP update), and the FastVCD / FastIP demixing-matrix update rules derived by four algebraic transformations of VCD/IP that are analytically equivalent to the originals but ~33% faster and more numerically stable. Real-time operation validated on Intel Core i9-13900KF CPU and NVIDIA Jetson AGX Xavier / AGX Orin, exceeding Online IVA-IP/ISS in SDR/SIR under diffuse-noise conditions.

- **Zotero key**: `4U5QAMLY`
- **DOI**: 10.1109/ACCESS.2025.3569590
- **Raw extraction**: `raw/papers/ishikawa-2025-real-time-speech-extraction/full-text.md` (1294 lines via MinerU)
- **Figures**: 17 figures mapped; 7 embedded in source page (Figs. 2, 3, 4, 6, 7, 8, 9, 10(a), 13, 14(a), 17(left)) — the rest are boxplot panels covering comparable metrics across SNRs / devices.
- **Pages created**:
  - `wiki/sources/ishikawa-2025-real-time-speech-extraction.md` — source page with Summary, Problem Formulation (ILRMA + RCSCME), Methodology (blockwise batch, SR-ILRMA / NSR-ILRMA, FastVCD / FastIP), Experimental Setup, Results, Key Contributions
  - `wiki/entities/yuto-ishikawa.md` — U. Tokyo, lead author
  - `wiki/entities/tomohiko-nakamura.md` — U. Tokyo
  - `wiki/entities/yu-takahashi.md` — Yamaha Corporation
  - `wiki/entities/kazunobu-kondo.md` — Yamaha Corporation
  - `wiki/concepts/rank-constrained-spatial-covariance-matrix-estimation.md` — RCSCME: rank-1 target SCM + full-rank diffuse-noise SCM with inverse-gamma sparsity prior; majorization-equalization updates; MWF target extraction
  - `wiki/concepts/fast-demixing-matrix-estimation.md` — FastVCD / FastIP: four algebraic transformations (Sherman–Morrison Hermitian inversion, redundant MatVec removal, row/column updates using $\mathbf{F}_{in}^{(l)}$ structure, closed-form $\varphi_{in}$ branch); analytically equivalent to VCD/IP
- **Pages updated**:
  - `wiki/entities/daichi-kitamura.md` — added contribution from this paper
  - `wiki/entities/norihiro-takamune.md` — added contribution from this paper
  - `wiki/entities/hiroshi-saruwatari.md` — added contribution from this paper
  - `wiki/concepts/independent-low-rank-matrix-analysis.md` — added SR-ILRMA / NSR-ILRMA variants row; cross-links to RCSCME and Fast Demixing
  - `wiki/concepts/spatial-regularization.md` — added "Spatially Regularized ILRMA (SR-ILRMA / NSR-ILRMA)" subsection; cross-links to Fast Demixing and RCSCME
  - `wiki/concepts/iterative-source-steering.md` — added "Comparison with FastVCD / FastIP" section contrasting the two fast-update paradigms
  - `wiki/concepts/spatial-covariance-matrix.md` — added cross-link to RCSCME
  - `wiki/index.md` — added 1 source, 4 entities, 2 concepts; updated statistics (total 1100 → 1107, entities 480 → 484, concepts 425 → 427, sources 166 → 167)
  - `wiki/sources/index.md` — added 1 source row
  - `wiki/entities/index.md` — added 4 entity rows
  - `wiki/concepts/index.md` — added 2 concept rows

---

## [2026-08-19] ingest | Neural Target Speech Extraction: An Overview (Zmolikova 2023)

- **Source**: `raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md` (Zotero: X5JSCD25)
- **Authors**: Katerina Zmolikova, Marc Delcroix, Tsubasa Ochiai, Keisuke Kinoshita, Jan Černocký, Dong Yu
- **Published**: IEEE Signal Processing Magazine 40, 2023, pp. 8–29
- **DOI**: 10.1109/MSP.2023.3240008
- **Summary**: Review/survey unifying neural target speech extraction (TSE) under a single framework (clue encoder + mixture encoder + fusion layer + target extractor) covering audio, visual, and spatial clue variants; reports comparative experiments with TD-SpeakerBeam and catalogs datasets/toolkits.
- **Pages created**:
  - `wiki/sources/zmolikova-2023-neural-target-speech-extraction-overview.md`
  - `wiki/entities/katerina-zmolikova.md`
  - `wiki/entities/marc-delcroix.md`
  - `wiki/entities/tsubasa-ochiai.md`
  - `wiki/entities/keisuke-kinoshita.md`
  - `wiki/entities/jan-cernocky.md`
  - `wiki/concepts/cocktail-party-problem.md`
  - `wiki/concepts/target-speaker-vad.md`
  - `wiki/concepts/target-speaker-asr.md`
  - `wiki/concepts/angle-feature.md`
- **Pages updated**:
  - `wiki/entities/dong-yu.md` — added TSE/PIT/MIMO beamformer contributions
  - `wiki/concepts/target-speaker-extraction.md` — added "Unified Neural TSE Framework" + "Extensions Beyond Waveform Extraction" sections, new concept cross-refs, expanded challenges
  - `wiki/concepts/td-speakerbeam.md` — added "Role in the TSE Survey Literature" section
  - `wiki/concepts/speaker-embedding.md` — added "Audio Clue Encoder Families in TSE" table
  - `wiki/concepts/film-layer.md` — added "Use in Target Speech Extraction" fusion-layer survey
  - `wiki/concepts/ideal-binary-mask.md` — added "Role in Target Speech Extraction" section
  - `wiki/synthesis/deep-speech-enhancement.md` — added Zmolikova 2023 reference in Insight 8 (TSE/PSE/OVC complementarity)

---

## [2026-08-20] ingest | SDP Min-max Common Part Estimation (Schepker & Doclo 2016)

- **Source**: `raw/papers/schepker-2016-sdp-minmax-acoustic-feedback/full-text.md` (Zotero: ADNDYTV8)
- **Authors**: Henning Schepker, Simon Doclo
- **Published**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 24, no. 2, pp. 246–257, Feb. 2016
- **DOI**: 10.1109/TASLP.2015.2507940
- **Summary**: Proposes a min-max SDP optimization for common part estimation of acoustic feedback paths, directly maximizing MSG (2–5 dB improvement over LS) with Lyapunov stability constraint, enabling faster AFC convergence and reduced variable-part parameters
- **Pages created**:
  - `wiki/sources/schepker-2016-sdp-minmax-acoustic-feedback.md`
  - `wiki/concepts/common-part-decomposition.md`
  - `wiki/concepts/min-max-common-part-estimation.md`
- **Pages updated**:
  - `wiki/entities/henning-schepker.md` — added paper, updated date, added Doclo cross-ref
  - `wiki/entities/simon-doclo.md` — added paper, updated date, added Schepker cross-ref
  - `wiki/concepts/adaptive-feedback-cancellation.md` — added common part decomposition section, added source
  - `wiki/concepts/maximum-stable-gain.md` — added min-max optimization section, added source
  - `wiki/concepts/prediction-error-method.md` — added common part integration section, added source
  - `wiki/concepts/hearing-aid-feedback-cancellation.md` — added common part decomposition section, added source

---

## [2026-08-20] ingest | AI Approaches in BSS Survey (Ansari 2023)

- **Source**: `raw/papers/ansari-2023-ai-bss-survey/full-text.md` (Zotero: ND66R5YG)
- **Authors**: Sam Ansari, Abbas Saad Alatrany, Khawla A. Alnajjar, Tarek Khater, Soliman Mahmoud, Dhiya Al-Jumeily, Abir Jaafar Hussain
- **Published**: Neurocomputing, 2023, art. 126895
- **DOI**: 10.1016/j.neucom.2023.126895
- **Summary**: Systematic literature survey of AI-based BSS proposing a three-way taxonomy (Classical ML / DL / Evolutionary), with benchmark tables, complexity comparison, and a forward-looking edge/mobile deployment roadmap. Applies the review-paper source-page template and the stricter concept-page threshold — only the AI-based-BSS taxonomy synthesis warranted updating the existing [[concepts/blind-source-separation]] page; no new concept pages were created.
- **Pages created**: 1 source (`wiki/sources/ansari-2023-ai-bss-survey.md`) + 7 entity pages (`wiki/entities/sam-ansari.md`, `abbas-saad-alatrany.md`, `khawla-a-alnajjar.md`, `tarek-khater.md`, `soliman-mahmoud.md`, `dhiya-al-jumeily.md`, `abir-jaafar-hussain.md`)
- **Pages updated**: 4 concept pages — `wiki/concepts/blind-source-separation.md` (added "AI-Based BSS Taxonomy" section with the three-way classification, cross-method findings, and open challenges), `wiki/concepts/tf-mask-estimation.md` (added DNN-based mask-prediction bullet and survey reference), `wiki/concepts/deep-clustering-speech-separation.md` (added survey reference), `wiki/concepts/cocktail-party-problem.md` (added survey reference)
- **Synthesis pages updated**: none — triage found only `deep-speech-enhancement.md` with 2 broad shared tags (deep-learning, survey), and the Ansari survey adds no new deep-speech-enhancement frontier data point, so the trigger checklist did not fire.
- **Routing note**: title contains "survey" — review-paper template applied (Summary / Taxonomy / Methodology / Applications Survey / Key Contributions / Limitations and Caveats). Stricter concept-page threshold applied; the survey's distinctive synthesis (the three-way AI-based-BSS taxonomy) was placed on the existing [[concepts/blind-source-separation]] page rather than spawning a new page.

---

## [2026-08-21] ingest | Feedback-guided DNN-based Controller Fusion for Robust Fixed-Parameter ANC (Bai 2026)

- **Source**: `raw/papers/bai-2026-feedback-guided-anc/full-text.md` (Zotero: MPHR6YAJ, arXiv: 2608.14061)
- **Authors**: Lu Bai, Yiming He, Xiaofeng Nan, Kai Chen, Jing Lu
- **Published**: arXiv preprint (eess.SY) 2026-08-14
- **DOI**: 10.48550/arXiv.2608.14061
- **Summary**: Proposes feedback-guided DNN-based controller fusion for robust fixed-parameter ANC — a causal WaveNet baseline fused with a feedback-guided mixture-of-experts of pre-trained per-path FIR experts, where the gating network consumes reference + control + delayed residual-error signals (unlike SFANC/GFANC which use reference-side features only). 10-expert streaming model attains 19.00 dB avg NR (50 Hz–5 kHz) on CCF-AATC headphone ANC with negligible 1–8 kHz amplification, at 32.69k params / 672.93 MMac/s with peak-MAC optimization (peak 34.62k → 14.15k per sample).
- **Pages created**:
  - `wiki/sources/bai-2026-feedback-guided-anc.md`
  - `wiki/entities/lu-bai.md`
  - `wiki/entities/yiming-he.md`
  - `wiki/entities/xiaofeng-nan.md`
  - `wiki/entities/kai-chen.md`
  - `wiki/concepts/feedback-guided-controller-fusion.md`
  - `wiki/concepts/frequency-aware-anc-loss.md`
- **Pages updated**:
  - `wiki/entities/jing-lu.md` — appended corresponding-author bullet + active-noise-control tag
  - `wiki/concepts/selective-fixed-filter-anc.md` — added "Feedback-Guided Controller Fusion (Bai 2026)" subsection contrasting with reference-only SFANC selection
  - `wiki/concepts/generative-fixed-filter-anc.md` — added "Feedback-Guided Fusion of Pre-Trained Experts (Bai 2026)" subsection
  - `wiki/concepts/hybrid-anc.md` — added "Feedforward–Feedback-Hybrid DNN (Bai 2026)" implementation architecture
  - `wiki/concepts/active-noise-control.md` — added Bai 2026 bullet under Deep Learning Approaches
  - `wiki/synthesis/ai-driven-anc.md` — added Section 2.5 (Feedback-Guided Controller Fusion as 4th architectural pattern), efficiency frontier table row, and Related Sources entry; new comparison axis: reference-only vs. reference+error feedback
  - `wiki/index.md`, `wiki/sources/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md` — 7 new entries, stats recounted
- **Extraction**: arXiv HTML via defuddle (v1 URL fallback after the unversioned URL returned 404); 5 figures (architecture, 2× NR spectra, time-domain, third-octave) downloaded and embedded as `![[raw/papers/.../figures/figN.png|caption]]`.

---

## [2026-08-22] ingest | Multi-Channel Differential ASR for Robust Wearer Speech Recognition on Smart Glasses (Yang et al. 2025)

- **Source**: `raw/papers/yang-2025-mc-differential-asr-smart-glasses/full-text.md` (Zotero: UVUJA5LX)
- **Authors**: Yufeng Yang, Yiteng Huang, Yong Xu, Li Wan, Suwon Shon, Yang Liu, Yifeng Fan, Zhaojun Yang, Olivier Siohan, Yue Liu, Ming Sun, Florian Metze
- **Published**: arXiv:2509.14430, 2025
- **DOI**: arXiv:2509.14430
- **Summary**: Multi-channel differential ASR — beamformer + close-mic + STD embedding as parallel frontends to a streaming RNN-T for robust wearer speech recognition on Ray-Ban Meta smart glasses; up to 18.0% relative WER reduction on real side-talk data over single-MVDR-frontend baseline.
- **Pages created**:
  - `raw/papers/yang-2025-mc-differential-asr-smart-glasses/full-text.md` — Defuddle extraction from arXiv HTML (4 figures downloaded)
  - `wiki/sources/yang-2025-mc-differential-asr-smart-glasses.md` — source page
  - `wiki/entities/yufeng-yang.md` — lead author (PhD intern at Meta)
  - `wiki/entities/yong-xu.md` — co-author (Meta)
  - `wiki/entities/suwon-shon.md` — co-author (Meta)
  - `wiki/entities/yang-liu.md` — co-author (Meta, also MMW side-talk rejection ASRU 2025)
  - `wiki/entities/yifeng-fan.md` — co-author (Meta)
  - `wiki/entities/zhaojun-yang.md` — co-author (Meta)
  - `wiki/entities/olivier-siohan.md` — co-author (Meta)
  - `wiki/entities/yue-liu.md` — co-author (Meta)
  - `wiki/entities/florian-metze.md` — co-author (CMU faculty; also AGADIR co-author)
  - `wiki/concepts/differential-asr.md` — novel framework introduced by this paper
  - `wiki/concepts/side-talk-detection.md` — VAD-adjacent task; distinctive TCN-based streaming formulation
  - `wiki/concepts/wearer-speech-recognition.md` — central research area for the smart-glasses ASR line (AGADIR, Feng 2025, Yang 2025)
- **Pages updated**:
  - `wiki/entities/li-wan.md` — appended new paper bullet + cross-ref
  - `wiki/entities/ming-sun.md` — appended new paper bullet
  - `wiki/entities/yiteng-huang.md` — appended new paper bullet
  - `wiki/concepts/nlcmv-beamforming.md` — added "WSR vs. Conversational Directional ASR" section contrasting NLCMV with adjusted MVDR
  - `wiki/concepts/mvdr-beamformer.md` — added "Wearer-Focused Adjusted MVDR (Yang 2025)" section + cross-refs to NLCMV and Differential ASR
  - `wiki/concepts/beamforming.md` — added "Differential ASR with MVDR Frontend" section
  - `wiki/concepts/voice-activity-detection.md` — added "Side-Talk Detection as Role-Conditional VAD" section
  - `wiki/concepts/multi-channel-speech-enhancement.md` — added Differential ASR technique bullet + cross-refs
  - `wiki/concepts/target-speaker-asr.md` — added "Privacy-Preserving Alternative: Differential ASR" section
  - `wiki/synthesis/multi-channel-speech-enhancement.md` — extended "where the decision lives" axis from {input, output} to {input, output, multi-frontend-fusion}; added Yang 2025 to Sources table and smart-glasses application row; updated thesis statement and Cross-Cutting Takeaway #4
  - `wiki/index.md`, `wiki/sources/index.md`, `wiki/entities/index.md`, `wiki/concepts/index.md`, `wiki/synthesis/index.md` — added 13 new entries; statistics updated to 1148/509/438/172/22/7

---

## [2026-08-22] ingest | Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters (Tesch & Gerkmann 2024)

- **Source**: `raw/papers/tesch-2024-spatially-selective-nonlinear-filters/full-text.md` (Zotero: LFX897WM, PDF key DZ3LMJ9U)
- **Authors**: Kristina Tesch, Timo Gerkmann
- **Published**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, 2024
- **DOI**: [10.1109/TASLP.2023.3334101](https://doi.org/10.1109/TASLP.2023.3334101)
- **Predecessor**: Tesch & Gerkmann, ICASSP 2023 [26]
- **Summary**: Journal extension of the ICASSP 2023 SSF paper. Systematically compares the steerable Spatially Selective Filter (SSF) against a PIT-trained Direct Separation (DS) baseline using matched JNF and McNet backbones. SSF advantage grows with speaker count (0.03 ΔPOLQA for 2 spk → 0.56 for 5 spk on McNet). Two blind DoA-estimation strategies (search-based and a compact DNN classifier) match oracle-DoA performance. Robustness experiments show trainable DoA-error tolerance, sharp sensitivity to >1 mm microphone perturbations, far-field/near-field trade-offs, per-speaker output decoupling in collocated-speaker scenarios, and superior generalization to unseen music noise.
- **Pages created**:
  - `wiki/sources/tesch-2024-spatially-selective-nonlinear-filters.md` (source)
  - `wiki/entities/kristina-tesch.md`, `wiki/entities/timo-gerkmann.md` (author entities)
  - `wiki/concepts/mcnet.md` (Multi-Cue Network architecture)
  - `wiki/concepts/direct-separation.md` (DS baseline with PIT)
  - `wiki/concepts/doa-informed-direct-separation.md` (iDS variant)
  - `wiki/concepts/dnn-based-doa-classifier.md` (proposed blind localizer)
  - `wiki/concepts/search-based-doa-estimation.md` (proposed search-based localizer)
- **Pages updated**:
  - `wiki/concepts/spatially-selective-nonlinear-filter.md` — added Tesch 2024 as the primary source; added "Multi-Speaker Separation (Tesch & Gerkmann 2024)" section with the SSF-vs-DS/iDS table, robustness findings, and blind-deployment strategies; clarified bidirectional F-LSTM conditioning; extended Related Concepts/Sources
  - `wiki/concepts/joint-nonlinear-filtering.md` — added Tesch 2024 as source; added "FT-JNF in Speech Separation" section describing the F-LSTM/T-LSTM stack in Tesch's terminology and the Williamson & Wang CRM expansion; extended Related Concepts/Sources
  - `wiki/concepts/target-speaker-extraction.md` — added Tesch 2024 to sources and Related Sources; extended SSF bullet in Spatial Methods to note the multi-speaker separation context and SSF-vs-DS finding

---

## [2026-08-22] ingest | Insights Into Deep Non-linear Filters for Improved Multi-channel Speech Enhancement (Tesch & Gerkmann 2023)

- **Source**: `raw/papers/tesch-2023-insights-deep-nonlinear-filters/full-text.md` (Zotero: QZMBNBLN)
- **Authors**: Kristina Tesch, Timo Gerkmann
- **Published**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, 2023
- **DOI**: 10.1109/TASLP.2022.3221046
- **Summary**: Systematic analysis of DNN-based joint non-linear spatial + tempo-spectral filters (JNF); introduces the FT-JNF architecture (two LSTM + FF with F→T sequence-dim switch) that outperforms an oracle MVDR + post-filter at low microphone counts and five SOTA baselines (EaBNet, FaSNet+TAC, COSPA, CRNN, T-JNF) on speaker extraction and CHiME3, with the fewest parameters (1.2M). Establishes that spectral information contributes more to spatial filtering than temporal information, and that joint non-linear filtering empirically validates the MMSE non-separability result for non-Gaussian noise. The FT-JNF backbone seeds the SSF (Tesch 2024), McNet, and NDF (Huang 2026) lineages.
- **Pages created**:
  - `wiki/sources/tesch-2023-insights-deep-nonlinear-filters.md` — source page with 6 figure embeds (Fig 1, 2, 4, 7, 8, 9), Tables II/III/IV, and six numbered Key Contributions
- **Pages updated**:
  - `wiki/entities/kristina-tesch.md` — wikilinked the existing Tesch 2023 [22] bullet to the new source page
  - `wiki/entities/timo-gerkmann.md` — wikilinked the existing Tesch 2023 [22] bullet to the new source page
  - `wiki/concepts/joint-nonlinear-filtering.md` — added Tesch 2023 to `sources:` frontmatter; added new "Information-Source Variants (Tesch & Gerkmann 2023)" section documenting the T-JNF/F-JNF/FT-JNF/NSF/PF variant family with the key empirical findings; added Tesch 2023 to `## Related Sources`
  - `wiki/concepts/spatially-selective-nonlinear-filter.md` — added Tesch 2023 to `sources:` frontmatter and `## Related Sources`
  - `wiki/concepts/mcnet.md` — added Tesch 2023 to `sources:` frontmatter and `## Related Sources`
  - `wiki/concepts/neural-directional-filtering.md` — added `sources:` field with Tesch 2023 (page previously had no sources field); added Tesch 2023 to `## Related Sources`
  - `wiki/synthesis/deep-speech-enhancement.md` — added Tesch 2023 to `sources:` frontmatter and Sources Synthesized table; expanded Insight 6 to split the end-to-end neural filter phase into two parallel lineages (2a. neural beamformers / filter-and-sum inspired vs 2b. mask-based non-linear joint filters), with Tesch 2023's FT-JNF as the type example of 2b; gap-fill trigger — the multi-channel synthesis previously omitted the foundational non-linear joint-filter lineage that later SSF/McNet/NDF works build on

---

## [2026-08-22] ingest | Speech extraction under extremely low SNR conditions (Ruan 2024)

- **Source**: `raw/papers/ruan-2024-speech-extraction-low-snr/full-text.md` (Zotero: N9UGYX3K)
- **Authors**: Haoxin Ruan, Lele Liao, Kai Chen, Jing Lu
- **Published**: Applied Acoustics 2024, Art. 110149
- **DOI**: 10.1016/j.apacoust.2024.110149
- **Summary**: OGIVE-based blind speech extraction at −20 dB SNR; real-speech cost-landscape analysis shows mixing-vector optimization is advantageous at extremely low SNR (wide flat convergence region); proposed natural-gradient variants (OGIVEa_NG best) match ILRMA separation across reverberant/real-room/noise-type conditions.
- **Pages created**: `wiki/sources/ruan-2024-speech-extraction-low-snr.md`, `wiki/entities/haoxin-ruan.md`, `wiki/entities/lele-liao.md`, `wiki/concepts/blind-source-extraction.md`, `wiki/concepts/independent-vector-extraction.md`, `wiki/concepts/ogive.md`, `wiki/concepts/natural-gradient.md`
- **Pages updated**: `wiki/entities/jing-lu.md` + `wiki/entities/kai-chen.md` (appended paper bullets), `wiki/concepts/independent-vector-analysis.md` (IVE/OGIVE/natural-gradient cross-refs, new source), `wiki/concepts/independent-low-rank-matrix-analysis.md` (low-SNR behavior note), `wiki/concepts/blind-source-separation.md` (BSE cross-ref), `wiki/synthesis/multi-channel-speech-enhancement.md` (blind-extraction branch paragraph in Insight 3 + sources table row)

---

## [2026-08-24] ingest | Fast Independent Vector Extraction (Scheibler & Ono 2020)

- **Source**: `raw/papers/scheibler-2020-fast-independent-vector-extraction/full-text.md` (Zotero: P4LS24WL, arXiv: 1910.10654)
- **Authors**: Robin Scheibler, Nobutaka Ono
- **Published**: IEEE ICASSP 2020, Barcelona, Spain
- **DOI**: 10.1109/ICASSP40776.2020.9053066
- **Summary**: FIVE — blind extraction of a single non-Gaussian source from a Gaussian background via iterative max-SINR beamforming with a target-suppressing reweighted background covariance; proven to globally minimize the OverIVA auxiliary function at every iteration via an exact eigendecomposition (special case of HEAD); peak SDR improvement in 1–3 iterations, ~5× faster than OverIVA and ≥10× faster than full AuxIVA.
- **Pages created**: `wiki/sources/scheibler-2020-fast-independent-vector-extraction.md`, `wiki/entities/robin-scheibler.md`, `wiki/concepts/fast-independent-vector-extraction.md`
- **Pages updated**: `wiki/entities/nobutaka-ono.md` (added FIVE contribution), `wiki/concepts/independent-vector-extraction.md` (FIVE in method families + convergence section), `wiki/concepts/ogive.md` (FIVE comparison section), `wiki/concepts/blind-source-extraction.md` (FIVE in method families), `wiki/concepts/independent-vector-analysis.md` (FIVE as EVD-family exemplar), `wiki/concepts/generalized-eigenvalue-decomposition.md` (FIVE application section), `wiki/concepts/blind-source-separation.md` (computational-cost cross-ref), `wiki/synthesis/multi-channel-speech-enhancement.md` (blind-extraction speed-frontier paragraph + timeline row)

---

## [2026-08-25] ingest | Exploiting Multi-Channel Speech Presence Probability in Parametric Multi-Channel Wiener Filter (Bagheri & Giacobello 2019)

- **Source**: `raw/papers/bagheri-2019-pmwf-spp/full-text.md` (Zotero: WNDECJQC)
- **Authors**: Saeed Bagheri, Daniele Giacobello
- **Published**: Interspeech 2019
- **DOI**: 10.21437/Interspeech.2019-2665
- **Summary**: Practical PMWF implementation exploiting MC-SPP in three ways — SPP-weighted noise PSD matrix tracking with direct Woodbury inverse updates, SPP-controlled trade-off parameter β(ℓ,k), and an MMSE output blend with a G_min suppression floor; outperforms MVDR and fixed-β MCWF on a 4-mic circular array (TIMIT, babble/pink NOISEX-92, T60 = 300 ms).
- **Pages created**: `wiki/sources/bagheri-2019-pmwf-spp.md`; `wiki/entities/saeed-bagheri.md`; `wiki/entities/daniele-giacobello.md`; `wiki/concepts/parametric-multi-channel-wiener-filter.md`; `wiki/concepts/multi-channel-speech-presence-probability.md`
- **Pages updated**: `wiki/concepts/multi-channel-wiener-filter.md` (PMWF section); `wiki/concepts/mvdr-beamformer.md` (MVDR as β=0 endpoint of PMWF); `wiki/concepts/speech-presence-probability.md` (MC-SPP extension section); `wiki/concepts/multichannel-mcra.md` (practical implementation with Woodbury inverse updates)
- **Synthesis**: triaged — no candidates passed tag-overlap threshold (all shared only 1 broad-topic tag)

---

## [2026-08-26] ingest | A low-complexity permutation alignment method for frequency-domain blind source separation (Kang 2019)

- **Source**: `raw/papers/kang-2019-low-complexity-permutation-alignment/full-text.md` (Zotero: IH67EZK3)
- **Authors**: Fang Kang, Feiran Yang, Jun Yang
- **Published**: Speech Communication, Vol. 112, 2019
- **DOI**: 10.1016/j.specom.2019.11.002
- **Summary**: Low-complexity three-stage permutation alignment for frequency-domain BSS — confidence-thresholded bin-wise alignment, local-centroid correction for low-confidence bins, then few-iteration global one-centroid clustering; matches Sawada/MBMC separation quality at 4–5× lower permutation-stage runtime.
- **Pages created**: `wiki/sources/kang-2019-low-complexity-permutation-alignment.md`, `wiki/entities/fang-kang.md`, `wiki/concepts/permutation-alignment.md`
- **Pages updated**: `wiki/entities/jun-yang.md` and `wiki/entities/feiran-yang.md` (new paper + BSS tags); `wiki/concepts/blind-source-separation.md`, `wiki/concepts/independent-vector-analysis.md`, `wiki/concepts/independent-low-rank-matrix-analysis.md` (permutation-alignment cross-refs, ILRMA runtime benchmark data point); `wiki/synthesis/multi-channel-speech-enhancement.md` (Kang 2019 row + "initialization-before-iteration" paragraph paralleling FIVE)

---

## [2026-08-27] ingest | A computationally efficient frequency-domain LMS algorithm with constraints on the adaptive filter (Rafaely & Elliott 2000)

- **Source**: `raw/papers/rafaely-2000-constrained-fdlms/full-text.md` (Zotero: KVF3QFKE)
- **Authors**: Boaz Rafaely, Stephen J. Elliott
- **Published**: IEEE Transactions on Signal Processing, vol. 48, no. 6, pp. 1649–1655, June 2000
- **DOI**: 10.1109/78.845922
- **Summary**: Extends the frequency-domain LMS algorithm with convex frequency-domain constraints (per-frequency magnitude limits, output-power limits, robust-stability margins for IMC feedback controllers) via a penalty-function formulation and steepest descent — implementable in real time on conventional DSP. Demonstrated on adaptive sound equalization, where a 4 dB magnitude constraint prevents the >20 dB filter peaks that conventional FDLMS produces away from the equalization microphone, and outperforms leaky LMS's global penalty.
- **Pages created**: `wiki/sources/rafaely-2000-constrained-fdlms.md`, `wiki/concepts/constrained-fdlms.md`
- **Pages updated**: `wiki/entities/boaz-rafaely.md` (added contribution + source), `wiki/entities/stephen-j-elliott.md` (added contribution + source), `wiki/concepts/output-constraint-anc-algorithms.md` (frequency-domain antecedent section), `wiki/concepts/leaky-fxlms-algorithm.md` (global-penalty limitations vs. explicit constraints), `wiki/concepts/robust-stability-constraint.md` (online enforcement via constrained FDLMS), `wiki/synthesis/nonlinear-anc-approaches.md` (output-constraint principle origin note)

---

## [2026-08-27] ingest | Detection of secondary-path irregularities in active noise control headphones (Guldenschuh & de Callafon 2014)

- **Source**: `raw/papers/guldenschuh-2014-secondary-path-irregularities/full-text.md` (Zotero: U78ASKLL)
- **Authors**: Markus Guldenschuh, Raymond de Callafon
- **Published**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 22, no. 7, 2014
- **DOI**: 10.1109/TASLP.2014.2321475
- **Summary**: In adaptive feedback ANC headphones (IMC + FxLMS), fit-induced secondary-path changes (leaks, lifting) mainly cause a low-frequency magnitude drop-off of G — additive uncertainty up to 17.3 dB below 300 Hz — which destabilizes both adaptation and feedback loop. Since W identifies G⁻¹, irregularities appear as DC-gain growth of W; a DC-gain stability constraint (Σ w_l < 1/U_max(0), 6 MACs per update) detects them without auxiliary noise or real-time FFT, interrupting adaptation and smoothly converging to a default filter (−20 dB scaled impulse) on violation.
- **Pages created**: `wiki/sources/guldenschuh-2014-secondary-path-irregularities.md`, `wiki/entities/markus-guldenschuh.md`, `wiki/entities/raymond-de-callafon.md`, `wiki/concepts/secondary-path-variability.md`, `wiki/concepts/dc-gain-stability-constraint.md`
- **Pages updated**: `wiki/concepts/leaky-fxlms-algorithm.md` (γ=0.005 data point, stabilizing adaptation under phase errors), `wiki/concepts/robust-stability-constraint.md` (time-domain DC reduction), `wiki/concepts/constrained-fdlms.md` (cost benchmark vs. 6-MAC check), `wiki/concepts/secondary-path-modeling.md` (headphone fit variability), `wiki/concepts/online-secondary-path-modeling.md` (feedback-headphone limitations), `wiki/concepts/uncertainty-modeling-for-anc.md` (headphone measurement data), `wiki/concepts/primary-path-variability.md` (contrast with secondary-path variability), `wiki/synthesis/feedback-anc-filter-design.md` (time-domain constraint checking section), `wiki/synthesis/secondary-path-modeling-evolution.md` (路线 5: 检测而非跟踪)

---

## [2026-08-30] ingest | 基于双传声器的蓝牙耳机降噪算法 (Yan, Qiu & Lu 2014)

- **Source**: `raw/papers/yan-2014-dual-mic-bt-noise-reduction/full-text.md` (MinerU extraction, language ch)
- **Authors**: Xinye Yan, Xiaojun Qiu (corresponding), Jing Lu — Key Laboratory of Modern Acoustics, Institute of Acoustics, Nanjing University
- **Published**: 应用声学 (Applied Acoustics) 2014, 33(3): 204–212
- **Summary**: 将双传声器降噪算法分为相干函数类（CPSD 为代表）与空间预分离类（ATF-GSC 为代表），在"约束语音损伤的最优滤波器"框架下统一分析：$\boldsymbol{h} = [\Phi_{xx} + \beta\Phi_{vv}]^{-1}\Phi_{xx}\boldsymbol{u}$（TF-GSC/SDW-MWF/GSC 失配分别为特例）。面向蓝牙耳机实现 ATF-GSC：安静环境预建模 RTF 阻塞矩阵对佩戴角度失配（0°/45°/90°）与不同使用者鲁棒；实验（白噪声/人声干扰/风噪声）表明 ATF-GSC 综合性能优于 CPSD，后者降噪量大但语音损伤严重（PESQ 最低）。
- **Pages created**:
  - `wiki/sources/yan-2014-dual-mic-bt-noise-reduction.md` — source page with system-model figure embed, taxonomy, methodology, and experimental comparison tables
  - `wiki/entities/xinye-yan.md` — first author (NJU)
  - `wiki/concepts/coherence-based-noise-reduction.md` — Le 1992/CPSD algorithm family, noise cross-PSD estimation as the key
  - `wiki/concepts/atf-gsc.md` — RTF-form GSC for two-mic BT headsets; pre-modeled blocking matrix robustness
  - `wiki/concepts/speech-distortion-constrained-noise-reduction.md` — SD-constrained optimal filter unifying TF-GSC/SDW-MWF/GSC-mismatch on one β trade-off curve
- **Pages updated**:
  - `wiki/entities/xiaojun-qiu.md` — appended Yan 2014 as corresponding author (merged with pre-existing ANC content; prior state restored from git after accidental overwrite)
  - `wiki/entities/jing-lu.md` — appended Yan 2014 co-author bullet
  - `wiki/concepts/gsc-beamformer.md` — new "ATF-GSC for Bluetooth Headsets" section (pre-modeled blocking matrix, β=1 equivalence under mismatch)
  - `wiki/concepts/multi-channel-wiener-filter.md` — new "Speech-Distortion-Constrained Generalization" section (SDW-MWF as β=μ=1 special case)
  - `wiki/concepts/spatial-coherence.md` — added 双传声器降噪 row to 应用 table
  - `wiki/concepts/relative-transfer-function.md` — new "Pre-modeled RTF for Near-Field Wearables" section
  - `wiki/synthesis/multi-channel-speech-enhancement.md` — added Yan 2014 to Sources Synthesized table (earliest entry, Application axis), new Bluetooth-headsets row in the Insight 7 application table, and a paragraph on the distortion-vs-NR trade-off axis the coherence lineage leaves implicit; added coherence/gsc/speech-distortion/bluetooth-headset tags to improve future triage recall
  - `wiki/index.md` + `wiki/{entities,concepts,sources,synthesis}/index.md` — new rows, Xiaojun Qiu summary updated, statistics updated (Total 1164→1169, Entities 513→514, Concepts 447→450, Sources 175→176)

---
---

## [2026-08-30] ingest | LPCNet: Improving Neural Speech Synthesis Through Linear Prediction (Valin & Skoglund 2018)

- **Source**: `raw/papers/valin-2018-lpcnet/full-text.md` (Zotero: ZGSNBWFM; arXiv 1810.11846, extracted from arXiv HTML via defuddle)
- **Authors**: Jean-Marc Valin (Mozilla), Jan Skoglund (Google LLC)
- **Published**: arXiv Oct 2018 (v2 Feb 2019); Proc. ICASSP 2019, Brighton, UK, pp. 5891–5895
- **DOI**: 10.48550/arXiv.1810.11846
- **Summary**: Introduces LPCNet — a WaveRNN variant that delegates spectral-envelope modeling to a classical all-pole LPC filter (derived from the 18-band Bark cepstrum via PSD → autocorrelation → Levinson-Durbin) so the network models only the spectrally flat excitation; with pre-emphasis before μ-law quantization (16 dB noise shaping at Nyquist), a DualFC output layer, precomputed μ-law embeddings, a pitch-correlation-driven sampling temperature with thresholding, and CELP-like μ-law-domain training noise injection, speaker-independent synthesis runs at ≈2.8 GFLOPS — real-time on a single Apple A8 (iPhone 6) core — an order of magnitude below WaveRNN/FFTNet/SampleRNN, with MUSHRA quality significantly above an equal-complexity WaveRNN+ baseline.
- **Pages created**: `wiki/sources/valin-2018-lpcnet.md`, `wiki/entities/jan-skoglund.md`, `wiki/concepts/wavernn.md`, `wiki/concepts/linear-prediction.md`, `wiki/concepts/dual-fc-layer.md`
- **Pages updated**: `wiki/concepts/lpcnet.md` (original-2018 architecture, efficiency techniques, complexity/MUSHRA — page previously described LPCNet only via the 2022 PLC paper), `wiki/entities/jean-marc-valin.md` (LPCNet bullet extended with source link + 2018 Mozilla affiliation note), `wiki/concepts/structured-sparsity.md` (LPCNet's 16×1 blocks + diagonal retention vs PercepNet's 16×4), `wiki/concepts/bark-scale-spectral-features.md` (new "Use in Neural Vocoding" section: 18 BFCC conditioning + LPC derivation), `wiki/concepts/gated-recurrent-unit.md` (LPCNet added to GRU-backbone list), `wiki/concepts/pitch-coherence.md` (precursor: global pitch correlation as conditioning + sampling temperature)
- **Figures**: 3 SVG figures downloaded from arXiv HTML (overview, training_noise2, mushra_line) into `raw/papers/valin-2018-lpcnet/figures/`; caption pairing verified against arXiv figure IDs (S3.F1/S3.F2/S4.F3)

---

## [2026-08-30] ingest | FARGAN: Very Low Complexity Speech Synthesis Using Framewise Autoregressive GAN with Pitch Prediction (Valin et al. 2024)

- **Source**: `raw/papers/valin-2024-fargan/full-text.md` (Zotero: 832PXENT)
- **Authors**: Jean-Marc Valin, Ahmed Mustafa, Jan Büthe
- **Published**: IEEE Signal Processing Letters 2024 (arXiv:2405.21069v2)
- **DOI**: 10.48550/arXiv.2405.21069
- **Summary**: FARGAN — a 600-MFLOPS framewise autoregressive GAN vocoder that uses long-term pitch prediction as a second autoregressive feedback and avoids teacher forcing by unrolling at training time; statistically tied with CARGAN and HiFi-GAN v1 at 64–110× lower complexity; replaced LPCNet in Opus 1.5's DRED.
- **Pages created**:
  - `wiki/sources/valin-2024-fargan.md`
  - `wiki/concepts/fargan.md`
  - `wiki/concepts/pitch-prediction.md`
  - `wiki/concepts/exposure-bias.md`
  - `wiki/synthesis/low-complexity-neural-vocoders.md` — new cross-source synthesis (LPCNet + FARGAN complexity-quality frontier)
- **Pages updated**:
  - `wiki/entities/jean-marc-valin.md` — FARGAN contribution bullet; Xiph.Org 2024 affiliation note
  - `wiki/entities/ahmed-mustafa.md` — FARGAN bullet (FWGAN lineage); sources frontmatter added
  - `wiki/entities/jan-buthe.md` — FARGAN bullet (NoLACE discriminator reuse); sources frontmatter added
  - `wiki/concepts/lpcnet.md` — new "Successor: FARGAN" section (dropped LPC filter, pitch prediction, Opus 1.5); Related Concepts/Sources extended
  - `wiki/concepts/pitch-coherence.md` — FARGAN paragraph completing the LPCNet → PercepNet → FARGAN pitch-feature progression
  - `wiki/concepts/bark-scale-spectral-features.md` — FARGAN inherits the 18-BFCC vector with no LPC analysis
  - `wiki/concepts/frequency-domain-loss.md` — FARGAN's six-resolution γ=0.5 spectral loss + STFT-discriminator findings
- **Figures**: 3 SVGs manually downloaded from arXiv HTML (`<object>` embeds are not auto-extracted); subframe-network layer labels recovered from per-glyph SVG text (Conv 2×1 → GRU1 → GRU2 → GRU3 → FC → FC → gain)
