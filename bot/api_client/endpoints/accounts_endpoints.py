# accounts_endpoints.py

BASE_URL = "/ver1/accounts"

def get_account_active_trading_entities(account_id: int) -> tuple[str, dict]:
    """Returns endpoint and parameters for active trading entities"""
    endpoint = f"{BASE_URL}/{account_id}/active_trading_entities"
    params = {"account_id": account_id}
    return endpoint, params

def get_account_balance_chart_data(account_id: int, date_from: str = None, date_to: str = None) -> tuple[str, dict]:
    """Returns endpoint and parameters for balance chart data"""
    endpoint = f"{BASE_URL}/{account_id}/balance_chart_data"
    params = {"account_id": account_id}
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    return endpoint, params

def get_account_balance_chart_data_summary(date_from: str = None, date_to: str = None) -> tuple[str, dict]:
    """Returns endpoint and parameters for balance chart summary"""
    endpoint = f"{BASE_URL}/summary/balance_chart_data"
    params = {}
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    return endpoint, params

def post_load_balances(account_id: int) -> tuple[str, dict]:
    """Returns endpoint and parameters for loading balances"""
    endpoint = f"{BASE_URL}/{account_id}/load_balances"
    params = {"account_id": account_id}
    return endpoint, params

def get_account_types_to_connect() -> tuple[str, dict]:
    """Returns endpoint for account types to connect"""
    endpoint = f"{BASE_URL}/types_to_connect"
    return endpoint, {}

def post_add_exchange_account(type: str, name: str, api_key: str, secret: str, **kwargs) -> tuple[str, dict]:
    """Returns endpoint and payload for adding exchange account"""
    endpoint = f"{BASE_URL}/new"
    payload = {
        "type": type,
        "name": name,
        "api_key": api_key,
        "secret": secret,
    }
    payload.update(kwargs)
    return endpoint, payload