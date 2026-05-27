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

---

## [2026-04-10] query (rewrite) | 如何估计次级通道

- **Answer updated**: `wiki/queries/how-to-estimate-secondary-path.md`
- **Summary**: Expanded from Kuo 1999 Section VI. Added: fundamental problem (y(n) causes biased convergence to 1/W(z)), additive random noise method with convergence analysis (online takes σ_d²/σ_v² times longer than offline), improvement techniques (adaptive noise cancellation ×30 speedup, adaptive predictor), overall modeling algorithm with 3 filters, comparison table, and multi-channel challenges.

---

## [2026-04-10] query (rewrite) | 如何估计次级通道

- **Answer updated**: `wiki/queries/how-to-estimate-secondary-path.md`
- **Summary**: Added two new methods: (1) Simultaneous Equations Method (Jin, Yang & Xiao 2007) — solves for W(z) and S(z) simultaneously from algebraic relations without auxiliary noise injection; (2) Genetic Algorithm (Chang & Chen 2010) — evolutionary search bypasses S(z) identification entirely, tolerant of nonlinearities but extremely high computation. Updated comparison table to 5 methods + pure delay approximation.

---

## [2026-04-10] query (rewrite) | 如何估计次级通道 — Zotero 文献综述

- **Answer updated**: `wiki/queries/how-to-estimate-secondary-path.md`
- **Summary**: Comprehensive rewrite based on 21 papers from Zotero library. Reorganized into 4 categories: (1) Explicit S(z) modeling — offline, additive noise (Yang 2026 RMFxLMS, Cao 2025 ELSTM-ANC-OSPM), overall modeling, coefficient update; (2) No auxiliary noise — simultaneous equations (Jin 2007, Fujii 1999, Kajikawa 2000); (3) No S(z) identification — SPR (Zhou 2007), evolutionary (GA: Chang 2010/96 cites, PSO: Rout 2012/72 cites), careful control (Lopes 2022/2024), meta-learning (Yang 2026); (4) Coping strategies — blended FxLMS (Sarkar 2025), modeling error analysis (Tabatabaei 2012/67 cites). Added full comparison table with 12 methods and 21 paper index.

---

## [2026-04-10] query (enhance) | 如何估计次级通道 — 添加 Zotero 链接

- **Answer updated**: `wiki/queries/how-to-estimate-secondary-path.md`
- **Summary**: Added `zotero://select/items/0_XXX` links to all 21 paper references (41 total link instances across inline tables and paper index). Clicking opens the paper directly in Zotero from Obsidian.

---

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

---

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

---

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

## [2026-04-12] ingest | Whisphone: Whispering Input Earbuds

- **Source**: `raw/papers/Fukumoto - 2025 - Whisphone whispering input earbuds.md` (Zotero: GD9G92MT, arXiv: 2501.01636)
- **Author**: Masaaki Fukumoto, Microsoft Corporation
- **Published**: arXiv preprint, 2025 (WISS2024 日文会议论文英文版)
- **Summary**: Whisphone — 利用 canal-type ANC 耳塞 + 耳道内 MEMS 麦克风捕捉骨传导耳语的私密语音输入设备。核心原理：耳道闭塞效应放大信号 ~10dB + ANC 降噪 ~30dB = 总 S/N 改善 40dB。在 80dB(A) 噪声下耳语识别 WER <10%（Google/Whisper，无需额外训练）。超过 80dB(A) 可切换正常语音仍保持私密。还探索了眨眼/舌头动作等亚听觉成分用于隐蔽控制命令。
- **Pages created/updated**:
  - `wiki/sources/fukumoto-2025-whisphone-paper-reading-note.md` — 完整中文阅读笔记
  - `wiki/index.md` — 更新
  - `wiki/log.md` — 记录

## [2026-04-12] ingest | Real-time Implementation of Delayed MPC in ANC Systems

- **Source**: `raw/papers/Liang 等 - 2026 - Real-time implementation of delayed model predictive control in active noise control systems.md` (Zotero: J5CZZBZ2, JSV 2026)
- **Authors**: Chao Liang, Francesco Ripamonti, Hamid Reza Karimi, Marek Pawełczyk
- **Published**: Journal of Sound and Vibration, Vol. 635, 119800, 2026
- **Summary**: 首次将延迟 MPC 实时应用于 ANC。核心洞察：主路径传播延迟 $N_{dp}$ 提供了免费的因果预览窗口——只要预测视界 $f < N_{dp}$，未来扰动全部已知，无需外部预测模型。推导出无约束 MPC 的解析闭式解，计算量仅比 FxNLMS 多 ~30%（921 vs 706 次乘法/样本）。实验验证：交通/飞机/人声/冲击噪声下降噪 13-19 dB，比 FxNLMS 提升 2.5-7.7 dB；冲击噪声 FxNLMS 完全无法抑制而 MPC 仍有效。瞬时收敛（无需迭代适应）。
- **Pages created/updated**:
  - `wiki/sources/liang-2026-delayed-mpc-anc-paper-reading-note.md` — 完整中文阅读笔记
  - `wiki/entities/chao-liang.md`, `wiki/entities/francesco-ripamonti.md`, `wiki/entities/marek-pawelczyk.md`
  - `wiki/index.md`, `wiki/log.md`

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

---

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

---

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
## [2026-04-17] ingest | Synthesis: Computational and Memory Efficiency
## [2026-04-17] ingest | Synthesis: AI-Driven Active Noise Control
## [2026-04-17] lint | Expanded AI-Driven ANC synthesis with details on SFANC, GFANC, and Deep ANC (CRN)
## [2026-04-17] lint | Health check: Created missing concept pages for Deep Learning for Signal Processing and Virtual Sensing; updated index
## [2026-04-18] ingest | It's ok to compare floating points for equality
## [2026-04-18] synthesis | Virtual Sensing Evolution: from RMT to Neural observation filters (Zotero)
## [2026-04-18] ingest | Source: Obs-TasNet paper (Neural Virtual Sensing)
## [2026-04-18] ingest | Added summary pages for 6 papers on Virtual Sensing
## [2026-04-18] synthesis | Head-Mounted ANC: Occlusion & Transparency (multi-modal convergence)
## [2026-04-18] ingest | Zhang 2024: Neural Network Augmented Kalman Filter for Robust Acoustic Howling Suppression
## [2026-04-18] ingest | Source: Karpathy: LLM OS
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

## [2026-04-22] ingest | Zhang 2022: Statistical signal processing approaches to analysis and synthesis of bone-conducted speech
- **Source**: `zotero://select/items/0_T6BE3UFG`
- **Summary**: Doctoral dissertation proposing WACF-CEP for noise-robust pitch extraction and LS-IIR for converting AC speech to synthetic BC speech.
- **Pages created/updated**:
  - `wiki/sources/zhang-2022-bone-conducted-speech-dissertation.md`
  - `wiki/sources/zhang-2022-bone-conducted-speech-reading-note.md`
  - `wiki/synthesis/multimodal-bc-speech-enhancement.md`
  - `wiki/index.md` — Updated statistics (167 pages)

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

---

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

---

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



## [2026-05-16] lint | Health check

- **Index consistency**: Found 6 entities, 6 concepts, 2 sources missing from main index; 4 synthesis pages over-counted in statistics (had 22 indexed, 18 actual). All gaps fixed.
- **Broken links**: None detected
- **Orphan pages**: N/A (all pages linked from index)
- **Statistics**: Updated from 398/156/144/70/22 to 408/162/150/72/18
- **Actions taken**: Added 14 missing index rows (6 entities, 6 concepts, 2 sources); corrected synthesis count; updated statistics.

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

---

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

---

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



---

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

---

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
