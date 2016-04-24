import cv2
import numpy as np

DEBUG=False

#
# Takes an input image which is assumed to only have one bib and returns the
# four corners of the bib in the form of an opencv contour (vector of points,
# i.e vector((x1,y1),(x2,y2),(x3,y3),(x4,y4)) )
#
def find_bib(image):
  width, height, depth = image.shape

  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
  #gray = cv2.equalizeHist(gray)
  blurred = cv2.GaussianBlur(gray,(5,5),0)

  debug_output("find_bib_blurred", blurred)
  #binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize=25, C=0);
  ret,binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU);
  #ret,binary = cv2.threshold(blurred, 170, 255, cv2.THRESH_BINARY);
  debug_output("find_bib_binary", binary)
  threshold_contours,hierarchy = find_contours(binary)

  debug_output("find_bib_threshold", binary)

  edges = cv2.Canny(gray,175,200, 3)
  edge_contours,hierarchy = find_contours(edges)

  debug_output("find_bib_edges", edges)

  contours = threshold_contours + edge_contours
  debug_output_contours("find_bib_threshold_contours", image, contours)

  rectangles = get_rectangles(contours)

  debug_output_contours("find_bib_rectangles", image, rectangles)

  potential_bibs = [rect for rect in rectangles if is_potential_bib(rect, width*height)]

  debug_output_contours("find_bib_potential_bibs", image, potential_bibs)

  ideal_aspect_ratio = 1.0
  potential_bibs = sorted(potential_bibs, key = lambda bib: abs(aspect_ratio(bib) - ideal_aspect_ratio))

  return potential_bibs[0] if len(potential_bibs) > 0 else np.array([[(0,0)],[(0,0)],[(0,0)],[(0,0)]])

#
# Checks that the size and aspect ratio of the contour is appropriate for a bib.
#
def is_potential_bib(rect, image_area):
  min_bib_size = image_area / 12;
  max_bib_size = image_area / 4;
  return (cv2.contourArea(rect) > min_bib_size and
          cv2.contourArea(rect) < max_bib_size and
          aspect_ratio(rect) > 0.75 and
          aspect_ratio(rect) < 2.5)

def aspect_ratio(rect):
  (x,y),(w,h),theta = cv2.minAreaRect(rect)
  return float(w) / float(h)

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
  rectangles = []
  for contour in contours:
    epsilon = 0.04*cv2.arcLength(contour,True)
    hull = cv2.convexHull(contour)
    approx = cv2.approxPolyDP(hull,epsilon,True)
    if (len(approx) == 4 and cv2.isContourConvex(approx)):
        rectangles.append(approx)

  return rectangles

def find_lines(img):
  edges = cv2.Canny(img,100,200)
  threshold = 60
  minLineLength = 10
  lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold, 0, minLineLength, 20);
  if (lines is None or len(lines) == 0):
      return

  #print lines
  for line in lines[0]:
    #print line
    cv2.line(img, (line[0],line[1]), (line[2],line[3]), (0,255,0), 2)
  cv2.imwrite("line_edges.jpg", edges)
  cv2.imwrite("lines.jpg", img)

def find_blobs(img):
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
     
    # Change thresholds
    params.minThreshold = 100;
    params.maxThreshold = 5000;
     
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 200
     
    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.785
     
    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.87
     
    # Filter by Inertia
    #params.filterByInertia = True
    #params.minInertiaRatio = 0.01

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector(params)
     
    # Detect blobs.
    keypoints = detector.detect(img)
    print keypoints
      
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]),
            (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite("blobs.jpg", im_with_keypoints);

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

def debug_output_contours(name, img, contours):
    if (DEBUG):
        tmp_img = np.copy(img)
        cv2.drawContours(tmp_img,contours,-1,(0,0,255), 2)
        debug_output(name, tmp_img)

def debug_output(name, img):
    if (DEBUG):
        cv2.imwrite(name + '.jpg', img)

if __name__ == "__main__":
  image_1 = cv2.imread("../photos-out/Frosty5k-1.jpg/subimage0.jpg")

  #sample = cv2.imread("../photos/GloryDays/bib-sample.jpg")
  #orb = cv2.ORB();

  #find_lines(image_1)

  #find_keypoints(sample)

  #kp1,des1 = orb.detectAndCompute(image_1,None)
  #sample_w_kp = cv2.drawKeypoints(sample, kp1)
  #cv2.imwrite("kp.jpg", sample_w_kp);

  bib = find_bib(image_1)

  cv2.drawContours(image_1,[bib],-1,(0,0,255), 2)
  x,y,w,h = cv2.boundingRect(bib)
  cv2.rectangle(image_1,(x,y),(x+w,y+h),(0,255,0),2)
  cv2.imwrite("out.jpg", image_1)

