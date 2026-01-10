import requests
import os

REGISTRY_URL = os.getenv(
    "REGISTRY_URL",
    "http://function-registry:7000"
)

def mark_warm(function_name: str, is_warm: bool):
    requests.patch(
        f"{REGISTRY_URL}/functions/{function_name}/warm",
        json={"is_warm": is_warm}
    )
