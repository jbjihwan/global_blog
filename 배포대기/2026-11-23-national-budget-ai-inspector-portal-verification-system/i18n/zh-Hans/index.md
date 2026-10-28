---
slug: national-budget-ai-inspector-portal-verification-system
title: "[AI实战 #6] 审计员综合Web门户搭建与20项端到端测试全通"
authors: [jbgih]
tags: [ai-agents, web-portal, test-automation, full-verification, audit-intelligence, devops]
date: 2026-11-23
keywords: ["审计员Web门户", "Vis.js知识图谱", "HWPX公文解析器", "20项测试全量验证", "国家预算AI审计终章"]
description: "国家预算AI审计系列最终篇。整合Vis.js知识图谱、10年判例库与HWPX即时解析器的审计员门户v3.0构建，以及20项测试全通复盘。"
---

![National Budget Inspector Web Portal v3.0 & 20/20 Verification](./images/01_national_budget_inspector_portal.png)

> 💡 **核心摘要 (Key Takeaways)**
> - **审计员综合Web门户v3.0落成**: 将分散的CLI脚本全面升级为具备7大专属工作区（综合大屏、6大标的区域、质询书自动生成、e国帮扶补助金、围标图谱、国会预算削减审查、判例库与HWPX解析）的实时统一管控中心。
> - **20项全量验证测试100%通过 (20/20 PASS)**: 从原型SQL生成到GraphRAG、实时流监控、DART法人登记追踪、围标网络识别、HWPX虚高比对，全领域测试无瑕疵通过。
> - **架构设计前瞻预防的两大瓶颈**: (1) 通过12个标准化RESTful DTO端点解耦异构审计引擎，(2) 引入环形DOM环状缓冲区（Circular DOM Ring Buffer）防止实时流导致前端内存溢出。
> - **实际排查的三大突发故障**: (1) Vis.js物理引擎无限振荡导致UI卡死，改用稳定化事件即刻冻结解决；(2) 50页大体量HWPX XML解析阻塞主循环，引入ThreadPoolExecutor异步工作队列解决；(3) 20项测试批处理中SQLite文件锁冲突，构建进程隔离内存池彻底根除。
> - **六部曲全景终章**: 超越简单的Prompt Engineering，在公共财政安全这一高精尖实务领域验证生产级AI工程体系。

{/* truncate */}

---

### ⚖️ 法律声明与匿名化说明 (Legal Notice & Anonymization)

> 为避免法律纠纷，本文涉及的所有招标机关（如`A振兴公团`、`B振兴院`、`C公团`、`D区政府`）、承包企业（如`○○信息科技(株)`、`○○咨询(株)`）、涉案人员（如`K某`、`P某`）、合同编号（`CNTR-2026-○○○○`）及具体日期均已进行100%化名及掩码（0000）处理。

---

### 回顾前5篇系列文章，我们的工程团队逐步攻克了国家预算AI审计的核心难关：

1. **第1篇: 自然语言转精确SQL与GraphRAG检索原型**
1. **第2篇: 400余项实证数据检验与审计院判例语义匹配评估**
1. **第3篇: 从400万件采购市场剔除85%噪声的三维标的分区引擎**
1. **第4篇: 联动DART企业公示与登记簿揪出借名空壳公司卡特尔**
1. **第5篇: 精准打击弱势企业5千万韩元拆单(Sector 5)与12月年底突击花钱(Sector 6)**

> “一线审计官需要的不是分散的Python脚本，而是一个能实时捕获异常、用知识图谱下钻股权脉络、拖入公文即可一键生成对照10年判例质询书的统一作战中心。”

为此，我们打造了“审计员综合Web门户v3.0”，并建立了全覆盖的“20项端到端自动化测试套件(20/20 PASS)”。本终章将全面揭秘其架构与填坑实录。

---

### 1. 审计员综合Web门户v3.0架构与7大工作区

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

- **实时综合监控大屏 (`/api/stats`, `/api/alerts`)**: 实时异常计数、高危紧急警报(Flash Alert)与内置AI对话助手。
- **6大标的区域全景矩阵 (`/api/sectors`)**: 针对Sector 1~6的多维筛选及采购总账实时核验表格。
- **自动化质询要求书生成 (`/api/summons`)**: 自动援引违规法条与审计院裁定要旨，一键排版标准审计行政格式质询书。
- **e国帮扶财政补助金反诈追查 (`/api/subsidy_fraud`)**: 重复领取、挪作私用及直系亲属账户间接输送追踪。
- **围标陪标网络图谱 (`/api/bidding_rings`, `/api/graph`)**: Vis.js动态力导向图呈现轮流坐庄与高管兼职网络。
- **国会预算审查削减分析器 (`/api/budget_cuts`)**: 依据历史结余不用率自动推导预算下调建议方案。
- **10年判例库与HWPX即时解析器 (`/api/precedents`, `/api/hwpx_analysis`)**: 拖拽公文即刻核算人工虚报并推荐5条高相关判例。

---

### 2. 架构设计中预见并防范的两大技术瓶颈

#### 📌 课题 1: 异构审计引擎单体耦合引发的服务器阻塞与雪崩
* GraphRAG、HWPX二进制解析、向量检索与DART接口开销迥异。若混入单进程，耗时的HWPX任务将卡死预警分发。我们通过12个规范化RESTful DTO端点完成隔离，单模块偶发异常不影响其他6大工作区正常运行。

#### 📌 课题 2: 实时数据流监控中的前端DOM超载与内存泄露
* 实时日志持续追加极易导致浏览器内存攀升至1.5GB以上引发崩溃。我们实现了仅保留最新100条节点的环形DOM环状缓冲算法，超额节点立即剥离释放，内存常年恒定在120MB以内。

---

### 3. 实际落地过程中排查的三大突发故障

#### 🐛 故障 1: Vis.js物理引擎无限振荡导致前端UI锁死
* 当节点超过50个时，斥力与弹簧力计算发散产生剧烈振荡，主线程100%卡死。通过将稳定迭代限制为150次，并在`stabilizationIterationsDone`事件触发后立即调用`network.setOptions({ physics: { enabled: false } })`强行冻结，彻底平复卡顿。

```javascript
// Stabilization freeze pattern
network.on("stabilizationIterationsDone", function () {
    network.setOptions({ physics: { enabled: false } });
    console.log("[Portal] Vis.js physics stabilized and frozen.");
});
```

#### 🐛 故障 2: 50页大体量HWPX XML解析阻塞主事件循环
* 解压XML和XPath遍历同步占用HTTP线程达8秒，导致并发请求504网关超时。改造成签发Job UUID并将解析派发至ThreadPoolExecutor异步线程池，前端轮询进度，其他API响应时间压回15ms内。

#### 🐛 故障 3: 20项自动化测试批处理并发时的SQLite文件锁冲突
* 批量运行测试时频繁抛出`sqlite3.OperationalError: database is locked`。引入测试隔离池，为每个测试分配带PID的临时文件或纯内存数据库`:memory:`，保证测试100%独立无干扰通过。

---

### 4. 20项端到端自动化测试全景汇总 (20/20 PASS)

20项检验脚本覆盖从数据清洗到前端展示的全链路，全部取得PASS评级。

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

### 5. 结语：AI智能体在公共工程领域的未来

通过结合领域知识的分区策略、DART图谱关联、标准公文自动化生成与完备的自动化测试体系，AI智能体得以真正扎根公共财政实务。感谢读者对本系列的关注与支持！
