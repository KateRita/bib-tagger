# bib-tagger
A project for parsing race photos and identifying bib numbers.

# pipeline
photo
(face detection, body boxes)
photo, body rectangles
(bib finder) = (specific bib feature detection), (generic bib feature detection + edge detection)
bib 4 corners
(perspective correction)
bib images
(OCR)
numbers & letters
(refine OCR)
bib #s

#Future
time & bib correlation
ID a runner, find them again
