import json
import os


def get_data_in_range(ticker, start_date, end_date, data_type, data_dir, period=None):
    """
    Gets finnhub data saved and processed on disk.
    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        data_type (str): Type of data from finnhub to fetch. Can be insider_trans, SEC_filings, news_data, insider_senti, or fin_as_reported.
        data_dir (str): Directory where the data is saved.
        period (str): Default to none, if there is a period specified, should be annual or quarterly.
    """
    # Validate data_dir exists
    if not os.path.isdir(data_dir):
        print(
            f"[TradingAgents] Data directory not found: {data_dir}. "
            "Set TRADINGAGENTS_DATA_DIR environment variable or config['data_dir']."
        )
        return {}

    # Build expected data path
    if period:
        data_path = os.path.join(
            data_dir,
            "finnhub_data",
            data_type,
            f"{ticker}_{period}_data_formatted.json",
        )
    else:
        data_path = os.path.join(
            data_dir, "finnhub_data", data_type, f"{ticker}_data_formatted.json"
        )

    # Validate data file exists
    if not os.path.isfile(data_path):
        print(f"[TradingAgents] Finnhub data file not found: {data_path}")
        return {}

    try:
        with open(data_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[TradingAgents] Error reading data file {data_path}: {e}")
        return {}

    # Filter keys (date, str in format YYYY-MM-DD) by the date range (str, str in format YYYY-MM-DD)
    filtered_data = {}
    for key, value in data.items():
        if start_date <= key <= end_date and len(value) > 0:
            filtered_data[key] = value
    return filtered_data
