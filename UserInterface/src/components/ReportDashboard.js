import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Globe, RefreshCcw, FileText } from 'lucide-react';
import remarkGfm from 'remark-gfm'; 

const ReportDashboard = ({ report, sources, resetSearch }) => {
  return (
    <div className="report-section">
      
      {/* Header Navigation */}
      <div className="report-header">
        <div className="logo-area" onClick={resetSearch}>
          <Globe size={24} /> <span>News Agent</span>
        </div>
        <button className="new-search-btn" onClick={resetSearch}>
          <RefreshCcw size={16} /> New Investigation
        </button>
      </div>

      <div className="content-wrapper">
        
        {/* 1. VISUAL SOURCES CAROUSEL */}
        {sources.length > 0 && (
          <div className="sources-carousel">
            <h3><FileText size={18} /> Verified Sources</h3>
            <div className="cards-container">
              {sources.map((source, idx) => (
                <a key={idx} href={source.url} target="_blank" rel="noopener noreferrer" className="source-card">
                  <div className="card-image">
                    {source.image ? (
                      <img src={source.image} alt="News thumbnail" />
                    ) : (
                      <div className="placeholder-img">📰</div>
                    )}
                  </div>
                  <div className="card-info">
                    <span className="domain">{new URL(source.url).hostname.replace('www.', '')}</span>
                    <h4>{source.title}</h4>
                  </div>
                </a>
              ))}
            </div>
          </div>
        )}

        {/* 2. MAIN MARKDOWN REPORT */}
        <div className="markdown-paper">
          <ReactMarkdown remarkPlugins={[remarkGfm]} 
         components={{
              // NEW LOGIC HERE
              a: ({node, ...props}) => {
                // Check if it's an internal anchor link (Footnote)
                const isFootnote = props.href && props.href.startsWith('#');
                
                if (isFootnote) {
                  // For footnotes, just use normal behavior (scroll)
                  return (
                    <a 
                      {...props} 
                      style={{color: '#2563eb', textDecoration: 'none', cursor: 'pointer'}} 
                    />
                  );
                } else {
                  // For external websites, open in new tab
                  return (
                    <a 
                      {...props} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      style={{color: '#2563eb', textDecoration: 'underline'}} 
                    />
                  );
                }
              }
            }}
            >{report}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default ReportDashboard;