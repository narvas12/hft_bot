import json
from api_client.client import ThreeCommasAPIClient
from dcaendpoint import create_dca_bot

class DCABotService:
    def __init__(self, api_client: ThreeCommasAPIClient):
        self.api_client = api_client

    def create_bot(self, bot_data: dict) -> dict:
        """
        Create a new DCA bot using the 3Commas API.

        :param bot_data: dict with required bot parameters as per API docs.
        :return: dict response from the API
        """
        endpoint = create_dca_bot()
        
        # The client should have a method like post_signed(endpoint, payload)
        response = self.api_client.post_signed(endpoint, json.dumps(bot_data))
        
        # You can handle errors here based on response status, for example:
        if response.status_code == 201:
            return response.json()
        else:
            # Raise or return error details
            raise Exception(f"Failed to create DCA bot: {response.status_code} - {response.text}")
