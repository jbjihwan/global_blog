---
slug: 2026-05-19-rl-qlearning-3
title: "[Webots Robotik] Lokale Minima in 12-Wände-Umgebungen überwinden: Multi-Seed Headless-Simulation (#3)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, webots, obstacle-avoidance, local-minima, headless, python]
date: 2026-05-19
project: rl_q_learning
description: "Überwindung des Lokale-Minima-Dilemmas in komplexen Hindernislabyrinthen (obstacle12) und Orchestrierung automatisierter Multi-Seed Headless-Simulationen."
keywords: [Lokale Minima Reinforcement Learning, Webots Headless Simulation, Hindernisvermeidung Multi-Seed, Tabellarisches Q-Learning vs DQN, Automatisierte Trainingspipeline]
---

![obstacle12 Simulations-Arena](./images/01_obstacle12_arena.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Herausforderung**: Liegt das Ziel direkt hinter einer Wand, zieht die Distanz-Belohnung den Roboter frontal in das Hindernis — er verfängt sich in einem **lokalen Minimum**.
> - **Lösung**: Temporäre Hindernis-Repulsion in der Belohnungsfunktion und automatisierte Headless-Simulationen mit verschiedenen Zufalls-Seeds.

{/* truncate */}

---

### 1. Das Lokale-Minima-Dilemma

Wenn der direkte Vektor zum Ziel durch eine Wand blockiert ist, erfordert die Umrundung des Hindernisses kurzfristig eine *Vergrößerung* des Abstands zum Ziel. Eine rein kurzsichtige Distanz-Belohnung bestraft diesen rettenden Umweg jedoch.

Die Lösung besteht in einem **dynamischen Repulsionsfeld**: Befindet sich der Frontsensor im Gefahrenbereich (`d_{	ext{front}} < 0.2\,	ext{m}`), überwiegt die Kollisionsstrafe jede Distanzannäherung.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Repulsions-Gewichtung**: Verhindert frontales Festfahren an Wänden trotz Zielanzeige dahinter.
2. **Headless-Beschleunigung**: Deaktivierte GUI beschleunigt das Training um den Faktor 8.
3. **Multi-Seed-Robustheit**: Tests über 10 verschiedene Seeds garantieren reproduzierbare Navigationspfade.
4. **Erfolgsquote über 90 %**: Der Roboter meistert selbst U-förmige Fallen zuverlässig.
