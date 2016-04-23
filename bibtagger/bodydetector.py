import cv2
import os
import numpy as np

def getbodyboxes(image):

    faces = findfaces(image)

    bodyrectangles = findbodies(image,faces)

    #drawboxes(image,bodies)

    return bodyrectangles


def findfaces(image):

    thisdirectory = os.path.dirname(os.path.realpath(__file__))

    haarcascadeFolder = os.path.join(thisdirectory,"haarcascades")
    cascPath = os.path.join(haarcascadeFolder, "haarcascade_frontalface_default.xml")

    #cascPath = os.path.join(haarcascadeFolder, "haarcascade_upperbody.xml")
    #cascPath = os.path.join(haarcascadeFolder, "haarcascade_fullbody.xml")
    #cascPath = os.path.join(haarcascadeFolder, "haarcascade_russian_plate_number.xml")

    print cascPath
    print os.path.isfile(cascPath)

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    print "Found {0} faces!".format(len(faces))

    #return list of boxes
    return faces

def findbodies(image, faces):

    bodies = np.zeros_like(faces)
    bodiesindex = 0

    #for each face, draw a body
    for (x, y, facewidth, faceheight) in faces:
        #3*faceheight, 7/3 * facewidth, .5*faceheight below the face.
        bodyheight = 3 * faceheight
        bodywidth = 7/3 * facewidth
        y_body = y + faceheight + .5 * faceheight
        x_body = x + .5 * facewidth - .5 * bodywidth

        bodies[bodiesindex] = (x_body,y_body, bodywidth, bodyheight)
        bodiesindex = bodiesindex + 1

        #cv2.rectangle(image, (x_body, y_body), (x_body+bodywidth, y_body+bodyheight), (0, 255, 0), 2)

    return bodies

def drawboxes(image, faces):

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Faces found", image)
    cv2.waitKey(0)