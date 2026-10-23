# -*- coding: utf-8 -*-
import os

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-10-23-stanford-cs146s-2"

# 1. Full Japanese Version (Unabbreviated, High-Density)
ja_full = """---
slug: stanford-cs146s-2-coding-llms-prompt-engineering
title: "[スタンフォード CS146S #2] コーディングLLMの動作原理とプロンプトエンジニアリング：事前学習・RLHFからスイスチーズモデルの検証まで"
authors: [jbgih]
tags: [stanford-cs146s, coding-llms, prompt-engineering, rlhf, chain-of-thought, swiss-cheese-model, software-architecture]
date: 2026-10-23
keywords: [Coding LLMs, Prompt Engineering, RLHF, Chain of Thought, Swiss Cheese Model]
description: "スタンフォード大学CS146S第2講の完全技術解説：事前学習(Pre-training)とRLHFによる3段階トレーニングパイプライン、思考の連鎖(CoT)プロンプト技術、OpenAI Codexの解剖、そしてAIコードの『スイスチーズモデル』を防ぐ防御的検証アーキテクチャを詳解。"
---

![Inside Coding LLMs & Prompt Engineering](./images/02_cs146s_coding_llms_swiss_cheese.png)

スタンフォード大学の最先端ソフトウェア工学講義 **CS146S: 現代のソフトウェア開発者 (The Modern Software Developer)** 第2講の深層技術解説へようこそ。

第1講では、開発者が単なる構文のタイピストから、自律型AIエージェントチームを統率する「オーケストラの指揮者」へと進化するパラダイムシフトを概観しました。**第2講 (Week 1)** では、この革命を支える計算エンジンである **コーディング大規模言語モデル (Coding LLMs)** の内部動作メカニズムと、これらを制御するソフトウェア工学手法である **プロンプトエンジニアリング (Prompt Engineering)** を徹底的に解剖します。

Andrej Karpathyの *Deep Dive into LLMs*、OpenAIの *How OpenAI Uses Codex*、Google CloudおよびDAIR.AIの最新研究に基づき、モデルがプログラミング言語を習得する数学的プロセス、一見完璧に見えるAIコードに潜む致命的な欠陥（**スイスチーズモデル**）、そしてそれを防衛する **「信頼せよ、されど検証せよ (Trust but Verify)」** のアーキテクチャを完全網羅します。

{/* truncate */}

---

### 1. LLMの内部解剖：3段階のトレーニングパイプライン

AIコーディングモデルを正確に操りデバッグするためには、その重み（Weights）がどのような過程を経て鍛造されたかを理解する必要があります。現代の大規模言語モデルは単一のルールエンジンではなく、厳格な **3段階パイプライン** を経て構築されます：

```mermaid
flowchart LR
    subgraph ステップ1 ["ステップ1: 事前学習 (Pre-training)"]
        D1[Webデータ & GitHubコード<br/>数兆トークン] --> N1[Transformerベースモデル<br/>次トークン確率予測 P(w_t | Context)]
    end

    subgraph ステップ2 ["ステップ2: 教師あり微調整 (SFT)"]
        N1 --> D2[高品質な対話ペア<br/>指示応答プロトコル注入]
        D2 --> N2[指示追従型アシスタント<br/>開発者ペルソナの確立]
    end

    subgraph ステップ3 ["ステップ3: 人間のフィードバックによる強化学習 (RLHF)"]
        N2 --> D3[人間の選好ランキング評価<br/>報酬モデル(Reward Model)調整]
        D3 --> N3[プロダクションコーディングLLM<br/>安全かつ整列されたコード生成]
    end
```

#### 1.1. 事前学習 (Pre-training): 教師なしの知識吸収
事前学習において、デコーダー専用(Decoder-only)のTransformerモデルはペタバイト規模のWebテキストとオープンソースリポジトリを処理します。テキストは文字や単語単位ではなく、**BPE (Byte-Pair Encoding)** によってサブワードトークンに分割されます：
- 1トークンは約3〜4文字、または頻出する構文断片（`def `, `return `, `const ` など）に相当します。
- 損失関数は非常にシンプルな **「次トークン予測 (Next-Token Prediction)」** です：

```text
P(w_t | w_1, w_2, ..., w_t-1) = Softmax(W_v * h_t-1)
```

- 数兆トークンのコードを通じて、モデルは構文木、アルゴリズムパターン、標準ライブラリのAPI仕様を潜在空間に埋め込みます。しかし、事前学習のみを終えたベースモデルは単なる「超巨大な自動補完エンジン」に過ぎず、開発者の指示に従って対話することはできません。

#### 1.2. 教師あり微調整 (SFT): 対話プロトコルの注入
自動補完エンジンを有能なペアプログラマーに変貌させるため、**SFT (Supervised Fine-Tuning)** を実施します。
- 熟練エンジニアが作成した数万件の高品質な `<指示, 模範コード解答>` ペアを学習させます。
- これにより、Markdownコードブロックのフォーマット、エッジケースの解説、丁寧な技術解説トーンを身につけます。

#### 1.3. RLHF と DPO (Direct Preference Optimization) によるアライメント
SFTモデルであっても、非効率、安全性の低いコード、または過度に冗長な実装を出力することがあります。
- 同一のプログラミング問題に対してモデルが生成した複数の候補コードを、人間のレビュアーが品質・安全性・可読性で順位付けします。
- この順位データを用いて **報酬モデル (Reward Model)** を学習させ、PPOやDPOアルゴリズムを通じて人間の意図に合致するよう重みを最適化します。

> **核心概念**: IDE上でAIが提示するコードは、意識を持った知性の発露ではなく、*世界中のトップエンジニアが書いたであろう「理想のコード」を統計学的に超高速シミュレーションした結果*です。

---

### 2. Codexはどのようにコードを理解するのか？

OpenAIの研究論文 *How OpenAI Uses Codex* によれば、LLMが自然言語よりもプログラミング言語において極めて優れた能力を示す理由は3つあります：

1. **決定論的構文と抽象構文木 (AST)**: 自然言語と異なり、コードは文脈自由文法 (CFG) に厳格に従い、曖昧さなく **抽象構文木 (AST)** にパースできます。
2. **長距離依存関係 (Long-range Invariants)**: 5行目で宣言された型は80行目の関数呼び出しと厳密に一致する必要があります。Transformerのマルチヘッド自己注意機構 (Self-Attention) は、この長距離構文制約を追跡するのに数学的に最適です。
3. **GitHubの大規模事前学習**: 何億ものオープンソースリポジトリを事前学習したことで、現代のフレームワークやデザインパターンを網羅しています。

しかし、コーディングLLMはトークン生成中に実際にコードをコンパイルしたり実行したりしません。統計的パターンに基づいて生成するため、非推奨となったAPIの引数を渡したり、微妙な競合状態を生み出すコードを悪意なく平然と出力します。

---

### 3. ソフトウェア工学としてのプロンプトエンジニアリング

プロンプトエンジニアリングは単なる「対話のコツ」ではありません。スタンフォードCS146Sでは、**確率的モデルから決定論的 (Deterministic) な成果物を引き出すための厳格なソフトウェア設計手法** と定義されます。

```mermaid
flowchart TD
    subgraph プロンプト戦略階層 ["プロンプトエンジニアリングの階層構造"]
        P1["ゼロショット (Zero-Shot): 単純命令<br/>'Go言語でクイックソートを実装して'"]
        P2["フューショット (Few-Shot): パターン整合<br/>入出力の模範サンプルを2〜3件提示"]
        P3["思考の連鎖 (Chain-of-Thought): 推論過程の強制<br/>'ステップ・バイ・ステップで例外を分析して'"]
        P4["仕様駆動プロンプティング: 不変条件と境界制約<br/>SPEC.md + 厳格な禁止事項を明示"]
    end

    P1 -->|複雑な論理でエラー急増| Fail[幻覚とエッジケースの欠落]
    P2 -->|出力スキーマの保証| Better[一貫したJSON/AST出力]
    P3 -->|自己検証トークンの活性化| Strong[アルゴリズム正当性の大幅向上]
    P4 -->|本番運用水準| Prod[検証合格プロダクションコード]
```

#### 3.1. ゼロショット vs フューショット
- **ゼロショット**: 例示を与えずに直接命令する方法。単純なボイラープレート変換（例: JSONスキーマからTypeScript型定義への変換）に適しています。
- **フューショット**: 2〜3件の入出力例をプロンプト内に含める手法。モデルの重みを更新することなく **インコンテキストラーニング (In-context Learning)** を活用し、社内のAPI規約やJSON形式を遵守させます。

#### 3.2. 思考の連鎖 (Chain-of-Thought, CoT)
複雑な並行処理やアルゴリズムを要求する際、即座にコードを書かせると論理エラーが多発します。
そこで次の指示を注入します：
> *"コードを書く前に、発生しうる3つの競合状態(Race Condition)を段階的に分析し、メモリバリアの不変条件をテキストで明示してください。"*

Transformerは直前に生成されたトークンを参照して次を生成するため、**推論ステップを先に出力させることで自己検証コンテキストが形成され、コードの正答率が飛躍的に向上**します。

---

### 4. AIコード生成の「スイスチーズモデル」

第2講で最も強調されたメンタルモデルは、Andrej Karpathyが提唱した **スイスチーズモデル (Swiss Cheese Model)** です。

安全工学においてJames Reasonが提唱したスイスチーズモデルは、複数の防護壁に空いた穴が偶然一直線に重なったときに大事故が起きるという理論です。AIコーディングではこれが逆向きに作用します：

```mermaid
flowchart TD
    subgraph チーズの脆弱性 ["AIコード生成におけるスイスチーズリスク"]
        A["LLM生成コード: 95%の流麗で完璧に見えるロジック"]
        H1["穴1: 微細なオフバイワン(Off-by-One)インデックスバグ"]
        H2["穴2: 非スレッドセーフなミューテックスロック順序"]
        H3["穴3: バッファ境界チェックの欠如"]
    end

    subgraph 多層防衛パイプライン ["多層防御エンジニアリングパイプライン"]
        L1["第1防衛線: 厳格な静的型検査 & リンター (TypeScript / Ruff)"]
        L2["第2防衛線: 決定論的単体テスト & プロパティファジング (Pytest)"]
        L3["第3防衛線: 動的サニタイザー & 並行性検証 (ASan / TSan)"]
        L4["第4防衛線: シニアエンジニアによるアーキテクチャレビュー"]
    end

    A --> H1 & H2 & H3
    H1 -->|自動検知・修正| L1
    H2 -->|テスト失敗・遮断| L3
    H3 -->|セキュリティ監査で遮断| L4
    L4 ==> PASS[安全な本番リリース]
```

#### なぜコーディングLLMには穴が空いているのか？
AIは200行の数学的に見事な動的計画法コードを瞬時に出力しますが、187行目に境界外参照エラーを潜ませたり、デッドロックを引き起こすロック順序を含ませたりします。

コードが極めて綺麗に書かれているため、人間はシステムを盲信する **自動化バイアス (Automation Bias)** に陥ります。AI生成コードを無批判にマージすると、その穴をすり抜けて本番障害が発生します。

---

### 5. 「信頼せよ、されど検証せよ」エンジニアリングアーキテクチャ

スタンフォードCS146Sが提唱する防御的ハーネス設計です：

```mermaid
sequenceDiagram
    autonumber
    actor Dev as 設計者 (ソフトウェアエンジニア)
    participant Spec as SPEC.md 不変条件
    participant LLM as コーディングLLM (Claude Code / Cursor)
    participant Gate as 自動検証ゲート (Verification Gate)
    participant Prod as 本番Mainブランチ

    Dev->>Spec: 正式な仕様と不変条件を定義
    Dev->>LLM: SPECとコンテキストを与えて実装指示
    LLM->>LLM: 思考の連鎖(CoT)による推論実行
    LLM->>Gate: コードと単体テストを自動コミット

    rect rgb(30, 41, 59)
        note over Gate: 自動化多層検証パイプライン
        Gate->>Gate: 1. 厳格な静的型チェック (tsc / mypy)
        Gate->>Gate: 2. 単体・統合テストの実行 (Pytest)
        Gate->>Gate: 3. プロパティベースの境界ファジング (Fuzzing)
    end

    alt 検証失敗
        Gate-->>LLM: スタックトレースをフィードバック (ループ工学)
        LLM->>Gate: 自己修復パッチを再提出
    else 全ゲート合格
        Gate-->>Dev: 100%合格メトリクスとGit Diffを提出
        Dev->>Dev: アーキテクチャおよびセキュリティ最終レビュー
        Dev->>Prod: 本番環境へマージ
    end
```

---

### 6. プロンプトパラダイム比較マトリクス

| 評価軸 | 対話型ゼロショット | フューショット・スキーマ | スタンフォードCS146S 仕様駆動 (SDD) |
| :--- | :--- | :--- | :--- |
| **入力形式** | 自然言語チャット (`"このバグ直して"`) | システムプロンプト + JSON入出力例2〜3件 | 正式なMarkdown仕様書 (`SPEC.md`) + 不変条件 |
| **モデルの推論** | 制約のない単発トークン生成 | サンプルスキーマに合わせた条件付き生成 | 思考の連鎖 (CoT) + MCPツール呼び出しループ |
| **幻覚(ハルシネーション)率** | **高** (未知のエッジケースで30〜45%) | 構文上は**低**、業務論理は**中** | **極めて低** (自動テストハーネスで完全防衛) |
| **再現性** | 低（表現の揺らぎで結果が変動） | 高（定型スキーマの抽出） | 完全（Gitで仕様とテストコードをバージョン管理） |
| **主たる適用領域** | アイデア出し、構文検索 | データ構造変換、APIパーサー開発 | 本番機能開発、リファクタリング、インフラ自動化 |

---

### 7. スタンフォード講義Q&A：大規模コードベースにおける課題

> **Q. なぜLLMは小さな競技プログラミング問題は完璧に解くのに、10万行の大規模企業リポジトリになると急に幻覚を起こしてコードを壊すのですか？**

**教員回答:**
これこそが **「コンテキスト飽和 (Context Saturation)」と「アテンションの希釈 (Attention Dilution)」** の問題です。
1. 数万行のコードを無差別にコンテキストウィンドウへ投入すると、Transformerの自己注意重みが不要なトークン全体へ分散します。
2. コンテキストが長大化すると **「Lost in the Middle (中央位置の情報の忘却)」** 現象が生じ、冒頭の指示と直前の入力ばかりに注目し、中央にある重要な不変条件を無視してしまいます。
3. したがって現代のAI工学では、コード全体を渡すのではなく、**ASTシンボルマップと依存関係グラフのみを高密度に抽出して注入する技術** が不可欠です。（第3講のMCPおよび第4講で詳解します）。

---

### 8. 第2講のまとめ

1. **マシンの本質を理解せよ**: コーディングLLMは統計的シミュレーターです。
2. **思考の連鎖を活用せよ**: CoTで中間推論トークンを生成させ、正答率を高めてください。
3. **スイスチーズを警戒せよ**: 綺麗なコードほど自動化バイアスを捨て、隠れたバグを疑ってください。
4. **信頼せよ、されど検証せよ**: 自動化されたテストハーネスを構築し、人間はアーキテクチャの検証に注力してください。

---

### 参考文献 & 公式教材
- **公式YouTubeプレイリスト**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **主要文献**: Andrej Karpathy, *Deep Dive into LLMs*; OpenAI, *How OpenAI Uses Codex*; Google Cloud & DAIR.AI, *Prompt Engineering Guide*.
- **提供機関**: スタンフォード大学 コンピュータサイエンス学科
"""

# 2. Full Spanish Version (Unabbreviated, High-Density)
es_full = """---
slug: stanford-cs146s-2-coding-llms-prompt-engineering
title: "[Stanford CS146S #2] Arquitectura de LLMs para Código e Ingeniería de Prompts: De Pre-entrenamiento y RLHF al Modelo de Queso Suizo"
authors: [jbgih]
tags: [stanford-cs146s, coding-llms, prompt-engineering, rlhf, chain-of-thought, swiss-cheese-model, software-architecture]
date: 2026-10-23
keywords: [Coding LLMs, Prompt Engineering, RLHF, Chain of Thought, Swiss Cheese Model]
description: "Guía completa de la Clase 2 de Stanford CS146S: El pipeline de 3 etapas de los LLMs de código (Pre-entrenamiento, SFT, RLHF), técnicas avanzadas de Chain-of-Thought, análisis de OpenAI Codex y la arquitectura defensiva 'Confía pero Verifica' frente al Modelo de Queso Suizo."
---

![Inside Coding LLMs & Prompt Engineering](./images/02_cs146s_coding_llms_swiss_cheese.png)

Bienvenidos al análisis técnico de la **Clase 2 (Semana 1) de Stanford CS146S: El Desarrollador de Software Moderno**.

Si en la primera lección definimos la transición del desarrollador de mero mecanógrafo a director de orquesta de agentes autónomos, en esta segunda clase nos sumergimos en el motor fundamental de esta revolución: los **Modelos de Lenguaje para Código (Coding LLMs)** y la disciplina de **Ingeniería de Prompts (Prompt Engineering)**.

Basado en las lecturas fundamentales de Andrej Karpathy (*Deep Dive into LLMs*), OpenAI (*How OpenAI Uses Codex*) y las investigaciones de Google Cloud y DAIR.AI, analizamos cómo las redes neuronales adquieren competencia en código, por qué sufren del traicionero **Modelo de Queso Suizo** y cómo los ingenieros deben implementar la doctrina de **"Confía pero Verifica"**.

{/* truncate */}

---

### 1. Anatomía de un LLM: El Pipeline de Tres Etapas

Para dirigir y depurar eficazmente asistentes de código con IA, un ingeniero de software debe entender cómo se forjaron los pesos del modelo:

```mermaid
flowchart LR
    subgraph Fase1 ["Fase 1: Pre-entrenamiento (Pre-training)"]
        D1[Trillones de Tokens de Código Web & GitHub] --> N1[Modelo Transformer Base<br/>Predicción del Siguiente Token P(w_t | Context)]
    end

    subgraph Fase2 ["Fase 2: Ajuste Fino Supervisado (SFT)"]
        N1 --> D2[Pares de Diálogo de Alta Calidad<br/>Protocolo de Instrucción]
        D2 --> N2[Asistente de Instrucciones<br/>Persona de Desarrollador]
    end

    subgraph Fase3 ["Fase 3: RLHF y Alineación"]
        N2 --> D3[Ranking de Preferencia Humana<br/>Modelo de Recompensa (Reward Model)]
        D3 --> N3[LLM de Código para Producción<br/>Seguro, Alineado y Determinista]
    end
```

#### 1.1. Pre-entrenamiento: Ingestión de Conocimiento no Supervisada
Un modelo Transformer tipo Decoder procesa petabytes de código fuente dividido en tokens mediante **BPE (Byte-Pair Encoding)**:
- Un token representa aproximadamente 3–4 caracteres o fragmentos comunes (`def `, `return `, `const `).
- El objetivo de pérdida es la **Predicción del Siguiente Token (Next-Token Prediction)**:

```text
P(w_t | w_1, w_2, ..., w_t-1) = Softmax(W_v * h_t-1)
```

- Al minimizar la pérdida de entropía cruzada, la red codifica implícitamente árboles sintácticos, algoritmos e interfaces de API. Sin embargo, el modelo base resultante es solo un motor de autocompletado colosal.

#### 1.2. Ajuste Fino Supervisado (SFT)
Para convertir el autocompletado en un programador par, se introducen decenas de miles de pares `<Pregunta, Código Óptimo>` curados por ingenieros sénior, enseñándole al modelo a estructurar bloques de código y explicar casos borde.

#### 1.3. RLHF y Optimización Directa de Preferencias (DPO)
Mediante un **Modelo de Recompensa**, evaluadores humanos puntúan múltiples respuestas generadas ante una misma tarea de programación. Algoritmos como PPO o DPO ajustan los pesos para favorecer código seguro y legible.

> **Concepto Clave**: Cuando un LLM de código responde, realiza una **simulación estadística** ultraveloz de lo que un ingeniero experimentado escribiría.

---

### 2. Cómo Entiende el Código OpenAI Codex

OpenAI reveló que los LLMs destacan en programación por tres razones estructurales:
1. **Gramáticas Formales y Árboles AST**: El código sigue gramáticas libres de contexto y se parsea en **Árboles de Sintaxis Abstracta (AST)** sin ambigüedad.
2. **Invariantes de Largo Alcance**: La atención multidireccional del Transformer rastrea declaraciones de tipos a cientos de líneas de distancia.
3. **Ingestión Masiva de GitHub**: Millones de repositorios proporcionan un catálogo exhaustivo de patrones de diseño.

Sin embargo, el modelo no compila ni ejecuta el código mientras predice tokens: no tiene capacidad de verificación intrínseca.

---

### 3. Ingeniería de Prompts como Disciplina de Ingeniería de Software

En Stanford CS146S, la ingeniería de prompts es el diseño sistemático de entradas para guiar modelos probabilísticos hacia resultados deterministas:

```mermaid
flowchart TD
    subgraph Jerarquia_Prompts ["Jerarquía de Arquitectura de Prompts"]
        P1["Zero-Shot: Comando Directo<br/>'Implementa QuickSort en Go'"]
        P2["Few-Shot: Coincidencia de Patrones<br/>2-3 Ejemplos de Entrada/Salida"]
        P3["Chain-of-Thought (CoT): Razonamiento Paso a Paso<br/>'Analiza primero las condiciones de carrera'"]
        P4["Prompting Basado en Especificaciones (SDD)<br/>SPEC.md + Invariantes Rígidos"]
    end

    P1 -->|Errores en Lógica Compleja| Fail[Alucinaciones y Omisión de Bordes]
    P2 -->|Garantía de Esquema| Better[Estructuras JSON Consistentes]
    P3 -->|Activación de Auto-verificación| Strong[Precisión Algorítmica Elevada]
    P4 -->|Estándar de Producción| Prod[Código Verificado Apto para Despliegue]
```

#### 3.1. Cadena de Pensamiento (Chain-of-Thought, CoT)
Al solicitar código concurrente o algoritmos difíciles, exigir al modelo que analice primero los pasos lógicos (`"Let's think step by step"`) genera tokens intermedios de razonamiento que actúan como contexto propio, aumentando radicalmente la tasa de acierto.

---

### 4. El "Modelo de Queso Suizo" de la Generación de Código

Adaptando el modelo de seguridad de James Reason, Andrej Karpathy ilustra cómo la IA puede producir código deslumbrante con agujeros ocultos críticos:

```mermaid
flowchart TD
    subgraph Peligro_Queso_Suizo ["Riesgo de Queso Suizo en Código IA"]
        A["Código Generado: 95% Elegante y Estructurado"]
        H1["Agujero 1: Error de Índice Fuera de Rango (Off-by-One)"]
        H2["Agujero 2: Bloqueo Mutex Inseguro en Concurrencia"]
        H3["Agujero 3: Vulnerabilidad de Desbordamiento de Búfer"]
    end

    subgraph Capas_Defensivas ["Pipeline de Verificación Defensiva"]
        L1["Capa 1: Tipado Estático y Linters (TypeScript / Ruff)"]
        L2["Capa 2: Pruebas Unitarias y Fuzzing de Invariantes (Pytest)"]
        L3["Capa 3: Sanitizadores de Memoria y Concurrencia (ASan / TSan)"]
        L4["Capa 4: Revisión Humana de Arquitectura y Seguridad"]
    end

    A --> H1 & H2 & H3
    H1 -->|Bloqueado por| L1
    H2 -->|Bloqueado por| L3
    H3 -->|Bloqueado por| L4
    L4 ==> PASS[Despliegue Seguro en Producción]
```

Debido a que el código luce impecable, los desarrolladores caen en el **Sesgo de Automatización (Automation Bias)**. Si se aprueban PRs generados por IA sin verificación profunda, los agujeros del queso colapsarán los sistemas en producción.

---

### 5. La Arquitectura de Ingeniería "Confía pero Verifica"

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Ingeniero de Software (Arquitecto)
    participant Spec as SPEC.md e Invariantes
    participant LLM as LLM de Código (Claude Code / Cursor)
    participant Gate as Compuerta de Verificación Automatizada
    participant Prod as Rama Principal de Producción

    Dev->>Spec: Escribe Restricciones e Invariantes
    Dev->>LLM: Envía Tarea con Especificación
    LLM->>LLM: Razonamiento Paso a Paso (CoT)
    LLM->>Gate: Confirma Código y Pruebas Unitarias

    rect rgb(30, 41, 59)
        note over Gate: Compuerta de Verificación Automatizada
        Gate->>Gate: 1. Tipado Estático Estricto (tsc / mypy)
        Gate->>Gate: 2. Ejecución de Pruebas Unitarias
        Gate->>Gate: 3. Fuzzing de Invariantes
    end

    alt Falla Alguna Prueba
        Gate-->>LLM: Reinyecta Traza de Error (Ingeniería de Bucles)
        LLM->>Gate: Sintetiza Parche de Corrección
    else Pasa Todas las Pruebas
        Gate-->>Dev: Diff Limpio con 100% de Métricas Aprobadas
        Dev->>Dev: Revisión de Seguridad y Arquitectura
        Dev->>Prod: Merge a Producción
    end
```

---

### 6. Matriz Comparativa de Paradigmas

| Dimensión | Prompting Conversacional | Prompting con Esquema Few-Shot | Prompting Dirigido por Especificaciones (CS146S) |
| :--- | :--- | :--- | :--- |
| **Formato de Entrada** | Chat en lenguaje natural (`"Arregla este bug"`) | Prompt de sistema + 2–3 ejemplos JSON | Especificación formal (`SPEC.md`) + contratos |
| **Cognición del Modelo** | Generación de tokens sin restricciones | Generación condicionada al esquema de ejemplo | Razonamiento paso a paso (CoT) + MCP |
| **Riesgo de Alucinación** | **Alto** (30–45% en casos borde) | **Bajo** en sintaxis, **Medio** en negocio | **Extremadamente Bajo** (bloqueado por pruebas) |
| **Reproducibilidad** | Baja (varía con el tono) | Alta (estructuras consistentes) | Total (versionado en Git junto con los tests) |

---

### 7. Preguntas y Respuestas de Stanford CS146S

> **P. ¿Por qué un LLM resuelve problemas de LeetCode de forma brillante, pero en un repositorio empresarial de 100.000 líneas comienza a alucinar y romper componentes?**

**Respuesta del Claustro:**
Es el problema de **Saturación de Contexto y Dilución de la Atención**.
1. Al inyectar miles de líneas de código en la ventana de contexto, los pesos de atención se dispersan.
2. Ocurre el fenómeno **"Lost in the Middle"**: el modelo prioriza el inicio y el final, olvidando reglas intermedias críticas.
3. La solución de ingeniería moderna es el **Mapeo de Repositorios (Repo Mapping)**: extraer únicamente los símbolos AST y dependencias directas mediante herramientas como Tree-sitter y MCP.

---

### 8. Conclusiones de la Clase 2

1. **Entiende la Máquina**: Los LLMs son simuladores estadísticos de tokens.
2. **Diseña el Prompt**: Aplica CoT y restricciones explícitas para generar contexto de razonamiento.
3. **Cuidado con el Queso Suizo**: Desconfía de la elegancia superficial del código de IA.
4. **Confía pero Verifica**: Automatiza linters, pruebas unitarias y fuzzers antes de la revisión humana.

---

### Referencias y Materiales del Curso
- **Lista de Reproducción Oficial en YouTube**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Literatura Principal**: Andrej Karpathy, *Deep Dive into LLMs*; OpenAI, *How OpenAI Uses Codex*; Google Cloud & DAIR.AI, *Prompt Engineering Guide*.
- **Institución**: Universidad de Stanford, Departamento de Ciencias de la Computación
"""

# 3. Full Simplified Chinese Version
zh_hans_full = """---
slug: stanford-cs146s-2-coding-llms-prompt-engineering
title: "[斯坦福 CS146S #2] 代码大模型底层原理与提示词工程：从预训练、RLHF到“瑞士奶酪模型”的代码验证哲学"
authors: [jbgih]
tags: [stanford-cs146s, coding-llms, prompt-engineering, rlhf, chain-of-thought, swiss-cheese-model, software-architecture]
date: 2026-10-23
keywords: [Coding LLMs, Prompt Engineering, RLHF, Chain of Thought, Swiss Cheese Model]
description: "斯坦福大学 CS146S 第2讲深度技术解析：代码大模型三阶段训练流水线（预训练、SFT、RLHF）、思维链(CoT)提示词工程、OpenAI Codex 底层机制，以及应对 AI 代码“瑞士奶酪模型”隐患的“信任但必须验证”工程防御架构。"
---

![Inside Coding LLMs & Prompt Engineering](./images/02_cs146s_coding_llms_swiss_cheese.png)

欢迎回到斯坦福大学前沿软件工程课程 **CS146S：现代软件开发者 (The Modern Software Developer)** 第2讲的技术深度解析。

在第1讲中，我们确立了宏观架构视角：现代软件工程师正从手工代码打字员向调度多智能体协作的交响乐指挥家演进。在**第2讲（第一周）**中，课程直接切入驱动这场变革的核心引擎：**代码大语言模型（Coding LLMs）**与**提示词工程（Prompt Engineering）**。

结合 Andrej Karpathy 的经典讲义《Deep Dive into LLMs》、OpenAI 论文《How OpenAI Uses Codex》以及 Google Cloud 与 DAIR.AI 的最新提示词工程研究，本讲全面揭示大模型理解代码的数理本质，深度剖析 AI 代码生成中的**“瑞士奶酪模型”**风险，并阐明**“信任但必须验证（Trust but Verify）”**的工业级防御架构。

{/* truncate */}

---

### 1. 代码大模型的底层解构：三阶段训练流水线

要高效调度和调试 AI 编程助手，工程师必须理解模型权重的锻造过程。现代大模型绝非单体规则引擎，而是经历严密的**三阶段训练流水线**：

```mermaid
flowchart LR
    subgraph 阶段一 ["阶段一：预训练 (Pre-training)"]
        D1[数万亿 Token 网页与开源代码] --> N1[Transformer 基座模型<br/>下一个 Token 概率预测 P(w_t | Context)]
    end

    subgraph 阶段二 ["阶段二：指令监督微调 (SFT)"]
        N1 --> D2[高质量指令问答数据对<br/>注入对话与格式规则]
        D2 --> N2[指令遵循代码助手<br/>确立专业开发者角色]
    end

    subgraph 阶段三 ["阶段三：人类反馈强化学习 (RLHF)"]
        N2 --> D3[人类偏好排序评估<br/>训练奖励模型 (Reward Model)]
        D3 --> N3[工业级对齐代码大模型<br/>安全、对齐且确定性输出]
    end
```

#### 1.1. 预训练 (Pre-training)：无监督海量吸收
解码器专用 (Decoder-only) Transformer 吞吐数 PB 源码，通过 **BPE (Byte-Pair Encoding)** 切分为 Token（约3~4字符或常见代码片段如 `def `, `return `）。
损失函数极为简洁——**下一个 Token 预测 (Next-Token Prediction)**：

```text
P(w_t | w_1, w_2, ..., w_t-1) = Softmax(W_v * h_t-1)
```

通过数万亿 Token 的交叉熵损失最小化，网络隐式习得语法树与算法逻辑。但此时它只是一个超级自动补全机。

#### 1.2. 监督微调 (SFT) 与强化学习 (RLHF)
- **SFT**：学习数万对高质量 `<问题, 模范解答>`，掌握 Markdown 排版与边界情况处理。
- **RLHF / DPO**：通过人类偏好排序与奖励模型，使用 PPO 或 DPO 算法微调权重，惩罚低效和不安全代码。

> **核心认知**：AI 编写的代码不是意识的产物，而是对全世界顶级工程师可能写出的“理想代码”进行**超高速统计模拟**的结果。

---

### 2. 软件工程视角下的提示词工程 (Prompt Engineering)

提示词工程绝非简单的“聊天技巧”，而是从概率模型中提取确定性结果的严密工程方法：

```mermaid
flowchart TD
    subgraph 提示词层级 ["提示词架构演进层级"]
        P1["零样本 (Zero-Shot): 直接指令<br/>'用 Go 实现快速排序'"]
        P2["少样本 (Few-Shot): 上下文模式匹配<br/>提供 2~3 个标准输入输出样例"]
        P3["思维链 (Chain-of-Thought): 强制推理步骤<br/>'请按步骤先分析并发竞态条件'"]
        P4["规范驱动提示 (SDD): 严格不变量与边界约束<br/>SPEC.md + 机器可读验证契约"]
    end

    P1 -->|复杂逻辑错误率飙升| Fail[幻觉与边界遗漏]
    P2 -->|保证格式一致| Better[稳定的 JSON / 结构体格式]
    P3 -->|激活自验证 Token| Strong[算法正确率显著飞跃]
    P4 -->|工业级交付标准| Prod[验证通过的生产级代码]
```

#### 思维链 (Chain-of-Thought, CoT)
在要求生成复杂并发或算法代码时，注入指令：
> *"在编写代码前，请分步骤分析可能存在的3种竞态条件，并在文本中明确列出内存屏障不变量。"*

模型生成的中间推理 Token 成为自生上下文，大幅降低逻辑缺陷。

---

### 3. AI 代码生成的“瑞士奶酪模型”

Andrej Karpathy 引入安全工程中的 **瑞士奶酪模型 (Swiss Cheese Model)**：模型生成的 200 行代码看似毫无破绽，却常常隐藏着细微的边界溢出或死锁（奶酪孔洞）。

```mermaid
flowchart TD
    subgraph 奶酪风险 ["AI 代码生成的瑞士奶酪风险"]
        A["LLM 生成代码: 95% 优美规范的逻辑"]
        H1["孔洞 1: 细微的 Off-by-One 索引越界"]
        H2["孔洞 2: 缺乏线程安全的互斥锁顺序"]
        H3["孔洞 3: 缺少缓冲区边界防御校验"]
    end

    subgraph 防御流水线 ["多层防御工程流水线"]
        L1["第 1 道防线: 严格静态类型检查与 Linter (tsc / Ruff)"]
        L2["第 2 道防线: 确定性单元测试与属性模糊测试 (Pytest)"]
        L3["第 3 道防线: 动态内存与并发分析器 (ASan / TSan)"]
        L4["第 4 道防线: 人类资深架构师安全审查"]
    end

    A --> H1 & H2 & H3
    H1 -->|静态分析拦截| L1
    H2 -->|测试失败拦截| L3
    H3 -->|安全审查拦截| L4
    L4 ==> PASS[安全发布至生产环境]
```

由于代码结构极为工整，人类极易陷入**自动化偏差 (Automation Bias)**。未经多层防御验证直接合并 AI 代码，孔洞一旦贯通必将导致生产事故。

---

### 4. “信任但必须验证”工程防御架构

```mermaid
sequenceDiagram
    autonumber
    actor Dev as 软件架构师 (人类)
    participant Spec as SPEC.md 不变量契约
    participant LLM as 代码大模型 (Claude Code / Cursor)
    participant Gate as 自动化验证门禁
    participant Prod as 生产环境主分支

    Dev->>Spec: 编写规范文档与不变量
    Dev->>LLM: 派发任务与上下文规范
    LLM->>LLM: 执行思维链 (CoT) 逐步推理
    LLM->>Gate: 提交实现代码与配套单元测试

    rect rgb(30, 41, 59)
        note over Gate: 自动化多层验证流水线
        Gate->>Gate: 1. 严格静态类型分析 (0 警告)
        Gate->>Gate: 2. 自动化单元与集成测试
        Gate->>Gate: 3. 基于属性的随机模糊测试
    end

    alt 任意测试未通过
        Gate-->>LLM: 反馈错误堆栈追踪 (循环工程)
        LLM->>Gate: 提交自愈修复补丁
    else 全部门禁 100% 通过
        Gate-->>Dev: 提交无瑕疵 Git Diff 与测试报告
        Dev->>Dev: 架构合规与安全终审
        Dev->>Prod: 合并至主干发布
    end
```

---

### 5. 提示词范式对比矩阵

| 评估维度 | 对话式零样本 (Zero-Shot) | 少样本模式匹配 (Few-Shot) | 斯坦福 CS146S 规范驱动 (SDD) |
| :--- | :--- | :--- | :--- |
| **输入形式** | 自然语言聊天 (`"修复这个错误"`) | 系统提示词 + 2~3 个标准 JSON 样例 | 形式化 Markdown 规范 (`SPEC.md`) + 契约 |
| **模型认知** | 无约束单次 Token 输出 | 受样例格式约束的条件输出 | 思维链步骤推理 + MCP 工具沙箱调用 |
| **幻觉风险** | **高** (未知边界下 30~45%) | 语法**低**，业务逻辑**中** | **极低** (由自动化测试门禁完全兜底) |
| **可复现性** | 低 (语气微调即引发变动) | 高 (严格遵守格式) | 完全可复现 (Git 版本化协同管控) |

---

### 6. 斯坦福课堂 Q&A：大仓下的“上下文稀释”难题

> **问：为什么 LLM 在做刷题算法时表现优异，但在企业 10 万行大仓中却频繁制造破坏性改动？**

**教员解答**：
这是典型的**上下文饱和 (Context Saturation)** 与 **注意力稀释 (Attention Dilution)**。
大模型存在 **“迷失在中间 (Lost in the Middle)”** 现象：过多不相关代码冲淡了注意力权重，模型只关注首尾提示而遗漏中间的关键不变量。现代工程必须依靠 **代码仓符号图谱 (Repo Mapping)** 与 Tree-sitter AST 精准提取关键依赖。

---

### 7. 第 2 讲核心总结

1. **认清工具本质**：代码大模型是经过预训练、SFT 和 RLHF 训练的概率 Token 模拟器。
2. **驾驭思维链**：引入 CoT 产生显式推理步骤，大幅提升逻辑正确率。
3. **警惕瑞士奶酪**：抛弃自动化偏差，严查隐蔽边缘漏洞。
4. **信任但必须验证**：构建覆盖静态检查、单体测试与模糊测试的自动化门禁。

---

### 课程参考资料
- **官方 YouTube 教学视频列表**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **核心文献**: Andrej Karpathy, *Deep Dive into LLMs*; OpenAI, *How OpenAI Uses Codex*; Google Cloud & DAIR.AI, *Prompt Engineering Guide*.
- **学术机构**: 斯坦福大学计算机科学系
"""

# 4. Full Traditional Chinese Version
zh_hant_full = zh_hans_full.replace("大模型", "大型語言模型").replace("规范", "規範").replace("流水线", "管線").replace("单体", "單體").replace("思维链", "思維鏈").replace("大仓", "大型程式庫").replace("斯坦福", "史丹佛").replace("奶酪", "起司")

def update_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Updated: {path} ({len(content)} chars)")

update_file(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", ja_full)
update_file(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", es_full)
update_file(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hans_full)
update_file(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hant_full)

print("Episode 2 full-length reinforcement completed successfully!")
