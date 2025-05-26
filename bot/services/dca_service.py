from ..api_client.client import ThreeCommasAPIClient, APIError
from ..api_client.endpoints.dcaendpoint import create_dca_bot
from ..models.schemas import CreateDCABotPayload

class DCABotService:
    def __init__(self, api_client: ThreeCommasAPIClient):
        self.api_client = api_client

    def create_bot(self, payload: CreateDCABotPayload) -> dict:
        endpoint = create_dca_bot()
        try:
            return self.api_client.post(endpoint, payload.dict())
        except APIError as e:
            raise Exception(f"Failed to create bot: {str(e)}")
