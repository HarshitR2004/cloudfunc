import json
import os
import time
from handler import handler

print("Function container started")

while True:
    payload = os.getenv("EVENT")

    if payload:
        event = json.loads(payload)
        result = handler(event)
        print(result)

        # clear event so it doesn't re-run
        os.environ["EVENT"] = ""

    time.sleep(0.5)

