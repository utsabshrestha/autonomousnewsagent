
# 🌍 Autonomous Global News Briefing Agent

![Python](https://img.shields.io/badge/Python-3.11-blue) ![LangGraph](https://img.shields.io/badge/AI-LangGraph-orange) ![Gemini](https://img.shields.io/badge/Model-Gemini%202.0%20Flash-magenta) ![React](https://img.shields.io/badge/Frontend-React-blue)

An autonomous AI agent that acts as a digital investigative journalist. Unlike simple "search wrapper" tools, this agent employs a **Plan-Act-Verify-Refine** loop to conduct deep research, critically evaluate sources, and synthesize factual reports with inline citations.

> **Key Differentiator:** Implements a **Self-Reflective Architecture** using LangGraph. If the agent finds irrelevant search results, it autonomously rejects them, rewrites its search query, and tries again—just like a human researcher.

---

## 🚀 Features

*   **🧠 Cognitive Architecture:** Uses a state machine (LangGraph) to manage the research lifecycle, not just a linear chain.
*   **🔄 Self-Correction Loop:** The "Critic" node evaluates search results for relevance. If data is insufficient, it triggers a "Re-Plan" state to change search strategies.
*   **⚡ Parallel Execution:** Uses `async` fan-out patterns to scrape and process multiple news sources simultaneously.
*   **🛡️ Hallucination Defense:** Enforces a "Filter-then-Act" workflow. Only sources that pass a strict LLM evaluation are scraped.
*   **📡 Real-Time Observability:** Frontend displays the agent's "thought process" via Server-Sent Events (SSE), showing users exactly what the AI is researching.
*   **🖼️ Multimedia Synthesis:** Extracts hero images from news sources to create a visual "News Card" interface alongside the text report.

---

## 🛠️ Tech Stack

*   **Orchestration:** [LangGraph](https://langchain-ai.github.io/langgraph/) (State Management & Cyclic Graphs)
*   **LLM Brain:** Google Gemini 2.0 Flash (1M Context Window)
*   **Search & Data:** Brave Search API (Discovery) + Jina AI (Scraping)
*   **Backend:** FastAPI (Python) with Streaming Response
*   **Frontend:** React (TypeScript) + Markdown Rendering

---

## 🧩 Architecture Flow

The system follows a strict graph topology to ensure reliability:

```mermaid
graph TD
    A[User Topic] --> B(Planner Node)
    B --> C{Search Node}
    C --> D[Deduplication & Blacklist]
    D --> E(Evaluator Node)
    E --> F{Sufficient Info?}
    F -- No --> B
    F -- Yes --> G[Parallel Scraper Dispatch]
    G --> H(Scrape Node 1) & I(Scrape Node 2) & J(Scrape Node 3)
    H & I & J --> K(Reporter Node)
    K --> L[Final Briefing]
```

### Node Breakdown

1.  **Planner Node:** Analyzes the user request and generates specific search queries (e.g., converting "Apple news" to "Apple stock performance Q4 2025").
2.  **Search & Dedupe:** Fetches results and removes duplicates or previously rejected URLs (Blacklisting).
3.  **Evaluator (The Critic):** An LLM call that judges snippets. It separates "Signal" from "Noise."
4.  **Router (The Switch):**
    *   *If < 3 valid sources:* Loop back to **Planner** with instructions to try new keywords.
    *   *If >= 3 valid sources:* Proceed to scraping.
5.  **Scraper:** Extracts main text and Hero Images using Regex + BeautifulSoup.
6.  **Reporter:** Synthesizes a markdown report with Harvard-style inline citations `[1]`.

---

## 📸 Demo

*(Add a screenshot here of your React UI showing the "News Cards" at the top and the "Agent Neural Log" sidebar)*

---

## 💻 Installation & Setup

### Prerequisites
*   Python 3.10+
*   Node.js & npm
*   API Keys: `GOOGLE_API_KEY`, `BRAVE_API_KEY`

### Backend
```bash
# Clone repository
git clone https://github.com/yourusername/news-agent.git
cd news-agent/backend

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI Server
python server.py
```

### Frontend
```bash
cd ../frontend
npm install
npm start
```

---

## 🧠 What I Learned

*   **State Management in AI:** How to use `TypedDict` and `operator.add` to maintain context across multiple autonomous loops.
*   **Conditional Routing:** Implementing logic gates in graphs to handle failure states (e.g., "Search yielded 0 results").
*   **Streaming Patterns:** Handling asynchronous data streams to push "Thought Logs" to the UI for better UX.

---

## 📜 License

MIT License.

---

### Tips for your Github Upload:
1.  **Generate that Mermaid Diagram:** GitHub renders the text inside the `mermaid` block as a real diagram automatically!
2.  **Screenshots:** Since you built a UI, **take a screenshot**. A project with a screenshot gets 10x more views than one without.
3.  **Clean Code:** Before uploading, run `pip freeze > requirements.txt` in your backend folder so others can install your libraries easily.