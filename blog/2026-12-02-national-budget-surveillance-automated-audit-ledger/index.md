---
slug: national-budget-surveillance-automated-audit-ledger
category_l1: practice
category_l2: ai
category_l3: project-budget
title: "Public Budget AI #9: Budget Anomaly Audit Engine Simulation"
authors: [jbgih]
tags: [budget-ai, anomaly-detection, automated-audit, legal-tech, sqlite-wal, devops, public-finance, practice, ai, budget-audit]
date: 2026-12-02
keywords: ["Public Budget AI Surveillance", "23825 Anomaly Sub-items Audit", "5-Option Decision Engine", "SQLite WAL High Throughput", "Cumulative Audit Ledger", "Fiscal Sanction Automation"]
description: "[Simulation] Automating review of 23,825 synthetic budget anomalies: a 5-option decision matrix, SQLite WAL batch pipeline and ledger."
---
> **Simulation notice — synthetic data**
> - This post describes a **simulation built on synthetic (generated) data**. The "findings", sanctions, recovery amounts and counts are not real audit results.
> - Every agency, company, region, amount and document number is **anonymized or replaced with a fictional value**; any resemblance to real entities is unintended.
> - Error logs, code excerpts and benchmark figures were **reconstructed to explain the design** and may not match the repository's run records or current implementation.
> - Apart from limited calls to the public procurement (KONEPS) and Open Fiscal Data APIs, the data sources named here (DART, corporate registries, e-Hojo+, K-EduFine, ALIO, NTIS, etc.) were **not connected**. A rebuild on public open data is in progress; its results will be published only as "statistical anomaly indicators", never as accusations.

![Public Budget AI #9 Cover](./images/01_cover.png)

> 💡 **Executive Summary (TL;DR)**
> - **The Target**: Scaling automated fiscal surveillance to all **23,825 anomaly sub-items** detected across the 677.4 trillion KRW South Korean national budget, executing standardized decisions via a **5-Option Matrix** (full cut, mediation adjustment, 48-hour minister summons, criminal prosecution, legitimate exception pass).
> - **Real Engineering Pitfalls Encountered**: 
>   1. `sqlite3.OperationalError: database is locked` and I/O starvation under rapid multi-record ingestion.
>   2. Double-dipping risk cascades where multi-category violations produced aggregate cut recommendations exceeding 100% of the allocated budget.
>   3. Markdown table rendering corruption and Jinja2 syntax crashes during minister summons dossier generation due to unescaped pipes and quotes in procurement titles.
> - **Clean Production Fixes**:
>   1. Switched SQLite to `WAL` mode with `PRAGMA synchronous = NORMAL`, batching commits into 1,000-case transaction chunks, boosting throughput to 95,000 inferences/sec (total playback in 0.25 seconds).
>   2. Built a deterministic `PriorityDecisionArbiter` with criminal law priority overrides and hard invariant clamping (`clamp(cut, 0, budget * 0.70)`).
>   3. Implemented a robust legal-clause cross-referencing normalizer and safe markdown serializer for the permanent ledger, locking in 121.72 trillion KRW in provisional savings across 23,911 verified cases.

{/* truncate */}

---

### 1. Target & Architecture: Eliminating the Human Inspector Bottleneck

In our previous milestones ([Public Budget AI #7](https://globaldevlog.com/blog/national-budget-local-subsidy-ehojo-audit) and [#8](https://globaldevlog.com/blog/national-budget-education-grant-audit)), we audited discrete fiscal domains: 243 municipal local subsidies (e-Hojo+) and 17 provincial education offices (K-EduFine). However, analyzing the full central government expenditure (677.4 trillion KRW) surfaced **23,825 flagged sub-items** across 55 ministries and agencies.

```text
+--------------------------------------------------------------------------------------------------+
|                            23,825 Central Budget Sub-items Surveillance                          |
+--------------------------------------------------------------------------------------------------+
                                                │
                                                ▼
       ┌─────────────────────────────────────────────────────────────────────────────────┐
       │             4-Risk Category Classifier (Rule & Statistical Engine)             │
       │  1. Sluggish Exec (>30% Disused)   2. Private Consign (Overhead Leakage)         │
       │  3. Wasteful Services (Inflated)   4. Q4 Dump & Cartel (Bid-Rigging §315)        │
       └─────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
       ┌─────────────────────────────────────────────────────────────────────────────────┐
       │             Standard 5-Option Decision Engine (Deterministic Matrix)            │
       │  • Option 1: Approve Full Cut (100% System Recommendation)                      │
       │  • Option 2: Direct Mediation Cut (50% Operational Compromise)                  │
       │  • Option 3: Issue 48h Formal Minister Summons Query (Assembly Subpoena)        │
       │  • Option 4: Criminal Prosecution Dispatch (Specific Economic Crimes Act)       │
       │  • Option 5: Legitimate Execution (Disaster / Inevitable Exemption Pass)        │
       └─────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼
       ┌─────────────────────────────────────────────────────────────────────────────────┐
       │             High-Throughput Storage & Immutable Ledger Generator                │
       │  • SQLite3 Engine (WAL Mode, In-Memory Buffer, 1k Chunk Commits)                │
       │  • Live Audit Ledger: CUMULATIVE_SURVEILLANCE_AUDIT_LEDGER.md                   │
       │  • Cumulative Cut: 121,718,409,348,635 KRW (121.72 Trillion KRW)                │
       └─────────────────────────────────────────────────────────────────────────────────┘
```

#### Core Operational Requirements
1. **Zero Human Inspector Bottleneck**: Auditing 23,825 cases manually takes ~11,900 human hours (30 minutes/case). The engine must ingest, evaluate, and assign statutory sanction recommendations across all cases in under 1 second.
2. **Immutable Traceability**: Every audited item must store all 5 evaluation options, the chosen verdict, statutory citations, and ministerial summons text in both a normalized relational database (`surveillance_review_log`) and a portable, version-controlled markdown ledger.
3. **Statutory Integrity**: Decisions must cross-reference applicable provisions of the National Finance Act (§45, §89), State Contract Act (§7, §27), Public Finance Recovery Act (§8), and Criminal Act (§315).

---

### 2. Real Engineering Pitfalls & Runtime Errors

#### Pitfall 1: SQLite Lock Deadlock & Disk Starvation (`database is locked`)

During our initial batch playback run across the 23,825 rows, the process aborted abruptly after processing case #3,412:

```text
sqlite3.OperationalError: database is locked
  File "D:\ai\antigravity\national_budget_ai\tools\run_surveillance_playback.py", line 142, in record_verdict
    cursor.execute("""
      INSERT OR REPLACE INTO surveillance_review_log (
        rank, case_id, ministry_name, budget_amount, potential_cut_amount, ...
      ) VALUES (?, ?, ?, ?, ?, ...)
    """, record)
sqlite3.OperationalError: database is locked
[FATAL] Pipeline halted at Case #3412. Progress: 14.32%.
```

* **Root Cause**: The default SQLite journal mode (`DELETE`) creates and destroys a rollback journal file on disk for every single `commit()`. Committing 23,825 times individually starved Windows OS file locks. When a background file indexer or reading thread touched the database file simultaneously, SQLite threw `OperationalError: database is locked`.

#### Pitfall 2: Compound Risk Conflicts & Budget Exceedance (`Double-Dipping`)

A significant number of sub-items suffered from compound pathologies. For example, Case `#1316576` (Ministry A, Smart Store Technology Supply) exhibited both **Q4 Dumping Risk (Score: 98)** and **Private Consignment Overhead Leakage (Score: 84)**.

```text
[ASSERTION FAILURE] Case #1316576:
  Allocated Budget:       50,000,000,000 KRW
  Calculated Option 1 Cut: 35,000,000,000 KRW (Dumping Penalty: 70%)
  Calculated Option 2 Cut: 20,000,000,000 KRW (Consignment Penalty: 40%)
  Aggregate Sum:          55,000,000,000 KRW > 50,000,000,000 KRW
ValueError: Proposed reduction (55.0B KRW) exceeds total project appropriation (50.0B KRW).
```

* **Root Cause**: Independent rule handlers evaluated violations sequentially without cross-category arbitration. Summing penalties across orthogonal heuristic rules produced absurd recommendations where the proposed budget cut exceeded the entire annual project budget.

#### Pitfall 3: Markdown Table Formatting Corruption & Jinja2 Template Crashes

To present the cumulative audit ledger to the National Assembly, the engine dynamically renders markdown tables containing the 5 evaluation options for each case. Sub-items containing pipe characters (`|`), quotes, or newline breaks in project descriptions shattered markdown tables:

```text
| 1316576 | Smart Store Tech | Direct Contract | 50B | Option 1 | Approve |
| 1316577 | R&D | Cloud | Edge | Next-Gen AI | 12B | Option 3 | Summons | <-- TABLE RUPTURED
```

* **Root Cause**: Unsanitized raw strings injected into markdown format strings created synthetic column delimiters, invalidating table column counts and crashing automated downstream PDF/HWPX compilation scripts.

---

### 3. Deep Root Cause & Production Fixes

#### Fix 1: SQLite WAL Mode, Synchronous Normal, and Chunk Transactions

We refactored the persistence layer by enabling Write-Ahead Logging (`WAL`), increasing memory cache, and wrapping commits into 1,000-item chunks.

```python
# Before (Synchronous Rollback Journal, Individual Commits):
conn = sqlite3.connect("surveillance_audit.db")
cursor = conn.cursor()
for case in all_cases:
    cursor.execute("INSERT OR REPLACE INTO surveillance_review_log ...", case)
    conn.commit()  # 23,825 disk write operations! 21.4 minutes elapsed.

# After (WAL Mode + 1,000 Case Chunk Commits):
conn = sqlite3.connect("surveillance_audit.db", timeout=60.0)
conn.execute("PRAGMA journal_mode = WAL;")
conn.execute("PRAGMA synchronous = NORMAL;")
conn.execute("PRAGMA cache_size = -64000;")  # 64MB In-Memory Cache
conn.execute("PRAGMA temp_store = MEMORY;")

cursor = conn.cursor()
BATCH_SIZE = 1000
for i in range(0, len(all_cases), BATCH_SIZE):
    chunk = all_cases[i : i + BATCH_SIZE]
    cursor.executemany("""
        INSERT OR REPLACE INTO surveillance_review_log (
            rank, case_id, ministry_name, detail_project_name, budget_subitem_name,
            budget_amount, executed_amount, disused_amount, risk_category, risk_score,
            potential_cut_amount, selected_option, all_options_json, decision,
            adjusted_cut_amount, legal_violations, summon_query, reviewer_note, reviewed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, chunk)
    conn.commit()
```

* **Result**: Total database write duration dropped from **21.4 minutes to 0.25 seconds**, achieving an ingestion rate of **95,644 rows/sec** with zero lock errors.

#### Fix 2: Priority Decision Arbiter and Clamped Budget Invariants

We introduced the `PriorityDecisionArbiter` class to resolve multi-category conflicts deterministically and enforce statutory clamping limits:

```python
class PriorityDecisionArbiter:
    # Hierarchy of legal sanctions: Criminal > Assembly Summons > Fiscal Reduction
    SEVERITY_HIERARCHY = [
        "연말몰아쓰기·덤핑위험",  # Option 1 + Option 4 (Prosecution)
        "민간위탁·간접비누수",    # Option 1 + Option 3 (Summons)
        "소모성용역·과대계상",    # Option 1 + Option 3 (Summons)
        "집행부진·고액불용"       # Option 1 + Option 3 (Summons)
    ]
    
    @classmethod
    def arbitrate_decision(cls, risk_categories: list[str], budget_amount: int, recommended_cut: int):
        # 1. Determine dominant risk category
        dominant_risk = next(
            (risk for risk in cls.SEVERITY_HIERARCHY if risk in risk_categories),
            "집행부진·고액불용"
        )
        
        # 2. Assign Statutory Verdict Option
        if dominant_risk == "연말몰아쓰기·덤핑위험":
            verdict = "선택지 1 (원안 감액 승인) + 선택지 4 (사법기관 정식 형사고발)"
        else:
            verdict = "선택지 1 (원안 감액 승인) + 선택지 3 (소관 부처 장관 소명 요구서 발부)"
            
        # 3. Hard Invariant Clamp: Never exceed 70% of project budget
        MAX_CUT_RATIO = 0.70
        clamped_cut = min(recommended_cut, int(budget_amount * MAX_CUT_RATIO))
        clamped_cut = max(clamped_cut, 0)
        
        return dominant_risk, verdict, clamped_cut
```

#### Fix 3: Sanitized Markdown Serializer for Table Formatting

To prevent table rupture, all strings entering the markdown generator pass through an HTML-entity normalizer:

```python
def sanitize_markdown_table_cell(text: str) -> str:
    if not text:
        return "-"
    # Escape pipe characters and remove breaking newlines
    cleaned = text.replace("|", "&#124;").replace("\n", " ").replace("\r", "")
    return cleaned.strip()
```

---

### 4. Verification & Production Benchmarks

The full automated surveillance audit pipeline was evaluated across the entire 2026 national budget dataset:

```text
================================================================================
           Public Budget AI #9: Automated Surveillance Audit Benchmark
================================================================================
Total Analyzed Sub-items:               23,825 Cases
Total Reviewed & Stacked Cases:         23,911 Cases (100.36% coverage)
Elapsed Execution Time:                 0.25 Seconds (Batch Engine)
Database Engine Mode:                   SQLite3 WAL Mode
Database Lock / Deadlock Incidents:     0 (100% Reliable)
Cumulative Confirmed Fiscal Cuts:       121,718,409,348,635 KRW (121.72 Trillion KRW)
Ministerial Summons Queries Issued:     18,432 Dossiers (Option 3)
Prosecution Criminal Referrals:          5,479 Dossiers (Option 4, Specific Economic Crimes)
Unassigned / Unresolved Cases:          0 Cases
Live Ledger File:                       reports/CUMULATIVE_SURVEILLANCE_AUDIT_LEDGER.md
================================================================================
```

#### Performance Comparison Table

| Metric | Manual Inspector Protocol | Pre-fix Engine (Naive Disk Sync) | Production Engine (WAL + Arbiter) |
| :--- | :---: | :---: | :---: |
| **Audit Processing Time** | ~11,900 Hours (495 Days) | 21.4 Minutes (Crash @ 14.3%) | **0.25 Seconds** |
| **Throughput (Cases/sec)** | ~0.0005 cases/sec | ~2.6 cases/sec | **95,644 cases/sec** |
| **Database Lock Failures** | N/A | 100% Failure Rate | **0 Incidents (Zero-Lock)** |
| **Multi-Risk Budget Overrun** | Occasional Human Drift | 1,280 Violations (>100% Cut) | **0 Violations (Clamped 70%)** |
| **Statutory Uniformity** | Subjective / Variable | Inconsistent Option Sets | **100% Standard 5-Option Matrix** |

---

### 5. Architectural Takeaways

1. **Deterministic Expert Systems over Pure LLM Inference for High-Volume Audits**: Passing 23,825 cases through commercial LLM APIs would incur over $4,500 in token costs and hours of latency. A hybrid architecture—where LLMs design the heuristic scoring and statutory rules while deterministic C/Python batch arbiters execute the millions of combinations—achieves sub-second execution at zero marginal cost.
2. **SQLite WAL Mode is Production-Grade for Batch Analytics**: With `PRAGMA synchronous = NORMAL` and 64MB memory caches, SQLite comfortably outperforms heavy external database clusters for localized read/write pipelines.
3. **Traceable Bureaucratic Accountability**: Generating statutory options alongside actual ministerial summons texts bridges data science and fiscal governance, turning raw anomaly detection into legally enforceable budget reform.
