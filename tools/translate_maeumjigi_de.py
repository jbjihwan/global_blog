# -*- coding: utf-8 -*-
"""
Batch translate Section 5: Maeumjigi Capstone Dev Logs (23 posts) into German,
stage them in 배포대기/<slug>/i18n/de/index.md and save to i18n/de production blog.
"""
import os
import shutil
import re

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")
BLOG_ROOT = os.path.join(GB_ROOT, "blog")
PROD_DE_ROOT = os.path.join(GB_ROOT, "i18n", "de", "docusaurus-plugin-content-blog")

DE_METAS = {
    "2026-03-26-maeumjigi-1": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #1] Erste Schritte & Planung: Claude Code KI-Workflows und der fundamentale Pivot zur mentalen Gesundheits-KI",
        "desc": "Tag 1 des Universitätsprojekts: Etablierung autonomer Claude Code KI-Workflows und der entscheidende Schwenk von einer Alarm-App zu Maeumjigi, einer KI für mentale Gesundheit.",
        "keywords": ["Claude Code KI-Workflows", "Mentale Gesundheit KI-Chatbot", "Capstone Projektarchitektur", "LLM Fine-Tuning Roadmap", "Autonome KI-Agenten Regeln"]
    },
    "2026-03-30-maeumjigi-2": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #2] Erste Alarm-App Konzeption und Testen",
        "desc": "Woche 1 Entwicklung: Bau des ersten Web-Scraper-Prototyps und Analyse der Grenzen einfacher Benachrichtigungs-Tools.",
        "keywords": ["Web Scraping Alarm-App", "Android Benachrichtigungs-Bot", "Frühe Projektplanung", "Mobile App Architektur", "Entwicklertagebuch Woche 1"]
    },
    "2026-03-31-maeumjigi-3": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #3] Alarm-App Build-Test und Start der Fine-Tuning-Vorverarbeitung",
        "desc": "Architektur-Woche 2: Start der Datenbereinigung für Llama 3.1 und Evaluierung von Multi-Turn-Dialogdatensätzen.",
        "keywords": ["Llama 3.1 Datenvorverarbeitung", "Multi-Turn Dialogbereinigung", "Dataset Tokenisierung", "Machine Learning Pipeline", "Capstone Woche 2"]
    },
    "2026-04-01-maeumjigi-4": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #4] Großangelegte Datenvorverarbeitung: Llama 3.1 Chat-Template & Autonome JSONL-Pipeline",
        "desc": "Aufbau einer automatisierten JSONL-Pipeline für Llama 3.1 Chat-Templates und Tokenisierungs-Validierung.",
        "keywords": ["Llama 3.1 Chat-Template", "JSONL Datenpipeline", "Automatisierte Vorverarbeitung", "Dataset Formatierung", "Empathie KI-Training"]
    },
    "2026-04-03-maeumjigi-5": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #5] Bereinigung von 100.000 Emotionsdaten und der Kostendruck von LLM-APIs",
        "desc": "Herausforderungen bei 100.000 klinischen Dialogpunkten, Kostenoptimierung bei API-Aufrufen und Batch-Verarbeitung.",
        "keywords": ["Emotionsdatensatz Bereinigung", "LLM API Kostenoptimierung", "Batch Inferenz Skalierung", "Klinische Dialoganalyse", "Capstone Woche 3"]
    },
    "2026-04-05-maeumjigi-6": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #6] Automatisierte Bericht-Pipeline: python-docx Visualisierung & Next.js 14 Frontend-Start",
        "desc": "Generierung automatisierter klinischer PDF/Word-Berichte mit python-docx und Initialisierung des Next.js 14 Dashboards.",
        "keywords": ["python-docx Berichtgenerierung", "Next.js 14 Dashboard", "Automatisierte Dokumentation", "Full-Stack KI-Architektur", "Klinische Berichte"]
    },
    "2026-04-07-maeumjigi-7": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #7] Optimierung synthetischer Daten (v5) und Frontend-Integration",
        "desc": "Qualitätskontrolle synthetischer Trainingsdaten v5 und Anbindung des interaktiven Frontends an das FastAPI-Backend.",
        "keywords": ["Synthetische Daten v5", "FastAPI Frontend Integration", "Next.js Chat UI", "Dataset Validierung", "KI-Modell Optimierung"]
    },
    "2026-04-08-maeumjigi-8": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #8] API-Kostenexplosion und Vorbereitung des Colab Fine-Tunings",
        "desc": "Lehren aus unerwarteten API-Rechnungen und Migration des Trainings auf Google Colab Pro mit QLoRA.",
        "keywords": ["Google Colab Pro Training", "QLoRA Fine-Tuning", "API Kostenkontrolle", "Budget-Engineering", "Open-Source LLMs"]
    },
    "2026-04-09-maeumjigi-9": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #9] Llama 3.1 Fine-Tuning Fehlerbehebung & Zwischenpräsentation Woche 6",
        "desc": "Lösung von CUDA Out-of-Memory (OOM) Fehlern beim Llama 3.1 Fine-Tuning und erfolgreiche universitäre Zwischenpräsentation.",
        "keywords": ["CUDA OOM Fehlerbehebung", "Llama 3.1 QLoRA Training", "Capstone Zwischenpräsentation", "GPU Speichermanagement", "Gradient Checkpointing"]
    },
    "2026-04-14-maeumjigi-10": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #10] Behebung von API-Rate-Limits: Unbemannte Automation & Resiliente Synthese-Pipeline",
        "desc": "Entwicklung einer robusten Daten-Synthese-Pipeline mit exponentiellem Backoff und unbemanntem 24/7 Batching.",
        "keywords": ["API Rate Limit Lösung", "Exponentieller Backoff", "Unbemannte Pipeline Automation", "Resiliente Datensynthese", "Automatisierte Workflows"]
    },
    "2026-04-19-maeumjigi-11": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #11] Evaluierung des M6-Modells auf synthetischen v5-Daten",
        "desc": "Quantitative Benchmark-Evaluierung des M6-Checkpoints mit Rouge-L, BLEU und klinischer Empathie-Metrik.",
        "keywords": ["M6 Modell Evaluierung", "Rouge-L BLEU Benchmark", "Klinische Empathie Metrik", "Fine-Tuning Checkpoint Analyse", "LLM Validierung"]
    },
    "2026-05-03-maeumjigi-12": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #12] 70B Riesenmodell Fine-Tuning & Kampf gegen GPU Out-of-Memory (OOM)",
        "desc": "Versuch des 70B-Modell-Trainings mit FSDP und 4-Bit-Quantisierung auf beschränkter Cloud-Hardware.",
        "keywords": ["70B Modell Fine-Tuning", "FSDP Quantisierung", "GPU VRAM Limitierungen", "Große Sprachmodelle Training", "Colab GPU Grenzen"]
    },
    "2026-05-04-maeumjigi-13": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #13] Grenzen des 70B-Trainings & Pivot zu Mid-Size-Modellen (HCX, Qwen)",
        "desc": "Strategischer Schwenk von schwerfälligen 70B-Modellen zu hochgradig optimierten Mid-Size-Architekturen (HyperCLOVA X, Qwen 2.5).",
        "keywords": ["Mid-Size Modell Pivot", "Qwen 2.5 Fine-Tuning", "HyperCLOVA X Optimierung", "Modellarchitektur Effizienz", "Edge Deployment Vorbereitung"]
    },
    "2026-05-06-maeumjigi-14": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #14] Abschluss des Modelltrainings & Aufbau der parallelen Inferenz-Pipeline",
        "desc": "Fertigstellung aller LoRA-Adapter und Implementierung einer parallelen Multi-Model-Inferenz-Pipeline zur Evaluierung.",
        "keywords": ["Parallele Inferenz Pipeline", "LoRA Adapter Zusammenführung", "Multi-Modell Benchmark", "FastAPI Inferenz Server", "Asynchrones Batching"]
    },
    "2026-05-07-maeumjigi-15": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #15] Visualisierung der Ergebnisse von 5 Modellen & Lokales Environment-Setup",
        "desc": "Vergleichende Benchmark-Diagramme für 5 feingetunte Modelle und Bereitstellung auf lokalen Testservern.",
        "keywords": ["Modell Benchmark Visualisierung", "Lokales Server Setup", "Matplotlib Evaluierung", "Latenz vs Genauigkeit", "Capstone Woche 10"]
    },
    "2026-05-08-maeumjigi-16": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #16] Fataler Konfigurationsfehler, 2. Fine-Tuning-Runde & React Native App-Start",
        "desc": "Aufdeckung eines LoRA-Hyperparameterfehlers, Start der bereinigten 2. Trainingsrunde und Prototyping der mobilen React Native App.",
        "keywords": ["LoRA Hyperparameter Korrektur", "2. Fine-Tuning Runde", "React Native Mobile App", "Expo Entwicklung", "Fehleranalyse Training"]
    },
    "2026-05-12-maeumjigi-17": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #17] Abschluss der 2. Trainingsrunde & Die Tücken automatisierter Pipelines",
        "desc": "Erfolgreiche Fertigstellung der 2. Fine-Tuning-Runde und Absicherung gegen unbemerkte Datenverzerrungen.",
        "keywords": ["2. Fine-Tuning Abschluss", "Automatisierte Pipeline Fallen", "Datenverzerrung Erkennung", "Modell Robustheit", "Capstone Woche 11"]
    },
    "2026-05-13-maeumjigi-18": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #18] Erweiterung der Inferenz-Tokens & Detaillierter Vergleich der 2. Trainingsrunde",
        "desc": "Analyse längerer Konversations-Tokens und Messung von Konsistenz und Halluzinationsfreiheit.",
        "keywords": ["Inferenz Token Erweiterung", "Multi-Turn Konversation", "Halluzinationsprüfung", "Llama 3.1 vs Qwen Benchmark", "Evaluierungsmetriken"]
    },
    "2026-05-17-maeumjigi-19": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #19] Automatisierte Evaluierungsberichte & FastAPI PostgreSQL 401 Debugging",
        "desc": "Generierung wöchentlicher Fortschrittsberichte und Lösung eines PostgreSQL-Authentifizierungs-Deadlocks unter Last.",
        "keywords": ["FastAPI PostgreSQL 401", "Connection Pool Debugging", "Automatisierte Berichte", "Datenbank Fehlersuche", "Backend Härtung"]
    },
    "2026-05-20-maeumjigi-20": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #20] Abschluss der 3. Trainingsrunde & Backend-Funktionserweiterungen",
        "desc": "Integration von Stimmungs-Trendanalysen in FastAPI und Fertigstellung der 3. Modelliteration.",
        "keywords": ["3. Fine-Tuning Runde", "Stimmungstrend Analyse", "FastAPI Endpunkte", "Klinische Zeitreihen", "Capstone Woche 12"]
    },
    "2026-05-22-maeumjigi-21": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #21] Optimierung der Datenmischungsverhältnisse & Start der 4. Trainingsrunde",
        "desc": "Feinabstimmung des Mischungsverhältnisses zwischen klinischen Fachdialogen und Empathie-Konversationen.",
        "keywords": ["Datenmischungsverhältnis Optimierung", "4. Fine-Tuning Runde", "Klinischer Dialog Ausgleich", "Loss Funktion Konvergenz", "Modell Feinschliff"]
    },
    "2026-05-30-maeumjigi-22": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #22] Der Triumph des 4. Trainings: Checkpoint-4400, Datenmischung & Gesamtsystem-Architektur",
        "desc": "Der Durchbruch mit Checkpoint-4400: Perfekte Balance aus klinischer Schärfe und menschlicher Wärme in der Gesamtsystemarchitektur.",
        "keywords": ["Checkpoint-4400 Durchbruch", "Gesamtsystem Architektur", "Klinische Empathie Balance", "Produktionsmodell Auswahl", "Capstone Meilenstein"]
    },
    "2026-06-18-maeumjigi-23": {
        "title": "[Maeumjigi Capstone Entwicklertagebuch #23] Zweistufiger Safety-Wrapper, AWS EC2 GPU-Budgetierung & Semesterabschluss-Verteidigung",
        "desc": "Deterministische Krisen-Schutzschicht (Sub-Millisekunden-Guardrail), AWS EC2 Inferenzkosten-Kalkulation und erfolgreiche Abschlussverteidigung.",
        "keywords": ["Zweistufiger Safety-Wrapper", "Krisenintervention Guardrails", "AWS EC2 Inferenzkosten", "Semesterabschluss Verteidigung", "Maeumjigi Finale"]
    }
}

def translate_post(slug, meta):
    src_idx = os.path.join(BLOG_ROOT, slug, "index.md")
    if not os.path.exists(src_idx):
        print(f"[SKIP] {slug} not found in blog/")
        return

    with open(src_idx, "r", encoding="utf-8") as f:
        content = f.read()

    # Split FrontMatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"[ERR] Invalid frontmatter in {slug}")
        return

    fm = parts[1]
    body = parts[2]

    # Update FrontMatter
    # Title
    fm = re.sub(r'title:\s*["\'].*?["\']', f'title: "{meta["title"]}"', fm)
    if 'title:' not in fm:
        fm += f'\ntitle: "{meta["title"]}"\n'

    # Description
    fm = re.sub(r'description:\s*["\'].*?["\']', f'description: "{meta["desc"]}"', fm)

    # Keywords
    kw_str = "[" + ", ".join([f'"{k}"' for k in meta["keywords"]]) + "]"
    fm = re.sub(r'keywords:\s*\[.*?\]', f'keywords: {kw_str}', fm)

    new_content = f"---{fm}---{body}"

    # 1. Save to Staging
    stage_dir = os.path.join(STAGING_ROOT, slug)
    stage_de_dir = os.path.join(stage_dir, "i18n", "de")
    os.makedirs(stage_de_dir, exist_ok=True)
    with open(os.path.join(stage_de_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(new_content.strip() + "\n")

    # 2. Save to i18n/de production blog dir
    prod_de_dir = os.path.join(PROD_DE_ROOT, slug)
    os.makedirs(prod_de_dir, exist_ok=True)
    with open(os.path.join(prod_de_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(new_content.strip() + "\n")

    # 3. Copy images
    src_images = os.path.join(BLOG_ROOT, slug, "images")
    if os.path.exists(src_images):
        dst_images = os.path.join(prod_de_dir, "images")
        os.makedirs(dst_images, exist_ok=True)
        for item in os.listdir(src_images):
            s = os.path.join(src_images, item)
            d = os.path.join(dst_images, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)

    print(f"[OK] Staged & saved German post: {slug}")

def main():
    print("=" * 65)
    print("Translating Section 5: Maeumjigi Capstone (23 posts) into German...")
    print("=" * 65)
    for slug, meta in DE_METAS.items():
        translate_post(slug, meta)
    print("\n[SECTION 5 COMPLETE] All 23 Maeumjigi posts staged and saved in German!")

if __name__ == "__main__":
    main()
