from ..api_client.client import ThreeCommasAPIClient
from ..api_client.endpoints.dcaendpoint import create_dca_bot
from ..models.schemas import CreateDCABotPayload
from ..api_client.client import APIError

class DCABotService:
    def __init__(self, api_client: ThreeCommasAPIClient):
        self.api_client = api_client

    def create_bot(self, payload: CreateDCABotPayload) -> dict:
        """
        Create a DCA bot using the 3Commas API.
        """
        endpoint = create_dca_bot()
        try:
            response = self.api_client.post(endpoint, payload.dict())
            return response
        except APIError as e:
            raise Exception(f"Failed to create bot: {str(e)}")
