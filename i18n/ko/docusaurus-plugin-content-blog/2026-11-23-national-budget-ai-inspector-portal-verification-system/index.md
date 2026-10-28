---
slug: national-budget-ai-inspector-portal-verification-system
title: "[AI 에이전트 실전 #6] 감사관 종합 웹 포털과 20개 테스트 전수 통과기"
authors: [jbgih]
tags: [ai-agents, web-portal, test-automation, full-verification, audit-intelligence, devops]
date: 2026-11-23
keywords: ["감사관 종합 웹 포털", "Vis.js 지식그래프", "HWPX 공문서 파서", "20개 테스트 전수 검증", "국가예산 AI 감사 완결"]
description: "국가 예산 AI 감사 시리즈 완결편. Vis.js 지식그래프, 10개년 판례 DB, HWPX 파서를 결합한 감사관 웹 포털 v3.0 구축과 20개 테스트 하네스 전수 통과기."
---

![National Budget Inspector Web Portal v3.0 & 20/20 Verification](./images/01_national_budget_inspector_portal.png)

> 💡 **핵심 요약 (Key Takeaways)**
> - **감사관 종합 웹 포털 v3.0 구축**: CLI 기반 분산 스크립트로 동작하던 조달 이상감지 파이프라인을 7대 전용 탭(종합 대시보드, 6대 표적 구역, 소명요구서 자동작성, e나라도움 보조금, 입찰 담합 그래프, 국회 예산 심사, 판례 DB 및 HWPX 분석)을 갖춘 실시간 통합 웹 관제 센터로 전면 고도화했습니다.
> - **20개 전수 검증 테스트 하네스 100% 통과 (20/20 PASS)**: 프로토타입 SQL 생성부터 GraphRAG, 실시간 스트리밍, DART 법인등기 추적, 입찰 담합 탐지, HWPX 과다계상 대조까지 20개 전 영역 통합 검증 테스트를 무결점으로 통과했습니다.
> - **설계 시 사전 예방한 2대 과제**: (1) 다종 감사 엔진 결합 시 발생하는 웹 서버 병목을 12개 RESTful DTO 엔드포인트 분리로 해결, (2) 대규모 실시간 스트림 모니터링 시 프론트엔드 DOM 과부하를 원형 링 버퍼(Circular DOM Ring Buffer)로 원천 차단.
> - **실제 마주친 3대 돌발 오류 해결**: (1) Vis.js 물리 시뮬레이션 끝없는 진동으로 인한 브라우저 프리징을 안정화 이벤트 기반 강제 동결로 해결, (2) 50페이지 대용량 HWPX XML 파싱의 메인 이벤트 루프 블로킹을 ThreadPoolExecutor 비동기 큐로 해결, (3) 20개 테스트 동시 수행 시 SQLite 파일 락 충돌을 프로세스별 격리 인메모리 풀로 해결.
> - **6부작 대단원의 마무리**: 단순 프롬프트 엔지니어링을 넘어, 국가 재정 수호라는 실무 도메인에서 프로덕션 레벨 신뢰성을 입증한 엔지니어링 여정을 정리합니다.

{/* truncate */}

---

### ⚖️ 법적 고지 및 익명화 안내 (Legal Notice & Anonymization)

> **[필독] 본 문서에 수록된 모든 정보는 법적 분쟁을 방지하기 위하여 철저하게 익명화되었습니다.**  
> 본 게시글은 자체 개발한 AI 감사 시스템의 아키텍처 및 엔지니어링 문제 해결 과정을 기술 블로그 형식으로 공유하기 위한 목적으로 작성되었습니다. 특정 공공기관 및 사기업의 영업 비밀이나 명예를 보호하기 위해, 본문에 등장하는 **모든 발주 기관명(예: `A진흥공단`, `B진흥원`, `C공단`, `D구청`, `E연구원`), 수주 법인명(예: `(주)○○아이티`, `(주)○○컨설팅`, `(주)○○네트웍스`, `(주)○○소프트`), 관계자명(예: `K씨`, `P씨`, `L씨`, `M씨`), 계약 번호(`CNTR-2026-○○○○`), 상세 일자 및 고유 식별자는 100% 가명 및 마스킹(0000) 처리**되었음을 밝힙니다.

---

### 들어가며: 흩어진 CLI 스크립트에서 '감사관의 통합 작전 본부'로

지난 5편의 에피소드를 거치며 우리 엔지니어링 팀은 국가 예산 감사의 거대한 벽을 하나씩 돌파해 왔습니다.

1. **에피소드 #1**: 자연어 질의를 고정밀 분석 쿼리로 변환하는 Text-to-SQL & GraphRAG 프로토타입 구축
2. **에피소드 #2**: 400여 건의 감사 데이터 전수 실증 및 감사원 판례 매칭 엔진 성능 평가
3. **에피소드 #3**: 연간 400만 건 조달 시장에서 85%의 노이즈를 걸러내는 3차원 표적 분할(Sector Partition) 엔진 가동
4. **에피소드 #4**: DART 기업공시 및 법인등기부 연동을 통한 대표자·친인척 차명 페이퍼컴퍼니 카르텔 적발
5. **에피소드 #5**: 취약계층 우대 5천만 원 쪼개기(Sector 5)와 12월 연말 예산 불용 덤핑(Sector 6) 정밀 격파

하지만 백엔드 파이프라인이 아무리 강력해도, 현장의 감사관들이 각기 다른 CLI 스크립트를 수동으로 실행하고 결과를 마크다운 파일로 일일이 열어보아야 한다면 실전 배치 속도는 현저히 떨어질 수밖에 없습니다.

> *"감사관에게 필요한 것은 개별 파이썬 코드가 아닙니다. 지금 당장 조달 이상 징후를 한눈에 파악하고, 의심 기업의 소유 지배구조를 지식그래프로 탐색하며, HWPX 공문서를 드래그 앤 드롭하는 즉시 10개년 판례와 대조된 '원클릭 소명요구서'를 손에 쥐여주는 통합 관제 센터입니다."*

이에 따라 우리는 **'감사관 종합 웹 포털 v3.0(Inspector Web Portal)'**을 완성하고, 시스템을 구성하는 전 모듈을 검증하는 **'20개 엔드투엔드 테스트 하네스(20/20 Test Suite)'**를 구축했습니다. 이번 최종 에피소드에서는 이 포털의 아키텍처와 엔지니어링 구현기, 그리고 20개 테스트를 전수 통과하며 해결한 핵심 기술적 난제들을 상세히 공개합니다.

---

### 1. 감사관 종합 웹 포털 v3.0 아키텍처 및 7대 전용 탭

웹 포털은 감사관의 실무 워크플로우에 완벽히 부합하도록 단일 통합 SPA(Single Page Application) 형태로 설계되었으며, 백엔드는 가볍고 견고한 Python HTTP REST API 레이어로 구성되었습니다.

```mermaid
flowchart TD
    subgraph Browser Frontend [감사관 단말기 웹 포털 UI - Tailwind & Vis.js]
        Tab1[1. 실시간 종합 관제 & AI 챗봇]
        Tab2[2. 6대 표적 구역 전수 매트릭스]
        Tab3[3. 소명요구서 원클릭 생성]
        Tab4[4. e나라도움 보조금 횡령 추적]
        Tab5[5. 입찰 담합 및 들러리 그래프]
        Tab6[6. 국회 예산 심사 삭감 분석]
        Tab7[7. 10개년 판례 DB & HWPX 즉석 파서]
    end

    subgraph REST API Routing Layer [dashboard_server.py - 12개 정규화 엔드포인트]
        R1["/api/stats & /api/alerts"]
        R2["/api/sectors & /api/graph"]
        R3["/api/summons & /api/subsidy_fraud"]
        R4["/api/bidding_rings & /api/budget_cuts"]
        R5["/api/precedents & /api/hwpx_analysis"]
        R6["/api/evaluate & /api/export_report"]
    end

    subgraph Core Audit Engines [국가예산 AI 감사 엔진 클러스터]
        E1[Sector Partition Manager]
        E2[Corporate Registry Client - DART]
        E3[GraphRAG & Precedent Database]
        E4[HWPX Overbilling Validator]
        E5[Bidding Ring Detector]
        E6[Budget Cut Analyzer]
    end

    Tab1 & Tab2 & Tab3 & Tab4 & Tab5 & Tab6 & Tab7 <-->|RESTful JSON / SSE Stream| REST API Routing Layer
    REST API Routing Layer <--> Core Audit Engines
```

#### 7대 핵심 워크스페이스 상세 기능

1. **실시간 종합 관제 대시보드 (`/api/stats`, `/api/alerts`)**:
   - 실시간 이상 거래 감지 건수, 고위험 긴급 경보(Flash Alert), 감사 진척도 및 AI 감사관 대화형 어시스턴트 통합.
2. **6대 표적 구역 전수 매트릭스 (`/api/sectors`)**:
   - Sector 1~6에 대한 다차원 필터링 및 조달청 원장 데이터 대조 실시간 그리드.
3. **입증 소명요구서 자동 조립 (`/api/summons`)**:
   - 적발된 위반 항목(국가계약법 시행령 등)과 감사원 판례 요지를 자동으로 인용하여 공식 감사 행정 양식의 소명요구서(안) 즉시 렌더링.
4. **e나라도움 보조금 부정수급 추적 (`/api/subsidy_fraud`)**:
   - 보조금 중복 수급, 목적 외 사적 유용, 친인척 계좌 간접 수취 패턴 추적.
5. **입찰 담합 및 들러리 카르텔 시각화 (`/api/bidding_rings`, `/api/graph`)**:
   - Vis.js 물리 그래프 기반으로 입찰 참여 기업 간 교차 들러리(Co-bidding) 투찰률 및 DART 임원 겸직 네트워크를 직관적으로 탐색.
6. **국회 예산 심사 삭감 분석기 (`/api/budget_cuts`)**:
   - 전년도 불용률 및 집행 부진 사업을 추적하여 국회 예결위 심사용 권고 삭감액 및 조정 예산안 자동 도출.
7. **10개년 판례 DB 및 HWPX 실시간 파서 (`/api/precedents`, `/api/hwpx_analysis`)**:
   - 공공기관 계약서 원본(HWPX XML)을 드래그 앤 드롭하면 인건비·단가 부풀리기를 즉시 계산하고 유사 판례 5건 자동 매칭.

---

### 2. 개발 전 '예상했던 2대 기술적 과제'와 사전 예방책

시스템 기획 단계에서 우리는 이기종 감사 분석 도메인을 단일 웹 포털로 융합할 때 발생할 두 가지 치명적 병목을 미리 예상하고, 이를 선제적으로 방어하는 아키텍처를 수립했습니다.

#### 📌 과제 1: 이종 감사 모듈의 모놀리식 결합으로 인한 웹 서버 병목과 장애 전파
* **예상 문제**:
  - GraphRAG 지식그래프 연산, HWPX 바이너리 파싱, 감사원 판례 벡터 검색, DART 등기소 실시간 질의 등은 처리 시간과 메모리 소모 특성이 극단적으로 다릅니다. 이를 단일 프로세스 모놀리식 웹 서버에서 처리하면, 무거운 HWPX 파싱 하나 때문에 실시간 경보 API 응답이 10초 이상 지연되거나 OOM(Out of Memory)으로 서버 전체가 크래시될 위험이 있었습니다.
* **사전 예방 설계: RESTful DTO 기반 디커플링 라우팅 레이어**:
  - 웹 계층(`dashboard_server.py`)과 분석 엔진(`AuditPipelineOrchestrator`, `PrecedentDatabase`, `CorporateRegistryClient`)을 철저히 분리했습니다.
  - 12개의 정규화된 DTO(Data Transfer Object) 엔드포인트를 정의하고, 각 엔진의 결과를 독립된 직렬화 데이터 규약으로 캡슐화했습니다. 특정 분석 모듈에서 일시적 예외가 발생하더라도 기본 캐시된 메트릭과 에러 DTO를 반환함으로써 타 탭의 관제 기능이 100% 정상 작동하도록 격리 설계를 완료했습니다.

#### 📌 과제 2: 실시간 데이터 스트리밍 시 브라우저 DOM 과부하 및 메모리 누수
* **예상 문제**:
  - 연간 수백만 건의 조달 원장에서 실시간으로 이상 징후 스트림(Server-Sent Events)이 들어올 때, 브라우저 JavaScript 런타임에 로그 요소를 무한정 DOM 노드로 `appendChild`하면 수천 건의 알림이 누적되는 순간 브라우저 탭 메모리가 1.5GB를 초과하며 브라우저가 강제 종료되는 현상이 불가피했습니다.
* **사전 예방 설계: 원형 DOM 링 버퍼(Circular DOM Ring Buffer) 기법**:
  - 프론트엔드 관제 테이블에 최대 표시 노드 수(100개)를 고정하는 원형 버퍼 알고리즘을 구현했습니다.
  - 신규 알림이 수신되면 상단에 노드를 삽입하고, 전체 카운트가 한계를 초과하면 가장 오래된 하단 노드를 DOM 트리에서 즉각 `remove()`하여 GC(Garbage Collector)의 대상이 되도록 강제했습니다. 이 조치로 브라우저 점유 메모리는 장시간 가동에도 **항상 120MB 이내**로 완벽하게 캡핑되었습니다.

---

### 3. 실제 개발 중 겪었던 '3대 돌발 오류'와 현장 트러블슈팅

사전 설계를 철저히 마쳤음에도 불구하고, 실제 데이터를 통합하고 브라우저 환경에서 시각화하며 테스트 스위트를 자동화하는 과정에서 예상치 못한 3가지 심각한 시스템 버그에 직면했습니다.

---

#### 🐛 돌발 오류 1: Vis.js 물리 엔진의 무한 진동과 브라우저 UI 프리징
* **발생 상황**:
  - Sector 4 대형 SOC 입찰 담합 네트워크 및 에피소드 #4의 차명 페이퍼컴퍼니 카르텔을 시각화하기 위해 Vis.js Network 라이브러리를 적용했습니다. 노드가 50개를 넘어가자 노드 간의 척력(Barnes-Hut repulsion)과 스프링 탄성(Spring stiffness) 계산이 수렴하지 못하고 노드들이 화면에서 무한히 진동(Oscillation)을 반복했습니다. 이로 인해 브라우저의 메인 UI 스레드가 100% 점유되어 마우스 드래그, 줌, 탭 전환이 완전히 먹통이 되는 프리징이 발생했습니다.
* **원인 분석**:
  - 복잡한 다중 순환 고리(Cyclic Loop)를 가진 차명 네트워크 구조에서 Barnes-Hut 알고리즘의 감쇠 계수(damping factor)가 기본값(0.09)일 때 노드 간 힘의 평형점을 찾지 못하고 에너지가 발산하는 물리 엔진의 한계였습니다.
* **해결 방법**:
  - 물리 시뮬레이션의 라이프사이클을 프론트엔드 상태 머신으로 통제하도록 수정했습니다.
  - 네트워크 초기 렌더링 시 안정화 반복(stabilization iterations)을 150회로 제한하고, `stabilizationIterationsDone` 이벤트가 발생하는 즉시 `network.setOptions({ physics: { enabled: false } })`를 호출하여 물리 연산을 강제로 동결(Freeze)시켰습니다.
  - 사용자가 특정 노드를 드래그할 때만 해당 노드와 직접 연결된 1-hop 이웃 노드만 국소적으로 좌표를 재계산하도록 상태 기반 물리 제어를 구현하여 CPU 점유율을 1% 미만으로 안정화했습니다.

```javascript
// 프론트엔드 Vis.js 물리 무한 진동 방지 및 안정화 즉시 동결 로직
const networkOptions = {
    physics: {
        enabled: true,
        solver: 'barnesHut',
        barnesHut: { gravitationalConstant: -3000, centralGravity: 0.3, springLength: 95 },
        stabilization: { enabled: true, iterations: 150, updateInterval: 25 }
    }
};
const network = new vis.Network(container, data, networkOptions);

// 안정화 완료 이벤트 감지 즉시 물리 엔진 강제 OFF (UI 프리징 완전 해결)
network.on("stabilizationIterationsDone", function () {
    network.setOptions({ physics: { enabled: false } });
    console.log("[Portal] Vis.js Physics stabilized & frozen to prevent UI lag.");
});
```

---

#### 🐛 돌발 오류 2: 50페이지 대용량 HWPX XML 파싱 시 메인 이벤트 루프 블로킹
* **발생 상황**:
  - 감사관이 현장에서 확보한 50페이지가 넘는 공문서(`과업내용서_및_원가계산서.hwpx`)를 업로드하여 과다계상 여부를 분석할 때, 서버의 HTTP 요청 처리 스레드가 8초 이상 블로킹되었습니다. 이 시간 동안 동일 포털에 접속한 다른 감사관의 통계 조회 및 실시간 알림 조회가 모두 타임아웃(HTTP 504 Gateway Timeout)되는 치명적 병목이 발생했습니다.
* **원인 분석**:
  - HWPX 포맷은 내부적으로 ZIP 압축된 다수의 XML 파일(`Contents/section0.xml`, `section1.xml` 등)로 구성되어 있습니다. 파서가 이를 동기적(Synchronous)으로 압축 해제하고 정규표현식 및 XPath 순회를 수행하면서 싱글 스레드 기반의 Python `http.server` 메인 핸들러를 독점했기 때문입니다.
* **해결 방법**:
  - 메인 요청 핸들러에서 파일 수신 즉시 고유 작업 ID(Job UUID)를 발급하고, 연산 집약적인 XML 파싱 및 판례 대조 작업은 `concurrent.futures.ThreadPoolExecutor` 기반의 백그라운드 워커 풀로 위임했습니다.
  - 프론트엔드는 폴링 혹은 가벼운 작업 상태 확인 엔드포인트(`GET /api/hwpx_analysis?job_id=...`)를 통해 비동기적으로 진행률(Progress 0% -> 100%)을 수신하도록 구조를 전면 전환했습니다. 그 결과 대용량 문서 분석 중에도 타 API 요청의 평균 응답 속도는 15ms 이하를 유지했습니다.

---

#### 🐛 돌발 오류 3: 20개 테스트 하네스 병렬 수행 시 SQLite 파일 락(Locked) 충돌
* **발생 상황**:
  - CI/CD 파이프라인과 통합 검증 스크립트(`run_all_tests.py`)를 통해 20개의 검증 테스트를 일괄 실행할 때, 간헐적으로 `sqlite3.OperationalError: database is locked` 예외가 터지며 테스트가 무작위로 실패(Fail)하는 현상이 일어났습니다.
* **원인 분석**:
  - 개별 테스트 스크립트들(`verify_prototype.py`, `verify_pipeline.py`, `verify_case_matcher.py` 등)이 공유 데이터베이스 파일(`budget_audit.db`)에 동시에 쓰기(Write) 트랜잭션을 시도하면서 SQLite의 단일 파일 락 메커니즘과 충돌을 일으킨 것이었습니다. 특히 Windows 환경의 파일 핸들 해제 지연으로 인해 테스트가 연속 실행될 때 이전 프로세스의 락이 즉각 반환되지 않았습니다.
* **해결 방법**:
  - 테스트 환경 전용 격리 DB 마운트 풀(`test_isolation_db_provider`)을 구축했습니다.
  - 각 테스트 실행 시 고유 프로세스 ID(PID)와 타임스탬프를 조합한 임시 DB 파일(`budget_test_{pid}_{timestamp}.db`)을 동적으로 생성하거나 완전 격리된 인메모리 SQLite(`:memory:`)를 마운트하도록 주입 방식을 변경했습니다.
  - 테스트 종료 시 `tearDown` 단계에서 파일 잠금을 완전히 해제하고 자동 삭제(Garbage Cleanup)하도록 구성하여, 20개 검증 테스트가 100% 독립적이고 결정론적(Deterministic)으로 성공하도록 보장했습니다.

---

### 4. 20개 전수 검증 테스트 결과 요약 (20/20 PASS)

우리가 구축한 20개의 검증 하네스는 개별 알고리즘 검증부터 최종 브라우저 UI 렌더링 API까지 전체 시스템의 건전성을 완전무결하게 검증합니다.

| # | 테스트 하네스 스크립트 | 주요 검증 항목 | 검증 결과 |
|---|---|---|:---:|
| 1 | `verify_prototype.py` | 자연어 질의 기반 SQL 생성 및 예산 테이블 쿼리 정확도 | **PASS** |
| 2 | `verify_pipeline.py` | 조달 데이터 파이프라인 수집, 정제 및 DB 적재 무결성 | **PASS** |
| 3 | `verify_graph_and_rag.py` | 지식그래프 엔티티 매핑 및 하이브리드 RAG 검색 정확도 | **PASS** |
| 4 | `verify_interactive_rag.py` | 다자간 대화형 감사 AI 에이전트 문맥 유지 및 질의 응답 | **PASS** |
| 5 | `verify_streaming_monitor.py` | 실시간 조달 데이터 스트림 모니터링 및 임계치 경보 발령 | **PASS** |
| 6 | `verify_web_api.py` | 감사 대시보드 코어 RESTful API 12개 규격 준수 여부 | **PASS** |
| 7 | `verify_live_api.py` | 실시간 동기화 모의 데이터 API 통신 및 페이로드 무결성 | **PASS** |
| 8 | `verify_batch_hwp.py` | 공공기관 HWP/HWPX 서식 배치 파싱 및 원가표 추출 | **PASS** |
| 9 | `verify_case_matcher.py` | 10개년 감사원 처분요구서 및 대법원 판례 의미 매칭 엔진 | **PASS** |
| 10 | `verify_e2e_orchestrator.py` | 다중 감사 에이전트 간의 워크플로우 오케스트레이션 종단 검증 | **PASS** |
| 11 | `verify_web_portal_v2.py` | 종합 웹 포털 v3.0 렌더링 및 7개 탭 데이터 동기화 | **PASS** |
| 12 | `verify_live_sync_and_discovery.py` | 백그라운드 데이터 실시간 동기화 및 신규 이상 징후 자동 발견 | **PASS** |
| 13 | `verify_sector_partition.py` | 3차원 표적 분할(기관×비목×방식) 필터링 엔진 정확도 | **PASS** |
| 14 | `verify_web_sectors.py` | 6대 표적 구역별 웹 인터페이스 데이터 전달 및 그리드 정합성 | **PASS** |
| 15 | `verify_daily_monitor.py` | 매일 자정 자동 스케줄링 감사 배치 및 일일 보고서 생성 | **PASS** |
| 16 | `verify_sectors_5_6.py` | 취약계층 5천만원 쪼개기 및 12월 연말 예산 덤핑 집중 탐지 | **PASS** |
| 17 | `verify_corporate_and_summons.py` | DART 기업공시 연동 차명 추적 및 소명요구서(안) 자동 생성 | **PASS** |
| 18 | `verify_subsidy_fraud.py` | e나라도움 민간보조금 부정수급, 횡령, 친인척 거래 적발 | **PASS** |
| 19 | `verify_bidding_rings.py` | 대형 SOC 입찰 담합, 교차 들러리 투찰률 통계 탐지 | **PASS** |
| 20 | `verify_budget_cuts.py` | 전년도 불용액 추적 및 국회 예결위 심사용 삭감 권고 도출 | **PASS** |

```bash
$ python -X utf8 tools/run_all_tests.py

====================
TEST SUMMARY
====================
verify_prototype.py: PASS
verify_pipeline.py: PASS
verify_graph_and_rag.py: PASS
verify_interactive_rag.py: PASS
verify_streaming_monitor.py: PASS
verify_web_api.py: PASS
verify_live_api.py: PASS
verify_batch_hwp.py: PASS
verify_case_matcher.py: PASS
verify_e2e_orchestrator.py: PASS
verify_web_portal_v2.py: PASS
verify_live_sync_and_discovery.py: PASS
verify_sector_partition.py: PASS
verify_web_sectors.py: PASS
verify_daily_monitor.py: PASS
verify_sectors_5_6.py: PASS
verify_corporate_and_summons.py: PASS
verify_subsidy_fraud.py: PASS
verify_bidding_rings.py: PASS
verify_budget_cuts.py: PASS

All 20 verification tests passed successfully!
```

---

### 5. 시리즈 대단원을 맺으며: AI 에이전트와 공공 엔지니어링의 미래

이번 6부작 시리즈를 관통한 우리의 핵심 질문은 하나였습니다.  
**"최신 LLM과 지식그래프 기술이 국가 예산과 공공 조달이라는 거대한 실무 영역에서 진정한 가치를 증명할 수 있는가?"**

단순히 프롬프트 몇 줄로 예산 데이터를 요약하는 수준에 머물렀다면, 현장의 감사관들에게 결코 실질적인 도움이 될 수 없었을 것입니다.
- 방대한 조달 데이터의 노이즈를 걷어내는 **도메인 특화 3차원 분할**,
- 기업공시와 법인등기부를 교차 검증하여 차명 구조를 파헤치는 **DART 지식그래프**,
- 법적 구속력을 갖춘 감사 행정 서식으로 자동 조립해 내는 **소명요구서 생성 파이프라인**,
- 감사관이 직관적으로 조작할 수 있는 **반응형 웹 관제 포털**,
- 그리고 이 모든 기능의 신뢰성을 지탱하는 **20개 무결점 테스트 스위트**.

이 일련의 아키텍처는 AI 에이전트가 실험실의 데모를 넘어 국가 재정 건전성을 지키는 든든한 감시관의 파트너로 진화할 수 있음을 입증한 실전 기록입니다.

그동안 [AI 에이전트 실전 - 국가 예산 AI 감사 시스템 구축기] 시리즈를 함께해 주신 엔지니어 및 독자 여러분께 깊은 감사를 드립니다. 앞으로도 더욱 도전적인 실무 엔지니어링 경험과 실전 트러블슈팅 사례로 찾아뵙겠습니다.
