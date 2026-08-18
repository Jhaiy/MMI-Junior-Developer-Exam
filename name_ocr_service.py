from processors.coordinates import name_coordinates, trainer_card_name
from processors.ocr import ocr_image
import time
from common.database import scan, update_card
from common.config import POLL_INTERVAL
import re

def clean_name(raw_name):
  if raw_name is None:
    return None

  # I'll use a regex pattern to recognize any EX because the extractor is returning some weird stuff.
  cleaned = raw_name.strip()
  cleaned = re.sub(r"(?i)\s*@\s*(x)?\s*[,.;:!?]*\s*$", " EX", cleaned)
  cleaned = re.sub(r"(?i)\s+ex\s*$", " EX", cleaned)
  cleaned = re.sub(r"(?i)\s*-\s*ex\s*$", " EX", cleaned)
  cleaned = re.sub(r"(?i)[@#*_~]+", "", cleaned)
  cleaned = re.sub(r"[\.,!?;:]+$", "", cleaned)
  cleaned = re.sub(r"(?i)\bex\b", "EX", cleaned)
  cleaned = re.sub(r"\s+", " ", cleaned).strip()

  if cleaned.lower().endswith("ex") is False and re.search(r"(?i)\bEX\b", cleaned):
    cleaned = re.sub(r"(?i)\s*EX\s*$", " EX", cleaned)

  return cleaned or None

def get_name_data():

  print("Scanning for unprocessed images...")
  records = scan("name")

  if not records:
    print("No records found with name as None.")
    return None

  record = records[0]
  
  card_id = record["id"]
  filepath = record["filepath"]
  return card_id, filepath

def scan_and_ocr_name():
  
  record = get_name_data()

  if record is None:
    print("Failed to fetch name data.")
    return None

  card_id, filepath = record

  print("Found record with id: ", card_id)

  image_path = filepath

  print("Cropping name region ", name_coordinates)
  name_text = ocr_image(image_path, name_coordinates)

  print("Extracting text with OCR...")
  if name_text is None or name_text.strip() == "":
    name_text = ocr_image(image_path, trainer_card_name)

  cleaned_name = clean_name(name_text)

  print("Extracted: ", cleaned_name)

  try:
    update_card(card_id, {"name": cleaned_name})
    print("Updated data store: name = ", cleaned_name)
  except Exception as e:
    print("Failed to update data, retrying...")

  return cleaned_name

if __name__ == "__main__":

  while True:
    if get_name_data() is not None:
      try:
        scan_and_ocr_name()
      except Exception as e:
        print(f"An error occurred: {e}")
        
    time.sleep(POLL_INTERVAL)

