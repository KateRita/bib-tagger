import unittest
import os
import cv2

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

    def test_findBibs(self):
        #image = cv2.imread(os.path.join(self.photodir,"Frosty5k","1.jpg"))
        #image = cv2.imread(os.path.join(self.photodir,"abba.png"))
        image = cv2.imread(os.path.join(self.photodir,"GloryDays","2.jpg"))

        #bd.getbodyboxes(image)
        bt.findBibs(image,os.path.join(self.photooutdir,"test_one_image"))

    #def test_nullImage(self):
        #self.assertEqual('foo'.upper(), 'FOO')
        #self.assertTrue('FOO'.isupper())
        #bt.findBibs(None,None)

if __name__ == '__main__':
    unittest.main()