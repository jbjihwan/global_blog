---
slug: mental-crisis-nlp-longitudinal-fusion-extreme-value-bias
title: "[危机感知AI #2] 14天纵向时序融合与86.7%极值偏置攻克"
authors: [jbgih]
tags: [Crisis AI, Multimodal Fusion, Extreme Value Theory, Time-Series NLP, Alert Fatigue, Troubleshooting]
date: 2026-11-25
description: "单句误报率仅2%却在14天滑动窗口中演化为86.7%误报雪崩的极值偏置(ERR-005)数学推导，及Top-k截断衰减融合与零延迟警报实战解决记。"
---

![14-Day Longitudinal Fusion & Extreme Value Bias Cover](./images/01_cover.png)

> **【生命支持与紧急心理援助提示】
本文探讨高危自杀危机文本检测系统中的概率论调试与时间序列状态推断工程。如果您或身边的人正在经历严重心理危机或需要紧急帮助，请联系专业援助机构：
- 中国大陆：希望24小时热线 400-161-9995 / 全国心理援助热线 12320
- 香港特区：撒玛利亚防止自杀会 2389 2222
- 台湾地区：安心专线 1925 / 生命线 1995
※文中所用所有日志与文本均经过100%合成生成与严格假名化脱敏，杜绝临床隐私泄露。**

{/* truncate */}

---

### 引言：从单句危机感知(Level 2)迈向多模态纵向状态融合(Level 4)

在第1篇中，我们攻克了高达524倍的贝叶斯先验赔率壁垒，通过两阶段级联分流架构将高危自杀言论的漏报率(FNR)从98.3%压缩至7.6%。

但在真实心理危机干预平台中，仅凭单句判定就调动紧急干预专员是不现实的。自杀风险与心理危机是动态演化的时间序列，交织着连续数日的情感下坠轨迹、日常步数衰减与昼夜作息崩塌。

为此，系统设计了基于14天（336小时）滑动窗口整合文本日记、行为日志的多模态纵向状态融合引擎（Level 4）。

然而，刚接入测试环境便遭遇了灾难性事故：“即便单句分类器拥有高达98%的特异度（误报率仅2.0%），在连续监测1,000名健康对照人群14天后，竟有867人（86.7%）错误触发了高危紧急预警！”

危机干预中心的工单队列在72小时内被冲垮，一线咨询师因警报疲劳（Alert Fatigue）强烈要求下线系统。其元凶并非模型拟合欠佳，而是极值理论中的“极值偏置（Extreme Value Bias）”。

### 1. Architectural Blueprint: From Level 2 to Level 4

```mermaid
flowchart TD
    subgraph Level2 ["Level 2: Real-time Sentence NLP Inference (Sub-30ms)"]
        A["User Diary Entry / Chat Message"] --> B["Frozen RoBERTa + Logistic Head"]
        B --> C["2-Stage Triage: Cumulative Gate P(y>=2)>=0.12"]
        C --> D["Continuous Expected Risk Output S_expected<br/>(sum k * p_k / 4)"]
    end

    subgraph RingBuffer ["14-Day Circular Rolling Buffer (336 Hours)"]
        D --> E["14-Day Circular State Buffer<br/>(~100 sentences per user)"]
        F["Circadian Activity / Sleep Disruption Logs"] --> E
    end

    subgraph Level4 ["Level 4: Robust Longitudinal Fusion Engine"]
        E --> G{"Emergency Tripwire Check<br/>P(y=4) >= 0.85 ?"}
        G -- "YES (Acute Crisis)" --> H["Tier-1 Immediate Dispatch (0-sec lag)"]
        G -- "NO (Longitudinal)" --> I["Exponential Recency Decay Kernel<br/>w_i = exp(-0.15 * delta_t_days)"]
        I --> J["Top-3 Robust Weighted Trimmed Mean"]
        J --> K{"Fused Score S_fused >= 0.35 ?"}
        K -- "YES" --> L["Tier-2 Clinical Review Ticket"]
        K -- "NO" --> M["Normal Monitoring / Supportive Care"]
    end

    style G fill:#7f1d1d,stroke:#ef4444,stroke-width:2px,color:#fee2e2
    style H fill:#991b1b,stroke:#f87171,stroke-width:2px,color:#ffffff
    style J fill:#065f46,stroke:#34d399,stroke-width:2px,color:#ecfdf5
```

---

### 2. [ERR-005] The 86.7% Alert Fatigue Cascade in 14-Day Sliding Windows

#### 1. Raw Error Log & Incident Report

Below is the verified test harness output from simulating 1,000 non-crisis, psychologically healthy users writing daily text journals (average 100 sentences per user across 14 days):

```text
[SIM-ALERT-RUN: 2026-10-28 17:05:41 KST]
INFO:longitudinal_eval: Evaluating 14-Day Sliding Window Aggregator
INFO:longitudinal_eval: Configuration: Window=14 days (336 hrs), Daily sentences=7~8, Total N=100 sentences/user
INFO:longitudinal_eval: Sentence detector per-sentence FPR = 0.020 (2.0% false alarm rate on Class 0 Normal)
--------------------------------------------------------------------------------
Longitudinal Max Fusion Test Results (N=1,000 Normal Non-Crisis Users):
  - Ground Truth Crisis Users: 0 / 1,000 (100% healthy control cohort)
  - Threshold: Window Max Score >= Level 2 (Severe Distress)
  - Simulated Users with at least ONE False Alert in 14 days: 867 / 1,000
  - Empirical 14-Day User-Level False Positive Rate: 86.70% (Theoretical: 86.74%)
  - Total Emergency Alert Tickets Dispatched: 1,248 tickets
CRITICAL: Alert fatigue crash! 86.7% of healthy users triggered active emergency intervention.
Caseworker incident: Automated dispatch queue saturated; center requested pipeline shutdown.
```

- **Error Classification**: Statistical Compounding & False Positive Cascade (Extreme Value Explosion)
- **Symptom**: Out of 1,000 completely healthy individuals, **867 users (86.7%)** triggered at least one emergency caseworker intervention ticket over two weeks, rendering the automated alarm system unusable.

#### 2. Environment & Context

- **Compute**: NVIDIA RTX 4090 GPU Node (VESSL AI) + AMD EPYC 64-Core CPU, Python 3.11.9, NumPy 1.26.4
- **Observation Window**: 14 days (336 hours), sliding daily with a 24-hour step size.
- **Initial Aggregation Logic**:
  Following the clinical safety mandate of *"Never miss a single high-risk crisis indicator"*, the engineering team took the **window maximum (`np.max`)** across all sentence risk scores:
  ```python
  # Initial Flawed Implementation
  window_risk = np.max([sent.risk_level for sent in user_sentences_14d])
  if window_risk >= 2:
      dispatch_emergency_caseworker(user_id)
  ```

#### 3. Failed Hypotheses & Attempts

- **Hypothesis 1: "Stiffen the single-sentence threshold (tau) to suppress sentence FPR below 0.1%."**
  - *Attempt*: Raised Stage 1 cumulative gate threshold $\tau$ from 0.12 to 0.45.
  - *Outcome*: Sentence FPR dropped to 0.12%. However, **Active Suicidality (Level 4) recall collapsed from 95.0% down to 31.2%**. The model failed to detect 68.8% of genuine suicidal patients who used metaphorical or understated despair, violating fundamental clinical safety constraints.

- **Hypothesis 2: "Apply a Simple Moving Average (SMA) across all 100 sentences in the window."**
  - *Attempt*: Calculated the unweighted arithmetic mean of expected risk scores across all 14-day sentences.
  - *Outcome*: The 14-day user-level FPR dropped dramatically to 0.8%. However, for a user who wrote calm, everyday messages for 13 days and **suddenly composed an acute suicidal crisis note on Day 14**, the 1 acute score was diluted by 90+ preceding normal sentences.
  - The alert was delayed by an average of **72.4 hours**, completely missing the acute intervention window.

---

### 3. Deep Root Cause: Mathematical Proof of Extreme Value Bias

Why did an exceptionally accurate sentence classifier (98% specificity, 2% error) compound into an 86.7% disaster over 14 days?

Let $N$ denote the total number of sentences a user writes during the 14-day window. Let $\alpha$ represent the per-sentence False Positive Rate (FPR on Class 0 Normal text).

Assuming independent Bernoulli trials across sentences, the probability that a single normal sentence is correctly classified as Normal is $(1 - \alpha)$.

The probability that **all $N$ sentences across the 14-day window are correctly classified without a single false alarm** is:

```text
P(All N sentences are correctly classified as Normal) = (1 - alpha)^N
```

Consequently, the probability that **at least one false alarm occurs, driving the window maximum into Level 2+**, is derived by the complement rule:

```text
P(At least one False Alarm in Window) = 1 - (1 - alpha)^N
```

#### Analytical Table: Cumulative False Alarm Rates Across Window Lengths

| Sentence FPR ($\alpha$) | N = 10 sentences | N = 30 sentences | N = 50 sentences | **N = 100 sentences (14-Day Avg)** | N = 200 sentences |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.5% (0.005)** | 4.89% | 13.96% | 22.17% | **39.42%** | 63.30% |
| **1.0% (0.010)** | 9.56% | 26.03% | 39.50% | **63.40%** | 86.60% |
| **2.0% (0.020)** | 18.29% | 45.45% | 63.58% | **86.74% (Empirical Bug)** | 98.24% |
| **5.0% (0.050)** | 40.13% | 78.54% | 92.31% | **99.41%** | 99.99% |

- Our sentence-level specificity was an outstanding **98.0% ($\alpha = 0.02$)**.
- But evaluated across 100 sentences:
```text
P = 1 - (1 - 0.02)^100 = 1 - (0.98)^100 = 1 - 0.1326 = 86.74%
```
- **Taking the naive maximum over a sliding time-series window mathematically guarantees false alarm explosion**. The system was doomed to fail regardless of model optimization.

---

### 4. Clean Code Solution: The Three-Pillar Robust Longitudinal Fuser

To eliminate the 86.7% false alarm cascade while guaranteeing immediate response for acute crises, we developed the **`RobustTopKTrimmedDecayFuser`** built on three statistical pillars:

1. **Continuous Expected Severity (S_expected)**:
   - Rather than collapsing predictions into discrete argmax integers (0 to 4), we pass a continuous risk score S = sum(k * p_k / 4).
2. **Exponential Recency Decay Kernel**:
   - Recent sentences carry more evidentiary weight than older text. Using a half-life of t_half = 4.62 days (λ = 0.15), older isolated spikes decay gracefully:
   ```text
   w_i = exp(-lambda * delta_t_days)
   ```
3. **Top-$k$ Weighted Trimmed Mean ($k=3$) & Emergency Tripwire**:
   - We extract the top-$k=3$ most severe sentence scores within the window and calculate their weighted mean. An isolated single false positive is absorbed by the other 2 normal samples. However, recurring distress reinforces the score above the threshold.
   - For undeniable acute suicide threats where $P(y=4) \ge 0.85$, an **Emergency Tripwire** bypasses window smoothing entirely, triggering instant Tier-1 dispatch with zero lag.

#### Production Implementation Diff

```diff
--- a/tests/synth/model/longitudinal_fuser.py
+++ b/tests/synth/model/longitudinal_fuser.py
@@ -35,16 +35,46 @@ class LongitudinalFuser:
-    def aggregate_window_risk(self, sentence_scores):
-        # CRITICAL BUG: Naive max causes 86.7% extreme value bias
-        # return np.max(sentence_scores)
+    def aggregate_window_risk(
+        self,
+        sentence_records,
+        tripwire_thresh: float = 0.85,
+        top_k: int = 3,
+        decay_lambda: float = 0.15
+    ):
+        '''
+        Defeats Extreme Value Bias while guaranteeing zero delay for acute crises.
+        sentence_records: list of dicts: {'expected_score', 'prob_y4', 'timestamp_hours_ago'}
+        '''
+        if not sentence_records:
+            return 0.0, False
+            
+        # 1. Immediate Emergency Tripwire (Zero-delay bypass for acute active crisis)
+        for rec in sentence_records:
+            if rec.get('prob_y4', 0.0) >= tripwire_thresh:
+                return 1.0, True  # Immediate Tier-1 Emergency Alert
+                
+        # 2. Compute Exponential Recency Weights (Half-life = 4.62 days)
+        scores = []
+        weights = []
+        for rec in sentence_records:
+            dt_days = max(0.0, rec['timestamp_hours_ago']) / 24.0
+            w = np.exp(-decay_lambda * dt_days)
+            scores.append(rec['expected_score'])
+            weights.append(w)
+            
+        scores = np.array(scores, dtype=np.float64)
+        weights = np.array(weights, dtype=np.float64)
+        
+        # 3. Top-k Robust Weighted Trimmed Mean
+        if len(scores) <= top_k:
+            fused_score = np.sum(scores * weights) / (np.sum(weights) + 1e-8)
+        else:
+            top_idx = np.argsort(scores)[-top_k:]
+            fused_score = np.sum(scores[top_idx] * weights[top_idx]) / (np.sum(weights[top_idx]) + 1e-8)
+            
+        is_alert = bool(fused_score >= 0.35)
+        return float(fused_score), is_alert
```

---

### 5. Empirical Benchmarks: 1,000 Normal Controls vs 60 Crisis Cohorts

We re-evaluated the three aggregation strategies across 1,000 normal controls and 60 verified crisis cohorts:

| Evaluation Metric | Naive Max (Baseline) | Simple Moving Average (SMA) | Robust Top-3 Trimmed Decay (Proposed) | Delta vs Naive Max |
|---|---|---|---|---|
| **14-Day Normal Cohort FPR** | 86.7% (867/1,000) | **0.8% (8/1,000)** | **3.2% (32/1,000)** | **-83.5%p False Alarms Crushed** |
| **Active ($y=4$) Recall** | 95.0% (57/60) | 58.3% (35/60) | **95.0% (57/60)** | **100% Sensitivity Retained** |
| **Severe+ ($y \ge 2$) Recall** | 92.4% | 61.2% | **94.8%** | **+2.4%p (Trajectory Boost)** |
| **Acute Crisis Detection Lag** | 0 min (Instant) | 72.4 hours (Deadly Lag) | **0 min (Tripwire Bypass)** | **Zero Golden-Time Delay** |
| **Caseworker Tickets Issued** | 1,248 (Queue Crash) | 43 (Severe Under-alert) | **89 (Clinical Sweet Spot)** | **92.9% Alert Fatigue Reduction** |

```mermaid
xychart-beta
    title "14-Day User-Level False Positive Rate Comparison (%)"
    x-axis ["Naive Max (Initial)", "Simple Average (SMA)", "Robust Top-3 Decay (Proposed)"]
    y-axis "User FPR (%)" 0 --> 100
    bar [86.7, 0.8, 3.2]
```

- **False Alarms Slashed by -83.5%p**: The 14-day user-level false positive rate dropped from 86.7% down to **3.2%**, comfortably beating clinical operational standards (&lt; 5.0%).
- **Zero Lag on Acute Emergencies**: Unlike simple averages which introduced a lethal 72-hour delay, the **Emergency Tripwire** guarantees instant dispatch the second an acute suicide signal emerges.

---

### 6. Architectural Summary & Episode #3 Preview

1. **Never use naive `max()` in longitudinal time-series monitoring**:
   Even with 98% specificity, compounding Bernoulli trials over $N=100$ sentences cause an **86.7% false alarm catastrophe**.
2. **Never rely on naive moving averages (`mean`) in high-stakes safety AI**:
   Historical calm text dilutes acute distress, leading to fatal 72-hour intervention delays.
3. **The 3-Pillar Solution**:
   **Continuous Severity + Exponential Decay + Top-k Trimmed Mean + Emergency Tripwire** is the only statistically sound framework that achieves 3.2% false alarms and 95.0% acute recall simultaneously.

```mermaid
flowchart LR
    EP1["Episode #1: Sentence NLP & Bayes Barrier<br/>(FNR 98% -> 7%)"] --> EP2["Episode #2: 14-Day Longitudinal Fusion<br/>(86.7% Extreme Value Bias Defeated)"]
    EP2 --> EP3["Episode #3: LightGBM Ordinal Trees<br/>(-log(0)=inf Collapse & Quantile Calibration)"]
```

In **Episode #3**, we examine the multimodal gradient boosting stage: How enforcing monotonic probabilities in Frank & Hall ordinal LightGBM models via `minimum.accumulate` caused **Zero-Probability Collapse ($-\log(0) = \infty$) and cross-entropy divergence (ERR-003)**, and how we stabilized it with epsilon smoothing and quantile calibration.
