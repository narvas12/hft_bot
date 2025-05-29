from typing import List, Optional
from pydantic import BaseModel

class TakeProfitStep(BaseModel):
    amount_percentage: float
    profit_percentage: float

class Strategy(BaseModel):
    strategy: str
    options: Optional[dict] = {}

class CreateDCABotPayload(BaseModel):
    account_id: int
    name: str
    pairs: str
    strategy_list: List[Strategy]
    base_order_volume: str                      # string as per 3Commas example
    # base_order_volume_type removed (not in example)
    take_profit_type: str
    take_profit: Optional[float] = None
    take_profit_steps: Optional[List[TakeProfitStep]] = []
    safety_order_volume: str                    # string as per 3Commas example
    # safety_order_volume_type removed (not in example)
    safety_order_step_percentage: str           # string as per example "1.0"
    max_safety_orders: int
    active_safety_orders_count: int
    martingale_volume_coefficient: str          # string as per example "2"
    martingale_step_coefficient: str            # string as per example "4.0"
    close_deals_timeout: Optional[int] = 0
