import cv2
import numpy as np
cam = cv2.VideoCapture(1)

cv2.namedWindow("test")

img_counter = 0
kernel = np.ones((4,4), np.uint8)
while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)

    img_erosion = cv2.erode(frame, kernel, iterations=1) 
    cv2.imshow("test1", img_erosion)
    gradient = cv2.morphologyEx(frame, cv2.MORPH_GRADIENT, kernel)
    cv2.imshow("test2", gradient)    
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
