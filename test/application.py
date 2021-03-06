import os
import classes
import requests
import json
from flask import Flask, request, render_template, redirect, url_for, session
from flask import Flask
from flask import jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():

  # Query for currency exchange rate
  currency = request.form.get("currency")
  res = requests.get("https://api.fixer.io/latest", params={
      "base": "USD", "symbols": currency})

  # Make sure request succeeded
  if res.status_code != 200:
      return jsonify({"success": False})

  # Make sure currency is in response
  data = res.json()
  if currency not in data["rates"]:
      return jsonify({"success": False})

  return jsonify({"success": True, "rate": data["rates"][currency]})
