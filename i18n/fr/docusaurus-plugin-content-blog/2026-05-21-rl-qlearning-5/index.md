---
slug: 2026-05-21-rl-qlearning-5
title: "[Robotique Webots] Sim-to-Real : Transfert matériel sur Arduino Uno, Bluetooth HC-06 & Vision par marqueurs ArUco (#5)"
authors: [jbgih]
tags: [reinforcement-learning, sim-to-real, arduino, robotics, computer-vision, aruco, python]
date: 2026-05-21
project: rl_q_learning
description: "Déploiement de la politique issue de la simulation sur un robot physique Arduino Uno à 2 roues motrices avec suivi de pose 6-DoF par caméra zénithale et marqueurs ArUco."
keywords: [Transfert Matériel Sim-to-Real, Suivi de Pose Marqueur ArUco, Navigation Robot Arduino Uno, Liaison Bluetooth HC-06, Réduction Écart Réalité Simulation]
---

![Suivi de pose par vision marqueur ArUco](./images/01_aruco_vision.png)

> 📌 **Points clés (TL;DR)**
> - **Le problème** : Contraintes sévères sur microcontrôleur (Arduino Uno avec 2 Ko de SRAM), glissement des roues et **Reality Gap** entre simulateur et monde réel.
> - **La solution** : Calcul de pose par vision externe au plafond (ArUco 6-DoF à 60 FPS) et transmission des commandes moteur en Bluetooth série HC-06.

{/* truncate */}

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Écart de réalité comblé** : La politique entraînée en virtuel pilote le robot réel sans nouvel apprentissage.
2. **Vision zénithale ArUco** : Précision millimétrique sans surcharger le robot de capteurs lourds.
3. **Simplicité matérielle** : Un microcontrôleur 8 bits économique suffit pour exécuter la navigation.
4. **Aboutissement du projet** : Chaîne complète validée, de la théorie mathématique à la démonstration physique.