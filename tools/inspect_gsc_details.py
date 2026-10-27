# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
SITE_URL = "sc-domain:globaldevlog.com"

def get_token():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
    req = google.auth.transport.requests.Request()
    creds.refresh(req)
    return creds.token

def main():
    token = get_token()
    today = datetime.now()
    end_date = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    start_date = (today - timedelta(days=14)).strftime('%Y-%m-%d')
    
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/searchAnalytics/query"
    
    # 1. Queries
    payload = {"startDate": start_date, "endDate": end_date, "dimensions": ["query"], "rowLimit": 20}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("=== Top Queries ===")
        for r in res.get('rows', []):
            print(f"Query: {r['keys'][0]} | Imp: {r.get('impressions', 0)} | Clicks: {r.get('clicks', 0)} | Pos: {r.get('position', 0):.1f}")

    # 2. Pages
    payload = {"startDate": start_date, "endDate": end_date, "dimensions": ["page"], "rowLimit": 20}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("\n=== Top GSC Pages ===")
        for r in res.get('rows', []):
            p = r['keys'][0].replace('https://globaldevlog.com', '')
            print(f"Page: {p:<50} | Imp: {r.get('impressions', 0)} | Clicks: {r.get('clicks', 0)} | Pos: {r.get('position', 0):.1f}")

if __name__ == '__main__':
    main()
