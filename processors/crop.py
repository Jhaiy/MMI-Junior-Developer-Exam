from PIL import Image

def crop_image(image_path, coordinates, output_path):

  selected_image = Image.open(image_path)

  image_region = selected_image.crop(coordinates)

  image_region.save(output_path)

  return image_region
