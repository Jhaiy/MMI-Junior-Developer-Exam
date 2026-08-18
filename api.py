from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from pathlib import Path
from common.database import supabase, get_card, get_card_image, fetch_card_ids
from flask_cors import CORS
import base64
import mimetypes
from flask import send_file

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
ALLOWED_IMAGE_CATEGORIES = {
    "resistance_filepath",
    "moves_filepath",
    "weakness_filepath",
    "filepath",
}


def resolve_image_path(image_path):
  if not image_path or not isinstance(image_path, str):
    return None

  candidate = Path(image_path)
  if not candidate.is_absolute():
    candidate = BASE_DIR / candidate

  resolved = candidate.resolve()
  if not resolved.exists() or not resolved.is_file():
    return None

  return resolved


CORS(
    app,
    resources={
        r"/*": {
            "origins": "http://localhost:3000"
        }
    }
)

UPLOAD_FOLDER = "uploaded_images" # This will be the variable for the upload folder path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["POST"])

def upload_image_to_directory_database():

  try:
    if "file" not in request.files:
      return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
      return jsonify({"error": "No file selected"}), 400

    record_id = str(uuid.uuid4()) # Generate uuid to be used as the record id so that the message broker can return this value and used in supabase as well as their id.

    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))

    file.save(filepath)

    record = {
      "id": record_id,
      "filename": file.filename,
      "filepath": filepath,
      "uploaded": True,
      "name": None,
      "lore": None,
      "weakness_filepath": None,
      "resistance_filepath": None,
      "moves_filepath": None,
    }

    supabase.table("pokemon-ocr").insert(record).execute()

    return jsonify({"record_id": record_id, "filename": file.filename, "filepath": filepath, "message": "File uploaded successfully"}), 200
  
  except Exception as e:
    return jsonify({"error": str(e)}), 500


# Here is the code to upload the image locally, then on the code below is the supabase configuration so once the image is uploaded locally,
# the metadata will be uploaded to supabase.

@app.route("/fetch_card_ids", methods=["GET"])

def get_card_id():
  try:
    card_id = fetch_card_ids()
    if not card_id:
      return jsonify({"error": "Failed to fetch cards"}), 404

    return jsonify(card_id), 200
  except Exception as e:
    return jsonify({"message": "Failed to fetch cards, please try again later.", "error": str(e)}), 500

@app.route("/get_card/<card_id>", methods=["GET"])

def get_card_info(card_id):
  try:
    card = get_card(card_id)
    if card:
      return jsonify(card), 200
    else:
      return jsonify({"error": "Card not found"}), 404
  except Exception as e:
    return jsonify({"message": "Simply, card not found.", "error": str(e)}), 500

@app.route("/get_card/<category>/<card_id>", methods=["GET"])

def card_image(card_id, category):
  try:
    if category not in ALLOWED_IMAGE_CATEGORIES:
      return jsonify({"error": "Invalid card image category"}), 400

    card = get_card_image(card_id, category)
    if not card:
      return jsonify({"error": "Card not found"}), 404

    image_path = resolve_image_path(card[0].get(category))
    if image_path is None:
      return jsonify({"error": "Image file not found"}), 404

    guessed_mime, _ = mimetypes.guess_type(str(image_path))
    return send_file(
      str(image_path),
      mimetype=guessed_mime or "application/octet-stream"
    )
  except Exception as e:
    return jsonify({"message": "Simply, card not found.", "error": str(e)}), 500

@app.route("/update_card/<card_id>", methods=["PUT"])

def update_card_info(card_id, data):
  try:
    response = supabase.table("pokemon-ocr").update(data).eq("id", card_id).execute()
    return jsonify(response.data), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
  
