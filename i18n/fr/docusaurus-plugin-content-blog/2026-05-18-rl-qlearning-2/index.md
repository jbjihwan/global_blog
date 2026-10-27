---
slug: 2026-05-18-rl-qlearning-2
title: "[Robotique Webots] Implémentation du Q-Learning tabulaire & Façonnement de récompenses denses (#2)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, reward-shaping, webots, robotics, machine-learning, python]
date: 2026-05-18
project: rl_q_learning
description: "Formulation mathématique de la mise à jour TD(0), décroissance exponentielle d'exploration epsilon-decay et reward shaping dense pour guider le robot mobile."
keywords: [Reward Shaping Q-Learning, Exploration Epsilon Greedy, Récompenses Éparses Apprentissage Renforcement, Équation de Bellman TD, Évitement Obstacles Robotique]
---

![Courbe de récompense d'entraînement](./images/01_reward_curve.png)

> 📌 **Points clés (TL;DR)**
> - **Le problème** : Des récompenses trop éparses (+1 à la cible, -1 en collision) provoquent une errance stérile du robot pendant des milliers d'épisodes.
> - **La solution** : Façonnement de récompense dense par variation de distance géométrique ($\Delta d$) et pénalisation des rotations sur place.

{/* truncate */}

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **La densité accélère l'apprentissage** : Les gradients de distance continus divisent le temps d'entraînement par 10.
2. **Exploration équilibrée** : La décroissance d'epsilon garantit la découverte précoce puis la consolidation.
3. **Convergence solide** : Les valeurs Q se stabilisent dès 200 épisodes sans divergence.
4. **Cap vers l'avant** : La pénalité de rotation empêche le robot de tourner en boucle indéfiniment.
