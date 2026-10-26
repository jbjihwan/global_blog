#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.family'] = "Malgun Gothic"

# Canvas: 9.2 x 10.2 inches at 100 dpi = 920 x 1020 px
fig, ax = plt.subplots(figsize=(9.2, 10.2), dpi=100)
fig.patch.set_facecolor('#0b1120')
ax.set_facecolor('#0b1120')

# Main Header
ax.text(4.6, 9.75, "위협 모델링: 동적 웹 서버 vs 정적 사이트(SSG)", 
        color='#ffffff', fontsize=22, fontweight='bold', ha='center')
ax.text(4.6, 9.35, "공격 표면(Attack Surface) 및 런타임 침해 위협 심층 비교", 
        color='#38bdf8', fontsize=15, fontweight='bold', ha='center')

# Top Box: Dynamic Server (Red)
box_top = patches.FancyBboxPatch((0.4, 5.0), 8.4, 4.05, boxstyle="round,pad=0.25",
                                linewidth=2.8, edgecolor='#ef4444', facecolor='#1e293b')
ax.add_patch(box_top)

ax.text(4.6, 8.65, "[위협 노출] 전통적 동적 웹 서버 (Node.js / Django)", 
        color='#fca5a5', fontsize=18.5, fontweight='bold', ha='center')
ax.plot([0.8, 8.4], [8.4, 8.4], color='#ef4444', linewidth=1.8)

top_desc = (
    "• 24시간 상시 대기 포트: 외부 침투 경로 항시 노출 (Port 80/443)\n"
    "• 데이터베이스 계층: SQL 인젝션 및 인증 토큰 탈취 위험 상존\n"
    "• 런타임 템플릿 실행: 원격 코드 실행(RCE) 침해 가능성\n"
    "• 서버 리소스 착취: 메모리 고갈 및 분산 서비스 거부(DoS) 공격 노출\n"
    "• npm 취약 패키지: 프로덕션 런타임에서 실시간 공격 체결"
)
ax.text(0.75, 8.0, top_desc, color='#f8fafc', fontsize=15.5,
        fontweight='bold', ha='left', va='top', linespacing=1.75)

# Bottom Box: Static Site (Green)
box_bot = patches.FancyBboxPatch((0.4, 0.6), 8.4, 4.05, boxstyle="round,pad=0.25",
                                linewidth=2.8, edgecolor='#10b981', facecolor='#1e293b')
ax.add_patch(box_bot)

ax.text(4.6, 4.25, "[보안 격리] 모던 정적 사이트 (GitHub Pages CDN)", 
        color='#6ee7b7', fontsize=18.5, fontweight='bold', ha='center')
ax.plot([0.8, 8.4], [4.0, 4.0], color='#10b981', linewidth=1.8)

bot_desc = (
    "• 빌드 시점 사전 컴파일: 순수 정적 파일(HTML/CSS/JS)만 제공\n"
    "• 상시 서버 프로세스 전무: 공격 가능한 백엔드 데몬 부재\n"
    "• 데이터베이스 포트 없음: SQL 인젝션 공격 표면 0%\n"
    "• 서버 사이드 RCE 완전 차단: 글로벌 엣지 CDN 읽기 전용 배포\n"
    "• npm audit 취약점 경고: 번들러 도구 한정, 런타임 위험 0%"
)
ax.text(0.75, 3.6, bot_desc, color='#f8fafc', fontsize=15.5,
        fontweight='bold', ha='left', va='top', linespacing=1.75)

ax.set_xlim(0, 9.2)
ax.set_ylim(0.2, 10.2)
ax.axis('off')
plt.tight_layout()

out_path = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc\test_vertical_threat.png"
fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
plt.close()
print("Saved to artifact:", out_path)
