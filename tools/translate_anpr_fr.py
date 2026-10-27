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
# ANPR 1 FRENCH
# ==============================================================================
a1_slug = "2026-06-25-vision-anpr-1"
a1_content = """---
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
"""

# ==============================================================================
# ANPR 2 FRENCH
# ==============================================================================
a2_slug = "2026-06-26-vision-anpr-2"
a2_content = """---
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
"""

# ==============================================================================
# ANPR 3 FRENCH
# ==============================================================================
a3_slug = "2026-06-27-vision-anpr-3"
a3_content = """---
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
"""

# ==============================================================================
# ANPR 4 FRENCH
# ==============================================================================
a4_slug = "2026-06-28-vision-anpr-4"
a4_content = """---
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
"""

# ==============================================================================
# ANPR 5 FRENCH
# ==============================================================================
a5_slug = "2026-06-29-vision-anpr-5"
a5_content = """---
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
"""

# Execute French Section 3
if __name__ == "__main__":
    print("=" * 60)
    print("Translating Section 3 (Vision ANPR, 5 posts) into French...")
    print("=" * 60)
    save_fr_post(a1_slug, a1_content)
    save_fr_post(a2_slug, a2_content)
    save_fr_post(a3_slug, a3_content)
    save_fr_post(a4_slug, a4_content)
    save_fr_post(a5_slug, a5_content)
    print("\n[FRENCH SECTION 3 COMPLETE] All 5 Vision ANPR posts staged and saved in French!")
