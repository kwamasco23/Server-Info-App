from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response, Flask, request, jsonify
import socket
import datetime
import os
import platform
import time
import psutil

app = Flask(__name__)

# ✅ PROMETHEUS METRICS
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total number of requests',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

VERSION = os.getenv("VERSION", "1.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "local")

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

start_time = time.time()


# 🔹 LOG + TRACK REQUESTS
@app.before_request
def before_request():
    request.start_time = time.time()

    print(f"""
[{datetime.datetime.now()}] REQUEST RECEIVED
Method: {request.method}
Path: {request.path}
IP: {request.remote_addr}
""")


@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(
        request.method,
        request.path
    ).inc()

    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(latency)

    return response


# 🔹 MAIN PAGE
@app.route("/", methods=["GET", "POST"])
def home():

    response_message = ""

    if request.method == "POST":

        name = request.form.get("name")
        message = request.form.get("message")

        response_message = f"""
        <h3>Response from server:</h3>
        Hello <b>{name}</b><br>
        Your message: {message}<br>
        Served by: {hostname}<br>
        Time: {datetime.datetime.now()}
        """

    uptime_seconds = int(time.time() - start_time)

    return f"""
    <h1>🚀 Interactive Server Info App</h1>

    <b>Version:</b> {VERSION}<br>
    <b>Environment:</b> {ENVIRONMENT}<br>
    <b>Build:</b> {BUILD_NUMBER}<br>
    <b>Hostname:</b> {hostname}<br>
    <b>IP Address:</b> {ip_address}<br>
    <b>Uptime:</b> {uptime_seconds} seconds<br>

    <hr>

    <h2>🖥 System Info</h2>
    CPU Usage: {psutil.cpu_percent()}%<br>
    Memory Usage: {psutil.virtual_memory().percent}%<br>
    Platform: {platform.system()} {platform.release()}<br>

    <hr>

    <h2>💬 Send a Message</h2>
    <form method="post">
        Name:<br>
        <input type="text" name="name"><br><br>

        Message:<br>
        <input type="text" name="message"><br><br>

        <input type="submit" value="Send">
    </form>

    {response_message}
    """


# 🔹 HEALTH CHECK
@app.route("/health")
def health():
    return {
        "status": "OK",
        "uptime_seconds": int(time.time() - start_time)
    }


# 🔹 API ENDPOINT
@app.route("/api/info")
def api_info():
    return jsonify({
        "hostname": hostname,
        "environment": ENVIRONMENT,
        "version": VERSION,
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent
    })


# 🔹 PROMETHEUS METRICS
@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


# 🔹 START APP
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002
    )