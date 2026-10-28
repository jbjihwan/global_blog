import React, { useState, useEffect, useMemo } from 'react';
import Link from '@docusaurus/Link';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {
  PageMetadata,
  HtmlClassNameProvider,
  ThemeClassNames,
} from '@docusaurus/theme-common';
import BlogLayout from '@theme/BlogLayout';
import SearchMetadata from '@theme/SearchMetadata';
import BlogListPageStructuredData from '@theme/BlogListPage/StructuredData';
import { ProjectIcon } from '@site/src/components/Icons';
import styles from './styles.module.css';

type SupportedLocale = 'en' | 'ko' | 'ja' | 'es';

interface ProjectInfo {
  id: string;
  name: string;
  badgeType: 'active' | 'upcoming';
  category: string;
  icon: string;
  subtitle: string;
  description: string;
  techTags: string[];
  hasPosts: boolean;
  upcomingBadgeText?: string;
}

interface LocaleContent {
  hubTitle: string;
  hubSubtitle: string;
  tabHub: string;
  tabCs329a: string;
  tabStanford: string;
  tabMaeumjigi: string;
  tabAnpr: string;
  tabRl: string;
  tabSecurity: string;
  tabAll: string;
  bannerCs329aTitle: string;
  bannerCs329aDesc: string;
  bannerStanfordTitle: string;
  bannerStanfordDesc: string;
  bannerMaeumjigiTitle: string;
  bannerMaeumjigiDesc: string;
  bannerAnprTitle: string;
  bannerAnprDesc: string;
  bannerRlTitle: string;
  bannerRlDesc: string;
  bannerSecurityTitle: string;
  bannerSecurityDesc: string;
  bannerAllTitle: string;
  bannerAllDesc: string;
  sortNewest: string;
  sortOldest: string;
  btnReadFirst: string;
  btnReadLatest: string;
  btnBack: string;
  btnReadPost: string;
  btnExploreProject: string;
  btnUpcoming: string;
  emptyNotice: string;
  projects: ProjectInfo[];
}

const I18N_DATA: Record<SupportedLocale, LocaleContent> = {
  ko: {
    hubTitle: '프로젝트 & 개발 일지',
    hubSubtitle: '관심 있는 프로젝트를 선택하여 개발 여정과 기술 기록을 확인해보세요.',
    tabHub: '프로젝트 허브',
    tabCs329a: '스탠포드 CS329A',
    tabStanford: '스탠포드 CS146S',
    tabMaeumjigi: '마음지기',
    tabAnpr: 'ANPR & 차선침범',
    tabRl: 'RL Q-Learning',
    tabSecurity: '보안 & 엔지니어링',
    tabAll: '전체 글 피드',
    bannerCs329aTitle: '프로젝트: 스탠포드 CS329A (자가 진화 AI 에이전트)',
    bannerCs329aDesc: '자율적 자기 개선 인공지능 에이전트: 추론 연산 스케일링, 프로세스 보상 모델(PRM), MCTS 계획 탐색, GRPO 강화학습, 개방형 코드 진화(ADAS/AlphaEvolve), VLA 피지컬 인텔리전스',
    bannerStanfordTitle: '프로젝트: 스탠포드 CS146S (The Modern Software Developer)',
    bannerStanfordDesc: 'AI 에이전트 시대의 현대 소프트웨어 개발론: 스펙 주도 개발(SDD), 루프 엔지니어링, MCP 표준 아키텍처',
    bannerMaeumjigiTitle: '프로젝트: 마음지기 (Maeumjigi Capstone Dev Log)',
    bannerMaeumjigiDesc: 'AI 자살 예방 상담 챗봇 파인튜닝 및 가드레일 개발 일지',
    bannerAnprTitle: '프로젝트: Blackbox ANPR & 차선 침범 적발 시스템',
    bannerAnprDesc: '블랙박스 차선 침범 감지 및 딥러닝 초해상화(EDSR) 기반 한국형 번호판 인식 시스템',
    bannerRlTitle: '프로젝트: RL Q-Learning (Webots 자율주행 로봇)',
    bannerRlDesc: 'Webots 물리 시뮬레이션 기반 648개 상태 공간 Q-Learning 로봇 주행 개발일지',
    bannerSecurityTitle: '프로젝트: 보안 & 웹 엔지니어링',
    bannerSecurityDesc: '정적 사이트 심층 보안 강화, 위협 모델링 및 npm 공급망 취약점 방어',
    bannerAllTitle: '전체 개발 일지 피드',
    bannerAllDesc: '모든 프로젝트의 글이 정렬 순서대로 표시됩니다.',
    sortNewest: '최근 작성순 (최신)',
    sortOldest: '과거 작성순 (1화부터)',
    btnReadFirst: '1화 바로가기',
    btnReadLatest: '최신화 바로가기',
    btnBack: '← 다른 프로젝트 선택',
    btnReadPost: '게시글 읽기 →',
    btnExploreProject: '개발일지 보러가기',
    btnUpcoming: '작성 예정',
    emptyNotice: '해당 카테고리의 포스트가 준비 중입니다.',
    projects: [
      {
        id: 'stanford_cs329a',
        name: '스탠포드 CS329A',
        badgeType: 'active',
        category: 'AI 에이전트 / 기계학습',
        icon: 'stanford_cs329a',
        subtitle: '스탠포드 대학교 자가 진화 AI 에이전트 (Self-Improving AI Agents) 전 강의 시리즈',
        description:
          '차세대 프론티어 AI의 핵심 패러다임. 추론 연산 스케일링, 프로세스 보상 모델(PRM), MCTS 계획 탐색, DeepSeek GRPO 강화학습, Sakana AI Scientist와 DeepMind AlphaEvolve 개방형 코드 진화, Lean 4 수학적 증명(AlphaProof), VLA 로보틱스까지 17개 전 강좌 완벽 분석.',
        techTags: ['Stanford CS329A', 'Self-Improving AI', 'MCTS', 'GRPO', 'PRM', 'VLA'],
        hasPosts: true,
      },
      {
        id: 'stanford_cs146s',
        name: '스탠포드 CS146S',
        badgeType: 'active',
        category: '소프트웨어 공학 / AI 에이전트',
        icon: 'stanford_cs146s',
        subtitle: '스탠포드 대학교 현대 소프트웨어 개발자 강의 시리즈',
        description:
          '수동 코딩에서 AI 에이전트 지휘자로의 대전환. 스펙 주도 개발(SDD), 루프 엔지니어링, 모델 컨텍스트 프로토콜(MCP)과 현대 풀스택 개발 방법론 완벽 해설.',
        techTags: ['Stanford CS146S', 'Agentic Workflows', 'Spec-Driven', 'MCP', 'CI/CD'],
        hasPosts: true,
      },
      {
        id: 'maeumjigi',
        name: '마음지기 (Maeumjigi)',
        badgeType: 'active',
        category: '캡스톤디자인 / AI 챗봇',
        icon: 'maeumjigi',
        subtitle: 'AI 자살 예방 상담 챗봇 캡스톤 개발일지',
        description:
          '우울 및 고위험 위기 발화를 실시간 감지하고 공감 상담을 수행하는 AI 챗봇. Llama 3.1 파인튜닝 (2:1 감성:일상 황금 비율), Safety Wrapper 가드레일, AWS EC2 GPU 서버 배포기.',
        techTags: ['PyTorch', 'Llama 3.1', 'Safety Wrapper', 'FastAPI', 'AWS EC2', 'CapDe'],
        hasPosts: true,
      },
      {
        id: 'anpr_vision',
        name: 'Blackbox ANPR & Lane Intrusion',
        badgeType: 'active',
        category: '컴퓨터 비전 / 지능형 교통(ITS)',
        icon: 'anpr_vision',
        subtitle: '실시간 블랙박스 차선 침범 적발 및 초해상화 번호판 인식 시스템',
        description:
          '블랙박스 영상에서 차선 침범 차량을 실시간 감지(IoU)하고, 저해상도 번호판을 EDSR_x4 딥러닝으로 복원하여 EasyOCR 및 Majority Voting으로 완벽하게 판독하는 비전 시스템 (v01~v11).',
        techTags: ['OpenCV', 'YOLOv5', 'EDSR (SR)', 'CSRT Tracker', 'EasyOCR', 'PyTorch'],
        hasPosts: true,
      },
      {
        id: 'rl_q_learning',
        name: 'RL Q-Learning',
        badgeType: 'active',
        category: '강화학습 / 로보틱스',
        icon: 'rl_q_learning',
        subtitle: 'Webots Q-Learning 자율주행 로봇 프로젝트',
        description:
          'Webots 시뮬레이터 환경에서 에이전트의 Q-Table 최적화 및 자율주행을 탐구하는 강화학습 프로젝트. 648개 이산 상태 공간 설계, 소켓 IPC 통신, 실제 Arduino 로봇 전이 기획.',
        techTags: ['Python', 'Webots', 'Q-Learning', 'NumPy', 'Socket IPC', 'Arduino'],
        hasPosts: true,
      },
      {
        id: 'security',
        name: '보안 & 웹 엔지니어링',
        badgeType: 'active',
        category: '웹 보안 / DevSecOps',
        icon: 'security',
        subtitle: '정적 웹 블로그 심층 보안 하드닝 및 공급망 취약점 방어',
        description:
          '45개 npm 취약점 경고의 실제 런타임 위협 모델링, Git 시크릿 스캔, 개인정보(PII) 누출 차단, Referrer Policy 및 지속적 보안 파이프라인 구축 기록.',
        techTags: ['npm audit', 'SSG Hardening', 'DevSecOps', 'Threat Modeling', 'CI/CD'],
        hasPosts: true,
      },
      {
        id: 'ai_research',
        name: 'AI Research & Tools',
        badgeType: 'upcoming',
        upcomingBadgeText: 'Planned · 연구 노트',
        category: '개발 도구 / AI 에이전트',
        icon: 'ai_research',
        subtitle: '자율 코딩 에이전트 및 LLM 응용 연구',
        description:
          'Antigravity CLI 커스터마이징, 에이전트 오케스트레이션, 프롬프트 엔지니어링 및 개발 생산성 극대화 도구 제작 기록.',
        techTags: ['Antigravity', 'Agentic AI', 'Prompt Engineering', 'TypeScript'],
        hasPosts: false,
      },
    ],
  },
  en: {
    hubTitle: 'Projects & Dev Logs',
    hubSubtitle: 'Select a project to explore dev logs and technical milestones.',
    tabHub: 'Projects Hub',
    tabCs329a: 'Stanford CS329A',
    tabStanford: 'Stanford CS146S',
    tabMaeumjigi: 'Maeumjigi',
    tabAnpr: 'ANPR & Lane Intrusion',
    tabRl: 'RL Q-Learning',
    tabSecurity: 'Security & Infra',
    tabAll: 'All Posts Feed',
    bannerCs329aTitle: 'Project: Stanford CS329A (Self-Improving AI Agents)',
    bannerCs329aDesc: 'Autonomous Self-Improving AI Agents: Test-Time Compute Scaling, PRM Verification, MCTS Tree Search, GRPO Reinforcement Learning, Open-Ended Evolution, and Vision-Language-Action Robotics',
    bannerStanfordTitle: 'Project: Stanford CS146S (The Modern Software Developer)',
    bannerStanfordDesc: 'Modern software engineering in the age of AI agents: Spec-Driven Development, Loop Engineering, and Model Context Protocol (MCP)',
    bannerMaeumjigiTitle: 'Project: Maeumjigi (Capstone Dev Log)',
    bannerMaeumjigiDesc: 'AI Suicide Prevention Counseling Chatbot Fine-tuning & Safety Wrapper Dev Log',
    bannerAnprTitle: 'Project: Blackbox ANPR & Lane Intrusion System',
    bannerAnprDesc: 'Real-time blackbox lane intrusion detection & deep super-resolution (EDSR) Korean ANPR system',
    bannerRlTitle: 'Project: RL Q-Learning (Webots Autonomous Robot)',
    bannerRlDesc: 'Webots physics-based 648-bin state space Q-learning autonomous robot dev logs',
    bannerSecurityTitle: 'Project: Security & Web Engineering',
    bannerSecurityDesc: 'Static site security hardening, threat modeling, and npm supply chain defense',
    bannerAllTitle: 'All Dev Logs Feed',
    bannerAllDesc: 'Chronological feed of all posts across all projects.',
    sortNewest: 'Newest First',
    sortOldest: 'Oldest First (From Ep. 1)',
    btnReadFirst: 'Start Ep. 1',
    btnReadLatest: 'Latest Ep.',
    btnBack: '← Select Another Project',
    btnReadPost: 'Read Post →',
    btnExploreProject: 'Explore Dev Logs',
    btnUpcoming: 'Coming Soon',
    emptyNotice: 'Posts in this category are coming soon.',
    projects: [
      {
        id: 'stanford_cs329a',
        name: 'Stanford CS329A',
        badgeType: 'active',
        category: 'AI Agents / Machine Learning',
        icon: 'stanford_cs329a',
        subtitle: 'Stanford University Self-Improving AI Agents Complete Lecture Series',
        description:
          'The definitive frontier of autonomous AI. In-depth analysis of test-time compute scaling, Process Reward Models (PRM), MCTS tree planning, DeepSeek GRPO RL, Sakana AI Scientist, AlphaEvolve open-ended code discovery, Lean 4 formal verification (AlphaProof), and VLA multimodal robotics across all 17 lectures.',
        techTags: ['Stanford CS329A', 'Self-Improving AI', 'MCTS', 'GRPO', 'PRM', 'VLA'],
        hasPosts: true,
      },
      {
        id: 'stanford_cs146s',
        name: 'Stanford CS146S',
        badgeType: 'active',
        category: 'Software Engineering / AI Agents',
        icon: 'stanford_cs146s',
        subtitle: 'Stanford University Modern Software Developer Series',
        description:
          'The paradigm shift from syntax typing to AI agent orchestration. Comprehensive breakdowns of Spec-Driven Development (SDD), Loop Engineering, and Model Context Protocol (MCP).',
        techTags: ['Stanford CS146S', 'Agentic Workflows', 'Spec-Driven', 'MCP', 'CI/CD'],
        hasPosts: true,
      },
      {
        id: 'maeumjigi',
        name: 'Maeumjigi',
        badgeType: 'active',
        category: 'Capstone Design / AI Chatbot',
        icon: 'maeumjigi',
        subtitle: 'AI Suicide Prevention Counseling Chatbot Dev Log',
        description:
          'Real-time crisis & depression detection with compassionate counseling. Llama 3.1 fine-tuning (2:1 emotional-to-daily ratio), Safety Wrapper guardrails, and AWS EC2 GPU deployment.',
        techTags: ['PyTorch', 'Llama 3.1', 'Safety Wrapper', 'FastAPI', 'AWS EC2', 'CapDe'],
        hasPosts: true,
      },
      {
        id: 'anpr_vision',
        name: 'Blackbox ANPR & Lane Intrusion',
        badgeType: 'active',
        category: 'Computer Vision / ITS',
        icon: 'anpr_vision',
        subtitle: 'Real-Time Lane Intrusion Detection & Super-Resolution ANPR System',
        description:
          'Real-time lane intrusion detection with IoU, blurry license plate reconstruction via EDSR_x4 super-resolution, and temporal majority voting EasyOCR pipeline across 11 iterations (v01 to v11).',
        techTags: ['OpenCV', 'YOLOv5', 'EDSR (SR)', 'CSRT Tracker', 'EasyOCR', 'PyTorch'],
        hasPosts: true,
      },
      {
        id: 'rl_q_learning',
        name: 'RL Q-Learning',
        badgeType: 'active',
        category: 'Reinforcement Learning / Robotics',
        icon: 'rl_q_learning',
        subtitle: 'Webots Q-Learning Autonomous Robot Project',
        description:
          'Q-Table optimization and autonomous navigation in Webots simulation environments. Continuous state discretization (648 bins), socket IPC communication, and Sim-to-Real hardware transfer.',
        techTags: ['Python', 'Webots', 'Q-Learning', 'NumPy', 'Socket IPC', 'Arduino'],
        hasPosts: true,
      },
      {
        id: 'security',
        name: 'Security & Web Engineering',
        badgeType: 'active',
        category: 'Web Security / DevSecOps',
        icon: 'security',
        subtitle: 'Static Site Security Hardening & Supply Chain Defense',
        description:
          'Threat modeling 45 npm audit vulnerabilities in static sites, git secret scanning, PII protection, Referrer Policy headers, and automated security verification pipelines.',
        techTags: ['npm audit', 'SSG Hardening', 'DevSecOps', 'Threat Modeling', 'CI/CD'],
        hasPosts: true,
      },
      {
        id: 'ai_research',
        name: 'AI Research & Tools',
        badgeType: 'upcoming',
        upcomingBadgeText: 'Planned',
        category: 'Developer Tools / AI Agents',
        icon: 'ai_research',
        subtitle: 'Agentic AI & Custom Dev Workflows',
        description:
          'Customizing Antigravity CLI, agent orchestration, prompt engineering, and building developer productivity tools.',
        techTags: ['Antigravity', 'Agentic AI', 'Prompt Engineering', 'TypeScript'],
        hasPosts: false,
      },
    ],
  },
  ja: {
    hubTitle: 'プロジェクト＆開発日誌',
    hubSubtitle: '関心のあるプロジェクトを選択して、開発の歩みと技術的な記録をご覧ください。',
    tabHub: 'プロジェクトハブ',
    tabCs329a: 'スタンフォード CS329A',
    tabStanford: 'スタンフォード CS146S',
    tabMaeumjigi: 'マウムジギ',
    tabAnpr: 'ANPR＆車線侵犯',
    tabRl: 'RL Q-Learning',
    tabSecurity: 'セキュリティ＆インフラ',
    tabAll: '全記事フィード',
    bannerCs329aTitle: 'プロジェクト: スタンフォード CS329A (自己進化AIエージェント)',
    bannerCs329aDesc: '自律型自己改善AIエージェント：推論時計算スケーリング、プロセス報酬モデル(PRM)、MCTS探索計画、GRPO強化学習、オープンエンド進化、VLAマルチモーダルロボティクス',
    bannerStanfordTitle: 'プロジェクト: スタンフォード CS146S (現代ソフトウェア開発者)',
    bannerStanfordDesc: 'AIエージェント時代の現代ソフトウェア開発論：仕様駆動開発(SDD)、ループエンジニアリング、MCP規格',
    bannerMaeumjigiTitle: 'プロジェクト: マウムジギ (卒業研究 開発日誌)',
    bannerMaeumjigiDesc: 'AI自殺予防カウンセリングチャットボットのファインチューニングおよびガードレール開発日誌',
    bannerAnprTitle: 'プロジェクト: Blackbox ANPR＆車線侵犯検知システム',
    bannerAnprDesc: 'ドラレコ車線侵犯リアルタイム検知および深層超解像(EDSR)ベースの韓国ナンバープレート認識システム',
    bannerRlTitle: 'プロジェクト: RL Q-Learning (Webots自律走行ロボット)',
    bannerRlDesc: 'Webots物理シミュレーションベースの648状態空間Q-Learning自律走行開発日誌',
    bannerSecurityTitle: 'プロジェクト: セキュリティ＆ウェブ工学',
    bannerSecurityDesc: '静的サイト深層セキュリティ強化、脅威モデリングおよびnpmサプライチェーン防御',
    bannerAllTitle: '全開発日誌フィード',
    bannerAllDesc: 'すべてのプロジェクトの記事が指定した順序で表示されます。',
    sortNewest: '新しい順 (最新)',
    sortOldest: '過去の順 (第1話から)',
    btnReadFirst: '第1話へ',
    btnReadLatest: '最新話へ',
    btnBack: '← ほかのプロジェクトを選択',
    btnReadPost: '記事を読む →',
    btnExploreProject: '開発日誌を見る',
    btnUpcoming: '作成予定',
    emptyNotice: 'このカテゴリの投稿は準備中です。',
    projects: [
      {
        id: 'stanford_cs329a',
        name: 'スタンフォード CS329A',
        badgeType: 'active',
        category: 'AIエージェント / 機械学習',
        icon: 'stanford_cs329a',
        subtitle: 'スタンフォード大学 自己進化AIエージェント講義シリーズ',
        description:
          '次世代フロンティアAIの中核パラダイム。推論時計算スケーリング、プロセス報酬モデル（PRM）、MCTS探索計画、DeepSeek GRPO強化学習、Sakana AI ScientistおよびDeepMind AlphaEvolveオープンエンド進化、Lean 4形式検証、VLAロボティクスなど全17講義を徹底解説。',
        techTags: ['Stanford CS329A', 'Self-Improving AI', 'MCTS', 'GRPO', 'PRM', 'VLA'],
        hasPosts: true,
      },
      {
        id: 'stanford_cs146s',
        name: 'スタンフォード CS146S',
        badgeType: 'active',
        category: 'ソフトウェア工学 / AIエージェント',
        icon: 'stanford_cs146s',
        subtitle: 'スタンフォード大学 現代ソフトウェア開発者講義シリーズ',
        description:
          '手動コーディングからAIエージェント指揮者への大転換。仕様駆動開発（SDD）、ループエンジニアリング、モデルコンテキストプロトコル（MCP）の完全解説。',
        techTags: ['Stanford CS146S', 'Agentic Workflows', 'Spec-Driven', 'MCP', 'CI/CD'],
        hasPosts: true,
      },
      {
        id: 'maeumjigi',
        name: 'マウムジギ (Maeumjigi)',
        badgeType: 'active',
        category: '卒業研究 / AIチャットボット',
        icon: 'maeumjigi',
        subtitle: 'AI自殺予防カウンセリングチャットボット開発日誌',
        description:
          'うつや高リスクの危機的発話をリアルタイムで検知し、共感型カウンセリングを行うAIチャットボット。Llama 3.1ファインチューニング（感情2:日常1の黄金比）、Safety Wrapperガードレール、AWS EC2 GPUサーバーデプロイ。',
        techTags: ['PyTorch', 'Llama 3.1', 'Safety Wrapper', 'FastAPI', 'AWS EC2', 'CapDe'],
        hasPosts: true,
      },
      {
        id: 'anpr_vision',
        name: 'Blackbox ANPR＆車線侵犯検知',
        badgeType: 'active',
        category: 'コンピュータビジョン / ITS',
        icon: 'anpr_vision',
        subtitle: 'リアルタイム車線侵犯検知および超解像ナンバープレート認識システム',
        description:
          'ドラレコ映像から車線侵犯車両を検知(IoU)し、EDSR_x4深層超解像で低解像度ナンバープレートを復元、EasyOCRと多数決投票(Majority Voting)で高精度認識を行うビジョンパイプライン(v01~v11).',
        techTags: ['OpenCV', 'YOLOv5', 'EDSR (SR)', 'CSRT Tracker', 'EasyOCR', 'PyTorch'],
        hasPosts: true,
      },
      {
        id: 'rl_q_learning',
        name: 'RL Q-Learning',
        badgeType: 'active',
        category: '強化学習 / ロボティクス',
        icon: 'rl_q_learning',
        subtitle: 'Webots Q-Learning 自律走行ロボットプロジェクト',
        description:
          'Webotsシミュレーション環境におけるQ-Tableの最適化と自律走行を探求する強化学習プロジェクト。648状態空間の離散化、ソケットIPC通信、実機Arduinoロボットへの移行計画。',
        techTags: ['Python', 'Webots', 'Q-Learning', 'NumPy', 'Socket IPC', 'Arduino'],
        hasPosts: true,
      },
      {
        id: 'security',
        name: 'セキュリティ＆ウェブ工学',
        badgeType: 'active',
        category: 'Webセキュリティ / DevSecOps',
        icon: 'security',
        subtitle: '静적サイト深層セキュリティ強化とサプライチェーン防御',
        description:
          '45件のnpm脆弱性警告に対する実行時脅威モデリング、Gitシークレットスキャン、個人情報(PII)保護、Referrer Policy適用および自動セキュリティパイプライン構築。',
        techTags: ['npm audit', 'SSG Hardening', 'DevSecOps', 'Threat Modeling', 'CI/CD'],
        hasPosts: true,
      },
      {
        id: 'ai_research',
        name: 'AI Research & Tools',
        badgeType: 'upcoming',
        upcomingBadgeText: 'Planned · 研究ノート',
        category: '開発ツール / AIエージェント',
        icon: 'ai_research',
        subtitle: '自律型コーディングエージェント＆LLM応用研究',
        description:
          'Antigravity CLIのカスタマイズ、エージェントオーケストレーション、プロンプトエンジニアリング、開発者生産性向上ツールの構築記録。',
        techTags: ['Antigravity', 'Agentic AI', 'Prompt Engineering', 'TypeScript'],
        hasPosts: false,
      },
    ],
  },
  es: {
    hubTitle: 'Proyectos y Diarios de Desarrollo',
    hubSubtitle: 'Selecciona un proyecto para explorar los diarios de desarrollo y los hitos técnicos.',
    tabHub: 'Panel de Proyectos',
    tabCs329a: 'Stanford CS329A',
    tabStanford: 'Stanford CS146S',
    tabMaeumjigi: 'Maeumjigi',
    tabAnpr: 'ANPR e Invasión',
    tabRl: 'RL Q-Learning',
    tabSecurity: 'Seguridad e Infra',
    tabAll: 'Todos los Posts',
    bannerCs329aTitle: 'Proyecto: Stanford CS329A (Agentes de IA Autoelevados)',
    bannerCs329aDesc: 'Agentes de IA autónomos con automejora: escalado de cómputo en inferencia, modelos de recompensa de procesos (PRM), búsqueda en árbol MCTS, RL con GRPO, evolución abierta de código y robótica VLA',
    bannerStanfordTitle: 'Proyecto: Stanford CS146S (El Desarrollador de Software Moderno)',
    bannerStanfordDesc: 'Ingeniería de software en la era de los agentes de IA: Desarrollo Guiado por Especificaciones (SDD), Loop Engineering y MCP',
    bannerMaeumjigiTitle: 'Proyecto: Maeumjigi (Diario de Desarrollo Capstone)',
    bannerMaeumjigiDesc: 'Ajuste fino de chatbot de IA para prevención del suicidio y desarrollo de Safety Wrapper',
    bannerAnprTitle: 'Proyecto: Blackbox ANPR e Invasión de Carril',
    bannerAnprDesc: 'Detección en tiempo real de invasión de carril y reconocimiento de matrículas con superresolución profunda (EDSR)',
    bannerRlTitle: 'Proyecto: RL Q-Learning (Robot Autónomo en Webots)',
    bannerRlDesc: 'Diarios de desarrollo de robot autónomo Q-Learning con espacio de 648 estados en Webots',
    bannerSecurityTitle: 'Proyecto: Seguridad e Ingeniería Web',
    bannerSecurityDesc: 'Blindaje de seguridad en sitios estáticos, modelado de amenazas y defensa de la cadena npm',
    bannerAllTitle: 'Todos los Diarios de Desarrollo',
    bannerAllDesc: 'Publicaciones de todos los proyectos ordenadas según tu preferencia.',
    sortNewest: 'Más recientes primero',
    sortOldest: 'Desde el inicio (Ep. 1)',
    btnReadFirst: 'Iniciar Ep. 1',
    btnReadLatest: 'Último Ep.',
    btnBack: '← Seleccionar otro proyecto',
    btnReadPost: 'Leer Artículo →',
    btnExploreProject: 'Ver Diarios de Desarrollo',
    btnUpcoming: 'Próximamente',
    emptyNotice: 'Las publicaciones de esta categoría se están preparando.',
    projects: [
      {
        id: 'stanford_cs329a',
        name: 'Stanford CS329A',
        badgeType: 'active',
        category: 'Agentes de IA / Aprendizaje Automático',
        icon: 'stanford_cs329a',
        subtitle: 'Serie Completa de Conferencias de Stanford sobre Agentes de IA Autoelevados',
        description:
          'La frontera definitiva de la IA autónoma. Desglose exhaustivo del escalado de cómputo en inferencia, modelos de recompensa de procesos (PRM), planificación de árbol MCTS, RL con GRPO, evolución abierta de código con AI Scientist y AlphaEvolve, verificación formal en Lean 4 y robótica VLA a lo largo de las 17 conferencias.',
        techTags: ['Stanford CS329A', 'Self-Improving AI', 'MCTS', 'GRPO', 'PRM', 'VLA'],
        hasPosts: true,
      },
      {
        id: 'stanford_cs146s',
        name: 'Stanford CS146S',
        badgeType: 'active',
        category: 'Ingeniería de Software / Agentes de IA',
        icon: 'stanford_cs146s',
        subtitle: 'Serie El Desarrollador de Software Moderno de Stanford',
        description:
          'El cambio de paradigma de escribir código a orquestar agentes. Desgloses de Desarrollo Guiado por Especificaciones (SDD), Loop Engineering y Model Context Protocol (MCP).',
        techTags: ['Stanford CS146S', 'Agentic Workflows', 'Spec-Driven', 'MCP', 'CI/CD'],
        hasPosts: true,
      },
      {
        id: 'maeumjigi',
        name: 'Maeumjigi',
        badgeType: 'active',
        category: 'Diseño Capstone / Chatbot de IA',
        icon: 'maeumjigi',
        subtitle: 'Diario de Desarrollo de Chatbot de IA para Prevención del Suicidio',
        description:
          'Detección en tiempo real de crisis y depresión con asesoramiento empático. Ajuste fino de Llama 3.1 (proporción 2:1 emocional y cotidiana), guardarraíles Safety Wrapper y despliegue en GPU de AWS EC2.',
        techTags: ['PyTorch', 'Llama 3.1', 'Safety Wrapper', 'FastAPI', 'AWS EC2', 'CapDe'],
        hasPosts: true,
      },
      {
        id: 'anpr_vision',
        name: 'Blackbox ANPR e Invasión de Carril',
        badgeType: 'active',
        category: 'Visión por Computadora / ITS',
        icon: 'anpr_vision',
        subtitle: 'Detección de Invasión de Carril en Tiempo Real y Sistema ANPR con Superresolución',
        description:
          'Detección en tiempo real de invasión de carril (IoU) en grabaciones de caja negra, restauración de matrículas borrosas con superresolución EDSR_x4 y votación temporal mayoritaria con EasyOCR (v01 a v11).',
        techTags: ['OpenCV', 'YOLOv5', 'EDSR (SR)', 'CSRT Tracker', 'EasyOCR', 'PyTorch'],
        hasPosts: true,
      },
      {
        id: 'rl_q_learning',
        name: 'RL Q-Learning',
        badgeType: 'active',
        category: 'Aprendizaje por Refuerzo / Robótica',
        icon: 'rl_q_learning',
        subtitle: 'Proyecto de Robot Autónomo con Q-Learning en Webots',
        description:
          'Optimización de Q-Table y navegación autónoma en entornos de simulación Webots. Discretización de espacio de estados (648 bins), comunicación IPC por sockets y transferencia Sim-to-Real a hardware.',
        techTags: ['Python', 'Webots', 'Q-Learning', 'NumPy', 'Socket IPC', 'Arduino'],
        hasPosts: true,
      },
      {
        id: 'security',
        name: 'Seguridad e Ingeniería Web',
        badgeType: 'active',
        category: 'Seguridad Web / DevSecOps',
        icon: 'security',
        subtitle: 'Blindaje de Seguridad en Sitios Estáticos y Defensa npm',
        description:
          'Modelado de amenazas de 45 vulnerabilidades en npm audit para sitios estáticos, escaneo de secretos git, protección de PII, políticas Referrer y pipeline de verificación continua.',
        techTags: ['npm audit', 'SSG Hardening', 'DevSecOps', 'Threat Modeling', 'CI/CD'],
        hasPosts: true,
      },
      {
        id: 'ai_research',
        name: 'AI Research & Tools',
        badgeType: 'upcoming',
        upcomingBadgeText: 'Planificado',
        category: 'Herramientas de Desarrollador / Agentes de IA',
        icon: 'ai_research',
        subtitle: 'IA Agéntica y Flujos de Desarrollo',
        description:
          'Personalización de Antigravity CLI, orquestación de agentes, ingeniería de prompts y herramientas de productividad para desarrolladores.',
        techTags: ['Antigravity', 'Agentic AI', 'Prompt Engineering', 'TypeScript'],
        hasPosts: false,
      },
    ],
  },
};

function formatCount(count: number, locale: SupportedLocale): string {
  if (locale === 'ko') return `${count}편`;
  if (locale === 'ja') return `${count}編`;
  return `${count} ${count === 1 ? 'Post' : 'Posts'}`;
}

function getEpisodeNumber(permalink: string): number {
  const m = permalink.match(/(?:maeumjigi|vision-anpr|rl-qlearning|stanford-cs146s|stanford-cs329a)-(\d+)/);
  return m ? parseInt(m[1], 10) : 999;
}

function getItemDate(item: any): string {
  if (item.date) {
    const str = String(item.date);
    const m = str.match(/^(\d{4}-\d{2}-\d{2})/);
    if (m) return m[1];
    return str.split('T')[0];
  }
  const m = item.permalink ? item.permalink.match(/(\d{4}-\d{2}-\d{2})/) : null;
  return m ? m[1] : '';
}

function BlogListPageMetadata(props: any) {
  const { metadata } = props;
  const {
    siteConfig: { title: siteTitle },
  } = useDocusaurusContext();
  const { blogDescription, blogTitle, permalink } = metadata;
  const isBlogOnlyMode = permalink === '/';
  const title = isBlogOnlyMode ? siteTitle : blogTitle;
  return (
    <>
      <PageMetadata title={title} description={blogDescription} />
      <SearchMetadata tag="blog_posts_list" />
    </>
  );
}

function ProjectHubView({
  projects,
  postCounts,
  locale,
  btnExploreProject,
  btnUpcoming,
  onSelectProject,
}: {
  projects: ProjectInfo[];
  postCounts: Record<string, number>;
  locale: SupportedLocale;
  btnExploreProject: string;
  btnUpcoming: string;
  onSelectProject: (id: string) => void;
}) {
  return (
    <div className={styles.projectHubContainer}>
      <div className={styles.projectGrid}>
        {projects.map((proj) => {
          const count = postCounts[proj.id] || 0;
          const countFormatted = formatCount(count, locale);
          const badgeText = proj.hasPosts
            ? `Active · ${countFormatted}`
            : (proj.upcomingBadgeText || 'Planned');

          const actionText = proj.hasPosts
            ? `${btnExploreProject} (${countFormatted}) →`
            : btnUpcoming;

          return (
            <div key={proj.id} className={styles.projectCard}>
              <div className={styles.cardTop}>
                <div className={styles.badgeRow}>
                  <span
                    className={clsx(
                      styles.badgeStatus,
                      proj.badgeType === 'active' ? styles.badgeActive : styles.badgeUpcoming
                    )}
                  >
                    {badgeText}
                  </span>
                  <span className={styles.categoryLabel}>{proj.category}</span>
                </div>
                <div className={styles.projectIconTitle}>
                  <span className={styles.projectIcon}>
                    <ProjectIcon id={proj.id} size={28} />
                  </span>
                  <h3 className={styles.projectTitle}>{proj.name}</h3>
                </div>
                <div className={styles.projectSubtitle}>{proj.subtitle}</div>
                <p className={styles.projectDescription}>{proj.description}</p>
                <div className={styles.techTags}>
                  {proj.techTags.map((tag) => (
                    <span key={tag} className={styles.techTag}>
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
              <div className={styles.cardAction}>
                {proj.hasPosts ? (
                  <a
                    href={`#${proj.id}`}
                    className={styles.btnPrimary}
                    onClick={(e) => {
                      e.preventDefault();
                      onSelectProject(proj.id);
                    }}
                  >
                    {actionText}
                  </a>
                ) : (
                  <button type="button" className={styles.btnDisabled} disabled>
                    {actionText}
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function BlogListPageContent(props: any) {
  const { metadata, sidebar } = props;
  const {
    i18n: { currentLocale },
  } = useDocusaurusContext();

  const locale = (currentLocale as SupportedLocale) in I18N_DATA
    ? (currentLocale as SupportedLocale)
    : 'en';
  const content = I18N_DATA[locale];

  const isFirstPage = metadata.page === 1;

  // Active tab state
  const [activeTab, setActiveTab] = useState<
    'hub' | 'stanford_cs329a' | 'stanford_cs146s' | 'maeumjigi' | 'rl_q_learning' | 'anpr_vision' | 'security' | 'all'
  >(isFirstPage ? 'hub' : 'all');

  // Sort order: 'asc' (oldest first) | 'desc' (newest first)
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const hash = window.location.hash.replace('#', '').toLowerCase();
      if (hash === 'stanford_cs329a' || hash === 'cs329a' || hash === 'stanford-cs329a') {
        setActiveTab('stanford_cs329a');
      } else if (hash === 'stanford_cs146s' || hash === 'stanford' || hash === 'cs146s' || hash === 'stanford-cs146s') {
        setActiveTab('stanford_cs146s');
      } else if (hash === 'maeumjigi') {
        setActiveTab('maeumjigi');
      } else if (hash === 'rl_q_learning' || hash === 'rl') {
        setActiveTab('rl_q_learning');
      } else if (hash === 'anpr_vision' || hash === 'anpr' || hash === 'cv') {
        setActiveTab('anpr_vision');
      } else if (hash === 'security' || hash === 'infra') {
        setActiveTab('security');
      } else if (hash === 'all') {
        setActiveTab('all');
      } else if (hash === 'hub' || hash === 'projects') {
        setActiveTab('hub');
      }
    }
  }, []);

  const handleSelectTab = (
    tab: 'hub' | 'stanford_cs329a' | 'stanford_cs146s' | 'maeumjigi' | 'rl_q_learning' | 'anpr_vision' | 'security' | 'all'
  ) => {
    setActiveTab(tab);
    if (typeof window !== 'undefined') {
      window.location.hash = tab === 'hub' ? 'projects' : tab;
    }
  };

  const allSidebarItems = sidebar?.items || [];

  const isSecurity = (item: any) =>
    item.permalink.includes('security') ||
    item.permalink.includes('static-site') ||
    item.permalink.includes('custom-domain') ||
    item.permalink.includes('cloudflare') ||
    item.permalink.includes('adsense');

  // Compute dynamic counts for each project
  const postCounts = useMemo(() => {
    return {
      stanford_cs329a: allSidebarItems.filter((item: any) => item.permalink.includes('stanford-cs329a')).length,
      stanford_cs146s: allSidebarItems.filter((item: any) => item.permalink.includes('stanford-cs146s')).length,
      maeumjigi: allSidebarItems.filter((item: any) => item.permalink.includes('maeumjigi')).length,
      anpr_vision: allSidebarItems.filter((item: any) => item.permalink.includes('vision-anpr')).length,
      rl_q_learning: allSidebarItems.filter((item: any) => item.permalink.includes('rl-qlearning')).length,
      security: allSidebarItems.filter(isSecurity).length,
    };
  }, [allSidebarItems]);

  // Filter and sort posts for the active project
  const projectPosts = useMemo(() => {
    let list: any[] = [];
    if (activeTab === 'stanford_cs329a') {
      list = allSidebarItems.filter((item: any) => item.permalink.includes('stanford-cs329a'));
    } else if (activeTab === 'stanford_cs146s') {
      list = allSidebarItems.filter((item: any) => item.permalink.includes('stanford-cs146s'));
    } else if (activeTab === 'maeumjigi') {
      list = allSidebarItems.filter((item: any) => item.permalink.includes('maeumjigi'));
    } else if (activeTab === 'rl_q_learning') {
      list = allSidebarItems.filter((item: any) => item.permalink.includes('rl-qlearning'));
    } else if (activeTab === 'anpr_vision') {
      list = allSidebarItems.filter((item: any) => item.permalink.includes('vision-anpr'));
    } else if (activeTab === 'security') {
      list = allSidebarItems.filter(isSecurity);
    } else if (activeTab === 'all') {
      list = allSidebarItems;
    }

    const sorted = [...list].sort((a: any, b: any) => {
      const epA = getEpisodeNumber(a.permalink);
      const epB = getEpisodeNumber(b.permalink);
      if (epA !== 999 && epB !== 999) {
        return sortOrder === 'asc' ? epA - epB : epB - epA;
      }
      const dateA = getItemDate(a);
      const dateB = getItemDate(b);
      return sortOrder === 'asc' ? dateA.localeCompare(dateB) : dateB.localeCompare(dateA);
    });

    return sorted;
  }, [allSidebarItems, activeTab, sortOrder]);

  // Determine first and latest episode links for quick navigation
  const sortedAscending = useMemo(() => {
    return [...projectPosts].sort((a: any, b: any) => {
      const epA = getEpisodeNumber(a.permalink);
      const epB = getEpisodeNumber(b.permalink);
      if (epA !== 999 && epB !== 999) return epA - epB;
      return getItemDate(a).localeCompare(getItemDate(b));
    });
  }, [projectPosts]);

  const firstPostLink = sortedAscending.length > 0 ? sortedAscending[0].permalink : null;
  const latestPostLink =
    sortedAscending.length > 0
      ? sortedAscending[sortedAscending.length - 1].permalink
      : null;

  return (
    <BlogLayout sidebar={sidebar}>
      {/* Anchors for Hash Navigation & Docusaurus Link Validation */}
      <span id="projects" aria-hidden="true" />
      <span id="stanford_cs329a" aria-hidden="true" />
      <span id="cs329a" aria-hidden="true" />
      <span id="stanford-cs329a" aria-hidden="true" />
      <span id="stanford_cs146s" aria-hidden="true" />
      <span id="stanford" aria-hidden="true" />
      <span id="cs146s" aria-hidden="true" />
      <span id="maeumjigi" aria-hidden="true" />
      <span id="anpr_vision" aria-hidden="true" />
      <span id="rl_q_learning" aria-hidden="true" />
      <span id="security" aria-hidden="true" />
      <span id="all" aria-hidden="true" />

      {/* Top Navigation & Hub Header */}
      <div className={styles.hubHeader}>
        <h1 className={styles.hubTitle}>{content.hubTitle}</h1>
        <p className={styles.hubSubtitle}>{content.hubSubtitle}</p>

        {/* Tab Switcher with Dynamic Counts */}
        <div className={styles.tabBar}>
          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'hub' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('hub')}
          >
            {content.tabHub}
          </button>
          <button
            type="button"
            className={clsx(
              styles.tabButton,
              activeTab === 'stanford_cs329a' && styles.tabButtonActive
            )}
            onClick={() => handleSelectTab('stanford_cs329a')}
          >
            {`${content.tabCs329a} (${formatCount(postCounts.stanford_cs329a, locale)})`}
          </button>
          <button
            type="button"
            className={clsx(
              styles.tabButton,
              activeTab === 'stanford_cs146s' && styles.tabButtonActive
            )}
            onClick={() => handleSelectTab('stanford_cs146s')}
          >
            {`${content.tabStanford} (${formatCount(postCounts.stanford_cs146s, locale)})`}
          </button>
          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'maeumjigi' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('maeumjigi')}
          >
            {`${content.tabMaeumjigi} (${formatCount(postCounts.maeumjigi, locale)})`}
          </button>
          <button
            type="button"
            className={clsx(
              styles.tabButton,
              activeTab === 'anpr_vision' && styles.tabButtonActive
            )}
            onClick={() => handleSelectTab('anpr_vision')}
          >
            {`${content.tabAnpr} (${formatCount(postCounts.anpr_vision, locale)})`}
          </button>
          <button
            type="button"
            className={clsx(
              styles.tabButton,
              activeTab === 'rl_q_learning' && styles.tabButtonActive
            )}
            onClick={() => handleSelectTab('rl_q_learning')}
          >
            {`${content.tabRl} (${formatCount(postCounts.rl_q_learning, locale)})`}
          </button>
          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'security' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('security')}
          >
            {`${content.tabSecurity} (${formatCount(postCounts.security, locale)})`}
          </button>
          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'all' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('all')}
          >
            {`${content.tabAll} (${formatCount(allSidebarItems.length, locale)})`}
          </button>
        </div>
      </div>

      {/* Hub Mode (Project Selection Grid & SSR Crawlable Directory) */}
      {activeTab === 'hub' && (
        <>
          <ProjectHubView
            projects={content.projects}
            postCounts={postCounts}
            locale={locale}
            btnExploreProject={content.btnExploreProject}
            btnUpcoming={content.btnUpcoming}
            onSelectProject={(id) => handleSelectTab(id as any)}
          />
          <div style={{ marginTop: '2.5rem', borderTop: '1px solid var(--ifm-color-emphasis-200)', paddingTop: '1.5rem' }}>
            <h3 style={{ fontSize: '1.1rem', marginBottom: '1rem', color: 'var(--ifm-color-emphasis-800)' }}>
              {locale === 'ko'
                ? `전체 기술 일지 및 아티클 목차 (${allSidebarItems.length}편)`
                : locale === 'ja'
                ? `全開発日誌・技術記事目次 (${allSidebarItems.length}編)`
                : locale === 'es'
                ? `Índice de Diarios y Artículos (${allSidebarItems.length} Posts)`
                : `All Engineering Logs & Articles Index (${allSidebarItems.length} Posts)`}
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '0.6rem' }}>
              {allSidebarItems.map((item: any) => (
                <a
                  key={item.permalink}
                  href={item.permalink}
                  style={{
                    display: 'block',
                    padding: '0.5rem 0.75rem',
                    borderRadius: '6px',
                    backgroundColor: 'var(--ifm-card-background-color, var(--ifm-color-emphasis-100))',
                    fontSize: '0.85rem',
                    textDecoration: 'none',
                    color: 'var(--ifm-color-emphasis-800)',
                    border: '1px solid var(--ifm-color-emphasis-200)',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}
                  title={item.title}
                >
                  {item.title}
                </a>
              ))}
            </div>
          </div>
        </>
      )}

      {/* Project View (Full Episode Grid with Sorting) */}
      {activeTab !== 'hub' && (
        <>
          {/* Banner */}
          <div className={styles.activeProjectBanner}>
            <div>
              <h3 className={styles.bannerTitle}>
                {activeTab === 'stanford_cs329a'
                  ? `${content.bannerCs329aTitle} (${formatCount(postCounts.stanford_cs329a, locale)})`
                  : activeTab === 'stanford_cs146s'
                  ? `${content.bannerStanfordTitle} (${formatCount(postCounts.stanford_cs146s, locale)})`
                  : activeTab === 'maeumjigi'
                  ? `${content.bannerMaeumjigiTitle} (${formatCount(postCounts.maeumjigi, locale)})`
                  : activeTab === 'anpr_vision'
                  ? `${content.bannerAnprTitle} (${formatCount(postCounts.anpr_vision, locale)})`
                  : activeTab === 'rl_q_learning'
                  ? `${content.bannerRlTitle} (${formatCount(postCounts.rl_q_learning, locale)})`
                  : activeTab === 'security'
                  ? `${content.bannerSecurityTitle} (${formatCount(postCounts.security, locale)})`
                  : `${content.bannerAllTitle} (${formatCount(allSidebarItems.length, locale)})`}
              </h3>
              <p className={styles.bannerDesc}>
                {activeTab === 'stanford_cs329a'
                  ? content.bannerCs329aDesc
                  : activeTab === 'stanford_cs146s'
                  ? content.bannerStanfordDesc
                  : activeTab === 'maeumjigi'
                  ? content.bannerMaeumjigiDesc
                  : activeTab === 'anpr_vision'
                  ? content.bannerAnprDesc
                  : activeTab === 'rl_q_learning'
                  ? content.bannerRlDesc
                  : activeTab === 'security'
                  ? content.bannerSecurityDesc
                  : content.bannerAllDesc}
              </p>
            </div>
            <button
              type="button"
              className={styles.backButton}
              onClick={() => handleSelectTab('hub')}
            >
              {content.btnBack}
            </button>
          </div>

          {/* Sort & Quick Actions Control Bar */}
          <div className={styles.sortBar}>
            <div className={styles.sortButtonsGroup}>
              <button
                type="button"
                className={clsx(
                  styles.sortButton,
                  sortOrder === 'asc' && styles.sortButtonActive
                )}
                onClick={() => setSortOrder('asc')}
              >
                {content.sortOldest}
              </button>
              <button
                type="button"
                className={clsx(
                  styles.sortButton,
                  sortOrder === 'desc' && styles.sortButtonActive
                )}
                onClick={() => setSortOrder('desc')}
              >
                {content.sortNewest}
              </button>
            </div>

            {/* Quick Action Navigation Links */}
            <div className={styles.quickActionsGroup}>
              {firstPostLink && (
                <Link to={firstPostLink} className={styles.quickActionBtn}>
                  {content.btnReadFirst}
                </Link>
              )}
              {latestPostLink && latestPostLink !== firstPostLink && (
                <Link to={latestPostLink} className={styles.quickActionBtn}>
                  {content.btnReadLatest}
                </Link>
              )}
            </div>
          </div>

          {/* Episode Cards Grid */}
          {projectPosts.length > 0 ? (
            <div className={styles.episodeGrid}>
              {projectPosts.map((post: any) => {
                const epNum = getEpisodeNumber(post.permalink);
                const date = getItemDate(post);

                return (
                  <Link
                    key={post.permalink}
                    to={post.permalink}
                    className={styles.episodeCard}
                  >
                    <div>
                      <div className={styles.episodeHeader}>
                        {epNum !== 999 ? (
                          <span className={styles.episodeBadge}>EP. {epNum}</span>
                        ) : (
                          <span className={styles.episodeBadge}>TECH</span>
                        )}
                        {date && <span className={styles.episodeDate}>{date}</span>}
                      </div>
                      <h4 className={styles.episodeTitle}>{post.title}</h4>
                    </div>
                    <div className={styles.episodeFooter}>
                      <span className={styles.readMoreText}>{content.btnReadPost}</span>
                    </div>
                  </Link>
                );
              })}
            </div>
          ) : (
            <div className={styles.emptyNotice}>
              <div className={styles.emptyIcon}>
                <ProjectIcon id="folder" size={36} />
              </div>
              <p>{content.emptyNotice}</p>
            </div>
          )}
        </>
      )}
    </BlogLayout>
  );
}

export default function BlogListPage(props: any) {
  return (
    <HtmlClassNameProvider
      className={clsx(
        ThemeClassNames.wrapper.blogPages,
        ThemeClassNames.page.blogListPage
      )}
    >
      <BlogListPageMetadata {...props} />
      <BlogListPageStructuredData {...props} />
      <BlogListPageContent {...props} />
    </HtmlClassNameProvider>
  );
}
