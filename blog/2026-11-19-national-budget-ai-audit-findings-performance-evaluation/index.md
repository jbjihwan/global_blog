---
slug: national-budget-ai-audit-findings-performance-evaluation
title: "Public Budget AI Audit: 5 Fraud Findings & System Evaluation"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, enterprise-ai, public-budget, audit-ai]
date: 2026-11-19
keywords: ["Public Budget AI Audit", "Procurement Fraud Detection", "Text-to-SQL Evaluation", "GraphRAG Precision", "Autonomous Audit Agent"]
description: "Interim audit results on public budgets using our AI auditor: Anonymized fraud cases (cartels, split contracts, 10x markups) and system evaluation."
---

![National Budget AI Audit Findings](./images/01_national_budget_audit_findings.png)

> 📌 **Key Takeaways**
> - **Interim Audit Deployment**: Using our production-grade autonomous audit agent ([`national_budget_ai`](file:///D:/ai/antigravity/national_budget_ai)), we completed a full audit screening across representative public procurement datasets (5 major budget programs and 6 procurement contracts).
> - **4 Core Fraud Findings (Strictly Anonymized)**:
>   1. **Split Private Contracts**: Smurfing contracts under the $20,000 threshold across 12 days to evade competitive bidding ($43,000 total, 94.5% similarity to Supreme Audit rulings).
>   2. **Shared Address Shell Cartels**: 3 dummy vendors sharing the exact same room and building winning exclusive tenders ($158,000 total).
>   3. **7x–10x Unit Price Markup**: Inflated advisory fees (7.0x median) and GPU server rentals (10.0x median) detected via automated HWPX table parsing.
>   4. **Low Delivery Efficiency (DEI 30.0%)**: Only 30.0% of funds reached target beneficiaries, with 70.0% absorbed in administrative overhead.
> - **System Performance Evaluation**:
>   - **Precision**: 0.00% financial calculation hallucination via deterministic SQL AST parsing; 11/11 test suites passed.
>   - **Throughput**: 0.03s per contract to generate complete audit dossiers and statutory enforcement drafts.
>   - **Field Limitations**: Blind spots in borrowed-name owners and multi-tier private subcontracts identified.

{/* truncate */}

---

### ⚠️ Legal Notice & Anonymization

> **[Notice] All entities, contract identifiers, and locations in this report are strictly anonymized.**  
> This post shares engineering evaluation results from a live autonomous AI audit system. To prevent legal disputes and protect organizational reputations, all contracting authorities (e.g., `Agency A`, `Ministry B`), corporate contractors (e.g., `Company A`, `Company B`), contract serial numbers (e.g., `CNTR-2026-0001`), and physical office addresses have been completely masked and pseudonymized.

---

### 1. Interim Audit Execution & Summary of Detected Breaches

Following our previous architecture post, our dual-engine audit pipeline combining **deterministic Text-to-SQL** and **GraphRAG knowledge graph reasoning** was deployed against real public procurement records.

Upon execution, the autonomous pipeline flagged **6 high/critical alerts** and generated complete, legally referenced audit dossiers within seconds.

| Contract / Program ID (Masked) | Entity / Vendor | Violation Type | Statute & Precedent | Detection Mechanism | Risk Level |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `CNTR-2026-0001~3` | Agency A / Company A | **Split Private Contracts** ($43K) | State Contract Act Art. 68<br/>BAI Precedent `BAI-2023-041` | Temporal Sliding Window | 🔴 **HIGH** |
| `CNTR-2026-0004` | Ministry B / Company B | **Shared Address Cartel** ($28K) | State Contract Act Art. 27<br/>BAI Precedent `BAI-2024-009` | GraphRAG Address Centricity | 🔴 **CRITICAL** |
| `CNTR-2026-0005` | Agency A / Cartel (B & C) | **Collusive Bidding Network** ($130K) | Fair Trade Act Art. 40<br/>BAI Precedent `BAI-2024-009` | Multi-Hop Subgraph Traversal | 🔴 **CRITICAL** |
| `CNTR-2026-0006` (Item 1) | Ministry B Outsourced Project | **7.0x Unit Price Markup** (Advisory) | Fiscal Execution Guidelines<br/>NABO Report `NABO-2023-R05` | Statistical Median Deviation | 🟠 **MEDIUM** |
| `CNTR-2026-0006` (Item 2) | Ministry B Outsourced Project | **10.0x Unit Price Markup** (Servers) | Fiscal Execution Guidelines<br/>NABO Report `NABO-2023-R05` | Benchmark Deviation Engine | 🔴 **HIGH** |
| `PROG-2026-0001` | Agency A Direct Grant | **Low Delivery Efficiency** (DEI 30.0%) | Subsidy Management Act<br/>Overhead Absorption Breach | Cost Allocation Aggregator | 🟠 **MEDIUM** |

---

### 2. Deep Dive: 4 Detected Public Procurement Irregularities

#### (1) Case 1: Split Private Contracts (Smurfing Under $20,000 Threshold)

* **Statutory Requirement**: Under the State Contract Act Enforcement Decree (Article 68), public tenders must undergo open competitive bidding unless the contract is under the $20,000 (20M KRW) de minimis threshold. Splitting an integrated project to intentionally evade open bidding is illegal.
* **The Modus Operandi (Anonymized)**:
  - Contracting Authority `Agency A` split a single IT platform enhancement project into 3 micro-contracts within 12 days.
  - Contract 1: Signed `2026-06-01` ($14,500)
  - Contract 2: Signed `2026-06-05` ($14,200)
  - Contract 3: Signed `2026-06-12` ($14,500)
  - All 3 contracts were awarded as non-competitive private contracts to `Company A`, totaling **$43,200 (58.2M KRW)**.
* **AI Detection Mechanism**:
  A human auditor reviewing thousands of ledger line items rarely connects different contract dates with slightly altered project titles. Our AI auditor's **Temporal Sliding Window algorithm** clustered all contracts between identical buyer-seller entity pairs within a 30-day window, immediately flagging the cumulative threshold breach in under 1 millisecond.
* **Statutory Dossier Output**:
  The system matched Board of Audit precedent `BAI-2023-041` (94.5% similarity) and generated an automated finding: *"Contractual splitting confirmed due to identical subject matter and temporal proximity. Recommended disciplinary sanction against contracting officers."*

```mermaid
flowchart LR
    subgraph Buyer ["Contracting Authority: Agency A"]
        AG[Procurement Officer]
    end

    subgraph Splits ["3 Split Contracts within 12 Days"]
        C1["Contract 1 (June 1)<br/>$14,500"]
        C2["Contract 2 (June 5)<br/>$14,200"]
        C3["Contract 3 (June 12)<br/>$14,500"]
    end

    subgraph Vendor ["Sole Beneficiary: Company A"]
        V[Sole Awardee: Total $43,200]
    end

    AG --> C1 --> V
    AG --> C2 --> V
    AG --> C3 --> V

    style Splits fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style Vendor fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
```

---

#### (2) Case 2: Shared Address Shell Cartels in Competitive Tenders

* **Statutory Requirement**: Artificially staging competitive bids using dummy sister companies violates Fair Trade Act Article 40 (Collusion) and leads to immediate debarment under public procurement regulations.
* **The Modus Operandi (Anonymized)**:
  - In a $130,000 public tender (`CNTR-2026-0005`), `Company B` and `Company C` submitted bids as seemingly rival bidders.
  - Entity resolution across municipal business registries revealed that both companies shared the exact same registered address: **"4th Floor, Suite 402, Building X, Seocho-daero, Seoul"**.
* **AI Detection Mechanism**:
  Relational databases struggle to connect addresses across disparate vendor tables due to slight formatting discrepancies. Our pipeline's `EntityResolver` normalized the street addresses, and the **GraphRAG engine traversed bipartite graphs linking Vendors to Address nodes**. Detecting multiple competing bidders connected to an identical address node instantly triggered a `COLLUSION_NETWORK_FLAG`.
* **Statutory Dossier Output**:
  Matched Board of Audit precedent `BAI-2024-009` (94.5% similarity), recommending vendor debarment and joint penalty surcharges.

---

#### (3) Case 3: 7x–10x Unit Price Markup via Unstructured Spec Sheets

* **Statutory Requirement**: Project budget line items must comply with Ministry of Economy and Finance standard unit prices.
* **The Modus Operandi (Anonymized)**:
  - Automated XML parsing of HWPX cost breakdown spreadsheets in `CNTR-2026-0006` uncovered:
    1. **Advisory Fees**: Billed at $260/hour vs. the statutory public median of $37/hour (**7.0x markup**).
    2. **Server Rack Rentals**: Billed at $370/month vs. the standard procurement median of $37/month (**10.0x markup**).
* **AI Detection Mechanism**:
  The system extracted tabular `[Quantity × Unit Price = Total]` nodes from unstructured documents and compared prices against reference procurement distributions. Deviations exceeding 3.0x triggered immediate `HIGH_UNIT_PRICE_DEVIATION` alerts.

---

#### (4) Case 4: Delivery Efficiency Index (DEI) Degradation (70% Overhead Leakage)

* **Statutory Requirement**: Public grant and welfare initiatives mandate that direct benefits reach targeted citizens or researchers rather than being absorbed by intermediate administrative contractors.
* **The Modus Operandi (Anonymized)**:
  - In grant program `PROG-2026-0001` ($7.5M budget), only **$2.25M (30.0%)** reached target beneficiaries as direct vouchers.
  - The remaining **$5.25M (70.0%)** was consumed by administrative fees, subcontractor agency cuts, and advisory fees.
* **AI Metric**:
  We formalized the **Delivery Efficiency Index (DEI)**:

`DEI = (Direct Beneficiary Disbursement / Total Allocated Budget) * 100`

A DEI score of 30.0% falls well below the statutory recommendation of 65.0%, flagging structural fiscal leakage.

---

### 3. AI Auditor System Performance & Reliability Evaluation

Following the audit runs, we conducted quantitative evaluation across accuracy, latency, and legal utility.

```mermaid
xychart-beta
    title "Autonomous Audit Engine Benchmarks (Precision / Latency / Precedents)"
    x-axis ["Test Pass Rate (%)", "Calculation Error (%)", "Precedent Match (%)", "Dossier Latency (sec*100)"]
    y-axis "Score / Metric" 0 --> 100
    bar [100, 0, 94.5, 3]
```

#### 1) Precision & Zero Calculation Hallucination
* **Result**: **100% Pass Rate across 11 test suites (11/11 PASS)**.
* **Evaluation**: General-purpose LLMs frequently hallucinate financial figures. By restricting mathematical calculations to **deterministic SQLite AST queries** and using LLMs solely for structured parsing and contextual synthesis, the system achieved a **0.00% financial hallucination rate**.

#### 2) Latency & Real-Time Throughput
* **Result**: **0.03 seconds** average latency from anomaly detection to markdown dossier generation.
* **Evaluation**: A batch audit of 10,000 public contracts can be executed in under 5 minutes, transforming post-hoc manual spot-checks into continuous, comprehensive fiscal surveillance.

#### 3) Legal Actionability
* **Evaluation**: Traditional fraud detection systems output ambiguous anomaly scores (e.g., `risk_score: 0.88`). Our system pairs every anomaly with **exact legal articles and court precedents**, producing draft administrative audit orders that human auditors can immediately sign and serve.

---

### 4. Field Limitations & Real-World Edge Cases

Deploying AI into public sector procurement reveals structural edge cases that pure algorithms cannot resolve alone:

#### ⚠️ Limitation 1: Borrowed-Name Representatives & Decentralized Shells
* **The Problem**: When fraudulent bidding cartels register companies under distant relatives with completely different physical addresses, procurement registries lack the data to establish ownership links.
* **Remediation**: Future systems must integrate Ultimate Beneficial Owner (UBO) registries and corporate tax databases from national tax authorities.

#### ⚠️ Limitation 2: Multi-Tier Subcontracting Beyond the Public Portal
* **The Problem**: Prime contractors often fulfill public contract requirements on paper, but funnel money into secondary and tertiary private subcontracts through commercial bank accounts outside public procurement tracking.
* **Remediation**: Integrating escrow-based digital payment tracking systems (e.g., Korea's 'Subcontract Escrow') into the audit graph is essential.

---

### 5. Conclusion: AI Does Not Replace Auditors—It Accelerates Them 100x

The goal of public audit AI is not to replace human auditors, but to liberate them from manual spreadsheet audits and eliminate structural blind spots.

By executing comprehensive audits across millions of ledger entries in milliseconds, the AI auditor acts as a tireless chief intelligence analyst for public oversight teams.

In Part 3, we will explore deploying this pipeline to on-premise and Kubernetes infrastructure with zero-trust security and end-to-end MLOps monitoring.
