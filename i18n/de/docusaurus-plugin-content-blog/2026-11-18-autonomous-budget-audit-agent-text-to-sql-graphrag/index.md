---
slug: autonomous-budget-audit-ai-agent-text-to-sql-graphrag
title: "Autonomer Haushalts-Audit-Agent: Text-to-SQL & GraphRAG"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, spec-driven-development, enterprise-ai, devops]
date: 2026-11-18
keywords: ["KI-Agenten-Architektur", "Text-to-SQL", "GraphRAG", "Spec-Driven Development", "Betrugserkennung"]
description: "Wie wir einen autonomen KI-Agenten zur Prüfung von 500 Mrd. $ Haushaltsausgaben bauten. 3 verhinderte Hürden und 3 gelöste Produktionsfehler im Detail."
---

![Autonomous Public Budget Audit Agent](./images/01_autonomous_budget_audit_agent.png)

> 📌 **Kernpunkte (Key Takeaways)**
> - **Das Ziel**: Bau eines autonomen KI-Agenten zur Überprüfung öffentlicher Haushaltsausgaben im Umfang von 500 Mrd. USD, der Vergabeverträge und unstrukturierte Dokumente analysiert, um Preisüberhöhungen und Scheinrechnungs-Kartelle aufzudecken.
> - **Präventive Architektur**: Beseitigung von LLM-Zahlenhalluzinationen durch **deterministisches Text-to-SQL**, während Netzwerkanalysen an einen **heterogenen Wissensgraphen (GraphRAG)** delegiert wurden.
> - **Gelöste reale Fehler**: (1) Fragmentierte Firmen- und Adressdaten mittels `EntityResolver` behoben; (2) Zeitlich gestaffelte Schleichvergaben via 30-Tage-Sliding-Window aufgedeckt; (3) Auditor-Misstrauen durch ein XAI-Dossier mit direkter Gesetzes- und Präzedenzfall-Bindung überwunden.
> - **Ergebnis**: 11 von 11 Test-Harness-Suiten bestanden, ein Kartell mit identischer Firmenadresse über 38,5 Mio. KRW und 70% Overhead-Verlust erfolgreich entlarvt.

{/* truncate */}

---

### Fazit für moderne Software-Entwickler:
1. **Zahlen gehören in die Datenbank**: LLMs dürfen nicht rechnen, sondern nur striktes SQL generieren.
2. **Reale Daten sind unsauber**: Sauberes Entity-Matching ist die Grundvoraussetzung für verlässliche Graphen.
3. **Erklärbarkeit schafft Rechtskraft**: Nur mit Anbindung an Gesetze und Präzedenzfälle werden KI-Warnungen von Auditoren akzeptiert.
