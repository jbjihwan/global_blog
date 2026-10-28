import os

base_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-11-23-national-budget-ai-inspector-portal-verification-system\i18n"

locales = {
    "ja": {
        "title": "[AI実践 #6] 監査官ウェブポータル構築と20全検証テスト通過記",
        "description": "国家予算AI監査シリーズ完結編。Vis.js知識グラフ、10カ年判例DB、HWPX即時パーサーを統合した監査官ウェブポータルv3.0の構築と20の検証テスト通過記。",
        "keywords": ["監査官ウェブポータル", "Vis.js知識グラフ", "HWPX文書パーサー", "20全テスト検証", "国家予算AI監査完結"],
        "key_takeaways_title": "重要ポイント (Key Takeaways)",
        "key_takeaways": [
            "**監査官総合ウェブポータルv3.0の完成**: CLIスクリプトだった調達異常検知を、7つの専用タブ（総合ダッシュボード、6大標的セクター、弁明要求書自動生成、eナラドウ厶補助金、入札談合グラフ、国会予算審査、判例DB＆HWPXパーサー）を備えたリアルタイム統合管制センターへ刷新。",
            "**20の全数検証テストハーネス100%通過 (20/20 PASS)**: プロトタイプSQL生成からGraphRAG、ストリーミング、DART法人登記追跡、入札カルテル、HWPX過大計上対照まで、全領域の統合検証テストを無欠点で通過。",
            "**設計時に予防した2大課題**: (1) 異種監査エンジンの結合ボトルネックを12のRESTful DTOエンドポイント分離で解決、(2) リアルタイムストリーミング時のDOM過負荷を円形リングバッファ（Circular DOM Ring Buffer）で防止。",
            "**開発中に解決した3大突発エラー**: (1) Vis.js物理演算の無限振動フリーズを安定化イベントによる強制凍結で解決、(2) 50ページのHWPX XMLパースによるメインループブロックをThreadPoolExecutor非同期キューで分離、(3) 並列テスト時のSQLiteファイルロック競合をプロセス別隔離メモリプールで解決。",
            "**全6部作シリーズの完結**: 単なるプロンプト調整を超え、国家財政保護という実務領域で高信頼性を実証したエンジニアリングの軌跡。"
        ],
        "legal_notice_title": "法的告知および匿名化について (Legal Notice & Anonymization)",
        "legal_notice": "本記事に記載されているすべての発注機関名（例: `A振興公団`、`B振興院`、`C公団`、`D区役所`）、受注企業名（例: `(株)○○IT`、`(株)○○コンサルティング`）、関係者名（例: `K氏`、`P氏`）、契約番号（`CNTR-2026-○○○○`）および日付は、法的紛争を防ぐため100%仮名およびマスキング（0000）処理されています。",
        "intro_p1": "過去5回のエピソードを通じて、私たちのチームは国家予算監査における巨大な技術的障壁を突破してきました。",
        "intro_list": [
            "エピソード #1: 自然言語をSQL/GraphRAGクエリへ変換するプロトタイプ構築",
            "エピソード #2: 400件以上の実証データと監査院判例マッチングエンジンの性能評価",
            "エピソード #3: 400万件の調達市場から85%のノイズを除去する3次元標的分割（Sector Partition）",
            "エピソード #4: DART企業開示・登記簿連動による名義貸しペーパーカンパニーカルテルの摘発",
            "エピソード #5: 弱者優遇5千万ウォン分割（Sector 5）と12月年末予算ダンピング（Sector 6）の精密迎撃"
        ],
        "intro_quote": "「監査官に必要なのは単なるPythonコードではありません。異常を即座に把握し、疑惑企業の支配構造を知識グラフで探索し、HWPX公文書をドラッグ＆ドロップして10カ年判例と対照された弁明要求書を出力する統合管制センターです。」",
        "intro_p2": "私たちは「監査官総合ウェブポータルv3.0」を完成させ、全モジュールを検証する「20の全数テストハーネス（20/20 PASS）」を構築しました。本稿ではその詳細を公開します。",
        "arch_title": "1. 監査官総合ウェブポータルv3.0のアーキテクチャと7大ワークスペース",
        "workspaces": [
            "**リアルタイム総合管制ダッシュボード (`/api/stats`, `/api/alerts`)**: 異常取引件数、高リスク緊急アラート、AI監査アシスタント対話。",
            "**6大標的セクター全数マトリクス (`/api/sectors`)**: Sector 1〜6の多次元フィルタリングおよび調達庁データ照会グリッド。",
            "**弁明要求書自動生成 (`/api/summons`)**: 違反条項と監査院判例要旨を引用した公式監査書式を即時レンダリング。",
            "**eナラドウ厶補助金不正受給追跡 (`/api/subsidy_fraud`)**: 重複受給、目的外私的流用、親族口座間接送金パターンの追跡。",
            "**入札談合・サクラカルテル可視化 (`/api/bidding_rings`, `/api/graph`)**: Vis.js物理グラフにより循環入札や役員兼任ネットワークを直感的に探索。",
            "**国会予算審査削減分析器 (`/api/budget_cuts`)**: 前年度不用率を追跡し国会予算決算委向けの削減勧告額を自動算出。",
            "**10カ年判例DB＆HWPXリアルタイムパーサー (`/api/precedents`, `/api/hwpx_analysis`)**: HWPX原本をドロップするだけで人件費水増しを即座に計算し類似判例5件をマッチング。"
        ],
        "challenges_title": "2. 設計時に事前予防した2大技術的課題",
        "ch1_title": "課題 1: 異種監査モジュールのモノリシック結合によるサーバーボトルネック",
        "ch1_desc": "GraphRAG、HWPXパース、ベクトル検索、DART照会は処理特性が異なります。単一プロセスで密結合させると、HWPXパースによりアラートAPIが10秒以上遅延する危険がありました。12の正規化RESTful DTOエンドポイントに分離し、エンジンを独立カプセル化することで他タブの稼働を完全保証しました。",
        "ch2_title": "課題 2: リアルタイムデータストリーミング時のDOM過負荷とメモリリーク",
        "ch2_desc": "大量の異常検知ログを際限なくDOMへ追加するとブラウザメモリが1.5GBを超えクラッシュします。最大ノード数を100件に固定する「円形DOMリングバッファ」を導入し、超過した古いノードを即時破棄することでメモリを常時120MB以内に抑制しました。",
        "bugs_title": "3. 開発中に直面した3大突発エラーと現場トラブルシューティング",
        "bug1_title": "突発エラー 1: Vis.js物理シミュレーションの無限振動とUIフリーズ",
        "bug1_desc": "ノードが50件を超えると反発力とバネ定数の計算が発散し無限振動が発生、ブラウザが完全停止しました。初期安定化回数を150回に制限し、`stabilizationIterationsDone`イベント検知時に物理演算を強制凍結（`physics: { enabled: false }`）することで解決しました。",
        "bug2_title": "突発エラー 2: 50ページ大容量HWPX XMLパースによるメインループブロック",
        "bug2_desc": "HWPX内の複数XML解凍とXPath走査がHTTPスレッドを8秒間占有し、他リクエストが504タイムアウトしました。ジョブUUIDを発行し`ThreadPoolExecutor`ワーカーキューへ非同期移譲、フロントエンドで進捗をポーリングする構造へ改修しました。",
        "bug3_title": "突発エラー 3: 20テスト並列実行時のSQLiteファイルロック競合",
        "bug3_desc": "20のテストを一括実行する際、`sqlite3.OperationalError: database is locked`が発生。テストごとにプロセスID（PID）付き一時DBファイルや`:memory:`インスタンスを割り当てる隔離プールを構築し、100%再現性のあるテスト実行を確立しました。",
        "test_title": "4. 20全数検証テスト結果サマリー (20/20 PASS)",
        "test_desc": "プロトタイプからフロントエンドAPIまで、全20の検証ハーネスが完全合格（100% PASS）しました。",
        "conclusion_title": "5. シリーズ完結に寄せて: AIエージェントと公共工学の未来",
        "conclusion_desc": "プロンプト調整にとどまらず、ドメイン特化の分割設計、DART知識グラフ、自動弁明書生成、Web統合ポータル、20の全数テストを統合することで、AIエージェントが国家財政を守る実用的な監視パートナーになり得ることを実証しました。ご愛読ありがとうございました！"
    },
    "zh-Hans": {
        "title": "[AI实战 #6] 审计员综合Web门户搭建与20项端到端测试全通",
        "description": "国家预算AI审计系列最终篇。整合Vis.js知识图谱、10年判例库与HWPX即时解析器的审计员门户v3.0构建，以及20项测试全通复盘。",
        "keywords": ["审计员Web门户", "Vis.js知识图谱", "HWPX公文解析器", "20项测试全量验证", "国家预算AI审计终章"],
        "key_takeaways_title": "核心摘要 (Key Takeaways)",
        "key_takeaways": [
            "**审计员综合Web门户v3.0落成**: 将分散的CLI脚本全面升级为具备7大专属工作区（综合大屏、6大标的区域、质询书自动生成、e国帮扶补助金、围标图谱、国会预算削减审查、判例库与HWPX解析）的实时统一管控中心。",
            "**20项全量验证测试100%通过 (20/20 PASS)**: 从原型SQL生成到GraphRAG、实时流监控、DART法人登记追踪、围标网络识别、HWPX虚高比对，全领域测试无瑕疵通过。",
            "**架构设计前瞻预防的两大瓶颈**: (1) 通过12个标准化RESTful DTO端点解耦异构审计引擎，(2) 引入环形DOM环状缓冲区（Circular DOM Ring Buffer）防止实时流导致前端内存溢出。",
            "**实际排查的三大突发故障**: (1) Vis.js物理引擎无限振荡导致UI卡死，改用稳定化事件即刻冻结解决；(2) 50页大体量HWPX XML解析阻塞主循环，引入ThreadPoolExecutor异步工作队列解决；(3) 20项测试批处理中SQLite文件锁冲突，构建进程隔离内存池彻底根除。",
            "**六部曲全景终章**: 超越简单的Prompt Engineering，在公共财政安全这一高精尖实务领域验证生产级AI工程体系。"
        ],
        "legal_notice_title": "法律声明与匿名化说明 (Legal Notice & Anonymization)",
        "legal_notice": "为避免法律纠纷，本文涉及的所有招标机关（如`A振兴公团`、`B振兴院`、`C公团`、`D区政府`）、承包企业（如`○○信息科技(株)`、`○○咨询(株)`）、涉案人员（如`K某`、`P某`）、合同编号（`CNTR-2026-○○○○`）及具体日期均已进行100%化名及掩码（0000）处理。",
        "intro_p1": "回顾前5篇系列文章，我们的工程团队逐步攻克了国家预算AI审计的核心难关：",
        "intro_list": [
            "第1篇: 自然语言转精确SQL与GraphRAG检索原型",
            "第2篇: 400余项实证数据检验与审计院判例语义匹配评估",
            "第3篇: 从400万件采购市场剔除85%噪声的三维标的分区引擎",
            "第4篇: 联动DART企业公示与登记簿揪出借名空壳公司卡特尔",
            "第5篇: 精准打击弱势企业5千万韩元拆单(Sector 5)与12月年底突击花钱(Sector 6)"
        ],
        "intro_quote": "“一线审计官需要的不是分散的Python脚本，而是一个能实时捕获异常、用知识图谱下钻股权脉络、拖入公文即可一键生成对照10年判例质询书的统一作战中心。”",
        "intro_p2": "为此，我们打造了“审计员综合Web门户v3.0”，并建立了全覆盖的“20项端到端自动化测试套件(20/20 PASS)”。本终章将全面揭秘其架构与填坑实录。",
        "arch_title": "1. 审计员综合Web门户v3.0架构与7大工作区",
        "workspaces": [
            "**实时综合监控大屏 (`/api/stats`, `/api/alerts`)**: 实时异常计数、高危紧急警报(Flash Alert)与内置AI对话助手。",
            "**6大标的区域全景矩阵 (`/api/sectors`)**: 针对Sector 1~6的多维筛选及采购总账实时核验表格。",
            "**自动化质询要求书生成 (`/api/summons`)**: 自动援引违规法条与审计院裁定要旨，一键排版标准审计行政格式质询书。",
            "**e国帮扶财政补助金反诈追查 (`/api/subsidy_fraud`)**: 重复领取、挪作私用及直系亲属账户间接输送追踪。",
            "**围标陪标网络图谱 (`/api/bidding_rings`, `/api/graph`)**: Vis.js动态力导向图呈现轮流坐庄与高管兼职网络。",
            "**国会预算审查削减分析器 (`/api/budget_cuts`)**: 依据历史结余不用率自动推导预算下调建议方案。",
            "**10年判例库与HWPX即时解析器 (`/api/precedents`, `/api/hwpx_analysis`)**: 拖拽公文即刻核算人工虚报并推荐5条高相关判例。"
        ],
        "challenges_title": "2. 架构设计中预见并防范的两大技术瓶颈",
        "ch1_title": "课题 1: 异构审计引擎单体耦合引发的服务器阻塞与雪崩",
        "ch1_desc": "GraphRAG、HWPX二进制解析、向量检索与DART接口开销迥异。若混入单进程，耗时的HWPX任务将卡死预警分发。我们通过12个规范化RESTful DTO端点完成隔离，单模块偶发异常不影响其他6大工作区正常运行。",
        "ch2_title": "课题 2: 实时数据流监控中的前端DOM超载与内存泄露",
        "ch2_desc": "实时日志持续追加极易导致浏览器内存攀升至1.5GB以上引发崩溃。我们实现了仅保留最新100条节点的环形DOM环状缓冲算法，超额节点立即剥离释放，内存常年恒定在120MB以内。",
        "bugs_title": "3. 实际落地过程中排查的三大突发故障",
        "bug1_title": "故障 1: Vis.js物理引擎无限振荡导致前端UI锁死",
        "bug1_desc": "当节点超过50个时，斥力与弹簧力计算发散产生剧烈振荡，主线程100%卡死。通过将稳定迭代限制为150次，并在`stabilizationIterationsDone`事件触发后立即调用`network.setOptions({ physics: { enabled: false } })`强行冻结，彻底平复卡顿。",
        "bug2_title": "故障 2: 50页大体量HWPX XML解析阻塞主事件循环",
        "bug2_desc": "解压XML和XPath遍历同步占用HTTP线程达8秒，导致并发请求504网关超时。改造成签发Job UUID并将解析派发至ThreadPoolExecutor异步线程池，前端轮询进度，其他API响应时间压回15ms内。",
        "bug3_title": "故障 3: 20项自动化测试批处理并发时的SQLite文件锁冲突",
        "bug3_desc": "批量运行测试时频繁抛出`sqlite3.OperationalError: database is locked`。引入测试隔离池，为每个测试分配带PID的临时文件或纯内存数据库`:memory:`，保证测试100%独立无干扰通过。",
        "test_title": "4. 20项端到端自动化测试全景汇总 (20/20 PASS)",
        "test_desc": "20项检验脚本覆盖从数据清洗到前端展示的全链路，全部取得PASS评级。",
        "conclusion_title": "5. 结语：AI智能体在公共工程领域的未来",
        "conclusion_desc": "通过结合领域知识的分区策略、DART图谱关联、标准公文自动化生成与完备的自动化测试体系，AI智能体得以真正扎根公共财政实务。感谢读者对本系列的关注与支持！"
    },
    "zh-Hant": {
        "title": "[AI實戰 #6] 審計員綜合Web門戶構建與20項測試全數通關",
        "description": "國家預算AI審計系列最終章。整合Vis.js知識圖譜、10年判例庫與HWPX即時解析器的審計門戶v3.0構建，以及20項測試全通復盤。",
        "keywords": ["審計員Web門戶", "Vis.js知識圖譜", "HWPX公文解析器", "20項測試全量驗證", "國家預算AI審計終章"],
        "key_takeaways_title": "核心摘要 (Key Takeaways)",
        "key_takeaways": [
            "**審計員綜合Web門戶v3.0落成**: 將分散的CLI腳本全面升級為具備7大專屬工作區的實時統一管控中心。",
            "**20項全量驗證測試100%通過 (20/20 PASS)**: 從原型SQL生成到GraphRAG、實時流監控、DART法人登記追蹤、圍標網絡識別、HWPX虛高比對，全領域測試無瑕疵通過。",
            "**架構設計前瞻預防的兩大瓶頸**: (1) 透過12個標準化RESTful DTO端點解耦異構審計引擎，(2) 引入環形DOM環狀緩衝區防止實時流導致前端內存溢出。",
            "**實際排查的三大突發故障**: (1) Vis.js物理引擎無限振盪導致UI卡死，改用穩定化事件即刻凍結解決；(2) 50頁大體量HWPX XML解析阻塞主循環，引入ThreadPoolExecutor異步工作隊列解決；(3) 20項測試批處理中SQLite文件鎖衝突，構建進程隔離內存池徹底根除。",
            "**六部曲全景終章**: 超越簡單的Prompt Engineering，在公共財政安全這一高精尖實務領域驗證生產級AI工程體系。"
        ],
        "legal_notice_title": "法律聲明與匿名化說明 (Legal Notice & Anonymization)",
        "legal_notice": "為避免法律糾紛，本文涉及的所有招標機關（如`A振興公團`、`B振興院`、`C公團`、`D區政府`）、承包企業（如`○○資訊科技(株)`、`○○顧問(株)`）、涉案人員（如`K某`、`P某`）、合約編號（`CNTR-2026-○○○○`）及具體日期均已進行100%化名及掩碼（0000）處理。",
        "intro_p1": "回顧前5篇系列文章，我們的工程團隊逐步攻克了國家預算AI審計的核心難關：",
        "intro_list": [
            "第1篇: 自然語言轉精確SQL與GraphRAG檢索原型",
            "第2篇: 400餘項實證數據檢驗與審計院判例語義匹配評估",
            "第3篇: 從400萬件採購市場剔除85%雜訊的三維標的分區引擎",
            "第4篇: 聯動DART企業公示與登記簿揪出借名空殼公司卡特爾",
            "第5篇: 精準打擊弱勢企業5千萬韓元拆單(Sector 5)與12月年底突擊花錢(Sector 6)"
        ],
        "intro_quote": "「一線審計官需要的不是分散的Python腳本，而是一個能實時捕獲異常、用知識圖譜下鑽股權脈絡、拖入公文即可一鍵生成對照10年判例質詢書的統一作戰中心。」",
        "intro_p2": "為此，我們打造了「審計員綜合Web門戶v3.0」，並建立了全覆蓋的「20項端到端自動化測試套件(20/20 PASS)」。本終章將全面揭秘其架構與填坑實錄。",
        "arch_title": "1. 審計員綜合Web門戶v3.0架構與7大工作區",
        "workspaces": [
            "**實時綜合監控大屏 (`/api/stats`, `/api/alerts`)**: 實時異常計數、高危緊急警報與內建AI對話助手。",
            "**6大標的區域全景矩陣 (`/api/sectors`)**: 針對Sector 1~6的多維篩選及採購總帳實時核驗表格。",
            "**自動化質詢要求書生成 (`/api/summons`)**: 自動援引違規法條與審計院裁定要旨，一鍵排版標準審計行政格式質詢書。",
            "**e國幫扶財政補助金反詐追查 (`/api/subsidy_fraud`)**: 重複領取、挪作私用及直系親屬帳戶間接輸送追蹤。",
            "**圍標陪標網絡圖譜 (`/api/bidding_rings`, `/api/graph`)**: Vis.js動態力導向圖呈現輪流坐莊與高管兼職網絡。",
            "**國會預算審查削減分析器 (`/api/budget_cuts`)**: 依據歷史結餘不用率自動推導預算下調建議方案。",
            "**10年判例庫與HWPX即時解析器 (`/api/precedents`, `/api/hwpx_analysis`)**: 拖曳公文即刻核算人工虛報並推薦5條高相關判例。"
        ],
        "challenges_title": "2. 架構設計中預見並防範的兩大技術瓶頸",
        "ch1_title": "課題 1: 異構審計引擎單體耦合引發的伺服器阻塞與雪崩",
        "ch1_desc": "GraphRAG、HWPX二進制解析、向量檢索與DART接口開銷迥異。若混入單進程，耗時的HWPX任務將卡死預警分發。我們透過12個規範化RESTful DTO端點完成隔離，單模組偶發異常不影響其他6大工作區正常運行。",
        "ch2_title": "課題 2: 實時數據流監控中的前端DOM超載與記憶體洩漏",
        "ch2_desc": "實時日誌持續追加極易導致瀏覽器記憶體攀升至1.5GB以上引發崩潰。我們實現了僅保留最新100條節點的環形DOM環狀緩衝演算法，超額節點立即剝離釋放，記憶體常年恆定在120MB以內。",
        "bugs_title": "3. 實際落地過程中排查的三大突發故障",
        "bug1_title": "故障 1: Vis.js物理引擎無限振盪導致前端UI鎖死",
        "bug1_desc": "當節點超過50個時，斥力與彈簧力計算發散產生劇烈振盪，主執行緒100%卡死。透過將穩定迭代限制為150次，並在`stabilizationIterationsDone`事件觸發後立即調用`network.setOptions({ physics: { enabled: false } })`強行凍結，徹底平復卡頓。",
        "bug2_title": "故障 2: 50頁大體量HWPX XML解析阻塞主事件循環",
        "bug2_desc": "解壓XML和XPath遍歷同步佔用HTTP執行緒達8秒，導致並發請求504閘道逾時。改造成簽發Job UUID並將解析派發至ThreadPoolExecutor異步執行緒池，前端輪詢進度，其他API響應時間壓回15ms內。",
        "bug3_title": "故障 3: 20項自動化測試批處理並發時的SQLite檔案鎖衝突",
        "bug3_desc": "批量運行測試時頻繁拋出`sqlite3.OperationalError: database is locked`。引入測試隔離池，為每個測試分配帶PID的臨時檔案或純記憶體資料庫`:memory:`，保證測試100%獨立無干擾通過。",
        "test_title": "4. 20項端到端自動化測試全景彙總 (20/20 PASS)",
        "test_desc": "20項檢驗腳本覆蓋從數據清洗到前端展示的全鏈路，全部取得PASS評級。",
        "conclusion_title": "5. 結語：AI智能體在公共工程領域的未來",
        "conclusion_desc": "透過結合領域知識的分區策略、DART圖譜關聯、標準公文自動化生成與完備的自動化測試體系，AI智能體得以真正扎根公共財政實務。感謝讀者對本系列的關注與支持！"
    },
    "es": {
        "title": "IA de Presupuesto #6: Portal Web de Auditoría y 20 Tests",
        "description": "Episodio final: Portal Web de Auditoría v3.0 con grafos Vis.js, búsqueda de precedentes de 10 años, analizador HWPX y superación de 20 tests de verificación.",
        "keywords": ["Portal Web de Auditoría", "Grafos Vis.js", "Parser HWPX", "Verificación 20 tests", "IA presupuestaria final"],
        "key_takeaways_title": "Puntos Clave (Key Takeaways)",
        "key_takeaways": [
            "**Inspector Web Portal v3.0 Construido**: Evolución de scripts CLI a una estación centralizada con 7 pestañas dedicadas (Panel General, 6 Sectores Objetivo, Redactor de Requerimientos, Subsidios, Grafos de Carteles, Análisis de Cortes y Precedentes con Parser HWPX).",
            "**20 Tests Automatizados Aprobados al 100% (20/20 PASS)**: Superación impecable en toda la suite, desde Text-to-SQL y GraphRAG hasta streaming, carteles DART y validación de sobrecostos HWPX.",
            "**2 Desafíos Prevenidos en Diseño**: (1) Cuello de botella en servidor resuelto mediante desacoplamiento en 12 endpoints RESTful DTO, (2) Saturación de memoria DOM mitigada con búfer circular (Circular DOM Ring Buffer).",
            "**3 Errores Inesperados en Producción**: (1) Congelación de Vis.js resuelta congelando la física tras estabilización, (2) Bloqueo del bucle de eventos por parsing HWPX resuelto con ThreadPoolExecutor, (3) Bloqueo de archivos SQLite resuelto con aislamiento en memoria por proceso.",
            "**Gran Final de la Serie de 6 Episodios**: Demostración de fiabilidad de nivel de producción en la protección fiscal pública."
        ],
        "legal_notice_title": "Aviso Legal y Anonimización (Legal Notice & Anonymization)",
        "legal_notice": "Todos los nombres de organismos (`Agencia A`, `Corporación C`), empresas (`Alfa IT`, `Beta Consultoría`), personas (`Sr. K`, `Sra. P`) y números de contrato (`CNTR-2026-○○○○`) han sido anonimizados al 100% para evitar disputas legales.",
        "intro_p1": "A lo largo de los 5 episodios anteriores, nuestro equipo superó desafíos monumentales en la auditoría fiscal:",
        "intro_list": [
            "Episodio #1: Prototipo Text-to-SQL y GraphRAG.",
            "Episodio #2: Evaluación de más de 400 casos frente a 10 años de jurisprudencia.",
            "Episodio #3: Partición en 3D que elimina el 85% del ruido en 4 millones de compras.",
            "Episodio #4: Detección de carteles de empresas fantasma con DART.",
            "Episodio #5: Desmantelamiento de fraccionamientos de $40K (Sector 5) y vertido de fin de año (Sector 6)."
        ],
        "intro_quote": "\"Los auditores necesitan una consola unificada donde ver anomalías en tiempo real, explorar redes corporativas y generar requerimientos legales con un solo clic.\"",
        "intro_p2": "Presentamos el Inspector Web Portal v3.0 y la verificación completa de los 20 tests automatizados.",
        "arch_title": "1. Arquitectura de Inspector Web Portal v3.0 y 7 Espacios de Trabajo",
        "workspaces": [
            "**Centro de Mando Ejecutivo (`/api/stats`, `/api/alerts`)**: Métricas y asistente AI.",
            "**Matriz de 6 Sectores (`/api/sectors`)**: Filtrado multidimensional en tiempo real.",
            "**Generador de Requerimientos (`/api/summons`)**: Redacción automática de actas legales.",
            "**Rastreador de Subsidios (`/api/subsidy_fraud`)**: Fraudes en subvenciones públicas.",
            "**Grafo de Carteles Vis.js (`/api/bidding_rings`, `/api/graph`)**: Redes de colusión interactiva.",
            "**Analizador de Recortes Presupuestarios (`/api/budget_cuts`)**: Recomendaciones parlamentarias.",
            "**Base de Precedentes y Parser HWPX (`/api/precedents`, `/api/hwpx_analysis`)**: Detección de sobrecostos."
        ],
        "challenges_title": "2. Dos Desafíos Anticipados y Prevenidos",
        "ch1_title": "Desafío 1: Cuellos de botella por acoplamiento monolítico de motores de auditoría",
        "ch1_desc": "Desacoplamos la capa web mediante 12 endpoints DTO normalizados, aislando fallos de servicios pesados.",
        "ch2_title": "Desafío 2: Saturación del DOM y fugas de memoria en streaming en vivo",
        "ch2_desc": "Implementamos un búfer circular de 100 nodos, manteniendo la memoria del navegador bajo 120MB.",
        "bugs_title": "3. Tres Errores Inesperados en Producción y su Solución",
        "bug1_title": "Error 1: Oscilación infinita en Vis.js y bloqueo del navegador",
        "bug1_desc": "Al superar 50 nodos, las fuerzas divergieron. Lo solucionamos congelando la física al recibir `stabilizationIterationsDone`.",
        "bug2_title": "Error 2: Bloqueo del servidor HTTP al analizar HWPX de 50 páginas",
        "bug2_desc": "Delegamos la descompresión y análisis XML a un ThreadPoolExecutor en segundo plano.",
        "bug3_title": "Error 3: Bloqueo de base de datos SQLite en 20 tests paralelos",
        "bug3_desc": "Creamos un pool de aislamiento con bases de datos temporales vinculadas al PID del proceso.",
        "test_title": "4. Resumen de Verificación: 20/20 Tests Aprobados",
        "test_desc": "Toda la suite pasó con éxito, garantizando solidez de punta a punta.",
        "conclusion_title": "5. Conclusión: El Futuro de la Auditoría Pública con Agentes IA",
        "conclusion_desc": "Demostramos que uniendo conocimiento de dominio, grafos y pruebas automatizadas, los agentes IA son guardianes fiables de las finanzas públicas."
    },
    "de": {
        "title": "KI-Haushaltsprüfung #6: Webportal & 20/20 Testsuite",
        "description": "Das Finale: Auditor-Webportal v3.0 mit Vis.js-Wissensgraphen, 10-Jahre-Urteils-DB, HWPX-Parser und 100% bestandenen 20 End-to-End-Verifikationstests.",
        "keywords": ["Prüfer-Webportal", "Vis.js-Wissensgraph", "HWPX-Dokumentenparser", "20 Verifikationstests", "KI-Haushaltsprüfung Finale"],
        "key_takeaways_title": "Wichtigste Erkenntnisse (Key Takeaways)",
        "key_takeaways": [
            "**Auditor-Webportal v3.0 Fertiggestellt**: Umwandlung einzelner CLI-Skripte in eine Echtzeit-Kommandozentrale mit 7 Reitern (Übersicht, 6 Sektoren, Vorladungsgenerator, Subventionen, Kartellgraphen, Haushaltskürzung und Urteils-DB mit HWPX-Parser).",
            "**100% Bestehensquote in 20 automatisierten Tests (20/20 PASS)**: Lückenlose Validierung von Text-to-SQL über GraphRAG bis hin zu DART-Registern und HWPX-Preispunkten.",
            "**2 Vorbeugende Entwurfsentscheidungen**: (1) Entkopplung heterogener Module über 12 normalisierte RESTful-DTO-Endpunkte, (2) Begrenzung des DOM-Speicherverbrauchs via zirkulärem Puffer (Circular DOM Ring Buffer).",
            "**3 Unerwartete Fehler in der Praxis behoben**: (1) Einfrieren von Vis.js durch sofortiges Einfrieren der Physik nach Stabilisierung behoben, (2) Blockierung des Event-Loops bei 50-seitigen HWPX-Dateien durch ThreadPoolExecutor gelöst, (3) SQLite-Dateisperren bei parallelen Tests durch prozessisolierte Datenbanken eliminiert.",
            "**Großes Finale der 6-teiligen Serie**: Nachweis produktionsreifer Zuverlässigkeit im öffentlichen Finanzwesen."
        ],
        "legal_notice_title": "Rechtlicher Hinweis und Anonymisierung (Legal Notice & Anonymization)",
        "legal_notice": "Alle Behörden (`Behörde A`), Unternehmen (`Alpha IT`, `Beta Consulting`), Personen (`Herr K`, `Frau P`) und Vertragsnummern (`CNTR-2026-○○○○`) wurden zum Schutz vor rechtlichen Streitigkeiten zu 100% anonymisiert.",
        "intro_p1": "In den letzten 5 Episoden haben wir zentrale Herausforderungen der Haushaltsprüfung gelöst:",
        "intro_list": [
            "Episode #1: Text-to-SQL & GraphRAG Baseline.",
            "Episode #2: 400+ Testfälle im Abgleich mit 10 Jahren Rechtsprechung.",
            "Episode #3: 3D-Sektorpartitionierung filtert 85% Hintergrundrauschen.",
            "Episode #4: Aufdeckung von Strohmann-Kartellen via DART-Register.",
            "Episode #5: Gezielte Bekämpfung von 50-Mio.-Splittings (Sektor 5) und Jahresend-Dumping (Sektor 6)."
        ],
        "intro_quote": "„Prüfer brauchen eine integrierte Konsole, auf der Alarme in Echtzeit aufleuchten, Netzwerke interaktiv erkundet und rechtssichere Vorladungen mit einem Klick erzeugt werden.“",
        "intro_p2": "Wir präsentieren das Auditor-Webportal v3.0 und die vollständige Validierung über 20 Test-Harnische.",
        "arch_title": "1. Architektur des Webportals v3.0 und 7 Arbeitsbereiche",
        "workspaces": [
            "**Leitstand & KI-Chat (`/api/stats`, `/api/alerts`)**: Echtzeit-Alarme und dialogorientierter KI-Prüfungsassistent.",
            "**6-Sektoren-Matrix (`/api/sectors`)**: Mehrdimensionale Filterung im Beschaffungsregister.",
            "**Vorladungs-Synthesizer (`/api/summons`)**: Automatisierte Erstellung formeller Prüfungsberichte.",
            "**Subventionsbetrugs-Tracker (`/api/subsidy_fraud`)**: Erkennung von Fördermittelmissbrauch.",
            "**Kartell-Wissensgraph (`/api/bidding_rings`, `/api/graph`)**: Interaktive Erkennung von Absprachen.",
            "**Haushaltskürzungsempfehlungen (`/api/budget_cuts`)**: Vorbereitung für den Haushaltsausschuss.",
            "**10-Jahre-Rechtsprechung & HWPX-Parser (`/api/precedents`, `/api/hwpx_analysis`)**: Sofortige Kostenprüfung."
        ],
        "challenges_title": "2. Vorbeugend Gelöste Herausforderungen",
        "ch1_title": "Herausforderung 1: Server-Engpässe durch monolithische Kopplung",
        "ch1_desc": "Trennung der Präsentationsschicht von schweren Engines über 12 DTO-Endpunkte mit Caching.",
        "ch2_title": "Herausforderung 2: DOM-Überlastung bei Echtzeit-Datenströmen",
        "ch2_desc": "Ein zirkulärer Ringpuffer begrenzt die Tabellenzeilen auf 100 und hält den RAM unter 120MB.",
        "bugs_title": "3. Drei Unerwartete Praxisfehler und deren Behebung",
        "bug1_title": "Fehler 1: Vis.js-Schwingungen und Browser-Einfrieren",
        "bug1_desc": "Ab 50 Knoten divergierte die Physik. Gelöst durch `physics: { enabled: false }` nach Stabilisierung.",
        "bug2_title": "Fehler 2: HWPX-Parsing blockiert HTTP-Hauptthread",
        "bug2_desc": "Auslagerung der XML-Dekodierung in einen ThreadPoolExecutor mit asynchronem Polling.",
        "bug3_title": "Fehler 3: SQLite-Dateisperre bei parallelen Tests",
        "bug3_desc": "Einführung isolierter PID-basierter Datenbanken und `:memory:`-Instanzen.",
        "test_title": "4. Verifikationsbericht: 20/20 Tests Bestanden",
        "test_desc": "Alle 20 Tests liefen fehlerfrei durch und bestätigen die Systemstabilität.",
        "conclusion_title": "5. Fazit: Die Zukunft autonomer Prüfungs-KI",
        "conclusion_desc": "Die Kombination aus Domänenpartitionierung, Wissensgraphen und solider Softwaretechnik macht KI-Agenten zu verlässlichen Hütern öffentlicher Gelder."
    },
    "fr": {
        "title": "IA Budgétaire #6: Portail Web d'Audit et 20 Tests Réussis",
        "description": "Le grand final: Portail Web d'Audit v3.0 intégrant graphes Vis.js, jurisprudence de 10 ans, parseur HWPX et validation à 100% des 20 tests de vérification.",
        "keywords": ["Portail Web d'Audit", "Graphes Vis.js", "Parseur HWPX", "Vérification 20 tests", "IA budgétaire finale"],
        "key_takeaways_title": "Points Clés (Key Takeaways)",
        "key_takeaways": [
            "**Portail Web d'Audit v3.0 Achevé**: Remplacement des scripts CLI par une console intégrée à 7 onglets (Vue d'ensemble, 6 Secteurs, Générateur de convocations, Subventions, Graphe d'ententes, Analyse budgétaire et Jurisprudence avec parseur HWPX).",
            "**100% de Réussite sur 20 Tests Automatisés (20/20 PASS)**: Validation complète couvrant Text-to-SQL, GraphRAG, streaming temps réel, cartels DART et surfacturations HWPX.",
            "**2 Défis Anticipés et Prévenus**: (1) Goulots d'étranglement évités par découplage en 12 points de terminaison RESTful DTO, (2) Saturation du DOM évitée par un tampon circulaire (Circular DOM Ring Buffer).",
            "**3 Bogues Inattendus Résolus**: (1) Oscillation infinie de Vis.js résolue en figeant la physique après stabilisation, (2) Blocage du thread HTTP par HWPX résolu avec ThreadPoolExecutor, (3) Verrous de fichiers SQLite résolus par isolation en mémoire par processus.",
            "**Apothéose de la Série en 6 Épisodes**: Démonstration d'une fiabilité éprouvée au service des finances publiques."
        ],
        "legal_notice_title": "Avis Juridique et Anonymisation (Legal Notice & Anonymization)",
        "legal_notice": "Toutes les institutions publiques (`Organisme A`), entreprises (`Alpha IT`), personnes (`M. K`) et références de marchés (`CNTR-2026-○○○○`) sont rigoureusement pseudonymisées.",
        "intro_p1": "Au cours des 5 épisodes précédents, nous avons franchi des étapes cruciales :",
        "intro_list": [
            "Épisode #1: Prototype Text-to-SQL et GraphRAG.",
            "Épisode #2: Évaluation sur 400 dossiers face à 10 ans de jurisprudence.",
            "Épisode #3: Partition 3D éliminant 85% du bruit sur 4 millions d'achats.",
            "Épisode #4: Révélation des cartels de prête-noms avec les registres DART.",
            "Épisode #5: Démantèlement des fractionnements à 50M (Secteur 5) et du dumping de fin d'année (Secteur 6)."
        ],
        "intro_quote": "« Les auditeurs ont besoin d'un centre opérationnel où les alertes s'affichent en temps réel, où les cartels s'explorent en graphes et où un dossier HWPX produit instantanément une convocation motivée. »",
        "intro_p2": "Voici le Portail Web d'Audit v3.0 et la validation exhaustive de ses 20 bancs d'essai.",
        "arch_title": "1. Architecture du Portail Web v3.0 et 7 Espaces Dédiés",
        "workspaces": [
            "**Centre de Contrôle & Chat IA (`/api/stats`, `/api/alerts`)**: Métriques temps réel et assistant conversationnel.",
            "**Matrice des 6 Secteurs (`/api/sectors`)**: Filtrage multicritère sur les marchés publics.",
            "**Générateur de Convocations (`/api/summons`)**: Rédaction automatisée avec visa légal.",
            "**Traçage des Subventions (`/api/subsidy_fraud`)**: Détection des détournements d'aides publiques.",
            "**Graphe Vis.js des Cartels (`/api/bidding_rings`, `/api/graph`)**: Cartographie interactive des ententes.",
            "**Analyseur de Coupes Budgétaires (`/api/budget_cuts`)**: Recommandations pour la commission des finances.",
            "**Jurisprudence & Parseur HWPX (`/api/precedents`, `/api/hwpx_analysis`)**: Détection des surcoûts."
        ],
        "challenges_title": "2. Deux Défis Anticipés et Prévenus",
        "ch1_title": "Défi 1: Engorgement du serveur par couplage monolithique des moteurs",
        "ch1_desc": "Découplage de la couche HTTP via 12 points d'accès DTO normalisés assurant la continuité de service.",
        "ch2_title": "Défi 2: Explosion de la mémoire du navigateur lors du streaming continu",
        "ch2_desc": "Mise en place d'un tampon circulaire borné à 100 entrées, maintenant la mémoire sous 120 Mo.",
        "bugs_title": "3. Trois Bogues de Production et leurs Solutions",
        "bug1_title": "Bogue 1: Oscillation infinie Vis.js et gel du navigateur",
        "bug1_desc": "Au-delà de 50 nœuds, les forces divergeaient. Résolu en désactivant la physique dès `stabilizationIterationsDone`.",
        "bug2_title": "Bogue 2: Analyse HWPX de 50 pages bloquant la boucle HTTP",
        "bug2_desc": "Délégation du traitement XML lourd à un ThreadPoolExecutor en arrière-plan avec suivi asynchrone.",
        "bug3_title": "Bogue 3: Conflit de verrou SQLite lors des tests parallèles",
        "bug3_desc": "Instanciation de bases isolées par identifiant de processus (PID) et en mémoire pure `:memory:`.",
        "test_title": "4. Bilan des Tests: 20/20 Réussites",
        "test_desc": "L'intégralité des 20 bancs d'essai s'est conclue par un statut PASS.",
        "conclusion_title": "5. Conclusion: L'Avenir de l'Ingénierie d'Audit Autonome",
        "conclusion_desc": "En associant vision métier, graphes de connaissances et rigueur logicielle, les agents IA deviennent de véritables remparts pour les deniers publics."
    },
    "pt-BR": {
        "title": "IA Orçamentária #6: Portal Web de Auditoria e 20 Testes",
        "description": "O final: Portal Web de Auditoria v3.0 com grafos Vis.js, base de 10 anos de precedentes, parser HWPX e aprovação total nos 20 testes de verificação.",
        "keywords": ["Portal Web de Auditoria", "Grafos Vis.js", "Parser HWPX", "Verificação 20 testes", "IA orçamentária final"],
        "key_takeaways_title": "Destaques Principais (Key Takeaways)",
        "key_takeaways": [
            "**Portal Web de Auditoria v3.0 Concluído**: Transição de scripts CLI para uma estação central com 7 abas (Visão Geral, 6 Setores Alvo, Intimações, Fraudes em Subsídios, Grafos de Cartéis, Cortes Orçamentários e Jurisprudência com Parser HWPX).",
            "**100% de Aprovação em 20 Testes Automatizados (20/20 PASS)**: Validação completa desde Text-to-SQL até detecção de laranjas e superfaturamento HWPX.",
            "**2 Desafios Prevenidos no Design**: (1) Gargalos de servidor eliminados pelo desacoplamento em 12 endpoints RESTful DTO, (2) Sobrecarga do DOM em streaming evitada via buffer circular (Circular DOM Ring Buffer).",
            "**3 Erros Inesperados em Produção**: (1) Travamento de Vis.js corrigido congelando a física após estabilização, (2) Bloqueio do loop HTTP por HWPX resolvido com ThreadPoolExecutor, (3) Conflitos de bloqueio SQLite eliminados com bancos isolados por processo.",
            "**Grande Final da Série de 6 Artigos**: Demonstração de robustez e confiabilidade de nível corporativo na proteção fiscal."
        ],
        "legal_notice_title": "Aviso Legal e Anonimização (Legal Notice & Anonymization)",
        "legal_notice": "Todas as agências (`Agência A`), empresas (`Alfa TI`), nomes de pessoas (`Sr. K`) e números de contratos (`CNTR-2026-○○○○`) foram 100% anonimizados.",
        "intro_p1": "Nos últimos 5 episódios, superamos marcos técnicos desafiadores:",
        "intro_list": [
            "Episódio #1: Linha de base com Text-to-SQL e GraphRAG.",
            "Episódio #2: Avaliação de mais de 400 casos frente a 10 anos de jurisprudência.",
            "Episódio #3: Particionamento 3D eliminando 85% do ruído em 4 milhões de contratos.",
            "Episódio #4: Desmascaramento de cartéis de fachada com a base DART.",
            "Episódio #5: Combate ao fracionamento de 50M (Setor 5) e desovas de fim de ano (Setor 6)."
        ],
        "intro_quote": "\"Auditores precisam de um centro unificado onde anomalias brilhem em tempo real, cartéis sejam visíveis em grafos e um documento HWPX gere intimações com precedentes com um clique.\"",
        "intro_p2": "Apresentamos o Portal Web de Auditoria v3.0 e a validação completa de 20 suites de testes.",
        "arch_title": "1. Arquitetura do Portal Web v3.0 e 7 Áreas de Trabalho",
        "workspaces": [
            "**Centro de Comando & Chat IA (`/api/stats`, `/api/alerts`)**: Métricas e assistente conversacional.",
            "**Matriz dos 6 Setores (`/api/sectors`)**: Filtragem em grade no diário de compras.",
            "**Sintetizador de Intimações (`/api/summons`)**: Redação automatizada com citação legal.",
            "**Rastreador de Subsídios (`/api/subsidy_fraud`)**: Detecção de desvios e repasses indiretos.",
            "**Grafo de Cartéis Vis.js (`/api/bidding_rings`, `/api/graph`)**: Exploração de conluios e sobreposições.",
            "**Analisador de Cortes Orçamentários (`/api/budget_cuts`)**: Recomendações para o comitê orçamentário.",
            "**Jurisprudência de 10 Anos & Parser HWPX (`/api/precedents`, `/api/hwpx_analysis`)**: Cálculo de sobrecustos."
        ],
        "challenges_title": "2. Dois Desafios Antecipados e Prevenidos",
        "ch1_title": "Desafio 1: Gargalos de servidor pelo acoplamento monolítico",
        "ch1_desc": "Desacoplamento em 12 endpoints DTO normalizados mantendo a operação das demais abas.",
        "ch2_title": "Desafío 2: Sobrecarga do DOM e vazamento de memória em streaming",
        "ch2_desc": "Implementação de buffer circular limitando em 100 linhas e fixando o consumo sob 120MB.",
        "bugs_title": "3. Três Erros Inesperados em Produção e Soluções",
        "bug1_title": "Erro 1: Oscilação infinita no Vis.js e travamento do navegador",
        "bug1_desc": "Acima de 50 nós, as forças divergiram. Corrigido desligando a física no evento `stabilizationIterationsDone`.",
        "bug2_title": "Erro 2: Processamento de HWPX de 50 páginas bloqueando o loop HTTP",
        "bug2_desc": "Envio do parsing XML a um ThreadPoolExecutor assíncrono com polling de progresso.",
        "bug3_title": "Erro 3: Conflito de arquivo SQLite durante testes paralelos",
        "bug3_desc": "Criação de pool isolado com bancos temporários por PID e instâncias `:memory:`.",
        "test_title": "4. Resumo da Verificação: 20/20 Testes Aprovados",
        "test_desc": "Todos os 20 testes passaram com sucesso, confirmando a confiabilidade do sistema.",
        "conclusion_title": "5. Conclusão: O Futuro da Engenharia de Auditoria com IA",
        "conclusion_desc": "A união de especialização de domínio, grafos e testes automatizados faz dos agentes IA guardiões indispensáveis das finanças públicas."
    }
}

for loc, d in locales.items():
    loc_dir = os.path.join(base_dir, loc)
    os.makedirs(loc_dir, exist_ok=True)
    
freeze_code_snippet = """```javascript
// Stabilization freeze pattern
network.on("stabilizationIterationsDone", function () {
    network.setOptions({ physics: { enabled: false } });
    console.log("[Portal] Vis.js physics stabilized and frozen.");
});
```"""

for loc, d in locales.items():
    loc_dir = os.path.join(base_dir, loc)
    os.makedirs(loc_dir, exist_ok=True)
    
    # Build markdown
    content = f"""---
slug: national-budget-ai-inspector-portal-verification-system
title: "{d['title']}"
authors: [jbgih]
tags: [ai-agents, web-portal, test-automation, full-verification, audit-intelligence, devops]
date: 2026-11-23
keywords: {str(d['keywords']).replace("'", '"')}
description: "{d['description']}"
---

![National Budget Inspector Web Portal v3.0 & 20/20 Verification](./images/01_national_budget_inspector_portal.png)

> 💡 **{d['key_takeaways_title']}**
"""
    for item in d['key_takeaways']:
        content += f"> - {item}\n"
    
    content += f"""
{{/* truncate */}}

---

### ⚖️ {d['legal_notice_title']}

> {d['legal_notice']}

---

### {d['intro_p1']}

"""
    for item in d['intro_list']:
        content += f"1. **{item}**\n"
    
    content += f"""
> {d['intro_quote']}

{d['intro_p2']}

---

### {d['arch_title']}

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

"""
    for ws in d['workspaces']:
        content += f"- {ws}\n"
    
    content += f"""
---

### {d['challenges_title']}

#### 📌 {d['ch1_title']}
* {d['ch1_desc']}

#### 📌 {d['ch2_title']}
* {d['ch2_desc']}

---

### {d['bugs_title']}

#### 🐛 {d['bug1_title']}
* {d['bug1_desc']}

{freeze_code_snippet}

#### 🐛 {d['bug2_title']}
* {d['bug2_desc']}

#### 🐛 {d['bug3_title']}
* {d['bug3_desc']}

---

### {d['test_title']}

{d['test_desc']}

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

### {d['conclusion_title']}

{d['conclusion_desc']}
"""
    
    file_path = os.path.join(loc_dir, "index.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Written {loc}: {file_path}")
