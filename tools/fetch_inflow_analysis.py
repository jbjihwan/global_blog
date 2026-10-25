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
    today_str = datetime.now().strftime('%Y-%m-%d')
    print("=" * 80)
    print(f"🚀 [GA4 심층 유입 분석] 오늘({today_str}) 실시간 및 당일 방문자 유입 경로 리포트")
    print("=" * 80)

    # 1. Realtime Users (Last 30 mins)
    print("\n[1] 실시간 활성 사용자 현황 (최근 30분)")
    res_rt = query_ga4(token, "runRealtimeReport", {
        "metrics": [{"name": "activeUsers"}, {"name": "screenPageViews"}],
        "dimensions": [{"name": "country"}, {"name": "city"}, {"name": "unifiedScreenName"}]
    })
    if res_rt and res_rt.get('rows'):
        print(f"{'Country':<18} | {'City':<15} | {'Active Page':<35} | {'Users':<6} | {'Views':<6}")
        print("-" * 85)
        for r in res_rt['rows']:
            co = r['dimensionValues'][0]['value']
            ci = r['dimensionValues'][1]['value']
            page = r['dimensionValues'][2]['value']
            u = r['metricValues'][0]['value']
            v = r['metricValues'][1]['value']
            print(f"{co:<18} | {ci:<15} | {page[:33]:<35} | {u:<6} | {v:<6}")
    else:
        print("현재 실시간 접속자: 0명 (최근 30분 기준)")

    # 2. Today's Overview (2026-10-25 00:00 ~ 현재)
    print(f"\n[2] 오늘 당일 전체 유입 개요 ({today_str} 00:00 ~ 현재)")
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
        print(f"• 오늘 활성 사용자: {users}명 (신규 방문자: {new_users}명, 재방문: {users - new_users}명)")
        print(f"• 오늘 총 세션 수:   {sessions}회 (사용자당 평균 {sessions/users:.2f}회)" if users > 0 else "")
        print(f"• 오늘 총 페이지뷰: {views}회 (세션당 {views/sessions:.2f}페이지)" if sessions > 0 else "")
        print(f"• 세션 참여율:       {eng_rate:.1f}% (이탈률: {bounce_rate:.1f}%)")
        print(f"• 사용자당 평균 체류 시간: {avg_dur:.1f}초 (총 {dur/60:.1f}분)")
    else:
        print("오늘(자정 이후) 표준 리포트 집계 건수가 아직 0건이거나 처리 중입니다.")

    # 3. Inflow Source & Medium Today
    print("\n[3] 오늘 유입 채널 및 소스/매체 (Traffic Sources & Channels)")
    res_src = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [
            {"name": "sessionDefaultChannelGroup"},
            {"name": "sessionSourceMedium"}
        ],
        "metrics": [
            {"name": "sessions"},
            {"name": "activeUsers"},
            {"name": "screenPageViews"},
            {"name": "engagementRate"},
            {"name": "userEngagementDuration"}
        ],
        "limit": 15
    })
    if res_src and res_src.get('rows'):
        print(f"{'채널 그룹':<18} | {'소스 / 매체':<28} | {'세션':<5} | {'사용자':<5} | {'뷰':<5} | {'참여율':<7} | {'평균체류':<8}")
        print("-" * 85)
        for r in res_src['rows']:
            ch = r['dimensionValues'][0]['value']
            sm = r['dimensionValues'][1]['value']
            sess = int(r['metricValues'][0]['value'])
            us = int(r['metricValues'][1]['value'])
            pv = int(r['metricValues'][2]['value'])
            eng = float(r['metricValues'][3]['value']) * 100
            dur = float(r['metricValues'][4]['value'])
            avg_t = (dur / us) if us > 0 else 0
            print(f"{ch:<18} | {sm:<28} | {sess:<5} | {us:<5} | {pv:<5} | {eng:<6.1f}% | {avg_t:<7.1f}s")
    else:
        print("유입 채널 데이터 집계 대기 중")

    # 4. Referrer URLs Today
    print("\n[4] 오늘 실제 참조 URL (Page Referrer / 유입 링크)")
    res_ref = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [{"name": "pageReferrer"}],
        "metrics": [{"name": "sessions"}, {"name": "activeUsers"}],
        "limit": 10
    })
    if res_ref and res_ref.get('rows'):
        print(f"{'참조 URL (Referrer)':<60} | {'세션':<6} | {'사용자':<6}")
        print("-" * 75)
        for r in res_ref['rows']:
            ref = r['dimensionValues'][0]['value']
            s = r['metricValues'][0]['value']
            u = r['metricValues'][1]['value']
            print(f"{ref[:58]:<60} | {s:<6} | {u:<6}")
    else:
        print("참조 URL 데이터 없음")

    # 5. Landing Pages (첫 진입 페이지)
    print("\n[5] 오늘 첫 진입 랜딩 페이지 (Landing Pages)")
    res_land = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [{"name": "landingPagePlusQueryString"}],
        "metrics": [
            {"name": "sessions"},
            {"name": "activeUsers"},
            {"name": "screenPageViews"},
            {"name": "bounceRate"}
        ],
        "limit": 15
    })
    if res_land and res_land.get('rows'):
        print(f"{'랜딩 페이지 URL':<50} | {'세션':<6} | {'사용자':<6} | {'뷰':<6} | {'이탈률':<7}")
        print("-" * 80)
        for r in res_land['rows']:
            lp = r['dimensionValues'][0]['value']
            s = int(r['metricValues'][0]['value'])
            u = int(r['metricValues'][1]['value'])
            v = int(r['metricValues'][2]['value'])
            br = float(r['metricValues'][3]['value']) * 100
            print(f"{lp[:48]:<50} | {s:<6} | {u:<6} | {v:<6} | {br:<6.1f}%")
    else:
        print("랜딩 페이지 데이터 집계 대기 중")

    # 6. Geographic Breakdown Today
    print("\n[6] 오늘 유입 국가 및 도시 (Geographic Demographics)")
    res_geo = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [{"name": "country"}, {"name": "city"}, {"name": "language"}],
        "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}],
        "limit": 15
    })
    if res_geo and res_geo.get('rows'):
        print(f"{'국가':<18} | {'도시':<18} | {'브라우저 언어':<15} | {'사용자':<5} | {'세션':<5} | {'뷰':<5}")
        print("-" * 75)
        for r in res_geo['rows']:
            co = r['dimensionValues'][0]['value']
            ci = r['dimensionValues'][1]['value']
            la = r['dimensionValues'][2]['value']
            u = r['metricValues'][0]['value']
            s = r['metricValues'][1]['value']
            v = r['metricValues'][2]['value']
            print(f"{co:<18} | {ci:<18} | {la:<15} | {u:<5} | {s:<5} | {v:<5}")
    else:
        print("지역 데이터 집계 대기 중")

    # 7. Device & OS Breakdown Today
    print("\n[7] 오늘 유입 디바이스 및 환경 (Device & Tech)")
    res_dev = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [{"name": "deviceCategory"}, {"name": "operatingSystem"}, {"name": "browser"}],
        "metrics": [{"name": "activeUsers"}, {"name": "sessions"}],
        "limit": 10
    })
    if res_dev and res_dev.get('rows'):
        print(f"{'디바이스':<12} | {'OS':<15} | {'브라우저':<15} | {'사용자':<6} | {'세션':<6}")
        print("-" * 60)
        for r in res_dev['rows']:
            cat = r['dimensionValues'][0]['value']
            os = r['dimensionValues'][1]['value']
            br = r['dimensionValues'][2]['value']
            u = r['metricValues'][0]['value']
            s = r['metricValues'][1]['value']
            print(f"{cat:<12} | {os:<15} | {br:<15} | {u:<6} | {s:<6}")

    # 8. Hourly Traffic Today
    print("\n[8] 오늘 시간대별 유입 추이 (Hourly Inflow)")
    res_hr = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "today", "endDate": "today"}],
        "dimensions": [{"name": "hour"}],
        "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}],
        "orderBys": [{"dimension": {"dimensionName": "hour"}}]
    })
    if res_hr and res_hr.get('rows'):
        print(f"{'시간':<6} | {'사용자':<6} | {'세션':<6} | {'뷰':<6}")
        print("-" * 30)
        for r in res_hr['rows']:
            h = r['dimensionValues'][0]['value']
            u = r['metricValues'][0]['value']
            s = r['metricValues'][1]['value']
            v = r['metricValues'][2]['value']
            print(f"{h:0>2}시    | {u:<6} | {s:<6} | {v:<6}")

    # 9. Comparison with Yesterday (Final Tally of 2026-10-24)
    print("\n[9] [참고] 어제(2026-10-24) 최종 유입 정산치")
    res_y = query_ga4(token, "runReport", {
        "dateRanges": [{"startDate": "yesterday", "endDate": "yesterday"}],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}, {"name": "sessionSourceMedium"}],
        "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}]
    })
    if res_y and res_y.get('rows'):
        for r in res_y['rows']:
            ch = r['dimensionValues'][0]['value']
            sm = r['dimensionValues'][1]['value']
            u = r['metricValues'][0]['value']
            s = r['metricValues'][1]['value']
            v = r['metricValues'][2]['value']
            print(f"• {ch:<18} ({sm}): {u}명 유입, {s}세션, {v}뷰")

if __name__ == '__main__':
    main()
