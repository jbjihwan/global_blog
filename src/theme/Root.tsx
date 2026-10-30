import React, { useEffect } from 'react';
import Head from '@docusaurus/Head';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useLocation } from '@docusaurus/router';
import WelcomeToast from '@site/src/components/WelcomeToast';

export default function Root({ children }: { children: React.ReactNode }) {
  const { i18n } = useDocusaurusContext();
  const location = useLocation();
  const currentLocale = i18n.currentLocale;

  // 1. Whitelist primary high-touch locales for Google index & AdSense review
  // Exclude 6 zero-traffic locales (de, fr, pt-BR, es, zh-Hans, ja) from index to eliminate "Scaled/Thin Content" penalty
  const isTargetLocale = ['en', 'ko', 'zh-Hant'].includes(currentLocale);

  // 2. Mental Crisis safety check: Never serve or run AdSense on suicide/crisis NLP research pages
  const isMentalCrisisPage = location.pathname.includes('mental-crisis');

  useEffect(() => {
    if (typeof window !== 'undefined') {
      try {
        const win = window as any;
        if (isMentalCrisisPage) {
          (win.adsbygoogle = win.adsbygoogle || []).pauseAdRequests = 1;
        } else {
          (win.adsbygoogle = win.adsbygoogle || []).pauseAdRequests = 0;
        }
      } catch (e) {
        // Safe fallback
      }
    }
  }, [isMentalCrisisPage]);

  return (
    <>
      {/* Search Engine Directives: noindex for non-core locales during AdSense review */}
      {!isTargetLocale && (
        <Head>
          <meta name="robots" content="noindex, follow" />
        </Head>
      )}

      {/* AdSense Script Guard: Completely omitted from mental-crisis YMYL pages */}
      {!isMentalCrisisPage && (
        <Head>
          <script
            async
            src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4654073335496617"
            crossOrigin="anonymous"
          />
        </Head>
      )}

      {children}
      <WelcomeToast />
    </>
  );
}
