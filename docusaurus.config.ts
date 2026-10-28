import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Global Dev Blog',
  tagline: 'Engineering Deep Dives in AI, Robotics, Computer Vision & Reinforcement Learning',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  url: 'https://globaldevlog.com',
  baseUrl: '/',

  // GitHub pages deployment config.
  organizationName: 'jbjihwan', // Usually your GitHub org/user name.
  projectName: 'global_blog', // Usually your repo name.
  trailingSlash: false,

  scripts: [
    {
      src: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4654073335496617',
      async: true,
      crossorigin: 'anonymous',
    },
  ],

  onBrokenLinks: 'throw',
  onBrokenAnchors: 'ignore',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'ja', 'ko', 'zh-Hans', 'zh-Hant', 'de', 'fr', 'pt-BR'],
    localeConfigs: {
      en: { label: 'English' },
      es: { label: 'Español' },
      ja: { label: '日本語' },
      ko: { label: '한국어' },
      'zh-Hans': { label: '简体中文' },
      'zh-Hant': { label: '繁體中文' },
      de: { label: 'Deutsch' },
      fr: { label: 'Français' },
      'pt-BR': { label: 'Português' },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: false,
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
          postsPerPage: 'ALL',
          blogSidebarCount: 'ALL',
          blogSidebarTitle: 'Projects & Dev Logs',
          blogTitle: 'Global Dev Blog',
          blogDescription: 'Production-grade AI engineering, Autonomous Systems, and Full-Stack Development Journey',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
        gtag: {
          trackingID: 'G-VM2CVW28SL',
          anonymizeIP: true,
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/social-card.png',
    metadata: [
      { name: 'referrer', content: 'strict-origin-when-cross-origin' },
      { name: 'author', content: 'Jaybee' },
      { name: 'naver-site-verification', content: 'f04ea0b38166c1e280ce8e18acef37093b75f383' },
    ],
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Global Dev Blog',
      logo: {
        alt: 'Global Dev Blog Logo',
        src: 'img/logo.svg',
      },
      items: [
        {to: '/blog', label: 'Blog', position: 'left'},
        {to: '/about', label: 'About', position: 'left'},
        {to: '/privacy-policy', label: 'Privacy Policy', position: 'left'},
        {to: '/contact', label: 'Contact', position: 'left'},
        { type: 'localeDropdown', position: 'right' },
        {
          href: 'https://github.com/jbjihwan/global_blog',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Explore & Feed',
          items: [
            {
              label: 'Blog Hub & All Posts',
              to: '/blog',
            },
            {
              label: 'GitHub Source Code',
              href: 'https://github.com/jbjihwan/global_blog',
            },
          ],
        },
        {
          title: 'About & Legal',
          items: [
            {
              label: 'About',
              to: '/about',
            },
            {
              label: 'Privacy Policy',
              to: '/privacy-policy',
            },
            {
              label: 'Contact',
              to: '/contact',
            },
          ],
        },
        {
          title: 'Connect & Code',
          items: [
            {
              label: 'GitHub Profile',
              href: 'https://github.com/jbjihwan',
            },
            {
              label: 'Blog Repository',
              href: 'https://github.com/jbjihwan/global_blog',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Jaybee. All rights reserved. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
