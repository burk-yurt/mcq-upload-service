from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
import json

app = Flask(__name__)

# Create a folder to store files
SAVE_DIR = "files"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/")
def home():
    return "MCQ Upload Service is live!"

@app.route("/upload", methods=["POST"])
def upload_json():
    data = request.get_json()
    if not data or "activities" not in data:
        return jsonify({"error": "Missing 'activities' field"}), 400

    filename = f"mcq_activities_{uuid.uuid4().hex[:8]}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data["activities"], f, indent=2)

    return jsonify({"downloadUrl": f"/files/{filename}"}), 200

@app.route("/files/<path:filename>")
def download_file(filename):
    return send_from_directory(SAVE_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
