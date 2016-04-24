import cv2
import os
import numpy as np
import bodydetector as bt
import find_bibs as bf

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

    # Creates a list of (sub_image, bib, bodybox) tuples
    bibs = [(getSubImage(image,bodybox), bf.find_bib(getSubImage(image,bodybox)), bodybox)
        for bodybox in bodyboxes]

    # Write out subimages
    for i in np.arange(len(bibs)):
        if(writefiles):
            cv2.imwrite(os.path.join(outdir,"subimage{}.jpg".format(i)), bibs[i][0])
            cv2.drawContours(bibs[i][0], [bibs[i][1]], -1, (0,0,255), 2)
            cv2.imwrite(os.path.join(outdir,"subimage_withbib{}.jpg".format(i)), bibs[i][0])

    # Return the bib corners back translated to the input image coordinate space
    return [subimage_to_image(bib[2], bib[1]) for bib in bibs]

def subimage_to_image(sub_image_box, contour):
    x_delta = sub_image_box[0]
    y_delta = sub_image_box[1]
    return [(pt[0][0] + x_delta, pt[0][1] + y_delta) for pt in contour]

def getSubImage(image,rectangle):
    #in: image, rectangle(x,y,width,height)
    #out: subimage

    (x,y,w,h) = rectangle

    return image[y:y+h,x:x+w,:]

def drawboxes(image, boxes, color = (0,255,0)):

    # Draw a rectangle around the faces
    for (x, y, w, h) in boxes:
        cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)
