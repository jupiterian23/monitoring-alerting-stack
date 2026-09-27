from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of HTTP requests"
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "HTTP request latency"
)

ERROR_COUNT = Counter(
    "app_errors_total",
    "Total number of application errors"
)


@app.route("/")
def home():
    REQUEST_COUNT.inc()

    start = time.time()
    time.sleep(random.uniform(0.01, 0.1))
    REQUEST_LATENCY.observe(time.time() - start)

    return jsonify({
        "service": "monitoring-alerting-demo",
        "status": "running"
    })


@app.route("/health")
def health():
    REQUEST_COUNT.inc()

    return jsonify({
        "status": "healthy"
    })


@app.route("/error")
def error():
    REQUEST_COUNT.inc()
    ERROR_COUNT.inc()

    return jsonify({
        "status": "error",
        "message": "Simulated application error"
    }), 500


@app.route("/alerts", methods=["POST"])
def alerts():
    return jsonify({
        "status": "alert received"
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
