---
slug: 2026-06-29-vision-anpr-5
title: "[Vision IA] Moteur OCR de plaques, Normalisation Regex & Vote majoritaire temporel (Évolution de v01 à v11) (#5)"
authors: [jbgih]
tags: [computer-vision, anpr, easyocr, regex, voting-ensemble, python]
date: 2026-06-29
project: anpr_vision
description: "Validation syntaxique des plaques par regex, optimisation d'EasyOCR, vote majoritaire sur fenêtre glissante temporelle et retour d'expérience sur 11 itérations de v01 à v11."
keywords: [EasyOCR Plaque Immatriculation, Ensemble Vote Majoritaire ANPR, Normalisation Regex Plaque, Précision Reconnaissance OCR, Systèmes Transport Intelligents]
---

![Vote majoritaire temporel et confirmation finale](./images/01_voting_evolution.png)

> 📌 **Points clés (TL;DR)**
> - **Le problème** : L'OCR sur une seule image subit inévitablement des confusions ponctuelles (ex. `6` confondu avec `8`) dues aux vibrations et aux reflets.
> - **La solution** : Filtrage grammatical strict par expressions régulières (Regex) associé à un vote majoritaire sur une fenêtre glissante de 11 images consécutives.

{/* truncate */}

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Le consensus élimine l'erreur** : Le vote majoritaire sur 11 images filtre les anomalies passagères.
2. **Garde-fous Regex** : Corrige immédiatement les confusions classiques (chiffres/lettres) selon la grammaire officielle des plaques.
3. **Taux de succès de 96 %** : Évolution progressive sur 11 versions pour atteindre une précision de niveau industriel.
4. **Pipeline complet opérationnel** : Une solution robuste de bout en bout pour la surveillance du trafic.