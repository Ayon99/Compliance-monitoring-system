import requests
import time
import random

URL = "http://127.0.0.1:8000/ingest-log"

services = ["auth-service", "payment-service", "order-service"]

messages = [
    ("INFO", "User login success"),
    ("ERROR", "Invalid token"),
    ("WARNING", "Slow response detected"),
    ("ERROR", "Database connection failed"),
    ("INFO", "Order placed successfully")
]

while True:
    level, message = random.choice(messages)

    log = {
        "service": random.choice(services),
        "level": level,
        "message": message,
        "user_id": f"user{random.randint(1,5)}"
    }

    try:
        res = requests.post(URL, json=log)
        print("Sent log:", log)
    except Exception as e:
        print("Error:", e)

    time.sleep(2)