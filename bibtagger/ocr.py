from PIL import Image

from pytesseract import image_to_string

def getOcr(filename):
    return image_to_string(Image.open(filename))