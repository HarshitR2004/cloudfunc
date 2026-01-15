import traceback
from docker_client import start_container, invoke_container
from container_pool import get_warm_container, set_warm_container
from registry_client import mark_warm
from container_manager import ContainerManager

def execute_function(message: dict):
    try:
        function_name = message.get("function")
        payload = message.get("payload")

        if not function_name:
            print("Function name missing in message.")
            return
        
        manager = get_warm_container(function_name)
        container = None

        if manager:
            print(f"Warm start for {function_name}")
            manager.reset_timer() 
            container = manager.get_container()
        else:
            print(f"Cold start for {function_name}")
            try:
                container = start_container(image=function_name, payload=payload)
                manager = ContainerManager(function_name, container)
                set_warm_container(function_name, manager)
                mark_warm(function_name, True)
                print(f"Container started: {container.id}")
            except Exception as e:
                print(f"Error starting container: {e}")
                traceback.print_exc()
                return

        if container:
            print(f"Executing {function_name} with payload {payload}")
            try:
                invoke_container(container, payload)
                print(f"Successfully invoked {function_name}")
            except Exception as e:
                print(f"Error invoking container: {e}")
                traceback.print_exc()

    except Exception as e:
        print(f"Unexpected error in execute_function: {e}")
        traceback.print_exc()
