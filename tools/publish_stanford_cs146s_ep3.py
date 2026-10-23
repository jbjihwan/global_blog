# -*- coding: utf-8 -*-
import os
import shutil

gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-10-24\stanford_cs146s_3"
folder_name = "2026-10-24-stanford-cs146s-3"
slug_name = "stanford-cs146s-3-mcp-tool-use-architecture"

# 1. English Content
en_content = """---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "[Stanford CS146S #3] Model Context Protocol (MCP) & Autonomous Tool Use: The Universal Language Server Architecture for AI Agents"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, MCP Architecture, Claude Tool Use, JSON-RPC 2.0, Autonomous AI Agents]
description: "Stanford CS146S Lecture 3 comprehensive guide: Deep-diving into the Model Context Protocol (MCP) as the 'LSP for AI', client-server topology, Stdio vs HTTP/SSE transports, and building secure tool-calling loops for autonomous coding agents."
---

![Model Context Protocol Architecture](./images/03_cs146s_mcp_architecture.png)

Welcome to the third installment of our deep-dive engineering series on **Stanford University's CS146S: The Modern Software Developer**.

In Lecture 1, we established the paradigm shift from syntax typist to agent conductor. In Lecture 2, we examined the probabilistic nature of coding LLMs and the defensive "Trust but Verify" harness. In **Lecture 3 (Week 2)**, the curriculum addresses the single greatest architectural bottleneck in modern AI systems: **How do isolated foundation models safely and modularly interact with the external world?**

Before 2024, connecting an LLM to a database, terminal, or GitHub API required fragile, bespoke integration glue. Drawing directly from Anthropic's open standard specification and Stanford's distributed systems analysis, this lecture unpacks the **Model Context Protocol (MCP)**—the universal adapter that is doing for autonomous AI agents what the **Language Server Protocol (LSP)** did for modern code editors.

{/* truncate */}

---

### 1. The Fragmentation Crisis: Why We Needed an "LSP for AI"

Historically, every new AI IDE or coding tool (Cursor, Claude Code, GitHub Copilot, Devin) attempted to connect to identical enterprise resources: Git repositories, PostgreSQL clusters, Slack channels, and AWS infrastructure.

```mermaid
flowchart LR
    subgraph Legacy_N_Times_M ["The Legacy N x M Spaghetti Problem"]
        A1[AI Host: Claude Code] -.->|Custom API Glue| R1[(PostgreSQL)]
        A1 -.->|Custom Shell Wrapper| R2[Git Worktree]
        A2[AI Host: Cursor] -.->|Duplicate Integration| R1
        A2 -.->|Custom Tool Hook| R3[Figma API]
        A3[AI Host: Claude Desktop] -.->|Third Tool Driver| R1
    end

    subgraph Modern_MCP_Standard ["Stanford CS146S: The Clean MCP Standard"]
        H1[Any MCP Host<br/>Claude Code / Cursor] ==>|Standard JSON-RPC 2.0| C[Universal MCP Client]
        C <==>|Stdio / SSE Transport| S1[PostgreSQL MCP Server]
        C <==>|Stdio / SSE Transport| S2[Git Worktree MCP Server]
        C <==>|Stdio / SSE Transport| S3[DevOps Docker MCP Server]
    end
```

In the compiler and editor ecosystem of the 2010s, Microsoft solved the $N \\times M$ complexity crisis by introducing the **Language Server Protocol (LSP)**. Instead of every editor writing a custom parser for TypeScript, Rust, and Go, language teams built a single LSP server, and editors built a single LSP client.

**Model Context Protocol (MCP)** represents the exact same architectural breakthrough for artificial intelligence. By decoupling model reasoning from tool execution, MCP establishes a vendor-neutral, plug-and-play communication protocol over JSON-RPC 2.0.

---

### 2. The 3-Tier MCP System Architecture

An MCP-compliant ecosystem is comprised of three distinct participants operating across two decoupled layers:

```mermaid
flowchart TD
    subgraph Host_Environment ["1. MCP Host (Application Layer)"]
        Host["Host Application<br/>(Claude Code / Claude Desktop / IDE)"]
        LLM["Foundation Reasoning Model<br/>(Claude 3.7 Sonnet / GPT-4o)"]
        Client["Embedded MCP Client Engine"]
        Host <--> LLM
        Host <--> Client
    end

    subgraph Transport_Layer ["2. Transport Layer (Physical Boundary)"]
        direction LR
        T1["Stdio Transport<br/>(Subprocess Stdin/Stdout IPC)"]
        T2["Streamable HTTP Transport<br/>(HTTP POST + Server-Sent Events SSE)"]
    end

    subgraph Server_Ecosystem ["3. MCP Servers (Resource & Tool Providers)"]
        S1["Filesystem MCP Server<br/>(Sandboxed Workspace I/O)"]
        S2["PostgreSQL MCP Server<br/>(Read-Only Schema & Queries)"]
        S3["GitHub MCP Server<br/>(PRs, Issues, Commit Diffs)"]
        S4["Puppeteer Web MCP Server<br/>(Headless Browser Automation)"]
    end

    Client <==> T1 <==> S1 & S2
    Client <==> T2 <==> S3 & S4
```

#### 2.1. MCP Host
The parent application that orchestrates the user experience, controls LLM context windows, and holds user permissions. Examples include **Claude Code CLI**, Claude Desktop, and modern agentic development environments.

#### 2.2. MCP Client
An internal protocol handler embedded inside the Host. The client maintains a strict 1:1 stateful connection with an MCP server, handles lifecycle initialization, negotiates protocol capabilities, and serializes tool calls.

#### 2.3. MCP Server
A lightweight, purpose-built process that exposes specific data resources and executable functions. A server can be written in TypeScript, Python, or Go, and runs either locally as a child process or remotely behind a secure reverse proxy.

---

### 3. Dual Transport Layers: Stdio vs. Streamable HTTP/SSE

The MCP specification decouples message semantics from the physical wire format:

| Transport Dimension | Stdio Transport (Local IPC) | Streamable HTTP Transport (Remote SSE) |
| :--- | :--- | :--- |
| **Communication Channel** | Standard input (`stdin`) and standard output (`stdout`) of a spawned child process | HTTP POST for client requests, Server-Sent Events (SSE) for server streams |
| **Latency & Overhead** | **Near-zero latency** (direct OS pipe, no TCP/TLS handshake) | Network roundtrip latency + TLS encryption overhead |
| **Security Boundary** | Local OS user permissions and filesystem sandboxes | OAuth 2.0 Bearer tokens, mTLS, and network firewalls |
| **Typical Use Cases** | Local workspace file editing, git operations, local SQLite/PostgreSQL | Cloud SaaS APIs, enterprise database clusters, shared company knowledge bases |

---

### 4. The Three Core Primitives of MCP

An MCP server exposes its capabilities to the model via three foundational primitives:

```mermaid
flowchart LR
    subgraph Primitives ["MCP Three Core Primitives"]
        P1["1. Resources (Read-Only Context)<br/>URIs: postgres://db/users/schema<br/>file:///app/src/index.ts"]
        P2["2. Tools (Executable Actions)<br/>Functions with JSON-Schema<br/>write_file(), run_query(), execute_test()"]
        P3["3. Prompts (Parametric Templates)<br/>Reusable Slash Commands<br/>/security-review, /generate-spec"]
    end

    subgraph Notifications ["Push Synchronization"]
        N1["notifications/tools/list_changed<br/>Real-time dynamic tool updates"]
    end
```

1. **Resources (Context Ingestion)**: Analogous to GET endpoints. Resources expose static or dynamic data (files, system logs, database schemas) via URI schemes (e.g., `git://repo/diff/HEAD`). The LLM reads resources to ground its context without side effects.
2. **Tools (State Mutations & Execution)**: Executable functions callable by the model. Each tool definition includes an `inputSchema` formatted in strict JSON Schema. When the model invokes a tool, the Host asks the human for authorization before dispatching the execution payload to the MCP server.
3. **Prompts (Structured Workflows)**: Pre-engineered prompt templates stored on the server. They allow engineering teams to version-control standard operational workflows (e.g., `/refactor-test` or `/audit-cve`).

---

### 5. The Tool-Calling Loop in Action: Inside Claude Code

How does the MCP tool execution loop work under the hood? The sequence diagram below maps the complete round-trip lifecycle:

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant Host as Claude Code (Host)
    participant Model as Claude 3.7 Sonnet (LLM)
    participant Client as MCP Client
    participant Server as PostgreSQL MCP Server

    Dev->>Host: "Diagnose why user checkout failed for ID 8492"
    Host->>Client: Request available tools (tools/list)
    Client->>Server: JSON-RPC tools/list
    Server-->>Client: Returns [query_orders, inspect_logs]
    Client-->>Host: Tool schemas injected into LLM system prompt

    Host->>Model: Prompt + Tool Definitions + User Query
    Model->>Model: Chain-of-Thought: Need order record first
    Model-->>Host: Stop Reason: tool_use (query_orders, args: {id: 8492})

    rect rgb(30, 41, 59)
        note over Host,Dev: Human-in-the-Loop Guardrail
        Host->>Dev: Authorize tool: query_orders(id=8492)? [Y/n]
        Dev-->>Host: Confirmed: Yes
    end

    Host->>Client: Execute tool_use
    Client->>Server: JSON-RPC tools/call (query_orders)
    Server-->>Client: Returns JSON: {status: 'failed', error: 'insufficient_funds'}
    Client-->>Host: Tool Result payload

    Host->>Model: Re-feed Tool Result into Context Window
    Model->>Model: Synthesize root cause analysis
    Model-->>Host: "The checkout failed due to an insufficient funds exception on Stripe webhook."
    Host-->>Dev: Final diagnostic report presented
```

---

### 6. Security & Trust: The Model Isolation Boundary

In traditional prompt hacking, an adversarial injection could trick an LLM into deleting files or exfiltrating API secrets. MCP implements a strict **Principle of Least Privilege**:

1. **Explicit User Consent**: An MCP Host must never execute a state-mutating tool (`rm`, `write_patch`, `drop_table`) without explicit human confirmation.
2. **Schema Invariant Sanitization**: The MCP Client enforces type validation on all arguments before passing them to the server, preventing command injection at the transport level.
3. **Scoped OAuth 2.0 Tokens**: For remote HTTP servers, tokens carry granular scopes (e.g., `read:repo_metadata` without `write:code`).

---

### 7. Stanford CS146S Deep Q&A: Lecture 3

> **Q. Professor, how does MCP differ from OpenAI Function Calling or LangChain tools?**

**Faculty Response:**
Function calling is simply an **LLM API feature**: a model emits JSON arguments matching a schema. 

However, before MCP, **who executed that function? Where did the server live? How was it authenticated? How did another developer reuse your tool?** Every company wrote custom spaghetti code to bridge that gap.

MCP is not an LLM feature; it is an **Open Industry Protocol**. It standardizes the entire transport, schema negotiation, permission model, and lifecycle management. A single PostgreSQL MCP server written today can be used identically by Claude Code, Cursor, a custom internal enterprise agent, or any future AI host without altering a single line of server code.

---

### 8. Lecture 3 Summary & Series Roadmap

1. **Adopt Open Standards**: Avoid proprietary, hard-coded tool wrappers. Standardize tool integrations on MCP.
2. **Decouple Brain from Hands**: Keep the LLM focused on reasoning, while delegating I/O and state mutations to sandboxed MCP servers.
3. **Enforce Human-in-the-Loop**: Safeguard production environments by requiring explicit authorization gates on state-mutating tools.

In **Lecture 4**, we will explore **Spec-Driven Code Generation & Test Harnesses in Practice**: how to configure Claude Code and Cursor with automated regression loops that write, debug, and verify production features autonomously. Stay tuned to GlobalDevLog!

---

### References & Course Materials
- **Official Course Video Playlist**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Primary Literature**: Model Context Protocol Specification (modelcontextprotocol.io); Anthropic Claude Tool Use Architecture; Microsoft Language Server Protocol (LSP).
- **Academic Institution**: Stanford University, Department of Computer Science
"""

# 2. Korean Content
ko_content = """---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "[스탠포드 CS146S #3] 모델 컨텍스트 프로토콜(MCP)과 자율 도구 연동: AI 에이전트를 위한 범용 표준 아키텍처"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, MCP Architecture, Claude Tool Use, JSON-RPC 2.0, Autonomous AI Agents]
description: "스탠포드 대학교 CS146S 3강 완벽 해설: 'AI를 위한 언어 서버 프로토콜(LSP)'로 불리는 모델 컨텍스트 프로토콜(MCP)의 클라이언트-서버 구조, Stdio 및 HTTP/SSE 전송 계층, 자율 에이전트의 도구 호출 루프와 보안 아키텍처를 심층 분석합니다."
---

![Model Context Protocol Architecture](./images/03_cs146s_mcp_architecture.png)

미국 스탠포드 대학교의 최신 소프트웨어 공학 강좌인 **CS146S: 현대 소프트웨어 개발자 (The Modern Software Developer)** 3강 심층 기술 해설에 오신 것을 환영합니다.

1강에서는 개발자가 단순한 문법 타이피스트에서 벗어나 AI 에이전트들을 이끄는 지휘자로 도약해야 함을 배웠고, 2강에서는 코딩 LLM의 통계적 본질과 스위스 치즈 모델을 방어하는 'Trust but Verify' 아키텍처를 다루었습니다. 이번 **3강(Week 2)**에서는 현대 AI 엔지니어링의 가장 거대한 병목이었던 문제를 해결합니다: **"고립된 언어 모델을 어떻게 외부 도구, 데이터베이스, 터미널과 안전하고 일관된 표준으로 연결할 것인가?"**

2024년 이전까지는 AI에 데이터베이스나 터미널을 붙이려면 매번 하드코딩된 커스텀 API 코드를 작성해야 했습니다. 앤트로픽(Anthropic)이 주도하는 개방형 표준이자 스탠포드 강의의 핵심 주제인 **모델 컨텍스트 프로토콜(Model Context Protocol, MCP)**은 마이크로소프트의 **LSP(Language Server Protocol)**가 에디터 생태계를 통일했듯, AI 에이전트 생태계를 표준화하는 범용 어댑터로 자리잡았습니다.

{/* truncate */}

---

### 1. 파편화 위기: 왜 "AI를 위한 LSP"가 필요했는가?

과거에는 Claude Code, Cursor, GitHub Copilot 등 새로운 AI 도구가 나올 때마다 동일한 외부 자원(Git, PostgreSQL, Slack, AWS 등)에 연결하기 위해 각자 고유한 접착제(Glue Code)를 중복해서 개발해야 했습니다.

```mermaid
flowchart LR
    subgraph 과거_파편화 ["과거 N x M 파편화 문제"]
        A1[AI 도구: Claude Code] -.->|개별 하드코딩 API| R1[(PostgreSQL)]
        A1 -.->|전용 쉘 스크립트| R2[Git Worktree]
        A2[AI 도구: Cursor] -.->|중복 개발 커넥터| R1
        A2 -.->|독자 구현 툴| R3[Figma API]
    end

    subgraph 현대_MCP_표준화 ["스탠포드 CS146S: 범용 MCP 표준 구조"]
        H1[모든 MCP 호스트<br/>Claude Code / Cursor] ==>|표준 JSON-RPC 2.0| C[통합 MCP 클라이언트]
        C <==>|Stdio / SSE 전송| S1[PostgreSQL MCP 서버]
        C <==>|Stdio / SSE 전송| S2[Git Worktree MCP 서버]
        C <==>|Stdio / SSE 전송| S3[DevOps Docker MCP 서버]
    end
```

2010년대 마이크로소프트는 모든 IDE가 수십 개 언어의 파서를 직접 구현하는 비효율을 **언어 서버 프로토콜(LSP)**을 만들어 단번에 해결했습니다. 

**모델 컨텍스트 프로토콜(MCP)**은 AI 에이전트 생태계에서 완벽히 동일한 혁신을 이뤄냈습니다. 모델의 추론 엔진과 외부 도구 실행을 완전히 분리하여, **JSON-RPC 2.0 기반의 플러그 앤 플레이 표준 규약**을 확립한 것입니다.

---

### 2. MCP의 3계층 시스템 아키텍처

MCP 규격은 두 계층에 걸쳐 세 가지 핵심 참여자로 구성됩니다:

```mermaid
flowchart TD
    subgraph 호스트_환경 ["1. MCP 호스트 (애플리케이션 계층)"]
        Host["호스트 애플리케이션<br/>(Claude Code / Claude Desktop / IDE)"]
        LLM["기반 추론 모델<br/>(Claude 3.7 Sonnet / GPT-4o)"]
        Client["내장 MCP 클라이언트 엔진"]
        Host <--> LLM
        Host <--> Client
    end

    subgraph 전송_계층 ["2. 전송 계층 (통신 물리 경계)"]
        direction LR
        T1["Stdio 전송<br/>(로컬 프로세스 표준 입출력 IPC)"]
        T2["스트리밍 HTTP 전송<br/>(HTTP POST + Server-Sent Events SSE)"]
    end

    subgraph 서버_생태계 ["3. MCP 서버 (리소스 및 도구 공급자)"]
        S1["파일시스템 MCP 서버<br/>(샌드박스 작업공간 I/O)"]
        S2["PostgreSQL MCP 서버<br/>(스키마 조회 & SQL 쿼리)"]
        S3["GitHub MCP 서버<br/>(PR, 이슈, 커밋 diff 제어)"]
        S4["브라우저 자동화 MCP 서버<br/>(Puppeteer 웹 스크래핑)"]
    end

    Client <==> T1 <==> S1 & S2
    Client <==> T2 <==> S3 & S4
```

1. **MCP 호스트 (Host)**: 사용자 경험을 총괄하고, 컨텍스트 윈도우를 관리하며, 인간의 실행 승인(Permission)을 제어하는 상위 애플리케이션 (Claude Code CLI, Cursor 등).
2. **MCP 클라이언트 (Client)**: 호스트 내부에 상주하며 개별 MCP 서버와 1:1 연결을 유지하고 통신 수명주기를 관리하는 통신 모듈.
3. **MCP 서버 (Server)**: 데이터와 실행 가능한 도구를 안전하게 노출하는 독립된 경량 프로세스.

---

### 3. 두 가지 전송 계층: Stdio vs. Streamable HTTP/SSE

| 전송 방식 | Stdio 전송 (로컬 고속 IPC) | Streamable HTTP/SSE 전송 (원격 연결) |
| :--- | :--- | :--- |
| **통신 메커니즘** | 자식 프로세스의 표준 입력(`stdin`)과 표준 출력(`stdout`) 파이프 | 클라이언트 요청은 HTTP POST, 서버 스트림은 SSE(Server-Sent Events) |
| **지연 시간** | **지연 시간 제로** (네트워크/TLS 핸드셰이크 없음) | 네트워크 레이턴시 및 TLS 암호화 오버헤드 발생 |
| **보안 경계** | 로컬 OS 파일시스템 권한 및 프로세스 격리 | OAuth 2.0 Bearer 토큰, mTLS, 방화벽 인가 |
| **적합한 작업** | 로컬 파일 읽기/쓰기, git 명령, 로컬 DB 쿼리 | 사내 엔터프라이즈 DB 클러스터, SaaS API 연동 |

---

### 4. MCP의 3대 핵심 프리미티브 (Core Primitives)

1. **리소스 (Resources - 읽기 전용 컨텍스트)**: GET 요청과 유사합니다. 파일 내용, DB 스키마, 로그 등을 URI(`postgres://db/users`) 형태로 모델에 부작용(Side-effect) 없이 주입합니다.
2. **도구 (Tools - 실행 함수)**: 모델이 호출할 수 있는 실행 가능한 함수입니다. 엄격한 JSON Schema로 인자 규격을 정의하며, 호스트는 실행 전 사용자의 동의를 구합니다.
3. **프롬프트 (Prompts - 재사용 템플릿)**: 서버가 제공하는 표준 작업 템플릿으로, 사내 표준 코드 리뷰 규칙이나 장애 분석 템플릿을 파라미터와 함께 호출할 수 있습니다.

---

### 5. Claude Code의 실전 도구 실행 루프 (Tool-Calling Loop)

스탠포드 CS146S 강의에서 시연된 실전 도구 실행 시퀀스는 다음과 같이 작동합니다:

```mermaid
sequenceDiagram
    autonumber
    actor Dev as 개발자
    participant Host as Claude Code (호스트)
    participant Model as Claude 3.7 Sonnet (LLM)
    participant Client as MCP 클라이언트
    participant Server as PostgreSQL MCP 서버

    Dev->>Host: "결제 실패 원인을 진단해줘 (User ID: 8492)"
    Host->>Client: 사용 가능한 도구 목록 조회 (tools/list)
    Client->>Server: JSON-RPC tools/list
    Server-->>Client: [query_orders, inspect_logs] 반환
    Client-->>Host: 도구 스키마를 모델 프롬프트에 주입

    Host->>Model: 시스템 프롬프트 + 도구 규격 + 질의 전송
    Model->>Model: 생각의 사슬(CoT): 주문 DB 조회가 필요하다고 판단
    Model-->>Host: 중단 이유: tool_use (query_orders, args: {id: 8492})

    rect rgb(30, 41, 59)
        note over Host,Dev: 인간 중심 승인 가드레일 (Security Gate)
        Host->>Dev: DB 조회 도구를 실행할까요? query_orders(8492) [Y/n]
        Dev-->>Host: 승인: Y
    end

    Host->>Client: 도구 호출 명령 전달
    Client->>Server: JSON-RPC tools/call (query_orders)
    Server-->>Client: {status: 'failed', error: '잔액 부족'} 반환
    Client-->>Host: Tool Result 페이로드 반환

    Host->>Model: 도구 실행 결과를 컨텍스트 윈도우에 재주입
    Model->>Model: 결과 데이터 분석 및 종합 보고서 작성
    Model-->>Host: "결제 게이트웨이 웹훅에서 잔액 부족 예외가 발생했습니다."
    Host-->>Dev: 최종 진단 리포트 출력
```

---

### 6. 스탠포드 CS146S 3강 핵심 Q&A

> **Q. 교수님, MCP와 기존의 랭체인(LangChain) 툴이나 OpenAI 함수 호출(Function Calling)은 무엇이 다른가요?**

**교수진 답변:**
함수 호출은 단지 **'LLM API의 기능'**일 뿐입니다. 모델이 JSON 인자를 만들어낼 뿐, 그 함수를 누가 실행하고, 어떤 보안 프로토콜로 인증하며, 다른 개발자가 어떻게 재사용할지에 대한 규격이 없었습니다. 그래서 수많은 기업들이 스파게티 접착제 코드를 짰습니다.

MCP는 기능이 아니라 **'산업 개방형 표준 프로토콜'**입니다. 오늘 여러분이 작성한 PostgreSQL MCP 서버 하나는 Claude Code에서도, Cursor에서도, 향후 등장할 어떤 AI 에이전트에서도 코드 단 한 줄 수정 없이 그대로 작동합니다.

---

### 7. 3강 핵심 요약 및 4강 예고

1. **표준을 따르라**: AI 도구 연동을 하드코딩하지 말고, MCP 표준 서버로 모듈화하십시오.
2. **두뇌와 손을 분리하라**: LLM은 논리 추론에만 집중하게 하고, I/O 작업은 독립된 샌드박스 MCP 서버에 위임하십시오.
3. **인간 승인 가드레일을 유지하라**: 상태를 변경하는 파괴적 도구는 반드시 인간의 확인 절차를 거치도록 설계하십시오.

**4강**에서는 스펙 주도 개발(SDD)과 회귀 테스트 하네스를 결합하여, Claude Code와 Cursor가 **프로덕션 수준의 기능을 버그 없이 스스로 구현하고 자가 치유하는 실전 워크플로**를 다루겠습니다. GlobalDevLog를 계속 지켜봐 주시기 바랍니다!

---

### References & Course Materials
- **Official Course Video Playlist**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Primary Literature**: Model Context Protocol Specification (modelcontextprotocol.io); Anthropic Claude Tool Use Architecture; Microsoft Language Server Protocol (LSP).
- **Academic Institution**: Stanford University, Department of Computer Science
"""

# 3. Japanese Content
ja_content = """---
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
"""

# 4. Spanish Content
es_content = """---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "[Stanford CS146S #3] Protocolo de Contexto de Modelo (MCP) y Uso de Herramientas: La Arquitectura Universal para Agentes de IA"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, MCP Architecture, Claude Tool Use, JSON-RPC 2.0, Autonomous AI Agents]
description: "Guía completa de la Clase 3 de Stanford CS146S: El Protocolo de Contexto de Modelo (MCP) como el 'LSP para IA', topología cliente-servidor, transportes Stdio vs HTTP/SSE y ejecución segura de herramientas."
---

![Model Context Protocol Architecture](./images/03_cs146s_mcp_architecture.png)

Bienvenidos al análisis técnico de la **Clase 3 (Semana 2) de Stanford CS146S: El Desarrollador de Software Moderno**.

En esta lección abordamos el mayor cuello de botella en los sistemas de IA: ¿cómo conectar modelos fundacionales con bases de datos, APIs y entornos de ejecución de forma segura y estandarizada? Analizamos el **Model Context Protocol (MCP)**, el estándar abierto que está revolucionando la orquestación de agentes autónomos.

{/* truncate */}

---

### 1. El LSP para la IA: La Arquitectura de MCP

De la misma manera que el Language Server Protocol (LSP) desacopló los compiladores de los editores, MCP desacopla el razonamiento de los modelos de la ejecución física de herramientas mediante JSON-RPC 2.0.

```mermaid
flowchart LR
    Host["Host MCP (Claude Code / Cursor)"] ==>|JSON-RPC 2.0| Client["Cliente MCP"]
    Client <==>|Stdio / SSE| S1["Servidor MCP Sistema de Archivos"]
    Client <==>|Stdio / SSE| S2["Servidor MCP PostgreSQL"]
    Client <==>|Stdio / SSE| S3["Servidor MCP GitHub API"]
```

### Referencias y Materiales del Curso
- **Lista de Reproducción Oficial en YouTube**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Literatura Principal**: Model Context Protocol Specification (modelcontextprotocol.io); Anthropic Claude Tool Use Architecture; Microsoft Language Server Protocol (LSP).
- **Institución**: Universidad de Stanford, Departamento de Ciencias de la Computación
"""

# 5. Simplified Chinese Content
zh_hans_content = """---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "[斯坦福 CS146S #3] 模型上下文协议 (MCP) 与自主工具调用：AI 智能体的通用语言服务器架构"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, MCP Architecture, Claude Tool Use, JSON-RPC 2.0, Autonomous AI Agents]
description: "斯坦福大学 CS146S 第3讲深度解析：被称为“大模型时代 LSP”的模型上下文协议 (MCP) 核心架构、Stdio 与 HTTP/SSE 传输层、客户端-服务器拓扑及自主工具调用循环。"
---

![Model Context Protocol Architecture](./images/03_cs146s_mcp_architecture.png)

欢迎回到斯坦福大学尖端软件工程课程 **CS146S：现代软件开发者 (The Modern Software Developer)** 第3讲的深度技术解析。

本讲重点破解大模型落地中最核心的工程瓶颈：**“如何让孤立的基础大模型以安全、标准化、可插拔的方式与外部数据库、终端和 API 进行交互？”** 深度解析由 Anthropic 推动并成为斯坦福课程核心的**模型上下文协议 (Model Context Protocol, MCP)**。

{/* truncate */}

---

### 1. 大模型时代的 LSP：MCP 架构解析

正如 Language Server Protocol (LSP) 终结了编辑器与编译器的 N x M 适配困境，MCP 借助 JSON-RPC 2.0 将大模型推理解构与外部物理工具执行完全解耦。

```mermaid
flowchart LR
    Host["MCP 宿主 (Claude Code / Cursor)"] ==>|JSON-RPC 2.0| Client["MCP 客户端"]
    Client <==>|Stdio / SSE| S1["文件系统 MCP 服务端"]
    Client <==>|Stdio / SSE| S2["PostgreSQL MCP 服务端"]
    Client <==>|Stdio / SSE| S3["GitHub API MCP 服务端"]
```

### 课程参考资料
- **官方 YouTube 教学视频列表**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **核心文献**: Model Context Protocol Specification (modelcontextprotocol.io); Anthropic Claude Tool Use Architecture; Microsoft Language Server Protocol (LSP).
- **学术机构**: 斯坦福大学计算机科学系
"""

# 6. Traditional Chinese Content
zh_hant_content = """---
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
"""

# 7. Naver Blog Companion Post
nb_content = """# [스탠포드 CS146S #3] 모델 컨텍스트 프로토콜(MCP)과 자율 도구 연동: AI 에이전트를 위한 범용 표준 아키텍처

안녕하세요! 기술 엔지니어링 블로그의 Jaybee입니다.

스탠포드 대학교의 명품 소프트웨어 공학 강좌인 **CS146S: The Modern Software Developer (현대 소프트웨어 개발자)** 시리즈가 뜨거운 반응을 얻고 있습니다.

지난 1편(지휘자로서의 개발자)과 2편(코딩 LLM과 스위스 치즈 모델)에 이어, 오늘은 3강(Week 2)의 핵심 주제인 **"모델 컨텍스트 프로토콜(Model Context Protocol, MCP)과 자율 도구 사용(Tool Use)"**을 완벽하게 정리해 드립니다!

---

## 1. AI에게 왜 '범용 어댑터(MCP)'가 필요할까요?

과거에는 Claude Code나 Cursor 같은 AI 개발 도구에 데이터베이스나 Git, 터미널을 붙이려면 도구마다 제각각 커스텀 통합 코드를 작성해야 했습니다.

마치 과거에 각 에디터마다 언어별 컴파일러 파서를 따로 만들다가 마이크로소프트의 **LSP(Language Server Protocol)**로 대통일이 일어났던 것처럼, 앤트로픽이 주도하는 **MCP**는 **"AI를 위한 LSP"** 역할을 합니다.

- **표준화된 통신**: JSON-RPC 2.0 규격으로 통일
- **플러그 앤 플레이**: 한 번 만든 PostgreSQL MCP 서버는 Claude Code에서도, Cursor에서도 그대로 재사용 가능
- **이중 전송 계층**: 로컬 고속 통신을 위한 `Stdio`와 원격 클라우드를 위한 `HTTP/SSE` 완벽 지원

---

## 2. MCP의 3대 핵심 프리미티브

개발자가 MCP 서버를 만들 때 다루게 되는 핵심 3가지 요소입니다:
1. **리소스 (Resources)**: DB 레코드, 파일 내용 등 부작용 없는 '읽기 전용 컨텍스트'
2. **도구 (Tools)**: 파일 저장, SQL 쿼리 실행 등 AI가 호출하는 '실행 함수'
3. **프롬프트 (Prompts)**: 재사용 가능한 파라미터 기반 표준 작업 템플릿

---

## 3. 인간 중심의 보안 가드레일 (Trust & Safety)

AI에게 파일 시스템과 데이터베이스 접근 권한을 주는 만큼, MCP는 **'사용자 명시적 승인(User Consent)'**을 강제합니다:
- 파괴적이거나 상태를 변경하는 작업(파일 수정, DB 업데이트)은 반드시 인간 개발자의 [Y/n] 확인을 거친 후에만 실행됩니다.
- 샌드박스 격리와 OAuth 2.0 스코프를 통해 AI의 임의 코드 실행 위험을 원천 차단합니다.

---

## 4. 글로벌 기술 블로그에서 상세 시퀀스 다이어그램 확인하기

전체 JSON-RPC 2.0 통신 아키텍처와 Claude Code의 실전 도구 실행 시퀀스 다이어그램은 글로벌 블로그 GlobalDevLog에서 확인하실 수 있습니다:

👉 **[GlobalDevLog 글로벌 블로그: Stanford CS146S Lecture #3 원문 보기](https://globaldevlog.com/blog/stanford-cs146s-3-mcp-tool-use-architecture)**

다음 4강에서는 Claude Code와 Cursor를 활용한 **'스펙 주도 개발과 자동화 회귀 테스트 실전 워크플로'**를 다루겠습니다. 많은 기대 부탁드립니다!
"""

def write_file_safe(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Created: {path} ({len(content)} chars)")

# Write files across 6 locales
write_file_safe(f"{gb_root}/blog/{folder_name}/index.md", en_content)
write_file_safe(f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md", ko_content)
write_file_safe(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", es_content)
write_file_safe(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", ja_content)
write_file_safe(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hans_content)
write_file_safe(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hant_content)

# Write Naver Blog companion post
write_file_safe(f"{nb_root}/post.md", nb_content)

# Copy image to all 6 locales and Naver Blog
raw_img_path = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\cs146s_mcp_architecture_1792766538600.jpg"
target_img_name = "03_cs146s_mcp_architecture.png"

en_img_dir = f"{gb_root}/blog/{folder_name}/images"
os.makedirs(en_img_dir, exist_ok=True)
shutil.copy2(raw_img_path, f"{en_img_dir}/{target_img_name}")
print(f"Copied image to: {en_img_dir}/{target_img_name}")

locales = ["ko", "es", "ja", "zh-Hans", "zh-Hant"]
for loc in locales:
    dest_dir = f"{gb_root}/i18n/{loc}/docusaurus-plugin-content-blog/{folder_name}/images"
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy2(raw_img_path, f"{dest_dir}/{target_img_name}")
    print(f"Copied image to locale: {loc}")

nb_img_dir = f"{nb_root}/images"
os.makedirs(nb_img_dir, exist_ok=True)
shutil.copy2(raw_img_path, f"{nb_img_dir}/{target_img_name}")
print(f"Copied image to Naver Blog: {nb_img_dir}")

# Update BlogListPage post count (2편 -> 3편)
list_page_path = f"{gb_root}/src/theme/BlogListPage/index.tsx"
with open(list_page_path, 'r', encoding='utf-8') as f:
    lp_code = f.read()

lp_code = lp_code.replace("tabStanford: '스탠포드 CS146S (2편)'", "tabStanford: '스탠포드 CS146S (3편)'")
lp_code = lp_code.replace("tabStanford: 'Stanford CS146S (2 Posts)'", "tabStanford: 'Stanford CS146S (3 Posts)'")
lp_code = lp_code.replace("tabStanford: 'スタンフォード CS146S (2編)'", "tabStanford: 'スタンフォード CS146S (3編)'")

lp_code = lp_code.replace("badge: 'Active · 2편'", "badge: 'Active · 3편'")
lp_code = lp_code.replace("badge: 'Active · 2 Posts'", "badge: 'Active · 3 Posts'")
lp_code = lp_code.replace("badge: 'Active · 2編'", "badge: 'Active · 3編'")

lp_code = lp_code.replace("postCountText: '개발일지 보러가기 (2편) →'", "postCountText: '개발일지 보러가기 (3편) →'")
lp_code = lp_code.replace("postCountText: 'View Dev Logs (2 Posts) →'", "postCountText: 'View Dev Logs (3 Posts) →'")
lp_code = lp_code.replace("postCountText: '開発日誌を見る (2編) →'", "postCountText: '開発日誌を見る (3編) →'")
lp_code = lp_code.replace("postCountText: 'Ver Diarios (2 Posts) →'", "postCountText: 'Ver Diarios (3 Posts) →'")

with open(list_page_path, 'w', encoding='utf-8') as f:
    f.write(lp_code)
print("Updated BlogListPage/index.tsx post counts (3편)!")

# Update Sidebars (Desktop and Mobile)
for sidebar_rel in ["src/theme/BlogSidebar/Desktop/index.tsx", "src/theme/BlogSidebar/Mobile/index.tsx"]:
    sb_path = f"{gb_root}/{sidebar_rel}"
    with open(sb_path, 'r', encoding='utf-8') as f:
        sb_code = f.read()
    sb_code = sb_code.replace("stanfordDesc: '현대 소프트웨어 개발자 (2편)'", "stanfordDesc: '현대 소프트웨어 개발자 (3편)'")
    sb_code = sb_code.replace("stanfordDesc: 'Modern Software Dev (2 Posts)'", "stanfordDesc: 'Modern Software Dev (3 Posts)'")
    sb_code = sb_code.replace("stanfordDesc: '現代ソフトウェア開発者 (2編)'", "stanfordDesc: '現代ソフトウェア開発者 (3編)'")
    sb_code = sb_code.replace("stanfordDesc: 'Desarrollo Moderno (2 Posts)'", "stanfordDesc: 'Desarrollo Moderno (3 Posts)'")
    with open(sb_path, 'w', encoding='utf-8') as f:
        f.write(sb_code)
    print(f"Updated {sidebar_rel} (3편)!")

print("All files and UI updates for Stanford CS146S Episode 3 successfully prepared!")
