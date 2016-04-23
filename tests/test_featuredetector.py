import unittest
import os
import cv2
import numpy as np

import bibtagger.featuredetector as fd

class testfeaturedetector(unittest.TestCase):

    photodir = ""

    #called before every test
    def setUp(self):
        #self.widget = Widget('The widget')
        self.basedir = os.path.dirname(os.path.abspath(os.curdir))
        self.photodir = os.path.join(self.basedir,"photos")
        self.photooutdir = os.path.join(self.basedir, "photos-out")
        print "setup"

    def tearDown(self):
        #self.widget.dispose()
        print "teardown"

    def test_featuredetector(self):

        print self.photodir

        #read in images
        images = []
        for i in np.arange(1,7):
            images.append(cv2.imread(os.path.join(self.photodir,"Frosty5k","{}.jpg".format(i))))

        #read in bib
        bib = cv2.imread(os.path.join(self.photodir,"Frosty5k","bib.jpg"))

        for i in np.arange(1,7):
            image = images[i-1]
            bib_kp, image_kp, matches = fd.findMatchesBetweenImages(bib, image)
            output = fd.drawMatches(bib, bib_kp, image, image_kp, matches)

            ftoutdir = os.path.join(self.photooutdir,"features")
            print "Writing images to folder {}".format(ftoutdir)

            if not os.path.exists(ftoutdir):
                os.makedirs(ftoutdir)

            cv2.imwrite(os.path.join(ftoutdir,"{}matches.jpg".format(i)), output)

if __name__ == '__main__':
    unittest.main()