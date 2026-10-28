# -*- coding: utf-8 -*-
import sys
import io
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from google.oauth2 import service_account
import google.auth.transport.requests

# Ensure UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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

def query_gsc(token, payload):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(SITE_URL, safe='')}/searchAnalytics/query"
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
    print("=" * 80)
    print("📊 [글로벌 블로그] 지난 방문자 종합 심층 분석 리포트 (GA4 & GSC)")
    print(f"생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    token = get_token()

    # 1. Total KPI (Last 30 Days)
    print("\n" + "=" * 50)
    print("📌 [1] 최근 30일 핵심 성과 지표 (Total Overview)")
    print("=" * 50)
    res_kpi = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "newUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "userEngagementDuration"},
            {"name": "engagementRate"},
            {"name": "bounceRate"}
        ]
    })
    if res_kpi and res_kpi.get('rows'):
        mv = res_kpi['rows'][0]['metricValues']
        users = int(mv[0]['value'])
        new_users = int(mv[1]['value'])
        returning_users = max(0, users - new_users)
        sessions = int(mv[2]['value'])
        views = int(mv[3]['value'])
        dur = float(mv[4]['value'])
        eng_rate = float(mv[5]['value']) * 100
        bounce_rate = float(mv[6]['value']) * 100
        avg_dur_user = (dur / users) if users > 0 else 0
        avg_dur_session = (dur / sessions) if sessions > 0 else 0
        pages_per_session = (views / sessions) if sessions > 0 else 0

        print(f"• 총 활성 사용자 (Active Users):     {users:,} 명")
        print(f"  - 신규 방문자 (New Users):        {new_users:,} 명 ({new_users/users*100:.1f}%)" if users > 0 else "")
        print(f"  - 재방문자 (Returning Users):     {returning_users:,} 명 ({returning_users/users*100:.1f}%)" if users > 0 else "")
        print(f"• 총 세션 수 (Total Sessions):       {sessions:,} 회")
        print(f"• 총 페이지뷰 (Total Page Views):    {views:,} 회")
        print(f"• 세션당 평균 페이지뷰:              {pages_per_session:.2f} 페이지")
        print(f"• 참여율 (Engagement Rate):          {eng_rate:.1f}%")
        print(f"• 이탈률 (Bounce Rate):              {bounce_rate:.1f}%")
        print(f"• 사용자당 평균 체류 시간:           {avg_dur_user:.1f} 초 ({avg_dur_user/60:.1f} 분)")
        print(f"• 세션당 평균 체류 시간:             {avg_dur_session:.1f} 초")
        print(f"• 전체 누적 체류 시간:               {dur/60:.1f} 분 ({dur/3600:.2f} 시간)")

    # 2. Daily Trend (Last 14 Days)
    print("\n" + "=" * 50)
    print("📈 [2] 최근 14일 일별 방문자 및 페이지뷰 추이")
    print("=" * 50)
    res_daily = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "14daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "date"}],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "userEngagementDuration"}
        ],
        "orderBys": [{"dimension": {"dimensionName": "date"}, "desc": False}]
    })
    if res_daily and res_daily.get('rows'):
        print(f"{'날짜':<12} | {'방문자(명)':<10} | {'세션(회)':<8} | {'페이지뷰':<8} | {'평균 체류(초)':<12}")
        print("-" * 55)
        for r in res_daily['rows']:
            d_raw = r['dimensionValues'][0]['value']
            d_str = f"{d_raw[:4]}-{d_raw[4:6]}-{d_raw[6:]}"
            u = int(r['metricValues'][0]['value'])
            s = int(r['metricValues'][1]['value'])
            pv = int(r['metricValues'][2]['value'])
            dur = float(r['metricValues'][3]['value'])
            avg_t = (dur / u) if u > 0 else 0
            print(f"{d_str:<12} | {u:<10} | {s:<8} | {pv:<8} | {avg_t:<12.1f}")

    # 3. Traffic Acquisition Channels & Sources
    print("\n" + "=" * 50)
    print("🧭 [3] 유입 채널 및 소스/매체 (Traffic Acquisition)")
    print("=" * 50)
    res_channels = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}, {"name": "sessionSourceMedium"}],
        "metrics": [{"name": "sessions"}, {"name": "activeUsers"}, {"name": "screenPageViews"}, {"name": "engagementRate"}],
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        "limit": 15
    })
    if res_channels and res_channels.get('rows'):
        print(f"{'기본 채널':<18} | {'소스 / 매체':<30} | {'세션':<6} | {'사용자':<6} | {'PV':<6} | {'참여율'}")
        print("-" * 78)
        for r in res_channels['rows']:
            ch = r['dimensionValues'][0]['value']
            sm = r['dimensionValues'][1]['value']
            s = r['metricValues'][0]['value']
            u = r['metricValues'][1]['value']
            pv = r['metricValues'][2]['value']
            er = float(r['metricValues'][3]['value']) * 100
            print(f"{ch:<18} | {sm:<30} | {s:<6} | {u:<6} | {pv:<6} | {er:.1f}%")

    # 4. Referrers
    print("\n" + "=" * 50)
    print("🔗 [4] 세부 유입 참조 URL (Top Page Referrers)")
    print("=" * 50)
    res_refs = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "pageReferrer"}],
        "metrics": [{"name": "activeUsers"}, {"name": "screenPageViews"}],
        "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
        "limit": 15
    })
    if res_refs and res_refs.get('rows'):
        print(f"{'Referrer URL':<60} | {'Users':<6} | {'Page Views':<8}")
        print("-" * 78)
        for r in res_refs['rows']:
            ref = r['dimensionValues'][0]['value'] or "(direct / bookmark / none)"
            u = r['metricValues'][0]['value']
            pv = r['metricValues'][1]['value']
            print(f"{ref[:58]:<60} | {u:<6} | {pv:<8}")

    # 5. Top Visited Pages & Reading Duration
    print("\n" + "=" * 50)
    print("📄 [5] 방문자가 가장 많이 읽은 인기 페이지 및 체류 시간")
    print("=" * 50)
    res_pages = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "pagePath"}],
        "metrics": [
            {"name": "screenPageViews"},
            {"name": "activeUsers"},
            {"name": "userEngagementDuration"},
            {"name": "bounceRate"}
        ],
        "orderBys": [{"metric": {"metricName": "screenPageViews"}, "desc": True}],
        "limit": 20
    })
    if res_pages and res_pages.get('rows'):
        print(f"{'Page Path':<50} | {'PV':<6} | {'Users':<6} | {'평균체류':<10} | {'이탈률'}")
        print("-" * 80)
        for r in res_pages['rows']:
            path = r['dimensionValues'][0]['value']
            pv = int(r['metricValues'][0]['value'])
            u = int(r['metricValues'][1]['value'])
            dur = float(r['metricValues'][2]['value'])
            br = float(r['metricValues'][3]['value']) * 100
            avg_t = (dur / u) if u > 0 else 0
            time_str = f"{int(avg_t//60)}m {int(avg_t%60)}s" if avg_t >= 60 else f"{avg_t:.0f}s"
            print(f"{path[:48]:<50} | {pv:<6} | {u:<6} | {time_str:<10} | {br:.1f}%")

    # 6. Global Demographics (Country & Language)
    print("\n" + "=" * 50)
    print("🌍 [6] 방문자 국가 및 브라우저 언어 분포")
    print("=" * 50)
    res_geo = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "country"}, {"name": "language"}],
        "metrics": [{"name": "activeUsers"}, {"name": "screenPageViews"}, {"name": "userEngagementDuration"}],
        "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
        "limit": 15
    })
    if res_geo and res_geo.get('rows'):
        print(f"{'국가(Country)':<22} | {'언어(Language)':<16} | {'사용자':<6} | {'페이지뷰':<8} | {'평균체류'}")
        print("-" * 68)
        for r in res_geo['rows']:
            co = r['dimensionValues'][0]['value']
            la = r['dimensionValues'][1]['value']
            u = int(r['metricValues'][0]['value'])
            pv = int(r['metricValues'][1]['value'])
            dur = float(r['metricValues'][2]['value'])
            avg_t = (dur / u) if u > 0 else 0
            time_str = f"{int(avg_t//60)}m {int(avg_t%60)}s" if avg_t >= 60 else f"{avg_t:.0f}s"
            print(f"{co:<22} | {la:<16} | {u:<6} | {pv:<8} | {time_str}")

    # 7. Device & Platform Breakdown
    print("\n" + "=" * 50)
    print("💻 [7] 기기(Device) 및 운영체제(OS) 환경")
    print("=" * 50)
    res_device = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "deviceCategory"}, {"name": "operatingSystem"}, {"name": "browser"}],
        "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}],
        "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
        "limit": 10
    })
    if res_device and res_device.get('rows'):
        print(f"{'Device':<12} | {'OS':<14} | {'Browser':<14} | {'Users':<6} | {'Sessions':<8} | {'PV'}")
        print("-" * 66)
        for r in res_device['rows']:
            dev = r['dimensionValues'][0]['value']
            os = r['dimensionValues'][1]['value']
            br = r['dimensionValues'][2]['value']
            u = r['metricValues'][0]['value']
            s = r['metricValues'][1]['value']
            pv = r['metricValues'][2]['value']
            print(f"{dev:<12} | {os:<14} | {br:<14} | {u:<6} | {s:<8} | {pv}")

    # 8. Google Search Console (Organic Search Keywords)
    print("\n" + "=" * 50)
    print("🔍 [8] 구글 검색 콘솔 (GSC) 상위 검색어 및 클릭/노출 현황")
    print("=" * 50)
    today = datetime.now()
    end_date = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    start_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')
    res_gsc = query_gsc(token, {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": 25
    })
    rows = res_gsc.get('rows', []) if res_gsc else []
    if rows:
        print(f"{'검색 쿼리(Keyword)':<38} | {'클릭':<5} | {'노출(Imp)':<9} | {'CTR':<7} | {'평균 순위'}")
        print("-" * 72)
        for r in rows:
            q = r['keys'][0]
            c = r.get('clicks', 0)
            imp = r.get('impressions', 0)
            ctr = r.get('ctr', 0) * 100
            pos = r.get('position', 0)
            print(f"{q[:36]:<38} | {c:<5} | {imp:<9} | {ctr:<6.1f}% | {pos:.1f}위")
    else:
        print("GSC 등록 데이터 없음")

    # 9. GSC Landing Pages
    print("\n" + "=" * 50)
    print("🎯 [9] 구글 검색 콘솔 (GSC) 검색 랜딩 페이지 성과")
    print("=" * 50)
    res_gsc_pages = query_gsc(token, {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["page"],
        "rowLimit": 15
    })
    p_rows = res_gsc_pages.get('rows', []) if res_gsc_pages else []
    if p_rows:
        print(f"{'랜딩 페이지 URL':<52} | {'클릭':<5} | {'노출':<8} | {'CTR':<7} | {'평균순위'}")
        print("-" * 80)
        for r in p_rows:
            page = r['keys'][0].replace("https://globaldevlog.com", "")
            c = r.get('clicks', 0)
            imp = r.get('impressions', 0)
            ctr = r.get('ctr', 0) * 100
            pos = r.get('position', 0)
            print(f"{page[:50]:<52} | {c:<5} | {imp:<8} | {ctr:<6.1f}% | {pos:.1f}위")

    print("\n" + "=" * 80)
    print("✅ 방문자 심층 조사 완료")
    print("=" * 80)

if __name__ == '__main__':
    main()
