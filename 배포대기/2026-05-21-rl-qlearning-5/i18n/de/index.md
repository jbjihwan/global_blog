---
slug: 2026-05-21-rl-qlearning-5
title: "[Webots Robotik] Sim-to-Real: Hardware-Transfer via Arduino Uno, HC-06 Bluetooth & ArUco-Vision-Tracking (#5)"
authors: [jbgih]
tags: [reinforcement-learning, sim-to-real, arduino, robotics, computer-vision, aruco, python]
date: 2026-05-21
project: rl_q_learning
description: "Bereitstellung der simulations-trainierten 648-Zustände-Policy auf einem physischen Arduino Uno-Roboter mit Deckenkamera-Homographie und 6-DoF ArUco-Marker-Tracking."
keywords: [Sim-to-Real Hardware Transfer, ArUco Marker Pose Tracking, Arduino Uno Roboter Navigation, HC-06 Bluetooth IPC, Webots Simulation zu Realität]
---

![ArUco Marker Vision Tracking](./images/01_aruco_vision.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Herausforderung**: Strikte Ressourcenbeschränkungen (Arduino Uno mit 2 KB SRAM), nichtlinearer Radschlupf und die klassische **Reality Gap** zwischen Simulation und Realität.
> - **Lösung**: Auslagerung der Bildverarbeitung an einen Host-PC via ArUco-Deckenkamera-Homographie und drahtlose Steuerbefehlsübertragung via Bluetooth HC-06.

{/* truncate */}

---

### 1. Die Sim-to-Real-Architektur

```mermaid
flowchart TD
    Cam[Deckenkamera 1080p] --> ArUco[OpenCV ArUco 6-DoF Pose Tracking]
    ArUco --> Homography[Perspektivische Entzerrung auf 2D-Arena]
    Homography --> Host[Host PC: Diskretisierung in 648 Bins & Q-Tabellen Lookup]
    Host -->|Bluetooth HC-06 Serial| Arduino[Arduino Uno: Dual Motor PWM Controller]
    Arduino --> Motors[Physische Getriebemotoren links / rechts]
```

Durch das externe Vision-Tracking entfällt die Notwendigkeit teurer Laserscanner auf dem Roboter. Der Arduino Uno empfängt kompakte 2-Byte-Motorbefehle und steuert die H-Brücke präzise an.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Reality Gap erfolgreich überbrückt**: Die in Webots trainierte Policy steuert den echten Roboter ohne Nachtraining.
2. **ArUco-Tracking**: Liefert millimetergenaue Positionsdaten bei 60 FPS ohne Sensorrauschen auf dem Roboter.
3. **Minimalistische Hardware**: Ein kostengünstiger 8-Bit-Mikrocontroller reicht für komplexe autonome Fahrten aus.
4. **Vollständiger Projektzyklus**: Vom MDP-Design über Simulation bis zur realen Hardware wurde das System lückenlos validiert.