from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import pytesseract

def ocr_image(image_path, coordinates):

  img = Image.open(image_path).convert("L")
  img = img.crop(coordinates)

  img = ImageOps.autocontrast(img)
  img = img.resize((img.width * 4, img.height * 4))
  img = img.filter(ImageFilter.MedianFilter(3))
  img = img.filter(ImageFilter.SHARPEN)

  img.save("debug.png")

  text = pytesseract.image_to_string(img)
  return text.strip()

# I had a little trouble with the extraction of text from the image, so I had to use some image processing techniques
# to enhance the image before passing it to pytesseract for OCR. Surprise surprise, it worked. Kudos to GeeksForGeeks it's where I got the idea.