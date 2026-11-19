import React, { useEffect } from 'react';
import Head from '@docusaurus/Head';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useLocation } from '@docusaurus/router';
import WelcomeToast from '@site/src/components/WelcomeToast';

export default function Root({ children }: { children: React.ReactNode }) {
  const { i18n } = useDocusaurusContext();
  const currentLocale = i18n.currentLocale;

  // Whitelist primary author-curated locales for Google index & AdSense review
  const isTargetLocale = ['en', 'ko'].includes(currentLocale);

  return (
    <>
      {/* Search Engine Directives: noindex for non-core locales during AdSense review */}
      {!isTargetLocale && (
        <Head>
          <meta name="robots" content="noindex, follow" />
        </Head>
      )}

      <Head>
        <script
          async
          src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4654073335496617"
          crossOrigin="anonymous"
        />
      </Head>

      {children}
      <WelcomeToast />
    </>
  );
}
