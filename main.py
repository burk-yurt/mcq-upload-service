
from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
import json

app = Flask(__name__)
SAVE_DIR = "files"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/")
def home():
    return send_from_directory(".", "README.html")

@app.route("/upload", methods=["POST"])
def upload_json():
    try:
        raw_body = request.get_data(as_text=True)
        print("🛬 RAW BODY:", raw_body)

        data = request.get_json(force=True)
        print("🧪 Parsed JSON:", data)

        if not data or "activities" not in data or not isinstance(data["activities"], list):
            print("❌ Missing or invalid 'activities'")
            return jsonify({"error": "Missing or invalid 'activities' list"}), 400

        filename = f"mcq_activities_{uuid.uuid4().hex[:8]}.json"
        filepath = os.path.join(SAVE_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data["activities"], f, indent=2)

        print(f"✅ File saved: {filename}")
        full_url = f"https://mcq-upload-service.onrender.com/files/{filename}"
        return jsonify({"downloadUrl": full_url}), 200

    except Exception as e:
        print("❌ EXCEPTION:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/files/<path:filename>")
def download_file(filename):
    return send_from_directory(SAVE_DIR, filename, as_attachment=True)

@app.route("/debug")
def debug():
    return jsonify({"status": "ok", "files": os.listdir(SAVE_DIR)})
