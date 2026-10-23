---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "[スタンフォード CS146S #3] モデルコンテキストプロトコル(MCP)と自律ツール連携：AIエージェントのための標準アーキテクチャ"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, MCP Architecture, Claude Tool Use, JSON-RPC 2.0, Autonomous AI Agents]
description: "スタンフォード大学CS146S第3講の完全解説：『AIのためのLSP』と呼ばれるModel Context Protocol(MCP)のクライアント・サーバ設計、Stdio/SSEトランスポート、自律エージェントのツール実行ループを詳解。"
---

![Model Context Protocol Architecture](./images/03_cs146s_mcp_architecture.png)

スタンフォード大学の最先端ソフトウェア工学講義 **CS146S: 現代のソフトウェア開発者 (The Modern Software Developer)** 第3講の技術解説へようこそ。

第3講では、AI工学の最大の課題であった「孤立した大規模言語モデルを外部ツールやデータベースとどのように安全かつ標準化された方法で連携させるか」を解決する **Model Context Protocol (MCP)** と自律ツール利用（Tool Use）を深掘りします。

{/* truncate */}

---

### 1. AIのためのLSP：MCPのアーキテクチャ

マイクロソフトの言語サーバプロトコル(LSP)がエディタとコンパイラの連携を統一したように、Anthropicが提唱するMCPはAIエージェントと外部コンテキストの接続をJSON-RPC 2.0で標準化します。

```mermaid
flowchart LR
    Host["MCPホスト (Claude Code / Cursor)"] ==>|JSON-RPC 2.0| Client["MCPクライアント"]
    Client <==>|Stdio / SSE| S1["ファイルシステム MCPサーバ"]
    Client <==>|Stdio / SSE| S2["PostgreSQL MCPサーバ"]
    Client <==>|Stdio / SSE| S3["GitHub API MCPサーバ"]
```

### 参考文献 & 公式教材
- **公式YouTubeプレイリスト**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **主要文献**: Model Context Protocol Specification (modelcontextprotocol.io); Anthropic Claude Tool Use Architecture; Microsoft Language Server Protocol (LSP).
- **提供機関**: スタンフォード大学 コンピュータサイエンス学科
