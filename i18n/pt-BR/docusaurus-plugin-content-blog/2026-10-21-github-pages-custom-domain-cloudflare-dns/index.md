---
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
