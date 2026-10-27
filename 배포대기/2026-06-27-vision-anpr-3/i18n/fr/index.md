---
slug: 2026-06-27-vision-anpr-3
title: "[Vision IA] Détection d'objets hiérarchique : ROI véhicule YOLOv3, Détecteur de plaque YOLOv5 & Suivi CSRT (#3)"
authors: [jbgih]
tags: [computer-vision, anpr, yolo, csrt-tracker, object-detection, opencv, python]
date: 2026-06-27
project: anpr_vision
description: "Localisation hiérarchique en deux étapes : détection large du véhicule par YOLOv3, détection ciblée de la plaque par YOLOv5 et suivi haute vitesse par filtre CSRT à 50 FPS."
keywords: [Détection Plaque Minéralogique YOLOv5, Suivi CSRT OpenCV, Détection d'Objets Hiérarchique, Suivi Véhicule Temps Réel, Localisation ROI Véhicule]
---

![Localisation de détection de plaque YOLOv5](./images/01_plate_localization.png)

> 📌 **Points clés (TL;DR)**
> - **Le problème** : Scanner directement une image 1080p complète pour y trouver une plaque de 30x15 pixels génère de faux positifs et fait chuter le débit sous 10 FPS.
> - **La solution** : Hiérarchie en 2 étapes — Détecter d'abord le véhicule (YOLOv3), puis localiser la plaque uniquement dans la zone du pare-chocs (YOLOv5), avec suivi CSRT sur les images intermédiaires.

{/* truncate */}

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Entonnoir hiérarchique** : Supprime les fausses détections sur les panneaux routiers.
2. **Gain de vitesse x5** : Le suivi CSRT allège la charge d'inférence GPU en espaçant les appels à YOLOv5.
3. **Suivi stable** : Maintient le verrouillage sur la plaque même lors des secousses du véhicule.
4. **Isolation optimale** : Transmet une vignette parfaitement cadrée au module de super-résolution.