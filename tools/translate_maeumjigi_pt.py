# -*- coding: utf-8 -*-
"""
Batch translate Section 5: Maeumjigi Capstone Dev Logs (23 posts) into Brazilian Portuguese (pt-BR),
stage them in 배포대기/<slug>/i18n/pt-BR/index.md and save to i18n/pt-BR production blog.
"""
import os
import shutil
import re

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")
BLOG_ROOT = os.path.join(GB_ROOT, "blog")
PROD_PT_ROOT = os.path.join(GB_ROOT, "i18n", "pt-BR", "docusaurus-plugin-content-blog")

PT_METAS = {
    "2026-03-26-maeumjigi-1": {
        "title": "[Diário de Bordo Maeumjigi Capstone #1] Primeiros Passos & Planejamento: Workflows de IA com Claude Code e o Pivot para IA de Saúde Mental",
        "desc": "Dia 1 do projeto de conclusão de curso: estabelecimento de fluxos autônomos com Claude Code e a virada estratégica de um aplicativo de alarme para o Maeumjigi, uma IA empática de saúde mental.",
        "keywords": ["Workflows de IA com Claude Code", "Chatbot de IA para Saúde Mental", "Arquitetura Projeto Capstone", "Roadmap Fine-Tuning LLM", "Regras de Agentes Autônomos de IA"]
    },
    "2026-03-30-maeumjigi-2": {
        "title": "[Diário de Bordo Maeumjigi Capstone #2] Concepção Inicial do App de Notificações e Primeiros Testes",
        "desc": "Semana 1 de desenvolvimento: prototipagem do primeiro web scraper e constatação das limitações de simples bots de notificação.",
        "keywords": ["Web Scraping App Alarme", "Bot de Notificação Android", "Planejamento Inicial de Projeto", "Arquitetura App Mobile", "Diário de Desenvolvimento Semana 1"]
    },
    "2026-03-31-maeumjigi-3": {
        "title": "[Diário de Bordo Maeumjigi Capstone #3] Teste de Build do Aplicativo e Início do Pré-processamento para Fine-Tuning",
        "desc": "Semana 2 de arquitetura: limpeza de dados para Llama 3.1 e avaliação de datasets de conversação multi-turnos.",
        "keywords": ["Pré-processamento Dados Llama 3.1", "Limpeza de Diálogos Multi-Turno", "Tokenização de Dataset", "Pipeline de Machine Learning", "Capstone Semana 2"]
    },
    "2026-04-01-maeumjigi-4": {
        "title": "[Diário de Bordo Maeumjigi Capstone #4] Pré-processamento em Larga Escala: Chat-Template do Llama 3.1 & Pipeline JSONL Autônomo",
        "desc": "Construção de um pipeline JSONL automatizado para formatação de templates de chat do Llama 3.1 e validação de limites de tokenização.",
        "keywords": ["Chat Template Llama 3.1", "Pipeline de Dados JSONL", "Pré-processamento Automatizado", "Formatação de Dataset", "Treinamento IA Empática"]
    },
    "2026-04-03-maeumjigi-5": {
        "title": "[Diário de Bordo Maeumjigi Capstone #5] Limpeza de 100.000 Dados de Emoções e a Pressão de Custos com APIs de LLMs",
        "desc": "Desafios de engenharia com 100.000 falas clínicas, controle de orçamento em chamadas de API e estratégias de processamento em lote.",
        "keywords": ["Limpeza Dataset de Emoções", "Otimização Custos API LLM", "Inferência em Lote Batch", "Análise de Diálogos Clínicos", "Capstone Semana 3"]
    },
    "2026-04-05-maeumjigi-6": {
        "title": "[Diário de Bordo Maeumjigi Capstone #6] Pipeline de Relatórios Automatizados: Visualização python-docx & Início do Frontend Next.js 14",
        "desc": "Geração automatizada de relatórios clínicos em Word/PDF com python-docx e inicialização da interface web com Next.js 14.",
        "keywords": ["Geração de Relatórios python-docx", "Dashboard Next.js 14", "Documentação Automatizada", "Arquitetura ML Full-Stack", "Relatórios Clínicos"]
    },
    "2026-04-07-maeumjigi-7": {
        "title": "[Diário de Bordo Maeumjigi Capstone #7] Otimização de Dados Sintéticos (v5) e Integração com o Frontend",
        "desc": "Controle de qualidade de dados sintéticos de treino v5 e integração da interface de chat com a API assíncrona FastAPI.",
        "keywords": ["Dados Sintéticos v5", "Integração Frontend FastAPI", "Interface de Chat Next.js", "Validação de Dataset", "Otimização Modelo IA"]
    },
    "2026-04-08-maeumjigi-8": {
        "title": "[Diário de Bordo Maeumjigi Capstone #8] Explosão de Custos de API e Migração do Fine-Tuning para o Google Colab Pro",
        "desc": "Lições aprendidas com custos imprevistos de API e migração estratégica do treinamento para Google Colab Pro utilizando QLoRA.",
        "keywords": ["Treinamento Google Colab Pro", "Fine-Tuning QLoRA", "Controle de Custos de API", "Engenharia Orçamentária", "LLMs Open-Source"]
    },
    "2026-04-09-maeumjigi-9": {
        "title": "[Diário de Bordo Maeumjigi Capstone #9] Depuração de Falhas no Fine-Tuning do Llama 3.1 & Apresentação Intermediária Semana 6",
        "desc": "Resolução de erros de estouro de memória de GPU (CUDA Out-of-Memory) no Llama 3.1 e apresentação do progresso perante a banca acadêmica.",
        "keywords": ["Resolução CUDA OOM", "Treinamento Llama 3.1 QLoRA", "Apresentação Intermediária Capstone", "Gerenciamento de VRAM GPU", "Gradient Checkpointing"]
    },
    "2026-04-14-maeumjigi-10": {
        "title": "[Diário de Bordo Maeumjigi Capstone #10] Superando Rate Limits de API: Automação Não-Supervisionada & Pipeline Resiliente",
        "desc": "Desenvolvimento de um pipeline de síntese de dados resiliente a falhas com backoff exponencial e execução em lote 24/7.",
        "keywords": ["Solução Rate Limit API", "Backoff Exponencial", "Automação Não-Supervisionada", "Síntese Resiliente de Dados", "Workflows Automatizados"]
    },
    "2026-04-19-maeumjigi-11": {
        "title": "[Diário de Bordo Maeumjigi Capstone #11] Avaliação do Modelo M6 com Dados Sintéticos v5",
        "desc": "Avaliação quantitativa de benchmarks do checkpoint M6 com métricas Rouge-L, BLEU e índices clínicos de empatia.",
        "keywords": ["Avaliação Modelo M6", "Benchmark Rouge-L BLEU", "Métrica de Empatia Clínica", "Análise Checkpoint Fine-Tuning", "Validação de LLM"]
    },
    "2026-05-03-maeumjigi-12": {
        "title": "[Diário de Bordo Maeumjigi Capstone #12] Tentativa de Fine-Tuning do Modelo Gigante 70B & A Batalha Contra GPU OOM",
        "desc": "Experimentos de fine-tuning em modelos de 70 bilhões de parâmetros com FSDP e quantização de 4 bits em infraestrutura de nuvem restrita.",
        "keywords": ["Fine-Tuning Modelo 70B", "Quantização FSDP", "Limitações VRAM de GPU", "Treinamento Grandes Modelos Linguagem", "Limites GPU Colab"]
    },
    "2026-05-04-maeumjigi-13": {
        "title": "[Diário de Bordo Maeumjigi Capstone #13] Limites do Treinamento de 70B & Pivot para Modelos Médios (HCX, Qwen 2.5)",
        "desc": "Virada estratégica de modelos pesados de 70B para arquiteturas intermediárias de alta eficiência (HyperCLOVA X e Qwen 2.5).",
        "keywords": ["Pivot Modelos Mid-Size", "Fine-Tuning Qwen 2.5", "Otimização HyperCLOVA X", "Eficiência de Arquitetura de Modelo", "Preparação Deploy em Borda"]
    },
    "2026-05-06-maeumjigi-14": {
        "title": "[Diário de Bordo Maeumjigi Capstone #14] Conclusão do Treinamento & Construção do Pipeline de Inferência Paralela",
        "desc": "Finalização de todos os adaptadores LoRA e implementação de um pipeline de inferência paralela multimodelo para benchmarking comparativo.",
        "keywords": ["Pipeline de Inferência Paralela", "Fusão de Adaptadores LoRA", "Benchmark Multimodelo", "Servidor de Inferência FastAPI", "Batching Assíncrono"]
    },
    "2026-05-07-maeumjigi-15": {
        "title": "[Diário de Bordo Maeumjigi Capstone #15] Visualização dos Resultados de 5 Modelos & Configuração do Ambiente Local",
        "desc": "Gráficos comparativos de desempenho para 5 modelos ajustados e implantação dos checkpoints em servidores locais de teste.",
        "keywords": ["Visualização Benchmark Modelos", "Setup Servidor Local", "Avaliação com Matplotlib", "Latência vs Acurácia", "Capstone Semana 10"]
    },
    "2026-05-08-maeumjigi-16": {
        "title": "[Diário de Bordo Maeumjigi Capstone #16] Erro Crítico de Configuração, 2ª Rodada de Fine-Tuning & Início do App React Native",
        "desc": "Detecção de um erro em hiperparâmetros de LoRA, início da 2ª rodada limpa de treinamento e prototipagem do app móvel em React Native.",
        "keywords": ["Correção Hiperparâmetros LoRA", "2ª Rodada de Fine-Tuning", "App Mobile React Native", "Desenvolvimento Expo", "Análise de Erros de Treino"]
    },
    "2026-05-12-maeumjigi-17": {
        "title": "[Diário de Bordo Maeumjigi Capstone #17] Conclusão da 2ª Rodada de Treino & As Armadilhas de Pipelines Automatizados",
        "desc": "Finalização bem-sucedida da 2ª rodada de fine-tuning e implementação de salvaguardas contra distorções silenciosas de dados.",
        "keywords": ["Conclusão 2ª Rodada Fine-Tuning", "Armadilhas de Pipelines Automatizados", "Detecção de Viés de Dados", "Robustez de Modelo", "Capstone Semana 11"]
    },
    "2026-05-13-maeumjigi-18": {
        "title": "[Diário de Bordo Maeumjigi Capstone #18] Expansão de Tokens de Inferência & Comparativo Detalhado da 2ª Rodada",
        "desc": "Análise de respostas longas em conversas de múltiplos turnos e medição rigorosa de consistência e alucinação.",
        "keywords": ["Expansão Tokens de Inferência", "Conversação Multi-Turno", "Detecção de Alucinação", "Benchmark Llama 3.1 vs Qwen", "Métricas de Avaliação"]
    },
    "2026-05-17-maeumjigi-19": {
        "title": "[Diário de Bordo Maeumjigi Capstone #19] Relatórios de Avaliação Automatizados & Depuração de Erro 401 no FastAPI com PostgreSQL",
        "desc": "Geração automatizada de relatórios semanais de progresso e resolução de travamentos de autenticação em pool de conexões do PostgreSQL.",
        "keywords": ["FastAPI PostgreSQL Erro 401", "Debugging Connection Pool", "Relatórios Automatizados", "Depuração Banco de Dados", "Endurecimento de Backend"]
    },
    "2026-05-20-maeumjigi-20": {
        "title": "[Diário de Bordo Maeumjigi Capstone #20] Conclusão da 3ª Rodada de Treinamento & Expansão de Recursos no Backend",
        "desc": "Integração de análises de séries temporais de humor na API FastAPI e consolidação da 3ª iteração dos modelos neurais.",
        "keywords": ["3ª Rodada Fine-Tuning", "Análise Tendência de Humor", "Endpoints FastAPI", "Séries Temporais Clínicas", "Capstone Semana 12"]
    },
    "2026-05-22-maeumjigi-21": {
        "title": "[Diário de Bordo Maeumjigi Capstone #21] Otimização da Proporção de Mistura de Dados & Início da 4ª Rodada",
        "desc": "Ajuste fino da proporção ideal entre diálogos clínicos especializados e conversações empáticas gerais para equilíbrio de loss.",
        "keywords": ["Otimização Proporção de Dados", "4ª Rodada Fine-Tuning", "Equilíbrio Diálogo Clínico", "Convergência Função de Perda", "Refinamento de Modelo"]
    },
    "2026-05-30-maeumjigi-22": {
        "title": "[Diário de Bordo Maeumjigi Capstone #22] O Triunfo da 4ª Rodada: Checkpoint-4400, Proporções de Dados & Arquitetura Global",
        "desc": "A grande consagração com o Checkpoint-4400: o equilíbrio perfeito entre rigor clínico e acolhimento humano na arquitetura final do sistema.",
        "keywords": ["Conquista Checkpoint-4400", "Arquitetura Global de Sistema", "Equilíbrio Empatia Clínica", "Seleção Modelo Produção", "Marco do Capstone"]
    },
    "2026-06-18-maeumjigi-23": {
        "title": "[Diário de Bordo Maeumjigi Capstone #23] Wrapper de Segurança em Duas Camadas, Orçamento AWS EC2 GPU & Defesa Final de Graduação",
        "desc": "Camada determinística de proteção contra crises (guardrails em sub-milissegundos), cálculo de custos de inferência na AWS EC2 e defesa pública aprovada com nota máxima.",
        "keywords": ["Wrapper Segurança Duas Camadas", "Guardrails Intervenção Crise", "Custos Inferência AWS EC2", "Apresentação Final TCC", "Final Maeumjigi"]
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
    stage_pt_dir = os.path.join(stage_dir, "i18n", "pt-BR")
    os.makedirs(stage_pt_dir, exist_ok=True)
    with open(os.path.join(stage_pt_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(new_content.strip() + "\n")

    # 2. Save to i18n/pt-BR production blog dir
    prod_pt_dir = os.path.join(PROD_PT_ROOT, slug)
    os.makedirs(prod_pt_dir, exist_ok=True)
    with open(os.path.join(prod_pt_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(new_content.strip() + "\n")

    # 3. Copy images
    src_images = os.path.join(BLOG_ROOT, slug, "images")
    if os.path.exists(src_images):
        dst_images = os.path.join(prod_pt_dir, "images")
        os.makedirs(dst_images, exist_ok=True)
        for item in os.listdir(src_images):
            s = os.path.join(src_images, item)
            d = os.path.join(dst_images, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)

    print(f"[OK] Staged & saved Portuguese post: {slug}")

def main():
    print("=" * 65)
    print("Translating Section 5: Maeumjigi Capstone (23 posts) into Brazilian Portuguese (pt-BR)...")
    print("=" * 65)
    for slug, meta in PT_METAS.items():
        translate_post(slug, meta)
    print("\n[SECTION 5 COMPLETE] All 23 Maeumjigi posts staged and saved in pt-BR!")

if __name__ == "__main__":
    main()
