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
# 1. STATIC SITE SECURITY HARDENING (npm audit truth)
# ==============================================================================
p1_slug = "2026-10-18-static-site-security-hardening"
p1_content = """---
slug: static-site-security-npm-audit-truth
title: "[Guide 2026] Résoudre les vulnérabilités npm audit sans casser vos builds : La vérité sur npm audit fix --force"
authors: [jbgih]
tags: [web-security, npm-audit, docusaurus, devops, supply-chain]
keywords: [Résolution vulnérabilités npm audit, Risques npm audit fix --force, Sécurité des sites statiques, Vulnérabilités de build npm, Alertes GHSA Docusaurus]
description: "Comment corriger les vulnérabilités npm audit sans casser vos builds en production. Pourquoi 45 failles d'outils de build ne posent aucun risque à l'exécution sur sites statiques."
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
"""

# ==============================================================================
# 2. CUSTOM DOMAIN ADSENSE SEO GUIDE
# ==============================================================================
p2_slug = "2026-10-20-custom-domain-adsense-seo-guide"
p2_content = """---
slug: github-pages-custom-domain-adsense-seo-guide
title: "De GitHub Pages à un domaine personnalisé : Le guide complet pour Porkbun, Cloudflare DNS, AdSense et le SEO multi-moteurs"
authors: [jbjihwan]
tags: [docusaurus, devops, cloudflare, seo, web-monetization]
keywords: [Domaine personnalisé GitHub Pages Docusaurus, Configuration DNS Cloudflare Porkbun CNAME, Fichier ads.txt site statique Google AdSense, Résolution erreur sitemap Google Search Console, Erreur hôte RSS Naver Search Advisor]
description: "Plan de production complet pour migrer un blog Docusaurus statique sur GitHub Pages vers un domaine personnalisé apex via Porkbun et Cloudflare DNS, réussir l'approbation Google AdSense et dominer le SEO."
---

Héberger un blog technique sur GitHub Pages sous l'adresse `username.github.io/project` est l'un des moyens les plus rapides de publier. Mais pour une monétisation professionnelle, vous vous heurtez à une contrainte majeure : **Google AdSense interdit formellement les sous-domaines gratuits comme `*.github.io`**. Pour obtenir la validation AdSense et bâtir une autorité de domaine durable, vous devez posséder votre propre domaine apex personnalisé.

Migrer un site statique vers un domaine personnalisé implique la délégation de serveurs de noms, la terminaison SSL à l'edge, des redirections canoniques, l'hébergement d'`ads.txt` et une indexation propre sur Google, Naver et Bing.

Découvrez dans ce guide notre migration sans aucune interruption de service de `jbjihwan.github.io/global_blog` vers `https://globaldevlog.com`.

{/* truncate */}

---

![Architecture de routage DNS et CDN en production](./images/01_dns_routing_architecture.png)

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Domaine propre obligatoire** : Google AdSense refuse les sous-domaines gratuits `github.io` ; un nom de domaine apex est indispensable.
2. **Puissance de Porkbun + Cloudflare** : Le CNAME Flattening et le certificat Universal SSL assurent une transition sans aucune interruption de service.
3. **SEO multi-moteurs** : Enregistrez vos sitemaps (`/sitemap.xml`) et flux RSS de manière synchronisée sur Google, Naver et Bing.
4. **Redirections canoniques** : Forcez systématiquement le HTTPS et redirigez le sous-domaine `www` vers le domaine apex.
"""

# ==============================================================================
# 3. GITHUB PAGES CUSTOM DOMAIN CLOUDFLARE DNS
# ==============================================================================
p3_slug = "2026-10-21-github-pages-custom-domain-cloudflare-dns"
p3_content = """---
slug: github-pages-custom-domain-cloudflare-dns
title: "Domaine personnalisé sur GitHub Pages #1 : Migration zéro interruption avec Porkbun et Cloudflare DNS (CNAME Flattening & Universal SSL)"
authors: [jbjihwan]
tags: [github-pages, custom-domain, porkbun, cloudflare, docusaurus, devops]
keywords: [Domaine personnalisé GitHub Pages Docusaurus, Configuration DNS Cloudflare Porkbun CNAME, CNAME Flattening domaine apex GitHub Pages, Certificat Edge SSL Cloudflare Full, Correction bug écrasement CNAME Docusaurus]
description: "Guide pas à pas pour abandonner les sous-domaines gratuits github.io, acquérir un domaine apex via Porkbun et le configurer sur Cloudflare Anycast DNS sans coupure HTTPS."
---

Héberger un blog d'ingénierie sur GitHub Pages sous `username.github.io/project` est gratuit et pratique. Toutefois, pour développer une marque pérenne et activer la monétisation, **Google AdSense bloque toute inscription sur les sous-domaines secondaires `github.io`**. De plus, l'autorité de recherche (PageRank) reste acquise à GitHub au lieu de valoriser votre domaine.

Ce premier volet détaille la méthodologie exacte pour migrer de `jbjihwan.github.io/global_blog` à `https://globaldevlog.com` grâce à une **architecture 3-tiers robuste Porkbun + Cloudflare + GitHub Pages**.

{/* truncate */}

---

### 1. Configuration étape par étape

#### Étape 1 : Délégation des serveurs de noms sur Porkbun
Réglez vos serveurs de noms sur Cloudflare Anycast :
- `curt.ns.cloudflare.com`
- `rozy.ns.cloudflare.com`

#### Étape 2 : Entrées DNS Cloudflare (CNAME Flattening)
- **Type** : `CNAME` | **Nom** : `@` | **Cible** : `jbjihwan.github.io` | **Proxy** : Activé
- **Type** : `CNAME` | **Nom** : `www` | **Cible** : `jbjihwan.github.io` | **Proxy** : Activé

#### Étape 3 : Empêcher la réinitialisation du fichier CNAME
Placez votre domaine dans `static/CNAME` pour que Docusaurus le copie automatiquement à la racine lors de chaque build :
```text
globaldevlog.com
```

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Séparation claire** : Porkbun gère le bureau d'enregistrement, Cloudflare assure le DNS et la sécurité edge, GitHub Pages sert les fichiers statiques.
2. **CNAME Flattening** : Permet de mapper le domaine apex directement sans adresses IP rigides.
3. **Sécurisation du CNAME Docusaurus** : L'ajout du fichier dans `static/CNAME` élimine les pannes de domaine lors des déploiements.
4. **Sécurité SSL totale** : Le mode Cloudflare SSL Full garantit un chiffrement de bout en bout.
"""

# ==============================================================================
# 4. STATIC SITE ADSENSE ADS-TXT GUIDE
# ==============================================================================
p4_slug = "2026-10-21-static-site-adsense-ads-txt-guide"
p4_content = """---
slug: static-site-adsense-ads-txt-guide
title: "[Monétisation Web #2] Approbation Google AdSense sur sites statiques : Résoudre le piège du 404 ads.txt & Intégration HeadTags"
authors: [jbgih]
tags: [google-adsense, docusaurus, github-pages, web-monetization, devops, cloudflare, seo]
date: 2026-10-21
keywords: [Correction erreur ads.txt Google AdSense, Intégration Docusaurus Google AdSense, Approbation AdSense site statique, Déploiement ads.txt GitHub Pages, Crawler Googlebot Cloudflare WAF]
description: "Guide développeur complet : configurer la vérification de propriété Google AdSense sur Docusaurus, déployer le fichier ads.txt à la racine et éviter les blocages de robots par Cloudflare WAF."
---

![Pipeline d'approbation et de crawl Google AdSense](./images/01_ads_txt_crawler_flow.png)

> 📌 **Points clés (TL;DR)**
> - **Le problème** : Contrairement aux CMS dynamiques (WordPress), les générateurs de sites statiques sur GitHub Pages déclenchent régulièrement l'alerte **« Revenus à risque : fichier ads.txt manquant »** car les robots sont bloqués par les règles WAF ou l'hydratation JS.
> - **La solution** : Injecter le script de l'éditeur directement dans `<head>` via `headTags` dans `docusaurus.config.ts`, déposer `ads.txt` dans `static/ads.txt` et créer une exception Cloudflare WAF pour `Googlebot-AdsTxt`.
> - **Le résultat** : 100 % d'accessibilité pour les robots, zéro erreur 404 sur `/ads.txt` et approbation rapide par Google AdSense.

{/* truncate */}

---

### 1. Configuration en 3 étapes

#### Étape 1 : Injection du script via HeadTags
```ts
headTags: [
  {
    tagName: 'script',
    attributes: {
      async: 'true',
      src: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4654073335496617',
      crossorigin: 'anonymous',
    },
  },
],
```

#### Étape 2 : Déploiement du fichier `static/ads.txt`
```text
google.com, pub-4654073335496617, DIRECT, f08c47fec0942fa0
```

#### Étape 3 : Règle de contournement WAF Cloudflare
Autorisez sans challenge les requêtes dont le `User Agent` contient `Googlebot`.

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Déploiement statique propre** : Déposer le fichier dans `static/ads.txt` assure sa disponibilité immédiate à la racine `domaine.com/ads.txt`.
2. **HeadTags natif Docusaurus** : Garantit que la balise de vérification est présente dans le HTML statique initial avant tout rendu React.
3. **Exception WAF indispensable** : Empêche Cloudflare de bloquer les sondes automatiques de Google AdSense.
4. **Validation sous 24h** : Permet une monétisation publicitaire sans impact sur les scores de vitesse Lighthouse.
"""

# Execute French Section 2
if __name__ == "__main__":
    print("=" * 60)
    print("Translating Section 2 (DevOps, Security, AdSense) into French...")
    print("=" * 60)
    save_fr_post(p1_slug, p1_content)
    save_fr_post(p2_slug, p2_content)
    save_fr_post(p3_slug, p3_content)
    save_fr_post(p4_slug, p4_content)
    print("\n[FRENCH SECTION 2 COMPLETE] All 4 DevOps & Security posts staged and saved in French!")
