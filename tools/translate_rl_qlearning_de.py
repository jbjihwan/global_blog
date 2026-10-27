# -*- coding: utf-8 -*-
import os
import shutil

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")

def save_de_post(slug, de_content):
    # 1. Save to Staging
    stage_dir = os.path.join(STAGING_ROOT, slug)
    stage_de_dir = os.path.join(stage_dir, "i18n", "de")
    os.makedirs(stage_de_dir, exist_ok=True)
    with open(os.path.join(stage_de_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(de_content.strip() + "\n")
    print(f"[STAGING OK] {slug} -> {stage_de_dir}\\index.md")

    # 2. Save to i18n/de production blog dir (ready for build)
    prod_de_dir = os.path.join(GB_ROOT, "i18n", "de", "docusaurus-plugin-content-blog", slug)
    os.makedirs(prod_de_dir, exist_ok=True)
    with open(os.path.join(prod_de_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(de_content.strip() + "\n")
    
    # 3. Copy images from blog/<slug>/images
    src_images = os.path.join(GB_ROOT, "blog", slug, "images")
    if os.path.exists(src_images):
        dst_images = os.path.join(prod_de_dir, "images")
        os.makedirs(dst_images, exist_ok=True)
        for item in os.listdir(src_images):
            s = os.path.join(src_images, item)
            d = os.path.join(dst_images, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
        print(f"[IMAGES OK] Copied images to {dst_images}")

# ==============================================================================
# RL 1 GERMAN
# ==============================================================================
r1_slug = "2026-05-17-rl-qlearning-1"
r1_content = """---
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

Kontinuierliche Sensormessungen $\mathbf{s} \in \mathbb{R}^7$ lassen sich nicht direkt in einer Q-Tabelle speichern. Wir zerlegen den Raum:
- **3 Sensorsektoren** (Links, Vorne, Rechts): Jeweils 3 diskrete Distanzstufen (Nah, Mittel, Weit) $\rightarrow 3^3 = 27$ Kombinationen.
- **Relativer Zielwinkel ($\theta_{\text{target}}$)**: 4 Quadranten (Vorne-Links, Vorne-Rechts, Hinten-Links, Hinten-Rechts) $\rightarrow 4$ Zustände.
- **Zielabstand**: 6 diskrete Distanzzonen $\rightarrow 6$ Zustände.

$$\text{Zustände gesamt} = 27 \times 4 \times 6 = 648 \text{ diskrete Zustände}$$

Dadurch passt die gesamte Q-Tabelle in weniger als 15 Kilobyte Speicher und konvergiert in wenigen hundert Episoden stabil.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Effiziente Diskretisierung**: 648 Bins ermöglichen schnelles tabellarisches Lernen ohne Deep-RL-Overhead.
2. **Schnelle IPC**: Ein lokaler TCP-Socket synchronisiert Physiksimulation und Python-Agenten mit über 100 Schritten pro Sekunde.
3. **Robuste Basis**: Die Struktur verhindert Speicherüberläufe und garantiert reproduzierbare Trainingsläufe.
4. **Hardware-Kompatibilität**: Der kompakte Zustandsraum erlaubt die spätere Ausführung direkt auf einem Arduino Uno.
"""

# ==============================================================================
# RL 2 GERMAN
# ==============================================================================
r2_slug = "2026-05-18-rl-qlearning-2"
r2_content = """---
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
> - **Lösung**: Dichtes Reward-Shaping mit Distanz-Delta ($\Delta d$) und Geschwindigkeitsanreizen sowie exponentieller $\epsilon$-Zerfall ($0.95 \rightarrow 0.05$).

{/* truncate */}

---

### 1. Die Bellman-Aktualisierungsregel (TD-Lernen)

Die Q-Tabelle wird nach jedem Zeitschritt $t$ aktualisiert:

$$Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[ r_{t+1} + \gamma \max_{a} Q(s_{t+1}, a) - Q(s_t, a_t) \right]$$

- **Lernrate ($\alpha = 0.15$)**: Steuert die Anpassungsgeschwindigkeit an neue Erfahrungen.
- **Diskontierungsfaktor ($\gamma = 0.95$)**: Gewichtet zukünftige Belohnungen gegenüber sofortigen Gewinnen.

---

### 2. Dichte Belohnungsfunktion (Reward Shaping)

$$R(s, a, s') = R_{\text{terminal}} + c_1 \cdot (d_t - d_{t+1}) + c_2 \cdot v_{\text{forward}} - c_3 \cdot \mathbb{I}_{\text{spin}}$$

Durch die Belohnung kontinuierlicher Annäherung ($d_t - d_{t+1} > 0$) findet der Roboter den Weg zum Ziel in unter 50 Episoden.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Dichtes Feedback schlägt Sparse Rewards**: Kontinuierliche Distanz-Deltas beschleunigen das Lernen um das 10-fache.
2. **Balancierte Exploration**: Exponentieller Epsilon-Decay sichert frühe Erkundung und späte Ausbeutung.
3. **Stabile Konvergenz**: Die Q-Werte stabilisieren sich nach 200 Episoden ohne Oszillationen.
4. **Vermeidung von Drehfallen**: Bestrafung reiner Drehbewegungen erzwingt Vorwärtsdrang.
"""

# ==============================================================================
# RL 3 GERMAN
# ==============================================================================
r3_slug = "2026-05-19-rl-qlearning-3"
r3_content = """---
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

Die Lösung besteht in einem **dynamischen Repulsionsfeld**: Befindet sich der Frontsensor im Gefahrenbereich ($d_{\text{front}} < 0.2\,\text{m}$), überwiegt die Kollisionsstrafe jede Distanzannäherung.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Repulsions-Gewichtung**: Verhindert frontales Festfahren an Wänden trotz Zielanzeige dahinter.
2. **Headless-Beschleunigung**: Deaktivierte GUI beschleunigt das Training um den Faktor 8.
3. **Multi-Seed-Robustheit**: Tests über 10 verschiedene Seeds garantieren reproduzierbare Navigationspfade.
4. **Erfolgsquote über 90 %**: Der Roboter meistert selbst U-förmige Fallen zuverlässig.
"""

# ==============================================================================
# RL 4 GERMAN
# ==============================================================================
r4_slug = "2026-05-20-rl-qlearning-4"
r4_content = """---
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
> - **Ziel**: Messung der reinen, deterministischen Leistungsfähigkeit der gelernten Greedy-Policy ($\epsilon = 0$) ohne stochastisches Rauschen zur Validierung der Praxistauglichkeit.
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
1. **Deterministischer Test ($\epsilon=0$)**: Belegt die Stabilität der Policy ohne Zufallsentscheidungen.
2. **Kompaktheit gewinnt**: < 15 KB Speicherbedarf macht tabellarisches Q-Learning ideal für Mikrocontroller.
3. **Geringe Latenz**: Sub-Millisekunden-Reaktionszeiten verhindern Kollisionen bei höheren Fahrgeschwindigkeiten.
4. **Bereit für Hardware**: Die deterministische Policy erfüllt alle Kriterien für den physischen Transfer.
"""

# ==============================================================================
# RL 5 GERMAN
# ==============================================================================
r5_slug = "2026-05-21-rl-qlearning-5"
r5_content = """---
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
"""

# Execute Section 4
if __name__ == "__main__":
    print("=" * 60)
    print("Translating Section 4 (RL Q-Learning, 5 posts) into German...")
    print("=" * 60)
    save_de_post(r1_slug, r1_content)
    save_de_post(r2_slug, r2_content)
    save_de_post(r3_slug, r3_content)
    save_de_post(r4_slug, r4_content)
    save_de_post(r5_slug, r5_content)
    print("\n[SECTION 4 COMPLETE] All 5 RL Q-Learning posts staged and saved in German!")
