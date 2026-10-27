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
# LECTURE 1 FRENCH
# ==============================================================================
lec1_slug = "2026-10-22-stanford-cs146s-1"
lec1_content = """---
slug: stanford-cs146s-1-modern-software-developer
title: "[Stanford CS146S #1] Vue d'ensemble du cours : Le développeur logiciel moderne — De la dactylographie syntaxique à la direction d'orchestre à l'ère des agents IA"
authors: [jbgih]
tags: [stanford-cs146s, agentic-workflows, spec-driven-development, human-agent-engineering, mcp, software-architecture]
date: 2026-10-22
keywords: [Stanford CS146S, Développeur Logiciel Moderne, Spec-Driven Development, Agents IA Autonomes, Model Context Protocol (MCP)]
description: "Stanford CS146S Cours 1 : La redéfinition fondamentale du développement logiciel moderne — de la saisie manuelle de code à l'orchestration d'agents IA autonomes via le Spec-Driven Development et le Loop Engineering."
---

![Stanford CS146S Développeur Logiciel Moderne](./images/01_cs146s_human_agent_orchestration.png)

Bienvenue dans l'analyse technique approfondie du cours **CS146S : The Modern Software Developer de l'Université Stanford**.

Au cours des cinq dernières décennies, l'enseignement de l'informatique a formé les développeurs à être des dactylographes rigoureux : mémoriser des syntaxes, concevoir des algorithmes à partir de zéro et écrire manuellement des milliers de lignes de code répétitif. Aujourd'hui, l'industrie logicielle traverse sa mutation la plus radicale depuis l'invention du compilateur : le passage de la **programmation manuelle** au **Human-Agent Engineering**.

Dans ce cours inaugural, nous analysons comment les leaders technologiques (Google, Meta, OpenAI) redéfinissent la productivité, pourquoi l'ingénieur devient un chef d'orchestre de systèmes et comment le **Spec-Driven Development (SDD)**, les **Workflows Agentiques** et le **Model Context Protocol (MCP)** constituent la boîte à outils essentielle du développeur moderne.

{/* truncate */}

---

### 1. Le changement de paradigme : Du typiste de syntaxe au chef d'orchestre

Dans les flux traditionnels d'ingénierie logicielle, le goulot d'étranglement a toujours été la vitesse de frappe au clavier et la charge cognitive liée à la syntaxe. Un ingénieur conçoit une architecture, la traduit en jetons de langage (Java, TypeScript, Python) et passe 70 % de son temps sur des tâches subalternes : contrôleurs REST, interfaces de schémas, tests CRUD et corrections de fautes de frappe.

Avec l'arrivée des modèles de raisonnement et des agents de code autonomes (Claude Code, Cursor, GitHub Copilot Workspace), le coût marginal de génération de code syntaxiquement valide est devenu quasi nul.

```mermaid
flowchart TD
    subgraph Traditional_Workflow ["Paradigme traditionnel : Développeur dactylographe"]
        A1[Idée architecturale humaine] -->|Frappe manuelle 70% du temps| B1[Boilerplate & Syntaxe]
        B1 -->|Écriture manuelle de tests| C1[Compilation & Débogage local]
        C1 -->|Vélocité linéaire lente| D1[Livraison d'une seule fonctionnalité]
    end

    subgraph Modern_Agentic_Workflow ["Paradigme Stanford CS146S : Développeur chef d'orchestre"]
        A2[Architecte humain : Spécification & Invariants] ==>|Spécification précise SPEC.md| B2[Escouade d'agents IA autonomes]
        B2 -->|Édition multi-fichiers via MCP| C2[Loop Engineering automatisé : Test & Auto-réparation]
        C2 -->|Feedback continu| B2
        C2 ==>|Codebase vérifiée| D2[Revue humaine d'architecture & de sécurité]
        D2 ==>|Vélocité démultipliée par 10| E2[Déploiement en production]
    end
```

Les développeurs modernes ne sont plus évalués au nombre de lignes de code écrites par jour. Ils agissent en tant qu'**Engineering Managers dirigeant une équipe d'agents IA autonomes**. Lorsqu'un responsable technique délègue des tâches, il ne dicte pas chaque touche de clavier : il fournit des spécifications claires, délimite les frontières du système et fixe des critères d'acceptation déterministes.

---

### 2. Spec-Driven Development (SDD) : « Quoi » avant « Comment »

La méthodologie centrale enseignée à Stanford CS146S est le **Spec-Driven Development (SDD)**. Dans l'assistance IA naïve, les développeurs s'expriment par des prompts conversationnels vagues comme : *« Peux-tu créer un système d'authentification ? »*

Cette approche mène inévitablement à des dérives architecturales et des hallucinations. En SDD, le livrable principal n'est pas le code brut, mais un document de spécification formel et directement exploitable par la machine (**`SPEC.md`**).

```markdown
# Modèle de spécification d'ingénierie (SPEC.md)

## 1. Contexte & Domaine métier
- Traitement idempotent des webhooks de paiement pour Stripe API v2024-06.
- Base de données : PostgreSQL 16 avec Row-Level Security (RLS) activée.

## 2. Invariants & Contraintes strictes
- Toutes les mutations de base de données DOIVENT se produire dans une transaction explicite.
- La validation de signature webhook (HMAC-SHA256) DOIT échouer immédiatement avant tout parsing de charge utile.
- Seuil de latence : temps de réponse P99 < 80 ms.

## 3. Interfaces & Schémas
- Entrée : `POST /api/v1/payments/webhook` avec mémoire tampon brute.
- Événements gérés : `payment_intent.succeeded`, `payment_intent.payment_failed`.

## 4. Exigences de vérification & Tests
- Couverture de tests unitaires > 95 % pour les rollbacks sur identifiants d'événements dupliqués.
- Test de concurrence : 50 webhooks simultanés identiques doivent produire exactement 1 insertion.
```

---

### 3. Workflows agentiques & Loop Engineering automatisé

Un concept fondateur du cours est le **Loop Engineering**. Les modèles de fondation sont probabilistes ; attendre d'un LLM qu'il génère un système distribué complexe en une seule passe sans erreur est mathématiquement irréaliste.

Le développement logiciel moderne structure le travail des agents en une boucle fermée auto-correctrice :

```mermaid
stateDiagram-v2
    [*] --> Spec_Ingestion: L'ingénieur fournit SPEC.md
    Spec_Ingestion --> Workspace_Planning: L'agent cartographie la codebase
    
    state Workspace_Planning {
        [*] --> IdentifierDependances
        IdentifierDependances --> FormulerPlanDePatch
    }

    Workspace_Planning --> Multi_File_Edit: Exécution des modifications de code
    Multi_File_Edit --> Automated_Verification: Déclenchement CI/CD & Tests unitaires
    
    state Automated_Verification {
        [*] --> LancerTests
        LancerTests --> InspecterCodeRetour
    }

    Automated_Verification --> Self_Correction: Échec de test ou erreur linter
    Self_Correction --> Multi_File_Edit: Injection de la trace d'erreur dans le contexte
    
    Automated_Verification --> Human_Review: Tous les tests passent (Exit Code 0)
    Human_Review --> Merge_Production: Validation d'architecture et de sécurité
    Merge_Production --> [*]
```

---

### 4. Model Context Protocol (MCP) : Le protocole universel

Le **Model Context Protocol (MCP)** permet aux agents de s'émanciper du simple chat pour interagir avec des outils d'ingénierie réels (systèmes de fichiers, bases de données, terminaux).

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Changement d'identité** : Le développeur passe du statut de typiste de syntaxe à celui de chef d'orchestre d'escouades d'agents IA.
2. **Spec-Driven Development (SDD)** : La rigueur d'ingénierie repose désormais sur des documents de spécification précis (`SPEC.md`).
3. **Loop Engineering & MCP** : Les architectures fiables s'appuient sur des boucles fermées d'auto-réparation et le protocole standardisé MCP.
4. **Le fardeau du relecteur** : La génération de code étant gratuite, la maîtrise des fondamentaux informatiques (systèmes d'exploitation, concurrence) devient indispensable pour auditer les failles subtiles.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique
"""

# ==============================================================================
# LECTURE 2 FRENCH
# ==============================================================================
lec2_slug = "2026-10-23-stanford-cs146s-2"
lec2_content = """---
slug: stanford-cs146s-2-coding-llms-prompt-engineering
title: "[Stanford CS146S #2] Au cœur des LLMs de code & du Prompt Engineering : Pré-entraînement, RLHF et le modèle du gruyère 'Trust but Verify'"
authors: [jbgih]
tags: [stanford-cs146s, coding-llms, prompt-engineering, rlhf, chain-of-thought, swiss-cheese-model, software-architecture]
date: 2026-10-23
keywords: [LLM de Code, Prompt Engineering, RLHF, Chain of Thought, Modèle du Gruyère Sécurité IA]
description: "Stanford CS146S Cours 2 : Les mécanismes internes des LLMs de programmation, du pré-entraînement au RLHF, le Chain-of-Thought prompting et la sécurisation via le modèle du gruyère."
---

![Au cœur des LLMs de code et du Prompt Engineering](./images/02_cs146s_coding_llms_swiss_cheese.png)

Bienvenue dans le deuxième volet de notre série technique sur le cours **Stanford CS146S : The Modern Software Developer**.

Dans le premier cours, nous avons défini le rôle de chef d'orchestre d'agents. Dans ce **Cours 2 (Semaine 1)**, le programme explore le moteur fondamental de cette transition : **les grands modèles de langage pour le code (Coding LLMs)** et la discipline du **Prompt Engineering**.

En nous appuyant sur les travaux d'Andrej Karpathy (*Deep Dive into LLMs*), d'OpenAI et de Google Cloud, ce cours dévoile comment les réseaux de neurones acquièrent leur maîtrise du code, pourquoi ils demeurent des simulateurs statistiques et comment appliquer la doctrine **« Trust but Verify »** face aux vulnérabilités du **modèle du gruyère** du code généré par IA.

{/* truncate */}

---

### 1. L'anatomie d'un LLM : Le pipeline d'entraînement en trois étapes

Pour piloter et déboguer efficacement un assistant IA, un ingénieur doit comprendre la genèse de ses poids :

```mermaid
flowchart LR
    subgraph Stage1 ["Étape 1 : Pré-entraînement"]
        D1[Milliers de milliards de tokens<br/>Web & Code GitHub] --> N1[Modèle de base Transformer<br/>Probabilité du prochain token P(w_t | Context)]
    end

    subgraph Stage2 ["Étape 2 : Supervised Fine-Tuning (SFT)"]
        N1 --> D2[Paires d'instructions de haute qualité<br/>Prompt & Réponse de référence]
        D2 --> N2[Assistant adapté aux instructions<br/>Protocole conversationnel]
    end

    subgraph Stage3 ["Étape 3 : RLHF & Alignement"]
        N2 --> D3[Classement de préférences humaines<br/>Scoring du modèle de récompense]
        D3 --> N3[LLM de code prêt pour la production<br/>Sûr, aligné et déterministe]
    end
```

---

### 2. Le modèle du gruyère de la sécurité du code IA

Aucune couche de vérification ne peut intercepter 100 % des défauts générés par une IA :

![Modèle du gruyère](./images/02_cs146s_coding_llms_swiss_cheese.png)

```mermaid
flowchart TD
    Bug[Bug potentiel généré par IA] --> Layer1["Couche 1 : Typage statique (TypeScript / Rust / mypy)"]
    Layer1 -->|Échappé par un trou de typage| Layer2["Couche 2 : Suite de tests déterministes (Unitaire & Intégration)"]
    Layer2 -->|Échappé par un trou de test| Layer3["Couche 3 : Tests basés sur les propriétés (Hypothesis)"]
    Layer3 -->|Échappé par un trou de fuzzing| Layer4["Couche 4 : Analyse de teinte & Linters AST"]
    Layer4 -->|Échappé par un trou AST| Layer5["Couche 5 : Revue humaine d'architecture et de sécurité"]
    Layer5 --> Blocked[Bug stoppé net avant la production !]
```

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Les trois étapes de fabrication** : Le pré-entraînement apporte les bases linguistiques, le SFT enseigne le suivi d'instructions, et le RLHF assure l'alignement et la sécurité.
2. **Chain-of-Thought (CoT)** : Permet au modèle d'allouer de la puissance de calcul logique intermédiaire avant d'écrire le code.
3. **Le modèle du gruyère** : Pour contrer les anomalies stochastiques de l'IA, une défense en profondeur (typage $\rightarrow$ tests $\rightarrow$ analyse AST $\rightarrow$ revue humaine) est indispensable.
4. **« Trust but Verify »** : La vitesse de l'IA n'a de valeur que si des garde-fous déterministes garantissent la robustesse du système.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique
"""

# ==============================================================================
# LECTURE 3 FRENCH
# ==============================================================================
lec3_slug = "2026-10-24-stanford-cs146s-3"
lec3_content = """---
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
1. **LSP pour l'IA** : Le Model Context Protocol (MCP) élimine la complexité $N \times M$ entre modèles et outils via un standard ouvert JSON-RPC 2.0.
2. **Architecture modulaire** : La séparation Hôte / Client / Serveur garantit une extensibilité sans faille.
3. **Transports Stdio & HTTP/SSE** : Stdio garantit une isolation et une performance maximales en local, tandis que SSE connecte les services cloud distants.
4. **Sécurité par défaut** : Le principe du moindre privilège (mode lecture seule par défaut) protège les données sensibles des actions incontrôlées des agents.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique
"""

# Execute French Batch 1
if __name__ == "__main__":
    print("=" * 60)
    print("Translating Stanford CS146S Lectures #1, #2, #3 into French...")
    print("=" * 60)
    save_fr_lecture(lec1_slug, lec1_content)
    save_fr_lecture(lec2_slug, lec2_content)
    save_fr_lecture(lec3_slug, lec3_content)
    print("\n[FRENCH BATCH 1 COMPLETE] Lectures 1, 2, 3 staged and saved in French!")
