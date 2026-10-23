import React, { useEffect, useState } from 'react';

interface ToastData {
  title: string;
  desc: string;
  actionText: string;
  actionUrl: string;
}

export default function WelcomeToast() {
  const [toast, setToast] = useState<ToastData | null>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (typeof window === 'undefined') return;

    // Check if dismissed in this session
    if (sessionStorage.getItem('welcome_toast_dismissed')) return;

    const path = window.location.pathname.toLowerCase();
    const isKo = path.startsWith('/ko');
    const isJa = path.startsWith('/ja');
    const isEs = path.startsWith('/es');

    const searchParams = new URLSearchParams(window.location.search);
    const kw = searchParams.get('utm_term') || searchParams.get('kw') || searchParams.get('q');
    const ref = document.referrer.toLowerCase();

    let title = '';
    let desc = '';
    let actionText = '';
    let actionUrl = isKo ? '/ko/blog' : isJa ? '/ja/blog' : isEs ? '/es/blog' : '/blog';

    if (kw) {
      if (isKo) {
        title = `💡 "${kw}" 주제를 찾아오셨군요!`;
        desc = `GlobalDevLog의 스탠포드 CS146S 최신 엔지니어링 시리즈를 둘러보세요.`;
        actionText = `시리즈 보러가기 →`;
      } else if (isJa) {
        title = `💡「${kw}」をお探しの皆様へ！`;
        desc = `スタンフォード大学 CS146S 最新AIエンジニアリングシリーズへようこそ。`;
        actionText = `シリーズを見る →`;
      } else if (isEs) {
        title = `💡 ¡Buscando "${kw}"!`;
        desc = `Bienvenido a la serie de ingeniería Stanford CS146S en GlobalDevLog.`;
        actionText = `Ver serie →`;
      } else {
        title = `💡 Searching for "${kw}"?`;
        desc = `Explore our Stanford CS146S deep-dive series on Agentic Workflows & MCP.`;
        actionText = `Explore Series →`;
      }
    } else if (ref.includes('google.')) {
      if (isKo) {
        title = `🔍 구글 검색 방문을 환영합니다!`;
        desc = `AI 에이전트 & 스펙 주도 개발(SDD) 스탠포드 CS146S 시리즈를 확인해보세요.`;
        actionText = `최신 글 보기 →`;
      } else if (isJa) {
        title = `🔍 Googleからのご訪問ありがとうございます！`;
        desc = `スタンフォード CS146S 現代ソフトウェア開発シリーズをご覧ください。`;
        actionText = `最新記事を見る →`;
      } else if (isEs) {
        title = `🔍 ¡Bienvenido desde Google!`;
        desc = `Descubre nuestra serie de Stanford CS146S sobre agentes de IA.`;
        actionText = `Leer ahora →`;
      } else {
        title = `🔍 Welcome Google Developer!`;
        desc = `Check out our Stanford CS146S series on autonomous agent architectures.`;
        actionText = `Read Latest →`;
      }
    } else if (ref.includes('naver.')) {
      title = `🟢 네이버 검색 방문을 환영합니다!`;
      desc = `스탠포드 CS146S 및 AI 엔지니어링 개발일지 전체 허브를 둘러보세요.`;
      actionText = `개발일지 허브 →`;
      actionUrl = '/ko/blog';
    } else if (ref.includes('chatgpt.com') || ref.includes('perplexity.ai') || ref.includes('claude.ai')) {
      if (isKo) {
        title = `🤖 AI 추천 방문을 환영합니다!`;
        desc = `검증된 아키텍처 다이어그램과 스탠포드 CS146S 원문을 확인해보세요.`;
        actionText = `아키텍처 보기 →`;
      } else {
        title = `🤖 Arrived via AI Assistant?`;
        desc = `Explore verified architecture blueprints and Stanford CS146S course logs.`;
        actionText = `View Blueprints →`;
      }
    } else if (ref.includes('github.com')) {
      if (isKo) {
        title = `🐙 GitHub 개발자님 환영합니다!`;
        desc = `GlobalDevLog의 오픈소스 프로젝트 및 기술 심층 분석을 확인해보세요.`;
        actionText = `프로젝트 허브 →`;
      } else {
        title = `🐙 Welcome GitHub Engineer!`;
        desc = `Explore production architectures, MCP protocols, and autonomous agents.`;
        actionText = `Explore Hub →`;
      }
    } else {
      return; // Silent if direct navigation without special referrer
    }

    setToast({ title, desc, actionText, actionUrl });
    // Animate in after 1.5 seconds
    const timer = setTimeout(() => setVisible(true), 1500);
    return () => clearTimeout(timer);
  }, []);

  if (!toast || !visible) return null;

  const handleDismiss = () => {
    setVisible(false);
    sessionStorage.setItem('welcome_toast_dismissed', 'true');
  };

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 9999,
        maxWidth: '380px',
        width: 'calc(100vw - 48px)',
        padding: '16px 20px',
        background: 'rgba(15, 23, 42, 0.88)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        border: '1px solid rgba(56, 189, 248, 0.35)',
        borderRadius: '14px',
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.45), 0 0 20px rgba(56, 189, 248, 0.15)',
        color: '#f8fafc',
        fontFamily: 'inherit',
        animation: 'fadeInUp 0.4s ease-out',
        display: 'flex',
        flexDirection: 'column',
        gap: '8px',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontWeight: 700, fontSize: '14px', color: '#38bdf8', letterSpacing: '-0.01em' }}>
          {toast.title}
        </span>
        <button
          onClick={handleDismiss}
          style={{
            background: 'none',
            border: 'none',
            color: '#94a3b8',
            fontSize: '18px',
            cursor: 'pointer',
            padding: '2px 6px',
            lineHeight: 1,
          }}
          aria-label="Close welcome banner"
        >
          ×
        </button>
      </div>
      <p style={{ margin: 0, fontSize: '13px', lineHeight: 1.5, color: '#cbd5e1' }}>
        {toast.desc}
      </p>
      <div style={{ marginTop: '4px', display: 'flex', justifyContent: 'flex-end' }}>
        <a
          href={toast.actionUrl}
          onClick={handleDismiss}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            fontSize: '12px',
            fontWeight: 600,
            color: '#0f172a',
            background: 'linear-gradient(135deg, #38bdf8 0%, #818cf8 100%)',
            padding: '6px 14px',
            borderRadius: '8px',
            textDecoration: 'none',
            boxShadow: '0 2px 8px rgba(56, 189, 248, 0.3)',
          }}
        >
          {toast.actionText}
        </a>
      </div>
    </div>
  );
}
