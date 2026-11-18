import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import { ProjectIcon } from '@site/src/components/Icons';
import allPostsData from '@site/src/data/all_posts.json';
import styles from './index.module.css';

interface ProjectCardData {
  id: string;
  name: string;
  badge: string;
  category: string;
  subtitle: string;
  description: string;
  tags: string[];
  link: string;
}

const FEATURED_PROJECTS_EN: ProjectCardData[] = [
  {
    id: 'sdc_replanning',
    name: 'SDC Mission Replanning',
    badge: 'Avionics AI · 3 Posts',
    category: 'Mission Critical / Aerospace / AI',
    subtitle: 'In-Flight Air Combat Dynamic Mission Replanning System',
    description:
      'Mission-critical software architecture for tactical data links (Link 16): zero-dependency RFC 8785 deterministic JCS canonicalization, Ed25519 multi-signature cryptographic envelopes, CPython 31.4s to 0.25s A* graph search optimization, and RK4 numerical fuel verification.',
    tags: ['Mission Replanning', 'Ed25519', 'RFC 8785 JCS', 'Link 16 MTU', 'RK4 Fuel', 'Simplex AI'],
    link: '/blog#sdc_replanning',
  },
  {
    id: 'security',
    name: 'Security, Python & Web Infra',
    badge: 'DevSecOps · 4 Posts',
    category: 'Web Security / Python Debugging',
    subtitle: 'Runtime Troubleshooting, DNS/Socket Debugging & Supply Chain Defense',
    description:
      'Hands-on debugging of real production bottlenecks: Windows socket.getaddrinfo DNS timeout hangs in Python urllib/requests, UTF-16 null-byte decoding traps, npm v8.3+ transitive overrides, static site threat modeling, and Cloudflare DNS migration.',
    tags: ['Python Debugging', 'npm audit', 'overrides', 'Cloudflare DNS', 'DevSecOps'],
    link: '/blog#security',
  },
  {
    id: 'anpr_vision',
    name: 'Blackbox ANPR & Vision ITS',
    badge: 'Computer Vision · 5 Posts',
    category: 'Computer Vision / Intelligent Transportation',
    subtitle: 'Real-Time Lane Intrusion Detection & Super-Resolution ANPR',
    description:
      'Real-time highway dashcam computer vision under strict 30 FPS latency constraints: geometric lane intrusion detection with Shapely polygon IoU, blurry license plate reconstruction via EDSR_x4 deep super-resolution, and temporal majority voting EasyOCR across 11 iterations.',
    tags: ['OpenCV', 'YOLOv5', 'EDSR Super-Resolution', 'CSRT Tracker', 'EasyOCR', 'PyTorch'],
    link: '/blog#anpr_vision',
  },
  {
    id: 'rl_q_learning',
    name: 'RL Q-Learning Mobile Robot',
    badge: 'Robotics · 5 Posts',
    category: 'Reinforcement Learning / Robotics',
    subtitle: 'Webots Q-Learning Autonomous Obstacle Avoidance Project',
    description:
      'From zero-knowledge exploration to deterministic navigation: continuous distance sensor discretization (648 state bins), velocity/distance reward shaping to counteract sparse reward starvation, and physical Sim-to-Real hardware transfer to dual-motor Arduino microcontrollers.',
    tags: ['Python', 'Webots Simulator', 'Q-Learning', 'NumPy', 'Socket IPC', 'Arduino Hardware'],
    link: '/blog#rl_q_learning',
  },
  {
    id: 'maeumjigi',
    name: 'LLM Fine-Tuning & Backend Debugging',
    badge: 'Full-Stack AI · 3 Posts',
    category: 'LLM Engineering / FastAPI / PostgreSQL',
    subtitle: 'Llama 3.1 Tokenization, Rate-Limit Recovery & Bcrypt 401 Troubleshooting',
    description:
      'Real-world debugging chronicles from building a full-stack conversational AI service: fixing Llama 3.1 missing <|eot_id|> infinite generation loops, surviving HTTP 429 rate limits with SQLite checkpoint state machines, and resolving FastAPI PostgreSQL $2a$/$2b$ Bcrypt 401 errors.',
    tags: ['Llama 3.1', 'FastAPI', 'PostgreSQL', 'Bcrypt 401 Fix', 'SQLite State Machine'],
    link: '/blog#maeumjigi',
  },
];

const FEATURED_PROJECTS_KO: ProjectCardData[] = [
  {
    id: 'sdc_replanning',
    name: '항공작전 동적 임무계획 (SDC)',
    badge: '항공전자 AI · 3편',
    category: '미션 크리티컬 / 항공우주 / AI',
    subtitle: '비행 중 실시간 경로 재계획 및 전술 데이터링크(Link 16) 검증 아키텍처',
    description:
      'CPython 3D A* 탐색의 31.4초 병목을 사전 베이킹 가시선(Viewshed) 행렬로 0.259초까지 단축한 과정, 8GB VRAM 환경의 듀얼 LLM CUDA OOM 해결, RFC 8785 결정론적 JCS 정규화 및 Ed25519 다중 서명 단편화 오류 해결 기록입니다.',
    tags: ['동적 임무계획', 'Ed25519', 'RFC 8785 JCS', 'Link 16 MTU', 'RK4 연료검증', 'Simplex AI'],
    link: '/ko/blog#sdc_replanning',
  },
  {
    id: 'security',
    name: '보안 · 파이썬 & 웹 인프라 디버깅',
    badge: '트러블슈팅 · 4편',
    category: '시스템 디버깅 / 공급망 보안',
    subtitle: '실전 런타임 오류 해결, Windows DNS 무한 대기 디버깅 및 패키지 보안',
    description:
      'Windows 환경에서 Python urllib·requests의 timeout 옵션이 socket.getaddrinfo DNS 조회에서 먹통이 되는 현상과 ThreadPoolExecutor(wait=False) 해결책, UTF-16 널 바이트(\\x00) 정규식 오류, npm overrides 전이 취약점 패치 및 Cloudflare DNS 마이그레이션을 다룹니다.',
    tags: ['Python 디버깅', 'socket.getaddrinfo', 'npm audit', 'overrides', 'Cloudflare DNS'],
    link: '/ko/blog#security',
  },
  {
    id: 'anpr_vision',
    name: '블랙박스 차선침범 & 초해상화 번호판 인식',
    badge: '컴퓨터 비전 · 5편',
    category: '컴퓨터 비전 / 지능형 교통체계(ITS)',
    subtitle: '30 FPS 실시간 제약 아래 구동되는 6단계 고속도로 영상 인식 파이프라인',
    description:
      '허프 변환 수직선 0 나눗셈 및 Shapely 자가 교차 폴리곤 크래시 해결, YOLOv3/YOLOv5 계층형 크롭 경계 예외 방어, EDSR_x4 초해상화 프레임 멈춤 병목(440ms → 1회 스태킹 호출) 및 EasyOCR 다수결 보팅 구현기입니다.',
    tags: ['OpenCV', 'YOLOv5', 'EDSR 초해상화', 'CSRT 추적기', 'EasyOCR', 'PyTorch'],
    link: '/ko/blog#anpr_vision',
  },
  {
    id: 'rl_q_learning',
    name: 'Webots Q-Learning 자율주행 로봇',
    badge: '로보틱스 · 5편',
    category: '강화학습 / 임베디드 로보틱스',
    subtitle: '648개 상태 공간 이산화부터 아두이노 실제 하드웨어 Sim-to-Real 이식까지',
    description:
      '연속 초음파 센서 값의 648개 이산 상태 매핑, 희소 보상 고갈과 12개 벽 장애물 국소 최적해(Local Minima) 탈출을 위한 보상 함수 튜닝, Webots 물리 시뮬레이터에서 실제 아두이노 2륜 로봇으로의 Sim-to-Real 이식 기록입니다.',
    tags: ['Python', 'Webots 시뮬레이터', 'Q-Learning', 'NumPy', 'TCP 소켓 IPC', '아두이노'],
    link: '/ko/blog#rl_q_learning',
  },
  {
    id: 'maeumjigi',
    name: 'LLM 파인튜닝 & 백엔드 트러블슈팅',
    badge: '풀스택 AI · 3편',
    category: 'LLM 엔지니어링 / FastAPI / PostgreSQL',
    subtitle: 'Llama 3.1 토큰 무한 생성 버그, API 429 복구 상태머신 및 Bcrypt 401 디버깅',
    description:
      'Llama 3.1 파인튜닝 시 <|eot_id|> 누락으로 인한 무한 생성 현상 해결, 대량 데이터 합성 중 HTTP 429 쿼터 차단과 SQLite 체크포인트 상태머신 복구, PostgreSQL 덤프 복원 후 발생한 $2a$/$2b$ Bcrypt 솔트 불일치 401 에러 해결기입니다.',
    tags: ['Llama 3.1', 'FastAPI', 'PostgreSQL', 'Bcrypt 401 해결', 'SQLite 체크포인트'],
    link: '/ko/blog#maeumjigi',
  },
];

export default function Home(): React.JSX.Element {
  const {
    i18n: { currentLocale },
  } = useDocusaurusContext();
  const isKo = currentLocale === 'ko';
  const totalPostsCount = allPostsData.length;
  const projects = isKo ? FEATURED_PROJECTS_KO : FEATURED_PROJECTS_EN;

  return (
    <Layout
      title={
        isKo
          ? 'Global Dev Blog | 실전 AI·로보틱스·비전·시스템 오류 해결 및 엔지니어링 기록'
          : 'Global Dev Blog | Production AI, Robotics & Systems Debugging Deep Dives'
      }
      description={
        isKo
          ? '직접 겪은 런타임 에러 트레이스백, 실패한 가설, 근본 원인 분석과 검증된 해결 코드를 기록하는 AI·로보틱스·컴퓨터 비전·보안 엔지니어링 기술 블로그입니다.'
          : 'Hands-on debugging postmortems, raw error tracebacks, root-cause analyses, and reproducible fixes in AI Systems, Robotics, Computer Vision, and Web Security.'
      }>
      <main className={styles.homeContainer}>
        {/* 1. Hero Section */}
        <section className={styles.heroSection}>
          <div className={styles.heroBadge}>
            {isKo
              ? '실전 에러 디버깅 노트 & 재현 가능한 엔지니어링 기록'
              : 'EMPIRICAL DEBUGGING LOGBOOK & REPRODUCIBLE ENGINEERING'}
          </div>
          <h1 className={styles.heroTitle}>Global Dev Blog</h1>
          <p className={styles.heroSubtitle}>
            {isKo ? (
              <>
                이론 요약 대신 실제 개발 현장에서 마주친{' '}
                <strong>런타임 에러 로그, 병목 원인 분석, 실패했던 시도와 최종 해결 코드(Before/After)</strong>를 기록합니다.
              </>
            ) : (
              <>
                Real-world technical postmortems, raw exception tracebacks, root-cause diagnostics, and verified fixes in{' '}
                <strong>Python Systems, Computer Vision, Autonomous Robotics, Aerospace Replanning, and Web Security</strong>.
              </>
            )}
          </p>

          <div className={styles.statsRow}>
            <div className={styles.statItem}>
              <span className={styles.statNumber}>{totalPostsCount}</span>
              <span className={styles.statLabel}>{isKo ? '정예 기술 포스트' : 'Verified Deep Dives'}</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statNumber}>5</span>
              <span className={styles.statLabel}>{isKo ? '실전 프로젝트 트랙' : 'Engineering Tracks'}</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statNumber}>100%</span>
              <span className={styles.statLabel}>{isKo ? '실제 실행·검증 코드' : 'Empirically Tested'}</span>
            </div>
          </div>

          <div className={styles.heroActions}>
            <Link className={styles.btnPrimary} to={isKo ? '/ko/blog' : '/blog'}>
              {isKo ? `전체 ${totalPostsCount}편 기술 포스트 보기 →` : `Explore All ${totalPostsCount} Technical Articles →`}
            </Link>
            <Link className={styles.btnSecondary} to={isKo ? '/ko/about' : '/about'}>
              {isKo ? '엔지니어 소개 & 실험 환경' : 'About the Lab & Hardware Rig'}
            </Link>
            <Link className={styles.btnSecondary} to={isKo ? '/ko/terms' : '/terms'}>
              {isKo ? '이용약관 & 연구 고지사항' : 'Terms & Research Disclaimer'}
            </Link>
          </div>
        </section>

        {/* 2. Core Engineering Project Tracks Showcase */}
        <section style={{ marginBottom: '4rem' }}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>
              <span>🛠️</span> {isKo ? '5대 핵심 엔지니어링 & 트러블슈팅 트랙' : '5 Core Engineering & Debugging Tracks'}
            </h2>
            <p className={styles.sectionSubtitle}>
              {isKo
                ? '각 프로젝트에서 실제로 발생한 런타임 오류, 성능 병목, 하드웨어 제약과 이를 해결한 코드 기록입니다.'
                : 'Production systems, hardware bottleneck analyses, and step-by-step error resolution chronicles.'}
            </p>
          </div>

          <div className={styles.projectsGrid}>
            {projects.map((proj) => (
              <div key={proj.id} className={styles.projectCard}>
                <div>
                  <div className={styles.cardHeader}>
                    <span className={styles.cardBadge}>{proj.badge}</span>
                    <span className={styles.cardCategory}>{proj.category}</span>
                  </div>

                  <div className={styles.projectTitleGroup}>
                    <div className={styles.projectIconBox}>
                      <ProjectIcon id={proj.id} size={24} />
                    </div>
                    <h3 className={styles.projectName}>{proj.name}</h3>
                  </div>

                  <div className={styles.projectSub}>{proj.subtitle}</div>
                  <p className={styles.projectDesc}>{proj.description}</p>

                  <div className={styles.techTags}>
                    {proj.tags.map((tag) => (
                      <span key={tag} className={styles.techTag}>
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>

                <div className={styles.cardFooter}>
                  <Link className={styles.cardLink} to={proj.link}>
                    {isKo ? '트랙 전체 글 보기 →' : 'View Project Series & Episodes →'}
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 3. Static Articles Directory (All 20 Curated Posts in SSG HTML) */}
        <section className={styles.articlesDirectory}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>
              <span>📚</span>{' '}
              {isKo
                ? `전체 오류 해결 & 기술 아티클 목록 (${totalPostsCount}편)`
                : `Complete Engineering & Troubleshooting Directory (${totalPostsCount} Posts)`}
            </h2>
            <p className={styles.sectionSubtitle}>
              {isKo
                ? '최신순으로 정렬된 실제 디버깅 기록과 아키텍처 검증 보고서입니다.'
                : 'All empirical debugging logs, root-cause analyses, and benchmark reports in chronological order.'}
            </p>
          </div>

          <div className={styles.articlesGrid}>
            {allPostsData.map((post: any) => {
              const postUrl = isKo ? `/ko${post.permalink}` : post.permalink;
              const postTitle = isKo ? post.title_ko || post.title : post.title;
              return (
                <Link key={post.permalink} className={styles.articleItem} to={postUrl}>
                  <span className={styles.articleTitle} title={postTitle}>
                    {postTitle}
                  </span>
                  <span className={styles.articleDate}>{post.date}</span>
                </Link>
              );
            })}
          </div>
        </section>

        {/* 4. Editorial Integrity & Verification Standards (E-E-A-T) */}
        <section>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>
              <span>🛡️</span> {isKo ? '작성 원칙 및 검증 기준' : 'Publication Ethics & Verification Rigor'}
            </h2>
            <p className={styles.sectionSubtitle}>
              {isKo
                ? '단순 요약이나 추상적 설명을 배제하고 직접 겪은 오류와 재현 가능한 해결책만 게시합니다.'
                : 'How we guarantee technical credibility, authentic debugging records, and empirical reproducibility.'}
            </p>
          </div>

          <div className={styles.infoGrid}>
            <div className={styles.infoCard}>
              <h3 className={styles.infoCardTitle}>
                <span>🔬</span> {isKo ? '100% 실제 환경 실행·검증' : '100% Empirically Tested'}
              </h3>
              <p className={styles.infoCardDesc}>
                {isKo
                  ? '이 블로그의 모든 트러블슈팅 코드와 벤치마크는 실제 워크스테이션(NVIDIA RTX 4060 GPU, Windows 11 / Ubuntu WSL2, Python 3.12, TypeScript, Webots)에서 직접 실행하고 검증한 결과만 수록합니다.'
                  : 'Every architectural pattern, Python/C++ snippet, machine learning pipeline, and troubleshooting fix published on this blog is executed and verified on actual lab hardware before publication.'}
              </p>
            </div>

            <div className={styles.infoCard}>
              <h3 className={styles.infoCardTitle}>
                <span>⚖️</span> {isKo ? '실패한 시도와 근본 원인 기록' : 'Failed Attempts & Root Causes'}
              </h3>
              <p className={styles.infoCardDesc}>
                {isKo
                  ? '단순히 정답 코드만 나열하지 않고, 처음에 왜 잘못된 가설을 세웠는지, 어떤 예외 트레이스백이 발생했는지, 그리고 왜 그 우회법이 실패했는지를 함께 기록합니다.'
                  : 'We document not just the final patch, but the raw stack traces, failed workarounds, and underlying OS/runtime mechanics that caused the bug in the first place.'}
              </p>
            </div>

            <div className={styles.infoCard}>
              <h3 className={styles.infoCardTitle}>
                <span>💻</span> {isKo ? '오픈소스 및 투명한 검증' : 'Open Source Accountability'}
              </h3>
              <p className={styles.infoCardDesc}>
                {isKo
                  ? '게시글에 수록된 코드는 GitHub 저장소(github.com/jbjihwan)와 연동되어 있으며, 독자가 동일한 환경에서 그대로 재현하고 검증할 수 있습니다.'
                  : 'Articles are tied to verifiable GitHub repositories (github.com/jbjihwan) so fellow engineers can inspect, reproduce, and validate every benchmark.'}
              </p>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
