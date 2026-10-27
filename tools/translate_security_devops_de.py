# -*- coding: utf-8 -*-
import os
import shutil

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")

def save_de_post(slug, de_content):
    # 1. Save to Staging
    stage_dir = os.path.join(STAGING_ROOT, slug)
    stage_de_dir = os.path.join(stage_dir, "i18n", "de")
    os.makedirs(stage_de_dir, exist_ok=True)
    with open(os.path.join(stage_de_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(de_content.strip() + "\n")
    print(f"[STAGING OK] {slug} -> {stage_de_dir}\\index.md")

    # 2. Save to i18n/de production blog dir (ready for build)
    prod_de_dir = os.path.join(GB_ROOT, "i18n", "de", "docusaurus-plugin-content-blog", slug)
    os.makedirs(prod_de_dir, exist_ok=True)
    with open(os.path.join(prod_de_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(de_content.strip() + "\n")
    
    # 3. Copy images from blog/<slug>/images
    src_images = os.path.join(GB_ROOT, "blog", slug, "images")
    if os.path.exists(src_images):
        dst_images = os.path.join(prod_de_dir, "images")
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
title: "[Leitfaden 2026] npm audit-Schwachstellen beheben ohne Builds zu zerstören: Die Wahrheit über npm audit fix --force"
authors: [jbgih]
tags: [web-security, npm-audit, docusaurus, devops, supply-chain]
keywords: [npm audit fix Fehlerbehebung, npm audit fix --force Risiko, Sicherheit statischer Webseiten, npm Sicherheitslücken, GHSA Schwachstellen]
description: "Wie Sie npm audit-Schwachstellen beheben, ohne Produktions-Builds zu beschädigen. Warum 45 Build-Tool-Sicherheitslücken auf statischen Seiten kein Laufzeitrisiko darstellen und wie GHSA-Warnungen sicher gelöst werden."
---

Jeder moderne Frontend-Entwickler kennt diesen plötzlichen Adrenalinstoß: Sie führen `npm audit` in Ihrem Dokumentations- oder Blog-Repository aus, und das Terminal warnt in leuchtend roter Schrift:

```text
45 vulnerabilities (15 moderate, 15 high, 15 critical)
To address all issues (including breaking changes), run:
  npm audit fix --force
```

Begriffe wie **Critical**, **Remote Code Execution (RCE)** und **Prototype Pollution** lösen sofort den Reflex aus, `npm audit fix --force` einzugeben, um die roten Warnungen schnellstmöglich verschwinden zu lassen.

In der Welt statischer Website-Generatoren (**Static Site Generators, SSG**) wie Docusaurus, Next.js (SSG) oder Hugo, die auf GitHub Pages oder AWS S3 gehostet werden, ist dieser Befehl jedoch oft ein fataler Fehler: Er bricht Produktions-Builds durch inkompatible Major-Updates, ohne die tatsächliche Sicherheit um ein einziges Prozent zu verbessern.

{/* truncate */}

---

### 1. Bedrohungsmodellierung: Dynamischer Webserver vs. Statische Seite (SSG)

Um zu verstehen, warum die meisten `npm audit`-Warnungen auf statischen Seiten Fehlalarme für die Produktionssicherheit sind, betrachten wir die fundamentale Angriffsfläche:

![Bedrohungsmodellierung: Dynamischer Webserver vs Statische Seite](./images/01_threat_model.png)

#### Traditioneller dynamischer Server (Node.js / Express / Django)
- **24/7 aktiver Prozess**: Ein Node.js-Daemon lauscht kontinuierlich auf Port 80/443.
- **Echtzeit-Ausführung**: Trifft eine bösartige HTTP-Anfrage ein, durchläuft sie Middleware-Pakete. Eine Schwachstelle (z. B. Prototype Pollution in `lodash` oder RCE in einer Template-Engine) kann zur Kompromittierung des gesamten Servers und zum Diebstahl von Umgebungsvariablen führen.

#### Statische Website (Docusaurus / GitHub Pages CDN)
- **Reine Build-Zeit-Nutzung**: Node.js läuft ausschließlich lokal oder in GitHub Actions während des Build-Prozesses.
- **Null Backend-Prozesse zur Laufzeit**: An die Besucher werden ausschließlich vorab kompilierte statische HTML-, CSS- und JavaScript-Dateien über Anycast-CDNs ausgeliefert.
- **RCE-Risiko = 0 %**: Selbst wenn ein Build-Tool (`webpack`, `micromatch`) eine theoretische RCE-Lücke hat, existiert zur Laufzeit kein Server, der Anfragen entgegennimmt.

---

### 2. Die Gefahren von `npm audit fix --force`

Der Parameter `--force` erlaubt npm, grundlegende Major-Versionssprünge (`breaking changes`) durchzuführen. Bei Docusaurus führt dies regelmäßig dazu, dass Webpack- oder Babel-Plugins auf Versionen aktualisiert werden, die von Docusaurus noch nicht unterstützt werden. Das Ergebnis: Die Schwachstellenwarnung verschwindet, aber `npm run build` bricht mit kryptischen Syntaxfehlern ab.

---

### 3. Best Practices: Der 4-Stufen-Sicherheitsleitfaden

```mermaid
flowchart TD
    A[npm audit meldet Schwachstellen] --> B{Betrifft die Lücke devDependencies?}
    B -->|Ja: Build-Tools wie Webpack/Babel| C[Prüfen: Wird Code ins Client-Bundle gepackt?]
    C -->|Nein: Reines Build-Tool| D[Risiko im SSG-Kontext: 0% | Kein npm audit fix --force!]
    C -->|Ja: Client-Runtime| E[Selektives Update via package.json overrides]
    B -->|Nein: Echte Runtime-Abhängigkeit| E
```

1. **Abhängigkeitsbereich prüfen**: Unterscheiden Sie strikt zwischen Entwicklungs-Tools (`devDependencies`) und Client-Bibliotheken.
2. **Selective Overrides nutzen**: Verwenden Sie das `overrides`-Feld in `package.json`, um Sub-Abhängigkeiten gezielt ohne Breaking Changes zu patchen:
   ```json
   "overrides": {
     "nth-check": "^2.1.1"
   }
   ```
3. **CI-Pipelines absichern**: Nutzen Sie `npm audit --omit=dev` in Produktions-Checks.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Kein blindes `npm audit fix --force`**: Erzwungene Updates brechen Build-Pipelines durch inkompatible Major-Versionen.
2. **SSG-Sicherheitsvorteil**: Da statische Seiten ohne laufenden Node.js-Server über CDNs ausgeliefert werden, stellen reine Build-Tool-Lücken kein Produktions-Laufzeitrisiko dar.
3. **Präzises Patchen mit Overrides**: Aktualisieren Sie betroffene transitive Abhängigkeiten gezielt über `package.json overrides`.
4. **Fokus auf echte Bedrohungen**: Schützen Sie stattdessen Ihre CI/CD-Secrets und Deployment-Tokens.
"""

# ==============================================================================
# 2. CUSTOM DOMAIN ADSENSE SEO GUIDE
# ==============================================================================
p2_slug = "2026-10-20-custom-domain-adsense-seo-guide"
p2_content = """---
slug: github-pages-custom-domain-adsense-seo-guide
title: "Von GitHub Pages zur eigenen Domain: Vollständiger Leitfaden für Porkbun, Cloudflare DNS, AdSense-Zulassung und Multi-Engine-SEO"
authors: [jbjihwan]
tags: [docusaurus, devops, cloudflare, seo, web-monetization]
keywords: [Docusaurus GitHub Pages Eigene Domain, Cloudflare DNS Porkbun CNAME Setup, Google AdSense ads.txt statische Seite, Google Search Console Sitemap Fehler, Naver Search Advisor RSS Host Fehler]
description: "Produktions-Leitfaden für die Migration eines statischen Docusaurus-Blogs auf GitHub Pages zu einer Apex-Custom-Domain mit Porkbun und Cloudflare DNS, Google AdSense-Verifizierung und Multi-Suchmaschinen-SEO."
---

Ein Entwickler-Blog auf GitHub Pages unter `username.github.io/project` ist eine der schnellsten Möglichkeiten, technische Artikel zu veröffentlichen. Sobald Ihre Leserschaft jedoch wächst und Sie eine professionelle Monetarisierung anstreben, stoßen Sie auf eine harte Grenze: **Google AdSense verbietet kostenlose Subdomains wie `*.github.io` strikt**. Für die AdSense-Verifizierung und nachhaltigen organischen Traffic benötigen Sie eine eigene Apex-Domain.

Die Migration einer statischen Dokumentationsseite auf eine eigene Domain erfordert weit mehr als einen einfachen DNS-Eintrag: Nameserver-Delegierung, Edge-SSL-Zertifikate, kanonische Weiterleitungen, automatisches `ads.txt`-Hosting und die korrekte Indexierung in Google, Naver und Bing.

In diesem Leitfaden beschreiben wir unsere Zero-Downtime-Migration von `jbjihwan.github.io/global_blog` zu `https://globaldevlog.com`.

{/* truncate */}

---

![Produktions-DNS & CDN-Routing-Architektur](./images/01_dns_routing_architecture.png)

### 1. Architektur-Übersicht: Das 3-Schichten-Modell

```mermaid
flowchart LR
    User[Besucher weltweit] --> Edge[Cloudflare Anycast CDN & DNS]
    Edge -->|Universal SSL Termination| Edge
    Edge -->|CNAME Flattening| Origin[GitHub Pages Static Storage]
    Origin --> Static[Vorab kompilierte HTML/CSS/JS Assets]
```

1. **Domain-Registrar (Porkbun)**: Verwaltet die Domain-Registrierung und delegiert Nameserver vollständig an Cloudflare.
2. **DNS & Edge-Sicherheit (Cloudflare Anycast DNS)**:
   - **CNAME Flattening**: Erlaubt es, die Apex-Domain (`globaldevlog.com`) ohne A-Record-Starrheit direkt auf GitHub Pages zu mappen.
   - **Universal SSL**: Stellt HTTPS-Zertifikate an der Edge bereit und erzwingt HTTP-zu-HTTPS-Weiterleitungen.
3. **Hosting-Plattform (GitHub Pages)**: Liefert die Docusaurus-Build-Artefakte weltweit aus.

---

### 2. Multi-Engine SEO-Indexierung: Fallen und Lösungen

Bei der Registrierung in internationalen und regionalen Suchmaschinen treten häufig typische Fehler auf:

| Suchmaschine | Typisches Problem | Technische Ursache & Lösung |
| :--- | :--- | :--- |
| **Google Search Console** | „Sitemap konnte nicht gelesen werden“ | Docusaurus generiert standardmäßig `/sitemap.xml`. Bei Domain-Wechsel muss die alte Property gelöscht und ein DNS-TXT-Eintrag verifiziert werden. |
| **Naver Search Advisor** | „Host-URL stimmt nicht überein“ | Naver verlangt strikte Übereinstimmung zwischen RSS-Link und registrierter URL (Trailing Slashes beachten). |
| **Bing Webmaster Tools** | Verzögerte Indexierung | Direkter Import über Google Search Console OAuth2 beschleunigt die Freischaltung auf wenige Minuten. |

---

### 📌 Management Summary (3–5 Zeilen)
1. **Eigene Domain zwingend erforderlich**: Google AdSense lehnt kostenlose Subdomains (`github.io`) grundsätzlich ab; eine eigene Apex-Domain ist Pflicht.
2. **Porkbun + Cloudflare-Vorteil**: CNAME Flattening und Universal SSL ermöglichen Zero-Downtime-Betrieb bei maximaler Ausfallsicherheit.
3. **Multi-Engine SEO**: Neben Google sollten Naver und Bing über saubere Sitemaps (`/sitemap.xml`) und RSS-Feeds parallel bedient werden.
4. **Kanonische Weiterleitungen**: Erzwingen Sie HTTPS und leiten Sie `www` konsistent auf die Apex-Domain weiter.
"""

# ==============================================================================
# 3. GITHUB PAGES CUSTOM DOMAIN CLOUDFLARE DNS
# ==============================================================================
p3_slug = "2026-10-21-github-pages-custom-domain-cloudflare-dns"
p3_content = """---
slug: github-pages-custom-domain-cloudflare-dns
title: "Eigene Domain auf GitHub Pages #1: Zero-Downtime-Migration mit Porkbun und Cloudflare DNS (CNAME Flattening & Universal SSL)"
authors: [jbjihwan]
tags: [github-pages, custom-domain, porkbun, cloudflare, docusaurus, devops]
keywords: [Docusaurus GitHub Pages Eigene Domain, Cloudflare DNS Porkbun CNAME Setup, CNAME Flattening Apex Domain, Cloudflare Full SSL Edge Zertifikat, CNAME Deployment Reset Bug Fix]
description: "Schritt-für-Schritt-Anleitung: Wechsel von kostenlosen github.io-Subdomains zu einer Apex-Domain via Porkbun und Cloudflare Anycast DNS ohne HTTPS-Ausfall."
---

Ein Entwickler-Blog auf GitHub Pages unter `username.github.io/project` ist kostengünstig und unkompliziert: Markdown committen, Git-Push ausführen und GitHub liefert die Seite global aus.

Sobald Sie jedoch professionelles Branding und Monetarisierung planen, stehen Sie vor einem Hindernis: **Google AdSense verbietet kostenlose Sekundär-Subdomains wie `*.github.io` vollständig**. Zudem bleibt die erarbeitete Domain Authority an GitHub gebunden anstatt Ihrer eigenen Marke zugutezukommen.

In diesem ersten Teil unserer Infrastrukturserie zeigen wir die exakte Zero-Downtime-Migration von `jbjihwan.github.io/global_blog` zu `https://globaldevlog.com` über eine hochverfügbare **Porkbun + Cloudflare + GitHub Pages 3-Stufen-Architektur**.

{/* truncate */}

---

### 1. Schritt-für-Schritt-Konfiguration

#### Schritt 1: Nameserver-Delegierung bei Porkbun
Ersetzen Sie bei Porkbun die Standard-Nameserver durch die zugewiesenen Cloudflare Anycast-Nameserver:
- `curt.ns.cloudflare.com`
- ` रोजी.ns.cloudflare.com`

#### Schritt 2: DNS-Einträge bei Cloudflare (CNAME Flattening)
Tragen Sie zwei DNS-Records ein:
- **Typ**: `CNAME` | **Name**: `@` (Apex) | **Ziel**: `jbjihwan.github.io` | **Proxy**: Aktiviert (Orange Cloud)
- **Typ**: `CNAME` | **Name**: `www` | **Ziel**: `jbjihwan.github.io` | **Proxy**: Aktiviert

#### Schritt 3: Docusaurus CNAME-Reset-Bug verhindern
GitHub Pages benötigt eine Datei namens `CNAME` im Root des Deployment-Branches. Wenn Sie `npm run deploy` ausführen, überschreibt Docusaurus den Branch. Legen Sie daher die CNAME-Datei in das Verzeichnis `static/CNAME`:
```text
globaldevlog.com
```
Dadurch kopiert Docusaurus die Domain-Datei bei jedem Build automatisch in das Root-Verzeichnis.

---

### 2. SSL/TLS-Verschlüsselung: Der Full (Strict) Modus

In den Cloudflare SSL/TLS-Einstellungen muss der Modus **Full** oder **Full (Strict)** gewählt werden. Da GitHub Pages automatisch Let's Encrypt-Zertifikate für Custom Domains ausstellt, ist die Verbindung zwischen Cloudflare Edge und GitHub Pages durchgängig verschlüsselt.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Strikte Trennung**: Porkbun übernimmt die Domain-Verwaltung, Cloudflare sichert DNS und Edge-Routing, GitHub Pages hostet die statischen Dateien.
2. **CNAME Flattening**: Ermöglicht das direkte Routing der Apex-Domain ohne starre IP-Adressen.
3. **Docusaurus CNAME-Sicherung**: Platzieren Sie die `CNAME`-Datei im `static/`-Ordner, um versehentliches Überschreiben bei Re-Deployments zu verhindern.
4. **Durchgängige Verschlüsselung**: Nutzen Sie Cloudflare SSL Full für nahtlose HTTPS-Sicherheit.
"""

# ==============================================================================
# 4. STATIC SITE ADSENSE ADS-TXT GUIDE
# ==============================================================================
p4_slug = "2026-10-21-static-site-adsense-ads-txt-guide"
p4_content = """---
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
"""

# Execute Section 2
if __name__ == "__main__":
    print("=" * 60)
    print("Translating Section 2 (DevOps, Security, AdSense) into German...")
    print("=" * 60)
    save_de_post(p1_slug, p1_content)
    save_de_post(p2_slug, p2_content)
    save_de_post(p3_slug, p3_content)
    save_de_post(p4_slug, p4_content)
    print("\n[SECTION 2 COMPLETE] All 4 DevOps & Security posts staged and saved in German!")
