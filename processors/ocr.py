from PIL import Image, ImageFilter, ImageEnhance
import pytesseract

def ocr_image(image_path, coordinates):

  selected_image = Image.open(image_path)

  convert_image = selected_image.convert("L")

  convert_image = convert_image.filter(ImageFilter.SHARPEN)

  enhancer = ImageEnhance.Contrast(convert_image)

  convert_image = enhancer.enhance(2)

  image_region = convert_image.crop(coordinates)

  extracted_text = pytesseract.image_to_string(image_region)

  return extracted_text

# I had a little trouble with the extraction of text from the image, so I had to use some image processing techniques
# to enhance the image before passing it to pytesseract for OCR. Surprise surprise, it worked. Kudos to GeeksForGeeks it's where I got the idea.