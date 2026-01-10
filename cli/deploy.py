import os
import subprocess
import requests
from config import API_GATEWAY_URL

def deploy_function(function_name: str):
    function_dir = os.path.abspath(function_name)

    if not os.path.isdir(function_dir):
        raise Exception("Function directory not found")

    image_name = f"{function_name}:latest"

    print(f"Building Docker image for {function_name}...")

    subprocess.run(
        ["docker", "build", "-t", image_name, function_dir],
        check=True
    )

    print("Registering function with CloudFunc...")

    resp = requests.post(
        f"{API_GATEWAY_URL}/deploy",
        json={
            "name": function_name,
            "image": image_name,
            "runtime": "python"
        }
    )

    resp.raise_for_status()

    print(f"Function '{function_name}' deployed successfully")
