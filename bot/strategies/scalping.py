def rsi_ema_scalping_strategy() -> dict:
    return {
        "strategy": "nonstop",
        "options": {
            "rsi_period": 14,
            "ema_period": 50,
            "rsi_buy_threshold": 30,
            "rsi_sell_threshold": 70,
            "stop_loss_pct": 0.02,
            "take_profit_pct": 0.04,
        }
    }
