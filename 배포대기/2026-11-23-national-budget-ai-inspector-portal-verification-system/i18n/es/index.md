---
slug: national-budget-ai-inspector-portal-verification-system
title: "IA de Presupuesto #6: Portal Web de Auditoría y 20 Tests"
authors: [jbgih]
tags: [ai-agents, web-portal, test-automation, full-verification, audit-intelligence, devops]
date: 2026-11-23
keywords: ["Portal Web de Auditoría", "Grafos Vis.js", "Parser HWPX", "Verificación 20 tests", "IA presupuestaria final"]
description: "Episodio final: Portal Web de Auditoría v3.0 con grafos Vis.js, búsqueda de precedentes de 10 años, analizador HWPX y superación de 20 tests de verificación."
---

![National Budget Inspector Web Portal v3.0 & 20/20 Verification](./images/01_national_budget_inspector_portal.png)

> 💡 **Puntos Clave (Key Takeaways)**
> - **Inspector Web Portal v3.0 Construido**: Evolución de scripts CLI a una estación centralizada con 7 pestañas dedicadas (Panel General, 6 Sectores Objetivo, Redactor de Requerimientos, Subsidios, Grafos de Carteles, Análisis de Cortes y Precedentes con Parser HWPX).
> - **20 Tests Automatizados Aprobados al 100% (20/20 PASS)**: Superación impecable en toda la suite, desde Text-to-SQL y GraphRAG hasta streaming, carteles DART y validación de sobrecostos HWPX.
> - **2 Desafíos Prevenidos en Diseño**: (1) Cuello de botella en servidor resuelto mediante desacoplamiento en 12 endpoints RESTful DTO, (2) Saturación de memoria DOM mitigada con búfer circular (Circular DOM Ring Buffer).
> - **3 Errores Inesperados en Producción**: (1) Congelación de Vis.js resuelta congelando la física tras estabilización, (2) Bloqueo del bucle de eventos por parsing HWPX resuelto con ThreadPoolExecutor, (3) Bloqueo de archivos SQLite resuelto con aislamiento en memoria por proceso.
> - **Gran Final de la Serie de 6 Episodios**: Demostración de fiabilidad de nivel de producción en la protección fiscal pública.

{/* truncate */}

---

### ⚖️ Aviso Legal y Anonimización (Legal Notice & Anonymization)

> Todos los nombres de organismos (`Agencia A`, `Corporación C`), empresas (`Alfa IT`, `Beta Consultoría`), personas (`Sr. K`, `Sra. P`) y números de contrato (`CNTR-2026-○○○○`) han sido anonimizados al 100% para evitar disputas legales.

---

### A lo largo de los 5 episodios anteriores, nuestro equipo superó desafíos monumentales en la auditoría fiscal:

1. **Episodio #1: Prototipo Text-to-SQL y GraphRAG.**
1. **Episodio #2: Evaluación de más de 400 casos frente a 10 años de jurisprudencia.**
1. **Episodio #3: Partición en 3D que elimina el 85% del ruido en 4 millones de compras.**
1. **Episodio #4: Detección de carteles de empresas fantasma con DART.**
1. **Episodio #5: Desmantelamiento de fraccionamientos de $40K (Sector 5) y vertido de fin de año (Sector 6).**

> "Los auditores necesitan una consola unificada donde ver anomalías en tiempo real, explorar redes corporativas y generar requerimientos legales con un solo clic."

Presentamos el Inspector Web Portal v3.0 y la verificación completa de los 20 tests automatizados.

---

### 1. Arquitectura de Inspector Web Portal v3.0 y 7 Espacios de Trabajo

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

- **Centro de Mando Ejecutivo (`/api/stats`, `/api/alerts`)**: Métricas y asistente AI.
- **Matriz de 6 Sectores (`/api/sectors`)**: Filtrado multidimensional en tiempo real.
- **Generador de Requerimientos (`/api/summons`)**: Redacción automática de actas legales.
- **Rastreador de Subsidios (`/api/subsidy_fraud`)**: Fraudes en subvenciones públicas.
- **Grafo de Carteles Vis.js (`/api/bidding_rings`, `/api/graph`)**: Redes de colusión interactiva.
- **Analizador de Recortes Presupuestarios (`/api/budget_cuts`)**: Recomendaciones parlamentarias.
- **Base de Precedentes y Parser HWPX (`/api/precedents`, `/api/hwpx_analysis`)**: Detección de sobrecostos.

---

### 2. Dos Desafíos Anticipados y Prevenidos

#### 📌 Desafío 1: Cuellos de botella por acoplamiento monolítico de motores de auditoría
* Desacoplamos la capa web mediante 12 endpoints DTO normalizados, aislando fallos de servicios pesados.

#### 📌 Desafío 2: Saturación del DOM y fugas de memoria en streaming en vivo
* Implementamos un búfer circular de 100 nodos, manteniendo la memoria del navegador bajo 120MB.

---

### 3. Tres Errores Inesperados en Producción y su Solución

#### 🐛 Error 1: Oscilación infinita en Vis.js y bloqueo del navegador
* Al superar 50 nodos, las fuerzas divergieron. Lo solucionamos congelando la física al recibir `stabilizationIterationsDone`.

```javascript
// Stabilization freeze pattern
network.on("stabilizationIterationsDone", function () {
    network.setOptions({ physics: { enabled: false } });
    console.log("[Portal] Vis.js physics stabilized and frozen.");
});
```

#### 🐛 Error 2: Bloqueo del servidor HTTP al analizar HWPX de 50 páginas
* Delegamos la descompresión y análisis XML a un ThreadPoolExecutor en segundo plano.

#### 🐛 Error 3: Bloqueo de base de datos SQLite en 20 tests paralelos
* Creamos un pool de aislamiento con bases de datos temporales vinculadas al PID del proceso.

---

### 4. Resumen de Verificación: 20/20 Tests Aprobados

Toda la suite pasó con éxito, garantizando solidez de punta a punta.

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

### 5. Conclusión: El Futuro de la Auditoría Pública con Agentes IA

Demostramos que uniendo conocimiento de dominio, grafos y pruebas automatizadas, los agentes IA son guardianes fiables de las finanzas públicas.
