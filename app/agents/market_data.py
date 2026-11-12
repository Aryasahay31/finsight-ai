"""FinSight AI - Market Data Agent"""

from app.models.schemas import AgentState
from app.tools.stock_data import get_stock_data


def market_data_agent(state: AgentState) -> AgentState:
    """Fetch comprehensive market data for the target company."""
    ticker = state["ticker"]
    logs = state.get("agent_logs", [])
    errors = state.get("errors", [])

    logs.append(f"[Market Data] Fetching stock data for {ticker}...")

    try:
        data = get_stock_data(ticker)

        if "error" in data:
            errors.append(f"[Market Data] Error fetching {ticker}: {data['error']}")
            logs.append(f"[Market Data] Failed to fetch data for {ticker}")
            return {**state, "market_data": {}, "agent_logs": logs, "errors": errors}

        logs.append(
            f"[Market Data] Success - Price: {data.get('current_price')}, "
            f"Market Cap: {data.get('market_cap')}, P/E: {data.get('pe_ratio')}"
        )

        return {**state, "market_data": data, "agent_logs": logs, "errors": errors}

    except Exception as e:
        errors.append(f"[Market Data] Error: {str(e)}")
        logs.append(f"[Market Data] Failed: {str(e)}")
        return {**state, "market_data": {}, "agent_logs": logs, "errors": errors}