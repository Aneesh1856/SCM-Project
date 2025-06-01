from flask import Flask, request, jsonify, render_template
from datetime import datetime
from pathlib import Path
import json


class Config:
    DEBUG = True
    DATA_FILE = Path("feedbacks.json")


class FeedbackStorage:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        if not self.file_path.exists():
            self.file_path.write_text("[]")

    def read_all(self):
        try:
            content = self.file_path.read_text()
            return json.loads(content)
        except Exception:
            return []

    def write_all(self, data):
        serialized = json.dumps(data, indent=4)
        self.file_path.write_text(serialized)

    def add_feedback(self, name: str, message: str):
        entry = {
            "name": name if name else "Anonymous",
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        all_feedback = self.read_all()
        all_feedback.append(entry)
        self.write_all(all_feedback)
        return entry

    def clear_all(self):
        self.write_all([])

    def add_sample(self):
        return self.add_feedback("Tester", "Sample feedback.")


def format_response(status="success", message="", data=None):
    response = {"status": status}
    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return response


def validate_feedback_payload(data):
    if not data:
        return False, "Request body must be JSON."
    message = data.get("message", "").strip()
    if not message:
        return False, "Feedback message is required."
    return True, None


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    storage = FeedbackStorage(app.config["DATA_FILE"])

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/submit", methods=["POST"])
    def submit():
        try:
            data = request.get_json()
            valid, error = validate_feedback_payload(data)
            if not valid:
                return jsonify(format_response("error", error)), 400

            name = data.get("name", "").strip()
            message = data["message"].strip()
            saved = storage.add_feedback(name, message)

            return jsonify(format_response("success", "Feedback submitted.", saved)), 201
        except Exception as e:
            return jsonify(format_response("error", "An error occurred.")), 500

    @app.route("/feedbacks", methods=["GET"])
    def get_feedbacks():
        try:
            entries = storage.read_all()
            return jsonify(format_response(data=entries)), 200
        except Exception:
            return jsonify(format_response("error", "Could not load feedbacks.")), 500

    @app.route("/debug/clear", methods=["POST"])
    def clear_feedbacks():
        try:
            storage.clear_all()
            return jsonify(format_response("success", "All feedbacks cleared."))
        except Exception:
            return jsonify(format_response("error", "Clear failed.")), 500

    @app.route("/debug/sample", methods=["POST"])
    def add_sample():
        try:
            entry = storage.add_sample()
            return jsonify(format_response("success", "Sample added.", entry))
        except Exception:
            return jsonify(format_response("error", "Could not add sample.")), 500

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "message": "Server is running",
            "timestamp": datetime.utcnow().isoformat()
        })

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify(format_response("error", "Not found.")), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify(format_response("error", "Internal error.")), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
