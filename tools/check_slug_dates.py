import os, re

blog_dir = r"D:\ai\antigravity\global_blog\blog"
no_date_slugs = []

for d in os.listdir(blog_dir):
    p = os.path.join(blog_dir, d, "index.md")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
        m = re.search(r"^slug:\s*([^\s\n\r]+)", c, re.MULTILINE)
        if m:
            slug = m.group(1).strip("'\"")
            if not re.match(r"^\d{4}-\d{2}-\d{2}", slug):
                dm = re.search(r"^date:\s*([^\s\n\r]+)", c, re.MULTILINE)
                dstr = dm.group(1).strip("'\"") if dm else "unknown"
                no_date_slugs.append((slug, dstr, d))

print(f"Total posts with clean slugs (no date in slug): {len(no_date_slugs)}")
for s, dt, folder in no_date_slugs:
    print(f"  Slug: {s:65} | Date: {dt}")
