from typing import Dict, Any 

container_pool: Dict[str, Any] = {}

def get_warm_container(function_name: str):
    """Returns the ContainerManager object if one exists."""
    return container_pool.get(function_name)

def set_warm_container(function_name: str, manager):
    """Adds a ContainerManager to the pool."""
    container_pool[function_name] = manager

def remove_container(function_name: str):
    """Removes a manager from the pool."""
    if function_name in container_pool:
        del container_pool[function_name]
