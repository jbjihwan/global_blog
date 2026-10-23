---
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
