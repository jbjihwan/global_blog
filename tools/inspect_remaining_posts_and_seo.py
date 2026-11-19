# -*- coding: utf-8 -*-
import json
import re
import urllib.request
from pathlib import Path
from google.oauth2 import service_account
import google.auth.transport.requests

ROOT = Path(r"D:\ai\antigravity\global_blog")
KEY_FILE = ROOT / "credentials" / "service_account.json"
SITE_URL = "sc-domain:globaldevlog.com"
BUILD = ROOT / "build"

def inspect_remaining_gsc():
    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    creds = service_account.Credentials.from_service_account_file(str(KEY_FILE), scopes=scopes)
    creds.refresh(google.auth.transport.requests.Request())
    token = creds.token

    targets = [
        "https://globaldevlog.com/blog",
        "https://globaldevlog.com/ko/blog",
        "https://globaldevlog.com/blog/2026-05-21-rl-qlearning-5",
        "https://globaldevlog.com/blog/2026-06-25-vision-anpr-1",
        "https://globaldevlog.com/blog/2026-06-26-vision-anpr-2",
        "https://globaldevlog.com/blog/2026-06-27-vision-anpr-3",
        "https://globaldevlog.com/blog/2026-06-28-vision-anpr-4",
        "https://globaldevlog.com/blog/2026-06-29-vision-anpr-5",
        "https://globaldevlog.com/blog/static-site-security-npm-audit-truth",
        "https://globaldevlog.com/blog/github-pages-custom-domain-cloudflare-dns",
        "https://globaldevlog.com/blog/npm-overrides-transitive-vulnerability-fix",
        "https://globaldevlog.com/blog/sdc-01-architecture-klm-model",
        "https://globaldevlog.com/blog/sdc-02-stack-spike-doctrine-hypotheses",
        "https://globaldevlog.com/blog/sdc-03-deterministic-jcs-ed25519-fragmentation",
        "https://globaldevlog.com/blog/python-urlopen-timeout-dns-hang-windows-fix",
        "https://globaldevlog.com/ko/blog/python-urlopen-timeout-dns-hang-windows-fix",
    ]
    insp_api = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
    print("=== GSC URL INSPECTION (REMAINING 16 URLs) ===")
    for u in targets:
        payload = json.dumps({
            "inspectionUrl": u,
            "siteUrl": SITE_URL,
            "languageCode": "ko-KR"
        }).encode("utf-8")
        req = urllib.request.Request(
            insp_api, data=payload, method="POST",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                res = json.loads(resp.read().decode("utf-8")).get("inspectionResult", {}).get("indexStatusResult", {})
                print(f"URL: {u}")
                print(f"  verdict={res.get('verdict')} | state={res.get('coverageState')} | lastCrawl={res.get('lastCrawlTime')} | referringUrls={res.get('referringUrls')}")
        except Exception as e:
            print(f"URL: {u} -> {e}")

def inspect_html_seo_and_links():
    print("\n=== STATIC HTML SEO & INTERNAL LINK GRAPH AUDIT ===")
    pages = [
        ("EN Home", BUILD / "index.html"),
        ("KO Home", BUILD / "ko" / "index.html"),
        ("EN Blog List", BUILD / "blog" / "index.html"),
        ("KO Blog List", BUILD / "ko" / "blog" / "index.html"),
        ("EN New Post", BUILD / "blog" / "python-urlopen-timeout-dns-hang-windows-fix" / "index.html"),
        ("KO New Post", BUILD / "ko" / "blog" / "python-urlopen-timeout-dns-hang-windows-fix" / "index.html"),
    ]
    for label, p in pages:
        if not p.exists():
            print(f"[{label}] MISSING: {p}")
            continue
        html = p.read_text(encoding="utf-8")
        title = re.findall(r"<title[^>]*>(.*?)</title>", html)
        canonical = re.findall(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', html)
        hreflangs = re.findall(r'<link[^>]+rel="alternate"[^>]+hreflang="([^"]+)"[^>]+href="([^"]+)"', html)
        hrefs = re.findall(r'href="([^"]+)"', html)
        blog_links = sorted(set(h for h in hrefs if "/blog/" in h))
        print(f"[{label}] title={title[0] if title else 'NONE'}")
        print(f"  canonical={canonical}")
        print(f"  hreflangs={hreflangs}")
        print(f"  internal /blog/ links count={len(blog_links)}: {blog_links[:10]}")

if __name__ == "__main__":
    inspect_html_seo_and_links()
    inspect_remaining_gsc()
