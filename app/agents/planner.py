"""Planner Agent - Identifies company ticker and competitors"""

import json
import re
from app.config import get_llm
from app.models.schemas import AgentState


def planner_agent(state: AgentState) -> AgentState:
    """Identifies stock ticker and competitor companies"""
    company = state["company"]
    llm = get_llm()

    prompt = f"""You are a financial analyst. For the company "{company}", provide:
1. The stock ticker symbol (US market, e.g., TSLA for Tesla, AAPL for Apple, MSFT for Microsoft, GOOGL for Google/Alphabet, AMZN for Amazon, META for Meta/Facebook, RELIANCE.NS for Reliance Industries)
2. Exactly 3 competitor company ticker symbols in the same market

IMPORTANT: Use standard Yahoo Finance ticker symbols. For US companies use simple symbols like TSLA, AAPL, MSFT. For Indian companies use .NS suffix like RELIANCE.NS, TCS.NS, INFY.NS.

Respond ONLY in this exact JSON format, nothing else:
{{"ticker": "SYMBOL", "competitors": ["COMP1", "COMP2", "COMP3"]}}

Example for Tesla:
{{"ticker": "TSLA", "competitors": ["GM", "F", "RIVN"]}}

Example for Reliance Industries:
{{"ticker": "RELIANCE.NS", "competitors": ["TCS.NS", "INFY.NS", "HDFCBANK.NS"]}}

Your response (JSON only, no explanation):"""

    try:
        response = llm.invoke(prompt)
        content = response.content.strip()

        # Try to extract JSON from response
        json_match = re.search(r'\{.*?\}', content, re.DOTALL)
        if json_match:
            plan = json.loads(json_match.group())
        else:
            plan = json.loads(content)

        state["plan"] = plan
        state["ticker"] = plan.get("ticker", company.upper())
        state["agent_logs"].append(f"Planner: {company} → {state['ticker']} | Competitors: {plan.get('competitors', [])}")

    except Exception as e:
        state["errors"].append(f"Planner error: {str(e)}")
        # Fallback - use company name as ticker
        state["ticker"] = company.upper()
        state["plan"] = {"ticker": company.upper(), "competitors": []}
        state["agent_logs"].append(f"Planner: Failed, using fallback ticker {company.upper()}")

    return state