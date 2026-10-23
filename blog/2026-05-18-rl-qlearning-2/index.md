---
slug: 2026-05-18-rl-qlearning-2
title: "[Webots Robotics] Tabular Q-Learning Implementation & Reward Shaping Tuning (#2)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, reward-shaping, webots, robotics, machine-learning, python]
date: 2026-05-18
project: rl_q_learning
description: "In-depth breakdown of Tabular Q-Learning TD(0) update formulas, exponential epsilon-decay exploration, and dense reward shaping to overcome sparse rewards in mobile robot navigation."
keywords: ["Q-Learning Reward Shaping", "Epsilon Greedy Exploration", "Sparse Reward Reinforcement Learning", "Bellman Optimality TD", "Robot Obstacle Avoidance"]
---

![Training Reward Curve](./images/01_reward_curve.png)

> 📌 **Key Takeaways (TL;DR)**
> - **Problem**: Sparse reward setups (+1.0 at goal, -1.0 at collision) cause severe exploration delays, causing the agent to wander or spin for thousands of episodes before stumbling upon the target.
> - **Solution**: Implemented a multi-objective **Dense Reward Shaping** mechanism combining potential-based Euclidean distance delta rewards (+0.1 × Δdist) with step (-0.01), turning (-0.01), and backward (-0.05) penalties, paired with exponential epsilon decay (1.0 → 0.05).
> - **Result**: The moving average reward shifted into a steady positive regime (0.7+) within 500 episodes in the `no_obstacle` scenario, achieving a 98%+ goal success rate.

{/* truncate */}

---

## 1. Tabular Q-Learning Update Formula & Agent Architecture

Tabular Q-Learning is an **off-policy Temporal Difference (TD(0))** algorithm grounded in the Bellman Optimality Equation.

The agent maintains an action-value table Q(s, a) structured as a 2D NumPy array of shape $(648, 4)$. Using the experience transition tuple $(s, a, r, s', done)$ streamed from the Webots socket server, the $Q$-values are updated in real time via:

### 📐 Q-Learning TD(0) Update Rule

```text
Target = r + γ * max_a' Q(s', a') * (1 - done)
TD Error = Target - Q(s, a)
Q(s, a) <- Q(s, a) + α * TD Error
```

* **Learning Rate (α = 0.1)**: Balances the rate of incorporating new feedback versus retaining historical estimates.
* **Discount Factor (γ = 0.99)**: Values long-term future returns, critical for multi-step navigation.
* **Terminal Masking (`1 - done`)**: Clamps future expectations to zero upon goal arrival or collision, isolating the terminal reward.

### 💻 Agent Core Implementation (`qlearning_agent.py`)

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
        """ε-Greedy behavior policy: Exploration vs. Exploitation"""
        if (not deterministic) and self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.n_actions))
        return int(np.argmax(self.Q[s]))

    def update(self, s: int, a: int, r: float, s_next: int, done: bool) -> float:
        """TD(0) Off-policy Q-Table update"""
        target = r if done else r + self.gamma * float(np.max(self.Q[s_next]))
        td_error = target - self.Q[s, a]
        self.Q[s, a] += self.alpha * td_error
        return float(td_error)

    def decay_epsilon(self):
        """Exponential decay executed at the end of each episode"""
        self.epsilon = max(self.eps_min, self.epsilon * self.eps_decay)
```

---

## 2. Exponential Epsilon-Greedy Decay Strategy

At the start of training, the agent has zero domain knowledge, requiring **ε = 1.0 (100% random exploration)** to discover the arena boundaries.

However, an uncurbed exploration rate induces perpetual collisions even after the optimal path has been resolved. We apply per-episode exponential decay:

**ε_(ep+1) = max(ε_min, ε_ep × 0.995)**

* **Episode 1**: ε = 1.0 (Full exploration)
* **Episode 300**: ε ≈ 0.22 (Shift toward exploiting high Q-values)
* **Episode 600**: ε = 0.05 (Floor exploration rate ε_min, 95% greedy execution)

---

## 3. Dense Reward Shaping for Sparse Navigation

A fundamental challenge in mobile robotics is **sparse reward feedback**. In a 1.2m × 1.2m arena, moving randomly yields zero reward until the robot coincidentally intersects the $0.10m$ goal tolerance.

To guide convergence, we engineered a **Dense Reward Shaping** schedule inside the Webots controller (`RL_controller.py`):

| Reward Component | Value | Design Objective & Physical Effect |
| :--- | :---: | :--- |
| **Goal Reached (`REWARD_GOAL`)** | **+1.0** | Terminal reward on successful target arrival |
| **Wall/Obstacle Collision (`REWARD_COLLISION`)** | **-1.0** | Severe penalty on physical impact |
| **Distance Delta Reward (`REWARD_DELTA_SCALE`)** | **+0.1 × Δdist** | Immediate feedback proportional to Euclidean distance reduction |
| **Step Time Penalty (`REWARD_STEP`)** | **-0.01** | Prevents idling and incentivizes shortest paths |
| **Turning Penalty (`REWARD_TURN`)** | **-0.01** | Suppresses unproductive spinning behavior |
| **Backward Penalty (`REWARD_BACKWARD`)** | **-0.05** | Discourages inefficient reverse driving |

### 🔍 Mathematical Principle of Distance Delta
**Δdist = dist_prev - dist_curr**
* Driving $0.05m$ toward the target awards $+0.1 \times 0.05 = +0.005$ immediately.
* Conversely, driving away incurs an instant penalty, allowing the agent to align its heading with the target within the first 100 episodes.

---

## 4. Empirical Evaluation: Reward and Success Curves

Training for 1,500 episodes in the `no_obstacle` world demonstrated remarkable convergence matching our theoretical expectations.

![Success Rate Curve](./images/02_success_curve.png)

### 📈 Convergence Milestones
1. **Episodes 0 ~ 200 (Exploration Phase)**:
   * Frequent wall collisions and 150-step timeouts keep the moving average reward in the negative range (-0.4 ~ -0.2).
2. **Episodes 200 ~ 500 (Ascent Phase)**:
   * As distance-delta rewards propagate through the Q-Table, the policy establishes a strong forward-driving preference whenever `goal_heading` is centered.
   * Success rate surges from 20% to **over 80%**.
3. **Episodes 500 ~ 1,500 (Asymptotic Convergence)**:
   * With ε settled at 0.05, average steps per episode plummet from 150 (timeout) to **15 ~ 22 steps**.
   * The 100-episode moving average success rate converges above **98.5%**.

---

## 5. What's Next?

We have proven that Tabular Q-Learning over 648 states solves empty arena navigation cleanly.

However, **real-world environments are packed with walls and obstacles**. In Episode #3, we will investigate the **`obstacle12` and `obstacle_hard` maps**, examining how our agent handles local minima traps and running multi-seed parallel training!

---

## Summary & Key Takeaways

- **Bellman Optimality Formulation**: Formulated tabular Q-value updates with learning rate α = 0.1 and discount factor γ = 0.95 to guarantee mathematical convergence across discrete state transitions.
- **Multi-Objective Reward Shaping**: Engineered a balanced reward function combining distance-delta incentives (+10 × Δd), goal arrival bonuses (+100), step costs (-0.1), and collision penalties (-50).
- **Adaptive Exploration Schedule**: Applied an exponential ε-decay policy from 1.0 down to a floor of 0.05 over 1,000 episodes, effectively balancing exploration with exploitation.
- **Empirical Convergence**: Validated rapid policy convergence within 300 to 500 episodes in open benchmark environments before scaling to obstacle-dense arenas.

