from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class TakeProfitStep(BaseModel):
    amount_percentage: float
    profit_percentage: float


class Strategy(BaseModel):
    strategy: str
    options: Optional[Dict[str, Any]] = {}


class CreateDCABotPayload(BaseModel):
    account_id: int
    name: str
    pairs: List[str]
    base_order_volume: str
    base_order_volume_type: Optional[str] = None
    safety_order_volume: str
    safety_order_volume_type: Optional[str] = None
    max_safety_orders: int
    active_safety_orders_count: int
    safety_order_step_percentage: str
    take_profit: Optional[str] = None
    take_profit_type: str
    min_profit_percentage: Optional[str] = None
    min_profit_type: Optional[str] = None
    martingale_volume_coefficient: str
    martingale_step_coefficient: str
    cooldown: Optional[str] = "0"
    close_deals_timeout: Optional[int] = None
    stop_loss_percentage: Optional[str] = None
    stop_loss_type: Optional[str] = "stop_loss"
    trailing_enabled: Optional[bool] = False
    trailing_deviation: Optional[str] = None
    tsl_enabled: Optional[bool] = False
    deal_start_delay_seconds: Optional[int] = None
    stop_loss_timeout_enabled: Optional[bool] = False
    stop_loss_timeout_in_seconds: Optional[int] = 0
    disable_after_deals_count: Optional[int] = None
    deals_counter: Optional[int] = None
    allowed_deals_on_same_pair: Optional[int] = None
    easy_form_supported: Optional[bool] = False
    strategy: Optional[str] = "long"
    max_active_deals: Optional[int] = 1
    leverage_type: Optional[str] = None
    leverage_custom_value: Optional[float] = None
    start_order_type: Optional[str] = "limit"
    reinvesting_percentage: Optional[str] = "100.0"
    risk_reduction_percentage: Optional[str] = "0.0"
    reinvested_volume_usd: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_price_percentage: Optional[float] = None
    max_price_percentage: Optional[float] = None
    profit_currency: Optional[str] = "quote_currency"
    type: Optional[str] = "Bot::SingleBot"
    url_secret: Optional[str] = None

    # Strategy-related fields
    strategy_list: List[Strategy]
    close_strategy_list: Optional[List[Strategy]] = []
    safety_strategy_list: Optional[List[Strategy]] = []

    take_profit_steps: Optional[List[TakeProfitStep]] = []



class AddExchangeAccountPayload(BaseModel):
    type: str = Field(..., description="Market code (e.g., 'binance')")
    name: str = Field(..., description="Name for this exchange account")
    api_key: str = Field(..., description="API key from the exchange")
    secret: str = Field(..., description="Secret key from the exchange")
    address: Optional[str] = Field(None, description="Wallet address (if required)")
    customer_id: Optional[str] = Field(None, description="Customer ID for Bitstamp")
    passphrase: Optional[str] = Field(None, description="Secret phrase for OKX")
    types_to_create: Optional[List[str]] = Field(default_factory=list, description="Array of related account types to be created")



class CreateGridBotPayload(BaseModel):
    account_id: int
    pair: str
    name: str = Field(..., max_length=40)
    upper_price: float
    lower_price: float
    quantity_per_grid: float
    grids_quantity: int
    max_active_buy_lines: Optional[int] = None
    max_active_sell_lines: Optional[int] = None
    order_currency_type: Optional[str] = "base"
    profit_currency_type: Optional[str] = "base"
    ignore_warnings: Optional[bool] = False
    trailing_up_enabled: Optional[bool] = False
    trailing_down_enabled: Optional[bool] = False
    grid_type: Optional[str] = "arithmetic"  # "geometric" or "arithmetic"
    expansion_down_enabled: Optional[bool] = False
    expansion_up_enabled: Optional[bool] = False
    expansion_up_stop_price: Optional[float] = None



class UpdateGridBotPayload(BaseModel):
    name: str = Field(..., max_length=40)
    upper_price: float
    lower_price: float
    quantity_per_grid: float
    grids_quantity: int
    order_currency_type: Optional[str] = "quote"
    profit_currency_type: Optional[str] = "quote"
    trailing_up_enabled: Optional[bool] = False
    trailing_down_enabled: Optional[bool] = False
    grid_type: Optional[str] = "arithmetic"
    expansion_down_enabled: Optional[bool] = False
    expansion_down_stop_price: Optional[float] = None
    expansion_up_enabled: Optional[bool] = False
    expansion_up_stop_price: Optional[float] = None
    lower_stop_loss_enabled: Optional[bool] = False
    lower_stop_loss_price: Optional[float] = None
    lower_stop_loss_action: Optional[str] = None
    upper_stop_loss_enabled: Optional[bool] = False
    upper_stop_loss_price: Optional[float] = None
    upper_stop_loss_action: Optional[str] = None
    leverage_type: Optional[str] = "cross"
    leverage_custom_value: Optional[float] = 1
    max_active_sell_lines: Optional[int] = None
    note: Optional[str] = Field(None, max_length=300)
    ignore_warnings: Optional[bool] = False
    mode: Optional[str] = "long"
