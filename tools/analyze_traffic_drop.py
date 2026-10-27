# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',
    'https://www.googleapis.com/auth/webmasters.readonly'
]
PROP_ID = "558130708"
SITE_URL = "sc-domain:globaldevlog.com"

def get_token(scopes):
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=scopes)
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
        print(f"GA4 Error {e.code}: {e.read().decode('utf-8')}")
        return None

def query_gsc(token, start_date, end_date, dimensions=['date']):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/searchAnalytics/query"
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "rowLimit": 100
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
        print(f"GSC Error {e.code}: {e.read().decode('utf-8')}")
        return None

def main():
    print("=" * 70)
    print("GA4 & Search Console Traffic Drop Diagnostic Analysis")
    print("=" * 70)
    
    ga_token = get_token(['https://www.googleapis.com/auth/analytics.readonly'])
    
    # 1. Day-by-Day Traffic for Last 28 Days
    print("\n[1] Daily Traffic Trend (Last 28 Days to Today)")
    res_daily = query_ga4(ga_token, "runReport", {
        "dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "date"}],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "engagementRate"},
            {"name": "userEngagementDuration"}
        ],
        "orderBys": [{"dimension": {"dimensionName": "date"}}]
    })
    
    daily_records = []
    if res_daily and res_daily.get('rows'):
        print(f"{'Date':<12} | {'Active Users':<12} | {'Sessions':<10} | {'Pageviews':<10} | {'Eng Rate':<10} | {'Avg Time':<10}")
        print("-" * 72)
        for r in res_daily['rows']:
            d_raw = r['dimensionValues'][0]['value']
            date_str = f"{d_raw[:4]}-{d_raw[4:6]}-{d_raw[6:]}"
            users = int(r['metricValues'][0]['value'])
            sess = int(r['metricValues'][1]['value'])
            pvs = int(r['metricValues'][2]['value'])
            eng = float(r['metricValues'][3]['value']) * 100
            dur = float(r['metricValues'][4]['value'])
            avg_t = dur / users if users > 0 else 0
            daily_records.append({"date": date_str, "users": users, "sessions": sess, "views": pvs})
            print(f"{date_str:<12} | {users:<12} | {sess:<10} | {pvs:<10} | {eng:<9.1f}% | {avg_t:<8.1f}s")
            
    # 2. Compare Last Week (e.g. 14~8 days ago) vs This Week (7~1 days ago)
    print("\n[2] Week-over-Week Comparison (7 Days Ago vs Previous 7 Days)")
    res_wow = query_ga4(ga_token, "runReport", {
        "dateRanges": [
            {"name": "This Week (Past 7d)", "startDate": "7daysAgo", "endDate": "yesterday"},
            {"name": "Last Week (8-14d Ago)", "startDate": "14daysAgo", "endDate": "8daysAgo"}
        ],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "userEngagementDuration"}
        ]
    })
    if res_wow and res_wow.get('rows'):
        print(json.dumps(res_wow, indent=2))
        
    # 3. Channel breakdown for This Week vs Last Week
    print("\n[3] Inflow Channels Comparison (Last 7 Days vs Prior 7 Days)")
    for period_name, start_d, end_d in [("Last Week (8-14d)", "14daysAgo", "8daysAgo"), ("This Week (1-7d)", "7daysAgo", "yesterday")]:
        print(f"\n--- {period_name} ({start_d} ~ {end_d}) ---")
        res_ch = query_ga4(ga_token, "runReport", {
            "dateRanges": [{"startDate": start_d, "endDate": end_d}],
            "dimensions": [{"name": "sessionDefaultChannelGroup"}, {"name": "sessionSourceMedium"}],
            "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}],
            "limit": 10
        })
        if res_ch and res_ch.get('rows'):
            print(f"{'Channel':<18} | {'Source / Medium':<25} | {'Users':<6} | {'Sessions':<8} | {'Pageviews':<10}")
            print("-" * 72)
            for r in res_ch['rows']:
                ch = r['dimensionValues'][0]['value']
                sm = r['dimensionValues'][1]['value']
                u = r['metricValues'][0]['value']
                s = r['metricValues'][1]['value']
                p = r['metricValues'][2]['value']
                print(f"{ch:<18} | {sm:<25} | {u:<6} | {s:<8} | {p:<10}")

    # 4. Top Landing Pages Comparison
    print("\n[4] Top Landing Pages: Last Week vs This Week")
    for period_name, start_d, end_d in [("Last Week (8-14d)", "14daysAgo", "8daysAgo"), ("This Week (1-7d)", "7daysAgo", "yesterday")]:
        print(f"\n--- {period_name} ---")
        res_lp = query_ga4(ga_token, "runReport", {
            "dateRanges": [{"startDate": start_d, "endDate": end_d}],
            "dimensions": [{"name": "pagePath"}],
            "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}],
            "limit": 10
        })
        if res_lp and res_lp.get('rows'):
            print(f"{'Page Path':<50} | {'Views':<8} | {'Users':<6}")
            print("-" * 68)
            for r in res_lp['rows']:
                path = r['dimensionValues'][0]['value']
                v = r['metricValues'][0]['value']
                u = r['metricValues'][1]['value']
                print(f"{path:<50} | {v:<8} | {u:<6}")

    # 5. Search Console Trend
    print("\n[5] Google Search Console Weekly Trend")
    try:
        gsc_token = get_token(['https://www.googleapis.com/auth/webmasters.readonly'])
        today = datetime.now()
        end_d = (today - timedelta(days=2)).strftime('%Y-%m-%d')
        start_d = (today - timedelta(days=28)).strftime('%Y-%m-%d')
        gsc_res = query_gsc(gsc_token, start_d, end_d, dimensions=['date'])
        if gsc_res and gsc_res.get('rows'):
            print(f"{'Date':<12} | {'Clicks':<8} | {'Impressions':<12} | {'CTR':<8} | {'Position':<8}")
            print("-" * 55)
            for r in gsc_res['rows']:
                dt = r['keys'][0]
                cl = r.get('clicks', 0)
                imp = r.get('impressions', 0)
                ctr = f"{r.get('ctr', 0)*100:.1f}%"
                pos = f"{r.get('position', 0):.1f}"
                print(f"{dt:<12} | {cl:<8} | {imp:<12} | {ctr:<8} | {pos:<8}")
        else:
            print("No GSC daily data returned.")
    except Exception as e:
        print(f"GSC query failed: {e}")

if __name__ == '__main__':
    main()
