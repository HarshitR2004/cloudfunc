import docker
import json

client = docker.from_env()

def start_container(image: str, payload: dict):
    return client.containers.run(
        image,
        command=["sleep", "infinity"],
        detach=True,
        auto_remove=False,
        environment={"EVENT": json.dumps(payload)}
    )

def stop_container(container):
    try:
        container.reload()  
        if container.status == "running":
            container.stop()
        container.remove()
    except Exception as e:
        print(f"Error stopping container: {e}")

def invoke_container(container, payload):
    container.reload()  # Ensure container still exists
    result = container.exec_run(
        cmd=["sh", "-c", f"EVENT='{json.dumps(payload)}' python handler.py"],
    )
    return result

