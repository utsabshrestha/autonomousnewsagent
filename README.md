
# Autonomous News Briefing Agent

![Python](https://img.shields.io/badge/Python-3.11-blue) ![LangGraph](https://img.shields.io/badge/AI-LangGraph-orange) ![Gemini](https://img.shields.io/badge/Model-Gemini%202.0%20Flash-magenta) ![React](https://img.shields.io/badge/Frontend-React-blue)

An autonomous AI agent that acts as a digital investigative journalist. Unlike simple "search wrapper" tools, this agent employs a **Plan-Act-Verify-Refine** loop to conduct deep research, critically evaluate sources, and synthesize factual reports with inline citations.

> **Key Differentiator:** Implements a **Self-Reflective Architecture** using LangGraph. If the agent finds irrelevant search results, it autonomously rejects them, rewrites its search query, and tries again—just like a human researcher.

---

## Features

*   **Cognitive Architecture:** Uses a state machine (LangGraph) to manage the research lifecycle, not just a linear chain.
*   **Self-Correction Loop:** The "Critic" node evaluates search results for relevance. If data is insufficient, it triggers a "Re-Plan" state to change search strategies.
*   **Parallel Execution:** Uses `async` fan-out patterns to scrape and process multiple news sources simultaneously.
*   **Hallucination Defense:** Enforces a "Filter-then-Act" workflow. Only sources that pass a strict LLM evaluation are scraped.
*   **Real-Time Observability:** Frontend displays the agent's "thought process" via Server-Sent Events (SSE), showing users exactly what the AI is researching.
*   **Multimedia Synthesis:** Extracts hero images from news sources to create a visual "News Card" interface alongside the text report.

---
Screenshots : 
<img width="1057" height="600" alt="image" src="https://github.com/user-attachments/assets/ebe3411c-e316-42e5-8042-b0ac2d9ed43e" />
<img width="1064" height="610" alt="image" src="https://github.com/user-attachments/assets/f68368c1-9b10-4745-805f-ec1b389a63d1" />
<img width="1071" height="611" alt="image" src="https://github.com/user-attachments/assets/c5b72ac4-74ca-46c5-b66b-09ba03833d9a" />

* Check out the demo video: https://github.com/user-attachments/assets/abbf0d77-22c1-4380-8d89-4dc7c43624f5
---

## Tech Stack

*   **Orchestration:** [LangGraph](https://langchain-ai.github.io/langgraph/) (State Management & Cyclic Graphs)
*   **LLM Brain:** Google Gemini 2.0 Flash (1M Context Window)
*   **Search & Data:** Brave Search API (Discovery) + Jina AI (Scraping)
*   **Backend:** FastAPI (Python) with Streaming Response
*   **Frontend:** React.Js + Markdown Rendering

---

## Architecture Flow

The system follows a strict graph topology to ensure reliability:

```mermaid
graph TD
    %% --- STYLING DEFINITIONS ---
    classDef ai fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000;
    classDef logic fill:#fffde7,stroke:#fbc02d,stroke-width:2px,color:#000;
    classDef ui fill:#333,stroke:#000,stroke-width:2px,color:#fff;

    subgraph LLM
        Gemini{{Google Gemini 2.0 Flash}}
    end

    %% --- NODES ---
    User((User Topic)):::ui
    Planner(Planner Node):::ai
    
    %% Research Phase
    Router{Search Router}:::logic
    S1[Search Node 1]:::logic
    S2[Search Node 2]:::logic
    S3[Search Node 3]:::logic
    
    Dedupe[Deduplication & Blacklist]:::logic
    Evaluator(Evaluator Node):::ai
    Check{Sufficient Info?}:::logic
    
    %% Extraction Phase
    Dispatch[Scraper Dispatch]:::logic
    Scrape1[Scrape Node 1]:::logic
    Scrape2[Scrape Node 2]:::logic

    %% Synthesis Phase
    Reporter(Reporter Node):::ai
    Final[Final Briefing UI]:::ui

    %% --- FLOW CONNECTIONS ---
    User --> Planner
    Planner --> Router
    
    %% Parallel Search
    Router --> S1 & S2 & S3
    S1 & S2 & S3 --> Dedupe
    
    Dedupe --> Evaluator
    Evaluator --> Check
    
    %% The Feedback Loop
    Check -- No / Retry --> Planner
    
    %% The Success Path
    Check -- Yes --> Dispatch
    Dispatch --> Scrape1 & Scrape2
    
    Scrape1 --> Reporter
    Scrape2 --> Reporter
    Reporter --> Final
   
   Planner o-.-o Gemini
Evaluator o-.-o Gemini

```

### Node Breakdown

1.  **Planner Node:** Analyzes the user request and generates up to 3 or more specific search queries (e.g., converting "Apple news" to "Apple stock performance Q4 2025").
2.  **Search & Dedupe:** Fetches results in parallel Search Nodes using Brave Search API, gathers all the results and removes duplicates or previously rejected URLs (Blacklisting).
3.  **Evaluator (The Critic):** An LLM call that judges snippets. It separates "Signal" from "Noise."
4.  **Router (The Switch):**
    *   *If < 6 valid sources:* Loop back to **Planner** with instructions to try new keywords and not use the previously used search queries.
    *   *If >= 6 valid sources:* Proceed to scraping.
5.  **Scraper:** Extracts main text and Hero Images using Regex + JinaAi.
6.  **Reporter:** Synthesizes a markdown report with Harvard-style inline citations `[1]`.


---

## Installation & Setup

### Prerequisites
*   Python 3.10+
*   Node.js & npm
*   API Keys: `GOOGLE_API_KEY`, `BRAVE_API_KEY`, `JinaAI Api Key`

### Backend
```bash
# Clone repository
git clone https://github.com/yourusername/autonomousnewsagent.git
cd autonomousnewsagent/Agent

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI Server
python server.py
```

### Frontend
```bash
cd ../UserInterface
npm install
npm start
```

---

## What I Learned
* **LangGraph Implementation:** I learned how to utilize langgraph to develop different nodes that have its own cognitive power, how to use langgraph to orchestrate different nodes and build an AI Agent utilizing the state of the art LLM like Gemini.
*   **State Management in AI:** How to use `TypedDict` and `operator.add` to maintain context across multiple autonomous loops.
*   **Conditional Routing:** Implementing logic gates in graphs to handle failure states (e.g., "Search yielded 0 results").
*   **Streaming Patterns:** Handling asynchronous data streams to push "Thought Logs" to the UI for better UX.



