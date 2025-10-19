# TradingAgents/graph/__init__.py
# Make re-exports resilient to missing optional dependencies during lightweight test runs.

try:
    from .conditional_logic import ConditionalLogic
except Exception:
    class ConditionalLogic:  # minimal stub
        pass

try:
    from .trading_graph import TradingAgentsGraph
except Exception:
    class TradingAgentsGraph:  # stub that raises when used
        def __init__(self, *args, **kwargs):
            raise ImportError("TradingAgentsGraph requires optional dependencies (LangChain/LLMs).")

try:
    from .setup import GraphSetup
except Exception:
    class GraphSetup:
        def __init__(self, *args, **kwargs):
            raise ImportError("GraphSetup requires optional dependencies (LangChain/LLMs).")

try:
    from .propagation import Propagator
except Exception:
    class Propagator:
        def __init__(self, *args, **kwargs):
            raise ImportError("Propagator requires optional dependencies.")

try:
    from .reflection import Reflector
except Exception:
    class Reflector:
        def __init__(self, *args, **kwargs):
            raise ImportError("Reflector requires optional dependencies.")

try:
    from .signal_processing import SignalProcessor
except Exception:
    class SignalProcessor:
        def __init__(self, *args, **kwargs):
            raise ImportError("SignalProcessor requires optional dependencies.")

__all__ = [
    "TradingAgentsGraph",
    "ConditionalLogic",
    "GraphSetup",
    "Propagator",
    "Reflector",
    "SignalProcessor",
]
