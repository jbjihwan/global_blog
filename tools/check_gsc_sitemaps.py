# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error
import urllib.parse
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly', 'https://www.googleapis.com/auth/webmasters']
SITE_URL = "sc-domain:globaldevlog.com"

def get_token():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    req = google.auth.transport.requests.Request()
    creds.refresh(req)
    return creds.token

def list_sitemaps():
    token = get_token()
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/sitemaps"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode('utf-8')}")
        return None

if __name__ == '__main__':
    res = list_sitemaps()
    print("GSC Sitemaps for", SITE_URL)
    print(json.dumps(res, indent=2))
