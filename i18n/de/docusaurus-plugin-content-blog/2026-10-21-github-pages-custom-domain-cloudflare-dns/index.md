---
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
