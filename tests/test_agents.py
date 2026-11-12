"""FinSight AI - Tests"""

import pytest
from app.tools.stock_data import _format_large_number
from app.tools.news_search import format_news_for_prompt


class TestStockData:
    def test_format_trillion(self):
        assert _format_large_number(2.5e12) == "2.50T"

    def test_format_billion(self):
        assert _format_large_number(150e9) == "150.00B"

    def test_format_million(self):
        assert _format_large_number(50e6) == "50.00M"

    def test_format_none(self):
        assert _format_large_number(None) == "N/A"


class TestNewsSearch:
    def test_format_empty(self):
        assert format_news_for_prompt([]) == "No recent news articles found."

    def test_format_error(self):
        assert format_news_for_prompt([{"error": "err"}]) == "No recent news articles found."

    def test_format_valid(self):
        articles = [{"title": "Test", "body": "Body", "source": "Src", "date": "", "url": ""}]
        assert "Test" in format_news_for_prompt(articles)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])