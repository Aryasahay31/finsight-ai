"""FinSight AI - News Search Tool (DuckDuckGo - free, no API key)"""

from duckduckgo_search import DDGS


def search_company_news(company: str, max_results: int = 8) -> list[dict]:
    """Search for recent news about a company."""
    try:
        with DDGS() as ddgs:
            query = f"{company} stock market news financial"
            results = list(ddgs.news(query, max_results=max_results))

            articles = []
            for r in results:
                articles.append({
                    "title": r.get("title", ""),
                    "body": r.get("body", ""),
                    "source": r.get("source", ""),
                    "date": r.get("date", ""),
                    "url": r.get("url", ""),
                })
            return articles

    except Exception as e:
        return [{"error": str(e)}]


def format_news_for_prompt(articles: list[dict]) -> str:
    """Format news articles into a string for the LLM prompt."""
    if not articles or (len(articles) == 1 and "error" in articles[0]):
        return "No recent news articles found."

    formatted = []
    for i, article in enumerate(articles, 1):
        if "error" in article:
            continue
        formatted.append(
            f"{i}. [{article['source']}] {article['title']}\n"
            f"   {article['body'][:200]}..."
        )

    return "\n\n".join(formatted) if formatted else "No recent news articles found."