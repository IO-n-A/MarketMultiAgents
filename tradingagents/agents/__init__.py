try:
    from .utils.agent_utils import Toolkit, create_msg_delete
except Exception:
    class Toolkit:  # lightweight stub for environments without optional deps
        def __init__(self, *args, **kwargs):
            pass
    def create_msg_delete():
        def delete_messages(state):
            return {"messages": []}
        return delete_messages
try:
    from .utils.agent_states import AgentState, InvestDebateState, RiskDebateState
except Exception:
    class AgentState(dict):  # minimal stub
        pass
    class InvestDebateState(dict):
        pass
    class RiskDebateState(dict):
        pass
try:
    from .utils.memory import FinancialSituationMemory
except Exception:
    class FinancialSituationMemory:
        def __init__(self, *args, **kwargs):
            pass

def _stub_not_available(name):
    def _stub(*args, **kwargs):
        raise ImportError(f"{name} is unavailable because optional dependencies are not installed.")
    return _stub

# Analysts (optional; provide stubs if missing)
try:
    from .analysts.fundamentals_analyst import create_fundamentals_analyst
except Exception:
    create_fundamentals_analyst = _stub_not_available("create_fundamentals_analyst")

try:
    from .analysts.market_analyst import create_market_analyst
except Exception:
    create_market_analyst = _stub_not_available("create_market_analyst")

try:
    from .analysts.news_analyst import create_news_analyst
except Exception:
    create_news_analyst = _stub_not_available("create_news_analyst")

try:
    from .analysts.social_media_analyst import create_social_media_analyst
except Exception:
    create_social_media_analyst = _stub_not_available("create_social_media_analyst")

# Momentum analyst and tool (tool works without LangChain via safe decorator fallback)
from .momentum_transformer.momentum_analyst import create_momentum_analyst, get_momentum_analysis

# Researchers (optional)
try:
    from .researchers.bear_researcher import create_bear_researcher
except Exception:
    create_bear_researcher = _stub_not_available("create_bear_researcher")

try:
    from .researchers.bull_researcher import create_bull_researcher
except Exception:
    create_bull_researcher = _stub_not_available("create_bull_researcher")

# Risk management (optional)
try:
    from .risk_mgmt.aggresive_debator import create_risky_debator
except Exception:
    create_risky_debator = _stub_not_available("create_risky_debator")

try:
    from .risk_mgmt.conservative_debator import create_safe_debator
except Exception:
    create_safe_debator = _stub_not_available("create_safe_debator")

try:
    from .risk_mgmt.neutral_debator import create_neutral_debator
except Exception:
    create_neutral_debator = _stub_not_available("create_neutral_debator")

# Managers (optional)
try:
    from .managers.research_manager import create_research_manager
except Exception:
    create_research_manager = _stub_not_available("create_research_manager")

try:
    from .managers.risk_manager import create_risk_manager
except Exception:
    create_risk_manager = _stub_not_available("create_risk_manager")

# Trader (optional)
try:
    from .trader.trader import create_trader
except Exception:
    create_trader = _stub_not_available("create_trader")

__all__ = [
    "FinancialSituationMemory",
    "Toolkit",
    "AgentState",
    "create_msg_delete",
    "InvestDebateState",
    "RiskDebateState",
    "create_bear_researcher",
    "create_bull_researcher",
    "create_research_manager",
    "create_fundamentals_analyst",
    "create_market_analyst",
    "create_neutral_debator",
    "create_news_analyst",
    "create_risky_debator",
    "create_risk_manager",
    "create_safe_debator",
    "create_social_media_analyst",
    "create_trader",
    "create_momentum_analyst",
    "get_momentum_analysis",
]
