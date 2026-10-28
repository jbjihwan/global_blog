# -*- coding: utf-8 -*-
import os

BASE_DIR = r"D:\ai\antigravity\global_blog\배포대기\2026-11-22-national-budget-ai-6-sector-full-suite\i18n"

POSTS = {
    "ja": {
        "title": "国家予算AI #5：6大標的分割監査の完成と年末予算ダンピング摘発",
        "description": "400万件の公共調達から死角を狙う6大標的分割監査体系。5千万ウォン特例の分割随意契約や12月末の予算消化ダンピング摘発の技術実録。",
        "keywords": '["6大標的分割監査", "女性企業5千万特例分割", "年末予算ダンピング", "調達異常検知AI", "公共財政監査"]',
        "content": '''---
slug: national-budget-ai-6-sector-full-suite
title: "国家予算AI #5：6大標的分割監査の完成と年末予算ダンピング摘発"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, procurement-fraud, year-end-dumping, spec-driven-development, devops]
date: 2026-11-22
keywords: ["6大標的分割監査", "女性企業5千万特例分割", "年末予算ダンピング", "調達異常検知AI", "公共財政監査"]
description: "400万件の公共調達から死角を狙う6大標的分割監査体系。5千万ウォン特例の分割随意契約や12月末の予算消化ダンピング摘発の技術実録。"
---

![6-Sector Targeted Audit: Divide & Conquer Suite](./images/01_national_budget_6_sector_suite.png)

> 📌 **要点まとめ (Key Takeaways)**
> - **6大標的分割監査の完成**: 年間400万件の公共調達データから85%の消耗品ノイズを除去し、不正が集中する**6大高リスク標的領域（Sector 1〜6）**の全数監査システムを構築。
> - **2大盲点の摘発**:
>   1. **Sector 5（5千万ウォン特例分割）**: 女性・障害者企業の随意契約限度額（5千万ウォン）を悪用し、**4,800万〜4,950万ウォンの上限直前で分割発注した2.45億ウォン**を摘発（監査院`BAI-2023-072`適合）。
>   2. **Sector 6（12月末の予算ダンピング）**: 予算不用返納を防ぐため、12月下旬のわずか4日間に特定企業へ集中発注した**1.64億ウォンの急造随意契約**を摘発（監査院`BAI-2022-094`適合）。
> - **事前設計による2大課題の克服**: 政策的優遇と不正分割を見分ける**スイートスポット（96〜99.8%）判定器**と、年末業務の物理的遂行可能性を逆算する時系列アナライザーを配備。
> - **実戦バグの解決**: セクター間重複分類の優先度ランク調整、消費税（VAT）内外判定の逆算正規化、会計年度繰越日の同期。

{/* truncate */}

---

### ⚠️ 法的告知および匿名化案内 (Legal Notice)

> **【注意】本稿の事例は厳格に匿名化されています。**  
> 機関名（`A公団`、`C公団`）、企業名（`D社`、`F社`）、人物名、契約番号はすべて仮名化・マスキング済みです。

---

### 1. 6大標的分割監査（Divide & Conquer）の全体像

```mermaid
flowchart TD
    Raw[年間400万件の公共調達データ] --> Filter{3次元標的分割マネージャー}
    Filter -->|85%正常消耗品| Drop[低リスクアーカイブ]
    Filter --> S1["Sector 1: 公共機関ICT少額分割"]
    Filter --> S2["Sector 2: 自治体イベント談合"]
    Filter --> S3["Sector 3: 委託事業間接費漏出(DEI)"]
    Filter --> S4["Sector 4: 50億超大型SOC入札談合"]
    Filter --> S5["🔴 Sector 5: 5千万ウォン特例分割"]
    Filter --> S6["🔴 Sector 6: 12月末不用防止ダンピング"]
    S1 & S2 & S3 & S4 & S5 & S6 --> Master[All Sectors Master Runner]
```

---

### 2. 事前想定された課題と予防設計

1. **合法特例と不正分割の境界**: 5千万ウォン上限の96.0%〜99.8%（4,800万〜4,990万ウォン）に集中し、同一発注者・受注者間で30日以内に反復される契約のみを高リスク指定。
2. **年末精算と突発ダンピングの識別**: 12月15日以降の超短期発注かつ会計閉鎖（12月31日）までの残日数が業務遂行に物理的に不足している契約を特定。

---

### 3. 実稼働で解決した3大突発バグ

1. **セクター間重複判定 ➔ 優先度ランク**: 法的ペナルティの重い順（特例悪用 ＞ 年末ダンピング ＞ 通常少額）に主セクターを決定。
2. **消費税（VAT）内外の混同 ➔ 予定価格逆算器**: 税込金額で5千万ウォンを超えて除外される現象を、税抜供給価格の逆算により是正。
3. **出納整理期間と会計年度のずれ ➔ 財政カレンダー正規化**: 繰越事業の判定精度を向上。

---

### 4. 摘発成果と17件全テスト合格

A公団の5千万ウォン特例スマーフィング（計1.47億ウォン）やC公団の12月下旬4日間3連続発注（計1.25億ウォン）を摘発。全17テストスイートを100%通過しました。
'''
    },
    "zh-Hans": {
        "title": "国家预算AI #5：六大靶向分区审计成型与年底突击花钱查处",
        "description": "在400万条政府采购记录中深挖死角的六大靶向分区审计系统。精准打击5000万韩元特例拆分单一来源与12月底突击花钱倾销的技术实录。",
        "keywords": '["六大靶向分区审计", "女性企业5千万特例拆分", "年底突击花钱倾销", "政府采购异常AI", "公共财政审计"]',
        "content": '''---
slug: national-budget-ai-6-sector-full-suite
title: "国家预算AI #5：六大靶向分区审计成型与年底突击花钱查处"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, procurement-fraud, year-end-dumping, spec-driven-development, devops]
date: 2026-11-22
keywords: ["六大靶向分区审计", "女性企业5千万特例拆分", "年底突击花钱倾销", "政府采购异常AI", "公共财政审计"]
description: "在400万条政府采购记录中深挖死角的六大靶向分区审计系统。精准打击5000万韩元特例拆分单一来源与12月底突击花钱倾销的技术实录。"
---

![6-Sector Targeted Audit: Divide & Conquer Suite](./images/01_national_budget_6_sector_suite.png)

> 📌 **核心摘要 (Key Takeaways)**
> - **六大靶向分区审计体系成型 (Divide & Conquer Full Suite)**: 在年均400万条庞大政府采购数据中过滤85%日常耗材噪音，构建覆盖腐败高发领域的**六大高危靶向分区（Sector 1~6）**全生命周期精准查处流水线。
> - **揭露两大隐秘死角**:
>   1. **Sector 5 (5000万韩元特例拆分)**: 利用扶持特例上限，在**4800万至4950万韩元临界区间恶意拆分并定向输送2.45亿韩元**（契合审计院先例`BAI-2023-072`）。
>   2. **Sector 6 (12月底突击花钱倾销)**: 为防预算收回，于12月下旬仅4天内向特定常客集中突击下发**1.64亿韩元单一来源合同**（契合审计院先例`BAI-2022-094`）。
> - **架构预判并解决2大难点**: 建立区分法定扶持与恶意拆分的**甜点区间分析器(96~99.8%)**，以及辨别突击花钱的**时间密集度与履约物理可行性反推引擎**。
> - **实战Bug排错**: 解决多分区重叠告警冲突、含税价与不含税价限额混淆计算、跨年度结转工期对齐问题。

{/* truncate */}

---

### ⚠️ 法律声明与匿名化说明 (Legal Notice)

> **【注意】本篇所有案例均已严格实施去标识化处理。**  
> 涉事机关（`A公团`、`C公团`）、企业（`D公司`、`F公司`）、当事人及合同编号均已做掩码隐藏。

---

### 1. 六大高危靶向分区审计总览

```mermaid
flowchart TD
    Raw[年均400万条政府采购数据] --> Filter{三维靶向分区管理器}
    Filter -->|85%常规耗材| Drop[低风险归档库]
    Filter --> S1["Sector 1: 公共机构ICT小额拆分"]
    Filter --> S2["Sector 2: 地方节庆投标围标"]
    Filter --> S3["Sector 3: 委托服务管理费漏损(DEI)"]
    Filter --> S4["Sector 4: 50亿+重大工程陪标垄断"]
    Filter --> S5["🔴 Sector 5: 5000万特例恶意拆分"]
    Filter --> S6["🔴 Sector 6: 12月底突击花钱倾销"]
    S1 & S2 & S3 & S4 & S5 & S6 --> Master[All Sectors Master Runner]
```

---

### 2. 预判挑战与架构防护

1. **法定政策特例与恶意拆分的辨别**: 仅锁定合同金额落入上限96%~99.8%区间且30天内由同一发包方频繁定向签署的异常合约。
2. **正常年终结算与突击倾销的辨识**: 针对12月15日后密集签约、且距年底结算日剩余时间无法完成真实交付的项目进行红牌预警。

---

### 3. 实战攻克3大突发Bug

1. **多分区间冲突导致重复告警**: 引入优先级排序器，按法纪严苛程度归集为主分区与辅助标签。
2. **含税与不含税价格导致限额误判**: 增设增值税剥离归一化器，自动还原不含税预算基数。
3. **财政年度与公历年度跨期误差**: 建立财政日历对照解析器，解决项目跨年结转时间错位。

---

### 4. 查处战果与17项全流程验证

查处A公团定向向D公司拆分输送1.47亿韩元，以及C公团12月下旬4天密集签发3笔课题（1.25亿韩元）案，全套17项测试100%全数通过。
'''
    },
    "zh-Hant": {
        "title": "國家預算AI #5：六大靶向分區審計成型與年底突擊花錢查處",
        "description": "在400萬條政府採購記錄中深挖死角的六大靶向分區審計系統。精準打擊5000萬韓元特例拆分單一來源與12月底突擊花錢傾銷的技術實錄。",
        "keywords": '["六大靶向分區審計", "女性企業5千萬特例拆分", "年底突擊花錢傾銷", "政府採購異常AI", "公共財政審計"]',
        "content": '''---
slug: national-budget-ai-6-sector-full-suite
title: "國家預算AI #5：六大靶向分區審計成型與年底突擊花錢查處"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, procurement-fraud, year-end-dumping, spec-driven-development, devops]
date: 2026-11-22
keywords: ["六大靶向分區審計", "女性企業5千萬特例拆分", "年底突擊花錢傾銷", "政府採購異常AI", "公共財政審計"]
description: "在400萬條政府採購記錄中深挖死角的六大靶向分區審計系統。精準打擊5000萬韓元特例拆分單一來源與12月底突擊花錢傾銷的技術實錄。"
---

![6-Sector Targeted Audit: Divide & Conquer Suite](./images/01_national_budget_6_sector_suite.png)

> 📌 **核心摘要 (Key Takeaways)**
> - **六大靶向分區審計體系成型 (Divide & Conquer Full Suite)**: 在年均400萬條龐大政府採購數據中過濾85%日常耗材噪音，構建覆蓋腐敗高發領域的**六大高危靶向分區（Sector 1~6）**全生命週期精準查處流水線。
> - **揭露兩大隱秘死角**:
>   1. **Sector 5 (5000萬韓元特例拆分)**: 利用扶持特例上限，在**4800萬至4950萬韓元臨界區間惡意拆分並定向輸送2.45億韓元**（契合審計院先例`BAI-2023-072`）。
>   2. **Sector 6 (12月底突擊花錢傾銷)**: 為防預算收回，於12月下旬僅4天內向特定常客集中突擊下發**1.64億韓元單一來源合同**（契合審計院先例`BAI-2022-094`）。
> - **架構預判並解決2大難點**: 建立區分法定扶持與惡意拆分的**甜點區間分析器(96~99.8%)**，以及辨別突擊花錢的**時間密集度與履約物理可行性反推引擎**。
> - **實戰Bug排錯**: 解決多分區重疊告警衝突、含稅價與不含稅價限額混淆計算、跨年度結轉工期對齊問題。

{/* truncate */}

---

### ⚠️ 法律聲明與匿名化說明 (Legal Notice)

> **【注意】本篇所有案例均已嚴格實施去識別化處理。**  
> 涉事機關（`A公團`、`C公團`）、企業（`D公司`、`F公司`）、當事人及合同編號均已做掩碼隱藏。

---

### 1. 六大高危靶向分區審計總覽

```mermaid
flowchart TD
    Raw[年均400萬條政府採購數據] --> Filter{三維靶向分區管理器}
    Filter -->|85%常規耗材| Drop[低風險歸檔庫]
    Filter --> S1["Sector 1: 公共機構ICT小額拆分"]
    Filter --> S2["Sector 2: 地方節慶投標圍標"]
    Filter --> S3["Sector 3: 委託服務管理費漏損(DEI)"]
    Filter --> S4["Sector 4: 50億+重大工程陪標壟斷"]
    Filter --> S5["🔴 Sector 5: 5000萬特例惡意拆分"]
    Filter --> S6["🔴 Sector 6: 12月底突擊花錢傾銷"]
    S1 & S2 & S3 & S4 & S5 & S6 --> Master[All Sectors Master Runner]
```

---

### 2. 預判挑戰與架構防護

1. **法定政策特例與惡意拆分的辨別**: 僅鎖定合同金額落入上限96%~99.8%區間且30天內由同一發包方頻繁定向簽署的異常合約。
2. **正常年終結算與突擊傾銷的辨識**: 針對12月15日後密集簽約、且距年底結算日剩餘時間無法完成真實交付的項目進行紅牌預警。

---

### 3. 實戰攻克3大突發Bug

1. **多分區間衝突導致重複告警**: 引入優先級排序器，按法紀嚴苛程度歸集為主分區與輔助標籤。
2. **含稅與不含稅價格導致限額誤判**: 增設增值稅剝離歸一化器，自動還原不含稅預算基數。
3. **財政年度與公曆年度跨期誤差**: 建立財政日曆對照解析器，解決項目跨年結轉時間錯位。

---

### 4. 查處戰果與17項全流程驗證

查處A公團定向向D公司拆分輸送1.47億韓元，以及C公團12月下旬4天密集簽發3筆課題（1.25億韓元）案，全套17項測試100%全數通過。
'''
    },
    "es": {
        "title": "Auditoría IA #5: Suite de 6 Sectores y Gasto de Fin de Año",
        "description": "Finalización de la suite de auditoría en 6 sectores: Detección de contratos fraccionados bajo excepciones de 40.000 $ y gasto apresurado de fin de año.",
        "keywords": '["Suite 6 Sectores", "Fraccionamiento de Contratos", "Gasto Fin de Año", "Detección Fraude IA", "Auditoría Compras Públicas"]',
        "content": '''---
slug: national-budget-ai-6-sector-full-suite
title: "Auditoría IA #5: Suite de 6 Sectores y Gasto de Fin de Año"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, procurement-fraud, year-end-dumping, spec-driven-development, devops]
date: 2026-11-22
keywords: ["Suite 6 Sectores", "Fraccionamiento de Contratos", "Gasto Fin de Año", "Detección Fraude IA", "Auditoría Compras Públicas"]
description: "Finalización de la suite de auditoría en 6 sectores: Detección de contratos fraccionados bajo excepciones de 40.000 $ y gasto apresurado de fin de año."
---

![6-Sector Targeted Audit: Divide & Conquer Suite](./images/01_national_budget_6_sector_suite.png)

> 📌 **Puntos Clave (Key Takeaways)**
> - **Suite Integral de 6 Sectores**: Filtrado de 85% de compras rutinarias sobre 4 millones de contratos, expandiendo la auditoría a **6 sectores críticos de fraude**.
> - **2 Grandes Puntos Ciegos Descubiertos**:
>   1. **Sector 5 (Fraccionamiento Preferencial de 40.000 $)**: Evasión mediante contratos concentrados en el 98% del umbral legal ($180.000 detectados).
>   2. **Sector 6 (Vaciado Presupuestario de Fin de Año)**: Rápida adjudicación de 3 contratos en 4 días a finales de diciembre para evitar la devolución de fondos.
> - **Prevención Arquitectural**: Algoritmo de proximidad (96-99.8%) y comprobación de viabilidad física de plazos de entrega.
> - **Corrección de Bugs**: Desduplicación entre sectores por peso de gravedad y normalización de precios netos sin IVA.

{/* truncate */}

---

### ⚠️ Aviso Legal y Anonimización (Legal Notice)

> **[Aviso] Todos los casos han sido rigurosamente anonimizados.**  
> Los nombres de agencias (`Agencia A`), contratistas (`Empresa D`), personas y contratos han sido totalmente enmascarados.

---

### 1. Arquitectura de Auditoría en 6 Sectores

```mermaid
flowchart TD
    Raw[4 Millones de Contratos Públicos] --> Filter{Gestor de Partición 3D}
    Filter -->|85% Consumibles| Drop[Archivo Bajo Riesgo]
    Filter --> S1["Sector 1: TIC <20k $"]
    Filter --> S2["Sector 2: Eventos Municipales"]
    Filter --> S3["Sector 3: Fuga de Subsidios DEI"]
    Filter --> S4["Sector 4: Grandes Licitaciones Monopolio"]
    Filter --> S5["🔴 Sector 5: Abuso de Excepción 40k $"]
    Filter --> S6["🔴 Sector 6: Vaciado Fin de Año"]
    S1 & S2 & S3 & S4 & S5 & S6 --> Master[All Sectors Master Runner]
```

---

### 2. Retos Previstos y Corrección de Fallos

1. **Excepción Política vs. Fraccionamiento**: Análisis de proximidad al umbral legal para evitar falsos positivos en empresas sociales legítimas.
2. **Cierre Rutinario vs. Vaciado Rápido**: Detección de proyectos donde el plazo hasta el 31 de diciembre hace físicamente imposible la entrega de los servicios.
3. **Colisiones Entre Sectores**: Asignación de sector prioritario según la gravedad penal del delito administrativo.
4. **Impuesto IVA**: Deducción inversa de importes con IVA para verificar el umbral legal real sin impuestos.

---

### 3. Validación y Resultados en Campo

Detección de 3 contratos fraccionados de 39.000 $ en la `Agencia A` y adjudicaciones exprés de 100.000 $ en la `Agencia C` en diciembre; 17/17 pruebas superadas.
'''
    },
    "de": {
        "title": "KI-Haushaltsprüfung #5: 6-Sektor-Suite & Jahresend-Dumping",
        "description": "Abschluss der 6-Sektor-Prüfsuite: Aufdeckung von Stückelungsverträgen unter Ausnutzung von 40.000-$-Sonderregeln und Jahresend-Etatsausgaben.",
        "keywords": '["6-Sektor-Prüfsuite", "Stückelungsverträge", "Jahresend-Etatausgaben", "Vergabebetrug KI", "Haushaltsprüfung"]',
        "content": '''---
slug: national-budget-ai-6-sector-full-suite
title: "KI-Haushaltsprüfung #5: 6-Sektor-Suite & Jahresend-Dumping"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, procurement-fraud, year-end-dumping, spec-driven-development, devops]
date: 2026-11-22
keywords: ["6-Sektor-Prüfsuite", "Stückelungsverträge", "Jahresend-Etatausgaben", "Vergabebetrug KI", "Haushaltsprüfung"]
description: "Abschluss der 6-Sektor-Prüfsuite: Aufdeckung von Stückelungsverträgen unter Ausnutzung von 40.000-$-Sonderregeln und Jahresend-Etatsausgaben."
---

![6-Sector Targeted Audit: Divide & Conquer Suite](./images/01_national_budget_6_sector_suite.png)

> 📌 **Kernaussagen (Key Takeaways)**
> - **Vollständige 6-Sektor-Prüfsuite**: Ausfilterung von 85% Routinebeschaffungen bei 4 Millionen Aufträgen, Ausweitung auf **6 Kernrisiko-Sektoren**.
> - **2 Versteckte Schwachstellen Aufgedeckt**:
>   1. **Sektor 5 (Stückelung unter 40.000-$-Ausnahme)**: Gezielte Häufung von Aufträgen bei 98% der Höchstgrenze (180.000 $ aufgedeckt).
>   2. **Sektor 6 (Jahresend-Etatsverbraten)**: 3 freihändige Vergaben in 4 Tagen Ende Dezember zur Vermeidung von Haushaltsrückzahlungen.
> - **Präventive Architektur**: Schwellenwert-Näherungsanalyse (96–99,8%) und Prüfung der zeitlichen Machbarkeit vor dem Jahresabschluss.
> - **Fehlerbehebung**: Prioritätsgewichtung bei Sektorkollisionen und Nettobetragsumrechnung ohne Mehrwertsteuer.

{/* truncate */}

---

### ⚠️ Rechtlicher Hinweis & Anonymisierung (Legal Notice)

> **[Hinweis] Alle Vorgänge wurden zum Schutz der Beteiligten vollständig anonymisiert.**  
> Behörden (`Behörde A`), Firmen (`Firma D`), Personen und Verträge wurden durch Pseudonyme ersetzt.

---

### 1. Architektur der 6-Sektor-Prüfsuite

```mermaid
flowchart TD
    Raw[4 Millionen Vergabeaufträge/Jahr] --> Filter{3D-Sektorpartitions-Manager}
    Filter -->|85% Routineaufwand| Drop[Niedrigrisiko-Archiv]
    Filter --> S1["Sektor 1: ICT-Stückelungen <20T $"]
    Filter --> S2["Sektor 2: Kommunale Event-Kartelle"]
    Filter --> S3["Sektor 3: Fördergeldabfluss DEI"]
    Filter --> S4["Sektor 4: Großausschreibungs-Monopole"]
    Filter --> S5["🔴 Sektor 5: 40T-$-Ausnahmemissbrauch"]
    Filter --> S6["🔴 Sektor 6: Jahresend-Mittelabfluss"]
    S1 & S2 & S3 & S4 & S5 & S6 --> Master[All Sectors Master Runner]
```

---

### 2. Vorhersehbare Herausforderungen & Fehlerbehebung

1. **Ausnahmeregelung vs. Missbrauch**: Proximitätsanalyse an der Grenze von 40.000 $, um reguläre Sozialförderungen nicht fälschlich zu beanstanden.
2. **Normaler Jahresabschluss vs. Notvergaben**: Aussortierung von Projekten, deren vertragliche Leistungen bis zum 31. Dezember physisch nicht erbracht werden können.
3. **Kollisionen bei Mehrfachzuweisung**: Rangfolge nach rechtlicher Schwere zur Vermeidung redundanter Berichte.
4. **Nettobetragsprüfung**: Rückrechnung von Bruttobeträgen zur zutreffenden Prüfung der Freigrenzen.

---

### 3. Validierung und Feldleistung

Erfolgreiche Aufdeckung gestückelter Vergaben bei `Behörde A` und überhasteter Jahresendvergaben bei `Behörde C`; 17/17 Testsuiten vollständig bestanden.
'''
    },
    "fr": {
        "title": "Audit IA #5 : Suite 6 Secteurs et Dépenses de Fin d'Année",
        "description": "Déploiement de la suite d'audit à 6 secteurs : Détection du fractionnement sous dérogation de 40 000 $ et du dumping budgétaire de fin d'année.",
        "keywords": '["Suite Audit 6 Secteurs", "Fractionnement Marchés", "Dépenses Fin d\'Année", "Détection Fraude IA", "Audit Marchés Publics"]',
        "content": '''---
slug: national-budget-ai-6-sector-full-suite
title: "Audit IA #5 : Suite 6 Secteurs et Dépenses de Fin d'Année"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, procurement-fraud, year-end-dumping, spec-driven-development, devops]
date: 2026-11-22
keywords: ["Suite Audit 6 Secteurs", "Fractionnement Marchés", "Dépenses Fin d'Année", "Détection Fraude IA", "Audit Marchés Publics"]
description: "Déploiement de la suite d'audit à 6 secteurs : Détection du fractionnement sous dérogation de 40 000 $ et du dumping budgétaire de fin d'année."
---

![6-Sector Targeted Audit: Divide & Conquer Suite](./images/01_national_budget_6_sector_suite.png)

> 📌 **Points Clés (Key Takeaways)**
> - **Suite d'Audit Intégrale à 6 Secteurs** : Filtrage de 85% des fournitures courantes sur 4 millions de marchés publics, étendant l'audit sur **6 zones à haut risque de fraude**.
> - **2 Angles Morts Critiques Dévoilés** :
>   1. **Secteur 5 (Fractionnement sous Dérogation 40 000 $)** : Contournement via des contrats concentrés à 98% du plafond dérogatoire (180 000 $ découverts).
>   2. **Secteur 6 (Dumping Budgétaire de Fin d'Année)** : 3 marchés passés en 4 jours fin décembre pour éviter le retour des crédits au Trésor.
> - **Anticipation Architecturale** : Détecteur de proximité des plafonds (96-99,8%) et analyse de faisabilité physique des délais d'exécution.
> - **Résolution de Bugs** : Gestion des collisions inter-secteurs par pondération et normalisation hors taxes (HT).

{/* truncate */}

---

### ⚠️ Mention Légale et Anonymisation (Legal Notice)

> **[Avis] Toutes les entités ont été rigoureusement anonymisées.**  
> Les organismes publics (`Agence A`), prestataires (`Société D`), personnes et numéros de marchés sont entièrement masqués.

---

### 1. Architecture Globale d'Audit en 6 Secteurs

```mermaid
flowchart TD
    Raw[4 Millions de Marchés Publics/An] --> Filter{Gestionnaire de Partition 3D}
    Filter -->|85% Fournitures| Drop[Archive Faible Risque]
    Filter --> S1["Secteur 1: TIC <20k $"]
    Filter --> S2["Secteur 2: Événements Municipaux"]
    Filter --> S3["Secteur 3: Fuite Subventions DEI"]
    Filter --> S4["Secteur 4: Grands Marchés Monopoles"]
    Filter --> S5["🔴 Secteur 5: Abus Dérogation 40k $"]
    Filter --> S6["🔴 Secteur 6: Dumping Budgétaire Décembre"]
    S1 & S2 & S3 & S4 & S5 & S6 --> Master[All Sectors Master Runner]
```

---

### 2. Défis Anticipés et Correction des Défaillances

1. **Dérogation Politique vs. Fractionnement** : Analyse de proximité fine du plafond légal pour ne pas pénaliser les entreprises sociales légitimes.
2. **Clôture Normale vs. Précipitation Injustifiée** : Détection des marchés passés après le 15 décembre dont l'exécution complète avant le 31 décembre est matériellement impossible.
3. **Collisions de Classification** : Définition d'un ordre de gravité juridique pour éviter les dossiers multiples.
4. **Calcul Hors Taxe (HT)** : Rétablissement du montant HT réel pour le contrôle des seuils réglementaires.

---

### 3. Validation et Résultats

Révélation de marchés fractionnés de 39 000 $ à l'`Agence A` et d'attributions précipitées de 100 000 $ à l'`Agence C` en décembre ; 17 suites de tests sur 17 validées avec succès.
'''
    },
    "pt-BR": {
        "title": "Auditoria IA #5: Suíte de 6 Setores e Gastos de Fim de Ano",
        "description": "Finalização da suíte de auditoria em 6 setores: Detecção de contratos fracionados sob isenção de US$ 40 mil e despejo orçamentário de fim de ano.",
        "keywords": '["Suíte de Auditoria 6 Setores", "Fracionamento de Contratos", "Gastos de Fim de Ano", "Detecção de Fraude IA", "Auditoria de Compras Públicas"]',
        "content": '''---
slug: national-budget-ai-6-sector-full-suite
title: "Auditoria IA #5: Suíte de 6 Setores e Gastos de Fim de Ano"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, procurement-fraud, year-end-dumping, spec-driven-development, devops]
date: 2026-11-22
keywords: ["Suíte de Auditoria 6 Setores", "Fracionamento de Contratos", "Gastos de Fim de Ano", "Detecção de Fraude IA", "Auditoria de Compras Públicas"]
description: "Finalização da suíte de auditoria em 6 setores: Detecção de contratos fracionados sob isenção de US$ 40 mil e despejo orçamentário de fim de ano."
---

![6-Sector Targeted Audit: Divide & Conquer Suite](./images/01_national_budget_6_sector_suite.png)

> 📌 **Principais Conclusões (Key Takeaways)**
> - **Suíte Completa em 6 Setores**: Filtragem de 85% de suprimentos rotineiros em 4 milhões de contratos, expandindo a vigilância para **6 setores críticos de fraude**.
> - **2 Pontos Cegos Revelados**:
>   1. **Setor 5 (Fracionamento sob Isenção de US$ 40 mil)**: Manobra concentrando contratos no limite de 98% do teto legal (US$ 180 mil identificados).
>   2. **Setor 6 (Despejo Orçamentário de Fim de Ano)**: 3 contratos concedidos em 4 dias no final de dezembro para evitar devolução de recursos.
> - **Prevenção Arquitetural**: Análise de proximidade ao teto (96-99,8%) e checagem de viabilidade física de entrega antes da virada do ano.
> - **Correção de Bugs**: Desduplicação inter-setorial por gravidade e normalização de preços sem impostos.

{/* truncate */}

---

### ⚠️ Aviso Legal e Anonimização (Legal Notice)

> **[Aviso] Todos os dados foram estritamente anonimizados.**  
> Órgãos públicos (`Órgão A`), contratadas (`Empresa D`), indivíduos e contratos foram totalmente mascarados.

---

### 1. Arquitetura da Suíte de Auditoria em 6 Setores

```mermaid
flowchart TD
    Raw[4 Milhões de Contratos Públicos/Ano] --> Filter{Gerenciador de Partição 3D}
    Filter -->|85% Suprimentos| Drop[Arquivo de Baixo Risco]
    Filter --> S1["Setor 1: TIC < US$ 20k"]
    Filter --> S2["Setor 2: Eventos Municipais"]
    Filter --> S3["Setor 3: Vazamento Subvenções DEI"]
    Filter --> S4["Setor 4: Grandes Licitações Monopólio"]
    Filter --> S5["🔴 Setor 5: Abuso de Isenção US$ 40k"]
    Filter --> S6["🔴 Setor 6: Despejo de Fim de Ano"]
    S1 & S2 & S3 & S4 & S5 & S6 --> Master[All Sectors Master Runner]
```

---

### 2. Desafios Previstos e Correção de Falhas

1. **Isenção Legítima vs. Fracionamento Malicioso**: Cálculo de proximidade fina para não prejudicar empresas sociais idôneas.
2. **Fechamento Normal vs. Gastos Apressados**: Sinalização de projetos assinados após 15 de dezembro cuja entrega até 31 de dezembro é fisicamente impossível.
3. **Colisões de Setores**: Priorização por gravidade jurídica para evitar multiplicidade de relatórios.
4. **Cálculo Sem Impostos**: Dedução reversa de valores brutos para verificação precisa dos limites legais.

---

### 3. Validação em Campo e Resultados

Descoberta de contratos fracionados de US$ 39 mil no `Órgão A` e repasses emergenciais de US$ 100 mil no `Órgão C` em dezembro; 17 baterias de testes aprovadas com sucesso.
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
