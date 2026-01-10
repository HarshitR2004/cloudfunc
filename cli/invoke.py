import json
import requests
from config import API_GATEWAY_URL

def invoke_function(function_name: str, data: str):
    try:
        payload = json.loads(data)
    except json.JSONDecodeError:
        raise Exception("Payload must be valid JSON")

    resp = requests.post(
        f"{API_GATEWAY_URL}/invoke/{function_name}",
        json={"payload": payload}
    )

    resp.raise_for_status()

    print(f"Invocation request sent for '{function_name}'")
    print("Execution will happen asynchronously.")
