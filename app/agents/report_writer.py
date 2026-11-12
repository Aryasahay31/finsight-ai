"""FinSight AI - Report Writer Agent"""

from langchain_core.messages import HumanMessage
from app.models.schemas import AgentState
from app.prompts.templates import REPORT_PROMPT
from app.config import get_llm


def report_writer_agent(state: AgentState) -> AgentState:
    """Write a comprehensive financial research report."""
    company = state["company"]
    ticker = state["ticker"]
    market_data = state.get("market_data", {})
    news_sentiment = state.get("news_sentiment", {})
    competitor_data = state.get("competitor_data", {})
    logs = state.get("agent_logs", [])
    errors = state.get("errors", [])

    logs.append(f"[Report Writer] Composing research report for {company}...")

    try:
        market_text = _format_market_data(market_data)
        sentiment_text = _format_sentiment(news_sentiment)
        competitor_text = competitor_data.get("analysis", "No competitor data available.")

        llm = get_llm()
        prompt = REPORT_PROMPT.format(
            company=company, ticker=ticker,
            market_data=market_text, sentiment_analysis=sentiment_text,
            competitor_analysis=competitor_text,
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        report = response.content.strip()

        logs.append(f"[Report Writer] Report completed ({len(report)} characters)")

        return {**state, "report": report, "agent_logs": logs, "errors": errors}

    except Exception as e:
        errors.append(f"[Report Writer] Error: {str(e)}")
        logs.append(f"[Report Writer] Failed: {str(e)}")
        return {**state, "report": f"Error generating report: {str(e)}", "agent_logs": logs, "errors": errors}


def _format_market_data(data: dict) -> str:
    if not data:
        return "No market data available."
    return (
        f"Company: {data.get('name', 'N/A')}\n"
        f"Ticker: {data.get('ticker', 'N/A')}\n"
        f"Sector: {data.get('sector', 'N/A')} | Industry: {data.get('industry', 'N/A')}\n"
        f"Current Price: {data.get('current_price', 'N/A')} {data.get('currency', '')}\n"
        f"Market Cap: {data.get('market_cap', 'N/A')}\n"
        f"P/E Ratio: {data.get('pe_ratio', 'N/A')} | Forward P/E: {data.get('forward_pe', 'N/A')}\n"
        f"EPS: {data.get('eps', 'N/A')}\n"
        f"Dividend Yield: {data.get('dividend_yield', 'N/A')}\n"
        f"52-Week High: {data.get('52_week_high', 'N/A')} | Low: {data.get('52_week_low', 'N/A')}\n"
        f"50-Day Avg: {data.get('50_day_avg', 'N/A')} | 200-Day Avg: {data.get('200_day_avg', 'N/A')}\n"
        f"Revenue: {data.get('revenue', 'N/A')}\n"
        f"Profit Margin: {data.get('profit_margin', 'N/A')}\n"
        f"Operating Margin: {data.get('operating_margin', 'N/A')}\n"
        f"Return on Equity: {data.get('return_on_equity', 'N/A')}\n"
        f"Debt to Equity: {data.get('debt_to_equity', 'N/A')}\n"
        f"Beta: {data.get('beta', 'N/A')}\n"
        f"6-Month Price Change: {data.get('6m_change', 'N/A')}\n"
        f"Analyst Target: {data.get('analyst_target', 'N/A')}\n"
        f"Analyst Recommendation: {data.get('recommendation', 'N/A')}"
    )


def _format_sentiment(data: dict) -> str:
    if not data:
        return "No sentiment data available."
    text = (
        f"Overall Sentiment: {data.get('overall', 'N/A')}\n"
        f"Confidence: {data.get('confidence', 'N/A')}\n"
        f"Summary: {data.get('summary', 'N/A')}\n"
        f"Articles Analyzed: {data.get('articles_found', 0)}"
    )
    if data.get("raw_analysis"):
        text += f"\n\nDetailed Analysis:\n{data['raw_analysis']}"
    return text