from pydantic import BaseModel, Field
from typing import List, Optional

class CreateDCABotPayload(BaseModel):
    name: str
    account_id: int
    pairs: List[str]
    base_order_volume: float
    take_profit: float
    safety_order_volume: float
    martingale_volume_coefficient: float
    martingale_step_coefficient: float
    max_safety_orders: int
    active_safety_orders_count: int
    safety_order_step_percentage: float
    take_profit_type: str = Field(default="total")
    strategy: str = Field(default="long")  # or "short"
    cooldown: int = Field(default=0)
    trailing_enabled: bool = Field(default=False)
    trailing_deviation: Optional[float] = None
    stop_loss_percentage: Optional[float] = None
    stop_loss_timeout_enabled: Optional[bool] = False
    stop_loss_timeout: Optional[int] = 0
    disable_after_deals_count: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "ETH USDT DCA Bot",
                "account_id": 123456,
                "pairs": ["BINANCE:ETH_USDT"],
                "base_order_volume": 10,
                "take_profit": 1.5,
                "safety_order_volume": 20,
                "martingale_volume_coefficient": 1.2,
                "martingale_step_coefficient": 1.1,
                "max_safety_orders": 5,
                "active_safety_orders_count": 2,
                "safety_order_step_percentage": 1.0,
                "take_profit_type": "total",
                "strategy": "long",
                "cooldown": 1800
            }
        }
