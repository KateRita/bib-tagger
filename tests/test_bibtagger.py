import unittest
import os
import cv2
import bibtagger.bodydetector as bd

import bibtagger.bibtagger as bt

class testbibtagger(unittest.TestCase):

    photodir = ""

    #called before every test
    def setUp(self):
        #self.widget = Widget('The widget')
        self.photodir = os.path.abspath(os.curdir)
        self.photodir = os.path.join(self.photodir,"..","photos")
        print "setup"

    def tearDown(self):
        #self.widget.dispose()
        print "teardown"

    def test_bodydetector(self):

        print self.photodir

        #image = cv2.imread(os.path.join(self.photodir,"Frosty5k","1.jpg"))
        #image = cv2.imread(os.path.join(self.photodir,"abba.png"))
        image = cv2.imread(os.path.join(self.photodir,"GloryDays","1.jpg"))

        print image.shape
        bd.getbodyboxes(image)

    def test_nullImage(self):
        #self.assertEqual('foo'.upper(), 'FOO')
        #self.assertTrue('FOO'.isupper())
        bt.findBibs(None)

if __name__ == '__main__':
    unittest.main()