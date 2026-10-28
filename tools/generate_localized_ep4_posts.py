# -*- coding: utf-8 -*-
import os

BASE_DIR = r"D:\ai\antigravity\global_blog\배포대기\2026-11-21-national-budget-ai-corporate-registry-cartel-detection\i18n"

POSTS = {
    "ja": {
        "title": "国家予算AI #4：DART企業支配構造の連携と名義貸しカルテル打破",
        "description": "調達データでは見抜けない名義貸し代表者（ペーパーカンパニー）を摘発するため、DART開示情報と法人登記簿を連携して実質的支配者を追跡した開発記録。",
        "keywords": '["名義貸しカルテル摘発", "DART企業支配構造連携", "法人登記簿AI分析", "実質的支配者追跡", "GraphRAGカルテル"]',
        "content": '''---
slug: national-budget-ai-corporate-registry-cartel-detection
title: "国家予算AI #4：DART企業支配構造の連携と名義貸しカルテル打破"
authors: [jbgih]
tags: [ai-agents, corporate-registry, dart-api, graphrag, cartel-detection, devops]
date: 2026-11-21
keywords: ["名義貸しカルテル摘発", "DART企業支配構造連携", "法人登記簿AI分析", "実質的支配者追跡", "GraphRAGカルテル"]
description: "調達データでは見抜けない名義貸し代表者（ペーパーカンパニー）を摘発するため、DART開示情報と法人登記簿を連携して実質的支配者を追跡した開発記録。"
---

![Breaking Cartels: Corporate Registry & DART Integration](./images/01_national_budget_corporate_registry.png)

> 📌 **要点まとめ (Key Takeaways)**
> - **第2弾の限界を技術で突破**: 「名義貸し代表者（ペーパーカンパニー）は調達データ単体では追跡不能」という課題を解決するため、**法人登記簿およびDART開示データをリアルタイム交差検証する[`CorporateRegistryClient`](file:///D:/ai/antigravity/national_budget_ai/src/pipeline/corporate_registry_client.py)**を新規構築。
> - **事前設計による2大課題の予防**:
>   1. 事業者番号・法人登録番号・DARTコードのID分断を**3点インデックスブリッジ**で解決。
>   2. 役員・株主データの無制限挿入によるグラフ爆発を防ぐ**支配力有意性しきい値(役員兼任+持分50%以上)**を設定。
> - **実戦で直面した3大バグの解決**:
>   1. 相互出資網巡回時の**循環参照(Cycle)無限再帰エラー** ➔ NetworkX強連結成分(SCC)縮約で解決。
>   2. 入札直前の急造ペーパー会社見落とし ➔ **設立180日未満判定モジュール**を配備。
>   3. 夫婦持分51:49による女性企業優遇偽装 ➔ 特殊関係者複合ルールエンジンで実質支配者を立証。
> - **実戦成果**: 実質支配者K氏が80%持分と役員兼任で2社を操っていた1.7億ウォン規模の偽装入札カルテルを完全摘発し、全17テストスイートPASSを達成。

{/* truncate */}

---

### ⚠️ 法的告知および匿名化案内 (Legal Notice & Anonymization)

> **【注意】本稿の全事例は紛争防止のため厳格に匿名化されています。**  
> 機関名（`A公団`、`B省`）、企業名（`B社`、`C社`）、人物名（`K氏`、`P氏`）、契約番号はすべて仮名化およびマスキング処理されています。

---

### 1. DART企業支配構造連携アーキテクチャ

公共調達グラフに**人物ノード、役員兼任エッジ、株主持分エッジ**を直接統合しました：

```mermaid
flowchart TD
    subgraph ProcurementData ["公共調達データ"]
        A[KONEPS調達契約] --> B[企業ノード]
    end

    subgraph CorporateRegistry ["法人登記 & DART開示連携"]
        C[登記所法人登記簿] --> D[CorporateRegistryClient]
        E[金融監督院DART] --> D
        D --> F[役員名簿<br/>代表/社内取締役]
        D --> G[株主名簿<br/>持分率/特殊関係者]
    end

    subgraph GovernanceGraph ["GraphRAG支配構造分析"]
        B --> H[企業-人物サブグラフ]
        F -->|DIRECTOR_OF| H
        G -->|OWNS_SHARE_OF| H
        H --> I{支配構造推論}
        I -->|同一人物80%持分&役員兼任| J[🔴 実質支配1人カルテル判定]
    end
```

---

### 2. 事前想定された課題と予防設計

1. **識別子の分断 ➔ 3点インデックスブリッジ**: 事業者番号・法人番号・DART固有コードをO(1)で相互変換するハッシュテーブルを構築。
2. **グラフ爆発の防止 ➔ 有意性しきい値**: 法的決定権を持つ取締役および50%以上の支配株主のみをグラフに投入。

---

### 3. 実装中に解決した3大バグ

1. **循環出資による無限再帰**: A社とB社が相互出資するループに対し、強連結成分(SCC)縮約アルゴリズムを導入してプロセス停止を解消。
2. **設立180日未満の急造会社見落とし**: 契約日と設立日の差分を計算し、6ヶ月未満のペーパーカンパニーにリスク加算点96点を自動付与。
3. **夫婦持分51:49偽装**: 女性代表51%、夫49%(社内取締役)のケースを特殊関係者合算ルールで捕捉。

---

### 4. 摘発成果と17件全テスト合格

表向き競合として入札に参加した2社が、実は同一人物K氏によって80%所有され役員を兼任されていた事実を摘発。17件の統合テストに全数合格しました。
'''
    },
    "zh-Hans": {
        "title": "国家预算AI #4：打通DART企业股权穿透与影子白手套围标查处",
        "description": "为攻克政府采购仅凭公开台账无法穿透借名代持白手套的盲区，融合DART公司治理与工商登记底册查处一人实际控制围标团伙的技术实战。",
        "keywords": '["白手套围标查处", "DART企业治理联动", "工商登记AI分析", "实控人股权穿透", "GraphRAG围标检测"]',
        "content": '''---
slug: national-budget-ai-corporate-registry-cartel-detection
title: "国家预算AI #4：打通DART企业股权穿透与影子白手套围标查处"
authors: [jbgih]
tags: [ai-agents, corporate-registry, dart-api, graphrag, cartel-detection, devops]
date: 2026-11-21
keywords: ["白手套围标查处", "DART企业治理联动", "工商登记AI分析", "实控人股权穿透", "GraphRAG围标检测"]
description: "为攻克政府采购仅凭公开台账无法穿透借名代持白手套的盲区，融合DART公司治理与工商登记底册查处一人实际控制围标团伙的技术实战。"
---

![Breaking Cartels: Corporate Registry & DART Integration](./images/01_national_budget_corporate_registry.png)

> 📌 **核心摘要 (Key Takeaways)**
> - **技术攻克第2篇行业盲区**: 针对“仅凭采购台账无法查出借名代持傀儡法人（白手套）”的痛点，全新构建了融合工商登记与DART监管披露的**股权穿透分析引擎([`CorporateRegistryClient`](file:///D:/ai/antigravity/national_budget_ai/src/pipeline/corporate_registry_client.py))**。
> - **架构预判并解决2大难点**:
>   1. 建立**三角哈希索引桥**，化解税号、企业登记号与DART代码间的格式割裂。
>   2. 设定**控制力显著性阈值（高管任职 + 50%以上持股）**，杜绝海量无意义人际关系引发图爆炸。
> - **实战解决3大线上突发Bug**:
>   1. 交叉持股引发的**递归循环死锁崩溃** ➔ 采用NetworkX强连通分量(SCC)环路缩减算法消除。
>   2. 招投标前夕突击注册空壳公司漏检 ➔ 增加**合同日溯源180天新设预警**。
>   3. 夫妻代持51:49规避监管套利 ➔ 引入直系亲属一致行动人复合判定引擎。
> - **实战战果**: 成功揭露幕后人K某持股80%兼任高管、同时操纵两家虚假竞标企业的1.7亿韩元围标大案，17项全流程测试100%全数通过。

{/* truncate */}

---

### ⚠️ 法律声明与匿名化说明 (Legal Notice & Anonymization)

> **【注意】本篇所有案例均已严格实施去标识化处理。**  
> 涉事机关（`A公团`）、中标商（`B公司`、`C公司`）、当事人（`K某`、`P某`）及合同编号均已做掩码隐藏。

---

### 1. DART公司治理与股权穿透架构

我们将财政采购图谱升级为涵盖**自然人节点、高管兼职边与股东持股边**的多维关系图谱：

```mermaid
flowchart TD
    subgraph ProcurementData ["政府采购基础数据"]
        A[KONEPS招标合同] --> B[中标企业节点]
    end

    subgraph CorporateRegistry ["工商登记与DART披露联动"]
        C[司法工商登记底册] --> D[CorporateRegistryClient]
        E[金融监管DART披露] --> D
        D --> F[高管名册<br/>法人/执行董事]
        D --> G[股东名册<br/>持股比例/一致行动人]
    end

    subgraph GovernanceGraph ["GraphRAG股权穿透图谱"]
        B --> H[企业-自然人子图]
        F -->|DIRECTOR_OF| H
        G -->|OWNS_SHARE_OF| H
        H --> I{治理结构推理}
        I -->|同一人持股80%兼任高管| J[🔴 一人实际控制影子围标判定]
    end
```

---

### 2. 预判挑战与架构防护

1. **多重企业标识符割裂 ➔ 三角索引桥**: 针对税务号、工商号与DART码，建立O(1)常数级双向映射哈希表。
2. **图节点爆炸风险 ➔ 治理显著性阈值**: 严格限定仅抽取执行董事及持股50%以上控股股东。

---

### 3. 实战攻克3大产线突发故障

1. **循环持股引发死循环**: 引入强连通分量(SCC)检测，遇交叉持股环路自动缩聚为单一实体集群。
2. **入伙3周空壳公司漏报**: 增设`check_newly_established`，对成立不足半年的竞标商直接标红(96分)。
3. **51:49夫妻股权粉饰**: 结合亲属关系图谱，识别“名义女代表51%、丈夫持股49%兼董事”的伪装套利。

---

### 4. 查处战果与17项全测试验证

成功查明B公司与C公司表面对手实为K某一人掌控的虚假竞标网络。17项集成测试套件全数通过验证。
'''
    },
    "zh-Hant": {
        "title": "國家預算AI #4：打通DART企業股權穿透與影子人頭圍標查處",
        "description": "為攻克政府採購僅憑公開台賬無法穿透借名代持人頭的盲區，融合DART公司治理與工商登記底冊查處一人實際控制圍標團夥的技術實戰。",
        "keywords": '["人頭圍標查處", "DART企業治理聯動", "工商登記AI分析", "實控人股權穿透", "GraphRAG圍標檢測"]',
        "content": '''---
slug: national-budget-ai-corporate-registry-cartel-detection
title: "國家預算AI #4：打通DART企業股權穿透與影子人頭圍標查處"
authors: [jbgih]
tags: [ai-agents, corporate-registry, dart-api, graphrag, cartel-detection, devops]
date: 2026-11-21
keywords: ["人頭圍標查處", "DART企業治理聯動", "工商登記AI分析", "實控人股權穿透", "GraphRAG圍標檢測"]
description: "為攻克政府採購僅憑公開台賬無法穿透借名代持人頭的盲區，融合DART公司治理與工商登記底冊查處一人實際控制圍標團夥的技術實戰。"
---

![Breaking Cartels: Corporate Registry & DART Integration](./images/01_national_budget_corporate_registry.png)

> 📌 **核心摘要 (Key Takeaways)**
> - **技術攻克第2篇行業盲區**: 針對「僅憑採購台賬無法查出借名代持傀儡法人（人頭公司）」的痛點，全新構建了融合工商登記與DART監管披露的**股權穿透分析引擎([`CorporateRegistryClient`](file:///D:/ai/antigravity/national_budget_ai/src/pipeline/corporate_registry_client.py))**。
> - **架構預判並解決2大難點**:
>   1. 建立**三角雜湊索引橋**，化解稅號、企業登記號與DART代碼間的格式割裂。
>   2. 設定**控制力顯著性閾值（高管任職 + 50%以上持股）**，杜絕海量無意義人際關係引發圖爆炸。
> - **實戰解決3大線上突發Bug**:
>   1. 交叉持股引發的**遞迴循環死鎖崩潰** ➔ 採用NetworkX強連通分量(SCC)環路縮減演算法消除。
>   2. 招投標前夕突擊註冊空殼公司漏檢 ➔ 增加**合同日溯源180天新設預警**。
>   3. 夫妻代持51:49規避監管套利 ➔ 引入直系親屬一致行動人複合判定引擎。
> - **實戰戰果**: 成功揭露幕後人K某持股80%兼任高管、同時操縱兩家虛假競標企業的1.7億韓元圍標大案，17項全流程測試100%全數通過。

{/* truncate */}

---

### ⚠️ 法律聲明與匿名化說明 (Legal Notice & Anonymization)

> **【注意】本篇所有案例均已嚴格實施去識別化處理。**  
> 涉事機關（`A公團`）、中標商（`B公司`、`C公司`）、當事人（`K某`、`P某`）及合同編號均已做掩碼隱藏。

---

### 1. DART公司治理與股權穿透架構

我們將財政採購圖譜升級為涵蓋**自然人節點、高管兼職邊與股東持股邊**的多維關係圖譜：

```mermaid
flowchart TD
    subgraph ProcurementData ["政府採購基礎數據"]
        A[KONEPS招標合同] --> B[中標企業節點]
    end

    subgraph CorporateRegistry ["工商登記與DART披露聯動"]
        C[司法工商登記底冊] --> D[CorporateRegistryClient]
        E[金融監管DART披露] --> D
        D --> F[高管名冊<br/>法人/執行董事]
        D --> G[股東名冊<br/>持股比例/一致行動人]
    end

    subgraph GovernanceGraph ["GraphRAG股權穿透圖譜"]
        B --> H[企業-自然人子圖]
        F -->|DIRECTOR_OF| H
        G -->|OWNS_SHARE_OF| H
        H --> I{治理結構推理}
        I -->|同一人持股80%兼任高管| J[🔴 一人實際控制影子圍標判定]
    end
```

---

### 2. 預判挑戰與架構防護

1. **多重企業識別碼割裂 ➔ 三角索引橋**: 針對稅務號、工商號與DART碼，建立O(1)常數級雙向映射雜湊表。
2. **圖節點爆炸風險 ➔ 治理顯著性閾值**: 嚴格限定僅抽取執行董事及持股50%以上控股股東。

---

### 3. 實戰攻克3大產線突發故障

1. **循環持股引發死循環**: 引入強連通分量(SCC)檢測，遇交叉持股環路自動縮聚為單一實體集群。
2. **入夥3週空殼公司漏報**: 增設`check_newly_established`，對成立不足半年的競標商直接標紅(96分)。
3. **51:49夫妻股權粉飾**: 結合親屬關係圖譜，識別「名義女代表51%、丈夫持股49%兼董事」的偽裝套利。

---

### 4. 查處戰果與17項全測試驗證

成功查明B公司與C公司表面對手實為K某一人掌控的虛假競標網絡。17項整合測試套件全數通過驗證。
'''
    },
    "es": {
        "title": "Auditoría IA #4: Cárteles con DART y Beneficiario Final",
        "description": "Integración del registro corporativo DART en GraphRAG para desenmascarar testaferros y cárteles controlados por una sola persona en compras públicas.",
        "keywords": '["Cárteles de Testaferros", "Registro Corporativo DART", "Beneficiario Real", "GraphRAG Corporativo", "Fraude en Licitaciones"]',
        "content": '''---
slug: national-budget-ai-corporate-registry-cartel-detection
title: "Auditoría IA #4: Cárteles con DART y Beneficiario Final"
authors: [jbgih]
tags: [ai-agents, corporate-registry, dart-api, graphrag, cartel-detection, devops]
date: 2026-11-21
keywords: ["Cárteles de Testaferros", "Registro Corporativo DART", "Beneficiario Real", "GraphRAG Corporativo", "Fraude en Licitaciones"]
description: "Integración del registro corporativo DART en GraphRAG para desenmascarar testaferros y cárteles controlados por una sola persona en compras públicas."
---

![Breaking Cartels: Corporate Registry & DART Integration](./images/01_national_budget_corporate_registry.png)

> 📌 **Puntos Clave (Key Takeaways)**
> - **Superación de Límites Previos**: Superando la limitación de la Parte 2 sobre testaferros, creamos el cliente [`CorporateRegistryClient`](file:///D:/ai/antigravity/national_budget_ai/src/pipeline/corporate_registry_client.py) que cruza el registro mercantil y la base de datos bursátil DART.
> - **Prevención Arquitectural**:
>   1. Puente tripartito para unificar NIF de empresa, registro judicial y código DART.
>   2. Umbral de relevancia en el grafo de conocimiento (directores ejecutivos + >50% de acciones).
> - **3 Errores de Producción Resueltos**:
>   1. Bucle infinito por participaciones cruzadas resuelto mediante componentes fuertemente conexos (SCC).
>   2. Detección de empresas fantasma creadas menos de 180 días antes de la licitación.
>   3. Esquema 51:49 entre cónyuges desenmascarado mediante reglas de vínculos familiares.
> - **Resultado**: Desenmascarado un cártel de 130.000 $ controlado al 80% por una sola persona; 17/17 pruebas superadas.

{/* truncate */}

---

### ⚠️ Aviso Legal y Anonimización (Legal Notice)

> **[Aviso] Todos los casos han sido rigurosamente anonimizados.**  
> Los nombres de agencias (`Agencia A`), empresas (`Empresa B`, `Empresa C`), personas (`Sr. K`) y números de contrato han sido completamente enmascarados.

---

### 1. Arquitectura de Gobernanza Corporativa y DART

```mermaid
flowchart TD
    subgraph ProcurementData ["Datos de Compras Públicas"]
        A[Contratos KONEPS] --> B[Nodo de Empresa]
    end

    subgraph CorporateRegistry ["Registros Mercantiles & DART"]
        C[Registro Mercantil] --> D[CorporateRegistryClient]
        E[Divulgaciones DART] --> D
        D --> F[Directorio de Ejecutivos]
        D --> G[Libro de Accionistas]
    end

    subgraph GovernanceGraph ["Grafo Extendido GraphRAG"]
        B --> H[Subgrafo Empresa-Persona]
        F -->|DIRECTOR_OF| H
        G -->|OWNS_SHARE_OF| H
        H --> I{Inferencia de Control}
        I -->|1 Individuo con 80% y Director| J[🔴 Cártel de Control Unipersonal]
    end
```

---

### 2. Retos Previstos y Corrección de Fallos

1. **Fragmentación de Claves**: Creación de tabla hash que reconcilia los identificadores fiscales y mercantiles en $O(1)$.
2. **Bucle por Participación Cruzada**: Bloqueado mediante condensación de ciclos con algoritmos de NetworkX.
3. **Empresas Recientes (<180 días)**: Detección automática de adjudicatarios recién constituidos.
4. **Artimaña Conyugal 51:49**: Extensión de GraphRAG con aristas familiares para desenmascarar el control efectivo.

---

### 3. Verificación con 17 Suites de Pruebas

Se confirmó la detección del cártel donde el `Sr. K` simulaba competencia entre dos empresas propias, con 17 de 17 pruebas superadas con éxito.
'''
    },
    "de": {
        "title": "KI-Haushaltsprüfung #4: DART-Unternehmensanalyse & Strohmänner",
        "description": "Aufdeckung von Strohmann-Kartellen durch Integration von DART-Unternehmensdaten und Handelsregistern zur Ermittlung wirtschaftlich Berechtigter.",
        "keywords": '["Strohmann-Kartelle", "DART-Unternehmensregister", "Wirtschaftlich Berechtigter", "GraphRAG-Governance", "Ausschreibungsabsprachen"]',
        "content": '''---
slug: national-budget-ai-corporate-registry-cartel-detection
title: "KI-Haushaltsprüfung #4: DART-Unternehmensanalyse & Strohmänner"
authors: [jbgih]
tags: [ai-agents, corporate-registry, dart-api, graphrag, cartel-detection, devops]
date: 2026-11-21
keywords: ["Strohmann-Kartelle", "DART-Unternehmensregister", "Wirtschaftlich Berechtigter", "GraphRAG-Governance", "Ausschreibungsabsprachen"]
description: "Aufdeckung von Strohmann-Kartellen durch Integration von DART-Unternehmensdaten und Handelsregistern zur Ermittlung wirtschaftlich Berechtigter."
---

![Breaking Cartels: Corporate Registry & DART Integration](./images/01_national_budget_corporate_registry.png)

> 📌 **Kernaussagen (Key Takeaways)**
> - **Überwindung früherer Grenzen**: Als Lösung für die in Teil 2 erwähnten Strohmann-Konstrukte wurde der [`CorporateRegistryClient`](file:///D:/ai/antigravity/national_budget_ai/src/pipeline/corporate_registry_client.py) geschaffen, der DART-Daten und Handelsregister abgleicht.
> - **Präventive Architektur**:
>   1. Dreiseitige Hash-Brücke zur Auflösung heterogener Unternehmens-IDs.
>   2. Relevanz-Schwellenwerte im Wissensgraphen (Vorstände + Anteile >50%).
> - **Behebung von 3 Produktionsfehlern**:
>   1. `RecursionError` bei Kreuzbeteiligungen durch Kondensation starker Zusammenhangskomponenten (SCC) behoben.
>   2. Erkennung von Scheinfirmen, die weniger als 180 Tage vor Vergabe gegründet wurden.
>   3. 51:49-Ehegatten-Aufteilung zur Vorteilserschleichung über Verwandtschaftskanten aufgedeckt.
> - **Ergebnis**: 130.000-Dollar-Kartell aufgedeckt, das zu 80% von einer einzigen Person kontrolliert wurde; 17/17 Tests bestanden.

{/* truncate */}

---

### ⚠️ Rechtlicher Hinweis & Anonymisierung (Legal Notice)

> **[Hinweis] Alle Vorgänge wurden zum Schutz der Beteiligten vollständig anonymisiert.**  
> Behörden (`Behörde A`), Firmen (`Firma B`, `Firma C`), Personen (`Herr K`) und Vertragsnummern wurden durch Pseudonyme ersetzt.

---

### 1. DART-Unternehmensanalyse-Architektur

```mermaid
flowchart TD
    subgraph ProcurementData ["Vergabedaten"]
        A[KONEPS-Verträge] --> B[Unternehmensknoten]
    end

    subgraph CorporateRegistry ["Handelsregister & DART"]
        C[Gerichtsregister] --> D[CorporateRegistryClient]
        E[DART-Meldungen] --> D
        D --> F[Vorstandsliste]
        D --> G[Aktionärsbuch]
    end

    subgraph GovernanceGraph ["GraphRAG-Governance"]
        B --> H[Firma-Person-Subgraph]
        F -->|DIRECTOR_OF| H
        G -->|OWNS_SHARE_OF| H
        H --> I{Eigentumsanalyse}
        I -->|1 Person mit 80% und Vorstand| J[🔴 Scheinkonkurrenz-Kartell]
    end
```

---

### 2. Vorhersehbare Herausforderungen & Fehlerbehebung

1. **ID-Fragmentierung**: O(1)-Hash-Tabelle überbrückt Steuernummern und Handelsregisternummern.
2. **Kreuzbeteiligungs-Schleifen**: Endlosschleifen über NetworkX-SCC-Zyklenkondensation eliminiert.
3. **180-Tage-Scheinfirmen**: Automatische Risikoaufschläge für Blitzgründungen vor Angebotsabgabe.
4. **Ehepartner-Tricks (51:49)**: Kombinierte Auswertung von Familienbanden und Organfunktionen.

---

### 3. Verifizierung mit 17 Test-Suiten

Erfolgreicher Nachweis, dass zwei scheinbare Bieterkonkurrenten von `Herrn K` beherrscht wurden; 17 von 17 Testsuiten vollständig bestanden.
'''
    },
    "fr": {
        "title": "Audit Budgétaire IA #4 : Registre DART et Prête-Noms",
        "description": "Intégration du registre des entreprises DART pour démasquer les prête-noms et les ententes contrôlées par une seule personne dans les marchés publics.",
        "keywords": '["Ententes Prête-Noms", "Registre DART Entreprises", "Bénéficiaire Effectif", "GraphRAG Gouvernance", "Fraude aux Enchères"]',
        "content": '''---
slug: national-budget-ai-corporate-registry-cartel-detection
title: "Audit Budgétaire IA #4 : Registre DART et Prête-Noms"
authors: [jbgih]
tags: [ai-agents, corporate-registry, dart-api, graphrag, cartel-detection, devops]
date: 2026-11-21
keywords: ["Ententes Prête-Noms", "Registre DART Entreprises", "Bénéficiaire Effectif", "GraphRAG Gouvernance", "Fraude aux Enchères"]
description: "Intégration du registre des entreprises DART pour démasquer les prête-noms et les ententes contrôlées par une seule personne dans les marchés publics."
---

![Breaking Cartels: Corporate Registry & DART Integration](./images/01_national_budget_corporate_registry.png)

> 📌 **Points Clés (Key Takeaways)**
> - **Dépassement de la Limite de l'Épisode 2** : Pour identifier les prête-noms introuvables via les seuls registres de commande publique, création du client [`CorporateRegistryClient`](file:///D:/ai/antigravity/national_budget_ai/src/pipeline/corporate_registry_client.py) reliant le greffe du tribunal et la base DART.
> - **Anticipation Architecturale** :
>   1. Table de hachage tripartite unifiant numéros fiscaux, d'immatriculation et codes DART.
>   2. Seuils de significativité dans le graphe (dirigeants effectifs + détentions >50%).
> - **3 Bugs de Production Résolus** :
>   1. Récursion infinie due aux participations croisées résolue par condensation des composantes fortement connexes (SCC).
>   2. Détection des sociétés coquilles créées moins de 180 jours avant la soumission.
>   3. Déguisement 51:49 entre conjoints démasqué via des arêtes de liens familiaux.
> - **Résultat** : Démantèlement d'une entente de 130 000 $ contrôlée à 80% par un individu unique ; 17/17 tests validés.

{/* truncate */}

---

### ⚠️ Mention Légale et Anonymisation (Legal Notice)

> **[Avis] Toutes les entités ont été rigoureusement anonymisées.**  
> Les organismes publics (`Agence A`), entreprises (`Société B`, `Société C`), personnes physiques (`M. K`) et numéros de contrat ont été entièrement masqués.

---

### 1. Architecture de Gouvernance d'Entreprise et DART

```mermaid
flowchart TD
    subgraph ProcurementData ["Données des Marchés Publics"]
        A[Contrats KONEPS] --> B[Noeud Entreprise]
    end

    subgraph CorporateRegistry ["Registres Judiciaires & DART"]
        C[Registre du Commerce] --> D[CorporateRegistryClient]
        E[Divulgations DART] --> D
        D --> F[Liste des Dirigeants]
        D --> G[Registre des Actionnaires]
    end

    subgraph GovernanceGraph ["Gouvernance GraphRAG"]
        B --> H[Sous-graphe Entreprise-Personne]
        F -->|DIRECTOR_OF| H
        G -->|OWNS_SHARE_OF| H
        H --> I{Analyse de Contrôle}
        I -->|1 Personne à 80% et Dirigeant| J[🔴 Entente Contrôlée par 1 Seul Homme]
    end
```

---

### 2. Défis Anticipés et Correction des Défaillances

1. **Fragmentation des Identifiants** : Table de correspondance $O(1)$ unifiant les identifiants fiscaux et judiciaires.
2. **Boucles de Participations Croisées** : Élimination des récursions infinies par l'algorithme SCC de NetworkX.
3. **Sociétés Récentes (<180 jours)** : Alerte automatique sur les entreprises créées juste avant l'appel d'offres.
4. **Combinaison Conjugale 51:49** : Analyse conjointe des liens familiaux et des mandats d'administrateurs.

---

### 3. Validation sur 17 Suites de Tests

Preuve établie que deux soumissionnaires rivaux étaient en réalité détenus à 80% par `M. K` ; 17 suites de tests sur 17 franchies avec succès.
'''
    },
    "pt-BR": {
        "title": "Auditoria IA #4: Registro DART e Quebra de Laranjas",
        "description": "Integração do registro societário DART no GraphRAG para desmascarar laranjas e cartéis controlados por uma única pessoa em compras governamentais.",
        "keywords": '["Cartel de Laranjas", "Registro Societário DART", "Beneficiário Efetivo", "GraphRAG Governança", "Fraude em Licitações"]',
        "content": '''---
slug: national-budget-ai-corporate-registry-cartel-detection
title: "Auditoria IA #4: Registro DART e Quebra de Laranjas"
authors: [jbgih]
tags: [ai-agents, corporate-registry, dart-api, graphrag, cartel-detection, devops]
date: 2026-11-21
keywords: ["Cartel de Laranjas", "Registro Societário DART", "Beneficiário Efetivo", "GraphRAG Governança", "Fraude em Licitações"]
description: "Integração do registro societário DART no GraphRAG para desmascarar laranjas e cartéis controlados por uma única pessoa em compras governamentais."
---

![Breaking Cartels: Corporate Registry & DART Integration](./images/01_national_budget_corporate_registry.png)

> 📌 **Principais Conclusões (Key Takeaways)**
> - **Superação da Limitação Anterior**: Para desmantelar laranjas invisíveis nos portais de licitação, criamos o cliente [`CorporateRegistryClient`](file:///D:/ai/antigravity/national_budget_ai/src/pipeline/corporate_registry_client.py) que cruza registros civis e demonstrações DART.
> - **Prevenção Arquitetural**:
>   1. Tabela hash tripla para resolver disparidades entre CNPJ, registro civil e códigos DART.
>   2. Filtros de significância no grafo de conhecimento (diretores estatutários + cotas >50%).
> - **3 Falhas Críticas Corrigidas**:
>   1. `RecursionError` por participações cruzadas resolvido via condensação de ciclos com componentes fortemente conexos (SCC).
>   2. Identificação de empresas de fachada abertas menos de 180 dias antes do contrato.
>   3. Manobra de cotas 51:49 entre cônjuges desarticulada por regras de laços de parentesco.
> - **Resultado**: Revelado conluio de US$ 130 mil controlado em 80% por uma única pessoa; 17/17 baterias de testes aprovadas.

{/* truncate */}

---

### ⚠️ Aviso Legal e Anonimização (Legal Notice)

> **[Aviso] Todos os dados foram estritamente anonimizados.**  
> Órgãos públicos (`Órgão A`), empresas (`Empresa B`, `Empresa C`), indivíduos (`Sr. K`) e contratos foram totalmente mascarados.

---

### 1. Arquitetura de Governança Societária e DART

```mermaid
flowchart TD
    subgraph ProcurementData ["Dados de Compras Públicas"]
        A[Contratos KONEPS] --> B[Nó Empresa]
    end

    subgraph CorporateRegistry ["Junta Comercial & DART"]
        C[Registro Civil de Empresas] --> D[CorporateRegistryClient]
        E[Demonstrações DART] --> D
        D --> F[Quadro de Diretores]
        D --> G[Livro de Sócios]
    end

    subgraph GovernanceGraph ["Governança GraphRAG"]
        B --> H[Subgrafo Empresa-Pessoa]
        F -->|DIRECTOR_OF| H
        G -->|OWNS_SHARE_OF| H
        H --> I{Inferência de Controle}
        I -->|1 Pessoa com 80% e Diretor| J[🔴 Cartel de Controle Unipessoal]
    end
```

---

### 2. Desafios Previstos e Correção de Falhas

1. **Fragmentação de Identificadores**: Mapeamento bidirecional $O(1)$ unificando registros fiscais e judiciais.
2. **Loops em Participações Cruzadas**: Eliminação de recursão infinita via algoritmo SCC do NetworkX.
3. **Empresas Recentes (<180 dias)**: Cálculo de delta temporal sinalizando empresas criadas às vésperas de editais.
4. **Artifício Conjugal 51:49**: Regras compostas rastreando cônjuges com assento de diretoria.

---

### 3. Validação em 17 Baterias de Testes

Comprovação de que duas empresas concorrentes pertenciam 80% ao `Sr. K`; 17/17 baterias de testes aprovadas com sucesso.
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
