from processors.coordinates import moves_coordinates
from processors.crop import crop_image
import time
from common.database import scan, update_card
from common.config import POLL_INTERVAL

def get_moves_data():

  print("Scanning for unprocessed images...")
  records = scan("moves_filepath")

  if not records:
    print("No records found with moves_filepath as None.")
    return None

  record = records[0]
  
  card_id = record["id"]
  filepath = record["filepath"]

  return card_id, filepath

def crop_moves_image():

  record = get_moves_data()

  if record is None:
    print("Failed to fetch moves data.")
    return None

  card_id, filepath = record
  print("Found record with id: ", card_id)

  image_path = filepath
  print("Cropping image: ", image_path)

  output_path = f"moves/{card_id}.png"

  cropped_image = crop_image(image_path, moves_coordinates, output_path)
  print("Cropping moves region: ", moves_coordinates)
  print("Saving cropped image: ", output_path)

  try:
    update_card(card_id, {"moves_filepath": output_path})
    print("Updated data store: moves_filepath = ", output_path)
  except Exception as e:
    print("Failed to update, retrying...")

  return cropped_image

if __name__ == "__main__":

  while True:
    if get_moves_data() is not None:
      try:
        crop_moves_image()
      except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(POLL_INTERVAL)

# So the process here is to first scan the database for any records that have moves_filepath as NULL.
# If there are any records found, it will then pass that data onto the crop_moves_image function which will then read the filepath of the image
# Then after reading the filepath, it will crop the image based on the coordinates provided in the moves_coordinates variable frm the coordinates.py file.
# After cropping the image and saving it locally, it will then use the update_card function to update the moves_filepath column in the database with the new cropped image path.
