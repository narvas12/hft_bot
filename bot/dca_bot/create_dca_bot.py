import json
import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from bot.config.config import THREE_COMMAS_API_KEY, THREE_COMMAS_BASE_URL, THREE_COMMAS_API_SECRET
from .signer import generate_signature
from .schemas import CreateDCABotPayload

# Initialize app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def make_3commas_request(method: str, path: str, params: dict = None, payload: dict = None):
    nonce = str(int(time.time() * 1000))
    url = f"{THREE_COMMAS_BASE_URL}{path}"

    query_string = ""
    if method == "GET" and params:
        query_string = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
        url = f"{url}?{query_string}"

    body = json.dumps(payload, separators=(",", ":"), sort_keys=True) if payload else ""

    # ❗ Pass query_string now
    signature = generate_signature(THREE_COMMAS_API_SECRET, path, query_string, body)

    headers = {
        "APIKEY": THREE_COMMAS_API_KEY,
        "Signature": signature,
        "Content-Type": "application/json",
    }

    async with AsyncClient() as client:
        if method == "GET":
            response = await client.get(url, headers=headers)
        elif method == "POST":
            response = await client.post(url, headers=headers, content=body)
        else:
            raise HTTPException(status_code=400, detail="Unsupported HTTP method")

    print(f"3Commas API Request: {method} {url}")
    print(f"Headers: {headers}")
    if payload:
        print(f"Payload: {payload}")
    print(f"Response: {response.status_code} {response.text}")

    if response.status_code == 204:
        return None
    if 200 <= response.status_code < 300:
        try:
            return response.json() if response.text else None
        except json.JSONDecodeError:
            return response.text
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text or f"3Commas API returned status code {response.status_code}"
        )


@app.post("/create-dca-bot/")
async def create_dca_bot(payload: CreateDCABotPayload):
    try:
        result = await make_3commas_request(
            "POST",
            "/public/api/ver1/bots/create_bot",
            payload=payload.dict()
        )
        return result or {"detail": "Bot created successfully (no content returned)"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-dca-bot/{bot_id}")
async def get_dca_bot(bot_id: int, include_events: bool = True):
    try:
        result = await make_3commas_request(
            "GET",
            f"/public/api/ver1/bots/{bot_id}/show",
            params={"include_events": str(include_events).lower()}
        )
        if result is None:
            raise HTTPException(status_code=404, detail="Bot not found")
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-dca-bots/")
async def list_dca_bots(
    account_id: Optional[int] = None,
    strategy: Optional[str] = None,
    order_direction: str = "DESC",
    limit: Optional[int] = None,
    offset: Optional[int] = None
):
    try:
        params = {
            "account_id": account_id,
            "strategy": strategy,
            "order_direction": order_direction,
            "limit": limit,
            "offset": offset
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        result = await make_3commas_request(
            "GET",
            "/public/api/ver1/bots",
            params=params
        )
        return result or {"detail": "No bots found"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/get-strategy-list/")
async def get_strategy_list(
    account_id: Optional[int] = Query(None, description="3Commas exchange account ID"),
    type: Optional[str] = Query(None, description="Strategy direction type"),
    strategy: Optional[str] = Query(None, description="Strategy name")
):
    try:
        params = {
            "account_id": account_id,
            "type": type,
            "strategy": strategy
        }
        params = {k: v for k, v in params.items() if v is not None}

        result = await make_3commas_request(
            "GET",
            "/public/api/ver1/bots/strategy_list",
            params=params
        )
        return result or {"detail": "No strategies found"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
