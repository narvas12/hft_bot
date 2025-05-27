from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from bot.config.config import THREE_COMMAS_API_KEY, THREE_COMMAS_BASE_URL
from .signer import sign_payload
from .schemas import CreateDCABotPayload

# First, initialize the app
app = FastAPI()

# Then, add CORS middleware to handle OPTIONS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Or list: ["POST"]
    allow_headers=["*"],
)

@app.post("/create-dca-bot/")
async def create_dca_bot(payload: CreateDCABotPayload):
    url = f"{THREE_COMMAS_BASE_URL}/ver1/bots/create_bot"
    signature = sign_payload(payload.dict())

    headers = {
        "APIKEY": THREE_COMMAS_API_KEY,
        "Signature": signature,
        "Content-Type": "application/json"
    }

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload.dict())

    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
