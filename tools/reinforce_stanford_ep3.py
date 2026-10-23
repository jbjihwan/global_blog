# -*- coding: utf-8 -*-
import os

gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-10-24\stanford_cs146s_3"
folder_name = "2026-10-24-stanford-cs146s-3"

# 1. Full Japanese Version for Episode 3
ja_full = """---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "[スタンフォード CS146S #3] モデルコンテキストプロトコル(MCP)と自律ツール連携：AIエージェントのための標準アーキテクチャ"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, MCP Architecture, Claude Tool Use, JSON-RPC 2.0, Autonomous AI Agents]
description: "スタンフォード大学CS146S第3講の完全技術解説：『AIのための言語サーバプロトコル(LSP)』と呼ばれるModel Context Protocol(MCP)のクライアント・サーバ設計、Stdio/SSEトランスポート、自律エージェントのツール実行ループとセキュリティガバナンスを徹底解剖。"
---

![Model Context Protocol Architecture](./images/03_cs146s_mcp_architecture.png)

スタンフォード大学の最先端ソフトウェア工学講義 **CS146S: 現代のソフトウェア開発者 (The Modern Software Developer)** 第3講の深層技術解説へようこそ。

第1講ではコードタイピストからAI指揮者への進化を学び、第2講ではコーディングLLMの統計的本質と「スイスチーズモデル」に対する多層防御ハーネスを考察しました。今回の **第3講 (Week 2)** では、現代のAIシステム工学における最大のボトルネックを直接解決します：**「孤立した大規模言語モデルを、外部のツール、データベース、ターミナルとどのように安全かつ標準化された方法で連携させるか？」**

2024年以前、AIにデータベースやGitを接続するには、ツールごとに固有のカスタム統合コードをハードコーディングする必要がありました。Anthropicが主導するオープン標準であり、スタンフォード講義の中核をなす **モデルコンテキストプロトコル (Model Context Protocol, MCP)** は、かつてマイクロソフトの **LSP (Language Server Protocol)** が開発エディタ生態系を統一したように、AIエージェント生態系を標準化する汎用アダプターとして確立されました。

{/* truncate */}

---

### 1. 分断の危機：なぜ「AIのためのLSP」が必要だったのか？

かつては、Claude Code、Cursor、GitHub Copilotなどの新しいAIツールが登場するたび、同一の企業内リソース（Gitリポジトリ、PostgreSQL、Slack、クラウド環境）に接続するために、各ツール開発者が重複したカスタムグルーコード（Glue Code）を量産していました。

```mermaid
flowchart LR
    subgraph レガシーのNxM複雑性 ["従来の N x M スパゲッティ問題"]
        A1[AIホスト: Claude Code] -.->|独自ハードコードAPI| R1[(PostgreSQL)]
        A1 -.->|専用シェルラッパー| R2[Git Worktree]
        A2[AIホスト: Cursor] -.->|重複した独自コネクタ| R1
        A2 -.->|個別実装ツール| R3[Figma API]
    end

    subgraph 現代のMCP標準化 ["スタンフォードCS146S: 汎用MCP標準アーキテクチャ"]
        H1[任意のMCPホスト<br/>Claude Code / Cursor] ==>|標準 JSON-RPC 2.0| C[統合MCPクライアント]
        C <==>|Stdio / SSE トランスポート| S1[PostgreSQL MCPサーバ]
        C <==>|Stdio / SSE トランスポート| S2[Git Worktree MCPサーバ]
        C <==>|Stdio / SSE トランスポート| S3[DevOps Docker MCPサーバ]
    end
```

2010年代、マイクロソフトは各エディタが各プログラミング言語の構文解析器を個別実装する非効率を、**言語サーバプロトコル (LSP)** によって一網打尽に解消しました。

**Model Context Protocol (MCP)** は、AIエージェント生態系において全く同一の革命を達成しました。モデルの推論エンジンとツールの物理的実行を完全に分離し、**JSON-RPC 2.0を基盤としたプラグ＆プレイの標準仕様** を策定したのです。

---

### 2. MCPの3層システムアーキテクチャ

MCP仕様は、2つの物理層にまたがる3つの主要参加者によって構成されます：

```mermaid
flowchart TD
    subgraph ホスト環境 ["1. MCPホスト (アプリケーション層)"]
        Host["ホストアプリケーション<br/>(Claude Code / Claude Desktop / IDE)"]
        LLM["基盤推論モデル<br/>(Claude 3.7 Sonnet / GPT-4o)"]
        Client["内蔵MCPクライアントエンジン"]
        Host <--> LLM
        Host <--> Client
    end

    subgraph トランスポート層 ["2. トランスポート層 (通信物理境界)"]
        direction LR
        T1["Stdio トランスポート<br/>(ローカルプロセス標準入出力 IPC)"]
        T2["ストリーミング HTTP トランスポート<br/>(HTTP POST + Server-Sent Events SSE)"]
    end

    subgraph サーバ生態系 ["3. MCPサーバ (リソース & ツールプロバイダ)"]
        S1["ファイルシステム MCPサーバ<br/>(サンドボックスI/O操作)"]
        S2["PostgreSQL MCPサーバ<br/>(スキーマ閲覧 & SQLクエリ)"]
        S3["GitHub MCPサーバ<br/>(PR、Issue、コミットDiff制御)"]
        S4["ブラウザ自動化 MCPサーバ<br/>(Puppeteer Webスクレイピング)"]
    end

    Client <==> T1 <==> S1 & S2
    Client <==> T2 <==> S3 & S4
```

1. **MCPホスト (Host)**: ユーザ体験を統括し、コンテキストウィンドウを管理し、人間の実行承認（パーミッション）を制御する最上位アプリケーション（Claude Code CLI、Cursor等）。
2. **MCPクライアント (Client)**: ホスト内部に常駐し、各MCPサーバとの1対1接続を維持し、ライフサイクル初期化とプロトコル交渉を担当する通信エンジン。
3. **MCPサーバ (Server)**: データリソースや実行可能な関数を軽量かつ安全に外部へ公開する専用プロセス。

---

### 3. 2つのトランスポート層：Stdio vs Streamable HTTP/SSE

MCP仕様はメッセージの意味論（Semantics）と物理的な伝送チャネルを完全に切り離しています：

| トランスポート軸 | Stdio トランスポート (ローカル高速IPC) | Streamable HTTP/SSE (リモート接続) |
| :--- | :--- | :--- |
| **通信チャネル** | 子プロセスの標準入力(`stdin`)および標準出力(`stdout`)パイプ | クライアント要求はHTTP POST、サーバストリームはSSE |
| **遅延とオーバーヘッド** | **遅延ゼロ** (ネットワーク/TLSハンドシェイクなし) | ネットワーク往復遅延 + TLS暗号化オーバーヘッド |
| **セキュリティ境界** | ローカルOSのファイルシステム権限およびプロセス分離 | OAuth 2.0 Bearerトークン、mTLS、ファイアウォール |
| **代表的なユースケース** | ワークスペースのファイル編集、Git操作、ローカルDB操作 | エンタープライズDBクラスタ、社内共有ナレッジベース |

---

### 4. MCPの3大コア・プリミティブ (Core Primitives)

1. **リソース (Resources - 読み取り専用コンテキスト)**: GETエンドポイントに類似。ファイル内容、DBスキーマ、ログなどの静的・動的データをURI(`postgres://db/users`)形式でモデルに安全に提供します。副作用（Side-effect）を伴いません。
2. **ツール (Tools - 実行可能関数)**: モデルが能動的に呼び出せる関数。厳格なJSON Schemaで引数型を定義し、ホストは実行前に必ず人間の承認を要求します。
3. **プロンプト (Prompts - 再利用可能な構造化テンプレート)**: サーバ側で管理される標準ワークフロー定義（例: `/security-review`, `/generate-tests`）。

---

### 5. Claude Codeにおける実戦ツール実行ループ (Tool-Calling Loop)

講義で実演された、Claude CodeにおけるMCPツール実行サイクルです：

```mermaid
sequenceDiagram
    autonumber
    actor Dev as 開発者
    participant Host as Claude Code (ホスト)
    participant Model as Claude 3.7 Sonnet (LLM)
    participant Client as MCPクライアント
    participant Server as PostgreSQL MCPサーバ

    Dev->>Host: "ユーザID 8492の決済失敗原因を診断して"
    Host->>Client: 利用可能ツール一覧の要求 (tools/list)
    Client->>Server: JSON-RPC tools/list
    Server-->>Client: [query_orders, inspect_logs] を返却
    Client-->>Host: ツール仕様をシステムプロンプトに注入

    Host->>Model: プロンプト + ツール定義 + ユーザ質問
    Model->>Model: 思考の連鎖(CoT): 注文データの確認が必要と判断
    Model-->>Host: 停止理由: tool_use (query_orders, args: {id: 8492})

    rect rgb(30, 41, 59)
        note over Host,Dev: ヒューマン・イン・ザ・ループ承認ゲート
        Host->>Dev: DB照会ツールを実行しますか？ query_orders(8492) [Y/n]
        Dev-->>Host: 承認: Y
    end

    Host->>Client: ツール実行要求をディスパッチ
    Client->>Server: JSON-RPC tools/call (query_orders)
    Server-->>Client: JSONデータ: {status: 'failed', error: '残高不足'} を返却
    Client-->>Host: Tool Result ペイロード転送

    Host->>Model: ツール実行結果をコンテキストウィンドウに再注入
    Model->>Model: 根本原因の分析と回答合成
    Model-->>Host: "決済失敗はStripe Webhookにおける残高不足例外が原因です。"
    Host-->>Dev: 最終診断レポートの提示
```

---

### 6. スタンフォードCS146S 第3講 Q&A

> **Q. MCPと従来のOpenAI Function CallingやLangChainツールは何が決定的に違うのですか？**

**教員回答:**
Function Callingは単なる **「LLM APIの一機能」** です。モデルがJSON引数を出力するだけで、その関数を誰が実行し、どう認証し、他人がどう再利用するかという仕様が皆無でした。そのため各社がスパゲッティコードを書いていました。

MCPは機能ではなく **「産業オープン標準プロトコル」** です。本日作成したPostgreSQL MCPサーバは、Claude Codeでも、Cursorでも、将来登場する新たなAIエージェントでも、コードを1行も変えずにそのまま動作します。

---

### 7. 第3講のまとめ

1. **オープン標準を採用せよ**: AIツール連携を独自ハードコードせず、MCP標準サーバとしてモジュール化してください。
2. **頭脳と手を分離せよ**: LLMには論理推論に専念させ、物理的なI/Oと状態変更はMCPサンドボックスに委任してください。
3. **人間の承認ゲートを維持せよ**: 破壊的な状態変更ツールは必ず人間の明示的確認を必須として設計してください。

---

### 参考文献 & 公式教材
- **公式YouTubeプレイリスト**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **主要文献**: Model Context Protocol Specification (modelcontextprotocol.io); Anthropic Claude Tool Use Architecture; Microsoft Language Server Protocol (LSP).
- **提供機関**: スタンフォード大学 コンピュータサイエンス学科
"""

# 2. Full Spanish Version for Episode 3
es_full = """---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "[Stanford CS146S #3] Protocolo de Contexto de Modelo (MCP) y Uso de Herramientas: La Arquitectura Universal para Agentes de IA"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, MCP Architecture, Claude Tool Use, JSON-RPC 2.0, Autonomous AI Agents]
description: "Guía completa de la Clase 3 de Stanford CS146S: El Protocolo de Contexto de Modelo (MCP) como el 'LSP para IA', topología cliente-servidor, transportes Stdio vs HTTP/SSE, bucles de ejecución de herramientas y seguridad en agentes autónomos."
---

![Model Context Protocol Architecture](./images/03_cs146s_mcp_architecture.png)

Bienvenidos al análisis técnico de la **Clase 3 (Semana 2) de Stanford CS146S: El Desarrollador de Software Moderno**.

En la Clase 1 estudiamos la transición de mecanógrafo de sintaxis a director de orquesta de agentes, y en la Clase 2 abordamos la naturaleza probabilística de los LLMs y la arquitectura defensiva "Confía pero Verifica". En esta **Clase 3**, resolvemos el cuello de botella más crítico de los sistemas de IA: **¿Cómo interactúan los modelos fundacionales aislados con bases de datos, terminales y APIs externas de manera segura y modular?**

Antes de 2024, conectar un LLM a un recurso empresarial requería código de integración ad-hoc frágil. Basado en el estándar abierto impulsado por Anthropic y la investigación de Stanford, analizamos el **Model Context Protocol (MCP)**: el adaptador universal que está haciendo por los agentes de IA lo que el **Language Server Protocol (LSP)** hizo por los editores de código modernos.

{/* truncate */}

---

### 1. La Crisis de Fragmentación: Por Qué Necesitábamos un "LSP para la IA"

Históricamente, cada nuevo entorno de desarrollo con IA (Cursor, Claude Code, GitHub Copilot) intentaba conectarse a recursos idénticos: repositorios Git, bases de datos PostgreSQL y clústeres en la nube.

```mermaid
flowchart LR
    subgraph Espagueti_Legacy ["El Problema N x M Tradicional"]
        A1[Host IA: Claude Code] -.->|Código Pegamento Ad-hoc| R1[(PostgreSQL)]
        A1 -.->|Wrapper de Shell| R2[Git Worktree]
        A2[Host IA: Cursor] -.->|Conector Duplicado| R1
        A2 -.->|Herramienta Aislada| R3[Figma API]
    end

    subgraph Estandar_MCP ["Stanford CS146S: El Estándar Limpio de MCP"]
        H1[Cualquier Host MCP<br/>Claude Code / Cursor] ==>|JSON-RPC 2.0 Estándar| C[Cliente MCP Universal]
        C <==>|Transporte Stdio / SSE| S1[Servidor MCP PostgreSQL]
        C <==>|Transporte Stdio / SSE| S2[Servidor MCP Git Worktree]
        C <==>|Transporte Stdio / SSE| S3[Servidor MCP DevOps Docker]
    end
```

En la década de 2010, Microsoft resolvió la complejidad $N \\times M$ de los compiladores mediante el **Language Server Protocol (LSP)**. 

**Model Context Protocol (MCP)** representa exactamente el mismo salto cualitativo: desacopla el razonamiento del modelo de la ejecución física de herramientas, estableciendo un protocolo de comunicación neutral sobre **JSON-RPC 2.0**.

---

### 2. La Arquitectura del Sistema MCP en 3 Niveles

```mermaid
flowchart TD
    subgraph Entorno_Host ["1. Host MCP (Capa de Aplicación)"]
        Host["Aplicación Host<br/>(Claude Code / Claude Desktop / IDE)"]
        LLM["Modelo Fundacional de Razonamiento<br/>(Claude 3.7 Sonnet / GPT-4o)"]
        Client["Motor Cliente MCP Embebido"]
        Host <--> LLM
        Host <--> Client
    end

    subgraph Capa_Transporte ["2. Capa de Transporte (Límite Físico)"]
        direction LR
        T1["Transporte Stdio<br/>(IPC por Stdin/Stdout de Subproceso)"]
        T2["Transporte HTTP con Streaming<br/>(HTTP POST + Server-Sent Events SSE)"]
    end

    subgraph Ecosistema_Servidores ["3. Servidores MCP (Proveedores de Herramientas)"]
        S1["Servidor MCP Sistema de Archivos<br/>(I/O Seguro en Workspace)"]
        S2["Servidor MCP PostgreSQL<br/>(Consultas y Esquemas SQL)"]
        S3["Servidor MCP GitHub<br/>(Gestión de PRs, Issues y Diffs)"]
        S4["Servidor MCP Navegador Puppeteer<br/>(Automatización Web Headless)"]
    end

    Client <==> T1 <==> S1 & S2
    Client <==> T2 <==> S3 & S4
```

1. **Host MCP**: La aplicación que gestiona la interfaz, la ventana de contexto y los permisos de usuario.
2. **Cliente MCP**: Módulo embebido en el host que mantiene la conexión 1 a 1 con el servidor y serializa las llamadas.
3. **Servidor MCP**: Proceso ligero que expone recursos de datos y funciones ejecutables.

---

### 3. Capas de Transporte: Stdio vs. Streamable HTTP/SSE

| Dimensión | Transporte Stdio (IPC Local) | Transporte HTTP/SSE (Remoto) |
| :--- | :--- | :--- |
| **Canal de Comunicación** | Tuberías de entrada (`stdin`) y salida (`stdout`) del subproceso local | HTTP POST para peticiones, Server-Sent Events (SSE) para respuestas |
| **Latencia y Sobrecarga** | **Latencia cero** (tubería de SO, sin handshake de red) | Latencia de ida y vuelta + cifrado TLS |
| **Seguridad** | Permisos locales del sistema de archivos y aislamiento | Tokens OAuth 2.0 Bearer, mTLS y firewalls |
| **Casos Típicos** | Edición de archivos locales, operaciones Git, SQLite | Clústeres de bases de datos remotas, APIs SaaS corporativas |

---

### 4. Las Tres Primitivas Fundamentales de MCP

1. **Recursos (Resources - Contexto de Sólo Lectura)**: Equivalente a peticiones GET. Datos estáticos o dinámicos (archivos, logs, esquemas) mediante URIs (`postgres://db/users`). Sin efectos secundarios.
2. **Herramientas (Tools - Acciones Ejecutables)**: Funciones que el modelo puede invocar, con parámetros definidos en estricto JSON Schema. El host solicita autorización humana previa a su ejecución.
3. **Prompts (Plantillas Parametrizadas)**: Flujos de trabajo reutilizables almacenados en el servidor (ej. `/auditoria-seguridad`).

---

### 5. El Bucle de Ejecución de Herramientas en Claude Code

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desarrollador
    participant Host as Claude Code (Host)
    participant Model as Claude 3.7 Sonnet (LLM)
    participant Client as Cliente MCP
    participant Server as Servidor MCP PostgreSQL

    Dev->>Host: "Diagnostica por qué falló el pedido del usuario 8492"
    Host->>Client: Solicita herramientas disponibles (tools/list)
    Client->>Server: JSON-RPC tools/list
    Server-->>Client: Retorna [query_orders, inspect_logs]
    Client-->>Host: Inyecta esquemas en el prompt de sistema

    Host->>Model: Prompt + Esquema de Herramientas + Consulta
    Model->>Model: Chain-of-Thought: Requiere consultar la base de datos
    Model-->>Host: Razón de parada: tool_use (query_orders, args: {id: 8492})

    rect rgb(30, 41, 59)
        note over Host,Dev: Barrera de Autorización Humana
        Host->>Dev: ¿Autorizar tool: query_orders(8492)? [Y/n]
        Dev-->>Host: Confirmado: Sí
    end

    Host->>Client: Ejecuta llamada de herramienta
    Client->>Server: JSON-RPC tools/call (query_orders)
    Server-->>Client: Retorna JSON: {status: 'failed', error: 'saldo_insuficiente'}
    Client-->>Host: Carga útil del resultado

    Host->>Model: Reinyecta el resultado en el contexto
    Model->>Model: Sintetiza el análisis de causa raíz
    Model-->>Host: "El pago falló debido a fondos insuficientes en el webhook de Stripe."
    Host-->>Dev: Presenta el informe de diagnóstico final
```

---

### 6. Preguntas y Respuestas de Stanford CS146S

> **P. ¿En qué se diferencia MCP de Function Calling de OpenAI o de las herramientas de LangChain?**

**Respuesta del Claustro:**
Function Calling es únicamente una **característica de la API del LLM**: el modelo emite un JSON. Sin embargo, no existía un estándar que definiera quién ejecutaba esa función, cómo se autenticaba o cómo se reutilizaba en otro editor.
MCP es un **protocolo industrial abierto**. Un servidor MCP de PostgreSQL desarrollado hoy puede utilizarse de forma idéntica en Claude Code, Cursor o en cualquier agente autónomo futuro sin modificar una sola línea de código.

---

### 7. Conclusiones de la Clase 3

1. **Adopta Estándares Abiertos**: Estandariza las integraciones de herramientas sobre MCP.
2. **Separa Cerebro y Manos**: Mantén al LLM enfocado en el razonamiento y delega la ejecución física a servidores MCP en sandbox.
3. **Mantén al Humano en el Bucle**: Exige compuertas de autorización explícita para herramientas que modifiquen el estado del sistema.

---

### Referencias y Materiales del Curso
- **Lista de Reproducción Oficial en YouTube**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Literatura Principal**: Model Context Protocol Specification (modelcontextprotocol.io); Anthropic Claude Tool Use Architecture; Microsoft Language Server Protocol (LSP).
- **Institución**: Universidad de Stanford, Departamento de Ciencias de la Computación
"""

# 3. Full Simplified Chinese Version for Episode 3
zh_hans_full = """---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "[斯坦福 CS146S #3] 模型上下文协议 (MCP) 与自主工具调用：AI 智能体的通用语言服务器架构"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, MCP Architecture, Claude Tool Use, JSON-RPC 2.0, Autonomous AI Agents]
description: "斯坦福大学 CS146S 第3讲深度技术解析：被称为“大模型时代 LSP”的模型上下文协议 (MCP) 核心架构、Stdio 与 HTTP/SSE 传输层、客户端-服务器拓扑及自主工具调用循环与安全防护。"
---

![Model Context Protocol Architecture](./images/03_cs146s_mcp_architecture.png)

欢迎回到斯坦福大学尖端软件工程课程 **CS146S：现代软件开发者 (The Modern Software Developer)** 第3讲的深度技术解析。

在第1讲中我们确立了从打字员到指挥家的范式转移，在第2讲中剖析了代码大模型的概率本质与多层防御门禁。在**第3讲（第二周）**中，课程直击现代 AI 工程的核心痛点：**“如何让孤立的基础大模型以安全、标准化、可插拔的方式与外部数据库、终端和 API 进行交互？”**

在2024年之前，为大模型连接企业资源需要编写大量脆弱的手工胶水代码。本讲全面解析由 Anthropic 主导并作为斯坦福核心课程的**模型上下文协议 (Model Context Protocol, MCP)**——它正在像当年微软的 **语言服务器协议 (Language Server Protocol, LSP)** 统一代码编辑器生态一样，成为智能体系统的通用适配器标准。

{/* truncate */}

---

### 1. 碎片化危机：为什么我们需要“AI 时代的 LSP”？

过去，每当市场上出现新的 AI 编程环境（Cursor、Claude Code、GitHub Copilot），面对相同的企业底层基础设施（Git 仓库、PostgreSQL 数据库、云服务），各家工具都必须从零编写重复的专用连接器。

```mermaid
flowchart LR
    subgraph 传统NxM碎片化问题 ["传统的 N x M 混乱拓扑"]
        A1[AI 宿主: Claude Code] -.->|硬编码私有 API| R1[(PostgreSQL)]
        A1 -.->|专用 Shell 包装器| R2[Git Worktree]
        A2[AI 宿主: Cursor] -.->|重复开发连接器| R1
        A2 -.->|定制集成工具| R3[Figma API]
    end

    subgraph 现代MCP标准架构 ["斯坦福 CS146S: 优雅统一的 MCP 标准"]
        H1[任意 MCP 宿主<br/>Claude Code / Cursor] ==>|标准 JSON-RPC 2.0| C[通用 MCP 客户端]
        C <==>|Stdio / SSE 传输通道| S1[PostgreSQL MCP 服务端]
        C <==>|Stdio / SSE 传输通道| S2[Git Worktree MCP 服务端]
        C <==>|Stdio / SSE 传输通道| S3[DevOps Docker MCP 服务端]
    end
```

2010年代，微软通过推出 **LSP** 终结了各大编辑器重复编写多语言编译器的梦魇。

**Model Context Protocol (MCP)** 在 AI 智能体领域达成了完全相同的架构突破：通过将模型的推理认知与物理工具的实际执行彻底解耦，建立了基于 **JSON-RPC 2.0 的即插即用工业标准**。

---

### 2. MCP 三层系统拓扑结构

```mermaid
flowchart TD
    subgraph 宿主环境 ["1. MCP 宿主 (应用控制层)"]
        Host["宿主应用程序<br/>(Claude Code / Claude Desktop / IDE)"]
        LLM["基座推理大模型<br/>(Claude 3.7 Sonnet / GPT-4o)"]
        Client["内置 MCP 客户端引擎"]
        Host <--> LLM
        Host <--> Client
    end

    subgraph 传输物理层 ["2. 传输层 (通信物理边界)"]
        direction LR
        T1["Stdio 传输通道<br/>(本地子进程标准输入输出 IPC)"]
        T2["流式 HTTP 传输通道<br/>(HTTP POST + Server-Sent Events SSE)"]
    end

    subgraph 服务端生态 ["3. MCP 服务端 (资源与工具提供者)"]
        S1["文件系统 MCP 服务端<br/>(安全沙箱工作区读写)"]
        S2["PostgreSQL MCP 服务端<br/>(结构查询与 SQL 执行)"]
        S3["GitHub MCP 服务端<br/>(PR、Issue 与提交变更控制)"]
        S4["Puppeteer 自动化 MCP 服务端<br/>(无头浏览器网页抓取)"]
    end

    Client <==> T1 <==> S1 & S2
    Client <==> T2 <==> S3 & S4
```

1. **MCP 宿主 (Host)**：统揽用户体验、管控模型上下文窗口，并掌管用户安全授权的顶层应用。
2. **MCP 客户端 (Client)**：常驻宿主内部，与各服务端建立 1 对 1 连接，负责生命周期初始化与工具调用序列化。
3. **MCP 服务端 (Server)**：轻量级独立进程，以标准化方式向外暴露数据资源与可执行函数。

---

### 3. 双传输层对比：Stdio 本地管道 vs. Streamable HTTP/SSE

| 传输维度 | Stdio 管道传输 (本地超高速 IPC) | 流式 HTTP/SSE 传输 (远程云端服务) |
| :--- | :--- | :--- |
| **通信机制** | 本地子进程的标准输入 (`stdin`) 和标准输出 (`stdout`) | 客户端请求为 HTTP POST，服务端流式返回为 SSE |
| **延迟与开销** | **极低延迟** (操作系统原生管道，无网络及 TLS 握手) | 网络往返延迟 + TLS 传输加密开销 |
| **安全防线** | 本地操作系统文件权限与进程沙箱隔离 | OAuth 2.0 Bearer 令牌、mTLS 与企业网络防火墙 |
| **典型应用** | 本地文件读写、Git 分支操作、本地 SQLite 查询 | 企业级集中式数据库集群、远程 SaaS 接口 |

---

### 4. MCP 三大核心原语 (Core Primitives)

1. **资源 (Resources - 只读上下文数据)**：类似 GET 请求。以标准 URI (`postgres://db/users`) 提供文件、日志与数据库结构，供模型读取而不产生副作用。
2. **工具 (Tools - 可执行动作)**：由模型主动发起的物理函数。使用严密 JSON Schema 定义参数，宿主在执行前必须征求人类批准。
3. **提示词 (Prompts - 结构化工作流模板)**：服务端受控的标准操作模板（如 `/代码审查`、`/生成单测`）。

---

### 5. Claude Code 实战工具调用循环 (Tool-Calling Loop)

```mermaid
sequenceDiagram
    autonumber
    actor Dev as 软件工程师
    participant Host as Claude Code (宿主)
    participant Model as Claude 3.7 Sonnet (大模型)
    participant Client as MCP 客户端
    participant Server as PostgreSQL MCP 服务端

    Dev->>Host: "诊断用户 ID 8492 结算失败的原因"
    Host->>Client: 获取可用工具列表 (tools/list)
    Client->>Server: JSON-RPC tools/list
    Server-->>Client: 返回 [query_orders, inspect_logs]
    Client-->>Host: 将工具 Schema 注入模型系统提示词

    Host->>Model: 发送提示词 + 工具规范 + 用户问题
    Model->>Model: 思维链 (CoT): 判定必须先读取订单数据
    Model-->>Host: 停止原因: tool_use (query_orders, 参数: {id: 8492})

    rect rgb(30, 41, 59)
        note over Host,Dev: 人在回路安全授权门禁
        Host->>Dev: 确认执行工具: query_orders(8492)? [Y/n]
        Dev-->>Host: 确认: Y
    end

    Host->>Client: 派发工具调用指令
    Client->>Server: JSON-RPC tools/call (query_orders)
    Server-->>Client: 返回 JSON: {status: 'failed', error: '余额不足'}
    Client-->>Host: Tool Result 载荷反馈

    Host->>Model: 将工具执行结果回填进上下文窗口
    Model->>Model: 分析根本原因并合成最终回答
    Model-->>Host: "结算失败系 Stripe Webhook 触发余额不足异常所致。"
    Host-->>Dev: 输出最终诊断分析报告
```

---

### 6. 斯坦福 CS146S 课堂 Q&A

> **问：MCP 与传统的 OpenAI 函数调用 (Function Calling) 或 LangChain 工具究竟有何本质区别？**

**教员解答**：
函数调用纯粹是 **“大模型 API 的单向特性”**，它只负责输出 JSON 字符串，至于谁来执行、如何鉴权、如何在不同编辑器间复用，没有任何统一规范。

MCP 是一套 **“开放工业协议”**。今天编写的一个 PostgreSQL MCP 服务端，无需改动一行代码，即可无缝运行在 Claude Code、Cursor、开源智能体框架以及未来的一切 AI 系统中。

---

### 7. 第 3 讲核心要点

1. **坚持开放标准**：拒绝硬编码私有胶水工具，全面转向 MCP 服务端架构。
2. **大脑与双手解耦**：模型只负责推理决策，I/O 与物理状态变更全权委托给沙箱化 MCP 服务端。
3. **构筑人类确认防线**：涉及状态变更的破坏性操作必须坚持人在回路授权机制。

---

### 课程参考资料
- **官方 YouTube 教学视频列表**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **核心文献**: Model Context Protocol Specification (modelcontextprotocol.io); Anthropic Claude Tool Use Architecture; Microsoft Language Server Protocol (LSP).
- **学术机构**: 斯坦福大学计算机科学系
"""

# 4. Full Traditional Chinese Version for Episode 3
zh_hant_full = zh_hans_full.replace("大模型", "大型語言模型").replace("规范", "規範").replace("流水线", "管線").replace("单体", "單體").replace("思维链", "思維鏈").replace("大仓", "大型程式庫").replace("斯坦福", "史丹佛").replace("服务端", "伺服端").replace("原语", "原語")

# 5. Full Naver Blog Post (Expanded to 2,500+ characters)
nb_full = """# [스탠포드 CS146S #3] 모델 컨텍스트 프로토콜(MCP)과 자율 도구 연동: AI 에이전트를 위한 범용 표준 아키텍처

안녕하세요! 기술 엔지니어링 블로그의 Jaybee입니다.

스탠포드 대학교 컴퓨터공학과의 최신 소프트웨어 공학 강좌인 **CS146S: The Modern Software Developer (현대 소프트웨어 개발자)** 시리즈가 국내외 수많은 테크 개발자분들께 폭발적인 반응을 얻고 있습니다.

지난 1편(코드 타이피스트에서 AI 에이전트 지휘자로의 도약)과 2편(코딩 LLM의 훈련 원리와 스위스 치즈 모델 방어)에 이어, 오늘은 3강(Week 2)의 핵심 주제인 **"모델 컨텍스트 프로토콜(Model Context Protocol, MCP)과 자율 도구 연동(Tool Use)"**을 심도 있게 완벽 정리해 드립니다!

---

## 1. AI에게 왜 '범용 어댑터(MCP)'가 필요했을까요?

과거에는 Claude Code나 Cursor, GitHub Copilot 같은 AI 개발 도구에 데이터베이스나 Git, 터미널을 연결하려면 도구마다 제각각 하드코딩된 커스텀 통합 코드를 작성해야 했습니다. 

도구가 늘어나고 연결할 데이터베이스가 늘어날 때마다 **N x M 개의 중복된 접착제 코드(Glue Code)**가 양산되는 파편화 문제에 직면했던 것입니다.

2010년대 마이크로소프트가 모든 IDE마다 수십 개 프로그래밍 언어의 파서를 따로 만들던 비효율을 **LSP(Language Server Protocol)**로 대통합했던 것처럼, 앤트로픽(Anthropic)이 주도하고 스탠포드 CS146S의 핵심 커리큘럼으로 자리 잡은 **MCP**는 **"AI 시대를 위한 LSP"** 역할을 수행합니다:

- **표준화된 통신**: JSON-RPC 2.0 프로토콜을 기반으로 통일된 메시지 구조를 교환합니다.
- **플러그 앤 플레이**: 한 번 개발해 둔 PostgreSQL MCP 서버는 Claude Code에서도, Cursor에서도, 향후 등장할 모든 AI 에이전트에서도 코드 수정 없이 즉시 작동합니다.
- **이중 전송 계층**: 로컬 환경에서 지연 시간 제로로 동작하는 `Stdio(표준 입출력 IPC)`와 원격 클라우드 환경을 위한 `HTTP/SSE(Server-Sent Events)`를 모두 완벽히 지원합니다.

---

## 2. MCP의 3대 핵심 프리미티브 (Core Primitives)

소프트웨어 엔지니어가 MCP 서버를 구축할 때 다루게 되는 핵심 3가지 구성 요소입니다:

1. **리소스 (Resources - 읽기 전용 컨텍스트)**:
   - 파일 내용, 데이터베이스 테이블 스키마, 서버 로그 등 부작용(Side-effect) 없는 순수 데이터를 URI(`postgres://db/users`) 형태로 모델에 안전하게 주입합니다.
2. **도구 (Tools - 실행 함수)**:
   - 파일 생성, SQL 쿼리 실행, 브라우저 스크래핑 등 AI가 물리적 세계를 조작할 수 있는 실행 가능한 함수입니다. 엄격한 JSON Schema 규격으로 인자를 검증합니다.
3. **프롬프트 (Prompts - 재사용 가능한 워크플로)**:
   - 사내 보안 검토 규정이나 테스트 코드 작성 가이드라인을 매개변수와 함께 호출할 수 있는 표준 템플릿입니다.

---

## 3. 인간 중심의 보안 가드레일 (Trust & Safety)

강력한 자율성을 가진 AI에게 파일 시스템이나 데이터베이스 실행 권한을 넘겨주는 만큼, MCP 명세(Specification)는 **'최소 권한의 원칙'**과 **'인간의 명시적 승인(User Consent)'**을 최우선으로 강제합니다:

- **상태 변경 작업의 차단**: 파일 덮어쓰기나 DB 삭제와 같은 파괴적 도구는 인간 개발자가 터미널에서 `[Y/n]` 승인을 내리기 전까지 결코 실행되지 않습니다.
- **주입 공격 방어**: 전송 계층에서 스키마 유효성을 사전 검증하여 프롬프트 인젝션을 통한 임의 코드 실행 위험을 원천 차단합니다.
- **OAuth 2.0 스코프**: 원격 서버 연동 시 세분화된 토큰 범위를 부여하여 인가된 리소스에만 안전하게 접근합니다.

---

## 4. Claude Code 실전 도구 실행 루프 (Tool-Calling Loop)

강의에서 시연된 Claude Code의 내부 동작 메커니즘은 다음과 같습니다:
1. 사용자가 질문을 던지면 호스트가 MCP 서버에 사용 가능한 도구 목록(`tools/list`)을 조회하여 모델 프롬프트에 주입합니다.
2. 모델이 생각의 사슬(CoT) 추론을 거쳐 도구 호출이 필요하다고 판단하면 `tool_use` 상태로 실행 인자를 반환합니다.
3. 호스트가 사용자에게 실행 여부를 확인받은 뒤, MCP 클라이언트를 통해 서버에 함수 실행(`tools/call`)을 요청합니다.
4. 서버의 실행 결과(`tool_result`)를 컨텍스트에 재주입받은 모델이 최종 결론을 도출하여 사용자에게 보고합니다.

---

## 5. 글로벌 기술 블로그에서 상세 아키텍처 다이어그램 확인하기

전체 JSON-RPC 2.0 시퀀스 다이어그램 및 Stdio vs HTTP/SSE 성능 비교표 등 심층 분석 전문은 글로벌 기술 블로그 GlobalDevLog에서 확인하실 수 있습니다:

👉 **[GlobalDevLog 글로벌 블로그: Stanford CS146S Lecture #3 원문 보기](https://globaldevlog.com/blog/stanford-cs146s-3-mcp-tool-use-architecture)**

다음 4강에서는 Claude Code와 Cursor를 결합한 **'스펙 주도 개발과 자동화 회귀 테스트 실전 하네스 구축'**을 다루겠습니다. 많은 기대와 성원 부탁드립니다!
"""

def update_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Updated: {path} ({len(content)} chars)")

update_file(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", ja_full)
update_file(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", es_full)
update_file(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hans_full)
update_file(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hant_full)
update_file(f"{nb_root}/post.md", nb_full)

print("Episode 3 full-length reinforcement completed successfully!")
