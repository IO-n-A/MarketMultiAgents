from typing import Annotated, Dict, Any, Optional
try:
    from langchain_core.prompts import ChatPromptTemplate
except Exception:
    ChatPromptTemplate = None  # type: ignore

try:
    from langchain_core.tools import tool
except Exception:
    def tool(x=None, *args, **kwargs):  # type: ignore
        if callable(x):
            return x
        def deco(f):
            return f
        return deco
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure local momentumtransformers (copied under this folder) is importable as top-level "mom_trans"
LOCAL_MT_ROOT = os.path.join(os.path.dirname(__file__), "momentumtransformers")
if os.path.isdir(LOCAL_MT_ROOT) and LOCAL_MT_ROOT not in sys.path:
    sys.path.insert(0, LOCAL_MT_ROOT)

# Safely import momentumtransformers components
try:
    from mom_trans.data_prep import deep_momentum_strategy_features
    from mom_trans.model_inputs import ModelFeatures
    try:
        from mom_trans.momentum_transformer import TftDeepMomentumNetworkModel  # optional for future model loading
    except Exception:
        TftDeepMomentumNetworkModel = None
except Exception as _e:
    deep_momentum_strategy_features = None
    ModelFeatures = None
    TftDeepMomentumNetworkModel = None

# Use interface directly to obtain structured OHLCV data
try:
    import tradingagents.dataflows.interface as interface
except Exception:
    class _InterfaceStub:
        def get_YFin_data(self, *args, **kwargs):
            raise ImportError(
                "tradingagents.dataflows.interface is unavailable; optional dependencies not installed"
            )
    interface = _InterfaceStub()


def _prepare_price_df(raw) -> pd.DataFrame:
    """Normalize interface.get_YFin_data output into a DataFrame with:
       - DatetimeIndex
       - 'close' column (float)
    """
    if isinstance(raw, str):
        raise ValueError(f"Data retrieval returned text instead of a DataFrame: {raw}")

    if not isinstance(raw, pd.DataFrame):
        raise ValueError("Unsupported data format; expected a pandas DataFrame.")

    df = raw.copy()

    # Normalize date/time
    date_col = None
    for cand in ["date", "Date", "timestamp", "Timestamp", "Datetime", "datetime"]:
        if cand in df.columns:
            date_col = cand
            break

    if date_col is not None:
        df["__dt"] = pd.to_datetime(df[date_col], errors="coerce", utc=False)
        df = df.dropna(subset=["__dt"])
        df = df.set_index("__dt")
    elif not isinstance(df.index, pd.DatetimeIndex):
        # Try to coerce existing index
        try:
            df.index = pd.to_datetime(df.index, errors="coerce")
            df = df.dropna(subset=[col for col in df.columns if col is not None])
        except Exception:
            raise ValueError("No usable datetime column/index found in price data.")

    # Normalize close column
    lower_map = {c.lower(): c for c in df.columns}
    close_src = lower_map.get("close") or lower_map.get("adj close") or lower_map.get("adj_close") or lower_map.get("adjclose")
    if close_src is None:
        # Attempt common alternatives
        for alias in ["closing price", "close_price", "c"]:
            if alias in lower_map:
                close_src = lower_map[alias]
                break

    if close_src is None:
        raise ValueError(f"Could not find a close/adj close column in data. Available columns: {list(df.columns)}")

    out = pd.DataFrame({"close": pd.to_numeric(df[close_src], errors="coerce")}, index=df.index)
    out = out.dropna()
    # Ensure strictly increasing time order
    out = out.sort_index()
    return out


class MomentumPredictor:
    """Wrapper class for momentum transformer predictions (with robust fallback)."""

    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_features = None
        self.is_trained = False

        # Optional: load a pre-trained TFT model if provided and available
        if model_path and os.path.exists(model_path) and TftDeepMomentumNetworkModel is not None:
            self.load_model(model_path)

    def load_model(self, model_path: str):
        """Load pre-trained TFT momentum model."""
        try:
            if TftDeepMomentumNetworkModel is None:
                raise RuntimeError("TftDeepMomentumNetworkModel is unavailable (TensorFlow/Keras not imported).")
            # Placeholder for real loading code if implemented in the upstream module
            # self.model = TftDeepMomentumNetworkModel.load_model(model_path)
            # For now, mark as not loaded to avoid runtime errors without full model artifacts
            self.is_trained = False
        except Exception as e:
            print(f"[MomentumPredictor] Failed to load momentum model: {e}")
            self.is_trained = False

    def predict_momentum(self, ticker: str, price_df: pd.DataFrame) -> Dict[str, Any]:
        """Generate momentum predictions for a ticker from normalized OHLCV price_df."""
        try:
            if deep_momentum_strategy_features is None:
                # Fallback without feature pipeline
                return self._fallback_from_price(ticker, price_df)

            # Prepare engineered features
            features_df = deep_momentum_strategy_features(price_df)
            features_df["ticker"] = ticker

            # If a trained model is available, wire it here. For now, fallback to technical signal.
            if not self.is_trained or self.model is None or ModelFeatures is None:
                return self._analyze_technical_features(features_df)

            # Example sketch for when a trained model is available:
            # mf = ModelFeatures(
            #     features_df,
            #     total_time_steps=252,
            #     train_valid_ratio=1.0,
            #     changepoint_lbws=None,
            #     split_tickers_individually=False,
            # )
            # preds = self.model.predict(mf.test_fixed)  # model API subject to upstream implementation
            # return self._convert_preds_to_signal(features_df, preds)

            return self._analyze_technical_features(features_df)
        except Exception as e:
            return {
                "momentum_signal": "ERROR",
                "confidence": 0.0,
                "technical_analysis": f"Prediction error: {e}",
                "sharpe_prediction": 0.0,
                "position_size": 0.0,
            }

    def _fallback_from_price(self, ticker: str, price_df: pd.DataFrame) -> Dict[str, Any]:
        """Simple momentum proxy using returns when full feature pipeline is unavailable."""
        if price_df is None or price_df.empty:
            return {
                "momentum_signal": "NO_DATA",
                "confidence": 0.0,
                "technical_analysis": "Insufficient data for analysis",
                "sharpe_prediction": 0.0,
                "position_size": 0.0,
            }

        closes = price_df["close"]
        daily_ret = closes.pct_change().dropna()
        # Simple normalized windows
        m21 = daily_ret.rolling(21).mean().iloc[-1] if len(daily_ret) >= 21 else 0.0
        m63 = daily_ret.rolling(63).mean().iloc[-1] if len(daily_ret) >= 21 else 0.0
        vol = daily_ret.rolling(21).std().iloc[-1] if len(daily_ret) >= 21 else daily_ret.std()
        vol = float(vol) if pd.notna(vol) and vol > 1e-12 else 1e-12

        short_momentum = float(m21 / vol)
        long_momentum = float(m63 / max(vol, 1e-12))

        momentum_score = 0.6 * short_momentum + 0.4 * long_momentum
        signal, confidence = self._score_to_signal(momentum_score)

        analysis = f"""Momentum Fallback Analysis:
- Short-term normalized momentum (21d): {short_momentum:.3f}
- Long-term normalized momentum (63d): {long_momentum:.3f}
- Composite momentum score: {momentum_score:.3f}
- Volatility proxy (21d std): {vol:.4f}

Recommendation: {signal} with {confidence:.1%} confidence (fallback)
"""
        return {
            "momentum_signal": signal,
            "confidence": confidence,
            "technical_analysis": analysis.strip(),
            "sharpe_prediction": momentum_score,
            "position_size": max(-0.2, min(0.2, momentum_score * 0.1)),  # capped sizing
        }

    def _analyze_technical_features(self, features_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze momentum using engineered features."""
        if features_df is None or len(features_df) == 0:
            return {
                "momentum_signal": "NO_DATA",
                "confidence": 0.0,
                "technical_analysis": "Insufficient data for analysis",
                "sharpe_prediction": 0.0,
                "position_size": 0.0,
            }

        latest = features_df.iloc[-1]

        short_momentum = float(latest.get("norm_monthly_return", 0.0))
        long_momentum = float(latest.get("norm_quarterly_return", 0.0))

        macd_short = float(latest.get("macd_8_24", 0.0))
        macd_long = float(latest.get("macd_32_96", 0.0))

        momentum_score = (short_momentum * 0.4 + long_momentum * 0.3 + macd_short * 0.2 + macd_long * 0.1)
        signal, confidence = self._score_to_signal(momentum_score)

        analysis = f"""Momentum Technical Analysis:
- Short-term momentum (monthly): {short_momentum:.3f}
- Long-term momentum (quarterly): {long_momentum:.3f}
- MACD signals: Short={macd_short:.3f}, Long={macd_long:.3f}
- Composite momentum score: {momentum_score:.3f}
- Daily volatility (proxy): {float(latest.get('daily_vol', 0.0)):.3f}

Recommendation: {signal} with {confidence:.1%} confidence
"""

        return {
            "momentum_signal": signal,
            "confidence": confidence,
            "technical_analysis": analysis.strip(),
            "sharpe_prediction": momentum_score,
            "position_size": max(-0.2, min(0.2, momentum_score * 0.1)),  # cap sizing
        }

    @staticmethod
    def _score_to_signal(score: float):
        if score > 0.5:
            return "STRONG_BUY", min(0.9, abs(score))
        if score > 0.1:
            return "BUY", min(0.7, abs(score))
        if score < -0.5:
            return "STRONG_SELL", min(0.9, abs(score))
        if score < -0.1:
            return "SELL", min(0.7, abs(score))
        return "NEUTRAL", 0.5


# Reusable predictor instance
_momentum_predictor = MomentumPredictor()


@tool
def get_momentum_analysis(
    ticker: Annotated[str, "Stock ticker symbol (e.g., AAPL, TSLA)"],
    start_date: Annotated[str, "Start date in YYYY-MM-DD format"],
    end_date: Annotated[str, "End date in YYYY-MM-DD format"],
) -> str:
    """
    Momentum Transformer Analysis Tool:
    - Fetches OHLCV data via the project's dataflow interface
    - Prepares features using the momentumtransformers pipeline
    - Produces signal, confidence, analysis text, and suggested sizing
    """
    try:
        raw = interface.get_YFin_data(ticker, start_date, end_date)
        price_df = _prepare_price_df(raw)
        analysis = _momentum_predictor.predict_momentum(ticker, price_df)

        result = f"""
MOMENTUM TRANSFORMER ANALYSIS FOR {ticker}
==========================================

Signal: {analysis['momentum_signal']}
Confidence: {analysis['confidence']:.1%}

{analysis['technical_analysis']}

Expected Sharpe Proxy: {analysis['sharpe_prediction']:.3f}
Recommended Position Size: {analysis['position_size']:.2%}

Note: Analysis uses the momentumtransformers feature pipeline. Model inference falls back to technical factors if a trained TFT is unavailable.
""".strip()
        try:
            out = Path("docs/agent_output_momentum.txt")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(result, encoding="utf-8")
        except Exception:
            pass
        return result
    except Exception as e:
        return f"Momentum analysis failed for {ticker}: {str(e)}"


def create_momentum_analyst(llm, toolkit):
    """Factory: Momentum Technical Analyst agent following existing patterns."""
    if ChatPromptTemplate is None:
        raise ImportError(
            "LangChain Core is required to create the momentum analyst agent. "
            "Install with: pip install langchain-core"
        )
    system_prompt = """You are a Momentum Technical Analyst specializing in quantitative momentum strategies using advanced machine learning models.

Your expertise includes:
- Temporal Fusion Transformer (TFT) models for momentum prediction
- Technical indicator analysis (MACD, normalized returns)
- Sharpe ratio optimization for risk-adjusted returns
- Changepoint detection for regime identification
- Quantitative position sizing based on momentum signals

Your role is to:
1. Analyze price momentum using sophisticated ML models
2. Provide technical analysis with confidence levels
3. Generate position recommendations based on momentum signals
4. Explain the quantitative reasoning behind your analysis
5. Integrate your momentum insights with other analysts' findings

Always provide:
- Clear momentum signal (BUY/SELL/NEUTRAL with strength indicators)
- Confidence level based on model predictions
- Technical analysis explaining the momentum factors
- Risk assessment and position sizing recommendations
- Model-based insights that complement fundamental and sentiment analysis
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{messages}"),
    ])

    # Bind the momentum analysis tool
    agent = prompt | llm.bind_tools([get_momentum_analysis])
    return agent