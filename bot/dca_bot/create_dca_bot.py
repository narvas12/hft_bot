from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient, RequestError, HTTPStatusError
from bot.config.config import THREE_COMMAS_API_KEY, THREE_COMMAS_BASE_URL
from .signer import sign_payload
from .schemas import CreateDCABotPayload
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to allowed domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.error")

@app.post("/create-dca-bot/")
async def create_dca_bot(payload: CreateDCABotPayload):
    url = f"{THREE_COMMAS_BASE_URL}/ver1/bots/create_bot"
    try:
        signature = sign_payload(payload.dict())

        headers = {
            "APIKEY": THREE_COMMAS_API_KEY,
            "Signature": signature,
            "Content-Type": "application/json"
        }

        async with AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload.dict())
            response.raise_for_status()  # Raises for 4xx/5xx

        try:
            return response.json()
        except ValueError:
            logger.error("Failed to decode JSON response", exc_info=True)
            raise HTTPException(status_code=502, detail="Invalid response format from 3Commas")

    except RequestError as e:
        logger.error("Network error while contacting 3Commas", exc_info=True)
        raise HTTPException(status_code=503, detail="Network error while contacting 3Commas")

    except HTTPStatusError as e:
        logger.error(f"3Commas returned HTTP error {e.response.status_code}: {e.response.text}", exc_info=True)
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"3Commas error: {e.response.text}"
        )

    except Exception as e:
        logger.error("Unexpected error while creating DCA bot", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
