import json
import urllib.request
from datetime import datetime
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_FILE = r"D:\ai\antigravity\global_blog\credentials\service_account.json"
PROP_ID = "558130708"
SITE_URL = "sc-domain:globaldevlog.com"

SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',
    'https://www.googleapis.com/auth/webmasters.readonly'
]

def get_token():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
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

def query_gsc(token, payload):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/searchAnalytics/query"
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

token = get_token()

# 1. This week daily (2026-10-26 to 2026-10-29)
res_daily = query_ga4(token, {
    "dateRanges": [{"startDate": "2026-10-26", "endDate": "2026-10-29"}],
    "dimensions": [{"name": "date"}],
    "metrics": [
        {"name": "activeUsers"},
        {"name": "sessions"},
        {"name": "screenPageViews"},
        {"name": "userEngagementDuration"},
        {"name": "engagementRate"},
        {"name": "bounceRate"}
    ],
    "orderBys": [{"dimension": {"dimensionName": "date"}, "desc": False}]
})

print("=== [1] THIS WEEK DAILY BREAKDOWN (2026-10-26 Mon ~ 2026-10-29 Thu) ===")
total_u = 0
total_s = 0
total_pv = 0
total_dur = 0
for row in res_daily.get('rows', []):
    d = row['dimensionValues'][0]['value']
    u = int(row['metricValues'][0]['value'])
    s = int(row['metricValues'][1]['value'])
    pv = int(row['metricValues'][2]['value'])
    dur = float(row['metricValues'][3]['value'])
    eng = float(row['metricValues'][4]['value']) * 100
    bounce = float(row['metricValues'][5]['value']) * 100
    avg_t = dur / max(1, u)
    total_u += u
    total_s += s
    total_pv += pv
    total_dur += dur
    print(f"{d} | Users: {u:>2} | Sessions: {s:>2} | PV: {pv:>3} | AvgTime: {avg_t:>4.1f}s | EngRate: {eng:>5.1f}% | Bounce: {bounce:>5.1f}%")

print(f"-> This Week Total: Sessions={total_s}, PV={total_pv}, TotalDur={total_dur/60:.1f}min")

# 2. Previous week same period (2026-10-19 Mon ~ 2026-10-22 Thu)
res_prev = query_ga4(token, {
    "dateRanges": [{"startDate": "2026-10-19", "endDate": "2026-10-22"}],
    "dimensions": [{"name": "date"}],
    "metrics": [
        {"name": "activeUsers"},
        {"name": "sessions"},
        {"name": "screenPageViews"},
        {"name": "userEngagementDuration"}
    ]
})
prev_s = sum(int(r['metricValues'][1]['value']) for r in res_prev.get('rows', []))
prev_pv = sum(int(r['metricValues'][2]['value']) for r in res_prev.get('rows', []))
print(f"\n=== [2] COMPARISON WITH LAST WEEK SAME PERIOD (10/19~10/22 vs 10/26~10/29) ===")
print(f"Last Week: Sessions={prev_s}, PV={prev_pv}")
print(f"This Week: Sessions={total_s}, PV={total_pv}")
print(f"Change: Sessions {(total_s - prev_s)/max(1, prev_s)*100:+.1f}%, PV {(total_pv - prev_pv)/max(1, prev_pv)*100:+.1f}%")

# 3. Pages this week
res_pages = query_ga4(token, {
    "dateRanges": [{"startDate": "2026-10-26", "endDate": "2026-10-29"}],
    "dimensions": [{"name": "pagePath"}],
    "metrics": [
        {"name": "screenPageViews"},
        {"name": "activeUsers"},
        {"name": "userEngagementDuration"}
    ],
    "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
    "limit": 20
})
print("\n=== [3] TOP PAGES VISITED THIS WEEK ===")
for r in res_pages.get('rows', []):
    p = r['dimensionValues'][0]['value']
    pv = r['metricValues'][0]['value']
    u = r['metricValues'][1]['value']
    dur = float(r['metricValues'][2]['value'])
    avg_t = dur / max(1, int(u))
    print(f"{p:<55} | PV: {pv:>3} | Users: {u:>2} | AvgTime: {avg_t:>4.1f}s")

# 4. Channels this week
res_ch = query_ga4(token, {
    "dateRanges": [{"startDate": "2026-10-26", "endDate": "2026-10-29"}],
    "dimensions": [{"name": "sessionDefaultChannelGroup"}, {"name": "sessionSourceMedium"}],
    "metrics": [
        {"name": "sessions"},
        {"name": "activeUsers"},
        {"name": "screenPageViews"}
    ],
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}]
})
print("\n=== [4] ACQUISITION CHANNELS THIS WEEK ===")
for r in res_ch.get('rows', []):
    ch = r['dimensionValues'][0]['value']
    sm = r['dimensionValues'][1]['value']
    s = r['metricValues'][0]['value']
    u = r['metricValues'][1]['value']
    pv = r['metricValues'][2]['value']
    print(f"{ch:<15} | {sm:<25} | Sessions: {s:>2} | Users: {u:>2} | PV: {pv:>3}")

# 5. Countries this week
res_geo = query_ga4(token, {
    "dateRanges": [{"startDate": "2026-10-26", "endDate": "2026-10-29"}],
    "dimensions": [{"name": "country"}],
    "metrics": [
        {"name": "activeUsers"},
        {"name": "screenPageViews"}
    ],
    "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
    "limit": 10
})
print("\n=== [5] TOP COUNTRIES THIS WEEK ===")
for r in res_geo.get('rows', []):
    c = r['dimensionValues'][0]['value']
    u = r['metricValues'][0]['value']
    pv = r['metricValues'][1]['value']
    print(f"{c:<20} | Users: {u:>2} | PV: {pv:>3}")

# 6. GSC query
import urllib.parse
res_gsc = query_gsc(token, {
    "startDate": "2026-10-20",
    "endDate": "2026-10-28",
    "dimensions": ["query"],
    "rowLimit": 20
})
print("\n=== [6] TOP SEARCH CONSOLE QUERIES (RECENT) ===")
for r in res_gsc.get('rows', []):
    q = r['keys'][0]
    clk = r['clicks']
    imp = r['impressions']
    ctr = r['ctr'] * 100
    pos = r['position']
    print(f"{q:<45} | Clicks: {clk:>2} | Imp: {imp:>3} | CTR: {ctr:>4.1f}% | Pos: {pos:>4.1f}")
