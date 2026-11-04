import json
import urllib.request
import urllib.parse
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
PROP_ID = "558130708"
SITE_URL = "sc-domain:globaldevlog.com"

SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',
    'https://www.googleapis.com/auth/webmasters.readonly'
]

creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
req = google.auth.transport.requests.Request()
creds.refresh(req)
token = creds.token

def query_gsc_sitemaps():
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/sitemaps"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return str(e)

print("=== GSC SITEMAPS ===")
print(query_gsc_sitemaps())
