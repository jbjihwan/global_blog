---
slug: national-budget-ai-sector-partition-live-monitoring
title: "Auditoria IA #3: Partição 3D e Portal Web em Tempo Real"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, live-streaming, koneps-api, web-dashboard, devops]
date: 2026-11-20
keywords: ["Partição 3D por Setores", "API de Compras Públicas", "Portal Web do Auditor", "Detecção de Fraude IA", "Filtro de Ruído"]
description: "Filtragem de 85% do ruído em compras públicas via partição 3D e conexão com APIs em tempo real no portal interativo do auditor v2.0 com Vis.js."
---

![3D Sector Partitioning & Live Audit Web Portal](./images/01_national_budget_sector_live_monitor.png)

> 📌 **Principais Conclusões (Key Takeaways)**
> - **Fim da Fadiga de Alertas**: Filtragem de mais de 85% do ruído de suprimentos rotineiros por meio do **Gerenciador de Partição 3D por Setores (SectorPartitionManager)**, focando o processamento de IA em áreas de alto risco.
> - **Prevenção Arquitetural**: Fila de buffer isolada em **SQLite com recuo exponencial** para lidar com instabilidades nas APIs públicas de compras.
> - **Resolução de 3 Bugs Críticos em Produção**:
>   1. Campos compostos com circunflexo (`^`) que quebravam esquemas ➔ Parser regex e tipagem forçada.
>   2. Travamento do navegador ao renderizar milhares de nós ➔ **Virtualização de subgrafos Ego-Network (Depth-1)** reduzindo latência em 98%.
>   3. Alertas redundantes na sincronização periódica ➔ **Hashes SHA-256** garantindo idempotência.
> - **Entrega**: Portal web interativo v2.0 em operação e 13/13 testes de integração aprovados.

{/* truncate */}

---

### ⚠️ Aviso Legal e Anonimização (Legal Notice)

> **[Aviso] Todos os dados foram estritamente anonimizados.**  
> Órgãos (`Órgão A`), empresas (`Empresa A`), números de contrato e endereços foram totalmente mascarados para evitar litígios.

---

### 1. Arquitetura de Partição 3D e Ingestão em Tempo Real

```mermaid
flowchart TD
    subgraph DataStream ["Etapa 1: Fluxo em Tempo Real e Resiliência"]
        A[API Compras Públicas] --> B[Parser Circunflexo ^]
        B --> C[Deduplicação SHA-256]
        C --> D[(SQLite Fila de Buffer)]
    end

    subgraph PartitionEngine ["Etapa 2: Motor de Partição 3D"]
        D --> E{Filtro Matricial 3D<br/>Órgão × Rubrica × Modalidade}
        E -->|85% Suprimentos| F[Arquivo de Baixo Risco]
        E -->|Alto Risco| G[Setor 1: TIC Fracionamento]
        E -->|Alto Risco| H[Setor 2: Conluio em Eventos]
        E -->|Alto Risco| I[Setor 3: Vazamento de Subsídios]
    end

    subgraph InspectorPortal ["Etapa 3: Portal do Auditor v2.0"]
        G --> J[Orquestrador E2E]
        H --> J
        I --> J
        J --> K[Vis.js Ego-Network]
        J --> L[Base de Jurisprudência (10 Anos)]
        J --> M[Parser de Custos HWPX]
        J --> N[Exportação de Dossiês]
    end
```

---

### 2. Desafios Previstos e Correção de Falhas

1. **Partição 3D**: Exclusão de 85% do ruído corriqueiro cruzando "Tipo de Órgão × Rubrica Orçamentária × Modalidade Licitatória".
2. **Caractere Circunflexo (`^`)**: Resolução com parser que desmembra registros multivalorados.
3. **Travamento de UI no Navegador**: Resoluçao com carregamento sob demanda dos vizinhos de primeiro grau (Depth-1).
4. **Hashes SHA-256**: Eliminação de renotificações duplicadas em contratos monitorados.

---

### 3. Portal do Auditor v2.0 e Validação Completa

Disponível em `http://localhost:8088`, o portal reúne visualização de conluios e geração automatizada de relatórios jurídicos, respaldado por 13/13 testes aprovados.
