import unittest

import bibtagger.bibtagger as bt

class testbibtagger(unittest.TestCase):

    #called before every test
    def setUp(self):
        #self.widget = Widget('The widget')
        print "setup"

    def tearDown(self):
        #self.widget.dispose()
        print "teardown"

    def test_nullImage(self):
        #self.assertEqual('foo'.upper(), 'FOO')
        #self.assertTrue('FOO'.isupper())
        bt.findBibs(None)

if __name__ == '__main__':
    unittest.main()