# balance_endpoints.py

BASE_URL = "/ver1/accounts"

def get_balance_chart_data(account_id: int, date_from: str, date_to: str = None) -> str:
    url = f"{BASE_URL}/{account_id}/balance_chart_data?date_from={date_from}"
    if date_to:
        url += f"&date_to={date_to}"
    return url

def get_balance_chart_data_summary(date_from: str, date_to: str = None) -> str:
    url = f"{BASE_URL}/summary/balance_chart_data?date_from={date_from}"
    if date_to:
        url += f"&date_to={date_to}"
    return url
