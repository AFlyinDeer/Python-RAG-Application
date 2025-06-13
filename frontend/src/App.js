import React, { useState, useEffect, useRef } from 'react';
import { Search, Database, AlertCircle, Loader2 } from 'lucide-react';
import Header from './components/Header';
import Message from './components/Message';

const App = () => {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState(null);
  const [error, setError] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const messagesEndRef = useRef(null);

  const API_BASE = 'http://localhost:5000/api';

  useEffect(() => {
    checkSystemStatus();
    initializeTheme();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const initializeTheme = () => {
    const savedTheme = localStorage.getItem('primeTheme');
    const isDark = savedTheme === 'dark';
    setDarkMode(isDark);
    
    setTimeout(() => {
      loadTheme(isDark ? 'lara-dark-blue' : 'lara-light-blue');
    }, 100);
    
    document.documentElement.classList.toggle('dark', isDark);
  };

  const loadTheme = (themeName) => {
    const existingLink = document.getElementById('theme-link');
    if (existingLink) existingLink.remove();
    
    const link = document.createElement('link');
    link.id = 'theme-link';
    link.rel = 'stylesheet';
    link.href = `https://unpkg.com/primereact/resources/themes/${themeName}/theme.css`;
    document.head.appendChild(link);
  };

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    loadTheme(newDarkMode ? 'lara-dark-blue' : 'lara-light-blue');
    document.documentElement.classList.toggle('dark', newDarkMode);
    setDarkMode(newDarkMode);
    localStorage.setItem('primeTheme', newDarkMode ? 'dark' : 'light');
  };

  const checkSystemStatus = async () => {
    try {
      const response = await fetch(`${API_BASE}/status`);
      const data = await response.json();
      setSystemStatus(data);
      console.log(data)
      setError(data.system_ready ? '' : 'System not ready. Click "Initialize System" to setup.');
    } catch (err) {
      setSystemStatus({system_ready: false})
      setError('Cannot connect to backend. Make sure Flask server is running.');
    }
  };

  const initializeSystem = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_BASE}/initialize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      
      const data = await response.json();
      
      if (data.success) {
        setError('');
        checkSystemStatus();
        addMessage('system', 'System initialized successfully! You can now ask questions.');
      } else {
        setError(data.error);
      }
    } catch (err) {
      setSystemStatus({system_ready: false})
      setError('Failed to initialize system. Check console for details.');
    } finally {
      setLoading(false);
    }
  };

  const addMessage = (type, content, sources = []) => {
    setMessages(prev => [...prev, {
      id: Date.now(),
      type,
      content,
      sources
    }]);
  };

  const handleSearch = async (e) => {
    e.preventDefault?.();
    
    if (!question.trim() || !systemStatus?.system_ready) return;

    const currentQuestion = question.trim();
    setQuestion('');
    setLoading(true);
    setError('');

    addMessage('user', currentQuestion);

    try {
      const response = await fetch(`${API_BASE}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: currentQuestion })
      });

      const data = await response.json();

    // Replace the success check with:
    if (response.ok && data.answer) {
      addMessage('assistant', data.answer, data.sources);
      
    } else {
      setError(data.error || 'Unknown error occurred');
      addMessage('error', `Error: ${data.error || 'Unknown error'}`);
    }
    } catch (err) {
      const errorMsg = 'Failed to get response. Check if the server is running.';
      setError(errorMsg);
      addMessage('error', errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`app ${darkMode ? 'dark' : ''}`}>
      <Header 
        darkMode={darkMode}
        toggleDarkMode={toggleDarkMode}
        systemStatus={systemStatus}
        loading={loading}
        initializeSystem={initializeSystem}
      />

      {error && (
        <div className="error-banner">
          <div className="container flex items-center gap-3">
            <AlertCircle size={20} />
            {error}
          </div>
        </div>
      )}

      <main className="content" style={{paddingTop: error ? '140px' : '100px'}}>
        <div className="container">
          {messages.length === 0 ? (
            <div className="welcome">
              <Database size={48} style={{margin: '0 auto 1rem', opacity: 0.5}} />
              <h2 style={{fontSize: '1.25rem', fontWeight: 500, marginBottom: '0.5rem'}}>
                Welcome to RAG Search
              </h2>
              <p>Ask questions about your documents to get started.</p>
            </div>
          ) : (
            <>
              {messages.map(message => (
                <Message key={message.id} message={message} />
              ))}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>
      </main>

      <footer className="footer">
        <div className="container">
          <div className="flex gap-3">
            <div style={{flex: 1, position: 'relative'}}>
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask a question about your documents..."
                disabled={loading || !systemStatus?.system_ready}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch(e)}
                className="input"
              />
              <Search 
                size={20} 
                style={{
                  position: 'absolute',
                  right: '0.75rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  color: 'var(--text-muted)'
                }}
              />
            </div>
            <button
              onClick={handleSearch}
              disabled={loading || !question.trim() || !systemStatus?.system_ready}
              className="btn btn-blue"
            >
              {loading ? (
                <>
                  <Loader2 size={16} style={{animation: 'spin 1s linear infinite'}} />
                  Searching...
                </>
              ) : (
                'Search'
              )}
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;