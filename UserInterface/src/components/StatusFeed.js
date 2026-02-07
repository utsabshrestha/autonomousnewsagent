import React, { useState } from 'react';
import { Search, Globe, Loader, CheckCircle, FileText } from 'lucide-react';

const StatusFeed = ({ topic, queries, foundUrls, currentAction }) => {
  
  // Track expanded state for each loop's queries and sources
  const [expandedQueries, setExpandedQueries] = useState({});
  const [expandedSources, setExpandedSources] = useState({});
  
  // Helper to get a favicon (Google's free service)
  const getFavicon = (url) => {
    try {
      const domain = new URL(url).hostname;
      return `https://www.google.com/s2/favicons?domain=${domain}&sz=32`;
    } catch {
      return "";
    }
  };

  const toggleQueries = (loopIndex) => {
    setExpandedQueries(prev => ({
      ...prev,
      [loopIndex]: !prev[loopIndex]
    }));
  };

  const toggleSources = (loopIndex) => {
    setExpandedSources(prev => ({
      ...prev,
      [loopIndex]: !prev[loopIndex]
    }));
  };

  return (
    <div className="status-feed-container">
      <h2>Researching: <span className="highlight">"{topic}"</span></h2>

      <div className="feed-steps">
        
        {/* ALTERNATING SEARCH & SOURCES BLOCKS - Loop through each iteration */}
        {queries.map((queryBatch, loopIndex) => (
          <React.Fragment key={`loop-${loopIndex}`}>
            
            {/* STEP 1: SEARCH QUERIES for this loop */}
            <div className="step-item">
              <div className="step-icon">
                <Search size={20} className="icon-blue" />
              </div>
              <div className="step-content">
                {loopIndex == 0 ? (<h3>Searching</h3>) : (<h3>Re-Searching</h3>)}
                <div className="query-pills">
                  {(expandedQueries[loopIndex] ? queryBatch : queryBatch.slice(0, 3)).map((q, i) => (
                    <div key={i} className="pill">
                      <Search size={12} /> {q}
                    </div>
                  ))}
                  {queryBatch.length > 3 && (
                      <div 
                        className="more-count clickable" 
                        onClick={() => toggleQueries(loopIndex)}
                      >
                        {expandedQueries[loopIndex] 
                          ? "Show less" 
                          : `...and ${queryBatch.length - 3} more`
                        }
                      </div>
                  )}
                </div>
              </div>
            </div>

            {/* STEP 2: FOUND SOURCES for this loop (if available) */}
            {foundUrls[loopIndex] && foundUrls[loopIndex].length > 0 && (
              <div className="step-item">
                <div className="step-icon">
                  <Globe size={20} className="icon-green" />
                </div>
                <div className="step-content">
                  <h3>Reviewed {foundUrls[loopIndex].length} Sources</h3>
                  <div className="sources-list-grid">
                    {(expandedSources[loopIndex] ? foundUrls[loopIndex] : foundUrls[loopIndex].slice(0, 6)).map((source, i) => (
                      <a 
                        key={i} 
                        href={source.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="mini-source-card"
                      >
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
                      </a>
                    ))}
                  </div>
                  {foundUrls[loopIndex].length > 6 && (
                    <div 
                      className="more-count clickable" 
                      onClick={() => toggleSources(loopIndex)}
                    >
                      {expandedSources[loopIndex] 
                        ? "Show less" 
                        : `...and ${foundUrls[loopIndex].length - 6} more`
                      }
                    </div>
                  )}
                </div>
              </div>
            )}

          </React.Fragment>
        ))}

        {/* STEP 3: CURRENT ACTION - Always at bottom */}
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