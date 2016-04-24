import cv2
import os
import numpy as np

def getbodyboxes(image):
    #in: numpy image
    #out: list [(x,y,width,height)]

    faces = findfaces(image)

    bodyrectangles = findbodies(image,faces)

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
    height, width, depth = image.shape
    scale = 1
    if (width > 1024):
        scale = 1024.0/width
        image = cv2.resize(image, None, fx=scale, fy=scale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(30, 30),
    )

    print "Found {0} faces!".format(len(faces))

    return [scale_rect(face, 1/scale) for face in faces]

def scale_rect(rect, scale):
    return [int(value*scale) for value in rect]

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
