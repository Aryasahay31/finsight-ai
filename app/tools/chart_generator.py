"""FinSight AI - Chart Generation Tool"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

CHARTS_DIR = "./charts"
os.makedirs(CHARTS_DIR, exist_ok=True)


def generate_price_chart(ticker: str, price_history: dict) -> str:
    """Generate a 6-month stock price chart."""
    if not price_history or not price_history.get("dates"):
        return ""

    dates = [datetime.strptime(d, "%Y-%m-%d") for d in price_history["dates"]]
    prices = price_history["close"]

    fig, ax = plt.subplots(figsize=(10, 5))
    color = "#2196F3" if prices[-1] >= prices[0] else "#F44336"
    ax.plot(dates, prices, color=color, linewidth=2)
    ax.fill_between(dates, prices, alpha=0.1, color=color)

    ax.set_title(f"{ticker} - 6 Month Price History", fontsize=14, fontweight="bold")
    ax.set_ylabel("Price", fontsize=11)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    ax.grid(True, alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    change = ((prices[-1] - prices[0]) / prices[0]) * 100
    sign = "+" if change > 0 else ""
    ax.annotate(f"{sign}{change:.1f}%", xy=(dates[-1], prices[-1]),
                fontsize=12, fontweight="bold", color=color)

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, f"{ticker}_price.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_comparison_chart(main_ticker: str, main_data: dict, competitors: list[dict]) -> str:
    """Generate a bar chart comparing P/E ratios across companies."""
    companies = [main_data.get("name", main_ticker)[:15]]
    pe_values = [main_data.get("pe_ratio", 0) if main_data.get("pe_ratio") != "N/A" else 0]

    for comp in competitors:
        if "error" not in comp:
            companies.append(comp.get("name", comp["ticker"])[:15])
            pe_values.append(comp.get("pe_ratio", 0) if comp.get("pe_ratio") != "N/A" else 0)

    if len(companies) < 2:
        return ""

    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#2196F3"] + ["#90CAF9"] * (len(companies) - 1)
    bars = ax.bar(companies, pe_values, color=colors, edgecolor="white", linewidth=1.5)

    for bar, val in zip(bars, pe_values):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                    f"{val:.1f}", ha="center", fontsize=10, fontweight="bold")

    ax.set_title("P/E Ratio Comparison", fontsize=14, fontweight="bold")
    ax.set_ylabel("P/E Ratio", fontsize=11)
    ax.grid(True, axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=30, ha="right")

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, f"{main_ticker}_comparison.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_volume_chart(ticker: str, price_history: dict) -> str:
    """Generate a trading volume chart."""
    if not price_history or not price_history.get("dates"):
        return ""

    dates = [datetime.strptime(d, "%Y-%m-%d") for d in price_history["dates"]]
    volumes = price_history["volume"]

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.bar(dates, volumes, color="#7E57C2", alpha=0.7, width=1.5)

    ax.set_title(f"{ticker} - Trading Volume", fontsize=14, fontweight="bold")
    ax.set_ylabel("Volume", fontsize=11)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    ax.grid(True, axis="y", alpha=0.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    path = os.path.join(CHARTS_DIR, f"{ticker}_volume.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path