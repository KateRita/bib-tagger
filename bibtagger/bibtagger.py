import cv2

import bodydetector as bt

def findBibs(image):

    bodyboxes = bt.getbodyboxes(image);

    return 1234