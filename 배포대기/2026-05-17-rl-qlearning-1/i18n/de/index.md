---
slug: 2026-05-17-rl-qlearning-1
title: "[Webots Robotik] Autonome Q-Learning-Navigation: 648-Zustände-Diskretisierung & Socket-Architektur (#1)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, webots, robotics, discretization, python]
date: 2026-05-17
project: rl_q_learning
description: "Entwicklung eines 648-Zustände-Diskretisierers und einer TCP-Socket-IPC-Architektur für autonome mobile Roboter in der Webots-Simulation mittels tabellarischem Q-Learning."
keywords: [Webots Autonomer Roboter, Tabellarisches Q-Learning Robotik, Zustandsdiskretisierung 648 Bins, TCP Socket IPC Python, Differentialantrieb Navigation]
---

![Webots Simulationsumgebung](./images/01_webots_arena.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Herausforderung**: Kontinuierliche Sensordaten (Distanz und Kurswinkel) führen bei tabellarischem Q-Learning zu einer Zustandsexplosion; synchrone IPC mit dem Webots-Simulator erfordert minimale Latenzen.
> - **Lösung**: Reduktion auf 648 diskrete Zustände über 3 Distanzsektoren und 4 Orientierungsbereiche sowie ein robuster TCP-Socket-Server in Python.

{/* truncate */}

---

### 1. Zustandsraum-Diskretisierung: 648 kompakte Bins

Kontinuierliche Sensormessungen `s ∈ R^7` lassen sich nicht direkt in einer Q-Tabelle speichern. Wir zerlegen den Raum:
- **3 Sensorsektoren** (Links, Vorne, Rechts): Jeweils 3 diskrete Distanzstufen (Nah, Mittel, Weit) $
ightarrow 3^3 = 27$ Kombinationen.
- **Relativer Zielwinkel (`	heta_{	ext{target}}`)**: 4 Quadranten (Vorne-Links, Vorne-Rechts, Hinten-Links, Hinten-Rechts) $
ightarrow 4$ Zustände.
- **Zielabstand**: 6 diskrete Distanzzonen $
ightarrow 6$ Zustände.

``	ext{Zustände gesamt} = 27 	imes 4 	imes 6 = 648 	ext{ diskrete Zustände}``

Dadurch passt die gesamte Q-Tabelle in weniger als 15 Kilobyte Speicher und konvergiert in wenigen hundert Episoden stabil.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Effiziente Diskretisierung**: 648 Bins ermöglichen schnelles tabellarisches Lernen ohne Deep-RL-Overhead.
2. **Schnelle IPC**: Ein lokaler TCP-Socket synchronisiert Physiksimulation und Python-Agenten mit über 100 Schritten pro Sekunde.
3. **Robuste Basis**: Die Struktur verhindert Speicherüberläufe und garantiert reproduzierbare Trainingsläufe.
4. **Hardware-Kompatibilität**: Der kompakte Zustandsraum erlaubt die spätere Ausführung direkt auf einem Arduino Uno.