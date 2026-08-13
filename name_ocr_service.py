from processors.coordinates import name_coordinates
from processors.ocr import ocr_image
import time
from common.database import scan, update_card
from common.config import POLL_INTERVAL

def get_name_data():
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

  image_path = filepath

  name_text = ocr_image(image_path, name_coordinates)

  update_card(card_id, {"name": name_text})

  return name_text

if __name__ == "__main__":

  while True:
    if get_name_data() is not None:
      try:
        scan_and_ocr_name()
      except Exception as e:
        print(f"An error occurred: {e}")
        
    time.sleep(POLL_INTERVAL)

