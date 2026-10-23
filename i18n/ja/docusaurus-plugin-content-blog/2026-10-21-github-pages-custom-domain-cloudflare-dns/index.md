---
slug: github-pages-custom-domain-cloudflare-dns
title: "[GitHub Pages 独自ドメイン #1] 無料の github.io を卒業し Porkbun + Cloudflare で独自ドメインを接続する: CNAMEフラット化と無料SSL"
authors: [jbjihwan]
tags: [github-pages, custom-domain, porkbun, cloudflare, docusaurus, devops]
keywords: [Docusaurus GitHub Pages Custom Domain, Cloudflare DNS Porkbun CNAME setup, CNAME Flattening apex domain GitHub Pages, Cloudflare Full SSL Edge Certificate, static CNAME deployment reset bug fix]
description: "無料のgithub.ioサブドメインから脱却し、Porkbunで取得した独自ドメインをCloudflare Anycast DNSとCNAMEフラット化を用いてGitHub Pagesに接続、DocusaurusのCNAMEリセット問題を解決する実践ガイド。"

---

GitHub Pagesの無料サブドメイン（`username.github.io/project`）上で技術ブログを運営することは、サーバー維持費ゼロかつGitプッシュだけで静的サイトが自動配信されるため、エンジニアにとって非常に魅力的な選択肢です。

しかし、プロフェッショナルなブランディングと**Google AdSenseによる収益化**を目指す段階で、決定的な技術的壁に直面します。**Google AdSenseの規約上、`*.github.io` などの無料2次サブドメインはサイト審査の申請自体が遮断されている**ためです。さらに、検索エンジンで積み上げたドメイン評価（Domain Authority）を自身の資産にするためには、独自の**ネイキッド／独自ドメイン（Apex Domain、例: `globaldevlog.com`）**が不可欠です。

本連載の第1回となる本記事では、既存の `jbjihwan.github.io/global_blog` から独自ドメイン `https://globaldevlog.com` へのゼロダウンタイム移行を実現した、**Porkbun + Cloudflare + GitHub Pages 3層アーキテクチャとDNS構築手順**を詳細に解説します。

{/* truncate */}

---

![静的エンジニアリングブログ向け本番DNSおよびCDNルーティングアーキテクチャ](./images/01_dns_routing_architecture.png)

---

## 1. アーキテクチャ設計思想: 3層構成の導入

独自ドメインをGitHub Pagesに接続する際、初心者が陥りがちなのが、レジストラからGitHubの4つの固定IP（`185.199.108.153` 等）へ直接 `Aレコード` を設定する手法です。

この旧来の手法には運用上の重大なデメリットがあります:
- エッジでのDDoS攻撃対策および不正ボット遮断機能の欠如。
- ネームサーバー切り替え時におけるグローバル伝播の遅延。
- 静的アセット（CSS/JS/画像）に対するグローバルCDNキャッシュの最適化ができない。

そこで、3つの専門レイヤーへ責任を明確に分離しました:

| レイヤー | 採用サービス | 主な選定理由と役割 |
| :--- | :--- | :--- |
| **1. レジストラ** | **Porkbun** | 初年度および毎年の更新料が業界最安クラス、無料のWHOISプライバシー保護、透明な価格体系 |
| **2. エッジDNS & セキュリティ** | **Cloudflare** | グローバル低遅延Anycast DNS、**ルートドメインのCNAMEフラット化（Flattening）**、無料Universal SSL、自動HTTPS強制 |
| **3. 静的オリジン** | **GitHub Pages** | Docusaurusでコンパイルされた成果物を配信、`gh-pages` ブランチによる自動同期、サーバー運用費完全0円 |

---

## 2. Step 1: Porkbunでのドメイン取得とCloudflareへのネームサーバー委任

1. **ドメイン取得**: Porkbunで希望のネイキッドドメイン（`globaldevlog.com`）を購入します。
2. **Cloudflareへドメイン追加**: Cloudflare管理画面で **[サイトを追加]** をクリックし、購入したドメインを入力して **Freeプラン** を選択します。
3. **割り当てられたネームサーバーの確認**: Cloudflare固有のネームサーバー（2件）を確認します:
   ```text
   roan.ns.cloudflare.com
   sneh.ns.cloudflare.com
   ```
4. **Porkbunのネームサーバー書き換え**: Porkbunの管理コンソール内 `Authoritative Nameservers` 画面で、デフォルト値を削除してCloudflareの2件を登録・保存します。（約5〜15分で全世界に反映されます）

---

## 3. Step 2: Cloudflare CNAME Flattening（フラット化）とFull SSL設定

DNSの標準規格（RFC 1034）では、ゾーンの頂点であるルートドメイン（`@`）にCNAMEレコードを設定することは禁止されています。

しかし、Cloudflareの **CNAME Flattening（フラット化）** 機能を使用すれば、ルートドメインであってもCNAMEレコードの恩恵をそのまま受けることができます。DNSクエリ受信時に、Cloudflareエッジがターゲット（`username.github.io`）のIPを自動解決して返却するためです。

### A. Cloudflare DNS レコードの登録
Cloudflareの **[DNS] > [レコード]** にて、以下の2つのプロキシレコードを追加します:

| 種類 (Type) | 名前 (Name) | ターゲット (Target) | プロキシ状態 (Proxy status) | TTL |
| :--- | :--- | :--- | :--- | :--- |
| **CNAME** | `@` | `jbjihwan.github.io` | **プロキシ済み（オレンジの雲を有効化）** | 自動 |
| **CNAME** | `www` | `jbjihwan.github.io` | **プロキシ済み（オレンジの雲を有効化）** | 自動 |

> **オレンジの雲（プロキシ）は必須**: プロキシを有効にすることで、すべてのトラフィックがCloudflareのAnycastエッジを通過し、自動SSL暗号化やキャッシュの恩恵を享受できます。

### B. SSL/TLS 暗号化モードの切り替え
Cloudflare左側メニューの **[SSL/TLS] > [概要]** へ移動します:
- 暗号化モードを **Full**（または **Full Strict**）に設定します。
- ブラウザ〜Cloudflare間、およびCloudflare〜GitHub Pages間の全経路でセキュアなエンドツーエンドHTTPS通信が保証されます。

---

## 4. Step 3: Docusaurus 設定ファイルの更新 (`docusaurus.config.ts`)

従来のサブディレクトリパス（`/global_blog/`）からドメインのルート（`/`）へパスをマッピングし直すため、`docusaurus.config.ts` を変更します:

```typescript
const config: Config = {
  title: 'Global Dev Blog',
  tagline: 'Engineering Deep Dives in AI, Robotics, Computer Vision',

  // 独自ドメインのルートURLを指定
  url: 'https://globaldevlog.com',
  // サブパスからルート '/' へ変更
  baseUrl: '/',

  organizationName: 'jbjihwan',
  projectName: 'global_blog',
  trailingSlash: false,
  // ...
};
```

---

## 5. Step 4: GitHub Pages デプロイ時のドメイン初期化バグの回避 (`static/CNAME`)

GitHub Pagesで独自ドメインを運用する際に最も多くの開発者が遭遇するトラブルが、**デプロイ実行時のドメイン設定消失問題**です:
1. GitHubのリポジトリ設定（`Settings > Pages > Custom domain`）に `globaldevlog.com` を保存する。
2. ローカルで記事を作成し、`npm run deploy` を実行する。
3. デプロイ完了後、GitHub上のCustom domain設定がクリアされ、サイトが404エラーまたはSSL警告画面になってしまう。

### 原因
Docusaurusのデプロイスクリプトは、ビルド成果物フォルダを強制プッシュ（`git push --force`）して `gh-pages` ブランチを再生成します。その際、ルートに `CNAME` ファイルが存在しないと、GitHubは独自ドメインの割り当てが解除されたと判定します。

### 確実な解決策
プロジェクトの `static/` フォルダ配下に、拡張子のない `CNAME` ファイルを作成します:

```text
globaldevlog.com
```

Docusaurusはビルド時に `static/` 配下のすべてのファイルを成果物ルートに自動複製するため、デプロイのたびに `CNAME` ファイルが `gh-pages` の最上位へ恒久的に配置され、設定が解除される心配がなくなります。

---

## 6. 本番環境での疎通検証

デプロイを実行します:
```bash
npm run deploy
```

デプロイ完了後、レスポンスヘッダーとSSL証明書の状態を確認します:

```bash
curl -I https://globaldevlog.com
# HTTP/2 200
# server: cloudflare
# strict-transport-security: max-age=31536000

curl -I https://www.globaldevlog.com
# HTTP/2 200 (またはルートへの 301 リダイレクト)
```

---

## 🔜 次回予告

独自ドメインの開通が完了したら、次は収益化の申請と検索エンジンのインデックス登録を加速させます:
- **第2回**: *[静的サイト収益化 #2] DocusaurusにおけるGoogle AdSense審査申請: ads.txt 404エラーの完全防止と非同期スクリプト組み込み*
- **第3回**: *[主要3大検索エンジンSEO #3] Google・Naver・Bingウェブマスター登録の実践: サイトマップ削除トラップとホストエラーの解決*

---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **サーバー費用ゼロのエンタープライズ構成**: 卸値ドメインレジストラ(Porkbun)、Anycast CDN・DNS(Cloudflare)、無料静的ホスティング(GitHub Pages)を組み合わせ、運用費ゼロで世界最高峰のエッジ配信網を実現します。
2. **CNAME Flattening によるルート制限の克服**: DNS標準(RFC 1034)で禁止されているルートドメイン(`@`)へのCNAME割り当てをCloudflare平坦化技術で解決し、直接GitHub Pagesへ紐付けます。
3. **Full Strict による完全な通信暗号化**: CloudflareのSSLモードを「Full (Strict)」に設定することで、訪問者〜CDN間だけでなくCDN〜GitHub Pagesオリジン間も強固なHTTPS暗号化を確立します。
4. **static/CNAME によるデプロイ永続化**: Docusaurusの `static/CNAME` 配置と設定ファイル更新により、デプロイ時にカスタムドメイン設定が初期化・消失するトラブルを恒久的に防ぎます。
