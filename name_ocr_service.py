from processors.coordinates import name_coordinates, trainer_card_name
from processors.ocr import ocr_image
import time
from common.database import scan, update_card
from common.config import POLL_INTERVAL

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

  print("Extracted: ", name_text)

  try:
    update_card(card_id, {"name": name_text})
    print("Updated data store: name = ", name_text)
  except Exception as e:
    print("Failed to update data, retrying...")

  return name_text

if __name__ == "__main__":

  while True:
    if get_name_data() is not None:
      try:
        scan_and_ocr_name()
      except Exception as e:
        print(f"An error occurred: {e}")
        
    time.sleep(POLL_INTERVAL)

