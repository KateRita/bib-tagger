from PIL import Image

from pytesseract import image_to_string

def getOcr(filename):
    print image_to_string(Image.open(filename))
