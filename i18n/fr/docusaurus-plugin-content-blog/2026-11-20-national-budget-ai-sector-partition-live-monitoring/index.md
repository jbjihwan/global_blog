---
slug: national-budget-ai-sector-partition-live-monitoring
title: "Audit Budgétaire IA #3 : Partition 3D et Portail Direct"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, live-streaming, koneps-api, web-dashboard, devops]
date: 2026-11-20
keywords: ["Partition 3D par Secteur", "API Marchés Publics Direct", "Portail Web d'Audit", "Détection Fraude IA", "Filtrage Bruit"]
description: "Filtrage de 85% du bruit des marchés publics par partition 3D et connexion aux API en temps réel pour le portail web d'audit interactif v2.0."
---

![3D Sector Partitioning & Live Audit Web Portal](./images/01_national_budget_sector_live_monitor.png)

> 📌 **Points Clés (Key Takeaways)**
> - **Fin de la Fatigue des Alertes** : Élimination de plus de 85% du bruit des fournitures courantes grâce au **Gestionnaire de Partition 3D (SectorPartitionManager)**, ciblant les capacités d'analyse sur les zones à haut risque.
> - **Prévention des Pannes d'API** : File d'attente tampon isolée en **SQLite avec retraits exponentiels** face aux coupures des API publiques.
> - **Résolution de 3 Bugs Critiques en Production** :
>   1. Délimiteur accent circonflexe (`^`) concaténant des sous-champs ➔ Parser regex et validation stricte de types.
>   2. Gel complet du navigateur lors du rendu de graphes massifs ➔ **Virtualisation par sous-graphes Ego-Network (Depth-1)**, réduisant la latence de 98%.
>   3. Alertes en double lors de la synchronisation ➔ **Hashes SHA-256** garantissant l'idempotence.
> - **Livrable** : Portail interactif pour auditeurs v2.0 validé par 13/13 tests d'intégration réussis.

{/* truncate */}

---

### ⚠️ Mention Légale et Anonymisation (Legal Notice)

> **[Avis] Toutes les entités ont été rigoureusement anonymisées.**  
> Les organismes publics (`Agence A`), entreprises (`Société A`), numéros de contrat et adresses ont été entièrement masqués.

---

### 1. Architecture de Partition 3D et Ingestion en Direct

```mermaid
flowchart TD
    subgraph DataStream ["Étape 1: Flux Temps Réel & Résilience"]
        A[API Marchés Publics] --> B[Parser Circonflexe ^]
        B --> C[Dédoublonnage SHA-256]
        C --> D[(SQLite File d'Attente Tampon)]
    end

    subgraph PartitionEngine ["Étape 2: Moteur de Partition 3D"]
        D --> E{Matrice 3D<br/>Entité × Ligne × Mode}
        E -->|85% Fournitures| F[Archive Faible Risque]
        E -->|Cibles Critiques| G[Secteur 1: TIC Saucissonnage]
        E -->|Cibles Critiques| H[Secteur 2: Ententes Événements]
        E -->|Cibles Critiques| I[Secteur 3: Fuite Subventions]
    end

    subgraph InspectorPortal ["Étape 3: Portail Web d'Audit v2.0"]
        G --> J[Orchestrateur Global]
        H --> J
        I --> J
        J --> K[Vis.js Ego-Network]
        J --> L[Base Précédents (10 ans)]
        J --> M[Contrôle Tableaux HWPX]
        J --> N[Export de Dossiers]
    end
```

---

### 2. Défis Anticipés et Solutions aux Bugs Réels

1. **Partition 3D par Secteur** : Élimination de 85% du bruit des consommables via le croisement "Type d'Organisme × Ligne Budgétaire × Mode de Passation".
2. **Caractère Circonflexe (`^`)** : Découpage sécurisé des champs d'anciennes API concaténées.
3. **Gel de l'Interface Vis.js** : Résolu par chargement à la demande des voisins directs (Depth-1).
4. **Hashes SHA-256 d'Empreinte** : Protection contre les doublons d'alertes lors des actualisations du statut des contrats.

---

### 3. Portail d'Audit v2.0 & Validation Intégrale

Accessible sur `http://localhost:8088`, le portail fournit visualisations d'ententes et production automatique de dossiers juridiques, validé par 13 tests d'intégration sans faille.
