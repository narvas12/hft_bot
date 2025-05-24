# dcaendpoints.py

BASE_URL = "/ver1/bots"

def create_dca_bot() -> str:
    return f"{BASE_URL}/create_bot"

def update_pairs_blacklist() -> str:
    return f"{BASE_URL}/update_pairs_black_list"

def get_pairs_blacklist() -> str:
    return f"{BASE_URL}/pairs_black_list"

def get_strategy_list() -> str:
    return f"{BASE_URL}/strategy_list"

def list_dca_bots() -> str:
    return f"{BASE_URL}"

def get_dca_bot_stats() -> str:
    return f"{BASE_URL}/stats"

def get_stats_by_date() -> str:
    return f"{BASE_URL}/stats_by_date"

def disable_dca_bot(bot_id: int) -> str:
    return f"{BASE_URL}/{bot_id}/disable"

def enable_dca_bot(bot_id: int) -> str:
    return f"{BASE_URL}/{bot_id}/enable"

def delete_dca_bot(bot_id: int) -> str:
    return f"{BASE_URL}/{bot_id}/delete"

def panic_sell_all_deals(bot_id: int) -> str:
    return f"{BASE_URL}/{bot_id}/panic_sell_all_deals"

def cancel_all_deals(bot_id: int) -> str:
    return f"{BASE_URL}/{bot_id}/cancel_all_deals"

def update_dca_bot(bot_id: int) -> str:
    return f"{BASE_URL}/{bot_id}/update"

def get_dca_bot(bot_id: int) -> str:
    return f"{BASE_URL}/{bot_id}/show"

def get_profit_by_day(bot_id: int) -> str:
    return f"{BASE_URL}/{bot_id}/profit_by_day"

def get_deals_stats(bot_id: int) -> str:
    return f"{BASE_URL}/{bot_id}/deals_stats"
