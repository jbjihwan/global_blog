import React, { useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

declare global {
  interface Window {
    adsbygoogle?: any[];
  }
}

const AD_LABELS: Record<string, string> = {
  ko: '광고 • ADVERTISEMENT',
  en: 'ADVERTISEMENT',
  ja: '広告 • ADVERTISEMENT',
  es: 'PUBLICIDAD',
  'zh-Hans': '广告 • ADVERTISEMENT',
  'zh-Hant': '廣告 • ADVERTISEMENT',
  de: 'ANZEIGE',
  fr: 'PUBLICITÉ',
  'pt-BR': 'PUBLICIDADE',
};

export default function AdCard(): React.JSX.Element {
  const {
    i18n: { currentLocale },
  } = useDocusaurusContext();

  const labelText = AD_LABELS[currentLocale] || 'ADVERTISEMENT';

  useEffect(() => {
    try {
      if (typeof window !== 'undefined') {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      }
    } catch (e) {
      // Ignore adsbygoogle push errors during development or if already filled
    }
  }, []);

  return (
    <div className="ad-card-container" aria-label={labelText}>
      <div className="ad-card-label">
        <span className="ad-card-label-line"></span>
        <span className="ad-card-label-text">{labelText}</span>
        <span className="ad-card-label-line"></span>
      </div>
      <div className="ad-card-slot">
        <ins
          className="adsbygoogle"
          style={{ display: 'block', minHeight: '90px' }}
          data-ad-client="ca-pub-4654073335496617"
          data-ad-format="auto"
          data-full-width-responsive="true"
        />
      </div>
    </div>
  );
}
