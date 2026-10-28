---
slug: national-budget-ai-inspector-portal-verification-system
title: "IA Budgétaire #6: Portail Web d'Audit et 20 Tests Réussis"
authors: [jbgih]
tags: [ai-agents, web-portal, test-automation, full-verification, audit-intelligence, devops]
date: 2026-11-23
keywords: ["Portail Web d"Audit", "Graphes Vis.js", "Parseur HWPX", "Vérification 20 tests", "IA budgétaire finale"]
description: "Le grand final: Portail Web d'Audit v3.0 intégrant graphes Vis.js, jurisprudence de 10 ans, parseur HWPX et validation à 100% des 20 tests de vérification."
---

![National Budget Inspector Web Portal v3.0 & 20/20 Verification](./images/01_national_budget_inspector_portal.png)

> 💡 **Points Clés (Key Takeaways)**
> - **Portail Web d'Audit v3.0 Achevé**: Remplacement des scripts CLI par une console intégrée à 7 onglets (Vue d'ensemble, 6 Secteurs, Générateur de convocations, Subventions, Graphe d'ententes, Analyse budgétaire et Jurisprudence avec parseur HWPX).
> - **100% de Réussite sur 20 Tests Automatisés (20/20 PASS)**: Validation complète couvrant Text-to-SQL, GraphRAG, streaming temps réel, cartels DART et surfacturations HWPX.
> - **2 Défis Anticipés et Prévenus**: (1) Goulots d'étranglement évités par découplage en 12 points de terminaison RESTful DTO, (2) Saturation du DOM évitée par un tampon circulaire (Circular DOM Ring Buffer).
> - **3 Bogues Inattendus Résolus**: (1) Oscillation infinie de Vis.js résolue en figeant la physique après stabilisation, (2) Blocage du thread HTTP par HWPX résolu avec ThreadPoolExecutor, (3) Verrous de fichiers SQLite résolus par isolation en mémoire par processus.
> - **Apothéose de la Série en 6 Épisodes**: Démonstration d'une fiabilité éprouvée au service des finances publiques.

{/* truncate */}

---

### ⚖️ Avis Juridique et Anonymisation (Legal Notice & Anonymization)

> Toutes les institutions publiques (`Organisme A`), entreprises (`Alpha IT`), personnes (`M. K`) et références de marchés (`CNTR-2026-○○○○`) sont rigoureusement pseudonymisées.

---

### Au cours des 5 épisodes précédents, nous avons franchi des étapes cruciales :

1. **Épisode #1: Prototype Text-to-SQL et GraphRAG.**
1. **Épisode #2: Évaluation sur 400 dossiers face à 10 ans de jurisprudence.**
1. **Épisode #3: Partition 3D éliminant 85% du bruit sur 4 millions d'achats.**
1. **Épisode #4: Révélation des cartels de prête-noms avec les registres DART.**
1. **Épisode #5: Démantèlement des fractionnements à 50M (Secteur 5) et du dumping de fin d'année (Secteur 6).**

> « Les auditeurs ont besoin d'un centre opérationnel où les alertes s'affichent en temps réel, où les cartels s'explorent en graphes et où un dossier HWPX produit instantanément une convocation motivée. »

Voici le Portail Web d'Audit v3.0 et la validation exhaustive de ses 20 bancs d'essai.

---

### 1. Architecture du Portail Web v3.0 et 7 Espaces Dédiés

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

- **Centre de Contrôle & Chat IA (`/api/stats`, `/api/alerts`)**: Métriques temps réel et assistant conversationnel.
- **Matrice des 6 Secteurs (`/api/sectors`)**: Filtrage multicritère sur les marchés publics.
- **Générateur de Convocations (`/api/summons`)**: Rédaction automatisée avec visa légal.
- **Traçage des Subventions (`/api/subsidy_fraud`)**: Détection des détournements d'aides publiques.
- **Graphe Vis.js des Cartels (`/api/bidding_rings`, `/api/graph`)**: Cartographie interactive des ententes.
- **Analyseur de Coupes Budgétaires (`/api/budget_cuts`)**: Recommandations pour la commission des finances.
- **Jurisprudence & Parseur HWPX (`/api/precedents`, `/api/hwpx_analysis`)**: Détection des surcoûts.

---

### 2. Deux Défis Anticipés et Prévenus

#### 📌 Défi 1: Engorgement du serveur par couplage monolithique des moteurs
* Découplage de la couche HTTP via 12 points d'accès DTO normalisés assurant la continuité de service.

#### 📌 Défi 2: Explosion de la mémoire du navigateur lors du streaming continu
* Mise en place d'un tampon circulaire borné à 100 entrées, maintenant la mémoire sous 120 Mo.

---

### 3. Trois Bogues de Production et leurs Solutions

#### 🐛 Bogue 1: Oscillation infinie Vis.js et gel du navigateur
* Au-delà de 50 nœuds, les forces divergeaient. Résolu en désactivant la physique dès `stabilizationIterationsDone`.

```javascript
// Stabilization freeze pattern
network.on("stabilizationIterationsDone", function () {
    network.setOptions({ physics: { enabled: false } });
    console.log("[Portal] Vis.js physics stabilized and frozen.");
});
```

#### 🐛 Bogue 2: Analyse HWPX de 50 pages bloquant la boucle HTTP
* Délégation du traitement XML lourd à un ThreadPoolExecutor en arrière-plan avec suivi asynchrone.

#### 🐛 Bogue 3: Conflit de verrou SQLite lors des tests parallèles
* Instanciation de bases isolées par identifiant de processus (PID) et en mémoire pure `:memory:`.

---

### 4. Bilan des Tests: 20/20 Réussites

L'intégralité des 20 bancs d'essai s'est conclue par un statut PASS.

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

### 5. Conclusion: L'Avenir de l'Ingénierie d'Audit Autonome

En associant vision métier, graphes de connaissances et rigueur logicielle, les agents IA deviennent de véritables remparts pour les deniers publics.
