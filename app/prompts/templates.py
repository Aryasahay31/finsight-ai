"""FinSight AI - Agent Prompt Templates"""

PLANNER_PROMPT = """You are a financial research planner. Given a company name, identify:
1. The stock ticker symbol (e.g., AAPL for Apple, RELIANCE.NS for Reliance Industries)
2. A list of 3-4 competitor companies in the same sector

Respond in this EXACT format (no extra text):
TICKER: <ticker_symbol>
COMPETITORS: <company1>|<company2>|<company3>

Company to analyze: {company}"""


SENTIMENT_PROMPT = """You are a financial news sentiment analyst. Analyze the following news 
headlines/snippets about {company} and provide a sentiment analysis.

News articles:
{news_articles}

Respond in this EXACT format:
OVERALL_SENTIMENT: <Bullish/Bearish/Neutral>
CONFIDENCE: <High/Medium/Low>
KEY_THEMES:
- <theme 1>
- <theme 2>
- <theme 3>
SUMMARY: <2-3 sentence summary of news sentiment>"""


COMPETITOR_PROMPT = """You are a financial comparison analyst. Compare the following companies 
based on the market data provided.

Main company: {company} ({ticker})
Main company data: {main_data}

Competitors data:
{competitor_data}

Provide a brief competitive analysis covering:
1. How {company} compares on key metrics (P/E, Market Cap, Revenue)
2. Strengths relative to competitors
3. Weaknesses relative to competitors
Keep it concise - 4-5 sentences max."""


REPORT_PROMPT = """You are a senior financial analyst at a research firm. Write a professional 
investment research report for {company} ({ticker}).

Use the following data to write the report:

## Market Data
{market_data}

## News Sentiment Analysis
{sentiment_analysis}

## Competitive Analysis
{competitor_analysis}

Write a structured report with these sections:
1. **Executive Summary** (2-3 sentences)
2. **Company Overview** (current price, market cap, key metrics)
3. **Financial Highlights** (revenue, margins, P/E analysis)
4. **News & Sentiment** (what the market is saying)
5. **Competitive Position** (vs peers)
6. **Risk Factors** (2-3 key risks)
7. **Outlook** (Bullish/Bearish/Neutral with reasoning)

IMPORTANT: Only use the data provided above. Do not make up numbers. 
Add a disclaimer that this is AI-generated and not financial advice."""


EVALUATOR_PROMPT = """You are a quality evaluator for financial research reports. 
Rate the following report on these dimensions (1-5 scale):

Report:
{report}

Rate each dimension and give a brief reason:
1. ACCURACY (Are claims supported by the data provided?)
2. COMPLETENESS (Does it cover all key areas?)
3. CLARITY (Is it well-written and easy to understand?)
4. USEFULNESS (Would an investor find this helpful?)

Respond in this EXACT format:
ACCURACY: <score>/5 - <one line reason>
COMPLETENESS: <score>/5 - <one line reason>
CLARITY: <score>/5 - <one line reason>
USEFULNESS: <score>/5 - <one line reason>
OVERALL: <average_score>/5
FEEDBACK: <one sentence on what could be improved>"""