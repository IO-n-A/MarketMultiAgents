import pytest
import pandas as pd
import numpy as np

import tradingagents.agents.momentum_transformer.momentum_analyst as momentum_module
from tradingagents.graph.conditional_logic import ConditionalLogic


def _make_price_df_with_date_and_adj_close(days: int = 130) -> pd.DataFrame:
    """Deterministic OHLCV-like DataFrame with Date column and Adj Close values."""
    idx = pd.date_range(start="2024-01-01", periods=days, freq="B")
    # Deterministic drift from -0.1% to +0.2% across the period
    returns = np.linspace(-0.001, 0.002, days)
    prices = 100.0 * np.cumprod(1.0 + returns)
    df = pd.DataFrame({"Date": idx, "Adj Close": prices})
    return df


def _make_price_df_with_index_and_uppercase(days: int = 60) -> pd.DataFrame:
    """DataFrame with DatetimeIndex and CLOSE column in uppercase."""
    idx = pd.date_range(start="2024-03-01", periods=days, freq="B")
    prices = 50.0 + np.linspace(0.0, 5.0, days)
    df = pd.DataFrame({"CLOSE": prices}, index=idx)
    return df


def test_agents_exports_tool():
    # Ensure the momentum tool is exported via the agents package
    from tradingagents.agents import get_momentum_analysis as exported_tool

    assert callable(exported_tool), "get_momentum_analysis should be exported and callable"


def test_prepare_price_df_handles_various_columns():
    # Case 1: Date + Adj Close columns
    raw1 = _make_price_df_with_date_and_adj_close(90)
    out1 = momentum_module._prepare_price_df(raw1)
    assert isinstance(out1.index, pd.DatetimeIndex)
    assert "close" in out1.columns
    assert out1.index.is_monotonic_increasing

    # Case 2: DatetimeIndex + uppercase CLOSE column
    raw2 = _make_price_df_with_index_and_uppercase(60)
    out2 = momentum_module._prepare_price_df(raw2)
    assert isinstance(out2.index, pd.DatetimeIndex)
    assert "close" in out2.columns
    assert out2.index.is_monotonic_increasing

    # Case 3: Missing any close-like column -> should raise
    bad = pd.DataFrame({"open": np.linspace(100, 120, 10)}, index=pd.date_range("2024-01-01", periods=10, freq="B"))
    with pytest.raises(ValueError):
        momentum_module._prepare_price_df(bad)


def test_get_momentum_analysis_fallback_path(monkeypatch):
    # Patch data retrieval to return deterministic prices
    monkeypatch.setattr(
        momentum_module.interface,
        "get_YFin_data",
        lambda ticker, s, e: _make_price_df_with_date_and_adj_close(130),
        raising=True,
    )
    # Force fallback by disabling feature pipeline
    monkeypatch.setattr(momentum_module, "deep_momentum_strategy_features", None, raising=False)

    result = momentum_module.get_momentum_analysis.invoke(
        {"ticker": "TEST", "start_date": "2024-01-01", "end_date": "2024-06-30"}
    )

    assert "MOMENTUM TRANSFORMER ANALYSIS FOR TEST" in result
    assert "Expected Sharpe Proxy:" in result
    assert "Recommended Position Size:" in result
    # Fallback analysis text includes "(fallback)" marker
    assert "(fallback)" in result


def test_get_momentum_analysis_with_engineered_features(monkeypatch):
    # Provide deterministic price data
    monkeypatch.setattr(
        momentum_module.interface,
        "get_YFin_data",
        lambda ticker, s, e: _make_price_df_with_date_and_adj_close(50),
        raising=True,
    )

    # Stub feature engineering to produce strong positive momentum at the last row
    def fake_features(price_df: pd.DataFrame) -> pd.DataFrame:
        n = len(price_df)
        df = pd.DataFrame(index=price_df.index.copy())
        df["norm_monthly_return"] = np.zeros(n)
        df["norm_quarterly_return"] = np.zeros(n)
        df["macd_8_24"] = np.zeros(n)
        df["macd_32_96"] = np.zeros(n)
        df["daily_vol"] = 0.05
        # last row with strong positive momentum and MACD
        df.iloc[-1] = [1.0, 1.0, 1.0, 1.0, 0.05]
        return df

    monkeypatch.setattr(momentum_module, "deep_momentum_strategy_features", fake_features, raising=False)
    # Ensure we remain on the engineered-features path (no trained model required)
    monkeypatch.setattr(momentum_module._momentum_predictor, "is_trained", False, raising=True)

    result = momentum_module.get_momentum_analysis.invoke(
        {"ticker": "TEST", "start_date": "2024-01-01", "end_date": "2024-03-31"}
    )

    assert "Momentum Technical Analysis:" in result
    assert "(fallback)" not in result
    # Expect a BUY-type signal given strongly positive features
    assert "Signal:" in result and "BUY" in result


def test_conditional_logic_should_continue_momentum():
    class DummyMsg:
        def __init__(self, tool_calls):
            self.tool_calls = tool_calls

    logic = ConditionalLogic()

    state_tools = {"messages": [DummyMsg([{"name": "get_momentum_analysis"}])]}
    state_clear = {"messages": [DummyMsg([])]}

    assert logic.should_continue_momentum(state_tools) == "tools_momentum"
    assert logic.should_continue_momentum(state_clear) == "Msg Clear Momentum"