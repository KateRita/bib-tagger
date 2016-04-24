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
        image = cv2.imread(os.path.join(self.photodir,"GloryDays","4.jpg"))

        #bd.getbodyboxes(image)
        bt.findBibs(image,os.path.join(self.photooutdir,"test_one_image"))

    def test_getsquare(self):
        corners = [(320, 353), (259, 359), (255, 308), (318, 303)]
        print corners
        square = bt.getsquare(corners)

        print square

        assert (square == (255,303,56,65))

    def test_getsquare_empty(self):
        corners = [(0, 0), (0, 0), (0, 0), (0, 0)]

        square = bt.getsquare(corners)
        assert (square == (0,0,0,0))

    #def test_nullImage(self):
        #self.assertEqual('foo'.upper(), 'FOO')
        #self.assertTrue('FOO'.isupper())
        #bt.findBibs(None,None)

if __name__ == '__main__':
    unittest.main()