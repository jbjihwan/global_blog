# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error
import sys
from datetime import datetime
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
    print("=" * 70)
    print(f"📊 [GA4] 오늘 (Today, {datetime.now().strftime('%Y-%m-%d')}) 및 최근 트래픽 심층 분석 리포트")
    print("=" * 70)

    # 1. Realtime (Last 30 mins)
    print("\n[1] 실시간 현황 (Realtime, 최근 30분)")
    res_rt = query_ga4(token, "runRealtimeReport", {
        "metrics": [{"name": "activeUsers"}, {"name": "screenPageViews"}, {"name": "eventCount"}],
        "dimensions": [{"name": "country"}, {"name": "deviceCategory"}]
    })
    if res_rt and res_rt.get('rows'):
        print(f"{'Country':<20} | {'Device':<15} | {'Active Users':<12} | {'Views':<6}")
        print("-" * 60)
        for r in res_rt['rows']:
            co = r['dimensionValues'][0]['value']
            dev = r['dimensionValues'][1]['value']
            users = r['metricValues'][0]['value']
            views = r['metricValues'][1]['value']
            print(f"{co:<20} | {dev:<15} | {users:<12} | {views:<6}")
    else:
        # Check total active users in realtime
        res_rt_tot = query_ga4(token, "runRealtimeReport", {"metrics": [{"name": "activeUsers"}]})
        tot_rt = res_rt_tot['rows'][0]['metricValues'][0]['value'] if res_rt_tot and res_rt_tot.get('rows') else "0"
        print(f"현재 실시간 활성 사용자 (최근 30분): {tot_rt}명")

    # 2. Today's KPIs
    print("\n[2] 오늘 (Today) 핵심 지표 (자정 ~ 현재)")
    res_today = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
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
    if res_today and res_today.get('rows'):
        mv = res_today['rows'][0]['metricValues']
        users = int(mv[0]['value'])
        new_users = int(mv[1]['value'])
        sessions = int(mv[2]['value'])
        views = int(mv[3]['value'])
        dur = float(mv[4]['value'])
        eng_rate = float(mv[5]['value']) * 100
        bounce_rate = float(mv[6]['value']) * 100 if len(mv) > 6 else 0.0
        avg_dur = (dur / users) if users > 0 else 0
        print(f"• 활성 사용자(Active Users): {users}명 (신규: {new_users}명)")
        print(f"• 총 세션 수(Sessions):       {sessions}회")
        print(f"• 페이지뷰(Page Views):       {views}회")
        print(f"• 참여율(Engagement Rate):   {eng_rate:.1f}% (이탈률: {bounce_rate:.1f}%)")
        print(f"• 1인당 평균 체류 시간:      {avg_dur:.1f}초")
        print(f"• 총 체류 시간:              {dur / 60:.1f}분 ({dur:.0f}초)")
    else:
        print("오늘 기록된 표준 리포트 데이터가 아직 집계 대기 중이거나 0건입니다.")

    # 3. Yesterday's KPIs (for comparison)
    print("\n[3] 어제 (Yesterday) 지표 비교")
    res_yest = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "yesterday", "endDate": "yesterday"}],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"},
            {"name": "userEngagementDuration"}
        ]
    })
    if res_yest and res_yest.get('rows'):
        mv = res_yest['rows'][0]['metricValues']
        y_users = int(mv[0]['value'])
        y_sess = int(mv[1]['value'])
        y_views = int(mv[2]['value'])
        y_dur = float(mv[3]['value'])
        print(f"• 어제 사용자: {y_users}명 | 세션: {y_sess}회 | 뷰: {y_views}회 | 체류: {y_dur/60:.1f}분")

    # 4. Hourly breakdown for today
    print("\n[4] 오늘 시간대별(Hour) 트래픽 추이")
    res_hour = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [{"name": "hour"}],
        "metrics": [{"name": "activeUsers"}, {"name": "screenPageViews"}, {"name": "sessions"}],
        "orderBys": [{"dimension": {"dimensionName": "hour"}}]
    })
    if res_hour and res_hour.get('rows'):
        print(f"{'Hour':<6} | {'Users':<6} | {'Views':<6} | {'Sessions':<8}")
        print("-" * 35)
        for r in res_hour['rows']:
            h = r['dimensionValues'][0]['value']
            u = r['metricValues'][0]['value']
            v = r['metricValues'][1]['value']
            s = r['metricValues'][2]['value']
            print(f"{h:0>2}시    | {u:<6} | {v:<6} | {s:<8}")
    else:
        print("시간대별 세부 데이터 없음")

    # 5. Pages viewed today
    print("\n[5] 오늘 방문된 페이지 (Top Pages Today)")
    res_today_pages = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [{"name": "pagePath"}, {"name": "pageTitle"}],
        "metrics": [{"name": "screenPageViews"}, {"name": "activeUsers"}, {"name": "userEngagementDuration"}],
        "limit": 15
    })
    if res_today_pages and res_today_pages.get('rows'):
        print(f"{'Page Path':<45} | {'Views':<6} | {'Users':<6} | {'Avg Time':<10}")
        print("-" * 75)
        for r in res_today_pages['rows']:
            p = r['dimensionValues'][0]['value']
            v = int(r['metricValues'][0]['value'])
            u = int(r['metricValues'][1]['value'])
            dur = float(r['metricValues'][2]['value'])
            avg_t = (dur / u) if u > 0 else 0
            print(f"{p:<45} | {v:<6} | {u:<6} | {avg_t:<10.1f}s")
    else:
        print("오늘 페이지뷰 데이터 집계 대기 중")

    # 6. Channels and Sources Today
    print("\n[6] 유입 채널 및 소스 (Today Acquisition)")
    res_src = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}, {"name": "sessionSourceMedium"}],
        "metrics": [{"name": "sessions"}, {"name": "activeUsers"}],
        "limit": 10
    })
    if res_src and res_src.get('rows'):
        print(f"{'Channel':<20} | {'Source / Medium':<25} | {'Sessions':<8} | {'Users':<6}")
        print("-" * 65)
        for r in res_src['rows']:
            ch = r['dimensionValues'][0]['value']
            sm = r['dimensionValues'][1]['value']
            s = r['metricValues'][0]['value']
            u = r['metricValues'][1]['value']
            print(f"{ch:<20} | {sm:<25} | {s:<8} | {u:<6}")

    # 7. Countries Today
    print("\n[7] 방문 국가 및 언어 (Today Demographics)")
    res_geo = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [{"name": "country"}, {"name": "city"}, {"name": "language"}],
        "metrics": [{"name": "activeUsers"}, {"name": "screenPageViews"}],
        "limit": 10
    })
    if res_geo and res_geo.get('rows'):
        print(f"{'Country':<18} | {'City':<15} | {'Language':<12} | {'Users':<6} | {'Views':<6}")
        print("-" * 65)
        for r in res_geo['rows']:
            co = r['dimensionValues'][0]['value']
            ci = r['dimensionValues'][1]['value']
            la = r['dimensionValues'][2]['value']
            u = r['metricValues'][0]['value']
            v = r['metricValues'][1]['value']
            print(f"{co:<18} | {ci:<15} | {la:<12} | {u:<6} | {v:<6}")

    # 8. Daily Trend for Past 7 Days
    print("\n[8] 최근 7일간 일별 트래픽 추이 (Daily Trend)")
    res_7d = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "date"}],
        "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}],
        "orderBys": [{"dimension": {"dimensionName": "date"}}]
    })
    if res_7d and res_7d.get('rows'):
        print(f"{'Date':<10} | {'Users':<6} | {'Sessions':<8} | {'Page Views':<10}")
        print("-" * 40)
        for r in res_7d['rows']:
            d = r['dimensionValues'][0]['value']
            d_formatted = f"{d[:4]}-{d[4:6]}-{d[6:]}"
            u = r['metricValues'][0]['value']
            s = r['metricValues'][1]['value']
            v = r['metricValues'][2]['value']
            print(f"{d_formatted:<10} | {u:<6} | {s:<8} | {v:<10}")

if __name__ == '__main__':
    main()
