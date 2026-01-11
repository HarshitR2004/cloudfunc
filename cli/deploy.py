import os
import tempfile
import shutil
import subprocess
import requests
from config import API_GATEWAY_URL

RUNTIME_IMAGE = "cloudfunc-python-runtime"

def deploy_function(function_name: str):
    function_dir = os.path.abspath(function_name)
    function_file = os.path.join(function_dir, "function.py")

    if not os.path.exists(function_file):
        raise Exception("function.py not found")

    build_dir = tempfile.mkdtemp()

    try:
        shutil.copy(function_file, os.path.join(build_dir, "function.py"))

        dockerfile_path = os.path.join(build_dir, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(f"""
FROM {RUNTIME_IMAGE}
COPY function.py /app/function.py
""")

        image_name = function_name.lower()

        subprocess.run(
            ["docker", "build", "-t", image_name, build_dir],
            check=True
        )

        requests.post(
            f"{API_GATEWAY_URL}/deploy",
            json={
                "name": function_name,
                "image": image_name,
                "runtime": "python"
            }
        ).raise_for_status()

        print(f"Function '{function_name}' deployed")

    finally:
        shutil.rmtree(build_dir)

