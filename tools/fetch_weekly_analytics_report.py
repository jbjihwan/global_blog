import json
import urllib.request
import urllib.parse
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

creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
req = google.auth.transport.requests.Request()
creds.refresh(req)
token = creds.token

def query_ga4(payload):
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{PROP_ID}:runReport"
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def query_gsc(payload):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/searchAnalytics/query"
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

# 1. Past 7 days (2026-10-28 to 2026-11-03) vs Previous 7 days (2026-10-21 to 2026-10-27)
print("=== [1] WEEK OVER WEEK SUMMARY ===")
res_cur = query_ga4({
    "dateRanges": [{"startDate": "2026-10-28", "endDate": "2026-11-03"}],
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

cur_u_total = sum(int(r['metricValues'][0]['value']) for r in res_cur.get('rows', []))
cur_s_total = sum(int(r['metricValues'][1]['value']) for r in res_cur.get('rows', []))
cur_pv_total = sum(int(r['metricValues'][2]['value']) for r in res_cur.get('rows', []))
cur_dur_total = sum(float(r['metricValues'][3]['value']) for r in res_cur.get('rows', []))

print("Current 7 Days (10/28 ~ 11/03) Daily:")
for r in res_cur.get('rows', []):
    d = r['dimensionValues'][0]['value']
    u = r['metricValues'][0]['value']
    s = r['metricValues'][1]['value']
    pv = r['metricValues'][2]['value']
    dur = float(r['metricValues'][3]['value'])
    eng = float(r['metricValues'][4]['value']) * 100
    print(f"  {d} | Users: {u:>2} | Sessions: {s:>2} | PV: {pv:>3} | Dur: {dur:>5.1f}s | Eng: {eng:>5.1f}%")

res_prev = query_ga4({
    "dateRanges": [{"startDate": "2026-10-21", "endDate": "2026-10-27"}],
    "metrics": [
        {"name": "activeUsers"},
        {"name": "sessions"},
        {"name": "screenPageViews"},
        {"name": "userEngagementDuration"}
    ]
})
prev_row = res_prev.get('rows', [{}])[0].get('metricValues', ['0', '0', '0', '0'])
prev_u = int(prev_row[0]['value'])
prev_s = int(prev_row[1]['value'])
prev_pv = int(prev_row[2]['value'])
prev_dur = float(prev_row[3]['value'])

print(f"\nWoW Total Comparison:")
print(f"  Previous 7 Days (10/21~10/27): Users={prev_u}, Sessions={prev_s}, PV={prev_pv}, Dur={prev_dur/60:.1f}m")
print(f"  Current 7 Days  (10/28~11/03): Users={cur_u_total}, Sessions={cur_s_total}, PV={cur_pv_total}, Dur={cur_dur_total/60:.1f}m")
diff_s = (cur_s_total - prev_s) / max(1, prev_s) * 100
diff_pv = (cur_pv_total - prev_pv) / max(1, prev_pv) * 100
print(f"  Rate of Change: Sessions={diff_s:+.1f}%, PageViews={diff_pv:+.1f}%")

# 2. Top Visited Pages
print("\n=== [2] TOP VISITED PAGES (10/28 ~ 11/03) ===")
res_pages = query_ga4({
    "dateRanges": [{"startDate": "2026-10-28", "endDate": "2026-11-03"}],
    "dimensions": [{"name": "pagePath"}, {"name": "pageTitle"}],
    "metrics": [
        {"name": "screenPageViews"},
        {"name": "activeUsers"},
        {"name": "userEngagementDuration"}
    ],
    "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
    "limit": 15
})
for r in res_pages.get('rows', []):
    path = r['dimensionValues'][0]['value']
    title = r['dimensionValues'][1]['value'][:40]
    pv = r['metricValues'][0]['value']
    u = r['metricValues'][1]['value']
    dur = float(r['metricValues'][2]['value'])
    print(f"  {path:<55} | PV: {pv:>3} | Users: {u:>2} | Dur: {dur:>5.1f}s | {title}")

# 3. Traffic Channels and Sources
print("\n=== [3] TRAFFIC CHANNELS & SOURCES (10/28 ~ 11/03) ===")
res_sources = query_ga4({
    "dateRanges": [{"startDate": "2026-10-28", "endDate": "2026-11-03"}],
    "dimensions": [{"name": "sessionDefaultChannelGroup"}, {"name": "sessionSourceMedium"}],
    "metrics": [
        {"name": "sessions"},
        {"name": "activeUsers"},
        {"name": "screenPageViews"},
        {"name": "engagementRate"}
    ],
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}]
})
for r in res_sources.get('rows', []):
    ch = r['dimensionValues'][0]['value']
    sm = r['dimensionValues'][1]['value']
    s = r['metricValues'][0]['value']
    u = r['metricValues'][1]['value']
    pv = r['metricValues'][2]['value']
    eng = float(r['metricValues'][3]['value']) * 100
    print(f"  {ch:<18} | {sm:<28} | Sessions: {s:>2} | Users: {u:>2} | PV: {pv:>3} | Eng: {eng:>5.1f}%")

# 4. Device and OS Breakdown
print("\n=== [4] DEVICES & OPERATING SYSTEMS ===")
res_devices = query_ga4({
    "dateRanges": [{"startDate": "2026-10-28", "endDate": "2026-11-03"}],
    "dimensions": [{"name": "deviceCategory"}, {"name": "operatingSystem"}],
    "metrics": [
        {"name": "activeUsers"},
        {"name": "sessions"},
        {"name": "screenPageViews"}
    ],
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}]
})
for r in res_devices.get('rows', []):
    dev = r['dimensionValues'][0]['value']
    os_name = r['dimensionValues'][1]['value']
    u = r['metricValues'][0]['value']
    s = r['metricValues'][1]['value']
    pv = r['metricValues'][2]['value']
    print(f"  {dev:<12} | {os_name:<15} | Users: {u:>2} | Sessions: {s:>2} | PV: {pv:>3}")

# 5. Countries
print("\n=== [5] GEOGRAPHIC DISTRIBUTION ===")
res_geo = query_ga4({
    "dateRanges": [{"startDate": "2026-10-28", "endDate": "2026-11-03"}],
    "dimensions": [{"name": "country"}, {"name": "city"}],
    "metrics": [
        {"name": "activeUsers"},
        {"name": "screenPageViews"}
    ],
    "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
    "limit": 10
})
for r in res_geo.get('rows', []):
    cntry = r['dimensionValues'][0]['value']
    city = r['dimensionValues'][1]['value']
    u = r['metricValues'][0]['value']
    pv = r['metricValues'][1]['value']
    print(f"  {cntry:<18} | {city:<20} | Users: {u:>2} | PV: {pv:>3}")

# 6. Google Search Console Analytics
print("\n=== [6] GOOGLE SEARCH CONSOLE PERFORMANCE ===")
res_gsc = query_gsc({
    "startDate": "2026-10-25",
    "endDate": "2026-11-02",
    "dimensions": ["query"],
    "rowLimit": 15
})
for r in res_gsc.get('rows', []):
    q = r['keys'][0]
    clk = r['clicks']
    imp = r['impressions']
    ctr = r['ctr'] * 100
    pos = r['position']
    print(f"  Query: {q:<40} | Clicks: {clk:>2} | Imp: {imp:>3} | CTR: {ctr:>5.1f}% | Pos: {pos:>4.1f}")

res_gsc_pages = query_gsc({
    "startDate": "2026-10-25",
    "endDate": "2026-11-02",
    "dimensions": ["page"],
    "rowLimit": 10
})
print("\n=== [7] GSC TOP SEARCH LANDING PAGES ===")
for r in res_gsc_pages.get('rows', []):
    pg = r['keys'][0]
    clk = r['clicks']
    imp = r['impressions']
    ctr = r['ctr'] * 100
    pos = r['position']
    print(f"  Page: {pg:<60} | Clicks: {clk:>2} | Imp: {imp:>3} | CTR: {ctr:>5.1f}% | Pos: {pos:>4.1f}")
