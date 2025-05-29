from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
DATA_FILE = "feedbacks.json"

def load_feedbacks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_feedback(feedback):
    data = load_feedbacks()
    data.append(feedback)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
