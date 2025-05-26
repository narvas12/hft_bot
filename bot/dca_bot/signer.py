import base64
import json
from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

from ..config.config import PRIVATE_KEY_PATH, THREE_COMMAS_API_KEY, THREE_COMMAS_API_SECRET

def sign_payload(payload: dict) -> str:
    message = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    digest = sha256(message).digest()

    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )

    signature = private_key.sign(
        digest,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()
