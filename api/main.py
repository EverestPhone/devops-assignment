
from fastapi import FastAPI
import time
import logging
import json
import os
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI()

ENV = os.getenv("APP_ENV", "dev")

REQUEST_COUNT = Counter("api_requests_total", "Total API Requests")
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Request latency")

logging.basicConfig(level=logging.INFO)

@app.get("/health")
def health():
    start = time.time()
    REQUEST_COUNT.inc()
    response = {"status": "ok", "environment": ENV}
    REQUEST_LATENCY.observe(time.time() - start)
    logging.info(json.dumps(response))
    return response

@app.get("/metrics")
def metrics():
    return generate_latest()
