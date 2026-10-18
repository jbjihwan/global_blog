#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enrich Maeumjigi dev logs (1-23 across en, ko, ja, es) with high-quality descriptions and {/* truncate */} tags.
"""

import os
import glob
import re

BASE_DIR = r"D:\ai\antigravity\global_blog"

DESCRIPTIONS = {
    1: {
        "ko": "캡스톤 디자인 첫날, Claude Code AI 코딩 어시스턴트 도입과 초기 알람 앱 기획 및 팀 협업 코딩 규칙(Claude.md)을 수립한 여정을 기록합니다.",
        "en": "Day 1 of our capstone project: Introducing Claude Code AI assistant, initial alarm app planning, and establishing team collaboration coding rules.",
        "ja": "キャップストーンデザイン初日、Claude Codeの導入と初期アラームアプリ企画、およびチーム開発協調ルール（Claude.md）を策定した記録です。",
        "es": "Día 1 del proyecto capstone: Introducción del asistente Claude Code, planificación inicial de la app de alarmas y reglas de codificación en equipo.",
    },
    2: {
        "ko": "JSoup 백그라운드 웹 크롤링 서비스와 룸 데이터베이스를 연동하여 특정 사이트 잔여석 감지 알람 앱의 기본 기능을 구현한 과정입니다.",
        "en": "Implementing the core alarm app functionality by integrating JSoup background web crawling with Android Room database for real-time reservation alerts.",
        "ja": "JSoupバックグラウンドWebクローリングとRoomデータベースを連携し、予約空き状況検知アラームアプリの基盤を実装したプロセスです。",
        "es": "Implementación de la funcionalidad principal de la app de alarmas integrando web scraping JSoup en segundo plano con base de datos Android Room.",
    },
    3: {
        "ko": "알람 앱 개발 완성 직후 팀 브레인스토밍을 거쳐 사회적 가치를 창출하는 자살예방 AI 챗봇 '마음지기' 프로젝트로 전격 피봇팅한 배경과 결정 과정입니다.",
        "en": "Completing the alarm app and executing a major project pivot toward 'Maeumjigi', an AI-powered mental health and suicide prevention chatbot.",
        "ja": "アラームアプリ完成直後、チームで議論を重ね社会的価値を創出する自殺予防AIチャットボット「マウムジギ」へ方針転換した決定過程です。",
        "es": "Culminación de la app de alarmas y pivote estratégico hacia 'Maeumjigi', un chatbot de IA para la prevención del suicidio y apoyo emocional.",
    },
    4: {
        "ko": "자살예방 챗봇 마음지기의 전체 시스템 아키텍처 설계, 감정 분류와 위기감지 파이프라인, 그리고 프롬프트 엔지니어링 기틀을 마련한 기록입니다.",
        "en": "Designing the full architecture for Maeumjigi: emotion classification, suicide crisis detection pipeline, and initial prompt engineering blueprint.",
        "ja": "マウムジギの全体システムアーキテクチャ設計、感情分類および危機検知パイプライン、初期プロンプトエンジニアリングの枠組みを構築した記録です。",
        "es": "Diseño de la arquitectura integral de Maeumjigi: detección de crisis de suicidio, clasificación de emociones y formulación de prompts.",
    },
    5: {
        "ko": "국립국어원 공공 말뭉치 데이터를 정제하여 대화 데이터셋을 구축하고, 대량 API 호출 중 마주한 첫 번째 API 과금 악몽과 대책을 다룹니다.",
        "en": "Purifying Korean public dialogue datasets and managing the first severe Anthropic API billing challenge encountered during automated data processing.",
        "ja": "国立国語院の公開コーパスデータを精製して対話データセットを構築し、大量API呼び出し中に直面した課金問題と対策をまとめます。",
        "es": "Depuración de corpus de diálogo público y resolución del primer desafío crítico de facturación de la API de Anthropic durante el procesamiento de datos.",
    },
    6: {
        "ko": "AI 허브 공감형 대화 데이터를 필터링하고 고품질 멀티턴 대화 구조로 변환하여 LLM 파인튜닝용 JSONL 데이터셋을 구축한 전처리 과정입니다.",
        "en": "Filtering AI Hub empathetic dialogue corpora and constructing structured multi-turn JSONL datasets optimized for open-source LLM fine-tuning.",
        "ja": "AI Hubの共感対話データをフィルタリングし、高品質なマルチターン対話構造のLLMファインチューニング用JSONLデータセットを構築した過程です。",
        "es": "Filtrado de datos de diálogo empático de AI Hub y estructuración de datasets JSONL multironda optimizados para el ajuste fino de LLMs.",
    },
    7: {
        "ko": "Claude API를 활용한 대규모 공감 대화 합성 데이터 증강 파이프라인 구축과 토큰 소비량을 최소화하기 위한 배치 최적화 기법을 공유합니다.",
        "en": "Building a scalable synthetic dialogue generation pipeline with Claude API while implementing batch token optimization to keep API costs under control.",
        "ja": "Claude APIを活用した大規模な共感対話合成データ増強パイプラインの構築と、トークン消費を最小化するバッチ最適化手法を解説します。",
        "es": "Construcción de un pipeline de generación de datos sintéticos con Claude API y técnicas de optimización de tokens para controlar costes.",
    },
    8: {
        "ko": "단일 동기 호출의 병목을 해결하기 위해 비동기(Async) 병렬 처리 크롤링 및 데이터 생성 파이프라인을 구축하여 처리 속도를 5배 향상시킨 기록입니다.",
        "en": "Replacing synchronous bottlenecks with an asynchronous multiprocessing pipeline, boosting data generation and crawling throughput by 5x.",
        "ja": "同期処理のボトルネックを解消するため、非同期並列処理パイプラインを構築し、データ生成速度を5倍に引き上げたエンジニアリング記録です。",
        "es": "Superación de cuellos de botella síncronos mediante un pipeline multiproceso asíncrono, acelerando la generación de datos en 5x.",
    },
    9: {
        "ko": "AWS 클라우드 환경에서 Llama 3.1 8B 모델의 1차 LoRA 파인튜닝 환경을 구축하고 첫 번째 에포크 학습을 성공적으로 완료한 기술 과정입니다.",
        "en": "Setting up the AWS GPU environment, configuring Unsloth LoRA for Llama 3.1 8B, and completing our very first fine-tuning training run.",
        "ja": "AWSクラウドGPU環境でLlama 3.1 8Bモデルの第1次LoRAファインチューニング環境を構築し、初回エポック学習を完了した技術記録です。",
        "es": "Configuración del entorno GPU en AWS, ajuste fino de LoRA en Llama 3.1 8B y ejecución exitosa del primer entrenamiento.",
    },
    10: {
        "ko": "Anthropic API 티어 2 승급을 통해 분당 요청 한도를 해제하고, Qwen 및 HCX 등 다양한 오픈소스 및 상용 모델의 대화 역량을 비교 탐색합니다.",
        "en": "Lifting Anthropic API tier limits to unlock high-concurrency requests and benchmark-testing diverse open-source candidates including Qwen and HCX.",
        "ja": "Anthropic APIのTier制限を解除して同時リクエスト数を引き上げ、QwenやHCXなど多様なモデルの対話性能を比較検討した記録です。",
        "es": "Aumento de límites de tasa de la API de Anthropic y evaluación comparativa de modelos de código abierto como Qwen y HCX.",
    },
    11: {
        "ko": "합성 데이터셋(v5)으로 학습한 모델(M6)의 정량 평가 결과, 일상 대화 능력이 붕괴되고 과도한 위기 반응만 유발되는 과적합 한계를 분석합니다.",
        "en": "Quantitative evaluation of model M6 trained on synthetic dataset v5, uncovering catastrophic forgetting of normal dialogue and empathy collapse.",
        "ja": "合成データセットv5で学習したM6モデルの定量評価を行い、日常対話能力の喪失と過度な危機反応を引き起こす過学習の限界を分析します。",
        "es": "Evaluación cuantitativa del modelo M6, revelando el colapso de la conversación cotidiana y la sobreactivación de respuestas de crisis.",
    },
    12: {
        "ko": "DSR1 70B 초대형 모델의 파인튜닝과 4비트 양자화 서빙에 도전하며 마주한 GPU VRAM OOM 에러와 메모리 오프로딩 트러블슈팅 경험입니다.",
        "en": "Tackling 70B parameter model fine-tuning with 4-bit QLoRA and resolving GPU VRAM OOM errors through aggressive memory offloading.",
        "ja": "DSR1 70B超大型モデルのファインチューニングに挑み、GPU VRAMのOOMエラーとメモリ管理トラブルシューティングを乗り越えた記録です。",
        "es": "Desafío del ajuste fino en modelos de 70B parámetros con QLoRA de 4 bits y resolución de errores OOM de memoria VRAM.",
    },
    13: {
        "ko": "100% 합성 데이터의 맹점을 깨닫고 실제 인간 상담 말뭉치를 2:1 비율로 재결합하여 균형 잡힌 감정 라벨링 데이터셋을 재구성한 과정입니다.",
        "en": "Recognizing synthetic data fatigue and restructuring training corpora with a 2:1 human-to-synthetic ratio to restore genuine conversational depth.",
        "ja": "合成データのみの限界を認識し、実際の人間相談コーパスを2:1の比率で再結合してバランスの取れた感情データセットを再構築した記録です。",
        "es": "Reestructuración del dataset con una proporción 2:1 de datos humanos y sintéticos para recuperar la naturalidad conversacional.",
    },
    14: {
        "ko": "HCX-Omni-8B와 Qwen35-9B의 파인튜닝을 완수하고, 듀얼 GPU를 100% 활용하는 멀티 GPU 병렬 추론(Eval) 자동화 스크립트를 구축한 내용입니다.",
        "en": "Completing fine-tuning for HCX-Omni-8B and Qwen35-9B, and building an automated multi-GPU parallel inference script for comprehensive evaluation.",
        "ja": "HCX-Omni-8BおよびQwen35-9Bのファインチューニングを完遂し、デュアルGPUを活用した並列推論自動化スクリプトを構築した記録です。",
        "es": "Finalización del ajuste fino en HCX y Qwen, y creación de un script de inferencia paralela multi-GPU para la evaluación de modelos.",
    },
    15: {
        "ko": "파인튜닝된 각 모델의 Perplexity와 벤치마크 지표를 분석하고, matplotlib을 활용해 모델별 성능 격차를 한눈에 파악하는 시각화 파이프라인을 구축합니다.",
        "en": "Analyzing Perplexity and dialogue response scores across models, and building an automated matplotlib visualization pipeline for mid-term evaluation.",
        "ja": "各ファインチューニングモデルのPerplexityと評価指標を分析し、matplotlibを活用してモデル間の性能差を可視化した記録です。",
        "es": "Análisis de perplejidad y métricas de rendimiento, construyendo un pipeline de visualización con matplotlib para comparar modelos.",
    },
    16: {
        "ko": "추론 결과에서 발견된 프롬프트 템플릿 하드코딩 오염 문제를 역추적하여 데이터셋 포맷팅 결함을 긴급 수정하고 재현성을 확보한 트러블슈팅입니다.",
        "en": "Diagnosing prompt template pollution hardcoded into training dialogues and performing rapid debugging to restore dataset formatting integrity.",
        "ja": "推論結果に現れたプロンプトテンプレートのハードコーディング汚染を逆追跡し、データセットのフォーマット欠陥を緊急修正した記録です。",
        "es": "Diagnóstico de errores de hardcoding en las plantillas de prompts y depuración urgente para asegurar la integridad de los datos.",
    },
    17: {
        "ko": "정제된 프롬프트 포맷과 LoRA rank/alpha 하이퍼파라미터 조정을 적용하여 2차 파인튜닝을 실행하고 학습 수렴도를 점검한 과정입니다.",
        "en": "Executing 2nd-round fine-tuning with clean chat templates and refined LoRA hyperparameters (rank and alpha) to optimize learning convergence.",
        "ja": "修正されたプロンプト形式とLoRAハイパーパラメータ調整を適用し、第2次ファインチューニングを実行して学習収束度を検証した記録です。",
        "es": "Ejecución de la 2ª ronda de fine-tuning con plantillas de chat limpias y ajuste de hiperparámetros LoRA para mejorar la convergencia.",
    },
    18: {
        "ko": "짧고 경직된 답변 문제를 해결하기 위해 max_new_tokens를 384로 확장하고, LoRA alpha 파라미터(8 vs 16)에 따른 답변 공감도 변화를 분석합니다.",
        "en": "Expanding inference max_new_tokens to 384 to eliminate stiff, clipped answers and analyzing the impact of LoRA alpha (8 vs 16) on empathetic depth.",
        "ja": "短く硬い回答を解決するためにmax_new_tokensを384に拡張し、LoRAのalpha値（8 vs 16）による回答の共感度の違いを分析した記録です。",
        "es": "Ampliación de max_new_tokens a 384 para enriquecer las respuestas y análisis del impacto de LoRA alpha (8 vs 16) en la empatía del bot.",
    },
    19: {
        "ko": "캡스톤 디자인 중간 발표를 위해 엑셀 평가 결과 집계 및 python-pptx 라이브러리를 활용한 발표 슬라이드 자동 생성 파이프라인을 구축합니다.",
        "en": "Automating evaluation data aggregation and generating presentation-ready slide decks using python-pptx for our capstone midterm defense.",
        "ja": "キャップストーンデザイン中間発表のため、評価結果のExcel集計およびpython-pptxを活用したスライド自動生成パイプラインを構築した記録です。",
        "es": "Automatización del resumen de resultados de evaluación y generación de presentaciones de diapositivas con python-pptx para el examen intermedio.",
    },
    20: {
        "ko": "과도한 공감으로 인한 전문성 결여를 방지하기 위해 일상 대화와 감정 위기 대화의 비율을 세밀하게 분할하는 3차 파인튜닝 전략을 설계합니다.",
        "en": "Designing our 3rd fine-tuning strategy, carefully calibrating the ratio between casual chat and crisis response to prevent emotional over-triggering.",
        "ja": "過度な共感による会話破綻を防ぐため、日常会話と感情危機対話の比率を精密に調整する第3次ファインチューニング戦略の設計記録です。",
        "es": "Estrategia para el 3º fine-tuning: calibración de la proporción entre charla casual y diálogo de crisis para evitar respuestas exageradas.",
    },
    21: {
        "ko": "감정 대화 대 일상 대화의 2:1 황금 비율 학습을 통해 모델이 일상 질문에는 명쾌하게 답하고 위기 신호에는 깊게 공감하는 최적 성능을 달성합니다.",
        "en": "Achieving peak model performance by training on the 2:1 emotional-to-daily dialogue ratio, balancing lucid conversational answers with empathetic care.",
        "ja": "感情対話対日常対話の2:1黄金比学習を通じて、日常の質問には明快に答え、危機シグナルには深く共感する最高性能を達成した記録です。",
        "es": "Alcance del rendimiento óptimo mediante la proporción 2:1 entre diálogo emocional y cotidiano, logrando empatía y coherencia.",
    },
    22: {
        "ko": "시스템 프롬프트 지시사항에 과적합되어 답변이 기계화되는 현상을 방지하기 위해 프롬프트 마스킹 및 정규화 기법을 도입한 4차 파인튜닝입니다.",
        "en": "Implementing 4th-round fine-tuning with prompt masking and regularization to defend against system prompt memorization and robotic outputs.",
        "ja": "システムプロンプトの過学習による機械的な回答を防止するため、プロンプトマスキングと正規化を導入した第4次ファインチューニングの記録です。",
        "es": "4ª ronda de fine-tuning: aplicación de enmascaramiento de prompts y regularización para evitar respuestas robóticas y sobreajuste.",
    },
    23: {
        "ko": "최종 산출물: 이중 안전망을 제공하는 Safety Wrapper 가드레일 아키텍처 구축과 AWS EC2 GPU 인스턴스 위 실시간 프로덕션 서빙 배포를 완수한 결말입니다.",
        "en": "Final Milestone: Building the dual-layer Safety Wrapper guardrail architecture and deploying our fine-tuned model to production on AWS EC2 GPU.",
        "ja": "最終成果物：二重の安全網を提供するSafety Wrapperガードレール構造を構築し、AWS EC2 GPU上での本番リアルタイム推論サービングを完遂した記録です。",
        "es": "Hito final: Construcción de la arquitectura de salvaguardas Safety Wrapper y despliegue del modelo en producción sobre GPUs de AWS EC2.",
    },
}

LOCALE_DIRS = {
    "en": os.path.join(BASE_DIR, "blog"),
    "ko": os.path.join(BASE_DIR, "i18n", "ko", "docusaurus-plugin-content-blog"),
    "ja": os.path.join(BASE_DIR, "i18n", "ja", "docusaurus-plugin-content-blog"),
    "es": os.path.join(BASE_DIR, "i18n", "es", "docusaurus-plugin-content-blog"),
}

def update_post(file_path, locale, ep_num):
    desc = DESCRIPTIONS[ep_num][locale]
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split frontmatter
    fm_match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", content, re.DOTALL)
    if not fm_match:
        print(f"Skipping {file_path}: No frontmatter match")
        return False

    fm_text = fm_match.group(1)
    body_text = fm_match.group(2)

    # Add description to frontmatter if not present
    if not re.search(r"^description:", fm_text, re.MULTILINE):
        # Insert description before the last line of frontmatter
        fm_text = fm_text.strip() + f'\ndescription: "{desc}"'

    # Check truncate
    if "{/* truncate */}" not in body_text:
        # We want to place {/* truncate */} after the first introductory paragraph
        # Usually body starts with ![Cover Image]... then an intro paragraph.
        # Let's find the first double newline after the cover image
        parts = re.split(r"(\r?\n\r?\n)", body_text, maxsplit=2)
        if len(parts) >= 3:
            # parts[0]: image line
            # parts[1]: newline
            # parts[2]: rest of body
            subparts = re.split(r"(\r?\n\r?\n)", parts[2], maxsplit=1)
            if len(subparts) >= 3:
                # subparts[0]: first intro paragraph
                # subparts[1]: newline
                # subparts[2]: remaining text
                body_text = f"{parts[0]}{parts[1]}{subparts[0]}\n\n{{/* truncate */}}\n\n{subparts[2]}"
            else:
                body_text = f"{parts[0]}{parts[1]}{parts[2]}\n\n{{/* truncate */}}\n"
        else:
            body_text = f"{body_text}\n\n{{/* truncate */}}\n"

    new_content = f"---\n{fm_text}\n---\n{body_text}"
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)
    return True

def main():
    updated = 0
    for locale, dir_path in LOCALE_DIRS.items():
        for ep in range(1, 24):
            pattern = os.path.join(dir_path, f"*-maeumjigi-{ep}", "index.md")
            matches = glob.glob(pattern)
            for m in matches:
                if update_post(m, locale, ep):
                    updated += 1
    print(f"Successfully processed and updated {updated} files with custom descriptions and truncate tags.")

if __name__ == "__main__":
    main()
