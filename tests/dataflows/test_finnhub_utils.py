from tradingagents.dataflows.finnhub_utils import get_data_in_range

def test_missing_dir_returns_empty(tmp_path):
    missing = tmp_path / "does_not_exist"
    res = get_data_in_range("AAPL", "2024-01-01", "2024-01-31", "news_data", str(missing))
    assert res == {}
