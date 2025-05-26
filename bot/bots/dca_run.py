from bot.api_client.client import ThreeCommasAPIClient
from bot.models.schemas import CreateDCABotPayload, StrategyOption
from ..services.dca_service import DCABotService


def main():
    import os
    from pydantic import ValidationError


    api_key = os.getenv("THREE_COMMAS_API_KEY")
    api_secret = os.getenv("THREE_COMMAS_API_SECRET")

    if not api_key or not api_secret:
        print("Please set THREE_COMMAS_API_KEY and THREE_COMMAS_API_SECRET environment variables.")
        return


    api_client = ThreeCommasAPIClient(api_key=api_key, api_secret=api_secret)
    dca_service = DCABotService(api_client)


    try:
        payload = CreateDCABotPayload(
            name="ETH USDT DCA Bot",
            account_id=2036669,
            pairs=["BINANCE:ETH_USDT"],
            base_order_volume=10,
            take_profit=1.5,
            safety_order_volume=20,
            martingale_volume_coefficient=1.2,
            martingale_step_coefficient=1.1,
            max_safety_orders=5,
            active_safety_orders_count=2,
            safety_order_step_percentage=1.0,
            take_profit_type="total",
            strategy_list=[
                StrategyOption(
                    strategy="nonstop",
                    options={
                        "rsi_period": 14,
                        "ema_period": 50,
                        "rsi_buy_threshold": 30,
                        "rsi_sell_threshold": 70,
                        "stop_loss_pct": 0.02,
                        "take_profit_pct": 0.04
                    }
                )
            ],
            cooldown=1800,
            trailing_enabled=False
        )
    except ValidationError as e:
        print(f"Payload validation error: {e}")
        return

    # Create the bot
    try:
        response = dca_service.create_bot(payload)
        print("Bot created successfully:")
        print(response)
    except Exception as e:
        print(f"Error creating bot: {e}")


if __name__ == "__main__":
    main()
