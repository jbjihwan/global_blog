---
slug: 2026-05-17-rl-qlearning-1
title: "[Robotique Webots] Navigation autonome par Q-Learning : Discrétisation en 648 états & Architecture socket (#1)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, webots, robotics, discretization, python]
date: 2026-05-17
project: rl_q_learning
description: "Conception d'un discrétiseur d'espace d'états en 648 cases et d'une architecture IPC par socket TCP pour la navigation d'un robot mobile Webots par Q-Learning tabulaire."
keywords: [Robot Autonome Webots, Q-Learning Tabulaire Robotique, Discrétisation d'États 648 Bins, Socket TCP IPC Python, Navigation Robot Différentiel]
---

![Environnement de simulation Webots](./images/01_webots_arena.png)

> 📌 **Points clés (TL;DR)**
> - **Le problème** : Des données de capteurs continues créent une explosion combinatoire d'états pour le Q-learning tabulaire ; la communication synchrone avec Webots exige une latence minime.
> - **La solution** : Discrétisation compacte en 648 états (3 secteurs de distance, 4 quadrants de cap et 6 zones d'éloignement) et liaison par socket TCP local.

{/* truncate */}

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Discrétisation ultra-compacte** : 648 états permettent un apprentissage rapide sans la lourdeur du Deep RL.
2. **IPC haute fréquence** : Le socket TCP synchronise la physique et l'agent à plus de 100 pas par seconde.
3. **Stabilité mathématique** : Convergence complète obtenue en quelques centaines d'épisodes.
4. **Portabilité embarquée** : La table Q tient en moins de 15 Ko, facilitant son déploiement sur Arduino Uno.
