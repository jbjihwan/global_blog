# -*- coding: utf-8 -*-
import os
import shutil

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")

def save_fr_lecture(slug, fr_content):
    # 1. Save to Staging
    stage_dir = os.path.join(STAGING_ROOT, slug)
    stage_fr_dir = os.path.join(stage_dir, "i18n", "fr")
    os.makedirs(stage_fr_dir, exist_ok=True)
    with open(os.path.join(stage_fr_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(fr_content.strip() + "\n")
    print(f"[STAGING OK] {slug} -> {stage_fr_dir}\\index.md")

    # 2. Save to i18n/fr production blog dir (ready for build)
    prod_fr_dir = os.path.join(GB_ROOT, "i18n", "fr", "docusaurus-plugin-content-blog", slug)
    os.makedirs(prod_fr_dir, exist_ok=True)
    with open(os.path.join(prod_fr_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(fr_content.strip() + "\n")
    
    # 3. Copy images from blog/<slug>/images
    src_images = os.path.join(GB_ROOT, "blog", slug, "images")
    if os.path.exists(src_images):
        dst_images = os.path.join(prod_fr_dir, "images")
        os.makedirs(dst_images, exist_ok=True)
        for item in os.listdir(src_images):
            s = os.path.join(src_images, item)
            d = os.path.join(dst_images, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
        print(f"[IMAGES OK] Copied images to {dst_images}")

# ==============================================================================
# LECTURE 4 FRENCH
# ==============================================================================
lec4_slug = "2026-10-25-stanford-cs146s-4"
lec4_content = """---
slug: stanford-cs146s-4-spec-driven-code-generation-test-harnesses
title: "[Stanford CS146S #4] Génération de code guidée par les spécifications & Test Harnesses : Construire des boucles de régression auto-réparatrices avec Claude Code & Cursor"
authors: [jbgih]
tags: [stanford-cs146s, spec-driven-development, test-harness, self-healing-code, claude-code, cursor, software-engineering, regression-testing]
date: 2026-10-25
keywords: [Spec-Driven Development, Test Harness pour Code IA, Génération de Code Auto-réparatrice, Tests Automatisés Claude Code, Vérification de Régression LLM]
description: "Stanford CS146S Cours 4 : Échapper au piège du 'vibe coding' grâce au Spec-Driven Development (SDD), construire des bancs de test en boucle fermée et automatiser les cycles Red-Green-Refactor avec Claude Code et Cursor."
---

![Génération de code guidée par les spécifications et banc de test auto-réparateur](./images/04_cs146s_spec_driven_test_harness.png)

Bienvenue dans le quatrième volet de notre analyse technique du cours **Stanford CS146S : The Modern Software Developer**.

Dans les cours précédents, nous avons exploré la transition vers le rôle de chef d'orchestre, la mécanique des LLMs de code et le Model Context Protocol (MCP). Dans ce **Cours 4 (Semaine 3)**, le programme aborde le défi pratique le plus pressant : **Comment construire de manière fiable des systèmes de milliers de lignes quand les LLMs hallucinent inévitablement et introduisent des régressions silencieuses ?**

L'approche naïve — souvent appelée sur les réseaux sociaux « vibe coding » ou programmation conversationnelle au jugé — échoue totalement en entreprise. En s'appuyant sur les travaux de recherche de Stanford, ce cours présente le **Spec-Driven Development (SDD)** et montre comment ériger un banc de test automatisé (**Test Harness**) avec **boucles de rétroaction auto-réparatrices**.

{/* truncate */}

---

### 1. Le piège du « Vibe Coding » : Pourquoi les prompts informels mènent à la dégradation

Sans spécification formelle, chaque échange conversationnel augmente l'entropie du système :

```mermaid
flowchart TD
    subgraph Vibe_Coding_Entropy ["L'anti-pattern : Vibe Coding conversationnel"]
        V1["Prompt vague : 'Ajoute le paiement'"] --> V2["Le LLM génère 300 lignes de code"]
        V2 --> V3["Le développeur survole le code (Semble plausible)"]
        V3 --> V4["Merge dans la branche principale"]
        V4 --> V5["Prompt suivant : 'Ajoute des coupons'"]
        V5 --> V6["Le LLM écrase silencieusement la logique de paiement"]
        V6 --> V7["Régression catastrophique en production"]
    end

    subgraph Spec_Driven_Determinism ["Stanford CS146S : Spec-Driven Development (SDD)"]
        S1["Spécification formelle (PRD & Contrat d'interface)"] --> S2["Suite de tests d'acceptation déterministe"]
        S2 --> S3["Génération de code par IA (Claude Code / Cursor)"]
        S3 --> S4["Exécution automatisée des tests"]
        S4 -->|Tests en échec| S5["Boucle d'auto-réparation avec traces d'erreur"]
        S5 --> S3
        S4 -->|Tous les tests passent| S6["Merge vérifié sans régression"]
    end
```

---

### 2. Le banc de test en boucle fermée (Red-Green-Refactor pour agents)

Dans le paradigme SDD, le banc de test sert de garde-fou absolu :

```mermaid
stateDiagram-v2
    [*] --> DefinitionSpec: L'ingénieur définit les invariants dans SPEC.md
    DefinitionSpec --> GenerationTests: Écriture des tests unitaires & de propriétés (RED)
    GenerationTests --> CodageAgent: L'agent IA implémente le code
    
    state Boucle_Auto_Reparation {
        [*] --> ExecutionHarness
        ExecutionHarness --> AnalyseTrace: Échec du test (Assertion Error)
        AnalyseTrace --> SynthesePatch: L'agent répare les lignes isolées
        SynthesePatch --> ExecutionHarness: Nouvel essai de test
    }
    
    CodageAgent --> Boucle_Auto_Reparation
    Boucle_Auto_Reparation --> ToutVert: Tous les tests réussis (GREEN)
    ToutVert --> Refactorisation: Nettoyage et vérification de typage
    Refactorisation --> Termine: Pull Request prête pour la production
    Termine --> [*]
```

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Fin du Vibe Coding** : Les prompts informels mènent à l'amnésie contextuelle et à des régressions catastrophiques en production.
2. **Spec-Driven Development** : Les spécifications formelles (`SPEC.md`) et les contrats d'interface constituent le vrai livrable de l'ingénieur.
3. **Boucles auto-réparatrices** : En recevant les traces d'erreur d'exécution, l'agent itère jusqu'à ce que la suite de tests soit 100 % verte.
4. **Intégrité des tests** : Les fichiers de test doivent être sanctuarisés pour empêcher l'agent de modifier les assertions à son avantage.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique
"""

# ==============================================================================
# LECTURE 5 FRENCH
# ==============================================================================
lec5_slug = "2026-10-26-stanford-cs146s-5"
lec5_content = """---
slug: 2026-10-26-stanford-cs146s-5
title: "[Stanford CS146S #5] Systèmes multi-agents & Orchestration en essaim : Coordonner les LLMs Architecte, Implémenteur et Critique"
authors: [jbgih]
tags: [stanford, cs146s, multi-agent-systems, swarm-orchestration, llm-agents, software-engineering, distributed-systems]
date: 2026-10-26
keywords: [Orchestration Multi-Agents LLM, Pattern Architecte Implémenteur Critique, Génération de Code en Essaim Autonome, Workflows DAG Agents, Protocole de Communication Inter-Agents]
description: "Stanford CS146S Cours 5 : Pourquoi les LLMs monolithiques échouent sur les grandes codebases et comment coordonner des agents spécialisés Architecte, Implémenteur et Critique via des graphes DAG asynchrones."
---

![Architecture d'orchestration en essaim multi-agents](./images/05_cs146s_multi_agent_swarm.png)

Bienvenue dans le cinquième volet de notre analyse technique du cours **Stanford CS146S : The Modern Software Developer**.

Dans les cours précédents, nous avons étudié le prompt engineering, le protocole MCP et les bancs de test auto-réparateurs. Tous reposaient sur un postulat implicite : une **session LLM unique** interagissant avec un développeur ou une codebase.

Cependant, dès qu'un projet dépasse quelques milliers de lignes de code et s'étend sur plusieurs microservices, ce paradigme monolithique s'effondre sous l'effet de la **saturation de contexte, de la dilution d'attention (*Attention Dilution*) et des biais d'auto-confirmation**.

Dans ce cours, les professeurs de Stanford dévoilent le futur de l'ingénierie logicielle IA-native : les **Systèmes Multi-Agents (MAS) et l'orchestration en essaim**. Nous examinons comment la séparation stricte des rôles entre **Architecte, Implémenteur et Critique** démultiplie la fiabilité et l'échelle des projets logiciels.

{/* truncate */}

---

### 1. Le pattern Architecte - Implémenteur - Critique (AIC)

Stanford propose une séparation fonctionnelle claire pour briser les biais cognitifs des modèles uniques :

```mermaid
flowchart LR
    User[Architecte humain / PRD] --> Arch[1. Agent Architecte Principal]
    Arch -->|Découpage en sous-tâches & Schémas API| Impl1[2a. Implémenteur Module A]
    Arch -->|Parallélisation| Impl2[2b. Implémenteur Module B]
    
    Impl1 --> Critic[3. Agent Critique & Vérificateur]
    Impl2 --> Critic
    
    Critic -->|Feedback si défauts| Impl1
    Critic -->|Tests 100% verts & Audit sécurité validé| Output[Codebase unifiée prête pour la prod]
```

1. **Lead Architect Agent** : Décompose le problème en un graphe orienté acyclique (DAG) et fige les interfaces.
2. **Implementer Agents** : Travaillent en parallèle dans des contextes isolés sans polluer leur mémoire de travail.
3. **Critic & Verifier Agent** : Effectue les revues de code et les tests de conformité. N'ayant pas écrit le code, il est totalement immunisé contre le biais d'auto-confirmation.

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Échec des modèles monolithiques** : Les agents uniques souffrent de dilution d'attention et d'amnésie sur les grands projets.
2. **Séparation des responsabilités** : L'architecture Architecte-Implémenteur-Critique garantit un développement parallèle et un contrôle qualité indépendant.
3. **Workflows en graphes DAG** : Les dépendances asynchrones permettent d'exécuter les modules sans blocage mutuel.
4. **Protocoles structurés** : Des échanges de messages au format JSON strict évitent les dérives d'interprétation.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique
"""

# ==============================================================================
# LECTURE 6 FRENCH
# ==============================================================================
lec6_slug = "2026-10-27-stanford-cs146s-6"
lec6_content = """---
slug: 2026-10-27-stanford-cs146s-6
title: "[Stanford CS146S #6] Débogage assisté par IA & Profilage d'exécution : Exploiter eBPF, le traçage dynamique et les LLMs pour la résolution d'incidents"
authors: [jbgih]
tags: [stanford, cs146s, ebpf, dynamic-tracing, ai-debugging, incident-response, site-reliability-engineering, linux-kernel]
date: 2026-10-27
keywords: [Débogage d'Exécution Assisté par IA, eBPF Traçage Dynamique LLM, Résolution Autonome d'Incidents, Observabilité Noyau IA SRE, Profilage de Performance en Production]
description: "Stanford CS146S Cours 6 : Comment la synergie entre extended Berkeley Packet Filters (eBPF) et agents diagnostiques LLM révolutionne le débogage en production — du traçage noyau sans intrusion à l'application de hotpatches automatisés."
---

![Architecture de débogage assisté par IA et traçage dynamique eBPF](./images/06_cs146s_ai_debugging_ebpf.png)

Bienvenue dans le sixième volet de notre analyse technique du cours **Stanford CS146S : The Modern Software Developer**.

Dans le cours précédent, nous avons abordé la coordination d'essaims multi-agents. Cependant, même les logiciels les plus rigoureusement testés finissent par affronter le chaos du monde réel en production.

À 3h du matin, lorsqu'un interblocage (*deadlock*) paralyse un cluster de paiement ou qu'une requête SQL non indexée fait bondir la latence à 12 secondes, les approches traditionnelles s'avèrent inopérantes. Les `printf` invasifs modifient les timings et masquent le problème (*effet Heisenbug*), et les agrégateurs de logs noient les ingénieurs SRE sous des gigaoctets de données inutiles.

Dans ce cours, les professeurs de Stanford dévoilent la nouvelle frontière de la résilience logicielle : **le débogage assisté par IA et le profilage d'exécution**. En combinant la puissance sans surcoût d'**extended Berkeley Packet Filters (eBPF)** avec des **agents LLM spécialisés en diagnostic SRE**, les équipes capturent les états du noyau en temps réel, identifient la cause racine et déploient des correctifs en quelques minutes.

{/* truncate */}

---

### 1. Observabilité noyau avec eBPF + Agent SRE

eBPF permet d'exécuter du bytecode sécurisé directement dans le noyau Linux, sans recompiler ni charger de modules externes, éliminant tout impact sur les performances :

```mermaid
sequenceDiagram
    autonumber
    participant K as Noyau Linux (Sondes eBPF)
    participant RB as Ring Buffer sans verrou
    participant D as Agent IA SRE (Diagnostiqueur LLM)
    participant GH as GitHub CI / Pipeline Hotpatch

    K->>RB: Capture de la latence des syscalls & verrous de sockets
    RB-->>D: Flux d'événements télémétriques (Flamegraph & pics de latence)
    D->>D: Analyse du trace noyau et corrélation avec le code source
    D-->>D: Cause racine identifiée : Contention de mutex dans worker_pool.rs:142
    D->>GH: Création d'une Pull Request de hotpatch avec correctif atomique
```

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Limites du débogage classique** : Les logs invasifs perturbent les conditions de course (Heisenbugs) et saturent les ingénieurs sous le bruit des logs.
2. **Précision sans surcoût d'eBPF** : Capture les appels système et contentions au niveau du noyau Linux avec un impact quasi nul.
3. **Diagnostic automatisé** : Les agents SRE analysent la télémétrie en temps réel et localisent précisément le goulot d'étranglement dans le code source.
4. **Correction express** : Du diagnostic à la synthèse d'un patch d'urgence, la durée de résolution des incidents est réduite de plusieurs heures à quelques minutes.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique
"""

# ==============================================================================
# LECTURE 7 FRENCH
# ==============================================================================
lec7_slug = "2026-10-28-stanford-cs146s-7"
lec7_content = """---
slug: 2026-10-28-stanford-cs146s-7
title: "[Stanford CS146S #7] Revue de code automatisée à l'échelle : Linters basés sur l'AST, analyse de teinte de sécurité et relecteurs de PR autonomes par LLM"
authors: [jbgih]
tags: [stanford, cs146s, code-review, static-analysis, ast, taint-analysis, llm-pr-review, devops, security]
date: 2026-10-28
keywords: [Revue de Code Automatisée à l'Échelle, Analyse Statique Basée sur l'AST, Analyse de Teinte de Sécurité LLM, Relecteur Autonome de Pull Request, Garde-fous CI IA]
description: "Stanford CS146S Cours 7 : Comment faire monter en échelle la qualité logicielle — combiner linters basés sur l'AST, analyse de teinte et relecteurs LLM sémantiques pour éliminer les débats de style et stopper les failles."
---

![Architecture de revue de code automatisée à grande échelle](./images/07_cs146s_code_review_at_scale.png)

Bienvenue dans le septième volet de notre analyse technique du cours **Stanford CS146S : The Modern Software Developer**.

Dans le cours précédent, nous avons traité la résolution d'incidents en production via eBPF. Cependant, comme tout leader technique le sait : le bug le plus économique est celui qui **n'est jamais fusionné dans la branche principale**.

Dans les organisations à haute vélocité, la revue de Pull Request (PR) est le rempart garantissant la qualité, l'intégrité architecturale et la sécurité. Mais avec la croissance des équipes, la revue humaine devient un gouffre opérationnel : les ingénieurs seniors passent 15 à 20 heures par semaine sur des détails futiles de formatage (*Bikeshedding*) et, épuisés par les volumineuses PR de 1 000 lignes (*Review Fatigue*), laissent passer de graves failles de sécurité.

Dans ce cours, les professeurs de Stanford présentent le schéma directeur d'une **Revue de code automatisée à l'échelle**. En superposant **linters AST**, **analyse de teinte de sécurité (*Taint Analysis*)** et **relecteurs autonomes par LLM**, les équipes éliminent 90 % de la pénibilité manuelle tout en interceptant les failles critiques.

{/* truncate */}

---

### 1. La hiérarchie automatisée en trois niveaux

Stanford propose une stricte division du travail de relecture :

```mermaid
flowchart TD
    PR[Nouvelle Pull Request soumise] --> Tier1["Niveau 1 : Linters AST (Tree-sitter / Semgrep)<br/>Exécution : < 2 sec. | Déterministe"]
    Tier1 -->|Erreurs syntaxiques ou frontières violées| Block1[PR bloquée avec suggestion de fix en ligne]
    
    Tier1 -->|Validé| Tier2["Niveau 2 : Analyse de teinte inter-procédurale<br/>Traçage des flux : Entrée non fiable -> Puits critique"]
    Tier2 -->|Injection SQL / XSS / RCE détectée| Block2[PR bloquée avec graphe de propagation]
    
    Tier2 -->|Validé| Tier3["Niveau 3 : Relecteur de PR autonome LLM<br/>Analyse d'intention sémantique & dérive d'architecture"]
    Tier3 -->|Validé| Human[Validation humaine finale stratégique]
```

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Automatisation contre l'épuisement** : Les revues purement humaines échouent face aux volumineuses PR en raison de la fatigue cognitive et du bikeshedding.
2. **Défense en trois niveaux** : Linters AST pour la syntaxe, analyse de teinte pour la sécurité des flux de données et LLM sémantique pour l'architecture.
3. **Accélération drastique** : 90 % des vérifications mécaniques sont validées immédiatement dans la chaîne CI/CD.
4. **Recentrage sur la valeur** : Les développeurs seniors se concentrent exclusivement sur la stratégie de conception et les décisions critiques.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique
"""

# Execute French Batch 2
if __name__ == "__main__":
    print("=" * 60)
    print("Translating Stanford CS146S Lectures #4, #5, #6, #7 into French...")
    print("=" * 60)
    save_fr_lecture(lec4_slug, lec4_content)
    save_fr_lecture(lec5_slug, lec5_content)
    save_fr_lecture(lec6_slug, lec6_content)
    save_fr_lecture(lec7_slug, lec7_content)
    print("\n[FRENCH BATCH 2 COMPLETE] Lectures 4, 5, 6, 7 staged and saved in French!")
