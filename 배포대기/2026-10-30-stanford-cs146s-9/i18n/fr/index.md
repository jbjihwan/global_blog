---
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