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

def query_gsc(payload):
    encoded_site = urllib.parse.quote(SITE_URL, safe="")
    url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"
    data_bytes = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

# 1. Event telemetry
events = query_ga4({
    "dateRanges": [{"startDate": "2026-10-28", "endDate": "2026-11-03"}],
    "dimensions": [{"name": "eventName"}],
    "metrics": [{"name": "eventCount"}, {"name": "totalUsers"}],
    "orderBys": [{"metric": {"metricName": "eventCount"}, "desc": True}]
})
print("=== GA4 EVENT TELEMETRY ===")
for r in events.get('rows', []):
    ev = r['dimensionValues'][0]['value']
    cnt = r['metricValues'][0]['value']
    u = r['metricValues'][1]['value']
    print(f"  {ev:<25} | Count: {cnt:>4} | Users: {u:>2}")

# 2. New vs Returning
user_types = query_ga4({
    "dateRanges": [{"startDate": "2026-10-28", "endDate": "2026-11-03"}],
    "dimensions": [{"name": "newVsReturning"}],
    "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}, {"name": "engagementRate"}],
})
print("\n=== NEW VS RETURNING USERS ===")
for r in user_types.get('rows', []):
    t = r['dimensionValues'][0]['value']
    u = r['metricValues'][0]['value']
    s = r['metricValues'][1]['value']
    pv = r['metricValues'][2]['value']
    eng = float(r['metricValues'][3]['value']) * 100
    print(f"  {t:<15} | Users: {u:>2} | Sessions: {s:>2} | PV: {pv:>3} | EngRate: {eng:>5.1f}%")

# 3. GSC full dates breakdown
gsc_dates = query_gsc({
    "startDate": "2026-10-20",
    "endDate": "2026-11-02",
    "dimensions": ["date"],
    "rowLimit": 20
})
print("\n=== GSC DAILY PERFORMANCE ===")
for r in gsc_dates.get('rows', []):
    dt = r['keys'][0]
    clk = r['clicks']
    imp = r['impressions']
    ctr = r['ctr'] * 100
    pos = r['position']
    print(f"  {dt} | Clicks: {clk:>2} | Imp: {imp:>3} | CTR: {ctr:>5.1f}% | Pos: {pos:>4.1f}")

# 4. Hourly distribution
hourly = query_ga4({
    "dateRanges": [{"startDate": "2026-10-28", "endDate": "2026-11-03"}],
    "dimensions": [{"name": "hour"}],
    "metrics": [{"name": "sessions"}, {"name": "screenPageViews"}],
    "orderBys": [{"dimension": {"dimensionName": "hour"}, "desc": False}]
})
print("\n=== HOURLY DISTRIBUTION (UTC) ===")
for r in hourly.get('rows', []):
    hr = r['dimensionValues'][0]['value']
    s = r['metricValues'][0]['value']
    pv = r['metricValues'][1]['value']
    print(f"  Hour {hr:0>2}:00 | Sessions: {s:>2} | PV: {pv:>3}")
