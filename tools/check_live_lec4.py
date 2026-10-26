import urllib.request
import ssl

url = "https://globaldevlog.com/blog/stanford-cs146s-4-spec-driven-code-generation-test-harnesses"
ctx = ssl.create_default_context()
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
        print(f"[{response.status}] {url}")
except Exception as e:
    print(f"[ERR {e}] {url}")
