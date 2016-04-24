import find_bibs as bf
import bibtagger as bt
import cv2
import numpy as np

class BibTaggerResult(object):
    def __init__(self):
        self.faces = 0
        self.bibs = 0
        self.swt  = 0
        self.bib_numbers = []


    def __str__(self):
        return "Result: {0} faces, {1} bibs, {2} SWT, {3} bib numbers: ({4})".format(self.faces,self.bibs,self.swt, len(self.bib_numbers), self.bib_numbers)
