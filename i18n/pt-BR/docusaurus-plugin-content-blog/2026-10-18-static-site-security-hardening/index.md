---
slug: static-site-security-npm-audit-truth
title: "Corrigir Vulnerabilidades npm sem Quebrar Builds de Produção"
authors: [jbgih]
tags: [web-security, npm-audit, docusaurus, devops, supply-chain]
keywords: ["npm audit fix", "npm audit fix --force", "vulnerabilidades npm", "segurança site estático"]
description: "Como resolver vulnerabilidades do npm audit sem quebrar builds. Por que npm audit fix --force falha em sites estáticos e como tratar alertas GHSA com segurança."
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