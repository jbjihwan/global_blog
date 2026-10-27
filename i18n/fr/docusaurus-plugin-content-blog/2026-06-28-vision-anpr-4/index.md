---
slug: 2026-06-28-vision-anpr-4
title: "[Vision IA] Surmonter le flou des vidéos de dashcam : Super-Résolution profonde (EDSR vs FSRCNN) & Empilement multi-images (#4)"
authors: [jbgih]
tags: [computer-vision, super-resolution, edsr, image-stacking, anpr, deep-learning, python]
date: 2026-06-28
project: anpr_vision
description: "Reconstruction des vignettes de plaques basse résolution par super-résolution profonde EDSR 4x et empilement temporel multi-images."
keywords: [Super Résolution EDSR, Défloutage Image Plaque, OpenCV dnn_superres, Empilement Multi-Images, Réseaux Résiduels Profonds]
---

![Résultats de Super-Résolution profonde EDSR](./images/01_edsr_sr_comparison.png)

> 📌 **Points clés (TL;DR)**
> - **Le problème** : Les plaques découpées mesurent souvent moins de 40x20 pixels avec une forte pixellisation de compression H.264 ; l'interpolation bicubique rend les caractères illisibles.
> - **La solution** : Restauration des contours de caractères par un réseau de neurones résiduel EDSR (facteur 4x) combiné à un moyennage temporel multi-images.

{/* truncate */}

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Échec de l'interpolation classique** : Les méthodes bicubiques floutent les caractères et trompent l'OCR.
2. **Puissance d'EDSR 4x** : Le réseau résiduel reconstruit la finesse des arêtes des lettres et chiffres.
3. **Réduction de bruit par empilement** : La combinaison de plusieurs images consécutives élimine le bruit du capteur.
4. **Bond de reconnaissance** : Fait passer le taux de succès de l'OCR de 42 % à plus de 89 %.
