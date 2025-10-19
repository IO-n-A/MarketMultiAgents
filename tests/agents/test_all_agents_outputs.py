import os
from pathlib import Path
import pytest
import pandas as pd
import numpy as np

import tradingagents.agents.momentum_transformer.momentum_analyst as momentum_module

# Helpers
def _make_price_df_with_date_and_adj_close(days: int = 130) -> pd.DataFrame:
    """Deterministic OHLCV-like DataFrame with Date column and Adj Close values."""
    idx = pd.date_range(start="2024-01-01", periods=days, freq="B")
    # Deterministic drift from -0.05% to +0.15% across the period
    returns = np.linspace(-0.0005, 0.0015, days)
    prices = 100.0 * np.cumprod(1.0 + returns)
    df = pd.DataFrame({"Date": idx, "Adj Close": prices})
    return df


def _fake_features_positive(price_df: pd.DataFrame) -> pd.DataFrame:
    """Create engineered features with a positive momentum at the last row."""
    n = len(price_df)
    df = pd.DataFrame(index=price_df.index.copy())
    df["norm_monthly_return"] = np.zeros(n)
    df["norm_quarterly_return"] = np.zeros(n)
    df["macd_8_24"] = np.zeros(n)
    df["macd_32_96"] = np.zeros(n)
    df["daily_vol"] = 0.05
    # Strong momentum on last row
    df.iloc[-1] = [0.6, 0.5, 0.4, 0.3, 0.05]
    return df


def _write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _assert_written(path: Path):
    assert path.exists(), f"{path} should be created"
    assert path.stat().st_size > 0, f"{path} should not be empty"


def test_all_agents_outputs_write_files(monkeypatch):
    """Generate per-agent outputs and write to docs/ for documentation snapshots.

    - Momentum: Use the real get_momentum_analysis tool with deterministic stubs to avoid I/O and networking.
    - Market, Social, News, Fundamentals: Use stubbed text to avoid external dependencies and LLM calls.
    """
    docs_dir = Path("docs")
    ticker = "TEST"
    start_date = "2024-01-01"
    end_date = "2024-06-30"

    # Momentum output via real tool with deterministic stubs
    monkeypatch.setattr(
        momentum_module.interface,
        "get_YFin_data",
        lambda t, s, e: _make_price_df_with_date_and_adj_close(130),
        raising=True,
    )
    monkeypatch.setattr(
        momentum_module,
        "deep_momentum_strategy_features",
        _fake_features_positive,
        raising=False,
    )
    # Ensure engineered-features path (no model inference)
    monkeypatch.setattr(
        momentum_module._momentum_predictor,
        "is_trained",
        False,
        raising=True,
    )

    momentum_text = momentum_module.get_momentum_analysis.invoke(
        {"ticker": ticker, "start_date": start_date, "end_date": end_date}
    )

    # Stubbed outputs for other analysts to keep test deterministic/offline
    outputs = {
        "agent_output_market.txt": (
            f"Market Analyst Report for {ticker} on {end_date}\n\n"
            "This is a stubbed market analysis used for documentation tests.\n"
            "- Highlights: trend overview, key indicators, volatility context.\n"
        ),
        "agent_output_social.txt": (
            f"Social Media Analyst Report for {ticker} on {end_date}\n\n"
            "This is a stubbed social/sentiment analysis used for documentation tests.\n"
            "- Highlights: sentiment shifts, engagement spikes, top themes.\n"
        ),
        "agent_output_news.txt": (
            f"News Analyst Report for {ticker} on {end_date}\n\n"
            "This is a stubbed macro/news analysis used for documentation tests.\n"
            "- Highlights: macro themes, sector catalysts, event risks.\n"
        ),
        "agent_output_fundamentals.txt": (
            f"Fundamentals Analyst Report for {ticker} on {end_date}\n\n"
            "This is a stubbed fundamentals analysis used for documentation tests.\n"
            "- Highlights: valuation context, margin trends, balance sheet notes.\n"
        ),
        "agent_output_momentum.txt": momentum_text,
    }

    # Write files and validate
    for fname, text in outputs.items():
        out_path = docs_dir / fname
        _write(out_path, text)
        _assert_written(out_path)