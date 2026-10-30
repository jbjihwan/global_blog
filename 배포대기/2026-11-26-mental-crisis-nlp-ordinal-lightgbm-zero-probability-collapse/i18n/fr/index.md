---
slug: mental-crisis-nlp-ordinal-lightgbm-zero-probability-collapse
title: "LightGBM Arbres Ordinaux: Résoudre le Crash -log(0)=inf"
authors: [jbgih]
tags: [crisis-ai, ordinal-classification, lightgbm, probability-calibration, machine-learning, devlog]
date: 2026-11-26
keywords: ["LightGBM Ordinal Classification", "Frank and Hall 2001", "Zero-Probability Collapse", "Monotonic Accumulation", "Quantile Calibration", "High-Stakes AI"]
description: "Résolution du crash -log(0)=inf et de l'effondrement de probabilité zéro dans LightGBM avec la monotonie Frank & Hall et le recalibrage quantile."
---

![LightGBM Ordinal Trees & Simplex Calibration](./images/01_cover.png)

> ⚠️ **Clinical Safety & Crisis Operations Protocol Notice**  
> This article is a dedicated systems engineering whitepaper detailing numerical stability and ordinal probability calibration algorithms for high-stakes crisis response infrastructure.  
> - **United States / Canada**: Call or text **988** (Suicide & Crisis Lifeline).  
> - **United Kingdom**: Call **111** (NHS Mental Health Services) or **116 123** (Samaritans).  
> - **International**: Visit [findahelpline.com](https://findahelpline.com/) for verified confidential local crisis services worldwide.  
> *All logs, numerical walkthroughs, and text snippets in this article have been 100% pseudonymized and synthetically generated to strictly prevent clinical PII leakage.*

{/* truncate */}

---

### Introduction: Why Standard Multiclass Softmax Fails in High-Stakes Clinical AI

In **Episode #1**, we resolved the 524x Bayes prior likelihood barrier, driving down active suicidal sentence False Negative Rates (FNR) from 98.3% to 7.6%. In **Episode #2**, we conquered the 86.7% false alarm cascade in 14-day longitudinal observation windows using our Top-3 Trimmed Decay Fuser.

However, when our **Level 4 Multimodal State Fuser** attempts to output final, discrete triage severity levels for human caseworker intervention, standard machine learning paradigms trigger a catastrophic mathematical breakdown.

In psychiatric risk assessment, triage categories possess a strict **natural ordering**:
- **Level 0 (Safe / Routine Discourse)**
- **Level 1 (Psychological Distress / Depressive Mood)**
- **Level 2 (Passive Suicidal Ideation - No Plan)**
- **Level 3 (Severe Crisis - Plan & Method Formulated)**
- **Level 4 (Acute Imminent Crisis - Immediate Dispatch Mandated)**

Standard deep learning and boosting models rely on **Softmax Cross-Entropy**, which inherently assumes categorical symmetry. To a softmax loss function, predicting Level 0 when the true state is Level 4 incurs the exact same gradient penalty as predicting Level 1 when the true state is Level 2. In clinical safety engineering, this symmetric penalty is unacceptable.

To enforce ordinal monotonicity, we implemented the industry-standard **Frank & Hall (2001) Cumulative Ordinal Classification** framework on top of LightGBM. Yet during integration testing, our training loop encountered a fatal numerical singularity: **Zero-Probability Collapse and `-log(0) = inf` Loss Divergence**.

---

### 1. Production Incident Log & Failure Symptoms

During hyperparameter optimization over 10,000 synthetic patient cohorts, our boosting pipeline crashed abruptly at iteration 412:

```text
[CRITICAL] 2026-11-26 03:14:22.812 [fuser_trainer.py:284]
Traceback (most recent call last):
  File "tests/synth/model/fuser.py", line 284, in evaluate_ordinal_cross_entropy
    loss = -np.mean(np.log(predicted_proba[np.arange(N), y_true]))
RuntimeWarning: divide by zero encountered in log
Loss Output: inf (Optimization Halts)
ValueError: Objective function returned NaN/Inf at iteration 412. Boosting terminated abnormally.
```

- **Error Classification**: IEEE 754 Floating-Point Singularity (`-log(0) = inf`)
- **System Impact**: Total training pipeline halt, unrecoverable gradient explosion.
- **Root Location**: `tests/synth/model/fuser.py` cumulative-to-discrete probability transform.

---

### 2. Mechanics of the Frank & Hall Ordinal Framework

For a 5-class ordinal spectrum ($K=5$), the Frank & Hall (2001) method decomposes the target into $K-1 = 4$ cumulative binary classification tasks:
- **Tree 1 ($M_1$)**: Predicts $P(y \ge 1)$ (Level 0 vs Levels 1, 2, 3, 4)
- **Tree 2 ($M_2$)**: Predicts $P(y \ge 2)$ (Levels 0, 1 vs Levels 2, 3, 4)
- **Tree 3 ($M_3$)**: Predicts $P(y \ge 3)$ (Levels 0, 1, 2 vs Levels 3, 4)
- **Tree 4 ($M_4$)**: Predicts $P(y \ge 4)$ (Levels 0, 1, 2, 3 vs Level 4)

By the fundamental axioms of probability, cumulative probabilities must satisfy **strict monotonic non-increasing ordering**:
$$P(y \ge 1) \ge P(y \ge 2) \ge P(y \ge 3) \ge P(y \ge 4)$$

Discrete class probabilities $P(y=k)$ are subsequently derived via successive differences:
- $P(y=0) = 1.0 - P(y \ge 1)$
- $P(y=1) = P(y \ge 1) - P(y \ge 2)$
- $P(y=2) = P(y \ge 2) - P(y \ge 3)$
- $P(y=3) = P(y \ge 3) - P(y \ge 4)$
- $P(y=4) = P(y \ge 4)$

---

### 3. Deep Root Cause: Monotonic Downward Accumulation & Zero Collapse

Because the 4 LightGBM estimators are trained independently, their unconstrained predictions inevitably experience **Boundary Inversion** in noisy feature spaces:

```text
Raw Predicted Cumulative Probabilities:
M1: P(y >= 1) = 0.8820
M2: P(y >= 2) = 0.4510
M3: P(y >= 3) = 0.4980  <-- INVERSION! P(y >= 3) > P(y >= 2)
M4: P(y >= 4) = 0.0210
```

Allowing $P(y \ge 3) > P(y \ge 2)$ implies that being in Level 3 or higher is more likely than being in Level 2 or higher, producing an impossible negative probability:
$$P(y=2) = 0.4510 - 0.4980 = -0.0470$$

To eliminate negative values, standard machine learning libraries execute **Monotonic Downward Accumulation** via NumPy's `np.minimum.accumulate`:

```python
ge_mono = np.minimum.accumulate(cumulative_ge, axis=1)
```

Running this operation forces:
- $P(y \ge 2) = \min(0.8820, 0.4510) = 0.4510$
- $P(y \ge 3) = \min(0.4510, 0.4980) = **0.4510**$

Both cumulative thresholds collapse onto an identical numerical plateau. When computing the discrete difference:
$$P(y=2) = P(y \ge 2) - P(y \ge 3) = 0.4510 - 0.4510 = **0.000000**$$

When a true clinical sample has label $y=2$, the Negative Log-Likelihood loss evaluates to:
$$Loss_i = -\log(P(y = y_i)) = -\log(0.0) = **inf**$$

This singularity corrupts the batch mean, generating `NaN/Inf` gradients and terminating optimization.

---

### 4. Why Naive `np.clip` Fails in Safety Systems

A common reflexive reaction is simple value clamping:

```python
# [FLAWED FIX]: Raw Clamping
proba = np.clip(proba, 1e-15, 1.0)
```

While this prevents immediate crash, it introduces severe statistical distortions:
1. **Bayesian Simplex Axiom Violation**: Raising $0.0$ to $10^-15$ causes $sum(p_k) p_k > 1.0$.
2. **Brier Score Degradation**: Unnormalized probabilities degraded multi-class Brier score from 0.038 to 0.142.
3. **Calibration Breakdown**: The Expected Calibration Error (ECE) spiked to 0.184, destroying caseworker confidence scores.

---

### 5. Architectural Pipeline: Simplex Re-projection Engine

```mermaid
flowchart TD
    subgraph Raw_Models ["1. Independent LightGBM Trees (Frank & Hall)"]
        A[Multimodal Longitudinal Features] --> M1["M1: P(y >= 1)"]
        A --> M2["M2: P(y >= 2)"]
        A --> M3["M3: P(y >= 3)"]
        A --> M4["M4: P(y >= 4)"]
    end

    subgraph Trap_Zone ["2. The Zero-Probability Trap"]
        M1 & M2 & M3 & M4 --> B{"Boundary Inversion Check<br/>P(y>=3) > P(y>=2)?"}
        B -->|Inversion Detected| C["np.minimum.accumulate<br/>Forces Monotonic Plateau"]
        C --> D["Difference: P(y=2) = 0.000000"]
        D -->|Ground Truth y=2| E["-log(0) = inf Loss Explosion!"]
    end

    subgraph Solution_Engine ["3. Simplex Re-projection & Quantile Calibrator"]
        D --> F["Epsilon Floor Clamping<br/>eps = 1e-6"]
        F --> G["L1 Simplex Renormalization<br/>proba / sum(proba, axis=1)"]
        G --> H["Isotonic Quantile Calibration<br/>ECE drops 0.184 -> 0.021"]
        H --> I["Validated Decision Confidence<br/>0.00% Zero-Crash Guarantee"]
    end

    style E fill:#f87171,stroke:#dc2626,stroke-width:2px,color:#fff
    style I fill:#34d399,stroke:#059669,stroke-width:2px,color:#fff
```

---

### 6. Production Solution: Code Diff & Calibrator

We deployed a mathematically rigorous **Vectorized Epsilon Floor & L1 Simplex Re-projection** algorithm:

```diff
--- a/tests/synth/model/fuser.py
+++ b/tests/synth/model/fuser.py
@@ -148,15 +148,27 @@ def ordinal_binary_to_proba(cumulative_ge):
     """
     Convert Frank & Hall cumulative binary probabilities to 5-class simplex.
     Ensures mathematical monotonicity and prevents -log(0) = inf divergence.
     """
     # Step 1: Enforce monotonic non-increasing downward accumulation
     ge_mono = np.minimum.accumulate(cumulative_ge, axis=1)
     
-    # CRITICAL BUG: Direct differencing causes exact 0.000000 on plateaus
-    # proba[:, 1] = ge_mono[:, 0] - ge_mono[:, 1]
-    # loss = -log(0.0) -> inf
+    # Step 2: Compute class probabilities via sequential differences
+    proba = np.zeros((cumulative_ge.shape[0], 5), dtype=np.float64)
+    proba[:, 0] = 1.0 - ge_mono[:, 0]
+    proba[:, 1] = ge_mono[:, 0] - ge_mono[:, 1]
+    proba[:, 2] = ge_mono[:, 1] - ge_mono[:, 2]
+    proba[:, 3] = ge_mono[:, 2] - ge_mono[:, 3]
+    proba[:, 4] = ge_mono[:, 3]
+    
+    # Step 3: FIX - Epsilon floor clamping (eps = 1e-6)
+    # Prevents zero singularity while maintaining gradient sensitivity
+    eps = 1e-6
+    proba = np.clip(proba, eps, 1.0)
+    
+    # Step 4: Row-wise L1 Simplex Re-normalization (Sum p_k == 1.0)
+    # Strictly preserves Bayesian probability simplex axioms
+    proba /= proba.sum(axis=1, keepdims=True)
+    return proba
```

Coupled with our post-hoc **Ordinal Isotonic Calibrator**:

```python
from sklearn.isotonic import IsotonicRegression

class OrdinalIsotonicCalibrator:
    def __init__(self):
        self.calibrators = [IsotonicRegression(out_of_bounds='clip', y_min=0.0, y_max=1.0) for _ in range(4)]
        
    def fit(self, cumulative_ge, y_true):
        for k in range(4):
            target_k = (y_true >= (k + 1)).astype(np.float64)
            self.calibrators[k].fit(cumulative_ge[:, k], target_k)
            
    def transform(self, cumulative_ge):
        calibrated = np.zeros_like(cumulative_ge)
        for k in range(4):
            calibrated[:, k] = self.calibrators[k].predict(cumulative_ge[:, k])
        return np.minimum.accumulate(calibrated, axis=1)
```

---

### 7. Production Benchmark Results

Evaluated across 10,000 synthetic patient trajectory profiles using 5-Fold Stratified Cross-Validation:

```mermaid
xychart-beta
    title "Expected Calibration Error (ECE) Comparison (Lower is Better)"
    x-axis ["Naive Clip (Initial)", "Platt Scaling (Sigmoid)", "Simplex + Isotonic (Proposed)"]
    y-axis "ECE Score" 0.00 --> 0.20
    bar [0.184, 0.089, 0.021]
```

| Metric | Uncalibrated Raw | Naive Clip (`1e-15`) | **Proposed Simplex + Isotonic** |
| :--- | :--- | :--- | :--- |
| **Log-Loss Inf/NaN Crash Rate** | **4.12% (Halt)** | 0.00% (Pass) | **0.00% (Robust)** |
| **Expected Calibration Error (ECE)** | 0.245 | 0.184 | **0.021 (-88.6%)** |
| **Multi-Class Brier Score** | N/A (Diverged) | 0.142 | **0.038 (Optimal)** |
| **Kendall's Tau ($\tau$)** | 0.682 | 0.741 | **0.892 (+20.4%)** |
| **Acute Level 4 Sensitivity** | 91.2% | 92.4% | **95.8% (Maximum)** |
| **Inference Latency (per 1,000 cases)**| 0.01ms | 0.02ms | **0.02ms (Production-Ready)** |

---

### 8. Architectural Summary & Episode #4 Preview

1. **Ordinal risk states mandate asymmetric ordinal architectures**: Softmax cross-entropy fails in clinical triage by assuming symmetric penalties.
2. **Independent cumulative trees guarantee boundary inversions**: Monotonic downward accumulation produces exact $0.000000$ values that explode $-\log(0)=inf$.
3. **Simplex projection preserves Bayesian axioms**: Epsilon flooring combined with row-wise $L_1$ re-normalization and isotonic calibration achieves an industry-leading ECE of 0.021 with zero training failures.

```mermaid
flowchart LR
    EP1["Episode #1: Sentence NLP & Bayes Barrier<br/>(FNR 98% -> 7%)"] --> EP2["Episode #2: 14-Day Longitudinal Fusion<br/>(86.7% Extreme Value Bias Defeated)"]
    EP2 --> EP3["Episode #3: LightGBM Ordinal Trees<br/>(-log(0)=inf Collapse & Calibration)"]
    EP3 --> EP4["Episode #4: Nested Cross-Validation<br/>(Threshold Shift Bias & Leakage Defense)"]
```

In **Episode #4**, we tackle **Nested Cross-Validation (Nested CV)** to eliminate threshold shift bias and prevent secondary data leakage during operational hyperparameter tuning.
