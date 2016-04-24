import unittest
import os
import cv2

#from directory.file import class
from bibtagger.swt import SWTScrubber

class test_swt(unittest.TestCase):

    photodir = ""

    #called before every test
    def setUp(self):
        #self.widget = Widget('The widget')
        self.basedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.photodir = os.path.join(self.basedir,"photos")
        self.photooutdir = os.path.join(self.basedir, "photos-out")
        print "setup"

    def tearDown(self):
        #self.widget.dispose()
        print "teardown"

    def test_swt(self):
        cv2.IMREAD_GRAYSCALE
        image = cv2.imread(os.path.join(self.photodir,"GloryDays","bib-sample.jpg"),cv2.IMREAD_GRAYSCALE)

        SWTImage = SWTScrubber.scrub(image)

        cv2.imwrite(os.path.join(self.photooutdir,"SWTImage.jpg"),SWTImage*255)



if __name__ == '__main__':
    unittest.main()