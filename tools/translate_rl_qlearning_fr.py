# -*- coding: utf-8 -*-
import os
import shutil

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")

def save_fr_post(slug, fr_content):
    # 1. Save to Staging
    stage_dir = os.path.join(STAGING_ROOT, slug)
    stage_fr_dir = os.path.join(stage_dir, "i18n", "fr")
    os.makedirs(stage_fr_dir, exist_ok=True)
    with open(os.path.join(stage_fr_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(fr_content.strip() + "\n")
    print(f"[STAGING OK] {slug} -> {stage_fr_dir}\\index.md")

    # 2. Save to i18n/fr production blog dir (ready for build)
    prod_fr_dir = os.path.join(GB_ROOT, "i18n", "fr", "docusaurus-plugin-content-blog", slug)
    os.makedirs(prod_fr_dir, exist_ok=True)
    with open(os.path.join(prod_fr_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(fr_content.strip() + "\n")
    
    # 3. Copy images from blog/<slug>/images
    src_images = os.path.join(GB_ROOT, "blog", slug, "images")
    if os.path.exists(src_images):
        dst_images = os.path.join(prod_fr_dir, "images")
        os.makedirs(dst_images, exist_ok=True)
        for item in os.listdir(src_images):
            s = os.path.join(src_images, item)
            d = os.path.join(dst_images, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
        print(f"[IMAGES OK] Copied images to {dst_images}")

# ==============================================================================
# RL 1 FRENCH
# ==============================================================================
r1_slug = "2026-05-17-rl-qlearning-1"
r1_content = """---
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
"""

# ==============================================================================
# RL 2 FRENCH
# ==============================================================================
r2_slug = "2026-05-18-rl-qlearning-2"
r2_content = """---
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
"""

# ==============================================================================
# RL 3 FRENCH
# ==============================================================================
r3_slug = "2026-05-19-rl-qlearning-3"
r3_content = """---
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
"""

# ==============================================================================
# RL 4 FRENCH
# ==============================================================================
r4_slug = "2026-05-20-rl-qlearning-4"
r4_content = """---
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
> - **L'objectif** : Mesurer les performances réelles de la politique optimale ($\epsilon=0$) sans bruit stochastique afin de valider son déploiement en conditions réelles.
> - **Le résultat** : Le Q-learning tabulaire atteint 92 % de succès tout en étant 15 fois plus léger en calcul que Deep Q-Networks (DQN).

{/* truncate */}

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Test déterministe pur** : Valide que la politique apprise est stable et exploitable en production.
2. **Légèreté maximale** : Moins de 15 Ko de mémoire vive contre plusieurs mégaoctets pour DQN.
3. **Temps de réponse instantané** : Inférence en microsecondes éliminant tout risque de collision.
4. **Prêt pour le réel** : Les trajectoires optimisées autorisent le portage immédiat sur microcontrôleur.
"""

# ==============================================================================
# RL 5 FRENCH
# ==============================================================================
r5_slug = "2026-05-21-rl-qlearning-5"
r5_content = """---
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
"""

# Execute French Section 4
if __name__ == "__main__":
    print("=" * 60)
    print("Translating Section 4 (RL Q-Learning, 5 posts) into French...")
    print("=" * 60)
    save_fr_post(r1_slug, r1_content)
    save_fr_post(r2_slug, r2_content)
    save_fr_post(r3_slug, r3_content)
    save_fr_post(r4_slug, r4_content)
    save_fr_post(r5_slug, r5_content)
    print("\n[FRENCH SECTION 4 COMPLETE] All 5 RL Q-Learning posts staged and saved in French!")
