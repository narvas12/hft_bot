import os
from ..api_client.client import ThreeCommasAPIClient
from ..services.dca_service import DCABotService
from ..models.schemas import CreateDCABotPayload
from ..config.settings import settings
from ..strategies.scalping import rsi_ema_scalping_strategy


THREECOMMAS_API_KEY=os.environ.get("THREECOMMAS_API_KEY")
THREECOMMAS_API_SECRET=os.environ.get("THREECOMMAS_API_SECRET") 

api_client = ThreeCommasAPIClient(
    settings.THREECOMMAS_API_KEY,
    settings.THREECOMMAS_API_SECRET
)

bot_service = DCABotService(api_client)

bot_payload = CreateDCABotPayload(
    name="BTC-USDT DCA Bot",
    account_id=2036669,
    pairs=["BINANCE:BTC_USDT"],
    base_order_volume=50,
    take_profit=1.5,
    safety_order_volume=50,
    martingale_volume_coefficient=1.05,
    martingale_step_coefficient=1.02,
    max_safety_orders=5,
    active_safety_orders_count=2,
    safety_order_step_percentage=1.0,
    strategy_list=[rsi_ema_scalping_strategy()],
    cooldown=1800
)

response = bot_service.create_bot(bot_payload)
print(response)
