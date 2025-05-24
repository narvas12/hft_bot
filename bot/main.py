# main.py
import logging
from .config.settings import settings
from .api_client.client import ThreeCommasAPIClient
from .services.accounts_service import AccountsService
from .core.operations.bot_operations import BotOperations

logger = logging.getLogger("main")

def initialize_services():
    """Initialize all required services"""
    client = ThreeCommasAPIClient(
        api_key=settings.THREECOMMAS_API_KEY,
        api_secret=settings.THREECOMMAS_API_SECRET
    )
    accounts_service = AccountsService(client)
    return BotOperations(accounts_service)

def main():
    """Entry point for the application"""
    try:
        bot = initialize_services()

        # Check if we have exchange credentials in settings
        if all(hasattr(settings, attr) for attr in ['EXCHANGE_API_KEY', 'EXCHANGE_SECRET_KEY']):
            logger.info("Adding exchange account using settings...")
            response = bot.add_exchange_account(
                type=getattr(settings, 'EXCHANGE_TYPE'),
                name=getattr(settings, 'EXCHANGE_NAME'),  
                api_key=settings.EXCHANGE_API_KEY,
                secret=settings.EXCHANGE_SECRET_KEY,
                passphrase=getattr(settings, 'EXCHANGE_PASSPHRASE', None),
                types_to_create=getattr(settings, 'EXCHANGE_TYPES_TO_CREATE', ['spot'])  
            )
            logger.info(f"Exchange account added successfully: {response}")
        else:
            logger.warning("Exchange credentials not found in settings. Skipping account addition.")

        logger.info("Starting strategy loop...")
        bot.run_strategy()

    except Exception as e:
        logger.error(f"Application failed: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()