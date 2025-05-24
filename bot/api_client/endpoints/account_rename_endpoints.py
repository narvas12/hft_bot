# account_rename_endpoints.py

BASE_URL = "/ver1/accounts"

def post_rename_account(account_id: int, new_name: str) -> str:
    # Note: 'name' is a query parameter, typically handled separately in requests.
    return f"{BASE_URL}/{account_id}/rename?name={new_name.replace(' ', '%20')}"

