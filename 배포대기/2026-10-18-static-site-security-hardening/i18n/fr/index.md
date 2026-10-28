---
slug: static-site-security-npm-audit-truth
title: "Corriger les vulnérabilités npm sans casser vos builds"
authors: [jbgih]
tags: [web-security, npm-audit, docusaurus, devops, supply-chain]
keywords: ["npm audit fix", "npm audit fix --force", "vulnérabilités npm", "sécurité site statique"]
description: "Comment corriger les vulnérabilités npm audit sans casser vos builds. Pourquoi npm audit fix --force est dangereux et comment sécuriser un site statique."
---

Tout développeur frontend a déjà ressenti cette montée d'adrénaline : vous lancez `npm audit` sur votre dépôt de blog ou de documentation, et le terminal s'affole en lettres rouges :

```text
45 vulnerabilities (15 moderate, 15 high, 15 critical)
To address all issues (including breaking changes), run:
  npm audit fix --force
```

Des termes tels que **Critical**, **Remote Code Execution (RCE)** et **Prototype Pollution** déclenchent un réflexe immédiat : saisir `npm audit fix --force` pour faire disparaître ces alertes.

Pourtant, dans l'univers des **générateurs de sites statiques (SSG)** comme Docusaurus, Next.js (SSG) ou Hugo hébergés sur GitHub Pages ou AWS S3, cette commande est souvent une grave erreur : elle brise les builds de production avec des montées de versions incompatibles sans améliorer votre sécurité réelle.

{/* truncate */}

---

### 1. Modélisation des menaces : Serveur dynamique vs Site statique (SSG)

![Modélisation des menaces : Serveur web dynamique vs Site statique](./images/01_threat_model.png)

#### Serveur dynamique classique (Node.js / Express / Django)
- **Processus actif 24h/24** : Un serveur écoute en permanence sur les ports 80/443.
- **Risque d'exécution en temps réel** : Une faille dans une dépendance peut permettre une exécution de code à distance (RCE) ou une fuite de variables d'environnement.

#### Site statique (Docusaurus / CDN GitHub Pages)
- **Utilisation restreinte au build** : Node.js s'exécute uniquement lors de la compilation sur votre machine ou dans GitHub Actions.
- **Zéro démon en production** : Les visiteurs ne reçoivent que des fichiers HTML, CSS et JavaScript pré-compilés via un réseau Anycast CDN.
- **Risque de RCE = 0 %** : Aucun processus serveur ne tourne en production pour intercepter une attaque.

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Éviter `npm audit fix --force`** : Les mises à jour forcées cassent vos builds en introduisant des versions majeures incompatibles.
2. **Avantage sécuritaire du SSG** : Les sites statiques sans backend actif sont totalement immunisés contre les failles d'exécution des outils de build.
3. **Correctifs ciblés avec overrides** : Utilisez la section `overrides` de `package.json` pour mettre à jour les sous-dépendances critiques sans casser l'écosystème.
4. **Priorité aux vraies menaces** : Sécurisez plutôt vos tokens de déploiement et secrets GitHub Actions.