import base64
import json
from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

from ..config.config import PRIVATE_KEY_PATH, THREE_COMMAS_API_KEY, THREE_COMMAS_API_SECRET

import hmac
import hashlib

def sign_payload(secret_key: str, total_params: str) -> str:
    secret_bytes = secret_key.encode('utf-8')
    data_bytes = total_params.encode('utf-8')
    signature = hmac.new(secret_bytes, data_bytes, hashlib.sha256).hexdigest()
    return signature.lower()
