import React from 'react';
import { Database, Sun, Moon, Loader2 } from 'lucide-react';

const Header = ({ 
  darkMode, 
  toggleDarkMode, 
  systemStatus, 
  loading, 
  initializeSystem 
}) => {
  return (
    <header className="header">
      <div className="container">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Database size={24} style={{color: '#3b82f6'}} />
            <h1 className="text-xl">RAG Search System</h1>
          </div>
          
          <div className="flex items-center gap-3">
            <StatusBadge status={systemStatus} />
            
            <button
              onClick={toggleDarkMode}
              className="btn btn-gray"
              title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
            
            {!systemStatus?.system_ready && (
              <button
                onClick={initializeSystem}
                disabled={loading}
                className="btn btn-blue"
              >
                {loading && <Loader2 size={16} style={{animation: 'spin 1s linear infinite'}} />}
                Initialize System
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

const StatusBadge = ({ status }) => {
  console.log(status)
  if (!status) {
    return (
      <div className="status status-loading">
        <Loader2 size={16} style={{animation: 'spin 1s linear infinite'}} />
        Checking...
      </div>
    );
  }

  if (status.system_ready) {
    return (
      <div className="status status-ready">
        Ready ({status.database_status})
      </div>
    );
  }

  return (
    <div className="status status-error">
      Not Ready
    </div>
  );
};

export default Header;