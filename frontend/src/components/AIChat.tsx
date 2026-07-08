import React, { useState, useRef, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from '../store';
import { sendMessage } from '../store/interactionSlice';
import { Send, Loader2, Bot } from 'lucide-react';

const AIChat: React.FC = () => {
  const [input, setInput] = useState('');
  const dispatch = useDispatch<AppDispatch>();
  const { chatHistory, isLoading } = useSelector((state: RootState) => state.interaction);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, isLoading]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    dispatch(sendMessage(input));
    setInput('');
  };

  return (
    <div className="glass-panel right-panel">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', paddingBottom: '0.5rem', borderBottom: '1px solid var(--surface-border)' }}>
        <Bot color="var(--primary)" size={24} />
        <h3 style={{ color: 'var(--text-main)', fontWeight: 600 }}>AI Assistant</h3>
      </div>
      
      <div className="chat-container">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {isLoading && (
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <form onSubmit={handleSend} className="chat-input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe interaction..."
          disabled={isLoading}
          style={{ flex: 1 }}
        />
        <button type="submit" className="btn-primary" disabled={isLoading || !input.trim()} style={{ display: 'flex', gap: '0.5rem' }}>
          {isLoading ? <Loader2 size={18} /> : (
            <>
              <Send size={18} />
              <span>Log</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default AIChat;
