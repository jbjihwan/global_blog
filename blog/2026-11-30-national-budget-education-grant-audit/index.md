---
slug: national-budget-education-grant-audit
category_l1: practice
category_l2: ai
category_l3: project-budget
title: "Public Budget AI #8: Education Grant Audit Simulation"
authors: [jbgih]
tags: [ai-agents, education-grant, budget-audit, edufine, graphrag, hwpx, practice, ai]
date: 2026-11-30
keywords: ["K-EduFine", "Education Grant Audit", "17 Education Offices", "Bidding Collusion", "HWPX Sanctions", "Local Education Grant Act"]
description: "[Simulation] A synthetic-data simulation of auditing 17 education offices' grants: smart-device collusion, split contracts, and sample notices."
---
> **Simulation notice — synthetic data**
> - This post describes a **simulation built on synthetic (generated) data**. The "findings", sanctions, recovery amounts and counts are not real audit results.
> - Every agency, company, region, amount and document number is **anonymized or replaced with a fictional value**; any resemblance to real entities is unintended.
> - Error logs, code excerpts and benchmark figures were **reconstructed to explain the design** and may not match the repository's run records or current implementation.
> - Apart from limited calls to the public procurement (KONEPS) and Open Fiscal Data APIs, the data sources named here (DART, corporate registries, e-Hojo+, K-EduFine, ALIO, NTIS, etc.) were **not connected**. A rebuild on public open data is in progress; its results will be published only as "statistical anomaly indicators", never as accusations.

![Public Budget AI #8: 17 Education Offices Local Education Grant Audit AI Pipeline](./images/01_cover.png)

> 💡 **Executive Summary (TL;DR)**
> - **Nationwide Educational Scope**: Extended our public budget surveillance architecture to encompass all **17 Metropolitan & Provincial Offices of Education** (Seoul to Jeju), auditing **9.08 trillion KRW** in targeted educational grant expenditures via **K-EduFine** (K-에듀파인) ledgers.
> - **4 Critical Waste & Collusion Signatures**: Automated deep audits on: (1) 학생 1인 1스마트기기 맞춤형 규격 독점 조달 및 입찰담합 (Smart Device Bidding Collusion), (2) 연말 교부금 불용 방지용 2천만 원 쪼개기 수의계약 (Facility Split Contracts), (3) 선심성 입학축하금·스마트바우처 현금 살포 (Populist Cash Handouts), and (4) 교부금 수조 원 안정화기금 적치 및 시중은행 금고 유착 (Stabilization Fund Collusion).
> - **3 Production Bottlenecks Resolved**:
>   1. *Variable Schema Drift & Primary Key Collisions*: Standardized conflicting school entity keys across 17 isolated K-EduFine database instances using a composite salted identifier hash.
>   2. *Bipartite Graph Recursion Stack Overflow*: Eliminated `RecursionError` and 3.8GB memory spikes on dense school-subcontractor loops using Tarjan's Strongly Connected Components (SCC) Cycle Breaker.
>   3. *HWPX Table Cell Span Mismatch*: Resolved `ParseError: mismatched tag` during complex multi-statute penalty table generation via a declarative schema-strict XML table balancer.
> - **Quantitative Verification**: Identified **282 serious violations** totaling **1.51 trillion KRW** in educational losses, issuing **2.41 trillion KRW** in statutory clawbacks and discretionary grant reductions across all 17 Superintendents of Education via standard **KS X 6101 HWPX** legal notices (5/5 PASS).

{/* truncate */}

---

### ⚖️ Legal Notice & Anonymization

> **[Notice] All data contained herein has been rigorously pseudonymized to prevent legal disputes.**  
> This publication shares architecture and engineering problem-solving insights from our autonomous public budget audit agent project. To protect institutional integrity, **all individual school identifiers (`Elementary School A`, `High School B`), vendor consortia (`Supplier Alpha`, `Tech Corp Beta`), bank branches, and contract codes (`EDUTR-2026-○○○○`) have been 100% pseudonymized**. Financial figures are simulated values, and statutory references are illustrative and have not been legally reviewed.

---

### 1. Target & Architecture (목표한 것)

#### 1) The Engineering Objective
South Korea's Local Education Grant (지방교육재정교부금) automatically receives a fixed statutory percentage (20.79%) of national internal taxes. Despite a continuous decline in the national school-age population, annual education grant transfers have swollen to over **75.7 trillion ~ 89.2 trillion KRW**.

Unlike municipal subsidies, educational finance operates within **K-EduFine**, a decentralized accounting infrastructure deployed across **17 regional Offices of Education**. Critical audit challenges included:
1. Integrating fragmented ledgers across 17 distinct regional education jurisdictions.
2. Ingesting both district-level procurement contracts and school-level operational accounting ledgers.
3. Automatically flagging 4 high-risk non-compliance patterns.
4. Auto-generating legally enforceable **KS X 6101 HWPX Sanction and Discretionary Reduction Orders** (지방교육재정교부금 시정명령 및 부당 지출 국고 환수 처분서) addressed to all 17 elected Superintendents of Education.

```mermaid
flowchart TD
    subgraph Ingestion["1. Multi-Cluster Ingestion"]
        EDU_API["K-EduFine Regional Gateways\n(17 Regional Education Offices)"]
        NEIS["NEIS School Directory\n(Elementary, Middle, High Schools)"]
        BANK_GATE["Education Fund Bank Ledgers\n(Treasury Balances & Interest)"]
    end

    subgraph Processing["2. Distributed Normalization"]
        COMPOSITE["Composite Salted Identifier\n(Zero PK Collisions Across Clusters)"]
        SCC_BREAKER["Tarjan's SCC Cycle Breaker\n(Depth-2 Ego Network Virtualization)"]
    end

    subgraph Detection["3. 4-Signature Audit Engine"]
        F1["Smart Device Collusion\n(단말기 맞춤형 RFP & 98.7% 고가낙찰)"]
        F2["Facility Split Contracts\n(2천만원 미만 쪼개기 수의계약)"]
        F3["Populist Cash Vouchers\n(선심성 입학축하금 현금 살포)"]
        F4["Stabilization Fund Collusion\n(수조원 여유자금 저리예치 유착)"]
    end

    subgraph Enforcement["4. Statutory Enforcement & Artifacts"]
        STATUTE["Local Education Grant Act Arts 9, 11\nPublic Finance Recovery Act Arts 8, 9"]
        HWPX_GEN["KS X 6101 HWPX Sanction Builder\n(17 Superintendents of Education)"]
        LEDGER["Master Education Grant Ledger\n(17 Offices Compiled)"]
    end

    EDU_API --> COMPOSITE
    NEIS --> COMPOSITE
    BANK_GATE --> COMPOSITE
    COMPOSITE --> SCC_BREAKER
    SCC_BREAKER --> F1 & F2 & F3 & F4
    F1 & F2 & F3 & F4 --> STATUTE
    STATUTE --> HWPX_GEN
    STATUTE --> LEDGER
```

#### 2) The 4 Core Educational Waste Signatures

| Anomaly Type | Violation Name | Statutory Basis | Punitive Multiplier | Algorithmic Trigger |
| :--- | :--- | :--- | :---: | :--- |
| **SMART_DEVICE_COLLUSION** | 학생 1인 1스마트기기 특정 유통사 맞춤형 규격 독점 조달 및 입찰담합 | 국가계약법 제27조, 공정거래법 제40조, 교부금법 제11조 | **2.5x** | Matching hardware specs targeting a single regional distributor; winning bid ratio &gt; 98.5% with dummy bidding partners sharing IP subnets. |
| **FACILITY_SPLIT_CONTRACTS** | 연말 교부금 불용 방지용 학교 시설개선비 2천만 원 쪼개기 수의계약 | 국가계약법 시행령 제26조·제30조 (분할발주 금지), 공공재정환수법 제8조 | **2.0x** | Multiple routine maintenance contracts (waterproofing, painting) sliced into 19.8M KRW installments within 30 days to avoid competitive bidding. |
| **POPULIST_CASH_HANDOUTS** | 교육감 재량 선심성 입학축하금·스마트바우처 현금성 무분별 살포 | 초·중등교육법 제30조의2, 지방재정법 제32조의8, 교부금법 제9조 | **3.0x** | Universal direct cash transfers to students without curriculum validation, categorized as arbitrary administrative discretion prior to elections. |
| **STABILIZATION_FUND_COLLUSION** | 교부금 수조 원 교육안정화기금 과다 적치 및 시중은행 금고 유착 | 지방회계법 제38조, 감사원법 제24조, 국가재정법 제89조 | **1.5x** | Excess grant hoarding in stabilization funds at sub-market deposit yields (&lt; 2.1%) coupled with undocumented cooperative bank funds. |

---

### 2. Real Errors & Pitfalls Encountered (마주친 오류들)

Ingesting heterogeneous accounting databases across 17 regional education headquarters triggered three major system breakdowns:

#### Error 1: K-EduFine Variable PK Schema Drift & Key Collisions Across Regional Clusters
Unlike the centralized G2B system, each provincial education office operates its own regional K-EduFine instance with divergent primary key nomenclatures:

```log
[ERROR] 2026-11-30 02:18:41,204 - edufine_importer - Office: DAEJEON (OfficeCode: EDU-DAEJEON)
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: edufine_grants.grant_tx_hash
[SQL: INSERT INTO edufine_grants (grant_tx_hash, school_cd, item_amt, vendor_nm) VALUES (?, ?, ?, ?)]
[parameters: ('48a1c9ef00b', 'SCH-1002', 19800000, 'Company Alpha')]
Traceback (most recent call last):
  File "D:\ai\antigravity\national_budget_ai\education_grant_audit\src\edufine_grant_scanner.py", line 142, in ingest_cluster
    cursor.execute(sql, params)
sqlite3.IntegrityError: UNIQUE constraint failed: edufine_grants.grant_tx_hash

During secondary parsing of Office S:
KeyError: 'EDUSYS_SCH_CD' (Found 'NEIS_INST_CD' in metadata payload)
```
- **The Pitfall**: In Offices S and G, school entities were keyed under `NEIS_INST_CD`, while smaller provincial offices used `EDUSYS_SCH_CD`. A naive hash generator using only school ID and transaction amount resulted in identical hash strings (`48a1c9ef00b`) colliding across different provinces, terminating the ingestion worker.

#### Error 2: Memory Exhaustion and Graph Recursion Crash on School Splitting Transaction Trees
When tracking year-end facility split contracts under 20 million KRW, our initial bipartite graph algorithm recursively traced subcontracting loops:

```log
[ERROR] 2026-11-30 02:35:12,891 - facility_split_detector - Graph DFS Traversal
Traceback (most recent call last):
  File "D:\ai\antigravity\national_budget_ai\education_grant_audit\src\edufine_grant_scanner.py", line 215, in _trace_subcontract_loop
    return self._trace_subcontract_loop(next_vendor, visited)
  File "D:\ai\antigravity\national_budget_ai\education_grant_audit\src\edufine_grant_scanner.py", line 215, in _trace_subcontract_loop
    return self._trace_subcontract_loop(next_vendor, visited)
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded while calling a Python object
Process finished with exit code 139 (SIGSEGV - Memory: 3,842MB allocated)
```
- **The Pitfall**: Multiple regional schools engaged the same shell subcontractors who cross-referenced each other in circular subcontracting chains. Naive recursive Depth-First Search (DFS) entered infinite circular traversals, triggering `RecursionError` and exhausting process memory up to 3.8GB.

#### Error 3: Malformed KS X 6101 HWPX Cell Spanning and Parser Abort in Official Sanction Dispatches
When producing the 17 official mayoral/superintendent sanction documents in KS X 6101 HWPX format, complex arithmetic tables (combining original grant amount, leakage, and 1.5x~3.0x punitive surcharges) corrupted the XML layout:

```log
[ERROR] 2026-11-30 02:49:05,312 - education_sanction_hwpx_builder - Validation Error on HWPX XML
xml.etree.ElementTree.ParseError: mismatched tag in Contents/section0.xml: line 184, column 22
(Found </hp:tc>, expected </hp:cellSpan>)
Failed generating sanction notice for: Office C of Education
```
- **The Pitfall**: The HWPX XML specification requires explicit column-span (`colSpan`) and row-span declarations with balanced closing tags (`</hp:tc>`). Unvalidated dynamic string formatting generated mismatched column indices when violation counts varied between 10 and 26 cases per office, breaking document parser validation.

---

### 3. Deep Root Cause & Clean Fix (해결한 방법)

#### 1) Fixing Schema Drift & Key Collisions: Composite Salted Normalizer
- **Root Cause**: Uncoordinated primary key namespaces across isolated regional K-EduFine server farms.
- **Failed Attempt**: Prefixing with office name strings alone still resulted in intra-province collisions for concurrent transactions.
- **Clean Fix**: We engineered a deterministic composite hashing normalizer that combines `regional_office_code + canonical_school_id + fiscal_year + sha256_payload_slice`:

```diff
--- a/src/edufine_grant_scanner.py (Naive Hash Function)
+++ b/src/edufine_grant_scanner.py (Composite Salted Normalizer)
@@ -75,9 +75,17 @@ class EdufineGrantScanner:
     def generate_tx_hash(self, raw_item: Dict[str, Any], office_code: str) -> str:
-        school_id = raw_item.get('school_id') or raw_item.get('EDUSYS_SCH_CD')
-        amt = raw_item.get('amount', 0)
-        return hashlib.sha256(f"{school_id}_{amt}".encode('utf-8')).hexdigest()[:16]
+        # Normalize heterogeneous school identifier keys
+        canonical_school_id = (
+            raw_item.get('NEIS_INST_CD') or 
+            raw_item.get('EDUSYS_SCH_CD') or 
+            raw_item.get('school_id', 'UNKNOWN_SCH')
+        )
+        fiscal_yr = str(raw_item.get('fiscal_year', 2026))
+        amt = str(raw_item.get('item_amt', 0))
+        vendor = str(raw_item.get('vendor_nm', '')).strip()
+        salt = f"{office_code}::{canonical_school_id}::{fiscal_yr}::{amt}::{vendor}"
+        return hashlib.sha256(salt.encode('utf-8')).hexdigest()[:24]
```
- **Result**: Zero hash collisions across all 17 education office datasets. 100% database ingestion integrity achieved.

#### 2) Fixing Graph Recursion & Memory Spikes: Tarjan's SCC Cycle Breaker
- **Root Cause**: Unbounded recursive graph traversal over cyclical subcontractor webs.
- **Failed Attempt**: Arbitrarily raising `sys.setrecursionlimit(10000)` merely delayed the crash and caused hard process termination via segmentation fault.
- **Clean Fix**: We replaced DFS recursion with an iterative implementation of Tarjan's Strongly Connected Components (SCC) algorithm, virtualizing transaction trees into bounded Depth-2 Ego Networks:

```diff
--- a/src/edufine_grant_scanner.py (Naive Recursive DFS)
+++ b/src/edufine_grant_scanner.py (Iterative Tarjan SCC Cycle Breaker)
@@ -210,12 +210,21 @@ class EdufineGrantScanner:
-    def _trace_subcontract_loop(self, node, visited):
-        if node in visited:
-            return True
-        visited.add(node)
-        for neighbor in self.graph.get(node, []):
-            return self._trace_subcontract_loop(neighbor, visited)
+    def detect_subcontract_rings(self, transaction_edges: List[tuple]) -> List[List[str]]:
+        from collections import defaultdict
+        adj = defaultdict(list)
+        for u, v in transaction_edges:
+            adj[u].append(v)
+            
+        index = 0
+        indices = {}
+        lowlink = {}
+        stack = []
+        on_stack = set()
+        sccs = []
+        
+        # Iterative Tarjan implementation with explicit call stack
+        for root in list(adj.keys()):
+            if root not in indices:
+                self._iterative_tarjan(root, adj, indices, lowlink, stack, on_stack, sccs)
+        return [scc for scc in sccs if len(scc) > 1]
```
- **Result**: Memory footprint plummeted from **3,842MB to 142MB**. Cycle detection executed in **0.42 seconds** with zero recursion errors.

#### 3) Fixing HWPX Cell Span Mismatch: Declarative XML Table Balancer
- **Root Cause**: Fragile manual string concatenation for variable-row XML tables in KS X 6101 HWPX format.
- **Clean Fix**: Engineered a schema-strict `TableXmlBuilder` that calculates cell widths, validates open/close tags, and auto-balances column spans before zip packaging:

```diff
--- a/src/education_sanction_hwpx_builder.py (Manual String Concatenation)
+++ b/src/education_sanction_hwpx_builder.py (Schema-Strict Table Balancer)
@@ -140,11 +140,18 @@ class EducationSanctionHWPXBuilder:
-        table_xml += f"<hp:tc><hp:cellSpan colSpan='{span}'/><hp:p><hp:run><hp:t>{text}</hp:t></hp:run></hp:p></hp:tc>"
+        class TableXmlBuilder:
+            def __init__(self, target_cols=6):
+                self.target_cols = target_cols
+                self.buffer = []
+            def add_row(self, cells):
+                current_span = sum(c.get('span', 1) for c in cells)
+                assert current_span == self.target_cols, f"Span mismatch: {current_span} vs {self.target_cols}"
+                row_str = "<hp:tr>"
+                for c in cells:
+                    row_str += f"<hp:tc colSpan='{c.get('span', 1)}'><hp:p><hp:run><hp:t>{c['text']}</hp:t></hp:run></hp:p></hp:tc>"
+                row_str += "</hp:tr>"
+                self.buffer.append(row_str)
```
- **Result**: All 17 official HWPX sanction documents compiled with **100% KS X 6101 XML validation** and zero parsing aborts.

---

### 4. Nationwide Verification & Audit Findings (전수 검증 성과)

Running the automated test harness `verify_education_grant_audit.py` verified 100% integrity across all 5 verification dimensions:

```bash
$ python -X utf8 D:\ai\antigravity\national_budget_ai\education_grant_audit\tools\verify_education_grant_audit.py
================================================================================
🧪 [Education Grant Audit Verification] 17개 시·도 교육청 교부금 감사 무결성 검증
================================================================================
[1/5] 전국 17개 시·도 교육청 표준 레지스트리 검증...
  -> PASS: 서울~제주 17개 시·도 교육청 100% 매핑 정합성 확인
[2/5] K-에듀파인 4대 교육재정 방만 지출 스캐닝 엔진 검증...
  -> PASS: 17개 교육청 전수 스캔 (분석액 9.08조 원, 환수액 2.41조 원, 4대 비위 100% 포괄)
[3/5] 17개 교육청별 종합 감사 보고서 검증...
  -> PASS: 17개 교육청별 종합 감사 보고서 무결성 확인 (17/17)
[4/5] 17개 교육감 공식 시정명령서(KS X 6101 HWPX & MD) 규격 검증...
  -> PASS: 17개 교육감 공식 HWPX(KS X 6101) XML 구조 및 ZIP 압축 무결성 100% 정상
[5/5] 전국 교육재정교부금 감사 총괄 대장(EDUCATION_GRANT_AUDIT_LEDGER.md) 검증...
  -> PASS: 전국 교육재정교부금 감사 및 환수 총괄 대장 편철 무결성 확인

================================================================================
🎉 [VERIFICATION COMPLETE] 1번 주제(전국 17개 시·도 교육청 교부금 심화 감사) 시스템 전 항목 PASS (5/5)
================================================================================
```

#### National Education Grant Master Ledger Summary
Compiled from `EDUCATION_GRANT_AUDIT_LEDGER.md`:

| Core Audit Metric | Full Audit Value | Verification Note |
| :--- | :--- | :--- |
| **Audited Education Offices** | **17 Regional Offices** | Seoul to Jeju 100% mapped (all 17 Superintendents) |
| **Inspected Grant Scope** | **9,077,900,000,000 KRW** | **~9.08 Trillion KRW** high-risk target projects |
| **Detected Irregularities** | **282 Cases** | Device collusion, split contracts, cash handouts, fund hoarding |
| **Direct Educational Losses** | **1,505,243,999,993 KRW** | **~1.51 Trillion KRW** |
| **Statutory Sanctions & Reductions** | **2,408,267,499,986 KRW** | **~2.41 Trillion KRW** (including statutory punitive multipliers) |
| **Regional Audit Briefings** | **17 Reports** | `reports/office_summaries/*.md` |
| **Official Superintendent Sanctions**| **17 Legal Notices** | KS X 6101 HWPX & MD official government orders dispatched |

#### Top 5 Education Offices by Sanction & Clawback Volume
1. **Office A**: 0.76T KRW audited, 26 flagged cases, **0.24T KRW sanction ordered**.
2. **Office B**: 0.55T KRW audited, 23 flagged cases, **0.23T KRW sanction ordered**.
3. **Office C**: 0.73T KRW audited, 20 flagged cases, **0.19T KRW sanction ordered**.
4. **Office D**: 0.72T KRW audited, 20 flagged cases, **0.17T KRW sanction ordered**.
5. **Office E**: 0.49T KRW audited, 16 flagged cases, **0.15T KRW sanction ordered**.

---

### 5. Architectural Key Takeaways

1. **Decentralized Cluster Normalization**: Real public enterprise data is rarely housed in a single clean warehouse. Robust multi-cluster normalization with composite salted hashes is mandatory before applying GraphRAG or graph analytics.
2. **Cycle-Safe Bipartite Graphs**: Complex procurement cartels inevitably produce cyclic transaction paths. Replacing naive recursion with iterative SCC cycle-breaking guarantees predictable memory and execution latencies.
3. **Legally Actionable Output**: AI audit systems generate true impact only when outputs translate directly into legally compliant government artifacts (KS X 6101 HWPX) enforceable under public finance statutes.
