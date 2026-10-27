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
# LECTURE 8 FRENCH
# ==============================================================================
lec8_slug = "2026-10-29-stanford-cs146s-8"
lec8_content = """---
slug: 2026-10-29-stanford-cs146s-8
title: "[Stanford CS146S #8] Architecture logicielle IA-native & Refactoring : Découpler les monolithes, éliminer la dette sémantique et migrations autonomes à grande échelle"
authors: [jbgih]
tags: [stanford-cs146s, ai-native-architecture, software-refactoring, semantic-debt, monolith-decoupling, autonomous-migration, code-modernization]
date: 2026-10-29
keywords: [Architecture Logicielle IA-Native, Découplage Automatisé de Monolithes, Réduction de la Dette Sémantique, Refactoring Guidé par AST, Migration de Code Autonome LLM]
description: "Stanford CS146S Cours 8 : Concevoir des architectures adaptées aux agents IA — éliminer la dette sémantique, découper les monolithes via les graphes d'AST et réussir des migrations sans interruption."
---

![Architecture logicielle IA-native et refactoring à grande échelle](./images/08_cs146s_ai_native_architecture_refactoring.png)

Bienvenue dans le huitième volet de notre analyse technique du cours **Stanford CS146S : The Modern Software Developer**.

Dans les cours précédents, nous avons abordé les compétences individuelles des agents et le débogage. Dans ce **Cours 8**, le programme analyse l'impact systémique à long terme du déploiement massif d'agents IA : **Comment concevoir des architectures logicielles que les agents IA peuvent explorer et modifier sans s'effondrer sous une complexité incontrôlable ? Et comment utiliser l'IA pour découpler les monolithes historiques ?**

Les architectures traditionnelles — caractérisées par des états mutables globaux et des monolithes tentaculaires de 100 000 lignes — saturent rapidement le raisonnement des LLMs. Les professeurs de Stanford formalisent ici le concept de **dette sémantique (*Semantic Debt*)**, posent les règles de l'**architecture IA-native** et détaillent la méthode de **découplage assisté par AST**.

{/* truncate */}

---

### 1. Dette technique vs Dette sémantique

La dette technique classique (compilateurs, linters) concerne le code obsolète ou mal typé. Mais à l'ère de l'IA, une menace bien plus insidieuse émerge : **la dette sémantique**.

```mermaid
flowchart TD
    subgraph Technical_Debt ["Dette technique traditionnelle"]
        T1["Avertissements de compilation"]
        T2["Bibliothèques obsolètes"]
        T3["Erreurs de linter & syntaxe"]
        T4["Détectable par outils déterministes"]
    end

    subgraph Semantic_Debt ["Dette sémantique (Ère de l'IA)"]
        S1["Hypothèses implicites dans le code"]
        S2["Incohérences subtiles d'interfaces"]
        S3["Fragmentation du contexte"]
        S4["Code syntaxiquement valide mais intention floue"]
    end
```

La dette sémantique survient lorsque le code compile parfaitement mais que sa logique conceptuelle est tellement fragmentée qu'aucun modèle ne peut en reconstituer le sens global.

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **La dette sémantique** : Le vrai danger moderne réside dans le code syntaxiquement valide dont l'intention métier est floue et fragmentée.
2. **Architecture IA-Native** : Modularité stricte, interfaces typées et graphes de dépendances acycliques sont indispensables au raisonnement des agents.
3. **Découplage par l'AST** : Les graphes d'appels AST permettent aux agents de localiser objectivement les frontières de découpage et de générer des façades propres.
4. **Validation par shadow run** : L'exécution miroir en parallèle valide la stricte équivalence comportementale avant la bascule en production.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique
"""

# ==============================================================================
# LECTURE 9 FRENCH
# ==============================================================================
lec9_slug = "2026-10-30-stanford-cs146s-9"
lec9_content = """---
slug: 2026-10-30-stanford-cs146s-9
title: "[Stanford CS146S #9] TDD autonome & Vérification formelle : Solveurs SMT Z3, invariants basés sur les propriétés et preuves mathématiques pour le code IA"
authors: [jbgih]
tags: [stanford-cs146s, autonomous-tdd, formal-verification, z3-smt-solver, property-based-testing, software-correctness, symbolic-execution]
date: 2026-10-30
keywords: [TDD Autonome ATDD, Solveur SMT Z3 Vérification Formelle, Tests Basés sur les Propriétés Hypothesis, Preuves Mathématiques Code LLM, Synthèse d'Invariants Systèmes IA]
description: "Stanford CS146S Cours 9 : Au-delà des tests unitaires empiriques — Comment les agents IA utilisent les tests basés sur les propriétés (PBT), l'exécution symbolique et le solveur SMT Z3 pour apporter des preuves mathématiques d'exactitude."
---

![TDD autonome et vérification formelle avec le solveur SMT Z3](./images/09_cs146s_autonomous_tdd_formal_verification.png)

Bienvenue dans le neuvième volet de notre analyse technique du cours **Stanford CS146S : The Modern Software Developer**.

Dans ce **Cours 9**, le programme de Stanford aborde l'ultime frontière de l'ingénierie IA : **Comment faire confiance à des modèles de langage stochastiques pour écrire du code ultra-critique sans aucun défaut dans la finance, l'aérospatiale ou la cryptographie ?**

Comme le formulait le pionnier Edsger Dijkstra il y a 50 ans : *« Les tests de programmes peuvent montrer la présence de bugs, mais jamais leur absence ! »* Ce cours détaille la transition des tests d'exemples classiques vers le **Property-Based Testing (PBT)**, l'**exécution symbolique** et la **vérification formelle via le solveur SMT Z3**.

{/* truncate */}

---

### 1. La vérification formelle avec le solveur SMT Z3

```python
from z3 import Int, Solver, unsat

# Vérification formelle d'invariant
balance = Int('balance')
withdrawal = Int('withdrawal')
s = Solver()

# Postcondition : Le solde ne doit jamais être négatif
new_balance = balance - withdrawal
s.add(balance >= 0)
s.add(withdrawal > 0)
s.add(new_balance < 0) # Recherche d'un contre-exemple

if s.check() == unsat:
    print("Preuve mathématique : L'invariant est respecté pour toute entrée possible !")
```

Lorsque Z3 renvoie `unsat`, il est formellement démontré qu'aucun état invalide ne peut survenir, quel que soit le nombre d'exécutions.

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **Dépassement des tests par l'exemple** : Les tests unitaires classiques favorisent le surapprentissage des agents IA sur les cas nominaux.
2. **Invariants universels (PBT)** : Les tests basés sur les propriétés éprouvent des milliers de combinaisons extrêmes générées stochastiquement.
3. **Preuves formelles Z3** : Les solveurs SMT apportent des preuves mathématiques d'exactitude absolue sur les contraintes critiques.
4. **Boucle CEGAR** : Les contre-exemples fournis par le solveur guident l'agent IA pour concevoir des correctifs irréfutables.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique
"""

# ==============================================================================
# LECTURE 10 FRENCH
# ==============================================================================
lec10_slug = "2026-10-31-stanford-cs146s-10"
lec10_content = """---
slug: 2026-10-31-stanford-cs146s-10
title: "[Stanford CS146S #10] Le futur du génie logiciel : Essaims d'agents autonomes, pipelines de déploiement sans intervention humaine et gestion de flottes d'IA"
authors: [jbgih]
tags: [stanford-cs146s, autonomous-engineering, zero-human-deployments, ai-fleets, software-future, agent-swarms, system-governance]
date: 2026-10-31
keywords: [Équipes Autonomes de Génie Logiciel, Pipelines de Déploiement Sans Humain, Gestion de Flottes Logicielles IA, Gouvernance Humain-Agent, Codebases Auto-Évolutives]
description: "Le grand final de Stanford CS146S : Synthèse des 10 cours vers l'usine logicielle autonome — pipelines zero-human, pilotage de flottes d'agents IA et la vocation redéfinie de l'ingénieur humain en chef d'orchestre."
---

![Le futur du génie logiciel et les flottes d'IA](./images/10_cs146s_future_software_engineering_ai_fleets.png)

Bienvenue dans le **dixième et dernier volet** de notre série technique d'analyse du cours **Stanford CS146S : The Modern Software Developer**.

Au fil des neuf cours précédents, nous avons déconstruit le développement logiciel classique :
- **Cours 1** : Du dactylographe au chef d'orchestre de systèmes.
- **Cours 2** : Mécanique des tokens et prompt engineering.
- **Cours 3** : Intégration d'outils standardisée avec le Model Context Protocol (MCP).
- **Cours 4** : Spec-Driven Development (SDD) et boucles d'auto-réparation.
- **Cours 5** : Essaims multi-agents (Architecte-Implémenteur-Critique).
- **Cours 6** : Télémétrie d'exécution noyau et résolution d'incidents avec eBPF.
- **Cours 7** : Linters AST et analyse de teinte de sécurité dans la CI/CD.
- **Cours 8** : Modularité IA-native et découplage de monolithes.
- **Cours 9** : Preuves mathématiques et solveurs SMT Z3.

Dans cette **apothéose finale**, le cursus de Stanford réunit ces innovations en une vision unifiée : **L'usine logicielle autonome (*The Autonomous Software Factory*)**. Nous explorons la gouvernance de flottes de centaines d'agents, les autoroutes de déploiement continu sans intervention humaine et le rôle pérenne de l'ingénieur de demain.

{/* truncate */}

---

### 1. Le pipeline de déploiement sans intervention humaine : « Dark Factories » du code

Dans l'industrie, une « Dark Factory » désigne une usine entièrement robotisée fonctionnant sans personnel au sol, sans lumière et sans chauffage.

En génie logiciel émerge le même principe : **les autoroutes de déploiement continu Zero-Human** :

```mermaid
flowchart LR
    Spec[1. Spécification SPEC.md humaine] ==> Swarm[2. Essaim d'agents autonomes]
    Swarm --> Build[3. Code multi-fichiers & Tests]
    Build --> Verify[4. Vérification formelle Z3 & PBT]
    Verify --> Shadow[5. Exécution miroir en cluster]
    Shadow --> Deploy[6. Déploiement progressif Canary 100%]
    Deploy ==> Telemetry[7. Télémétrie eBPF en temps réel]
    Telemetry -.->|Anomalie détectée| Swarm
```

1. **Prise de spécification** : L'architecte humain définit les objectifs et les contraintes de sécurité.
2. **Implémentation autonome** : Les agents implémenteurs produisent code, migrations et tests en parallèle.
3. **Portails de vérification formelle** : Les solveurs Z3 certifient l'exactitude avant toute fusion.
4. **Déploiement progressif automatisé** : Rollout progressif et rollback instantané à la moindre anomalie détectée par eBPF.

---

### 2. Le mot de la fin : L'ingénieur chef d'orchestre

> **« L'IA ne remplacera pas les ingénieurs logiciels. Mais les ingénieurs qui dirigent des agents d'IA remplaceront ceux qui s'obstinent à écrire du code ligne par ligne. »**

Libéré de la saisie répétitive, l'ingénieur s'élève vers sa véritable vocation : **concepteur de systèmes, garant éthique et chef d'orchestre de la puissance computationnelle**.

---

### 📌 Synthèse Exécutive (3–5 lignes)
1. **L'usine logicielle autonome** : L'union des spécifications, essaims d'agents, solveurs Z3 et sondes eBPF permet des déploiements fluides sans intervention humaine.
2. **Gestion de flottes IA** : Le pilotage de centaines d'agents requiert des budgets de tokens stricts et des bacs à sable sécurisés.
3. **Du dactylographe au chef d'orchestre** : La valeur se déplace de la production de syntaxe vers l'architecture de systèmes et la formalisation d'invariants.
4. **Renaissance des fondamentaux** : La maîtrise des systèmes d'exploitation, des réseaux et de la logique formelle est plus cruciale que jamais.

### Références & Supports de cours
- **Playlist officielle des cours** : [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institution** : Université Stanford, Département d'Informatique
"""

# Execute French Batch 3
if __name__ == "__main__":
    print("=" * 60)
    print("Translating Stanford CS146S Lectures #8, #9, #10 into French...")
    print("=" * 60)
    save_fr_lecture(lec8_slug, lec8_content)
    save_fr_lecture(lec9_slug, lec9_content)
    save_fr_lecture(lec10_slug, lec10_content)
    print("\n[FRENCH BATCH 3 COMPLETE] Lectures 8, 9, 10 staged and saved in French!")
