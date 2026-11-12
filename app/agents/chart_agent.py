"""FinSight AI - Chart Generator Agent"""

from app.models.schemas import AgentState
from app.tools.chart_generator import (
    generate_price_chart, generate_comparison_chart, generate_volume_chart,
)


def chart_agent(state: AgentState) -> AgentState:
    """Generate charts from collected market data."""
    ticker = state["ticker"]
    market_data = state.get("market_data", {})
    competitor_data = state.get("competitor_data", {})
    logs = state.get("agent_logs", [])
    errors = state.get("errors", [])
    chart_paths = []

    logs.append(f"[Chart Generator] Creating visualizations for {ticker}...")

    try:
        price_history = market_data.get("price_history")
        if price_history:
            path = generate_price_chart(ticker, price_history)
            if path:
                chart_paths.append(path)
                logs.append(f"[Chart Generator] Created price chart")

            vol_path = generate_volume_chart(ticker, price_history)
            if vol_path:
                chart_paths.append(vol_path)
                logs.append(f"[Chart Generator] Created volume chart")

        comp_data = competitor_data.get("data", [])
        if comp_data and market_data:
            comp_path = generate_comparison_chart(ticker, market_data, comp_data)
            if comp_path:
                chart_paths.append(comp_path)
                logs.append(f"[Chart Generator] Created comparison chart")

        logs.append(f"[Chart Generator] Generated {len(chart_paths)} charts total")

        return {**state, "chart_paths": chart_paths, "agent_logs": logs, "errors": errors}

    except Exception as e:
        errors.append(f"[Chart Generator] Error: {str(e)}")
        logs.append(f"[Chart Generator] Failed: {str(e)}")
        return {**state, "chart_paths": chart_paths, "agent_logs": logs, "errors": errors}