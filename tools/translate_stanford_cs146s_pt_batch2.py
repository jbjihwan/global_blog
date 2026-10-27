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
# LECTURE 4 PORTUGUESE (pt-BR)
# ==============================================================================
lec4_slug = "2026-10-25-stanford-cs146s-4"
lec4_content = """---
slug: stanford-cs146s-4-spec-driven-code-generation-test-harnesses
title: "[Stanford CS146S #4] Geração de Código Orientada por Especificação & Test Harnesses: Loops Autocicatrizantes de Regressão com Claude Code & Cursor"
authors: [jbgih]
tags: [stanford-cs146s, spec-driven-development, test-harness, self-healing-code, claude-code, cursor, software-engineering, regression-testing]
date: 2026-10-25
keywords: [Spec-Driven Development, Test Harness para IA de Código, Geração de Código Autocicatrizante, Claude Code Testes Automatizados, Verificação de Regressão LLM]
description: "Stanford CS146S Aula 4: Como escapar da armadilha do 'Vibe Coding' — construção de test harnesses fechados e ciclos de autorrecuperação Red-Green-Refactor com Claude Code e Cursor."
---

![Geração de Código Orientada por Especificação e Test Harness Autocicatrizante](./images/04_cs146s_spec_driven_test_harness.png)

Bem-vindo à quarta parte da nossa análise técnica da série **CS146S: The Modern Software Developer da Universidade de Stanford**.

Nas aulas anteriores, exploramos a mentalidade de maestro de IA, o funcionamento interno dos modelos de linguagem e o Model Context Protocol (MCP). Na **Aula 4 (Semana 3)**, o curso enfrenta o desafio de engenharia mais urgente das equipes de tecnologia: **Como construir sistemas de software corporativos de milhares de linhas com confiabilidade, quando os LLMs inevitavelmente alucinam, introduzem regressões silenciosas e se desviam dos requisitos de produto?**

A abordagem ingênua — popularmente chamada nas redes sociais de "Vibe Coding" ou prompt conversacional desestruturado — falha de forma catastrófica em ambientes de missão crítica. Com base em experimentos de laboratório de Stanford, esta aula formaliza o **Spec-Driven Development (SDD)** e ensina a implementar um **Test Harness** automatizado com **loops de feedback autocicatrizantes (Self-Healing Loops)** usando ferramentas modernas como Claude Code e Cursor.

{/* truncate */}

---

### 1. A Falácia do "Vibe Coding": Por Que o Prompting Sem Especificação Entra em Colapso

Quando desenvolvedores confiam em interações puramente conversacionais com agentes de IA, a entropia do sistema cresce a cada interação:

```mermaid
flowchart TD
    subgraph Vibe_Coding_Entropy ["O Antipadrão: Conversational Vibe Coding"]
        V1["Prompt Vago: 'Adicione um checkout de pagamento'"] --> V2["LLM gera 300 linhas de código"]
        V2 --> V3["Desenvolvedor bate o olho rapidamente (Parece correto)"]
        V3 --> V4["Merge direto na branch principal"]
        V4 --> V5["Próximo Prompt: 'Adicione cupons de desconto'"]
        V5 --> V6["LLM sobrescreve silenciosamente a lógica de status de pagamento"]
        V6 --> V7["Regressão catastrófica em produção"]
    end

    subgraph Spec_Driven_Determinism ["Stanford CS146S: Spec-Driven Development (SDD)"]
        S1["Especificação Formal (PRD & Contrato de Interfaces)"] --> S2["Suíte de Testes Determinística (Harness)"]
        S2 --> S3["Geração de Código por IA (Claude Code / Cursor)"]
        S3 --> S4["Execução Automatizada de Testes (pytest / vitest)"]
        S4 -->|Testes Falham (Vermelho)| S5["Loop de Autocorreção com Stacktraces Reais"]
        S5 --> S3
        S4 -->|Todos os Testes Aprovados (Verde)| S6["Merge Verificado sem Regressões"]
    end
```

O "Vibe Coding" fracassa porque o modelo de linguagem esquece restrições anteriores ao longo da conversa (*Attention Dilution*) e não existe nenhuma autoridade determinística que valide o comportamento do código.

---

### 2. O Test Harness Fechado: O Ciclo Red-Green-Refactor para Agentes de IA

No Spec-Driven Development, o Test Harness funciona como uma barreira matemática inegociável:

```mermaid
stateDiagram-v2
    [*] --> SpecDefinition: Desenvolvedor define invariantes em SPEC.md
    SpecDefinition --> TestGeneration: Geração de testes unitários e de propriedade (RED)
    TestGeneration --> AgentCoding: Agente de IA sintetiza o código-fonte
    
    state Self_Healing_Loop {
        [*] --> RunHarness
        RunHarness --> AnalyzeTrace: Teste falha (Assertion Error)
        AnalyzeTrace --> SynthesizePatch: Agente repara linhas pontuais
        SynthesizePatch --> RunHarness: Reexecução imediata dos testes
    }
    
    AgentCoding --> Self_Healing_Loop
    Self_Healing_Loop --> AllGreen: Todos os testes aprovados (GREEN)
    AllGreen --> Refactor: Limpeza de código e verificação de tipos
    Refactor --> Done: Pull Request pronto para produção
    Done --> [*]
```

#### As Três Regras de Ouro do Harness Engineering:
1. **Escreva os Testes Primeiro**: Os critérios de aceitação devem estar formalizados antes que o agente gere a primeira linha de implementação.
2. **Arquivos de Teste Imutáveis**: O agente tem permissão para alterar apenas arquivos de implementação — nunca a suíte de testes (*Prevenção de Adulteração de Testes*).
3. **Feedback Determinístico**: O agente consome códigos de saída padronizados da CLI (0 = Sucesso; diferente de 0 = Falha detalhada com números de linha).

---

### 3. Fluxos de Trabalho Práticos com Claude Code & Cursor

Nas sessões práticas de Stanford, os estudantes implementaram microserviços com Claude Code sob estrita governança SDD:
- **Arquivo de Regras `CLAUDE.md`**: Define comandos de build, execução de testes e diretrizes arquiteturais.
- **Execução em Subprocesso**: O Claude Code executa `pytest tests/test_payment.py` localmente no terminal.
- **Reparação Iterativa**: Se houver falha, o agente lê a mensagem de erro, diagnostica a raiz do problema e ajusta os arquivos necessários.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Fim do Vibe Coding**: Prompts conversacionais soltos geram entropia acelerada e regressões silenciosas no código.
2. **Spec-Driven Development (SDD)**: Especificações formais e suítes de testes determinísticas são os alicerces indispensáveis da IA confiável.
3. **Loops Autocicatrizantes**: Ciclos fechados (teste $\rightarrow$ diagnóstico $\rightarrow$ patch atômico) permitem que agentes corrijam bugs de forma autônoma.
4. **Imutabilidade dos Testes**: O agente jamais deve ter permissão para modificar os testes a fim de forçar aprovação artificial.

### Referências
- **Playlist Oficial do Curso**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
"""

# ==============================================================================
# LECTURE 5 PORTUGUESE (pt-BR)
# ==============================================================================
lec5_slug = "2026-10-26-stanford-cs146s-5"
lec5_content = """---
slug: 2026-10-26-stanford-cs146s-5
title: "[Stanford CS146S #5] Sistemas Multiagente & Orquestração de Enxames: Coordenação de LLMs Arquitetos, Implementadores e Críticos"
authors: [jbgih]
tags: [stanford, cs146s, multi-agent-systems, swarm-orchestration, llm-agents, software-engineering, distributed-systems]
date: 2026-10-26
keywords: [Orquestração Multiagente, Padrão Arquiteto Implementador Crítico, Geração de Código em Enxame Autônomo, Fluxos de Agentes DAG, Protocolo de Comunicação Inter-Agentes]
description: "Stanford CS146S Aula 5: Por que LLMs monolíticos de contexto único colapsam em repositórios corporativos e como coordenar agentes especializados de Arquitetura, Implementação e Crítica em fluxos assíncronos DAG."
---

![Arquitetura de Orquestração de Enxame Multiagente](./images/05_cs146s_multi_agent_swarm.png)

Bem-vindo à Aula 5 da nossa análise técnica da série **CS146S: The Modern Software Developer da Universidade de Stanford**.

Nas aulas anteriores, exploramos engenharia de prompt, mecanismos de transformadores, o protocolo MCP e test harnesses autocicatrizantes. Todos esses modelos compartilhavam uma premissa básica: **uma única sessão primária de LLM** interagindo com um desenvolvedor ou repositório.

Contudo, quando um projeto de software ultrapassa milhares de linhas de código e dezenas de microserviços, essa abordagem monolítica desmorona. Agentes individuais sofrem de **saturação de contexto, dispersão de atenção (*Attention Dilution*) e bloqueio cognitivo**.

Nesta aula, os professores de Stanford apresentam a fronteira da engenharia nativa de IA: **Sistemas Multiagente (MAS) e Orquestração de Enxames (Swarm Orchestration)**. Verificamos como a divisão funcional entre **Arquitetos, Implementadores e Críticos**, operando sobre grafos acíclicos dirigidos (DAGs) e barramentos de mensagens estruturados, multiplica a precisão e a escalabilidade dos projetos.

{/* truncate */}

---

### 1. Os Limites de Escala de Agentes Monolíticos

Por que não podemos simplesmente despejar um repositório corporativo de 500.000 linhas em uma janela de contexto de 1 milhão de tokens e pedir para a IA *"refatorar todo o pipeline de pagamentos"*?

Pesquisadores de Stanford identificam três gargalos fundamentais:

```mermaid
flowchart TD
    subgraph Monolithic_Failure ["Gargalos dos Agentes Monolíticos Individuais"]
        A1["Contexto Gigantesco (500k+ Tokens)"] --> A2["Attention Dilution & Degradação Needle-in-a-Haystack"]
        A2 --> A3["Instruction Drift: O modelo esquece restrições iniciais ao ler arquivos posteriores"]
        
        B1["Colusão de Papéis no Agente Único"] --> B2["Self-Confirmation Bias: O gerador avalia o próprio código como correto"]
        B2 --> B3["Armadilha da Alucinação: Falta de contraprova objetiva"]
        
        C1["Execução Estritamente Sequencial"] --> C2["Alta Latência: Uma única thread processa tarefas complexas em série"]
    end
```

---

### 2. O Padrão Arquiteto-Implementador-Crítico (AIC)

A solução apresentada no Stanford CS146S é a separação funcional em três papéis complementares de agentes:

```mermaid
flowchart LR
    User[Arquiteto Humano / PRD] --> Arch[1. Agente Arquiteto Líder]
    Arch -->|Decomposição em Subtarefas & Esquemas de API| Impl1[2a. Implementador Módulo A]
    Arch -->|Paralelização Assíncrona| Impl2[2b. Implementador Módulo B]
    
    Impl1 --> Critic[3. Agente Crítico & Verificador]
    Impl2 --> Critic
    
    Critic -->|Feedback Detalhado em Falhas| Impl1
    Critic -->|Suíte de Testes 100% Verde & Auditoria de Segurança| Output[Base de Código Unificada e Verificada]
```

1. **Lead Architect Agent**: Analisa o PRD, decompõe o problema em um Grafo Acíclico Dirigido (DAG) de tarefas e define contratos de interface estritos.
2. **Implementer Agents**: Múltiplas instâncias autônomas que implementam módulos individuais concorrentemente.
3. **Critic & Verifier Agent**: Executa auditorias determinísticas de segurança, linters e testes de integração. Como o crítico não escreveu o código, ele está 100% livre do *Viés de Autoconfirmação*.

---

### 3. Orquestração Assíncrona via DAG & Memória Compartilhada

Para que dezenas de agentes colaborem sem bloqueios concorrentes, o sistema adota payloads estruturados em JSON e um quadro-negro centralizado de contexto compartilhado (Shared Blackboard Memory).

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Limites Monolíticos**: Agentes de contexto único sofrem de dispersão de atenção e viés de autoconfirmação em grandes bases de código.
2. **Padrão Arquiteto-Implementador-Crítico**: A divisão de papéis permite desenvolvimento paralelo com auditoria independente de qualidade.
3. **Fluxos em DAG**: Grafos assíncronos evitam bloqueios mútuos e escalam radicalmente a velocidade de entrega.
4. **Contratos Estruturados**: Esquemas estritos em JSON entre agentes garantem determinismo e integridade sistêmica.

### Referências
- **Playlist Oficial do Curso**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
"""

# ==============================================================================
# LECTURE 6 PORTUGUESE (pt-BR)
# ==============================================================================
lec6_slug = "2026-10-27-stanford-cs146s-6"
lec6_content = """---
slug: 2026-10-27-stanford-cs146s-6
title: "[Stanford CS146S #6] Depuração Guiada por IA & Perfilamento em Tempo de Execução: eBPF, Rastreamento Dinâmico e LLMs para Mitigação de Incidentes"
authors: [jbgih]
tags: [stanford, cs146s, ebpf, dynamic-tracing, ai-debugging, incident-response, site-reliability-engineering, linux-kernel]
date: 2026-10-27
keywords: [Depuração de Runtime com IA, eBPF Rastreamento Dinâmico LLM, Mitigação Autônoma de Incidentes, Observabilidade de Kernel IA SRE, Profiling de Performance em Produção]
description: "Stanford CS146S Aula 6: Como a fusão entre extended Berkeley Packet Filters (eBPF) e agentes de diagnóstico LLM revoluciona a depuração em produção — do tracing não-invasivo de kernel ao hotpatch automatizado."
---

![Depuração Guiada por IA e Rastreamento Dinâmico com eBPF](./images/06_cs146s_ai_debugging_ebpf.png)

Bem-vindo à Aula 6 da nossa análise técnica da série **CS146S: The Modern Software Developer da Universidade de Stanford**.

Na aula anterior, estudamos a orquestração de enxames multiagente para construção de bases de código modulares. Porém, mesmo o software mais rigorosamente testado em laboratório encontra a realidade implacável dos ambientes de produção.

Às 3 da manhã, quando um deadlock obscuro de concorrência congela um cluster distribuído de processamento ou uma consulta sem índice faz a latência disparar para 12 segundos, as abordagens convencionais de depuração fracassam. Análises estáticas não capturam condições dinâmicas de corrida, injeções invasivas de logs alteram a cronologia dos eventos (*Efeito Heisenbug*), e plataformas de APM afogam os engenheiros de confiabilidade (SREs) em gigabytes de ruído.

Nesta aula, os professores de Stanford apresentam o estado da arte da resiliência operacional: **Depuração Guiada por IA & Perfilamento em Tempo de Execução**. Conectando programas **eBPF (extended Berkeley Packet Filters)** a **agentes de diagnóstico SRE baseados em LLMs**, engenheiros capturam telemetria de kernel com custo próximo a zero, identificam a causa-raiz em segundos e geram hotpatches verificados de forma autônoma.

{/* truncate */}

---

### 1. O Dilema da Depuração Tradicional em Produção

Ao enfrentar interrupções em microserviços de alto rendimento, os engenheiros lidam com três paradoxos:

```mermaid
flowchart TD
    subgraph Traditional_Failure ["Vulnerabilidades da Triagem Tradicional de Incidentes"]
        A1["Logging Invasivo / Hooks de Depuração"] --> A2["Efeito Heisenbug: O timing muda e o bug desaparece sob observação"]
        
        B1["APM Distribuído & Agregação Massiva de Logs"] --> B2["Cegueira por Logs: Milhões de linhas JSON ocultam a causa real"]
        B2 --> B3["Sobrecarga Cognitiva: Humanos não conseguem correlacionar threads entre pods"]
        
        C1["Core Dumps Pós-Mortem"] --> C2["Alto Downtime: O serviço precisa cair para capturar o estado da memória"]
    end
```

---

### 2. A Solução: Observabilidade de Kernel via eBPF + Diagnóstico por IA

O eBPF permite executar programas seguros de bytecode diretamente no espaço de kernel do Linux sem recompilar o kernel nem carregar módulos perigosos. Dessa forma, chamadas de sistema (syscalls), sockets de rede e kprobes são monitorados com overhead imperceptível.

```mermaid
sequenceDiagram
    autonumber
    participant K as Kernel Linux (Probes eBPF)
    participant RB as Lockless Ring Buffer
    participant D as Agente AI SRE (Diagnóstico LLM)
    participant GH as GitHub CI / Pipeline de Hotpatch

    K->>RB: Capturar latência de syscalls & contenção de sockets em tempo real
    RB-->>D: Streaming de telemetria (Flamegraphs & picos de latência)
    D->>D: O LLM analisa traces de kernel e correlaciona com o código-fonte
    D-->>D: Causa-raiz diagnosticada: Contenção de Mutex em worker_pool.rs:142
    D->>GH: Sintetizar Pull Request de Hotpatch com patch atômico corretivo
```

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Limites do Debugging Convencional**: Logs invasivos alteram o tempo das condições de corrida (Heisenbugs) e ferramentas de APM inundam equipes com ruído.
2. **Precisão com eBPF**: Rastreamento em nível de kernel intercepta chamadas de sistema com overhead próximo a zero e sem alterar o código da aplicação.
3. **Diagnóstico Automatizado**: Agentes LLM SRE analisam buffers de telemetria e localizam o ponto exato da falha na base de código.
4. **Resolução em Minutos**: Da análise de traces à síntese de um hotpatch validado por testes, o tempo de restauração (MTTR) cai drasticamente.

### Referências
- **Playlist Oficial do Curso**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
"""

# ==============================================================================
# LECTURE 7 PORTUGUESE (pt-BR)
# ==============================================================================
lec7_slug = "2026-10-28-stanford-cs146s-7"
lec7_content = """---
slug: 2026-10-28-stanford-cs146s-7
title: "[Stanford CS146S #7] Revisão Automatizada de Código em Escala: Linters com AST, Análise de Taint de Segurança e Revisores Autônomos de PR com LLM"
authors: [jbgih]
tags: [stanford, cs146s, code-review, static-analysis, ast, taint-analysis, llm-pr-review, devops, security]
date: 2026-10-28
keywords: [Revisão Automatizada de Código em Escala, Análise Estática Baseada em AST, Análise de Taint de Segurança LLM, Revisor Autônomo de Pull Request, Continuous Integration Guardrails de IA]
description: "Stanford CS146S Aula 7: Como equipes de engenharia escalam revisões de código — combinação de linters em Abstract Syntax Tree (AST), análise estática de taint e revisores semânticos com LLM para eliminar bikeshedding e brechas de segurança."
---

![Revisão Automatizada de Código em Escala](./images/07_cs146s_code_review_at_scale.png)

Bem-vindo à Aula 7 da nossa análise técnica da série **CS146S: The Modern Software Developer da Universidade de Stanford**.

Na aula anterior, analisamos a resolução de incidentes em produção com eBPF e agentes de IA. Contudo, qualquer líder técnico sênior sabe: o bug mais barato e seguro é **aquele que nunca chega a ser mesclado na branch principal**.

Em organizações de tecnologia modernas, a revisão de código em Pull Requests (PR Review) é o guardião central da qualidade, integridade arquitetural e segurança. Porém, à medida que os times crescem, a revisão humana converte-se em um gargalo operacional massivo. Engenheiros seniores perdem de 15 a 20 horas semanais analisando diffs, debatem detalhes cosméticos irrelevantes (*Bikeshedding*) e, exaustos diante de PRs com mais de mil linhas (*Review Fatigue*), deixam passar condições de corrida sutis ou injeções SQL.

Nesta aula, os professores de Stanford apresentam a arquitetura de **Revisão Automatizada de Código em Escala**. Através de uma hierarquia em três níveis composta por **Linters com AST (Tree-sitter, Semgrep)**, **Análise Estática de Taint** e **Revisores Autônomos de PR com LLMs**, as equipes eliminam 90% do trabalho mecânico de revisão e bloqueiam vulnerabilidades com determinismo absoluto.

{/* truncate */}

---

### 1. A Crise da Revisão de Código Manual

Por que o modelo tradicional de revisão humana falha ao escalar?

```mermaid
flowchart TD
    subgraph Review_Breakdown ["Os Três Grandes Desafios da Revisão Humana"]
        A1["A Armadilha do Bikeshedding"] --> A2["Discussões intermináveis sobre formatação e convenções de nomenclatura"]
        A2 --> A3["Latência Operacional: PRs bloqueados por dias por detalhes cosméticos"]
        
        B1["Fadiga Cognitiva do Revisor"] --> B2["Diff de 10 linhas: 10 apontamentos críticos.<br/>Diff de 1.000 linhas: 'LGTM' (Looks Good To Me)"]
        B2 --> B3["Vulnerabilidades críticas passam despercebidas para a produção"]
        
        C1["Cegueira de Contexto"] --> C2["O humano analisa apenas o trecho do diff, sem rastrear o grafo de chamadas completo"]
    end
```

---

### 2. A Hierarquia Automatizada de Revisão em Três Camadas

Stanford propõe uma linha de defesa estruturada:

```mermaid
flowchart TD
    PR[Novo Pull Request Enviado] --> Tier1["Nível 1: Linters com AST (Tree-sitter / Semgrep)<br/>Execução: < 2 segundos | Determinístico"]
    Tier1 -->|Erro de Sintaxe ou Violação de Fronteira| Block1[PR bloqueado imediatamente com sugestão de correção inline]
    
    Tier1 -->|Aprovado| Tier2["Nível 2: Análise Interprocedural de Taint<br/>Rastreia fluxo de dados: Entrada Não-Confiável -> Sink Crítico"]
    Tier2 -->|Caminho de SQLi / XSS / RCE Detectado| Block2[PR bloqueado com grafo visual de Taint]
    
    Tier2 -->|Aprovado| Tier3["Nível 3: Revisor Autônomo de PR com LLM<br/>Avalia intenção semântica & desvio arquitetural"]
    Tier3 -->|Aprovado| Human[Aprovação Humana Estratégica Final]
```

1. **Nível 1 (Linters com AST)**: Inspeciona a árvore sintática abstrata em milissegundos, bloqueando APIs inseguras e violações de fronteiras modulares.
2. **Nível 2 (Análise de Taint)**: Rastreia se entradas de usuários não validadas alcançam pontos sensíveis de execução (como comandos SQL ou funções de shell).
3. **Nível 3 (Revisor com LLM)**: Avalia a coerência semântica do código, conformidade com os contratos de interface e surgimento de débitos de arquitetura.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Automação Contra a Fadiga**: Revisões manuais colapsam diante de grandes diffs devido ao esgotamento cognitivo e debates cosméticos.
2. **Defesa em Três Níveis**: Linters com AST cuidam da sintaxe, análise de taint garante segurança de dados e LLMs avaliam integridade arquitetural.
3. **Queda Drástica de Latência**: 90% do trabalho repetitivo de revisão é resolvido instantaneamente no pipeline de CI.
4. **Foco no Que Importa**: Engenheiros seniores concentram-se exclusivamente em decisões estratégicas de design de sistemas.

### Referências
- **Playlist Oficial do Curso**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
"""

def main():
    print("=" * 65)
    print("Translating Stanford CS146S Batch 2 (Lec 4~7) into Brazilian Portuguese (pt-BR)...")
    print("=" * 65)
    save_pt_lecture(lec4_slug, lec4_content)
    save_pt_lecture(lec5_slug, lec5_content)
    save_pt_lecture(lec6_slug, lec6_content)
    save_pt_lecture(lec7_slug, lec7_content)
    print("\n[BATCH 2 COMPLETE] Lectures 4, 5, 6, 7 staged and saved in pt-BR!")

if __name__ == "__main__":
    main()
