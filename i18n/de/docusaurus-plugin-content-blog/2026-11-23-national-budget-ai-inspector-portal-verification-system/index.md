---
slug: national-budget-ai-inspector-portal-verification-system
title: "KI-Haushaltsprüfung #6: Webportal & 20/20 Testsuite"
authors: [jbgih]
tags: [ai-agents, web-portal, test-automation, full-verification, audit-intelligence, devops]
date: 2026-11-23
keywords: ["Prüfer-Webportal", "Vis.js-Wissensgraph", "HWPX-Dokumentenparser", "20 Verifikationstests", "KI-Haushaltsprüfung Finale"]
description: "Das Finale: Auditor-Webportal v3.0 mit Vis.js-Wissensgraphen, 10-Jahre-Urteils-DB, HWPX-Parser und 100% bestandenen 20 End-to-End-Verifikationstests."
---

![National Budget Inspector Web Portal v3.0 & 20/20 Verification](./images/01_national_budget_inspector_portal.png)

> 💡 **Wichtigste Erkenntnisse (Key Takeaways)**
> - **Auditor-Webportal v3.0 Fertiggestellt**: Umwandlung einzelner CLI-Skripte in eine Echtzeit-Kommandozentrale mit 7 Reitern (Übersicht, 6 Sektoren, Vorladungsgenerator, Subventionen, Kartellgraphen, Haushaltskürzung und Urteils-DB mit HWPX-Parser).
> - **100% Bestehensquote in 20 automatisierten Tests (20/20 PASS)**: Lückenlose Validierung von Text-to-SQL über GraphRAG bis hin zu DART-Registern und HWPX-Preispunkten.
> - **2 Vorbeugende Entwurfsentscheidungen**: (1) Entkopplung heterogener Module über 12 normalisierte RESTful-DTO-Endpunkte, (2) Begrenzung des DOM-Speicherverbrauchs via zirkulärem Puffer (Circular DOM Ring Buffer).
> - **3 Unerwartete Fehler in der Praxis behoben**: (1) Einfrieren von Vis.js durch sofortiges Einfrieren der Physik nach Stabilisierung behoben, (2) Blockierung des Event-Loops bei 50-seitigen HWPX-Dateien durch ThreadPoolExecutor gelöst, (3) SQLite-Dateisperren bei parallelen Tests durch prozessisolierte Datenbanken eliminiert.
> - **Großes Finale der 6-teiligen Serie**: Nachweis produktionsreifer Zuverlässigkeit im öffentlichen Finanzwesen.

{/* truncate */}

---

### ⚖️ Rechtlicher Hinweis und Anonymisierung (Legal Notice & Anonymization)

> Alle Behörden (`Behörde A`), Unternehmen (`Alpha IT`, `Beta Consulting`), Personen (`Herr K`, `Frau P`) und Vertragsnummern (`CNTR-2026-○○○○`) wurden zum Schutz vor rechtlichen Streitigkeiten zu 100% anonymisiert.

---

### In den letzten 5 Episoden haben wir zentrale Herausforderungen der Haushaltsprüfung gelöst:

1. **Episode #1: Text-to-SQL & GraphRAG Baseline.**
1. **Episode #2: 400+ Testfälle im Abgleich mit 10 Jahren Rechtsprechung.**
1. **Episode #3: 3D-Sektorpartitionierung filtert 85% Hintergrundrauschen.**
1. **Episode #4: Aufdeckung von Strohmann-Kartellen via DART-Register.**
1. **Episode #5: Gezielte Bekämpfung von 50-Mio.-Splittings (Sektor 5) und Jahresend-Dumping (Sektor 6).**

> „Prüfer brauchen eine integrierte Konsole, auf der Alarme in Echtzeit aufleuchten, Netzwerke interaktiv erkundet und rechtssichere Vorladungen mit einem Klick erzeugt werden.“

Wir präsentieren das Auditor-Webportal v3.0 und die vollständige Validierung über 20 Test-Harnische.

---

### 1. Architektur des Webportals v3.0 und 7 Arbeitsbereiche

```mermaid
flowchart TD
    subgraph Browser Frontend [Inspector Web Portal UI - Tailwind & Vis.js]
        Tab1[1. Executive Command Center]
        Tab2[2. 6-Sector Partitioning Matrix]
        Tab3[3. Summons Generation Engine]
        Tab4[4. Subsidy Fraud Tracker]
        Tab5[5. Bidding Ring & Co-bidding Graph]
        Tab6[6. Budget Cut Analyzer]
        Tab7[7. 10-Yr Precedents & Live HWPX Parser]
    end

    subgraph REST API Routing Layer [dashboard_server.py - 12 Normalized Endpoints]
        R1["/api/stats & /api/alerts"]
        R2["/api/sectors & /api/graph"]
        R3["/api/summons & /api/subsidy_fraud"]
        R4["/api/bidding_rings & /api/budget_cuts"]
        R5["/api/precedents & /api/hwpx_analysis"]
        R6["/api/evaluate & /api/export_report"]
    end

    subgraph Core Audit Engines [Public Budget AI Cluster]
        E1[Sector Partition Manager]
        E2[Corporate Registry Client - DART]
        E3[GraphRAG & Precedent Database]
        E4[HWPX Overbilling Validator]
        E5[Bidding Ring Detector]
        E6[Budget Cut Analyzer]
    end

    Tab1 & Tab2 & Tab3 & Tab4 & Tab5 & Tab6 & Tab7 <-->|RESTful JSON / SSE Streams| REST API Routing Layer
    REST API Routing Layer <--> Core Audit Engines
```

- **Leitstand & KI-Chat (`/api/stats`, `/api/alerts`)**: Echtzeit-Alarme und dialogorientierter KI-Prüfungsassistent.
- **6-Sektoren-Matrix (`/api/sectors`)**: Mehrdimensionale Filterung im Beschaffungsregister.
- **Vorladungs-Synthesizer (`/api/summons`)**: Automatisierte Erstellung formeller Prüfungsberichte.
- **Subventionsbetrugs-Tracker (`/api/subsidy_fraud`)**: Erkennung von Fördermittelmissbrauch.
- **Kartell-Wissensgraph (`/api/bidding_rings`, `/api/graph`)**: Interaktive Erkennung von Absprachen.
- **Haushaltskürzungsempfehlungen (`/api/budget_cuts`)**: Vorbereitung für den Haushaltsausschuss.
- **10-Jahre-Rechtsprechung & HWPX-Parser (`/api/precedents`, `/api/hwpx_analysis`)**: Sofortige Kostenprüfung.

---

### 2. Vorbeugend Gelöste Herausforderungen

#### 📌 Herausforderung 1: Server-Engpässe durch monolithische Kopplung
* Trennung der Präsentationsschicht von schweren Engines über 12 DTO-Endpunkte mit Caching.

#### 📌 Herausforderung 2: DOM-Überlastung bei Echtzeit-Datenströmen
* Ein zirkulärer Ringpuffer begrenzt die Tabellenzeilen auf 100 und hält den RAM unter 120MB.

---

### 3. Drei Unerwartete Praxisfehler und deren Behebung

#### 🐛 Fehler 1: Vis.js-Schwingungen und Browser-Einfrieren
* Ab 50 Knoten divergierte die Physik. Gelöst durch `physics: { enabled: false }` nach Stabilisierung.

```javascript
// Stabilization freeze pattern
network.on("stabilizationIterationsDone", function () {
    network.setOptions({ physics: { enabled: false } });
    console.log("[Portal] Vis.js physics stabilized and frozen.");
});
```

#### 🐛 Fehler 2: HWPX-Parsing blockiert HTTP-Hauptthread
* Auslagerung der XML-Dekodierung in einen ThreadPoolExecutor mit asynchronem Polling.

#### 🐛 Fehler 3: SQLite-Dateisperre bei parallelen Tests
* Einführung isolierter PID-basierter Datenbanken und `:memory:`-Instanzen.

---

### 4. Verifikationsbericht: 20/20 Tests Bestanden

Alle 20 Tests liefen fehlerfrei durch und bestätigen die Systemstabilität.

| # | Test Script | Scope | Status |
|---|---|---|:---:|
| 1 | `verify_prototype.py` | Text-to-SQL Baseline | **PASS** |
| 2 | `verify_pipeline.py` | Data Pipeline Ingestion | **PASS** |
| 3 | `verify_graph_and_rag.py` | Knowledge Graph & RAG | **PASS** |
| 4 | `verify_interactive_rag.py` | Multi-Turn AI Agent Context | **PASS** |
| 5 | `verify_streaming_monitor.py` | Real-Time Stream Anomaly | **PASS** |
| 6 | `verify_web_api.py` | 12 RESTful API Endpoints | **PASS** |
| 7 | `verify_live_api.py` | Mock Data Live Sync | **PASS** |
| 8 | `verify_batch_hwp.py` | Batch HWP/HWPX Document Parsing | **PASS** |
| 9 | `verify_case_matcher.py` | 10-Yr Precedent Semantic Matcher | **PASS** |
| 10 | `verify_e2e_orchestrator.py` | Multi-Agent Orchestration | **PASS** |
| 11 | `verify_web_portal_v2.py` | Web Portal v3.0 7-Tab Sync | **PASS** |
| 12 | `verify_live_sync_and_discovery.py` | Background Sync & Discovery | **PASS** |
| 13 | `verify_sector_partition.py` | 3D Sector Partition Engine | **PASS** |
| 14 | `verify_web_sectors.py` | Sector UI Data Transmission | **PASS** |
| 15 | `verify_daily_monitor.py` | Daily Midnight Audit Scheduler | **PASS** |
| 16 | `verify_sectors_5_6.py` | $40K Smurfing & Year-End Dumps | **PASS** |
| 17 | `verify_corporate_and_summons.py` | DART Registry & Summons Gen | **PASS** |
| 18 | `verify_subsidy_fraud.py` | Subsidy Fraud Detection | **PASS** |
| 19 | `verify_bidding_rings.py` | SOC Bidding Ring Detection | **PASS** |
| 20 | `verify_budget_cuts.py` | Budget Cut Analyzer | **PASS** |

```bash
$ python -X utf8 tools/run_all_tests.py
All 20 verification tests passed successfully! (20/20 PASS)
```

---

### 5. Fazit: Die Zukunft autonomer Prüfungs-KI

Die Kombination aus Domänenpartitionierung, Wissensgraphen und solider Softwaretechnik macht KI-Agenten zu verlässlichen Hütern öffentlicher Gelder.
