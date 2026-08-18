from processors.coordinates import lore_coordinates
from processors.ocr import ocr_image
import time
from common.database import scan, update_card
from common.config import POLL_INTERVAL
import re

def clean_lore(raw_lore):
  if raw_lore is None:
    return None

  cleaned = raw_lore.strip()
  cleaned = cleaned.replace("’", "'").replace("`", "'")
  cleaned = re.sub(r"\s+", " ", cleaned)
  cleaned = re.sub(r"^[\s\.\-–—:;,_]+", "", cleaned)
  cleaned = re.sub(r"^(?:\d+\s+|SS\s*>\s*)", "", cleaned, flags=re.IGNORECASE)
  cleaned = re.sub(r"(?i)\s*@\s*x\s*", " EX ", cleaned)
  cleaned = re.sub(r"(?i)\s*@\s*ex\s*", " EX ", cleaned)
  cleaned = re.sub(r"(?i)\bEX\b", "EX", cleaned)
  cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()

  return cleaned or None


def get_lore_data():

  print("Scanning for unprocessed images...")
  records = scan("lore")

  if not records:
    print("No records found with lore as None.")
    return None

  record = records[0]
  
  card_id = record["id"]
  filepath = record["filepath"]

  return card_id, filepath

def scan_and_ocr_lore():
  
  record = get_lore_data()

  if record is None:
    print("Failed to fetch lore data.")
    return None

  card_id, filepath = record
  print("Found record with id: ", card_id)

  image_path = filepath

  print("Cropping lore region: ", lore_coordinates)

  lore_text = ocr_image(image_path, lore_coordinates)
  print("Extracting lore with OCR...")

  cleaned_lore = clean_lore(lore_text)
  print("Extracted: ", cleaned_lore)

  try:
    update_card(card_id, {"lore": cleaned_lore})
    print("Updated data store: lore = ", cleaned_lore)
  except Exception as e:
    print("Failed to update, retrying...")

  return cleaned_lore

if __name__ == "__main__":

  while True:
    if get_lore_data() is not None:
      try:
        scan_and_ocr_lore()
      except Exception as e:
        print(f"An error occurred: {e}")
        
    time.sleep(POLL_INTERVAL)

# This is the same as the others more like the name_ocr_service.py, but this one is for the lore.