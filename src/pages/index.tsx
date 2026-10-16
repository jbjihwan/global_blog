import React from 'react';
import { Redirect } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  // Redirect users landing on the homepage directly to the blog
  return <Redirect to={`${siteConfig.baseUrl}blog`} />;
}
