from typing import List, Optional
from pydantic import BaseModel

class AddExchangeAccountRequest(BaseModel):
    type: str
    name: str
    api_key: str
    secret: str
    address: Optional[str] = None
    customer_id: Optional[str] = None
    passphrase: Optional[str] = None
    types_to_create: Optional[List[str]] = None

class AddExchangeAccountResponse(BaseModel):
    id: int
    name: str
    exchange_name: str
    market_icon: Optional[str]
    market_code: str

