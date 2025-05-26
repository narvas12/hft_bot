import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import httpx

from bot.config.config import THREE_COMMAS_API_KEY, THREE_COMMAS_API_SECRET, THREE_COMMAS_BASE_URL
from bot.exchange.schemas import AddExchangeAccountRequest, AddExchangeAccountResponse

from .signer import sign_payload


app = FastAPI()


EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
EXCHANGE_API_SECRET = os.getenv("EXCHANGE_API_SECRET")
EXCHANGE_PASSPHRASE = os.getenv("EXCHANGE_PASSPHRASE") 

@app.post("/ver1/accounts/new", response_model=AddExchangeAccountResponse)
async def add_exchange_account(request_body: AddExchangeAccountRequest):
    path = "/ver1/accounts/new"
    url = f"{THREE_COMMAS_BASE_URL}{path}"

    # Build full payload by adding API credentials from server-side config
    payload = request_body.dict(exclude_none=True)
    payload.update({
        "api_key": EXCHANGE_API_KEY,
        "secret": EXCHANGE_API_SECRET,
    })

    # Add passphrase if needed and configured on backend
    if EXCHANGE_PASSPHRASE:
        payload["passphrase"] = EXCHANGE_PASSPHRASE

    json_body_str = json.dumps(payload, separators=(',', ':'))  # compact JSON

    # Signature is based on path + JSON string payload
    total_params = f"{path}{json_body_str}"
    signature = sign_payload(THREE_COMMAS_API_SECRET, total_params)

    headers = {
        "Apikey": THREE_COMMAS_API_KEY,
        "Signature": signature,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, content=json_body_str)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()