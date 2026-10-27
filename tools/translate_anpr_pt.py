# -*- coding: utf-8 -*-
import os
import shutil

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")

def save_pt_post(slug, pt_content):
    # 1. Save to Staging
    stage_dir = os.path.join(STAGING_ROOT, slug)
    stage_pt_dir = os.path.join(stage_dir, "i18n", "pt-BR")
    os.makedirs(stage_pt_dir, exist_ok=True)
    with open(os.path.join(stage_pt_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(pt_content.strip() + "\n")
    print(f"[STAGING OK] {slug} -> {stage_pt_dir}\\index.md")

    # 2. Save to i18n/pt-BR production blog dir (ready for build)
    prod_pt_dir = os.path.join(GB_ROOT, "i18n", "pt-BR", "docusaurus-plugin-content-blog", slug)
    os.makedirs(prod_pt_dir, exist_ok=True)
    with open(os.path.join(prod_pt_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(pt_content.strip() + "\n")
    
    # 3. Copy images from blog/<slug>/images
    src_images = os.path.join(GB_ROOT, "blog", slug, "images")
    if os.path.exists(src_images):
        dst_images = os.path.join(prod_pt_dir, "images")
        os.makedirs(dst_images, exist_ok=True)
        for item in os.listdir(src_images):
            s = os.path.join(src_images, item)
            d = os.path.join(dst_images, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
        print(f"[IMAGES OK] Copied images to {dst_images}")

# ==============================================================================
# ANPR 1 PORTUGUESE
# ==============================================================================
a1_slug = "2026-06-25-vision-anpr-1"
a1_content = """---
slug: 2026-06-25-vision-anpr-1
title: "[Visão Computacional] Monitoramento de Faixas por Dashcam & ANPR com Super-Resolução: Pipeline em 6 Estágios & Restrições em Tempo Real (#1)"
authors: [jbgih]
tags: [computer-vision, anpr, object-detection, super-resolution, opencv, deep-learning, python]
date: 2026-06-25
project: anpr_vision
description: "Arquitetura de um pipeline de visão computacional em 6 estágios: Detecção dinâmica de faixas, critérios geométricos de IoU, localização de placas via YOLOv5, super-resolução EDSR e votação majoritária de OCR."
keywords: [ANPR Pipeline Visão Computacional, Análise de Vídeo Dashcam Tempo Real, Detecção de Veículos YOLOv5, Super Resolução Placas, Sistemas Inteligentes de Transporte ITS]
---

![Diagrama do Pipeline ANPR em 6 Estágios](./images/01_pipeline_diagram.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Filmagens de dashcam em alta velocidade sofrem com vibrações mecânicas, reflexos de iluminação e desfoque por movimento. O OCR direto falha devido à baixa resolução dos recortes de placas.
> - **Solução**: Um pipeline modular em 6 estágios com restrição estrita de 30 FPS, integrando detecção de faixas, detecção hierárquica por YOLO, super-resolução EDSR e votação temporal por OCR.

{/* truncate */}

---

### 1. Visão Geral dos 6 Estágios do Pipeline

```mermaid
flowchart LR
    A[1. Entrada de Vídeo 30 FPS] --> B[2. Detecção Dinâmica de Faixas]
    B --> C[3. Detecção Hierárquica de Veículo & Placa]
    C --> D[4. Validação Geométrica de Invasão de Faixa por IoU]
    D --> E[5. Super-Resolução Profunda EDSR]
    E --> F[6. EasyOCR & Votação Majoritária Temporal]
```

1. **Ingestão de Vídeo**: Decodificação assíncrona de streams de vídeo 1080p usando multithreading no OpenCV.
2. **Detecção de Faixas**: Filtragem de bordas Canny, máscara de região de interesse (ROI trapezoidal) e Transformada Probabilística de Hough (`HoughLinesP`).
3. **Localização Hierárquica**: Detecção preliminar de veículos com YOLOv3, seguida por segmentação refinada de placas via YOLOv5.
4. **Métrica de Invasão**: Cálculo da sobreposição de polígonos (Intersection over Union - IoU) entre a base do veículo e a faixa demarcada.
5. **Super-Resolução**: Ampliação de 4x em recortes de placas miniaturizadas (inferiores a 40x20 pixels) via modelo neural residual EDSR.
6. **OCR & Consenso**: Extração de texto com EasyOCR e suavização estatística através de janela deslizante temporal de 11 frames.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Arquitetura Modular**: O isolamento em 6 módulos desacoplados permite otimizar gargalos de GPU e CPU de forma independente.
2. **Processamento em Tempo Real**: O sistema garante operação sustentada a 30 FPS para telemetria confiável em veículos em movimento.
3. **Resiliência a Desfoque**: A super-resolução EDSR reconstrói placas inelegíveis onde algoritmos convencionais falham.
4. **Filtragem de Falsos Positivos**: Critérios geométricos de IoU evitam disparos indevidos em oscilações de pista.
"""

# ==============================================================================
# ANPR 2 PORTUGUESE
# ==============================================================================
a2_slug = "2026-06-26-vision-anpr-2"
a2_content = """---
slug: 2026-06-26-vision-anpr-2
title: "[Visão Computacional] Delimitação Dinâmica de Faixas & Critério Geométrico de Invasão por IoU (#2)"
authors: [jbgih]
tags: [computer-vision, anpr, lane-detection, hough-transform, iou, opencv, python]
date: 2026-06-26
project: anpr_vision
description: "Filtragem de bordas Canny, Transformada de Hough probabilística (HoughLinesP), limiares angulares e cálculo de IoU poligonal para monitoramento de faixas de rolamento."
keywords: [OpenCV Detecção de Faixas, HoughLinesP Rastreamento Faixa, Detecção Invasão de Faixa, Cálculo IoU Poligonal, Canny Detecção de Bordas Rodovia]
---

![Sobreposição de Detecção Dinâmica de Faixas](./images/01_lane_detection.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Reflexos no asfalto molhado, emendas de piche e sombras de viadutos produzem ruídos lineares; comparações simples de coordenadas X falham em curvas.
> - **Solução**: Combinação de ROI trapezoidal adaptativa, filtros angulares de inclinação positiva/negativa e sobreposição de polígonos com limiar de IoU > 0,15.

{/* truncate */}

---

### 1. Formulação Matemática da Extração de Faixas

A geometria das linhas delimitadoras da pista é modelada por equações lineares no plano da imagem:

$$y = m \\cdot x + b, \\quad \\text{onde } m = \\frac{y_2 - y_1}{x_2 - x_1}$$

Para descartar marcações transversais e sombras horizontais, definimos limiares estritos de inclinação angular:
- **Faixa Esquerda**: $-0.85 < m < -0.45$
- **Faixa Direita**: $+0.45 < m < +0.85$

---

### 2. Critério de Invasão de Faixa Baseado em IoU Poligonal

A invasão de faixa é confirmada quando o polígono delimitador da base do veículo $P_{\\text{veiculo}}$ intercepta o polígono da faixa de rodagem $P_{\\text{faixa}}$:

$$\\text{IoU}_{\\text{invasao}} = \\frac{\\text{Area}(P_{\\text{veiculo}} \\cap P_{\\text{faixa}})}{\\text{Area}(P_{\\text{veiculo}})} > \\theta_{\\text{limiar}}$$

Adotando um limiar $\\theta = 0.15$, ruídos momentâneos de vibração são filtrados com precisão, enquanto mudanças reais de faixa são registradas de modo determinístico.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Filtragem Angular**: Limiares de inclinação matemática eliminam 95% das linhas espúrias geradas por sombras e remendos de asfalto.
2. **IoU Poligonal Superior**: A área de sobreposição geométrica é imune a falsos positivos em curvas acentuadas.
3. **Eficiência Computacional**: A Transformada de Hough na ROI trapezoidal consome menos de 3 milissegundos por quadro.
4. **Gatilho Determinístico**: A confirmação de invasão dispara automaticamente o módulo de leitura em alta resolução.
"""

# ==============================================================================
# ANPR 3 PORTUGUESE
# ==============================================================================
a3_slug = "2026-06-27-vision-anpr-3"
a3_content = """---
slug: 2026-06-27-vision-anpr-3
title: "[Visão Computacional] Detecção Hierárquica de Objetos: ROI Veicular com YOLOv3, Detector de Placas YOLOv5 & Rastreamento CSRT (#3)"
authors: [jbgih]
tags: [computer-vision, anpr, yolo, csrt-tracker, object-detection, opencv, python]
date: 2026-06-27
project: anpr_vision
description: "Localização hierárquica em dois estágios: Detecção global do veículo via YOLOv3, inferência focada de placas via YOLOv5 e rastreamento com filtro de correlação CSRT a mais de 50 FPS."
keywords: [YOLOv5 Detecção de Placas, CSRT Tracker OpenCV, Detecção Hierárquica de Objetos, Rastreamento Veicular Tempo Real, Localização ROI Veicular]
---

![Localização de Placas Veiculares com YOLOv5](./images/01_plate_localization.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Buscar placas minúsculas (30x15 pixels) diretamente no quadro 1080p completo causa falsos positivos em placas de trânsito e derruba a taxa de inferência para menos de 10 FPS.
> - **Solução**: Abordagem em dois estágios — primeiro localiza-se o veículo (YOLOv3), depois isola-se a placa apenas no recorte (YOLOv5), intercalando quadros intermediários com o leve e rápido rastreador CSRT.

{/* truncate */}

---

### 1. O Princípio da Detecção Hierárquica em Cascata

Em vez de processar o quadro inteiro com uma rede neural pesada, o sistema aplica um estreitamento progressivo da região de interesse:

```mermaid
flowchart TD
    Frame[Quadro Full HD 1920x1080] --> Step1["Estágio 1: YOLOv3 detecta a caixa delimitadora do veículo"]
    Step1 --> Crop[Isolamento do recorte do veículo]
    Crop --> Step2["Estágio 2: YOLOv5 busca a placa apenas na região frontal/traseira"]
    Step2 --> Plate[Recorte limpo da placa (ex: 40x20 px)]
    Plate --> Step3["Estágio 3: Rastreador CSRT assume quadros seguintes a 50+ FPS"]
```

Com o rastreamento por correlação do CSRT, a inferência neural do YOLOv5 precisa ser executada apenas a cada 5 quadros, mantendo o pipeline leve e altamente responsivo.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Afunilamento Hierárquico**: Elimina completamente falsos positivos em outdoors e placas de sinalização urbana.
2. **Ganho de Velocidade de 5x**: O rastreador CSRT reduz drasticamente a demanda de ciclos da GPU.
3. **Rastreamento Contínuo**: A placa permanece travada mesmo sob inclinações bruscas e frenagens.
4. **Entrega Otimizada**: O recorte de alta precisão é repassado diretamente para a etapa de super-resolução.
"""

# ==============================================================================
# ANPR 4 PORTUGUESE
# ==============================================================================
a4_slug = "2026-06-28-vision-anpr-4"
a4_content = """---
slug: 2026-06-28-vision-anpr-4
title: "[Visão Computacional] Superando Artefatos em Vídeos de Dashcam: Super-Resolução Profunda (EDSR vs FSRCNN) & Empilhamento Multi-Frame (#4)"
authors: [jbgih]
tags: [computer-vision, super-resolution, edsr, image-stacking, anpr, deep-learning, python]
date: 2026-06-28
project: anpr_vision
description: "Reconstrução de recortes de placas de baixa resolução através de Super-Resolução Profunda EDSR 4x e empilhamento temporal de múltiplos quadros (Image Stacking)."
keywords: [EDSR Super Resolução, Restauração de Imagens de Placas, OpenCV dnn_superres, Multi-Frame Image Stacking, Deep Residual Upscaling]
---

![Comparativo de Super-Resolução Profunda com EDSR](./images/01_edsr_sr_comparison.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Recortes de placas em dashcams medem com frequência menos de 40x20 pixels com severa compressão H.264. A interpolação bicúbica comum borra os caracteres.
> - **Solução**: Aplicação de redes residuais profundas aprimoradas (EDSR) para ampliação de 4x e média temporal de múltiplos quadros para cancelamento de ruído estocástico.

{/* truncate */}

---

### 1. Comparativo de Modelos: EDSR vs. FSRCNN

| Modelo de Super-Resolução | Tempo de Inferência (ms) | Qualidade da Reconstrução | Recomendação de Uso |
| :--- | :--- | :--- | :--- |
| **Interpolação Bicúbica** | < 1 ms | Muito borrada; caracteres fundidos | Inadequado para OCR |
| **FSRCNN (Fast SR)** | ~ 8 ms | Nitidez moderada de bordas | Dispositivos móveis de borda |
| **EDSR (Enhanced Deep Residual)** | ~ 35 ms | **Excelente definição de caracteres & contraste** | **Pipeline de Produção** |

O EDSR remove camadas supérfluas de Batch Normalization e emprega blocos residuais expandidos, reconstruindo contornos alfanuméricos nítidos a partir de imagens extremamente pixeladas.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Limites da Interpolação Simples**: Algoritmos clássicos amplificam blocos de compressão e impedem a leitura pelo OCR.
2. **Reconstrução com EDSR 4x**: Redes neurais residuais restauram bordas e contraste com fidelidade matemática.
3. **Empilhamento de Quadros**: A média temporal cancela o ruído do sensor antes do processamento textual.
4. **Salto de Acurácia**: A super-resolução eleva a taxa de sucesso do OCR de 42% para mais de 89%.
"""

# ==============================================================================
# ANPR 5 PORTUGUESE
# ==============================================================================
a5_slug = "2026-06-29-vision-anpr-5"
a5_content = """---
slug: 2026-06-29-vision-anpr-5
title: "[Visão Computacional] Motor de OCR para ANPR, Normalização com Regex & Votação Majoritária Temporal (Evolução de v01 a v11) (#5)"
authors: [jbgih]
tags: [computer-vision, anpr, easyocr, regex, voting-ensemble, python]
date: 2026-06-29
project: anpr_vision
description: "Validação sintática de placas, otimização do EasyOCR, votação por maioria em janela deslizante temporal e a jornada de desenvolvimento ao longo de 11 iterações de v01 a v11."
keywords: [EasyOCR Reconhecimento de Placas, ANPR Majority Voting Ensemble, Normalização Regex Placas, Acurácia OCR Visão, Sistemas Inteligentes de Transporte ITS]
---

![Votação Majoritária Temporal e Validação Final](./images/01_voting_evolution.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Quadros isolados sofrem inevitavelmente com erros de leitura pontuais por reflexo ou vibração (ex.: confundir `6` com `8` ou `B` com `8`).
> - **Solução**: Combinação de EasyOCR, correção sintática por expressões regulares (Regex) e comitê de decisão por maioria temporal (*Sliding-Window Majority Voting*) sobre 11 quadros sucessivos.

{/* truncate */}

---

### 1. O Mecanismo de Votação por Maioria Temporal

Em vez de confiar no resultado de um único quadro instável, o sistema agrega predições em uma janela deslizante contínua de 11 frames:

```mermaid
flowchart TD
    F1["Quadro 1: 24가1511"] --> Buffer[Buffer Circular: 11 Quadros]
    F2["Quadro 2: 24가1511"] --> Buffer
    F3["Quadro 3: 24가1571 (Erro de Leitura)"] --> Buffer
    F4["Quadro 4: 24가1511"] --> Buffer
    Buffer --> Voting{"Votação Majoritária: Qual string tem maior frequência?"}
    Voting -->|8 de 11 Votos| Confirmed["Placa Confirmada: 24가1511 (Confiança: 94.2%)"]
```

---

### 2. A Evolução do Projeto: De v01 a v11

Ao longo de 11 iterações de engenharia, a equipe elevou a precisão global de ponta a ponta de modestos 31% para impressionantes 96% em condições reais de tráfego.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Consenso Temporal**: A votação por maioria em janela deslizante neutraliza erros transientes de vibração da câmera.
2. **Correção Sintática por Regex**: Padrões sintáticos inválidos são tratados antes da computação dos votos.
3. **Robustez Comprovada**: Mais de 11 ciclos evolutivos consolidaram uma precisão superior a 96% em tráfego real.
4. **Sistema Completo**: A integração dos 6 módulos resulta em uma solução pronta para produção em sistemas ITS.
"""

def main():
    print("=" * 65)
    print("Translating Section 3: Vision ANPR (5 posts) into pt-BR...")
    print("=" * 65)
    save_pt_post(a1_slug, a1_content)
    save_pt_post(a2_slug, a2_content)
    save_pt_post(a3_slug, a3_content)
    save_pt_post(a4_slug, a4_content)
    save_pt_post(a5_slug, a5_content)
    print("\n[SECTION 3 COMPLETE] All 5 Vision ANPR posts staged and saved in pt-BR!")

if __name__ == "__main__":
    main()
