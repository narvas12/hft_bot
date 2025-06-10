import json
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from bot.config.config import THREE_COMMAS_API_KEY, THREE_COMMAS_BASE_URL, THREE_COMMAS_API_SECRET
from .signer import generate_signature
from .schemas import AddExchangeAccountPayload, CreateDCABotPayload, CreateGridBotPayload, UpdateGridBotPayload

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

#=================================EXCHANGE ACCOUNT ENDPOINTS=================================
@app.post("/add-exchange-account/")
async def add_exchange_account(payload: AddExchangeAccountPayload):
    try:
        result = await make_3commas_request(
            "POST",
            "/public/api/ver1/accounts/new",
            payload=payload.dict(exclude_none=True)
        )
        return result or {"detail": "Exchange account added successfully (no content returned)"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/account/list")
async def get_accounts_list():
    """
    Fetch the list of all exchange accounts associated with your 3Commas API key.
    """
    try:
        response = await make_3commas_request(
            "GET",
            "/public/api/ver1/accounts"
        )
        print(f"Accounts List Response: {response}")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/account/details/{account_id}")
async def get_account_details(account_id: int = Path(..., description="3Commas account ID")):
    """
    Fetch exchange account details using the 3Commas account ID.
    """
    try:
        response = await make_3commas_request(
            "GET",
            f"/public/api/ver1/accounts/{account_id}"
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#=================================EXCHANGE ACCOUNT ENDPOINTS END=================================

#=================================DCA ENDPOINTS=================================
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


@app.post("/enable-dca-bot/{bot_id}")
async def enable_dca_bot(bot_id: int):
    try:
        result = await make_3commas_request(
            method="POST",
            path=f"/public/api/ver1/bots/{bot_id}/enable"
        )
        return result or {"detail": f"Bot {bot_id} enabled successfully (no content returned)"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/disable-dca-bot/{bot_id}")
async def disable_dca_bot(bot_id: int):
    try:
        result = await make_3commas_request(
            method="POST",
            path=f"/public/api/ver1/bots/{bot_id}/disable"
        )
        return result or {"detail": f"Bot {bot_id} disabled successfully (no content returned)"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/delete-dca-bot/{bot_id}")
async def delete_dca_bot(bot_id: int):
    try:
        result = await make_3commas_request(
            method="POST",
            path=f"/public/api/ver1/bots/{bot_id}/delete"
        )
        return result or {"detail": f"Bot {bot_id} deleted successfully (no content returned)"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update-dca-bot/{bot_id}")
async def update_dca_bot(bot_id: int, payload: CreateDCABotPayload):
    try:
        result = await make_3commas_request(
            method="POST",
            path=f"/public/api/ver1/bots/{bot_id}/update",
            payload=payload.dict()
        )
        return result or {"detail": f"Bot {bot_id} updated successfully (no content returned)"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#=================================DCA ENDPOINTS END=================================



#=================================GRID ENDPOINTS=================================
@app.post("/create-grid-bot/")
async def create_grid_bot(payload: CreateGridBotPayload):
    try:
        result = await make_3commas_request(
            "POST",
            "/public/api/ver1/grid_bots/manual",
            payload=payload.dict(exclude_none=True)
        )
        return result or {"detail": "Grid bot created successfully (no content returned)"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.patch("/{bot_id}/manual")
async def update_grid_bot(bot_id: int = Path(..., description="3Commas Grid Bot ID"),
                          payload: UpdateGridBotPayload = ...):
    try:
        endpoint = f"/public/api/ver1/grid_bots/{bot_id}/manual"
        response = await make_3commas_request(
            method="PATCH",
            path=endpoint,
            body=payload.dict(exclude_none=True)
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.get("/grid-bots/{bot_id}")
def get_grid_bot(bot_id: int = Path(..., description="Grid Bot ID")):
    """
    Get a single Grid Bot by its ID.
    """
    response = make_3commas_request(
        method="GET",
        path=f"/public/api/ver1/grid_bots/{bot_id}",
    )
    return response


@app.get("/grid-bots")
def list_grid_bots(
    account_ids: Optional[List[int]] = Query(None, description="Comma-separated list of account IDs"),
    state: Optional[str] = Query(None, description="Bot state: enabled or disabled"),
    sort_by: Optional[str] = Query(None),
    sort_direction: Optional[str] = Query("DESC", regex="^(ASC|DESC)$"),
    limit: Optional[int] = Query(None),
    offset: Optional[int] = Query(None),
    from_date: Optional[str] = Query(None, alias="from"),
    base: Optional[str] = Query(None),
    quote: Optional[str] = Query(None)
):
    """
    Get a list of Grid Bots with optional filters.
    """
    query_params = {}

    if account_ids:
        query_params["account_ids[]"] = account_ids
    if state:
        query_params["state"] = state
    if sort_by:
        query_params["sort_by"] = sort_by
    if sort_direction:
        query_params["sort_direction"] = sort_direction
    if limit:
        query_params["limit"] = limit
    if offset:
        query_params["offset"] = offset
    if from_date:
        query_params["from"] = from_date
    if base:
        query_params["base"] = base
    if quote:
        query_params["quote"] = quote

    response = make_3commas_request(
        method="GET",
        path="/public/api/ver1/grid_bots",
        params=query_params
    )
    return response


@app.get("/grid-bots/{bot_id}/profits")
def get_grid_bot_profits(
    bot_id: int = Path(..., description="Grid Bot ID"),
    from_date: Optional[str] = Query(None, alias="from", description="Filter from ISO date"),
    to_date: Optional[str] = Query(None, alias="to", description="Filter to ISO date")
):
    """
    Get profit details for a specific Grid Bot.
    """
    query_params = {}
    if from_date:
        query_params["from"] = from_date
    if to_date:
        query_params["to"] = to_date

    response = make_3commas_request(
        method="GET",
        path=f"/public/api/ver1/grid_bots/{bot_id}/profits",
        params=query_params
    )
    return response


@app.post("/grid-bots/{bot_id}/enable")
def enable_grid_bot(bot_id: int = Path(..., description="Grid Bot ID")):
    """
    Enable a specific Grid Bot by ID.
    """
    response = make_3commas_request(
        method="POST",
        path=f"/public/api/ver1/grid_bots/{bot_id}/enable"
    )
    return response


@app.post("/grid-bots/{bot_id}/disable")
def disable_grid_bot(bot_id: int = Path(..., description="Grid Bot ID")):
    """
    Disable a specific Grid Bot by ID.
    """
    response = make_3commas_request(
        method="POST",
        path=f"/public/api/ver1/grid_bots/{bot_id}/disable"
    )
    return response


@app.delete("/grid-bots/{bot_id}")
def delete_grid_bot(bot_id: int = Path(..., description="Grid Bot ID")):
    """
    Delete a specific Grid Bot by ID.
    """
    response = make_3commas_request(
        method="DELETE",
        path=f"/public/api/ver1/grid_bots/{bot_id}"
    )
    return response


@app.get("/grid-bots/{bot_id}/required-balances")
def get_required_balances(bot_id: int = Path(..., description="Grid Bot ID")):
    """
    Get required and missing balances for launching a Grid Bot.
    Works only for Spot exchanges.
    """
    response = make_3commas_request(
        method="GET",
        path=f"/public/api/ver1/grid_bots/{bot_id}/required_balances"
    )
    return response


@app.get("/grid-bots/{bot_id}/events")
def get_grid_bot_events(
    bot_id: int = Path(..., description="Grid Bot ID"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    per_page: int = Query(100, ge=1, le=100, description="Records per page (1–100)")
):
    """
    Retrieve a list of events for a specific Grid Bot by ID.
    """
    response = make_3commas_request(
        method="GET",
        path=f"/public/api/ver1/grid_bots/{bot_id}/events",
        params={"page": page, "per_page": per_page}
    )
    return response


@app.get("/grid-bots/{bot_id}/market-orders")
def get_grid_bot_market_orders(
    bot_id: int = Path(..., description="Unique 3Commas ID for this Grid Bot entity"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to fetch"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    Returns a list of market orders for a specific Grid Bot by ID.
    """
    response = make_3commas_request(
        method="GET",
        path=f"/public/api/ver1/grid_bots/{bot_id}/market_orders",
        params={"limit": limit, "offset": offset}
    )
    return response
#=================================GRID ENDPOINTS END=================================