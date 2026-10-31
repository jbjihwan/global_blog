import React, { memo, useMemo } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { NavbarSecondaryMenuFiller } from '@docusaurus/theme-common';
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
  crisisDetectionName: string;
  crisisDetectionDesc: string;
  nationalBudgetName: string;
  nationalBudgetDesc: string;
  cs329aName: string;
  cs329aDesc: string;
  stanfordName: string;
  stanfordDesc: string;
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
    crisisDetectionName: '[고위험 AI] 위기 텍스트 정밀 감지',
    crisisDetectionDesc: '자살/위기 AI & FNR 제로화',
    nationalBudgetName: '국가 예산 AI 감사',
    nationalBudgetDesc: '공공조달 & 비리 탐지',
    cs329aName: '스탠포드 CS329A',
    cs329aDesc: '자가 진화 AI 에이전트',
    stanfordName: '스탠포드 CS146S',
    stanfordDesc: '현대 소프트웨어 개발자',
    maeumjigiName: '마음지기 AI 챗봇',
    maeumjigiDesc: 'Llama 3.1 파인튜닝',
    anprName: '스마트 비전 ANPR',
    anprDesc: '차선 침범 & 번호판 인식',
    rlName: 'RL Q-Learning 로봇',
    rlDesc: 'Webots 자율주행',
    securityName: '보안 & 웹 엔지니어링',
    securityDesc: '취약점 방어 & 하드닝',
  },
  en: {
    mainTitle: 'Projects & Dev Logs',
    homeHub: 'All Projects Hub',
    projectsHeader: 'Projects Category',
    postsHeader: 'Dev Log Table of Contents',
    allPostsName: 'All Posts Feed',
    allPostsDesc: 'Total Dev Logs',
    crisisDetectionName: '[Crisis AI] Suicide Risk NLP',
    crisisDetectionDesc: 'Crisis Detection & FNR Zero',
    nationalBudgetName: 'Public Budget AI',
    nationalBudgetDesc: 'Procurement Fraud Audit',
    cs329aName: 'Stanford CS329A',
    cs329aDesc: 'Self-Improving AI Agents',
    stanfordName: 'Stanford CS146S',
    stanfordDesc: 'Modern Software Dev',
    maeumjigiName: 'Maeumjigi AI Chatbot',
    maeumjigiDesc: 'Llama 3.1 Fine-tuning',
    anprName: 'Smart Vision ANPR',
    anprDesc: 'Lane Intrusion & ANPR',
    rlName: 'RL Q-Learning Robot',
    rlDesc: 'Webots Autonomous Driving',
    securityName: 'Security & Web Infra',
    securityDesc: 'Vulnerability Defense',
  },
  ja: {
    mainTitle: 'プロジェクト＆開発日誌',
    homeHub: '全プロジェクトハブ',
    projectsHeader: 'プロジェクト分類',
    postsHeader: '開発日誌 目次',
    allPostsName: '全記事フィード',
    allPostsDesc: '全開発日誌',
    crisisDetectionName: '【高リスクAI】危機検知NLP',
    crisisDetectionDesc: '自殺・心理的危機＆FNRゼロ化',
    nationalBudgetName: '国家予算AI監査',
    nationalBudgetDesc: '公共調達＆不正検知',
    cs329aName: 'スタンフォード CS329A',
    cs329aDesc: '自己進化AIエージェント',
    stanfordName: 'スタンフォード CS146S',
    stanfordDesc: '現代ソフトウェア開発者',
    maeumjigiName: 'マウムジギ AIチャットボット',
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
    crisisDetectionName: '[IA Crisis] Detección Suicida NLP',
    crisisDetectionDesc: 'Detección de Crisis y FNR Cero',
    nationalBudgetName: 'Auditoría Presupuesto IA',
    nationalBudgetDesc: 'Fraude en Compras Públicas',
    cs329aName: 'Stanford CS329A',
    cs329aDesc: 'Agentes de IA Autoelevados',
    stanfordName: 'Stanford CS146S',
    stanfordDesc: 'Desarrollo Moderno',
    maeumjigiName: 'Chatbot IA Maeumjigi',
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
  if (permalink.includes('mental-crisis-nlp-suicide-risk-detection-fnr-zero')) return 1;
  const mc = permalink.match(/(?:mental-crisis|crisis-detection).*?-(\d+)/);
  if (mc) return parseInt(mc[1], 10);
  if (permalink.includes('autonomous-budget-audit-agent-text-to-sql-graphrag')) return 1;
  if (permalink.includes('national-budget-ai-audit-findings-performance-evaluation')) return 2;
  if (permalink.includes('national-budget-ai-sector-partition-live-monitoring')) return 3;
  if (permalink.includes('national-budget-ai-corporate-registry-cartel-detection')) return 4;
  if (permalink.includes('national-budget-ai-6-sector-full-suite')) return 5;
  if (permalink.includes('national-budget-ai-inspector-portal-verification-system')) return 6;
  const m = permalink.match(/(?:maeumjigi|vision-anpr|rl-qlearning|stanford-cs146s|stanford-cs329a)-(\d+)/);
  return m ? parseInt(m[1], 10) : 999;
}

function BlogSidebarMobileSecondaryMenu({ sidebar }: { sidebar: any }) {
  const location = useLocation();
  const {
    i18n: { currentLocale },
  } = useDocusaurusContext();

  const locale = (currentLocale as SupportedLocale) in SIDEBAR_I18N
    ? (currentLocale as SupportedLocale)
    : 'en';
  const t = SIDEBAR_I18N[locale];

  const blogHomeUrl = '/blog';

  const currentProjectId = useMemo(() => {
    const path = location.pathname.toLowerCase();
    if (path.includes('mental-crisis') || path.includes('crisis-detection')) return 'crisis_detection';
    if (path.includes('national-budget') || path.includes('autonomous-budget-audit')) return 'national_budget';
    if (path.includes('stanford-cs329a')) return 'stanford_cs329a';
    if (path.includes('stanford-cs146s')) return 'stanford_cs146s';
    if (path.includes('maeumjigi')) return 'maeumjigi';
    if (path.includes('vision-anpr')) return 'anpr_vision';
    if (path.includes('rl-qlearning')) return 'rl_q_learning';
    if (
      path.includes('security') ||
      path.includes('static-site') ||
      path.includes('custom-domain') ||
      path.includes('cloudflare') ||
      path.includes('adsense')
    ) return 'security';

    const hash = (location.hash || '').replace('#', '').toLowerCase();
    if (hash === 'crisis_detection' || hash === 'crisis' || hash === 'mental-crisis') return 'crisis_detection';
    if (hash === 'national_budget' || hash === 'budget' || hash === 'national-budget') return 'national_budget';
    if (hash === 'stanford_cs329a' || hash === 'cs329a' || hash === 'stanford-cs329a') return 'stanford_cs329a';
    if (hash === 'stanford_cs146s' || hash === 'stanford' || hash === 'cs146s' || hash === 'stanford-cs146s') return 'stanford_cs146s';
    if (hash === 'maeumjigi') return 'maeumjigi';
    if (hash === 'anpr_vision' || hash === 'anpr' || hash === 'cv') return 'anpr_vision';
    if (hash === 'rl_q_learning' || hash === 'rl') return 'rl_q_learning';
    if (hash === 'security' || hash === 'infra') return 'security';
    if (hash === 'all') return 'all';

    return 'crisis_detection';
  }, [location.pathname, location.hash]);

  const projects = useMemo(() => {
    const items = sidebar.items || [];
    const findFirst = (pattern: RegExp, defaultHash: string) => {
      const matched = items.filter((item: any) => pattern.test(item.permalink));
      if (!matched.length) return `${blogHomeUrl}#${defaultHash}`;
      matched.sort((a: any, b: any) => getEpisodeNumber(a.permalink) - getEpisodeNumber(b.permalink));
      return matched[0].permalink;
    };

    const isCrisis = (item: any) =>
      item.permalink.includes('mental-crisis') ||
      item.permalink.includes('crisis-detection');

    const isNationalBudget = (item: any) =>
      item.permalink.includes('national-budget') ||
      item.permalink.includes('autonomous-budget-audit') ||
    item.permalink.includes('local-subsidy');

    const isSecurity = (item: any) =>
      item.permalink.includes('security') ||
      item.permalink.includes('static-site') ||
      item.permalink.includes('custom-domain') ||
      item.permalink.includes('cloudflare') ||
      item.permalink.includes('adsense') ||
      item.permalink.includes('npm-overrides') ||
      item.permalink.includes('vulnerability');

    const crisisCount = items.filter(isCrisis).length;
    const budgetCount = items.filter(isNationalBudget).length;
    const cs329aCount = items.filter((item: any) => item.permalink.includes('stanford-cs329a')).length;
    const cs146sCount = items.filter((item: any) => item.permalink.includes('stanford-cs146s')).length;
    const maeumjigiCount = items.filter((item: any) => item.permalink.includes('maeumjigi')).length;
    const anprCount = items.filter((item: any) => item.permalink.includes('vision-anpr')).length;
    const rlCount = items.filter((item: any) => item.permalink.includes('rl-qlearning')).length;
    const securityCount = items.filter(isSecurity).length;
    const totalCount = items.length;

    return [
      {
        id: 'crisis_detection',
        name: t.crisisDetectionName,
        desc: `${t.crisisDetectionDesc} (${formatCount(crisisCount, locale)})`,
        icon: 'crisis_detection',
        count: crisisCount,
        targetUrl: findFirst(/(?:mental-crisis|crisis-detection)/, 'crisis_detection'),
        filter: isCrisis,
        sortAscending: true,
      },
      {
        id: 'national_budget',
        name: t.nationalBudgetName,
        desc: `${t.nationalBudgetDesc} (${formatCount(budgetCount, locale)})`,
        icon: 'national_budget',
        count: budgetCount,
        targetUrl: findFirst(/(?:national-budget|autonomous-budget-audit|local-subsidy)/, 'national_budget'),
        filter: isNationalBudget,
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
        id: 'security',
        name: t.securityName,
        desc: `${t.securityDesc} (${formatCount(securityCount, locale)})`,
        icon: 'security',
        count: securityCount,
        targetUrl: findFirst(/(?:security|static-site|custom-domain|cloudflare|adsense)/, 'security'),
        filter: isSecurity,
        sortAscending: true,
      },
      {
        id: 'stanford_cs329a',
        name: t.cs329aName,
        desc: `${t.cs329aDesc} (${formatCount(cs329aCount, locale)})`,
        icon: 'stanford_cs329a',
        count: cs329aCount,
        targetUrl: findFirst(/stanford-cs329a/, 'stanford_cs329a'),
        filter: (item: any) => item.permalink.includes('stanford-cs329a'),
        sortAscending: true,
      },
      {
        id: 'stanford_cs146s',
        name: t.stanfordName,
        desc: `${t.stanfordDesc} (${formatCount(cs146sCount, locale)})`,
        icon: 'stanford_cs146s',
        count: cs146sCount,
        targetUrl: findFirst(/stanford-cs146s/, 'stanford_cs146s'),
        filter: (item: any) => item.permalink.includes('stanford-cs146s'),
        sortAscending: true,
      },
    ];
  }, [sidebar.items, t, locale, blogHomeUrl]);

  const activeProject = useMemo(() => {
    return projects.find((p) => p.id === currentProjectId) || projects[0];
  }, [projects, currentProjectId]);

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
    <div className={styles.mobileContainer}>
      {/* Tier 1: Home */}
      <div className={styles.sectionBlock}>
        <Link to={blogHomeUrl} className={styles.homeButton}>
          <ProjectIcon id="home" size={17} />
          <span>{t.homeHub}</span>
        </Link>
      </div>

      {/* Tier 2: Projects */}
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
                <ProjectIcon id={proj.id} size={18} />
                <div className={styles.projectInfo}>
                  <div>{proj.name}</div>
                  <div className={styles.projectBadge}>{proj.desc}</div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Tier 3: Posts */}
      <div className={styles.sectionBlock}>
        <div className={styles.sectionHeader}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}>
            <ProjectIcon id={activeProject.id} size={14} />
            {activeProject.name} ({displayPosts.length})
          </span>
        </div>
        <ul className={styles.postList}>
          {displayPosts.map((item: any) => {
            const isCurrent =
              location.pathname === item.permalink ||
              location.pathname === `${item.permalink}/` ||
              location.pathname.endsWith(item.permalink);

            return (
              <li key={item.permalink} className={styles.postItem}>
                <Link
                  to={item.permalink}
                  className={clsx(
                    styles.postLink,
                    isCurrent && styles.postLinkActive
                  )}
                >
                  {item.title}
                </Link>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}

function BlogSidebarMobile(props: any) {
  return (
    <NavbarSecondaryMenuFiller
      component={BlogSidebarMobileSecondaryMenu}
      props={props}
    />
  );
}

export default memo(BlogSidebarMobile);
