import logging
from ..config.settings import settings
from ..api_client.client import ThreeCommasAPIClient
from ..services.accounts_service import AccountsService
from ..core.operations.bot_operations import BotOperations

logger = logging.getLogger("add_exchange")

def main():
    try:
        client = ThreeCommasAPIClient(
            api_key=settings.THREECOMMAS_API_KEY,
            api_secret=settings.THREECOMMAS_API_SECRET
        )
        accounts_service = AccountsService(client)
        bot = BotOperations(accounts_service)

        logger.info("Adding exchange account using settings...")
        response = bot.add_exchange_account(
            type=settings.EXCHANGE_TYPE,
            name=settings.EXCHANGE_NAME,
            api_key=settings.THREECOMMAS_API_KEY,
            secret=settings.THREECOMMAS_API_SECRET,
            passphrase=getattr(settings, 'EXCHANGE_PASSPHRASE', None),
            types_to_create=getattr(settings, 'EXCHANGE_TYPES_TO_CREATE', ['spot'])  
        )
        logger.info(f"Exchange account added successfully: {response}")

    except Exception as e:
        logger.error(f"Failed to add exchange account: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
