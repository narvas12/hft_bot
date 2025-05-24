from pydantic import Extra
from pydantic_settings import BaseSettings
from typing import Optional, List
import os
import json

class Settings(BaseSettings):
    # 3Commas API Settings
    THREECOMMAS_API_KEY: str
    THREECOMMAS_API_SECRET: str
    STRATEGY: str = "dummy"
    POLL_INTERVAL: int = 5 
    THREE_COMMAS_API_BASE_URL: str = "https://api.3commas.io/public/api"
    
    # Exchange Settings
    EXCHANGE_TYPE: str = "binance"
    EXCHANGE_NAME: Optional[str] = "My Exchange Account"
    EXCHANGE_API_KEY: str
    EXCHANGE_SECRET_KEY: str
    EXCHANGE_PASSPHRASE: Optional[str] = None
    
    # These are not used in your code, can be removed if not needed
    EXCHANGE_TYPE_TO_USE: Optional[str] = None
    EXCHANGE_TYPE_TO_USE_FOR_BACKTESTING: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = Extra.allow  # ✅ Allow unexpected fields from .env

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "EXCHANGE_TYPES_TO_CREATE":
                return [x.strip() for x in raw_val.split(",")]
            return json.loads(raw_val) if raw_val.startswith("[") and raw_val.endswith("]") else raw_val

settings = Settings()