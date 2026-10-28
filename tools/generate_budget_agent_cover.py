# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

def create_cover():
    width = 1200
    height = 630
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255)) # Dark slate navy
    draw = ImageDraw.Draw(img)

    # Background gradient / grid lines
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(30, 41, 59, 100), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(30, 41, 59, 100), width=1)

    # Accent glow top bar
    draw.rectangle([0, 0, width, 6], fill=(56, 189, 248, 255))

    # Try loading clean fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        subtitle_font = ImageFont.truetype("arial.ttf", 20)
        card_header_font = ImageFont.truetype("arialbd.ttf", 18)
        card_body_font = ImageFont.truetype("arial.ttf", 14)
        badge_font = ImageFont.truetype("arialbd.ttf", 13)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        card_header_font = ImageFont.load_default()
        card_body_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()

    # Title & Badge
    draw.rounded_rectangle([60, 45, 260, 75], radius=6, fill=(30, 58, 138, 200), outline=(96, 165, 250, 255), width=1)
    draw.text((75, 52), "PRODUCTION AI AGENT #1", fill=(147, 197, 253), font=badge_font)

    draw.text((60, 90), "Autonomous Public Budget Audit Agent", fill=(248, 250, 252), font=title_font)
    draw.text((60, 142), "Dual-Engine Architecture: Deterministic Text-to-SQL + GraphRAG Cartel Detection", fill=(148, 163, 184), font=subtitle_font)

    # 3 Architecture Columns
    col_width = 330
    col_gap = 40
    start_y = 200
    card_h = 360

    # Column 1: Ingestion & Resolution
    c1_x = 60
    draw.rounded_rectangle([c1_x, start_y, c1_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 220), outline=(56, 189, 248, 200), width=2)
    draw.rounded_rectangle([c1_x + 16, start_y + 16, c1_x + col_width - 16, start_y + 50], radius=6, fill=(14, 116, 144, 150))
    draw.text((c1_x + 28, start_y + 24), "[1] Data Normalization & Ingestion", fill=(224, 242, 254), font=card_header_font)

    items_c1 = [
        ("HWPX Budget Parser", "Formula parsing (Unit Price x Qty = Total)"),
        ("Entity Resolver", "Strip (주)/(유), normalize street addresses"),
        ("KONEPS Procurement", "Track split contracts & bidding metadata"),
        ("dBrain+ Fiscal Collector", "Analyze budget execution and delays")
    ]
    cur_y = start_y + 68
    for title, desc in items_c1:
        draw.rounded_rectangle([c1_x + 16, cur_y, c1_x + col_width - 16, cur_y + 58], radius=8, fill=(15, 23, 42, 180), outline=(51, 65, 85, 255), width=1)
        draw.text((c1_x + 26, cur_y + 10), title, fill=(56, 189, 248), font=card_body_font)
        draw.text((c1_x + 26, cur_y + 32), desc, fill=(148, 163, 184), font=badge_font)
        cur_y += 68

    # Column 2: Dual Brain Engine
    c2_x = c1_x + col_width + col_gap
    draw.rounded_rectangle([c2_x, start_y, c2_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 220), outline=(129, 140, 248, 200), width=2)
    draw.rounded_rectangle([c2_x + 16, start_y + 16, c2_x + col_width - 16, start_y + 50], radius=6, fill=(67, 56, 202, 150))
    draw.text((c2_x + 28, start_y + 24), "[2] Dual-Engine Reasoning", fill=(238, 242, 255), font=card_header_font)

    items_c2 = [
        ("Query Router", "Intent classifier (Stat vs Cartel vs Law)"),
        ("Deterministic Text-to-SQL", "100% zero-hallucination fiscal SQL"),
        ("GraphRAG NetworkX Engine", "Traverse shared address paper cartels"),
        ("Temporal Sliding Window", "Detect smurfing under 20M KRW limit")
    ]
    cur_y = start_y + 68
    for title, desc in items_c2:
        draw.rounded_rectangle([c2_x + 16, cur_y, c2_x + col_width - 16, cur_y + 58], radius=8, fill=(15, 23, 42, 180), outline=(51, 65, 85, 255), width=1)
        draw.text((c2_x + 26, cur_y + 10), title, fill=(165, 180, 252), font=card_body_font)
        draw.text((c2_x + 26, cur_y + 32), desc, fill=(148, 163, 184), font=badge_font)
        cur_y += 68

    # Column 3: XAI & Action
    c3_x = c2_x + col_width + col_gap
    draw.rounded_rectangle([c3_x, start_y, c3_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 220), outline=(52, 211, 153, 200), width=2)
    draw.rounded_rectangle([c3_x + 16, start_y + 16, c3_x + col_width - 16, start_y + 50], radius=6, fill=(6, 95, 70, 150))
    draw.text((c3_x + 28, start_y + 24), "[3] XAI Audit Dossier & Action", fill=(209, 250, 229), font=card_header_font)

    items_c3 = [
        ("Statute & Case Matcher", "State Contract Act & BAI precedents 1:1"),
        ("DEI Index Calculator", "Spot indirect overhead leakage (>50%)"),
        ("Dynamic Risk Scorer", "Real-time 5-tier threat evaluation"),
        ("Action Plan Generator", "Automated contract hold advisories")
    ]
    cur_y = start_y + 68
    for title, desc in items_c3:
        draw.rounded_rectangle([c3_x + 16, cur_y, c3_x + col_width - 16, cur_y + 58], radius=8, fill=(15, 23, 42, 180), outline=(51, 65, 85, 255), width=1)
        draw.text((c3_x + 26, cur_y + 10), title, fill=(52, 211, 153), font=card_body_font)
        draw.text((c3_x + 26, cur_y + 32), desc, fill=(148, 163, 184), font=badge_font)
        cur_y += 68

    # Footer
    draw.text((60, 590), "Global Dev Blog • Spec-Driven Agent Engineering Case Study", fill=(100, 116, 139), font=badge_font)
    draw.text((width - 250, 590), "https://globaldevlog.com", fill=(100, 116, 139), font=badge_font)

    out_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-11-18-autonomous-budget-audit-agent-text-to-sql-graphrag\blog\images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "01_autonomous_budget_audit_agent.png")
    img.save(out_path, format="PNG")
    print(f"Cover image saved to: {out_path}")

if __name__ == "__main__":
    create_cover()
