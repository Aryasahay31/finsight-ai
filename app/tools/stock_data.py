"""FinSight AI - Stock Data Tool (yfinance)"""

import yfinance as yf
from datetime import datetime, timedelta


def get_stock_data(ticker: str) -> dict:
    """Fetch comprehensive stock data for a given ticker symbol."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        history = stock.history(start=start_date, end=end_date)

        data = {
            "ticker": ticker,
            "name": info.get("longName", info.get("shortName", ticker)),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "current_price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "currency": info.get("currency", "USD"),
            "market_cap": _format_large_number(info.get("marketCap")),
            "market_cap_raw": info.get("marketCap", 0),
            "pe_ratio": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else "N/A",
            "forward_pe": round(info.get("forwardPE", 0), 2) if info.get("forwardPE") else "N/A",
            "eps": info.get("trailingEps", "N/A"),
            "dividend_yield": f"{round(info.get('dividendYield', 0) * 100, 2)}%" if info.get("dividendYield") else "N/A",
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            "50_day_avg": round(info.get("fiftyDayAverage", 0), 2) if info.get("fiftyDayAverage") else "N/A",
            "200_day_avg": round(info.get("twoHundredDayAverage", 0), 2) if info.get("twoHundredDayAverage") else "N/A",
            "revenue": _format_large_number(info.get("totalRevenue")),
            "profit_margin": f"{round(info.get('profitMargins', 0) * 100, 2)}%" if info.get("profitMargins") else "N/A",
            "operating_margin": f"{round(info.get('operatingMargins', 0) * 100, 2)}%" if info.get("operatingMargins") else "N/A",
            "return_on_equity": f"{round(info.get('returnOnEquity', 0) * 100, 2)}%" if info.get("returnOnEquity") else "N/A",
            "debt_to_equity": round(info.get("debtToEquity", 0), 2) if info.get("debtToEquity") else "N/A",
            "beta": round(info.get("beta", 0), 2) if info.get("beta") else "N/A",
            "analyst_target": info.get("targetMeanPrice", "N/A"),
            "recommendation": info.get("recommendationKey", "N/A"),
        }

        if not history.empty:
            data["price_history"] = {
                "dates": [d.strftime("%Y-%m-%d") for d in history.index],
                "close": [round(p, 2) for p in history["Close"].tolist()],
                "volume": history["Volume"].tolist(),
            }
            first_price = history["Close"].iloc[0]
            last_price = history["Close"].iloc[-1]
            data["6m_change"] = f"{round(((last_price - first_price) / first_price) * 100, 2)}%"
        else:
            data["price_history"] = None
            data["6m_change"] = "N/A"

        return data

    except Exception as e:
        return {"error": str(e), "ticker": ticker}


def get_competitor_data(tickers: list[str]) -> list[dict]:
    """Fetch basic data for competitor companies."""
    results = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            results.append({
                "ticker": ticker,
                "name": info.get("longName", info.get("shortName", ticker)),
                "current_price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
                "market_cap": _format_large_number(info.get("marketCap")),
                "pe_ratio": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else "N/A",
                "revenue": _format_large_number(info.get("totalRevenue")),
                "profit_margin": f"{round(info.get('profitMargins', 0) * 100, 2)}%" if info.get("profitMargins") else "N/A",
                "recommendation": info.get("recommendationKey", "N/A"),
            })
        except Exception as e:
            results.append({"ticker": ticker, "error": str(e)})
    return results


def _format_large_number(num) -> str:
    if num is None:
        return "N/A"
    if num >= 1e12:
        return f"{num / 1e12:.2f}T"
    if num >= 1e9:
        return f"{num / 1e9:.2f}B"
    if num >= 1e6:
        return f"{num / 1e6:.2f}M"
    return str(num)