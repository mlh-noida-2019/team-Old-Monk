# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import time
import serial
import io
arr = []
brr = []
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i1", "--image1", required=True,
				help="path to the input image1")
ap.add_argument("-i2", "--image2", required=True,
				help="path to the input image2")
args = vars(ap.parse_args())
# load the image, convert it to grayscale, and blur it slightly


def im(a):
	image = cv2.imread(args[a])
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imshow("Image1", gray)
	gray = cv2.GaussianBlur(gray, (7, 7), 0)
	cv2.imshow("Image2", gray)
	# perform edge detection, then perform a dilation + erosion to
	# close gaps in between object edges
	edged = cv2.Canny(gray, 50, 100)
	cv2.imshow("canny", edged)
	edged = cv2.dilate(edged, None, iterations=1)
	cv2.imshow("dilate", edged)
	edged = cv2.erode(edged, None, iterations=1)
	cv2.imshow("erode", edged)
	# find contours in the edge map
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
							cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# sort the contours from left-to-right and initialize the
	# 'pixels per metric' calibration variable
	(cnts, _) = contours.sort_contours(cnts)
	pixelsPerMetric = None
	# loop over the contours individually
	for c in cnts:
		# if the contour is not sufficiently large, ignore it
		if cv2.contourArea(c) < 100:
			continue

		# compute the rotated bounding box of the contour
		orig = image.copy()
		box = cv2.minAreaRect(c)
		box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
		box = np.array(box, dtype="int")

		# order the points in the contour such that they appear
		# in top-left, top-right, bottom-right, and bottom-left
		# order, then draw the outline of the rotated bounding
		# box
		box = perspective.order_points(box)
		cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

		# loop over the original points and draw them
		for (x, y) in box:
			cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

		# unpack the ordered bounding box, then compute the midpoint
		# between the top-left and top-right coordinates, followed by
		# the midpoint between bottom-left and bottom-right coordinates
		(tl, tr, br, bl) = box
		(tltrX, tltrY) = midpoint(tl, tr)
		(blbrX, blbrY) = midpoint(bl, br)

		# compute the midpoint between the top-left and top-right points,
		# followed by the midpoint between the top-righ and bottom-right
		(tlblX, tlblY) = midpoint(tl, bl)
		(trbrX, trbrY) = midpoint(tr, br)

		# draw the midpoints on the image
		cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
		cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

		# draw lines between the midpoints
		cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
				 (255, 0, 255), 2)
		cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
				 (255, 0, 255), 2)
		# compute the Euclidean distance between the midpoints
		dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
		dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
		#print("{:.1f}px".format(dA))
		#print("{:.1f}px".format(dB))
		arr.append(dA)
		arr.append(dB)
		brr.append(tltrX)
		brr.append(tltrY)
		brr.append(trbrX)
		brr.append(trbrY)
		break


im("image1")
im("image2")
xx = (arr[0]/arr[2])-1
#print(xx)
yy = 6/xx
print(yy)
dimA = (arr[0] / 812)*yy
dimB = (arr[1] / 812)*yy
image = cv2.imread("image1")
# draw the object sizes on the image
"""cv2.putText(image, "{:.1f}cm".format(dimA),
			(int(brr[0] - 15), int(brr[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (100, 100, 100), 2)
cv2.putText(image, "{:.1f}cm".format(dimB),
			(int(brr[2] + 10), int(brr[3])), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (100, 100, 100), 2)

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(1)
"""
qq=""+str(dimA)+"  "+str(dimB) +" "+str(yy)
print(dimA)
print(dimB)
print(qq)
ArduinoSerial = serial.Serial('/dev/ttyACM0',9600)
time.sleep(2)
sio=io.TextIOWrapper(io.BufferedRWPair(ArduinoSerial,ArduinoSerial))
sio.print(str(qq))
sio.flush()
sio.close
