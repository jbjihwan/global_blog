---
slug: national-budget-ai-inspector-portal-verification-system
title: "[AI実践 #6] 監査官ウェブポータル構築と20全検証テスト通過記"
authors: [jbgih]
tags: [ai-agents, web-portal, test-automation, full-verification, audit-intelligence, devops]
date: 2026-11-23
keywords: ["監査官ウェブポータル", "Vis.js知識グラフ", "HWPX文書パーサー", "20全テスト検証", "国家予算AI監査完結"]
description: "国家予算AI監査シリーズ完結編。Vis.js知識グラフ、10カ年判例DB、HWPX即時パーサーを統合した監査官ウェブポータルv3.0の構築と20の検証テスト通過記。"
---

![National Budget Inspector Web Portal v3.0 & 20/20 Verification](./images/01_national_budget_inspector_portal.png)

> 💡 **重要ポイント (Key Takeaways)**
> - **監査官総合ウェブポータルv3.0の完成**: CLIスクリプトだった調達異常検知を、7つの専用タブ（総合ダッシュボード、6大標的セクター、弁明要求書自動生成、eナラドウ厶補助金、入札談合グラフ、国会予算審査、判例DB＆HWPXパーサー）を備えたリアルタイム統合管制センターへ刷新。
> - **20の全数検証テストハーネス100%通過 (20/20 PASS)**: プロトタイプSQL生成からGraphRAG、ストリーミング、DART法人登記追跡、入札カルテル、HWPX過大計上対照まで、全領域の統合検証テストを無欠点で通過。
> - **設計時に予防した2大課題**: (1) 異種監査エンジンの結合ボトルネックを12のRESTful DTOエンドポイント分離で解決、(2) リアルタイムストリーミング時のDOM過負荷を円形リングバッファ（Circular DOM Ring Buffer）で防止。
> - **開発中に解決した3大突発エラー**: (1) Vis.js物理演算の無限振動フリーズを安定化イベントによる強制凍結で解決、(2) 50ページのHWPX XMLパースによるメインループブロックをThreadPoolExecutor非同期キューで分離、(3) 並列テスト時のSQLiteファイルロック競合をプロセス別隔離メモリプールで解決。
> - **全6部作シリーズの完結**: 単なるプロンプト調整を超え、国家財政保護という実務領域で高信頼性を実証したエンジニアリングの軌跡。

{/* truncate */}

---

### ⚖️ 法的告知および匿名化について (Legal Notice & Anonymization)

> 本記事に記載されているすべての発注機関名（例: `A振興公団`、`B振興院`、`C公団`、`D区役所`）、受注企業名（例: `(株)○○IT`、`(株)○○コンサルティング`）、関係者名（例: `K氏`、`P氏`）、契約番号（`CNTR-2026-○○○○`）および日付は、法的紛争を防ぐため100%仮名およびマスキング（0000）処理されています。

---

### 過去5回のエピソードを通じて、私たちのチームは国家予算監査における巨大な技術的障壁を突破してきました。

1. **エピソード #1: 自然言語をSQL/GraphRAGクエリへ変換するプロトタイプ構築**
1. **エピソード #2: 400件以上の実証データと監査院判例マッチングエンジンの性能評価**
1. **エピソード #3: 400万件の調達市場から85%のノイズを除去する3次元標的分割（Sector Partition）**
1. **エピソード #4: DART企業開示・登記簿連動による名義貸しペーパーカンパニーカルテルの摘発**
1. **エピソード #5: 弱者優遇5千万ウォン分割（Sector 5）と12月年末予算ダンピング（Sector 6）の精密迎撃**

> 「監査官に必要なのは単なるPythonコードではありません。異常を即座に把握し、疑惑企業の支配構造を知識グラフで探索し、HWPX公文書をドラッグ＆ドロップして10カ年判例と対照された弁明要求書を出力する統合管制センターです。」

私たちは「監査官総合ウェブポータルv3.0」を完成させ、全モジュールを検証する「20の全数テストハーネス（20/20 PASS）」を構築しました。本稿ではその詳細を公開します。

---

### 1. 監査官総合ウェブポータルv3.0のアーキテクチャと7大ワークスペース

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

- **リアルタイム総合管制ダッシュボード (`/api/stats`, `/api/alerts`)**: 異常取引件数、高リスク緊急アラート、AI監査アシスタント対話。
- **6大標的セクター全数マトリクス (`/api/sectors`)**: Sector 1〜6の多次元フィルタリングおよび調達庁データ照会グリッド。
- **弁明要求書自動生成 (`/api/summons`)**: 違反条項と監査院判例要旨を引用した公式監査書式を即時レンダリング。
- **eナラドウ厶補助金不正受給追跡 (`/api/subsidy_fraud`)**: 重複受給、目的外私的流用、親族口座間接送金パターンの追跡。
- **入札談合・サクラカルテル可視化 (`/api/bidding_rings`, `/api/graph`)**: Vis.js物理グラフにより循環入札や役員兼任ネットワークを直感的に探索。
- **国会予算審査削減分析器 (`/api/budget_cuts`)**: 前年度不用率を追跡し国会予算決算委向けの削減勧告額を自動算出。
- **10カ年判例DB＆HWPXリアルタイムパーサー (`/api/precedents`, `/api/hwpx_analysis`)**: HWPX原本をドロップするだけで人件費水増しを即座に計算し類似判例5件をマッチング。

---

### 2. 設計時に事前予防した2大技術的課題

#### 📌 課題 1: 異種監査モジュールのモノリシック結合によるサーバーボトルネック
* GraphRAG、HWPXパース、ベクトル検索、DART照会は処理特性が異なります。単一プロセスで密結合させると、HWPXパースによりアラートAPIが10秒以上遅延する危険がありました。12の正規化RESTful DTOエンドポイントに分離し、エンジンを独立カプセル化することで他タブの稼働を完全保証しました。

#### 📌 課題 2: リアルタイムデータストリーミング時のDOM過負荷とメモリリーク
* 大量の異常検知ログを際限なくDOMへ追加するとブラウザメモリが1.5GBを超えクラッシュします。最大ノード数を100件に固定する「円形DOMリングバッファ」を導入し、超過した古いノードを即時破棄することでメモリを常時120MB以内に抑制しました。

---

### 3. 開発中に直面した3大突発エラーと現場トラブルシューティング

#### 🐛 突発エラー 1: Vis.js物理シミュレーションの無限振動とUIフリーズ
* ノードが50件を超えると反発力とバネ定数の計算が発散し無限振動が発生、ブラウザが完全停止しました。初期安定化回数を150回に制限し、`stabilizationIterationsDone`イベント検知時に物理演算を強制凍結（`physics: { enabled: false }`）することで解決しました。

```javascript
// Stabilization freeze pattern
network.on("stabilizationIterationsDone", function () {
    network.setOptions({ physics: { enabled: false } });
    console.log("[Portal] Vis.js physics stabilized and frozen.");
});
```

#### 🐛 突発エラー 2: 50ページ大容量HWPX XMLパースによるメインループブロック
* HWPX内の複数XML解凍とXPath走査がHTTPスレッドを8秒間占有し、他リクエストが504タイムアウトしました。ジョブUUIDを発行し`ThreadPoolExecutor`ワーカーキューへ非同期移譲、フロントエンドで進捗をポーリングする構造へ改修しました。

#### 🐛 突発エラー 3: 20テスト並列実行時のSQLiteファイルロック競合
* 20のテストを一括実行する際、`sqlite3.OperationalError: database is locked`が発生。テストごとにプロセスID（PID）付き一時DBファイルや`:memory:`インスタンスを割り当てる隔離プールを構築し、100%再現性のあるテスト実行を確立しました。

---

### 4. 20全数検証テスト結果サマリー (20/20 PASS)

プロトタイプからフロントエンドAPIまで、全20の検証ハーネスが完全合格（100% PASS）しました。

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

### 5. シリーズ完結に寄せて: AIエージェントと公共工学の未来

プロンプト調整にとどまらず、ドメイン特化の分割設計、DART知識グラフ、自動弁明書生成、Web統合ポータル、20の全数テストを統合することで、AIエージェントが国家財政を守る実用的な監視パートナーになり得ることを実証しました。ご愛読ありがとうございました！
