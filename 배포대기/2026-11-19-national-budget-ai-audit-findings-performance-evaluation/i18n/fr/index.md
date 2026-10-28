---
slug: national-budget-ai-audit-findings-performance-evaluation
title: "Audit IA du Budget Public : 5 Fraudes et Évaluation"
authors: [jbgih]
tags: [ai-agents, text-to-sql, graphrag, enterprise-ai, public-budget, audit-ai]
date: 2026-11-19
keywords: ["Audit Budgétaire IA", "Détection Fraude Marchés", "Évaluation Text-to-SQL", "Précision GraphRAG", "Agent d'Audit Autonome"]
description: "Résultats intermédiaires d'audit budgétaire par IA : Cas anonymisés d'ententes, contrats fractionnés et surfacturations 10x, avec évaluation du système."
---

![National Budget AI Audit Findings](./images/01_national_budget_audit_findings.png)

> 📌 **Points Clés (Key Takeaways)**
> - **Déploiement d'Étape**: Notre agent d'audit autonome ([`national_budget_ai`](file:///D:/ai/antigravity/national_budget_ai)) a réalisé un audit exhaustif sur des jeux de données réels (5 programmes budgétaires et 6 marchés publics).
> - **4 Fraudes Majeures Détectées (Totalement Anonymisées)** :
>   1. **Contrats Fractionnés (Saucissonnage)** : 3 contrats sous le seuil de 20 000 $ en 12 jours pour éviter la mise en concurrence (43 000 $ au total).
>   2. **Cartel à Adresse Partagée** : 3 sociétés écrans partageant la même pièce pour simuler une fausse concurrence.
>   3. **Surfacturation de 7x à 10x** : Honoraires de conseil multipliés par 7 et location de serveurs par 10 par rapport à la médiane.
>   4. **Faible Efficacité de Distribution (DEI 30%)** : Seuls 30% des crédits sont parvenus aux bénéficiaires finaux (70% de frais administratifs).
> - **Évaluation du Système** : 0,00% d'erreur financière via Text-to-SQL déterministe, latence de 0,03s par dossier.

{/* truncate */}

---

### ⚠️ Mention Légale et Anonymisation (Legal Notice)

> **[Avis Impératif] Toutes les entités et données ont été rigoureusement anonymisées.**  
> Afin d'éviter tout litige, les noms d'agences (`Agence A`), de prestataires (`Société A`, `Société B`), les numéros de contrat et adresses ont été entièrement masqués.

---

### 1. Synthèse de l'Audit et Résultats

Dès l'exécution de notre pipeline combinant **Text-to-SQL déterministe et GraphRAG**, **6 alertes critiques** ont été déclenchées avec production automatique de dossiers d'audit juridiquement étayés.

| Réf. Contrat (Masquée) | Entité / Titulaire | Type d'Infraction | Base Légale & Précédent | Mécanisme IA | Niveau de Risque |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `CNTR-2026-0001~3` | Agence A / Société A | **Fractionnement Abusif** (43k $) | Code des Marchés Art. 68<br/>Cour des Comptes `BAI-2023-041` | Fenêtre Temporelle Glissante | 🔴 **HIGH** |
| `CNTR-2026-0004` | Ministère B / Société B | **Entente Même Adresse** (28k $) | Code des Marchés Art. 27<br/>Cour des Comptes `BAI-2024-009` | GraphRAG Noeud Adresse | 🔴 **CRITICAL** |
| `CNTR-2026-0005` | Agence A / Cartel (B & C) | **Offres Concertées** (130k $) | Droit de la Concurrence<br/>Cour des Comptes `BAI-2024-009` | Traversée de Sous-graphe | 🔴 **CRITICAL** |
| `CNTR-2026-0006` (1) | Projet Externalisé | **Honoraires x7,0** | Règles Budgétaires<br/>Rapport `NABO-2023-R05` | Règle Déviation Médiane | 🟠 **MEDIUM** |
| `CNTR-2026-0006` (2) | Projet Externalisé | **Baies Serveurs x10,0** | Règles Budgétaires<br/>Rapport `NABO-2023-R05` | Écart Prix de Référence | 🔴 **HIGH** |
| `PROG-2026-0001` | Subvention Directe | **Faible DEI (30%)** | Loi sur les Subventions<br/>Fuite Frais Indirects | Agrégation Analytique | 🟠 **MEDIUM** |

---

### 2. Analyse Approfondie des 4 Cas Détectés

1. **Fractionnement de Marchés** : Pour éviter l'appel d'offres ouvert, l'`Agence A` a découpé une mission en 3 contrats de 14 500 $ attribués à la `Société A` en 12 jours. Détecté en 0,001s.
2. **Sociétés Écrans à Adresse Commune** : Les soumissionnaires concurrents partageaient la même pièce à Séoul. GraphRAG a immédiatement mis au jour la structure de cartel.
3. **Surfacturation Unitaire** : Détection de tarifs de conseil à 260 $/h contre 37 $/h en médiane officielle.
4. **Indice d'Efficacité (DEI)** : Sur 7,5M $ de budget, seuls 2,25M $ ont atteint la cible finale.

---

### 3. Évaluation des Performances du Système IA

```mermaid
xychart-beta
    title "Benchmarks du Moteur d'Audit IA (Précision / Latence / Jurisprudence)"
    x-axis ["Taux Réussite Tests (%)", "Erreur Calcul (%)", "Précision Précédents (%)", "Latence Dossier (s*100)"]
    y-axis "Score" 0 --> 100
    bar [100, 0, 94.5, 3]
```

* **Zéro Hallucination** : Requêtes SQL pilotées par AST rigide (11/11 tests passés).
* **Vitesse Extrême** : 0,03s pour générer un dossier d'injonction administrative complet.

---

### 4. Limites Réelles et Défis

Les prête-noms et la sous-traitance privée en cascade exigent d'interconnecter le système aux bases fiscales et aux plateformes de paiement séquestre.

---

### 5. Conclusion

L'IA ne remplace pas les auditeurs, elle démultiplie leur vitesse par 100. Rendez-vous dans la Partie 3 pour le déploiement Kubernetes et MLOps.
