"""FinSight AI - Competitor Analysis Agent"""

from langchain_core.messages import HumanMessage
from app.models.schemas import AgentState
from app.tools.stock_data import get_competitor_data
from app.prompts.templates import COMPETITOR_PROMPT
from app.config import get_llm


def competitor_agent(state: AgentState) -> AgentState:
    """Analyze competitors and compare with the target company."""
    company = state["company"]
    ticker = state["ticker"]
    main_data = state.get("market_data", {})
    comp_info = state.get("competitor_data", {})
    comp_tickers = comp_info.get("tickers", [])
    logs = state.get("agent_logs", [])
    errors = state.get("errors", [])

    if not comp_tickers:
        logs.append("[Competitor] No competitor tickers found, skipping")
        return {
            **state,
            "competitor_data": {"tickers": [], "data": [], "analysis": "No competitors identified."},
            "agent_logs": logs, "errors": errors,
        }

    logs.append(f"[Competitor] Fetching data for: {', '.join(comp_tickers)}...")

    try:
        comp_data = get_competitor_data(comp_tickers)
        valid_comps = [c for c in comp_data if "error" not in c]

        if not valid_comps:
            logs.append("[Competitor] Could not fetch any competitor data")
            return {
                **state,
                "competitor_data": {"tickers": comp_tickers, "data": [], "analysis": "Could not fetch competitor data."},
                "agent_logs": logs, "errors": errors,
            }

        logs.append(f"[Competitor] Got data for {len(valid_comps)} competitors, analyzing...")

        comp_formatted = ""
        for c in valid_comps:
            comp_formatted += (
                f"\n{c['name']} ({c['ticker']}): "
                f"Price={c['current_price']}, Market Cap={c['market_cap']}, "
                f"P/E={c['pe_ratio']}, Revenue={c['revenue']}, "
                f"Profit Margin={c['profit_margin']}"
            )

        main_formatted = (
            f"Price={main_data.get('current_price', 'N/A')}, "
            f"Market Cap={main_data.get('market_cap', 'N/A')}, "
            f"P/E={main_data.get('pe_ratio', 'N/A')}, "
            f"Revenue={main_data.get('revenue', 'N/A')}, "
            f"Profit Margin={main_data.get('profit_margin', 'N/A')}"
        )

        llm = get_llm()
        prompt = COMPETITOR_PROMPT.format(
            company=company, ticker=ticker,
            main_data=main_formatted, competitor_data=comp_formatted,
        )
        response = llm.invoke([HumanMessage(content=prompt)])

        logs.append("[Competitor] Analysis complete")

        return {
            **state,
            "competitor_data": {"tickers": comp_tickers, "data": comp_data, "analysis": response.content.strip()},
            "agent_logs": logs, "errors": errors,
        }

    except Exception as e:
        errors.append(f"[Competitor] Error: {str(e)}")
        logs.append(f"[Competitor] Failed: {str(e)}")
        return {
            **state,
            "competitor_data": {**comp_info, "analysis": f"Error: {str(e)}"},
            "agent_logs": logs, "errors": errors,
        }