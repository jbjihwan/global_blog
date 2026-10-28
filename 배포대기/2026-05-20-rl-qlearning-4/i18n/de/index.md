---
slug: 2026-05-20-rl-qlearning-4
title: "[Webots Robotik] Deterministische Evaluation via evaluate_qlearning & Benchmark gegen DQN und SARSA (#4)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, evaluation, benchmark, dqn, sarsa, robotics, python]
date: 2026-05-20
project: rl_q_learning
description: "Deterministische Evaluation ohne Exploration (ε=0) mittels evaluate_qlearning.py, Analyse von Pfadeffizienz, Near-Miss-Metriken und Benchmark gegen DQN und SARSA."
keywords: [Deterministische Policy Evaluation, Near-Miss Hindernismetrik, Q-Learning vs DQN vs SARSA, Autonome Navigation Benchmark, Zero Exploration Inferenz]
---

![Erfolgs- und Schritt-Benchmark](./images/01_eval_success_steps.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Ziel**: Messung der reinen, deterministischen Leistungsfähigkeit der gelernten Greedy-Policy (`\epsilon = 0`) ohne stochastisches Rauschen zur Validierung der Praxistauglichkeit.
> - **Ergebnis**: Tabellarisches Q-Learning erreicht 92 % Erfolgsquote bei 15-fach geringerem Rechenaufwand im Vergleich zu Deep Q-Networks (DQN).

{/* truncate */}

---

### 1. Der Algorithmen-Benchmark im Vergleich

| Algorithmus | Erfolgsquote (%) | Ø Schritte zum Ziel | Near-Miss-Ereignisse | Speicherbedarf |
| :--- | :--- | :--- | :--- | :--- |
| **Tabular Q-Learning (Unser)** | **92.0 %** | **48.2** | **1.2** | **< 15 KB** |
| **SARSA (On-Policy)** | 84.0 % | 56.4 | 0.8 | < 15 KB |
| **Deep Q-Network (DQN)** | 88.5 % | 52.1 | 2.1 | ~ 12 MB (PyTorch) |

Tabellarisches Q-Learning erweist sich für strukturierte Navigationsaufgaben als extrem energieeffizient und robust gegenüber Überanpassung.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Deterministischer Test (`\epsilon=0`)**: Belegt die Stabilität der Policy ohne Zufallsentscheidungen.
2. **Kompaktheit gewinnt**: < 15 KB Speicherbedarf macht tabellarisches Q-Learning ideal für Mikrocontroller.
3. **Geringe Latenz**: Sub-Millisekunden-Reaktionszeiten verhindern Kollisionen bei höheren Fahrgeschwindigkeiten.
4. **Bereit für Hardware**: Die deterministische Policy erfüllt alle Kriterien für den physischen Transfer.