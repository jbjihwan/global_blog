# -*- coding: utf-8 -*-
"""
generate_adsense_remediation_cover.py - Generates 1200x630 dark-themed technical cover image
for Standalone Web Engineering & Security Article: Solving AdSense Low Value Content, YMYL Guards, and Cloudflare WAF Blocks.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def generate_cover(output_paths):
    width = 1200
    height = 630
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)

    # Background grid
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(30, 41, 59, 100), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(30, 41, 59, 100), width=1)

    # Accent bar: Amber / Warning Orange
    draw.rectangle([0, 0, width, 6], fill=(245, 158, 11, 255))

    fonts_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
    try:
        title_font = ImageFont.truetype(os.path.join(fonts_dir, "arialbd.ttf"), 34)
        subtitle_font = ImageFont.truetype(os.path.join(fonts_dir, "arial.ttf"), 16)
        card_header_font = ImageFont.truetype(os.path.join(fonts_dir, "arialbd.ttf"), 16)
        card_body_font = ImageFont.truetype(os.path.join(fonts_dir, "arial.ttf"), 13)
        badge_font = ImageFont.truetype(os.path.join(fonts_dir, "arialbd.ttf"), 12)
    except Exception:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        card_header_font = ImageFont.load_default()
        card_body_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()

    # Badge
    draw.rounded_rectangle([60, 40, 510, 68], radius=6, fill=(120, 53, 15, 230), outline=(251, 191, 36, 255), width=1)
    draw.text((75, 47), "SECURITY & INFRA • ADSENSE POLICY & WAF DEFENSE", fill=(254, 243, 199), font=badge_font)

    # Title & Subtitle
    draw.text((60, 82), "Fixing AdSense Low Value Content & WAF Blocks", fill=(248, 250, 252), font=title_font)
    draw.text((60, 134), "Defeating Scaled Content Traps, YMYL Route Script Guards, and Cloudflare WAF Crawler Bypasses", fill=(148, 163, 184), font=subtitle_font)

    # 3 Cards Layout
    col_width = 330
    col_gap = 45
    start_y = 185
    card_h = 390

    # Card 1: Target & Architecture (Sky/Blue)
    c1_x = 60
    draw.rounded_rectangle([c1_x, start_y, c1_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 230), outline=(56, 189, 248, 200), width=2)
    draw.rounded_rectangle([c1_x + 14, start_y + 14, c1_x + col_width - 14, start_y + 44], radius=6, fill=(12, 74, 110, 180))
    draw.text((c1_x + 22, start_y + 20), "1. TARGET & ARCHITECTURE", fill=(224, 242, 254), font=card_header_font)

    c1_text = [
        "• AdSense Rejection Remediated:",
        "  'Needs Attention' & 'Low Value Content'.",
        "• Thin Scaled Content Eliminated:",
        "  Pruning 7 machine-translated locales.",
        "  Consolidating to 2 core languages (EN/KO).",
        "• YMYL Compliance Architecture:",
        "  Zero ads on mental crisis research pages.",
        "• Cloudflare WAF Crawler Pass-through:",
        "  Whitelisting Mediapartners-Google.",
        "• Automated Sitemaps Synchronization:",
        "  Google Search Console Webmasters API."
    ]
    y_offset = start_y + 55
    for line in c1_text:
        is_bullet = line.startswith("•")
        f = card_body_font
        color = (241, 245, 249) if is_bullet else (148, 163, 184)
        draw.text((c1_x + 20, y_offset), line, fill=color, font=f)
        y_offset += 24 if is_bullet else 20

    # Card 2: Real Errors & Pitfalls (Red/Rose)
    c2_x = c1_x + col_width + col_gap
    draw.rounded_rectangle([c2_x, start_y, c2_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 230), outline=(239, 68, 68, 200), width=2)
    draw.rounded_rectangle([c2_x + 14, start_y + 14, c2_x + col_width - 14, start_y + 44], radius=6, fill=(153, 27, 27, 180))
    draw.text((c2_x + 22, start_y + 20), "2. ERRORS & PITFALLS", fill=(254, 226, 226), font=card_header_font)

    c2_text = [
        "• Static Script Leaks into YMYL Pages:",
        "  docusaurus.config scripts array bypasses",
        "  client routes, risking account termination.",
        "• Ghost Locales in Navbar & Sitemaps:",
        "  noindex still left 7 locales in navbar.",
        "  Obsolete sitemaps caused GSC 404 flags.",
        "• Cloudflare WAF Parameter Conflict:",
        "  Code 10041: 'phases' and 'phase' clash.",
        "• Bot Fight Mode 403 Challenges:",
        "  Googlebot blocked by Cloudflare CAPTCHAs."
    ]
    y_offset = start_y + 55
    for line in c2_text:
        is_bullet = line.startswith("•")
        f = card_body_font
        color = (254, 202, 202) if is_bullet else (203, 213, 225)
        draw.text((c2_x + 20, y_offset), line, fill=color, font=f)
        y_offset += 24 if is_bullet else 20

    # Card 3: Deep Root Cause & Fix (Emerald/Green)
    c3_x = c2_x + col_width + col_gap
    draw.rounded_rectangle([c3_x, start_y, c3_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 230), outline=(16, 185, 129, 200), width=2)
    draw.rounded_rectangle([c3_x + 14, start_y + 14, c3_x + col_width - 14, start_y + 44], radius=6, fill=(6, 78, 59, 180))
    draw.text((c3_x + 22, start_y + 20), "3. ROOT CAUSE & BENCHMARK", fill=(209, 250, 229), font=card_header_font)

    c3_text = [
        "• Dynamic Root.tsx Route Isolation:",
        "  pauseAdRequests=1 on /mental-crisis*.",
        "  Zero ad DOM containers or layout shifts.",
        "• Strict Locales & gh-pages Pruning:",
        "  git rm -rf old locales, clean 404 live.",
        "• Cloudflare WAF Skip Rule Resolved:",
        "  Unchecked local phase, verified bot bypass.",
        "• Official GSC API Automated Purge:",
        "  7 obsolete sitemaps deleted (204 OK).",
        "• 100% Policy Clean for AdSense Review."
    ]
    y_offset = start_y + 55
    for line in c3_text:
        is_bullet = line.startswith("•")
        f = card_body_font
        color = (167, 243, 208) if is_bullet else (203, 213, 225)
        draw.text((c3_x + 20, y_offset), line, fill=color, font=f)
        y_offset += 24 if is_bullet else 20

    # Save to all target paths
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img.save(p, format="PNG")
        print(f"[+] Successfully generated cover image: {p}")

if __name__ == "__main__":
    slug = "google-adsense-low-value-content-cloudflare-fix"
    staging_base = f"global_blog/배포대기/2026-12-01-{slug}"
    targets = [
        os.path.join(staging_base, "blog", "images", "01_cover.png"),
        os.path.join(staging_base, "i18n", "ko", "images", "01_cover.png"),
        os.path.join("global_blog", "blog", f"2026-12-01-{slug}", "images", "01_cover.png"),
        os.path.join("global_blog", "i18n", "ko", "docusaurus-plugin-content-blog", f"2026-12-01-{slug}", "images", "01_cover.png")
    ]
    generate_cover(targets)
