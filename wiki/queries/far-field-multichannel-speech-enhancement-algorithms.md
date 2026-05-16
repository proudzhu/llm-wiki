---
type: query
created: 2026-04-11
updated: 2026-04-12
sources:
  - raw/articles/far-field-multichannel-speech-enhancement.md
tags:
  - speech-enhancement
  - microphone-array
  - beamforming
  - dereverberation
  - deep-learning
  - zotero
---

# Far-Field Multichannel Speech Enhancement Algorithms

> 远场多麦克风语音增强算法综述。基于 Zotero 文献库整理，涵盖传统信号处理、统计模型与深度学习方法。

---

## 1. 问题定义与信号模型

远场多麦克风语音增强目标：从 $M$ 个麦克风观测信号 $\mathbf{y}(t) \in \mathbb{R}^M$ 中恢复目标语音 $s(t)$。

**STFT 域信号模型**（噪声+混响）：
$$Y_m(k,n) = H_{m}(k,n)S(k,n) + V_m(k,n)$$

其中 $H_m(k,n)$ 为声学传递函数（含直达声与混响），$V_m(k,n)$ 为加性噪声。

**核心挑战**：
- 加性噪声（稳态/非稳态）
- 房间混响（早期反射 + 晚期混响）
- 说话人位置未知/移动
- 麦克风阵列孔径受限
- 计算复杂度与实时性约束

---

## 2. 经典波束形成（Beamforming）

### 2.1 延迟求和波束形成器（DS）

最基本的线性波束形成器：
$$w_{\text{DS}}(\theta) = \frac{1}{M} \mathbf{d}(k,\theta)$$

其中 $\mathbf{d}(k,\theta) = [1, e^{-j2\pi f \tau_2(\theta)}, \dots, e^{-j2\pi f \tau_M(\theta)}]^T$ 为**导向向量（steering vector）**，$\tau_m(\theta)$ 为第 $m$ 个麦克风相对于参考麦克风的传播延迟。

**算法步骤**：
1. 计算每个麦克风信号相对于目标方向 $\theta_0$ 的时延补偿：$\tau_m(\theta_0) = \frac{\mathbf{p}_m \cdot \mathbf{u}(\theta_0)}{c}$，其中 $\mathbf{p}_m$ 为麦克风位置，$\mathbf{u}(\theta_0)$ 为目标方向单位向量，$c$ 为声速
2. 对每个通道施加时延补偿：$y_m[n] = x_m[n - \tau_m(\theta_0)]$
3. 求和平均：$y[n] = \frac{1}{M}\sum_{m=1}^{M} y_m[n]$

**频域实现**：
$$Y(k,n) = \frac{1}{M}\sum_{m=1}^{M} X_m(k,n) \cdot e^{j2\pi k \tau_m(\theta_0)/N}$$

**方向性因子（Directivity Factor）**：
$$D = \frac{| \mathbf{w}^H \mathbf{d} |^2}{\mathbf{w}^H \mathbf{w}} = M$$

对于均匀线性阵列（ULA），波束宽度近似为：
$$\theta_{\text{3dB}} \approx 0.886 \frac{\lambda}{Md} \quad (\text{弧度})$$

特点：固定波束形成，鲁棒但增益有限。白噪声增益（WNG）为 $M$，即信噪比改善 $10\log_{10}(M)$ dB。

### 2.2 最小方差无畸变响应（MVDR）

**参考文献库**：
- Souden et al., [*"On Optimal Frequency-Domain Multichannel Linear Filtering for Noise Reduction"*](zotero://select/items/0_SHZJBBAL), IEEE TASLP — 库中标记为 **PMWF**，推导了参数化多通道非因果维纳滤波器的闭式解，统一了 MVDR 与 GSC 框架
- Grondain et al., [*"Gray Jedi MVDR Post-filtering"*](zotero://select/items/0_REPCYC4D) (2023, preprint) — MVDR 后滤波改进

**优化准则**：
$$\mathbf{w}_{\text{MVDR}}(k) = \arg\min_{\mathbf{w}} \mathbf{w}^H \mathbf{\Phi}_{vv} \mathbf{w} \quad \text{s.t.} \quad \mathbf{w}^H \mathbf{d} = 1$$

闭式解：
$$\mathbf{w}_{\text{MVDR}} = \frac{\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}{\mathbf{d}^H \mathbf{\Phi}_{vv}^{-1}\mathbf{d}}$$

**详细推导**：

使用 Lagrange 乘子法。构造拉格朗日函数：
$$\mathcal{L}(\mathbf{w}, \lambda) = \mathbf{w}^H \mathbf{\Phi}_{vv} \mathbf{w} + \lambda(\mathbf{w}^H \mathbf{d} - 1) + \lambda^*(\mathbf{d}^H \mathbf{w} - 1)$$

对 $\mathbf{w}$ 求导并置零：
$$\frac{\partial \mathcal{L}}{\partial \mathbf{w}^*} = \mathbf{\Phi}_{vv}\mathbf{w} + \lambda \mathbf{d} = \mathbf{0} \implies \mathbf{w} = -\lambda \mathbf{\Phi}_{vv}^{-1}\mathbf{d}$$

代入约束 $\mathbf{w}^H \mathbf{d} = 1$：
$$-\lambda^* \mathbf{d}^H \mathbf{\Phi}_{vv}^{-1}\mathbf{d} = 1 \implies \lambda^* = -\frac{1}{\mathbf{d}^H \mathbf{\Phi}_{vv}^{-1}\mathbf{d}}$$

因此：
$$\mathbf{w}_{\text{MVDR}} = \frac{\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}{\mathbf{d}^H \mathbf{\Phi}_{vv}^{-1}\mathbf{d}}$$

**输出信噪比**：
$$\text{SNR}_{\text{out}} = \frac{|\mathbf{w}^H \mathbf{d}|^2 \phi_{ss}}{\mathbf{w}^H \mathbf{\Phi}_{vv} \mathbf{w}} = \mathbf{d}^H \mathbf{\Phi}_{vv}^{-1} \mathbf{d} \cdot \phi_{ss}$$

**实用估计算法**：

1. **噪声 PSD 矩阵估计**（语音缺席期间）：
   $$\widehat{\mathbf{\Phi}}_{vv}(k,n) = \alpha \widehat{\mathbf{\Phi}}_{vv}(k,n-1) + (1-\alpha)\mathbf{y}(k,n)\mathbf{y}^H(k,n)$$
   其中 $\alpha \approx 0.8 \sim 0.95$ 为平滑因子

2. **RTF 向量估计**（相干/扩散场模型）：
   $$\mathbf{d} = \frac{\text{principal eigenvector of } \mathbf{\Phi}_{yy}}{\text{first element}}$$

3. **正则化**（防止矩阵病态）：
   $$\mathbf{w}_{\text{MVDR}} = \frac{(\mathbf{\Phi}_{vv} + \epsilon \mathbf{I})^{-1}\mathbf{d}}{\mathbf{d}^H (\mathbf{\Phi}_{vv} + \epsilon \mathbf{I})^{-1}\mathbf{d}}$$
   其中 $\epsilon = 10^{-3} \cdot \text{trace}(\mathbf{\Phi}_{vv})/M$

关键：需要准确估计 **RTF 向量** $\mathbf{d}$ 和 **噪声 PSD 矩阵** $\mathbf{\Phi}_{vv}$。

### 2.3 广义旁瓣对消器（GSC）

**参考文献库**：
- Souden et al. — 库中标注：GSC 与参数化多通道维纳滤波器的关系 [↗](zotero://select/items/0_SHZJBBAL)
- Spriet et al., [*"Spatially pre-processed speech distortion weighted multi-channel Wiener filtering for noise reduction"*](zotero://select/items/0_7VMZFQG7) — 库中标注 **To Read**，提出空间预处理的 SDW-MWF

GSC 将约束优化转为无约束优化：
$$\mathbf{w}_{\text{GSC}} = \mathbf{w}_q - \mathbf{B} \mathbf{w}_a$$

其中：
- $\mathbf{w}_q$ 为准静态波束形成器（通常取 DS：$\mathbf{w}_q = \mathbf{d}/M$），满足 $\mathbf{w}_q^H \mathbf{d} = 1$
- $\mathbf{B}$ 为阻塞矩阵（blocking matrix），满足 $\mathbf{B}^H \mathbf{d} = \mathbf{0}$，即阻塞目标信号
- $\mathbf{w}_a$ 为自适应权重，通过最小化输出功率得到

**详细推导**：

将 GSC 结构代入 MVDR 优化目标：
$$\min_{\mathbf{w}_a} (\mathbf{w}_q - \mathbf{B}\mathbf{w}_a)^H \mathbf{\Phi}_{vv} (\mathbf{w}_q - \mathbf{B}\mathbf{w}_a)$$

对 $\mathbf{w}_a$ 求导：
$$-2\text{Re}\{\mathbf{B}^H \mathbf{\Phi}_{vv}(\mathbf{w}_q - \mathbf{B}\mathbf{w}_a)\} = \mathbf{0}$$

解得：
$$\mathbf{w}_a = (\mathbf{B}^H \mathbf{\Phi}_{vv} \mathbf{B})^{-1} \mathbf{B}^H \mathbf{\Phi}_{vv} \mathbf{w}_q$$

**阻塞矩阵构造**：

对于 $M$ 个麦克风，阻塞矩阵 $\mathbf{B} \in \mathbb{C}^{M \times (M-1)}$ 的列空间与 $\mathbf{d}$ 正交。一种常用构造：

$$\mathbf{B} = \begin{bmatrix}
-d_2^* & -d_3^* & \cdots & -d_M^* \\
d_1^* & 0 & \cdots & 0 \\
0 & d_1^* & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & d_1^*
\end{bmatrix}$$

**自适应算法**（NLMS）：
$$\mathbf{w}_a[n+1] = \mathbf{w}_a[n] + \mu \frac{\mathbf{z}[n] e^*[n]}{\|\mathbf{z}[n]\|^2 + \delta}$$

其中 $\mathbf{z}[n] = \mathbf{B}^H \mathbf{y}[n]$ 为阻塞矩阵输出（噪声参考），$e[n] = \mathbf{w}_q^H \mathbf{y}[n] - \mathbf{w}_a^H[n] \mathbf{z}[n]$ 为误差信号。

**GSC 与 MVDR 的等价性**：可以证明，当 $\mathbf{w}_a$ 收敛到最优值时，$\mathbf{w}_{\text{GSC}} = \mathbf{w}_{\text{MVDR}}$。GSC 的优势在于将约束优化转为无约束自适应问题，便于在线实现。

### 2.4 差分波束形成

**参考文献库**：
- Jin et al. (2023), [*"Differential Beamforming From a Geometric Perspective"*](zotero://select/items/0_NCDQUQGD) — 从几何视角分析差分波束形成，讨论方向性因子与白噪声增益
- Buck, [*"Aspects of first-order differential microphone arrays in the presence of sensor imperfections"*](zotero://select/items/0_SGCWALN2) — 库中已读，分析传感器非理想性
- Xiong et al. (2026, preprint), [*"A directional-derivative-constrained method for continuously steerable differential beamformers with uniform circular arrays"*](zotero://select/items/0_I72LCJH7) — 最新进展

差分波束形成利用声压梯度信息，适用于小孔径阵列。

**一阶差分麦克风阵列（FDMA）**：

两个间距为 $d$ 的全向麦克风，差分输出：
$$y[n] = x_1[n] - \beta x_2[n - \Delta]$$

其中 $\beta$ 为加权系数，$\Delta$ 为整数延迟。

**频率响应**：
$$H(\omega, \theta) = 1 - \beta e^{-j\omega(\Delta - d\cos\theta/c)}$$

**心型指向**（cardioid）：取 $\beta = 1$，$\Delta = d/c$：
$$|H(\omega, \theta)| = 2\left|\sin\left(\frac{\omega d}{2c}(1 - \cos\theta)\right)\right|$$

低频近似（$\omega d/c \ll 1$）：
$$H(\omega, \theta) \approx \frac{\omega d}{c}(1 + \cos\theta)$$

**方向性因子（DI）**：
- 一阶差分：$\text{DI} = 4.8$ dB（心型）
- $N$ 阶差分：$\text{DI} = 10\log_{10}(N+1)^2$ dB

**白噪声增益（WNG）**：
$$\text{WNG} = \frac{|H(\omega, \theta_0)|^2}{\sum_{m=1}^{M} |w_m|^2}$$

差分局阵的 WNG 随频率降低而恶化（$\propto (\omega d/c)^2$），这是低频段的主要问题。

**Xiong et al. (2026) 方向导数约束方法**：

提出在 UCA 上构建连续可控差分局阵。核心思想：将方向导数约束作为优化条件：
$$\min_{\mathbf{w}} \mathbf{w}^H \mathbf{w} \quad \text{s.t.} \quad \mathbf{w}^H \mathbf{d}(\theta_0) = 1, \quad \frac{\partial}{\partial\theta}\mathbf{w}^H \mathbf{d}(\theta)\Big|_{\theta=\theta_0} = 0$$

### 2.5 深度学习波束形成

**参考文献库**：
- Chen et al. (2026, preprint), [*"Neural network-based time-frequency-bin-wise linear combination of beamformers for underdetermined target source extraction"*](zotero://select/items/0_R4362BJ2) — 最新：基于神经网络在 TF 单元级别线性组合多个波束形成器
- Kienegger & Gerkmann (2026, preprint), [*"Autoregressive guidance of deep spatially selective filters using bayesian tracking for efficient extraction of moving speakers"*](zotero://select/items/0_IKQ4EY2A) — 贝叶斯跟踪 + 深度空域滤波
- Bologni & Larraza (2026, preprint), [*"A two-step approach for speech enhancement in low-SNR scenarios using cyclostationary beamforming and DNNs"*](zotero://select/items/0_C7E6EULK) — 低信噪比下平稳性波束形成+DNN 两步法

**Chen et al. (2026) Neural BF 组合方法**：

在 TF 单元 $(k,n)$ 级别，网络输出多个预计算波束形成器的加权组合：
$$\mathbf{w}(k,n) = \sum_{r=1}^{R} \alpha_r(k,n) \mathbf{w}_r(k)$$

其中 $\mathbf{w}_r$ 为预计算的波束形成器（如 MVDR、DS、null-former 等），$\alpha_r(k,n)$ 由网络预测，满足 $\sum_r \alpha_r = 1$。

网络输入：多通道 STFT 特征（IPD、ILD、对数功率谱）
网络输出：$R$ 个权重 $\alpha_r(k,n)$

**Kienegger & Gerkmann (2026) 贝叶斯跟踪深度滤波**：

将深度空间滤波器的参数建模为贝叶斯后验分布：
$$p(\mathbf{w}_n | \mathbf{y}_{1:n}) \propto p(\mathbf{y}_n | \mathbf{w}_n) \cdot p(\mathbf{w}_n | \mathbf{w}_{n-1})$$

其中状态转移 $p(\mathbf{w}_n | \mathbf{w}_{n-1})$ 由说话人运动模型建模，观测似然 $p(\mathbf{y}_n | \mathbf{w}_n)$ 由深度滤波器输出。

---

## 3. 多通道维纳滤波（MWF）及其变体

### 3.1 多通道维纳滤波器（MCWF）

最优线性估计器（MMSE 意义下）：
$$\mathbf{w}_{\text{MCWF}} = (\mathbf{\Phi}_{ss} + \mathbf{\Phi}_{vv})^{-1}\mathbf{\Phi}_{ss}\mathbf{d}$$

需要估计 **语音 PSD 矩阵** $\mathbf{\Phi}_{ss}$ 和 **噪声 PSD 矩阵** $\mathbf{\Phi}_{vv}$。

**详细推导**：

MCWF 最小化均方误差：
$$\mathbf{w}_{\text{MCWF}} = \arg\min_{\mathbf{w}} E\{|S(k,n) - \mathbf{w}^H \mathbf{y}(k,n)|^2\}$$

展开代价函数：
$$J(\mathbf{w}) = E\{|S|^2\} - \mathbf{w}^H E\{\mathbf{y}S^*\} - E\{S\mathbf{y}^H\}\mathbf{w} + \mathbf{w}^H E\{\mathbf{y}\mathbf{y}^H\}\mathbf{w}$$

其中：
- $E\{\mathbf{y}\mathbf{y}^H\} = \mathbf{\Phi}_{yy} = \mathbf{\Phi}_{ss} + \mathbf{\Phi}_{vv}$
- $E\{\mathbf{y}S^*\} = \mathbf{\Phi}_{ss}\mathbf{d}$（假设语音与噪声不相关）

对 $\mathbf{w}$ 求导并置零：
$$\frac{\partial J}{\partial \mathbf{w}^*} = -\mathbf{\Phi}_{ss}\mathbf{d} + (\mathbf{\Phi}_{ss} + \mathbf{\Phi}_{vv})\mathbf{w} = \mathbf{0}$$

解得：
$$\mathbf{w}_{\text{MCWF}} = (\mathbf{\Phi}_{ss} + \mathbf{\Phi}_{vv})^{-1}\mathbf{\Phi}_{ss}\mathbf{d}$$

**与 MVDR 的关系**：

MCWF 可以重写为 MVDR 加一个标量 Wiener 后滤波器：
$$\mathbf{w}_{\text{MCWF}} = \underbrace{\frac{(\mathbf{\Phi}_{vv} + \mu^{-1}\mathbf{\Phi}_{ss})^{-1}\mathbf{d}}{\mathbf{d}^H(\mathbf{\Phi}_{vv} + \mu^{-1}\mathbf{\Phi}_{ss})^{-1}\mathbf{d}}}_{\text{空间滤波器}} \cdot \underbrace{\frac{\phi_s}{\phi_s + \mu/\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}}_{\text{后滤波器}}$$

当 $\mu=1$ 时，MCWF = MVDR × Wiener 增益。

**秩-1 近似**：

假设点声源模型，$\mathbf{\Phi}_{ss} = \phi_{ss} \mathbf{d}\mathbf{d}^H$（秩-1 矩阵）。利用矩阵求逆引理：
$$(\mathbf{\Phi}_{vv} + \phi_{ss}\mathbf{d}\mathbf{d}^H)^{-1} = \mathbf{\Phi}_{vv}^{-1} - \frac{\phi_{ss}\mathbf{\Phi}_{vv}^{-1}\mathbf{d}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}}{1 + \phi_{ss}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}$$

代入 MCWF 公式：
$$\mathbf{w}_{\text{MCWF}} = \frac{\phi_{ss}\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}{1 + \phi_{ss}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}} = \frac{\phi_{ss}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}{1 + \phi_{ss}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}} \cdot \mathbf{w}_{\text{MVDR}}$$

即 MCWF = $G_{\text{Wiener}} \cdot \mathbf{w}_{\text{MVDR}}$，其中 Wiener 增益 $G_{\text{Wiener}} = \frac{\xi}{1+\xi}$，$\xi = \phi_{ss}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}$ 为输出信噪比。

### 3.2 语音失真加权多通道维纳滤波（SDW-MWF）

**参考文献库**：
- Spriet et al. — 库中标注 **To Read** [↗](zotero://select/items/0_7VMZFQG7)
- Souden et al. — 库中标注 PMWF [↗](zotero://select/items/0_SHZJBBAL)

在噪声抑制与语音失真之间引入权衡参数 $\mu$：
$$\mathbf{w}_{\text{SDW-MWF}} = (\mathbf{\Phi}_{ss} + \mu\mathbf{\Phi}_{vv})^{-1}\mathbf{\Phi}_{ss}\mathbf{d}$$

**代价函数**：
$$J(\mathbf{w}) = E\{|S - \mathbf{w}^H\mathbf{y}|^2\} + (\mu-1)E\{|\mathbf{w}^H\mathbf{v}|^2\}$$

其中第一项为语音失真 + 残余噪声，第二项惩罚残余噪声功率。$\mu$ 控制两者之间的权衡：

| $\mu$ 值 | 行为 | 噪声抑制 | 语音失真 |
|----------|------|----------|----------|
| $\mu = 1$ | 标准 MCWF | 中等 | 低 |
| $\mu > 1$ | 更激进的噪声抑制 | 高 | 较高 |
| $\mu < 1$ | 更保守 | 低 | 更低 |
| $\mu \to \infty$ | 趋近 MVDR（无语音失真） | 最低 | 最低 |

**秩-1 近似下的闭式解**：

$$\mathbf{w}_{\text{SDW-MWF}} = \frac{\phi_{ss}\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}{\mu + \phi_{ss}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}} = \frac{\xi/\mu}{1 + \xi/\mu} \cdot \mathbf{w}_{\text{MVDR}}$$

其中 $\xi = \phi_{ss}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}$。

### 3.3 参数化多通道维纳滤波（PMWF）

**参考文献库**：
- Souden et al., 库中标注 **PMWF, To Read** [↗](zotero://select/items/0_SHZJBBAL)

通过单一参数统一 MVDR ($\mu \to \infty$) 与 MCWF ($\mu = 1$)：
$$\mathbf{w}_{\text{PMWF}} = \frac{(\mathbf{\Phi}_{vv} + \mu^{-1}\mathbf{\Phi}_{ss})^{-1}\mathbf{d}}{\mathbf{d}^H(\mathbf{\Phi}_{vv} + \mu^{-1}\mathbf{\Phi}_{ss})^{-1}\mathbf{d}}$$

注意与 SDW-MWF 的区别：PMWF 对滤波器进行**归一化**（保持无畸变响应 $\mathbf{w}^H\mathbf{d} = 1$），而 SDW-MWF 不归一化（允许语音失真换取更多噪声抑制）。

**与 MVDR 的关系**：

利用秩-1 近似 $\mathbf{\Phi}_{ss} = \phi_{ss}\mathbf{d}\mathbf{d}^H$ 和矩阵求逆引理：

$$(\mathbf{\Phi}_{vv} + \mu^{-1}\phi_{ss}\mathbf{d}\mathbf{d}^H)^{-1}\mathbf{d} = \mathbf{\Phi}_{vv}^{-1}\mathbf{d} - \frac{\mu^{-1}\phi_{ss}\mathbf{\Phi}_{vv}^{-1}\mathbf{d}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}{1 + \mu^{-1}\phi_{ss}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}} = \frac{\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}{1 + \mu^{-1}\phi_{ss}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}$$

分母：
$$\mathbf{d}^H(\mathbf{\Phi}_{vv} + \mu^{-1}\phi_{ss}\mathbf{d}\mathbf{d}^H)^{-1}\mathbf{d} = \frac{\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}{1 + \mu^{-1}\phi_{ss}\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}$$

因此：
$$\mathbf{w}_{\text{PMWF}} = \frac{\mathbf{\Phi}_{vv}^{-1}\mathbf{d}}{\mathbf{d}^H\mathbf{\Phi}_{vv}^{-1}\mathbf{d}} = \mathbf{w}_{\text{MVDR}}$$

**关键结论**：在秩-1 假设下，PMWF **恒等于** MVDR，与 $\mu$ 无关！这说明 PMWF 的真正价值在于**非秩-1** 场景（如扩散噪声场、多声源）。

### 3.4 基于 GEVD 的 SDW-MWF

**参考文献库**：
- Zhang et al. (2023), [*"SDW-SWF: Speech Distortion Weighted Single-Channel Wiener Filter for Noise Reduction"*](zotero://select/items/0_G92LE4HL) — 利用 GEVD 低秩近似

利用广义特征值分解估计协方差矩阵，提高鲁棒性。

**GEVD 方法**：

对 $\mathbf{\Phi}_{yy}$ 和 $\mathbf{\Phi}_{vv}$ 进行广义特征值分解：
$$\mathbf{\Phi}_{yy} \mathbf{q}_i = \lambda_i \mathbf{\Phi}_{vv} \mathbf{q}_i$$

其中 $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_M > 0$。在点声源假设下，最大特征值 $\lambda_1$ 对应语音+噪声子空间，其余对应纯噪声子空间。

**低秩近似**：
$$\mathbf{\Phi}_{ss} \approx (\lambda_1 - 1)\mathbf{\Phi}_{vv}\mathbf{q}_1\mathbf{q}_1^H\mathbf{\Phi}_{vv}$$

代入 SDW-MWF：
$$\mathbf{w}_{\text{GEVD-SDW-MWF}} = \frac{(\lambda_1 - 1)\mathbf{q}_1\mathbf{q}_1^H\mathbf{\Phi}_{vv}\mathbf{d}}{\mu + (\lambda_1 - 1)\mathbf{q}_1^H\mathbf{\Phi}_{vv}\mathbf{d}}$$

GEVD 的优势在于不需要显式估计 $\mathbf{\Phi}_{ss}$，直接从 $\mathbf{\Phi}_{yy}$ 和 $\mathbf{\Phi}_{vv}$ 的特征结构提取语音子空间。

### 3.5 分布式多通道维纳滤波

**参考文献库**：
- Didier & Waterschoot (2026, preprint), [*"Distributed multichannel wiener filtering for wireless acoustic sensor networks"*](zotero://select/items/0_43GZERAY) — 最新

适用于分布式麦克风网络（WASN）。

**问题设置**：

$N$ 个节点，每个节点有 $M_n$ 个麦克风。总通道数 $M = \sum_n M_n$。中心化 MWF 需要所有节点将原始数据发送到融合中心，通信开销 $O(M)$。

**分布式算法**（扩散 LMS 类型）：

每个节点 $n$ 维护局部滤波器 $\mathbf{w}_n$ 和协方差估计 $\mathbf{\Phi}_{vv}^{(n)}$。迭代：

1. **自适应步**（局部更新）：
   $$\mathbf{w}_n^{(i+1/2)} = \mathbf{w}_n^{(i)} - \mu \nabla_{\mathbf{w}_n^*} J_n(\mathbf{w}_n^{(i)})$$

2. **组合步**（邻居信息融合）：
   $$\mathbf{w}_n^{(i+1)} = \sum_{l \in \mathcal{N}_n} c_{nl} \mathbf{w}_l^{(i+1/2)}$$

其中 $\mathcal{N}_n$ 为节点 $n$ 的邻居集合，$c_{nl}$ 为组合权重（通常取 Metropolis 或最大度数规则）。

**收敛性**：在连通图假设下，分布式算法收敛到中心化 MWF 解。

---

## 4. 噪声 PSD 矩阵估计

### 4.1 基于语音存在概率（SPP）的估计

**参考文献库**：
- Souden et al., [*"Gaussian Model-Based Multichannel Speech Presence Probability"*](zotero://select/items/0_KTE6J37S) — 库中标注 **To Read**，基于高斯模型的多通道 SPP
- Bagheri et al. (2019), [*"Exploiting Multi-Channel Speech Presence Probability in Parametric Multi-Channel Wiener Filter"*](zotero://select/items/0_WNDECJQC) — 库中标注 **To Read**
- Ji & Baek, [*"A priori SAP estimator based on the magnitude square coherence for dual-channel microphone system"*](zotero://select/items/0_W32YYPPA) — 库中标注 **⭐⭐⭐⭐⭐**，利用 MSC 估计语音缺席概率

利用语音存在概率加权更新噪声 PSD：
$$\widehat{\mathbf{\Phi}}_{vv}(k,n) = \alpha \widehat{\mathbf{\Phi}}_{vv}(k,n-1) + (1-\alpha)(1-p(k,n))\mathbf{y}(k,n)\mathbf{y}^H(k,n)$$

**语音存在概率 $p(k,n)$ 的计算**：

基于似然比检验。定义两个假设：
- $H_1$：语音存在，$\mathbf{y} \sim \mathcal{CN}(\mathbf{0}, \mathbf{\Phi}_{ss} + \mathbf{\Phi}_{vv})$
- $H_0$：语音缺席，$\mathbf{y} \sim \mathcal{CN}(\mathbf{0}, \mathbf{\Phi}_{vv})$

似然比：
$$\Lambda(k,n) = \frac{p(\mathbf{y}|H_1)}{p(\mathbf{y}|H_0)} = \frac{1}{\det(\mathbf{I} + \mathbf{\Phi}_{vv}^{-1}\mathbf{\Phi}_{ss})} \exp\left(\mathbf{y}^H[\mathbf{\Phi}_{vv}^{-1} - (\mathbf{\Phi}_{ss}+\mathbf{\Phi}_{vv})^{-1}]\mathbf{y}\right)$$

语音存在概率：
$$p(k,n) = \left[1 + \frac{1-q(k,n)}{q(k,n)} \cdot \frac{1}{\Lambda(k,n)}\right]^{-1}$$

其中 $q(k,n)$ 为语音先验存在概率（通常取 0.5）。

**Gaussian Model 简化**（Souden et al.）：

在秩-1 假设下，似然比简化为：
$$\Lambda(k,n) = \frac{1}{1+\xi} \exp\left(\frac{\xi}{1+\xi} |\mathbf{w}_{\text{MVDR}}^H \mathbf{y}|^2 / \phi_{vv}\right)$$

其中 $\xi$ 为先验信噪比。

### 4.2 基于 coherence 的估计

**参考文献库**：
- Schwarz & Kellermann (2015), ["Coherent-to-Diffuse Power Ratio Estimation for Dereverberation"](zotero://select/items/0_AT69JCEX) — 库中标注 **⭐⭐⭐⭐⭐**, TASLP, 139 citations
- Ji & Baek — 利用幅度平方相干性 (MSC) [↗](zotero://select/items/0_W32YYPPA)

**幅度平方相干性（MSC）**：
$$\Gamma_{xy}(k,n) = \frac{|\widehat{\phi}_{xy}(k,n)|^2}{\widehat{\phi}_{xx}(k,n)\widehat{\phi}_{yy}(k,n)}$$

其中 $\widehat{\phi}_{xy}$ 为互 PSD 的递归估计。

**Ji & Baek 的 MSC-based SAP 估计**：

对双通道信号 $x_1, x_2$：
- 语音存在时：MSC 较高（语音相干）
- 语音缺席时：MSC 较低（噪声非相干）

阈值检测：
$$\text{SAP}(k,n) = \begin{cases} 1 & \Gamma_{x_1 x_2}(k,n) > \gamma \\ 0 & \text{otherwise} \end{cases}$$

其中阈值 $\gamma$ 由 ROC 曲线优化确定。

**Schwarz & Kellermann 的 CDR 估计**：

相干-扩散比（Coherent-to-Diffuse Ratio）：
$$\text{CDR}(k,n) = \frac{\Gamma(k,n) - \Gamma_d(k)}{\Gamma_s(k) - \Gamma(k,n)} \cdot \frac{1 - \Gamma_s(k)}{1 - \Gamma_d(k)}$$

其中 $\Gamma_s$ 为相干场 MSC（=1），$\Gamma_d$ 为扩散场 MSC（$=\text{sinc}(2\pi f d/c)$）。

### 4.3 基于倒谱平滑的噪声估计

**参考文献库**：
- Breithaupt et al., [*"A novel a priori SNR estimation approach based on selective cepstro-temporal smoothing"*](zotero://select/items/0_WUNQDUNP) — 库中标注 **⭐⭐⭐⭐, 168 citations**, 提出 CTS/TCS 方法
- Gerkmann & Hendriks, [*"Unbiased MMSE-Based Noise Power Estimation With Low Complexity and Low Tracking Delay"*](zotero://select/items/0_A84ZJUKV) — 库中标注 **⭐⭐⭐⭐, LC-MMSE, 585 citations**

**Gerkmann & Hendriks 的 LC-MMSE 方法**：

最小化对数谱幅度估计的均方误差：
$$\widehat{\lambda}_v = \arg\min_{\lambda_v} E\{(\log|S| - \log|\widehat{S}|)^2\}$$

闭式解：
$$\widehat{\lambda}_v(k,n) = \frac{|Y(k,n)|^2}{\gamma(k,n)} \cdot \frac{1}{1 + \text{SNR}_{\text{prior}}}$$

其中 $\gamma = |Y|^2/\lambda_v$ 为后验信噪比。

**Breithaupt 的 CTS/TCS 方法**：

1. 将功率谱转为倒谱域：$c[m] = \text{IDFT}\{\log|Y(k,n)|^2\}$
2. 低时倒（quefrency）分量对应谱包络（慢变），高时倒分量对应谱细节（快变）
3. 对低时倒分量进行时间平滑，保留谱包络的连续性
4. 转换回频域得到平滑的噪声估计

---

## 5. 去混响（Dereverberation）

### 5.1 基于线性预测的方法（WPE）

加权预测误差（WPE）是最经典的去混响方法，利用多通道线性预测消除晚期混响。

**信号模型**：

含混响的 STFT 系数建模为：
$$y_m(k,n) = d_m(k,n) + r_m(k,n)$$

其中 $d_m$ 为直达声（含早期反射），$r_m$ 为晚期混响。

**多通道线性预测**：
$$\widehat{d}_m(k,n) = y_m(k,n) - \sum_{l=1}^{L} \mathbf{g}_l^H(k) \mathbf{y}(k, n-l)$$

其中 $\mathbf{y}(k, n-l) = [y_1(k,n-l-\delta), \dots, y_M(k,n-l-\delta)]^T$，$\delta$ 为预测延迟（通常取 1-3 帧）。

**优化准则**：

最小化加权预测误差功率：
$$\min_{\mathbf{G}} \sum_n \frac{|\widehat{d}_m(k,n)|^2}{\lambda(k,n)}$$

其中 $\lambda(k,n)$ 为权重（通常取前一次迭代的预测误差功率）。

**迭代加权最小二乘（IRLS）解法**：

1. 初始化：$\lambda^{(0)}(k,n) = |y_m(k,n)|^2$
2. 第 $i$ 次迭代：
   $$\mathbf{g}^{(i)}(k) = \left(\sum_n \frac{\mathbf{y}(k,n-\delta)\mathbf{y}^H(k,n-\delta)}{\lambda^{(i-1)}(k,n)}\right)^{-1} \left(\sum_n \frac{\mathbf{y}(k,n-\delta)y_m^*(k,n)}{\lambda^{(i-1)}(k,n)}\right)$$
3. 更新权重：$\lambda^{(i)}(k,n) = |y_m(k,n) - \mathbf{g}^{(i)H}(k)\mathbf{y}(k,n-\delta)|^2$
4. 收敛后：$d_m(k,n) = y_m(k,n) - \mathbf{g}^H(k)\mathbf{y}(k,n-\delta)$

### 5.2 基于相干-扩散比（CDR）的方法

**参考文献库**：
- Schwarz & Kellermann (2015), [*"Coherent-to-Diffuse Power Ratio Estimation for Dereverberation"*](zotero://select/items/0_AT69JCEX) — **核心文献**，提出 CDR 估计器用于去混响
- Schwarz (2019), [*"Dereverberation and robust speech recognition using spatial coherence models"*](zotero://select/items/0_BD6AVHPW) — 博士论文，系统性论述

利用语音的相干性与噪声/混响的扩散性之间的差异进行抑制。

**相干-扩散功率比（CDR）估计**：

$$\text{CDR}(k) = \frac{\Gamma_{\text{meas}}(k) - \Gamma_{\text{diff}}(k)}{\Gamma_{\text{coh}}(k) - \Gamma_{\text{meas}}(k)}$$

其中 $\Gamma_{\text{meas}}$ 为测量 MSC，$\Gamma_{\text{diff}}$ 为扩散场模型 MSC，$\Gamma_{\text{coh}} = 1$ 为相干场 MSC。

**CDR 加权去混响**：
$$H_{\text{CDR}}(k,n) = \frac{\text{CDR}(k,n)}{1 + \text{CDR}(k,n)}$$

### 5.3 维纳增益设计

**参考文献库**：
- Xiang & Chen (2024, preprint), [*"Design of the wiener gain in noisy and reverberant environments"*](zotero://select/items/0_3BGQBT2D) — 最新

### 5.4 经典综述

**参考文献库**：
- (2016), [*"Fifty Years of Reverberation Reduction"*](zotero://select/items/0_KJC97JIR) — 库中有此 presentation，50 年综述

---

## 6. DOA 估计与声源定位

### 6.1 GCC-PHAT

**参考文献库**：
- Grondain & Glass (2018), [*"A Study of the Complexity and Accuracy of Direction of Arrival Estimation Methods Based on GCC-PHAT for a Pair of Close Microphones"*](zotero://select/items/0_KPFCXSPR) — 库中标注 **⭐⭐⭐⭐, 23 citations**
- Grondain & Maheux (2023, preprint), [*"Fast Cross-Correlation for TDoA Estimation on Small Aperture Microphone Arrays"*](zotero://select/items/0_YZ35BT9X) — 最新
- Bechler & Kroschel, [*"CONSIDERING THE SECOND PEAK IN THE GCC FUNCTION FOR MULTI-SOURCE TDOA ESTIMATION"*](zotero://select/items/0_BPTCUEYE) — 库中标注，多声源 TDOA

**广义互相关（GCC）**：

两通道信号 $x_1[n], x_2[n]$ 的广义互相关：
$$R_{12}(\tau) = \int_{-\infty}^{\infty} \Psi(f) G_{12}(f) e^{j2\pi f \tau} df$$

其中 $G_{12}(f) = X_1(f)X_2^*(f)$ 为互功率谱，$\Psi(f)$ 为加权函数。

**PHAT 加权**：
$$\Psi_{\text{PHAT}}(f) = \frac{1}{|G_{12}(f)|}$$

PHAT 加权归一化幅度，仅保留相位信息，在混响环境下更鲁棒。

**TDoA 估计**：
$$\widehat{\tau}_{12} = \arg\max_{\tau} R_{12}^{\text{PHAT}}(\tau)$$

**DOA 转换**（线性阵列）：
$$\theta = \arccos\left(\frac{c \cdot \widehat{\tau}_{12}}{d}\right)$$

**Grondain & Maheux (2023) 快速 GCC**：

利用麦克风阵列的几何结构，仅在可能的 TDoA 范围内搜索，减少 70%+ 计算量。

### 6.2 MUSIC / 子空间方法

**参考文献库**：
- Manamperi et al. (2022), [*"Drone Audition: Sound Source Localization Using On-Board Microphones"*](zotero://select/items/0_A6PIMN7W) — 使用 MUSIC 进行 DOA 估计

**MUSIC 算法**：

1. 计算协方差矩阵：$\mathbf{R} = E\{\mathbf{y}\mathbf{y}^H\}$
2. 特征值分解：$\mathbf{R} = \mathbf{E}_s \mathbf{\Lambda}_s \mathbf{E}_s^H + \mathbf{E}_n \mathbf{\Lambda}_n \mathbf{E}_n^H$
3. 空间谱：
   $$P_{\text{MUSIC}}(\theta) = \frac{1}{\mathbf{d}^H(\theta)\mathbf{E}_n\mathbf{E}_n^H\mathbf{d}(\theta)}$$
4. DOA 估计：$\widehat{\theta} = \arg\max_\theta P_{\text{MUSIC}}(\theta)$

### 6.3 最新进展

**参考文献库**：
- Duan & Pan (2026), [*"An approach to direction-of-arrival estimation for airborne microphone arrays"*](zotero://select/items/0_LH8CSALP) — 最新
- Grinstein et al. (2023, preprint), [*"Dual input neural networks for positional sound source localization"*](zotero://select/items/0_L8BUXRMB) — 神经网络定位

---

## 7. 盲源分离（BSS）/ 独立向量分析（IVA）

**参考文献库**：
- Ono (2011), [*"Stable and fast update rules for independent vector analysis based on auxiliary function technique"*](zotero://select/items/0_4354E22N) — **AuxIVA**, 经典算法
- Nakashima & Ono (2026), [*"Online independent low-rank matrix analysis as a lightweight and trainable model for real-time multichannel music source separation"*](zotero://select/items/0_ZRYGE8QR) — 最新进展
- Guo & Luo (2023), [*"A Survey of Optimization Methods for Independent Vector Analysis in Audio Source Separation"*](zotero://select/items/0_DA3F64K6) — 综述

**IVA 问题设置**：

$M$ 个观测信号，$N$ 个源信号：
$$\mathbf{y}(k,n) = \sum_{l=1}^{N} \mathbf{a}_l(k) s_l(k,n)$$

目标：估计解混矩阵 $\mathbf{W}(k)$ 使得 $\mathbf{z}(k,n) = \mathbf{W}^H(k)\mathbf{y}(k,n)$ 的各分量独立。

**AuxIVA 算法**（Ono, 2011）：

辅助函数方法。构造辅助函数 $Q(\mathbf{W}, \mathbf{V})$ 使得：
$$\mathcal{L}(\mathbf{W}) \leq Q(\mathbf{W}, \mathbf{V})$$

对每个频率 bin $k$ 和源 $l$，迭代更新：

1. 计算辅助变量：
   $$v_l(n) = \sqrt{\sum_k \frac{|z_l(k,n)|^2}{\sigma_l^2(k)}}$$

2. 更新解混矩阵列：
   $$\mathbf{w}_l(k) \leftarrow \left(\frac{1}{N}\sum_n \frac{v_l(n)}{|z_l(k,n)|} \mathbf{y}(k,n)\mathbf{y}^H(k,n)\right)^{-1} \mathbf{e}_l$$

3. 归一化：$\mathbf{w}_l(k) \leftarrow \mathbf{w}_l(k) / \sqrt{\mathbf{w}_l^H(k) \mathbf{R}(k) \mathbf{w}_l(k)}$

AuxIVA 的优势：无需步长选择，保证单调收敛，计算效率高。

**排列模糊（Permutation Problem）**：

频域 BSS 的固有模糊性：每个频率 bin 的解混矩阵 $\mathbf{W}(k)$ 是独立估计的，因此分离出的源顺序在不同 $k$ 之间可能不同：
$$z_l(k,n) = \mathbf{w}_l^H(k)\mathbf{y}(k,n)$$

在 bin $k$ 中 $z_1$ 可能对应说话人 A，而在 bin $k+1$ 中 $z_1$ 可能对应说话人 B。直接 IFFT 会导致灾难性后果。

### 排列对齐方法详解

#### 方法 1：基于 DOA 的对齐

**原理**：同一声源在不同频率 bin 的 DOA 应该一致。

**步骤**：
1. 对每个频率 bin $k$ 和每个分离源 $l$，估计其等效 DOA：
   $$\widehat{\theta}_l(k) = \arg\max_\theta \frac{|\mathbf{w}_l^H(k)\mathbf{d}(\theta)|^2}{\|\mathbf{w}_l(k)\|^2 \|\mathbf{d}(\theta)\|^2}$$

2. 将 bin $k$ 的排列与 bin $k-1$ 对齐：
   $$\pi_k = \arg\min_{\pi} \sum_l |\widehat{\theta}_l(k) - \widehat{\theta}_{\pi(l)}(k-1)|$$

**优点**：物理意义明确，对语音信号效果好。
**缺点**：需要阵列几何信息，在混响环境下 DOA 估计不准确。

#### 方法 2：基于包络相关的对齐

**原理**：同一源在不同频率 bin 的时频包络（功率随时间的变化）高度相关。

**步骤**：
1. 计算每个 bin $k$ 和源 $l$ 的功率包络：
   $$P_l(k,n) = |z_l(k,n)|^2$$

2. 对相邻 bin $k$ 和 $k-1$，计算所有排列下包络的相关系数：
   $$\rho_{l,m} = \frac{\sum_n (P_l(k,n) - \bar{P}_l(k))(P_m(k-1,n) - \bar{P}_m(k-1))}{\sqrt{\sum_n (P_l(k,n) - \bar{P}_l(k))^2 \sum_n (P_m(k-1,n) - \bar{P}_m(k-1))^2}}$$

3. 选择最优排列：
   $$\pi_k = \arg\max_\pi \sum_l \rho_{l, \pi(l)}$$

**优点**：不需要阵列几何，适用于任意信号。
**缺点**：在低 SNR 或短时信号下包络估计不可靠；对 $P_l(k,n)$ 的平滑敏感。

**改进：分组包络相关（Sawada et al.）**：

将频率 bin 分组（如 5-10 个 bin 一组），组内用同一排列。组间再用包络相关对齐。这减少了逐 bin 对齐的误差累积。

#### 方法 3：IVA 内在解决（Ono, 2011）

IVA 的核心创新：通过在似然函数中建模**频率间依赖关系**，自动解决排列模糊。

**标准 IVA 目标函数**：
$$\min_{\mathbf{W}} \sum_l E\left[\log p_l(\mathbf{z}_l)\right] - \sum_k \log |\det \mathbf{W}(k)|$$

其中 $\mathbf{z}_l = [z_l(1,n), z_l(2,n), \dots, z_l(K,n)]^T$ 为源 $l$ 在**所有频率 bin** 的向量。

关键区别：$p_l(\mathbf{z}_l)$ 建模了**所有频率 bin 的联合分布**，而不是独立处理每个 bin。这使得不同 bin 的分离结果自然对齐。

**AuxIVA 的具体实现**：

假设源服从球对称复拉普拉斯分布：
$$p_l(\mathbf{z}_l) \propto \exp\left(-\sqrt{\sum_k \frac{|z_l(k,n)|^2}{\sigma_l^2(k)}}\right)$$

辅助变量 $v_l(n)$ 本质上是源 $l$ 在所有频率 bin 的**联合功率**：
$$v_l(n) = \sqrt{\sum_k \frac{|z_l(k,n)|^2}{\sigma_l^2(k)}}$$

由于 $v_l(n)$ 跨频率求和，不同 bin 的更新方向被耦合在一起——这隐式地保证了一致的排列。

**IVA vs 传统 IFDMA（Independent Freq-Domain ICA）**：

| 特性 | IFDMA + 后验对齐 | IVA |
|------|-----------------|-----|
| 排列对齐 | 需要额外后处理步骤 | 内置于目标函数 |
| 误差累积 | 逐 bin 对齐可能累积误差 | 全局优化，无累积 |
| 计算量 | 低（逐 bin ICA）+ 对齐开销 | 中等（联合优化） |
| 收敛性 | 不保证全局最优 | 辅助函数保证单调收敛 |
| 排列一致性 | 可能失败（低 SNR/混响） | 鲁棒性更强 |

#### 方法 4：基于相干性的对齐

**原理**：利用分离信号之间的相干性判断排列一致性。

**互功率谱相干性**：
$$\gamma_{lm}(k, k') = \frac{|E\{z_l(k,n)z_m^*(k',n)\}|^2}{E\{|z_l(k,n)|^2\}E\{|z_m(k',n)|^2\}}$$

对于同一源（$l=m$），不同频率 bin 间的相干性应较高（尤其是相邻 bin）。对于不同源（$l \neq m$），相干性应接近零。

**算法**：
1. 初始化 bin 0 的排列为恒等映射
2. 对 bin $k$，计算所有 $M!$ 种排列下的总体相干性：
   $$C(\pi) = \sum_l \gamma_{l, \pi(l)}(k, k-1)$$
3. 选择最大化相干性的排列

#### 方法 5：基于深度学习的方法

近年来，端到端时域分离模型（如 Conv-TasNet, SepFormer, DPRNN）天然避免了排列问题——它们直接在时域操作，没有频域独立估计的问题。

但对于频域模型，也出现了神经网络辅助排列对齐的方法：

1. **排列不变训练（PIT, Permutation Invariant Training）**：
   $$\mathcal{L}_{\text{PIT}} = \min_{\pi} \sum_l \|\mathbf{s}_l - \widehat{\mathbf{s}}_{\pi(l)}\|^2$$

   训练时自动选择最优排列，推理时网络学会一致的输出顺序。

2. **注意力机制对齐**：在频域 BSS 的输出后接一个注意力层，自动学习跨频率 bin 的源对应关系。

---

## 8. 双麦克风语音增强

**参考文献库**：
- Jeub et al. (2009), [*"Noise reduction for dual-microphone mobile phones exploiting power level differences"*](zotero://select/items/0_LJWC8IL9) — 库中标注 **⭐⭐⭐⭐⭐, 111 citations**, 利用功率级差 (PLD)
- Fu et al. (2013), [*"Dual-microphone noise reduction for mobile phone application"*](zotero://select/items/0_4L8BUAA9) — 库中标注 **To Read**，MVDR 滤波 + PLD
- Aarabi (2004), [*"Phase-based dual-microphone robust speech enhancement"*](zotero://select/items/0_D8ASTBEC) — 库中标注 **⭐⭐⭐**, PEF (phase-error filter), 163 citations
- Hu & Wang (2011), [*"Robustness analysis of time-domain and frequency-domain adaptive null-forming schemes"*](zotero://select/items/0_MCQ9CBH5) — 库中标注 **⭐⭐⭐⭐**, 零陷形成

### 8.1 功率级差法（PLD）

**Jeub et al. (2009) PLD 方法**：

两个麦克风，一个靠近嘴巴（近端），一个远离（远端）。在噪声场中，近端麦克风的语音功率高于远端。

**功率级差特征**：
$$\Delta P(k,n) = 10\log_{10}\frac{\widehat{\phi}_{x_1 x_1}(k,n)}{\widehat{\phi}_{x_2 x_2}(k,n)}$$

其中 $x_1$ 为近端麦克风，$x_2$ 为远端麦克风。

**语音存在检测**：
$$\text{SPP}(k,n) = \begin{cases} 1 & \Delta P(k,n) > \gamma_{\text{PLD}} \\ 0 & \text{otherwise} \end{cases}$$

PLD 方法的优势：不需要 DOA 估计，计算简单，适合手机等嵌入式设备。

### 8.2 相位误差滤波器（PEF）

**Aarabi (2004) PEF 方法**：

利用两通道信号的相位差来区分语音和噪声。

**相位差**：
$$\Delta\phi(k,n) = \angle X_1(k,n) - \angle X_2(k,n)$$

对于目标方向 $\theta_0$ 的声源，理论相位差为：
$$\Delta\phi_{\text{target}}(k) = -2\pi f \frac{d\cos\theta_0}{c}$$

**相位误差**：
$$e_\phi(k,n) = |\Delta\phi(k,n) - \Delta\phi_{\text{target}}(k)|$$

**PEF 增益函数**：
$$H_{\text{PEF}}(k,n) = \begin{cases} 1 & e_\phi(k,n) < \epsilon \\ 0 & \text{otherwise} \end{cases}$$

或平滑版本：
$$H_{\text{PEF}}(k,n) = \frac{1}{1 + \beta e_\phi^2(k,n)}$$

### 8.3 自适应零陷形成

**Hu & Wang (2011) 时域/频域自适应零陷**：

目标：在干扰方向形成零陷（null），同时保持目标方向无畸变。

**频域自适应零陷**：
$$\mathbf{w}(k,n+1) = \mathbf{w}(k,n) - \mu \mathbf{x}(k,n) y^*(k,n)$$

其中 $\mathbf{x}(k,n)$ 为输入向量，$y(k,n) = \mathbf{w}^H(k,n)\mathbf{x}(k,n)$ 为输出。

零陷方向由约束矩阵 $\mathbf{C}$ 指定：
$$\min_{\mathbf{w}} \mathbf{w}^H \mathbf{R} \mathbf{w} \quad \text{s.t.} \quad \mathbf{C}^H \mathbf{w} = \mathbf{f}$$

---

## 9. 深度学习语音增强

### 9.1 Tan & Wang (2018) CRNN

**参考文献库**：
- Tan & Wang (2018), [*"A Convolutional Recurrent Neural Network for Real-Time Speech Enhancement"*](zotero://select/items/0_F8A8SVLS) — 库中标注 **CRN, ⭐⭐⭐⭐⭐, 321 citations**, Interspeech 2018

**核心思想**：将卷积的局部特征提取能力与 LSTM 的长时建模能力结合，直接在时域估计复数 mask（cIRM），同时建模幅度和相位。

**网络架构**：

```
输入: [B, 2, T]                    # B=batch, 2=(实部,虚部), T=时间样本
  │
  ▼
┌─────────────────────────────────┐
│        Encoder (Conv1D)          │
│  Conv1d(2→16, k=64, s=16)       │
│  + BatchNorm + PReLU             │
│  ↓                              │
│  [B, 16, T/16]                  │
│  Conv1d(16→32, k=32, s=8)       │
│  + BatchNorm + PReLU             │
│  ↓                              │
│  [B, 32, T/128]                 │
└─────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────┐
│     Bottleneck (LSTM × 2)       │
│  LSTM(32→256, bidirectional)    │
│  ↓                              │
│  [B, T/128, 512]               │
│  Linear(512→256) + ReLU        │
│  ↓                              │
│  [B, T/128, 256]               │
└─────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────┐
│      Decoder (TransConv1D)       │
│  TransConv1d(256→16, k=32, s=8) │
│  + BatchNorm + ReLU              │
│  ↓                              │
│  [B, 16, T/16]                  │
│  TransConv1d(16→2, k=64, s=16)  │
│  ↓                              │
│  [B, 2, T]                      │
└─────────────────────────────────┘
  │
  ▼
输出: [B, 2, T]                    # 复数 mask (实部, 虚部)
  │
  ▼
增强输出: Y ⊙ M                    # 输入 STFT × 复数 mask
```

**参数量分解**：

| 层 | 参数量 | 占比 |
|----|--------|------|
| Conv1d (2→16, k=64) | 2,064 | 0.2% |
| Conv1d (16→32, k=32) | 16,416 | 1.5% |
| BiLSTM (32→256) | 295,936 | 26.9% |
| BiLSTM (256→256) | 525,312 | 47.8% |
| Linear (512→256) | 131,328 | 11.9% |
| TransConv1d (256→16, k=32) | 131,088 | 11.9% |
| TransConv1d (16→2, k=64) | 2,064 | 0.2% |
| BatchNorm + bias | 1,732 | 0.2% |
| **总计** | **~1.1M** | 100% |

**计算量（MACs per inference）**：

| 层 | MACs | 占比 |
|----|------|------|
| Conv1d (2→16) | 2,097,152 | 12.4% |
| Conv1d (16→32) | 1,048,576 | 6.2% |
| BiLSTM × 2 | 10,485,760 | 62.0% |
| Linear | 131,072 | 0.8% |
| TransConv1d (256→16) | 2,097,152 | 12.4% |
| TransConv1d (16→2) | 1,048,576 | 6.2% |
| **总计** | **~17M** | 100% |

**训练细节**：
- 采样率：16 kHz
- STFT：FFT size 512, hop 256
- Loss：复数 mask 的 L2 损失 + 时域波形 L1 损失
- 数据集：VoiceBank+DEMAND（11,572 训练 / 824 测试 utterances）
- 优化器：Adam, lr = 0.001, batch = 128

### 9.2 FRCRN (Zhao & Ma, 2024)

**参考文献库**：
- Zhao & Ma (2024), [*"FRCRN: boosting feature representation using frequency recurrence for monaural speech enhancement"*](zotero://select/items/0_JBLW4HGZ)

**核心思想**：在 CRNN 瓶颈层引入频率递归（Frequency Recurrence），沿频率维度传播 LSTM 状态，捕获相邻频带间的谐波结构相关性。

**网络架构**：

```
输入: [B, 1, F, T]                  # 单通道 STFT 幅度谱
  │
  ▼
┌──────────────────────────────────┐
│         Encoder (Conv2D)          │
│  Conv2d(1→64, k=(7,1), s=(2,1))  │  # 频率下采样
│  + PReLU                         │
│  ↓ [B, 64, F/2, T]              │
│  Conv2d(64→128, k=(1,3), s=(1,2))│  # 时间下采样
│  + PReLU                         │
│  ↓ [B, 128, F/2, T/2]           │
│  Conv2d(128→256, k=(1,3), s=(1,2))│
│  ↓ [B, 256, F/2, T/4]           │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│  Frequency-Recurrence LSTM        │
│                                  │
│  for f in range(F/2):            │
│    h[f] = LSTM(x[f], h[f-1])     │  # 频率维度递归
│    h[f] = LSTM_time(h[f], prev_h[f]) │  # 时间维度递归
│                                  │
│  ↓ [B, F/2, T/4, 256]           │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│     Decoder (TransConv2D)         │
│  TransConv2d(256→128, s=(1,2))   │
│  TransConv2d(128→64, s=(1,2))    │
│  TransConv2d(64→1, k=(7,1), s=(2,1))│
│  ↓ [B, 1, F, T]                 │
└──────────────────────────────────┘
  │
  ▼
输出: 复数 mask [B, 2, F, T]
```

**参数量**：
- Encoder Conv2D: ~1.2M
- Freq-Rec LSTM: ~2.1M（频率 LSTM 0.8M + 时间 LSTM 1.3M）
- Decoder TransConv2D: ~1.5M
- **总计：~4.8M**

**计算量**：
- Conv2D 编码: ~8.5G MACs
- Freq-Rec LSTM: ~12.3G MACs（频率递归显著增加计算）
- TransConv2D 解码: ~7.2G MACs
- **总计：~28G MACs**

**关键改进 vs CRNN**：
| 特性 | CRNN | FRCRN |
|------|------|-------|
| 输入 | 时域 | 频域（STFT 幅度+相位） |
| 递归维度 | 仅时间 | 频率 + 时间（双向） |
| 参数量 | 1.1M | 4.8M |
| 计算量 | 17M MACs | 28G MACs |
| 谐波建模 | 无 | 频率递归捕获 |
| DNS Challenge PESQ | 2.05 | 2.42 |

### 9.3 Strake et al. (2020) ConvLSTM CRNN

**参考文献库**：
- Strake et al. (2020), [*"Fully Convolutional Recurrent Networks for Speech Enhancement"*](zotero://select/items/0_W36RRSVW) — ICASSP 2020, 63 citations

**核心思想**：用 ConvLSTM 替代标准 LSTM，在保留空间结构的同时建模时空依赖。

**网络架构**：

```
输入: [B, 2, F, T]                  # 复数 STFT（实部+虚部）
  │
  ▼
┌──────────────────────────────────┐
│     Encoder (Conv2D × 4)          │
│  Conv(2→32, k=3, s=1) + PReLU   │
│  Conv(32→64, k=2, s=2) + PReLU  │  # 下采样
│  Conv(64→128, k=2, s=2) + PReLU │
│  Conv(128→256, k=2, s=2) + PReLU│
│  ↓ [B, 256, F/8, T/8]           │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│      ConvLSTM × 2                 │
│  ConvLSTM(256→256, k=3)         │  # 保持空间维度
│  ConvLSTM(256→256, k=3)         │
│  ↓ [B, 256, F/8, T/8]           │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│     Decoder (TransConv2D × 4)     │
│  TransConv(256→128, k=2, s=2)   │
│  TransConv(128→64, k=2, s=2)    │
│  TransConv(64→32, k=2, s=2)     │
│  TransConv(32→2, k=3, s=1)      │
│  ↓ [B, 2, F, T]                 │
└──────────────────────────────────┘
  │
  ▼
输出: 复数 mask [B, 2, F, T]
```

**参数量**：
- Conv2D 编码: ~1.8M
- ConvLSTM × 2: ~2.4M
- TransConv2D 解码: ~1.6M
- **总计：~5.8M**

**计算量**：~35G MACs

ConvLSTM vs 标准 LSTM 的比较：
| 特性 | 标准 LSTM | ConvLSTM |
|------|-----------|----------|
| 空间信息保持 | 需展平为一维 | 保留 2D 结构 |
| 感受野 | 仅时间维度 | 频率 + 时间 |
| 参数量 | 较少 | 较多（k×k 卷积核） |
| 特征图对齐 | 需要额外处理 | Skip connection 天然对齐 |

### 9.4 Wu et al. (2025) Ultra-Low Latency SE

**参考文献库**：
- Wu et al. (2025), [*"Ultra-Low Latency Speech Enhancement - A Comprehensive Study"*](zotero://select/items/0_3E2SZB7V)

**核心贡献**：系统性研究了 8 种 SE 架构的延迟-性能权衡，涵盖纯时域、频域、混合方法。

**对比的架构**：

| 模型 | 算法延迟 | 计算延迟 | 总延迟 | PESQ (DNS) | 参数量 |
|------|---------|---------|--------|-----------|--------|
| Full-band LSTM | 0 ms | 32 ms | 32 ms | 2.31 | 4.3M |
| Full-band GRU | 0 ms | 16 ms | 16 ms | 2.28 | 3.1M |
| Subband LSTM | 2 ms | 4 ms | 6 ms | 2.15 | 1.8M |
| Subband GRU | 2 ms | 2 ms | 4 ms | 2.12 | 1.2M |
| Conv-TasNet | 1 ms | 8 ms | 9 ms | 2.25 | 5.2M |
| DPRNN | 8 ms | 4 ms | 12 ms | 2.35 | 3.7M |
| TF-GridNet | 8 ms | 16 ms | 24 ms | 2.52 | 13.2M |
| **DCCRN** | 8 ms | 8 ms | 16 ms | 2.38 | 3.7M |

**Subband GRU 架构**（最低延迟）：

```
输入: [B, N_sub, T_frame]            # N_sub=256 子带, frame=2ms
  │
  ▼
┌──────────────────────────────────┐
│    Subband Encoder (Linear)        │
│  Linear(N_sub → 64)              │
│  ↓ [B, 64]                       │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│         GRU × 2                   │
│  GRU(64 → 128)                   │
│  GRU(128 → 128)                  │
│  ↓ [B, 128]                     │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│    Subband Decoder (Linear)        │
│  Linear(128 → N_sub)             │
│  ↓ [B, N_sub]                   │
└──────────────────────────────────┘
  │
  ▼
输出: Gain [B, N_sub]              # 每子带增益
```

**关键发现**：
1. 算法延迟 > 8ms 后性能提升趋于饱和
2. GRU 比 LSTM 在低延迟场景更优（参数量少 1/3，性能相近）
3. 子带方法比全带方法延迟更低但性能略有下降
4. 计算延迟占总延迟的比例随硬件加速显著变化

### 9.5 多通道/多麦克风深度增强

**参考文献库**：
- Xu et al. (2026, preprint), [*"ArrayDPS-refine: generative refinement of discriminative multi-channel speech enhancement"*](zotero://select/items/0_QV4SXU3P) — 最新，生成式精细化
- Wang & Li (2026, preprint), [*"Global rotation equivariant phase modeling for speech enhancement with deep magnitude-phase interaction"*](zotero://select/items/0_RMXTPH2T) — 最新，旋转等变 + 幅度-相位联合建模

**Wang & Li (2026) 旋转等变相位建模**：

核心思想：麦克风阵列旋转时，声场相位应该等变变换。设计旋转等变网络：
$$f(R_\theta \mathbf{x}) = R_\theta f(\mathbf{x})$$

其中 $R_\theta$ 为旋转操作。这保证了模型对不同阵列朝向的泛化能力。

**网络架构**：

```
输入: [B, M, F, T]                   # M 通道多麦克风 STFT
  │
  ▼
┌──────────────────────────────────┐
│   SO(2) 等变卷积 (Circular Conv)   │
│  沿麦克风维度做循环卷积            │
│  保证旋转等变性                    │
│  ↓ [B, C, F, T]                 │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│  幅度-相位交互模块 (MPI)            │
│  Mag Branch: Conv2D + SE         │
│  Phase Branch: Conv2D + SE       │
│  Cross-Attention(Mag↔Phase)      │  # 双向交互
│  ↓ [B, 2, F, T]                 │
└──────────────────────────────────┘
  │
  ▼
输出: 复数 mask [B, 2, F, T]

参数量: ~6.2M
计算量: ~42G MACs
```

### 9.6 神经波束形成

**参考文献库**：
- Chen et al. (2026, preprint), [*"Neural network-based time-frequency-bin-wise linear combination of beamformers for underdetermined target source extraction"*](zotero://select/items/0_R4362BJ2) — 最新
- (专利), [*"Method for neural beamforming, channel shortening and noise reduction"*](zotero://select/items/0_T9NYJKQT) — 神经波束形成 + 信道缩短

**Chen et al. (2026) Neural BF 组合方法**：

在 TF 单元 $(k,n)$ 级别，网络输出多个预计算波束形成器的加权组合：
$$\mathbf{w}(k,n) = \sum_{r=1}^{R} \alpha_r(k,n) \mathbf{w}_r(k)$$

其中 $\mathbf{w}_r$ 为预计算的波束形成器（如 MVDR、DS、null-former 等），$\alpha_r(k,n)$ 由网络预测，满足 $\sum_r \alpha_r = 1$。

**网络架构**：

```
输入: IPD + ILD + 对数功率谱 [B, C_in, F, T]
  │
  ▼
┌──────────────────────────────────┐
│    Feature Extractor               │
│  Conv2d(C_in→64, k=3) + BN+ReLU │
│  Conv2d(64→64, k=3) + BN+ReLU   │
│  ↓ [B, 64, F, T]                │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│    Mask Estimation (U-Net)         │
│  Encoder: Conv2d × 4             │
│  Bottleneck: Conv2d × 2          │
│  Decoder: TransConv2d × 4        │
│  Skip connections                │
│  ↓ [B, 64, F, T]                │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│    Weight Prediction               │
│  Linear(64 → R)                  │  # R 个波束形成器权重
│  Softmax                          │  # 保证 Σα = 1
│  ↓ [B, R, F, T]                 │
└──────────────────────────────────┘
  │
  ▼
输出: α_1...α_R → w(k,n) = Σ α_r w_r(k)

参数量: ~1.5M
计算量: ~3G MACs（不含预计算 BF）
预计算 BF: R × M 通道（可离线）
```

### 9.7 波束形成特征 + DNN 分离

**参考文献库**：
- (2020), [*"Beamformed Feature for Learning-based Dual-channel Speech Separation"*](zotero://select/items/0_UB9Q24MJ) — 利用固定波束形成特征进行 DNN 分离

**方法**：先用固定波束形成器（如 MVDR）对多通道信号做初步增强，然后将波束形成输出 + 残余噪声估计作为 DNN 输入。

```
多通道输入 [M, F, T]
  │
  ▼
┌──────────────────┐     ┌──────────────────┐
│  MVDR Beamformer  │     │  Noise Estimator  │
│  ↓ [1, F, T]     │     │  ↓ [1, F, T]     │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
         ▼                        ▼
┌──────────────────────────────────────┐
│    Concat: [BF_output, Noise_est]    │
│    ↓ [2, F, T]                      │
└────────────────┬─────────────────────┘
                 ▼
┌──────────────────────────────────────┐
│    Separation DNN (Conv-TasNet)       │
│    Encoder → DPRNN → Decoder         │
│    ↓ [2, T] (2 个说话人)              │
└──────────────────────────────────────┘
```

### 9.8 骨导 + 气导融合

**参考文献库**：
- Kuang & Yang (2024), [*"A lightweight speech enhancement network fusing bone- and air-conducted speech"*](zotero://select/items/0_VBVTU72Z)

**核心思想**：骨导信号（bone-conducted）包含低频语音信息且不受空气噪声影响，与气导信号融合可显著提升低 SNR 场景下的增强效果。

**网络架构**：

```
骨导信号 [B, 1, T] ─┐                      ┌→ [B, 1, T] 增强语音
                     │                      │
气导信号 [B, 1, T] ──┼→ Dual-Stream Encoder  │
                     │   Conv1D × 2         │
                     │   ↓                  │
                     │   [B, 64, T/4] 每流   │
                     │                      │
                     └→ Cross-Attention     │
                        (骨导→气导 query)    │
                        (气导→骨导 query)    │
                        ↓                   │
                        [B, 64, T/4] 融合    │
                           │                │
                        ┌─┴────────────────┤
                        │   Conv1D Decoder  │
                        │   ↓               │
                        └→ [B, 1, T] ──────┘

参数量: ~0.8M
计算量: ~4G MACs
```

### 9.9 轻量级网络

**参考文献库**：
- Dang et al. (2023), [*"THLNet: two-stage heterogeneous lightweight network for monaural speech enhancement"*](zotero://select/items/0_IITHWLSN)
- Zhao et al. (2026), [*"A low parameter channel grouped iterative convolutional recurrent network for speech enhancement of noise-reducing headphones"*](zotero://select/items/0_37GCAS6P) — 最新

**THLNet（Dang et al., 2023）**：

两阶段异构轻量网络：
- Stage 1（粗增强）：MobileNet-style depthwise separable conv，~0.3M 参数
- Stage 2（精细化）：轻量 LSTM，~0.2M 参数
- **总计：~0.5M 参数，~2G MACs**

**Zhao et al. (2026) 通道分组迭代 CRN**：

将 CRN 的通道分组，组内迭代处理：

```
输入: [B, 1, F, T]
  │
  ▼
┌──────────────────────────────────┐
│    Channel-Grouped Conv × G       │
│  Split channels into G groups    │
│  Each group: Conv2d + BN + ReLU  │
│  ↓ [B, C, F/2, T/2]             │
└──────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────┐
│    Iterative LSTM × K steps       │
│  Each step: process 1/G channels  │
│  Hidden state shared across      │
│  iterations                      │
│  ↓ [B, C, F/2, T/2]             │
└──────────────────────────────────┘
  │
  ▼
输出: 增益 mask [B, 1, F, T]

参数量: ~0.35M (G=4, K=4)
计算量: ~1.8G MACs
```

### 9.10 深度噪声抑制竞赛（DNS Challenge）

**参考文献库**：
- Reddy et al. (2021), [*"ICASSP 2021 Deep Noise Suppression Challenge"*](zotero://select/items/0_P2ID54CH) — DNS Challenge，194 citations

DNS Challenge 定义了 SE 领域的标准 benchmark。2021 年 Track 1（实时，<40ms 延迟）的 top 方案：

| 排名 | 方案 | 架构 | 参数量 | PESQ (NoReverb) |
|------|------|------|--------|-----------------|
| 1 | NXP (Team) | Subband GRU + 后滤波 | 2.1M | 2.61 |
| 2 | Tsinghua | Full-band DCCRN | 3.7M | 2.55 |
| 3 | ByteDance | Conv-TasNet variant | 5.2M | 2.52 |
| Baseline | Microsoft | Full-band LSTM | 4.3M | 2.05 |

**DNS Challenge 评估指标**：
- **PESQ**：Perceptual Evaluation of Speech Quality（主观质量相关）
- **STOI**：Short-Time Objective Intelligibility（可懂度）
- **SI-SDR**：Scale-Invariant Signal-to-Distortion Ratio

### 9.11 综述

**参考文献库**：
- Mehrash et al. (2023), *"A review of deep learning techniques for speech processing"* — 综述

---

## 10. 语音存在概率（SPP）与先验 SNR 估计

**参考文献库**：
- Ji & Baek — MSC-based SAP [↗](zotero://select/items/0_W32YYPPA)
- Breithaupt et al. — CTS/TCS [↗](zotero://select/items/0_WUNQDUNP)
- Gerkmann & Hendriks — LC-MMSE [↗](zotero://select/items/0_A84ZJUKV)
- Esch & Vary, [*"EFFICIENT MUSICAL NOISE SUPPRESSION FOR SPEECH ENHANCEMENT SYSTEMS"*](zotero://select/items/0_R2EM3VTN) — 库中标注 **⭐⭐⭐, 115 citations**

---

## 11. 麦克风阵列处理系统

### 11.1 Habets 系列讲义

**参考文献库**：
- Habets (2013), *"Linear and Parametric Microphone Array Processing"* — **Part I ~ Part VI**，系列教程
  - [Part I: Introduction](zotero://select/items/0_8WIBFX7T)
  - [Part II: Linear Spatial Processing](zotero://select/items/0_MUUQW5WG)
  - [Part III: Distributed Linear Spatial Processing](zotero://select/items/0_DRUM822U)
  - [Part IV: Parametric Spatial Processing](zotero://select/items/0_5NJG2FTY)
  - [Part V: Joint Linear and Parametric Spatial Processing](zotero://select/items/0_QBKEEME6)
  - [Part VI: Wrap-up](zotero://select/items/0_T3MCRW79)

### 11.2 ODAS 系统

**参考文献库**：
- Grondain et al. (2022), [*"ODAS: Open embeddeD Audition System"*](zotero://select/items/0_JASLZ3LH) — 开源嵌入式听觉系统

### 11.3 HARK 机器人听觉

**参考文献库**：
- Nakajima et al., [*"Blind Source Separation With Parameter-Free Adaptive Step-Size Method for Robot Audition"*](zotero://select/items/0_47JU845I) — GHDSS 算法
- Valin et al., [*"Enhanced Robot Audition Based on Microphone Array Source Separation with Post-Filter"*](zotero://select/items/0_QY54E8BJ) — GSS + post-filter

---

## 12. 关键书籍

**参考文献库**：
- Tashev (2009), [*"Sound Capture and Processing: Practical Approaches"*](zotero://select/items/0_E4VRQ55V)
- Schrammen & Jax (2022), [*"Front-end signal processing for far-field speech communication"*](zotero://select/items/0_WQTPRE5L) — 专门针对远场语音通信的前端信号处理
- Messner (2013), [*"Differential Microphone Arrays"*](zotero://select/items/0_AFKQP2A2) — 博士论文/书
- Elliott (2000), *"Signal Processing for Active Control"* — ANC Collection
- Hansen & Snyder (2020), *"Active Control of Noise and Vibration"* — ANC Collection

---

## 13. 算法对比总结

| 方法类别 | 代表算法 | 优点 | 缺点 | 复杂度 |
|---------|---------|------|------|--------|
| **固定波束形成** | DS, Differential | 简单、鲁棒 | 增益有限 | $O(M)$ |
| **自适应波束形成** | MVDR, GSC | 高增益 | 需准确 RTF/噪声 PSD | $O(M^2)$ |
| **多通道维纳滤波** | MCWF, SDW-MWF, PMWF | MMSE 最优 | 需 $\Phi_{ss}, \Phi_{vv}$ | $O(M^3)$ |
| **盲源分离** | AuxIVA, ILRMA | 无需阵列几何 | 排列模糊、计算量大 | $O(M^2K)$ |
| **去混响** | WPE, CDR | 抑制晚期混响 | 对 RT60 敏感 | $O(M^2L^2)$ |
| **深度学习 (单通道)** | CRNN, FRCRN | 强非线性建模 | 泛化性受限 | 取决于模型 |
| **深度学习 (多通道)** | Neural BF, ArrayDPS | 联合空-谱建模 | 训练数据需求大 | 高 |
| **混合方法** | BF + DNN, SPP + MWF | 兼顾可解释性与性能 | 系统设计复杂 | 中高 |

---

## 14. 关键开放问题

1. **RTF/DOA 的鲁棒估计**：低 SNR 与高混响下
2. **非平稳噪声抑制**：风噪、音乐噪声
3. **多说话人分离 + 增强**：underdetermined 场景
4. **超低延迟实时处理**：<10ms 端到端延迟
5. **小阵列/可穿戴设备**：麦克风间距受限
6. **分布式阵列同步与融合**
7. **深度模型的可解释性与泛化**
8. **神经-传统方法融合**：Neural Beamforming, Guided Deep Filters

---

## 参考文献索引（来自 Zotero 库）

| # | 文献 | 库中标注 | Zotero 链接 |
|---|------|---------|------------|
| 1 | Gannot et al. (2017) *A Consolidated Perspective on Multimicrophone Speech Enhancement* | To Read, Reviews | [↗](zotero://select/items/0_B7ZDZGZX) |
| 2 | Souden et al. *On Optimal Frequency-Domain Multichannel Linear Filtering* | To Read, PMWF | [↗](zotero://select/items/0_SHZJBBAL) |
| 3 | Spriet et al. *Spatially pre-processed SDW-MWF* | To Read | [↗](zotero://select/items/0_7VMZFQG7) |
| 4 | Schwarz & Kellermann (2015) *Coherent-to-Diffuse Power Ratio Estimation* | ⭐⭐⭐⭐⭐, 139 citations | [↗](zotero://select/items/0_AT69JCEX) |
| 5 | Schwarz (2019) *Dereverberation and robust speech recognition using spatial coherence models* | 博士论文 | [↗](zotero://select/items/0_BD6AVHPW) |
| 6 | Ono (2011) *AuxIVA* | AuxIVA | [↗](zotero://select/items/0_4354E22N) |
| 7 | Jeub et al. (2009) *PLD dual-mic* | ⭐⭐⭐⭐⭐, 111 citations | [↗](zotero://select/items/0_LJWC8IL9) |
| 8 | Tan & Wang (2018) *CRNN* | ⭐⭐⭐⭐⭐, CRN, 321 citations | [↗](zotero://select/items/0_F8A8SVLS) |
| 9 | Habets (2013) *Linear and Parametric Microphone Array Processing* Part I-VI | Read | [Part I](zotero://select/items/0_8WIBFX7T) ~ [Part VI](zotero://select/items/0_T3MCRW79) |
| 10 | Gerkmann & Hendriks *Unbiased MMSE Noise Power Estimation* | ⭐⭐⭐⭐, LC-MMSE, 585 citations | [↗](zotero://select/items/0_A84ZJUKV) |
| 11 | Breithaupt et al. *Selective cepstro-temporal smoothing* | ⭐⭐⭐⭐, 168 citations | [↗](zotero://select/items/0_WUNQDUNP) |
| 12 | Aarabi (2004) *Phase-based dual-microphone* | ⭐⭐⭐, PEF, 163 citations | [↗](zotero://select/items/0_D8ASTBEC) |
| 13 | Jin et al. (2023) *Differential Beamforming From a Geometric Perspective* | 最新 | [↗](zotero://select/items/0_NCDQUQGD) |
| 14 | Schrammen & Jax (2022) *Front-end signal processing for far-field speech communication* | 书 | [↗](zotero://select/items/0_WQTPRE5L) |
| 15 | Reddy et al. (2021) *DNS Challenge* | 194 citations | [↗](zotero://select/items/0_P2ID54CH) |
| 16 | Grondain & Glass (2018) *GCC-PHAT Study* | ⭐⭐⭐⭐, 23 citations | [↗](zotero://select/items/0_KPFCXSPR) |
| 17 | Chen et al. (2026) *Neural BF + DNN* | preprint, 最新 | [↗](zotero://select/items/0_R4362BJ2) |
| 18 | Xiong et al. (2026) *Differential BF with UCA* | preprint, 最新 | [↗](zotero://select/items/0_I72LCJH7) |
| 19 | Wu et al. (2025) *Ultra-Low Latency SE* | Read | [↗](zotero://select/items/0_3E2SZB7V) |
| 20 | Zhang et al. (2023) *SDW-SWF with GEVD* | 最新 | [↗](zotero://select/items/0_G92LE4HL) |

---

*文档生成时间: 2026-04-11*
*数据来源: Zotero 本地 API (localhost:23119)*

## 相关 Wiki 页面

- [[concepts/active-noise-control|Active Noise Control]] — 主动噪声控制概述（语音增强的互补技术）
- [[concepts/multi-channel-anc|Multi-Channel ANC]] — 多通道 ANC，涉及多传感器/多执行器的 FxLMS 扩展
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — ANC 标准自适应算法
- [[concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]] — 在线次级路径建模
- [[concepts/offline-secondary-path-modeling|Offline Secondary-Path Modeling]] — 离线次级路径建模
- [[concepts/frequency-domain-anc|Frequency-Domain ANC]] — 频域 ANC 算法
- [[concepts/subband-anc|Subband ANC]] — 子带 ANC 算法
- [[concepts/simplified-adaptive-feedback-anc|Simplified Adaptive Feedback ANC]] — 简化自适应反馈 ANC
