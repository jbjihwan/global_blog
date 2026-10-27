# -*- coding: utf-8 -*-
import os

base_dir = r"D:\ai\antigravity\global_blog"
pt_pages_dir = os.path.join(base_dir, "i18n", "pt-BR", "docusaurus-plugin-content-pages")
os.makedirs(pt_pages_dir, exist_ok=True)

# 1. Portuguese about.md
pt_about = """---
title: Sobre Mim & Global Dev Blog
description: Sobre Jihwan Park (jbjihwan) e o Global Dev Blog - Artigos e mergulhos técnicos profundos em IA, Robótica, Visão Computacional e Aprendizado por Reforço.
keywords: [Sobre mim, Jihwan Park, Engenheiro de IA, Robótica, Visão Computacional, Aprendizado por Reforço, Maeumjigi]
---

# Sobre Mim & Global Dev Blog

Bem-vindo ao **Global Dev Blog**, um diário técnico de engenharia de software e pesquisa mantido por **Jihwan Park (jbjihwan)**.

Este blog documenta implementações práticas, desafios reais de engenharia em produção, arquitetura de sistemas e benchmarks empíricos nas áreas de **Inteligência Artificial, Robótica, Visão Computacional Avançada e Aprendizado por Reforço**.

---

## 👨‍💻 Quem Sou Eu

Sou um engenheiro de software especializado em Inteligência Artificial e Robótica, focado em transformar formulações algorítmicas teóricas em sistemas resilientes de alta performance em tempo real, operando em dispositivos edge e clusters na nuvem. Minhas principais áreas de especialização incluem:

- **Sistemas Autônomos & Aprendizado por Reforço**: Formulação de Processos de Decisão de Markov (MDP), mapeamento contínuo-para-discreto de estados e ações, modelagem densa de recompensas (reward shaping) e transferência Sim-to-Real para robôs móveis.
- **Visão Computacional Profunda**: Pipelines de inferência multiestágio em tempo real, detecção de objetos (YOLOv3/v5/v8), rastreamento multiobjeto (CSRT, DeepSORT), Super-Resolução (EDSR) e Reconhecimento Óptico de Caracteres (OCR) com filtragem temporal.
- **Processamento de Linguagem Natural & IA Segura**: Fine-tuning eficiente de parâmetros (PEFT/LoRA) em arquiteturas Llama, regressão ordinal sob desbalanceamento severo de classes e guardrails determinísticos para prevenção de crises.
- **Engenharia de ML Full-Stack**: Microserviços assíncronos de alto rendimento com FastAPI, conteinerização Docker, documentação técnica multilíngue em Docusaurus e aplicações móveis em React Native.

---

## 📚 Séries Principais Deste Blog

### 1. 🧠 Diário de Desenvolvimento Maeumjigi (23 Episódios)
Engenharia e arquitetura de um chatbot de intervenção psicológica em saúde mental 24/7:
- Geração sintética de diálogos clínicos via pipelines automatizados de LLM.
- Mitigação de excesso de confiança (weak-label overconfidence) através de regressão ordinal com limiares cumulativos.
- Guardrails determinísticos em sub-milissegundos para detecção de crises e protocolos de emergência.

### 2. 🤖 Robô Autônomo com Q-Learning no Webots (5 Episódios)
Do aprendizado por tentativa e erro à navegação autônoma resiliente com desvio de obstáculos:
- Discretização de sensores de distância de 6 setores em 648 estados compactos.
- Reward shaping geométrico por velocidade e delta de distância para evitar mínimos locais.
- Implementação prática da Q-Table em hardware físico com Arduino Uno e microcontroladores.

### 3. 🚗 Sistema de Visão Computacional ANPR para Dashcam (5 Episódios)
Pipeline embarcado de visão em tempo real para identificação veicular em alta velocidade:
- Pipeline ponta a ponta de 6 estágios operando com restrição rígida de 30 FPS.
- Ajuste dinâmico de faixas de rolamento por polinômios e cálculo de IoU poligonal.
- Super-resolução EDSR 4x para placas degradadas e votação majoritária temporal no OCR.

### 4. 🎓 Stanford CS146S: Engenharia de Software Moderna (10 Episódios)
Exploração aprofundada do currículo avançado da Universidade de Stanford:
- Do desenvolvedor digitador ao maestro de sistemas de IA autônomos.
- Protocolo MCP (Model Context Protocol), orquestração de enxames de agentes e verificação formal via Z3 SMT.
"""

# 2. Portuguese contact.md
pt_contact = """---
title: Contato
description: Informações de contato de Jihwan Park, autor e mantenedor do Global Dev Blog.
keywords: [Contato, Jihwan Park, E-mail, GitHub, Colaboração Técnica]
---

# Contato

Obrigado por visitar o **Global Dev Blog**. Se você tiver dúvidas sobre implementações de código, sugestões de melhorias, propostas de projetos ou interesse em colaboração técnica em IA e Robótica, sinta-se à vontade para entrar em contato.

---

## 📬 Contato Direto

- **E-mail**: [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com)  
  *Para discussões técnicas, propostas de pesquisa ou dúvidas gerais.*

---

## 💻 Código Aberto & Repositórios

- **Perfil no GitHub**: [@jbjihwan](https://github.com/jbjihwan)
- **Código-fonte do Blog**: [github.com/jbjihwan/global_blog](https://github.com/jbjihwan/global_blog)
- **Issues e Discussões**: Se você encontrar erros de digitação, problemas no código ou links quebrados, pode abrir uma issue diretamente no GitHub:
  👉 [Abrir uma Issue no GitHub](https://github.com/jbjihwan/global_blog/issues)

---

## ⏱️ Tempo de Resposta

Normalmente respondo a consultas técnicas e e-mails dentro de **24 a 48 horas**.
"""

# 3. Portuguese privacy-policy.md
pt_privacy = """---
title: Política de Privacidade
description: Política de Privacidade do Global Dev Blog referente ao uso do Google Analytics 4, cookies do Google AdSense e conformidade com LGPD/GDPR.
keywords: [Política de Privacidade, Google AdSense, Google Analytics, LGPD, GDPR, Cookies]
---

# Política de Privacidade

**Última atualização: 27 de Outubro de 2026**

O **Global Dev Blog** (`https://globaldevlog.com`), mantido por Jihwan Park, respeita a privacidade de seus visitantes. Esta política descreve como as informações são coletadas, utilizadas e protegidas em conformidade com as diretrizes internacionais de proteção de dados, incluindo a LGPD (Lei Geral de Proteção de Dados - Brasil) e a GDPR (Regulamento Geral sobre a Proteção de Dados - União Europeia).

---

## 1. Coleta e Uso de Informações Técnicas

O Global Dev Blog é um site puramente estático hospedado em CDN Anycast de alta performance. O site não exige cadastro, criação de conta de usuário nem armazena senhas ou dados bancários em servidores próprios.

No entanto, para melhorar a experiência do usuário, monitorar o desempenho técnico e exibir conteúdos relevantes, utilizamos serviços analíticos e de publicidade de terceiros.

---

## 2. Google Analytics 4 (GA4)

Utilizamos o **Google Analytics 4** para coletar dados agregados e anônimos sobre o tráfego do blog. Esses dados incluem:
- Páginas visitadas e tempo de permanência em cada artigo técnico.
- Tipo de navegador, sistema operacional e categoria do dispositivo (desktop ou mobile).
- País e cidade aproximada de acesso (com mascaramento automático de endereço IP).
- Páginas de origem (referrers) e canais de aquisição de tráfego.

Essas informações são utilizadas exclusivamente para entender quais artigos de IA, Robótica e Visão Computacional geram maior interesse técnico e para otimizar a velocidade de carregamento global do site.

---

## 3. Google AdSense e Cookies de Terceiros

Este site utiliza o **Google AdSense** para exibir anúncios automáticos. O Google utiliza cookies (como o cookie DoubleClick DART) para veicular anúncios com base nas visitas anteriores dos usuários a este e a outros sites na internet.

- **Controle de Anúncios Personalizados**: Os usuários podem desativar o uso de cookies para publicidade personalizada acessando as [Configurações de Anúncios do Google](https://www.google.com/settings/ads).
- Alternativamente, você pode optar por não permitir o uso de cookies de fornecedores terceiros para publicidade baseada em interesses visitando o site [www.aboutads.info](https://www.aboutads.info).

---

## 4. Arquivos de Log e Segurança

Como a maioria dos provedores de infraestrutura web (GitHub Pages e Cloudflare), registros padrão de tráfego (como timestamps e códigos de status HTTP) podem ser processados temporariamente para fins de segurança, prevenção de ataques de negação de serviço (DDoS) e garantia de integridade da infraestrutura.

---

## 5. Seus Direitos de Privacidade

Dependendo da sua localização, você possui direitos sob leis de privacidade como a LGPD ou GDPR, incluindo o direito de solicitar esclarecimentos sobre o tratamento de dados.

Se você tiver qualquer dúvida sobre esta Política de Privacidade ou sobre as práticas deste blog, entre em contato através do e-mail:  
📩 **jbgihwan@gmail.com**
"""

with open(os.path.join(pt_pages_dir, "about.md"), "w", encoding="utf-8") as f:
    f.write(pt_about.strip() + "\n")
print(f"[OK] Created {pt_pages_dir}\\about.md")

with open(os.path.join(pt_pages_dir, "contact.md"), "w", encoding="utf-8") as f:
    f.write(pt_contact.strip() + "\n")
print(f"[OK] Created {pt_pages_dir}\\contact.md")

with open(os.path.join(pt_pages_dir, "privacy-policy.md"), "w", encoding="utf-8") as f:
    f.write(pt_privacy.strip() + "\n")
print(f"[OK] Created {pt_pages_dir}\\privacy-policy.md")
