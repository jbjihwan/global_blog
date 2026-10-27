---
slug: stanford-cs146s-3-mcp-tool-use-architecture
title: "[Stanford CS146S #3] Model Context Protocol (MCP) & Utilisation autonome d'outils : L'architecture Language Server universelle pour les agents IA"
authors: [jbgih]
tags: [stanford-cs146s, mcp, model-context-protocol, tool-use, claude-code, json-rpc, software-architecture]
date: 2026-10-24
keywords: [Model Context Protocol, Architecture MCP, Claude Tool Use, Protocole JSON-RPC 2.0, Agents IA Autonomes]
description: "Stanford CS146S Cours 3 : Analyse approfondie du Model Context Protocol (MCP) comme 'LSP pour l'IA', topologie client-serveur, transports Stdio vs HTTP/SSE et boucles sécurisées d'appels d'outils."
---

![Architecture du Model Context Protocol](./images/03_cs146s_mcp_architecture.png)

Bienvenue dans le troisième volet de notre analyse technique du cours **Stanford CS146S : The Modern Software Developer**.

Dans ce **Cours 3 (Semaine 2)**, le programme s'attaque au plus grand défi architectural des systèmes d'IA modernes : **Comment des modèles de fondation isolés peuvent-ils interagir de manière modulaire et sécurisée avec le monde extérieur ?**

Avant 2024, connecter un LLM à une base de données ou un terminal exigeait du code d'intégration propriétaire et fragile. En se basant sur le standard ouvert d'Anthropic, ce cours détaille le **Model Context Protocol (MCP)** — l'adaptateur universel qui accomplit pour les agents IA ce que le **Language Server Protocol (LSP)** a accompli pour les éditeurs de code modernes.

{/* truncate */}

---

### 1. La crise de la fragmentation : Pourquoi nous avions besoin d'un « LSP pour l'IA »

Historiquement, chaque outil d'IA (Cursor, Claude Code, GitHub Copilot) tentait de se connecter aux mêmes ressources d'entreprise :

```mermaid
flowchart LR
    subgraph Legacy_N_Times_M ["Le problème spaghetti hérité N x M"]
        A1[Hôte IA : Claude Code] -.->|API propriétaire| R1[(PostgreSQL)]
        A1 -.->|Script shell custom| R2[Dépôt Git]
        A2[Hôte IA : Cursor] -.->|Intégration dupliquée| R1
        A2 -.->|Hook spécifique| R3[API Figma]
    end

    subgraph Modern_MCP_Standard ["Standard MCP propre de Stanford"]
        H1[Tout hôte MCP<br/>Claude Code / Cursor] ==>|Standard JSON-RPC 2.0| C[Client MCP Universel]
        C <==>|Transport Stdio / SSE| S1[Serveur MCP PostgreSQL]
        C <==>|Transport Stdio / SSE| S2[Serveur MCP Git]
        C <==>|Transport Stdio / SSE| S3[Serveur MCP Figma]
    end
```

---

### 2. L'architecture en 3 couches de MCP

1. **Hôte MCP (Host)** : L'application qui orchestre le flux de travail de l'agent (ex. Claude Code, Cursor).
2. **Client MCP** : La couche protocolaire dans l'hôte qui gère les connexions et sérialise les messages JSON-RPC 2.0.
3. **Serveur MCP** : Un processus léger exposant des ressources ou actions standardisées (serveur Git, serveur SQL, etc.).

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **LSP pour l'IA** : Le Model Context Protocol (MCP) élimine la complexité $N 	imes M$ entre modèles et outils via un standard ouvert JSON-RPC 2.0.
2. **Architecture modulaire** : La séparation Hôte / Client / Serveur garantit une extensibilité sans faille.
3. **Transports Stdio & HTTP/SSE** : Stdio garantit une isolation et une performance maximales en local, tandis que SSE connecte les services cloud distants.
4. **Sécurité par défaut** : Le principe du moindre privilège (mode lecture seule par défaut) protège les données sensibles des actions incontrôlées des agents.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique