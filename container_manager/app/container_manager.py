import threading
from docker_client import stop_container
from registry_client import mark_warm

from container_pool import container_pool, remove_container

class ContainerManager:
    def __init__(self, function_name: str, container, timeout: int = 60):
        self.function_name = function_name
        self.container = container
        self.timeout = timeout
        self.timer = None
        self.lock = threading.Lock()
        self.reset_timer()
        print(f"ContainerManager created for {self.function_name}. Cleanup in {self.timeout}s.")

    def _cleanup(self):
        """The actual cleanup action when the timer expires."""
        with self.lock:
            if container_pool.get(self.function_name) is self:
                print(f"Idle timeout reached. Cleaning up container for {self.function_name}.")
                try:
                    stop_container(self.container)
                    mark_warm(self.function_name, False)
                except Exception as e:
                    print(f"Error during container cleanup for {self.function_name}: {e}")
                finally:
                    # Always remove from pool
                    remove_container(self.function_name)
            else:
                print(f"Cleanup for {self.function_name} aborted; container has been replaced.")


    def reset_timer(self):
        """Cancels the existing timer and starts a new one."""
        with self.lock:
            if self.timer:
                self.timer.cancel()
            
            self.timer = threading.Timer(self.timeout, self._cleanup)
            self.timer.daemon = True
            self.timer.start()
        print(f"Timer reset for {self.function_name}. New cleanup in {self.timeout}s.")

    def get_container(self):
        return self.container
