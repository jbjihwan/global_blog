---
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