import docker
import json

client = docker.from_env()

def start_container(image: str, payload: dict):
    return client.containers.run(
        image,
        detach=True,
        auto_remove=False,
        stdin_open=True,
        tty=False
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
    try:
        container.reload()
        socket = container.attach_socket(params={'stdin': 1, 'stream': 1})
        socket._sock.sendall((json.dumps(payload) + '\n').encode('utf-8'))
        socket.close()
        
        import time
        time.sleep(0.5) 
        logs = container.logs(tail=10).decode('utf-8')
        print(f"Function output:\n{logs}", flush=True)
        
    except Exception as e:
        print(f"Error invoking container: {e}", flush=True)


