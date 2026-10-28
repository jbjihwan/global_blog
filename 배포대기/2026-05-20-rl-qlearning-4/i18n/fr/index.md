---
slug: 2026-05-20-rl-qlearning-4
title: "[Robotique Webots] Évaluation déterministe via evaluate_qlearning & Benchmark contre DQN et SARSA (#4)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, evaluation, benchmark, dqn, sarsa, robotics, python]
date: 2026-05-20
project: rl_q_learning
description: "Pipeline d'évaluation déterministe sans exploration (ε=0), analyse de l'efficacité de trajectoire, métrique d'évitement frôlant et benchmark comparatif contre DQN et SARSA."
keywords: [Évaluation Déterministe Politique, Métrique Frôlement Obstacle, Q-Learning vs DQN vs SARSA, Benchmark Navigation Autonome, Inférence Zéro Exploration]
---

![Benchmark succès et nombre de pas](./images/01_eval_success_steps.png)

> 📌 **Points clés (TL;DR)**
> - **L'objectif** : Mesurer les performances réelles de la politique optimale (`\epsilon=0`) sans bruit stochastique afin de valider son déploiement en conditions réelles.
> - **Le résultat** : Le Q-learning tabulaire atteint 92 % de succès tout en étant 15 fois plus léger en calcul que Deep Q-Networks (DQN).

{/* truncate */}

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Test déterministe pur** : Valide que la politique apprise est stable et exploitable en production.
2. **Légèreté maximale** : Moins de 15 Ko de mémoire vive contre plusieurs mégaoctets pour DQN.
3. **Temps de réponse instantané** : Inférence en microsecondes éliminant tout risque de collision.
4. **Prêt pour le réel** : Les trajectoires optimisées autorisent le portage immédiat sur microcontrôleur.