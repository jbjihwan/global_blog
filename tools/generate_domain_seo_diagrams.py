import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMAGE_DIRS = [
    r"D:\ai\antigravity\global_blog\blog\2026-10-20-custom-domain-adsense-seo-guide\images",
    r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog\2026-10-20-custom-domain-adsense-seo-guide\images",
    r"D:\ai\antigravity\global_blog\i18n\ja\docusaurus-plugin-content-blog\2026-10-20-custom-domain-adsense-seo-guide\images",
    r"D:\ai\antigravity\global_blog\i18n\es\docusaurus-plugin-content-blog\2026-10-20-custom-domain-adsense-seo-guide\images",
]

for d in IMAGE_DIRS:
    os.makedirs(d, exist_ok=True)

def generate_dns_architecture():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=200)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    # Box 1: Registrar
    r1 = patches.FancyBboxPatch((0.5, 1.2), 2.5, 3.2, boxstyle="round,pad=0.2", linewidth=2, edgecolor='#38bdf8', facecolor='#1e293b')
    ax.add_patch(r1)
    ax.text(1.75, 4.0, "1. Registrar\n(Porkbun)", color='#38bdf8', fontsize=11, fontweight='bold', ha='center')
    ax.text(1.75, 2.6, "- Custom Domain\n  globaldevlog.com\n- WHOIS Privacy Free\n- NS Delegation to\n  Cloudflare\n  (roan & sneh)", color='#cbd5e1', fontsize=8.5, ha='center', va='center')

    # Arrow 1 -> 2
    ax.annotate('', xy=(3.4, 2.8), xytext=(2.9, 2.8), arrowprops=dict(arrowstyle="->", color='#94a3b8', lw=2))

    # Box 2: Cloudflare Edge DNS
    r2 = patches.FancyBboxPatch((3.6, 1.2), 3.2, 3.2, boxstyle="round,pad=0.2", linewidth=2, edgecolor='#f59e0b', facecolor='#1e293b')
    ax.add_patch(r2)
    ax.text(5.2, 4.0, "2. Cloudflare Edge DNS\n& Security Layer", color='#f59e0b', fontsize=11, fontweight='bold', ha='center')
    ax.text(5.2, 2.6, "- CNAME Flattening (@)\n  -> jbjihwan.github.io\n- CNAME www\n- Global Anycast CDN\n- Auto Universal SSL\n- DDoS & Bot Shield", color='#cbd5e1', fontsize=8.5, ha='center', va='center')

    # Arrow 2 -> 3
    ax.annotate('', xy=(7.2, 2.8), xytext=(6.7, 2.8), arrowprops=dict(arrowstyle="->", color='#94a3b8', lw=2))

    # Box 3: GitHub Pages Origin
    r3 = patches.FancyBboxPatch((7.4, 1.2), 3.0, 3.2, boxstyle="round,pad=0.2", linewidth=2, edgecolor='#10b981', facecolor='#1e293b')
    ax.add_patch(r3)
    ax.text(8.9, 4.0, "3. GitHub Pages Origin\n(Docusaurus SSG)", color='#10b981', fontsize=11, fontweight='bold', ha='center')
    ax.text(8.9, 2.6, "- static/CNAME file\n- baseUrl: '/'\n- 4 Locales (en/ko/ja/es)\n- Zero Server Cost\n- High Availability CDN", color='#cbd5e1', fontsize=8.5, ha='center', va='center')

    ax.text(5.5, 4.9, "Production DNS & CDN Routing Architecture for Static Engineering Blog", color='#ffffff', fontsize=12.5, fontweight='bold', ha='center')
    ax.set_xlim(0, 11)
    ax.set_ylim(0.8, 5.4)
    ax.axis('off')
    plt.tight_layout()

    out_name = "01_dns_routing_architecture.png"
    for d in IMAGE_DIRS:
        fig.savefig(os.path.join(d, out_name), facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

def generate_indexing_pipeline():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=200)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    # 4 columns for search engines & monetization
    # Col 1: Google
    c1 = patches.FancyBboxPatch((0.4, 1.0), 2.3, 3.5, boxstyle="round,pad=0.15", linewidth=1.8, edgecolor='#4285F4', facecolor='#1e293b')
    ax.add_patch(c1)
    ax.text(1.55, 4.1, "Google Search\nConsole", color='#60a5fa', fontsize=10.5, fontweight='bold', ha='center')
    ax.text(1.55, 2.5, "- DNS TXT Domain Auth\n- 4 Sitemaps Submitted\n  (en, ko, ja, es)\n- Root Error Fix\n  (Detail -> Delete)\n- URL Inspection Req", color='#cbd5e1', fontsize=8, ha='center', va='center')

    # Col 2: Naver
    c2 = patches.FancyBboxPatch((3.0, 1.0), 2.3, 3.5, boxstyle="round,pad=0.15", linewidth=1.8, edgecolor='#03C75A', facecolor='#1e293b')
    ax.add_patch(c2)
    ax.text(4.15, 4.1, "Naver Search\nAdvisor", color='#4ade80', fontsize=10.5, fontweight='bold', ha='center')
    ax.text(4.15, 2.5, "- Dual Auth (HTML+Meta)\n- Host-Level Registration\n- sitemap.xml & RSS\n- Priority Crawl Request\n  (/blog, /ko/blog)\n- Yeti Bot Acceleration", color='#cbd5e1', fontsize=8, ha='center', va='center')

    # Col 3: Bing
    c3 = patches.FancyBboxPatch((5.6, 1.0), 2.3, 3.5, boxstyle="round,pad=0.15", linewidth=1.8, edgecolor='#008373', facecolor='#1e293b')
    ax.add_patch(c3)
    ax.text(6.75, 4.1, "Bing Webmaster\n& AI Index", color='#2dd4bf', fontsize=10.5, fontweight='bold', ha='center')
    ax.text(6.75, 2.5, "- GSC 1-Click Import\n- Instant Domain Sync\n- Manual Sitemap Submit\n  (Skip 48hr Delay)\n- ChatGPT Search &\n  Copilot Ingestion", color='#cbd5e1', fontsize=8, ha='center', va='center')

    # Col 4: AdSense
    c4 = patches.FancyBboxPatch((8.2, 1.0), 2.4, 3.5, boxstyle="round,pad=0.15", linewidth=1.8, edgecolor='#F4B400', facecolor='#1e293b')
    ax.add_patch(c4)
    ax.text(9.4, 4.1, "Google AdSense\nMonetization", color='#fbbf24', fontsize=10.5, fontweight='bold', ha='center')
    ax.text(9.4, 2.5, "- Custom Apex Domain\n  (Required for Auth)\n- Client ID Script Injection\n- static/ads.txt Deployed\n  (Verified HTTP 200)\n- Review Underway", color='#cbd5e1', fontsize=8, ha='center', va='center')

    ax.text(5.5, 4.9, "Global Search Engine Indexing & AdSense Monetization Pipeline", color='#ffffff', fontsize=12.5, fontweight='bold', ha='center')
    ax.set_xlim(0, 11)
    ax.set_ylim(0.7, 5.4)
    ax.axis('off')
    plt.tight_layout()

    out_name = "02_indexing_pipeline.png"
    for d in IMAGE_DIRS:
        fig.savefig(os.path.join(d, out_name), facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

if __name__ == '__main__':
    generate_dns_architecture()
    generate_indexing_pipeline()
    print("Successfully generated all diagrams!")
