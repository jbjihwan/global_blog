#!/usr/bin/env python3
import os
from PIL import Image

KO_BLOG = r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog"
eps = [
    "2026-03-31-maeumjigi-3",
    "2026-04-01-maeumjigi-4",
    "2026-04-03-maeumjigi-5",
    "2026-04-05-maeumjigi-6",
    "2026-04-07-maeumjigi-7",
    "2026-04-08-maeumjigi-8",
    "2026-05-17-maeumjigi-19",
    "2026-06-18-maeumjigi-23"
]

for ep in eps:
    p = os.path.join(KO_BLOG, ep, "images", "01_cover.png")
    if os.path.exists(p):
        with Image.open(p) as im:
            print(f"{ep:<30} | {im.size}")
    else:
        print(f"{ep:<30} | NOT FOUND")
