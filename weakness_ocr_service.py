from processors.coordinates import weakness_coordinates
from processors.crop import crop_image
from common.database import scan, update_card
import time
from common.config import POLL_INTERVAL

def get_weakness_data():

  print("Scanning for unprocessed images...")
  records = scan("weakness_filepath")

  if not records:
    print("No records found with weakness_filepath as None.")
    return None

  record = records[0]
  
  card_id = record["id"]
  filepath = record["filepath"]

  return card_id, filepath

def crop_weakness_image():
  
  record = get_weakness_data()

  if record is None:
    print("Failed to fetch weakness data.")
    return None

  card_id, filepath = record
  print("Found record with id: ", card_id)

  image_path = filepath
  print("Cropping image: ", image_path)

  output_path = f"weakness/{card_id}.png"

  cropped_image = crop_image(image_path, weakness_coordinates, output_path)
  print("Cropping weakness region: ", weakness_coordinates)
  print("Saving cropped image: ", output_path)

  try:
    update_card(card_id, {"weakness_filepath": output_path})
    print("Updated data store: weakness_filepath = ", output_path)
  except Exception as e:
    print("Failed to update, retrying...")

  return cropped_image

if __name__ == "__main__":

  while True:
    if get_weakness_data() is not None:
      try:
        crop_weakness_image()
      except Exception as e:
        print(f"An error occurred: {e}")
        
    time.sleep(POLL_INTERVAL)

# Again, same as the other ones but for weakness.