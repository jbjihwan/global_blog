---
slug: 2026-05-19-rl-qlearning-3
title: "[Robotique Webots] Vaincre les minima locaux face à 12 murs : Simulation headless multi-graines (#3)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, webots, obstacle-avoidance, local-minima, headless, python]
date: 2026-05-19
project: rl_q_learning
description: "Résolution du piège des minima locaux dans des environnements d'obstacles complexes et entraînement automatisé sans interface graphique (headless) sous plusieurs graines aléatoires."
keywords: [Minima Locaux Apprentissage Renforcement, Simulation Headless Webots, Évitement Obstacles Multi-Graines, Q-Learning Tabulaire vs DQN, Pipeline Entraînement Automatisé]
---

![Arène de simulation obstacle12](./images/01_obstacle12_arena.png)

> 📌 **Points clés (TL;DR)**
> - **Le problème** : Quand la cible se trouve derrière un mur, la seule récompense de proximité attire le robot dans une impasse frontale : un **minimum local**.
> - **La solution** : Champ de répulsion d'obstacle prioritaire et accélération par simulation headless sans rendu graphique.

{/* truncate */}

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Répulsion dynamique** : Empêche le robot de percuter les obstacles même si la cible est droit devant.
2. **Gain de vitesse x8** : L'exécution headless réduit drastiquement les temps de calcul.
3. **Robustesse multi-graines** : Validation sur 10 graines aléatoires pour garantir l'absence de biais.
4. **Taux de succès de 90 %** : Capable de contourner des chicanes en U complexes.
