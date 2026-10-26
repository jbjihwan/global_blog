#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.family'] = "Malgun Gothic"

fig, ax = plt.subplots(figsize=(9.2, 9.4), dpi=100)
fig.patch.set_facecolor('#0b1120')
ax.set_facecolor('#0b1120')

# Header
ax.text(4.6, 8.95, "정적 블로그 4단계 심층 보안 강화 파이프라인", 
        color='#ffffff', fontsize=21.5, fontweight='bold', ha='center')

steps = [
    ("1. 시크릿 유출 스캔 (Git Secret Scanning)", "• API 키, PAT 토큰, 인증서 정규식 패턴 사전 검출 및 커밋 원천 차단", "#38bdf8", 7.1),
    ("2. 개인정보(PII) 격리 (Privacy Filter)", "• 전화번호, 주민등록번호, 팀원 실명 등 개인 식별 정보 자동 마스킹", "#818cf8", 5.2),
    ("3. 공급망(npm) 검토 (Supply Chain Audit)", "• npm audit fix 맹신 배제 및 빌드 무결성 보존, 런타임 영향도 기반 분류", "#fbbf24", 3.3),
    ("4. 클라이언트 프라이버시 (Client Privacy)", "• 엄격한 Referrer Policy 적용, Giscus 댓글 iframe 샌드박스화 및 .gitignore 강화", "#34d399", 1.4),
]

for title, desc, col, y in steps:
    card = patches.FancyBboxPatch((0.4, y), 8.4, 1.5, boxstyle="round,pad=0.2",
                                 linewidth=2.5, edgecolor=col, facecolor='#1e293b')
    ax.add_patch(card)
    
    # Title
    ax.text(0.7, y + 1.05, title, color=col, fontsize=16.5, fontweight='bold', ha='left', va='center')
    
    # Description
    ax.text(0.7, y + 0.45, desc, color='#f8fafc', fontsize=14.0, fontweight='bold', ha='left', va='center')

    # Downward arrow
    if y > 1.5:
        arrow = patches.FancyArrowPatch((4.6, y - 0.05), (4.6, y - 0.35),
                                       arrowstyle='->', mutation_scale=20, color='#94a3b8', linewidth=2.5)
        ax.add_patch(arrow)

ax.set_xlim(0, 9.2)
ax.set_ylim(0.9, 9.4)
ax.axis('off')
plt.tight_layout()

out_path = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\test_vertical_pipeline.png"
fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved:", out_path)
