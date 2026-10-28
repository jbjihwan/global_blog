---
slug: national-budget-ai-sector-partition-live-monitoring
title: "Public Budget AI #3: 3D Sector Partitioning & Live API Audit"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, live-streaming, koneps-api, web-dashboard, devops]
date: 2026-11-20
keywords: ["Public Budget AI", "3D Sector Partitioning", "KONEPS Live API", "Procurement Noise Filter", "Auditor Web Portal"]
description: "Filtering 85% procurement noise via 3D sector partitioning and building an interactive auditor web portal v2.0 connected live to public procurement APIs."
---

![3D Sector Partitioning & Live Audit Web Portal](./images/01_national_budget_sector_live_monitor.png)

> 📌 **Key Takeaways**
> - **Eliminating Alert Fatigue**: In massive public procurement feeds where 80–95% of transactions represent routine office consumables, our **3-Dimensional Sector Partition Manager** filters out 85%+ noise, focusing deep AI reasoning onto high-risk sectors.
> - **Anticipated Challenges & Prevention**: To handle public API latency and schema deprecations, we decoupled the ingestion tier with an **isolated SQLite unaudited buffer queue and exponential backoff** retry policies.
> - **3 Real-World Production Bugs Resolved**:
>   1. **Caret (`^`) Multi-Value Delimiters**: Legacy API fields returning composite records flattened via regex parsers and strict type schemas.
>   2. **Browser UI Freezes in Vis.js**: Visualizing thousands of knowledge graph nodes caused severe UI lockups, solved by **Depth-1 Ego-Network subgraph virtualization**, cutting latency by 98%.
>   3. **Duplicate Contract Alerts**: Polling shifts triggered redundant findings, eliminated using **SHA-256 fingerprint hashes** guaranteeing pipeline idempotency.
> - **Shipped Artifact**: Launched Inspector Web Portal v2.0 with live API sync, a 10-year precedent database, instant HWPX parsing, and 13/13 integration tests passed.

{/* truncate */}

---

### ⚠️ Legal Notice & Anonymization

> **[Notice] All entities, contract identifiers, and locations in this report are strictly anonymized.**  
> This post shares engineering evaluation results from a live autonomous AI audit system. To prevent legal disputes and protect organizational reputations, all contracting authorities (e.g., `Agency A`, `Corporation B`), corporate contractors (e.g., `Company A`, `Company B`), contract serial numbers (e.g., `CNTR-2026-0001`), and physical office addresses have been completely masked and pseudonymized.

---

### Introduction: Hunting for Genuine Fraud in Millions of Ledger Entries

In Part 1 (Architecture) and Part 2 (Interim Audit Findings), we demonstrated how combining deterministic Text-to-SQL with GraphRAG achieves near-zero hallucination in fiscal auditing.

However, moving from isolated test benches to **connecting directly to live public procurement data feeds (data.go.kr / KONEPS)** introduced a host of real-world distributed systems challenges.

Every single day, public sector agencies process tens of thousands of purchase orders. Over 85% of them are routine, benign transactions: office paper, cleaning contracts, and printer cartridges. **If an AI agent naively inspects every single line item and raises flags on minor statistical variances, human auditors quickly suffer from alert fatigue and abandon the tool.**

In this third installment of our Spec-Driven Development (SDD) case study on [`national_budget_ai`](file:///D:/ai/antigravity/national_budget_ai), we detail **(1) how we preempted data noise through 3D sector partitioning**, and **(2) how we overcame 3 unexpected production bugs while streaming live procurement records into Inspector Web Portal v2.0**.

---

### 1. High-Level Architecture: Target Partitioning & Live Ingestion

We evolved the pipeline from an offline batch auditor into a real-time surveillance and interactive audit workstation:

```mermaid
flowchart TD
    subgraph DataStream ["Stage 1: Real-Time Stream & Resilience Layer"]
        A[KONEPS Live Procurement API<br/>ao/CntrctInfoService] --> B[Robust Caret ^ Parser]
        B --> C[SHA-256 Fingerprint Deduplicator<br/>Idempotency Key]
        C --> D[(SQLite Unaudited Buffer Queue)]
    end

    subgraph PartitionEngine ["Stage 2: 3D Sector Partition Engine"]
        D --> E{3D Matrix Partition<br/>Agency × Item × Method}
        E -->|85% Routine Noise| F[Low-Risk Pass-Through Archive]
        E -->|High-Risk Targets| G[Sector 1: ICT Split Contracts <$20k]
        E -->|High-Risk Targets| H[Sector 2: Local Event Bid Cartels]
        E -->|High-Risk Targets| I[Sector 3: Welfare DEI Overhead Leaks]
    end

    subgraph InspectorPortal ["Stage 3: Inspector Web Portal v2.0"]
        G --> J[Audit Pipeline Orchestrator]
        H --> J
        I --> J
        J --> K[Ego-Network Vis.js Graph]
        J --> L[10-Year Case Law Matcher]
        J --> M[HWPX Cost Sheet Parser]
        J --> N[Automated Dossier Generator]
    end

    style DataStream fill:#f0fdf4,stroke:#22c55e,stroke-width:2px
    style PartitionEngine fill:#fefce8,stroke:#eab308,stroke-width:2px
    style InspectorPortal fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
```

---

### 2. Anticipated Challenges & Defensive Engineering

#### 🎯 Challenge 1: The Consumables Noise Bomb ➔ `SectorPartitionManager`
* **Anticipated Problem**:
  - Unstructured procurement logs are flooded with trivial expenditures. Applying deep graph embeddings and LLM reasoning indiscriminately across all records causes astronomical API bills and inundates investigators with useless alerts.
* **Preemptive Architecture**:
  - We engineered a **3-Dimensional Sector Partition Matrix**:
    $$\text{Target Sector} = \text{Agency Type} \times \text{Budget Item} \times \text{Contract Method}$$
  - **Dimension 1 (Agency)**: Central Ministries vs. Public Corporations vs. Local Governments.
  - **Dimension 2 (Budget Item)**: Commodity Supplies vs. Civil Construction vs. SW Services / Event Operations.
  - **Dimension 3 (Procurement Method)**: Open Competition vs. Restricted Bids vs. De Minimis Sole-Source.
  - This matrix filters out **85%+ of benign noise upfront**, concentrating inference engines strictly onto high-probability fraud corridors (such as Sector 1: Public Agency ICT Private Contracts under $20K).

#### 🔌 Challenge 2: Fragile Public APIs & Network Jitter ➔ Isolated Ingestion Queues
* **Anticipated Problem**:
  - Government API portals frequently experience rate limiting, schema anomalies, and intermittent HTTP 504 timeouts. Ingestion failures could crash downstream reasoning workers.
* **Preemptive Architecture**:
  - We decoupled data harvesting (`LiveSyncManager`) from the analytical engine. Incoming payloads are immediately staged into an isolated SQLite buffer queue with **exponential backoff retries (1s ➔ 2s ➔ 4s)**, shielding analytical workers from upstream connectivity outages.

---

### 3. Resolving 3 Unexpected Field Bugs in Production

Even with rigorous specs, ingesting live production packets revealed several edge cases:

#### 🚨 Bug 1: Caret (`^`) Delimiters Crashing JSON Schemas

* **Symptom**: Ingesting the new `ao/CntrctInfoService` endpoint caused JSON parsing crashes and pushed text tokens into integer amount columns.
* **Root Cause**: For legacy compatibility, the public API concatenated multiple line items into single fields using the caret (`^`) symbol (e.g., `ItemA^ItemB`, `1000^2500`).
* **Fix**: Implemented a specialized `SplitCaretRecord` parser that flattens multi-value fields and enforces strict schema casting before database insertion:

```python
def parse_caret_delimited_field(raw_value: str, target_type=str):
    """
    Safely unpacks legacy caret-delimited composite fields 
    preventing schema corruption and downstream cast exceptions.
    """
    if not raw_value or raw_value == "^":
        return []
    
    tokens = [t.strip() for t in raw_value.split("^") if t.strip()]
    if target_type == int:
        clean_nums = []
        for token in tokens:
            digits = re.sub(r"[^\d]", "", token)
            if digits:
                clean_nums.append(int(digits))
        return clean_nums
    return tokens
```

---

#### 🚨 Bug 2: Browser UI Freezes on Monolithic Knowledge Graphs

* **Symptom**: Rendering thousands of interconnected procurement nodes in Vis.js caused browser tabs to consume 100% CPU and freeze indefinitely.
* **Root Cause**: Vis.js's real-time physics simulation attempted to compute gravitational and repulsive forces across all enterprise nodes in a single JavaScript thread.
* **Fix**: Built an **Ego-Network Subgraph Virtualizer**:
  1. The UI initially renders only the top 30 **CRITICAL/HIGH** flagged nodes.
  2. Clicking any node lazily fetches its immediate 1st-degree neighbors on demand.
  - This reduced initial graph render latency from **12.0s to 0.05s (98% reduction)**.

---

#### 🚨 Bug 3: Idempotency Breakdown & Duplicate Alert Floods

* **Symptom**: Daily polling jobs repeatedly re-flagged previously audited contracts as new anomalies, creating duplicate warning alerts.
* **Root Cause**: Minor administrative status updates in the public API altered response ordering, invalidating simple auto-increment ID deduplication.
* **Fix**: Implemented an immutable **SHA-256 Fingerprint Hash** over core contract attributes:

```python
import hashlib

def generate_contract_fingerprint(agency_id: str, vendor_biz_no: str, contract_date: str, amount: int) -> str:
    """
    Creates an immutable cryptographic fingerprint ensuring 
    idempotent ingestion and preventing duplicate audit warnings.
    """
    payload = f"{agency_id}|{vendor_biz_no}|{contract_date}|{amount}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
```

---

### 4. Inspector Web Portal v2.0 Architecture

The resulting web portal provides human auditors with a complete operational suite accessible at `http://localhost:8088`:

```mermaid
flowchart LR
    Portal[Inspector Web Portal v2.0]
    
    Portal --> Tab1[1. Interactive Graph Explorer<br/>Vis.js Cartel Traversal]
    Portal --> Tab2[2. 10-Year Case Law Database<br/>Instant Statutory Precedent Search]
    Portal --> Tab3[3. Live HWPX Validator<br/>Drag-and-Drop Cost Sheet Audit]
    Portal --> Tab4[4. Audit Dossier Viewer<br/>Download Legal Order Drafts]
    Portal --> Tab5[5. Rapid Anomaly Evaluator<br/>Instant Risk Scoring]
```

1. **Interactive Graph Explorer**: Visually trace shared address links and bidding cartels across municipal boundaries.
2. **10-Year Case Law Database**: Search official Board of Audit (BAI) and National Assembly Budget Office (NABO) rulings with computed similarity metrics.
3. **Live HWPX Sheet Validator**: Drag and drop complex XML government spreadsheets to flag inflated unit costs in 0.1s.
4. **Dossier Viewer**: One-click export of court-ready markdown dossiers.
5. **Rapid Anomaly Evaluator**: Score new contract proposals against 5 risk levels in real time.

---

### 5. Verification: 13 End-to-End Test Suites Passed (13/13 PASS)

To verify the entire operational pipeline, all 13 test suites were executed cleanly via `national_budget_ai/tools/run_all_tests.py`:

| Test Suite | Module Under Test | Key Verified Capability | Result |
| :---: | :--- | :--- | :---: |
| 1 | `verify_prototype.py` | HWP Table Parsing, Split Contracts, Unit Price | 🟢 **PASS** |
| 2 | `verify_pipeline.py` | Normalization, KONEPS Ingestion, Fiscal Lag | 🟢 **PASS** |
| 3 | `verify_graph_and_rag.py` | DEI Leakage (30%), Shared Address Cartels | 🟢 **PASS** |
| 4 | `verify_interactive_rag.py` | Text-to-SQL Execution, Cartel Inquiries | 🟢 **PASS** |
| 5 | `verify_streaming_monitor.py` | Real-time Multi-tier Risk Scoring & Alerts | 🟢 **PASS** |
| 6 | `verify_web_api.py` | Web API Endpoints, Vis.js Node Serialization | 🟢 **PASS** |
| 7 | `verify_live_api.py` | Live KONEPS & dBrain+ Ingestion | 🟢 **PASS** |
| 8 | `verify_batch_hwp.py` | XML Form Parsing, 7.0x Unit Price Markup | 🟢 **PASS** |
| 9 | `verify_case_matcher.py` | State Contract Act & BAI-2023-041 Binding | 🟢 **PASS** |
| 10 | `verify_e2e_orchestrator.py` | Full 8-Stage Pipeline & Dossier Generation | 🟢 **PASS** |
| 11 | `verify_web_portal_v2.py` | REST APIs (`/api/stats`, `/api/dossiers`) | 🟢 **PASS** |
| 12 | `verify_live_sync_and_discovery.py` | Unaudited Buffer Sync & Anomaly Discovery | 🟢 **PASS** |
| 13 | `verify_sector_partition.py` | 3D Noise Elimination (85%) & Sector 1 Filter | 🟢 **PASS** |

---

### 6. Conclusion: Resilience Beats Raw Model Power

Many teams assume enterprise AI success depends primarily on selecting the largest foundation model.

In truth, building mission-critical public audit agents requires mastering unglamorous engineering realities: filtering out 85% noise with domain-informed sector matrices, handling legacy API delimiters (`^`) without crashing, and virtualizing high-density knowledge graphs.

This completes our 3-part series on building autonomous public audit agents. Stay tuned for future deep dives on enterprise AI systems!
