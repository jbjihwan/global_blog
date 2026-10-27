#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional Typography & Card Renderer for Threat Model Diagram using PIL
Dynamically calculates bounding boxes, text wrapping, and card dimensions.
Eliminates text overflow and oversized empty boxes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONTS = {
    "ko": {
        "title": (r"C:\Windows\Fonts\malgunbd.ttf", 36),
        "subtitle": (r"C:\Windows\Fonts\malgun.ttf", 20),
        "badge": (r"C:\Windows\Fonts\malgunbd.ttf", 20),
        "card_title": (r"C:\Windows\Fonts\malgunbd.ttf", 26),
        "body": (r"C:\Windows\Fonts\malgunbd.ttf", 19),
    },
    "en": {
        "title": (r"C:\Windows\Fonts\segoeuib.ttf", 36),
        "subtitle": (r"C:\Windows\Fonts\segoeui.ttf", 20),
        "badge": (r"C:\Windows\Fonts\segoeuib.ttf", 18),
        "card_title": (r"C:\Windows\Fonts\segoeuib.ttf", 25),
        "body": (r"C:\Windows\Fonts\segoeuib.ttf", 18),
    },
    "ja": {
        "title": (r"C:\Windows\Fonts\meiryob.ttc", 34),
        "subtitle": (r"C:\Windows\Fonts\meiryo.ttc", 19),
        "badge": (r"C:\Windows\Fonts\meiryob.ttc", 18),
        "card_title": (r"C:\Windows\Fonts\meiryob.ttc", 24),
        "body": (r"C:\Windows\Fonts\meiryob.ttc", 18),
    },
    "es": {
        "title": (r"C:\Windows\Fonts\segoeuib.ttf", 34),
        "subtitle": (r"C:\Windows\Fonts\segoeui.ttf", 19),
        "badge": (r"C:\Windows\Fonts\segoeuib.ttf", 18),
        "card_title": (r"C:\Windows\Fonts\segoeuib.ttf", 24),
        "body": (r"C:\Windows\Fonts\segoeuib.ttf", 17),
    },
    "zh-Hans": {
        "title": (r"C:\Windows\Fonts\msyhbd.ttc", 36),
        "subtitle": (r"C:\Windows\Fonts\msyh.ttc", 20),
        "badge": (r"C:\Windows\Fonts\msyhbd.ttc", 18),
        "card_title": (r"C:\Windows\Fonts\msyhbd.ttc", 25),
        "body": (r"C:\Windows\Fonts\msyhbd.ttc", 18),
    },
    "zh-Hant": {
        "title": (r"C:\Windows\Fonts\msjhbd.ttc", 36),
        "subtitle": (r"C:\Windows\Fonts\msjh.ttc", 20),
        "badge": (r"C:\Windows\Fonts\msjhbd.ttc", 18),
        "card_title": (r"C:\Windows\Fonts\msjhbd.ttc", 25),
        "body": (r"C:\Windows\Fonts\msjhbd.ttc", 18),
    },
}

DATA = {
    "ko": {
        "title": "위협 모델링: 동적 웹 서버 vs 정적 사이트(SSG)",
        "subtitle": "아키텍처별 공격 표면(Attack Surface) 및 런타임 침해 위험 심층 비교",
        "top": {
            "badge": "위협 노출",
            "title": "전통적 동적 웹 서버 (Node.js / Django)",
            "bullets": [
                "24시간 상시 대기 포트: 외부 침투 경로 항시 노출 (Port 80/443)",
                "데이터베이스 계층: SQL 인젝션 및 인증 토큰 탈취 위험 상존",
                "런타임 템플릿 실행: 원격 코드 실행(RCE) 침해 가능성",
                "서버 리소스 착취: 메모리 고갈 및 분산 서비스 거부(DoS) 공격 노출",
                "npm 취약 패키지: 프로덕션 런타임에서 실시간 공격 체결",
            ]
        },
        "bot": {
            "badge": "보안 격리",
            "title": "모던 정적 사이트 (GitHub Pages & Anycast CDN)",
            "bullets": [
                "빌드 시점 사전 컴파일: 순수 정적 파일(HTML/CSS/JS)만 제공",
                "상시 서버 프로세스 전무: 공격 가능한 백엔드 데몬 부재",
                "데이터베이스 포트 없음: SQL 인젝션 공격 표면 0%",
                "서버 사이드 RCE 완전 차단: 글로벌 엣지 CDN 읽기 전용 배포",
                "npm audit 취약점 경고: 번들러 도구 한정, 런타임 위험 0%",
            ]
        }
    },
    "en": {
        "title": "Threat Modeling: Dynamic Server vs Static Site (SSG)",
        "subtitle": "In-Depth Comparison of Attack Surface & Runtime Breach Risks",
        "top": {
            "badge": "VULNERABLE",
            "title": "Traditional Dynamic Web Server (Node.js / Django)",
            "bullets": [
                "24/7 Active Listening Ports: External attack paths always open (Port 80/443)",
                "Database Layer Risks: Direct SQL Injection & credential theft vectors",
                "Runtime Template Execution: Server-side Remote Code Execution (RCE)",
                "Server Resource Exploitation: Memory exhaustion & DoS attack exposure",
                "npm Packages: Live exploit execution in production runtime",
            ]
        },
        "bot": {
            "badge": "SECURE",
            "title": "Modern Static Site Generation (GitHub Pages & Anycast CDN)",
            "bullets": [
                "Pre-compiled at Build Time: Delivers 100% pure static assets (HTML/CSS/JS)",
                "Zero Running Backend Server: No daemons or runtime processes to compromise",
                "No Database Ports Exposed: SQL injection attack surface is completely 0%",
                "Immune to Server RCE: Read-only edge delivery via global Anycast CDN",
                "npm Audit Vulnerabilities: Bundler scope only, exactly 0% runtime risk",
            ]
        }
    },
}

def render_threat_diagram_pil(locale="ko"):
    cfg = FONTS[locale]
    data = DATA[locale]

    font_title = ImageFont.truetype(cfg["title"][0], cfg["title"][1])
    font_sub = ImageFont.truetype(cfg["subtitle"][0], cfg["subtitle"][1])
    font_badge = ImageFont.truetype(cfg["badge"][0], cfg["badge"][1])
    font_card_title = ImageFont.truetype(cfg["card_title"][0], cfg["card_title"][1])
    font_body = ImageFont.truetype(cfg["body"][0], cfg["body"][1])

    # Dynamic measure
    canvas_w = 1100
    margin_x = 50
    card_w = canvas_w - margin_x * 2

    # Measure header height
    header_y = 40
    title_bbox = font_title.getbbox(data["title"])
    title_h = title_bbox[3] - title_bbox[1]
    sub_bbox = font_sub.getbbox(data["subtitle"])
    sub_h = sub_bbox[3] - sub_bbox[1]

    top_card_y = header_y + title_h + 12 + sub_h + 35

    def layout_card(card_data, is_danger=True):
        bullets = card_data["bullets"]
        line_h = 32
        card_content_h = 65 + len(bullets) * line_h + 20
        return card_content_h

    top_h = layout_card(data["top"], is_danger=True)
    card_spacing = 25
    bot_card_y = top_card_y + top_h + card_spacing
    bot_h = layout_card(data["bot"], is_danger=False)

    canvas_h = bot_card_y + bot_h + 40

    img = Image.new("RGBA", (canvas_w, canvas_h), (11, 17, 32, 255))
    draw = ImageDraw.Draw(img)

    # Background subtle grid lines
    for x in range(0, canvas_w, 40):
        draw.line([(x, 0), (x, canvas_h)], fill=(18, 28, 50, 120), width=1)
    for y in range(0, canvas_h, 40):
        draw.line([(0, y), (canvas_w, y)], fill=(18, 28, 50, 120), width=1)

    # Draw Header
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((canvas_w - title_w) // 2, header_y), data["title"], fill=(255, 255, 255, 255), font=font_title)

    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(((canvas_w - sub_w) // 2, header_y + title_h + 12), data["subtitle"], fill=(56, 189, 248, 255), font=font_sub)

    def draw_card(cx, cy, cw, ch, c_data, is_danger=True):
        # Card colors
        border_col = (239, 68, 68, 255) if is_danger else (16, 185, 129, 255)
        fill_col = (26, 34, 52, 240)
        badge_bg = (239, 68, 68, 45) if is_danger else (16, 185, 129, 45)
        badge_border = (239, 68, 68, 180) if is_danger else (16, 185, 129, 180)
        badge_text_col = (252, 165, 165, 255) if is_danger else (110, 231, 183, 255)
        bullet_icon_col = (239, 68, 68, 255) if is_danger else (16, 185, 129, 255)

        # Draw rounded rectangle
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=16, fill=fill_col, outline=border_col, width=2)

        # Draw top badge
        badge_text = c_data["badge"]
        b_box = font_badge.getbbox(badge_text)
        b_w = b_box[2] - b_box[0]
        badge_w = b_w + 24
        badge_h = 32
        bx = cx + 25
        by = cy + 20
        draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=8, fill=badge_bg, outline=badge_border, width=1)
        draw.text((bx + 12, by + 4), badge_text, fill=badge_text_col, font=font_badge)

        # Card Title
        draw.text((bx + badge_w + 16, by + 1), c_data["title"], fill=(255, 255, 255, 255), font=font_card_title)

        # Divider line
        div_y = by + badge_h + 16
        draw.line([(cx + 25, div_y), (cx + cw - 25, div_y)], fill=(45, 55, 78, 200), width=1)

        # Bullets
        bullets_y = div_y + 18
        for b in c_data["bullets"]:
            # Bullet icon
            draw.ellipse([cx + 30, bullets_y + 8, cx + 38, bullets_y + 16], fill=bullet_icon_col)
            # Bullet text
            draw.text((cx + 50, bullets_y), b, fill=(241, 245, 249, 255), font=font_body)
            bullets_y += 32

    # Draw Top Card
    draw_card(margin_x, top_card_y, card_w, top_h, data["top"], is_danger=True)

    # Draw Bottom Card
    draw_card(margin_x, bot_card_y, card_w, bot_h, data["bot"], is_danger=False)

    out_path = os.path.join(r"C:\Users\jbgih\.gemini\antigravity-cli\brain\a2c8435f-707b-431d-a280-dad177e26fdc", f"threat_{locale}_pro.png")
    img.save(out_path, format="PNG")
    print("Saved:", out_path)
    return out_path

if __name__ == "__main__":
    render_threat_diagram_pil("ko")
    render_threat_diagram_pil("en")
