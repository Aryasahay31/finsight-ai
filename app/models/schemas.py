"""FinSight AI - Data Models"""

from typing import TypedDict
from pydantic import BaseModel


class AgentState(TypedDict):
    company: str
    ticker: str
    plan: list[str]
    market_data: dict
    news_sentiment: dict
    competitor_data: dict
    chart_paths: list[str]
    report: str
    evaluation: dict
    agent_logs: list[str]
    errors: list[str]


class AnalysisRequest(BaseModel):
    company: str


class AnalysisResponse(BaseModel):
    company: str
    ticker: str
    report: str
    evaluation: dict
    chart_paths: list[str]
    agent_logs: list[str]
    errors: list[str]