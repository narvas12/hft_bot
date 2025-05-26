import os


THREE_COMMAS_API_KEY = os.environ.get("THREE_COMMAS_API_KEY")
THREE_COMMAS_API_SECRET = os.environ.get("THREE_COMMAS_API_SECRET")
PRIVATE_KEY_PATH = os.environ.get("PRIVATE_KEY_PATH", "keys/private_key.pem")
THREE_COMMAS_BASE_URL = os.environ.get("THREE_COMMAS_BASE_URL", "https://api.3commas.io/public/api")
if not THREE_COMMAS_API_KEY or not THREE_COMMAS_API_SECRET:
    raise ValueError("THREE_COMMAS_API_KEY and THREE_COMMAS_API_SECRET must be set in environment variables.")