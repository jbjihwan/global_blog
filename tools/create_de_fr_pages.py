# -*- coding: utf-8 -*-
import os

base_dir = r"D:\ai\antigravity\global_blog"

de_pages_dir = os.path.join(base_dir, "i18n", "de", "docusaurus-plugin-content-pages")
fr_pages_dir = os.path.join(base_dir, "i18n", "fr", "docusaurus-plugin-content-pages")

os.makedirs(de_pages_dir, exist_ok=True)
os.makedirs(fr_pages_dir, exist_ok=True)

# 1. German about.md
de_about = """---
title: Über mich & Global Dev Blog
description: Über Jihwan Park (jbjihwan) und Global Dev Blog - Technische Deep Dives in KI, Robotik, Computer Vision und Reinforcement Learning.
keywords: [Über mich, Jihwan Park, KI-Ingenieur, Robotik, Computer Vision, Reinforcement Learning, Maeumjigi]
---

# Über mich & Global Dev Blog

Willkommen beim **Global Dev Blog**, einem technischen Entwickler- und Forschungstagebuch von **Jihwan Park (jbjihwan)**.

Dieser Blog dokumentiert praktische Implementierungen, reale Herausforderungen bei der Produktionsbereitstellung, Architektur-Trade-offs und empirische Benchmarks in den Bereichen **Künstliche Intelligenz, Robotik, Deep Computer Vision und Reinforcement Learning**.

---

## 👨‍💻 Wer ich bin

Ich bin ein KI- und Robotik-Software-Ingenieur, der theoretische Algorithmen in robuste Echtzeitsysteme auf Edge-Geräten und Cloud-Servern überführt. Meine Schwerpunkte umfassen:

- **Autonome Systeme & Reinforcement Learning**: Formulierung von Markov-Entscheidungsprozessen (MDP), kontinuierlich-zu-diskreten Zustands-Aktions-Mappings, dichtes Reward-Shaping und Sim-to-Real-Hardwaretransfer.
- **Deep Computer Vision**: Echtzeit-Mehrstufen-Inferenzpipelines, Objekterkennung (YOLOv3/v5/v8), Mehrfachobjektverfolgung (CSRT, DeepSORT), Super-Resolution (EDSR) und optische Zeichenerkennung (OCR) mit temporaler Filterung.
- **Natural Language Processing & Safety AI**: Parametereffizientes Fine-Tuning (PEFT/LoRA) auf Llama-Architekturen, ordinale Regression unter extremem Klassenungleichgewicht und deterministische Guardrails.
- **Full-Stack ML Engineering**: Hochdurchsatz-FastAPI-Microservices, Containerisierung, mehrsprachige Docusaurus-Dokumentation und plattformübergreifende React Native-Apps.

---

## 📚 Hauptserien auf diesem Blog

### 1. 🧠 Maeumjigi Capstone Dev Log (23 Episoden)
Entwicklung eines KI-gestützten Systems zur Krisenerkennung und Suizidprävention:
- Synthetische klinische Dialoggenerierung mittels groß angelegter LLM-Pipelines.
- Beseitigung extremer Weak-Label-Overconfidence durch ordinale Regression und kumulative Schwellenwerte.
- Entwicklung deterministischer Safety-Wrapper-Guardrails zur Gewährleistung sub-millisekündlicher Krisenintervention.

### 2. 🤖 Webots Q-Learning Autonomer Roboter (5 Episoden)
Von Nullwissen-Exploration zu deterministischer Hindernisvermeidung:
- Diskretisierung von 6-Sektor-Distanzsensoren in 648 kompakte Zustände.
- Geometrische Geschwindigkeits- und Distanz-Delta-Reward-Gestaltung gegen spärliche Belohnungen.
- Bereitstellung der Q-Tabelle auf physischen Differentialantriebsrobotern via Arduino Uno.

### 3. 🚗 Blackbox ANPR & Spurerkennung Vision AI (5 Episoden)
Echtzeit-Embedded-Visionsystem für Dashcam-Aufnahmen bei hoher Geschwindigkeit:
- 6-stufige End-to-End-Pipeline mit strikter 30-FPS-Latenzgrenze.
- Dynamische Polynomanpassung für Fahrspuren und geometrische IoU-Kriterien.
- Kennzeichenerkennung mit EDSR-Super-Resolution und temporalem Majority Voting.
"""

# 2. German contact.md
de_contact = """---
title: Kontakt
description: Kontaktinformationen für Jihwan Park, Autor und Betreiber des Global Dev Blogs.
keywords: [Kontakt, Jihwan Park, E-Mail, GitHub, Technische Zusammenarbeit]
---

# Kontakt

Vielen Dank für Ihren Besuch auf **Global Dev Blog**. Wenn Sie Fragen zu technischen Implementierungen haben, an einer Zusammenarbeit interessiert sind oder Feedback zu den Artikeln geben möchten, freue ich mich über Ihre Nachricht.

---

## 📬 Direkte Anfragen

- **E-Mail**: [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com)  
  *Für Forschungsdiskussionen, technische Anfragen oder Fehlerberichte.*

---

## 💻 Open Source & Code-Repositories

- **GitHub-Profil**: [@jbjihwan](https://github.com/jbjihwan)
- **Blog-Quellcode-Repository**: [github.com/jbjihwan/global_blog](https://github.com/jbjihwan/global_blog)
- **Issues & Diskussionen**: Bei Tippfehlern, Code-Problemen oder defekten Links können Sie direkt ein GitHub-Issue erstellen:
  👉 [GitHub Issue erstellen](https://github.com/jbjihwan/global_blog/issues)

---

## ⏱️ Antwortzeit

Technische Anfragen beantworte ich in der Regel innerhalb von **24 bis 48 Stunden**.
"""

# 3. German privacy-policy.md
de_privacy = """---
title: Datenschutzerklärung (Privacy Policy)
description: Datenschutzerklärung für Global Dev Blog bezüglich Google Analytics 4, Google AdSense Cookies und Datenschutzrichtlinien.
keywords: [Datenschutzerklärung, Privacy Policy, Google AdSense, Google Analytics, DSGVO, Cookies]
---

# Datenschutzerklärung (Privacy Policy)

**Gültig ab:** 18. Oktober 2026  
**Zuletzt aktualisiert:** 18. Oktober 2026

Der Schutz Ihrer Daten ist auf **Global Dev Blog** (erreichbar unter [https://globaldevlog.com/](https://globaldevlog.com/)) von höchster Priorität. Diese Datenschutzerklärung legt dar, welche Arten von personenbezogenen Daten erfasst und verarbeitet werden.

Bei Fragen wenden Sie sich gerne per E-Mail an [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com).

---

## 1. Protokolldateien (Log Files)

Global Dev Blog verwendet standardmäßige Protokolldateien. Diese erfassen Besucher beim Laden der Website:
- IP-Adressen (anonymisiert)
- Browsertyp und -version
- Internet Service Provider (ISP)
- Datums- und Zeitstempel
- Verweisende und Ausgangsseiten
- Klickzahlen und Interaktionsereignisse

Diese Daten sind nicht mit persönlich identifizierbaren Informationen verknüpft und dienen der Trendanalyse, Site-Administration und Leistungsoptimierung.

---

## 2. Cookies und Web Beacons

Global Dev Blog verwendet Cookies zur Speicherung von Spracheinstellungen (Englisch, Deutsch, Französisch, Koreanisch usw.) und Theme-Präferenzen (Hell-/Dunkelmodus), um das Nutzererlebnis zu optimieren.

---

## 3. Google Analytics 4 (GA4)

Global Dev Blog verwendet **Google Analytics 4** (Mess-ID: `G-VM2CVW28SL`), einen Webanalysedienst der Google LLC.
- **IP-Anonymisierung**: IP-Adressen werden nicht dauerhaft gespeichert.
- **Opt-out**: Sie können die Datenerfassung durch das Google Analytics Browser-Add-on deaktivieren: [https://tools.google.com/dlpage/gaoptout](https://tools.google.com/dlpage/gaoptout).

---

## 4. Google AdSense & Werbung von Drittanbietern

Google ist ein Drittanbieter auf unserer Website und verwendet DART-Cookies, um Anzeigen basierend auf vorherigen Besuchen anzuzeigen.
- Nutzer können personalisierte Werbung in den Google-Anzeigeneinstellungen deaktivieren: [https://www.google.com/settings/ads](https://www.google.com/settings/ads).
- Weitere Deaktivierungsoptionen finden Sie unter: [http://www.aboutads.info/choices/](http://www.aboutads.info/choices/).
"""

# Write German files
with open(os.path.join(de_pages_dir, "about.md"), "w", encoding="utf-8") as f:
    f.write(de_about)
with open(os.path.join(de_pages_dir, "contact.md"), "w", encoding="utf-8") as f:
    f.write(de_contact)
with open(os.path.join(de_pages_dir, "privacy-policy.md"), "w", encoding="utf-8") as f:
    f.write(de_privacy)

print("German pages created successfully.")

# 4. French about.md
fr_about = """---
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
"""

# 5. French contact.md
fr_contact = """---
title: Contact
description: Coordonnées de Jihwan Park, auteur et responsable de Global Dev Blog.
keywords: [Contact, Jihwan Park, Email, GitHub, Collaboration technique]
---

# Contact

Merci de votre visite sur **Global Dev Blog**. Pour toute question technique sur nos implémentations, proposition de collaboration ou retour sur nos articles, n'hésitez pas à me contacter.

---

## 📬 Demandes directes

- **Email** : [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com)  
  *Pour discussions de recherche, questions techniques ou signalement d'anomalies.*

---

## 💻 Open Source & Dépôts de code

- **Profil GitHub** : [@jbjihwan](https://github.com/jbjihwan)
- **Dépôt source du blog** : [github.com/jbjihwan/global_blog](https://github.com/jbjihwan/global_blog)
- **Issues & Discussions** : Pour signaler une coquille ou un lien mort :
  👉 [Ouvrir une Issue sur GitHub](https://github.com/jbjihwan/global_blog/issues)

---

## ⏱️ Délai de réponse

Je réponds généralement aux messages techniques sous **24 à 48 heures**.
"""

# 6. French privacy-policy.md
fr_privacy = """---
title: Politique de Confidentialité (Privacy Policy)
description: Politique de confidentialité pour Global Dev Blog concernant Google Analytics 4, les cookies Google AdSense et la protection des données.
keywords: [Politique de Confidentialité, Privacy Policy, Google AdSense, Google Analytics, RGPD, Cookies]
---

# Politique de Confidentialité (Privacy Policy)

**Date d'entrée en vigueur :** 18 octobre 2026  
**Dernière mise à jour :** 18 octobre 2026

Sur **Global Dev Blog** (accessible à l'adresse [https://globaldevlog.com/](https://globaldevlog.com/)), la protection de vos données personnelles est une priorité absolue. Cette politique décrit la nature des données collectées et leur utilisation.

Pour toute question, contactez-nous à l'adresse [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com).

---

## 1. Fichiers journaux (Log Files)

Global Dev Blog applique une procédure standard de journalisation des accès :
- Adresses IP (anonymisées)
- Type et version du navigateur
- Fournisseur d'accès Internet (FAI)
- Horodatages des visites
- Pages de référence et de sortie
- Nombre de clics et interactions

Ces données ne sont reliées à aucune information personnellement identifiable et servent à l'administration du site et à l'optimisation des performances.

---

## 2. Cookies et balises Web

Global Dev Blog utilise des cookies pour mémoriser les préférences linguistiques (anglais, français, allemand, coréen, etc.) et le thème d'affichage (mode clair/sombre) afin d'optimiser l'expérience de navigation.

---

## 3. Google Analytics 4 (GA4)

Global Dev Blog utilise **Google Analytics 4** (ID de mesure : `G-VM2CVW28SL`), un service d'analyse d'audience fourni par Google LLC.
- **Anonymisation IP** : Les adresses IP ne sont pas conservées.
- **Désactivation** : Vous pouvez empêcher la collecte de données via le module complémentaire de navigateur : [https://tools.google.com/dlpage/gaoptout](https://tools.google.com/dlpage/gaoptout).

---

## 4. Google AdSense & Publicité tierce

Google est un fournisseur tiers sur notre site et utilise des cookies DART pour diffuser des annonces pertinentes.
- Les visiteurs peuvent désactiver la publicité personnalisée dans les paramètres des annonces Google : [https://www.google.com/settings/ads](https://www.google.com/settings/ads).
- D'autres options de désactivation sont disponibles sur : [http://www.aboutads.info/choices/](http://www.aboutads.info/choices/).
"""

with open(os.path.join(fr_pages_dir, "about.md"), "w", encoding="utf-8") as f:
    f.write(fr_about)
with open(os.path.join(fr_pages_dir, "contact.md"), "w", encoding="utf-8") as f:
    f.write(fr_contact)
with open(os.path.join(fr_pages_dir, "privacy-policy.md"), "w", encoding="utf-8") as f:
    f.write(fr_privacy)

print("French pages created successfully.")
