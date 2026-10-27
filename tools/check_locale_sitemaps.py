# -*- coding: utf-8 -*-
import os
import urllib.request
import xml.etree.ElementTree as ET

GB_ROOT = r"D:\ai\antigravity\global_blog"
locales = ['en', 'ko', 'es', 'ja', 'zh-Hans', 'zh-Hant', 'de', 'fr', 'pt-BR']

print("Checking local sitemaps per locale:")
for loc in locales:
    if loc == 'en':
        p = os.path.join(GB_ROOT, "build", "sitemap.xml")
    else:
        p = os.path.join(GB_ROOT, "build", loc, "sitemap.xml")
    if os.path.exists(p):
        tree = ET.parse(p)
        root = tree.getroot()
        urls = [e.text for e in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        print(f"  [{loc}] sitemap.xml exists: {len(urls)} URLs")
    else:
        print(f"  [{loc}] sitemap.xml MISSING!")

print("\nChecking live sitemaps on https://globaldevlog.com:")
for loc in ['ko', 'de', 'fr', 'pt-BR']:
    url = f"https://globaldevlog.com/{loc}/sitemap.xml"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            urls = [e.text for e in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
            print(f"  [HTTP {resp.status}] {url} -> {len(urls)} URLs")
    except Exception as e:
        print(f"  [ERR] {url}: {e}")
