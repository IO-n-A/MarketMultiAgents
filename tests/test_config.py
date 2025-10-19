from tradingagents.dataflows.config import set_config, get_config, initialize_config

def test_set_config_overrides_data_dir(tmp_path, monkeypatch):
    # reset any prior state in case of reused interpreter
    initialize_config()
    set_config({"data_dir": str(tmp_path)})
    cfg = get_config()
    assert cfg["data_dir"] == str(tmp_path)
