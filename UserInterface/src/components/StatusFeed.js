import React from 'react';
import { Search, Globe, Loader, CheckCircle, FileText } from 'lucide-react';

const StatusFeed = ({ topic, queries, foundUrls, currentAction }) => {
  
  // Helper to get a favicon (Google's free service)
  const getFavicon = (url) => {
    try {
      const domain = new URL(url).hostname;
      return `https://www.google.com/s2/favicons?domain=${domain}&sz=32`;
    } catch {
      return "";
    }
  };

  return (
    <div className="status-feed-container">
      <h2>Researching: <span className="highlight">"{topic}"</span></h2>

      <div className="feed-steps">
        
        {/* STEP 1: SEARCH QUERIES */}
        {queries.length > 0 && (
          <div className="step-item">
            <div className="step-icon">
              <Search size={20} className="icon-blue" />
            </div>
            <div className="step-content">
              <h3>Searching</h3>
              <div className="query-pills">
                {queries.slice(0, 3).map((q, i) => (
                  <div key={i} className="pill">
                    <Search size={12} /> {q}
                  </div>
                ))}
                {queries.length > 3 && (
                    <div className="more-count">...and {queries.length - 3} more</div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* STEP 2: FOUND SOURCES */}
        {foundUrls.length > 0 && (
          <div className="step-item">
             <div className="step-icon">
              <Globe size={20} className="icon-green" />
            </div>
            <div className="step-content">
              <h3>Reviewed {foundUrls.length} Sources</h3>
              <div className="sources-list-grid">
                {foundUrls.slice(0, 6).map((source, i) => (
                  <div key={i} className="mini-source-card">
                    <img 
                      src={getFavicon(source.url)} 
                      alt="icon" 
                      className="favicon"
                      onError={(e) => e.target.style.display = 'none'} 
                    />
                    <div className="source-info">
                      <span className="source-title">{source.title || "News Article"}</span>
                      <span className="source-domain">{new URL(source.url).hostname.replace('www.', '')}</span>
                    </div>
                  </div>
                ))}
                {foundUrls.length > 6 && (
                   <div className="more-count">...and {foundUrls.length - 6} more</div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* STEP 3: CURRENT ACTION (Scraping/Thinking) */}
        <div className="step-item active">
          <div className="step-icon">
            <Loader size={20} className="spin" />
          </div>
          <div className="step-content">
            <h3>{currentAction || "Initializing..."}</h3>
            <p className="subtext">Extracting facts and verifying citations...</p>
          </div>
        </div>

      </div>
    </div>
  );
};

export default StatusFeed;