---
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
