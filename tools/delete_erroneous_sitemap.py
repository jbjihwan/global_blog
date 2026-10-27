# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import urllib.parse
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
SCOPES = ['https://www.googleapis.com/auth/webmasters']
SITE_URL = "sc-domain:globaldevlog.com"

creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
req = google.auth.transport.requests.Request()
creds.refresh(req)
token = creds.token

# Delete erroneous entry
err_feed = "https://globaldevlog.com/"
url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/sitemaps/{urllib.parse.quote(err_feed, safe='')}"
req_del = urllib.request.Request(url, method='DELETE', headers={"Authorization": f"Bearer {token}"})
try:
    with urllib.request.urlopen(req_del) as resp:
        print(f"[SUCCESS {resp.status}] Deleted erroneous sitemap: {err_feed}")
except urllib.error.HTTPError as e:
    print(f"[FAIL {e.code}] {err_feed}: {e.read().decode('utf-8')}")
