# -*- coding: utf-8 -*-
import json
import urllib.request
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
PROP_ID = "558130708"

def get_token():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=['https://www.googleapis.com/auth/analytics.readonly'])
    req = google.auth.transport.requests.Request()
    creds.refresh(req)
    return creds.token

def query_ga4(token, payload):
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{PROP_ID}:runReport"
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def main():
    token = get_token()
    
    # 1. Inspect Oct 20 peak by Country, City, Operating System, Browser
    print("=== [1] 2026-10-20 (Peak Day) Breakdown ===")
    res_peak = query_ga4(token, {
        "dateRanges": [{"startDate": "2026-10-20", "endDate": "2026-10-20"}],
        "dimensions": [
            {"name": "country"},
            {"name": "city"},
            {"name": "operatingSystem"},
            {"name": "browser"},
            {"name": "deviceCategory"}
        ],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "userEngagementDuration"}
        ]
    })
    if res_peak and res_peak.get('rows'):
        print(f"{'Country':<15} | {'City':<15} | {'OS':<12} | {'Browser':<12} | {'Users':<6} | {'Views':<6} | {'Avg Time':<8}")
        print("-" * 80)
        for r in res_peak['rows']:
            co, ci, os, br, dev = [d['value'] for d in r['dimensionValues']]
            u, s, v, dur = [float(m['value']) for m in r['metricValues']]
            avg_t = dur / u if u > 0 else 0
            print(f"{co:<15} | {ci:<15} | {os:<12} | {br:<12} | {int(u):<6} | {int(v):<6} | {avg_t:<7.1f}s")

    # 2. Inspect Oct 24~26 Breakdown
    print("\n=== [2] 2026-10-24 ~ 2026-10-26 (Low Period) Breakdown ===")
    res_low = query_ga4(token, {
        "dateRanges": [{"startDate": "2026-10-24", "endDate": "2026-10-26"}],
        "dimensions": [
            {"name": "country"},
            {"name": "city"},
            {"name": "operatingSystem"},
            {"name": "browser"},
            {"name": "sessionDefaultChannelGroup"}
        ],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "userEngagementDuration"}
        ]
    })
    if res_low and res_low.get('rows'):
        print(f"{'Country':<15} | {'City':<15} | {'OS':<12} | {'Channel':<15} | {'Users':<6} | {'Views':<6} | {'Avg Time':<8}")
        print("-" * 85)
        for r in res_low['rows']:
            co, ci, os, br, ch = [d['value'] for d in r['dimensionValues']]
            u, s, v, dur = [float(m['value']) for m in r['metricValues']]
            avg_t = dur / u if u > 0 else 0
            print(f"{co:<15} | {ci:<15} | {os:<12} | {ch:<15} | {int(u):<6} | {int(v):<6} | {avg_t:<7.1f}s")

    # 3. Check Naver Blog or Inflow Referrers across the last 14 days
    print("\n=== [3] Referrers across the last 14 days ===")
    res_ref = query_ga4(token, {
        "dateRanges": [{"startDate": "14daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "pageReferrer"}, {"name": "sessionSourceMedium"}],
        "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}],
        "limit": 20
    })
    if res_ref and res_ref.get('rows'):
        print(f"{'Page Referrer':<60} | {'Source/Medium':<20} | {'Users':<6} | {'Views':<6}")
        print("-" * 95)
        for r in res_ref['rows']:
            ref, sm = [d['value'] for d in r['dimensionValues']]
            u, s, v = [int(m['value']) for m in r['metricValues']]
            print(f"{ref[:58]:<60} | {sm[:18]:<20} | {u:<6} | {v:<6}")

if __name__ == '__main__':
    main()
