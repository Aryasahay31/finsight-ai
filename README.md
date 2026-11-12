# FinSight AI

A multi-agent financial analysis platform built with LangGraph, FastAPI, and Streamlit. The system orchestrates 7 specialized AI agents through a stateful workflow to produce investment research reports with real market data, news sentiment analysis, competitor comparisons, and auto-generated charts.

## What it demonstrates

- **Multi-agent orchestration** using LangGraph StateGraph with shared typed state
- **Plan-and-Execute pattern** where a Planner agent decomposes tasks for downstream agents
- **ReAct pattern** in the News Sentiment agent (Think, Act, Observe cycle)
- **Tool integration** with yfinance (market data), DuckDuckGo (news search), and matplotlib (charts)
- **LLM-as-Judge evaluation** where an Evaluator agent scores the final report on accuracy, completeness, clarity, and usefulness
- **Persistent vector memory** using ChromaDB to store and recall past analyses
- **Provider flexibility** with support for both Ollama (local) and Groq (cloud) LLMs

## Architecture
User Input (Company Name)
|
[1. Planner Agent]
| Identifies ticker symbol and 3 competitors
v
[2. Market Data Agent]
| Fetches stock price, volume, market cap, P/E, 52-week range
v
[3. News Sentiment Agent]
| Searches recent news and runs sentiment analysis
v
[4. Competitor Agent]
| Pulls competitor data and generates comparison
v
[5. Chart Generator Agent]
| Creates price history, volume, and comparison charts
v
[6. Report Writer Agent]
| Writes structured investment research report
v
[7. Evaluator Agent]
| Scores report quality (LLM-as-Judge)
v
Final Output (Report + Charts + Evaluation)

All agents share a single `AgentState` (TypedDict) that flows through the LangGraph StateGraph. Each agent reads from and writes to this shared state.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Orchestration | LangGraph (StateGraph) |
| LLM | Ollama (Llama 3.2) or Groq (Llama 3.1) |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Market Data | yfinance |
| News Search | DuckDuckGo Search |
| Charts | matplotlib |
| Memory | ChromaDB (persistent vector store) |
| Containerization | Docker + docker-compose |

## Project Structure

All agents share a single `AgentState` (TypedDict) that flows through the LangGraph StateGraph. Each agent reads from and writes to this shared state.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Orchestration | LangGraph (StateGraph) |
| LLM | Ollama (Llama 3.2) or Groq (Llama 3.1) |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Market Data | yfinance |
| News Search | DuckDuckGo Search |
| Charts | matplotlib |
| Memory | ChromaDB (persistent vector store) |
| Containerization | Docker + docker-compose |

## Project Structure
finsight-ai/
├── app/
│ ├── config.py # LLM provider config and factory
│ ├── main.py # FastAPI endpoints
│ ├── models/
│ │ └── schemas.py # AgentState, request/response models
│ ├── prompts/
│ │ └── templates.py # Prompt templates for all agents
│ ├── tools/
│ │ ├── stock_data.py # yfinance integration
│ │ ├── news_search.py # DuckDuckGo news search
│ │ └── chart_generator.py # matplotlib chart generation
│ ├── memory/
│ │ └── store.py # ChromaDB vector memory
│ └── agents/
│ ├── planner.py # Task decomposition
│ ├── market_data.py # Stock data fetching
│ ├── news_sentiment.py # News search + sentiment
│ ├── competitor.py # Peer comparison
│ ├── chart_agent.py # Chart generation
│ ├── report_writer.py # Report synthesis
│ ├── evaluator.py # LLM-as-Judge scoring
│ └── orchestrator.py # LangGraph workflow builder
├── frontend/
│ └── app.py # Streamlit UI
├── tests/
│ └── test_agents.py # Unit tests
├── .env.example # Environment config template
├── requirements.txt
├── Dockerfile
└── docker-compose.yml

## Setup

### Prerequisites

- Python 3.11+
- Groq API key (free at [console.groq.com](https://console.groq.com)) or Ollama installed locally

### Installation

```bash
git clone https://github.com/Aryasahay31/finsight-ai.git
cd finsight-ai
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
```

Edit `.env` and set your LLM provider:
LLM_PROVIDER=groq
GROQ_API_KEY=your_actual_key_here

### Running

Start the backend:

```bash
uvicorn app.main:app --reload
```

Start the frontend (in a separate terminal):

```bash
streamlit run frontend/app.py
```

Open `http://localhost:8501` in your browser.

### Docker

```bash
docker-compose up --build
```

## Usage

1. Enter a company name (e.g., Tesla, Apple, Reliance Industries)
2. Click Analyze
3. The 7-agent pipeline runs sequentially
4. View results across four tabs: Report, Charts, Evaluation, Agent Logs

## Agentic AI Concepts Covered

| Concept | Implementation |
|---------|---------------|
| Multi-Agent Systems | 7 specialized agents in a LangGraph workflow |
| Shared State | AgentState (TypedDict) passed through all agents |
| Plan-and-Execute | Planner agent decomposes company analysis into subtasks |
| ReAct Pattern | News Sentiment agent uses Think/Act/Observe cycle |
| Tool Use | yfinance, DuckDuckGo, matplotlib as agent tools |
| LLM-as-Judge | Evaluator agent scores report on 4 dimensions |
| Vector Memory | ChromaDB stores past analyses for retrieval |
| Guardrails | Error handling with graceful fallbacks per agent |
| Orchestration | LangGraph StateGraph manages agent execution order |

## License

MIT
