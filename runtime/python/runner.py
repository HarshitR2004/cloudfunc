import json
import sys
import time
from importlib import import_module

user_module = import_module("function")

print("CloudFunc Python runtime started", flush=True)

while True:
    line = sys.stdin.readline()

    if not line:
        time.sleep(0.1)
        continue

    event = json.loads(line)
    result = user_module.handler(event)
    print(result, flush=True)
