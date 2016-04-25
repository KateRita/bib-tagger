import cv2
import os
import numpy as np
import bodydetector as bt
import find_bibs as bf
from bib import Bib
from bibtaggerresult import BibTaggerResult

from swt import SWTScrubber
import ocr
import re

def findBibs(image,outdir):

    #prep out dir
    writefiles = True
    if(outdir == None):
        writefiles = False
    else:
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    bodyboxes = bt.getbodyboxes(image)

    print "Found {} bodies!".format(len(bodyboxes))

    #draw bodyboxes on image, and write out
    imagecopy = np.copy(image)
    drawboxes(imagecopy,bodyboxes)
    if(writefiles):
        cv2.imwrite(os.path.join(outdir,"0_0bodyboxes.jpg"), imagecopy)

    # Creates a list of Bibs
    bibs = [ Bib(image, bodybox) for bodybox in bodyboxes ]

    # Write out subimages, with bibs outlined
    if(writefiles):
        for i, bib in enumerate(bibs):
            cv2.imwrite(os.path.join(outdir,"{}_1subimage.jpg".format(i)), bib.body_image())
            cv2.imwrite(os.path.join(outdir,"{}_1subimage_withbib.jpg".format(i)), bib.body_image_with_bib())


    swtsuccesses = 0
    for i, bib in enumerate(bibs):

        SWTbib = None
        try :
            bibimage = bib.smallest_subimage_containing_bib()

            height, width, depth = bibimage.shape
            best_width=376.0
            scale = best_width / width

            bibimage = cv2.resize(bibimage, None, fx=scale, fy=scale)
            bib.number = run_swt_and_ocr(bibimage, i, "normal", writefiles, outdir)

            if not bib.has_bib_number():
                bibimage_inverted = (255-bibimage)
                bib.number = run_swt_and_ocr(bibimage_inverted, i, "inverted", writefiles, outdir)

            if not bib.has_bib_number():
                bibimage = cv2.cvtColor(bibimage_inverted, cv2.COLOR_BGR2GRAY);
                bibimage = cv2.GaussianBlur(bibimage,(5,5),0)
                bibimage = cv2.equalizeHist(bibimage)
                ret,bibimage = cv2.threshold(bibimage, 75, 255, cv2.THRESH_BINARY);
                bibimage = cv2.cvtColor(bibimage, cv2.COLOR_GRAY2BGR);
                bibimage = cv2.fastNlMeansDenoisingColored(bibimage,None,10,10,7,21)
                bib.number = run_swt_and_ocr(bibimage, i, "inverted_and_normalized", writefiles, outdir)

            #found some words in this image
            if (SWTbib is not None):
                swtsuccesses += 1

        except Bib:
            print "SWT failed"

    result = BibTaggerResult()
    result.faces = len(bodyboxes)
    result.bibs = sum(1 for bib in bibs if bib.bib_found)
    result.swt = swtsuccesses
    result.bib_numbers = [ bib.number for bib in bibs if bib.has_bib_number() ]

    print result

    return result


def run_swt_and_ocr(image, i, name, writefiles, outdir):
    bib_number = None

    if(writefiles):
        cv2.imwrite(os.path.join(outdir,"{}_2bibimage_{}.jpg".format(i, name)),image)

    SWTbib = SWTScrubber.scrub(image)
    if(writefiles and SWTbib is not None):
        SWTpath = os.path.join(outdir,"{}_3SWTimage_{}.jpg".format(i, name))
        cv2.imwrite(SWTpath, (255-(255*SWTbib)))
        bib_number = ocr.getOcr(SWTpath)
        print bib_number
        bib_number = re.sub("[^0-9]", "", bib_number)

    return bib_number

def getSubImage(image,rectangle):
    #in: image, rectangle(x,y,width,height)
    #out: subimage

    (x,y,w,h) = rectangle

    return image[y:y+h,x:x+w,:]

def drawboxes(image, boxes, color = (0,255,0)):

    # Draw a rectangle around the faces
    for (x, y, w, h) in boxes:
        cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
