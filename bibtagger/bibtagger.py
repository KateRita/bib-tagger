import cv2
import os
import numpy as np
import bodydetector as bt
import find_bibs as bf

from sys import maxint
from swt import SWTScrubber

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

    # Creates a list of (sub_image, bib, bodybox) tuples
    bibs = [(getSubImage(image,bodybox), bf.find_bib(getSubImage(image,bodybox)), bodybox)
        for bodybox in bodyboxes]

    # Write out subimages, with bibs outlined
    for i in np.arange(len(bibs)):
        if(writefiles):
            cv2.drawContours(bibs[i][0], [bibs[i][1]], -1, (0,0,255), 2)
            cv2.imwrite(os.path.join(outdir,"{}_1subimage.jpg".format(i)), bibs[i][0])


    # Return the bib corners back translated to the input image coordinate space
    bibcorners = [subimage_to_image(bib[2], bib[1]) for bib in bibs]

    bibsFound = 0
    SWTSuccess = 0

    for i in np.arange(len(bibs)):
        bibcorner = bibcorners[i]
        subimage = bibs[i][0]

        bibsquare = getsquare(bibcorner)

        if bibsquare[2] == 0 and bibsquare[3]==0:
            #if it's null, we want original body image
            bibimage = subimage
        else:
            bibimage = getSubImage(image,bibsquare)
            bibsFound += 1

        SWTbib = None
        try :
            SWTbib = SWTScrubber.scrub(bibimage)

            if(writefiles):
                cv2.imwrite(os.path.join(outdir,"{}_2bibimage.jpg".format(i)),bibimage)

            if(writefiles and SWTbib != None):
                SWTpath = os.path.join(outdir,"{}_3SWTimage.jpg".format(i))
                cv2.imwrite(SWTpath,  SWTbib * 255)
                SWTSuccess +=1

        except ValueError:
            print "SWT failed"


    print "Result: {0} faces, {1} bibs, {2} SWT".format(len(bodyboxes),bibsFound,SWTSuccess)

    return 1234

def getsquare(fourcorners):
    minx = fourcorners[0][0]
    miny = fourcorners[0][1]
    maxx = minx
    maxy = miny

    for (x,y) in fourcorners:
        if x<minx : minx = x
        if x>maxx : maxx = x
        if y<miny : miny = y
        if y>maxy : maxy = y

    return (minx, miny, maxy- miny, maxx - minx)


def subimage_to_image(sub_image_box, contour):
    x_delta = sub_image_box[0]
    y_delta = sub_image_box[1]
    return [(pt[0][0] + x_delta, pt[0][1] + y_delta) for pt in contour]

def getSubImage(image,rectangle):
    #in: image, rectangle(x,y,width,height)
    #out: subimage

    (x,y,w,h) = rectangle

    return image[y:y+h,x:x+w,:]

def drawboxes(image, boxes):

    # Draw a rectangle around the faces
    for (x, y, w, h) in boxes:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
