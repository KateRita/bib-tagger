import collections
import cv2
import os
import numpy as np
import bodydetector as bt
import find_bibs as bf
from bib import Bib

from sys import maxint
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

    for i, bib in enumerate(bibs):

        SWTbib = None
        try :
            bibimage = bib.smallest_subimage_containing_bib()
            if(writefiles):
                cv2.imwrite(os.path.join(outdir,"{}_2bibimage.jpg".format(i)),bibimage)

            SWTbib = SWTScrubber.scrub(bibimage)
            if(writefiles and SWTbib != None):
                SWTpath = os.path.join(outdir,"{}_3SWTimage.jpg".format(i))
                cv2.imwrite(SWTpath,  SWTbib * 255)
                bib.number = ocr.getOcr(SWTpath)

        except ValueError:
            print "SWT failed"

    bibs_found = sum(1 for bib in bibs if bib.bib_found)
    SWTSuccess = sum(1 for bib in bibs if bib.number != None and bib.number != '')
    print "Result: {0} faces, {1} bibs, {2} SWT".format(len(bodyboxes),bibs_found,SWTSuccess)

    return [ bib.number for bib in bibs if bib.number != None and bib.number != '' ]

def getSubImage(image,rectangle):
    #in: image, rectangle(x,y,width,height)
    #out: subimage

    (x,y,w,h) = rectangle

    return image[y:y+h,x:x+w,:]

def drawboxes(image, boxes, color = (0,255,0)):

    # Draw a rectangle around the faces
    for (x, y, w, h) in boxes:
        cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
