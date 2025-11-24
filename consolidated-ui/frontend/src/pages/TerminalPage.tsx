/**
 * Terminal Page
 *
 * Displays terminal monitoring interface with real-time output streaming
 * Route: /terminals
 */

import React from 'react';
import { TerminalMonitor } from '../components/terminals/TerminalMonitor';

export const TerminalPage: React.FC = () => {
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Terminal Monitor</h1>
        <p className="page-subtitle">Real-time terminal output and management</p>
      </header>

      <main className="page-content">
        <TerminalMonitor />
      </main>
    </div>
  );
};

export default TerminalPage;
