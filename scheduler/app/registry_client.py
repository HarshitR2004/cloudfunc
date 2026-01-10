import requests
import os

REGISTRY_URL = os.getenv(
    "REGISTRY_URL",
    "http://function-registry:7000"
)

def fetch_function(function_name: str):
    try:
        resp = requests.get(
            f"{REGISTRY_URL}/functions/{function_name}",
            timeout=2
        )
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Registry unreachable: {e}")

