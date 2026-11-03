# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

def create_cover(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    width = 1200
    height = 630
    img = Image.new("RGBA", (width, height), (15, 23, 42, 255)) # Dark slate navy
    draw = ImageDraw.Draw(img)

    # Background grid lines
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=(30, 41, 59, 100), width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=(30, 41, 59, 100), width=1)

    # Accent glow top bar (Gold / Amber / Emerald gradient)
    draw.rectangle([0, 0, width, 6], fill=(245, 158, 11, 255)) # Amber gold

    # Fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        subtitle_font = ImageFont.truetype("arial.ttf", 18)
        card_header_font = ImageFont.truetype("arialbd.ttf", 16)
        card_body_font = ImageFont.truetype("arial.ttf", 13)
        badge_font = ImageFont.truetype("arialbd.ttf", 12)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        card_header_font = ImageFont.load_default()
        card_body_font = ImageFont.load_default()
        badge_font = ImageFont.load_default()

    # Top Category Badge
    badge_text = "PUBLIC BUDGET AI #9 · FULL-SCALE SURVEILLANCE & 5-OPTION DECISION ENGINE"
    draw.rectangle([60, 40, 720, 68], fill=(30, 58, 138, 220), outline=(59, 130, 246, 255), width=1)
    draw.text((75, 47), badge_text, font=badge_font, fill=(147, 197, 253, 255))

    # Main Title
    draw.text((60, 85), "23,825 Anomaly Sub-items Automated Surveillance", font=title_font, fill=(255, 255, 255, 255))
    draw.text((60, 130), "5-Option Decision Engine & Live Cumulative Audit Ledger", font=title_font, fill=(245, 158, 11, 255))

    # Subtitle
    subtitle = "677.4T KRW Budget Scanning | SQLite WAL Batch Pipeline | Legal Sanction Dispatch & 121.7T KRW Cut Ledger"
    draw.text((60, 180), subtitle, font=subtitle_font, fill=(148, 163, 184, 255))

    # 3 Main Architecture Cards
    card_y = 230
    card_h = 330
    card_w = 330

    # Card 1: 4 Risk Categories Scanner
    c1_x = 60
    draw.rectangle([c1_x, card_y, c1_x + card_w, card_y + card_h], fill=(30, 41, 59, 230), outline=(51, 65, 85, 255), width=2)
    draw.rectangle([c1_x, card_y, c1_x + card_w, card_y + 40], fill=(51, 65, 85, 255))
    draw.text((c1_x + 15, card_y + 12), "1. 4-Risk Anomaly Ingestion", font=card_header_font, fill=(255, 255, 255, 255))
    
    c1_items = [
        ("Target Scope:", "677.4T KRW / 23,825 Sub-items"),
        ("1. Sluggish Exec:", "Disused > 30% (Fiscal Act §89)"),
        ("2. Private Consign:", "Overhead Leakage (Refund Act §8)"),
        ("3. Wasteful Services:", "Inflated Unit Cost (Contract §7)"),
        ("4. Q4 Dump / Cartel:", "Split Bidding Rings (Crim. §315)"),
        ("Batch Pipeline:", "0.25s Fast Playback Engine"),
        ("Throughput:", "95,000 Inferences / Sec")
    ]
    cur_y = card_y + 55
    for label, val in c1_items:
        draw.text((c1_x + 15, cur_y), label, font=card_header_font, fill=(245, 158, 11, 255))
        draw.text((c1_x + 15, cur_y + 18), val, font=card_body_font, fill=(203, 213, 225, 255))
        cur_y += 38

    # Card 2: 5-Option Standard Decision Matrix
    c2_x = 420
    draw.rectangle([c2_x, card_y, c2_x + card_w, card_y + card_h], fill=(30, 41, 59, 230), outline=(245, 158, 11, 150), width=2)
    draw.rectangle([c2_x, card_y, c2_x + card_w, card_y + 40], fill=(180, 83, 9, 255))
    draw.text((c2_x + 15, card_y + 12), "2. 5-Option Decision Matrix", font=card_header_font, fill=(255, 255, 255, 255))

    c2_items = [
        ("Option 1:", "Approve Full Cut (100% Demand Cap)"),
        ("Option 2:", "Direct Mediation Cut (50% Compromise)"),
        ("Option 3:", "48h Minister Summons Formal Query"),
        ("Option 4:", "Prosecution Dispatch (Public Loss Act)"),
        ("Option 5:", "Legitimate Execution (Exception Pass)"),
        ("Collision Arbiter:", "Criminal Law Priority Tree Rule"),
        ("Constraint Invariant:", "clamp(cut, 0, budget * 0.70)")
    ]
    cur_y = card_y + 55
    for label, val in c2_items:
        draw.text((c2_x + 15, cur_y), label, font=card_header_font, fill=(251, 191, 36, 255))
        draw.text((c2_x + 15, cur_y + 18), val, font=card_body_font, fill=(203, 213, 225, 255))
        cur_y += 38

    # Card 3: SQLite WAL & Ledger Stacking
    c3_x = 780
    draw.rectangle([c3_x, card_y, c3_x + card_w, card_y + card_h], fill=(30, 41, 59, 230), outline=(16, 185, 129, 150), width=2)
    draw.rectangle([c3_x, card_y, c3_x + card_w, card_y + 40], fill=(5, 150, 105, 255))
    draw.text((c3_x + 15, card_y + 12), "3. Storage & Ledger Stacking", font=card_header_font, fill=(255, 255, 255, 255))

    c3_items = [
        ("Database Engine:", "SQLite3 WAL Mode (No Lock)"),
        ("Review Log DB:", "surveillance_review_log (19 cols)"),
        ("Live Ledger Doc:", "CUMULATIVE_SURVEILLANCE_AUDIT"),
        ("Verified Cuts:", "121.72 Trillion KRW (100%)"),
        ("Summons Dispatch:", "Automated Assembly Dossier"),
        ("HWPX Generation:", "Full National Audit Report v2026"),
        ("Audit Integrity:", "Zero False Dismissal Guarantee")
    ]
    cur_y = card_y + 55
    for label, val in c3_items:
        draw.text((c3_x + 15, cur_y), label, font=card_header_font, fill=(110, 231, 183, 255))
        draw.text((c3_x + 15, cur_y + 18), val, font=card_body_font, fill=(203, 213, 225, 255))
        cur_y += 38

    # Bottom watermark bar
    draw.rectangle([60, 580, 1110, 605], fill=(15, 23, 42, 200))
    draw.text((65, 585), "Global Dev Blog · Public Budget AI Series Ep. 9 · Open Source Public Finance Anomaly Defense", font=badge_font, fill=(100, 116, 139, 255))

    img.save(output_path, "PNG")
    print(f"[OK] Generated cover at {output_path}")

if __name__ == "__main__":
    out_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-12-02-national-budget-surveillance-automated-audit-ledger\blog\images"
    os.makedirs(out_dir, exist_ok=True)
    create_cover(os.path.join(out_dir, "01_cover.png"))
