def execute_trade(signal: str) -> None:
    if signal == "buy":
        print("[3Commas] Executing BUY order...")
    elif signal == "sell":
        print("[3Commas] Executing SELL order...")
    else:
        print("[3Commas] No action taken.")
