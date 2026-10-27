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
    
    # 1. Total summary per day from 2026-10-18 to 2026-10-26
    print("=== Daily Traffic Summary ===")
    res = query_ga4(token, {
        "dateRanges": [{"startDate": "2026-10-18", "endDate": "today"}],
        "dimensions": [{"name": "date"}],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "newUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "engagementRate"},
            {"name": "userEngagementDuration"}
        ],
        "orderBys": [{"dimension": {"dimensionName": "date"}}]
    })
    
    for r in res.get('rows', []):
        dt = r['dimensionValues'][0]['value']
        dt_fmt = f"{dt[:4]}-{dt[4:6]}-{dt[6:]}"
        u = int(r['metricValues'][0]['value'])
        nu = int(r['metricValues'][1]['value'])
        s = int(r['metricValues'][2]['value'])
        p = int(r['metricValues'][3]['value'])
        eng = float(r['metricValues'][4]['value']) * 100
        dur = float(r['metricValues'][5]['value'])
        avg_d = dur / u if u > 0 else 0
        print(f"{dt_fmt} | Users: {u:>2} (New: {nu:>2}) | Sess: {s:>2} | Views: {p:>3} | Eng: {eng:5.1f}% | AvgDur: {avg_d:5.1f}s")

if __name__ == '__main__':
    main()
