---
title: À propos & Global Dev Blog
description: À propos de Jihwan Park (jbjihwan) et Global Dev Blog - Analyses techniques approfondies en IA, Robotique, Vision par Ordinateur et Apprentissage par Renforcement.
keywords: [À propos, Jihwan Park, Ingénieur IA, Robotique, Vision par Ordinateur, Apprentissage par Renforcement, Maeumjigi]
---

# À propos & Global Dev Blog

Bienvenue sur **Global Dev Blog**, un carnet de bord technique et d'ingénierie rédigé par **Jihwan Park (jbjihwan)**.

Ce blog documente des projets pratiques d'ingénierie, des défis de déploiement en production, des compromis d'architecture et des benchmarks empiriques en **Intelligence Artificielle, Robotique, Vision par Ordinateur et Apprentissage par Renforcement**.

---

## 👨‍💻 Qui suis-je

Je suis un ingénieur logiciel en IA et Robotique, passionné par la transformation d'algorithmes théoriques en systèmes robustes et en temps réel sur systèmes embarqués et serveurs cloud. Mes domaines d'expertise couvrent :

- **Systèmes autonomes & Apprentissage par renforcement** : Formulation de processus décisionnels de Markov (MDP), cartographie d'états-actions discrets, ingénierie de récompenses denses et transfert Sim-to-Real.
- **Vision par ordinateur avancée** : Pipelines d'inférence multi-étapes temps réel, détection d'objets (YOLOv3/v5/v8), suivi multi-objets (CSRT, DeepSORT), super-résolution (EDSR) et OCR de plaques d'immatriculation avec vote temporel.
- **Traitement du langage naturel & Sécurité IA** : Fine-tuning efficace des paramètres (PEFT/LoRA) sur architectures Llama, régression ordinale sous déséquilibre de classes extrême et garde-fous déterministes.
- **Ingénierie ML Full-Stack** : Microservices FastAPI à haut débit, conteneurisation, documentation multilingue Docusaurus et applications mobiles React Native.

---

## 📚 Séries phares du blog

### 1. 🧠 Journal de bord Maeumjigi Capstone (23 épisodes)
Développement d'un système IA de détection de détresse psychologique et d'intervention d'urgence :
- Génération de dialogues cliniques synthétiques via pipelines LLM.
- Résolution du sur-apprentissage des étiquettes faibles par régression ordinale.
- Conception de garde-fous déterministes garantissant une intervention en moins d'une milliseconde.

### 2. 🤖 Robot mobile autonome Q-Learning Webots (5 épisodes)
De l'exploration sans connaissances préalables à l'évitement déterministe d'obstacles :
- Discrétisation de 6 secteurs de capteurs de distance en 648 états compacts.
- Façonnement géométrique des récompenses de vitesse et de distance.
- Déploiement de la table Q sur robots différentiels physiques via Arduino Uno.

### 3. 🚗 Vision IA Dashcam ANPR & Franchissement de voies (5 épisodes)
Système embarqué de vision temps réel pour séquences de dashcam sur autoroute :
- Pipeline complet en 6 étapes respectant une contrainte stricte de 30 FPS.
- Ajustement polynomial de trajectoire de voie et calcul d'intrusion géométrique IoU.
- Restauration de plaques floues par super-résolution EDSR et vote majoritaire temporel.
