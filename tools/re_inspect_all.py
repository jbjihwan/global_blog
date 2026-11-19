# -*- coding: utf-8 -*-
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path
from google.oauth2 import service_account
import google.auth.transport.requests

ROOT = Path(r"D:\ai\antigravity\global_blog")
KEY_FILE = ROOT / "credentials" / "service_account.json"
SITE_URL = "sc-domain:globaldevlog.com"
GA4_PROPERTY_ID = "508704754"

def check_live_urls():
    print("=== 1. LIVE WEBSITE HTTP & HTML CHECK ===")
    targets = [
        "https://globaldevlog.com/",
        "https://globaldevlog.com/ko/",
        "https://globaldevlog.com/sitemap.xml",
        "https://globaldevlog.com/ko/sitemap.xml",
        "https://globaldevlog.com/ads.txt",
        "https://globaldevlog.com/robots.txt",
        "https://globaldevlog.com/ko/terms",
        "https://globaldevlog.com/blog/python-urlopen-timeout-dns-hang-windows-fix",
        "https://globaldevlog.com/ko/blog/python-urlopen-timeout-dns-hang-windows-fix",
    ]
    for url in targets:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; InspectionBot/1.0)"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                status = resp.status
                ads_cnt = body.count("adsbygoogle.js")
                has_suicide = ("suicide" in body.lower()) or ("자살" in body)
                if url.endswith("sitemap.xml"):
                    locs = re.findall(r"<loc>(.*?)</loc>", body)
                    print(f"[HTTP {status}] {url} -> URLs in sitemap: {len(locs)}")
                    for l in locs[:5]:
                        print(f"   sample loc: {l}")
                elif url.endswith("ads.txt") or url.endswith("robots.txt"):
                    print(f"[HTTP {status}] {url} -> {body.strip()[:120]}")
                else:
                    has_ko_heading = "5대 핵심 엔지니어링" in body
                    print(f"[HTTP {status}] {url} -> len={len(body)}, adsbygoogle.js={ads_cnt}, suicide/자살={has_suicide}, ko_heading={has_ko_heading}")
        except Exception as e:
            print(f"[ERROR] {url} -> {e}")

def check_gsc():
    print("\n=== 2. GOOGLE SEARCH CONSOLE SITEMAPS & URL INSPECTION ===")
    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    creds = service_account.Credentials.from_service_account_file(str(KEY_FILE), scopes=scopes)
    creds.refresh(google.auth.transport.requests.Request())
    token = creds.token

    # Sitemaps list
    sm_url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/sitemaps"
    req = urllib.request.Request(sm_url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        sm_data = json.loads(resp.read().decode("utf-8"))
        for sm in sm_data.get("sitemap", []):
            print(f"Sitemap: {sm.get('path')} | lastSubmitted={sm.get('lastSubmitted')} | lastDownloaded={sm.get('lastDownloaded')} | errors={sm.get('errors')} | warnings={sm.get('warnings')} | contents={sm.get('contents')}")

    # Inspect live sitemap URLs to get exact blog URLs
    live_sm = urllib.request.urlopen("https://globaldevlog.com/sitemap.xml", timeout=10).read().decode("utf-8")
    en_locs = re.findall(r"<loc>(.*?)</loc>", live_sm)
    live_ko_sm = urllib.request.urlopen("https://globaldevlog.com/ko/sitemap.xml", timeout=10).read().decode("utf-8")
    ko_locs = re.findall(r"<loc>(.*?)</loc>", live_ko_sm)

    print(f"\nLive EN sitemap URLs ({len(en_locs)}):")
    for u in en_locs:
        print("  ", u)

    inspect_targets = [
        "https://globaldevlog.com/",
        "https://globaldevlog.com/ko/",
        "https://globaldevlog.com/ko/terms",
    ]
    # Add first 6 blog URLs from EN sitemap and 3 from KO sitemap
    en_blogs = [u for u in en_locs if "/blog/" in u and not u.endswith("/blog") and "/tags/" not in u and "/archive" not in u]
    ko_blogs = [u for u in ko_locs if "/blog/" in u and not u.endswith("/blog") and "/tags/" not in u and "/archive" not in u]
    inspect_targets.extend(en_blogs[:7])
    inspect_targets.extend(ko_blogs[:4])

    print("\n--- GSC URL Inspection Results ---")
    insp_api = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
    for u in inspect_targets:
        payload = json.dumps({
            "inspectionUrl": u,
            "siteUrl": SITE_URL,
            "languageCode": "ko-KR"
        }).encode("utf-8")
        ireq = urllib.request.Request(
            insp_api,
            data=payload,
            method="POST",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        try:
            with urllib.request.urlopen(ireq, timeout=20) as iresp:
                res = json.loads(iresp.read().decode("utf-8")).get("inspectionResult", {}).get("indexStatusResult", {})
                print(f"URL: {u}")
                print(f"  verdict={res.get('verdict')} | coverageState={res.get('coverageState')} | lastCrawlTime={res.get('lastCrawlTime')} | googleCanonical={res.get('googleCanonical')}")
        except Exception as e:
            print(f"URL: {u} -> Inspect Error: {e}")

def check_local_posts():
    print("\n=== 3. LOCAL 20 POSTS QUALITY & CONSISTENCY AUDIT ===")
    blog_en = ROOT / "blog"
    blog_ko = ROOT / "i18n" / "ko" / "docusaurus-plugin-content-blog"
    en_dirs = sorted([d for d in blog_en.iterdir() if d.is_dir()])
    ko_dirs = sorted([d for d in blog_ko.iterdir() if d.is_dir()])
    print(f"EN post folders: {len(en_dirs)}, KO post folders: {len(ko_dirs)}")
    print(f"Folder names identical: {[d.name for d in en_dirs] == [d.name for d in ko_dirs]}")

    issues = []
    for d in en_dirs:
        en_md = (d / "index.md").read_text(encoding="utf-8")
        ko_md = (blog_ko / d.name / "index.md").read_text(encoding="utf-8")
        en_body = en_md.split("---", 2)[2] if en_md.count("---") >= 2 else en_md
        ko_body = ko_md.split("---", 2)[2] if ko_md.count("---") >= 2 else ko_md
        en_words = len(en_body.split())
        ko_chars = len(ko_body.strip())

        # Check images referenced in markdown exist
        for lang, md_text, base_dir in [("EN", en_md, d), ("KO", ko_md, blog_ko / d.name)]:
            img_refs = re.findall(r"!\[.*?\]\((.*?)\)", md_text)
            for ref in img_refs:
                if ref.startswith("http"):
                    continue
                clean_ref = ref.lstrip("./")
                img_path = base_dir / clean_ref
                if not img_path.exists():
                    issues.append(f"[{lang}] Missing image in {d.name}: {ref}")

        # Check forbidden terms
        for lang, md_text in [("EN", en_md), ("KO", ko_md)]:
            if re.search(r"suicide|자살|자해|claude code|d:\\ai", md_text, re.I):
                issues.append(f"[{lang}] Forbidden term in {d.name}")

        # Check boilerplate TL;DR or excessive Mermaid
        en_tldr = len(re.findall(r"TL;DR|Executive Summary", en_body, re.I))
        en_mermaid = len(re.findall(r"```mermaid", en_body, re.I))
        print(f"  {d.name}: EN={en_words}w, KO={ko_chars}c | TL;DR={en_tldr}, Mermaid={en_mermaid}")

    if issues:
        print("ISSUES FOUND:")
        for iss in issues:
            print("  !", iss)
    else:
        print("Zero broken images or forbidden terms across all 20 EN & 20 KO posts.")

if __name__ == "__main__":
    check_live_urls()
    check_gsc()
    check_local_posts()
