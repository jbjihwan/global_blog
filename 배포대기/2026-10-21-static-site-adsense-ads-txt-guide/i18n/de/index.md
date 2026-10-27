---
slug: static-site-adsense-ads-txt-guide
title: "[Web-Monetarisierung #2] Google AdSense-Zulassung für statische Websites: Lösung der ads.txt 404-Crawler-Falle & HeadTags-Integration"
authors: [jbgih]
tags: [google-adsense, docusaurus, github-pages, web-monetization, devops, cloudflare, seo]
date: 2026-10-21
keywords: [Google AdSense ads.txt Fehlerbehebung, Docusaurus Google AdSense Integration, Statische Website AdSense Zulassung, GitHub Pages ads.txt Deployment, Cloudflare WAF Googlebot Crawler]
description: "Vollständiger Entwickler-Leitfaden: Google AdSense-Verifizierung auf Docusaurus einrichten, statische ads.txt im Root bereitstellen und Cloudflare WAF-Crawler-Blockaden verhindern."
---

![Google AdSense Genehmigung und Crawler-Pipeline](./images/01_ads_txt_crawler_flow.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Das Problem**: Im Gegensatz zu dynamischen CMS (WordPress) lösen statische Websites (Docusaurus, Hugo) auf GitHub Pages häufig die Warnung **„Erträge gefährdet: ads.txt fehlt“** aus, weil Crawler durch Hydration-Verzögerungen oder WAF-Regeln blockiert werden.
> - **Die Lösung**: Verifizierungs-Tag direkt über `headTags` in `docusaurus.config.ts` einfügen, `ads.txt` in `static/ads.txt` platzieren und Cloudflare WAF-Bypass-Regeln für den `Googlebot-AdsTxt`-Crawler definieren.
> - **Das Ergebnis**: 100 % automatisierte Crawler-Erreichbarkeit, keine 404-Fehler und erfolgreiche AdSense-Freischaltung bei anhaltenden Lighthouse-Scores über 95.

{/* truncate */}

---

### 1. Das Problem: Warum statische Seiten bei ads.txt scheitern

Google AdSense verlangt zwei fundamentale technische Voraussetzungen:
1. **Publisher-Tag im `<head>`**: `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-..." crossorigin="anonymous"></script>`
2. **Validierte `ads.txt` unter der Root-Domain**: `https://example.com/ads.txt`

Bei Single Page Applications (SPAs) und SSGs schlägt die Validierung oft fehl, wenn JavaScript erst clientseitig gerendert wird oder Cloudflare Managed Challenge Bot-Filter den AdSense-Crawler versehentlich blockieren.

---

### 2. Die Lösungsschritte

#### Schritt 1: Saubere HeadTags-Injektion in Docusaurus
Fügen Sie das Skript in `docusaurus.config.ts` ein:
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

#### Schritt 2: Platzierung von `ads.txt`
Erstellen Sie die Datei `static/ads.txt`:
```text
google.com, pub-4654073335496617, DIRECT, f08c47fec0942fa0
```
Docusaurus kopiert Dateien aus `static/` direkt in das Root-Verzeichnis des Build-Outputs (`build/ads.txt`).

#### Schritt 3: Cloudflare WAF-Regel für Googlebot-AdsTxt
Erstellen Sie eine WAF-Ausnahmeregel, damit Crawler nicht durch Bot-Protection-Challenges geblockt werden:
- **Feld**: `User Agent`
- **Operator**: `contains`
- **Wert**: `Googlebot`
- **Aktion**: `Bypass / Skip`

---

### 📌 Management Summary (3–5 Zeilen)
1. **Automatisierte Bereitstellung**: Die Platzierung der `ads.txt` im `static/`-Verzeichnis garantiert die Verfügbarkeit unter `domain.com/ads.txt`.
2. **HeadTags statt React-Hooks**: Die Injektion über `docusaurus.config.ts headTags` stellt sicher, dass der AdSense-Code bereits im initialen statischen HTML enthalten ist.
3. **Cloudflare WAF konfigurieren**: Der `Googlebot-AdsTxt`-Crawler muss explizit von Bot-Challenges ausgenommen werden.
4. **Verifizierung nach 24 Stunden**: Sobald die DNS- und WAF-Pfade frei sind, schließt Google die Publisher-Prüfung erfolgreich ab.