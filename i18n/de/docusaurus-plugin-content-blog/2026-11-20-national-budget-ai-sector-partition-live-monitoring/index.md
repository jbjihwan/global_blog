---
slug: national-budget-ai-sector-partition-live-monitoring
title: "KI-Haushaltsprüfung #3: 3D-Sektorpartitionierung & Portal"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, live-streaming, koneps-api, web-dashboard, devops]
date: 2026-11-20
keywords: ["3D-Sektorpartitionierung", "Vergabe-API-Anbindung", "Prüfer-Webportal", "KI-Anomalieerkennung", "Rauschfilterung"]
description: "Filterung von 85% Beschaffungsrauschen durch 3D-Partitionierung und Anbindung von Live-APIs für das interaktive Rechnungsprüfer-Webportal v2.0."
---

![3D Sector Partitioning & Live Audit Web Portal](./images/01_national_budget_sector_live_monitor.png)

> 📌 **Kernaussagen (Key Takeaways)**
> - **Beseitigung von Alarmmüdigkeit**: Der **3D-Sektorpartitions-Manager (SectorPartitionManager)** filtert über 85% des Rauschens von Routinebeschaffungen heraus und fokussiert die KI-Kapazität auf Hochrisiko-Sektoren.
> - **Präventive Architektur**: Eine isolierte **SQLite-Puffer-Warteschlange mit exponentiellem Backoff** schützt das System vor Timeouts und Schemaänderungen öffentlicher APIs.
> - **Behebung von 3 Produktionsfehlern**:
>   1. Zirkumflex-Trennzeichen (`^`) in API-Feldern ➔ Regex-Parser zur Datenbereinigung implementiert.
>   2. Browser-Freeze beim Rendern tausender Graphknoten ➔ **Depth-1 Ego-Network-Virtualisierung** senkt Latenz um 98%.
>   3. Doppelte Alarme bei Polling ➔ **SHA-256-Fingerprint-Hashes** garantieren Idempotenz.
> - **Fertiges Portal**: Inspector Web Portal v2.0 mit 13/13 bestandenen Integrationstests freigegeben.

{/* truncate */}

---

### ⚠️ Rechtlicher Hinweis & Anonymisierung (Legal Notice)

> **[Hinweis] Alle Vorgänge wurden zum Schutz der Beteiligten vollständig anonymisiert.**  
> Behörden (`Behörde A`), Unternehmen (`Firma A`), Vertragsnummern und Adressen wurden durch Pseudonyme und Maskierungen ersetzt.

---

### 1. 3D-Sektorpartitionierung und Live-Stream-Architektur

```mermaid
flowchart TD
    subgraph DataStream ["Stufe 1: Echtzeit-Datenstrom & Resilienz"]
        A[Vergabe-Live-API] --> B[Caret ^ Parser]
        B --> C[SHA-256 Deduplizierung]
        C --> D[(SQLite Puffer-Warteschlange)]
    end

    subgraph PartitionEngine ["Stufe 2: 3D-Partitions-Engine"]
        D --> E{3D-Matrixfilter<br/>Behörde × Posten × Vergabeart}
        E -->|85% Routineaufwand| F[Niedrigrisiko-Archiv]
        E -->|Hochrisikoziele| G[Sektor 1: ICT-Stückelungsverträge]
        E -->|Hochrisikoziele| H[Sektor 2: Event-Kartelle]
        E -->|Hochrisikoziele| I[Sektor 3: Fördergeldabfluss]
    end

    subgraph InspectorPortal ["Stufe 3: Prüfer-Webportal v2.0"]
        G --> J[Orchestrierungs-Pipeline]
        H --> J
        I --> J
        J --> K[Vis.js Ego-Network]
        J --> L[10-Jahres-Präzedenzdatenbank]
        J --> M[HWPX-Kostenprüfung]
        J --> N[Dossier-Export]
    end
```

---

### 2. Vorhersehbare Herausforderungen & Fehlerbehebung

1. **3D-Sektorpartitionierung**: Eliminierte 85% des Rauschens über "Behördentyp × Budgetposten × Vergabeform".
2. **Caret-Trennzeichen (`^`)**: Gelöst durch Typ-strikte Entpackung zusammengesetzter Alt-Felder.
3. **UI-Einfrieren im Browser**: Gelöst durch bedarfsgesteuertes Nachladen unmittelbarer Nachbarknoten (Depth-1).
4. **SHA-256-Hashes**: Verhinderten Mehrfacheinträge und redundante Alarme bei API-Zustandsänderungen.

---

### 3. Prüfer-Portal v2.0 & Volle Verifizierung

Das Webportal (`http://localhost:8088`) bietet interaktive Kartellerkennung und Rechtsauswertungen, bestätigt durch 13/13 bestandene E2E-Tests.
