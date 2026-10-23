# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error
import sys
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def get_token():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    req = google.auth.transport.requests.Request()
    creds.refresh(req)
    return creds.token

def run_ga4_report(property_id, start_date="30daysAgo", end_date="today"):
    token = get_token()
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
    
    # 1. Page views & engagement
    payload = {
        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
        "dimensions": [{"name": "pagePath"}, {"name": "pageTitle"}],
        "metrics": [
            {"name": "screenPageViews"},
            {"name": "activeUsers"},
            {"name": "userEngagementDuration"}
        ],
        "limit": 20
    }
    
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"GA4 Error {e.code}: {e.read().decode('utf-8')}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fetch_ga4.py <PROPERTY_ID>")
    else:
        prop_id = sys.argv[1]
        print(f"Fetching GA4 report for Property ID: {prop_id}...")
        res = run_ga4_report(prop_id)
        if res:
            rows = res.get('rows', [])
            print(f"Found {len(rows)} page rows:")
            for r in rows:
                path = r['dimensionValues'][0]['value']
                views = r['metricValues'][0]['value']
                users = r['metricValues'][1]['value']
                duration = float(r['metricValues'][2]['value'])
                print(f"  {path:<45} | Views: {views:<4} | Users: {users:<3} | Total Duration: {duration:.0f}s")
