import json
import urllib.request
import urllib.parse
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

# Check previous week (10/21 ~ 10/27) vs current week (10/28 ~ 11/03) for pagePath prefixes
prev_pages = query_ga4({
    "dateRanges": [{"startDate": "2026-10-21", "endDate": "2026-10-27"}],
    "dimensions": [{"name": "pagePath"}],
    "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}, {"name": "userEngagementDuration"}],
    "limit": 100
})

cur_pages = query_ga4({
    "dateRanges": [{"startDate": "2026-10-28", "endDate": "2026-11-03"}],
    "dimensions": [{"name": "pagePath"}],
    "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}, {"name": "userEngagementDuration"}],
    "limit": 100
})

def categorize_path(p):
    for loc in ['/de/', '/fr/', '/pt-BR/', '/es/', '/ja/', '/zh-Hans/', '/zh-Hant/']:
        if p.startswith(loc):
            return "pruned_locales"
    if p.startswith('/ko/'):
        return "korean"
    return "english_root"

prev_cat = {"pruned_locales": 0, "korean": 0, "english_root": 0}
for r in prev_pages.get('rows', []):
    p = r['dimensionValues'][0]['value']
    pv = int(r['metricValues'][0]['value'])
    cat = categorize_path(p)
    prev_cat[cat] += pv

cur_cat = {"pruned_locales": 0, "korean": 0, "english_root": 0}
for r in cur_pages.get('rows', []):
    p = r['dimensionValues'][0]['value']
    pv = int(r['metricValues'][0]['value'])
    cat = categorize_path(p)
    cur_cat[cat] += pv

print("=== CATEGORY BREAKDOWN OF PAGEVIEWS ===")
print("Previous Week (10/21 ~ 10/27):", prev_cat)
print("Current Week  (10/28 ~ 11/03):", cur_cat)

# Engagement rate and bounce rate previous week
prev_summary = query_ga4({
    "dateRanges": [{"startDate": "2026-10-21", "endDate": "2026-10-27"}],
    "metrics": [
        {"name": "activeUsers"},
        {"name": "sessions"},
        {"name": "screenPageViews"},
        {"name": "engagementRate"},
        {"name": "bounceRate"},
        {"name": "averageSessionDuration"}
    ]
})
print("\n=== PREVIOUS WEEK OVERALL METRICS ===")
row = prev_summary['rows'][0]['metricValues']
print(f"Users: {row[0]['value']}, Sessions: {row[1]['value']}, PV: {row[2]['value']}, EngRate: {float(row[3]['value'])*100:.2f}%, BounceRate: {float(row[4]['value'])*100:.2f}%, AvgSessionDur: {float(row[5]['value']):.1f}s")

# Current week summary
cur_summary = query_ga4({
    "dateRanges": [{"startDate": "2026-10-28", "endDate": "2026-11-03"}],
    "metrics": [
        {"name": "activeUsers"},
        {"name": "sessions"},
        {"name": "screenPageViews"},
        {"name": "engagementRate"},
        {"name": "bounceRate"},
        {"name": "averageSessionDuration"}
    ]
})
print("\n=== CURRENT WEEK OVERALL METRICS ===")
row2 = cur_summary['rows'][0]['metricValues']
print(f"Users: {row2[0]['value']}, Sessions: {row2[1]['value']}, PV: {row2[2]['value']}, EngRate: {float(row2[3]['value'])*100:.2f}%, BounceRate: {float(row2[4]['value'])*100:.2f}%, AvgSessionDur: {float(row2[5]['value']):.1f}s")

# Check country breakdown previous vs current
prev_geo = query_ga4({
    "dateRanges": [{"startDate": "2026-10-21", "endDate": "2026-10-27"}],
    "dimensions": [{"name": "country"}],
    "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}],
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
    "limit": 10
})
print("\n=== PREVIOUS WEEK GEO BREAKDOWN ===")
for r in prev_geo.get('rows', []):
    c = r['dimensionValues'][0]['value']
    u = r['metricValues'][0]['value']
    s = r['metricValues'][1]['value']
    pv = r['metricValues'][2]['value']
    print(f"  {c:<20} | Users: {u:>2} | Sessions: {s:>2} | PV: {pv:>3}")
