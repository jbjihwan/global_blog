# -*- coding: utf-8 -*-
import json
import urllib.request
from datetime import datetime, timedelta
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
SITE_URL = "sc-domain:globaldevlog.com"

def get_token():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    req = google.auth.transport.requests.Request()
    creds.refresh(req)
    return creds.token

def run():
    token = get_token()
    today = datetime.now()
    end_date = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    start_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/searchAnalytics/query"
    
    # Device query
    req = urllib.request.Request(
        url,
        data=json.dumps({"startDate": start_date, "endDate": end_date, "dimensions": ["device"]}).encode('utf-8'),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        dev_data = json.loads(resp.read().decode('utf-8'))
        print("Device breakdown:")
        for r in dev_data.get('rows', []):
            print(f"  {r['keys'][0]}: {r.get('impressions', 0)} impressions, {r.get('clicks', 0)} clicks")

if __name__ == '__main__':
    run()
