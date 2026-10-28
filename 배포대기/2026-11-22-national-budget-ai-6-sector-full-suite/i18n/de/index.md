---
slug: national-budget-ai-6-sector-full-suite
title: "KI-Haushaltsprüfung #5: 6-Sektor-Suite & Jahresend-Dumping"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, procurement-fraud, year-end-dumping, spec-driven-development, devops]
date: 2026-11-22
keywords: ["6-Sektor-Prüfsuite", "Stückelungsverträge", "Jahresend-Etatausgaben", "Vergabebetrug KI", "Haushaltsprüfung"]
description: "Abschluss der 6-Sektor-Prüfsuite: Aufdeckung von Stückelungsverträgen unter Ausnutzung von 40.000-$-Sonderregeln und Jahresend-Etatsausgaben."
---

![6-Sector Targeted Audit: Divide & Conquer Suite](./images/01_national_budget_6_sector_suite.png)

> 📌 **Kernaussagen (Key Takeaways)**
> - **Vollständige 6-Sektor-Prüfsuite**: Ausfilterung von 85% Routinebeschaffungen bei 4 Millionen Aufträgen, Ausweitung auf **6 Kernrisiko-Sektoren**.
> - **2 Versteckte Schwachstellen Aufgedeckt**:
>   1. **Sektor 5 (Stückelung unter 40.000-$-Ausnahme)**: Gezielte Häufung von Aufträgen bei 98% der Höchstgrenze (180.000 $ aufgedeckt).
>   2. **Sektor 6 (Jahresend-Etatsverbraten)**: 3 freihändige Vergaben in 4 Tagen Ende Dezember zur Vermeidung von Haushaltsrückzahlungen.
> - **Präventive Architektur**: Schwellenwert-Näherungsanalyse (96–99,8%) und Prüfung der zeitlichen Machbarkeit vor dem Jahresabschluss.
> - **Fehlerbehebung**: Prioritätsgewichtung bei Sektorkollisionen und Nettobetragsumrechnung ohne Mehrwertsteuer.

{/* truncate */}

---

### ⚠️ Rechtlicher Hinweis & Anonymisierung (Legal Notice)

> **[Hinweis] Alle Vorgänge wurden zum Schutz der Beteiligten vollständig anonymisiert.**  
> Behörden (`Behörde A`), Firmen (`Firma D`), Personen und Verträge wurden durch Pseudonyme ersetzt.

---

### 1. Architektur der 6-Sektor-Prüfsuite

```mermaid
flowchart TD
    Raw[4 Millionen Vergabeaufträge/Jahr] --> Filter{3D-Sektorpartitions-Manager}
    Filter -->|85% Routineaufwand| Drop[Niedrigrisiko-Archiv]
    Filter --> S1["Sektor 1: ICT-Stückelungen &lt;20T $"]
    Filter --> S2["Sektor 2: Kommunale Event-Kartelle"]
    Filter --> S3["Sektor 3: Fördergeldabfluss DEI"]
    Filter --> S4["Sektor 4: Großausschreibungs-Monopole"]
    Filter --> S5["🔴 Sektor 5: 40T-$-Ausnahmemissbrauch"]
    Filter --> S6["🔴 Sektor 6: Jahresend-Mittelabfluss"]
    S1 & S2 & S3 & S4 & S5 & S6 --> Master[All Sectors Master Runner]
```

---

### 2. Vorhersehbare Herausforderungen & Fehlerbehebung

1. **Ausnahmeregelung vs. Missbrauch**: Proximitätsanalyse an der Grenze von 40.000 $, um reguläre Sozialförderungen nicht fälschlich zu beanstanden.
2. **Normaler Jahresabschluss vs. Notvergaben**: Aussortierung von Projekten, deren vertragliche Leistungen bis zum 31. Dezember physisch nicht erbracht werden können.
3. **Kollisionen bei Mehrfachzuweisung**: Rangfolge nach rechtlicher Schwere zur Vermeidung redundanter Berichte.
4. **Nettobetragsprüfung**: Rückrechnung von Bruttobeträgen zur zutreffenden Prüfung der Freigrenzen.

---

### 3. Validierung und Feldleistung

Erfolgreiche Aufdeckung gestückelter Vergaben bei `Behörde A` und überhasteter Jahresendvergaben bei `Behörde C`; 17/17 Testsuiten vollständig bestanden.
