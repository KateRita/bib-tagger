import cv2
import os
import numpy as np
import bodydetector as bt
import find_bibs as bf
from bib import Bib

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

    SWTSuccess = 0

    for i, bib in enumerate(bibs):

        SWTbib = None
        try :
            bibimage = bib.smallest_subimage_containing_bib()

            height, width, depth = bibimage.shape
            best_width=256.0
            scale = best_width / width
            bibimage = cv2.resize(bibimage, None, fx=scale, fy=scale)
            #bibimage = cv2.cvtColor(bibimage, cv2.COLOR_BGR2GRAY);
            #blurred = cv2.GaussianBlur(bibimage,(5,5),0)
            #bibimage = cv2.equalizeHist(bibimage)
            #ret,bibimage = cv2.threshold(blurred, 190, 255, cv2.THRESH_BINARY);
            #bibimage = cv2.cvtColor(bibimage, cv2.COLOR_GRAY2BGR);
            #bibimage = cv2.fastNlMeansDenoisingColored(bibimage,None,10,10,7,21)
            if(writefiles):
                cv2.imwrite(os.path.join(outdir,"{}_2bibimage.jpg".format(i)),bibimage)

            SWTbib = SWTScrubber.scrub(bibimage)
            if(writefiles and SWTbib is not None):
                SWTpath = os.path.join(outdir,"{}_3SWTimage.jpg".format(i))
                cv2.imwrite(SWTpath, 255*SWTbib)
                bib.number = ocr.getOcr(SWTpath)

            if not bib.has_bib_number():
                bibimage_inverted = (255-bibimage)
                if(writefiles):
                    cv2.imwrite(os.path.join(outdir,"{}_2bibimage_inverted.jpg".format(i)),bibimage_inverted)

                SWTbib = SWTScrubber.scrub(bibimage_inverted)
                if(writefiles and SWTbib is not None):
                    SWTpath = os.path.join(outdir,"{}_3SWTimage_inverted.jpg".format(i))
                    cv2.imwrite(SWTpath, 255*SWTbib)
                    bib.number = ocr.getOcr(SWTpath)

            #found some words in this image
            if (SWTbib is not None):
                SWTSuccess += 1

        except Bib:
            print "SWT failed"

    bibs_found = sum(1 for bib in bibs if bib.bib_found)
    bib_numbers_found = sum(1 for bib in bibs if bib.has_bib_number())
    print "Result: {0} faces, {1} bibs, {2} SWT, {3} bib numbers".format(len(bodyboxes),bibs_found,SWTSuccess, bib_numbers_found)
    return [ bib.number for bib in bibs if bib.has_bib_number() ]

def getSubImage(image,rectangle):
    #in: image, rectangle(x,y,width,height)
    #out: subimage

    (x,y,w,h) = rectangle

    return image[y:y+h,x:x+w,:]

def drawboxes(image, boxes, color = (0,255,0)):

    # Draw a rectangle around the faces
    for (x, y, w, h) in boxes:
        cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
