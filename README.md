# MarketAgents

A comprehensive, production-ready multi-agent framework for financial trading using Large Language Models (LLMs), integrating specialized agents for sentiment analysis, technical analysis, fundamental analysis, and trading decision-making. The system provides:

- **Multi-Agent Architecture**: Specialized agents (sentiment, technical, fundamental, trading) collaborating in a coordinated workflow


- **LLM Integration**: Support for multiple LLM providers (OpenAI, OpenRouter, Anthropic, Google, Ollama) with configurable reasoning modes
- **Data Integration**: Unified data fetching from financial APIs, news sources, and market data providers
- **Momentum Transformers**: Advanced momentum-based trading strategies with transformer architectures
- **Production Features**: Comprehensive logging, configuration management, and evaluation frameworks
- **Open Data**: Uses publicly available financial data sources with no proprietary dependencies

The framework implements state-of-the-art multi-agent systems for financial decision-making, combining the reasoning capabilities of LLMs with traditional quantitative trading approaches.

# Contents
- [Key Features](#key-features)
- [Architecture Overview](#architecture-overview)
- [File Structure](#file-structure)
- [Setup and Configuration](#setup-and-configuration)
- [Usage Workflows](#usage-workflows)
- [Enhanced Features](#enhanced-features)
- [Data Sources and Attribution](#data-sources-and-attribution)
- [Evaluation Methodology](#evaluation-methodology)
- [Troubleshooting](#troubleshooting)
- [License](#license)

# Key Features

## Multi-Agent LLM Architecture
- **Specialized Agents**: Sentiment Analyst, Technical Analyst, Fundamental Analyst, and Trading Agent with distinct roles

### Attribution #1

```bib
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```


- **Collaborative Workflow**: Agents communicate and share insights through structured message passing
- **LLM Reasoning Modes**: Deep-thinking and quick-thinking LLM configurations for different analysis phases
- **Provider Flexibility**: Support for OpenAI, OpenRouter, Anthropic, Google Gemini, and Ollama

- **Technical Indicators**: Comprehensive technical analysis with RSI, MACD, moving averages, and custom indicators

- **Sentiment Analysis**: Multi-source sentiment aggregation from social media and news

- **Risk Management**: Integrated risk assessment and position sizing algorithms

- **Momentum Transformers**: Deep learning-based momentum strategies using transformer architectures.

### Attribution #2

```bib
@article{wood2021trading,
  title={Trading with the Momentum Transformer: An Intelligent and Interpretable Architecture},
  author={Wood, Kieran and Giegerich, Sven and Roberts, Stephen and Zohren, Stefan},
  journal={arXiv preprint arXiv:2112.08534},
  year={2021}
}

@article {Wood111,
	author = {Wood, Kieran and Roberts, Stephen and Zohren, Stefan},
	title = {Slow Momentum with Fast Reversion: A Trading Strategy Using Deep Learning and Changepoint Detection},
	volume = {4},
	number = {1},
	pages = {111--129},
	year = {2022},
	doi = {10.3905/jfds.2021.1.081},
	publisher = {Institutional Investor Journals Umbrella},
	issn = {2640-3943},
	URL = {https://jfds.pm-research.com/content/4/1/111},
	eprint = {https://jfds.pm-research.com/content/4/1/111.full.pdf},
	journal = {The Journal of Financial Data Science}
}
```


### Configuration Management System
- **YAML Configuration**: Central configuration via `config/` directory with validation
- **API Key Management**: Secure key resolution from environment variables or config files
- **Model Parameters**: Configurable LLM parameters, trading thresholds, and risk settings
- **Data Source Configuration**: Region-specific source mappings and validation rules

### Data Integration and Validation
- **Multi-Source Data Fetching**: Financial data from Yahoo Finance, Alpha Vantage, and other APIs
- **News and Sentiment Sources**: Integration with news APIs and social media sentiment
- **Data Validation**: SHA-256 fingerprinting, uniqueness assertions, and provenance tracking
- **Quality Assurance**: Automated data integrity checks and temporal alignment validation

### Production-Ready Infrastructure
- **Comprehensive Logging**: Structured logging protocol with archiving and audit trails
- **Backtesting Framework**: Automated multi-fold cross-validation with statistical aggregation
- **Diagnostic Reports**: Systematic analysis reports with artifact generation
- **Batch Processing**: Multi-asset workflows with consolidated reporting

## Architecture Overview

The system implements a modern multi-agent architecture centered around specialized LLM-powered agents that collaborate in financial decision-making processes.

The framework consists of:
- **TradingAgents Core**: Multi-agent orchestration system with LLM integration
- **MomentumTransformers**: Deep learning momentum strategies
- **Data Pipeline**: Unified data fetching and preprocessing
- **Evaluation System**: Backtesting and performance analysis
- **Configuration Management**: YAML-based settings and API key handling

```
├── tradingagents/           # Main multi-agent framework
│   ├── graph/               # Agent orchestration and communication
│   ├── dataflows/           # Data processing pipelines
│   ├── interface/           # External API integrations
│   └── config/              # Configuration management
│
├── momentumtransformers/    # Deep momentum strategies
│   ├── mom_trans/           # Transformer implementation
│   ├── data/                # Training data (gitignored)
│   └── examples/            # Usage examples
│
├── cli/                     # Command-line interface
├── config/                  # Configuration files
├── docs/                    # Documentation and logs
├── eval_results/            # Evaluation results
├── results/                 # Generated results
├── tests/                   # Comprehensive test suite
├── .gitignore               # Git ignore patterns
├── .python-version          # Python version specification
├── .pytest_cache/           # Pytest cache
├── LICENSE                  # MIT license
├── main.py                  # Main CLI entry point
├── pyproject.toml           # Project configuration
├── requirements.txt         # Runtime dependencies
├── run_local_trader.py      # Local trading execution script
└── uv.lock                  # Dependency lock file
```

## File Structure

```
TradingAgents/
├── README.md                     # Comprehensive documentation
├── LICENSE                       # MIT license
├── pyproject.toml                # Project configuration and tooling
├── requirements.txt              # Runtime dependencies
├── uv.lock                       # Dependency lock file
├── main.py                       # Main CLI entry point
├── run_local_trader.py           # Local trading execution script
│
├── tradingagents/                # Core multi-agent framework
│   ├── __init__.py
│   ├── graph/                    # Agent graph and orchestration
│   │   ├── trading_graph.py      # Main trading workflow
│   │   └── nodes/                # Individual agent nodes
│   ├── dataflows/                # Data processing
│   │   ├── config.py             # Configuration utilities
│   │   ├── interface.py          # External integrations
│   │   └── tools/                # Trading tools
│   └── default_config.py         # Default settings
│
├── momentumtransformers/         # Momentum transformer module
│   ├── mom_trans/                # Core transformer code
│   │   ├── momentum_transformer.py
│   │   ├── backtest.py
│   │   └── data.py
│   ├── paper.md                  # Research paper
│   ├── paper_v1.md               # Previous version
│   ├── run_backtest.ipynb        # Backtesting notebook
│   └── Graphs and stats.ipynb    # Analysis notebook
│
├── cli/                          # Command-line utilities
│   ├── main.py                   # CLI entry point
│   └── utils.py                  # CLI utilities
│
├── config/                       # Configuration files
│   ├── master_API_keys.yaml      # API keys (gitignored)
│   └── (other config files)
│
├── docs/                         # Documentation
│   ├── implementation.md         # Implementation guide
│   ├── prompts.md                # System prompts
│   ├── ToDo.md                   # Development tasks
│   └── ARCHIVE/                  # Archived documentation
│
├── tests/                        # Test suite
│   ├── agents/                   # Agent-specific tests
│   ├── test_config.py            # Configuration tests
│   └── conftest.py               # Test fixtures
│
├── data/                         # (gitignored) Input datasets
├── results/                      # (gitignored) Generated results
└── assets/                       # Static assets
```

## Setup and Configuration

### Requirements
- Python 3.10+
- API keys for LLM providers (OpenAI, OpenRouter, etc.)
- Financial data API keys (optional, for enhanced data sources)

### Installation

```bash
# Clone repository
git clone https://github.com/TradingAgents-AI/TradingAgents.git
cd TradingAgents

# Optional virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install runtime dependencies
pip install -r requirements.txt

# Install development tools (optional)
pip install -r requirements-dev.txt
pre-commit install
```

### Configuration Setup

The system uses YAML configuration files for reproducible workflows:

```bash
# Configuration files are in config/ directory
ls config/
# master_API_keys.yaml          # API key management (gitignored)
# (other configuration files as needed)
```

### API Key Setup (Required)

Configure API keys for LLM providers:

```bash
# Option 1: Environment variables (recommended)
export OPENAI_API_KEY="your_openai_api_key_here"
export OPENROUTER_API_KEY="your_openrouter_api_key_here"
# Add other provider keys as needed

# Option 2: Configuration file
cp config/master_API_keys.yaml.example config/master_API_keys.yaml
# Edit config/master_API_keys.yaml with your API keys
```

## Usage Workflows

All commands shown from repository root. The system uses comprehensive logging and headless operation.

### Basic Trading Analysis

```bash
# Run multi-agent trading analysis for AAPL
python main.py \
  --ticker AAPL \
  --analysis-mode full \
  --llm-provider openai \
  --log-level INFO
```

### Local Trading Execution

```bash
# Execute local trading with momentum strategies
python run_local_trader.py \
  --tickers "AAPL,MSFT,GOOGL" \
  --strategy momentum \
  --risk-management enabled \
  --log-level INFO
```

### CLI-Based Analysis

```bash
# Interactive CLI for trading analysis
python -m cli.main \
  --ticker NVDA \
  --research-depth comprehensive \
  --llm-engine gpt-4o-mini \
  --output-dir results/NVDA
```

### Momentum Transformer Backtesting

```bash
# Run momentum transformer backtest
cd momentumtransformers
python -m mom_trans.backtest \
  --start-date 2017-01-01 \
  --end-date 2024-01-01 \
  --tickers "AAPL,MSFT,GOOGL" \
  --output-dir ../results/momentum_backtest
```

### Advanced Multi-Agent Workflow

```bash
# Full multi-agent analysis with all components
python main.py \
  --ticker TSLA \
  --use-all-agents \
  --sentiment-analysis \
  --technical-analysis \
  --fundamental-analysis \
  --risk-assessment \
  --llm-provider openrouter \
  --deep-think-llm gpt-4o \
  --quick-think-llm gpt-4o-mini \
  --output-dir results/TSLA_full
```

## Enhanced Features

### 🆕 Multi-Agent Collaboration
- **Agent Specialization**: Each agent focuses on specific aspects of trading analysis
- **Message Passing**: Structured communication between agents for coordinated decision-making
- **Consensus Building**: Multi-agent consensus algorithms for trading signals
- **Error Handling**: Robust error recovery and agent fallback mechanisms

### 🆕 Advanced LLM Integration
- **Provider Agnostic**: Unified interface for multiple LLM providers
- **Reasoning Modes**: Separate deep-thinking and quick-thinking LLM configurations
- **Prompt Engineering**: Optimized prompts for financial analysis and trading
- **Context Management**: Efficient context window utilization for long-term analysis

### 🆕 Momentum Transformer Strategies
- **Deep Momentum**: Neural network-based momentum detection using transformers
- **Multi-Scale Analysis**: Analysis across different time horizons
- **Feature Engineering**: Automated feature extraction from price and volume data
- **Backtesting Framework**: Comprehensive evaluation of momentum strategies

### 🆕 Comprehensive Data Sources

**Financial Market Data:**
- Yahoo Finance API for historical price data
- Alpha Vantage for real-time and historical data
- Financial Modeling Prep for fundamental data

**News and Sentiment:**
- NewsAPI for financial news aggregation
- Social media sentiment from Twitter/X API
- Reddit sentiment analysis via PRAW

**Economic Indicators:**
- FRED (Federal Reserve Economic Data) for macroeconomic data
- OECD and World Bank data for global economic indicators

### 🆕 Production Infrastructure
- **Structured Logging**: Comprehensive logging with JSON formatting and archival
- **Configuration Validation**: YAML schema validation for all configuration files
- **Error Recovery**: Automatic retry mechanisms and graceful degradation
- **Performance Monitoring**: Built-in metrics collection and alerting

## Sources

This project exclusively uses open, publicly available data sources:

### Financial Data Providers
- **Yahoo Finance**: Historical price data via yfinance library (Public Domain)
- **Alpha Vantage**: Real-time and historical financial data (Free tier available)
- **Financial Modeling Prep**: Fundamental data and financial statements (API access)

### News and Sentiment Sources
- **NewsAPI**: Global news aggregation (API key required)
- **Twitter/X API**: Social media sentiment data (API key required)
- **Reddit API**: Community sentiment via PRAW library (API key required)

### Economic Data Sources
- **Federal Reserve Economic Data (FRED)**: Macroeconomic indicators (Public Domain)
- **OECD Statistics**: International economic data (Public Domain)
- **World Bank Open Data**: Global development indicators (Public Domain)

### LLM Providers
- **OpenAI**: GPT models for reasoning and analysis
- **OpenRouter**: Unified access to multiple LLM providers
- **Anthropic**: Claude models for advanced reasoning
- **Google Gemini**: Multimodal LLM capabilities
- **Ollama**: Local LLM deployment and inference

All data sources are properly attributed with citations and license compliance. No proprietary or paywalled data sources are used in default workflows.

## Evaluation Methodology

### Performance Metrics
- **Sharpe Ratio**: Risk-adjusted return measurement
- **Maximum Drawdown**: Peak-to-trough decline assessment
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profit divided by gross loss

### Backtesting Framework
- **Walk-Forward Analysis**: Out-of-sample testing with rolling windows
- **Monte Carlo Simulation**: Statistical robustness testing
- **Risk-Adjusted Metrics**: Comprehensive risk evaluation
- **Benchmarking**: Comparison against market indices and strategies

### Agent Performance Evaluation
- **Individual Agent Metrics**: Performance of each specialized agent
- **Collaboration Efficiency**: Multi-agent synergy measurement
- **Decision Quality**: Accuracy of trading signals and predictions
- **Robustness Testing**: Performance under various market conditions

## Troubleshooting

### Common Issues and Solutions

**Configuration Issues:**
```bash
# Verify configuration system
python -c "from tradingagents.dataflows.config import get_config; print('Config system working')"

# Check API key resolution
python -c "from tradingagents.dataflows.config import get_api_key; print(get_api_key('openai') or 'No OpenAI key')"
```

**LLM Provider Issues:**
```bash
# Test LLM connectivity
python -c "from tradingagents.graph.nodes.llm_node import LLMNode; node = LLMNode(); print('LLM node ready')"

# Verify provider configuration
python -c "import os; print('OPENAI_API_KEY' in os.environ)"
```

**Data Fetching Issues:**
```bash
# Test data interfaces
python -c "from tradingagents.dataflows.interface import DataInterface; di = DataInterface(); print('Data interface ready')"

# Verify ticker data availability
python -c "import yfinance as yf; data = yf.download('AAPL', period='1d'); print('Yahoo Finance working')"
```

**Import Errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: Requires Python 3.10+
- Verify virtual environment activation

**API Rate Limiting:**
- Implement request throttling for API calls
- Use caching for frequently accessed data
- Monitor API usage and implement fallback strategies

**Performance Issues:**
- Use appropriate LLM model sizes for your hardware
- Enable caching for repeated analyses
- Configure parallel processing where available

### Getting Help
- Check the comprehensive logging output for diagnostic information
- Review configuration files in `config/` directory for settings
- Examine test files in `tests/` directory for usage examples
- All diagnostic reports are saved for post-analysis

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Data Sources

**Data Providers:**
- Yahoo Finance: Historical financial data
- Alpha Vantage: Financial market data APIs
- Financial Modeling Prep: Fundamental financial data
- NewsAPI: Global news aggregation
- Federal Reserve Economic Data (FRED): Macroeconomic statistics
- OECD: International economic indicators

**LLM Providers:**
- OpenAI: GPT series models
- Anthropic: Claude models
- Google: Gemini models
- OpenRouter: Unified LLM access platform
- Ollama: Local LLM infrastructure

**Research Foundations:**
- Based on academic research in multi-agent systems and financial trading
- Implements methodologies from papers on momentum strategies and LLM applications
- Follows best practices in quantitative finance and machine learning

**Open Source Philosophy:**
This project is committed to open science and reproducible research using only publicly available data sources and transparent methodologies.
