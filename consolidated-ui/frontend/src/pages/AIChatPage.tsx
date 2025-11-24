import React from 'react';
import { AIAssistant } from '../components/AIAssistant/AIAssistant';

export const AIChatPage: React.FC = () => {
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>AI Assistant</h1>
        <p className="page-subtitle">
          Get help with development tasks, coding questions, and technical guidance
        </p>
      </header>

      <main className="page-content">
        <AIAssistant />
      </main>
    </div>
  );
};

export default AIChatPage;
