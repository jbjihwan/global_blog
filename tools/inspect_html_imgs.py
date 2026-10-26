import urllib.request, ssl, re

ctx = ssl.create_default_context()
url = "https://globaldevlog.com/ko/blog/maeumjigi-1"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    html = resp.read().decode('utf-8')

for tag in re.findall(r'<img[^>]+>', html):
    print("IMG TAG:", tag)
