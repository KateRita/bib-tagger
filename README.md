# bib-tagger
A project for parsing race photos and identifying bib numbers.

bib-tagger will read in a directory of photos and attempt to identify each visible bib number.

## pipeline
* face detection, body detection
* bib detection
* SWT on bib
* OCR on SWT results

## Dependencies

Probably could stand to clean these up a bit, do we need all of these?
*Scipy
*Numpy
*pytesseract
**tesseract-ocr
*Pillow

## Usage

Main.py will run through all of the file in a directory labeled 'photos'.
modify tests\test_bibtagger.py to test the entire pipeline on a single file.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

### ToDo

* Refining SWT & OCR based on smaller problem set of bib detection
* Create results hash map

## Credits

First version created by KateRita & Ryanr23

* Facial/Body Detection Reference: http://people.csail.mit.edu/talidekel/papers/RBNR.pdf
* SWT Reference: http://research.microsoft.com/pubs/149305/1509.pdf
* SWT Reference/Starting Point: https://github.com/mypetyak/StrokeWidthTransform/blob/master/swt.py
* OCR C++ Library: https://github.com/tesseract-ocr/tesseract
* OCR Python Wrapper: https://pypi.python.org/pypi/pytesseract
