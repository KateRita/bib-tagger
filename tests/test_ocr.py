import unittest
import os
import bibtagger.ocr as ocr

import bibtagger.bibtagger as bt

class testbibtagger(unittest.TestCase):

    photodir = ""

    #called before every test
    def setUp(self):
        #self.widget = Widget('The widget')
        self.basedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.photodir = os.path.join(self.basedir,"photos")
        self.photooutdir = os.path.join(self.basedir, "photos-out")
        print "Test Setup"

    def tearDown(self):
        #self.widget.dispose()
        print "Test Teardown"

    def test_testocr(self):
        inputpath = os.path.join(self.photooutdir,"test_one_image","1_3SWTimage.jpg")
        print "OCR RESULT", ocr.getOcr(inputpath)


if __name__ == '__main__':
    unittest.main()