---
slug: 2026-05-21-rl-qlearning-5
title: "[Robótica Webots] Sim-to-Real: Transferência para Hardware com Arduino Uno, Bluetooth HC-06 & Rastreamento ArUco (#5)"
authors: [jbgih]
tags: [reinforcement-learning, sim-to-real, arduino, robotics, computer-vision, aruco, python]
date: 2026-05-21
project: rl_q_learning
description: "Implantação da política de 648 estados treinada em simulação em um robô físico Arduino Uno, com homografia de câmera zenital e rastreamento de pose 6-DoF com marcadores ArUco."
keywords: [Sim-to-Real Hardware Transfer, ArUco Marker Pose Tracking, Arduino Uno Roboter Navigation, HC-06 Bluetooth IPC, Webots Simulation zu Realität]
---

![Rastreamento Visual com Marcadores ArUco](./images/01_aruco_vision.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Limitações severas de hardware (Arduino Uno com apenas 2 KB de SRAM), deslizamento não linear das rodas e o clássico abismo da realidade (**Reality Gap**) entre simulação e ambiente físico.
> - **Solução**: Desacoplamento da visão computacional para um PC Host através de câmera superior com homografia e transmissão sem fio de comandos compactos via Bluetooth HC-06.

{/* truncate */}

---

### 1. A Arquitetura Sim-to-Real

```mermaid
flowchart TD
    Cam[Câmera Superior 1080p] --> ArUco[Rastreamento de Pose ArUco 6-DoF OpenCV]
    ArUco --> Homography[Transformação Homográfica para Coordenadas 2D da Arena]
    Homography --> Host[PC Host: Discretização em 648 Bins & Consulta na Tabela Q]
    Host -->|Comando Serial Bluetooth HC-06| Arduino[Arduino Uno: Controlador PWM Dual Motor]
    Arduino --> Motors[Motores Físicos com Caixa de Redução Esquerda/Direita]
```

Graças ao sistema de rastreamento visual externo, o robô móvel não precisa carregar sensores LiDAR pesados. O microcontrolador Arduino Uno processa comandos de apenas 2 bytes e controla a ponte H de potência com precisão milimétrica.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Transposição Bem-Sucedida**: A política treinada no Webots guiou o robô real sem necessidade de novo treinamento físico.
2. **Rastreamento ArUco Confiável**: Entrega telemetria em alta frequência a 60 FPS com precisão milimétrica.
3. **Hardware Minimalista**: Um microcontrolador simples de 8 bits foi suficiente para condução autônoma sofisticada.
4. **Ciclo Completo de Engenharia**: Do design do MDP matemático à validação em hardware físico, todo o ciclo foi comprovado.