"""FinSight AI - News Sentiment Agent (ReAct Pattern)"""

from langchain_core.messages import HumanMessage
from app.models.schemas import AgentState
from app.tools.news_search import search_company_news, format_news_for_prompt
from app.prompts.templates import SENTIMENT_PROMPT
from app.config import get_llm


def news_sentiment_agent(state: AgentState) -> AgentState:
    """Search news and analyze sentiment for the company."""
    company = state["company"]
    logs = state.get("agent_logs", [])
    errors = state.get("errors", [])

    logs.append(f"[News Sentiment] Searching recent news for {company}...")

    try:
        articles = search_company_news(company)
        news_text = format_news_for_prompt(articles)

        if news_text == "No recent news articles found.":
            logs.append("[News Sentiment] No news articles found")
            return {
                **state,
                "news_sentiment": {
                    "overall": "Neutral", "confidence": "Low",
                    "summary": "No recent news articles found for analysis.",
                    "articles_found": 0,
                },
                "agent_logs": logs, "errors": errors,
            }

        logs.append(f"[News Sentiment] Found {len(articles)} articles, analyzing sentiment...")

        llm = get_llm()
        prompt = SENTIMENT_PROMPT.format(company=company, news_articles=news_text)
        response = llm.invoke([HumanMessage(content=prompt)])
        text = response.content.strip()

        sentiment_data = {"raw_analysis": text, "articles_found": len(articles), "articles": articles[:5]}

        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("OVERALL_SENTIMENT:"):
                sentiment_data["overall"] = line.split(":", 1)[1].strip()
            elif line.startswith("CONFIDENCE:"):
                sentiment_data["confidence"] = line.split(":", 1)[1].strip()
            elif line.startswith("SUMMARY:"):
                sentiment_data["summary"] = line.split(":", 1)[1].strip()

        logs.append(
            f"[News Sentiment] Sentiment: {sentiment_data.get('overall', 'N/A')} "
            f"(Confidence: {sentiment_data.get('confidence', 'N/A')})"
        )

        return {**state, "news_sentiment": sentiment_data, "agent_logs": logs, "errors": errors}

    except Exception as e:
        errors.append(f"[News Sentiment] Error: {str(e)}")
        logs.append(f"[News Sentiment] Failed: {str(e)}")
        return {
            **state,
            "news_sentiment": {"overall": "N/A", "summary": f"Error: {str(e)}"},
            "agent_logs": logs, "errors": errors,
        }