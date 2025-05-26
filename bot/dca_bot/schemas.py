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
    base_order_volume: float
    base_order_volume_type: str
    take_profit_type: str
    take_profit: Optional[float]
    take_profit_steps: List[TakeProfitStep]
    safety_order_volume: float
    safety_order_volume_type: str
    safety_order_step_percentage: float
    max_safety_orders: int
    active_safety_orders_count: int
    martingale_volume_coefficient: float
    martingale_step_coefficient: float
    close_deals_timeout: Optional[int] = 0
