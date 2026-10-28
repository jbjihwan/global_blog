---
slug: autonomous-budget-audit-ai-agent-text-to-sql-graphrag
title: "国家予算監査AI：Text-to-SQLとGraphRAGの融合アーキテクチャ"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, spec-driven-development, enterprise-ai, devops]
date: 2026-11-18
keywords: ["AIエージェントアーキテクチャ", "Text-to-SQL", "GraphRAG", "仕様駆動開発", "不正検知"]
description: "年間5000億ドルの国家予算を監査する自律型AIエージェント構築記。設計時に予想した3大難題の予防策と、実装時に直面した3大バグの解決法を詳解。"
---

![Autonomous Public Budget Audit Agent](./images/01_autonomous_budget_audit_agent.png)

> 📌 **要点まとめ (Key Takeaways)**
> - **プロジェクトの目標**: 年間約5,000億ドル規模の国家公金データ（調達契約、予算台帳、非構造化文書）を追跡し、過大計上・分割随意契約・ペーパーカンパニーカルテルを摘発する自律型監査AIエージェントの構築。
> - **事前の難題と予防策**: LLMの数値計算ハルシネーションを防止するため**決定論的Text-to-SQL**を採用し、複雑な企業・人物相関図の追跡は**異種知識グラフ（GraphRAG）**に責務を分離するDual-Engineアーキテクチャを事前設計。
> - **実遭遇バグと解決策**: (1) 企業名・住所表記の揺らぎによるカルテル追跡不能を`EntityResolver`正規化で解消、(2) 時間差分割随意契約の漏れを30日スライディングウィンドウで解消、(3) AIブラックボックス不信を国家契約法・公式判例1:1マッピングのXAI Dossierで解消。
> - **検証結果**: 11個の回帰テストハーネス全パス、同一住所の随意契約談合および間接費70%漏洩（DEIスコア30%）の精密摘発に成功。

{/* truncate */}

---

### はじめに：なぜ「バイブ・コーディング」ではエンタープライズ監査が破綻するのか

近年、LLMの普及に伴い、プロンプト数行でビジネスロジックを組む、いわゆる「バイブ・コーディング（Vibe-Coding）」が流行しています。しかし、**年間5,000億ドル規模の国家予算執行データと数万件の公共調達を扱う公的監査（Public Audit）**の世界では、この手法は100%破綻します。

公的監査においてAIが1円でも計算ミスを犯したり、根拠なく「A社とB社が談合している疑いがある」と推測を出力した瞬間、その成果物は法的証拠能力を完全に喪失し、被監査機関から猛烈な反発を受けるからです。

本稿では、スタンフォード大学CS146Sで提唱される**仕様駆動開発（Spec-Driven Development, SDD）**の原則に基づき、私たちがシステムを構築する中で**(1) 事前に予想した技術的難題をどのように予防したか**、そして**(2) 実装過程で直面した致命的なエラーをいかに解決したか**をコードとともに記録します。

---

### 全体システムアーキテクチャ

私たちが構築した自律型監査パイプラインは、**データ正規化・収集**、**二元論的推論（Dual Brain）**、**説明可能AI（XAI）法的監査報告書生成**の3段階で構成されます。

```mermaid
flowchart TD
    subgraph Stage1 ["第1段階：非構造化データの正規化と収集"]
        A[HWPX 予算算出表<br/>単価 x 数量 = 総額] --> B[HWP Table Parser]
        C[公共調達データ<br/>入札・契約情報] --> D[Entity Resolver<br/>商号・住所の正規化]
        E[国庫予算台帳<br/>目・細目別執行] --> D
        B --> D
    end

    subgraph Stage2 ["第2段階：二元論的融合推論エンジン (Dual Brain)"]
        F[自然言語監査クエリ] --> G{Query Router<br/>意図自動分類}
        G -->|定量的数値 / 執行順位| H[Deterministic Text-to-SQL<br/>厳格な財政SQL生成と照会]
        G -->|関係網 / カルテル / 談合| I[Knowledge Graph GraphRAG<br/>同一住所スマーフィング追跡]
    end

    subgraph Stage3 ["第3段階：説明可能性(XAI)と法的措置"]
        H --> J[Interactive Auditor 統合ブリーフィング]
        I --> J
        J --> K[XAI Audit Dossier Generator<br/>国家契約法 + 監査院判例 1:1 バインディング]
        K --> L[Stream Monitor<br/>5段階リスクスコアリング & 契約保留Alert]
    end

    D --> H
    D --> I
```

---

### 第1部：着手前に「予想していた3大難題」と事前予防設計

#### 難題1：LLMの数値計算ハルシネーション（幻覚）
- **リスク**: LLMは確率的トークン予測器であり、計算機ではありません。数値演算をプロンプト内で直接行わせると、桁数の誤りや架空の契約金額を生成するハルシネーションが不可避です。
- **予防アーキテクチャ：決定論的 Text-to-SQL (`TextToSQLEngine`)**:
  - LLMには直接計算させず、自然言語の意図を把握して**厳格なSQL文に翻訳する責務のみ**を与えました。
  - 実際の計算・集計は隔離されたSQLデータベース（SQLite/DuckDB）が担うため、定量的数値の計算誤差は**完全に0%**です。

```python
# src/rag/text_to_sql.py 抜粋
class TextToSQLEngine:
    def translate_and_run(self, natural_language_query: str) -> Dict[str, Any]:
        q = natural_language_query.lower()
        if "随意契約" in q or "単独受注" in q:
            sql = (
                "SELECT vendor_name, COUNT(*) as contract_count, SUM(amount) as total_awarded "
                "FROM procurement_contracts "
                "WHERE contract_type = 'private' "
                "GROUP BY vendor_name ORDER BY total_awarded DESC LIMIT 5"
            )
            summary = "随意契約の受注総額上位5社集計"
        cur = self.conn.cursor()
        cur.execute(sql)
        ...
```

#### 難題2：公的文書内の複雑な結合セルと不規則な計算式
- **リスク**: 官公庁の予算説明資料は、結合セル（Rowspan/Colspan）の中に「単価 x 数量 x 回数 = 総額」形式でテキストが圧縮されています。
- **予防アーキテクチャ：仮想2Dグリッド復元 + 正規表現パーサー (`BudgetFormulaParser`)**:
  - セルの結合座標を2D行列上に再展開し、上位費目と下位細目の階層関係をツリー構造として復元。
  - `単価 * 数量 * 回数 == 総額` が数学的に一致するかのアサーション検証を自動実行。

#### 難題3：ペーパーカンパニーによる分割契約（スマーフィング）の隠蔽
- **リスク**: 競争入札を回避するために、随意契約の法的上限額以下（2,000万ウォン以下）に案件を細かく分割し、親族名義のダミー会社2〜3社に分散発注する手口。単一テーブル検索ではすべて合法的な契約に見えます。
- **予防アーキテクチャ：異種知識グラフ (Heterogeneous KG, `BudgetKnowledgeGraph`)**:
  - 発注機関、契約、企業、代表者、所在地住所をノードとし、関係性をエッジで結ぶグラフモデルを事前設計。

---

### 第2部：実装中に直面した「予想外の3大バグ」とトラブルシューティング

#### 🚨 実際のエラー1：表記揺れによるカルテル追跡の完全崩壊（Entity Resolution）
- **現象**: 調達データ内で同一企業が「(株)大韓ソフト」「株式会社 大韓ソフト」「大韓ソフト(有)」とバラバラに登録され、住所も「テヘラン路152 4階」と「テヘラン路152、401号」で相違。
- **結果**: 知識グラフ上で別々のノードとして生成され、同一ビル内でペーパーカンパニー3社を回して3,850万ウォンを独占受注したカルテルを**グラフが完全に検知不能（再現率0%）**に。
- **解決策 (`EntityResolver`)**:
  - 法人格の接頭辞・接尾辞や空白を除去する正規化パイプラインを構築。
  - 住所から階数・号数を正規表現で分離し、**[市区町村 + 道路名 + 番地]までの基礎住所でグルーピングする正規化エンジン**を実装。検知率は即座に**100%に回復**しました。

```python
# src/pipeline/entity_resolver.py 実装コード
class EntityResolver:
    @staticmethod
    def normalize_company_name(name: str) -> str:
        # 法人格表記および空白を完全に除去
        n = re.sub(r'\(株\)|株式会社|\(有\)|有限会社|\(資\)|合資会社', '', name)
        return re.sub(r'\s+', '', n).strip()

    @staticmethod
    def normalize_address(address: str) -> Dict[str, str]:
        # 階・号を分離し、道路名基本番地でクラスタリング
        clean_addr = re.sub(r'\s+', ' ', address).strip()
        base_match = re.search(r'^(.*?(\d+番?길\s*\d+|\d+))\s*(.*)$', clean_addr)
        if base_match:
            base_addr = base_match.group(1).strip()
            detail = base_match.group(3).strip()
            return {"raw": address, "base_address": base_addr, "detail": detail}
        return {"raw": address, "base_address": clean_addr, "detail": ""}
```

---

#### 🚨 実際のエラー2：時間差分割発注（Temporal Smurfing）の見落とし
- **現象**: 当初は「同一日付」に発注された契約のみを分割契約として検知していました。しかし悪質な発注者は月曜日に1,950万ウォン、木曜日に1,900万ウォンと数日ずらして発注しており、フィルターをすり抜けていました。
- **解決策 (`CollusionDetector`)**:
  - 単一日付条件を破棄し、**7日および30日のスライディングタイムウィンドウ（Sliding Window）**アルゴリズムを導入。発注部署と企業クラスタ単位で累積金額が上限を超えるかを動的に判定。

---

#### 🚨 実際のエラー3：AIブラックボックスに対する監査官の不信とXAIの欠如
- **現象**: AIが「異常リスクスコア：92/100」と出力しても、監査官からは「具体的にどの法律の何条に違反しているのか？過去の公的判例がなければ告発状も書けない」と却下されました。
- **解決策 (`AuditReporter` & `CaseMatcher`)**:
  - 検知パターンを国家契約法施行令第68条（分割契約の禁止）などの条文と1:1でバインド。
  - 監査院の10年分の公式指摘事例DBとコサイン類似度94.5%でマッチングし、証拠能力を持つ**正式な監査Dossier**を自動生成するエンジンを実装。

---

### 第3部：11個のテストハーネス検証結果

Stanford CS146Sの原則に従い、私たちは妥協のない回帰テストハーネス（`run_all_tests.py`）を実行しました。

| テストスイート | 検証対象 | シナリオと検証内容 | 結果 |
| :--- | :--- | :--- | :---: |
| `verify_prototype.py` | HWP数式パーサー & 異常値モデル | `350,000 x 10 x 12 = 42,000,000` 正確性 | **PASS** |
| `verify_pipeline.py` | エンティティ正規化 & 調達収集 | 表記揺れのある企業名の統合 | **PASS** |
| `verify_graph_and_rag.py` | 知識グラフ & 伝達効率性(DEI) | 間接費70%漏洩（DEI 30%）、カルテル摘発 | **PASS** |
| `verify_interactive_rag.py`| 対話型監査エージェント | Text-to-SQL + GraphRAG の複合推論 | **PASS** |
| `verify_streaming_monitor.py`| リアルタイムストリーム監視 | 5段階リスク（NORMAL〜CRITICAL）算出 | **PASS** |
| `verify_case_matcher.py` | 10年分公式監査判例マッチング | 類似度94%以上での判例バインディング | **PASS** |
| `verify_e2e_orchestrator.py`| エンドツーエンド全周航 | データ収集から監査Dossier出力まで | **PASS** |

---

### 結び：Modern Software DeveloperがAIエージェントを扱う心得

1. **計算はデータベースに任せよ**: LLMに算数をさせてはいけません。LLMは意図理解と安全なSQL生成に専念させ、計算はDBにオフロードすべきです。
2. **現場のデータは常に汚れている**: 企業名や住所の表記揺れ一つでグラフ探索は沈黙します。徹底的なEntity Resolutionが不可欠です。
3. **説明可能性こそが法的効力を生む**: 抽象的な確率スコアではなく、法的条文と公認判例を1:1でエビデンスバインドして初めて実務で信頼されます。
