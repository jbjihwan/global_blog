#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.family'] = "Malgun Gothic"

fig, ax = plt.subplots(figsize=(9.2, 9.8), dpi=100)
fig.patch.set_facecolor('#0b1120')
ax.set_facecolor('#0b1120')

# Header
ax.text(4.6, 9.35, "글로벌 정적 엔지니어링 블로그 DNS & CDN 라우팅 아키텍처", 
        color='#ffffff', fontsize=20.5, fontweight='bold', ha='center')

steps = [
    ("1. 도메인 등록기관 (Porkbun)", 
     "• 커스텀 도메인: globaldevlog.com 등록 및 무료 WHOIS 개인정보 보호\n• 공인 네임서버(NS) 위임: Cloudflare Anycast 네임서버 지정", 
     "#38bdf8", 6.8),
    ("2. Cloudflare Edge DNS & Anycast 보안 보호막", 
     "• CNAME 플래트닝: 루트(@) 도메인을 GitHub Pages 오리진으로 직통 연동\n• CNAME www 리다이렉트 포워딩 & 전 세계 초고속 CDN 캐싱\n• 자동 유니버설 SSL 인증서(HTTPS) & DDoS 및 악성 크롤러 차단", 
     "#f59e0b", 3.8),
    ("3. GitHub Pages 오리진 (Docusaurus SSG)", 
     "• static/CNAME 바인딩: 사전 컴파일된 다국어(6개 국어) 정적 파일 제공\n• 서버 호스팅 및 인프라 유지비용 $0 & 99.99% 고가용성 글로벌 서빙", 
     "#10b981", 0.8),
]

for title, desc, col, y in steps:
    h = 2.4 if y == 3.8 else 2.1
    card = patches.FancyBboxPatch((0.4, y), 8.4, h, boxstyle="round,pad=0.2",
                                 linewidth=2.5, edgecolor=col, facecolor='#1e293b')
    ax.add_patch(card)
    
    # Title
    ax.text(0.7, y + h - 0.5, title, color=col, fontsize=17.0, fontweight='bold', ha='left', va='center')
    ax.plot([0.7, 8.4], [y + h - 0.8, y + h - 0.8], color=col, linewidth=1.5)
    
    # Description
    ax.text(0.7, y + (h - 0.8)/2, desc, color='#f8fafc', fontsize=14.0, fontweight='bold', ha='left', va='center', linespacing=1.65)

    # Downward arrow
    if y > 1.0:
        arrow = patches.FancyArrowPatch((4.6, y - 0.1), (4.6, y - 0.45),
                                       arrowstyle='->', mutation_scale=20, color='#94a3b8', linewidth=2.5)
        ax.add_patch(arrow)

ax.set_xlim(0, 9.2)
ax.set_ylim(0.4, 9.8)
ax.axis('off')
plt.tight_layout()

out_path = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\test_vertical_dns.png"
fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved:", out_path)
