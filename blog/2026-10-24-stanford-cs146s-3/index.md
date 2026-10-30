---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "Stanford CS146S: Model Context Protocol MCP Guide (Notes #3)"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, MCP Architecture, Claude Tool Use, JSON-RPC 2.0, Autonomous AI Agents]
description: "Master Stanford CS146S Lecture 3: Model Context Protocol (MCP) architecture, Stdio vs SSE transports, and secure tool-calling loops for AI agents."
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

In the compiler and editor ecosystem of the 2010s, Microsoft solved the $N \times M$ complexity crisis by introducing the **Language Server Protocol (LSP)**. Instead of every editor writing a custom parser for TypeScript, Rust, and Go, language teams built a single LSP server, and editors built a single LSP client.

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

---

### 5.5 Production Gotchas: Real-World MCP Engineering Traps

While the Model Context Protocol (MCP) provides a clean JSON-RPC architecture, deploying MCP servers in multi-agent production fleets introduces three subtle systems engineering hurdles:

#### Gotcha 1: OS Pipe Deadlocks on Stdio Transports (The 64KB Buffer Stall)
In Stdio transport mode, if an MCP server emits debug logging via `stdout` instead of `stderr`, or if a tool response (such as a massive git diff or directory tree) exceeds the standard operating system pipe buffer (typically 64KB on Linux/Windows), the sub-process blocks permanently on `write()` while the parent process waits for a closing newline, freezing the entire IDE.
- **Production Defense**: Enforce strict separation: `stdout` is reserved exclusively for framed JSON-RPC packets; all diagnostics must flow through `stderr`. For payload sizes exceeding 32KB, chunk the response or return a file-pointer reference.

#### Gotcha 2: SSE Stream Desynchronization on Network Hiccups
For remote MCP servers operating over Server-Sent Events (SSE), transient WiFi drops or proxy timeouts terminate the HTTP connection. If the server does not support idempotent replay tokens (`Last-Event-ID`), an in-flight tool call execution will complete on the server while the agent believes it failed, resulting in duplicate side-effects (e.g., duplicated git commits or double database inserts).
- **Production Defense**: Implement idempotency keys for all mutating tools and maintain an in-memory ring buffer of recent event IDs for seamless stream reconnection.

#### Gotcha 3: Dynamic Tool Schema Mutation Security Leaks
If an MCP server exposes dynamically mutating tool definitions based on user prompts or repository contents, prompt injection attacks can inject malicious tool descriptions that trick the agent into executing arbitrary system commands.
- **Production Defense**: Tool schemas must be declared statically at server initialization. Never dynamically evaluate tool definitions based on untrusted repository contents.

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

### 📌 3–5 Line Executive Summary
1. **The MCP Standardization Paradigm**: Model Context Protocol (MCP) serves as the "LSP for AI Agents", replacing brittle $N \times M$ custom wrappers with an open, bidirectional JSON-RPC 2.0 protocol across AI hosts and tools.
2. **Decoupling Brain from Hands**: The LLM context window remains strictly dedicated to high-level logical reasoning, delegating physical I/O and state mutations to sandboxed, isolated MCP servers.
3. **Dual Transport Architecture**: High-speed, local low-latency workflows execute via sub-millisecond Stdio pipes, while enterprise distributed agents scale via Streamable HTTP/SSE secured with OAuth 2.0.
4. **Human-in-the-Loop Security Guardrails**: Mission-critical agent deployments enforce the Principle of Least Privilege—blocking destructive disk and database state mutations until explicit developer confirmation is granted.

### References & Course Materials
- **Official Course Video Playlist**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Primary Literature**: Model Context Protocol Specification (modelcontextprotocol.io); Anthropic Claude Tool Use Architecture; Microsoft Language Server Protocol (LSP).
- **Academic Institution**: Stanford University, Department of Computer Science