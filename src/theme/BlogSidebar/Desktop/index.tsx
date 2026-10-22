import React, { memo, useMemo } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { ProjectIcon } from '@site/src/components/Icons';
import styles from './styles.module.css';

type SupportedLocale = 'en' | 'ko' | 'ja' | 'es';

interface SidebarLocaleData {
  mainTitle: string;
  homeHub: string;
  projectsHeader: string;
  postsHeader: string;
  allPostsName: string;
  allPostsDesc: string;
  maeumjigiName: string;
  maeumjigiDesc: string;
  anprName: string;
  anprDesc: string;
  rlName: string;
  rlDesc: string;
  securityName: string;
  securityDesc: string;
  stanfordName: string;
  stanfordDesc: string;
}

const SIDEBAR_I18N: Record<SupportedLocale, SidebarLocaleData> = {
  ko: {
    mainTitle: '프로젝트 & 개발 일지',
    homeHub: '전체 프로젝트 허브',
    projectsHeader: '프로젝트 분류',
    postsHeader: '게시글 목차',
    allPostsName: '전체 글 피드',
    allPostsDesc: '34개 전체 개발일지',
    maeumjigiName: '마음지기 AI 챗봇',
    maeumjigiDesc: 'Llama 3.1 파인튜닝 (23편)',
    anprName: '스마트 비전 ANPR',
    anprDesc: '차선 침범 & 번호판 인식 (5편)',
    rlName: 'RL Q-Learning 로봇',
    rlDesc: 'Webots 자율주행 주행 (5편)',
    securityName: '보안 & 웹 엔지니어링',
    securityDesc: '취약점 방어 & 하드닝 (1편)',
    stanfordName: '스탠포드 CS146S',
    stanfordDesc: '현대 소프트웨어 개발자 (2편)',
  },
  en: {
    mainTitle: 'Projects & Dev Logs',
    homeHub: 'All Projects Hub',
    projectsHeader: 'Projects Category',
    postsHeader: 'Dev Log Table of Contents',
    allPostsName: 'All Posts Feed',
    allPostsDesc: '34 total dev logs',
    maeumjigiName: 'Maeumjigi AI Chatbot',
    maeumjigiDesc: 'Llama 3.1 Fine-tuning (23 Posts)',
    anprName: 'Smart Vision ANPR',
    anprDesc: 'Lane Intrusion & ANPR (5 Posts)',
    rlName: 'RL Q-Learning Robot',
    rlDesc: 'Webots Autonomous Driving (5 Posts)',
    securityName: 'Security & Web Infra',
    securityDesc: 'Vulnerability Defense (1 Post)',
    stanfordName: 'Stanford CS146S',
    stanfordDesc: 'Modern Software Dev (2 Posts)',
  },
  ja: {
    mainTitle: 'プロジェクト＆開発日誌',
    homeHub: '全プロジェクトハブ',
    projectsHeader: 'プロジェクト分類',
    postsHeader: '開発日誌 目次',
    allPostsName: '全記事フィード',
    allPostsDesc: '全34編の開発日誌',
    maeumjigiName: 'マウムジギ AIチャットボット',
    maeumjigiDesc: 'Llama 3.1 ファインチューニング (23編)',
    anprName: 'スマートビジョン ANPR',
    anprDesc: '車線侵犯＆ナンバー認識 (5編)',
    rlName: 'RL Q-Learning ロボット',
    rlDesc: 'Webots 自律走行 (5編)',
    securityName: 'セキュリティ＆インフラ',
    securityDesc: '脆弱性防御＆強化 (1編)',
    stanfordName: 'スタンフォード CS146S',
    stanfordDesc: '現代ソフトウェア開発者 (2編)',
  },
  es: {
    mainTitle: 'Proyectos y Diarios',
    homeHub: 'Panel de Proyectos',
    projectsHeader: 'Categorías de Proyectos',
    postsHeader: 'Índice de Publicaciones',
    allPostsName: 'Todos los Posts',
    allPostsDesc: '34 diarios de desarrollo',
    maeumjigiName: 'Chatbot IA Maeumjigi',
    maeumjigiDesc: 'Fine-tuning Llama 3.1 (23 Posts)',
    anprName: 'Visión Inteligente ANPR',
    anprDesc: 'Invasión de Carril y ANPR (5 Posts)',
    rlName: 'Robot RL Q-Learning',
    rlDesc: 'Conducción en Webots (5 Posts)',
    securityName: 'Seguridad e Infraestructura',
    securityDesc: 'Blindaje y Hardening (1 Post)',
    stanfordName: 'Stanford CS146S',
    stanfordDesc: 'Desarrollo Moderno (2 Posts)',
  },
};

function getEpisodeNumber(permalink: string): number {
  const m = permalink.match(/(?:maeumjigi|vision-anpr|rl-qlearning|stanford-cs146s)-(\d+)/);
  return m ? parseInt(m[1], 10) : 999;
}

function BlogSidebarDesktop({ sidebar }: { sidebar: any }) {
  const location = useLocation();
  const {
    i18n: { currentLocale },
  } = useDocusaurusContext();

  const locale = (currentLocale as SupportedLocale) in SIDEBAR_I18N
    ? (currentLocale as SupportedLocale)
    : 'en';
  const t = SIDEBAR_I18N[locale];

  const blogHomeUrl = '/blog';
  const isHubPage =
    location.pathname.endsWith('/blog') ||
    location.pathname.endsWith('/blog/');

  // Determine active project from pathname or hash
  const currentProjectId = useMemo(() => {
    const path = location.pathname.toLowerCase();
    if (path.includes('stanford-cs146s')) return 'stanford_cs146s';
    if (path.includes('maeumjigi')) return 'maeumjigi';
    if (path.includes('vision-anpr')) return 'anpr_vision';
    if (path.includes('rl-qlearning')) return 'rl_q_learning';
    if (path.includes('security') || path.includes('static-site-security')) return 'security';

    // If on blog list/hub page, check hash
    const hash = (location.hash || '').replace('#', '').toLowerCase();
    if (hash === 'stanford_cs146s' || hash === 'stanford' || hash === 'cs146s') return 'stanford_cs146s';
    if (hash === 'maeumjigi') return 'maeumjigi';
    if (hash === 'anpr_vision' || hash === 'anpr' || hash === 'cv') return 'anpr_vision';
    if (hash === 'rl_q_learning' || hash === 'rl') return 'rl_q_learning';
    if (hash === 'security' || hash === 'infra') return 'security';
    if (hash === 'all') return 'all';

    // Default to maeumjigi when on hub
    return 'maeumjigi';
  }, [location.pathname, location.hash]);

  // Project definitions with target URLs
  const projects = useMemo(() => {
    const items = sidebar.items || [];
    const findFirst = (pattern: RegExp) => {
      const matched = items.filter((item: any) => pattern.test(item.permalink));
      if (!matched.length) return blogHomeUrl;
      // Return lowest episode number
      matched.sort((a: any, b: any) => getEpisodeNumber(a.permalink) - getEpisodeNumber(b.permalink));
      return matched[0].permalink;
    };

    return [
      {
        id: 'stanford_cs146s',
        name: t.stanfordName,
        desc: t.stanfordDesc,
        icon: 'stanford_cs146s',
        count: items.filter((item: any) => item.permalink.includes('stanford-cs146s')).length || 1,
        targetUrl: findFirst(/stanford-cs146s/),
        filter: (item: any) => item.permalink.includes('stanford-cs146s'),
        sortAscending: true,
      },
      {
        id: 'maeumjigi',
        name: t.maeumjigiName,
        desc: t.maeumjigiDesc,
        icon: 'maeumjigi',
        count: 23,
        targetUrl: findFirst(/maeumjigi/),
        filter: (item: any) => item.permalink.includes('maeumjigi'),
        sortAscending: true,
      },
      {
        id: 'anpr_vision',
        name: t.anprName,
        desc: t.anprDesc,
        icon: 'anpr_vision',
        count: 5,
        targetUrl: findFirst(/vision-anpr/),
        filter: (item: any) => item.permalink.includes('vision-anpr'),
        sortAscending: true,
      },
      {
        id: 'rl_q_learning',
        name: t.rlName,
        desc: t.rlDesc,
        icon: 'rl_q_learning',
        count: 5,
        targetUrl: findFirst(/rl-qlearning/),
        filter: (item: any) => item.permalink.includes('rl-qlearning'),
        sortAscending: true,
      },
      {
        id: 'security',
        name: t.securityName,
        desc: t.securityDesc,
        icon: 'security',
        count: 1,
        targetUrl: findFirst(/security|static-site-security/),
        filter: (item: any) =>
          item.permalink.includes('security') || item.permalink.includes('static-site-security'),
        sortAscending: true,
      },
      {
        id: 'all',
        name: t.allPostsName,
        desc: t.allPostsDesc,
        icon: 'all',
        count: items.length,
        targetUrl: `${blogHomeUrl}#all`,
        filter: () => true,
        sortAscending: false,
      },
    ];
  }, [sidebar.items, t, blogHomeUrl]);

  // Active project object
  const activeProject = useMemo(() => {
    return projects.find((p) => p.id === currentProjectId) || projects[0];
  }, [projects, currentProjectId]);

  // Filter and sort posts for the active project
  const displayPosts = useMemo(() => {
    const rawItems = sidebar.items || [];
    const filtered = rawItems.filter(activeProject.filter);
    if (activeProject.sortAscending) {
      return [...filtered].sort(
        (a: any, b: any) => getEpisodeNumber(a.permalink) - getEpisodeNumber(b.permalink)
      );
    }
    return filtered;
  }, [sidebar.items, activeProject]);

  return (
    <aside className="col col--3">
      <nav className={clsx(styles.sidebar, 'thin-scrollbar')} aria-label={t.mainTitle}>
        {/* Tier 1: Home / Project Hub */}
        <div className={styles.sectionBlock}>
          <Link
            to={blogHomeUrl}
            className={clsx(styles.homeButton, isHubPage && styles.homeButtonActive)}
          >
            <span className={styles.homeIcon}>
              <ProjectIcon id="home" size={17} />
            </span>
            <span className={styles.homeText}>{t.homeHub}</span>
          </Link>
        </div>

        {/* Tier 2: Project Categories */}
        <div className={styles.sectionBlock}>
          <div className={styles.sectionHeader}>
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}>
              <ProjectIcon id="folder" size={14} />
              {t.projectsHeader}
            </span>
          </div>
          <div className={styles.projectList}>
            {projects.map((proj) => {
              const isActive = currentProjectId === proj.id;
              return (
                <Link
                  key={proj.id}
                  to={proj.targetUrl}
                  className={clsx(
                    styles.projectCard,
                    isActive && styles.projectCardActive
                  )}
                >
                  <span className={styles.projectIcon}>
                    <ProjectIcon id={proj.id} size={18} />
                  </span>
                  <div className={styles.projectInfo}>
                    <div className={styles.projectName}>{proj.name}</div>
                    <div className={styles.projectBadge}>{proj.desc}</div>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Tier 3: Filtered Posts Table of Contents */}
        <div className={styles.sectionBlock}>
          <div className={styles.postsHeaderRow}>
            <div className={styles.sectionHeader}>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}>
                <ProjectIcon id={activeProject.id} size={14} />
                {activeProject.name} ({displayPosts.length})
              </span>
            </div>
          </div>
          <ul className={clsx(styles.sidebarItemList, 'clean-list')}>
            {displayPosts.map((item: any) => {
              const isCurrent =
                location.pathname === item.permalink ||
                location.pathname === `${item.permalink}/` ||
                location.pathname.endsWith(item.permalink);

              return (
                <li key={item.permalink} className={styles.sidebarItem}>
                  <Link
                    to={item.permalink}
                    className={clsx(
                      styles.sidebarItemLink,
                      isCurrent && styles.sidebarItemLinkActive
                    )}
                  >
                    {item.title}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      </nav>
    </aside>
  );
}

export default memo(BlogSidebarDesktop);
