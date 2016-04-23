import cv2
import os
import numpy as np
import bodydetector as bt

def findBibs(image,outdir):

    #prep out dir
    writefiles = True
    if(outdir == None):
        writefiles = False
    else:
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    bodyboxes = bt.getbodyboxes(image)

    print "found {} bodies".format(len(bodyboxes))

    #draw bodyboxes on image, and write out
    imagecopy = np.copy(image)
    drawboxes(imagecopy,bodyboxes)
    if(writefiles):
        cv2.imwrite(os.path.join(outdir,"bodyboxes.jpg"), imagecopy)

    for i in np.arange(len(bodyboxes)):
        #get subimage
        subimage = getSubImage(image,bodyboxes[i])

        #write out subimage
        if(writefiles):
            cv2.imwrite(os.path.join(outdir,"subimage{}.jpg".format(i)), subimage)

    return 1234

def getSubImage(image,rectangle):
    #in: image, rectangle(x,y,width,height)
    #out: subimage

    (x,y,w,h) = rectangle

    return image[y:y+h,x:x+w,:]

def drawboxes(image, boxes):

    # Draw a rectangle around the faces
    for (x, y, w, h) in boxes:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)