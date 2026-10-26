import urllib.request, ssl

ctx = ssl.create_default_context()
url = "https://globaldevlog.com/ads.txt"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        print(f"Status: {resp.status}")
        print("Live ads.txt content:\n", resp.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
