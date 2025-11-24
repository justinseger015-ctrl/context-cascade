import React, { useState, useRef } from 'react';
import FloatingTextInput from '../FloatingTextInput';
import Button from '../Button';
import marked from '../../utils/marked';
import './AIAssistant.scss';

interface AIMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

export const AIAssistant: React.FC = () => {
  const [messages, setMessages] = useState<AIMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<any>();

  const handleSendMessage = async () => {
    const userInput = inputRef.current?.getValue();
    if (!userInput || !userInput.trim()) return;

    const userMessage: AIMessage = {
      role: 'user',
      content: userInput,
      timestamp: Date.now(),
    };
    setMessages(prev => [...prev, userMessage]);
    inputRef.current?.setValue('');

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_input: userInput,
          context: {
            current_agent: 'general',
            conversation_history: messages.slice(-5),
          },
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      const aiMessage: AIMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: Date.now(),
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      console.error('[AIAssistant] Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-assistant">
      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h2>Welcome to AI Assistant</h2>
            <p>Ask me anything about development, coding, or technical questions!</p>
            <p>I support Markdown and LaTeX math notation.</p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.role}`}>
            <div className="message-role">
              {msg.role === 'user' ? 'You' : 'AI Assistant'}
            </div>
            <div
              className="message-content"
              dangerouslySetInnerHTML={{
                __html: msg.role === 'assistant' ? marked(msg.content) : msg.content
              }}
            />
          </div>
        ))}

        {loading && (
          <div className="message message-assistant loading">
            <div className="message-role">AI Assistant</div>
            <div className="message-content">Thinking...</div>
          </div>
        )}

        {error && (
          <div className="message message-error">
            <div className="message-role">Error</div>
            <div className="message-content">{error}</div>
          </div>
        )}
      </div>

      <div className="input-container">
        <FloatingTextInput
          ref={inputRef}
          label="Ask the AI Assistant..."
          multiline={true}
          onEnter={handleSendMessage}
        />
        <Button onClick={handleSendMessage} disabled={loading}>
          {loading ? 'Sending...' : 'Send'}
        </Button>
      </div>
    </div>
  );
};
