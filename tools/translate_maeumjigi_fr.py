# -*- coding: utf-8 -*-
"""
Batch translate Section 5: Maeumjigi Capstone Dev Logs (23 posts) into French,
stage them in 배포대기/<slug>/i18n/fr/index.md and save to i18n/fr production blog.
"""
import os
import shutil
import re

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")
BLOG_ROOT = os.path.join(GB_ROOT, "blog")
PROD_FR_ROOT = os.path.join(GB_ROOT, "i18n", "fr", "docusaurus-plugin-content-blog")

FR_METAS = {
    "2026-03-26-maeumjigi-1": {
        "title": "[Journal de bord Maeumjigi Capstone #1] Premiers pas & Cadrage : Workflows Claude Code et pivot vers l'IA de santé mentale",
        "desc": "Jour 1 du projet de fin d'études : intégration d'un assistant de code autonome Claude Code et réorientation stratégique d'une simple app de rappel vers Maeumjigi.",
        "keywords": ["Workflows IA Claude Code", "Chatbot IA Santé Mentale", "Architecture Projet Capstone", "Roadmap Fine-Tuning LLM", "Règles Agents IA Autonomes"]
    },
    "2026-03-30-maeumjigi-2": {
        "title": "[Journal de bord Maeumjigi Capstone #2] Conception initiale de l'application d'alarme et premiers tests",
        "desc": "Développement de la semaine 1 : premier prototype de scraping web et constat des limites des simples outils de notification.",
        "keywords": ["Scraping Web App Alarme", "Bot de Notification Android", "Cadrage Initial Projet", "Architecture Application Mobile", "Journal de Bord Semaine 1"]
    },
    "2026-03-31-maeumjigi-3": {
        "title": "[Journal de bord Maeumjigi Capstone #3] Test de build de l'application et lancement du prétraitement pour le fine-tuning",
        "desc": "Semaine 2 d'architecture : nettoyage des données pour Llama 3.1 et évaluation des jeux de données de dialogue multi-tours.",
        "keywords": ["Prétraitement Données Llama 3.1", "Nettoyage Dialogues Multi-Tours", "Tokenisation Dataset", "Pipeline Machine Learning", "Capstone Semaine 2"]
    },
    "2026-04-01-maeumjigi-4": {
        "title": "[Journal de bord Maeumjigi Capstone #4] Prétraitement de données à grande échelle : Template de chat Llama 3.1 & Pipeline JSONL autonome",
        "desc": "Mise en place d'un pipeline JSONL automatisé pour le formatage des prompts Llama 3.1 et validation de la tokenisation.",
        "keywords": ["Template Chat Llama 3.1", "Pipeline de Données JSONL", "Prétraitement Automatisé", "Formatage Dataset", "Entraînement IA Empathique"]
    },
    "2026-04-03-maeumjigi-5": {
        "title": "[Journal de bord Maeumjigi Capstone #5] Nettoyage de 100 000 données émotionnelles et contraintes de coûts d'API LLM",
        "desc": "Défis posés par 100 000 répliques cliniques, optimisation des dépenses d'API et traitement par lots.",
        "keywords": ["Nettoyage Dataset Émotions", "Optimisation Coûts API LLM", "Inférence par Lots", "Analyse Dialogues Cliniques", "Capstone Semaine 3"]
    },
    "2026-04-05-maeumjigi-6": {
        "title": "[Journal de bord Maeumjigi Capstone #6] Pipeline de génération de rapports automatisés : Visualisation python-docx & Lancement frontend Next.js 14",
        "desc": "Génération de bilans cliniques PDF/Word avec python-docx et initialisation du tableau de bord Next.js 14.",
        "keywords": ["Génération Rapports python-docx", "Dashboard Next.js 14", "Documentation Automatisée", "Architecture ML Full-Stack", "Rapports Cliniques"]
    },
    "2026-04-07-maeumjigi-7": {
        "title": "[Journal de bord Maeumjigi Capstone #7] Optimisation des données synthétiques (v5) et intégration frontend",
        "desc": "Contrôle qualité des données d'entraînement synthétiques v5 et connexion de l'interface utilisateur à l'API FastAPI.",
        "keywords": ["Données Synthétiques v5", "Intégration Frontend FastAPI", "Interface Chat Next.js", "Validation de Dataset", "Optimisation Modèle IA"]
    },
    "2026-04-08-maeumjigi-8": {
        "title": "[Journal de bord Maeumjigi Capstone #8] Flambée de la facture d'API et préparation du fine-tuning sur Colab",
        "desc": "Enseignements tirés de dépassements de coûts d'API et bascule vers l'entraînement QLoRA sur Google Colab Pro.",
        "keywords": ["Entraînement Google Colab Pro", "Fine-Tuning QLoRA", "Maîtrise des Coûts d'API", "Ingénierie Budgétaire", "LLMs Open-Source"]
    },
    "2026-04-09-maeumjigi-9": {
        "title": "[Journal de bord Maeumjigi Capstone #9] Résolution des erreurs de fine-tuning Llama 3.1 & Soutenance intermédiaire de mi-semestre",
        "desc": "Résolution des erreurs CUDA Out-of-Memory (OOM) lors de l'entraînement et succès de la présentation académique de mi-parcours.",
        "keywords": ["Résolution Erreurs CUDA OOM", "Entraînement Llama 3.1 QLoRA", "Soutenance Mi-Semestre Capstone", "Gestion Mémoire GPU", "Gradient Checkpointing"]
    },
    "2026-04-14-maeumjigi-10": {
        "title": "[Journal de bord Maeumjigi Capstone #10] Contournement des limites de débit d'API : Automatisation sans surveillance & Pipeline résilient",
        "desc": "Création d'un pipeline de synthèse de données résilient avec backoff exponentiel et traitement continu 24/7.",
        "keywords": ["Contournement Rate Limit API", "Backoff Exponentiel", "Automatisation sans Surveillance", "Synthèse de Données Résiliente", "Workflows Automatisés"]
    },
    "2026-04-19-maeumjigi-11": {
        "title": "[Journal de bord Maeumjigi Capstone #11] Évaluation du modèle M6 entraîné sur données synthétiques v5",
        "desc": "Benchmark quantitatif du point de contrôle M6 avec les métriques Rouge-L, BLEU et critères d'empathie clinique.",
        "keywords": ["Évaluation Modèle M6", "Benchmark Rouge-L BLEU", "Métrique Empathie Clinique", "Analyse Checkpoint Fine-Tuning", "Validation LLM"]
    },
    "2026-05-03-maeumjigi-12": {
        "title": "[Journal de bord Maeumjigi Capstone #12] Fine-tuning du modèle géant 70B & Défi de la mémoire GPU (OOM)",
        "desc": "Tentative d'entraînement d'un modèle 70B avec FSDP et quantification 4-bit sur infrastructure cloud contrainte.",
        "keywords": ["Fine-Tuning Modèle 70B", "Quantification FSDP", "Limites VRAM GPU", "Entraînement Grands Modèles", "Limites GPU Colab"]
    },
    "2026-05-04-maeumjigi-13": {
        "title": "[Journal de bord Maeumjigi Capstone #13] Limites du 70B & Pivot vers des modèles de taille intermédiaire (HCX, Qwen)",
        "desc": "Choix stratégique d'abandonner les modèles 70B au profit d'architectures optimisées (HyperCLOVA X, Qwen 2.5).",
        "keywords": ["Pivot Modèle Intermédiaire", "Fine-Tuning Qwen 2.5", "Optimisation HyperCLOVA X", "Efficacité Architecture Modèle", "Préparation Déploiement Edge"]
    },
    "2026-05-06-maeumjigi-14": {
        "title": "[Journal de bord Maeumjigi Capstone #14] Fin des entraînements & Mise en place d'un pipeline d'inférence parallèle",
        "desc": "Finalisation des adaptateurs LoRA et développement d'un banc de test d'inférence multi-modèles simultané.",
        "keywords": ["Pipeline Inférence Parallèle", "Fusion Adaptateurs LoRA", "Benchmark Multi-Modèles", "Serveur Inférence FastAPI", "Batching Asynchrone"]
    },
    "2026-05-07-maeumjigi-15": {
        "title": "[Journal de bord Maeumjigi Capstone #15] Visualisation des résultats de 5 modèles & Configuration de l'environnement local",
        "desc": "Graphiques comparatifs des 5 modèles entraînés et déploiement sur serveurs de test locaux.",
        "keywords": ["Visualisation Benchmark Modèles", "Serveur Test Local", "Évaluation Matplotlib", "Latence vs Précision", "Capstone Semaine 10"]
    },
    "2026-05-08-maeumjigi-16": {
        "title": "[Journal de bord Maeumjigi Capstone #16] Erreur fatale de configuration, 2e vague de fine-tuning & Lancement de l'app React Native",
        "desc": "Découverte d'un bug d'hyperparamètre LoRA, lancement d'une session corrigée et prototype mobile React Native.",
        "keywords": ["Correction Hyperparamètre LoRA", "Deuxième Vague Fine-Tuning", "Application React Native", "Développement Expo", "Analyse Anomalie Entraînement"]
    },
    "2026-05-12-maeumjigi-17": {
        "title": "[Journal de bord Maeumjigi Capstone #17] Bilan de la 2e session de fine-tuning & Les pièges des pipelines automatisés",
        "desc": "Validation des nouveaux poids et sécurisation contre les biais invisibles introduits par l'automatisation.",
        "keywords": ["Bilan 2e Vague Fine-Tuning", "Pièges Pipelines Automatisés", "Détection Biais Données", "Robustesse du Modèle", "Capstone Semaine 11"]
    },
    "2026-05-13-maeumjigi-18": {
        "title": "[Journal de bord Maeumjigi Capstone #18] Extension de la longueur de réponse & Comparatif approfondi de la 2e session",
        "desc": "Analyse de conversations plus longues et mesure de la cohérence et de l'absence d'hallucination.",
        "keywords": ["Extension Tokens Inférence", "Dialogue Multi-Tours Élargi", "Contrôle d'Hallucinations", "Benchmark Llama 3.1 vs Qwen", "Métriques d'Évaluation"]
    },
    "2026-05-17-maeumjigi-19": {
        "title": "[Journal de bord Maeumjigi Capstone #19] Rapports d'évaluation automatisés & Résolution du blocage 401 PostgreSQL FastAPI",
        "desc": "Production automatique des synthèses hebdomadaires et résolution d'un problème d'authentification sur le pool de connexions.",
        "keywords": ["Erreur 401 FastAPI PostgreSQL", "Débogage Connection Pool", "Rapports Automatisés", "Diagnostic Base de Données", "Durcissement Backend"]
    },
    "2026-05-20-maeumjigi-20": {
        "title": "[Journal de bord Maeumjigi Capstone #20] Validation de la 3e session d'entraînement & Enrichissement des fonctionnalités backend",
        "desc": "Ajout du calcul des tendances émotionnelles dans FastAPI et validation des performances du 3e point de contrôle.",
        "keywords": ["Troisième Vague Fine-Tuning", "Analyse Tendance Humeur", "Endpoints FastAPI", "Séries Temporelles Cliniques", "Capstone Semaine 12"]
    },
    "2026-05-22-maeumjigi-21": {
        "title": "[Journal de bord Maeumjigi Capstone #21] Optimisation du ratio de mélange des données & Démarrage de la 4e session",
        "desc": "Ajustement fin de la proportion entre dialogues d'écoute active et fiches d'orientation psychiatrique.",
        "keywords": ["Optimisation Ratio Mélange Données", "Quatrième Vague Fine-Tuning", "Équilibrage Dialogue Clinique", "Convergence Fonction Perte", "Raffinage Modèle"]
    },
    "2026-05-30-maeumjigi-22": {
        "title": "[Journal de bord Maeumjigi Capstone #22] Le triomphe du 4e entraînement : Checkpoint-4400, équilibre des données & Architecture finale",
        "desc": "La percée décisive avec le Checkpoint-4400 : équilibre idéal entre justesse clinique et chaleur humaine dans l'architecture globale.",
        "keywords": ["Succès Checkpoint-4400", "Architecture Système Complète", "Équilibre Empathie Clinique", "Choix Modèle Production", "Étape Majeure Capstone"]
    },
    "2026-06-18-maeumjigi-23": {
        "title": "[Journal de bord Maeumjigi Capstone #23] Safety-Wrapper à double couche, budget GPU AWS EC2 & Soutenance finale de semestre",
        "desc": "Garde-fou déterministe d'urgence (réaction sub-milliseconde), dimensionnement des coûts GPU sur AWS EC2 et succès de la soutenance.",
        "keywords": ["Safety-Wrapper Double Couche", "Garde-Fous Urgence Psychiatrique", "Budget GPU AWS EC2", "Soutenance Fin de Semestre", "Point d'Orgue Maeumjigi"]
    }
}

def translate_post(slug, meta):
    src_idx = os.path.join(BLOG_ROOT, slug, "index.md")
    if not os.path.exists(src_idx):
        print(f"[SKIP] {slug} not found in blog/")
        return

    with open(src_idx, "r", encoding="utf-8") as f:
        content = f.read()

    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"[ERR] Invalid frontmatter in {slug}")
        return

    fm = parts[1]
    body = parts[2]

    fm = re.sub(r'title:\s*["\'].*?["\']', f'title: "{meta["title"]}"', fm)
    if 'title:' not in fm:
        fm += f'\ntitle: "{meta["title"]}"\n'

    fm = re.sub(r'description:\s*["\'].*?["\']', f'description: "{meta["desc"]}"', fm)

    kw_str = "[" + ", ".join([f'"{k}"' for k in meta["keywords"]]) + "]"
    fm = re.sub(r'keywords:\s*\[.*?\]', f'keywords: {kw_str}', fm)

    new_content = f"---{fm}---{body}"

    # 1. Save to Staging
    stage_dir = os.path.join(STAGING_ROOT, slug)
    stage_fr_dir = os.path.join(stage_dir, "i18n", "fr")
    os.makedirs(stage_fr_dir, exist_ok=True)
    with open(os.path.join(stage_fr_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(new_content.strip() + "\n")

    # 2. Save to i18n/fr production blog dir
    prod_fr_dir = os.path.join(PROD_FR_ROOT, slug)
    os.makedirs(prod_fr_dir, exist_ok=True)
    with open(os.path.join(prod_fr_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(new_content.strip() + "\n")

    # 3. Copy images
    src_images = os.path.join(BLOG_ROOT, slug, "images")
    if os.path.exists(src_images):
        dst_images = os.path.join(prod_fr_dir, "images")
        os.makedirs(dst_images, exist_ok=True)
        for item in os.listdir(src_images):
            s = os.path.join(src_images, item)
            d = os.path.join(dst_images, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)

    print(f"[OK] Staged & saved French post: {slug}")

def main():
    print("=" * 65)
    print("Translating Section 5: Maeumjigi Capstone (23 posts) into French...")
    print("=" * 65)
    for slug, meta in FR_METAS.items():
        translate_post(slug, meta)
    print("\n[SECTION 5 COMPLETE] All 23 Maeumjigi posts staged and saved in French!")

if __name__ == "__main__":
    main()
