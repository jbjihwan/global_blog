with open(r"D:\ai\antigravity\global_blog\build\blog.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = 0
while True:
    idx = html.find("google-adsense", idx)
    if idx == -1:
        break
    snippet = html[max(0, idx-80):min(len(html), idx+200)]
    print(f"--- Occurrence at {idx} ---")
    print(snippet)
    idx += len("google-adsense")
