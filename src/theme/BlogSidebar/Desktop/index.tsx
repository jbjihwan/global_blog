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
  sdcName: string;
  sdcDesc: string;
  maeumjigiName: string;
  maeumjigiDesc: string;
  anprName: string;
  anprDesc: string;
  rlName: string;
  rlDesc: string;
  securityName: string;
  securityDesc: string;
}

const SIDEBAR_I18N: Record<SupportedLocale, SidebarLocaleData> = {
  ko: {
    mainTitle: '프로젝트 & 개발 일지',
    homeHub: '전체 프로젝트 허브',
    projectsHeader: '프로젝트 분류',
    postsHeader: '게시글 목차',
    allPostsName: '전체 글 피드',
    allPostsDesc: '전체 개발일지',
    sdcName: '항공작전 동적 임무계획',
    sdcDesc: 'Link 16 & 실시간 경로탐색',
    maeumjigiName: 'LLM & 백엔드 디버깅',
    maeumjigiDesc: 'Llama 3.1 & FastAPI 401',
    anprName: '스마트 비전 ANPR',
    anprDesc: '차선 침범 & 번호판 인식',
    rlName: 'RL Q-Learning 로봇',
    rlDesc: 'Webots 자율주행',
    securityName: '보안 & 파이썬 디버깅',
    securityDesc: 'DNS 타임아웃 & 공급망 방어',
  },
  en: {
    mainTitle: 'Projects & Dev Logs',
    homeHub: 'All Projects Hub',
    projectsHeader: 'Projects Category',
    postsHeader: 'Dev Log Table of Contents',
    allPostsName: 'All Posts Feed',
    allPostsDesc: 'Total Dev Logs',
    sdcName: 'SDC Mission Replanning',
    sdcDesc: 'Avionics AI & Link 16 JCS',
    maeumjigiName: 'LLM & Backend Debugging',
    maeumjigiDesc: 'Llama 3.1 & FastAPI 401',
    anprName: 'Smart Vision ANPR',
    anprDesc: 'Lane Intrusion & ANPR',
    rlName: 'RL Q-Learning Robot',
    rlDesc: 'Webots Autonomous Driving',
    securityName: 'Security & Python Debugging',
    securityDesc: 'DNS Timeouts & Supply Chain',
  },
  ja: {
    mainTitle: 'プロジェクト＆開発日誌',
    homeHub: '全プロジェクトハブ',
    projectsHeader: 'プロジェクト分類',
    postsHeader: '開発日誌 目次',
    allPostsName: '全記事フィード',
    allPostsDesc: '全開発日誌',
    sdcName: 'SDC 動的任務再計画',
    sdcDesc: 'Link 16 & 経路探索',
    maeumjigiName: 'LLM & バックエンド',
    maeumjigiDesc: 'Llama 3.1 ファインチューニング',
    anprName: 'スマートビジョン ANPR',
    anprDesc: '車線侵犯＆ナンバー認識',
    rlName: 'RL Q-Learning ロボット',
    rlDesc: 'Webots 自律走行',
    securityName: 'セキュリティ＆インフラ',
    securityDesc: '脆弱性防御＆強化',
  },
  es: {
    mainTitle: 'Proyectos y Diarios',
    homeHub: 'Panel de Proyectos',
    projectsHeader: 'Categorías de Proyectos',
    postsHeader: 'Índice de Publicaciones',
    allPostsName: 'Todos los Posts',
    allPostsDesc: 'Diarios de desarrollo',
    sdcName: 'Replanificación SDC',
    sdcDesc: 'IA Aviónica y Link 16',
    maeumjigiName: 'LLM y Backend Debugging',
    maeumjigiDesc: 'Fine-tuning Llama 3.1',
    anprName: 'Visión Inteligente ANPR',
    anprDesc: 'Invasión de Carril y ANPR',
    rlName: 'Robot RL Q-Learning',
    rlDesc: 'Conducción en Webots',
    securityName: 'Seguridad e Infraestructura',
    securityDesc: 'Blindaje y Hardening',
  },
};

function formatCount(count: number, locale: SupportedLocale): string {
  if (locale === 'ko') return `${count}편`;
  if (locale === 'ja') return `${count}編`;
  return `${count} ${count === 1 ? 'Post' : 'Posts'}`;
}

function getEpisodeNumber(permalink: string): number {
  const sdcM = permalink.match(/sdc-0?(\d+)/);
  if (sdcM) return parseInt(sdcM[1], 10);
  const m = permalink.match(/(?:maeumjigi|vision-anpr|rl-qlearning)-(\d+)/);
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

  const blogHomeUrl = locale === 'ko' ? '/ko/blog' : '/blog';
  const isHubPage =
    location.pathname.endsWith('/blog') ||
    location.pathname.endsWith('/blog/');

  const currentProjectId = useMemo(() => {
    const path = location.pathname.toLowerCase();
    if (path.includes('sdc-')) return 'sdc_replanning';
    if (path.includes('maeumjigi')) return 'maeumjigi';
    if (path.includes('vision-anpr')) return 'anpr_vision';
    if (path.includes('rl-qlearning')) return 'rl_q_learning';
    if (
      path.includes('security') ||
      path.includes('static-site') ||
      path.includes('custom-domain') ||
      path.includes('cloudflare') ||
      path.includes('npm-overrides') ||
      path.includes('python-urlopen')
    ) return 'security';

    const hash = (location.hash || '').replace('#', '').toLowerCase();
    if (hash === 'sdc' || hash === 'sdc_replanning' || hash === 'sdc-replanning') return 'sdc_replanning';
    if (hash === 'maeumjigi') return 'maeumjigi';
    if (hash === 'anpr_vision' || hash === 'anpr' || hash === 'cv') return 'anpr_vision';
    if (hash === 'rl_q_learning' || hash === 'rl') return 'rl_q_learning';
    if (hash === 'security' || hash === 'infra') return 'security';

    return 'sdc_replanning';
  }, [location.pathname, location.hash]);

  const projects = useMemo(() => {
    const items = sidebar.items || [];
    const findFirst = (pattern: RegExp, defaultHash: string) => {
      const matched = items.filter((item: any) => pattern.test(item.permalink));
      if (!matched.length) return `${blogHomeUrl}#${defaultHash}`;
      matched.sort((a: any, b: any) => getEpisodeNumber(a.permalink) - getEpisodeNumber(b.permalink));
      return matched[0].permalink;
    };

    const isSdc = (item: any) => item.permalink.includes('sdc-');
    const isSecurity = (item: any) =>
      item.permalink.includes('security') ||
      item.permalink.includes('static-site') ||
      item.permalink.includes('custom-domain') ||
      item.permalink.includes('cloudflare') ||
      item.permalink.includes('npm-overrides') ||
      item.permalink.includes('vulnerability') ||
      item.permalink.includes('python-urlopen');

    const sdcCount = items.filter(isSdc).length;
    const maeumjigiCount = items.filter((item: any) => item.permalink.includes('maeumjigi')).length;
    const anprCount = items.filter((item: any) => item.permalink.includes('vision-anpr')).length;
    const rlCount = items.filter((item: any) => item.permalink.includes('rl-qlearning')).length;
    const securityCount = items.filter(isSecurity).length;

    return [
      {
        id: 'sdc_replanning',
        name: t.sdcName,
        desc: `${t.sdcDesc} (${formatCount(sdcCount, locale)})`,
        icon: 'sdc_replanning',
        count: sdcCount,
        targetUrl: findFirst(/sdc-/, 'sdc_replanning'),
        filter: isSdc,
        sortAscending: true,
      },
      {
        id: 'security',
        name: t.securityName,
        desc: `${t.securityDesc} (${formatCount(securityCount, locale)})`,
        icon: 'security',
        count: securityCount,
        targetUrl: findFirst(/(?:security|static-site|custom-domain|cloudflare|npm-overrides|python-urlopen)/, 'security'),
        filter: isSecurity,
        sortAscending: false,
      },
      {
        id: 'anpr_vision',
        name: t.anprName,
        desc: `${t.anprDesc} (${formatCount(anprCount, locale)})`,
        icon: 'anpr_vision',
        count: anprCount,
        targetUrl: findFirst(/vision-anpr/, 'anpr_vision'),
        filter: (item: any) => item.permalink.includes('vision-anpr'),
        sortAscending: true,
      },
      {
        id: 'rl_q_learning',
        name: t.rlName,
        desc: `${t.rlDesc} (${formatCount(rlCount, locale)})`,
        icon: 'rl_q_learning',
        count: rlCount,
        targetUrl: findFirst(/rl-qlearning/, 'rl_q_learning'),
        filter: (item: any) => item.permalink.includes('rl-qlearning'),
        sortAscending: true,
      },
      {
        id: 'maeumjigi',
        name: t.maeumjigiName,
        desc: `${t.maeumjigiDesc} (${formatCount(maeumjigiCount, locale)})`,
        icon: 'maeumjigi',
        count: maeumjigiCount,
        targetUrl: findFirst(/maeumjigi/, 'maeumjigi'),
        filter: (item: any) => item.permalink.includes('maeumjigi'),
        sortAscending: true,
      },
    ].filter((p) => p.count > 0);
  }, [sidebar.items, t, locale, blogHomeUrl]);

  const activeProject = useMemo(() => {
    return projects.find((p) => p.id === currentProjectId) || projects[0];
  }, [projects, currentProjectId]);

  const displayPosts = useMemo(() => {
    if (!activeProject) return [];
    const rawItems = sidebar.items || [];
    const filtered = rawItems.filter(activeProject.filter);
    if (activeProject.sortAscending) {
      return [...filtered].sort(
        (a: any, b: any) => getEpisodeNumber(a.permalink) - getEpisodeNumber(b.permalink)
      );
    }
    return filtered;
  }, [sidebar.items, activeProject]);

  if (!activeProject) return null;

  return (
    <aside className="col col--3">
      <nav className={clsx(styles.sidebar, 'thin-scrollbar')} aria-label={t.mainTitle}>
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

        <div className={styles.sectionBlock}>
          <div className={styles.sectionHeader}>
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}>
              <ProjectIcon id="folder" size={14} />
              {t.projectsHeader}
            </span>
          </div>
          <div className={styles.projectList}>
            {projects.map((proj) => {
              const isActive = activeProject.id === proj.id;
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
