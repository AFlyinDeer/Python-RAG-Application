import React from 'react';
import { FileText } from 'lucide-react';

const Message = ({ message }) => {
  const getMessageClass = () => {
    switch (message.type) {
      case 'user': return 'message message-user';
      case 'error': return 'message message-error';
      case 'system': return 'message message-system';
      default: return 'message message-assistant';
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start' }}>
      <div className={getMessageClass()}>
        <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
        
        {message.sources && message.sources.length > 0 && (
          <div className="sources">
            <div style={{ fontWeight: 500, marginBottom: '0.5rem' }}>Sources:</div>
            {message.sources.map((source, idx) => (
              <div key={idx} className="source">
                <FileText size={16} style={{ marginTop: '0.125rem', flexShrink: 0 }} />
                <div>
                  <div style={{ fontWeight: 500 }}>
                    {typeof source === 'string' ? source : `${source.file} (p.${source.page})`}
                    {typeof source === 'object' && source.type && (
                      <span style={{ 
                        marginLeft: '0.25rem', 
                        fontSize: '0.75rem', 
                        background: 'var(--bg-tertiary)', 
                        padding: '0.125rem 0.25rem', 
                        borderRadius: '0.25rem' 
                      }}>
                        {source.type}
                      </span>
                    )}
                  </div>
                  {typeof source === 'object' && source.content && (
                    <div style={{ color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                      {source.content}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
        
        <div style={{ fontSize: '0.75rem', opacity: 0.7, marginTop: '0.5rem' }}>
          {message.timestamp}
        </div>
      </div>
    </div>
  );
};

export default Message;