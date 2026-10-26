#!/usr/bin/env python3
import os
from PIL import Image

p = r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog\2026-10-18-static-site-security-hardening\images\01_threat_model.png"
with Image.open(p) as im:
    print(f"Path: {p}")
    print(f"Size: {im.size}, Format: {im.format}, Mode: {im.mode}")
