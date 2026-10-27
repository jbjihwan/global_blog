# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error
import urllib.parse
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
SCOPES = ['https://www.googleapis.com/auth/webmasters']
SITE_URL = "sc-domain:globaldevlog.com"

def get_token():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    req = google.auth.transport.requests.Request()
    creds.refresh(req)
    return creds.token

def submit_sitemap(feedpath):
    token = get_token()
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/sitemaps/{urllib.parse.quote(feedpath, safe='')}"
    req = urllib.request.Request(url, method='PUT', headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[SUCCESS {resp.status}] Submitted: {feedpath}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[FAIL {e.code}] {feedpath}: {e.read().decode('utf-8')}")
        return False

if __name__ == '__main__':
    for feed in [
        "https://globaldevlog.com/de/sitemap.xml",
        "https://globaldevlog.com/fr/sitemap.xml",
        "https://globaldevlog.com/pt-BR/sitemap.xml"
    ]:
        submit_sitemap(feed)
