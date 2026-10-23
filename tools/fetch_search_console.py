# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error
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

def query_search_console(dimensions=['query'], row_limit=50):
    token = get_token()
    today = datetime.now()
    end_date = (today - timedelta(days=2)).strftime('%Y-%m-%d')  # GSC has 2-day delay
    start_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')
    
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/searchAnalytics/query"
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "rowLimit": row_limit,
    }
    
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode('utf-8')}")
        return None

if __name__ == '__main__':
    print(f"Querying Search Console for {SITE_URL}...")
    
    # 1. Top Search Queries (Keywords)
    print("\n=== [1] Top Search Keywords (Queries) ===")
    queries_data = query_search_console(dimensions=['query'], row_limit=25)
    rows = queries_data.get('rows', []) if queries_data else []
    if not rows:
        print("No search query data recorded yet (or site was recently registered).")
    else:
        print(f"{'Query':<35} | {'Clicks':<6} | {'Impressions':<11} | {'CTR':<7} | {'Avg Pos':<7}")
        print("-" * 75)
        for r in rows:
            q = r['keys'][0]
            clicks = r.get('clicks', 0)
            imp = r.get('impressions', 0)
            ctr = f"{r.get('ctr', 0)*100:.1f}%"
            pos = f"{r.get('position', 0):.1f}"
            print(f"{q:<35} | {clicks:<6} | {imp:<11} | {ctr:<7} | {pos:<7}")
            
    # 2. Top Landing Pages
    print("\n=== [2] Top Landing Pages ===")
    pages_data = query_search_console(dimensions=['page'], row_limit=15)
    page_rows = pages_data.get('rows', []) if pages_data else []
    if not page_rows:
        print("No page data recorded yet.")
    else:
        print(f"{'Page URL':<60} | {'Clicks':<6} | {'Impressions':<11} | {'CTR':<7}")
        print("-" * 90)
        for r in page_rows:
            p = r['keys'][0].replace('https://globaldevlog.com', '')
            clicks = r.get('clicks', 0)
            imp = r.get('impressions', 0)
            ctr = f"{r.get('ctr', 0)*100:.1f}%"
            print(f"{p:<60} | {clicks:<6} | {imp:<11} | {ctr:<7}")
            
    # 3. Country Distribution
    print("\n=== [3] Top Countries ===")
    country_data = query_search_console(dimensions=['country'], row_limit=10)
    country_rows = country_data.get('rows', []) if country_data else []
    if not country_rows:
        print("No country data recorded yet.")
    else:
        for r in country_rows:
            c = r['keys'][0]
            clicks = r.get('clicks', 0)
            imp = r.get('impressions', 0)
            print(f"Country: {c.upper()} - Clicks: {clicks}, Impressions: {imp}")
