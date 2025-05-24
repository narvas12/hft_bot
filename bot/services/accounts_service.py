# services/accounts_service.py
from typing import List, Optional, Dict, Any
from ..api_client.client import ThreeCommasAPIClient, APIError, AuthenticationError, RateLimitError
from ..api_client.endpoints import accounts_endpoints as endpoints
from ..utils.logger import get_logger

logger = get_logger("AccountsService")

class AccountServiceError(Exception):
    """Base class for account service exceptions"""
    pass

class AccountNotFoundError(AccountServiceError):
    """Account not found exception"""
    pass

class InvalidAccountParametersError(AccountServiceError):
    """Invalid account parameters exception"""
    pass

class AccountsService:
    def __init__(self, client: ThreeCommasAPIClient):
        if not isinstance(client, ThreeCommasAPIClient):
            raise ValueError("client must be a ThreeCommasAPIClient instance")
        self.client = client

    def _handle_api_call(self, callable, *args, **kwargs) -> Any:
        """Wrapper for handling API calls with consistent error handling"""
        try:
            return callable(*args, **kwargs)
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise AccountServiceError("Invalid API credentials") from e
        except RateLimitError as e:
            logger.error("API rate limit exceeded")
            raise AccountServiceError("Too many requests, please try again later") from e
        except APIError as e:
            logger.error(f"API request failed: {str(e)}")
            if "not found" in str(e).lower():
                raise AccountNotFoundError("Account not found") from e
            raise AccountServiceError(f"API operation failed: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise AccountServiceError("Service operation failed") from e

    def get_account_active_trading_entities(self, account_id: int) -> Dict:
        """Get active trading entities for an account"""
        if not isinstance(account_id, int) or account_id <= 0:
            raise InvalidAccountParametersError("Invalid account ID")

        endpoint, params = endpoints.get_account_active_trading_entities(account_id)
        return self._handle_api_call(self.client.get, endpoint, params=params)

    def get_account_balance_chart_data(
        self,
        account_id: int,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Dict:
        """Get balance chart data for an account"""
        if not isinstance(account_id, int) or account_id <= 0:
            raise InvalidAccountParametersError("Invalid account ID")

        endpoint, params = endpoints.get_account_balance_chart_data(
            account_id, date_from, date_to
        )
        return self._handle_api_call(self.client.get, endpoint, params=params)

    def get_account_balance_chart_data_summary(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Dict:
        """Get balance chart data summary"""
        endpoint, params = endpoints.get_account_balance_chart_data_summary(date_from, date_to)
        return self._handle_api_call(self.client.get, endpoint, params=params)

    def post_load_balances(self, account_id: int) -> Dict:
        """Load balances for an account"""
        if not isinstance(account_id, int) or account_id <= 0:
            raise InvalidAccountParametersError("Invalid account ID")

        endpoint, params = endpoints.post_load_balances(account_id)
        return self._handle_api_call(self.client.post, endpoint, params=params)

    def get_account_types_to_connect(self) -> Dict:
        """Get available account types to connect"""
        endpoint, params = endpoints.get_account_types_to_connect()
        return self._handle_api_call(self.client.get, endpoint, params=params)

    def add_exchange_account(
        self,
        type: str,
        name: str,
        api_key: str,
        secret: str,
        passphrase: Optional[str] = None,
        address: Optional[str] = None,
        customer_id: Optional[str] = None,
        types_to_create: Optional[List[str]] = None
    ) -> Dict:
        """
        Add a new exchange account with comprehensive error handling
        
        Args:
            type: Market code from Supported Market List
            name: Name for the exchange account
            api_key: API key from the exchange
            secret: Secret key from the exchange
            passphrase: Required for some exchanges like OKX
            address: Wallet address (for certain exchanges)
            customer_id: Unique ID for Bitstamp exchange
            types_to_create: Array of account types to create
            
        Returns:
            dict: Response from the API
            
        Raises:
            InvalidAccountParametersError: If required parameters are missing or invalid
            AccountServiceError: For other service-related errors
        """
        if not all([type, name, api_key, secret]):
            raise InvalidAccountParametersError("Missing required parameters")

        try:
            endpoint, payload = endpoints.post_add_exchange_account(
                type=type,
                name=name,
                api_key=api_key,
                secret=secret,
                passphrase=passphrase,
                address=address,
                customer_id=customer_id,
                types_to_create=types_to_create
            )
            return self._handle_api_call(self.client.post, endpoint, params=payload)
        except ValueError as e:
            raise InvalidAccountParametersError(f"Invalid parameter: {str(e)}") from e