from flask import Flask, request, jsonify
import socket
import datetime
import os
import platform

app = Flask(__name__)

VERSION = os.getenv("VERSION", "1.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "local")

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


# 🔹 LOG EVERY REQUEST
@app.before_request
def log_request():

    print(f"""
[{datetime.datetime.now()}] REQUEST RECEIVED
Method: {request.method}
Path: {request.path}
IP: {request.remote_addr}
""")


@app.route("/", methods=["GET", "POST"])
def home():

    response_message = ""

    if request.method == "POST":

        name = request.form.get("name")
        message = request.form.get("message")

        # 🔹 LOG POST DATA
        print(f"""
[{datetime.datetime.now()}] POST DATA RECEIVED
Name: {name}
Message: {message}
Served by: {hostname}
""")

        response_message = f"""
        <h3>Response from server:</h3>
        Hello <b>{name}</b><br>
        Your message: {message}<br>
        Served by: {hostname}<br>
        Time: {datetime.datetime.now()}
        """

    return f"""
    <h1>Interactive Server Info App</h1>

    Version: {VERSION}<br>
    Environment: {ENVIRONMENT}<br>
    Hostname: {hostname}<br>

    <hr>

    <form method="post">

        Name:<br>
        <input type="text" name="name"><br><br>

        Message:<br>
        <input type="text" name="message"><br><br>

        <input type="submit" value="Send">

    </form>

    {response_message}

    """


@app.route("/health")
def health():

    print(f"[{datetime.datetime.now()}] Health check called")

    return {
        "status": "OK"
    }


@app.route("/api/info")
def api_info():

    print(f"[{datetime.datetime.now()}] API info endpoint called")

    return jsonify({
        "hostname": hostname
    })


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5002)