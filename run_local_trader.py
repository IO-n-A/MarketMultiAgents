import yaml
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Load API keys if needed (e.g., FinnHub)
# Ensure the config file exists and is correctly formatted.
# For this run, we will assume offline tools, so no keys are strictly necessary.
# keys = yaml.safe_load(open('/config/master-api-keys.yaml'))

cfg = DEFAULT_CONFIG.copy()
cfg['llm_provider'] = 'openrouter'         # tells TradingAgents to use OpenAI-compatible endpoint
cfg['backend_url'] = 'http://localhost:8000/v1'  # Triton server
cfg['deep_think_llm'] = 'fingpt-mt'        # name from /tensorrt_engines
cfg['quick_think_llm'] = 'fingpt-forecaster'
cfg['online_tools'] = False                # disable internet tools if working offline
# cfg['data_dir'] = '/path/to/your/data'     # set this to your local datasets
# optionally set other keys, e.g., cfg['finnhub_api_key'] = keys['finnhub_token']

ta = TradingAgentsGraph(config=cfg)
_, decision = ta.propagate('AAPL', '2024-05-10')
print(decision)