from processors.coordinates import resistance_coordinates
from processors.crop import crop_image
import time
from common.database import scan, update_card
from common.config import POLL_INTERVAL

def get_resistance_data():

  print("Scanning for unprocessed images...")
  records = scan("resistance_filepath")

  if not records:
    print("No records found with resistance_filepath as None.")
    return None

  record = records[0]
  
  card_id = record["id"]
  filepath = record["filepath"]

  return card_id, filepath

def crop_resistance_image():

  record = get_resistance_data()

  if record is None:
    print("Failed to fetch resistance data.")
    return None

  card_id, filepath = record
  print("Found record with id: ", card_id)

  image_path = filepath

  output_path = f"resistance/{card_id}.png"

  cropped_image = crop_image(image_path, resistance_coordinates, output_path)
  print("Cropping resistance region: ", resistance_coordinates)
  print("Saving cropped image: ", output_path)

  try:
    update_card(card_id, {"resistance_filepath": output_path})
    print("Updated data store: weakness_filepath = ", output_path)
  except Exception as e:
    print("Failed to update, retrying...")
  
  return cropped_image

if __name__ == "__main__":

  while True:
    if get_resistance_data() is not None:
      try:
        crop_resistance_image()
      except Exception as e:
        print(f"An error occurred: {e}")
        
    time.sleep(POLL_INTERVAL)

# This will be the same as the other ocr services but for the resistance.