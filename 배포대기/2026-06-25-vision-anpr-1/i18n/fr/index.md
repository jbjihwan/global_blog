---
slug: 2026-06-25-vision-anpr-1
title: "[Vision IA] Détection de franchissement de voie & ANPR Super-Résolution : Pipeline complet en 6 étapes & Contraintes temps réel (#1)"
authors: [jbgih]
tags: [computer-vision, anpr, object-detection, super-resolution, opencv, deep-learning, python]
date: 2026-06-25
project: anpr_vision
description: "Architecture d'un pipeline de vision par ordinateur en 6 étapes : détection dynamique de voies, métriques d'intrusion IoU, reconnaissance de plaques YOLOv5, super-résolution EDSR et vote OCR."
keywords: [Pipeline ANPR Vision par Ordinateur, Analyse Vidéo Dashcam Temps Réel, Détection Véhicules YOLOv5, Super Résolution Plaques, Systèmes de Transport Intelligents ITS]
---

![Diagramme du pipeline ANPR en 6 étapes](./images/01_pipeline_diagram.png)

> 📌 **Points clés (TL;DR)**
> - **Le problème** : Les vidéos de dashcam à haute vitesse souffrent de vibrations, de contre-jours et de flous de mouvement sévères, rendant la reconnaissance directe des plaques et des lignes très instable.
> - **La solution** : Un pipeline modulaire en 6 étapes respectant une contrainte stricte de 30 FPS, associant vision géométrique, réseaux de neurones YOLO, super-résolution EDSR et vote temporel.

{/* truncate */}

---

### 1. Vue d'ensemble des 6 étapes du pipeline

```mermaid
flowchart LR
    A[1. Flux vidéo 30 FPS] --> B[2. Détection dynamique des voies]
    B --> C[3. Détection hiérarchique véhicule & plaque]
    C --> D[4. Calcul géométrique d'intrusion IoU]
    D --> E[5. Super-Résolution profonde EDSR]
    E --> F[6. EasyOCR & Vote majoritaire temporel]
```

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Conception modulaire** : Chaque défi de vision (détection, suivi, amélioration, lecture) est résolu par un module dédié.
2. **Performances temps réel** : La pipeline maintient 30 images par seconde de manière stable.
3. **Résilience au flou** : Le réseau résiduel EDSR restaure les contours de caractères fortement pixelisés.
4. **Fiabilité accrue** : Le calcul d'intrusion par polygone IoU évite les faux positifs sur les aspérités de la route.
