import hmac
import hashlib

def generate_signature(api_secret: str, request_path: str, query_string: str = "", request_body: str = "") -> str:
    """
    Generate HMAC SHA256 signature for 3Commas API.

    :param api_secret: Your 3Commas secret key
    :param request_path: The full API path (e.g., /public/api/ver1/bots/create_bot)
    :param query_string: The URL query string (e.g., param1=value1&param2=value2)
    :param request_body: The raw request body (for POST/PUT requests)
    :return: Hex-encoded HMAC SHA256 signature
    """
    # Form the full payload string to sign
    total_params = request_path
    if query_string:
        total_params += "?" + query_string
    total_params += request_body

    # Compute HMAC SHA256 signature
    signature = hmac.new(
        api_secret.encode("utf-8"),
        total_params.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return signature
