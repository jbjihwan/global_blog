# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

def create_cover():
    width = 1200
    height = 630
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255)) # Dark slate navy
    draw = ImageDraw.Draw(img)

    # Background grid lines
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(30, 41, 59, 100), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(30, 41, 59, 100), width=1)

    # Accent glow top bar (Emerald green for audit report)
    draw.rectangle([0, 0, width, 6], fill=(16, 185, 129, 255))

    # Try loading clean fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 38)
        subtitle_font = ImageFont.truetype("arial.ttf", 19)
        card_header_font = ImageFont.truetype("arialbd.ttf", 17)
        card_body_font = ImageFont.truetype("arial.ttf", 14)
        badge_font = ImageFont.truetype("arialbd.ttf", 13)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        card_header_font = ImageFont.load_default()
        card_body_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()

    # Title & Badge
    draw.rounded_rectangle([60, 42, 270, 72], radius=6, fill=(6, 78, 59, 220), outline=(52, 211, 153, 255), width=1)
    draw.text((75, 49), "PRODUCTION AI AGENT #2", fill=(167, 243, 208), font=badge_font)

    draw.text((60, 85), "National Budget AI Audit Findings & Evaluation", fill=(248, 250, 252), font=title_font)
    draw.text((60, 137), "Autonomous Detection of Cartels, Split Contracts & 10x Unit Price Markup (Anonymized)", fill=(148, 163, 184), font=subtitle_font)

    # 3 Architecture Columns
    col_width = 330
    col_gap = 40
    start_y = 195
    card_h = 370

    # Column 1: Detected Cases
    c1_x = 60
    draw.rounded_rectangle([c1_x, start_y, c1_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 220), outline=(239, 68, 68, 200), width=2)
    draw.rounded_rectangle([c1_x + 16, start_y + 16, c1_x + col_width - 16, start_y + 50], radius=6, fill=(127, 29, 29, 150))
    draw.text((c1_x + 24, start_y + 24), "[1] Detected Fraud Cases (Anonymized)", fill=(254, 202, 202), font=card_header_font)

    items_c1 = [
        ("Split Private Contracts", "3 contracts under 20M limit (Art. 68 breach)"),
        ("Shared Address Cartel", "3 shell vendors sharing exact same room"),
        ("10x Unit Price Markup", "Server rack 10.0x / Advisory 7.0x median"),
        ("Overhead Leakage (DEI 30%)", "70% absorbed in administrative expenses")
    ]
    cur_y = start_y + 68
    for title, desc in items_c1:
        draw.rounded_rectangle([c1_x + 16, cur_y, c1_x + col_width - 16, cur_y + 60], radius=8, fill=(15, 23, 42, 180), outline=(51, 65, 85, 255), width=1)
        draw.text((c1_x + 26, cur_y + 10), title, fill=(248, 113, 113), font=card_body_font)
        draw.text((c1_x + 26, cur_y + 34), desc, fill=(148, 163, 184), font=badge_font)
        cur_y += 70

    # Column 2: System Performance
    c2_x = c1_x + col_width + col_gap
    draw.rounded_rectangle([c2_x, start_y, c2_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 220), outline=(56, 189, 248, 200), width=2)
    draw.rounded_rectangle([c2_x + 16, start_y + 16, c2_x + col_width - 16, start_y + 50], radius=6, fill=(14, 116, 144, 150))
    draw.text((c2_x + 24, start_y + 24), "[2] AI Engine Performance Metrics", fill=(224, 242, 254), font=card_header_font)

    items_c2 = [
        ("Deterministic Precision", "100% test pass rate (11/11 test suites)"),
        ("High-Speed Inference", "0.03s dossier generation per finding"),
        ("Zero Financial Hallucination", "Strict SQL AST validation & schema locking"),
        ("Precedent Legal Binding", "94.5% similarity to Board of Audit rulings")
    ]
    cur_y = start_y + 68
    for title, desc in items_c2:
        draw.rounded_rectangle([c2_x + 16, cur_y, c2_x + col_width - 16, cur_y + 60], radius=8, fill=(15, 23, 42, 180), outline=(51, 65, 85, 255), width=1)
        draw.text((c2_x + 26, cur_y + 10), title, fill=(56, 189, 248), font=card_body_font)
        draw.text((c2_x + 26, cur_y + 34), desc, fill=(148, 163, 184), font=badge_font)
        cur_y += 70

    # Column 3: Evaluation & Limits
    c3_x = c2_x + col_width + col_gap
    draw.rounded_rectangle([c3_x, start_y, c3_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 220), outline=(168, 85, 247, 200), width=2)
    draw.rounded_rectangle([c3_x + 16, start_y + 16, c3_x + col_width - 16, start_y + 50], radius=6, fill=(88, 28, 135, 150))
    draw.text((c3_x + 24, start_y + 24), "[3] Field Evaluation & Limitations", fill=(243, 232, 255), font=card_header_font)

    items_c3 = [
        ("Evidence Preservation", "Automated cryptographically hashed audit trails"),
        ("Immediate Legal Utility", "Direct article mapping for inspection teams"),
        ("Limit: De Facto Owners", "Borrowed names require corporate tax cross-check"),
        ("Limit: Multi-Tier Subcontracts", "Downstream cash tracing beyond tier-1")
    ]
    cur_y = start_y + 68
    for title, desc in items_c3:
        draw.rounded_rectangle([c3_x + 16, cur_y, c3_x + col_width - 16, cur_y + 60], radius=8, fill=(15, 23, 42, 180), outline=(51, 65, 85, 255), width=1)
        draw.text((c3_x + 26, cur_y + 10), title, fill=(192, 132, 252), font=card_body_font)
        draw.text((c3_x + 26, cur_y + 34), desc, fill=(148, 163, 184), font=badge_font)
        cur_y += 70

    # Footer
    draw.text((60, 592), "Global Dev Blog • Spec-Driven Agent Engineering Case Study", fill=(100, 116, 139), font=badge_font)
    draw.text((width - 250, 592), "https://globaldevlog.com", fill=(100, 116, 139), font=badge_font)

    base_stage = r"D:\ai\antigravity\global_blog\배포대기\2026-11-19-national-budget-ai-audit-findings-performance-evaluation"
    primary_dir = os.path.join(base_stage, "blog", "images")
    os.makedirs(primary_dir, exist_ok=True)
    out_path = os.path.join(primary_dir, "01_national_budget_audit_findings.png")
    img.save(out_path, format="PNG")
    print(f"Primary cover image saved to: {out_path}")

    # Replicate to all 8 locale folders
    locales = ["ko", "ja", "zh-Hans", "zh-Hant", "es", "de", "fr", "pt-BR"]
    for loc in locales:
        loc_dir = os.path.join(base_stage, "i18n", loc, "images")
        os.makedirs(loc_dir, exist_ok=True)
        dest_path = os.path.join(loc_dir, "01_national_budget_audit_findings.png")
        shutil.copyfile(out_path, dest_path)
        print(f"Copied to: {dest_path}")

if __name__ == "__main__":
    create_cover()
