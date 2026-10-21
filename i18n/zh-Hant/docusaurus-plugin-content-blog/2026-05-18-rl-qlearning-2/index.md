---
slug: 2026-05-18-rl-qlearning-2
title: "[Webots 機器人] 表格型 Q-Learning 實作與獎勵函數(Reward Shaping)調優 (#2)"
authors: [jbgih]
tags: [強化學習, Q-Learning, 獎勵函數, Webots, 機器人學, 機器學習, Python]
date: 2026-05-18
project: rl_q_learning
description: "深度解析 Webots 移動機器人的表格型 Q-Learning (Tabular Q-Learning) TD(0) 更新公式、指數衰減 ε-貪婪探索策略，以及克服稀疏獎勵 (Sparse Reward) 的稠密獎勵塑造 (Dense Reward Shaping) 調優實戰。"
keywords: ["Q-Learning 獎勵塑造", "Epsilon 貪婪探索", "稀疏獎勵強化學習", "貝爾曼最佳方程式 TD", "機器人避障"]
---

![訓練獎勵曲線](./images/01_reward_curve.png)

> 📌 **核心重點 (TL;DR)**
> - **問題 (Problem)**：在僅於目標抵達 (+1.0) 與牆面碰撞 (-1.0) 時給予反饋的稀疏獎勵 (Sparse Reward) 環境下，代理人往往需要經歷數千個回合的原地打轉或盲目徘徊，才能偶然遭遇目標，探索嚴重延遲。
> - **解決方案 (Solution)**：設計了結合基於位能的歐氏距離增量獎勵 (+0.1 × Δdist) 與單步 (-0.01)、轉向 (-0.01)、倒車 (-0.05) 懲罰的多目標**稠密獎勵塑造 (Dense Reward Shaping)** 機制，並搭配指數衰減的 ε-貪婪 (Epsilon-Greedy, 1.0 → 0.05) 探索策略。
> - **實驗結果 (Result)**：在無障礙 (`no_obstacle`) 情境下，移動平均獎勵在 500 個回合以內穩健轉正並進入高位區間 (0.7+)，最終導航成功率達到 98% 以上。

{/* truncate */}

---

## 1. 表格型 Q-Learning 更新公式與代理人架構

表格型 Q-Learning (Tabular Q-Learning) 是一種建立在貝爾曼最佳方程式 (Bellman Optimality Equation) 之上的**離策略時序差分 (Off-policy Temporal Difference, TD(0))** 演算法。

代理人維護一個形狀為 $(648, 4)$ 的二維 NumPy 陣列作為動作價值表 $Q(s, a)$。利用從 Webots Socket 伺服器即時傳輸的狀態轉移元組 $(s, a, r, s', done)$，代理人依照下列公式即時更新 $Q$ 值：

### 📐 Q-Learning TD(0) 核心更新公式

```text
Target = r + γ * max_a' Q(s', a') * (1 - done)
TD Error = Target - Q(s, a)
Q(s, a) <- Q(s, a) + α * TD Error
```

* **學習率 (Learning Rate, α = 0.1)**：平衡吸收全新經驗與保留歷史估計值之間的權重。
* **折扣因子 (Discount Factor, γ = 0.99)**：量化未來長期累積回報的現值，對多步導航至關重要。
* **終止狀態遮罩 (`1 - done`)**：在抵達目標或發生碰撞導致回合結束時，將未來的預期價值遮罩為 0，精準提取終止即時獎勵。

### 💻 代理人核心實作 (`qlearning_agent.py`)

```python
import numpy as np

class QLearningAgent:
    def __init__(self, n_states=648, n_actions=4, alpha=0.1, gamma=0.99,
                 eps_start=1.0, eps_min=0.05, eps_decay=0.995, seed=0):
        self.rng = np.random.default_rng(seed)
        self.Q = np.zeros((n_states, n_actions), dtype=np.float64)
        self.alpha = float(alpha)
        self.gamma = float(gamma)
        self.epsilon = float(eps_start)
        self.eps_min = float(eps_min)
        self.eps_decay = float(eps_decay)
        self.n_actions = int(n_actions)

    def act(self, s: int, deterministic: bool = False) -> int:
        """ε-貪婪行為策略：探索與利用的動態權衡"""
        if (not deterministic) and self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.n_actions))
        return int(np.argmax(self.Q[s]))

    def update(self, s: int, a: int, r: float, s_next: int, done: bool) -> float:
        """TD(0) 離策略 Q 表格更新"""
        target = r if done else r + self.gamma * float(np.max(self.Q[s_next]))
        td_error = target - self.Q[s, a]
        self.Q[s, a] += self.alpha * td_error
        return float(td_error)

    def decay_epsilon(self):
        """每個回合結束時執行的指數衰減"""
        self.epsilon = max(self.eps_min, self.epsilon * self.eps_decay)
```

---

## 2. 指數衰減 ε-貪婪探索策略

在訓練初期，代理人對場地環境毫無先驗知識，必須仰賴 **ε = 1.0 (100% 全隨機探索)** 來觸碰邊界並發現目標。

然而，若不對探索率進行收斂，即便代理人已經摸索出最佳路徑，仍會因高頻隨機動作而不斷撞牆。為此，我們在每個回合結束時套用逐回合指數衰減公式：

$$\varepsilon_{ep+1} = \max(\varepsilon_{min}, \varepsilon_{ep} \times 0.995)$$

* **第 1 回合**：ε = 1.0（全方位隨機探索）
* **第 300 回合**：ε ≈ 0.22（探索顯著收斂，重心轉向利用高 Q 值經驗）
* **第 600 回合**：ε = 0.05（降至設定的最低探索下限 ε_min，保持 95% 確定性最佳利用）

---

## 3. 克服稀疏導航獎勵的稠密獎勵塑造機制

移動機器人導航面臨的核心挑戰是**極端稀疏的獎勵反饋 (Sparse Reward Feedback)**。在 $1.2\text{m} \times 1.2\text{m}$ 的競技場中，隨機漫遊幾乎無法獲得任何有效反饋，直到偶然撞入 $0.10\text{m}$ 的目標容差範圍。

為了有效引導策略收斂，我們在 Webots 控制器 (`RL_controller.py`) 內部設計了多層**稠密獎勵塑造 (Dense Reward Shaping)** 體系：

| 獎勵組成項 | 數值設定 | 設計意圖與物理效果 |
| :--- | :---: | :--- |
| **抵達目標 (`REWARD_GOAL`)** | **+1.0** | 成功抵達目標位置時的正向終止獎勵 |
| **碰撞牆面/障礙 (`REWARD_COLLISION`)** | **-1.0** | 發生物理接觸時的嚴厲懲罰與回合截斷 |
| **距離增量獎勵 (`REWARD_DELTA_SCALE`)** | **+0.1 × Δdist** | 與歐氏距離縮短量成正比的即時位能引導反饋 |
| **單步時間懲罰 (`REWARD_STEP`)** | **-0.01** | 防止停滯不前，鼓勵代理人探索最短耗時路徑 |
| **轉向懲罰 (`REWARD_TURN`)** | **-0.01** | 抑制無意義的原地高頻擺頭與打轉行為 |
| **倒車懲罰 (`REWARD_BACKWARD`)** | **-0.05** | 懲罰效率低下的後退動作，強化直面前方目標 |

### 🔍 距離增量 (Distance Delta) 的數學原理
$$\Delta dist = dist_{prev} - dist_{curr}$$
* 朝目標方向前進一步 ($0.05\text{m}$)，立即獲得 $+0.1 \times 0.05 = +0.005$ 的即時正向激勵。
* 相反地，若背離目標行駛，則會承受即時扣分。這使得代理人在最初 100 個回合內就能迅速學會將車頭朝向對準目標中心。

---

## 4. 實證評估：獎勵曲線與成功率收斂

在 `no_obstacle`（無障礙場地）中進行 1,500 個回合的完整訓練，展現了與理論分析高度契合的優異收斂特性。

![成功率曲線](./images/02_success_curve.png)

### 📈 收斂階段里程碑
1. **第 0 ~ 200 回合（初期探索階段）**：
   * 頻繁發生撞牆以及達到 150 步逾時上限，移動平均獎勵徘徊在負數區間 (-0.4 ~ -0.2)。
2. **第 200 ~ 500 回合（快速攀升階段）**：
   * 隨著距離增量位能獎勵在 Q 表格中有效反向傳播，策略在 `goal_heading` 居中時建立起強烈的直行傾向。
   * 成功率從 20% 迅猛攀升至 **80% 以上**。
3. **第 500 ~ 1,500 回合（漸近收斂穩定階段）**：
   * ε 穩定在 0.05 下限，單回合平均消耗步數從 150 步劇降至 **15 ~ 22 步**。
   * 100 回合移動平均成功率穩定收斂在 **98.5% 以上**。

---

## 5. 下一步研究方向

我們已經驗證，在 648 個離散狀態空間下，表格型 Q-Learning 能夠乾淨俐落地征服開闊平原導航。

然而，**真實物理世界充滿著複雜的牆面與死胡同障礙**。在第 3 篇中，我們將直面 **`obstacle12` 與 `obstacle_hard` 迷宮地圖**，深入剖析代理人如何跳出局部最佳陷阱，並利用多重隨機種子平行訓練建構高強健性導航策略！
