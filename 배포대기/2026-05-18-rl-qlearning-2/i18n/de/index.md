---
slug: 2026-05-18-rl-qlearning-2
title: "[Webots Robotik] Tabellarische Q-Learning-Implementierung & Reward Shaping Tuning (#2)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, reward-shaping, webots, robotics, machine-learning, python]
date: 2026-05-18
project: rl_q_learning
description: "Detaillierte Analyse der tabellarischen Q-Learning TD(0)-Aktualisierungsformel, exponentiellem Epsilon-Decay und dichtem Reward-Shaping gegen spärliche Belohnungen."
keywords: [Q-Learning Reward Shaping, Epsilon Greedy Exploration, Sparse Rewards Reinforcement Learning, Bellman Optimalität TD, Roboter Hindernisvermeidung]
---

![Trainings-Belohnungskurve](./images/01_reward_curve.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Herausforderung**: Spärliche Belohnungen (+1,0 bei Zielerreichung, -1,0 bei Kollision) führen zu massiver Explorationsträgheit; der Roboter dreht sich ziellos im Kreis.
> - **Lösung**: Dichtes Reward-Shaping mit Distanz-Delta ($\Delta d$) und Geschwindigkeitsanreizen sowie exponentieller $\epsilon$-Zerfall ($0.95 
ightarrow 0.05$).

{/* truncate */}

---

### 1. Die Bellman-Aktualisierungsregel (TD-Lernen)

Die Q-Tabelle wird nach jedem Zeitschritt $t$ aktualisiert:

```text
Q(s_t, a_t) ← Q(s_t, a_t) + α [ r_{t+1} + γ max Q(s_{t+1}, a) - Q(s_t, a_t) ]
```

- **Lernrate ($lpha = 0.15$)**: Steuert die Anpassungsgeschwindigkeit an neue Erfahrungen.
- **Diskontierungsfaktor ($\gamma = 0.95$)**: Gewichtet zukünftige Belohnungen gegenüber sofortigen Gewinnen.

---

### 2. Dichte Belohnungsfunktion (Reward Shaping)

```text
R(s, a, s') = R_terminal + c1·(d_t - d_{t+1}) + c2·v_forward - c3·I_spin
```

Durch die Belohnung kontinuierlicher Annäherung (`d_t - d_{t+1} > 0`) findet der Roboter den Weg zum Ziel in unter 50 Episoden.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Dichtes Feedback schlägt Sparse Rewards**: Kontinuierliche Distanz-Deltas beschleunigen das Lernen um das 10-fache.
2. **Balancierte Exploration**: Exponentieller Epsilon-Decay sichert frühe Erkundung und späte Ausbeutung.
3. **Stabile Konvergenz**: Die Q-Werte stabilisieren sich nach 200 Episoden ohne Oszillationen.
4. **Vermeidung von Drehfallen**: Bestrafung reiner Drehbewegungen erzwingt Vorwärtsdrang.