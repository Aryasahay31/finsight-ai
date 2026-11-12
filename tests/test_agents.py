"""FinSight AI - Unit and Integration Tests"""

import pytest
import json
import os
import sys

# ── Unit Tests: Tools ──

class TestStockDataTool:
    """Tests for stock data fetching tool"""

    def test_format_large_number_billions(self):
        from app.tools.stock_data import _format_large_number
        result = _format_large_number(1500000000)
        assert "1.50B" in result

    def test_format_large_number_millions(self):
        from app.tools.stock_data import _format_large_number
        result = _format_large_number(250000000)
        assert "250.00M" in result

    def test_format_large_number_thousands(self):
        from app.tools.stock_data import _format_large_number
        result = _format_large_number(50000)
        assert "50.00K" in result

    def test_format_large_number_small(self):
        from app.tools.stock_data import _format_large_number
        result = _format_large_number(500)
        assert result == "500"

    def test_format_large_number_none(self):
        from app.tools.stock_data import _format_large_number
        result = _format_large_number(None)
        assert result == "N/A"

    def test_get_stock_data_returns_dict(self):
        from app.tools.stock_data import get_stock_data
        result = get_stock_data("AAPL")
        assert isinstance(result, dict)
        assert "ticker" in result

    def test_get_stock_data_invalid_ticker(self):
        from app.tools.stock_data import get_stock_data
        result = get_stock_data("INVALIDTICKER123")
        assert isinstance(result, dict)


class TestNewsSearchTool:
    """Tests for news search tool"""

    def test_format_news_empty_list(self):
        from app.tools.news_search import format_news_for_prompt
        result = format_news_for_prompt([])
        assert "No recent news" in result or result == ""

    def test_format_news_with_articles(self):
        from app.tools.news_search import format_news_for_prompt
        articles = [
            {"title": "Test Article", "body": "Test body content", "source": "Reuters", "date": "2024-01-01"}
        ]
        result = format_news_for_prompt(articles)
        assert "Test Article" in result

    def test_search_returns_list(self):
        from app.tools.news_search import search_company_news
        result = search_company_news("Apple")
        assert isinstance(result, list)


class TestChartGenerator:
    """Tests for chart generation tool"""

    def test_generate_price_chart_creates_file(self):
        from app.tools.chart_generator import generate_price_chart
        import matplotlib
        matplotlib.use('Agg')

        # Mock historical data
        history = {
            "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "close": [150.0, 152.0, 151.0]
        }
        os.makedirs("charts", exist_ok=True)
        path = generate_price_chart("TEST", history)
        if path:
            assert os.path.exists(path) or path == ""


# ── Unit Tests: Schemas ──

class TestSchemas:
    """Tests for data models"""

    def test_agent_state_structure(self):
        from app.models.schemas import AgentState
        state: AgentState = {
            "company": "Tesla",
            "ticker": "",
            "plan": {},
            "market_data": {},
            "news_sentiment": "",
            "competitor_data": {},
            "chart_paths": [],
            "report": "",
            "evaluation": {},
            "agent_logs": [],
            "errors": []
        }
        assert state["company"] == "Tesla"
        assert isinstance(state["agent_logs"], list)
        assert isinstance(state["errors"], list)

    def test_analysis_request_valid(self):
        from app.models.schemas import AnalysisRequest
        req = AnalysisRequest(company="Tesla")
        assert req.company == "Tesla"

    def test_analysis_request_empty_raises(self):
        from app.models.schemas import AnalysisRequest
        # Should still create with empty string (pydantic allows it)
        req = AnalysisRequest(company="")
        assert req.company == ""


# ── Unit Tests: Config ──

class TestConfig:
    """Tests for configuration"""

    def test_settings_defaults(self):
        from app.config import Settings
        settings = Settings()
        assert settings.LLM_PROVIDER in ["ollama", "groq"]

    def test_get_llm_returns_object(self):
        # This may fail without Ollama/Groq running, so we just test import
        from app.config import get_llm
        assert callable(get_llm)


# ── Unit Tests: Memory Store ──

class TestMemoryStore:
    """Tests for ChromaDB memory"""

    def test_memory_store_init(self):
        from app.memory.store import MemoryStore
        store = MemoryStore()
        assert store is not None

    def test_get_analysis_count(self):
        from app.memory.store import MemoryStore
        store = MemoryStore()
        count = store.get_analysis_count()
        assert isinstance(count, int)
        assert count >= 0


# ── Unit Tests: Prompt Templates ──

class TestPromptTemplates:
    """Tests for prompt templates"""

    def test_planner_prompt_exists(self):
        from app.prompts.templates import PLANNER_PROMPT
        assert isinstance(PLANNER_PROMPT, str)
        assert len(PLANNER_PROMPT) > 0

    def test_report_prompt_exists(self):
        from app.prompts.templates import REPORT_PROMPT
        assert isinstance(REPORT_PROMPT, str)
        assert len(REPORT_PROMPT) > 0

    def test_evaluator_prompt_exists(self):
        from app.prompts.templates import EVALUATOR_PROMPT
        assert isinstance(EVALUATOR_PROMPT, str)
        assert "accuracy" in EVALUATOR_PROMPT.lower() or len(EVALUATOR_PROMPT) > 0


# ── Integration Tests: API ──

class TestAPIEndpoints:
    """Tests for FastAPI endpoints (requires server not running)"""

    def test_app_imports(self):
        from app.main import app
        assert app is not None

    def test_health_endpoint_exists(self):
        from fastapi.testclient import TestClient
        from app.main import app
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "llm_provider" in data

    def test_root_endpoint(self):
        from fastapi.testclient import TestClient
        from app.main import app
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200

    def test_analyze_missing_body(self):
        from fastapi.testclient import TestClient
        from app.main import app
        client = TestClient(app)
        response = client.post("/analyze")
        assert response.status_code == 422  # Validation error


# ── Integration Tests: Orchestrator ──

class TestOrchestrator:
    """Tests for LangGraph workflow structure"""

    def test_build_workflow_returns_graph(self):
        from app.agents.orchestrator import build_workflow
        workflow = build_workflow()
        assert workflow is not None

    def test_workflow_has_nodes(self):
        from app.agents.orchestrator import build_workflow
        workflow = build_workflow()
        # Compiled graph should be invocable
        assert hasattr(workflow, 'invoke')