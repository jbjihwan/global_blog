import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {
  PageMetadata,
  HtmlClassNameProvider,
  ThemeClassNames,
} from '@docusaurus/theme-common';
import BlogLayout from '@theme/BlogLayout';
import BlogListPaginator from '@theme/BlogListPaginator';
import SearchMetadata from '@theme/SearchMetadata';
import BlogPostItems from '@theme/BlogPostItems';
import BlogListPageStructuredData from '@theme/BlogListPage/StructuredData';
import styles from './styles.module.css';

type SupportedLocale = 'en' | 'ko' | 'ja' | 'es';

interface ProjectInfo {
  id: string;
  name: string;
  badge: string;
  badgeType: 'active' | 'upcoming';
  category: string;
  icon: string;
  subtitle: string;
  description: string;
  techTags: string[];
  postCountText: string;
  hasPosts: boolean;
}

interface LocaleContent {
  hubTitle: string;
  hubSubtitle: string;
  tabHub: string;
  tabMaeumjigi: string;
  tabRl: string;
  tabAll: string;
  bannerMaeumjigiTitle: string;
  bannerMaeumjigiDesc: string;
  bannerRlTitle: string;
  bannerRlDesc: string;
  bannerAllTitle: string;
  bannerAllDesc: string;
  btnBack: string;
  projects: ProjectInfo[];
}

const I18N_DATA: Record<SupportedLocale, LocaleContent> = {
  ko: {
    hubTitle: '🚀 프로젝트 & 개발 일지',
    hubSubtitle: '관심 있는 프로젝트를 선택하여 개발 여정과 기술 기록을 확인해보세요.',
    tabHub: '📂 프로젝트 선택 허브',
    tabMaeumjigi: '🧠 마음지기 (23편)',
    tabRl: '🤖 RL Q-Learning (5편)',
    tabAll: '📑 전체 글 피드',
    bannerMaeumjigiTitle: '🏷️ 프로젝트: 마음지기 (Maeumjigi Capstone Dev Log)',
    bannerMaeumjigiDesc: 'AI 자살 예방 상담 챗봇 파인튜닝 및 가드레일 개발 일지 (총 23회차)',
    bannerRlTitle: '🏷️ 프로젝트: RL Q-Learning (Webots 자율주행 로봇)',
    bannerRlDesc: 'Webots 물리 시뮬레이션 기반 648개 상태 공간 Q-Learning 로봇 주행 개발일지',
    bannerAllTitle: '🏷️ 전체 개발 일지 피드',
    bannerAllDesc: '모든 프로젝트의 글이 최신순으로 표시됩니다.',
    btnBack: '← 다른 프로젝트 선택',
    projects: [
      {
        id: 'maeumjigi',
        name: '마음지기 (Maeumjigi)',
        badge: 'Active · 23 Posts',
        badgeType: 'active',
        category: '캡스톤디자인 / AI 챗봇',
        icon: '🧠',
        subtitle: 'AI 자살 예방 상담 챗봇 캡스톤 개발일지',
        description:
          '우울 및 고위험 위기 발화를 실시간 감지하고 공감 상담을 수행하는 AI 챗봇. Llama 3.1 파인튜닝 (2:1 감성:일상 황금 비율), Safety Wrapper 가드레일, AWS EC2 GPU 서버 배포기.',
        techTags: ['PyTorch', 'Llama 3.1', 'Safety Wrapper', 'FastAPI', 'AWS EC2', 'CapDe'],
        postCountText: '개발일지 보러가기 (23편) →',
        hasPosts: true,
      },
      {
        id: 'rl_q_learning',
        name: 'RL Q-Learning',
        badge: 'Active · 5편',
        badgeType: 'active',
        category: '강화학습 / 로보틱스',
        icon: '🤖',
        subtitle: 'Webots Q-Learning 자율주행 로봇 프로젝트',
        description:
          'Webots 시뮬레이터 환경에서 에이전트의 Q-Table 최적화 및 자율주행을 탐구하는 강화학습 프로젝트. 648개 이산 상태 공간 설계, 소켓 IPC 통신, 실제 Arduino 로봇 전이 기획.',
        techTags: ['Python', 'Webots', 'Q-Learning', 'NumPy', 'Socket IPC', 'Arduino'],
        postCountText: '개발일지 보러가기 (5편) →',
        hasPosts: true,
      },
      {
        id: 'ai_research',
        name: 'AI Research & Tools',
        badge: 'Planned · 연구 노트',
        badgeType: 'upcoming',
        category: '개발 도구 / AI 에이전트',
        icon: '⚡',
        subtitle: '자율 코딩 에이전트 및 LLM 응용 연구',
        description:
          'Antigravity CLI 커스터마이징, 에이전트 오케스트레이션, 프롬프트 엔지니어링 및 개발 생산성 극대화 도구 제작 기록.',
        techTags: ['Antigravity', 'Agentic AI', 'Prompt Engineering', 'TypeScript'],
        postCountText: '작성 예정 ⏳',
        hasPosts: false,
      },
    ],
  },
  en: {
    hubTitle: '🚀 Projects & Dev Logs',
    hubSubtitle: 'Select a project to explore dev logs and technical milestones.',
    tabHub: '📂 Project Selection Hub',
    tabMaeumjigi: '🧠 Maeumjigi (23 Posts)',
    tabRl: '🤖 RL Q-Learning (5 Posts)',
    tabAll: '📑 All Posts Feed',
    bannerMaeumjigiTitle: '🏷️ Project: Maeumjigi (Capstone Dev Log)',
    bannerMaeumjigiDesc:
      'AI Suicide Prevention Counseling Chatbot Fine-tuning & Safety Wrapper Dev Log (23 Episodes)',
    bannerRlTitle: '🏷️ Project: RL Q-Learning (Webots Autonomous Robot)',
    bannerRlDesc: 'Webots physics-based 648-bin state space Q-learning autonomous robot dev logs',
    bannerAllTitle: '🏷️ All Dev Logs Feed',
    bannerAllDesc: 'Chronological feed of all posts across all projects.',
    btnBack: '← Select Another Project',
    projects: [
      {
        id: 'maeumjigi',
        name: 'Maeumjigi',
        badge: 'Active · 23 Posts',
        badgeType: 'active',
        category: 'Capstone Design / AI Chatbot',
        icon: '🧠',
        subtitle: 'AI Suicide Prevention Counseling Chatbot Dev Log',
        description:
          'Real-time crisis & depression detection with compassionate counseling. Llama 3.1 fine-tuning (2:1 emotional-to-daily ratio), Safety Wrapper guardrails, and AWS EC2 GPU deployment.',
        techTags: ['PyTorch', 'Llama 3.1', 'Safety Wrapper', 'FastAPI', 'AWS EC2', 'CapDe'],
        postCountText: 'Explore Dev Logs (23 Posts) →',
        hasPosts: true,
      },
      {
        id: 'rl_q_learning',
        name: 'RL Q-Learning',
        badge: 'Active · 5 Posts',
        badgeType: 'active',
        category: 'Reinforcement Learning / Robotics',
        icon: '🤖',
        subtitle: 'Webots Q-Learning Autonomous Robot Project',
        description:
          'Q-Table optimization and autonomous navigation in Webots simulation environments. Continuous state discretization (648 bins), socket IPC communication, and Sim-to-Real hardware transfer.',
        techTags: ['Python', 'Webots', 'Q-Learning', 'NumPy', 'Socket IPC', 'Arduino'],
        postCountText: 'Explore Dev Logs (5 Posts) →',
        hasPosts: true,
      },
      {
        id: 'ai_research',
        name: 'AI Research & Tools',
        badge: 'Planned',
        badgeType: 'upcoming',
        category: 'Developer Tools / AI Agents',
        icon: '⚡',
        subtitle: 'Agentic AI & Custom Dev Workflows',
        description:
          'Customizing Antigravity CLI, agent orchestration, prompt engineering, and building developer productivity tools.',
        techTags: ['Antigravity', 'Agentic AI', 'Prompt Engineering', 'TypeScript'],
        postCountText: 'Coming Soon ⏳',
        hasPosts: false,
      },
    ],
  },
  ja: {
    hubTitle: '🚀 プロジェクト＆開発日誌',
    hubSubtitle: '関心のあるプロジェクトを選択して、開発の歩みと技術的な記録をご覧ください。',
    tabHub: '📂 プロジェクト選択ハブ',
    tabMaeumjigi: '🧠 マウムジギ (23編)',
    tabRl: '🤖 RL Q-Learning (5編)',
    tabAll: '📑 全記事フィード',
    bannerMaeumjigiTitle: '🏷️ プロジェクト: マウムジギ (卒業研究 開発日誌)',
    bannerMaeumjigiDesc:
      'AI自殺予防カウンセリングチャットボットのファインチューニングおよびガードレール開発日誌（全23回）',
    bannerRlTitle: '🏷️ プロジェクト: RL Q-Learning (Webots自律走行ロボット)',
    bannerRlDesc: 'Webots物理シミュレーションベースの648状態空間Q-Learning自律走行開発日誌',
    bannerAllTitle: '🏷️ 全開発日誌フィード',
    bannerAllDesc: 'すべてのプロジェクトの記事が最新順に表示されます。',
    btnBack: '← ほかのプロジェクトを選択',
    projects: [
      {
        id: 'maeumjigi',
        name: 'マウムジギ (Maeumjigi)',
        badge: 'Active · 23編',
        badgeType: 'active',
        category: '卒業研究 / AIチャットボット',
        icon: '🧠',
        subtitle: 'AI自殺予防カウンセリングチャットボット開発日誌',
        description:
          'うつや高リスクの危機的発話をリアルタイムで検知し、共感型カウンセリングを行うAIチャットボット。Llama 3.1ファインチューニング（感情2:日常1の黄金比）、Safety Wrapperガードレール、AWS EC2 GPUサーバーデプロイ。',
        techTags: ['PyTorch', 'Llama 3.1', 'Safety Wrapper', 'FastAPI', 'AWS EC2', 'CapDe'],
        postCountText: '開発日誌を見る (23編) →',
        hasPosts: true,
      },
      {
        id: 'rl_q_learning',
        name: 'RL Q-Learning',
        badge: 'Active · 5編',
        badgeType: 'active',
        category: '強化学習 / ロボティクス',
        icon: '🤖',
        subtitle: 'Webots Q-Learning 自律走行ロボットプロジェクト',
        description:
          'Webotsシミュレーション環境におけるQ-Tableの最適化と自律走行を探求する強化学習プロジェクト。648状態空間の離散化、ソケットIPC通信、実機Arduinoロボットへの移行計画。',
        techTags: ['Python', 'Webots', 'Q-Learning', 'NumPy', 'Socket IPC', 'Arduino'],
        postCountText: '開発日誌を見る (5編) →',
        hasPosts: true,
      },
      {
        id: 'ai_research',
        name: 'AI Research & Tools',
        badge: 'Planned · 研究ノート',
        badgeType: 'upcoming',
        category: '開発ツール / AIエージェント',
        icon: '⚡',
        subtitle: '自律型コーディングエージェント＆LLM応用研究',
        description:
          'Antigravity CLIのカスタマイズ、エージェントオーケストレーション、プロンプトエンジニアリング、開発者生産性向上ツールの構築記録。',
        techTags: ['Antigravity', 'Agentic AI', 'Prompt Engineering', 'TypeScript'],
        postCountText: '作成予定 ⏳',
        hasPosts: false,
      },
    ],
  },
  es: {
    hubTitle: '🚀 Proyectos y Diarios de Desarrollo',
    hubSubtitle: 'Selecciona un proyecto para explorar los diarios de desarrollo y los hitos técnicos.',
    tabHub: '📂 Panel de Proyectos',
    tabMaeumjigi: '🧠 Maeumjigi (23 Posts)',
    tabRl: '🤖 RL Q-Learning (5 Posts)',
    tabAll: '📑 Todos los Posts',
    bannerMaeumjigiTitle: '🏷️ Proyecto: Maeumjigi (Diario de Desarrollo Capstone)',
    bannerMaeumjigiDesc:
      'Ajuste fino de chatbot de IA para prevención del suicidio y desarrollo de Safety Wrapper (23 episodios)',
    bannerRlTitle: '🏷️ Proyecto: RL Q-Learning (Robot Autónomo en Webots)',
    bannerRlDesc: 'Diarios de desarrollo de robot autónomo Q-Learning con espacio de 648 estados en Webots',
    bannerAllTitle: '🏷️ Todos los Diarios de Desarrollo',
    bannerAllDesc: 'Publicaciones de todos los proyectos ordenadas cronológicamente.',
    btnBack: '← Seleccionar otro proyecto',
    projects: [
      {
        id: 'maeumjigi',
        name: 'Maeumjigi',
        badge: 'Activo · 23 Posts',
        badgeType: 'active',
        category: 'Diseño Capstone / Chatbot de IA',
        icon: '🧠',
        subtitle: 'Diario de Desarrollo de Chatbot de IA para Prevención del Suicidio',
        description:
          'Detección en tiempo real de crisis y depresión con asesoramiento empático. Ajuste fino de Llama 3.1 (proporción 2:1 emocional y cotidiana), guardarraíles Safety Wrapper y despliegue en GPU de AWS EC2.',
        techTags: ['PyTorch', 'Llama 3.1', 'Safety Wrapper', 'FastAPI', 'AWS EC2', 'CapDe'],
        postCountText: 'Ver Diarios de Desarrollo (23 Posts) →',
        hasPosts: true,
      },
      {
        id: 'rl_q_learning',
        name: 'RL Q-Learning',
        badge: 'Activo · 5 Posts',
        badgeType: 'active',
        category: 'Aprendizaje por Refuerzo / Robótica',
        icon: '🤖',
        subtitle: 'Proyecto de Robot Autónomo con Q-Learning en Webots',
        description:
          'Optimización de Q-Table y navegación autónoma en entornos de simulación Webots. Discretización de espacio de estados (648 bins), comunicación IPC por sockets y transferencia Sim-to-Real a hardware.',
        techTags: ['Python', 'Webots', 'Q-Learning', 'NumPy', 'Socket IPC', 'Arduino'],
        postCountText: 'Ver Diarios de Desarrollo (5 Posts) →',
        hasPosts: true,
      },
      {
        id: 'ai_research',
        name: 'AI Research & Tools',
        badge: 'Planificado',
        badgeType: 'upcoming',
        category: 'Herramientas de Desarrollador / Agentes de IA',
        icon: '⚡',
        subtitle: 'IA Agéntica y Flujos de Desarrollo',
        description:
          'Personalización de Antigravity CLI, orquestación de agentes, ingeniería de prompts y herramientas de productividad para desarrolladores.',
        techTags: ['Antigravity', 'Agentic AI', 'Prompt Engineering', 'TypeScript'],
        postCountText: 'Próximamente ⏳',
        hasPosts: false,
      },
    ],
  },
};

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
  onSelectProject,
}: {
  projects: ProjectInfo[];
  onSelectProject: (id: string) => void;
}) {
  return (
    <div className={styles.projectHubContainer}>
      <div className={styles.projectGrid}>
        {projects.map((proj) => (
          <div key={proj.id} className={styles.projectCard}>
            <div className={styles.cardTop}>
              <div className={styles.badgeRow}>
                <span
                  className={clsx(
                    styles.badgeStatus,
                    proj.badgeType === 'active' ? styles.badgeActive : styles.badgeUpcoming
                  )}
                >
                  {proj.badge}
                </span>
                <span className={styles.categoryLabel}>{proj.category}</span>
              </div>
              <div className={styles.projectIconTitle}>
                <span className={styles.projectIcon}>{proj.icon}</span>
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
                <button
                  type="button"
                  className={styles.btnPrimary}
                  onClick={() => onSelectProject(proj.id)}
                >
                  {proj.postCountText}
                </button>
              ) : (
                <button type="button" className={styles.btnDisabled} disabled>
                  {proj.postCountText}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function BlogListPageContent(props: any) {
  const { metadata, items, sidebar } = props;
  const {
    i18n: { currentLocale },
  } = useDocusaurusContext();

  const locale = (currentLocale as SupportedLocale) in I18N_DATA
    ? (currentLocale as SupportedLocale)
    : 'en';
  const content = I18N_DATA[locale];

  const isFirstPage = metadata.page === 1;

  // Determine initial view based on hash if in browser
  const [activeTab, setActiveTab] = useState<'hub' | 'maeumjigi' | 'rl_q_learning' | 'all'>(
    isFirstPage ? 'hub' : 'all'
  );

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const hash = window.location.hash.replace('#', '');
      if (hash === 'maeumjigi') {
        setActiveTab('maeumjigi');
      } else if (hash === 'rl_q_learning' || hash === 'rl') {
        setActiveTab('rl_q_learning');
      } else if (hash === 'all') {
        setActiveTab('all');
      } else if (hash === 'hub' || hash === 'projects') {
        setActiveTab('hub');
      }
    }
  }, []);

  const handleSelectTab = (tab: 'hub' | 'maeumjigi' | 'rl_q_learning' | 'all') => {
    setActiveTab(tab);
    if (typeof window !== 'undefined') {
      window.location.hash = tab === 'hub' ? 'projects' : tab;
    }
  };

  // Filter posts based on active project
  const isRlPost = (item: any) => {
    const permalink = item.content?.metadata?.permalink || '';
    const project = item.content?.metadata?.frontMatter?.project || '';
    return permalink.includes('rl-qlearning') || project === 'rl_q_learning';
  };

  const filteredItems = items.filter((item: any) => {
    if (activeTab === 'maeumjigi') {
      return !isRlPost(item);
    }
    if (activeTab === 'rl_q_learning') {
      return isRlPost(item);
    }
    return true; // 'all'
  });

  return (
    <BlogLayout sidebar={sidebar}>
      {/* Top Navigation & Hub Header */}
      <div className={styles.hubHeader}>
        <h1 className={styles.hubTitle}>{content.hubTitle}</h1>
        <p className={styles.hubSubtitle}>{content.hubSubtitle}</p>

        {/* Tab Switcher */}
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
            className={clsx(styles.tabButton, activeTab === 'maeumjigi' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('maeumjigi')}
          >
            {content.tabMaeumjigi}
          </button>
          <button
            type="button"
            className={clsx(
              styles.tabButton,
              activeTab === 'rl_q_learning' && styles.tabButtonActive
            )}
            onClick={() => handleSelectTab('rl_q_learning')}
          >
            {content.tabRl}
          </button>
          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'all' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('all')}
          >
            {content.tabAll}
          </button>
        </div>
      </div>

      {/* Hub Mode (Project Selection Grid) */}
      {activeTab === 'hub' && (
        <ProjectHubView
          projects={content.projects}
          onSelectProject={(id) => handleSelectTab(id as any)}
        />
      )}

      {/* Posts view (Maeumjigi, RL Q-Learning, or All) */}
      {activeTab !== 'hub' && (
        <>
          <div className={styles.activeProjectBanner}>
            <div>
              <h3 className={styles.bannerTitle}>
                {activeTab === 'maeumjigi'
                  ? content.bannerMaeumjigiTitle
                  : activeTab === 'rl_q_learning'
                  ? content.bannerRlTitle
                  : content.bannerAllTitle}
              </h3>
              <p className={styles.bannerDesc}>
                {activeTab === 'maeumjigi'
                  ? content.bannerMaeumjigiDesc
                  : activeTab === 'rl_q_learning'
                  ? content.bannerRlDesc
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
          <BlogPostItems items={filteredItems} />
          <BlogListPaginator metadata={metadata} />
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
