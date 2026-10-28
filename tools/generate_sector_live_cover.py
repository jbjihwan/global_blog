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

    # Accent glow top bar (Cyan/Indigo for live stream and portal)
    draw.rectangle([0, 0, width, 6], fill=(14, 165, 233, 255))

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
    draw.rounded_rectangle([60, 42, 270, 72], radius=6, fill=(14, 116, 144, 220), outline=(56, 189, 248, 255), width=1)
    draw.text((75, 49), "PRODUCTION AI AGENT #3", fill=(224, 242, 254), font=badge_font)

    draw.text((60, 85), "3D Sector Partitioning & Live Audit Web Portal", fill=(248, 250, 252), font=title_font)
    draw.text((60, 137), "Eliminating 85% Procurement Noise and Streaming Live APIs into Interactive Dossiers", fill=(148, 163, 184), font=subtitle_font)

    # 3 Architecture Columns
    col_width = 330
    col_gap = 40
    start_y = 195
    card_h = 370

    # Column 1: Sector Partitioning
    c1_x = 60
    draw.rounded_rectangle([c1_x, start_y, c1_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 220), outline=(56, 189, 248, 200), width=2)
    draw.rounded_rectangle([c1_x + 16, start_y + 16, c1_x + col_width - 16, start_y + 50], radius=6, fill=(14, 116, 144, 150))
    draw.text((c1_x + 24, start_y + 24), "[1] 3D Sector Partitioning", fill=(224, 242, 254), font=card_header_font)

    items_c1 = [
        ("85% Noise Elimination", "Filter routine consumables & office supplies"),
        ("Sector 1: ICT Split Contracts", "Pinpoint sub-$20k private contract smurfs"),
        ("Sector 2: Event Agency Bids", "Detect regional festival kickback networks"),
        ("Sector 3: Welfare DEI Leak", "Track indirect administrative takes (>50%)")
    ]
    cur_y = start_y + 68
    for title, desc in items_c1:
        draw.rounded_rectangle([c1_x + 16, cur_y, c1_x + col_width - 16, cur_y + 60], radius=8, fill=(15, 23, 42, 180), outline=(51, 65, 85, 255), width=1)
        draw.text((c1_x + 26, cur_y + 10), title, fill=(56, 189, 248), font=card_body_font)
        draw.text((c1_x + 26, cur_y + 34), desc, fill=(148, 163, 184), font=badge_font)
        cur_y += 70

    # Column 2: Live API & Resilience
    c2_x = c1_x + col_width + col_gap
    draw.rounded_rectangle([c2_x, start_y, c2_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 220), outline=(129, 140, 248, 200), width=2)
    draw.rounded_rectangle([c2_x + 16, start_y + 16, c2_x + col_width - 16, start_y + 50], radius=6, fill=(67, 56, 202, 150))
    draw.text((c2_x + 24, start_y + 24), "[2] Live API & Resilience", fill=(238, 242, 255), font=card_header_font)

    items_c2 = [
        ("KONEPS Live Stream Sync", "Automated sync with public procurement API"),
        ("Robust Caret (^) Parser", "Parse complex multi-value delimiter fields"),
        ("Idempotent Fingerprint", "SHA-256 keys preventing duplicate alerts"),
        ("Daily Background Monitor", "Continuous zero-downtime anomaly watcher")
    ]
    cur_y = start_y + 68
    for title, desc in items_c2:
        draw.rounded_rectangle([c2_x + 16, cur_y, c2_x + col_width - 16, cur_y + 60], radius=8, fill=(15, 23, 42, 180), outline=(51, 65, 85, 255), width=1)
        draw.text((c2_x + 26, cur_y + 10), title, fill=(165, 180, 252), font=card_body_font)
        draw.text((c2_x + 26, cur_y + 34), desc, fill=(148, 163, 184), font=badge_font)
        cur_y += 70

    # Column 3: Web Portal v2.0
    c3_x = c2_x + col_width + col_gap
    draw.rounded_rectangle([c3_x, start_y, c3_x + col_width, start_y + card_h], radius=12, fill=(30, 41, 59, 220), outline=(52, 211, 153, 200), width=2)
    draw.rounded_rectangle([c3_x + 16, start_y + 16, c3_x + col_width - 16, start_y + 50], radius=6, fill=(6, 95, 70, 150))
    draw.text((c3_x + 24, start_y + 24), "[3] Inspector Web Portal v2.0", fill=(209, 250, 229), font=card_header_font)

    items_c3 = [
        ("Vis.js Ego-Network Graph", "Sub-graph virtualization solving UI freeze"),
        ("10-Yr Precedent Explorer", "Instant search across BAI & NABO rulings"),
        ("Instant HWPX Table Parser", "Live drag-and-drop markup verification"),
        ("Court-Ready Export", "One-click legal audit dossiers & markdown")
    ]
    cur_y = start_y + 68
    for title, desc in items_c3:
        draw.rounded_rectangle([c3_x + 16, cur_y, c3_x + col_width - 16, cur_y + 60], radius=8, fill=(15, 23, 42, 180), outline=(51, 65, 85, 255), width=1)
        draw.text((c3_x + 26, cur_y + 10), title, fill=(52, 211, 153), font=card_body_font)
        draw.text((c3_x + 26, cur_y + 34), desc, fill=(148, 163, 184), font=badge_font)
        cur_y += 70

    # Footer
    draw.text((60, 592), "Global Dev Blog • Spec-Driven Agent Engineering Case Study", fill=(100, 116, 139), font=badge_font)
    draw.text((width - 250, 592), "https://globaldevlog.com", fill=(100, 116, 139), font=badge_font)

    base_stage = r"D:\ai\antigravity\global_blog\배포대기\2026-11-20-national-budget-ai-sector-partition-live-monitoring"
    primary_dir = os.path.join(base_stage, "blog", "images")
    os.makedirs(primary_dir, exist_ok=True)
    out_path = os.path.join(primary_dir, "01_national_budget_sector_live_monitor.png")
    img.save(out_path, format="PNG")
    print(f"Primary cover image saved to: {out_path}")

    # Replicate to all 8 locale folders
    locales = ["ko", "ja", "zh-Hans", "zh-Hant", "es", "de", "fr", "pt-BR"]
    for loc in locales:
        loc_dir = os.path.join(base_stage, "i18n", loc, "images")
        os.makedirs(loc_dir, exist_ok=True)
        dest_path = os.path.join(loc_dir, "01_national_budget_sector_live_monitor.png")
        shutil.copyfile(out_path, dest_path)
        print(f"Copied to: {dest_path}")

if __name__ == "__main__":
    create_cover()
