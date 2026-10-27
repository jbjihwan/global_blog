# -*- coding: utf-8 -*-
import os
import shutil

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")

def save_pt_lecture(slug, pt_content):
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
# LECTURE 8 PORTUGUESE (pt-BR)
# ==============================================================================
lec8_slug = "2026-10-29-stanford-cs146s-8"
lec8_content = """---
slug: 2026-10-29-stanford-cs146s-8
title: "[Stanford CS146S #8] Arquitetura de Software Nativa de IA & Refatoração: Desacoplamento de Monólitos, Redução de Débito Semântico e Migrações Autônomas"
authors: [jbgih]
tags: [stanford-cs146s, ai-native-architecture, software-refactoring, semantic-debt, monolith-decoupling, autonomous-migration, code-modernization]
date: 2026-10-29
keywords: [Arquitetura de Software Nativa de IA, Desacoplamento Automatizado de Monólitos, Redução de Débito Semântico, Refatoração Baseada em AST, Migração Autônoma de Código com LLM]
description: "Stanford CS146S Aula 8: Como projetar arquiteturas para agentes de IA autônomos — eliminação de débito semântico, quebra de monólitos legados via grafos de AST e migrações de código com zero downtime."
---

![Arquitetura de Software Nativa de IA e Refatoração em Larga Escala](./images/08_cs146s_ai_native_architecture_refactoring.png)

Bem-vindo à oitava parte da nossa análise técnica da série **CS146S: The Modern Software Developer da Universidade de Stanford**.

Nas sessões anteriores, exploramos engenharia de prompt (Aula 2), ferramentas MCP (Aula 3), test harnesses autocicatrizantes (Aula 4), enxames multiagente (Aula 5), tracing de kernel com eBPF (Aula 6) e revisão automatizada de PRs (Aula 7).

Na **Aula 8**, o currículo foca nas implicações sistêmicas de longo prazo do uso de agentes de IA: **Como projetar arquiteturas de software que agentes de IA consigam navegar, compreender e modificar sem sucumbir à complexidade crescente? E como utilizar agentes para decompor com segurança grandes monólitos legados?**

As arquiteturas tradicionais de software — caracterizadas por estado mutável global, dependências cíclicas e monólitos com centenas de milhares de linhas — sobrecarregam a capacidade de raciocínio lógico dos modelos. Nesta aula, os professores de Stanford formalizam o conceito de **Débito Semântico (*Semantic Debt*)**, estabelecem os mandamentos da **Arquitetura Nativa de IA** e fornecem um guia prático para **Decomposição de Monólitos baseada em AST**.

{/* truncate */}

---

### 1. O Paradoxo da Velocidade: Débito Técnico vs. Débito Semântico

Métricas clássicas de engenharia medem o **débito técnico**: bibliotecas desatualizadas, queries lentas sem índice, cobertura de testes insuficiente. Compiladores e linters estáticos conseguem detectar esses problemas de forma determinística.

No entanto, quando agentes de IA geram código em ritmo acelerado, surge uma ameaça muito mais insidiosa: o **Débito Semântico (*Semantic Debt*)**.

```mermaid
flowchart TD
    subgraph Technical_Debt ["Débito Técnico Tradicional"]
        T1["Avisos de Compilador & Erros de Sintaxe"]
        T2["Dependências Antigas e Desatualizadas"]
        T3["Violações de Linter & Formatação"]
        T4["Mensurável por Ferramentas Determinísticas"]
    end

    subgraph Semantic_Debt ["Débito Semântico (Era da IA)"]
        S1["Suposições Ocultas & Estado Implícito"]
        S2["Inconsistências Sutis de Interface"]
        S3["Fragmentação de Contexto Entre Repositórios"]
        S4["Código Sintaticamente Válido, Mas com Domínio Obscuro"]
    end
```

O débito semântico ocorre quando o código compila perfeitamente sem erros e passa em todos os testes unitários, mas a intenção conceitual do sistema tornou-se tão fragmentada que nenhum modelo de IA consegue mais assimilar a visão global da arquitetura.

---

### 2. Princípios da Arquitetura de Software Nativa de IA

Para manter bases de código gerenciáveis por agentes autônomos, Stanford propõe quatro diretrizes:

1. **Arquitetura Hexagonal Rígida (Ports & Adapters)**: A lógica de negócio deve ser 100% isolada de frameworks, bancos de dados e APIs externas. Um agente precisa ser capaz de testar a regra de negócio central sem precisar subir um banco real.
2. **Orçamento Explícito de Contexto**: Módulos e pacotes devem ter tamanho contido para que suas interfaces e definições de tipos caibam em 25% da janela de contexto do LLM.
3. **Contratos Determinísticos de Interface**: Proibido usar dicionários genéricos ou JSON solto como parâmetros de funções. Cada interface deve ser formalizada com esquemas estáticos (Pydantic, Zod, Protobuf).
4. **Grafos de Dependência Sem Ciclos**: Dependências circulares geram loops infinitos de refatoração para os agentes.

---

### 3. Decomposição de Monólitos Baseada em AST

A migração segura de monólitos para serviços modulares ocorre em quatro fases:

```mermaid
stateDiagram-v2
    [*] --> AST_Analysis: 1. Análise Estática de Dependências via AST
    AST_Analysis --> Cluster_Detection: 2. Identificação de Domínios Fracamente Acoplados
    Cluster_Detection --> Interface_Synthesis: 3. Síntese de Fachadas Tipadas pelo Agente
    Interface_Synthesis --> Shadow_Execution: 4. Execução em Sombra (Shadow Run) para Validação
    Shadow_Execution --> Cutover: Migração Verificada com Zero Downtime
    Cutover --> [*]
```

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Identificação do Débito Semântico**: O risco central na era da IA não é código com erros de sintaxe, mas código sintaticamente perfeito cuja lógica conceitual está fragmentada.
2. **Arquitetura Nativa de IA**: Modularidade estrita, esquemas tipados inegociáveis e ausência de dependências cíclicas são requisitos indispensáveis.
3. **Decomposição com AST**: Grafos de sintaxe abstrata permitem aos agentes delimitar fronteiras de domínio e sintetizar fachadas com precisão.
4. **Execução em Sombra**: A validação em sombra (Shadow Run) garante equivalência comportamental exata antes da virada definitiva em produção.

### Referências
- **Playlist Oficial do Curso**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
"""

# ==============================================================================
# LECTURE 9 PORTUGUESE (pt-BR)
# ==============================================================================
lec9_slug = "2026-10-30-stanford-cs146s-9"
lec9_content = """---
slug: 2026-10-30-stanford-cs146s-9
title: "[Stanford CS146S #9] TDD Autônomo & Verificação Formal: Solvers Z3 SMT, Invariantes Baseados em Propriedades e Provas Matemáticas para Código de IA"
authors: [jbgih]
tags: [stanford-cs146s, autonomous-tdd, formal-verification, z3-smt-solver, property-based-testing, software-correctness, symbolic-execution]
date: 2026-10-30
keywords: [Test-Driven Development Autônomo ATDD, Verificação Formal Solver Z3 SMT, Property-Based Testing com Hypothesis, Provas Matemáticas para Código de LLM, Síntese de Invariantes em IA]
description: "Stanford CS146S Aula 9: Além dos testes unitários empíricos — Como agentes autônomos de IA utilizam Property-Based Testing (PBT), execução simbólica e solvers Z3 SMT para garantir correção matematicamente comprovável em códigos de missão crítica."
---

![TDD Autônomo e Verificação Formal com Z3 SMT Solver](./images/09_cs146s_autonomous_tdd_formal_verification.png)

Bem-vindo à nona parte da nossa análise técnica da série **CS146S: The Modern Software Developer da Universidade de Stanford**.

Nas aulas anteriores, estudamos engenharia de prompt, MCP, enxames multiagente, eBPF e arquiteturas nativas de IA. Na **Aula 9**, o currículo de Stanford enfrenta o maior dilema da computação contemporânea: **Como equipes de engenharia podem confiar em modelos de linguagem probabilísticos e não-determinísticos ao construir códigos de missão crítica para finanças, aeroespacial, criptografia e infraestrutura distribuída?**

Como Edsger Dijkstra afirmou há mais de meio século: *“Testes de programas podem demonstrar a presença de erros, mas nunca sua ausência!”* Nesta aula, pesquisadores de Stanford demonstram a transição indispensável de testes pontuais para o **Property-Based Testing (PBT) Autônomo**, a **Execução Simbólica** e a **Verificação Formal com o Solver Z3 SMT**.

{/* truncate */}

---

### 1. Os Limites dos Testes Unitários Baseados em Exemplos

Em testes unitários tradicionais, o desenvolvedor valida apenas alguns valores arbitrários:

```python
def test_calculate_fee():
    assert calculate_fee(100) == 5
    assert calculate_fee(0) == 0
```

Quando um agente de IA gera código para passar nesses testes, frequentemente ocorre o **Overfitting de Testes**:
- O agente sintetiza uma lógica que satisfaz especificamente essas 2 entradas, mas falha catastróficamente com números negativos, overflow de inteiros ou valores extremos.

---

### 2. Property-Based Testing (PBT) com Hypothesis

Em vez de testar números estáticos, o engenheiro formaliza **invariantes matemáticos universais**:

```text
Para toda entrada x pertencente ao Domínio de Entradas:
    Propriedade(f(x)) == Verdadeiro
```

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=0, max_value=1_000_000))
def test_fee_always_less_than_amount(amount):
    fee = calculate_fee(amount)
    assert 0 <= fee <= amount
```

O framework gera milhares de casos estocásticos de borda, localiza o menor contraexemplo possível (*Shrinking*) e força o agente de IA a implementar a lógica matemática correta e robusta.

---

### 3. Verificação Formal com o Solver Z3 SMT

O patamar máximo de garantia é a prova matemática formal através de solvers SMT (Satisfiability Modulo Theories):

```python
from z3 import Int, Solver, sat, unsat

# Verificação formal de invariantes de saldo
balance = Int('balance')
withdrawal = Int('withdrawal')
s = Solver()

# Pós-condição: Saldo nunca pode se tornar negativo
new_balance = balance - withdrawal
s.add(balance >= 0)
s.add(withdrawal > 0)
s.add(new_balance < 0) # Busca ativamente por um contraexemplo

if s.check() == unsat:
    print("Matematicamente Provado: Invariante válida para todas as entradas possíveis!")
else:
    print("Contraexemplo encontrado:", s.model())
```

Se o solver Z3 retornar `unsat` (insatisfatível), está matematicamente provado que, sob as pré-condições estabelecidas, **nenhum estado inválido de sistema jamais poderá ocorrer** — não importa se o sistema processar bilhões de transações.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Limites de Testes Simples**: Testes baseados em exemplos pontuais geram overfitting em agentes de IA e ignoram casos críticos de borda.
2. **Invariantes por PBT**: O teste baseado em propriedades valida leis fundamentais do sistema sob milhares de cenários estocásticos extremos.
3. **Provas Matemáticas com Z3**: Solvers SMT oferecem garantia matemática absoluta da correção algorítmica.
4. **Loop CEGAR de Autocura**: Contraexemplos gerados pelos solvers são devolvidos ao agente como especificações determinísticas para correção imediata do código.

### Referências
- **Playlist Oficial do Curso**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
"""

# ==============================================================================
# LECTURE 10 PORTUGUESE (pt-BR)
# ==============================================================================
lec10_slug = "2026-10-31-stanford-cs146s-10"
lec10_content = """---
slug: 2026-10-31-stanford-cs146s-10
title: "[Stanford CS146S #10] O Futuro da Engenharia de Software: Enxames de Agentes Autônomos, Pipelines Zero-Human Deployment e Gestão de Frotas de IA"
authors: [jbgih]
tags: [stanford-cs146s, autonomous-engineering, zero-human-deployments, ai-fleets, software-future, agent-swarms, system-governance]
date: 2026-10-31
keywords: [Equipes Autônomas de Engenharia de Software, Pipelines de Zero-Human Deployment, Gestão de Frotas de Agentes de IA, Governança Humano-Agente, Bases de Código Auto-Otimizáveis]
description: "A grande final de Stanford CS146S: A síntese do currículo de 10 semanas para a fábrica autônoma de software — pipelines sem intervenção humana, orquestração de frotas de IA e o papel redefinido do engenheiro de software como maestro de sistemas."
---

![O Futuro da Engenharia de Software e Frotas de IA](./images/10_cs146s_future_software_engineering_ai_fleets.png)

Bem-vindo à aula final e síntese da série **CS146S: The Modern Software Developer da Universidade de Stanford**.

Ao longo de dez semanas intensivas, este currículo desconstruiu cinco décadas de premissas sobre programação tradicional. Do surgimento da Engenharia Humano-Agente (Aula 1) e da física interna de Coding LLMs (Aula 2) ao protocolo MCP (Aula 3), harnesses autocicatrizantes (Aula 4), orquestração de enxames (Aula 5), observabilidade de kernel via eBPF (Aula 6), revisão automatizada de código em escala (Aula 7), arquiteturas nativas de IA (Aula 8) e verificação formal com solvers Z3 SMT (Aula 9).

Na **Aula 10**, os professores de Stanford unem todos esses fios conceituais em uma visão integrada do futuro da computação: **A Fábrica de Software Autônoma**. Analisamos a transição para pipelines de **Zero-Human Continuous Deployment**, a coordenação de **frotas globais de IA** e a consolidação do papel do engenheiro humano como **Maestro e Arquiteto de Sistemas**.

{/* truncate */}

---

### 1. A Fábrica de Software Autônoma: O Pipeline Zero-Human Deployment

No modelo maduro de engenharia de software nativo de IA, nenhuma linha de código em produção precisa ser digitada manualmente por humanos. O fluxo opera de forma contínua e autônoma:

```mermaid
flowchart LR
    Spec[1. Especificação Humana SPEC.md] --> Swarm[2. Enxame de Agentes de Implementação]
    Swarm --> Harness[3. Test Harness Autocicatrizante]
    Harness --> Proof[4. Prova Formal Z3 SMT]
    Proof --> Shadow[5. Execução em Sombra no Cluster]
    Shadow --> CanDeploy[6. Canary Zero-Human Deployment]
    CanDeploy --> Prod((7. Produção Global))
```

1. **Especificação & Invariantes**: O arquiteto humano elabora a especificação de produto e define as restrições inegociáveis.
2. **Síntese Concorrente por Enxames**: Dezenas de agentes especializados escrevem código e testes em paralelo.
3. **Validação Determinística**: O test harness fecha o ciclo de autocura eliminando regressões.
4. **Verificação Matemática Formal**: Algoritmos de missão crítica são provados via lógica simbólica.
5. **Execução em Sombra & Canary Deployment**: O novo código roda em paralelo com tráfego real sem impacto aos usuários até atingir 100% de estabilidade.

---

### 2. Gestão e Governança de Frotas de IA em Escala

À medida que centenas de agentes de IA trabalham simultaneamente na mesma base de código, as organizações exigem ferramentas rigorosas de governança:

- **Controle Orçamentário de Tokens**: Monitoramento em tempo real do custo por feature desenvolvida.
- **Trilhas de Auditoria Determinísticas**: Registro imutável de todas as chamadas de ferramentas e decisões lógicas dos agentes.
- **Guardrails de Segurança Invioláveis**: Bloqueio criptográfico de acesso a chaves mestras e bancos de produção não autorizados.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **A Fábrica Autônoma de Software**: A integração de SDD, enxames de agentes e verificação formal viabiliza pipelines contínuos de desenvolvimento sem toque manual.
2. **Pipelines Zero-Human**: A entrega contínua com validação em sombra e canários automatizados reduz o ciclo de entrega de semanas para minutos.
3. **Governança de Frotas de IA**: A liderança técnica foca na gestão de políticas, limites orçamentários de tokens e barreiras inegociáveis de segurança.
4. **O Engenheiro como Maestro**: O valor do profissional de tecnologia agora reside na formulação de problemas complexos, rigor arquitetural e supervisão estratégica de sistemas.

### Referências
- **Playlist Oficial do Curso**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Departamento**: Universidade de Stanford, Departamento de Ciência da Computação
"""

def main():
    print("=" * 65)
    print("Translating Stanford CS146S Batch 3 (Lec 8~10) into Brazilian Portuguese (pt-BR)...")
    print("=" * 65)
    save_pt_lecture(lec8_slug, lec8_content)
    save_pt_lecture(lec9_slug, lec9_content)
    save_pt_lecture(lec10_slug, lec10_content)
    print("\n[BATCH 3 COMPLETE] Lectures 8, 9, 10 staged and saved in pt-BR!")

if __name__ == "__main__":
    main()
