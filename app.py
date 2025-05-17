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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    name = data.get("name", "Anonymous")
    message = data.get("message", "")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback = {
        "name": name,
        "message": message,
        "timestamp": timestamp
    }
    save_feedback(feedback)
    return jsonify({"status": "success", "feedback": feedback})

@app.route("/feedbacks")
def feedbacks():
    return jsonify(load_feedbacks())

if __name__ == "__main__":
    app.run(debug=True)
