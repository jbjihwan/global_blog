# -*- coding: utf-8 -*-
import os
import urllib.request
import xml.etree.ElementTree as ET

# 1. Check local build/sitemap.xml
local_sitemap = r"D:\ai\antigravity\global_blog\build\sitemap.xml"
if os.path.exists(local_sitemap):
    tree = ET.parse(local_sitemap)
    root = tree.getroot()
    namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [loc.text for loc in root.findall('.//ns:loc', namespaces)]
    print(f"Total URLs in local sitemap: {len(urls)}")
    
    locales = ['/de/', '/fr/', '/pt-BR/', '/ko/', '/es/', '/ja/', '/zh-Hans/', '/zh-Hant/']
    for loc in locales:
        count = sum(1 for u in urls if loc in u)
        print(f"  Locale '{loc}': {count} URLs")
else:
    print("Local sitemap.xml not found")

# 2. Check live sitemap
print("\nFetching live https://globaldevlog.com/sitemap.xml...")
try:
    req = urllib.request.Request("https://globaldevlog.com/sitemap.xml", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read()
        live_root = ET.fromstring(content)
        live_urls = [loc.text for loc in live_root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        print(f"Total URLs in live sitemap: {len(live_urls)}")
        for loc in ['/de/', '/fr/', '/pt-BR/']:
            count = sum(1 for u in live_urls if loc in u)
            print(f"  Live Locale '{loc}': {count} URLs")
except Exception as e:
    print(f"Error fetching live sitemap: {e}")
