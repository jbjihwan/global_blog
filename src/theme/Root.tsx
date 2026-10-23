import React from 'react';
import WelcomeToast from '@site/src/components/WelcomeToast';

export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <WelcomeToast />
    </>
  );
}
