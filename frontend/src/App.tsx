import React from 'react';
import InteractionForm from './components/InteractionForm';
import AIChat from './components/AIChat';

const App: React.FC = () => {
  return (
    <div className="app-container">
      <InteractionForm />
      <AIChat />
    </div>
  );
};

export default App;
