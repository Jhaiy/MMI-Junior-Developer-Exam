from processors.coordinates import lore_coordinates
from processors.ocr import ocr_image
import time
from common.database import scan, update_card
from common.config import POLL_INTERVAL

def get_lore_data():
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

  image_path = filepath

  lore_text = ocr_image(image_path, lore_coordinates)

  update_card(card_id, {"lore": lore_text})

  return lore_text

if __name__ == "__main__":

  while True:
    if get_lore_data() is not None:
      try:
        scan_and_ocr_lore()
      except Exception as e:
        print(f"An error occurred: {e}")
        
    time.sleep(POLL_INTERVAL)

# This is the same as the others more like the name_ocr_service.py, but this one is for the lore.