# add_exchange.py

from bot.api_client.client import ThreeCommasAPIClient
from bot.services.accounts_service import AccountsService
import os

API_KEY = os.environ.get("THREECOMMAS_API_KEY")
API_SECRET = os.environ.get("THREECOMMAS_API_SECRET")


def add_exchange_account_example():
    client = ThreeCommasAPIClient(api_key=API_KEY, api_secret=API_SECRET)
    accounts_service = AccountsService(client)

    response = accounts_service.add_exchange_account(
        type="binance",
        name="My Binance Account",
        api_key="binance_api_key_here",
        secret="binance_secret_here",
        address="optional_wallet_address",
        types_to_create=["binance_margin"]
    )

    return response
