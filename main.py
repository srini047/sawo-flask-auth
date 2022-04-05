from flask import Flask, render_template, request
from sawo import createTemplate, verifyToken
import json
import os

API_KEY = os.getenv("60061273-af9b-4a32-bdc2-7a7a97a75d2b")

app = Flask(__name__)
createTemplate("./templates/partials", flask=True)

load = ''
loaded = 0


def setPayload(payload):
    global load
    load = payload


def setLoaded(reset=False):
    global loaded
    if reset:
        loaded = 0
    else:
        loaded += 1


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_page")
def login_page():
    setLoaded()
    setPayload(load if loaded < 2 else '')
    sawo = {
        "auth_key": API_KEY,
        "to": "login",
        "identifier": "email"
    }
    return render_template("login.html", sawo=sawo, load=load)


@app.route("/login", methods=["POST", "GET"])
def login():
    payload = json.loads(request.data)["payload"]
    setLoaded(True)
    setPayload(payload)
    status = 200 if(verifyToken(payload)) else 404
    return {"status": status}


if __name__ == '__main__':
    app.run()