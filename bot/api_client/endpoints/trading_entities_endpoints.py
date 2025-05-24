# trading_entities_endpoints.py

BASE_URL = "/ver1/accounts"

def get_active_trading_entities(account_id: int) -> str:
    return f"{BASE_URL}/{account_id}/active_trading_entities"
