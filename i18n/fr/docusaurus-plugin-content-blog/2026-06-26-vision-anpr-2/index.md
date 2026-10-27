---
slug: 2026-06-26-vision-anpr-2
title: "[Vision IA] Extraction dynamique des lignes de voie & Critère géométrique d'intrusion par IoU (#2)"
authors: [jbgih]
tags: [computer-vision, anpr, lane-detection, hough-transform, iou, opencv, python]
date: 2026-06-26
project: anpr_vision
description: "Filtrage des contours par Canny, transformée de Hough probabiliste (HoughLinesP), seuils de pente et calcul d'intrusion géométrique par polygone IoU."
keywords: [Détection de Voies OpenCV, Suivi de Lignes HoughLinesP, Détection Franchissement Ligne, Calcul IoU Polygone, Détection de Contours Canny]
---

![Overlay de détection dynamique de voie](./images/01_lane_detection.png)

> 📌 **Points clés (TL;DR)**
> - **Le problème** : Les reflets sur route mouillée et les ombres créent des lignes parasites ; une simple vérification de coordonnées X déclenche des alertes erronées.
> - **La solution** : Filtrage strict par pentes de droites et calcul du chevauchement de surface (IoU > 0,15) entre le polygone du véhicule et le tracé de la voie.

{/* truncate */}

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Filtrage géométrique rigoureux** : Les seuils de pente éliminent 95 % des lignes parasites causées par les ombres.
2. **Critère d'intrusion IoU** : L'intersection de polygones élimine les fausses alertes dans les virages.
3. **Exécution ultrarapide** : Le traitement Hough sur zone d'intérêt requiert moins de 3 millisecondes par image.
4. **Déclenchement déterministe** : Le franchissement avéré active immédiatement la lecture de plaque en haute résolution.
