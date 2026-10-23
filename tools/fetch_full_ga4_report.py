# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
PROP_ID = "558130708"

def get_token():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    req = google.auth.transport.requests.Request()
    creds.refresh(req)
    return creds.token

def query_ga4(token, endpoint, payload):
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{PROP_ID}:{endpoint}"
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
        print(f"API Error {e.code}: {e.read().decode('utf-8')}")
        return None

def main():
    token = get_token()
    
    # 1. Total KPI Overview (Last 30 days)
    print("=== [1] GA4 Overall Traffic KPIs (Last 30 Days) ===")
    res_kpi = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "userEngagementDuration"},
            {"name": "engagementRate"},
            {"name": "bounceRate"}
        ]
    })
    if res_kpi and res_kpi.get('rows'):
        mv = res_kpi['rows'][0]['metricValues']
        users = mv[0]['value']
        sessions = mv[1]['value']
        views = mv[2]['value']
        dur = float(mv[3]['value'])
        eng_rate = float(mv[4]['value']) * 100
        bounce_rate = float(mv[5]['value']) * 100 if len(mv) > 5 else 0.0
        avg_dur_per_user = (dur / float(users)) if float(users) > 0 else 0
        print(f"Total Active Users:        {users}")
        print(f"Total Sessions:            {sessions}")
        print(f"Total Screen Page Views:   {views}")
        print(f"Engagement Rate:           {eng_rate:.1f}%")
        print(f"Avg Engagement Per User:   {avg_dur_per_user:.1f} seconds")
        print(f"Total Engagement Time:     {dur / 60:.1f} minutes")
        
    # 2. Traffic Channels (Acquisition)
    print("\n=== [2] Traffic Channels (How Users Found Your Site) ===")
    res_channel = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}, {"name": "sessionSourceMedium"}],
        "metrics": [{"name": "sessions"}, {"name": "activeUsers"}],
        "limit": 10
    })
    if res_channel and res_channel.get('rows'):
        print(f"{'Channel':<20} | {'Source / Medium':<25} | {'Sessions':<8} | {'Users':<6}")
        print("-" * 65)
        for r in res_channel['rows']:
            ch = r['dimensionValues'][0]['value']
            src = r['dimensionValues'][1]['value']
            sess = r['metricValues'][0]['value']
            us = r['metricValues'][1]['value']
            print(f"{ch:<20} | {src:<25} | {sess:<8} | {us:<6}")

    # 3. Countries and Languages
    print("\n=== [3] Global Demographics (Country & Language) ===")
    res_geo = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "country"}, {"name": "language"}],
        "metrics": [{"name": "activeUsers"}, {"name": "screenPageViews"}],
        "limit": 10
    })
    if res_geo and res_geo.get('rows'):
        print(f"{'Country':<25} | {'Browser Language':<18} | {'Users':<6} | {'Page Views':<10}")
        print("-" * 65)
        for r in res_geo['rows']:
            co = r['dimensionValues'][0]['value']
            la = r['dimensionValues'][1]['value']
            us = r['metricValues'][0]['value']
            pv = r['metricValues'][1]['value']
            print(f"{co:<25} | {la:<18} | {us:<6} | {pv:<10}")

    # 4. Top 10 Most Read Blog Posts
    print("\n=== [4] Top 10 Most Visited Content / Posts ===")
    res_pages = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "pagePath"}],
        "metrics": [
            {"name": "screenPageViews"},
            {"name": "activeUsers"},
            {"name": "userEngagementDuration"}
        ],
        "limit": 12
    })
    if res_pages and res_pages.get('rows'):
        print(f"{'Page Path':<50} | {'Views':<6} | {'Users':<6} | {'Avg Time (s)':<12}")
        print("-" * 80)
        for r in res_pages['rows']:
            path = r['dimensionValues'][0]['value']
            views = int(r['metricValues'][0]['value'])
            us = int(r['metricValues'][1]['value'])
            tot_sec = float(r['metricValues'][2]['value'])
            avg_sec = (tot_sec / us) if us > 0 else 0
            print(f"{path:<50} | {views:<6} | {us:<6} | {avg_sec:<12.1f}")

    # 5. Realtime Users (Last 30 mins)
    print("\n=== [5] Realtime Traffic (Last 30 Minutes) ===")
    res_rt = query_ga4(token, "runRealtimeReport", {
        "metrics": [{"name": "activeUsers"}]
    })
    if res_rt and res_rt.get('rows'):
        rt_users = res_rt['rows'][0]['metricValues'][0]['value']
        print(f"Current Realtime Active Users (Last 30 mins): {rt_users}")
    else:
        print("Current Realtime Active Users (Last 30 mins): 0")

if __name__ == '__main__':
    main()
