from flask import Flask, request, jsonify, send_from_directory
import os
from spleeter.separator import Separator
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

separator = Separator("spleeter:2stems")

@app.route("/separate", methods=["POST"])
def separate_audio():
    if "file" not in request.files:
        return jsonify({"error": "Nessun file caricato"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nessun file selezionato"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    separator.separate_to_file(filepath, OUTPUT_FOLDER)

    output_path = os.path.join(OUTPUT_FOLDER, os.path.splitext(filename)[0])

    return jsonify({
        "vocals": f"/download/{filename}/vocals.wav",
        "instrumental": f"/download/{filename}/accompaniment.wav"
    })

@app.route("/download/<filename>/<stem>", methods=["GET"])
def download_file(filename, stem):
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_from_directory(output_path, stem)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
