import cv2
import numpy as np

#
# Takes an input image which is assumed to only have one bib and returns the
# four corners of the bib in the form of an opencv contour (vector of points,
# i.e vector((x1,y1),(x2,y2),(x3,y3)(x4,y4)) )
#
def find_bib(image):
  edges = cv2.Canny(image,175,200)
  #cv2.imwrite("edges.jpg", edges)

  contours,hierarchy = find_contours(edges)

  #potential_contours = [c for c in contours if cv2.contourArea(cv2.approxPolyDP(c,0.02*cv2.arcLength(c,True),True)) > 300]
  #cv2.drawContours(image,potential_contours,-1,(0,255,0), 2)

  rectangles = get_rectangles(contours)

  potential_bibs = [rect for rect in rectangles if is_potential_bib(rect)]

  #cv2.drawContours(image,potential_bibs,-1,(0,0,255), 2)
  #cv2.imwrite("with_potentials.jpg", image)

  return potential_bibs[0] if len(potential_bibs) > 0 else np.array([[(0,0)],[(0,0)],[(0,0)],[(0,0)]])

#
# Checks that the size and aspect ratio of the contour is appropriate for a bib.
#
def is_potential_bib(rect):
  x,y,w,h = cv2.boundingRect(rect)
  aspect_ratio = float(w) / float(h)
  return (cv2.contourArea(rect) > 500 and
          aspect_ratio > 1 and
          aspect_ratio < 2)

def find_bibs(image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
  binary = cv2.GaussianBlur(gray,(5,5),0)
  ret,binary = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU);
  #binary = cv2.adaptiveThreshold(binary, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
  #ret,binary = cv2.threshold(binary, 190, 255, cv2.THRESH_BINARY);

  #lapl = cv2.Laplacian(image,cv2.CV_64F)
  #gray = cv2.cvtColor(lapl, cv2.COLOR_BGR2GRAY);
  #blurred = cv2.GaussianBlur(lapl,(5,5),0)
  #ret,binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU);
  #cv2.imwrite("lapl.jpg", lapl)

  edges = cv2.Canny(image,175,200)
  cv2.imwrite("edges.jpg", edges)
  binary = edges

  cv2.imwrite("binary.jpg", binary)
  contours,hierarchy = find_contours(binary)

  return get_rectangles(contours)

def find_contours(image):
  #return cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE);
  #return cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);
  return cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE);

def get_rectangles(contours):
  #remove_contours(contours, 100, 5000);
  rectangles = []
  for contour in contours:
    epsilon = 0.02*cv2.arcLength(contour,True)
    hull = cv2.convexHull(contour)
    approx = cv2.approxPolyDP(hull,epsilon,True)
    if (len(approx) == 4 and cv2.isContourConvex(approx)):
      rectangles.append(approx)

  return rectangles

def find_lines(img):
  edges = cv2.Canny(img,100,200)
  threshold = 90
  minLineLength = 10
  lines = cv2.HoughLinesP(edges, 1, cv2.CV_PI/180, threshold, 0, minLineLength, 20);
  #print lines
  for line in lines[0]:
    print line
    cv2.line(img, (line[0],line[1]), (line[2],line[3]), (0,255,0), 2)
  cv2.imwrite("line_edges.jpg", edges)
  cv2.imwrite("lines.jpg", img)

def find_keypoints(img):
  # Initiate FAST object with default values
  fast = cv2.FastFeatureDetector()

  # find and draw the keypoints
  kp = fast.detect(img,None)
  img2 = cv2.drawKeypoints(img, kp, color=(255,0,0))

  # Print all default params
  print "Threshold: ", fast.getInt('threshold')
  print "nonmaxSuppression: ", fast.getBool('nonmaxSuppression')
  #print "neighborhood: ", fast.getInt('type')
  print "Total Keypoints with nonmaxSuppression: ", len(kp)

  cv2.imwrite('fast_true.png',img2)

if __name__ == "__main__":
  image_1 = cv2.imread("../photos/GloryDays/3.jpg")

  #sample = cv2.imread("../photos/GloryDays/bib-sample.jpg")
  #orb = cv2.ORB();

  #find_lines(image_1)

  #find_keypoints(sample)

  #kp1,des1 = orb.detectAndCompute(image_1,None)
  #sample_w_kp = cv2.drawKeypoints(sample, kp1)
  #cv2.imwrite("kp.jpg", sample_w_kp);

  bib = find_bib(image_1)
  image_1 = cv2.imread("edges.jpg")

  x,y,w,h = cv2.boundingRect(bib)
  cv2.drawContours(image_1,[bib],-1,(0,0,255), 2)
  cv2.rectangle(image_1,(x,y),(x+w,y+h),(0,255,0),2)

  cv2.imwrite("out.jpg", image_1)

