---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "[史丹佛 CS146S #3] 模型上下文協定 (MCP) 與自主工具調用：AI 智慧代理人的通用標準架構"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, MCP Architecture, Claude Tool Use, JSON-RPC 2.0, Autonomous AI Agents]
description: "史丹佛大學 CS146S 第3講深度解析：被譽為「AI 時代 LSP」的模型上下文協定 (MCP) 核心架構、Stdio 與 HTTP/SSE 傳輸機制、客戶端-伺服器拓撲及工具執行循環。"
---

![Model Context Protocol Architecture](./images/03_cs146s_mcp_architecture.png)

歡迎回到史丹佛大學尖端軟體工程課程 **CS146S：現代軟體開發者 (The Modern Software Developer)** 第3講的技術解析。

本講剖析 AI 軟體工程的核心瓶頸：如何讓大型語言模型安全且標準化地調用外部工具與企業資料庫？全面解析被稱為「AI 時代 LSP」的**模型上下文協定 (Model Context Protocol, MCP)**。

{/* truncate */}

---

### 1. AI 時代的 LSP：MCP 架構解析

正如微軟 Language Server Protocol (LSP) 統整了程式編輯器生態，MCP 藉由 JSON-RPC 2.0 將模型認知與外部工具徹底解耦，建立標準化擴充介面。

```mermaid
flowchart LR
    Host["MCP 宿主 (Claude Code / Cursor)"] ==>|JSON-RPC 2.0| Client["MCP 客戶端"]
    Client <==>|Stdio / SSE| S1["檔案系統 MCP 伺服器"]
    Client <==>|Stdio / SSE| S2["PostgreSQL MCP 伺服器"]
    Client <==>|Stdio / SSE| S3["GitHub API MCP 伺服器"]
```

### 課程參考資料
- **官方 YouTube 影片播放清單**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **主要文獻**: Model Context Protocol Specification (modelcontextprotocol.io); Anthropic Claude Tool Use Architecture; Microsoft Language Server Protocol (LSP).
- **學術機構**: 史丹佛大學電腦科學系
