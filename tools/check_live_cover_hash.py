import urllib.request, ssl

ctx = ssl.create_default_context()
url = "https://globaldevlog.com/ko/assets/images/01_cover-8e6ecae73858a2c32f20886c97e77030.png"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        print("New image status:", resp.status, "Length:", resp.headers.get('Content-Length'))
except Exception as e:
    print("New image error:", e)

# Also check what the blog post HTML references:
url_page = "https://globaldevlog.com/ko/blog/maeumjigi-1"
req_page = urllib.request.Request(url_page, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req_page, context=ctx, timeout=10) as resp_page:
        html = resp_page.read().decode('utf-8')
        import re
        imgs = re.findall(r'src="([^"]+01_cover[^"]+)"', html)
        print("HTML image references for 01_cover:", imgs)
except Exception as e:
    print("Page error:", e)
