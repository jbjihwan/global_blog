import urllib.request
import ssl

urls = [
    "https://globaldevlog.com/blog/2026-10-25-stanford-cs146s-4",
    "https://globaldevlog.com/blog/2026-10-26-stanford-cs146s-5",
    "https://globaldevlog.com/blog/2026-10-27-stanford-cs146s-6",
    "https://globaldevlog.com/blog/2026-10-28-stanford-cs146s-7",
]

ctx = ssl.create_default_context()

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            print(f"[{response.status}] {url}")
    except Exception as e:
        print(f"[ERR {e}] {url}")
