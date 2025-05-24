# core/operations/bot_operations.py
import time
from typing import Optional, List
from ...utils.logger import get_logger
from ...services.accounts_service import AccountsService
from ...strategies.dummy import DummyStrategy
from ...config.settings import settings

logger = get_logger("BotOperations")

class BotOperations:
    def __init__(self, accounts_service: AccountsService):
        """Initialize the BotOperations with required services"""
        self.accounts_service = accounts_service
        self.strategy = DummyStrategy()

    def add_exchange_account(
        self,
        type: str,
        name: str,
        api_key: str,
        secret: str,
        passphrase: Optional[str] = None,
        address: Optional[str] = None,
        customer_id: Optional[str] = None,
        types_to_create: Optional[List[str]] = None,
        use_settings: bool = False
    ):
        """
        Add a new exchange account with comprehensive parameter handling
        
        Args:
            type: Market code from Supported Market List (e.g., "binance")
            name: Name for the exchange account
            api_key: API key from the exchange (ignored if use_settings=True)
            secret: Secret key from the exchange (ignored if use_settings=True)
            passphrase: Required for some exchanges like OKX
            address: Wallet address (for certain exchanges)
            customer_id: Unique ID for Bitstamp exchange
            types_to_create: Array of account types to create (e.g., ["binance_margin"])
            use_settings: If True, uses credentials from settings.py instead of parameters
        
        Returns:
            dict: Response from the API with account details
        """
        try:
            if use_settings:
                # Use credentials from settings
                payload = {
                    "type": type,
                    "name": name,
                    "api_key": settings.EXCHANGE_API_KEY,
                    "secret": settings.EXCHANGE_SECRET_KEY,
                }
                if hasattr(settings, 'EXCHANGE_PASSPHRASE'):
                    payload["passphrase"] = settings.EXCHANGE_PASSPHRASE
            else:
                # Use passed parameters
                payload = {
                    "type": type,
                    "name": name,
                    "api_key": api_key,
                    "secret": secret,
                }
                if passphrase:
                    payload["passphrase"] = passphrase

            # Add optional parameters that aren't credential-related
            if address:
                payload["address"] = address
            if customer_id:
                payload["customer_id"] = customer_id
            if types_to_create:
                payload["types_to_create"] = types_to_create

            logger.info(f"Attempting to add exchange account: {name} ({type})")
            response = self.accounts_service.add_exchange_account(**payload)
            
            logger.info("Exchange account added successfully")
            logger.debug(f"Account details: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to add exchange account: {e}")
            raise

    def get_balance_data(
        self, 
        account_id: int, 
        date_from: str = "2023-01-01", 
        date_to: str = "2023-12-31"
    ):
        """
        Get balance data for a specific account
        
        Args:
            account_id: ID of the account to query
            date_from: Start date for data (YYYY-MM-DD)
            date_to: End date for data (YYYY-MM-DD)
            
        Returns:
            dict: Balance chart data
        """
        try:
            balance_data = self.accounts_service.get_account_balance_chart_data(
                account_id=account_id,
                date_from=date_from,
                date_to=date_to
            )
            logger.info(f"Balance data retrieved for account {account_id}")
            return balance_data
        except Exception as e:
            logger.error(f"Error fetching balance data: {e}")
            raise

    def run_strategy(self):
        """Main trading strategy loop"""
        logger.info("Starting trading strategy")
        while True:
            try:
                signal = self.strategy.generate_signal()
                logger.info(f"Generated signal: {signal}")
                # Here you would add your trade execution logic
                # execute_trade(signal)
                time.sleep(settings.POLL_INTERVAL)
            except KeyboardInterrupt:
                logger.info("Strategy stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in strategy loop: {e}")
                time.sleep(settings.ERROR_RETRY_DELAY)