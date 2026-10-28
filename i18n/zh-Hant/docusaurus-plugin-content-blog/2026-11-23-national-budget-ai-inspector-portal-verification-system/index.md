---
slug: national-budget-ai-inspector-portal-verification-system
title: "[AI實戰 #6] 審計員綜合Web門戶構建與20項測試全數通關"
authors: [jbgih]
tags: [ai-agents, web-portal, test-automation, full-verification, audit-intelligence, devops]
date: 2026-11-23
keywords: ["審計員Web門戶", "Vis.js知識圖譜", "HWPX公文解析器", "20項測試全量驗證", "國家預算AI審計終章"]
description: "國家預算AI審計系列最終章。整合Vis.js知識圖譜、10年判例庫與HWPX即時解析器的審計門戶v3.0構建，以及20項測試全通復盤。"
---

![National Budget Inspector Web Portal v3.0 & 20/20 Verification](./images/01_national_budget_inspector_portal.png)

> 💡 **核心摘要 (Key Takeaways)**
> - **審計員綜合Web門戶v3.0落成**: 將分散的CLI腳本全面升級為具備7大專屬工作區的實時統一管控中心。
> - **20項全量驗證測試100%通過 (20/20 PASS)**: 從原型SQL生成到GraphRAG、實時流監控、DART法人登記追蹤、圍標網絡識別、HWPX虛高比對，全領域測試無瑕疵通過。
> - **架構設計前瞻預防的兩大瓶頸**: (1) 透過12個標準化RESTful DTO端點解耦異構審計引擎，(2) 引入環形DOM環狀緩衝區防止實時流導致前端內存溢出。
> - **實際排查的三大突發故障**: (1) Vis.js物理引擎無限振盪導致UI卡死，改用穩定化事件即刻凍結解決；(2) 50頁大體量HWPX XML解析阻塞主循環，引入ThreadPoolExecutor異步工作隊列解決；(3) 20項測試批處理中SQLite文件鎖衝突，構建進程隔離內存池徹底根除。
> - **六部曲全景終章**: 超越簡單的Prompt Engineering，在公共財政安全這一高精尖實務領域驗證生產級AI工程體系。

{/* truncate */}

---

### ⚖️ 法律聲明與匿名化說明 (Legal Notice & Anonymization)

> 為避免法律糾紛，本文涉及的所有招標機關（如`A振興公團`、`B振興院`、`C公團`、`D區政府`）、承包企業（如`○○資訊科技(株)`、`○○顧問(株)`）、涉案人員（如`K某`、`P某`）、合約編號（`CNTR-2026-○○○○`）及具體日期均已進行100%化名及掩碼（0000）處理。

---

### 回顧前5篇系列文章，我們的工程團隊逐步攻克了國家預算AI審計的核心難關：

1. **第1篇: 自然語言轉精確SQL與GraphRAG檢索原型**
1. **第2篇: 400餘項實證數據檢驗與審計院判例語義匹配評估**
1. **第3篇: 從400萬件採購市場剔除85%雜訊的三維標的分區引擎**
1. **第4篇: 聯動DART企業公示與登記簿揪出借名空殼公司卡特爾**
1. **第5篇: 精準打擊弱勢企業5千萬韓元拆單(Sector 5)與12月年底突擊花錢(Sector 6)**

> 「一線審計官需要的不是分散的Python腳本，而是一個能實時捕獲異常、用知識圖譜下鑽股權脈絡、拖入公文即可一鍵生成對照10年判例質詢書的統一作戰中心。」

為此，我們打造了「審計員綜合Web門戶v3.0」，並建立了全覆蓋的「20項端到端自動化測試套件(20/20 PASS)」。本終章將全面揭秘其架構與填坑實錄。

---

### 1. 審計員綜合Web門戶v3.0架構與7大工作區

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

- **實時綜合監控大屏 (`/api/stats`, `/api/alerts`)**: 實時異常計數、高危緊急警報與內建AI對話助手。
- **6大標的區域全景矩陣 (`/api/sectors`)**: 針對Sector 1~6的多維篩選及採購總帳實時核驗表格。
- **自動化質詢要求書生成 (`/api/summons`)**: 自動援引違規法條與審計院裁定要旨，一鍵排版標準審計行政格式質詢書。
- **e國幫扶財政補助金反詐追查 (`/api/subsidy_fraud`)**: 重複領取、挪作私用及直系親屬帳戶間接輸送追蹤。
- **圍標陪標網絡圖譜 (`/api/bidding_rings`, `/api/graph`)**: Vis.js動態力導向圖呈現輪流坐莊與高管兼職網絡。
- **國會預算審查削減分析器 (`/api/budget_cuts`)**: 依據歷史結餘不用率自動推導預算下調建議方案。
- **10年判例庫與HWPX即時解析器 (`/api/precedents`, `/api/hwpx_analysis`)**: 拖曳公文即刻核算人工虛報並推薦5條高相關判例。

---

### 2. 架構設計中預見並防範的兩大技術瓶頸

#### 📌 課題 1: 異構審計引擎單體耦合引發的伺服器阻塞與雪崩
* GraphRAG、HWPX二進制解析、向量檢索與DART接口開銷迥異。若混入單進程，耗時的HWPX任務將卡死預警分發。我們透過12個規範化RESTful DTO端點完成隔離，單模組偶發異常不影響其他6大工作區正常運行。

#### 📌 課題 2: 實時數據流監控中的前端DOM超載與記憶體洩漏
* 實時日誌持續追加極易導致瀏覽器記憶體攀升至1.5GB以上引發崩潰。我們實現了僅保留最新100條節點的環形DOM環狀緩衝演算法，超額節點立即剝離釋放，記憶體常年恆定在120MB以內。

---

### 3. 實際落地過程中排查的三大突發故障

#### 🐛 故障 1: Vis.js物理引擎無限振盪導致前端UI鎖死
* 當節點超過50個時，斥力與彈簧力計算發散產生劇烈振盪，主執行緒100%卡死。透過將穩定迭代限制為150次，並在`stabilizationIterationsDone`事件觸發後立即調用`network.setOptions({ physics: { enabled: false } })`強行凍結，徹底平復卡頓。

```javascript
// Stabilization freeze pattern
network.on("stabilizationIterationsDone", function () {
    network.setOptions({ physics: { enabled: false } });
    console.log("[Portal] Vis.js physics stabilized and frozen.");
});
```

#### 🐛 故障 2: 50頁大體量HWPX XML解析阻塞主事件循環
* 解壓XML和XPath遍歷同步佔用HTTP執行緒達8秒，導致並發請求504閘道逾時。改造成簽發Job UUID並將解析派發至ThreadPoolExecutor異步執行緒池，前端輪詢進度，其他API響應時間壓回15ms內。

#### 🐛 故障 3: 20項自動化測試批處理並發時的SQLite檔案鎖衝突
* 批量運行測試時頻繁拋出`sqlite3.OperationalError: database is locked`。引入測試隔離池，為每個測試分配帶PID的臨時檔案或純記憶體資料庫`:memory:`，保證測試100%獨立無干擾通過。

---

### 4. 20項端到端自動化測試全景彙總 (20/20 PASS)

20項檢驗腳本覆蓋從數據清洗到前端展示的全鏈路，全部取得PASS評級。

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

### 5. 結語：AI智能體在公共工程領域的未來

透過結合領域知識的分區策略、DART圖譜關聯、標準公文自動化生成與完備的自動化測試體系，AI智能體得以真正扎根公共財政實務。感謝讀者對本系列的關注與支持！
