import requests
import os

REGISTRY_URL = os.getenv(
    "REGISTRY_URL",
    "http://function-registry:7000"
)

def register_function(data):
    resp = requests.post(
        f"{REGISTRY_URL}/functions",
        json={
            "name": data.name,
            "image": data.image,
            "runtime": data.runtime
        }
    )
    resp.raise_for_status()
    return resp.json()

def get_function(name: str):
    resp = requests.get(
        f"{REGISTRY_URL}/functions/{name}"
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()

