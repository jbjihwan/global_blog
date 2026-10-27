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
# 1. STATIC SITE SECURITY HARDENING (npm audit truth)
# ==============================================================================
p1_slug = "2026-10-18-static-site-security-hardening"
p1_content = """---
slug: static-site-security-npm-audit-truth
title: "[Guia 2026] Resolvendo Vulnerabilidades do npm audit sem Quebrar Builds: A Verdade sobre o npm audit fix --force"
authors: [jbgih]
tags: [web-security, npm-audit, docusaurus, devops, supply-chain]
keywords: [Correção npm audit fix, Risco npm audit fix force, Segurança de Sites Estáticos, Vulnerabilidades npm, Falhas de Segurança GHSA]
description: "Como resolver vulnerabilidades reportadas pelo npm audit sem quebrar builds de produção. Por que 45 falhas de ferramentas de compilação em sites estáticos não representam risco em tempo de execução e como tratar alertas do GHSA com segurança."
---

Todo desenvolvedor frontend moderno conhece aquela súbita onda de adrenalina: você roda `npm audit` no repositório do seu blog ou documentação técnica, e o terminal alerta em vermelho brilhante:

```text
45 vulnerabilities (15 moderate, 15 high, 15 critical)
To address all issues (including breaking changes), run:
  npm audit fix --force
```

Termos como **Critical**, **Remote Code Execution (RCE)** e **Prototype Pollution** ativam imediatamente o reflexo de digitar `npm audit fix --force` para eliminar os avisos vermelhos o mais rápido possível.

No entanto, no universo dos Geradores de Sites Estáticos (**Static Site Generators - SSG**) como Docusaurus, Next.js (SSG) ou Hugo hospedados em GitHub Pages ou AWS S3, esse comando costuma ser um erro fatal: ele quebra compilações de produção ao forçar atualizações com breaking changes, sem aumentar a segurança real do seu site em um único porcento.

{/* truncate */}

---

### 1. Modelagem de Ameaças: Servidor Web Dinâmico vs. Site Estático (SSG)

Para compreender por que a maioria dos alertas de `npm audit` em sites estáticos são falsos positivos em relação à segurança de produção, analisamos a superfície fundamental de ataque:

![Modelagem de Ameaças: Servidor Web Dinâmico vs Site Estático](./images/01_threat_model.png)

#### Servidor Dinâmico Tradicional (Node.js / Express / Django)
- **Processo Ativo 24/7**: Um daemon do Node.js escuta requisições continuamente nas portas 80 e 443.
- **Execução em Tempo Real**: Quando uma requisição HTTP maliciosa chega, ela atravessa middlewares. Qualquer falha (como Prototype Pollution no `lodash` ou RCE em template engines) pode comprometer o servidor inteiro e vazar variáveis de ambiente.

#### Site Estático (Docusaurus / GitHub Pages CDN)
- **Uso Estritamente em Tempo de Build**: O Node.js é executado apenas na sua máquina local ou em runners efêmeros do GitHub Actions durante o processo de geração.
- **Zero Processos Backend em Runtime**: Os visitantes recebem exclusivamente arquivos estáticos HTML, CSS e JavaScript pré-compilados entregues por CDNs Anycast globais.
- **Risco de RCE = 0%**: Mesmo que uma ferramenta de build (`webpack`, `micromatch`) contenha uma vulnerabilidade teórica de RCE, em produção não existe nenhum servidor ouvindo requisições para explorar essa falha.

---

### 2. Os Riscos Reais de Executar `npm audit fix --force`

O parâmetro `--force` instrui o npm a instalar saltos de versão maior (*major version bumps*), que introduzem quebras de retrocompatibilidade. No ecossistema Docusaurus, isso frequentemente atualiza plugins do Webpack ou Babel para versões ainda incompatíveis com o framework. O resultado: os avisos de vulnerabilidade somem, mas o comando `npm run build` passa a falhar com erros de sintaxe indecifráveis.

---

### 3. Guia de 4 Passos para Resolução Segura

```mermaid
flowchart TD
    A[npm audit reporta vulnerabilidades] --> B{A falha afeta devDependencies?}
    B -->|Sim: Ferramentas de build como Webpack/Babel| C[Inspecionar: O código é injetado no bundle do cliente?]
    C -->|Não: Apenas ferramenta de build| D[Risco em SSG: 0% | NÃO rode npm audit fix --force!]
    C -->|Sim: Runtime do cliente| E[Atualização seletiva via package.json overrides]
    B -->|Não: Dependência real de produção| E
```

1. **Classifique o Escopo**: Separe rigorosamente ferramentas de desenvolvimento (`devDependencies`) de bibliotecas enviadas ao navegador.
2. **Utilize Overrides Seletivos**: Use a seção `overrides` do `package.json` para corrigir dependências transitivas específicas sem quebrar dependências raiz:
   ```json
   "overrides": {
     "nth-check": "^2.1.1"
   }
   ```
3. **Auditoria Segura no CI**: Em pipelines de integração contínua para sites estáticos, execute `npm audit --omit=dev` para avaliar apenas o que vai para os clientes.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Evite `npm audit fix --force`**: Comandos forçados quebram pipelines ao introduzir alterações incompatíveis de versão maior.
2. **Vantagem de Segurança do SSG**: Por não haver servidores Node.js rodando em produção, falhas de ferramentas de compilação têm risco zero de exploração em runtime.
3. **Atualizações Seletivas**: Utilize `overrides` no `package.json` para mitigar dependências transitivas com segurança.
4. **Foco no Que Realmente Importa**: Proteja chaves de API, credenciais de CI/CD e tokens de deploy.
"""

# ==============================================================================
# 2. CUSTOM DOMAIN ADSENSE SEO GUIDE
# ==============================================================================
p2_slug = "2026-10-20-custom-domain-adsense-seo-guide"
p2_content = """---
slug: github-pages-custom-domain-adsense-seo-guide
title: "Do GitHub Pages ao Domínio Próprio: Guia Completo para Porkbun, Cloudflare DNS, Aprovação no AdSense e SEO Multi-Mecanismos"
authors: [jbjihwan]
tags: [docusaurus, devops, cloudflare, seo, web-monetization]
keywords: [Docusaurus GitHub Pages Domínio Próprio, Cloudflare DNS Porkbun CNAME Setup, Google AdSense ads.txt Site Estático, Google Search Console Erro de Sitemap, Naver Search Advisor RSS Host]
description: "Guia completo de engenharia: Migração de um blog estático Docusaurus no GitHub Pages para um domínio próprio apex com Porkbun e Cloudflare DNS, verificação do Google AdSense e SEO avançado."
---

Hospedar um blog de engenharia no GitHub Pages sob o endereço `usuario.github.io/projeto` é uma das formas mais práticas de começar. Contudo, quando a sua audiência cresce e você busca monetização profissional, depara-se com um bloqueio rígido: **o Google AdSense proíbe expressamente subdomínios gratuitos como `*.github.io`**. Para obter aprovação e construir autoridade duradoura de marca, um domínio próprio apex é obrigatório.

Migrar um site estático para um domínio customizado envolve muito mais do que cadastrar um registro de DNS: requer delegação de nameservers, terminação de certificados SSL na edge, redirecionamentos canônicos, entrega automática de `ads.txt` e indexação simultânea no Google, Bing e Naver.

Neste guia, documentamos a migração com zero downtime de `jbjihwan.github.io/global_blog` para `https://globaldevlog.com`.

{/* truncate */}

---

![Arquitetura de Roteamento DNS e CDN de Produção](./images/01_dns_routing_architecture.png)

### 1. Visão Geral da Arquitetura em Três Camadas

```mermaid
flowchart LR
    User[Visitantes Globais] --> Edge[Cloudflare Anycast CDN & DNS]
    Edge -->|Terminação Universal SSL| Edge
    Edge -->|CNAME Flattening| Origin[Armazenamento Estático GitHub Pages]
    Origin --> Static[Assets HTML/CSS/JS Pré-compilados]
```

1. **Registrador de Domínio (Porkbun)**: Gerencia o registro do domínio e delega os nameservers integralmente para a Cloudflare.
2. **DNS & Segurança de Borda (Cloudflare Anycast DNS)**:
   - **CNAME Flattening**: Permite mapear o domínio raiz apex (`globaldevlog.com`) diretamente para o GitHub Pages sem necessidade de registros A estáticos.
   - **Universal SSL**: Provê criptografia HTTPS de ponta a ponta na edge e força o redirecionamento de HTTP para HTTPS.
3. **Plataforma de Hospedagem (GitHub Pages)**: Distribui os arquivos estáticos gerados pelo Docusaurus globalmente.

---

### 2. Indexação SEO em Múltiplos Mecanismos de Busca

Ao submeter o domínio em ferramentas de webmaster internacionais e regionais, erros típicos podem ocorrer:

| Mecanismo de Busca | Erro Frequente | Causa Raiz & Solução |
| :--- | :--- | :--- |
| **Google Search Console** | "Não foi possível ler o sitemap" | O Docusaurus gera `/sitemap.xml` por padrão. Ao trocar de domínio, remova a propriedade antiga e valide via registro TXT no DNS. |
| **Naver Search Advisor** | "URL de host incompatível" | O Naver exige correspondência exata entre o RSS e o domínio cadastrado (atenção a barras finais `/`). |
| **Bing Webmaster Tools** | Indexação lenta | Importe as configurações diretamente via OAuth2 do Google Search Console para indexação em minutos. |

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Domínio Próprio É Obrigatório**: O Google AdSense rejeita subdomínios gratuitos; um domínio apex é indispensável para aprovação.
2. **Vantagem de Porkbun + Cloudflare**: CNAME Flattening e SSL Universal garantem migração sem nenhuma queda de serviço.
3. **SEO Multi-Mecanismos**: Cadastre sitemaps e feeds RSS no Google, Bing e Naver simultaneamente.
4. **Redirecionamento Canônico**: Force HTTPS e encaminhe tráfego `www` para o apex de forma consistente.
"""

# ==============================================================================
# 3. GITHUB PAGES CUSTOM DOMAIN CLOUDFLARE DNS
# ==============================================================================
p3_slug = "2026-10-21-github-pages-custom-domain-cloudflare-dns"
p3_content = """---
slug: github-pages-custom-domain-cloudflare-dns
title: "Domínio Customizado no GitHub Pages #1: Migração com Zero Downtime Usando Porkbun e Cloudflare DNS (CNAME Flattening & Universal SSL)"
authors: [jbjihwan]
tags: [github-pages, custom-domain, porkbun, cloudflare, docusaurus, devops]
keywords: [Docusaurus GitHub Pages Domínio Customizado, Cloudflare DNS Porkbun Configuração CNAME, CNAME Flattening Domínio Apex, Cloudflare Full SSL Certificado Edge, Correção Bug Reset CNAME Deploy]
description: "Guia passo a passo: Como migrar de subdomínios gratuitos github.io para um domínio apex próprio usando Porkbun e Cloudflare Anycast DNS sem interrupção de HTTPS."
---

Manter um blog no GitHub Pages sob `usuario.github.io/projeto` é econômico e rápido: basta commitar markdown, dar git push e a página é entregue globalmente.

Porém, ao buscar uma presença profissional e monetização com anúncios, você encontra uma barreira intransponível: **o Google AdSense veta totalmente subdomínios gratuitos como `*.github.io`**. Além disso, toda autoridade de domínio construída fica atrelada ao GitHub em vez da sua marca pessoal.

Neste primeiro episódio da nossa série de infraestrutura, demonstramos a migração exata de `jbjihwan.github.io/global_blog` para `https://globaldevlog.com` através de uma arquitetura resiliente combinando **Porkbun + Cloudflare + GitHub Pages**.

{/* truncate */}

---

### 1. Configuração Prática Passo a Passo

#### Passo 1: Delegação de Nameservers no Porkbun
No painel do Porkbun, substitua os nameservers padrão pelos servidores Anycast fornecidos pela Cloudflare:
- `curt.ns.cloudflare.com`
- `roxy.ns.cloudflare.com`

#### Passo 2: Configuração de Registros de DNS na Cloudflare (CNAME Flattening)
Crie dois registros essenciais:
- **Tipo**: `CNAME` | **Nome**: `@` (Apex) | **Destino**: `jbjihwan.github.io` | **Proxy**: Ativado (Nuvem Laranja)
- **Tipo**: `CNAME` | **Nome**: `www` | **Destino**: `jbjihwan.github.io` | **Proxy**: Ativado

#### Passo 3: Prevenção do Bug de Reset de CNAME no Docusaurus
O GitHub Pages precisa de um arquivo `CNAME` na raiz da branch de deploy. Ao rodar `npm run deploy`, o Docusaurus pode recriar a branch e apagar esse arquivo. Para evitar isso permanentemente, crie o arquivo em `static/CNAME`:
```text
globaldevlog.com
```
Assim, a cada build, o Docusaurus copia automaticamente o domínio para a raiz de publicação.

---

### 2. Criptografia SSL/TLS: O Modo Full (Strict)

No painel SSL/TLS da Cloudflare, selecione o modo **Full** ou **Full (Strict)**. Como o GitHub Pages emite certificados Let's Encrypt automáticos para domínios customizados, a conexão entre os nós de borda da Cloudflare e os servidores de origem do GitHub Pages permanece criptografada de ponta a ponta.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Separação de Responsabilidades**: Porkbun gerencia o registro, Cloudflare cuida do DNS e borda, e GitHub Pages hospeda os arquivos estáticos.
2. **CNAME Flattening**: Roteamento direto do domínio raiz sem amarras a endereços IP estáticos.
3. **Blindagem do CNAME no Docusaurus**: Guarde o arquivo `CNAME` na pasta `static/` para prevenir deleções acidentais em novos deploys.
4. **HTTPS Ininterrupto**: Utilize o modo Cloudflare SSL Full para segurança criptográfica contínua.
"""

# ==============================================================================
# 4. STATIC SITE ADSENSE ADS-TXT GUIDE
# ==============================================================================
p4_slug = "2026-10-21-static-site-adsense-ads-txt-guide"
p4_content = """---
slug: static-site-adsense-ads-txt-guide
title: "[Monetização Web #2] Aprovação do Google AdSense para Sites Estáticos: Resolução da Armadilha 404 do ads.txt & Integração HeadTags"
authors: [jbgih]
tags: [google-adsense, docusaurus, github-pages, web-monetization, devops, cloudflare, seo]
date: 2026-10-21
keywords: [Google AdSense Correção Erro ads.txt, Docusaurus Integração Google AdSense, Aprovação AdSense Site Estático, GitHub Pages ads.txt Deploy, Cloudflare WAF Googlebot Crawler]
description: "Guia completo de engenharia: Como configurar a verificação do Google AdSense no Docusaurus, disponibilizar ads.txt estático na raiz e evitar bloqueios de crawlers pelo Cloudflare WAF."
---

![Aprovação do Google AdSense e Pipeline de Crawlers](./images/01_ads_txt_crawler_flow.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **O Problema**: Diferente de CMS dinâmicos como WordPress, sites estáticos (Docusaurus, Hugo) no GitHub Pages frequentemente disparam o alerta **"Ganhos em risco: arquivo ads.txt ausente"**, porque crawlers encontram erros 404 causados por hidratação tardia ou regras de firewall (WAF).
> - **A Solução**: Inserir o script oficial via `headTags` no `docusaurus.config.ts`, disponibilizar o arquivo `static/ads.txt` na raiz da compilação e criar regras de bypass no Cloudflare WAF para o user-agent `Googlebot-AdsTxt`.
> - **O Resultado**: Rastreabilidade 100% automatizada por crawlers, zero erros 404 e aprovação rápida no AdSense mantendo pontuação de performance no Lighthouse acima de 95.

{/* truncate */}

---

### 1. O Desafio Técnico: Por Que Sites Estáticos Falham na Verificação do ads.txt

O Google AdSense impõe dois pré-requisitos técnicos:
1. **Tag do Publicador no `<head>`**: `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-..." crossorigin="anonymous"></script>`
2. **Arquivo `ads.txt` Validado na Raiz do Domínio**: `https://seudominio.com/ads.txt`

Em Single Page Applications (SPAs) e sites gerados por SSG, falhas ocorrem quando o arquivo não está na raiz estática de build ou quando o sistema de desafio de bots da Cloudflare bloqueia o robô de verificação do Google.

---

### 2. As Três Etapas de Implementação

#### Etapa 1: Injeção Limpa via HeadTags no Docusaurus
Configure o script em `docusaurus.config.ts`:
```ts
headTags: [
  {
    tagName: 'script',
    attributes: {
      async: 'true',
      src: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4654073335496617',
      crossorigin: 'anonymous',
    },
  },
],
```

#### Etapa 2: Posicionamento Correto do `ads.txt`
Crie o arquivo em `static/ads.txt`:
```text
google.com, pub-4654073335496617, DIRECT, f08c47fec0942fa0
```
O Docusaurus copia automaticamente qualquer arquivo em `static/` diretamente para a raiz do diretório compilado (`build/ads.txt`).

#### Etapa 3: Regra de Bypass no Cloudflare WAF para o Googlebot
Crie uma regra de exceção no firewall para evitar desafios interativos (Managed Challenge) aos robôs de indexação:
- **Campo**: `User Agent`
- **Operador**: `contains`
- **Valor**: `Googlebot`
- **Ação**: `Bypass / Skip`

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Prevenção do Alerta de Receita**: A ausência do `ads.txt` na raiz impede a monetização; sua entrega estática via `static/` é essencial.
2. **Injeção Correta de Tags**: Utilize `headTags` no Docusaurus para garantir que o script de verificação esteja presente antes da hidratação do React.
3. **Configuração de Borda sem Bloqueios**: Ajuste o WAF da Cloudflare para permitir que robôs legítimos do Google leiam o arquivo sem encontrar desafios interativos.
4. **Performance Preservada**: A entrega puramente estática preserva notas máximas no Google Lighthouse.
"""

def main():
    print("=" * 65)
    print("Translating Section 2: Security & DevOps (4 posts) into pt-BR...")
    print("=" * 65)
    save_pt_post(p1_slug, p1_content)
    save_pt_post(p2_slug, p2_content)
    save_pt_post(p3_slug, p3_content)
    save_pt_post(p4_slug, p4_content)
    print("\n[SECTION 2 COMPLETE] All 4 Security & DevOps posts staged and saved in pt-BR!")

if __name__ == "__main__":
    main()
