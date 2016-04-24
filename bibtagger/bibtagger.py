import cv2
import os
import numpy as np
import bodydetector as bt
import find_bibs as bf
from bib import Bib
from bibtaggerresult import BibTaggerResult

from swt import SWTScrubber
import ocr

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
            if(writefiles):
                cv2.imwrite(os.path.join(outdir,"{}_2bibimage.jpg".format(i)),bibimage)

            SWTbib = SWTScrubber.scrub(bibimage)
            if(writefiles and SWTbib is not None):
                SWTpath = os.path.join(outdir,"{}_3SWTimage.jpg".format(i))
                cv2.imwrite(SWTpath,  SWTbib * 255)
                bib.number = ocr.getOcr(SWTpath)

            #found some words in this image
            if (SWTbib is not None):
                swtsuccesses += 1

        except ValueError:
            print "SWT failed"

    result = BibTaggerResult()
    result.faces = len(bodyboxes)
    result.bibs = sum(1 for bib in bibs if bib.bib_found)
    result.swt = swtsuccesses
    result.bib_numbers = [ bib.number for bib in bibs if bib.number != None and bib.number != '' ]

    print result

    return result

def getSubImage(image,rectangle):
    #in: image, rectangle(x,y,width,height)
    #out: subimage

    (x,y,w,h) = rectangle

    return image[y:y+h,x:x+w,:]

def drawboxes(image, boxes, color = (0,255,0)):

    # Draw a rectangle around the faces
    for (x, y, w, h) in boxes:
        cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
