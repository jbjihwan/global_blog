---
slug: autonomous-budget-audit-ai-agent-text-to-sql-graphrag
title: "Agent d'Audit Budgétaire : Text-to-SQL et GraphRAG"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, spec-driven-development, enterprise-ai, devops]
date: 2026-11-18
keywords: ["Architecture d'Agents IA", "Text-to-SQL", "GraphRAG", "Spec-Driven Development", "Détection de Fraude"]
description: "Comment nous avons développé un agent IA autonome pour auditer 500 milliards $ de budgets publics. 3 défis anticipés et 3 bugs réels résolus en production."
---

![Autonomous Public Budget Audit Agent](./images/01_autonomous_budget_audit_agent.png)

> 📌 **Points Clés (Key Takeaways)**
> - **L'Objectif**: Développer un agent IA autonome capable d'auditer 500 milliards de dollars de dépenses publiques annuelles, détectant les surfacturations, le saucissonnage de marchés et les cartels d'entreprises écrans.
> - **Architecture Préventive**: Élimination des hallucinations de calcul par un moteur **Text-to-SQL Déterministe**, couplé à un **Graphe de Connaissances (GraphRAG)** pour l'analyse des réseaux de collusion.
> - **Bugs Réels Résolus**: (1) Résolution de la fragmentation des noms d'entreprises et adresses via `EntityResolver`; (2) Détection du saucissonnage temporel de contrats via une fenêtre glissante de 30 jours; (3) Levée du scepticisme des auditeurs grâce à un dossier XAI reliant chaque alerte aux lois et à la jurisprudence.
> - **Vérification**: 11 suites de tests validées à 100%, révélant une entente illicite de 38,5 millions KRW et 70% de fuites de frais indirects.

{/* truncate */}
