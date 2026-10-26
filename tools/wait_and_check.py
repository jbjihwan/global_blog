import urllib.request
import ssl
import time

print("Waiting 25 seconds for GitHub Pages CDN propagation...")
time.sleep(25)

urls = [
    "https://globaldevlog.com/blog/2026-10-29-stanford-cs146s-8",
    "https://globaldevlog.com/blog/2026-10-30-stanford-cs146s-9",
    "https://globaldevlog.com/blog/2026-10-31-stanford-cs146s-10",
]

ctx = ssl.create_default_context()
for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            print(f"[{response.status}] {url}")
    except Exception as e:
        print(f"[{e}] {url}")
