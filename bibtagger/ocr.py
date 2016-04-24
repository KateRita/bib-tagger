from PIL import Image

from pytesseract import image_to_string

#tesseract command line options: https://tesseract-ocr.googlecode.com/svn/trunk/doc/tesseract.1.html
#image_to_string implementation/syntax: 
def getOcr(filename):
    #,config='-psm 10') option for single digit recognition
    #return image_to_string(Image.open(filename),config="-psm 6") #5
    #return image_to_string(Image.open(filename)) #3
    #return image_to_string(Image.open(filename),config="-psm 7") #5
    return image_to_string(Image.open(filename),config="-psm 7 digits") #4

