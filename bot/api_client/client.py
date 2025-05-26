# api_client/client.py
import os
import time
import requests
import base64
from urllib.parse import urlencode
import hmac
import hashlib
import json
from typing import Optional, Dict, Any
from ..config.settings import settings
from ..utils.logger import get_logger

logger = get_logger("APIClient")

class APIError(Exception):
    """Base class for API exceptions"""
    pass

class AuthenticationError(APIError):
    """Authentication related errors"""
    pass

class RateLimitError(APIError):
    """Rate limit exceeded errors"""
    pass

class ThreeCommasAPIClient:
    BASE_URL = settings.THREE_COMMAS_API_BASE_URL
    MAX_RETRIES = 3
    RETRY_DELAY = 5 

    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise AuthenticationError("API key and secret must be provided")

        # Debugging type of api_secret
        logger.debug(f"Type of api_secret before encoding: {type(api_secret)}")
        
        self.api_key = api_key
        
        # Encode the secret key to bytes for HMAC
        self.api_secret = api_secret.encode('utf-8')
        
        logger.debug(f"Type of api_secret after encoding: {type(self.api_secret)}")

        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _get_timestamp(self) -> str:
        return str(int(time.time() * 1000))

    def _sign(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        try:
            path = f"/public/api{endpoint}"

            query_string = ""
            if params:
                query_string = urlencode(sorted(params.items()))

            if query_string:
                string_to_sign = f"{path}?{query_string}"
            else:
                string_to_sign = path

            signature = hmac.new(
                self.api_secret,
                string_to_sign.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            return signature
        except Exception as e:
            logger.error(f"Signing failed: {str(e)}")
            raise APIError("Failed to sign request") from e

    def _get_headers(self, signature: str) -> dict:
        return {
            "Apikey": self.api_key,
            "Signature": signature,
            "Content-Type": "application/json",
        }

    def _handle_response(self, response: requests.Response) -> Any:
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                raise AuthenticationError("Invalid API credentials") from http_err
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded") from http_err
            else:
                error_msg = self._extract_error_message(response)
                raise APIError(f"API request failed: {error_msg}") from http_err
        except ValueError as json_err:
            raise APIError("Invalid JSON response") from json_err

    def _extract_error_message(self, response: requests.Response) -> str:
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                return error_data.get("error", {}).get("message", response.text)
            else:
                return str(error_data)
        except ValueError:
            return response.text

    def _request_with_retry(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Any:
        last_exception = None
        for attempt in range(self.MAX_RETRIES):
            try:
                signature = self._sign(method, endpoint, params if method.upper() == "GET" else None)
                headers = self._get_headers(signature)
                url = self.BASE_URL + endpoint

                logger.debug(f"{method.upper()} {url}")
                logger.debug(f"Headers: {headers}")
                logger.debug(f"Payload: {json.dumps(params, indent=2)}")

                if method.upper() == "GET":
                    response = self.session.get(url, headers=headers, params=params)
                else:
                    response = self.session.post(url, headers=headers, json=params)

                return self._handle_response(response)

            except RateLimitError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise
                retry_after = int(response.headers.get('Retry-After', self.RETRY_DELAY))
                logger.warning(f"Rate limited, retrying in {retry_after} seconds...")
                time.sleep(retry_after)

            except Exception as e:
                last_exception = e
                if attempt == self.MAX_RETRIES - 1:
                    break
                logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(self.RETRY_DELAY)

        logger.error(f"Request failed after {self.MAX_RETRIES} attempts")
        raise APIError("Max retries exceeded") from last_exception

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Make a GET request to the API"""
        try:
            logger.debug(f"GET {endpoint} with params: {params}")
            return self._request_with_retry("GET", endpoint, params)
        except Exception as e:
            logger.error(f"GET request failed: {str(e)}")
            raise

    def post(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Make a POST request to the API"""
        try:
            logger.debug(f"POST {endpoint} with payload: {params}")
            return self._request_with_retry("POST", endpoint, params)
        except Exception as e:
            logger.error(f"POST request failed: {str(e)}")
            raise
