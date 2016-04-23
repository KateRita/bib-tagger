import cv
import cv2

def find_bibs(image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
  binary = cv2.GaussianBlur(gray,(5,5),0)
  #ret,binary = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU);
  binary = cv2.adaptiveThreshold(binary, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
  #ret,binary = cv2.threshold(binary, 190, 255, cv2.THRESH_BINARY);

  #lapl = cv2.Laplacian(image,cv2.CV_64F)
  #gray = cv2.cvtColor(lapl, cv2.COLOR_BGR2GRAY);
  #blurred = cv2.GaussianBlur(lapl,(5,5),0)
  #ret,binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU);
  #cv2.imwrite("lapl.jpg", lapl)

  edges = cv2.Canny(image,175,200)
  cv2.imwrite("edges.jpg", edges)
  #binary = edges

  cv2.imwrite("binary.jpg", binary)
  contours,hierarchy = find_contours(binary)

  return get_corners(contours)

def find_contours(image):
  #return cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE);
  return cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);

def get_corners(contours):
  #remove_contours(contours, 100, 5000);
  corners = []
  for contour in contours:
    epsilon = 0.02*cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,epsilon,True)
    #print len(contour),len(approx)
    #if (len(approx) >= 4 and cv2.isContourConvex(approx)):
      #sort_rect_corners(approx)
      #corners.append(approx)
    corners.append(approx)

  return corners

def find_lines(img):
  edges = cv2.Canny(img,100,200)
  threshold = 90
  minLineLength = 10
  lines = cv2.HoughLinesP(edges, 1, cv.CV_PI/180, threshold, 0, minLineLength, 20);
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
  image_1 = cv2.imread("../photos/GloryDays/1.jpg")

  sample = cv2.imread("../photos/GloryDays/bib-sample.jpg")
  orb = cv2.ORB();

  find_lines(image_1)

  find_keypoints(sample)

  kp1,des1 = orb.detectAndCompute(image_1,None)
  sample_w_kp = cv2.drawKeypoints(sample, kp1)
  cv2.imwrite("kp.jpg", sample_w_kp);

  bibs = find_bibs(image_1)
  image_1 = cv2.imread("binary.jpg")

  for bib in bibs:
    x,y,w,h = cv2.boundingRect(bib)
    #print x,y,w,h
    cv2.rectangle(image_1,(x,y),(x+w,y+h),(0,255,0),2)

  cv2.imwrite("out.jpg", image_1)

