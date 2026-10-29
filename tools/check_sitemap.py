import xml.etree.ElementTree as ET

tree = ET.parse(r"D:\ai\antigravity\global_blog\build\sitemap.xml")
root = tree.getroot()

budget_urls = []
for url in root:
    loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    if loc is not None and "budget" in loc.text:
        budget_urls.append(loc.text)

print(f"Total budget URLs in sitemap: {len(budget_urls)}")
for u in sorted(budget_urls)[:20]:
    print(" -", u)
