
import time
import logging
import json
from datetime import datetime
import os

ENV = os.getenv("APP_ENV", "dev")

logging.basicConfig(level=logging.INFO)

def update_today_records():
    while True:
        now = datetime.utcnow().isoformat()
        log = {"updated_timestamp": now, "environment": ENV}
        logging.info(json.dumps(log))
        time.sleep(15)

if __name__ == "__main__":
    update_today_records()
