"""FinSight AI - Agent Orchestrator (LangGraph)"""

from langgraph.graph import StateGraph, END
from app.models.schemas import AgentState
from app.agents.planner import planner_agent
from app.agents.market_data import market_data_agent
from app.agents.news_sentiment import news_sentiment_agent
from app.agents.competitor import competitor_agent
from app.agents.chart_agent import chart_agent
from app.agents.report_writer import report_writer_agent
from app.agents.evaluator import evaluator_agent


def build_workflow() -> StateGraph:
    """Build and compile the multi-agent workflow graph."""
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_agent)
    workflow.add_node("market_data", market_data_agent)
    workflow.add_node("news_sentiment", news_sentiment_agent)
    workflow.add_node("competitor", competitor_agent)
    workflow.add_node("chart_generator", chart_agent)
    workflow.add_node("report_writer", report_writer_agent)
    workflow.add_node("evaluator", evaluator_agent)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "market_data")
    workflow.add_edge("market_data", "news_sentiment")
    workflow.add_edge("news_sentiment", "competitor")
    workflow.add_edge("competitor", "chart_generator")
    workflow.add_edge("chart_generator", "report_writer")
    workflow.add_edge("report_writer", "evaluator")
    workflow.add_edge("evaluator", END)

    return workflow.compile()


agent_workflow = build_workflow()


def run_analysis(company: str) -> AgentState:
    """Run the full analysis pipeline for a company."""
    initial_state: AgentState = {
        "company": company,
        "ticker": "",
        "plan": [],
        "market_data": {},
        "news_sentiment": {},
        "competitor_data": {},
        "chart_paths": [],
        "report": "",
        "evaluation": {},
        "agent_logs": [],
        "errors": [],
    }
    result = agent_workflow.invoke(initial_state)
    return result