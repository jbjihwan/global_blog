# -*- coding: utf-8 -*-
import os

BASE_DIR = r"D:\ai\antigravity\global_blog\배포대기\2026-11-19-national-budget-ai-audit-findings-performance-evaluation\i18n"

POSTS = {
    "ja": {
        "title": "国家予算AI監査の中間結果：不正摘発とAI監査官の性能評価",
        "description": "国家予算AI監査システムの中間運用結果：分割随意契約、ペーパーカンパニー談合、単価10倍水増しの摘発事例（完全匿名化）とAI監査官の精度・性能・限界を評価。",
        "keywords": '["国家予算AI監査", "公共調達不正検知", "Text-to-SQL性能", "GraphRAG評価", "自律型AIエージェント"]',
        "content": '''---
slug: national-budget-ai-audit-findings-performance-evaluation
title: "国家予算AI監査の中間結果：不正摘発とAI監査官の性能評価"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, enterprise-ai, public-budget, audit-ai]
date: 2026-11-19
keywords: ["国家予算AI監査", "公共調達不正検知", "Text-to-SQL性能", "GraphRAG評価", "自律型AIエージェント"]
description: "国家予算AI監査システムの中間運用結果：分割随意契約、ペーパーカンパニー談合、単価10倍水増しの摘発事例（完全匿名化）とAI監査官の精度・性能・限界を評価。"
---

![National Budget AI Audit Findings](./images/01_national_budget_audit_findings.png)

> 📌 **要点まとめ (Key Takeaways)**
> - **中間監査の実施概要**: 年間約650兆ウォン規模の国家予算データセットから、5つの主要事業および6つの調達契約を対象にAI監査エージェント([`national_budget_ai`](file:///D:/ai/antigravity/national_budget_ai))の中間全数検証を完了しました。
> - **4大不正執行の摘発（完全匿名化）**:
>   1. **分割随意契約**: 2,000万ウォン以下の少額随意契約規定を悪用し、12日間に3件へ分割契約した事例（計5,820万ウォン、国家契約法施行令第68条違反、監査院判例類似度94.5%）。
>   2. **同一住所共有ペーパーカンパニー談合**: 同一ビル同一室を登録住所とする3社による偽装競争入札（計2億1,310万ウォン規模）。
>   3. **基準単価7〜10倍の水増し**: 専門家助言料が中央値比7.0倍、GPUサーバーラック賃貸料が中央値比10.0倍の暴利を検出。
>   4. **事業伝達効率(DEI)の著しい低下**: 予算の受取人直接伝達率30.0%、間接管理費・手数料等への漏出率70.0%を特定。
> - **AIシステム総合性能評価**:
>   - **精度**: 決定論的Text-to-SQLによる財務計算ハルシネーション0%、11全テストケースPASS。
>   - **速度**: 契約1件あたりの監査Dossierおよび行政処分勧告案の生成に平均0.03秒。
>   - **実務上の限界**: 名義貸し代表者および多段階民間下請けの資金追跡における課題を明文化。

{/* truncate */}

---

### ⚠️ 法的告知および匿名化案内 (Legal Notice & Anonymization)

> **【必読】本稿に収録されているすべての事例は、紛争防止のため厳格に匿名化されています。**  
> 本レポートは、独自開発したAI監査システムの工学的実証結果を共有する目的で作成されました。特定公的機関および企業の営業秘密や名誉を保護するため、**発注機関名（例：`A公団`、`B省`）、受注企業名（例：`A社`、`B社`、`C社`）、契約番号（例：`CNTR-2026-0001`）、詳細所在地（例：`ソウル市瑞草区○○ビル`）はすべて仮名化およびマスキング処理**されています。

---

### 1. 中間監査の実施結果および摘発総合サマリー

前回のアーキテクチャ解説で紹介した通り、私たちは**決定論的Text-to-SQL**と**GraphRAGナレッジグラフ推論**を統合した自律型監査パイプラインを構築しました。

実際の公共調達およびデジタル財政データをパイプラインに投入したところ、即座に**6件の高リスク（HIGH/CRITICAL）フラッシュアラート**と法的根拠付き監査Dossierが自動生成されました。

| 契約・事業識別子（仮名） | 対象機関 / 契約企業 | 摘発類型 | 違反法令および判例 | AI検知メカニズム | リスク度 |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `CNTR-2026-0001~3` | A公団 / A社 | **分割随意契約** (5,820万W) | 国家契約法施行令第68条<br/>監査院 `BAI-2023-041` | 時間差スライディングウィンドウ | 🔴 **HIGH** |
| `CNTR-2026-0004` | B省 / B社 | **住所共有談合** (3,850万W) | 国家契約法第27条<br/>監査院 `BAI-2024-009` | GraphRAG同一住所ノード | 🔴 **CRITICAL** |
| `CNTR-2026-0005` | A公団 / カルテル(B・C社) | **広域入札談合** (1億7,460万W) | 公正取引法第40条<br/>監査院 `BAI-2024-009` | 複数ノード巡回サブグラフ | 🔴 **CRITICAL** |
| `CNTR-2026-0006` (項目1) | B省委託事業 | **助言料7.0倍水増し** | 予算執行指針<br/>国会予算政策処 `NABO-2023-R05` | 中央値偏差分析ルール | 🟠 **MEDIUM** |
| `CNTR-2026-0006` (項目2) | B省委託事業 | **ラック賃貸10.0倍水増し** | 予算執行指針<br/>国会予算政策処 `NABO-2023-R05` | 調達標準偏差エンジン | 🔴 **HIGH** |
| `PROG-2026-0001` | A公団直接支援事業 | **伝達効率低下** (DEI 30.0%) | 補助金管理法<br/>間接管理費過大漏出 | 支出費目比率集計 | 🟠 **MEDIUM** |

---

### 2. AI監査官が摘発した4大不正手口の分析

#### (1) 事例1：少額特例を悪用した「時間差分割随意契約」
* **背景法令**: 国家契約法上、2,000万ウォン以下の少額案件に限り随意契約が認められますが、単一事業を意図的に分割して随意契約を結ぶことは違法です。
* **手口**: `A公団`は同一のIT保守業務をわずか12日間に3件へ分割（6/1: 1,950万W、6/5: 1,920万W、6/12: 1,950万W）。受注企業はすべて`A社`単独（計5,820万ウォン）。
* **AIの検知**: 人間が膨大な伝票から見落としがちな日付の分散を、AIの**時間差スライディングウィンドウ（30日枠）**が集計し、0.001秒で限度額超過を捕捉。監査院判例`BAI-2023-041`（類似度94.5%）を自動紐付けしました。

#### (2) 事例2：同一住所を共有するペーパーカンパニー入札談合
* **手口**: `B省`および`A公団`の競争入札において、外見上別会社に見える`B社`と`C社`が競合として参加。しかし両社の所在地を照合した結果、ソウル市内の同一ビル同一号室に登記されていました。
* **AIの検知**: `EntityResolver`で住所表記の揺れを正規化した後、**GraphRAGナレッジグラフ上で事業者ノードと住所ノードの接続構造を解析**。同一住所に連なる談合カルテルを瞬時に摘発しました。

#### (3) 事例3：非構造化内訳書からの単価7〜10倍水増し検出
* **手口**: 非構造化HWPX内訳書において、専門家助言料が公的標準中央値（時給5万W）の**7.0倍（時給35万W）**、サーバーラック賃貸料が標準中央値の**10.0倍（月額50万W）**で計上。
* **AIの検知**: 文書内XMLテーブルをパースし、調達統計データベースの分布値と比較して3倍以上の異常値を自動警報。

#### (4) 事例4：事業伝達効率(DEI) 30% — 予算の70%が間接費へ漏出
* **指標**: 独自策定した伝達効率指数 `DEI = (直接受取人執行額 / 総予算) * 100`。
* **結果**: 100億ウォンの事業において、最終受取人に届いたのはわずか30億ウォン（30.0%）。残り70億ウォンは中間団体の管理費や外注手数料に費消されていた構造的浪費を検出。

---

### 3. AI監査システムの性能・精度総合評価

```mermaid
xychart-beta
    title "AI監査エンジン性能ベンチマーク (精度 / 速度 / 判例整合性)"
    x-axis ["テスト通過率 (%)", "財務計算誤差率 (%)", "判例マッチング度 (%)", "Dossier生成時間 (秒×100)"]
    y-axis "測定値" 0 --> 100
    bar [100, 0, 94.5, 3]
```

1. **ゼロ・ハルシネーション（計算誤差0%）**: 計算処理をLLMから切り離し、AST検証済みSQLiteクエリエンジンに委ねることで、金額の捏造や誤差を完全防止（11/11テスト全通過）。
2. **高速スループット（1件0.03秒）**: 10,000件規模の契約データを約5分で全数スクリーニング可能。
3. **法的拘束力への接続（Actionability）**: 単なる異常値スコアではなく、違反条文と監査院判例を引用した監査報告書草案を出力。

---

### 4. 現場適用で判明した実務上の限界と克服課題

1. **名義貸し代表者（名目上の経営者）の追跡限界**: 登記上の代表者と住所が完全に異なり、親族名義等で分散されている場合、調達データ単体での判定は困難。国税庁の株主名簿や課税データとのAPI連携が必須。
2. **多段階民間下請けによる資金流出**: 1次受注企業から2次・3次のダミー下請けへの民間銀行送金は調達網の外部となるため、エスクロー型下請け代金支払システムとの連携が求められます。

---

### 5. 結び：AIは監査官を代替するのではなく、100倍加速する

AI監査の真髄は人間の代替ではなく、全数調査による死角の撲滅です。次回は、本システムをオンプレミスおよびKubernetesへ無停止デプロイするDevOps/MLOps構成を解説します。
'''
    },
    "zh-Hans": {
        "title": "国家预算AI审计中期成果：5大违规揭露与AI审计系统评估",
        "description": "国家预算AI审计系统中期运行结果：拆分随意签约、皮包公司围标、单价虚高10倍等查处案例（完全匿名化）及AI审计员精度与局限性评估。",
        "keywords": '["国家预算AI审计", "政府采购围标检测", "Text-to-SQL评估", "GraphRAG精度", "自主审计智能体"]',
        "content": '''---
slug: national-budget-ai-audit-findings-performance-evaluation
title: "国家预算AI审计中期成果：5大违规揭露与AI审计系统评估"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, enterprise-ai, public-budget, audit-ai]
date: 2026-11-19
keywords: ["国家预算AI审计", "政府采购围标检测", "Text-to-SQL评估", "GraphRAG精度", "自主审计智能体"]
description: "国家预算AI审计系统中期运行结果：拆分随意签约、皮包公司围标、单价虚高10倍等查处案例（完全匿名化）及AI审计员精度与局限性评估。"
---

![National Budget AI Audit Findings](./images/01_national_budget_audit_findings.png)

> 📌 **核心摘要 (Key Takeaways)**
> - **中期审计范围**: 在涵盖约650万亿韩元的公共财政数据中，针对5项核心预算项目和6项政府采购合同，全面运行了自主AI审计系统([`national_budget_ai`](file:///D:/ai/antigravity/national_budget_ai))。
> - **4大核心违规查处（严格匿名化）**:
>   1. **拆分规避公开招标**: 利用2000万韩元以下小额单一来源采购规定，在12天内将同一项目拆分为3笔合同（总计5820万韩元，违反国家合同法，审计院先例匹配度94.5%）。
>   2. **同地址空壳公司围标网络**: 3家挂牌在同一大厦同一室的关联企业联合参与竞标（总金额2.13亿韩元）。
>   3. **单价虚高7至10倍**: 专家咨询费高出公立中位数7.0倍，GPU服务器机架租赁费高出采购中位数10.0倍。
>   4. **预算传导效率低下(DEI 30.0%)**: 仅30.0%资金直达最终受益群体，70.0%被中间管理及外包环节截留。
> - **系统综合性能评估**: 
>   - **精度**: 基于确定性Text-to-SQL实现财务计算零幻觉，11项集成测试套件100%全数通过。
>   - **速度**: 生成完整法律证据卷宗平均耗时0.03秒。
>   - **局限性**: 剖析了隐名实控人与多级民间转包资金追踪的技术盲区。

{/* truncate */}

---

### ⚠️ 法律声明与匿名化说明 (Legal Notice & Anonymization)

> **【注意】本文所有案例均已严格实施去标识化与匿名处理。**  
> 本报告旨在从工程架构角度分享AI在财政审计中的实战检验数据。为保护相关机构与企业的合法权益，文中所涉及的**发包单位（如`A公团`、`B部委`）、中标企业（如`A公司`、`B公司`）、合同编号（如`CNTR-2026-0001`）及详细登记地址均已进行代称替换与掩码隐藏**。

---

### 1. 审计运行概况与查处成果汇总

正如架构篇所述，我们构建了融合**确定性Text-to-SQL引擎**与**GraphRAG知识图谱推理引擎**的自主审计流水线。

在导入实际政府采购与财政台账数据后，系统即刻触发了**6项高/极高风险警报**并自动归档了法律卷宗。

| 业务/合同标识（代称） | 涉事单位 / 中标商 | 违规类型 | 适用法条与先例 | AI检测机制 | 风险等级 |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `CNTR-2026-0001~3` | A公团 / A公司 | **化整为零随意签约** (5820万) | 国家合同法施行令第68条<br/>审计院 `BAI-2023-041` | 时间滑动窗口算法 | 🔴 **HIGH** |
| `CNTR-2026-0004` | B部委 / B公司 | **共享注册地址围标** (3850万) | 国家合同法第27条<br/>审计院 `BAI-2024-009` | GraphRAG同一地址节点 | 🔴 **CRITICAL** |
| `CNTR-2026-0005` | A公团 / 卡特尔(B·C公司) | **跨项目串通投标** (1.746亿) | 反垄断法第40条<br/>审计院 `BAI-2024-009` | 知识图谱子图遍历 | 🔴 **CRITICAL** |
| `CNTR-2026-0006` (项1) | B部委外包项目 | **咨询单价虚高7.0倍** | 预算执行指南<br/>国会预算政策处 `NABO-2023-R05` | 统计中位数偏离规则 | 🟠 **MEDIUM** |
| `CNTR-2026-0006` (项2) | B部委外包项目 | **机架租赁虚高10.0倍** | 预算执行指南<br/>国会预算政策处 `NABO-2023-R05` | 基准价格偏离引擎 | 🔴 **HIGH** |
| `PROG-2026-0001` | A公团直营项目 | **传导效率不足** (DEI 30.0%) | 财政补贴管理法<br/>间接管理成本漏损 | 科目支出占比归集 | 🟠 **MEDIUM** |

---

### 2. AI审计员查获的4大典型违规剖析

#### (1) 案例1：规避招标的“化整为零时间差拆分合同”
* **违法手段**: 发包方`A公团`在12天内将同一平台升级任务拆为3份（6月1日1950万、6月5日1920万、6月12日1950万），均直接定向授予`A公司`，累计金额超标。
* **AI检测**: 传统人工核查难以在数万条记录中捕捉跨天拆分。AI审计系统的**时间滑动窗口算法（30天聚合）**在0.001秒内完成发包方-承接方合同累计，精准匹配审计院判例`BAI-2023-041`（相似度94.5%）。

#### (2) 案例2：共享注册地址的皮包公司围标网络
* **违法手段**: `B公司`与`C公司`表面互为竞标对手，但工商地址完全重叠于首尔市某大厦同一房间。
* **AI检测**: `EntityResolver`统一清洗地址后，**GraphRAG知识图谱通过实体-地址共现图谱计算中心度与回环**，精准锁定共谋卡特尔，并引用审计院`BAI-2024-009`建议限制投标资格。

#### (3) 案例3：非结构化预算表中单价虚高7~10倍
* **手段与检测**: 解析非结构化表格，将专家咨询费（35万/小时 vs 行业中位数5万/小时）及机柜租金（50万/月 vs 标准中位数5万/月）与官方标准库对比，自动触发超标预警。

#### (4) 案例4：项目传导效率(DEI)仅30% — 70%资金流失于中间环节
* **评估公式**: $DEI = \frac{\text{直达受惠对象资金}}{\text{总下拨预算}} \times 100$。
* **现状**: 100亿韩元项目中，仅30亿直达扶持对象，70亿被各级管理费消耗。

---

### 3. AI审计系统综合性能与精度评估

```mermaid
xychart-beta
    title "AI审计引擎基准性能测试 (精度 / 延迟 / 判例匹配率)"
    x-axis ["测试通过率 (%)", "财务计算误差 (%)", "先例匹配度 (%)", "卷宗生成耗时 (秒*100)"]
    y-axis "指标值" 0 --> 100
    bar [100, 0, 94.5, 3]
```

1. **零财务计算幻觉**: 剥离LLM的数学运算功能，由确定性AST校验引擎执行底层SQL，实现**0.00%计算差错**。
2. **极高吞吐能力**: 单笔违规线索整理至Markdown卷宗仅需**0.03秒**。
3. **法律执行力挂钩**: 直接生成包含具体法条及处分建议的公文草案。

---

### 4. 实战盲区与后续演进

1. **隐名实控人与亲友代持**: 单纯政府采购数据无法突破代持迷雾，亟需引入税务股东底册与反洗钱(AML)实控人数据库。
2. **多级转包体外循环**: 一级中标商通过商业银行向二三级皮包公司分流资金时脱离采购网，后续需对接工程款托管保障系统。

---

### 5. 结语：AI并不取代审计员，而是赋予其百倍效能

AI的使命在于通过全量扫描杜绝监管死角。下一篇我们将深入探讨该系统在企业级专有云及Kubernetes集群中的安全部署与MLOps监控。
'''
    },
    "zh-Hant": {
        "title": "國家預算AI審計中期成果：5大違規揭露與AI審計系統評估",
        "description": "國家預算AI審計系統中期運行結果：拆分隨意簽約、空殼公司圍標、單價虛高10倍等查處案例（完全匿名化）及AI審計員精度與局限性評估。",
        "keywords": '["國家預算AI審計", "政府採購圍標檢測", "Text-to-SQL評估", "GraphRAG精度", "自主審計智慧體"]',
        "content": '''---
slug: national-budget-ai-audit-findings-performance-evaluation
title: "國家預算AI審計中期成果：5大違規揭露與AI審計系統評估"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, enterprise-ai, public-budget, audit-ai]
date: 2026-11-19
keywords: ["國家預算AI審計", "政府採購圍標檢測", "Text-to-SQL評估", "GraphRAG精度", "自主審計智慧體"]
description: "國家預算AI審計系統中期運行結果：拆分隨意簽約、空殼公司圍標、單價虛高10倍等查處案例（完全匿名化）及AI審計員精度與局限性評估。"
---

![National Budget AI Audit Findings](./images/01_national_budget_audit_findings.png)

> 📌 **核心摘要 (Key Takeaways)**
> - **中期審計範圍**: 在涵蓋約650萬億韓元的公共財政數據中，針對5項核心預算項目和6項政府採購合同，全面運行了自主AI審計系統([`national_budget_ai`](file:///D:/ai/antigravity/national_budget_ai))。
> - **4大核心違規查處（嚴格匿名化）**:
>   1. **拆分規避公開招標**: 利用2000萬韓元以下小額單一來源採購規定，在12天內將同一項目拆分為3筆合同（總計5820萬韓元，違反國家合同法，審計院先例匹配度94.5%）。
>   2. **同地址空殼公司圍標網絡**: 3家掛牌在同一大廈同一室的關聯企業聯合參與競標（總金額2.13億韓元）。
>   3. **單價虛高7至10倍**: 專家諮詢費高出公立中位數7.0倍，GPU伺服器機架租賃費高出採購中位數10.0倍。
>   4. **預算傳導效率低下(DEI 30.0%)**: 僅30.0%資金直達最終受益群體，70.0%被中間管理及外包環節截留。
> - **系統綜合性能評估**: 
>   - **精度**: 基於確定性Text-to-SQL實現財務計算零幻覺，11項集成測試套件100%全數通過。
>   - **速度**: 生成完整法律證據卷宗平均耗時0.03秒。
>   - **局限性**: 剖析了隱名實控人與多級民間轉包資金追蹤的技術盲區。

{/* truncate */}

---

### ⚠️ 法律聲明與匿名化說明 (Legal Notice & Anonymization)

> **【注意】本文所有案例均已嚴格實施去識別化與匿名處理。**  
> 本報告旨在從工程架構角度分享AI在財政審計中的實戰檢驗數據。為保護相關機構與企業的合法權益，文中所涉及的**發包單位（如`A公團`、`B部委`）、中標企業（如`A公司`、`B公司`）、合同編號（如`CNTR-2026-0001`）及詳細登記地址均已進行代稱替換與掩碼隱藏**。

---

### 1. 審計運行概況與查處成果匯總

正如架構篇所述，我們構建了融合**確定性Text-to-SQL引擎**與**GraphRAG知識圖譜推理引擎**的自主審計流水線。

在導入實際政府採購與財政台賬數據後，系統即刻觸發了**6項高/極高風險警報**並自動歸檔了法律卷宗。

| 業務/合同標識（代稱） | 涉事單位 / 中標商 | 違規類型 | 適用法條與先例 | AI檢測機制 | 風險等級 |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `CNTR-2026-0001~3` | A公團 / A公司 | **化整為零隨意簽約** (5820萬) | 國家合同法施行令第68條<br/>審計院 `BAI-2023-041` | 時間滑動窗口算法 | 🔴 **HIGH** |
| `CNTR-2026-0004` | B部委 / B公司 | **共享註冊地址圍標** (3850萬) | 國家合同法第27條<br/>審計院 `BAI-2024-009` | GraphRAG同一地址節點 | 🔴 **CRITICAL** |
| `CNTR-2026-0005` | A公團 / 卡特爾(B·C公司) | **跨項目串通投標** (1.746億) | 反壟斷法第40條<br/>審計院 `BAI-2024-009` | 知識圖譜子圖遍歷 | 🔴 **CRITICAL** |
| `CNTR-2026-0006` (項1) | B部委外包項目 | **諮詢單價虛高7.0倍** | 預算執行指南<br/>國會預算政策處 `NABO-2023-R05` | 統計中位數偏離規則 | 🟠 **MEDIUM** |
| `CNTR-2026-0006` (項2) | B部委外包項目 | **機架租賃虛高10.0倍** | 預算執行指南<br/>國會預算政策處 `NABO-2023-R05` | 基準價格偏離引擎 | 🔴 **HIGH** |
| `PROG-2026-0001` | A公團直營項目 | **傳導效率不足** (DEI 30.0%) | 財政補貼管理法<br/>間接管理成本漏損 | 科目支出占比歸集 | 🟠 **MEDIUM** |

---

### 2. AI審計員查獲的4大典型違規剖析

#### (1) 案例1：規避招標的「化整為零時間差拆分合同」
* **手段**: 發包方`A公團`在12天內將同一平台升級任務拆為3份（1950萬、1920萬、1950萬），均直接定向授予`A公司`。
* **AI檢測**: **時間滑動窗口算法（30天窗口）**在0.001秒內精準捕捉跨天分拆並匹配審計院判例`BAI-2023-041`。

#### (2) 案例2：共享註冊地址的空殼公司圍標網絡
* **手段**: `B公司`與`C公司`表面互為競標對手，但工商地址完全重疊於首爾市某大廈同一房間。
* **AI檢測**: `EntityResolver`正規化後，**GraphRAG知識圖譜遍歷共現地址節點**，鎖定圍標集團。

#### (3) 案例3：非結構化預算表中單價虛高7~10倍
* **手段與檢測**: 解析非結構化表格，將專家諮詢費（35萬/小時 vs 5萬中位數）及機櫃租金（50萬/月 vs 5萬中位數）自動對比預警。

#### (4) 案例4：項目傳導效率(DEI)僅30%
* **指標**: $DEI = \frac{\text{直達受惠對象資金}}{\text{總下撥預算}} \times 100$。100億韓元項目中僅30億元直達扶持對象。

---

### 3. AI審計系統綜合性能與精度評估

```mermaid
xychart-beta
    title "AI審計引擎基準性能測試 (精度 / 延遲 / 判例匹配率)"
    x-axis ["測試通過率 (%)", "財務計算誤差 (%)", "先例匹配度 (%)", "卷宗生成耗時 (秒*100)"]
    y-axis "指標值" 0 --> 100
    bar [100, 0, 94.5, 3]
```

1. **零財務計算幻覺**: 透過確定性AST檢驗引擎執行底層SQL，達成**0.00%計算差錯**。
2. **極高吞吐能力**: 單筆違規線索生成完整卷宗僅需**0.03秒**。
3. **法律執行力連結**: 自動生成包含適用法規與處分建議的公文草案。

---

### 4. 實戰盲區與後續演進

1. **隱名實控人與親友代持**: 亟需引入稅務股東底冊與實質受益人(UBO)數據庫。
2. **多級轉包體外循環**: 需對接政府工程款託管保障系統，穿透民間多層下包。

---

### 5. 結語：AI並不取代審計員，而是賦予其百倍效能

AI的使命在於消滅死角。下一篇我們將探討該系統在企業私有雲與Kubernetes集群中的零信任部署。
'''
    },
    "es": {
        "title": "Auditoría IA de Presupuesto Público: Fraudes y Evaluación",
        "description": "Resultados provisionales de auditoría de presupuestos públicos con IA: Casos anonimizados de cárteles, contratos divididos y sobreprecios de 10x.",
        "keywords": '["Auditoría Presupuesto IA", "Fraude en Compras Públicas", "Evaluación Text-to-SQL", "Precisión GraphRAG", "Agente Autónomo"]',
        "content": '''---
slug: national-budget-ai-audit-findings-performance-evaluation
title: "Auditoría IA de Presupuesto Público: Fraudes y Evaluación"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, enterprise-ai, public-budget, audit-ai]
date: 2026-11-19
keywords: ["Auditoría Presupuesto IA", "Fraude en Compras Públicas", "Evaluación Text-to-SQL", "Precisión GraphRAG", "Agente Autónomo"]
description: "Resultados provisionales de auditoría de presupuestos públicos con IA: Casos anonimizados de cárteles, contratos divididos y sobreprecios de 10x."
---

![National Budget AI Audit Findings](./images/01_national_budget_audit_findings.png)

> 📌 **Puntos Clave (Key Takeaways)**
> - **Despliegue Provisional**: Ejecutamos nuestro agente de auditoría autónomo ([`national_budget_ai`](file:///D:/ai/antigravity/national_budget_ai)) sobre registros reales de contratación pública (5 programas y 6 contratos clave).
> - **4 Fraudes Detectados (Completamente Anonimizados)**:
>   1. **Contratos Divididos (Smurfing)**: Fraccionamiento de proyectos bajo el umbral de $20,000 durante 12 días para eludir licitaciones abiertas ($43,000 en total).
>   2. **Cártel con Dirección Compartida**: 3 empresas fantasma registradas en la misma sala ganando licitaciones públicas.
>   3. **Sobreprecios de 7x a 10x**: Tarifas de asesoría infladas 7 veces y alquiler de racks GPU 10 veces respecto a la mediana oficial.
>   4. **Fuga en Eficiencia de Entrega (DEI 30%)**: Solo el 30% llegó a beneficiarios finales, perdiéndose el 70% en gastos de gestión.
> - **Evaluación del Sistema**: 0.00% alucinación financiera, latencia de 0.03s por informe y análisis de límites prácticos en el terreno.

{/* truncate */}

---

### ⚠️ Aviso Legal y Anonimización (Legal Notice & Anonymization)

> **[Aviso Obligatorio] Todos los casos han sido estrictamente anonimizados.**  
> Con el fin de evitar litigios y proteger la confidencialidad, las identidades de agencias (`Agencia A`, `Ministerio B`), contratistas (`Empresa A`, `Empresa B`), números de contrato y direcciones físicas han sido completamente enmascaradas.

---

### 1. Resumen de Hallazgos y Ejecución de Auditoría

Al conectar nuestro motor híbrido (**Text-to-SQL Determinista + GraphRAG**), se generaron de forma inmediata **6 alertas de alto riesgo** y expedientes sancionadores automáticos.

| Identificador (Enmascarado) | Entidad / Contratista | Tipo de Infracción | Ley y Precedente | Mecanismo IA | Nivel de Riesgo |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `CNTR-2026-0001~3` | Agencia A / Empresa A | **Contratos Divididos** ($43K) | Ley de Contratos Art. 68<br/>Tribunal Cuentas `BAI-2023-041` | Ventana Temporal Móvil | 🔴 **HIGH** |
| `CNTR-2026-0004` | Ministerio B / Empresa B | **Cártel Misma Dirección** ($28K) | Ley de Contratos Art. 27<br/>Tribunal Cuentas `BAI-2024-009` | GraphRAG Nodo Dirección | 🔴 **CRITICAL** |
| `CNTR-2026-0005` | Agencia A / Cártel B y C | **Colusión en Licitación** ($130K) | Ley de Competencia Art. 40<br/>Tribunal Cuentas `BAI-2024-009` | Recorrido de Subgrafos | 🔴 **CRITICAL** |
| `CNTR-2026-0006` (1) | Proyecto Externalizado | **Asesoría Inflada 7.0x** | Guías de Ejecución Fiscal<br/>Informe NABO `NABO-2023-R05` | Desviación Mediana Oficial | 🟠 **MEDIUM** |
| `CNTR-2026-0006` (2) | Proyecto Externalizado | **Racks GPU Inflados 10.0x** | Guías de Ejecución Fiscal<br/>Informe NABO `NABO-2023-R05` | Motor de Precios Base | 🔴 **HIGH** |
| `PROG-2026-0001` | Subvención Directa | **Baja Eficiencia (DEI 30%)** | Ley de Subvenciones<br/>Fuga en Gastos Indirectos | Agregador de Partidas | 🟠 **MEDIUM** |

---

### 2. Análisis de las 4 Irregularidades Principales

1. **Fraccionamiento de Contratos**: Para evadir licitaciones abiertas, se emitieron 3 contratos privados en 12 días por $14,500 cada uno a la `Empresa A`. El algoritmo de ventana temporal detectó la acumulación en milisegundos.
2. **Cártel con Dirección Idéntica**: La `Empresa B` y la `Empresa C` simularon competir, pero compartían la misma oficina en Seúl. GraphRAG detectó la centralidad del nodo físico.
3. **Inflación de Precios Unitarios**: Parseo de tablas HWPX descubrió tarifas horarias de consultoría a $260/h frente a la mediana de $37/h (7x).
4. **Índice de Eficiencia de Entrega (DEI)**: Solo el 30% del presupuesto llegó a los beneficiarios finales.

---

### 3. Evaluación de Rendimiento del Motor IA

```mermaid
xychart-beta
    title "Benchmarks del Motor de Auditoría IA (Precisión / Latencia / Jurisprudencia)"
    x-axis ["Aprobación Pruebas (%)", "Error Financiero (%)", "Alineación Legal (%)", "Latencia Expediente (s*100)"]
    y-axis "Métrica" 0 --> 100
    bar [100, 0, 94.5, 3]
```

* **Cero Alucinación Financiera**: Cálculos delegados a un AST SQL determinista (11/11 pruebas pasadas con 0% de error).
* **Alta Velocidad**: 0.03 segundos para formular el expediente sancionador legal.

---

### 4. Límites Prácticos y Próximos Retos

* **Testaferros y Empresas Fantasma Descentralizadas**: Domicilios distintos impiden la detección sin acceso a registros de titularidad real (UBO) e impuestos.
* **Subcontratación Privada Multinivel**: Los pagos a subcontratistas en cuentas privadas escapan del portal público sin integración con sistemas de custodia (Escrow).

---

### 5. Conclusión

La IA no reemplaza a los auditores; los acelera 100 veces eliminando puntos ciegos. En la Parte 3 analizaremos su despliegue en Kubernetes y MLOps continuo.
'''
    },
    "de": {
        "title": "KI-Haushaltsprüfung: 5 Betrugsfälle & Systembewertung",
        "description": "Zwischenergebnisse der KI-Haushaltsprüfung: Anonymisierte Fälle von Kartellen, Stückelungsverträgen und 10-fachen Aufschlägen sowie Systembewertung.",
        "keywords": '["KI-Haushaltsprüfung", "Vergabebetrugserkennung", "Text-to-SQL-Bewertung", "GraphRAG-Präzision", "Autonomer Prüfagent"]',
        "content": '''---
slug: national-budget-ai-audit-findings-performance-evaluation
title: "KI-Haushaltsprüfung: 5 Betrugsfälle & Systembewertung"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, enterprise-ai, public-budget, audit-ai]
date: 2026-11-19
keywords: ["KI-Haushaltsprüfung", "Vergabebetrugserkennung", "Text-to-SQL-Bewertung", "GraphRAG-Präzision", "Autonomer Prüfagent"]
description: "Zwischenergebnisse der KI-Haushaltsprüfung: Anonymisierte Fälle von Kartellen, Stückelungsverträgen und 10-fachen Aufschlägen sowie Systembewertung."
---

![National Budget AI Audit Findings](./images/01_national_budget_audit_findings.png)

> 📌 **Kernaussagen (Key Takeaways)**
> - **Zwischenprüfung**: Unser autonomer KI-Prüfungsagent ([`national_budget_ai`](file:///D:/ai/antigravity/national_budget_ai)) wurde auf repräsentative öffentliche Beschaffungsdaten angewendet (5 Haushaltsprogramme, 6 Verträge).
> - **4 Aufgedeckte Kernverstöße (Vollständig Anonymisiert)**:
>   1. **Gestückelte Freihändige Vergaben**: Umgehung offener Ausschreibungen durch 3 Teilverträge unter 20.000 $ innerhalb von 12 Tagen (Gesamt: 43.000 $).
>   2. **Scheinfirmenkartelle mit Identischer Adresse**: 3 Scheinfirmen im selben Büro manipulierten Ausschreibungen.
>   3. **7- bis 10-fache Preisüberhöhung**: Beratungsstundensätze (7x) und Servermieten (10x) über dem Median.
>   4. **Geringe Auslieferungseffizienz (DEI 30%)**: Nur 30% der Mittel erreichten Begünstigte; 70% versickerten in Verwaltungskosten.
> - **Leistungsbewertung**: 0,00% Finanzhalluzination durch deterministisches Text-to-SQL, 0,03s Latenz pro Dossier.

{/* truncate */}

---

### ⚠️ Rechtlicher Hinweis & Anonymisierung (Legal Notice)

> **[Wichtiger Hinweis] Alle Vorgänge wurden zum Schutz der Beteiligten vollständig anonymisiert.**  
> Behörden (`Behörde A`), Unternehmen (`Firma A`, `Firma B`), Vertragsnummern und Adressen wurden durch Pseudonyme und Maskierungen ersetzt.

---

### 1. Prüfungsüberblick und Übersicht der Verstöße

Die Pipeline löste sofort **6 Hochrisiko-Warnmeldungen** aus und erstellte prüffeste Berichte mit Gesetzesbezug.

| Vertrags-ID (Maskiert) | Akteur / Auftragnehmer | Verstoß | Gesetz & Präzedenzfall | KI-Erkennungsmechanismus | Risiko |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `CNTR-2026-0001~3` | Behörde A / Firma A | **Gestückelte Vergabe** (43T $) | Vergaberecht Art. 68<br/>Rechnungshof `BAI-2023-041` | Gleitendes Zeitfenster | 🔴 **HIGH** |
| `CNTR-2026-0004` | Ministerium B / Firma B | **Adresskartell** (28T $) | Vergaberecht Art. 27<br/>Rechnungshof `BAI-2024-009` | GraphRAG Adressknoten | 🔴 **CRITICAL** |
| `CNTR-2026-0005` | Behörde A / Kartell (B&C) | **Angebotsabsprachen** (130T $) | Kartellgesetz Art. 40<br/>Rechnungshof `BAI-2024-009` | Subgraphentraversierung | 🔴 **CRITICAL** |
| `CNTR-2026-0006` (1) | Fremdvergabe | **Beratungshonorar 7x** | Haushaltsrichtlinien<br/>Prüfbericht `NABO-2023-R05` | Median-Abweichungsregel | 🟠 **MEDIUM** |
| `CNTR-2026-0006` (2) | Fremdvergabe | **Servermiete 10x** | Haushaltsrichtlinien<br/>Prüfbericht `NABO-2023-R05` | Referenzpreis-Engine | 🔴 **HIGH** |
| `PROG-2026-0001` | Förderprogramm | **Niedrige DEI (30%)** | Subventionsgesetz<br/>Verwaltungskostenüberschreitung | Kostenstellenaggregation | 🟠 **MEDIUM** |

---

### 2. Analyse der 4 Hauptverstöße

1. **Gestückelte Vergaben**: Innerhalb von 12 Tagen wurden drei Verträge über je 14.500 $ an `Firma A` vergeben. Das Zeitfenstermodell deckte die Umgehung in 0,001s auf.
2. **Scheinfirmenkartell**: `Firma B` und `Firma C` traten als Konkurrenten auf, teilten sich jedoch dieselbe Büronummer. GraphRAG identifizierte die Scheinbieter.
3. **Preisüberhöhung**: XML-Tabellenparsing deckte Beratungssätze von 260 $/h gegenüber dem Richtwert von 37 $/h auf.
4. **DEI-Index**: Von 7,5 Mio. $ Budget kamen nur 2,25 Mio. $ direkt an.

---

### 3. Leistungsbewertung des KI-Systems

```mermaid
xychart-beta
    title "KI-Prüfungsengine Benchmark (Genauigkeit / Latenz / Rechtssicherheit)"
    x-axis ["Testquote (%)", "Rechenfehler (%)", "Präzedenzfallabgleich (%)", "Dossier-Latenz (s*100)"]
    y-axis "Messwert" 0 --> 100
    bar [100, 0, 94.5, 3]
```

* **Null Halluzination**: Deterministisches SQL verhindert jegliche Zahlenfälschung (11/11 Tests bestanden).
* **Latenz**: 0,03 Sekunden pro Dossier.

---

### 4. Grenzen in der Praxis

Strohmänner und mehrstufige private Subunternehmerflüsse erfordern künftig Anbindungen an Steuerregister und Treuhand-Zahlungssysteme.

---

### 5. Fazit

KI ersetzt keine Rechnungsprüfer, sondern beschleunigt sie um das Hundertfache. Teil 3 widmet sich dem Kubernetes- und MLOps-Betrieb.
'''
    },
    "fr": {
        "title": "Audit IA du Budget Public : 5 Fraudes et Évaluation",
        "description": "Résultats intermédiaires d'audit budgétaire par IA : Cas anonymisés d'ententes, contrats fractionnés et surfacturations 10x, avec évaluation du système.",
        "keywords": '["Audit Budgétaire IA", "Détection Fraude Marchés", "Évaluation Text-to-SQL", "Précision GraphRAG", "Agent d\'Audit Autonome"]',
        "content": '''---
slug: national-budget-ai-audit-findings-performance-evaluation
title: "Audit IA du Budget Public : 5 Fraudes et Évaluation"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, enterprise-ai, public-budget, audit-ai]
date: 2026-11-19
keywords: ["Audit Budgétaire IA", "Détection Fraude Marchés", "Évaluation Text-to-SQL", "Précision GraphRAG", "Agent d\'Audit Autonome"]
description: "Résultats intermédiaires d'audit budgétaire par IA : Cas anonymisés d'ententes, contrats fractionnés et surfacturations 10x, avec évaluation du système."
---

![National Budget AI Audit Findings](./images/01_national_budget_audit_findings.png)

> 📌 **Points Clés (Key Takeaways)**
> - **Déploiement d'Étape**: Notre agent d'audit autonome ([`national_budget_ai`](file:///D:/ai/antigravity/national_budget_ai)) a réalisé un audit exhaustif sur des jeux de données réels (5 programmes budgétaires et 6 marchés publics).
> - **4 Fraudes Majeures Détectées (Totalement Anonymisées)** :
>   1. **Contrats Fractionnés (Saucissonnage)** : 3 contrats sous le seuil de 20 000 $ en 12 jours pour éviter la mise en concurrence (43 000 $ au total).
>   2. **Cartel à Adresse Partagée** : 3 sociétés écrans partageant la même pièce pour simuler une fausse concurrence.
>   3. **Surfacturation de 7x à 10x** : Honoraires de conseil multipliés par 7 et location de serveurs par 10 par rapport à la médiane.
>   4. **Faible Efficacité de Distribution (DEI 30%)** : Seuls 30% des crédits sont parvenus aux bénéficiaires finaux (70% de frais administratifs).
> - **Évaluation du Système** : 0,00% d'erreur financière via Text-to-SQL déterministe, latence de 0,03s par dossier.

{/* truncate */}

---

### ⚠️ Mention Légale et Anonymisation (Legal Notice)

> **[Avis Impératif] Toutes les entités et données ont été rigoureusement anonymisées.**  
> Afin d'éviter tout litige, les noms d'agences (`Agence A`), de prestataires (`Société A`, `Société B`), les numéros de contrat et adresses ont été entièrement masqués.

---

### 1. Synthèse de l'Audit et Résultats

Dès l'exécution de notre pipeline combinant **Text-to-SQL déterministe et GraphRAG**, **6 alertes critiques** ont été déclenchées avec production automatique de dossiers d'audit juridiquement étayés.

| Réf. Contrat (Masquée) | Entité / Titulaire | Type d'Infraction | Base Légale & Précédent | Mécanisme IA | Niveau de Risque |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `CNTR-2026-0001~3` | Agence A / Société A | **Fractionnement Abusif** (43k $) | Code des Marchés Art. 68<br/>Cour des Comptes `BAI-2023-041` | Fenêtre Temporelle Glissante | 🔴 **HIGH** |
| `CNTR-2026-0004` | Ministère B / Société B | **Entente Même Adresse** (28k $) | Code des Marchés Art. 27<br/>Cour des Comptes `BAI-2024-009` | GraphRAG Noeud Adresse | 🔴 **CRITICAL** |
| `CNTR-2026-0005` | Agence A / Cartel (B & C) | **Offres Concertées** (130k $) | Droit de la Concurrence<br/>Cour des Comptes `BAI-2024-009` | Traversée de Sous-graphe | 🔴 **CRITICAL** |
| `CNTR-2026-0006` (1) | Projet Externalisé | **Honoraires x7,0** | Règles Budgétaires<br/>Rapport `NABO-2023-R05` | Règle Déviation Médiane | 🟠 **MEDIUM** |
| `CNTR-2026-0006` (2) | Projet Externalisé | **Baies Serveurs x10,0** | Règles Budgétaires<br/>Rapport `NABO-2023-R05` | Écart Prix de Référence | 🔴 **HIGH** |
| `PROG-2026-0001` | Subvention Directe | **Faible DEI (30%)** | Loi sur les Subventions<br/>Fuite Frais Indirects | Agrégation Analytique | 🟠 **MEDIUM** |

---

### 2. Analyse Approfondie des 4 Cas Détectés

1. **Fractionnement de Marchés** : Pour éviter l'appel d'offres ouvert, l'`Agence A` a découpé une mission en 3 contrats de 14 500 $ attribués à la `Société A` en 12 jours. Détecté en 0,001s.
2. **Sociétés Écrans à Adresse Commune** : Les soumissionnaires concurrents partageaient la même pièce à Séoul. GraphRAG a immédiatement mis au jour la structure de cartel.
3. **Surfacturation Unitaire** : Détection de tarifs de conseil à 260 $/h contre 37 $/h en médiane officielle.
4. **Indice d'Efficacité (DEI)** : Sur 7,5M $ de budget, seuls 2,25M $ ont atteint la cible finale.

---

### 3. Évaluation des Performances du Système IA

```mermaid
xychart-beta
    title "Benchmarks du Moteur d'Audit IA (Précision / Latence / Jurisprudence)"
    x-axis ["Taux Réussite Tests (%)", "Erreur Calcul (%)", "Précision Précédents (%)", "Latence Dossier (s*100)"]
    y-axis "Score" 0 --> 100
    bar [100, 0, 94.5, 3]
```

* **Zéro Hallucination** : Requêtes SQL pilotées par AST rigide (11/11 tests passés).
* **Vitesse Extrême** : 0,03s pour générer un dossier d'injonction administrative complet.

---

### 4. Limites Réelles et Défis

Les prête-noms et la sous-traitance privée en cascade exigent d'interconnecter le système aux bases fiscales et aux plateformes de paiement séquestre.

---

### 5. Conclusion

L'IA ne remplace pas les auditeurs, elle démultiplie leur vitesse par 100. Rendez-vous dans la Partie 3 pour le déploiement Kubernetes et MLOps.
'''
    },
    "pt-BR": {
        "title": "Auditoria IA do Orçamento Público: Fraudes e Avaliação",
        "description": "Resultados preliminares da auditoria de orçamento público com IA: Casos anonimizados de cartéis, contratos fracionados e superfaturamento de 10x.",
        "keywords": '["Auditoria Orçamento IA", "Fraude em Licitações", "Avaliação Text-to-SQL", "Precisão GraphRAG", "Agente Autônomo de Auditoria"]',
        "content": '''---
slug: national-budget-ai-audit-findings-performance-evaluation
title: "Auditoria IA do Orçamento Público: Fraudes e Avaliação"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, enterprise-ai, public-budget, audit-ai]
date: 2026-11-19
keywords: ["Auditoria Orçamento IA", "Fraude em Licitações", "Avaliação Text-to-SQL", "Precisão GraphRAG", "Agente Autônomo de Auditoria"]
description: "Resultados preliminares da auditoria de orçamento público com IA: Casos anonimizados de cartéis, contratos fracionados e superfaturamento de 10x."
---

![National Budget AI Audit Findings](./images/01_national_budget_audit_findings.png)

> 📌 **Principais Conclusões (Key Takeaways)**
> - **Execução Intermediária**: Nosso agente autônomo de auditoria ([`national_budget_ai`](file:///D:/ai/antigravity/national_budget_ai)) realizou uma varredura completa sobre dados reais de compras públicas (5 programas e 6 contratos chave).
> - **4 Fraudes Críticas Detectadas (Totalmente Anonimizadas)**:
>   1. **Fracionamento de Licitação**: Divisão de contratos abaixo do teto de dispensa ($20.000) em 12 dias para fugir da concorrência aberta ($43.000 no total).
>   2. **Cartel de Empresas Fantasma com Mesmo Endereço**: 3 empresas registradas na mesma sala simulando concorrência pública.
>   3. **Superfaturamento de 7x a 10x**: Consultorias 7 vezes acima da mediana e locação de servidores GPU inflada em 10 vezes.
>   4. **Baixo Índice de Eficiência de Entrega (DEI 30%)**: Apenas 30% chegaram aos beneficiários finais (70% retidos em custos administrativos).
> - **Avaliação de Desempenho**: Zero alucinação financeira via Text-to-SQL determinístico e latência de 0,03s por relatório.

{/* truncate */}

---

### ⚠️ Aviso Legal e Anonimização (Legal Notice)

> **[Aviso Obrigatório] Todos os casos foram rigorosamente anonimizados.**  
> Para evitar disputas legais, os órgãos públicos (`Órgão A`, `Ministério B`), contratadas (`Empresa A`, `Empresa B`), números de contrato e endereços foram completamente mascarados.

---

### 1. Resumo da Auditoria e Irregularidades Identificadas

A execução do pipeline híbrido gerou de imediato **6 alertas de alto risco** com relatórios jurídicos fundamentados.

| Código Contrato (Mascarado) | Entidade / Contratada | Tipo de Infração | Legislação & Jurisprudência | Mecanismo de Detecção IA | Risco |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `CNTR-2026-0001~3` | Órgão A / Empresa A | **Fracionamento de Contrato** ($43K) | Lei de Licitações Art. 68<br/>Tribunal de Contas `BAI-2023-041` | Janela Deslizante Temporal | 🔴 **HIGH** |
| `CNTR-2026-0004` | Ministério B / Empresa B | **Cartel Mesmo Endereço** ($28K) | Lei de Licitações Art. 27<br/>Tribunal de Contas `BAI-2024-009` | GraphRAG Nó de Endereço | 🔴 **CRITICAL** |
| `CNTR-2026-0005` | Órgão A / Cartel (B e C) | **Conluio em Licitação** ($130K) | Lei Concorrencial Art. 40<br/>Tribunal de Contas `BAI-2024-009` | Travessia de Subgrafo | 🔴 **CRITICAL** |
| `CNTR-2026-0006` (1) | Projeto Terceirizado | **Consultoria Inflada 7,0x** | Diretrizes Orçamentárias<br/>Relatório `NABO-2023-R05` | Regra de Desvio da Mediana | 🟠 **MEDIUM** |
| `CNTR-2026-0006` (2) | Projeto Terceirizado | **Servidor GPU Inflado 10,0x** | Diretrizes Orçamentárias<br/>Relatório `NABO-2023-R05` | Motor de Preço de Referência | 🔴 **HIGH** |
| `PROG-2026-0001` | Repasse Direto | **Baixa Eficiência (DEI 30%)** | Lei de Subvenções<br/>Vazamento em Custos Indiretos | Agregador Orçamentário | 🟠 **MEDIUM** |

---

### 2. Análise Detalhada dos 4 Principais Casos

1. **Fracionamento para Dispensa**: Três contratos de $14.500 concedidos à `Empresa A` em 12 dias para burlar licitação aberta. Detectado em 0,001s.
2. **Cartel no Mesmo Endereço**: A `Empresa B` e a `Empresa C` disputaram licitação dividindo a mesma sala comercial. GraphRAG apontou conluio imediato.
3. **Superfaturamento em Planilhas**: Parsing de tabelas HWPX revelou consultoria a $260/h contra mediana oficial de $37/h.
4. **Índice DEI**: De $7,5 milhões alocados, apenas $2,25 milhões chegaram aos beneficiários reais.

---

### 3. Avaliação de Desempenho do Sistema de Auditoria IA

```mermaid
xychart-beta
    title "Benchmarks do Motor de Auditoria IA (Precisão / Latência / Jurisprudência)"
    x-axis ["Aprovação Testes (%)", "Erro Cálculo (%)", "Aderência Legal (%)", "Latência Dossiê (s*100)"]
    y-axis "Métrica" 0 --> 100
    bar [100, 0, 94.5, 3]
```

* **Zero Alucinação Financeira**: Motor de consulta AST SQL determinístico (11/11 testes aprovados com 0% de erro).
* **Alta Velocidade**: 0,03 segundos para emissão do dossiê comprobatório.

---

### 4. Limitações de Campo e Desafios

Laranjas societários e subcontratação privada exigem integração futura com bases da Receita Federal e plataformas de pagamento em custódia (Escrow).

---

### 5. Conclusão

A IA não substitui auditores humanos; ela os acelera 100 vezes eliminando pontos cegos. Na Parte 3 abordaremos a infraestrutura Kubernetes e MLOps.
'''
    }
}

for loc, data in POSTS.items():
    loc_dir = os.path.join(BASE_DIR, loc)
    os.makedirs(loc_dir, exist_ok=True)
    post_file = os.path.join(loc_dir, "index.md")
    with open(post_file, "w", encoding="utf-8") as f:
        f.write(data["content"].strip() + "\n")
    print(f"Generated {loc}: {post_file} (Title: {len(data['title'])} chars, Desc: {len(data['description'])} chars)")
