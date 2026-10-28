---
slug: autonomous-budget-audit-ai-agent-text-to-sql-graphrag
title: "Agente de Auditoria Orçamentária: Text-to-SQL & GraphRAG"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, spec-driven-development, enterprise-ai, devops]
date: 2026-11-18
keywords: ["Arquitetura de Agentes de IA", "Text-to-SQL", "GraphRAG", "Spec-Driven Development", "Detecção de Fraude"]
description: "Como construímos um agente de IA autônomo para auditar $500B em orçamentos públicos. 3 desafios prevenidos e 3 bugs críticos resolvidos em produção."
---

![Autonomous Public Budget Audit Agent](./images/01_autonomous_budget_audit_agent.png)

> 📌 **Principais Conclusões (Key Takeaways)**
> - **O Objetivo**: Construir um agente autônomo de IA para auditar US$ 500 bilhões em gastos públicos anuais, rastreando licitações e desarticulando fraudes de superfaturamento e cartéis de empresas de fachada.
> - **Prevenção Arquitetural**: Eliminação de alucinações numéricas delegando cálculos a um motor **Text-to-SQL Determinístico**, enquanto o mapeamento de conluios foi isolado em um **Grafo de Conhecimento (GraphRAG)** em arquitetura Dual-Brain.
> - **Bugs Reais Resolvidos**: (1) Resolução da fragmentação de nomes e endereços de empresas com o `EntityResolver`; (2) Identificação de fracionamento temporal de contratos via janelas deslizantes de 30 dias; (3) Superação da desconfiança de auditores integrando gerador de dossiês XAI vinculado a leis e precedentes.
> - **Resultados**: 11 suítes de testes de regressão aprovadas com 100% de sucesso, identificando cartel de US$ 38.5M KRW e 70% de vazamento em despesas indiretas.

{/* truncate */}
