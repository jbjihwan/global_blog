#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate custom branded assets (favicon.ico, social-card.png) for Global Dev Blog.
"""

import os
from PIL import Image, ImageDraw, ImageFont

STATIC_IMG = r"D:\ai\antigravity\global_blog\static\img"

def create_favicon():
    size = (64, 64)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded background
    draw.rounded_rectangle([4, 4, 60, 60], radius=14, fill=(15, 23, 42, 255), outline=(79, 70, 229, 255), width=2)
    # Draw globe circle
    draw.ellipse([14, 14, 50, 50], outline=(56, 189, 248, 180), width=2)
    # Draw code brackets < / >
    draw.line([(25, 27), (19, 32), (25, 37)], fill=(56, 189, 248, 255), width=2)
    draw.line([(34, 25), (30, 39)], fill=(16, 185, 129, 255), width=2)
    draw.line([(39, 27), (45, 32), (39, 37)], fill=(56, 189, 248, 255), width=2)

    ico_path = os.path.join(STATIC_IMG, "favicon.ico")
    img.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print(f"Created favicon at: {ico_path}")

def create_social_card():
    width, height = 1200, 630
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)

    # Subtle background gradient grid lines
    for x in range(0, width, 60):
        draw.line([(x, 0), (x, height)], fill=(30, 41, 59, 100), width=1)
    for y in range(0, height, 60):
        draw.line([(0, y), (width, y)], fill=(30, 41, 59, 100), width=1)

    # Top highlight accent bar
    draw.rectangle([0, 0, width, 6], fill=(79, 70, 229, 255))
    # Glowing gradient circle behind logo
    draw.ellipse([100, 140, 260, 300], fill=(79, 70, 229, 60), outline=(56, 189, 248, 120), width=3)
    # Draw large code bracket symbol inside globe
    draw.line([(155, 190), (135, 220), (155, 250)], fill=(56, 189, 248, 255), width=6)
    draw.line([(188, 180), (172, 260)], fill=(16, 185, 129, 255), width=6)
    draw.line([(205, 190), (225, 220), (205, 250)], fill=(56, 189, 248, 255), width=6)

    # Text details
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 68)
        font_med = ImageFont.truetype("arial.ttf", 32)
        font_tag = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        font_large = ImageFont.load_default()
        font_med = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    # Brand Title
    draw.text((310, 160), "Global Dev Blog", fill=(248, 250, 252, 255), font=font_large)

    # Subtitle
    subtitle = "Production-grade AI Engineering, Autonomous Systems & Computer Vision"
    draw.text((315, 248), subtitle, fill=(148, 163, 184, 255), font=font_med)

    # Badges row
    badges = [
        ("🤖 Autonomous Robotics (Webots RL)", (30, 58, 138), (96, 165, 250)),
        ("👁️ Vision ANPR & OCR", (19, 78, 74), (45, 212, 191)),
        ("🧠 LLM Guardrail & Safety", (67, 56, 202), (165, 180, 252)),
        ("🛡️ Static Site Security", (6, 78, 59), (52, 211, 153)),
    ]

    x_offset = 110
    y_badge = 360
    for text, bg_col, border_col in badges:
        # approximate badge width
        badge_w = len(text) * 11 + 30
        draw.rounded_rectangle([x_offset, y_badge, x_offset + badge_w, y_badge + 46], radius=10, fill=bg_col, outline=border_col, width=2)
        draw.text((x_offset + 14, y_badge + 11), text, fill=(241, 245, 249, 255), font=font_tag)
        x_offset += badge_w + 18
        if x_offset > 800:
            x_offset = 110
            y_badge += 60

    # Footer note
    draw.text((110, 545), "https://globaldevlog.com/  •  4-Locale Multilingual Technical Series", fill=(100, 116, 139, 255), font=font_tag)

    card_path = os.path.join(STATIC_IMG, "social-card.png")
    img.save(card_path, format="PNG")
    print(f"Created social card at: {card_path}")

if __name__ == "__main__":
    create_favicon()
    create_social_card()
