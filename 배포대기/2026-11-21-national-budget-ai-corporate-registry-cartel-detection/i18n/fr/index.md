---
slug: national-budget-ai-corporate-registry-cartel-detection
title: "Audit Budgétaire IA #4 : Registre DART et Prête-Noms"
authors: [jbgih]
tags: [ai-agents, corporate-registry, dart-api, graphrag, cartel-detection, devops]
date: 2026-11-21
keywords: ["Ententes Prête-Noms", "Registre DART Entreprises", "Bénéficiaire Effectif", "GraphRAG Gouvernance", "Fraude aux Enchères"]
description: "Intégration du registre des entreprises DART pour démasquer les prête-noms et les ententes contrôlées par une seule personne dans les marchés publics."
---

![Breaking Cartels: Corporate Registry & DART Integration](./images/01_national_budget_corporate_registry.png)

> 📌 **Points Clés (Key Takeaways)**
> - **Dépassement de la Limite de l'Épisode 2** : Pour identifier les prête-noms introuvables via les seuls registres de commande publique, création du client [`CorporateRegistryClient`](file:///D:/ai/antigravity/national_budget_ai/src/pipeline/corporate_registry_client.py) reliant le greffe du tribunal et la base DART.
> - **Anticipation Architecturale** :
>   1. Table de hachage tripartite unifiant numéros fiscaux, d'immatriculation et codes DART.
>   2. Seuils de significativité dans le graphe (dirigeants effectifs + détentions >50%).
> - **3 Bugs de Production Résolus** :
>   1. Récursion infinie due aux participations croisées résolue par condensation des composantes fortement connexes (SCC).
>   2. Détection des sociétés coquilles créées moins de 180 jours avant la soumission.
>   3. Déguisement 51:49 entre conjoints démasqué via des arêtes de liens familiaux.
> - **Résultat** : Démantèlement d'une entente de 130 000 $ contrôlée à 80% par un individu unique ; 17/17 tests validés.

{/* truncate */}

---

### ⚠️ Mention Légale et Anonymisation (Legal Notice)

> **[Avis] Toutes les entités ont été rigoureusement anonymisées.**  
> Les organismes publics (`Agence A`), entreprises (`Société B`, `Société C`), personnes physiques (`M. K`) et numéros de contrat ont été entièrement masqués.

---

### 1. Architecture de Gouvernance d'Entreprise et DART

```mermaid
flowchart TD
    subgraph ProcurementData ["Données des Marchés Publics"]
        A[Contrats KONEPS] --> B[Noeud Entreprise]
    end

    subgraph CorporateRegistry ["Registres Judiciaires & DART"]
        C[Registre du Commerce] --> D[CorporateRegistryClient]
        E[Divulgations DART] --> D
        D --> F[Liste des Dirigeants]
        D --> G[Registre des Actionnaires]
    end

    subgraph GovernanceGraph ["Gouvernance GraphRAG"]
        B --> H[Sous-graphe Entreprise-Personne]
        F -->|DIRECTOR_OF| H
        G -->|OWNS_SHARE_OF| H
        H --> I{Analyse de Contrôle}
        I -->|1 Personne à 80% et Dirigeant| J[🔴 Entente Contrôlée par 1 Seul Homme]
    end
```

---

### 2. Défis Anticipés et Correction des Défaillances

1. **Fragmentation des Identifiants** : Table de correspondance $O(1)$ unifiant les identifiants fiscaux et judiciaires.
2. **Boucles de Participations Croisées** : Élimination des récursions infinies par l'algorithme SCC de NetworkX.
3. **Sociétés Récentes (<180 jours)** : Alerte automatique sur les entreprises créées juste avant l'appel d'offres.
4. **Combinaison Conjugale 51:49** : Analyse conjointe des liens familiaux et des mandats d'administrateurs.

---

### 3. Validation sur 17 Suites de Tests

Preuve établie que deux soumissionnaires rivaux étaient en réalité détenus à 80% par `M. K` ; 17 suites de tests sur 17 franchies avec succès.
